# Ralph Orchestrator → Loaf 吸收计划

**Date**: 2026-04-12
**Source**: `docs/research/workflow-research-ralph-orchestrator.md`
**Target**: `1st-cc-plugin/workflows/loaf/` (v0.6.0)

---

## 已覆盖机制（无需迁移）

以下 ralph-orchestrator 机制已被 loaf 充分实现，仅作确认记录：

| Ralph 机制 | Loaf 等价实现 | 覆盖度 |
|-----------|-------------|--------|
| Backpressure gates (test/lint/typecheck) | P1 gate (187 tests) + verify_cmd + hooks | 完全覆盖 |
| Evaluator separation (Critic hat) | spec-reviewer + quality-reviewer + verifier agents | 完全覆盖 |
| Disk-as-state (memories/tasks on disk) | `.workflow/` 目录 + JSON schemas | 完全覆盖 |
| Step-Wave decomposition | tasks.json DAG + wave.json + orchestrator | 完全覆盖 |
| Evidence-before-claims (anti-rationalization) | anti-rationalization skill + SubagentStop hook | 完全覆盖 |
| Plan disposability | state.json + resume-pack + handoff | 部分覆盖（loaf 的 plan 更结构化，不如 ralph 那么"disposable"，但有 delta 机制补偿） |
| Parallel loops via worktrees | orchestrated profile: `isolation: worktree` | 完全覆盖 |
| LLM-as-judge | quality-reviewer spec_fit + quality_fit | 完全覆盖 |

---

## 可吸收机制

### 机制 1: Confidence-Based Decision Protocol

**原理**: 当 agent 遇到歧义时，用 0-100 分数量化置信度。>80 自主行动；50-80 行动但记录到 `decisions.md`；<50 选安全默认并记录。低置信度时有明确偏好序列：可逆 > 不可逆，增量 > 破坏，窄范围 > 宽范围，已有模式 > 新方案。

**Ralph 实现**: `presets/code-assist.yml` Builder/Critic hat 的 instructions 中内嵌 Confidence Protocol，decisions 记录到 `.ralph/agent/decisions.md`。

**Loaf 当前状态**: **部分有**。quality-reviewer 有 confidence-gated findings（suppress < 0.60），reflect skill 有 confidence score。但 **implementer 和 orchestrator 没有决策协议** — 它们遇到歧义时要么 BLOCKED 要么猜。

**为什么 Loaf 需要这个**:
- Implementer 的 build-fix loop 在第 3-10 次重试时经常做出低置信度决策（换方案 vs 继续修），没有记录机制
- Orchestrator 在 complex+ 遇到 delta 需求时的 re-entry 决策缺乏量化依据
- 当前的 BLOCKED 信号是二元的（pass/blocked），没有中间地带表达"我做了但不确定"

**实施步骤**:

1. **创建 `skills/confidence-protocol/SKILL.md`** (新 internal skill):
```yaml
---
name: confidence-protocol
description: "This skill should be used when agents encounter ambiguity during implementation. Provides a structured decision protocol with confidence scoring and audit trail."
---
```
内容要点：
- 定义 3 级置信度阈值（>80, 50-80, <50）
- 定义安全默认偏好序列
- 定义 decision log 格式（JSON，append 到 `.workflow/decisions.jsonl`）

2. **更新 `protocol/schemas/` 新增 `decisions.schema.json`**:
```json
{
  "type": "object",
  "required": ["id", "timestamp", "agent", "task_id", "confidence", "decision", "alternatives", "reversible"],
  "properties": {
    "id": { "type": "string", "pattern": "^DEC-\\d{3}$" },
    "confidence": { "type": "integer", "minimum": 0, "maximum": 100 },
    "reversible": { "type": "boolean" }
  }
}
```

3. **更新 `agents/implementer.md`**: 在 Process 步骤 7（On failure）和步骤 8（Build-fix loop）之间加入 Confidence Protocol 引用：
```markdown
## Decision Protocol
When encountering ambiguity (multiple fix approaches, unclear scope boundary):
1. Score confidence 0-100
2. >80: proceed autonomously
3. 50-80: proceed + append to `.workflow/decisions.jsonl`
4. <50: choose safest default + append + include in DONE_WITH_CONCERNS output
```

4. **更新 `agents/orchestrator.md`**: 在 Completion Detection 后加入同样的 Decision Protocol section，特别是 delta re-entry 决策。

5. **在 `plugin.json` 的 skills 中注册** `confidence-protocol`。

6. **在 `protocol/scripts/protected-files.json`** 中添加 `decisions.jsonl`。

**优先级**: P1 | **工作量**: S

---

### 机制 2: Token Budget Smart Zone

**原理**: 设定 context window 的最优使用区间（Ralph 称 "smart zone" = 40-60% of 176K）。超过上限触发 aggressive atomicity（强制拆小任务），超过阈值触发 handoff。

**Ralph 实现**: `CLAUDE.md:77` Tenet #1 + `hatless_ralph.rs:344-348` 仅注入 active hats instructions 减少 token 消耗。

**Loaf 当前状态**: **部分有**。loaf 的 evolution docs 引用了 PAUL 的 context quality degradation curve（50% 触发 aggressive atomicity, 70% 触发 resume-pack）。scope-tracker hook 异步跟踪 context health。但 **没有量化到具体 token 阈值，也没有自动触发机制**。

**为什么 Loaf 需要这个**:
- Complex+ 任务在 EXECUTE 阶段常因 context 膨胀导致 implementer 输出质量下降
- 当前 stall detection（2 次相同 stdout_hash）是 lagging indicator — context 压力是 leading indicator
- Orchestrator 需要提前知道何时触发 slice handoff 而非等到 stall

**实施步骤**:

1. **更新 `skills/config/SKILL.md`** 新增配置字段:
```yaml
context_budget:
  smart_zone_max: 0.60        # 超过此值 = aggressive atomicity
  handoff_threshold: 0.75     # 超过此值 = 强制 slice handoff
  monitor_interval: per_task  # 每个 task 完成后检查
```

2. **更新 `protocol/schemas/state.schema.json`** 的 `context_health` 字段：当前只有 `estimated_pct`，增加 `zone` enum：
```json
"zone": {
  "type": "string",
  "enum": ["green", "yellow", "red"],
  "description": "green: <smart_zone_max, yellow: smart_zone_max..handoff_threshold, red: >handoff_threshold"
}
```

3. **更新 `agents/orchestrator.md`** 的 Task Dispatch Protocol：在步骤 6（Wait for agent return）之后加入：
```markdown
## Context Budget Check (after each task)
1. Read state.json context_health.estimated_pct
2. If zone=yellow: warn, reduce remaining task complexity if possible
3. If zone=red: trigger slice handoff (complex+) or advance to VERIFY (standard)
```

4. **更新 `hooks/scope-tracker.sh`**: 在 context monitor 部分增加 zone 计算逻辑，写入 state.json。

5. **更新 `docs/design/cross-cutting.md`** 增加 Token Budget 小节。

**优先级**: P1 | **工作量**: M

---

### 机制 3: Replay-Based Integration Testing

**原理**: 录制完整 workflow session 的输入/输出为 JSONL fixture，回放时不调用真实 LLM API，实现确定性集成测试。

**Ralph 实现**: `--record-session session.jsonl` 录制，`smoke_runner` 回放。Fixtures 在 `crates/ralph-core/tests/fixtures/`。

**Loaf 当前状态**: **部分有**。P1 gate (187 tests) 测试 schema 校验和 state transitions。P2 E2E (107 tests) 测试 profile 流程。`smoke-test-harness.py` 模拟 state-op.py lifecycle。但 **所有测试都是 schema/script 级别 — 没有端到端 workflow session 的录制/回放**。

**为什么 Loaf 需要这个**:
- 当前无法测试 "skill prompt + agent prompt + hook 联合行为" 的集成正确性
- Schema 测试通过不代表真实 workflow 行为正确（类似 ralph 的 "mock tests passed but prod failed" 教训）
- 新版本发布前需要 regression 检测 skill prompt 变更对 workflow 行为的影响

**实施步骤**:

1. **创建 `protocol/scripts/record-workflow.py`**: 新脚本，wrap state-op.py 调用链，记录每步输入/输出到 `.workflow/session-recording.jsonl`：
```python
# 每条记录: {"step": N, "command": "...", "input": {...}, "output": {...}, "state_before": {...}, "state_after": {...}}
```

2. **创建 `protocol/scripts/replay-workflow.py`**: 回放脚本，读取 recording，逐步执行并对比 state 差异：
```python
# 对比: actual_state vs recorded_state → diff report
# 退出码: 0 = 所有步骤匹配, 1 = 有差异
```

3. **创建 `protocol/fixtures/recordings/` 目录**: 每个 profile 至少一个录制文件：
```
recordings/
├── quick-basic.jsonl
├── simple-two-tasks.jsonl
├── standard-happy-path.jsonl
├── complex-with-delta.jsonl
└── orchestrated-parallel.jsonl
```

4. **集成到 `protocol/scripts/run-p2-e2e.py`**: 新增 replay test category，在 P2 E2E 中执行。

5. **更新 `docs/next-steps.md`**: 标记 replay testing 已实现。

**优先级**: P2 | **工作量**: L

---

### 机制 4: Explicit Anti-Pattern Documentation

**原理**: 在框架指导文件中明确列出 **不应该做什么** 及原因，与"应该做什么"同等重要。

**Ralph 实现**: `CLAUDE.md:89-95` 列出 5 条 Anti-Patterns，每条带解释：
- ❌ Building features into the orchestrator that agents can handle
- ❌ Complex retry logic (fresh context handles recovery)
- ❌ Detailed step-by-step instructions (use backpressure instead)
- ❌ Scoping work at task selection time (scope at plan creation instead)
- ❌ Assuming functionality is missing without code verification

**Loaf 当前状态**: **缺失**。各 agent 有 "Anti-Patterns (MUST NOT)" section（如 implementer.md:68-74），但 **框架级别没有统一的 anti-pattern 清单**。设计哲学散布在 evolution docs 中，不集中。

**为什么 Loaf 需要这个**:
- 新贡献者（或新 session 的 Claude）不知道 loaf 的设计禁区
- Anti-patterns 是从失败中学到的——比正面指令更高效地避免重复犯错
- Agent-level MUST NOT 是战术的，缺少战略层的 "loaf 框架不做什么"

**实施步骤**:

1. **在 `README.md` 中新增 `## Anti-Patterns` section**（在现有 Profile 表格之后）:
```markdown
## Anti-Patterns

- ❌ 在 orchestrator 中写业务代码（orchestrator 只调度，implementer 执行）
- ❌ 跳过 verify_cmd 声称"看起来正确"（evidence-before-claims 是核心纪律）
- ❌ 在 EXECUTE 阶段修改 spec（走 delta 流程，不直接改）
- ❌ 用 complex profile 处理 quick-fix 级任务（过度编排的成本 > 收益）
- ❌ 信任 agent 自述而非 verify-evidence.jsonl（SubagentStop hook 存在的原因）
- ❌ 手动编辑 protocol 文件（state.json, tasks.json 由 state-op.py 管理）
```

2. **各 agent `.md` 文件的 Anti-Patterns section 保持不变**（战术级），README 的是战略级补充。

**优先级**: P0 | **工作量**: S

---

### 机制 5: Default-to-Failure-Path Semantics

**原理**: 当 agent 没有明确发出成功信号时，系统默认走失败/拒绝路径。Ralph 的 Critic hat `default_publishes: review.rejected`，Finalizer `default_publishes: finalization.failed`。

**Ralph 实现**: preset YAML 中每个 hat 有 `default_publishes` 字段，EventLoop 在 hat 未显式 publish 时使用此默认值。

**Loaf 当前状态**: **部分有**。SubagentStop hook (Ralph Loop G8) 要求 evidence 才能退出。但 **implementer 的默认状态是"什么都没发生"而非"失败"** — 如果 implementer 超时或崩溃，orchestrator 不一定能检测到。

**为什么 Loaf 需要这个**:
- Implementer 在 build-fix loop 第 10 次后 exit 但未输出 BLOCKED marker 的边缘情况
- Quality-reviewer 如果未产出 verify-review.json 就退出，orchestrator 可能误认为 "review passed"
- 偏向安全比偏向乐观更适合自动化编排

**实施步骤**:

1. **更新 `agents/orchestrator.md`** 的 Completion Detection section，增加 timeout/default 逻辑:
```markdown
## Default-to-Failure Semantics
If implementer returns without a recognized marker (TASK COMPLETE, BLOCKED, DONE_WITH_CONCERNS):
- Treat as BLOCKED with reason "no_completion_marker"
- Record in event-log.jsonl
- Do NOT advance to next task
```

2. **更新 `agents/quality-reviewer.md`** 增加类似语义: 未产出 verify-review.json → 视为 review failed。

3. **更新 `docs/design/spec-gates.md`** 的 gate failure taxonomy 加入 "implicit failure (no output)" 类型。

**优先级**: P1 | **工作量**: S

---

### 机制 6: Hat Topology Token 优化（Prompt 分层注入）

**原理**: 多角色系统中，只向当前活跃角色注入完整 instructions，其他角色仅显示名称和职责摘要。减少 token 消耗，保持在 smart zone。

**Ralph 实现**: `hatless_ralph.rs:344-348` — active hats 注入 full instructions，非活跃 hats 仅 topology table (name + triggers + publishes)。

**Loaf 当前状态**: **不适用于 agent 架构**。Loaf 用独立 subagent（每个 agent.md 是独立进程），不在同一 prompt 中混入多角色 instructions。但 **loaf 的 command skills（start, standard, complex 等）会在主对话中加载较多上下文**。

**为什么 Loaf 需要这个**:
- `/loaf:standard` 等 command skill 会加载完整 skill 内容 + references — 如果同时 load 多个 skill 可能膨胀
- Orchestrator agent 的 prompt 包含 task dispatch protocol + wave merge protocol + completion detection — 对简单 standard profile 有冗余

**实施步骤**:

1. **审计当前 skill token 消耗**: 运行 `validate-plugin.py` 检查每个 skill 的 token count。

2. **对超过 3k tokens 的 skills**: 将细节移到 `references/`，主 SKILL.md 保留核心逻辑，reference 按需加载。

3. **对 orchestrator.md**: 将 Complex+ 特有内容（slice handoff, wave merge）移到条件段：
```markdown
## Complex+ Only (skip for standard)
{slice/wave details}
```
使 standard profile 调度时 orchestrator 可以指示跳过无关段落。

**优先级**: P2 | **工作量**: M

---

## 实施路线图

| Phase | 机制 | Priority | Effort | 前置依赖 |
|-------|------|----------|--------|----------|
| **Phase 1** | #4 Anti-Pattern Documentation | P0 | S | 无 |
| **Phase 2a** | #1 Confidence Decision Protocol | P1 | S | 需先确定 decisions.jsonl schema |
| **Phase 2b** | #5 Default-to-Failure Semantics | P1 | S | 无 |
| **Phase 2c** | #2 Token Budget Smart Zone | P1 | M | 需更新 state.schema.json + scope-tracker hook |
| **Phase 3a** | #3 Replay-Based Integration Testing | P2 | L | 需 P1/P2 E2E 框架稳定 |
| **Phase 3b** | #6 Prompt 分层注入 | P2 | M | 需 skill token audit |

**总工作量**: 2S + 2M + 1L = 约 3-5 个实现 session

---

## 不采纳的机制（附理由）

| Ralph 机制 | 为何不采纳 | Loaf 替代方案 |
|-----------|-----------|-------------|
| Hat-based event routing | 需要运行时 EventBus，loaf 用 subagent + state.json 已解耦 | Orchestrator task dispatch via Agent tool |
| Telegram RObot (human-in-loop) | 外部依赖重，loaf 的 AskUserQuestion + delta flow 已覆盖 | AskUserQuestion + 3-way human acceptance (G4) |
| Session recording via CLI flag | 需要 CLI 二进制，loaf 是纯 prompt/script 框架 | state-op.py event-log + replay-workflow.py (机制 #3) |
| Web Dashboard | 超出 Claude Code plugin 范畴 | `/loaf:status` command + statusline hook |
| Multi-backend adapters (Kiro/Gemini/Codex) | loaf 运行在 Claude Code 内，单一后端 | 不需要 |
