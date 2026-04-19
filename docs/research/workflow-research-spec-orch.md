# Workflow Research Report: spec-orch

> 逆向工程研究报告 — 生成时间：2025-07-18

---

## 1. 框架概况

| 维度 | 说明 |
|------|------|
| **类型** | Spec-Driven Delivery Control Plane |
| **文件数** | ~2144 files |
| **语言** | Python 3.11+（51,771 行）|
| **包名** | `spec-orch`（PyPI）|
| **版本** | 0.5.2（Alpha, post-core-extraction baseline）|
| **入口** | `spec-orch` CLI |
| **范式** | Gate-First, Evidence-Driven, Seven-Plane Architecture |
| **核心哲学** | "Prompt is advice — Harness is enforcement" |

spec-orch 是一个 **spec-driven 的软件交付控制面**，专为 AI agent 编排设计。它不是聊天机器人、不是 multi-agent playground、也不是 IDE——而是一个使软件交付 **orchestratable, verifiable, operable, and evolvable** 的运维系统。其最鲜明的特征是："Spec is the requirement, not issue. Merge is not done — Gate is done."

---

## 2. 源清单

| 文件/目录 | 角色 |
|-----------|------|
| `src/spec_orch/` | 核心 Python 包 |
| `src/spec_orch/planes/` | 七平面架构实现 |
| `src/spec_orch/gates/` | Gate 系统（enforcement 核心）|
| `src/spec_orch/evidence/` | Evidence 收集与追踪 |
| `src/spec_orch/evolution/` | 闭环进化机制 |
| `src/spec_orch/cli/` | CLI 入口与命令 |
| `tests/` | 测试套件（pytest）|
| `pyproject.toml` | Python 包定义 |
| `README.md` | 架构概览与设计哲学 |
| `CLAUDE.md` | Claude Code 引导文档 |
| `docs/` | 设计文档与规范 |
| `.github/workflows/` | CI 配置 |

---

## 3. 对象模型

### Seven-Plane Architecture

spec-orch 的核心组织单元是**七个平面（Plane）**，每个平面负责交付过程的一个维度：

| Plane | 职责 |
|-------|------|
| **Specification Plane** | Spec 是需求的唯一来源（不是 issue，不是 ticket）|
| **Planning Plane** | 技术方案与任务分解 |
| **Execution Plane** | AI agent 执行编排 |
| **Gate Plane** | 质量门禁——enforcement 的核心 |
| **Evidence Plane** | 证据收集、关联、审计 |
| **Observability Plane** | 可观测性（metrics, traces, logs）|
| **Evolution Plane** | 闭环进化——从 evidence 中学习改进流程 |

### 核心实体

1. **Spec**：需求的唯一表示，不是 issue 也不是 ticket。Spec 是整个系统的驱动输入。
2. **Gate**：质量门禁，是 enforcement 的物化机制。"Merge is not done — Gate is done" 意味着交付完成的标准不是代码合并，而是通过所有 gate。
3. **Evidence**：门禁通过的证据记录。每个 gate 要求提交 evidence 才能 pass。
4. **Plan**：技术方案，由 spec 推导。
5. **Task**：原子执行单元，由 plan 分解。
6. **Evolution Record**：进化记录，由 evidence 分析生成，反馈到流程改进。

### 实体关系

```
Spec ──derive──→ Plan ──decompose──→ Tasks
  │                                     │
  │                                     ↓
  │                              Execution (AI Agent)
  │                                     │
  │                                     ↓
  └──────── Gate ←── Evidence ←── Execution Results
                │
                ↓
         Evolution Record → 改进 Spec/Gate/Plan 模板
```

### Context Isolation

- 每个 spec 在独立目录中维护完整的 lifecycle artifacts
- Gate 评估是原子性的——通过或不通过，无中间状态
- Evidence 关联到特定 gate + spec，形成审计链

---

## 4. 流程与状态机

### Happy Path

```
1. Spec 创建
    ↓ Specification Plane 接收需求
2. Plan 生成
    ↓ Planning Plane 推导技术方案
3. Task 分解
    ↓ 原子任务列表生成
4. Execution
    ↓ Execution Plane 编排 AI agent 执行
5. Gate 评估
    ↓ Gate Plane 逐个检查 gate
    ↓ 每个 gate 要求 evidence
6. Evidence 收集
    ↓ Evidence Plane 记录审计证据
7. Evolution
    ↓ Evolution Plane 分析 evidence，生成改进建议
    ↓ 反馈到 Spec/Gate 模板 → 闭环
```

### Gate 状态机

```
Gate Status:
  NOT_EVALUATED → EVALUATING → {PASSED, FAILED, BLOCKED}
  FAILED → NOT_EVALUATED (retry with new evidence)
  BLOCKED → NOT_EVALUATED (dependency gate 通过后解除)
```

### Failure Path

- **Gate 失败**：执行停止，要求提交新 evidence 后重试
- **Evidence 不足**：Gate 拒绝评估，返回所需 evidence 类型清单
- **Spec 变更**：触发受影响 gate 重新评估（change propagation）
- **AI agent 执行失败**：Execution Plane 记录失败，生成 evidence，Gate 自动 FAIL

---

## 5. 执行保障审计

| 机制 | 级别 | 说明 |
|------|------|------|
| Gate 系统 | **Hard** | 无 evidence 不可通过 gate，无 gate pass 不可完成交付 |
| Evidence 强制关联 | **Hard** | 每个 gate 决定必须附带 evidence record |
| Spec 作为唯一需求源 | **Hard** | 系统只接受 spec 驱动的工作流，不支持 ad-hoc 任务 |
| Seven-Plane 隔离 | **Hard** | 平面间通过定义清晰的接口通信，不可跨平面直接操作 |
| CI 集成 | **Hard** | Gate 评估可在 CI 中自动触发 |
| "Prompt is advice" | **Soft** | AI prompt 是建议性的，harness（代码）才是强制性的 |
| Evolution 反馈 | **Soft** | 改进建议由系统生成但由人类决定是否采纳 |
| Observability | **Soft** | 可观测性数据收集自动进行，但分析和响应需人工介入 |
| Spec 质量 | **Unenforced** | Spec 内容的质量依赖作者，无自动化质量校验 |

---

## 6. Prompt 目录

### Prompt 1: Gate 评估指令

**触发条件**：Execution 完成后自动进入 Gate Plane

**核心指令摘要**：
> 评估当前 gate 的通过条件。检查所有 required evidence 是否已提交。对每项 evidence 执行验证规则。若所有 evidence 通过验证则 gate PASS，否则 gate FAIL 并返回具体失败原因和所需补充 evidence。Gate 决定不可被 prompt 覆盖——"Prompt is advice, Harness is enforcement"。

### Prompt 2: Evolution 分析指令

**触发条件**：Sprint/milestone 结束后的 evolution 分析

**核心指令摘要**：
> 分析本周期内所有 gate 的 evidence 记录。识别重复出现的 gate 失败模式。提取可改进的流程瓶颈。生成具体的改进建议：是否需要新增 gate、修改 gate 条件、优化 spec 模板、或调整执行策略。输出结构化的 Evolution Record。

---

## 7. 微观设计亮点

### 7.1 "Prompt is advice — Harness is enforcement"

这是 spec-orch 最精炼的设计哲学。AI prompt 永远是"建议"级别的——LLM 可能遵循也可能偏离。真正的 enforcement 由 Python harness 代码实现——gate 检查、evidence 校验、状态转移都是代码逻辑，不依赖 LLM 自律。

### 7.2 Evidence-Driven Gate

Gate 不是简单的 approve/reject 按钮，而是要求提交 **具体 evidence** 才能通过。这将质量门禁从"人说了算"变为"证据说了算"，大幅提升了审计能力和可追溯性。

### 7.3 闭环 Evolution

Evolution Plane 不只是"回顾"，而是**自动分析 evidence 模式**并生成流程改进建议。这使得交付流程本身成为可迭代的对象——不仅代码在迭代，流程也在迭代。

---

## 8. 宏观设计亮点

### 8.1 "Gate is done, not merge"

传统开发以 merge 为完成标志——代码合入主干即视为"done"。spec-orch 翻转了这个定义：**通过所有 gate 才是 done**。Merge 只是 gate 通过后的一个机械步骤。这将质量标准从"代码合并"提升为"证据充分"。

### 8.2 Seven-Plane Architecture 的关注点分离

七个平面的设计实现了交付过程各维度的完全解耦。每个平面可以独立演进、独立测试、独立配置。这种架构使得企业可以按需启用/禁用特定平面（如只用 Spec + Gate，不用 Evolution），实现渐进式采纳。

---

## 9. 失败模式与局限

| # | 失败模式 | 严重度 | 说明 |
|---|---------|--------|------|
| 1 | **Gate 过度设计** | High | 如果 gate 条件设置过于严格，每次 execution 都 fail，开发者可能绕过系统 |
| 2 | **Evidence 伪造** | Medium | Evidence 来自 AI agent 的自报告，可能被 LLM 幻觉污染 |
| 3 | **Seven-Plane 认知负担** | High | 七个平面的概念开销对小团队来说过重，可能导致弃用 |
| 4 | **Alpha 版本稳定性** | High | 0.5.2 alpha 版本意味着 API 和行为可能在后续版本中 breaking change |
| 5 | **Spec 变更的级联影响** | Medium | Spec 变更触发 gate 重评估，但 cascade 深度和范围可能难以预测 |
| 6 | **Evolution 建议的可操作性** | Medium | 自动生成的改进建议可能过于抽象，缺乏具体实施步骤 |
| 7 | **2144 文件的学习曲线** | High | 大型 Python codebase 增加了理解和贡献的门槛 |

---

## 10. 迁移评估

### 可迁移候选

| 候选 | 价值 | 迁移难度 | 目标位置 |
|------|------|---------|---------|
| **"Prompt is advice — Harness is enforcement" 原则** | 设计哲学 | 低 | 所有 `1st-cc-plugin/` 插件的 enforcement 设计指导 |
| **Evidence-driven gate** | 可审计的质量门禁 | 中 | `quality/` 插件组 |
| **Gate 系统概念** | 从 approve → evidence-based pass | 中 | `workflows/deep-plan` |
| **Evolution loop** | 流程自改进 | 高 | 长期建设，扩展 `integrations/catchup` |
| **Spec-as-requirement 范式** | 需求管理升级 | 中 | 方法论层面影响全局 |

### 建议采纳顺序

1. **"Prompt is advice — Harness is enforcement"** → 设计哲学，立即指导所有 enforcement 决策
2. **Evidence-driven gate 概念** → 替代简单 approve/reject，提升 `deep-plan` 的质量保证
3. **Spec-as-requirement** → 长期方法论升级

---

## 11. 开放问题

1. **Alpha → GA 路径**：0.5.2 alpha 意味着 API 尚不稳定，何时达到 1.0？当前 breaking change 的频率和影响范围？
2. **轻量化路径**：Seven-Plane 能否提供 "lite" 模式（如只启用 Spec + Gate + Evidence 三个平面）供小团队使用？
3. **Evidence 验证深度**：Evidence 来自 AI agent 自报告，如何防止 LLM 幻觉导致的虚假 evidence？是否有 evidence 交叉验证机制？
4. **Performance 影响**：Gate 评估 + Evidence 收集 + Evolution 分析的累积开销对 CI/CD 流水线的影响有多大？
5. **与现有工具集成**：spec-orch 与 GitHub Issues / Jira / Linear 的集成策略？Spec 是否可以从 issue 自动导入？

---

## 附录：Gemini Deepdive 补充信息

> 来源：`1st-cc-plugin/workflows/loaf/docs/gemini-roadmap-review/deepdive-spec-orch.md`
> 补充内容：Evolution Pipeline、Context Assembler、Human Gate 的具体实现机制，主报告中未覆盖到的代码级细节。

### A.1 Evolution Pipeline 的 4-Phase 生命周期

spec-orch 不仅支持 workflow 执行，还实现了 **workflow 自身的演化管线**：

- **触发器**（`src/spec_orch/services/evolution/evolution_trigger.py`）：使用确定性的、锁保护的运行计数器（`.spec_orch_evolution/run_counter.json`），达到 `trigger_after_n_runs` 阈值时触发演化。
- **生命周期协议**（`src/spec_orch/domain/protocols.py`）：Nodes 实现 `LifecycleEvolver`，遵循严格的 4-phase 状态机：`observe` → `propose` → `validate` → `promote`。
- **专业化 Evolvers**：`PromptEvolver`、`PlanStrategyEvolver`、`ConfigEvolver`、`IntentEvolver`、`SkillEvolver`。
- **数据结构**（`src/spec_orch/domain/evolution.py`）：
  - `EvolutionProposal`：`change_type`（如 `prompt_variant`、`scoper_hint`）、evidence、confidence
  - `EvolutionOutcome`：result、validation method（`A_B_COMPARE` / `RULE_VALIDATOR` / `EVAL_RUNNER`）、metrics
- **PromotionRegistry**：评估 promotion gates，记录 lineage 后才允许提议变更激活。

### A.2 Context Assembler 的动态上下文管理

不同于全局统一 prompt，spec-orch 为每个 node 动态组装定制化上下文：

- **`ContextAssembler.assemble()`**（`src/spec_orch/services/context/context_assembler.py`）：构建 `ContextBundle`。
- **`NodeContextSpec`**（`src/spec_orch/domain/context.py`）：定义 node 所需的上下文维度（`required_task_fields`、`max_tokens_budget`）。
- **`ContextBundle`** 包含四个上下文层：
  - **Task**：Spec 快照、架构笔记、验收标准
  - **Execution**：文件树、`git diff`、builder 工具事件
  - **Learning**：episodic/procedural memory（`MemoryService`）、匹配 skills、相似失败样本
  - **Evidence**：已收集的证据
- **Token 预算与过滤**（`ContextRanker`）：按 `max_tokens_budget` 截断，附加 `truncation_metadata`（`retained_chars` vs `original_chars`），并过滤内部框架事件（`_filter_framework_events`）。

### A.3 Human Gate / Approval 的策略引擎

- **`GateService`**（`src/spec_orch/services/gate_service.py`）：通过 `GateSkillRegistry` 中注册的 skills 评估条件。
- **`GatePolicy` + `gate.policy.yaml`**：定义 `spec_exists`、`spec_approved`、`human_acceptance`、`within_boundaries` 等条件。Profiles 允许 daemon 模式禁用 `human_acceptance` 而 CI 模式强制更严格规则。
- **Demotion / Promotion 逻辑**：
  - 检查 `claimed_flow`（如 `hotfix` vs `standard` vs `full`）
  - 分析 `git_diff` 大小（`demotion_diff_threshold`）：若 "hotfix" 过大 → 建议降级为 "standard"；若 "standard" 意外触碰非代码文件 → 建议升级为 "full"
- **事件发射**：向 `EventBus`（`EventTopic.GATE_RESULT`）发射 `GateVerdict`，记录失败条件和回退原因。
