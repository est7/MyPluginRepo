# 14. Final Evolution Proposal — That's All

> **定位**：基于 4 份进化意见（09-Codex / 10-Gemini / 11-Claude / 12-Codex-v2）、4 份输入材料、8 份 vendor 研究报告和 PAUL 框架分析的最终裁决文档。
>
> **目标**：冻结进化方向和协议 schema，作为后续重写 `00-08` 主线文档的唯一依据。

---

## 0. 裁决总览

| # | 分歧 | 裁决 | 理由 |
|---|------|------|------|
| 1 | Protocol-first vs Enforcement-first | **先协议后硬化**，verify-evidence 和 reconcile 两条关键路径 enforcement 同步落 | 没有协议，enforcement 不知道检查什么；但关键路径不同步硬化，协议会退化成建议文档 |
| 2 | context.jsonl | **仅 Complex+ 引入** | Moderate 以下靠 durable docs + code-understanding 做粗粒度注入，避免过早引入间接层 |
| 3 | SDD→BDD→TDD 漏斗 | **按 profile 递减** | Complex+ 完整漏斗，Moderate 仅 BDD 场景 + verify_cmd，Simple 仅 verify_cmd |
| 4 | slice/wave/handoff | **P0 预留槽位**，定义 schema 和触发条件，Moderate 以下默认跳过 | 骨架原则是"先冻结再裁剪"，槽位不预留就是后续破坏性变更 |
| 5 | Reconcile 强度 | **按 profile 递减** | Complex+ PAUL 式逐条 AC 对账，Moderate 轻量 reconcile，Simple/Trivial minimum closure |

---

## 1. 不变的共识（直接继承，不再讨论）

以下来自 4 份意见的交集，加上输入材料和研究报告反复验证的结论：

1. **6 phase 骨架保留**：Triage → Discover → Spec & Plan → Execute → Verify → Settle
2. **Spec 是 transient**，Acceptance/Reconcile 是 durable
3. **Profile 只做减法**：trivial/simple/moderate/complex/harness 在同一骨架上裁剪
4. **Verify over self-report**：agent 不能自报完成，必须有结构化证据
5. **Fresh-context resume > 继续会话**：恢复靠结构化产物，不靠对话历史
6. **排斥项不变**：❌ 固定 6 文档模型 / ❌ Memory-first / ❌ Spec 作长期 SOT / ❌ 运行时追加 Phase

---

## 2. 本轮进化的核心主链

```
AC (验收条件)
  → tasks.json (每个 task 绑定 AC + verify_cmd + allowed_paths)
    → verify-evidence.json (结构化执行证据)
      → reconcile-settlement.json (planned-vs-actual 对账)
        → durable backflow (architecture / interfaces / invariants / lessons)
```

**这条链是整个进化的脊柱。** 没有它：
- "verify over self-report" 只是口号
- "reconcile is closure" 只是态度
- "fresh-context resume" 缺少恢复支点
- "slice/wave" 也只是更复杂的 ceremony

---

## 3. 新增协议 Schema 定义

### 3.1 tasks.json（P0）

Phase 2 产出，Phase 3 消费。每个 task 必须是 machine-checkable 的执行单元。

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
      "status": "pending"
    }
  ]
}
```

**必填字段**：`id`, `goal`, `covers_ac`, `verify_cmd`
**推荐字段**：`allowed_paths`, `depends_on`, `rollback`, `wave`

**Profile 裁剪**：
| Profile | tasks.json 要求 |
|---------|----------------|
| trivial | 无（直接执行） |
| simple | 单条 task，仅 `id` + `goal` + `verify_cmd` |
| moderate | 完整 tasks.json，`covers_ac` 必填 |
| complex+ | 完整 + `allowed_paths` + `depends_on` + `wave` |

### 3.2 verify-evidence.json（P0）

Phase 4 产出。Ralph Loop 的硬抓手。

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

**Enforcement 规则**（同步硬化）：
- Ralph Loop (G8) 触发条件：`verify-evidence` 缺失 或 `exit_code != 0` → task 不得标记完成
- 无 evidence 不得进入 Phase 5

### 3.3 reconcile-settlement.json（P0）

Phase 5 产出。唯一 closure artifact。

```json
{
  "task_id": "T-1024",
  "profile": "moderate",
  "execution_status": "success | partial | failed",
  "summary": "Added JWT validation to auth middleware",

  "planned_vs_actual": {
    "planned_scope": ["src/auth/middleware.ts", "src/auth/jwt.ts"],
    "actual_scope": ["src/auth/middleware.ts", "src/auth/jwt.ts", "src/auth/types.ts"],
    "deviation": "Added types.ts for JWT payload type definitions (minor scope expansion)"
  },

  "ac_results": [
    { "id": "AC-1", "result": "PASS", "evidence_ref": "verify-evidence-001" },
    { "id": "AC-2", "result": "PASS", "evidence_ref": "verify-evidence-002" },
    { "id": "AC-3", "result": "FAIL", "reason": "Edge case: expired token returns 500 instead of 401" }
  ],

  "api_contract_changes": [
    { "type": "added", "entity": "POST /api/auth/validate", "detail": "New endpoint for token validation" }
  ],

  "architecture_changes": [],

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
    "Token refresh flow not yet implemented — tracked as follow-up"
  ],

  "lessons": [
    "jose library API differs from jsonwebtoken — document migration path"
  ],

  "concerns": [],

  "backflow_targets": {
    "architecture": false,
    "interfaces": true,
    "invariants": true
  }
}
```

**Profile 裁剪**（Minimum Closure Contract）：

| Profile | 最低关闭要求 |
|---------|-------------|
| trivial | `summary` + `verification_done` + `actual_scope` |
| simple | trivial + `concerns?` + `lessons?` |
| moderate | 轻量 reconcile：`planned_vs_actual` + `ac_results` + `backflow_targets` |
| complex+ | 完整 reconcile：全字段，逐条 AC 对账 |

**Enforcement 规则**（同步硬化）：
- 无 reconcile-settlement 不得标记任务 DONE
- `ac_results` 中存在 FAIL 且无 `concerns` 说明 → 状态为 `DONE_WITH_CONCERNS`，不得直接进入 DONE

### 3.4 context.jsonl（仅 Complex+）

Phase 1 产出，Phase 3 消费。控制 worker agent 的上下文边界。

```jsonl
{"file": "src/auth/middleware.ts", "reason": "Main modification target — JWT validation logic"}
{"file": "src/auth/types.ts", "reason": "JWT payload type definitions"}
{"file": "tests/auth/login.test.ts", "reason": "Test file to update"}
{"file": "docs/interfaces.md", "reason": "API contract reference", "mode": "read-only"}
```

**触发条件**：Profile 为 complex 或 harness 时产出。Moderate 以下不产出，靠 durable docs + code-understanding.md 做粗粒度上下文。

### 3.5 slice.md / wave.json / handoff.md（P0 预留槽位）

#### slice.md — 执行闭包定义

```markdown
## Slice S-001

### Scope
- AC covered: AC-1, AC-3
- Modules: src/auth/
- Wave: 1

### Entry Condition
- Baseline Plan locked
- context.jsonl generated (Complex+)

### Exit Condition
- All tasks in this slice verified
- verify-evidence collected for each task
- OR: BLOCKED / DONE_WITH_CONCERNS recorded

### Handoff Trigger (满足任一则结束当前 slice)
- 完成一个独立 AC 集合
- 修改文件超出 allowed_paths
- 引入新设计决策（需回 Plan Gate）
- context 使用率 > 70%
- 出现 BLOCKED / DONE_WITH_CONCERNS
```

#### wave.json — 并行任务分组

```json
{
  "waves": [
    {
      "wave": 1,
      "tasks": ["task-001", "task-002"],
      "parallel": true,
      "isolation": "worktree"
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

#### handoff.md — fresh-context 恢复载体

```markdown
## Handoff H-001

### Current State
- Phase: EXECUTE
- Slice: S-001
- Last completed task: task-001
- Next task: task-002

### Resume Bootstrap (固定顺序)
1. Load .workflow/state.json
2. Load durable docs (architecture.md, invariants.md)
3. Load current slice's context.jsonl (Complex+)
4. Load last verify-evidence
5. Ready — continue from next task

### Decisions in this slice
- Chose jose over jsonwebtoken (ADR-003)

### Open Concerns
- Token refresh not yet addressed
```

**Profile 裁剪**：

| Profile | slice | wave | handoff |
|---------|-------|------|---------|
| trivial | skip | skip | skip |
| simple | skip | skip | skip |
| moderate | skip | skip | skip (单 session 内完成) |
| complex | 单 slice 或按需切 | 可选 | 跨 session 时必须 |
| harness | 多 slice | wave.json 必须 | 每个 slice 结束时必须 |

---

## 4. SDD→BDD→TDD 漏斗（按 Profile 递减）

### 漏斗模型

```
SDD: 定义边界、不变量、契约、错误模型、non-goals
  ↓
BDD: 定义 Given/When/Then 验收场景
  ↓
TDD: 绑定 verify_cmd，Red→Green→Refactor 循环
```

### Profile 裁剪

| Profile | SDD | BDD | TDD (verify_cmd) |
|---------|-----|-----|-------------------|
| trivial | skip | skip | skip |
| simple | skip | skip | ✅ verify_cmd 必须 |
| moderate | skip | ✅ Given/When/Then 场景 | ✅ verify_cmd 必须 |
| complex | ✅ Constraints + Boundaries + Non-goals | ✅ 完整 BDD 场景 | ✅ Red→Green→Refactor |
| harness | ✅ 完整 SDD | ✅ 完整 BDD + Rubric | ✅ 严格 TDD + pass@k |

### spec.md 结构调整

Moderate 版：

```markdown
## 修改目标
[1-3 句话]

## 验收场景 (BDD)
### Scenario 1: [名称]
Given [前置条件]
When [动作]
Then [期望结果]

## Scope / Non-goals
- In scope: ...
- Out of scope: ...
```

Complex+ 版：

```markdown
## SDD 约束 (Constraints & Boundaries)
- Scope: [本次只修改的模块]
- Non-goals: [明确不做的事]
- Invariants: [不可打破的规则]
- Contracts: [接口契约]
- Error Model: [错误分类与处理]

## BDD 验收场景
### Scenario 1: [名称]
Given ...
When ...
Then ...

## 功能性需求
- FR-001: ...

## 非功能约束
- 性能 / 安全 / 兼容性
```

---

## 5. Enforcement 升级

### 5.1 关键路径 Enforcement（P0 同步落）

| 规则 | 检查点 | 机制 | Profile |
|------|--------|------|---------|
| 无 verify-evidence 不得完成 task | G8 Ralph Loop | SubagentStop hook：扫描输出，要求 `exit_code` + `stdout_excerpt` | Moderate+ |
| 无 AC 对账不得关闭 Settle | G9→P5 transition | settle 脚本校验 reconcile-settlement.json 存在且 ac_results 非空 | Moderate+ |
| DONE_WITH_CONCERNS 不直接进 DONE | P5 内部 | concerns 非空时状态锁定，需人工决策 | All |
| 超 allowed_paths 修改触发 delta | G6 Delta Re-entry | PostToolUse hook 比对 Write/Edit 路径与 allowed_paths | Complex+ |

### 5.2 Gate Taxonomy 统一（来自 09-Codex + GSD）

所有 gate 失败统一分为 4 类路由：

| 类型 | 含义 | 处理 |
|------|------|------|
| `preflight` | 前置条件不满足 | 阻断，不允许进入下一步 |
| `revision` | 可修复的问题 | 打回生产者，bounded loop (max N + stall detection) |
| `escalation` | 需要用户决策 | 暂停，呈现给用户 |
| `abort` | 继续执行会扩大损害 | 立即停止，回滚 |

### 5.3 Completion Markers（防逃逸）

每个阶段的 agent 输出必须包含结构化完成标记：

```
## TASK COMPLETE — task-001
## VERIFICATION PASSED — 3/3 tests
## ESCALATION NEEDED — cannot resolve auth dependency conflict
## BLOCKED — waiting for user decision on token format
```

Orchestrator 通过检测这些标记判断 agent 状态，不依赖自由文本。

### 5.4 Anti-Rationalization 检查清单

在 EXECUTE 阶段注入，封堵常见的跳步借口：

| 借口 | 反驳 |
|------|------|
| "This is just a simple string change" | 任何行为变更必须有对应 verify_cmd |
| "I already know what the code does" | 必须先完成 code-understanding（Moderate+） |
| "Tests can be added later" | Plan 中标注了测试计划就必须执行 |
| "The plan needs a small adjustment" | 走 Delta 流程，不得静默修改 Baseline |
| "It looks correct to me" | 提供 verify-evidence，不接受主观断言 |

### 5.5 Stall Detection

所有 bounded revision loop 增加 stall detection：

- **条件**：连续 2 次 revision 的错误描述相同（或 issue count 不减）
- **行为**：立即 escalation 给用户，不再继续循环
- **适用于**：G2 (Spec/Plan Review), G5 (Build-Fix), G8 (Ralph Loop)

### 5.6 Profile × Enforcement 交叉矩阵

| Profile | Gate hard-block | Ralph Loop | Reconcile | Anti-rat | Stall detection |
|---------|-----------------|------------|-----------|----------|-----------------|
| trivial | G0 only | skip | minimum closure | skip | skip |
| simple | G0, G7(Quick) | skip | minimum closure + concern | skip | G5 only |
| moderate | G0-G9 (soft→hard) | ✅ required | 轻量 reconcile + AC | ✅ required | All revision loops |
| complex | G0-G11 (hard) | ✅ required | 完整 AC 对账 | ✅ required | All + stall → abort |
| harness | G0-G11 + custom | ✅ required | 完整 AC 对账 + retrospective | ✅ required | All + stall → abort |

---

## 6. Verify 阶段拆分：spec-fit vs quality-fit（来自 12-Codex）

当前 VERIFY 的审查混为一体。拆成两个独立结果：

| 审查维度 | 检查内容 | Profile |
|----------|---------|---------|
| **spec-fit** | 是否按 spec/AC/boundaries 做对？BDD 场景是否全部 PASS？ | Moderate+ |
| **quality-fit** | 是否有坏味道？性能风险？安全问题？架构越层？ | Moderate+ |

**输出结构**：

```json
{
  "spec_fit": {
    "ac_coverage": "3/3 AC covered",
    "boundary_violations": [],
    "result": "PASS"
  },
  "quality_fit": {
    "architecture_violations": [],
    "unnecessary_dependencies": [],
    "missing_tests": [],
    "code_smells": ["Long method in jwt.ts:45-120"],
    "result": "PASS_WITH_NOTES"
  }
}
```

---

## 7. Orchestrator/Worker 角色边界（来自 11-Claude）

在 Moderate+ 的 EXECUTE 阶段，写入角色约束（不需要实现 dispatcher 进程，只需要行为边界）：

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

## 8. Resume-Bootstrap 协议（来自 11-Claude + PAUL）

定义 fresh-context 恢复的确定性流程：

```
Step 1: Load .workflow/state.json (当前 phase, task 指针, delta 计数)
Step 2: Load durable docs (architecture.md, invariants.md, interfaces.md)
Step 3: Load current slice context (Complex+: context.jsonl; Moderate: code-understanding.md)
Step 4: Load last verify-evidence (知道上次验证到哪)
Step 5: Ready — continue from current task

禁止：
- 依赖历史对话恢复状态
- 全量加载代码库
- 从旧 spec 反推当前任务
```

---

## 9. 对现有主线文档的改造清单

### `00-overview.md`

1. 更新设计原则，增加"协议驱动"和"enforcement 保障"
2. 增加 `AC → Task → Evidence → Reconcile` 主链说明
3. 增加 Profile × Closure 矩阵（Minimum Closure Contract）
4. 增加 Profile × Enforcement 交叉矩阵
5. 增加 slice/wave/handoff 预留槽位描述
6. 增加 Gate Taxonomy 统一分类（preflight/revision/escalation/abort）

### `01-triage.md`

- 无重大改动，当前设计完整

### `02-discover.md`

1. Complex+ 增加 context.jsonl 产出步骤
2. Moderate 以下维持 code-understanding.md 路线

### `03-spec-and-plan.md`

1. 增加 `tasks.json` 最小 schema（含 `covers_ac`, `verify_cmd`, `allowed_paths`）
2. spec.md 结构按 SDD→BDD→TDD 漏斗重写（按 profile 递减）
3. ADR 触发条件不变，但 ADR 模板约束为 1 页：Context, Decision, Consequences
4. 增加 slice.md schema（Complex+ 在此阶段定义 slice 边界）
5. 增加 wave.json schema（Harness 在此阶段定义并行分组）

### `04-execute.md`

1. 增加 Scope Guard：PostToolUse hook 比对 allowed_paths
2. 增加 Orchestrator/Worker 角色边界
3. 增加 Anti-Rationalization 检查清单
4. 增加 Completion Markers 协议
5. 增加 slice 执行闭包（Complex+）：entry/exit condition, handoff trigger
6. Delta re-entry 增加 "超 allowed_paths" 自动触发条件

### `05-verify.md`

1. 增加 `verify-evidence.json` schema
2. 拆分 spec-fit vs quality-fit 双审查
3. Ralph Loop 硬绑到 verify-evidence：无 evidence → task 不得完成
4. 增加 Stall Detection 阈值

### `06-settle.md`

1. `settlement.json` 升级为 `reconcile-settlement.json`，增加 `planned_vs_actual` 和 `ac_results`
2. 增加 Minimum Closure Contract（按 profile 递减）
3. 增加 `DONE_WITH_CONCERNS` 不得直接进入 DONE 的规则
4. AC Traceability Matrix：`AC → tasks → evidence → result`

### `07-cross-cutting.md`

1. 增加 Resume-Bootstrap 协议
2. 增加 Gate Taxonomy 统一分类
3. 增加 Completion Markers
4. 增加 Profile × Enforcement 交叉矩阵
5. 增加 Stall Detection 通用规则
6. Protected files 列表增加 `reconcile-settlement.json`
7. 增加 handoff.md schema（Complex+ 跨 session 时必须）

### `08-reference-map.md`

1. 增加 PAUL 框架引用（reconcile, AC-first, boundaries, handoff）
2. 按"机制 → 来源 → 痛点 → 位置"四列重构（采纳 10-Gemini 建议）
3. 更新原创机制索引

---

## 10. 优先级排序

### P0：骨架重写时必须落（协议 + 关键 enforcement）

1. `tasks.json` schema（含 `covers_ac`, `verify_cmd`）
2. `verify-evidence.json` schema
3. `reconcile-settlement.json` schema（含 `planned_vs_actual`, `ac_results`）
4. Minimum Closure Contract（按 profile 递减）
5. Ralph Loop 硬绑 verify-evidence
6. DONE_WITH_CONCERNS 不得直闭
7. Gate Taxonomy 统一分类
8. Completion Markers
9. Anti-Rationalization 检查清单
10. Stall Detection
11. slice.md / wave.json / handoff.md 槽位预留（schema + 触发条件）
12. SDD→BDD→TDD 漏斗（按 profile 递减）
13. Resume-Bootstrap 协议

### P1：骨架重写后第一轮补强

14. spec-fit / quality-fit 双审查
15. Orchestrator/Worker 角色边界
16. Scope Guard (allowed_paths enforcement)
17. context.jsonl (Complex+)
18. Profile × Enforcement 交叉矩阵完整实现
19. plan-validator (machine-check tasks.json)

### P2：成熟期扩展

20. Worktree-based parallel execution
21. DAG dependency checker
22. pass@k reliability metric
23. Multi-model reviewer 并行
24. Deterministic state mutation CLI（替代 hook 方案）

---

## 11. 从 4 份意见中采纳与不采纳的明细

### 采纳

| 来源 | 采纳内容 |
|------|---------|
| **09-Codex** | 8 条工程规律（全部）；7 个 gap 中的 4.2(reconcile 唯一关闭)、4.3(plan as protocol)、4.4(gate taxonomy)、4.5(inner/outer loop → orchestrator/worker)、4.6(fresh-context)、4.7(反漂移微协议) |
| **09-Codex** | Option B (Protocol-First) 作为主路线，A 的门禁先落，C 只做 P2 预留 |
| **10-Gemini** | 7 项具体实现中的 6 项：SDD→BDD→TDD 漏斗(按 profile 递减)、spec.md 约束+场景结构、verify_cmd 强制、stdout evidence、reconcile-settlement.json、anti-rationalization |
| **10-Gemini** | reference-map 按"机制→来源→痛点→位置"四列重构 |
| **11-Claude** | verify-evidence 结构化 schema、covers_ac 绑定、Profile × Enforcement 交叉矩阵、resume-bootstrap 协议、Orchestrator/Worker 角色边界 |
| **11-Claude** | enforcement 三选一原则：每条规则要么有 hook 拦截、要么有 schema 校验、要么有 gate hard-block |
| **12-Codex** | AC→Task→Evidence→Reconcile 主链优先；Minimum Closure Contract；Evidence Bundle；spec-fit vs quality-fit；Protocol Overlay 策略（先冻结协议再回写主线） |
| **12-Codex** | 真相源暂定 repo 内结构化 artifact，不急上 issue-centered 设计 |

### 不采纳

| 来源 | 不采纳内容 | 理由 |
|------|-----------|------|
| **09-Codex** | 4.1 slice 优先级高于 task/ac/evidence | 12-Codex 的裁决更合理：slice 建立在协议化 task 之上 |
| **10-Gemini** | context.jsonl 全 profile 引入 | 当前阶段 Moderate 以下不需要精确注入的复杂度 |
| **10-Gemini** | 所有非 trivial 都走完整 SDD→BDD→TDD | Simple 只需 verify_cmd，Moderate 只需 BDD + verify_cmd |
| **10-Gemini** | 弱化 v1 的 profile/gate/state/observability 体系 | 这些是骨架级基础设施，v2 方法论应并入而非替换 |
| **11-Claude** | plan.json 优先级低于 verify_cmd | 两者都重要，但考虑到 plan 需要更复杂的 validator 实现，verify_cmd 确实更容易先落 |
| **13-Gemini** | Persona Shifting 代替 Subagent | 过于依赖 Gemini 平台特性，不是通用方案 |
| **13-Gemini** | Plan Mode 硬映射到 Phase 1 & 2 | 平台特定实现，不进入通用骨架 |
| **13-Gemini** | save_memory / tracker_create_task | 平台特定工具，不进入通用骨架 |

### 辩证对待（来自 13-Gemini）

| 机制 | 判断 |
|------|------|
| Anti-Rationalization 借口清单 | **采纳核心思路**，但不限于 Gemini 单 Agent 场景，泛化为通用 EXECUTE 约束 |
| 三层批评模式 (Acknowledge→Risk→Mitigate) | **采纳作为 quality-fit 审查结构**，但不强制为唯一审查模式 |
| 产物门控状态转换 | **已被 Gate Taxonomy 覆盖**，无需单独作为 Gemini 专属机制 |

---

## 12. 最终结论

当前 `my-workflow` 的问题不在骨架结构，而在**协议层偏薄、enforcement 缺位**。

本轮进化的核心动作是 4 件事：

1. **Plan 变协议**：tasks.json 从自由文本变成 machine-checkable schema
2. **Verify 变证据**：verify-evidence.json 从主观断言变成结构化记录
3. **Settle 变对账**：reconcile-settlement.json 从收尾总结变成 planned-vs-actual 强制对账
4. **Execute 预留切片**：slice/wave/handoff 槽位冻结，Complex+ 启用

这 4 件事做完，骨架从"结构清楚的 workflow 文档"升级为"关键路径可校验的协议面"。

后续基于本文重写 `00-08` 主线文档。
