# My Workflow — 冻结骨架 v2

> 综合 8 个 vendor 框架研究 + Anthropic harness 论文 + PAUL 框架 + 4 份进化意见裁决，
> 冻结一套覆盖 quick → orchestrated 的可拔插工作流骨架。
>
> **核心原则**：先冻结最大完整骨架，Profile 只做减法，不做加法。

---

## 设计原则

1. **双入口**：模糊请求走打分路由；显式 `/command` 直接跳过打分进入对应层级
2. **先冻结再裁剪**：所有 phase/artifact/gate 现在定义完，profile 只跳过/降级/关闭
3. **协议驱动**：Plan 是 machine-checkable 的 `tasks.json`，不是自由文本；Verify 靠 `verify-evidence.json` 结构化记录，不靠主观断言
4. **产物驱动**：phase 转换的唯一凭证是结构化产物，不是 agent 的自我声称
5. **Enforcement 保障**：每条规则必须有 hook 拦截、schema 校验或 gate hard-block 三者之一
6. **Spec 是 transient**：spec/plan/tasks 只服务执行期，任务结束后归档销毁，不进入后续任务上下文
7. **Acceptance/Backflow 是 durable**：任务闭环时结算，提炼长期知识回流到 durable docs
8. **验证优先于自报告**：用独立 agent/脚本/编译/测试验证
9. **人在环中**：关键转换点有用户确认 gate
10. **可观测**：每个阶段的状态、耗时、产物可追踪

---

## 核心主链

整个工作流的脊柱是一条 machine-checkable 的追踪链：

```
AC (验收条件)
  → tasks.json (每个 task 绑定 AC + verify_cmd + allowed_paths)
    → verify-evidence.json (结构化执行证据)
      → reconcile-settlement.json (planned-vs-actual 对账)
        → durable backflow (architecture / interfaces / invariants / lessons)
```

没有这条链：
- "verify over self-report" 只是口号
- "reconcile is closure" 只是态度
- "fresh-context resume" 缺少恢复支点
- "slice/wave" 也只是更复杂的 ceremony

所有协议 schema 的权威定义见 [09-schemas.md](./09-schemas.md)。

---

## 冻结的 6 阶段骨架

```
Phase 0: TRIAGE        — 复杂度评估与路由（或显式跳过）
Phase 1: DISCOVER      — 需求澄清 + 代码理解 + 人类确认理解
Phase 2: SPEC & PLAN   — 规格化 + 技术方案 + 任务拆解 + ADR(条件触发)
Phase 3: EXECUTE       — 编码 + 内循环修复 + Delta 处理
Phase 4: VERIFY        — 双维审查 + 质量 gate + 人类验收
Phase 5: SETTLE        — 结算 + Backflow + Transient 归档/销毁
```

### 与 10 阶段旧版的映射

| 旧 Phase | 合并到 | 理由 |
|----------|--------|------|
| CLARIFY + RESEARCH | → Phase 1 DISCOVER | 澄清和探索是同一个"理解问题"循环，拆开会引入不必要的 gate |
| SPECIFY + PLAN | → Phase 2 SPEC & PLAN | spec 和 plan 在同一次思考中产出，分开是人为切割 |
| IMPLEMENT | → Phase 3 EXECUTE | 1:1 |
| VERIFY + REVIEW | → Phase 4 VERIFY | review 是 verify 的一种形式，不需要独立 phase |
| DELIVER + RETROSPECT | → Phase 5 SETTLE | deliver 是 settle 的子步骤，retrospect 是 backflow 的子步骤 |

**关键**：Phase 合并不意味着内部步骤消失。Phase 1 内部仍有"澄清 → 探索 → 理解摘要 → 人类确认"四步。只是不作为独立 phase 占据状态机槽位。

---

## Profile 裁剪矩阵 (The Subtraction Model)

| Phase | Quick | Simple | Standard | Complex | Orchestrated |
|-------|---------|--------|----------|---------|---------|
| **0. TRIAGE** | ✅ 自动极速定级 | ✅ 自动定级 | ✅ 自动定级 | ✅ 强制人工确认 | ✅ 强制人工确认 |
| **1. DISCOVER** | ⏭️ 透传 | ⬇️ 仅 1 句话目标 | ✅ 澄清 + 代码理解摘要 | ✅ 全量 + 人类确认 + context.jsonl | ✅ 全量 + 多源研究 + context.jsonl |
| **2. SPEC & PLAN** | ⏭️ 透传 | ⏭️ 透传 (仅 verify_cmd) | ⬇️ BDD 场景 + 轻量 spec + tasks.json | ✅ SDD+BDD + Full spec + ADR + Task DAG + slice.md | ✅ + 架构师审 + wave.json |
| **3. EXECUTE** | ✅ 直接修改 | ✅ 单步修改 | ✅ 顺序执行 + Scope Guard | ✅ DAG 编排 / 并发 + slice 闭包 | ✅ Worktree 隔离并发 |
| **4. VERIFY** | ⬇️ Quick (lint) | ✅ Standard (unit) | ✅ Full (spec-fit) | ✅ Full + quality-fit + review agent | ✅ + 人工 UAT + 外部模型 |
| **5. SETTLE** | ⬇️ minimum closure | ⬇️ minimum + concerns | ✅ 轻量 reconcile + AC 对账 | ✅ 完整 reconcile + backflow | ✅ 完整 retrospective |

---

## 产物模型 (Artifact Model)

### Transient — 执行期临时产物

| Artifact | 创建于 | 消费于 | 销毁于 |
|----------|--------|--------|--------|
| `spec.md` | Phase 2 | Phase 3 | Phase 5 (归档到 `.archive/`) |
| `tasks.json` | Phase 2 | Phase 3, 4 | Phase 5 |
| `code-understanding.md` | Phase 1 | Phase 2 | Phase 5 |
| `context.jsonl` | Phase 1 (Complex+) | Phase 3 | Phase 5 |
| `verify-evidence.json` | Phase 4 | Phase 4 (Ralph Loop), Phase 5 | Phase 5 (归档) |
| `slice.md` | Phase 2 (Complex+) | Phase 3, 5 | Phase 5 |
| `wave.json` | Phase 2 (Orchestrated) | Phase 3 | Phase 5 |
| `handoff.md` | Phase 3/4 (Complex+) | 下个 session Phase 0 | 下个 session 完成后 |
| `verify-review.json` | Phase 4 | Phase 4, 5 | Phase 5 |

**规则**：Transient 产物在 Phase 5 后对后续任务**不可见**。

### Decision — 决策产物

| Artifact | 创建于 | 触发条件 | 生命周期 |
|----------|--------|---------|---------|
| `docs/adr/XXXX-title.md` | Phase 2 | 引入新依赖 / 跨架构边界 / 新接口 | 永久 |

**规则**：Simple 任务禁止生成 ADR。Standard 条件触发。Complex+ 强制评估。

### Durable — 长期记忆产物

| Artifact | 更新于 | 消费于 | 说明 |
|----------|--------|--------|------|
| `docs/architecture.md` | Phase 5 backflow | 下个任务 Phase 0 | 当前架构高层视图 |
| `docs/interfaces.md` | Phase 5 backflow | 下个任务 Phase 0 | 对外接口契约 |
| `docs/invariants.md` | Phase 5 backflow | 下个任务 Phase 0 | 项目铁律/不变量 |
| `reconcile-settlement.json` | Phase 5 | 归档（可查询） | 任务结算记录 |
| `lessons.jsonl` | Phase 5 | 下个任务 Phase 0 (合成后) | 经验回流 |

**规则**：后续任务 Phase 0 默认加载 architecture + invariants + 近期 lessons。旧 spec **不加载**。

### Delta 处理模型

Phase 3 内部的增量变更管理：

| 层 | 说明 | 可变性 |
|----|------|--------|
| `Baseline Plan` | 人类确认后的基线版本 | 不可变 |
| `Delta Log` | 增量变化追加记录 | Append-only |
| `Effective View` | 当前执行视图 (基线+增量汇总) | 按需重生成 |

**Delta 处理规则**：
- 不改主路径/验收标准/依赖 → 只追加 Delta
- 改了主路径/影响范围/依赖/验收 → 生成新 Effective View + 重入 Plan Gate
- 修改超出 `allowed_paths` → 自动触发 Delta Re-entry

---

## Gate 模型

### Gate 列表

| Gate | 类型 | 位置 | 机制 | Profile |
|------|------|------|------|---------|
| **G0: Triage Gate** | Soft→Hard | P0→P1 | 打分 + 用户确认 (complex+ 强制) | All |
| **G1: Understanding Confirm** | Hard | P1 内部 | 代码理解摘要 → 人类确认 | Standard+ |
| **G2: Spec/Plan Review** | Soft→Hard | P2 结束 | 人类审查 spec+plan，可打回 | Standard+ |
| **G3: ADR Trigger** | Conditional | P2 内部 | 引入新依赖/跨边界 → 强制 ADR | Complex+ |
| **G4: Pre-Execute Contract** | Soft | P2→P3 | Execution contract 协商 (可选) | Orchestrated |
| **G5: Build-Fix Loop** | Hard | P3 内部 | 编译/测试失败 → 修复 (max N + stall detection) | All |
| **G6: Delta Re-entry** | Conditional | P3→P4 / P4→P3 | Delta 改变主路径 或 超 allowed_paths → 回 Plan Gate | All |
| **G7: 3-Layer Checkpoint** | Hard | P3→P4 | Quick/Standard/Full (按 profile 降级) | All |
| **G8: Ralph Loop** | Hard | P4 内部 | verify-evidence 必须存在且 exit_code=0 | Standard+ |
| **G9: Human Acceptance** | Hard | P4→P5 | 人类验收确认 | Complex+ |
| **G10: Prompt Injection Scan** | Hard | P0, P1 | 外部输入安全扫描 | All |
| **G11: State Mutation Boundary** | Hard | All | 受保护文件 hook + 状态文件写入拦截 | All |

### Gate Taxonomy — 统一失败路由

所有 gate 失败统一分为 4 类：

| 类型 | 含义 | 处理 |
|------|------|------|
| `preflight` | 前置条件不满足 | 阻断，不允许进入下一步 |
| `revision` | 可修复的问题 | 打回生产者，bounded loop (max N + stall detection) |
| `escalation` | 需要用户决策 | 暂停，呈现给用户 |
| `abort` | 继续执行会扩大损害 | 立即停止，回滚 |

**Stall Detection**：所有 `revision` 类 loop 增加 stall detection —— 连续 2 次 revision 错误描述相同（或 issue count 不减）→ 自动升级为 `escalation`。

---

## Minimum Closure Contract（按 Profile 递减）

无论任务多简单，都需要结构化闭环。闭环强度按 profile 递减：

| Profile | 最低关闭要求 |
|---------|-------------|
| quick | `summary` + `verification_done` + `actual_scope`（可内联到 commit message） |
| simple | quick + `concerns?` + `lessons?` |
| standard | `planned_vs_actual` + `ac_results` + `verification_done` + `backflow_targets` |
| complex+ | 全字段 reconcile-settlement.json，逐条 AC 对账 |

**Enforcement**：
- 无 `reconcile-settlement` → 任务不得标记 DONE
- `ac_results` 存在 FAIL 且 `concerns` 为空 → 状态锁定为 `DONE_WITH_CONCERNS`
- `DONE_WITH_CONCERNS` 不得直接进入 DONE，需人工决策（close / follow-up / waiver）

---

## Profile × Enforcement 交叉矩阵

| Profile | Gate hard-block | Ralph Loop | Reconcile | Anti-Rationalization | Stall Detection |
|---------|-----------------|------------|-----------|---------------------|-----------------|
| quick | G0 only | skip | minimum closure | skip | skip |
| simple | G0, G7(Quick) | skip | minimum + concern | skip | G5 only |
| standard | G0-G9 (soft→hard) | ✅ required | 轻量 reconcile + AC | ✅ required | All revision loops |
| complex | G0-G11 (hard) | ✅ required | 完整 AC 对账 | ✅ required | All + stall → abort |
| orchestrated | G0-G11 + custom | ✅ required | 完整 AC + retrospective | ✅ required | All + stall → abort |

---

## Slice / Wave / Handoff 执行闭包

Complex+ 任务需要的执行隔离与跨 session 恢复机制。

| 机制 | 用途 | Profile |
|------|------|---------|
| `slice.md` | 执行闭包定义 — AC 覆盖、模块范围、entry/exit/handoff 触发条件 | Complex+ |
| `wave.json` | 并行任务分组 — 同 wave 内 task 可并行执行，wave 间有依赖 | Orchestrated 必须, Complex 可选 |
| `handoff.md` | fresh-context 恢复载体 — 跨 session 时的确定性 resume bootstrap | Complex+ 跨 session 时必须 |

**Slice 切分判据**：

- **可以放在同一 slice**：修改同一模块、共享同一组 AC、需要连续推理链、中间决策强耦合
- **必须切片**：涉及多个子系统、可独立验证和回滚、可独立 code review、输出只是另一 task 的输入引用

所有 schema 定义见 [09-schemas.md](./09-schemas.md)。

---

## SDD→BDD→TDD 漏斗（按 Profile 递减）

```
SDD: 定义边界、不变量、契约、错误模型、non-goals
  ↓
BDD: 定义 Given/When/Then 验收场景
  ↓
TDD: 绑定 verify_cmd，Red→Green→Refactor 循环
```

| Profile | SDD | BDD | TDD (verify_cmd) |
|---------|-----|-----|-------------------|
| quick | skip | skip | skip |
| simple | skip | skip | ✅ verify_cmd 必须 |
| standard | skip | ✅ Given/When/Then 场景 | ✅ verify_cmd 必须 |
| complex | ✅ Constraints + Boundaries + Non-goals | ✅ 完整 BDD 场景 | ✅ Red→Green→Refactor |
| orchestrated | ✅ 完整 SDD | ✅ 完整 BDD + Rubric | ✅ 严格 TDD + pass@k |

---

## 扩展性模型

### Core Required (必须硬编码)
- 6 阶段状态机引擎
- AC → Task → Evidence → Reconcile 主链
- State mutation boundary (hook + protected files)
- 3-layer checkpoints
- Settlement/backflow engine
- Prompt injection scan
- ADR 触发器 (条件启用)
- Task-end retrospective 槽位
- Gate Taxonomy (preflight/revision/escalation/abort)
- Completion Markers
- Anti-Rationalization 检查清单
- Stall Detection

### Core Optional (核心支持，可关闭)
- Sprint/execution contract (D4)
- 脏原型重构路径 (E7)
- pass@k reliability metric (F3)
- Rubric evaluator (G3)

### Plugin Extension (插件扩展)
- 平台特定反模式检查
- 自定义 checkpoint 脚本
- 自定义 agent persona

### Out (坚决排斥)
- ❌ 固定 6 文档模型
- ❌ Memory-first / Journal-first
- ❌ Spec 作为长期 SOT
- ❌ 运行时追加 Phase

---

## 文档结构

```
my-workflow/
├── 00-overview.md          ← 本文件：冻结骨架 + 主链 + 产物模型 + Gate 模型
├── 01-triage.md            ← Phase 0: 复杂度评估与路由
├── 02-discover.md          ← Phase 1: 需求澄清 + 代码理解 + context.jsonl(Complex+)
├── 03-spec-and-plan.md     ← Phase 2: SDD→BDD→TDD + tasks.json + ADR + slice/wave
├── 04-execute.md           ← Phase 3: 编码 + Scope Guard + Orchestrator/Worker + Delta
├── 05-verify.md            ← Phase 4: spec-fit/quality-fit + Ralph Loop + Stall Detection
├── 06-settle.md            ← Phase 5: reconcile-settlement + AC 对账 + Backflow
├── 07-cross-cutting.md     ← 跨阶段：Resume-Bootstrap/Gate Taxonomy/Completion Markers/hooks
├── 08-reference-map.md     ← 机制 ↔ 来源 ↔ 痛点 ↔ 位置引用索引
└── 09-schemas.md           ← 协议 Schema 集中定义（权威参考）
```

每个阶段 md 包含：
1. **目的** — 解决什么问题
2. **内部步骤** — 该 phase 内的执行序列
3. **输入/输出产物** — 进入和退出条件（schema 引用 09-schemas.md）
4. **Gate 定义** — 该阶段涉及的门禁 + 失败路由类型
5. **Profile 行为矩阵** — 5 个层级各怎么做
6. **参考框架** — 引用哪些 vendor 的哪些机制
7. **Hooks** — 涉及的 hook 事件
8. **失败路径** — 出错怎么办（按 Gate Taxonomy 分类）
