# Phase 3: EXECUTE — 编码 + Delta 处理 + 内循环

## 目的

将 Plan 变成代码。这是唯一允许修改源代码的阶段。

核心挑战不是"怎么写代码"——agent 已经很擅长这个。核心挑战是：
1. **执行过程中需求/理解变化了怎么办**（Delta 处理）
2. **编译/测试失败怎么办**（Build-fix loop）
3. **并行执行时状态怎么隔离**（Worktree + DAG）

---

## 内部步骤

```
[来自 Phase 2 的 Baseline Plan + tasks]
    │
    ▼
[Step 3.1] Pre-Execute 检查
    │   G11: State mutation boundary — 确认受保护文件列表
    │   加载 Baseline Plan + tasks
    │   Complex+: 按 wave/DAG 分配 agent
    │   Harness: 创建 worktree (E1)
    │
    ▼
[Step 3.2] Task 执行循环 ──────────────────────────────────┐
    │   For each task (or wave of parallel tasks):          │
    │     a. Agent 读取 task spec (files, action, verify)   │
    │     b. Agent 实现代码变更                               │
    │     c. Agent 运行 task 级验证 (compile, lint)          │
    │     d. 通过 → 下一个 task                              │
    │     e. 失败 → Build-fix loop (G5)                     │
    │                                                       │
    │   [G5: Build-Fix Loop]                                │
    │     compile/test 失败 → 修复 agent → 重试              │
    │     max 10 次 + stall detection                       │
    │     全部失败 → git reset task 变更 + Escalation        │
    │                                                       │
    ├── Task 完成 → 检查是否有 Delta ──────────────────────┤
    │                                                       │
    │   [Step 3.3] Delta 检测与处理                          │
    │     发现需求变化/理解修正/新增范围？                     │
    │     → 记录到 delta-log.jsonl                          │
    │     → [G6: Delta Re-entry Gate] 评估影响               │
    │       ├─ 不改主路径 → 追加 Delta，继续执行              │
    │       └─ 改了主路径/依赖/验收 → 生成 Effective View     │
    │          → 回 Phase 2 重入 Plan Gate                   │
    │                                                       │
    └───────────────────────────────────────────────────────┘
    │
    ▼
[Step 3.4] 执行完成
    │   所有 tasks 完成（或部分完成 + delta 记录）
    │   → G7: 3-Layer Checkpoint
    │   → 进入 Phase 4
```

---

## 输入产物

| 产物 | 来源 | 必需？ |
|------|------|--------|
| Baseline Plan (`plan.md`) | Phase 2 | Moderate+ |
| Task list (`tasks.md` / `plan.json`) | Phase 2 | Moderate+ |
| Execution contract | Phase 2 (Harness only) | Harness |
| code-understanding.md | Phase 1 | 参考 |

## 输出产物

| 产物 | 类型 | 说明 |
|------|------|------|
| 源代码变更 | — | 实际代码 |
| `delta-log.jsonl` | Transient | 增量变更记录 |
| `effective-plan.md` | Transient (按需生成) | 当 delta 触发时 |
| Checkpoint 状态 | Transient | G7 检查点输出 |

---

## Delta 处理模型（来自真实场景，核心创新）

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

---

## Gate 定义

### G5: Build-Fix Loop

| 属性 | 值 |
|------|-----|
| 类型 | Hard |
| 触发 | compile 或 test 失败 |
| 行为 | 启动修复 agent → 重新编译/测试 → 重试 |
| 上限 | 10 次（来自 yoyo-evolve） |
| Stall detection | 连续 2 次相同错误 → 提前 escalate |
| 全部失败 | `git reset --hard` task 变更 → 创建 issue → 跳过该 task |

### G6: Delta Re-entry Gate

| 属性 | 值 |
|------|-----|
| 类型 | Conditional |
| 触发 | Delta 记录后评估影响 |
| 轻微 delta | 追加 log，继续 |
| 重大 delta | 回 Phase 2 |

### G7: 3-Layer Checkpoint

| 属性 | 值 |
|------|-----|
| 类型 | Hard |
| 触发 | 所有 tasks 执行完成 |
| Quick | lint + format（Trivial/Simple） |
| Standard | Quick + unit tests（Moderate） |
| Full | Standard + integration tests + coverage（Complex+） |
| 失败 | → 回 Build-fix loop（G5） |

### G11: State Mutation Boundary

| 属性 | 值 |
|------|-----|
| 类型 | Hard |
| 触发 | 任何 Write/Edit 操作 |
| 行为 | PostToolUse hook 检查目标文件是否在受保护列表中 |
| 受保护 | workflow 状态文件、Baseline Plan、settlement.json |
| 违规 | **阻断** + 警告 |

---

## Profile 行为矩阵

| Step | Trivial | Simple | Moderate | Complex | Harness |
|------|---------|--------|----------|---------|---------|
| 3.1 Pre-execute | 无 | 无 | 加载 plan | DAG 分配 | Worktree 创建 |
| 3.2 Task loop | 直接改 | 单步改 | 顺序执行 | Wave 并行 | Worktree 并行 |
| G5 Build-fix | max 3 | max 5 | max 10 | max 10 | max 10 + 外部模型修复 |
| 3.3 Delta | 无 | 无 | 追加模式 | 追加 + Effective View | 全量 Delta 管理 |
| G7 Checkpoint | Quick | Standard | Full | Full | Full + 人工预检 |
| 外部模型 | 无 | 无 | 无 | 可选 | ✅ 脏原型→重构 (E7) |

---

## 参考框架

| 机制 | 来源 | 如何使用 |
|------|------|---------|
| Delta 三层模型 | 真实场景 `真实场景.md` | 核心创新，直接采用 |
| Build-fix loop + stall detection | GSD `evolve.sh`, yoyo-evolve | max N + 连续相同错误检测 |
| Wave-based parallel | GSD executor | tasks 按 wave 分组并发 |
| DAG-ordered agents | ECC-Mobile | 按依赖图编排 |
| Worktree 隔离 | Superpowers, FlowSpec | 每个并行 agent 独立 worktree |
| Thin orchestrator | GSD | orchestrator 只做路由+状态，不写代码 |
| Checkpoint-restart | yoyo-evolve | 超时 agent 的部分进度保存 |
| 脏原型重构 | CCG `execute.md` | 外部模型→Claude审查→应用 |
| Protected files + git diff | yoyo-evolve `evolve.sh:1296` | 关键文件修改检测 |
| Completion markers | GSD agents | Agent 输出 `## TASK COMPLETE` |

---

## Hooks

| Hook | 事件 | 行为 |
|------|------|------|
| `state-guard` | PostToolUse (Write/Edit) | 检查目标是否受保护文件 |
| `build-check` | PostToolUse (Write .rs/.ts/.py) | 触发增量编译检查 |
| `delta-record` | 自定义 | 写入 delta-log.jsonl |
| `checkpoint` | Phase transition (P3→P4) | 运行 3-layer checkpoint |

---

## 失败路径

| 场景 | 处理 |
|------|------|
| Build-fix 耗尽 10 次 | git reset task 变更 → 创建 self-issue → 跳过该 task → 继续 |
| 所有 tasks 失败 | → Abort: 整个执行阶段回滚到 Phase 2，重新 plan |
| 并行 agent 之间文件冲突 | → Orchestrator 检测 → 串行化冲突 tasks |
| Delta 导致回 Phase 2 | 保留已完成的 task 变更（git commit），只重新 plan 未完成部分 |
| 外部模型超时 | 2 次重试 → 降级为 Claude-only（不用外部模型） |
| 上下文窗口 DEGRADING | 写 checkpoint → 启动 fresh subagent 继续 |

---

## Open Questions

1. **Delta re-entry 的自动判断可靠吗？** "是否改了主路径"这个判断本身是 LLM 做的。考虑加一个 hard signal：如果 delta 修改了 Baseline Plan 中 `## 影响范围` 列出的文件之外的文件 → 自动触发 Effective View 生成。
2. **并行 agent 的 STATE.md 写入冲突**：GSD 的方案是 orchestrator 独占写权限。但在 Claude Code 中，subagent 没有权限模型。考虑只用 append-only 日志（delta-log.jsonl）替代共享 state 文件？
3. **git reset 是否过于激进？** yoyo-evolve 对失败 task 做 `git reset --hard`。但如果 task 部分完成且有价值呢？考虑改为 `git stash` + 人工决定？
