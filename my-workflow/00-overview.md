# My Workflow — 冻结骨架 v1

> 综合 8 个 vendor 框架研究 + Anthropic harness 论文 + 真实半自动开发场景 + 两份第三方设计方案，
> 冻结一套覆盖 trivial → harness 的可拔插工作流骨架。
>
> **核心原则**：先冻结最大完整骨架，Profile 只做减法，不做加法。

---

## 设计原则

1. **双入口**：模糊请求走打分路由；显式 `/command` 直接跳过打分进入对应层级
2. **先冻结再裁剪**：所有 phase/artifact/gate 现在定义完，profile 只跳过/降级/关闭
3. **产物驱动**：phase 转换的唯一凭证是产物，不是 agent 的自我声称
4. **Spec 是 transient**：spec/plan/tasks 只服务执行期，任务结束后归档销毁，不进入后续任务上下文
5. **Acceptance/Backflow 是 durable**：任务闭环时结算，提炼长期知识回流到 durable docs
6. **验证优先于自报告**：用独立 agent/脚本/编译/测试验证
7. **人在环中**：关键转换点有用户确认 gate
8. **可观测**：每个阶段的状态、耗时、产物可追踪

---

## 冻结的 6 阶段骨架

```
Phase 0: TRIAGE        — 复杂度评估与路由（或显式跳过）
Phase 1: DISCOVER      — 需求澄清 + 代码理解 + 人类确认理解
Phase 2: SPEC & PLAN   — 规格化 + 技术方案 + 任务拆解 + ADR(条件触发)
Phase 3: EXECUTE       — 编码 + 内循环修复 + Delta 处理
Phase 4: VERIFY        — 三层检查点 + 质量 gate + 人类验收
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

| Phase | Trivial | Simple | Moderate | Complex | Harness |
|-------|---------|--------|----------|---------|---------|
| **0. TRIAGE** | ✅ 自动极速定级 | ✅ 自动定级 | ✅ 自动定级 | ✅ 强制人工确认 | ✅ 强制人工确认 |
| **1. DISCOVER** | ⏭️ 透传 | ⬇️ 仅 1 句话目标 | ✅ 澄清 + 代码理解摘要 | ✅ 全量 + 人类确认理解 | ✅ 全量 + 多源研究 |
| **2. SPEC & PLAN** | ⏭️ 透传 | ⏭️ 透传 (无 spec/plan) | ⬇️ 轻量 spec + 单节点 plan | ✅ Full spec + ADR + Task DAG | ✅ + 架构师审 + BDD |
| **3. EXECUTE** | ✅ 直接修改 | ✅ 单步修改 | ✅ 顺序执行 | ✅ DAG 编排 / 并发 | ✅ Worktree 隔离并发 |
| **4. VERIFY** | ⬇️ Quick (lint) | ✅ Standard (unit) | ✅ Full (integration) | ✅ Full + review agent | ✅ + 人工 UAT + 外部模型 |
| **5. SETTLE** | ⏭️ 透传 | ⬇️ 仅 commit message | ✅ Settlement + 接口变更 | ✅ 深度 backflow | ✅ 完整 retrospective |

---

## 产物模型 (Artifact Model)

### Transient — 执行期临时产物

| Artifact | 创建于 | 消费于 | 销毁于 |
|----------|--------|--------|--------|
| `spec.md` | Phase 2 | Phase 3 | Phase 5 (归档到 `.archive/`) |
| `plan.json` / `plan.md` | Phase 2 | Phase 3 | Phase 5 |
| `tasks.md` | Phase 2 | Phase 3 | Phase 5 |
| `code-understanding.md` | Phase 1 | Phase 2 | Phase 5 |
| `delta-log.jsonl` | Phase 3 | Phase 3-4 | Phase 5 |

**规则**：Transient 产物在 Phase 5 后对后续任务**不可见**。

### Decision — 决策产物

| Artifact | 创建于 | 触发条件 | 生命周期 |
|----------|--------|---------|---------|
| `docs/adr/XXXX-title.md` | Phase 2 | 引入新依赖 / 跨架构边界 / 新接口 | 永久 |
| `decision-log.jsonl` | Phase 2-3 | 任何被人类确认的关键决策 | 永久 |

**规则**：Simple 任务禁止生成 ADR。Moderate 条件触发。Complex+ 强制评估。

### Durable — 长期记忆产物

| Artifact | 更新于 | 消费于 | 说明 |
|----------|--------|--------|------|
| `docs/architecture.md` | Phase 5 backflow | 下个任务 Phase 0 | 当前架构高层视图 |
| `docs/interfaces.md` | Phase 5 backflow | 下个任务 Phase 0 | 对外接口契约 |
| `docs/invariants.md` | Phase 5 backflow | 下个任务 Phase 0 | 项目铁律/不变量 |
| `settlement.json` | Phase 5 | 归档 | 任务结算记录 |
| `lessons.jsonl` | Phase 5 | 下个任务 Phase 0 (合成后) | 经验回流 |

**规则**：后续任务 Phase 0 默认加载 architecture + invariants + 近期 lessons。旧 spec **不加载**。

### Delta 处理模型 (来自真实场景)

Phase 3 内部的增量变更管理：

| 层 | 说明 | 可变性 |
|----|------|--------|
| `Baseline Plan` | 人类确认后的基线版本 | 默认不可变 |
| `Delta Log` | 增量变化追加记录 | Append-only |
| `Effective View` | 当前执行视图 (基线+增量汇总) | 按需重生成 |

**Delta 处理规则**：
- 不改主路径/验收标准/依赖 → 只追加 Delta
- 改了主路径/影响范围/依赖/验收 → 生成新 Effective View + 重入 Plan Gate

---

## Gate 模型

| Gate | 类型 | 位置 | 机制 | Profile |
|------|------|------|------|---------|
| **G0: Triage Gate** | Soft→Hard | P0→P1 | 打分 + 用户确认 (complex+ 强制) | All |
| **G1: Understanding Confirm** | Hard | P1 内部 | 代码理解摘要 → 人类确认 | Moderate+ |
| **G2: Spec/Plan Review** | Soft→Hard | P2 结束 | 人类审查 spec+plan，可打回 | Moderate+ |
| **G3: ADR Trigger** | Conditional | P2 内部 | 引入新依赖/跨边界 → 强制 ADR | Complex+ |
| **G4: Pre-Execute Contract** | Soft | P2→P3 | Execution contract 协商 (可选) | Harness |
| **G5: Build-Fix Loop** | Hard | P3 内部 | 编译/测试失败 → 修复 (max N + stall detection) | All |
| **G6: Delta Re-entry** | Conditional | P3→P4 / P4→P3 | Delta 改变主路径 → 回 Plan Gate | All |
| **G7: 3-Layer Checkpoint** | Hard | P3→P4 | Quick/Standard/Full (按 profile 降级) | All |
| **G8: Ralph Loop** | Hard | P4 内部 | Agent 不能自报完成，必须有 verify 证据 | Moderate+ |
| **G9: Human Acceptance** | Hard | P4→P5 | 人类验收确认 | Complex+ |
| **G10: Prompt Injection Scan** | Hard | P0, P1 | 外部输入安全扫描 | All |
| **G11: State Mutation Boundary** | Hard | All | 受保护文件 hook + 状态文件写入拦截 | All |

---

## CONSIDER 项最终裁决

合并 discussion-notes 的分类 + 我之前的建议：

| 项 | 最终裁决 | 分类 | 理由 |
|----|---------|------|------|
| B3 6 文档模型 | **OUT** | — | 固定 6 文档过于死板 |
| B5 Spec as source of truth | **修正为 REJECT** | — | Spec 是 transient，不是长期 SOT |
| D4 Sprint contract | **CORE OPTIONAL** | P2 预留槽位 | Harness 启用，默认关闭 |
| D5 ADR | **CORE REQUIRED** | P2 条件触发 | 槽位必须存在，Simple 跳过 |
| E5 Deterministic state ops | **CORE REQUIRED (轻量版)** | Hook + protected files | 不是 CLI 工具，是 PostToolUse hook 拦截受保护文件写入 |
| E7 脏原型重构 | **CORE OPTIONAL** | P3 外部模型路径 | Harness 启用 |
| F3 pass@k | **CORE OPTIONAL** | P4 预留槽位 | 默认关闭，有需要时启用 |
| F7 三层检查点 | **CORE REQUIRED** | P4 | 核心安全网 |
| F9 反模式 grep | **PLUGIN EXTENSION** | Hook 槽位 | 不进核心 |
| G3 Rubric evaluator | **CORE OPTIONAL** | P2/P4 预留 | 默认关闭 |
| J1 两层记忆 | **OUT** | — | 不做 memory-first |
| J2 Instinct 衰减 | **OUT** | — | 同上 |
| J3 Journal | **OUT** | — | Event logging (H4) 覆盖 |
| J5 Session evaluation | **CORE REQUIRED** | P5 retrospective | 槽位必须存在，Simple 降级为 commit message |
| K5 Prompt injection scan | **CORE REQUIRED** | G10 | 低成本高价值 |

---

## 扩展性模型

### Core Required (必须硬编码)
- 6 阶段状态机引擎
- State mutation boundary (hook + protected files)
- 3-layer checkpoints
- Settlement/backflow engine
- Prompt injection scan
- ADR 触发器 (条件启用)
- Task-end retrospective 槽位

### Core Optional (核心支持，可关闭)
- Sprint/execution contract (D4)
- 脏原型重构路径 (E7)
- pass@k reliability metric (F3)
- Rubric evaluator (G3)

### Plugin Extension (插件扩展)
- 平台特定反模式检查 (F9)
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
├── 00-overview.md          ← 本文件：冻结骨架 + 产物模型 + Gate 模型 + 特性裁决
├── 01-triage.md            ← Phase 0: 复杂度评估与路由
├── 02-discover.md          ← Phase 1: 需求澄清 + 代码理解 + 人类确认
├── 03-spec-and-plan.md     ← Phase 2: 规格 + 方案 + ADR + 任务拆解
├── 04-execute.md           ← Phase 3: 编码 + Delta 处理 + 内循环
├── 05-verify.md            ← Phase 4: 检查点 + 质量 gate + 人类验收
├── 06-settle.md            ← Phase 5: 结算 + Backflow + 归档
├── 07-cross-cutting.md     ← 跨阶段：状态管理/可观测/安全/hooks/config
└── 08-reference-map.md     ← 各机制 ↔ 参考框架引用索引
```

每个阶段 md 包含：
1. **目的** — 解决什么问题
2. **内部步骤** — 该 phase 内的执行序列
3. **输入/输出产物** — 进入和退出条件
4. **Gate 定义** — 该阶段涉及的门禁
5. **Profile 行为矩阵** — 5 个层级各怎么做
6. **参考框架** — 引用哪些 vendor 的哪些机制
7. **Hooks** — 涉及的 hook 事件
8. **失败路径** — 出错怎么办
9. **Open Questions** — 待讨论的设计决策
