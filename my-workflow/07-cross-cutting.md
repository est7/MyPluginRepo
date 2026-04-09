# Cross-Cutting Mechanisms — 状态管理 / Gate Taxonomy / Resume / 可观测 / 安全 / Hooks / Config

## 目的

定义贯穿所有 Phase 的横切关注点。这些不属于某个特定阶段，而是工作流引擎层面的基础设施。

---

## 1. 状态管理

### 1.1 任务状态机

```
TRIAGE → DISCOVER → SPEC_PLAN → EXECUTE → VERIFY → SETTLE → DONE
                                    ↑           │
                                    └── delta ───┘ (re-entry via G6)
```

每个状态转换必须经过对应的 gate。不允许跳跃（但允许透传/降级）。

### 1.2 State Mutation Boundary (G11)

**问题**：如果 agent 直接 Write/Edit 状态文件，状态会不一致。

**方案（轻量版，非 CLI）**：

```
受保护文件列表：
- .workflow/state.json              (当前任务状态)
- .workflow/reconcile-settlement.json (结算结果)
- .workflow/tasks.json               (Baseline Plan，Phase 2 锁定后禁写)
- docs/architecture.md               (durable，仅 Phase 5 backflow)
- docs/interfaces.md                 (durable，仅 Phase 5 backflow)
- docs/invariants.md                 (durable，仅 Phase 5 backflow)

执行方式：
- PostToolUse hook 检测 Write/Edit 目标路径
- 命中受保护文件 → 阻断 + 警告
- Agent 必须通过 workflow 命令间接修改（如 /workflow advance, /workflow settle）
```

**演进路径**：早期用 hook + protected list；需求增长后可升级为确定性 CLI 工具。

### 1.3 .workflow/ 目录结构

```
.workflow/
├── state.json                  # 当前任务状态 (phase, profile, gates_passed)
├── triage-result.json          # Phase 0 输出
├── code-understanding.md       # Phase 1 输出 (transient)
├── context.jsonl               # Phase 1 输出 (Complex+, transient)
├── spec.md                     # Phase 2 输出 (transient)
├── tasks.json                  # Phase 2 输出 (transient, Baseline 锁定后 protected)
├── slice.md                    # Phase 2 输出 (Complex+, transient)
├── wave.json                   # Phase 2 输出 (Orchestrated, transient)
├── delta-log.jsonl             # Phase 3 输出 (append-only)
├── effective-plan.md           # Phase 3 按需生成 (transient)
├── handoff.md                  # Phase 3/4 输出 (Complex+ 跨 session)
├── verify-evidence.json        # Phase 4 输出 (transient)
├── verify-review.json          # Phase 4 输出 (transient)
├── reconcile-settlement.json   # Phase 5 输出 (durable)
├── event-log.jsonl             # 全生命周期事件日志 (append-only)
└── .archive/                   # 归档的 transient 产物
    └── {task-id}/
```

---

## 2. Gate Taxonomy — 统一失败路由

所有 gate 失败统一分为 4 类（定义见 [00-overview.md](./00-overview.md)）：

| 类型 | 含义 | 处理 |
|------|------|------|
| `preflight` | 前置条件不满足 | 阻断，不允许进入下一步 |
| `revision` | 可修复的问题 | 打回生产者，bounded loop (max N + stall detection) |
| `escalation` | 需要用户决策 | 暂停，呈现给用户 |
| `abort` | 继续执行会扩大损害 | 立即停止，回滚 |

### Stall Detection

所有 `revision` 类 loop 增加 stall detection：

- 连续 2 次 revision 错误描述相同（或 issue count 不减）→ 自动升级为 `escalation`
- 适用于：G2 Plan Review、G5 Build-Fix、G8 Ralph Loop
- 避免 agent 陷入无意义的修复循环

### Anti-Rationalization 检查清单

在 EXECUTE 阶段注入（Standard+），封堵常见的跳步借口：

| 借口 | 反驳 |
|------|------|
| "This is just a simple string change" | 任何行为变更必须有对应 verify_cmd |
| "I already know what the code does" | 必须先完成 code-understanding（Standard+） |
| "Tests can be added later" | Plan 中标注了测试计划就必须执行 |
| "The plan needs a small adjustment" | 走 Delta 流程，不得静默修改 Baseline |
| "It looks correct to me" | 提供 verify-evidence，不接受主观断言 |

---

## 3. Resume-Bootstrap 协议

### 3.1 暂停

任何时候用户可以中断。`.workflow/state.json` 记录当前 phase + 最后 gate 状态 + 已产出产物列表。

### 3.2 恢复

- `--from-phase=N` → 从指定 phase 恢复
- `--resume` → 从上次暂停点继续
- 恢复时按固定加载顺序重建上下文

### 3.3 Resume 固定加载顺序

```
1. state.json           → 恢复到正确 phase + profile
2. Durable docs         → architecture + invariants + 近期 lessons
3. handoff.md (如存在)  → 跨 session 恢复载体（确定性 resume）
4. tasks.json (Baseline) → 执行计划
5. delta-log.jsonl       → 增量变更记录
6. 当前 phase 的 transient 产物 → 执行上下文
```

**关键约束**：不依赖对话历史。`handoff.md` 提供完整的恢复上下文，新 session 的 agent 可以从零开始理解任务状态。

### 3.4 handoff.md（Complex+ 跨 session）

当 slice 结束且任务未全部完成时，产出 `handoff.md`（schema 见 [09-schemas.md §7](./09-schemas.md)）。

**Handoff 触发条件**（满足任一）：
- 完成一个独立 AC 集合
- 修改文件超出 allowed_paths
- 引入新设计决策（需回 Plan Gate）
- context 使用率 > 70% (DEGRADING)
- 出现 BLOCKED / DONE_WITH_CONCERNS

**参考**：OpenSpec 的"中断一个变更，处理另一个后再回来" + ECC-Mobile 的 `--from-phase=N` + PAUL 的 slice/handoff 模型。

---

## 4. 可观测性

### 4.1 Event Log (H4)

所有阶段转换和关键操作记录到 `event-log.jsonl`：

```json
{
  "ts": "2026-04-08T10:23:00Z",
  "event": "phase_transition",
  "from": "DISCOVER",
  "to": "SPEC_PLAN",
  "gate": "G1_understanding_confirm",
  "result": "pass",
  "duration_ms": 45000
}
```

事件类型：
- `phase_transition` — 阶段转换
- `gate_result` — gate 通过/失败（含 Gate Taxonomy 类型）
- `delta_recorded` — delta 追加
- `build_fix_attempt` — 编译修复尝试
- `stall_detected` — stall detection 触发
- `escalation` — 升级给用户
- `task_complete` — 单个 task 完成（含 Completion Marker）
- `session_start` / `session_end` — 会话边界

### 4.2 Context Window Monitor (H2)

| 阈值 | 级别 | 行为 |
|------|------|------|
| 0-50% | PEAK | 正常 |
| 50-70% | GOOD | 正常 |
| 70-85% | DEGRADING | 警告，建议写 checkpoint / handoff |
| 85%+ | CRITICAL | 强制写 checkpoint → fresh subagent |

**实现**：PostToolUse hook 注入 context 使用率估算。来自 GSD `gsd-context-monitor.js`。

### 4.3 StatusLine (H3)

状态栏显示：`[Phase] [Task N/M] [Context: XX%] [Profile: standard]`

**实现**：StatusLine hook。来自 Trellis `statusline.py`。

### 4.4 Completion Markers (H5)

每个 agent（尤其是 subagent）输出特定标记表示完成（schema 见 [09-schemas.md §10](./09-schemas.md)）：

```
## TASK COMPLETE — task-03
## VERIFICATION PASSED — 3/3 tests
## PLANNING COMPLETE
## ESCALATION NEEDED — {reason}
## BLOCKED — {reason}
## DONE_WITH_CONCERNS — {concern list}
```

Orchestrator 通过 grep/regex 检测这些标记判断 agent 状态，而不依赖 agent 的自由文本声称。

**规则**：
- Agent 不能只说 "Done" 或 "Looks good"
- 标记必须包含具体 task id 或数据
- 无 Completion Marker → Orchestrator 不前进

---

## 5. 安全

### 5.1 Prompt Injection 防御 (G10, K1, K5)

三层防御：

| 层 | 机制 | 来源 |
|----|------|------|
| **Boundary Nonce** | 外部内容用随机 nonce 标记边界 | yoyo-evolve |
| **Pattern Scan** | grep 已知 injection 模式 | GSD `prompt-injection-scan.sh` |
| **Content Isolation** | 外部内容不直接注入 prompt，先经过清洗 | 通用最佳实践 |

### 5.2 Protected Files (K2)

| 文件 | 保护级别 | 说明 |
|------|---------|------|
| `.workflow/state.json` | Hard — 禁止 agent 直接写 | 状态文件 |
| `.workflow/tasks.json` | Hard — Phase 2 锁定后禁写 | Baseline Plan |
| `.workflow/reconcile-settlement.json` | Hard — 只有 Phase 5 可写 | 结算 |
| `docs/architecture.md` | Soft — 仅允许 Phase 5 backflow 更新 | Durable |
| `docs/invariants.md` | Soft — 仅允许 Phase 5 backflow 更新 | Durable |

**实现**：PostToolUse hook + 文件路径匹配 + 当前 phase 检查。

### 5.3 Deny-First Permission (K3)

```json
{
  "deny": ["Write(.workflow/state.json)", "Write(.workflow/tasks.json)"],
  "allow": ["Read(*)", "Write(src/*)"]
}
```

Deny 列表优先于 allow。来自 yoyo-evolve 的 deny-first 模型。

### 5.4 Sensitive File Access (K4)

```json
{
  "deny_read": [".env", "secrets/*", "credentials.*", ".workflow/reconcile-settlement.json (非 Phase 5)"]
}
```

---

## 6. Hooks 总览

### 6.1 按事件分类

| 事件 | Hooks | Phase |
|------|-------|-------|
| **SessionStart** | durable-docs-loader, state-restore, statusline-init | P0 |
| **PreToolUse** | injection-scan (Read external), commit-validate (git commit), state-guard (Write protected) | All |
| **PostToolUse** | context-monitor, build-check (Write .rs/.ts/.py), scope-guard (Write vs allowed_paths), state-guard | All |
| **SubagentStop** | ralph-loop (verify-evidence 检测), completion-marker (扫描 Completion Markers) | P3, P4 |
| **PreCompact** | checkpoint-save (保存当前产物状态) | All |
| **Stop** | session-evaluation (Complex+), event-log-close | P5 / 会话结束 |

### 6.2 Hook 执行保障

| 约束 | 机制 | 来源 |
|------|------|------|
| Hook 超时 | 5s 硬超时 (SIGTERM → SIGKILL) | yoyo-evolve `hooks.rs` |
| Hook 失败不阻断主流程 | 除显式标记为 Hard 的 gate | 通用 |
| Hook 路径安全 | 禁止 `..` 和绝对路径 | FlowSpec `hooks/config.py` |

### 6.3 Hook → Gate 映射

| Hook | Gate | 类型 |
|------|------|------|
| `state-guard` | G11: State Mutation Boundary | Hard |
| `scope-guard` | Scope Guard (Complex+) | Hard (Complex+) / Soft (Standard) |
| `ralph-loop` | G8: Ralph Loop | Hard (Standard+) |
| `commit-validate` | Conventional Commits | Hard |
| `completion-marker` | Completion Marker detection | Hard (Standard+) |
| `injection-scan` | G10: Prompt Injection Scan | Hard |
| `settlement-validate` | Settlement Validation | Hard (Standard+) |

---

## 7. Config 系统

### 7.1 三层配置

| 层 | 位置 | 优先级 | 说明 |
|----|------|--------|------|
| **项目级** | `.claude/workflow.local.md` (YAML frontmatter) | 低 | 项目默认值 |
| **会话级** | 显式命令参数 (`/complex --skip-research`) | 中 | 单次会话覆盖 |
| **对话级** | 用户口头指令 ("这次跳过 TDD") | 高 | 即时覆盖 |

### 7.2 项目级配置 Schema

```yaml
---
workflow:
  default_profile: standard
  scorer:
    require_confirmation: true
    fallback_profile: standard

  # Phase 级开关
  discover:
    research: auto          # auto | always | never
    code_understanding: auto
  spec_plan:
    adr: auto               # auto | always | never
    plan_checker: auto
    bdd_scenarios: auto
  execute:
    parallel_agents: auto
    worktree_isolation: auto
    external_models: never   # never | auto | always
    delta_management: auto
    scope_guard: auto
    anti_rationalization: auto
  verify:
    tdd: auto
    pass_at_k: never
    review_agent: auto
    rubric_evaluator: never
    ralph_loop: auto
    spec_fit: auto
    quality_fit: auto
  settle:
    backflow: auto
    lessons_synthesis: auto
    minimum_closure: auto

  # 受保护文件（追加到默认列表）
  protected_files:
    - "src/core/auth/**"
    - "database/migrations/**"
---
```

### 7.3 auto 的含义

`auto` = 根据 profile 决定：
- Quick/Simple → 关闭
- Standard → 按需（gate 判断）
- Complex+ → 开启

这实现了"profile 只做减法"：默认 auto 跟随 profile，用户可以显式 override 为 `always` 或 `never`。

---

## 8. 文档分层总览

| 层 | 产物 | 生命周期 | 后续任务可见？ |
|----|------|---------|--------------|
| **Transient** | spec, tasks.json, code-understanding, context.jsonl, delta-log, verify-evidence, verify-review, slice.md, wave.json | Phase 2-5 | ❌ 归档后不可见 |
| **Decision** | ADR | 永久 | ✅ 按需加载 |
| **Durable** | architecture, interfaces, invariants, lessons, reconcile-settlement | 永久 | ✅ 默认加载 |
| **Archive** | .archive/{task-id}/ | 永久存储 | ❌ 仅显式追溯 |
| **Observable** | event-log.jsonl | 永久 | ✅ 可查询 |

---

## Open Questions (跨阶段)

1. **`.workflow/` 目录是否 gitignore？** Transient 产物不应进入 git，但 reconcile-settlement.json 和 durable docs 应该。考虑 `.workflow/` gitignore + durable docs 在 `docs/` 下（已在 git 中）。
2. **多任务并发**：如果同时有两个任务在跑（不同 worktree），`.workflow/state.json` 会冲突。考虑 `.workflow/{task-id}/state.json` 命名空间隔离？
3. **Config hot-reload**：用户修改 `workflow.local.md` 后，正在运行的任务是否立即生效？建议：Phase 切换时重新读取。
4. **Deterministic state ops 的演进路径**：当前用 hook 实现。如果未来 hook 不够（比如需要原子性 state transition），再升级为 CLI 工具。判断标准：当出现 state corruption 事件时再升级。
