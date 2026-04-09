# Protocol Schemas — 协议 Schema 集中定义

> 所有 machine-checkable 协议的权威定义。各 phase 文档引用本文件，不重复定义。

---

## 1. tasks.json

**产出于**：Phase 2 (SPEC & PLAN)
**消费于**：Phase 3 (EXECUTE)、Phase 4 (VERIFY)、Phase 5 (SETTLE)
**类型**：Transient

### 完整 Schema

```json
{
  "tasks": [
    {
      "id": "task-001",
      "goal": "Implement JWT validation in auth middleware",
      "covers_ac": ["AC-1", "AC-3"],
      "verify_cmd": "npm test -- --testPathPattern=auth",
      "allowed_paths": ["src/auth/**", "tests/auth/**"],
      "depends_on": [],
      "rollback": "git restore --source=HEAD~1 -- src/auth",
      "wave": 1,
      "status": "pending | in_progress | passed | failed | skipped"
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | ✅ | 唯一标识，格式 `task-NNN` |
| `goal` | string | ✅ | 一句话描述 task 目标 |
| `covers_ac` | string[] | Standard+ | 本 task 覆盖的 AC 列表 |
| `verify_cmd` | string | Simple+ | 验证命令（编译/测试/lint） |
| `allowed_paths` | string[] | Complex+ | 允许修改的文件 glob 模式 |
| `depends_on` | string[] | Complex+ | 前置依赖 task id 列表 |
| `rollback` | string | Complex+ | 回滚命令 |
| `wave` | number | Complex+ | 并行分组编号（同 wave 可并行） |
| `status` | string | ✅ | 任务状态 |

### 按 Profile 裁剪

| Profile | 必填字段 |
|---------|---------|
| quick | 无 tasks.json（直接执行） |
| simple | `id`, `goal`, `verify_cmd` |
| standard | + `covers_ac` |
| complex | + `allowed_paths`, `depends_on`, `rollback`, `wave` |
| orchestrated | 全字段 |

---

## 2. verify-evidence.json

**产出于**：Phase 4 (VERIFY)
**消费于**：Phase 4 (Ralph Loop)、Phase 5 (reconcile AC 对账)
**类型**：Transient（归档到 .archive/）

### Schema

```json
{
  "task_id": "task-001",
  "verify_cmd": "npm test -- --testPathPattern=auth",
  "exit_code": 0,
  "stdout_excerpt": "PASS src/auth/login.test.ts (3 tests, 3 passed)",
  "stdout_hash": "sha256:abc123...",
  "timestamp": "2026-04-08T10:30:00Z"
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_id` | string | ✅ | 对应 tasks.json 中的 id |
| `verify_cmd` | string | ✅ | 实际执行的验证命令 |
| `exit_code` | number | ✅ | 命令退出码，0 = 通过 |
| `stdout_excerpt` | string | ✅ | 关键输出摘录（非全文） |
| `stdout_hash` | string | 推荐 | 完整 stdout 的 SHA-256 |
| `timestamp` | string | ✅ | ISO 8601 时间戳 |

### Enforcement 规则

- Ralph Loop (G8) 检测：`verify-evidence` 缺失 → task 不得标记完成
- `exit_code != 0` → task 标记 `failed`，触发 build-fix loop (G5)
- 进入 Phase 5 前必须所有 Standard+ task 有对应 evidence

---

## 3. reconcile-settlement.json

**产出于**：Phase 5 (SETTLE)
**消费于**：Backflow engine、后续任务 Phase 0
**类型**：Durable（归档但可查询）

### 完整 Schema

```json
{
  "task_id": "T-1024",
  "profile": "standard",
  "execution_status": "success | partial | failed",
  "summary": "Added JWT validation to auth middleware",

  "planned_vs_actual": {
    "planned_scope": ["src/auth/middleware.ts", "src/auth/jwt.ts"],
    "actual_scope": ["src/auth/middleware.ts", "src/auth/jwt.ts", "src/auth/types.ts"],
    "deviation": "Added types.ts for JWT payload type definitions (minor scope expansion)"
  },

  "ac_results": [
    {
      "id": "AC-1",
      "result": "PASS | FAIL | SKIP",
      "evidence_ref": "verify-evidence-001",
      "reason": ""
    }
  ],

  "api_contract_changes": [
    { "type": "added | modified | removed", "entity": "POST /api/auth/validate", "detail": "..." }
  ],

  "architecture_changes": [
    "Added cache layer module depending on module-a"
  ],

  "new_invariants": [
    "All auth endpoints must validate JWT before processing request body"
  ],

  "decisions_confirmed": [
    "Use jose library over jsonwebtoken — lighter, ESM-native"
  ],

  "verification_done": {
    "unit_tests": "8 passed, 0 failed",
    "integration_tests": "2 passed",
    "coverage_delta": "+3.1%"
  },

  "residual_risks": [
    "Token refresh flow not yet implemented"
  ],

  "lessons": [
    "jose library API differs from jsonwebtoken — document migration path"
  ],

  "concerns": [
    "AC-3 FAIL: expired token returns 500 instead of 401 — tracked as follow-up"
  ],

  "backflow_targets": {
    "architecture": false,
    "interfaces": true,
    "invariants": true
  }
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_id` | string | ✅ | 任务标识 |
| `profile` | string | ✅ | 执行时的 profile 级别 |
| `execution_status` | string | ✅ | success / partial / failed |
| `summary` | string | ✅ | 一句话描述 |
| `planned_vs_actual` | object | Standard+ | 计划范围 vs 实际范围对比 |
| `ac_results` | array | Standard+ | 逐条 AC PASS/FAIL |
| `api_contract_changes` | array | Standard+ | 接口变更 |
| `architecture_changes` | array | Complex+ | 架构变更 |
| `new_invariants` | array | Standard+ | 新发现的不变量 |
| `decisions_confirmed` | array | Complex+ | 已确认的决策 |
| `verification_done` | object | ✅ | 验证结果汇总 |
| `residual_risks` | array | Standard+ | 残余风险 |
| `lessons` | array | Standard+ | 经验教训 |
| `concerns` | array | 有则必填 | 未解决的顾虑 |
| `backflow_targets` | object | Standard+ | 哪些 durable docs 需要更新 |

### Minimum Closure Contract（按 Profile 递减）

| Profile | 最低字段 |
|---------|---------|
| quick | `summary`, `verification_done`, `actual_scope`（可内联到 commit message） |
| simple | quick + `concerns?` + `lessons?` |
| standard | `planned_vs_actual` + `ac_results` + `verification_done` + `backflow_targets` |
| complex+ | 全字段，逐条 AC 对账 |

### Enforcement 规则

- 无 reconcile-settlement → 任务不得标记 DONE
- `ac_results` 存在 FAIL 且 `concerns` 为空 → 状态锁定为 `DONE_WITH_CONCERNS`
- `DONE_WITH_CONCERNS` 不得直接进入 DONE，需人工决策（close / follow-up / waiver）

---

## 4. context.jsonl

**产出于**：Phase 1 (DISCOVER)
**消费于**：Phase 3 (EXECUTE)
**类型**：Transient
**适用 Profile**：仅 Complex+

### Schema

```jsonl
{"file": "src/auth/middleware.ts", "reason": "Main modification target", "mode": "read-write"}
{"file": "src/auth/types.ts", "reason": "JWT payload type definitions", "mode": "read-write"}
{"file": "docs/interfaces.md", "reason": "API contract reference", "mode": "read-only"}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file` | string | ✅ | 文件路径 |
| `reason` | string | ✅ | 为什么需要这个文件 |
| `mode` | string | 推荐 | `read-write`（默认）/ `read-only` |

### 用途

- 控制 worker agent 的上下文边界，防止无关文件污染上下文
- 不同 worker 可以有不同的 context.jsonl，实现并行隔离
- Phase 3 启动时，只向 worker 注入 JSONL 声明的文件

---

## 5. slice.md

**产出于**：Phase 2 (Complex+)
**消费于**：Phase 3、Phase 5
**类型**：Transient
**适用 Profile**：Complex+ 启用，Standard 以下跳过

### Schema

```markdown
## Slice S-001

### Scope
- AC covered: AC-1, AC-3
- Modules: src/auth/
- Tasks: task-001, task-002
- Wave: 1

### Entry Condition
- Baseline Plan locked
- context.jsonl generated

### Exit Condition
- All tasks in this slice verified (verify-evidence collected)
- OR: BLOCKED / DONE_WITH_CONCERNS recorded

### Handoff Trigger (满足任一则结束当前 slice)
- 完成一个独立 AC 集合
- 修改文件超出 allowed_paths
- 引入新设计决策（需回 Plan Gate）
- context 使用率 > 70% (DEGRADING)
- 出现 BLOCKED / DONE_WITH_CONCERNS
```

### 设计原则

来自 PAUL 框架的 slice 判断标准：

**可以放在同一 slice**：修改同一模块、共享同一组 AC、需要连续推理链、中间决策强耦合

**必须切片**：涉及多个子系统、可独立验证和回滚、可独立 code review、输出只是另一 task 的输入引用

---

## 6. wave.json

**产出于**：Phase 2 (Orchestrated)
**消费于**：Phase 3
**类型**：Transient
**适用 Profile**：Orchestrated 必须，Complex 可选

### Schema

```json
{
  "waves": [
    {
      "wave": 1,
      "tasks": ["task-001", "task-002"],
      "parallel": true,
      "isolation": "worktree | branch | none"
    },
    {
      "wave": 2,
      "tasks": ["task-003"],
      "depends_on_waves": [1],
      "parallel": false
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `wave` | number | ✅ | wave 编号，执行顺序 |
| `tasks` | string[] | ✅ | 本 wave 包含的 task id |
| `parallel` | boolean | ✅ | 是否并行执行 |
| `isolation` | string | 并行时必填 | 隔离策略 |
| `depends_on_waves` | number[] | 推荐 | 前置依赖 wave |

---

## 7. handoff.md

**产出于**：Phase 3/4 (slice 结束时)
**消费于**：下一 session 的 Phase 0 (Resume-Bootstrap)
**类型**：Transient（跨 session 传递）
**适用 Profile**：Complex+ 跨 session 时必须

### Schema

```markdown
## Handoff H-001

### Current State
- Phase: EXECUTE
- Slice: S-001
- Last completed task: task-001
- Next task: task-002

### Resume Bootstrap
1. Load .workflow/state.json
2. Load durable docs (architecture.md, invariants.md)
3. Load current slice's context.jsonl
4. Load last verify-evidence
5. Ready — continue from next task

### Decisions Made in This Slice
- Chose jose over jsonwebtoken (ADR-003)

### Open Concerns
- Token refresh not yet addressed

### Delta Summary
- D-001: Added types.ts (minor scope expansion)
```

---

## 8. verify-review.json（审查结果）

**产出于**：Phase 4 (VERIFY)
**消费于**：Phase 4 (人类审查参考)、Phase 5 (reconcile)
**类型**：Transient

### Schema

```json
{
  "spec_fit": {
    "ac_coverage": "3/3 AC covered by tests",
    "boundary_violations": [],
    "result": "PASS | FAIL | PASS_WITH_NOTES"
  },
  "quality_fit": {
    "architecture_violations": [],
    "unnecessary_dependencies": [],
    "missing_tests": [],
    "code_smells": ["Long method in jwt.ts:45-120"],
    "result": "PASS | FAIL | PASS_WITH_NOTES"
  }
}
```

### 说明

- **spec-fit**：是否按 spec/AC/boundaries 做对
- **quality-fit**：是否有坏味道、性能风险、安全问题、架构越层
- 拆分两个维度避免审查混为一体（来自 12-Codex 建议）
- Standard+：至少 agent 自检产出 spec-fit
- Complex+：独立 review agent 产出完整双审查

---

## 9. AC Traceability Matrix（追踪矩阵）

非独立文件，由 reconcile 阶段自动生成。结构如下：

```
AC-1 → task-001, task-003 → verify-evidence-001, verify-evidence-004 → PASS
AC-2 → task-002           → verify-evidence-002                     → PASS
AC-3 → task-003           → verify-evidence-004                     → FAIL (reason: ...)
```

**用途**：SETTLE 阶段逐条 AC 对账的依据。没有 traceability matrix，reconcile 就退化为自然语言总结。

---

## 10. Completion Markers（完成标记）

非文件 schema，是 agent 输出的结构化标记。Orchestrator 通过检测这些标记判断 agent 状态。

```
## TASK COMPLETE — task-001
## VERIFICATION PASSED — 3/3 tests
## PLANNING COMPLETE
## ESCALATION NEEDED — {reason}
## BLOCKED — {reason}
## DONE_WITH_CONCERNS — {concern list}
```

**规则**：
- Agent 不能只说 "Done" 或 "Looks good"
- 标记必须包含具体 task id 或数据
- Orchestrator 通过 grep/regex 检测标记，不依赖自由文本
