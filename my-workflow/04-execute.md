# Phase 3: EXECUTE — 编码 + Scope Guard + Delta 处理 + 内循环

## 目的

将 `tasks.json` 协议变成代码。这是唯一允许修改源代码的阶段。

核心挑战不是"怎么写代码"——agent 已经很擅长这个。核心挑战是：
1. **Scope Guard**：确保修改不超出 `allowed_paths` 声明的范围
2. **执行过程中需求/理解变化了怎么办**（Delta 处理）
3. **编译/测试失败怎么办**（Build-fix loop）
4. **并行执行时状态怎么隔离**（Slice + Wave + Worktree）
5. **角色边界**：Orchestrator 不写代码，Worker 不改目标

---

## Orchestrator / Worker 角色边界

在 Standard+ 的 EXECUTE 阶段，明确行为边界（不需要实现 dispatcher 进程，只需要行为约束）：

### Orchestrator 职责

```
✓ 分配 task 给 Worker
✓ 读取 verify-evidence
✓ 决定是否触发 delta re-entry
✓ 管理 slice/wave 编排 (Complex+)
✗ 不直接写业务代码
✗ 不修改 spec 的目标函数
✗ 不自行决定跳过 verify
```

### Worker 职责

```
✓ 执行单个 task
✓ 生成 verify-evidence
✓ 在 allowed_paths 范围内修改代码
✗ 不主动修改其他 task 的范围
✗ 不自行决定跳过 verify_cmd
✗ 不修改 Baseline Plan
```

---

## 内部步骤

```
[来自 Phase 2 的 Baseline Plan (tasks.json) + spec + slice/wave]
    │
    ▼
[Step 3.1] Pre-Execute 检查
    │   G11: State mutation boundary — 确认受保护文件列表
    │   加载 tasks.json + Baseline Plan
    │   Standard+: 加载 Anti-Rationalization 检查清单
    │   Complex+: 加载 slice.md，按 wave/DAG 分配 agent + context.jsonl
    │   Orchestrated: 创建 worktree (E1)
    │
    ▼
[Step 3.2] Task 执行循环 ──────────────────────────────────┐
    │   For each task (or wave of parallel tasks):          │
    │     a. Agent 读取 task (goal, allowed_paths, verify)  │
    │     b. Scope Guard: 限定修改范围 (Complex+)           │
    │     c. Agent 实现代码变更                               │
    │     d. Agent 运行 task 级验证 (compile, lint)          │
    │     e. 通过 → 输出 Completion Marker → 下一个 task     │
    │     f. 失败 → Build-fix loop (G5)                     │
    │                                                       │
    │   [G5: Build-Fix Loop]                                │
    │     compile/test 失败 → 修复 agent → 重试              │
    │     max 10 次 + stall detection                       │
    │     全部失败 → git reset task 变更 + Escalation        │
    │                                                       │
    ├── Task 完成 → 检查是否有 Delta ──────────────────────┤
    │                                                       │
    │   [Step 3.3] Delta 检测与处理                          │
    │     发现需求变化/理解修正/新增范围/超 allowed_paths？    │
    │     → 记录到 delta-log.jsonl                          │
    │     → [G6: Delta Re-entry Gate] 评估影响               │
    │       ├─ 不改主路径 → 追加 Delta，继续执行              │
    │       └─ 改了主路径/依赖/验收/超 allowed_paths          │
    │          → 生成 Effective View → 回 Phase 2            │
    │                                                       │
    └───────────────────────────────────────────────────────┘
    │
    ▼
[Step 3.4] Slice 闭包判断 (Complex+)
    │   检查 slice exit condition:
    │     - 所有 tasks 完成 → 继续 Phase 4
    │     - Handoff trigger 命中 → 产出 handoff.md → 结束当前 slice
    │
    ▼
[Step 3.5] 执行完成
    │   所有 tasks 完成（或部分完成 + delta 记录）
    │   → G7: 3-Layer Checkpoint
    │   → 进入 Phase 4
```

---

## Completion Markers

每个 task 完成后，agent 必须输出结构化标记（Orchestrator 通过 grep/regex 检测，不依赖自由文本）：

```
## TASK COMPLETE — task-001
## VERIFICATION PASSED — 3/3 tests
## ESCALATION NEEDED — {reason}
## BLOCKED — {reason}
## DONE_WITH_CONCERNS — {concern list}
```

**规则**：
- Agent 不能只说 "Done" 或 "Looks good"
- 标记必须包含具体 task id 或数据
- 无 Completion Marker → Orchestrator 不前进

---

## Anti-Rationalization 检查清单

在 EXECUTE 阶段注入（Standard+），封堵常见的跳步借口：

| 借口 | 反驳 |
|------|------|
| "This is just a simple string change" | 任何行为变更必须有对应 verify_cmd |
| "I already know what the code does" | 必须先完成 code-understanding（Standard+） |
| "Tests can be added later" | Plan 中标注了测试计划就必须执行 |
| "The plan needs a small adjustment" | 走 Delta 流程，不得静默修改 Baseline |
| "It looks correct to me" | 提供 verify-evidence，不接受主观断言 |

---

## Scope Guard（Complex+）

**机制**：PostToolUse hook 比对 Write/Edit 目标路径与当前 task 的 `allowed_paths` glob 模式。

**行为**：
- 匹配 → 允许
- 不匹配 → 自动触发 Delta Re-entry (G6)，记录为 `scope_change` delta

**Profile**：
- Complex+：硬检查，不匹配即触发 delta
- Standard：软提示，记录但不阻断
- Simple/Quick：不启用

---

## 输入产物

| 产物 | 来源 | 必需？ |
|------|------|--------|
| `tasks.json` (Baseline) | Phase 2 | Simple+ |
| `spec.md` | Phase 2 | Standard+ |
| `context.jsonl` | Phase 1 | Complex+ |
| `slice.md` | Phase 2 | Complex+ |
| `wave.json` | Phase 2 | Orchestrated |
| code-understanding.md | Phase 1 | 参考 |

## 输出产物

| 产物 | 类型 | 说明 |
|------|------|------|
| 源代码变更 | — | 实际代码 |
| `delta-log.jsonl` | Transient | 增量变更记录 |
| `effective-plan.md` | Transient (按需生成) | 当 delta 触发时 |
| `handoff.md` | Transient | Complex+ slice 结束时产出 |
| Completion Markers | 内嵌于 agent 输出 | Orchestrator 检测 |
| Checkpoint 状态 | Transient | G7 检查点输出 |

---

## Delta 处理模型

### 三层结构

```
Baseline Plan (不可变，Phase 2 锁定)
    ↓
Delta Log (append-only, 每条 delta 一个条目)
    ↓
Effective View (按需汇总，当前执行视图)
```

### Delta 条目 Schema

```json
{
  "delta_id": "D-003",
  "type": "scope_change | understanding_fix | bug_found | requirement_add",
  "reason": "发现模块 B 也需要修改",
  "impact": "影响范围新增 src/module-b/",
  "decision": "在 task-03 后追加 task-03b",
  "task_patch": { "add": ["task-03b"], "modify": [], "remove": [] },
  "status": "applied | pending_review"
}
```

### 路由规则

| 条件 | 动作 |
|------|------|
| 不改主路径、不改验收、不改依赖、不新增一级模块 | 只追加 Delta，继续执行 |
| 影响范围新增模块 / task 依赖变化 / 已确认决策被否定 | 生成 Effective View |
| 需求范围变化 / 架构决策变化 / 验收标准变化 | **回 Phase 2** 重入 Plan Gate |
| 修改超出 `allowed_paths` (Scope Guard) | 自动触发 Delta Re-entry |

---

## Slice 执行闭包（Complex+）

Complex+ 任务按 slice 组织执行。每个 slice 有明确的 entry/exit/handoff 条件。

### Handoff Trigger（满足任一则结束当前 slice）

- 完成一个独立 AC 集合
- 修改文件超出 allowed_paths
- 引入新设计决策（需回 Plan Gate）
- context 使用率 > 70% (DEGRADING)
- 出现 BLOCKED / DONE_WITH_CONCERNS

当 slice 结束且任务未全部完成时，产出 `handoff.md`（schema 见 [09-schemas.md](./09-schemas.md) §7）供下一 session Resume-Bootstrap。

---

## Gate 定义

### G5: Build-Fix Loop

| 属性 | 值 |
|------|-----|
| 类型 | Hard |
| 触发 | compile 或 test 失败 |
| 行为 | 启动修复 agent → 重新编译/测试 → 重试 |
| 上限 | 10 次（来自 yoyo-evolve） |
| Stall detection | 连续 2 次相同错误 → `escalation` |
| 全部失败 | `git reset --hard` task 变更 → 创建 issue → 跳过该 task |

### G6: Delta Re-entry Gate

| 属性 | 值 |
|------|-----|
| 类型 | Conditional |
| 触发 | Delta 记录后评估影响 / Scope Guard 不匹配 |
| 轻微 delta | 追加 log，继续 |
| 重大 delta | 回 Phase 2 |

### G7: 3-Layer Checkpoint

| 属性 | 值 |
|------|-----|
| 类型 | Hard |
| 触发 | 所有 tasks 执行完成 |
| Quick | lint + format（Quick/Simple） |
| Standard | Quick + unit tests（Standard） |
| Full | Standard + integration tests + coverage（Complex+） |
| 失败 | → 回 Build-fix loop（G5） |

### G11: State Mutation Boundary

| 属性 | 值 |
|------|-----|
| 类型 | Hard |
| 触发 | 任何 Write/Edit 操作 |
| 行为 | PostToolUse hook 检查目标文件是否在受保护列表中 |
| 受保护 | workflow 状态文件、Baseline Plan、reconcile-settlement.json |
| 违规 | `preflight` 阻断 + 警告 |

---

## Profile 行为矩阵

| Step | Quick | Simple | Standard | Complex | Orchestrated |
|------|---------|--------|----------|---------|---------|
| 3.1 Pre-execute | 无 | 加载 tasks.json | 加载 plan + anti-rat | DAG 分配 + context.jsonl | Worktree 创建 |
| 3.2 Task loop | 直接改 | 单步改 | 顺序执行 | Wave 并行 | Worktree 并行 |
| Scope Guard | 无 | 无 | 软提示 | ✅ 硬检查 | ✅ 硬检查 |
| Anti-Rationalization | 无 | 无 | ✅ 注入 | ✅ 注入 | ✅ 注入 |
| Completion Markers | 无 | 无 | ✅ 必须 | ✅ 必须 | ✅ 必须 |
| G5 Build-fix | max 3 | max 5 | max 10 | max 10 | max 10 + 外部模型修复 |
| 3.3 Delta | 无 | 无 | 追加模式 | 追加 + Effective View | 全量 Delta 管理 |
| 3.4 Slice 闭包 | 无 | 无 | 无 | ✅ slice exit check | ✅ slice + wave |
| G7 Checkpoint | Quick | Standard | Full | Full | Full + 人工预检 |
| 外部模型 | 无 | 无 | 无 | 可选 | ✅ 脏原型→重构 (E7) |

---

## 参考框架

| 机制 | 来源 | 如何使用 |
|------|------|---------|
| Delta 三层模型 | 真实场景 | 核心创新，直接采用 |
| Build-fix loop + stall detection | GSD `evolve.sh`, yoyo-evolve | max N + 连续相同错误检测 |
| Wave-based parallel | GSD executor | tasks 按 wave 分组并发 |
| DAG-ordered agents | ECC-Mobile | 按依赖图编排 |
| Worktree 隔离 | Superpowers, FlowSpec | 每个并行 agent 独立 worktree |
| Thin orchestrator | GSD, Trellis | orchestrator 只做路由+状态，不写代码 |
| Orchestrator/Worker 边界 | 11-Claude 建议 | 行为约束，非进程模型 |
| Scope Guard (allowed_paths) | 11-Claude + 12-Codex | PostToolUse hook 比对 |
| Anti-Rationalization | 13-Gemini（泛化） | 通用 EXECUTE 约束 |
| Completion markers | GSD agents | Agent 输出结构化标记 |
| Checkpoint-restart | yoyo-evolve | 超时 agent 的部分进度保存 |
| 脏原型重构 | CCG `execute.md` | 外部模型→Claude 审查→应用 |
| Protected files + git diff | yoyo-evolve `evolve.sh:1296` | 关键文件修改检测 |
| Slice / Handoff | PAUL 框架 | 执行闭包 + 跨 session 恢复 |

---

## Hooks

| Hook | 事件 | 行为 |
|------|------|------|
| `state-guard` | PostToolUse (Write/Edit) | 检查目标是否受保护文件 |
| `scope-guard` | PostToolUse (Write/Edit) | 比对路径与 allowed_paths (Complex+) |
| `build-check` | PostToolUse (Write .rs/.ts/.py) | 触发增量编译检查 |
| `delta-record` | 自定义 | 写入 delta-log.jsonl |
| `checkpoint` | Phase transition (P3→P4) | 运行 3-layer checkpoint |
| `completion-marker` | SubagentStop | 扫描 agent 输出中的 Completion Marker |

---

## 失败路径

| 场景 | Gate Taxonomy | 处理 |
|------|--------------|------|
| Build-fix 耗尽 10 次 | `abort` | git reset task 变更 → 创建 self-issue → 跳过该 task |
| Build-fix stall (连续相同错误) | `escalation` | 提前 escalate 给用户 |
| 所有 tasks 失败 | `abort` | 整个执行阶段回滚到 Phase 2，重新 plan |
| 并行 agent 之间文件冲突 | `revision` | Orchestrator 检测 → 串行化冲突 tasks |
| Delta 导致回 Phase 2 | `revision` | 保留已完成的 task 变更（git commit），只重新 plan 未完成部分 |
| 外部模型超时 | `revision` | 2 次重试 → 降级为 Claude-only |
| 上下文窗口 DEGRADING | `revision` | 写 checkpoint / handoff.md → 启动 fresh subagent 继续 |

---

## Open Questions

1. **Delta re-entry 的自动判断可靠吗？** "是否改了主路径"这个判断本身是 LLM 做的。Scope Guard 提供了一个 hard signal：超出 `allowed_paths` 即自动触发。但语义层面的判断仍依赖 LLM。
2. **并行 agent 的 STATE.md 写入冲突**：GSD 的方案是 orchestrator 独占写权限。但在 Claude Code 中，subagent 没有权限模型。考虑只用 append-only 日志（delta-log.jsonl）替代共享 state 文件？
3. **git reset 是否过于激进？** yoyo-evolve 对失败 task 做 `git reset --hard`。但如果 task 部分完成且有价值呢？考虑改为 `git stash` + 人工决定？
