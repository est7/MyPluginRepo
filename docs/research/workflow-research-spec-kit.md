# Workflow Research Report: spec-kit

> 逆向工程研究报告 — 生成时间：2025-07-18

---

## 1. 框架概况

| 维度 | 说明 |
|------|------|
| **类型** | Spec-Driven Development Orchestration Framework |
| **文件数** | ~312 files |
| **语言** | Python 3.11+（核心），Markdown（模板），YAML（workflow 定义）|
| **包名** | `specify-cli`（via `uv tool install`）|
| **入口** | `specify` CLI 命令 |
| **版本** | 0.7.4.dev0 |
| **作者** | GitHub |
| **许可证** | MIT |
| **范式** | Intent-Driven Development — Specification 是可执行源码而非文档 |

spec-kit 是 GitHub 官方开源的 SDD 框架，核心理念是**将 specification 视为可执行源码**而非辅助文档。框架通过 CLI（`specify`）驱动完整的 SDD 工作流，集成 20+ AI agent 后端，提供 60+ 社区扩展和 10+ preset，并内置可恢复的 workflow 编排引擎。

---

## 2. 源清单

| 文件/目录 | 角色 |
|-----------|------|
| `src/specify_cli/__init__.py` | 主源码（~217KB），CLI 入口与核心逻辑 |
| `src/specify_cli/agents.py` | Agent 配置与集成注册（~24KB）|
| `src/specify_cli/extensions.py` | Extension 管理器（~101KB）|
| `src/specify_cli/presets.py` | Preset 管理器（~70KB）|
| `src/specify_cli/integrations/` | 20+ AI agent 集成实现 |
| `src/specify_cli/workflows/` | Workflow 编排引擎 + 10 种 step 类型 |
| `templates/` | 8 个核心命令模板 |
| `extensions/` | 60+ 社区扩展 |
| `presets/` | 10+ 社区 preset |
| `workflows/` | 内置 SDD workflow 定义（YAML）|
| `docs/` | API/用户文档 |
| `tests/` | pytest 测试套件 |
| `pyproject.toml` | Python 包定义 |
| `README.md` | 概览（~57KB）|
| `spec-driven.md` | 方法论深度解读（~25KB）|
| `AGENTS.md` | 集成架构文档（~17KB）|

---

## 3. 对象模型

### 核心实体

#### Specification Artifacts（产出物层）

1. **Constitution** (`constitution.md`)：项目级治理原则与开发标准，注入每个 AI prompt。
2. **Specification** (`spec/###-feature-name/spec.md`)：功能描述（用户视角的"what"），含 User Scenarios (P1-P3)、Acceptance Criteria (Gherkin BDD)、Key Entities。
3. **Plan** (`spec/###-feature-name/plan.md`)：技术翻译——spec → 架构。附带 `data-model.md`, `contracts/`, `research.md`。
4. **Tasks** (`spec/###-feature-name/tasks.md`)：原子任务 [T001]-[TNNN]，含 status (`[ ]`/`[X]`/`[~]`)、dependency、execution sequence。

#### Framework Registries（框架层）

| Registry | 作用 |
|----------|------|
| **INTEGRATION_REGISTRY** | agent key → IntegrationBase（20+ 集成）|
| **STEP_REGISTRY** | step type → StepBase class（10 种 step）|
| **EXTENSION_REGISTRY** | extension key → ExtensionManifest（60+ 扩展）|
| **PRESET_REGISTRY** | preset key → PresetManifest（优先级堆栈）|
| **CATALOG_STACK** | 有序目录源（env var → project → user → built-in）|

#### Workflow Execution Objects（运行时层）

| 对象 | 说明 |
|------|------|
| `WorkflowDefinition` | 解析后的 YAML：ID, name, version, schema, inputs, steps |
| `StepContext` | 执行上下文：inputs, step results, item, integration defaults |
| `StepResult` | 执行结果：status, output dict, nested steps, error message |
| `RunStatus` enum | CREATED → RUNNING → {COMPLETED, FAILED, PAUSED, ABORTED} |
| `StepStatus` enum | PENDING → {RUNNING, COMPLETED, FAILED, SKIPPED, PAUSED} |

### 实体关系

```
Constitution ──inject──→ Every AI Prompt
    │
Specification ──translate──→ Plan ──decompose──→ Tasks
    │                          │                    │
    └─── spec/###/ ────────────┘────────────────────┘
                                                    │
WorkflowDefinition ──contains──→ Steps ──execute──→ TaskItems
    │                              │
    ├── command step              ├── Integration (AI agent)
    ├── prompt step               ├── StepContext
    ├── shell step                └── StepResult
    ├── if/switch/while
    ├── fan_out/fan_in
    └── gate step (human review)
```

### Context Isolation

- 每个 feature spec 在 `spec/###-feature-name/` 目录内隔离
- Workflow run 持久化于 `.specify/.workflow-runs/`，支持断点恢复
- 4 层模板解析栈确保覆盖优先级：overrides → presets → extensions → core

---

## 4. 流程与状态机

### SDD 开发工作流（7 阶段）

```
Phase 0: INITIALIZATION
    ↓ specify init <project-name>
Phase 1: CONSTITUTION ESTABLISHMENT
    ↓ /speckit.constitution（定义原则）
Phase 2: SPECIFICATION (Clarification → Spec)
    ↓ /speckit.specify + /speckit.clarify
Phase 3: PLANNING (Technical Translation)
    ↓ /speckit.plan（spec → architecture + data models + contracts）
Phase 4: TASKING (Decomposition)
    ↓ /speckit.tasks（plan → atomic [T###]）
Phase 5: IMPLEMENTATION (Code Generation)
    ↓ /speckit.implement（execute tasks）
Phase 6: VERIFICATION (Quality Gates)
    ↓ /speckit.verify, /speckit.review
Phase 7: ITERATION (Refinement)
    ↓ /speckit.refine, /speckit.iterate
```

### Workflow Engine 状态转移

```
RunStatus:
  CREATED → RUNNING → {COMPLETED, PAUSED, FAILED, ABORTED}
  PAUSED ↔ RUNNING (resume)
  FAILED ↔ RUNNING (retry)

StepStatus:
  PENDING → RUNNING → {COMPLETED, FAILED, SKIPPED, PAUSED}
```

### Failure Path

- **Spec 歧义**：运行 `/speckit.clarify` 进入 clarification loop
- **Plan 违反 constitution**：修改 `plan.md` 直至与 constitution 对齐
- **Task 验收失败**：`/speckit.verify` 创建后续 task
- **Workflow 中断**：状态持久化，`specify workflow resume <run_id>` 恢复

---

## 5. 执行保障审计

| 机制 | 级别 | 说明 |
|------|------|------|
| Constitution 注入 | **Hard** | Constitution 自动注入每个 AI prompt，不可绕过 |
| Template 4 层解析栈 | **Hard** | 模板解析顺序固定，overrides → presets → extensions → core |
| Feature 自动编号 | **Hard** | F001, F002... 由框架自动分配，确保唯一性 |
| Task [TNNN] 原子性 | **Soft** | 每个 task 要求独立可测，但由 LLM 自律执行 |
| Acceptance Criteria (Gherkin) | **Soft** | 模板要求 Gherkin 格式，但不做语法校验 |
| Gate step (human review) | **Hard** | Workflow gate 步骤阻断执行直到人类审批 |
| Workflow 状态持久化 | **Hard** | JSON 持久化于 `.specify/.workflow-runs/`，支持恢复 |
| Extension/Preset 优先级 | **Hard** | CATALOG_STACK 严格按序解析，高优先级覆盖低优先级 |
| 质量 review 结果 | **Unenforced** | Extension 级 review（security, code review）纯建议性 |

---

## 6. Prompt 目录

### Prompt 1: /speckit.specify（规格创建）

**模板来源**：`templates/specify.md`

**核心指令摘要**：
> 基于用户描述的功能需求，创建结构化的 specification 文档。包含：Feature Description（用户视角的"what"而非"how"）、User Scenarios（按 P1-P3 优先级排列）、Acceptance Criteria（Gherkin BDD 格式）、Key Entities、Edge Cases、Out of Scope。Constitution 内容自动注入作为约束上下文。

**Context 注入**：Constitution + Repository Status + Feature Description

### Prompt 2: /speckit.implement（实施执行）

**模板来源**：`templates/implement.md`

**核心指令摘要**：
> 读取 tasks.md 中的 [TNNN] 任务列表，按依赖顺序逐个执行。每完成一个 task，标记 `[X]` 并验证 acceptance criteria。使用集成的 AI agent CLI 生成代码。遇到 blocked task (`[~]`) 时跳过并记录原因。

---

## 7. 微观设计亮点

### 7.1 4 层模板解析栈

```
Priority（从高到低）：
1. .specify/templates/overrides/     (项目级覆盖)
2. .specify/presets/templates/       (preset 定制)
3. .specify/extensions/templates/    (扩展添加)
4. Core Spec Kit defaults            (内置默认)
```

这种分层覆盖机制使得企业可以在不 fork 框架的情况下深度定制模板，同时保留核心默认值作为 fallback。

### 7.2 Jinja2 沙箱表达式引擎

Workflow step 支持 Jinja2 子集表达式（sandboxed, no I/O）：`inputs.*`, `steps.<id>.output.*`, `item`, `fan_in.*`。这使得 step 之间可以通过类型安全的表达式传递数据，而非依赖全局变量。

### 7.3 10 种 Step 类型覆盖完整编排模式

`command`, `prompt`, `shell`, `if`, `switch`, `while_loop`, `do_while`, `fan_out`, `fan_in`, `gate` — 这 10 种 step 类型构成了一个图灵完备的 workflow DSL，可以表达任意复杂的编排逻辑。

---

## 8. 宏观设计亮点

### 8.1 "Specification 是可执行源码"

spec-kit 的核心创新是将 specification 从"辅助文档"提升为"可执行源码"。Specification 不再是写完就被遗忘的 Word 文档，而是直接驱动代码生成的输入。这种范式翻转使得 spec 的维护与代码的迭代同步进行。

### 8.2 "Constitution 是组织宪法"

Constitution 机制将项目级原则和标准提升为"宪法"级别的治理文件——它被注入到每一次 AI 交互中，确保所有生成内容都在统一的约束空间内。这是一种将"文化"编码为"机制"的尝试。

---

## 9. 失败模式与局限

| # | 失败模式 | 严重度 | 说明 |
|---|---------|--------|------|
| 1 | **单文件 217KB 的 `__init__.py`** | High | 主源码集中在单一巨型文件中，违背模块化原则，增加维护和理解成本 |
| 2 | **Constitution 漂移** | Medium | Constitution 内容过长时可能超出 context window，导致部分原则被 LLM 遗忘 |
| 3 | **20+ 集成的维护负担** | High | 每个 AI agent 的 API 变化都需要更新对应 integration，测试覆盖面挑战大 |
| 4 | **Workflow 引擎复杂度** | Medium | 10 种 step 类型 + resume + retry 组合出大量边界 case，状态一致性难以完全保证 |
| 5 | **Extension 质量参差** | Medium | 60+ 社区 extension 缺乏统一的质量把关标准 |
| 6 | **Gherkin criteria 无自动执行** | Low | Acceptance criteria 用 Gherkin 格式编写但未集成 BDD 测试框架自动执行 |

---

## 10. 迁移评估

### 可迁移候选

| 候选 | 价值 | 迁移难度 | 目标位置 |
|------|------|---------|---------|
| **Constitution 机制** | 项目级原则注入每个 AI prompt | 低 | `1st-cc-plugin/` 全局 constitution 支持 |
| **4 层模板解析栈** | 企业级定制能力 | 中 | `meta/plugin-optimizer` 模板系统 |
| **Gate step (human review)** | Workflow 级人类审批 | 中 | `workflows/deep-plan` 引入 gate 概念 |
| **Integration registry 模式** | Multi-agent 后端支持 | 高 | `integrations/async-agent` 扩展 |
| **Workflow resume 能力** | 断点恢复 | 高 | 长期建设目标 |

### 建议采纳顺序

1. **Constitution 机制** → 最高 ROI，立即可为所有插件增加治理层
2. **Gate step 概念** → 丰富 `deep-plan` 的质量门禁
3. **模板分层覆盖** → 提升 `1st-cc-plugin/` 的企业级定制能力

---

## 11. 开放问题

1. **单文件架构的未来**：217KB 的 `__init__.py` 是否会在后续版本中拆分？当前的 dev 版本号暗示尚在积极重构。
2. **Extension 市场**：60+ 社区 extension 是否有版本兼容性管理？一个 extension 的 breaking change 如何通知用户？
3. **Workflow 调试**：复杂 workflow（包含 fan_out + gate + retry）的调试体验如何？是否有可视化工具？
4. **性能瓶颈**：Constitution + 模板 + 上下文的累积 token 开销是否有监控和优化策略？
