# Implementation Roadmap — TDD-First Workflow Implementation

> **目标**：将 00-09 冻结骨架 + 15-18 进化共识转化为可执行的实施计划。
>
> **核心路径**：Schema → Fixture → Transition Validator → Gate Test → Profile E2E → Skill/Command/Agent
>
> **总原则**（来自 15§10.1 Gate-First TDD + 18§2）：
> - 先测协议内核，再测 hook 门禁，再跑跨 profile e2e，最后才封装 command/skill workflow
> - 先搭 harness（状态外部化 + 验证外部化 + 约束环境化），不先堆 prompt
> - 状态机是真相源，hooks 是 enforcement adapter（15§0 核心判断）

---

## Vendor 参考实现索引

> **核心原则**（来自 18§0）：不整套照搬任何框架，按子系统选最佳参考。
>
> **使用方式**：实施每个 P 阶段时，先去对应的 vendor 目录读实际代码，理解它怎么做的，再写自己的实现。不要凭空编写。

所有 vendor 框架已克隆到 `vendor/` 目录。下表按实施部位列出"去哪里看、看什么"：

### 按实施阶段的参考路径

#### P0: Schema + State Machine + Transition

| 要实现的 | 第一参考 | 本地路径 | 看什么 |
|---------|---------|---------|--------|
| state.json schema | FlowSpec | `vendor/flowspec/` | 状态定义、DAG model、transition 规则 |
| transition validator | FlowSpec | `vendor/flowspec/` | workflow state validation、config schema |
| completion status 4 态 | Claude-Code-Workflow | `vendor/Claude-Code-Workflow/` | Completion Status Protocol、3-Strike escalation |
| triage routing | Get-Shit-Done | `vendor/get-shit-done/` | thin orchestrator、quick path、context budget |
| scope-aware ceremony | Compound Engineering | `vendor/compound-engineering-plugin/` | `ce:work` Phase 0 三级路由 |
| ambiguity gate | Ouroboros | `vendor/ouroboros/` | Ambiguity Gate 公式（≤0.2 才执行）|

#### P1: Gate Tests

| 要实现的 | 第一参考 | 本地路径 | 看什么 |
|---------|---------|---------|--------|
| artifact-gated transition | FlowSpec | `vendor/flowspec/` | gate 输入/输出约束、artifact 检查 |
| Ralph Loop (evidence gate) | Trellis | `vendor/Trellis/` | SubagentStop verify-before-success |
| stall detection 4 模式 | Ouroboros | `vendor/ouroboros/` | Stateless Stagnation Detection |
| anti-rationalization | PAUL | `vendor/paul/` | evidence-before-claims、diagnostic failure routing |

#### P2: Profile E2E

| 要实现的 | 第一参考 | 本地路径 | 看什么 |
|---------|---------|---------|--------|
| continuation / resume | Compound Engineering | `vendor/compound-engineering-plugin/` | Phase 0.1 resume existing work |
| context degradation 阈值 | PAUL | `vendor/paul/` | 50%/70% token budget 阈值 |
| slice / handoff | PAUL | `vendor/paul/` | handoff.md、resume-bootstrap |
| fresh subagent pattern | Get-Shit-Done | `vendor/get-shit-done/` | worker 隔离、context rot 对抗 |

#### P3: Hooks

| 要实现的 | 第一参考 | 本地路径 | 看什么 |
|---------|---------|---------|--------|
| hook runner + fail-safe | FlowSpec | `vendor/flowspec/` | hook config、timeout、路径安全 |
| never-crash wrapper | claude-reflect | `vendor/claude-reflect/` | `try/except: sys.exit(0)` 模式 |
| hook profile gating | Everything Claude Code | `vendor/everything-claude-code/` | `run-with-flags.js`、`ECC_HOOK_PROFILE` |
| Stop hook 硬阻断 | oh-my-claudecode | `vendor/oh-my-claudecode/` | `persistent-mode.cjs` 的 `{decision: "block"}` |
| PreToolUse phase guard | FlowSpec | `vendor/flowspec/` | 写保护 + 路径检查 |
| deny-first permission | yoyo-evolve | `vendor/yoyo-evolve/` | boundary nonce、hook 超时语义 |
| checkpoint hooks | ECC-Mobile | `vendor/everything-claude-code-mobile/` | pre-compact、auto-checkpoint |
| config protection | Everything Claude Code | `vendor/everything-claude-code/` | 阻止修改 linter/formatter 配置 |

#### P4: Skill / Command / Agent

| 要实现的 | 第一参考 | 本地路径 | 看什么 |
|---------|---------|---------|--------|
| command 入口设计 | Get-Shit-Done | `vendor/get-shit-done/` | command 只是入口，workflow 是过程 |
| command → workflow 映射 | FlowSpec | `vendor/flowspec/` | `/flow:assess`、`/flow:plan` 等 |
| skill 拆分 discipline | Superpowers | `vendor/superpowers/` | skill discovery、invocation discipline |
| agent 角色拆分 | Superpowers | `vendor/superpowers/` | implementer/reviewer/planner 分离 |
| tiered persona reviewers | Compound Engineering | `vendor/compound-engineering-plugin/` | 28+ persona、confidence gating |
| 双盲独立审查 | Everything Claude Code | `vendor/everything-claude-code/` | Santa Method |
| scenario keyword detection | oh-my-claudecode | `vendor/oh-my-claudecode/` | `UserPromptSubmit` hook 关键词匹配 |
| completion markers | Get-Shit-Done | `vendor/get-shit-done/` | agent 输出结构化完成信号 |
| context isolation | Ouroboros | `vendor/ouroboros/` | FilteredContext 隔离模式 |
| knowledge compounding | Compound Engineering | `vendor/compound-engineering-plugin/` | `ce:compound` skill、docs/solutions/ |
| memory routing | claude-reflect | `vendor/claude-reflect/` | `find_claude_files()` + `suggest_claude_file()` |

### 按 vendor 的快速定位表

| Vendor | 本地路径 | 最值得看的部分 | 对应 P 阶段 |
|--------|---------|---------------|------------|
| FlowSpec | `vendor/flowspec/` | 状态机、transition、hooks runner、schema validation | P0, P1, P3 |
| Get-Shit-Done | `vendor/get-shit-done/` | 路由、command 入口、fresh worker、completion markers | P0, P2, P4 |
| PAUL | `vendor/paul/` | handoff/resume、evidence-before-claims、context 阈值 | P1, P2 |
| Trellis | `vendor/Trellis/` | Ralph Loop、verify-before-success、JSONL 注入 | P1 |
| Compound Engineering | `vendor/compound-engineering-plugin/` | scope-aware triage、continuation resume、review pipeline | P0, P2, P4 |
| Everything Claude Code | `vendor/everything-claude-code/` | hook profile gating、Santa Method、Strategic Compact | P3, P4 |
| ECC-Mobile | `vendor/everything-claude-code-mobile/` | checkpoint hooks、DAG 编排、feature state JSON | P3 |
| claude-reflect | `vendor/claude-reflect/` | never-crash hook、hybrid detection、memory routing | P3, P4 |
| oh-my-claudecode | `vendor/oh-my-claudecode/` | Stop hook 硬阻断、UserPromptSubmit 关键词检测 | P3, P4 |
| Ouroboros | `vendor/ouroboros/` | ambiguity gate、stall detection 4 模式、FilteredContext | P0, P1, P4 |
| yoyo-evolve | `vendor/yoyo-evolve/` | deny-first permission、boundary nonce、checkpoint-restart | P3 |
| Superpowers | `vendor/superpowers/` | agent 角色拆分、skill discipline、session 上下文注入 | P4 |
| Claude-Code-Workflow | `vendor/Claude-Code-Workflow/` | Completion Status Protocol、3-Strike、统一任务模型 | P0 |

### 使用纪律

1. **实施前必读**：开始每个 sub-step 之前，先去对应 vendor 目录读实际代码，理解它的实现方式
2. **借机制不借框架**：只抄你需要的那个子系统的实现思路，不要把整个框架的架构搬过来
3. **适配不照搬**：vendor 的实现要按我们的 schema/fixture/transition 体系重写，不能直接复制文件
4. **记录来源**：每个实现如果参考了 vendor 代码，在注释或 commit message 中注明来源

---

## 术语速查

| 术语 | 含义 | 来源 |
|------|------|------|
| profile | 治理强度等级：quick / simple / standard / complex / orchestrated | 00-overview |
| lane | 使用方式（如 standard/semi-auto vs standard/full）| 17§2-5 |
| route_source | 路由信号来源：explicit / scenario / continuation / score | 17§3 |
| state.json | 状态机唯一真相源 | 15§4.1 |
| transition | 状态机合法转换 | 15§4.2 |
| fixture | 某个 profile 从 triage 到 settle 的全套中间产物快照 | 本文件定义 |
| resume-pack | standard 轻量恢复包（相比 complex 的 handoff.md）| 16§6 |
| background-alignment | pre-spec 背景资料对齐槽位 | 16§4 |
| continuation | 沿已有 baseline 追加 delta，不重走 triage | 16§5, 17§3.4 |
| completion status | DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT | 15§4.4 (来自 CCW) |

---

## TDD 工作方法（贯穿 P0-P4 的执行纪律）

本文档的每一个 P 阶段都遵循同一套 TDD 工作循环。这不是建议，是强制要求。

### Red → Green → Refactor

```
1. RED:   先写一个会失败的测试（描述"什么应该成立"）
2. GREEN: 写让测试通过的最小实现（不多不少）
3. REFACTOR: 测试仍绿的前提下清理代码
```

### 在本项目中的具体含义

**P0 — Schema + Fixture 阶段**：

```
RED:    写 JSON Schema → 用一个故意缺字段的 fixture 跑校验 → 必须报错
GREEN:  补全 fixture 字段 → 校验通过
REFACTOR: 检查 schema 是否过严/过松，调整约束
```

这一步的产出不是"一堆文件"，而是"一套通过校验的 fixture 矩阵"。
fixture 就是测试的 expected output——它定义了每个 profile 在每个 phase 应该长什么样。

**P0 — Transition Validator 阶段**：

```
RED:    定义 transitions.json → 写一个非法转换用例（如 TRIAGE→SETTLE）→ validator 必须拒绝
GREEN:  实现 validator 让它拒绝非法、放行合法
REFACTOR: 检查 transition table 是否覆盖所有 profile 路径
```

**P1 — Gate Test 阶段**：

```
RED:    对每个 gate 写一个 fail fixture（如：standard 任务缺 verify-evidence）→ gate 必须阻断
GREEN:  实现 gate 检查逻辑
REFACTOR: 抽取共用的校验函数
```

**P2 — Profile E2E 阶段**：

```
RED:    写 BDD scenario（如：quick 路径 TRIAGE→EXECUTE→SETTLE→DONE）→ 用 fixture 跑完整流转 → 每步 transition 和 artifact 必须匹配
GREEN:  确保整条路径的 transition + schema + gate 全部联通
REFACTOR: 检查不同 profile 之间的共用逻辑
```

**P3/P4 — Hook + Prompt 阶段**：

```
RED:    对每个 hook 写阻断/放行测试对 → hook 必须在正确时刻拦截/放行
GREEN:  实现 hook 逻辑（调用 P0-P1 的 validator）
REFACTOR: hook 只做 adapter，不复制 gate 逻辑
```

### 关键纪律

1. **不允许跳过 RED**。没有先失败的测试，就没有实现的资格。
2. **Fixture 是规范的可执行形态**。09-schemas.md 是文档，fixture 才是真相。如果 fixture 和文档冲突，以 fixture 为准，然后更新文档。
3. **Schema 先于 Fixture，Fixture 先于 Validator，Validator 先于 Gate，Gate 先于 E2E，E2E 先于 Prompt**。这个顺序不可逆转。
4. **每完成一个 sub-step，所有已有测试必须仍然为绿**。新增不能破坏已有。
5. **状态机流转测试是整个 workflow 正确性的锚点**。如果 transition validator 的测试没通过，不允许进入 P1。

### 这套方法的核心价值

它把 workflow 的正确性从"prompt 自觉遵守"转移到了"测试锁死"：

```
传统做法：写很多规则文档 → 希望 AI 自觉遵守 → 发现它不遵守 → 补更多文档
TDD 做法：写 schema + fixture → 测试锁死预期 → 实现通过测试 → prompt 只能在测试允许的范围内操作
```

前者的约束是 soft 的（可绕过），后者的约束是 hard 的（不通过就不能推进）。

---

## P0: Schema 可执行化 + Fixture + Transition Validator

> **目标**：让 09-schemas.md 的 10 个 schema 变成可测试的契约；为每个 profile 建立全套中间态 mock；实现状态机转换校验器。
>
> **验收标准**：
> - 所有 schema 有对应的 JSON Schema 文件
> - 每个 profile 有完整 fixture 目录
> - transition validator 能拒绝非法转换
> - 所有 P0 测试通过

### P0.1 JSON Schema 可执行化

**做什么**：把 09-schemas.md 里的 10 个 schema 定义转为正式的 JSON Schema 文件。

**产出**：

```
.workflow/schemas/
├── tasks.schema.json
├── verify-evidence.schema.json
├── reconcile-settlement.schema.json
├── context.schema.json
├── slice.schema.json
├── wave.schema.json
├── handoff.schema.json
├── verify-review.schema.json
├── triage-result.schema.json          ← 新增（来自 17§8）
├── state.schema.json                  ← 新增（来自 15§4.1）
├── resume-pack.schema.json            ← 新增（来自 16§6）
└── background-alignment.schema.json   ← 新增（来自 16§4）
```

**新增 schema 说明**：

#### state.json（来自 15§4.1）

状态机唯一真相源。所有 hooks 读取此文件判断当前状态，所有 transition 通过统一入口变更此文件。

```json
{
  "profile": "standard",
  "lane": "standard/semi-auto",
  "phase": "EXECUTE",
  "status": "in_progress",
  "completion_status": null,
  "current_unit": "S-001",
  "unit_type": "task",
  "current_task": "task-003",
  "session_policy": "single",
  "allowed_transitions": ["EXECUTE->VERIFY", "EXECUTE->DELTA", "EXECUTE->BLOCKED"],
  "delta_count": 1,
  "stall_count": 0,
  "revision_count": 0,
  "context_usage_pct": 35
}
```

字段说明：

| 字段 | 类型 | 说明 | 来源 |
|------|------|------|------|
| `profile` | enum | quick/simple/standard/complex/orchestrated | 00-overview |
| `lane` | string | profile/lane 组合 | 17§5 |
| `phase` | enum | TRIAGE/DISCOVER/SPEC_PLAN/EXECUTE/VERIFY/SETTLE/DONE | 00-overview |
| `status` | enum | pending/in_progress/blocked/needs_context | 15§4.4 |
| `completion_status` | enum? | null/DONE/DONE_WITH_CONCERNS/BLOCKED/NEEDS_CONTEXT | 15§4.4 (CCW 4态) |
| `current_unit` | string? | 当前执行单元 ID（slice 或 task） | 15§7 |
| `unit_type` | enum | task/slice/wave | 15§7 |
| `current_task` | string? | 当前 task ID | — |
| `session_policy` | enum | single/fresh-per-slice/fresh-per-task | 15§6.2 |
| `allowed_transitions` | string[] | 当前合法转换列表 | 15§4.1 |
| `delta_count` | number | 累计 delta 数 | 04-execute |
| `stall_count` | number | 连续 revision 未进展计数 | 15§3.10 (Ouroboros) |
| `revision_count` | number | 当前 gate 的 revision 次数 | 07-cross-cutting |
| `context_usage_pct` | number | 上下文使用率估算 | 16§6.2 (PAUL 50%/70% 阈值) |

#### triage-result.json（来自 17§8）

路由层的结构化输出。不再只输出 profile，而是输出完整路由决策。

```json
{
  "profile": "standard",
  "lane": "standard/semi-auto",
  "route_source": "scenario",
  "continuation": false,
  "ambiguity_score": 0.15,
  "scores": {
    "scope": 3,
    "novelty": 2,
    "risk": 1,
    "reversibility": 2
  },
  "hard_constraints": [],
  "upgrade_triggers": ["new_dependency", "cross_module_spread", "contract_change"]
}
```

| 字段 | 说明 | 来源 |
|------|------|------|
| `route_source` | explicit/scenario/continuation/score | 17§3 |
| `continuation` | 是否沿已有 baseline 继续 | 17§3.4, 16§5 |
| `ambiguity_score` | 0-1，≤0.2 允许执行 | 15§3.10 (Ouroboros Ambiguity Gate) |
| `upgrade_triggers` | 命中任一则升级 lane/profile | 17§4.1 |

#### resume-pack.json（来自 16§6）

standard 的轻量恢复包。比 handoff.md 轻，比对话历史可靠。

```json
{
  "phase": "EXECUTE",
  "goal": "Add user avatar upload endpoint",
  "baseline_ref": "spec.md#baseline",
  "latest_delta": "D-003",
  "next_action": "Implement file validation in upload handler",
  "open_questions": ["Max file size policy not confirmed"],
  "context_usage_pct": 45
}
```

#### background-alignment.json（来自 16§4）

pre-spec 背景资料对齐。Discover 末尾产出，spec 之前消费。

```json
{
  "design_refs": ["figma://page-user-profile"],
  "reference_behavior": "Current avatar shows initials fallback",
  "api_docs": ["docs/interfaces.md#user-service"],
  "team_conventions": ["All file uploads go through S3 proxy"],
  "known_constraints": ["Max 5MB per file, JPEG/PNG only"],
  "out_of_scope": ["Video avatar support"],
  "inherited_decisions": ["ADR-005: S3 proxy architecture"]
}
```

### P0.2 Profile Fixture（全套中间态 Mock）

**做什么**：为每个 profile 创建一套从 triage 到 settle 的完整产物快照。这是 TDD 的 "expected output"。

**产出**：

```
.workflow/fixtures/
├── quick/
│   ├── triage-result.json
│   ├── state-triage.json         ← phase=TRIAGE 时的 state
│   ├── state-execute.json        ← phase=EXECUTE 时的 state
│   ├── state-settle.json         ← phase=SETTLE 时的 state
│   ├── state-done.json           ← phase=DONE 时的 state
│   └── reconcile-settlement.json ← minimum closure
│
├── simple/
│   ├── triage-result.json
│   ├── state-{phase}.json        ← 每个经过的 phase 一份
│   ├── tasks.json                ← 最小字段集
│   ├── verify-evidence.json
│   └── reconcile-settlement.json
│
├── standard-semi-auto/           ← 场景2：新接口 + 持续微调
│   ├── triage-result.json        ← route_source=scenario, lane=standard/semi-auto
│   ├── background-alignment.json ← pre-spec 背景资料
│   ├── state-{phase}.json
│   ├── tasks.json
│   ├── verify-evidence.json
│   ├── verify-review.json
│   ├── resume-pack.json          ← 轻量恢复包
│   ├── reconcile-settlement.json
│   └── continuation/             ← 追加 delta 场景
│       ├── triage-result.json    ← continuation=true, 不重走完整 triage
│       ├── delta-log.jsonl
│       └── state-execute.json    ← 直接从 EXECUTE 继续
│
├── standard-full/                ← 完整 standard 路径
│   ├── triage-result.json        ← route_source=score, lane=standard/full
│   ├── state-{phase}.json
│   ├── tasks.json
│   ├── verify-evidence.json
│   ├── verify-review.json
│   └── reconcile-settlement.json
│
├── complex/
│   ├── triage-result.json
│   ├── state-{phase}.json
│   ├── tasks.json                ← 全字段
│   ├── context.jsonl
│   ├── slice.md
│   ├── verify-evidence.json
│   ├── verify-review.json
│   ├── handoff.md                ← slice 结束时的跨 session 恢复
│   └── reconcile-settlement.json ← 完整 AC 对账
│
└── orchestrated/
    ├── triage-result.json
    ├── state-{phase}.json
    ├── tasks.json
    ├── context.jsonl
    ├── slice.md
    ├── wave.json
    ├── verify-evidence.json
    ├── verify-review.json
    ├── handoff.md
    └── reconcile-settlement.json
```

**Fixture 设计原则**：

1. 每个 fixture 必须能通过对应的 JSON Schema 校验
2. state-{phase}.json 之间的转换必须符合 transition table
3. reconcile-settlement.json 的字段集必须满足对应 profile 的 Minimum Closure Contract
4. standard-semi-auto 的 continuation/ 子目录专门测试 16§5 的 continuation path

### P0.3 Transition Table + Validator

**做什么**：定义状态机合法转换表，实现校验脚本。

**产出**：

```
.workflow/
├── transitions.json              ← 合法转换定义
└── scripts/
    ├── validate-schema.py        ← 校验任意 JSON 文件 against schema
    ├── validate-transition.py    ← 校验 state A → state B 是否合法
    └── validate-closure.py       ← 校验 reconcile-settlement 满足 profile 的 minimum closure
```

#### transitions.json

```json
{
  "transitions": [
    {"from": "TRIAGE",     "to": "DISCOVER",   "requires": ["triage-result.json"],    "profiles": "all"},
    {"from": "TRIAGE",     "to": "EXECUTE",    "requires": ["triage-result.json"],    "profiles": ["quick"]},
    {"from": "DISCOVER",   "to": "SPEC_PLAN",  "requires": ["G1:understanding_confirm"], "profiles": ["standard+"]},
    {"from": "DISCOVER",   "to": "EXECUTE",    "requires": [],                        "profiles": ["simple"]},
    {"from": "SPEC_PLAN",  "to": "EXECUTE",    "requires": ["tasks.json", "G2:spec_plan_review"], "profiles": ["standard+"]},
    {"from": "EXECUTE",    "to": "VERIFY",     "requires": ["G7:checkpoint"],          "profiles": "all"},
    {"from": "EXECUTE",    "to": "BLOCKED",    "requires": [],                        "profiles": "all"},
    {"from": "VERIFY",     "to": "SETTLE",     "requires": ["verify-evidence.json"],   "profiles": ["standard+"]},
    {"from": "VERIFY",     "to": "EXECUTE",    "requires": ["G6:delta_re_entry"],      "profiles": "all"},
    {"from": "VERIFY",     "to": "SETTLE",     "requires": [],                        "profiles": ["quick", "simple"]},
    {"from": "SETTLE",     "to": "DONE",       "requires": ["reconcile-settlement.json"], "profiles": "all"}
  ],
  "profile_shortcuts": {
    "quick":  ["TRIAGE", "EXECUTE", "SETTLE", "DONE"],
    "simple": ["TRIAGE", "DISCOVER", "EXECUTE", "VERIFY", "SETTLE", "DONE"]
  },
  "completion_statuses": ["DONE", "DONE_WITH_CONCERNS", "BLOCKED", "NEEDS_CONTEXT"],
  "escalation_rule": {
    "trigger": "3 consecutive non-DONE of same category",
    "action": "auto-escalate to ESCALATION",
    "source": "15§4.4 (CCW 3-Strike)"
  }
}
```

#### validate-transition.py 的测试用例（先写 failing test）

来自 15§10.1 Gate-First TDD：

```
# 合法路径 — 必须通过
TRIAGE → DISCOVER (standard)          ✅
TRIAGE → EXECUTE (quick)              ✅
EXECUTE → VERIFY (all)                ✅
VERIFY → SETTLE (有 evidence)         ✅
VERIFY → EXECUTE (delta re-entry)     ✅

# 非法路径 — 必须拒绝
TRIAGE → EXECUTE (standard)           ❌ 不允许跳过 DISCOVER
TRIAGE → SETTLE (any)                 ❌ 不允许跳过执行
DISCOVER → EXECUTE (standard)         ❌ 必须经过 SPEC_PLAN
EXECUTE → SETTLE (standard+)          ❌ 必须经过 VERIFY
VERIFY → DONE (any)                   ❌ 必须经过 SETTLE
SETTLE → DONE (无 reconcile)          ❌ 缺失 closure artifact
```

### P0.4 Hook 容错基线

**做什么**：在写任何业务 hook 之前，建立两个基线机制。

来自 15§P0.5：

1. **never-crash wrapper**（来自 15§3.6, claude-reflect）：所有 hook 共用的 try/catch 包裹器，任何 hook 内部错误不阻断主流程
2. **hook profile gating**（来自 15§3.5, ECC）：根据 state.json 的 profile 字段决定激活哪些 hooks，避免 quick 任务跑全量 hooks

**产出**：

```
.workflow/scripts/
├── hook-wrapper.sh               ← never-crash 包裹器
└── hook-profile-gate.sh          ← 读取 state.json profile，决定是否执行当前 hook
```

### P0 验收

- [ ] 12 个 JSON Schema 文件全部创建
- [ ] 5 个 profile 的 fixture 目录完整（含 standard-semi-auto 的 continuation 子目录）
- [ ] 所有 fixture 通过 schema 校验
- [ ] transition validator 拒绝所有非法路径
- [ ] transition validator 放行所有合法路径
- [ ] never-crash wrapper 测试：hook 内部抛错时主流程不中断
- [ ] hook profile gating 测试：quick profile 下只激活最小 hook 集

---

## P1: Gate Tests（脚本驱动，不涉及 Claude hook 接入）

> **目标**：为每个 gate 写 pass/fail 测试。使用 fixture 驱动，不依赖真实 AI agent。
>
> **原则**（来自 15§10.1）：先让这些测试失败，再让它们通过。
>
> **验收标准**：
> - 每个 gate 有至少 1 个 pass fixture + 1 个 fail fixture
> - 所有 gate test 通过

### P1.1 Schema Gate Tests

**测试目标**：非法 schema 被拒绝。

```
# 必须拒绝
tasks.json 缺 id                     → schema validation error
tasks.json 缺 verify_cmd (simple+)   → schema validation error
verify-evidence 缺 exit_code         → schema validation error
reconcile-settlement 缺 summary      → schema validation error
state.json phase 非法值              → schema validation error
triage-result 缺 profile             → schema validation error

# 必须接受
quick 的 reconcile 只有 summary + verification_done + actual_scope → valid
simple 的 tasks.json 只有 id + goal + verify_cmd → valid
```

### P1.2 Transition Gate Tests

**测试目标**：非法转换被阻断。

复用 P0.3 的测试用例，加上 profile-specific 路径：

```
# Profile shortcuts
quick:  TRIAGE → EXECUTE → SETTLE → DONE                    ✅ 合法
quick:  TRIAGE → DISCOVER → ...                              ❌ quick 不过 DISCOVER（虽然不报错，但应该被标记为非必要路径）

# Continuation 路由（来自 16§5, 17§3.4）
standard-semi-auto + continuation=true: 直接进入 EXECUTE     ✅
standard-semi-auto + continuation=true: 但有 upgrade_trigger → 强制回 TRIAGE  ✅
```

### P1.3 Closure Gate Tests

**测试目标**：不满足 Minimum Closure Contract 的 reconcile 被拒绝。

```
# quick: 只需 summary + verification_done + actual_scope
quick + 有 summary + 有 verification_done     → PASS
quick + 缺 summary                            → FAIL

# standard: 需要 planned_vs_actual + ac_results + verification_done + backflow_targets
standard + 全有                                → PASS
standard + 缺 ac_results                      → FAIL
standard + ac_results 有 FAIL 但 concerns 为空 → 强制 DONE_WITH_CONCERNS（不允许 DONE）

# complex+: 全字段 + 逐条 AC 对账
complex + ac_results 覆盖所有 tasks.json 的 covers_ac → PASS
complex + 遗漏 AC-3                           → FAIL
```

### P1.4 Evidence Gate Tests（Ralph Loop — G8）

**测试目标**：无 evidence 不允许完成（15§5.4）。

```
# Standard+
task 有 verify-evidence + exit_code=0          → 允许标记 passed
task 无 verify-evidence                        → 阻断，不允许完成
task 有 verify-evidence + exit_code=1          → 标记 failed，触发 build-fix

# Quick/Simple
不要求 evidence                                → 放行
```

### P1.5 Stall Detection Tests

**测试目标**：连续 revision 无进展时自动升级（来自 15§3.10, Ouroboros 4 模式）。

```
# 模式 1：循环重复
revision_count=2 + 两次错误描述相同             → escalation

# 模式 2：无进展
revision_count=2 + issue count 不减             → escalation

# 模式 3：漂移过大
修改超出 allowed_paths                          → delta re-entry (G6)

# 3-Strike（来自 15§4.4 CCW）
连续 3 次 BLOCKED (同类别)                      → auto-escalate
```

### P1 验收

- [ ] 每个 gate 有 pass + fail fixture
- [ ] schema validation 拒绝所有非法 schema
- [ ] transition validation 拒绝所有非法路径
- [ ] closure validation 按 profile 检查 minimum closure
- [ ] evidence gate 无 evidence 时阻断 standard+
- [ ] stall detection 正确触发 escalation

---

## P2: Profile E2E（BDD Scenarios）

> **目标**：用 BDD scenario 验证每个 profile 的完整路径。每个 scenario 是一个从 triage 到 done 的端到端 fixture 流转。
>
> **验收标准**：
> - 每个 profile 至少 1 个 happy path scenario
> - standard-semi-auto 有 continuation scenario
> - complex 有 slice handoff + fresh session 场景

### P2.1 Quick Path

```gherkin
Scenario: Quick — typo fix
  Given a task "fix typo in README"
  When triage scores scope=1, novelty=0, risk=0, reversibility=0
  Then profile is "quick" and lane is "quick/patch"
  And phase jumps TRIAGE → EXECUTE → SETTLE → DONE
  And reconcile-settlement contains only summary + verification_done + actual_scope
  And no tasks.json is produced
  And no verify-evidence is produced
```

### P2.2 Simple Path

```gherkin
Scenario: Simple — add utility function
  Given a task "add formatDate util"
  When triage routes to simple
  Then phase sequence is TRIAGE → DISCOVER → EXECUTE → VERIFY → SETTLE → DONE
  And tasks.json has id + goal + verify_cmd (minimal fields)
  And verify-evidence is collected after VERIFY
  And reconcile-settlement has minimum + concerns
```

### P2.3 Standard/Semi-Auto Path（场景 2：新接口落地）

```gherkin
Scenario: Standard semi-auto — new API endpoint with iterative refinement
  Given a task "implement user avatar upload endpoint"
  And route_source is "scenario"
  When triage routes to standard/semi-auto
  Then background-alignment.json is produced before spec
  And phase sequence is TRIAGE → DISCOVER → SPEC_PLAN → EXECUTE → VERIFY → SETTLE → DONE
  And tasks.json has id + goal + covers_ac + verify_cmd
  And verify-evidence is collected
  And verify-review contains spec_fit
  And reconcile-settlement has planned_vs_actual + ac_results

Scenario: Standard semi-auto — continuation delta
  Given previous task "user avatar upload" is DONE
  And a new request "add file size validation"
  When continuation=true and baseline is unchanged
  Then triage is skipped (phase jumps to EXECUTE)
  And delta-log.jsonl gets a new entry
  And no new spec is produced
  And verify-evidence covers only the new delta

Scenario: Standard semi-auto — resume after interruption
  Given task is in EXECUTE phase and context_usage_pct=55
  When session is interrupted
  Then resume-pack.json is generated
  And new session loads resume-pack to restore state
  And execution continues from next_action
```

### P2.4 Standard/Full Path

```gherkin
Scenario: Standard full — complete CRUD feature
  Given a task "add user management CRUD"
  When triage routes to standard/full
  Then full spec + BDD scenarios are produced
  And tasks.json has covers_ac
  And verify-review contains spec_fit + quality_fit (self-check)
  And reconcile-settlement has full planned_vs_actual
```

### P2.5 Complex Path（场景 3：跨模块重构）

```gherkin
Scenario: Complex — cross-module auth refactor
  Given a task "migrate auth to JWT across all services"
  When triage routes to complex/full (human confirmed)
  Then SDD + BDD + TDD pipeline is followed
  And ADR is triggered (new dependency: jose)
  And tasks.json has full fields including allowed_paths + depends_on + wave
  And context.jsonl is produced
  And slice.md defines execution boundary
  And verify-review has independent review agent output
  And reconcile-settlement has full AC traceability matrix

Scenario: Complex — slice handoff across sessions
  Given slice S-001 is complete and S-002 is next
  When slice boundary is reached
  Then handoff.md is generated with resume-bootstrap
  And state.json session_policy is "fresh-per-slice"
  And new session loads handoff.md + durable docs to bootstrap
  And execution continues from S-002's first task
```

### P2.6 Orchestrated Path

```gherkin
Scenario: Orchestrated — multi-team feature with parallel workers
  Given a task "implement payment integration across 3 services"
  When triage routes to orchestrated (human confirmed)
  Then wave.json defines parallel execution groups
  And each wave task has worktree isolation
  And orchestrator only consumes completion markers + verify-evidence
  And reconcile-settlement has full retrospective
```

### P2.7 升级/降级 Path

```gherkin
Scenario: Upgrade from standard to complex
  Given task is in standard/semi-auto
  When new_dependency is introduced (hits upgrade_trigger)
  Then system prompts upgrade to complex/full
  And state.json profile changes to complex
  And additional artifacts (ADR, context.jsonl, slice.md) are required

Scenario: Ambiguity gate blocks execution
  Given ambiguity_score is 0.4 (above 0.2 threshold)
  Then DISCOVER → SPEC_PLAN transition is blocked
  And system requires clarification before proceeding
```

### P2 验收

- [ ] 5 个 profile 的 happy path 全部通过
- [ ] standard-semi-auto 的 continuation 场景通过
- [ ] standard-semi-auto 的 resume-pack 恢复场景通过
- [ ] complex 的 slice handoff 场景通过
- [ ] 升级/降级路径通过
- [ ] ambiguity gate 阻断场景通过

---

## P3: Hook 接入（Claude Code hooks 实现）

> **目标**：将 P0-P2 验证过的 gate 逻辑接入 Claude Code 的 hook 事件系统。
>
> **原则**（来自 15§4.2）：hooks 不直接定义流程，只做 4 件事：读取状态 → 校验合法性 → 必要时阻断 → 调用统一 transition validator
>
> **验收标准**：
> - 每个 hook 有阻断/放行测试
> - hook 内部错误不阻断主流程（never-crash baseline）
> - hook 按 profile 分层激活（profile gating）

### P3.1 SessionStart Hook

**职责**（来自 15§5.1）：

- 读取 `.workflow/state.json`
- 校验当前 session 是否允许继续当前 unit
- complex+ 且无 handoff/resume-pack → 拒绝直接恢复执行
- 注入当前 phase/profile/unit 到上下文

**测试**：

```
session start + state.json 存在 + phase=EXECUTE         → 注入上下文，继续
session start + state.json 不存在                        → 初始化新任务流程
session start + complex + 无 handoff.md                  → 阻断，要求先做 handoff
session start + standard + 有 resume-pack.json           → 恢复，继续
```

### P3.2 PreToolUse Hook

**职责**（来自 15§5.2）：

- DISCOVER/SPEC_PLAN phase 不允许 Write/Edit 代码文件
- EXECUTE 中校验写入目标是否超出 allowed_paths
- VERIFY 中阻断无关业务修改
- complex+ 检查 session 是否越过 unit 边界

**测试**：

```
phase=DISCOVER + Write(src/foo.ts)                       → 阻断
phase=EXECUTE + Write(src/auth/jwt.ts) + allowed_paths 包含 → 放行
phase=EXECUTE + Write(src/payment/pay.ts) + allowed_paths 不包含 → 阻断，触发 G6
phase=VERIFY + Write(src/auth/jwt.ts)                    → 阻断（verify 不改代码）
```

### P3.3 PostToolUse Hook

**职责**（来自 15§5.3）：

- 更新 actual_scope
- 检查 delta 触发条件
- 检测 context 使用率（16§6.2 PAUL 50%/70% 阈值）
- 记录 evidence 候选信息

**测试**：

```
Write(new-file.ts) 超出 planned_scope                    → 记录到 actual_scope + 检查是否触发 delta
context_usage_pct > 50%                                  → 警告 aggressive atomicity
context_usage_pct > 70%                                  → 强制写 resume-pack + 建议结束 session
```

### P3.4 Stop / SubagentStop Hook

**职责**（来自 15§5.4）：

- 无 verify-evidence 时不允许 task 标完成
- 无 reconcile-settlement 时不允许 unit 标 closed
- DONE_WITH_CONCERNS 时阻止伪装成 DONE

**设计原则**（来自 15§3.8, OMC）：Stop hook 应拆成小的专责 hooks，每个独立失败，不做巨型 all-in-one。

**测试**：

```
Stop + standard + 无 verify-evidence                     → 阻断
Stop + standard + 有 verify-evidence + 无 reconcile      → 阻断
Stop + standard + 有 reconcile + ac FAIL + 无 concerns    → 强制 DONE_WITH_CONCERNS
Stop + quick + 无 evidence                               → 放行（quick 不要求）
Stop + hook 内部错误                                     → 放行（never-crash baseline）
```

### P3.5 Hook Profile Gating 实现

**做什么**（来自 15§3.5, ECC Hook Profile Gating）：

根据 state.json 的 profile 决定哪些 hooks 激活：

| Hook | quick | simple | standard | complex | orchestrated |
|------|-------|--------|----------|---------|-------------|
| SessionStart: state inject | ✅ | ✅ | ✅ | ✅ | ✅ |
| SessionStart: handoff check | — | — | — | ✅ | ✅ |
| PreToolUse: phase write guard | — | — | ✅ | ✅ | ✅ |
| PreToolUse: allowed_paths | — | — | — | ✅ | ✅ |
| PostToolUse: scope track | — | — | ✅ | ✅ | ✅ |
| PostToolUse: context monitor | — | — | ✅ | ✅ | ✅ |
| Stop: evidence check | — | — | ✅ | ✅ | ✅ |
| Stop: reconcile check | ✅ | ✅ | ✅ | ✅ | ✅ |
| Stop: completion status | — | — | ✅ | ✅ | ✅ |

### P3 验收

- [ ] 每个 hook 有阻断/放行测试对
- [ ] hook 内部错误不阻断主流程
- [ ] quick profile 只激活 2 个 hook
- [ ] complex profile 激活全量 hook
- [ ] SessionStart 能从 resume-pack 恢复 standard 任务
- [ ] PreToolUse 在错误 phase 阻断写入
- [ ] Stop 在无 evidence 时阻断 standard+ 完成

---

## P4: Skill / Command / Agent Prompt

> **目标**：基于已验证的协议编写 prompt 层。此时 schema、gate、transition 已被测试锁死，prompt 只是"调用已验证协议的 UI 层"。
>
> **原则**（来自 18§5.4）：
> - agent 负责角色职责
> - command 负责入口
> - skill 负责知识和纪律
> - 它们都不是状态机真相源

### P4.1 Commands（入口层）

每个 command 轻量，只负责收集输入 + 选择 workflow + 触发后续：

| Command | 触发 | 做什么 |
|---------|------|--------|
| `/workflow:start` | 用户发起新任务 | 进入 TRIAGE，输出 triage-result.json |
| `/workflow:continue` | 用户追加 delta | 检测 continuation 条件，跳过/压缩 triage |
| `/workflow:resume` | 新 session 恢复 | 读取 state.json + handoff/resume-pack，bootstrap |
| `/workflow:status` | 查看当前状态 | 读取 state.json，显示 phase + progress |
| `/workflow:advance` | 推进到下一 phase | 调用 transition validator，更新 state.json |
| `/workflow:settle` | 主动触发结算 | 进入 SETTLE phase，生成 reconcile-settlement |

### P4.2 Skills（知识与纪律层）

| Skill | 触发条件 | 职责 |
|-------|---------|------|
| triage-router | 模糊请求进入时 | 4 路路由（17§3）+ ambiguity gate |
| spec-writer | SPEC_PLAN phase | SDD→BDD→TDD 漏斗 + tasks.json 生成 |
| evidence-collector | VERIFY phase | 执行 verify_cmd + 收集 verify-evidence.json |
| reconcile-engine | SETTLE phase | 生成 reconcile-settlement.json + backflow |
| background-aligner | DISCOVER phase (standard+) | 收集 pre-spec 背景资料 |
| anti-rationalization | EXECUTE + VERIFY phase | 15§3.9 PAUL patterns 注入 |

### P4.3 Agents（角色层）

来自 18§5.1 (Superpowers 角色拆分) + 04-execute (Orchestrator/Worker 边界)：

| Agent | 职责 | Profile |
|-------|------|---------|
| orchestrator | 调度 tasks，消费 completion markers，不持有执行细节 | standard+ |
| implementer | 按 task 执行编码，产出 completion marker | standard+ |
| spec-reviewer | 独立审查 spec/plan，不信任 implementer 自报 | complex+ |
| quality-reviewer | spec-fit + quality-fit 审查 | complex+ |
| verifier | 执行 verify_cmd，产出 verify-evidence | standard+ |

### P4.4 Anti-Rationalization Injection（来自 15§3.9, PAUL）

在 EXECUTE 和 VERIFY phase 的 skill prompt 中注入：

- **evidence-before-claims**：每个断言必须先列证据，再给结论
- **diagnostic failure routing**：失败分三路——intent（需求理解错了）/ spec（设计有问题）/ code（实现有 bug）
- **"confidence without evidence is the #1 cause of false completion"**

### P4 验收

- [ ] 每个 command 能正确读写 state.json
- [ ] command 不包含业务逻辑（只做入口）
- [ ] skill 遵循已验证的 schema
- [ ] agent 角色边界清晰，不越权
- [ ] anti-rationalization 在 EXECUTE/VERIFY prompt 中可见

---

## 实施顺序总览

```
P0: Schema + Fixture + Transition Validator + Hook Baseline
│   ├── P0.1 JSON Schema 可执行化 (12 files)
│   ├── P0.2 Profile Fixture (5 profiles × N artifacts)
│   ├── P0.3 Transition Table + Validator
│   └── P0.4 Hook 容错基线 (never-crash + profile gating)
│
P1: Gate Tests (脚本驱动)
│   ├── P1.1 Schema Gate Tests
│   ├── P1.2 Transition Gate Tests
│   ├── P1.3 Closure Gate Tests
│   ├── P1.4 Evidence Gate Tests (Ralph Loop)
│   └── P1.5 Stall Detection Tests
│
P2: Profile E2E (BDD Scenarios)
│   ├── P2.1 Quick Path
│   ├── P2.2 Simple Path
│   ├── P2.3 Standard/Semi-Auto Path + Continuation + Resume
│   ├── P2.4 Standard/Full Path
│   ├── P2.5 Complex Path + Slice Handoff
│   ├── P2.6 Orchestrated Path
│   └── P2.7 Upgrade/Downgrade Path
│
P3: Hook 接入 (Claude Code hooks)
│   ├── P3.1 SessionStart
│   ├── P3.2 PreToolUse
│   ├── P3.3 PostToolUse
│   ├── P3.4 Stop / SubagentStop
│   └── P3.5 Hook Profile Gating
│
P4: Skill / Command / Agent Prompt
    ├── P4.1 Commands (入口层)
    ├── P4.2 Skills (知识与纪律层)
    ├── P4.3 Agents (角色层)
    └── P4.4 Anti-Rationalization Injection
```

---

## 参考来源索引

| 实施部位 | 主要来源 | 具体章节 |
|---------|---------|---------|
| state.json schema | 15 | §4.1 唯一真相源 |
| Completion Status 4 态 | 15 | §4.4 (CCW 协议) |
| 3-Strike escalation | 15 | §4.4 (CCW) |
| Hook 布局 | 15 | §5.1-5.4 |
| Never-crash wrapper | 15 | §3.6 (claude-reflect) |
| Hook profile gating | 15 | §3.5 (ECC) |
| Stop hook 拆分 | 15 | §3.8 (OMC) |
| Fresh session per slice | 15 | §7.2, §9.1 |
| Gate-First TDD 顺序 | 15 | §10.1 |
| Stall detection 4 模式 | 15 | §3.10 (Ouroboros) |
| Anti-rationalization | 15 | §3.9 (PAUL) |
| Semi-auto lane | 16 | §3 |
| Background alignment | 16 | §4 |
| Continuation path | 16 | §5 |
| Resume-pack | 16 | §6 |
| Deterministic trigger backflow | 16 | §7 + 15§9.5 |
| Light quality gate (4 项) | 16 | §8 |
| Pluggable routing layer | 17 | §2-3 |
| 4 路 routing signals | 17 | §3 |
| Route priority | 17 | §4 (hard > continuation > explicit > scenario > score) |
| Lane concept (profile × lane) | 17 | §5 |
| triage-result schema | 17 | §8 |
| Ambiguity gate (≤0.2) | 17 | §8 (Ouroboros) |
| 实施参考矩阵（谁借谁） | 18 | §16 完整矩阵 |
| 先 harness 后 prompt | 18 | §2 |
| Command/Skill/Agent 职责分离 | 18 | §5.4 |
| Review pipeline | 18 | §11.5 (CE + ECC Santa Method) |

---

## 附录 A：实施细节规格（从 00-09 主线 + 14-18 进化稿中提取）

> 以下内容在主体 P0-P4 中被引用但未完整展开。新 agent 实施时必须查阅本附录以获取精确参数。

### A1. tasks.json 按 Profile 必填字段矩阵

来源：14§3.1, 09-schemas

| 字段 | quick | simple | standard | complex | orchestrated |
|------|-------|--------|----------|---------|-------------|
| `id` | — | ✅ | ✅ | ✅ | ✅ |
| `goal` | — | ✅ | ✅ | ✅ | ✅ |
| `covers_ac` | — | — | ✅ | ✅ | ✅ |
| `verify_cmd` | — | ✅ | ✅ | ✅ | ✅ |
| `allowed_paths` | — | — | — | ✅ | ✅ |
| `depends_on` | — | — | — | ✅ | ✅ |
| `rollback` | — | — | — | ✅ | ✅ |
| `wave` | — | — | — | ✅ | ✅ |
| `status` | — | ✅ | ✅ | ✅ | ✅ |

quick 不产出 tasks.json（直接执行）。

### A2. Minimum Closure Contract 按 Profile 必填字段

来源：14§3.3, 00-overview

| Profile | 必填字段 |
|---------|---------|
| quick | `summary` + `verification_done` + `actual_scope`（可内联 commit message）|
| simple | quick 字段 + `concerns?`（可选）+ `lessons?`（可选）|
| standard | `planned_vs_actual` + `ac_results` + `verification_done` + `backflow_targets` |
| complex+ | 全字段，逐条 AC 对账 |

### A3. reconcile-settlement.json 完整字段定义

来源：09-schemas, 14§3.3

```
task_id:            string, 必填
profile:            enum (quick/simple/standard/complex/orchestrated), 必填
execution_status:   enum (success/partial/failed), 必填
summary:            string, 必填
planned_vs_actual:  {planned_scope: string[], actual_scope: string[], deviation: string}, Standard+
ac_results:         [{id, result: PASS|FAIL|SKIP, evidence_ref, reason}], Standard+
api_contract_changes: [{type: added|modified|removed, entity, detail}], Standard+
architecture_changes: string[], Complex+
new_invariants:     string[], Standard+
decisions_confirmed: string[], Complex+
verification_done:  {unit_tests, integration_tests, coverage_delta}, 必填
residual_risks:     string[], Standard+
lessons:            string[], Standard+
concerns:           string[], 有则必填
backflow_targets:   {architecture: bool, interfaces: bool, invariants: bool}, Standard+
```

### A4. verify-review.json 完整字段定义

来源：09-schemas, 14§6

```
spec_fit:
  ac_coverage:          string (如 "3/3 AC covered by tests")
  boundary_violations:  string[]
  result:               enum (PASS / FAIL / PASS_WITH_NOTES)

quality_fit:
  architecture_violations:  string[]
  unnecessary_dependencies: string[]
  missing_tests:            string[]
  code_smells:              string[]
  result:                   enum (PASS / FAIL / PASS_WITH_NOTES)
```

### A5. context.jsonl 字段定义

来源：09-schemas, 14§3.4

```jsonl
{"file": "string", "reason": "string", "mode": "read-write|read-only"}
```

`mode: "read-only"` 标记仅供参考不可修改的文件。PreToolUse hook 据此区分可写/只读。仅 Complex+ 产出。

### A6. Completion Markers 精确格式

来源：09-schemas, 14§5.3

Agent 必须输出以下精确格式（orchestrator 通过 regex 检测，不依赖自由文本）：

```
## TASK COMPLETE — {task-id}
## VERIFICATION PASSED — {count}/{total} tests
## PLANNING COMPLETE
## ESCALATION NEEDED — {reason}
## BLOCKED — {reason}
## DONE_WITH_CONCERNS — {concern list}
## NEEDS_CONTEXT — {what is needed}
```

### A7. Gate Failure Taxonomy — 每个 Gate 的失败类型

来源：00-overview, 07-cross-cutting

| Gate | 失败类型 | 处理 |
|------|---------|------|
| G0 Triage | preflight | 阻断，不允许进入 |
| G1 Understanding | revision | 打回重写摘要，max 3 次 → escalation |
| G2 Spec/Plan Review | revision | 打回修改 spec/plan，max 3 次 + stall detection |
| G3 ADR Trigger | preflight | 必须产出 ADR 才能继续 |
| G4 Contract | preflight | 必须达成合同才能进入 EXECUTE |
| G5 Build-Fix | revision | 修复重试，max 按 profile：quick=3, simple=5, standard+=10 |
| G6 Delta Re-entry | conditional | 判断 delta 类型，路由到正确 phase |
| G7 Checkpoint | preflight | 未通过 lint/test → 不进入 VERIFY |
| G8 Ralph Loop | revision | 缺 evidence → 重跑验证，max 3 次 |
| G9 Human Acceptance | revision | 失败分三路：bug→P3, 方案偏差→P2, 需求变化→P1 |
| G10 Injection Scan | abort | 检测到注入 → 立即停止 |
| G11 State Guard | abort | 非法写入受保护文件 → 阻断 |

### A8. G5 Build-Fix 失败后的完整动作序列

来源：04-execute

```
build-fix 耗尽（达到 profile max）→
  1. git reset --hard 回退该 task 变更
  2. 创建 self-issue 记录失败原因
  3. 跳过该 task（标记 failed）
  4. 如果所有 tasks 全部失败 → 回滚整个 EXECUTE → 回 Phase 2 重新 plan
```

### A9. G9 Human Acceptance 失败后的三路分流

来源：05-verify

| 失败类型 | 路由目标 | 说明 |
|---------|---------|------|
| 实现 bug | → Phase 3 EXECUTE | 直接修复 |
| 方案偏差 / UI 方向 | → Phase 2 SPEC & PLAN | 重做 plan |
| 需求变化 / 验收标准变化 | → Phase 1 DISCOVER | 重新澄清需求 |

### A10. Profile × Enforcement 完整交叉矩阵

来源：00-overview

| Profile | Gate hard-block | Ralph Loop | Reconcile | Anti-Rat | Stall Detection |
|---------|-----------------|------------|-----------|----------|-----------------|
| quick | G0 only | skip | minimum closure | skip | skip |
| simple | G0, G7(Quick) | skip | minimum + concern | skip | G5 only |
| standard | G0-G9 (soft→hard) | ✅ required | 轻量 reconcile + AC | ✅ required | All revision loops |
| complex | G0-G11 (hard) | ✅ required | 完整 AC 对账 | ✅ required | All + stall→abort |
| orchestrated | G0-G11 + custom | ✅ required | 完整 AC + retrospective | ✅ required | All + stall→abort |

### A11. Scope Guard 按 Profile 硬/软区分

来源：04-execute

| Profile | Scope Guard 行为 |
|---------|-----------------|
| quick | 无 |
| simple | 无 |
| standard | **软提示**：记录到 actual_scope，不阻断 |
| complex+ | **硬检查**：超出 allowed_paths → 阻断 → 触发 G6 delta re-entry |

### A12. Context Window Monitor 四级阈值

来源：07-cross-cutting §4.2, 16§6.2 (PAUL)

| 使用率 | 级别 | 动作 |
|--------|------|------|
| 0-50% | PEAK | 无限制 |
| 50-70% | GOOD | 警告，建议 aggressive atomicity（拆小任务）|
| 70-85% | DEGRADING | 强制写 resume-pack（standard）/ handoff（complex+）|
| 85%+ | CRITICAL | 强制写 checkpoint → 启动 fresh subagent 继续 |

### A13. Resume-Bootstrap 固定加载顺序

来源：07-cross-cutting §3.2-3.3, 14§8

```
Step 1: .workflow/state.json — 当前 phase、task 指针、delta count
Step 2: durable docs — architecture.md, invariants.md, interfaces.md
Step 3: handoff.md (complex+) 或 resume-pack.json (standard)
Step 4: tasks.json — 当前 task 列表和状态
Step 5: delta-log.jsonl — 累积变更记录
Step 6: 当前 phase transient — verify-evidence（如果在 VERIFY）
```

**三条禁令**：
- ❌ 不依赖对话历史恢复状态
- ❌ 不加载整个代码库
- ❌ 不从旧 spec 推断当前任务

### A14. Orchestrator/Worker 角色边界（Do/Don't 列表）

来源：14§7, 04-execute

**Orchestrator**：
- ✅ 分配 task 给 worker
- ✅ 读取 verify-evidence
- ✅ 判断是否触发 delta re-entry
- ✅ 管理 slice/wave 编排（complex+）
- ❌ 不直接写业务代码
- ❌ 不修改 spec 的目标函数
- ❌ 不决定跳过 verify

**Worker/Implementer**：
- ✅ 执行单个 task
- ✅ 产出 verify-evidence
- ✅ 在 allowed_paths 内修改代码
- ❌ 不修改其他 task 的 scope
- ❌ 不决定跳过 verify_cmd
- ❌ 不修改 Baseline Plan

### A15. Anti-Rationalization 具体 Excuse→Rebuttal 表

来源：14§5.4

| Agent 借口 | 反驳 |
|-----------|------|
| "This is just a simple string change" | 任何行为变更都需要 verify_cmd |
| "I already know what the code does" | 必须完成 code-understanding（standard+）|
| "Tests can be added later" | Plan 标注了测试计划就必须执行 |
| "The plan needs a small adjustment" | 走 Delta 流程，不允许静默修改 Baseline |
| "It looks correct to me" | 提供 verify-evidence，主观断言被拒绝 |

### A16. DONE_WITH_CONCERNS vs DONE+notes 语义区分

来源：15§9.4

```
DONE + notes/lessons  ≠  DONE_WITH_CONCERNS
轻量备注              ≠  未解决风险
```

**DONE_WITH_CONCERNS 仅适用于**：
- 有 follow-up 待处理
- 有 waiver（豁免）
- 有用户可见风险
- 有 AC FAIL / SKIP

Quick/Simple 有 notes 但无以上条件 → 仍为 DONE，不升级。

**Enforcement 位置**：validate-closure.py 检查 + Stop hook 二次确认。

### A17. Deterministic Backflow 触发器列表

来源：15§9.5, 16§7

**默认无 backflow**。仅命中以下条件时触发：

1. 改了公共接口 / API 契约 → patch `docs/interfaces.md`
2. 新增依赖 → patch `docs/architecture.md`
3. 改了既有 invariant → patch `docs/invariants.md`
4. 命中敏感路径 → 记录到 lessons
5. 产生 follow-up / waiver / residual risk → 记录 concerns
6. 有 AC FAIL / SKIP → 强制记录

**原则**：AI 提取事实（改了什么），规则决定动作（是否 backflow）。不让 AI 判断"值不值得记"。

### A18. Standard Session Reset 条件

来源：15§9.3

Standard 默认单 session。满足任一条件时强制 reset：

1. context_usage_pct > 70%
2. 出现 delta re-entry
3. 出现新设计决策
4. 同一问题 2 轮 revision 无进展

### A19. Continuation Path 完整 6 条件检查

来源：16§5.2

允许 continuation（不重走 triage）的前提——**全部满足**：

1. 基线目标不变
2. 验收锚点不变
3. 不新增一级模块
4. 不新增依赖
5. 不改架构决策
6. 只是 task/AC/UI/test patch

任一不满足 → 按新任务重走 triage。

### A20. Semi-Auto Lane 退出条件

来源：16§3.2

命中任一条件 → 退出 semi-auto，回 standard/full 或更高：

1. 新增依赖
2. 跨模块扩散
3. 验收标准变化
4. 主调用链理解被推翻
5. 需要新 ADR

### A21. Routing Priority + 3 个 Scenario Template

来源：17§3-4

**路由优先级**（从高到低）：
```
1. Hard constraints（新依赖/跨模块/新协议/架构边界/敏感路径）
2. Continuation route（是否沿已有 baseline 继续）
3. Explicit route（用户显式指定）
4. Scenario route（命中已知场景模板）
5. Score route（打分兜底）
```

**3 个 Scenario Template**：

| 场景模板 | 默认路由 |
|---------|---------|
| UI 字段补逻辑（后台补字段 + UI 补显示）| → simple/patch |
| 新接口落地 + UI 骨架 + data/ui 连接 + 持续微调 | → standard/semi-auto |
| 跨模块方案设计 / 重构 / 工程设计文档 | → complex/full |

### A22. Diagnostic Failure Routing 目标

来源：15§3.9, 18§11.6

| 失败分类 | 含义 | 路由目标 |
|---------|------|---------|
| intent | 需求理解错了 | → Phase 1 DISCOVER |
| spec | 设计有问题 | → Phase 2 SPEC & PLAN |
| code | 实现有 bug | → Phase 3 EXECUTE (build-fix) |

### A23. Background-Alignment 在 Discover 中的位置

来源：16§4.2

```
clarification → minimal implementation context → background alignment → code understanding → spec/plan
```

Background alignment 在 minimal context **之后**、code understanding **之前**。不能调换顺序：背景资料限定了代码理解的探索范围。

### A24. SDD→BDD→TDD Spec 模板

来源：14§4, 03-spec-and-plan

**Standard spec.md 模板**（BDD only）：
```markdown
## 修改目标
## 验收场景 (BDD)
Given ...
When ...
Then ...
## Scope / Non-goals
## 测试计划
```

**Complex+ spec.md 模板**（SDD + BDD + FR + NFR）：
```markdown
## SDD 约束
- Scope / Non-goals
- Invariants
- Contracts
- Error Model
## BDD 验收场景
Given/When/Then (完整)
## 功能性需求 (FR-xxx)
## 非功能约束
## 测试计划（Red→Green→Refactor）
```

### A25. ADR 模板约束

来源：14§9

ADR 限制为 **1 页**，仅含 3 节：

```markdown
## Context
## Decision
## Consequences
```

### A26. Stall Detection 4 模式 → Gate 映射

来源：15§3.10

| 模式 | 描述 | 适用 Gate |
|------|------|----------|
| 1. 循环重复 | 相同输出反复出现 | All revision loops |
| 2. 无进展 | 指标/issue count 不变 | G5 Build-Fix, G8 Ralph Loop |
| 3. 漂移过大 | 修改超出 allowed_paths | 触发 G6 Delta Re-entry |
| 4. 收敛假阳性 | 看似完成但质量不够 | G8 Ralph Loop |

Mode 4 是最危险的——agent 认为自己完成了但 evidence 质量不足。

### A27. 3-Strike Escalation 语义

来源：15§4.4

"连续 3 次**相同类别**的非 DONE 状态"中，类别指：
- BLOCKED（连续 3 次 BLOCKED → escalation）
- NEEDS_CONTEXT（连续 3 次 NEEDS_CONTEXT → escalation）
- DONE_WITH_CONCERNS（连续 3 次 → escalation）

不同类别之间的计数不累加。

### A28. Event Log Schema

来源：07-cross-cutting §4.1

P0.1 应新增 `event-log.schema.json`：

```jsonl
{"ts": "ISO8601", "event": "phase_transition", "from": "DISCOVER", "to": "SPEC_PLAN", "gate": "G1", "result": "pass", "duration_ms": 1200}
```

事件类型：`phase_transition`, `gate_result`, `delta_recorded`, `build_fix_attempt`, `stall_detected`, `escalation`, `task_complete`, `session_start`, `session_end`

### A29. .workflow/ 运行时目录结构

来源：07-cross-cutting §1.3

```
.workflow/
├── state.json                    ← 状态机唯一真相源
├── event-log.jsonl               ← 全生命周期事件日志
├── schemas/                      ← JSON Schema 定义
├── scripts/                      ← validator / hook 脚本
├── fixtures/                     ← 测试 fixture
└── .archive/{task-id}/           ← 已归档的 transient 产物
```

### A30. Hook 5 秒硬超时

来源：07-cross-cutting §6.2

所有 hook 执行超过 5 秒 → SIGTERM → 再超时 → SIGKILL。hook 不能无限阻塞主流程。

### A31. Deliver Gate 按 Profile

来源：06-settle

| Profile | 交付方式 |
|---------|---------|
| quick | 直接 commit |
| simple | 直接 commit + 可选 PR |
| standard | branch + PR |
| complex | branch + PR + CI 必须通过 |
| orchestrated | + 人工合并确认 |

### A32. Config 系统三层优先级

来源：07-cross-cutting §7

```
项目级（.claude/workflow.local.md YAML frontmatter）
  < 会话级（命令参数 --profile=standard）
    < 对话级（用户口头指令 "按 complex 走"）
```

高优先级覆盖低优先级。`auto` 值表示"遵循 profile 默认设置"。

### A33. Light Quality Gate — Semi-Auto 专用 4 项检查

来源：16§8

Standard/semi-auto lane 不做完整 code review，只检查：

1. 架构越层
2. 不必要依赖
3. 漏测试
4. 明显坏味道

作为 verify-review.json 的 quality_fit 输出，但 **跳过** spec-fit 中的完整 AC 覆盖度分析。

### A34. Review Pipeline — Confidence Gating

来源：18§11.5 (CE)

Complex+ review 的 findings 必须带 confidence score：
- 低于阈值的 finding → 排除出报告
- 4 级 severity：P0 (critical) / P1 (major) / P2 (moderate) / P3 (minor)
- 4 级 autofix：safe_auto / gated_auto / manual / human
