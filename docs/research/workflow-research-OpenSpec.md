# Workflow Research Report: OpenSpec

> **研究日期**: 2025-07  
> **仓库**: fission-ai/OpenSpec  
> **文件数**: ~784  
> **许可证**: 未明确声明  
> **npm**: @fission-ai/openspec  

---

## 1. 框架概况

OpenSpec 是一个以 "Fluid not rigid, iterative not waterfall" 为核心理念的 spec framework。其最大特色是 **delta-first** 设计——将 spec 的修改（ADDED/MODIFIED/REMOVED/RENAMED）作为一等公民，通过 artifact dependency graph (DAG) 管理 spec 演化流程。框架生成面向多种 AI agent IDE 的 slash command（Claude、Cursor、Copilot、Continue、Cline），强调 **brownfield-native**（对既有项目修改友好）。

| 属性 | 值 |
|------|------|
| **类型** | Iterative Spec Evolution Framework (npm package) |
| **语言** | TypeScript (core) + YAML (schema) |
| **入口** | `npx @fission-ai/openspec` CLI |
| **核心模块** | `src/core/` (artifact-graph, validation, config, init, update) |
| **Schema** | `schemas/spec-driven/schema.yaml` (artifact dependency 定义) |
| **CI** | GitHub Actions (multi-platform matrix: linux/macos/windows) |
| **社区** | Discord + contributor-friendly docs |

---

## 2. 源清单

| 文件/目录 | 用途 | 重要度 |
|-----------|------|--------|
| `src/core/artifact-graph/graph.ts` | Artifact dependency DAG 实现 (Kahn's algorithm) | ★★★ |
| `src/core/artifact-graph/types.ts` | Schema 类型定义 | ★★★ |
| `schemas/spec-driven/schema.yaml` | Artifact type + dependency 声明 | ★★★ |
| `src/core/validation/constants.ts` | 内容校验规则 (SHALL/MUST, scenarios) | ★★★ |
| `src/core/config-schema.ts` | 三级配置系统 (global → project → change) | ★★☆ |
| `src/core/init.ts` | 项目初始化逻辑 | ★★☆ |
| `src/core/update.ts` | 版本升级与 artifact 迁移 | ★★☆ |
| `src/core/schemas/base.schema.ts` | 核心数据结构定义 | ★★☆ |
| `schemas/spec-driven/templates/` | AI agent prompt 模板 | ★★☆ |
| `docs/concepts.md` | Delta-first 设计理念详解 | ★★★ |

---

## 3. 对象模型

### 核心实体

```
Change (变更单元, 以目录组织)
  ├── proposal.md           # 变更提案
  ├── specs/                # Delta specs (ADDED/MODIFIED/REMOVED/RENAMED)
  ├── design.md             # 设计方案
  ├── tasks.md              # 任务清单
  └── metadata/             # 元数据

Spec (需求规约)
  ├── requirement: string   # 必须包含 SHALL/MUST 关键词
  ├── scenarios: Scenario[] # ≥1 个场景
  └── domain: string        # 按领域组织 (auth/, payments/, ui/)

Scenario
  ├── title: string         # 4 个 # 开头
  ├── given/when/then       # BDD 格式 (可选)
  └── verification: string

ArtifactType (schema.yaml 定义)
  ├── name: string          # proposal, spec, delta-spec, design, tasks...
  ├── dependencies: string[] # 前置 artifact
  └── ai_guidance: string    # AI agent 提示

ArtifactGraph (DAG)
  ├── nodes: ArtifactType[]
  ├── edges: dependency[]
  └── topological_order()    # Kahn's algorithm
```

### Delta 模型

```
DeltaSpec
  ├── operation: ADDED | MODIFIED | REMOVED | RENAMED
  ├── target_spec: SpecId?     # MODIFIED/REMOVED 必须引用
  ├── content: string          # MODIFIED 必须包含完整内容 (非 diff)
  └── migration: string?       # REMOVED 必须包含迁移说明
```

### 实体关系

- **Change** 包含一个 **Proposal** + 多个 **Delta Spec** + 一个 **Design** + 一个 **Tasks**
- **ArtifactGraph** 定义 artifact 创建的依赖顺序（proposal → spec → design → tasks）
- **Spec** 按 **domain** 组织（非按文件），多个 Change 可修改同一 domain 的 spec
- **Delta Spec** 引用已有 **Spec**，通过 archive 过程合并回主 spec

### Context 隔离

每个 Change 是独立的工作单元，包含自己的 proposal、specs、design、tasks。多个 Change 可并行修改同一 spec 的不同部分，通过 delta merge 避免冲突。

---

## 4. 流程与状态机

### Happy Path

```
[提案] /opsx:propose → 创建 Change 目录 + proposal.md
   ↓
[规约] /opsx:continue → 编写 delta specs (ADDED/MODIFIED/REMOVED)
   ↓  (或 /opsx:ff 一次性完成所有步骤)
[设计] /opsx:continue → 基于 specs 编写 design.md
   ↓
[任务] /opsx:continue → 将 design 拆解为 tasks.md
   ↓
[实现] 按 task 编码
   ↓
[归档] Delta specs merge 回主 spec 目录
```

### Artifact Dependency Graph (DAG)

```
proposal → spec/delta-spec → design → tasks → implementation
```

Kahn's algorithm 确保 artifact 只能在其依赖已完成时创建。例如，不能在没有 proposal 的情况下编写 spec。

### 状态转移

| 触发 | 转移 | 约束 |
|------|------|------|
| `/opsx:propose` | ∅ → Proposal created | 无前置依赖 |
| `/opsx:continue` | Proposal → Specs | Proposal 必须存在 |
| `/opsx:continue` | Specs → Design | ≥1 spec/delta-spec 必须存在 |
| `/opsx:continue` | Design → Tasks | Design 必须存在 |
| `/opsx:ff` | ∅ → Tasks | 跳过中间审核，一次性完成 |

### Failure Paths

| 失败场景 | 系统响应 |
|----------|----------|
| 缺少 SHALL/MUST 关键词 | Validation 拒绝，提示修正 |
| Scenario 格式不正确 | 要求 4 个 # 开头的标题 |
| MODIFIED delta 无完整内容 | 拒绝，要求包含完整更新内容 |
| REMOVED delta 无迁移说明 | 拒绝，要求 migration path |
| Circular dependency in graph | Kahn's algorithm 检测 → 错误 |
| 跳过 artifact 依赖 | ArtifactGraph 阻止创建 |

---

## 5. 执行保障审计

| 机制 | 级别 | 说明 |
|------|------|------|
| ArtifactGraph (Kahn's Algorithm) | **Hard** | DAG 拓扑排序强制 artifact 创建顺序 |
| Cycle Detection | **Hard** | Schema 定义中的循环依赖编译期检测 |
| SHALL/MUST Keyword Requirement | **Hard** | Validation 检查 requirement 必须包含 SHALL 或 MUST |
| Scenario Format Validation | **Hard** | 场景标题必须以 4 个 # 开头 |
| Delta Operation Completeness | **Hard** | MODIFIED 需完整内容, REMOVED 需 migration |
| Purpose/Section 完整性 | **Hard** | 空 section 检查 (Purpose, Requirements 等) |
| Profile 系统 (Core vs Custom) | **Soft** | 用户选择简单/详细模式，但可手动覆盖 |
| 三级配置 (global→project→change) | **Soft** | 配置覆盖规则由框架管理 |
| AI Guidance in Schema | **Unenforced** | Schema 中嵌入 AI 提示，但不强制 AI 遵循 |

---

## 6. Prompt 目录

### Prompt 1: Schema-Embedded AI Guidance

```yaml
# schemas/spec-driven/schema.yaml 中的 artifact type 定义
- name: spec
  dependencies: [proposal]
  ai_guidance: |
    编写需求规约时:
    - 每个 requirement 必须包含 SHALL 或 MUST 关键词
    - 每个 requirement 至少 1 个 scenario
    - 按领域组织 (auth/, payments/, ui/)
    - 使用 delta 操作 (ADDED/MODIFIED/REMOVED) 而非全量替换
```

### Prompt 2: Context Stacking

```
Slash command 执行时，自动注入:
  /opsx:propose → 仅 proposal context
  /opsx:continue (at specs) → proposal + specs context
  /opsx:continue (at design) → proposal + specs + design context
  /opsx:continue (at tasks) → proposal + specs + design + tasks context

每一阶段包含所有前置 artifact 的内容，确保 AI 的决策基于完整上下文。
```

---

## 7. 微观设计亮点

### 7.1 Delta-First 设计

传统 spec 框架要求全量替换 spec 文件，任何修改都需要重写整个文档。OpenSpec 将 delta（ADDED/MODIFIED/REMOVED/RENAMED）作为 **一等公民**——修改操作不是边缘案例，而是核心操作。这使得多个 Change 可以并行修改同一 spec 而不冲突。

### 7.2 Kahn's Algorithm 实现的 Artifact Graph

使用经典的 Kahn's algorithm 进行拓扑排序，不仅防止了 artifact 创建的乱序，还在 schema 定义时就检测循环依赖。这是一个少见的将图算法应用于 spec workflow 管理的设计。

### 7.3 Remediation Guidance in Validation Errors

校验失败时，错误信息不仅指出问题，还提供修复模板路径。例如 "Missing SHALL keyword → see templates/spec-template.md for correct format"。这降低了用户修正错误的认知成本。

---

## 8. 宏观设计亮点

### 8.1 "Brownfield-Native" 哲学

多数 spec 框架假设用户从零开始（greenfield）。OpenSpec 明确为 **brownfield 场景** 设计——通过 delta spec 机制，在现有系统上进行增量修改是框架的核心用例，而非 afterthought。

### 8.2 多 IDE Skill Generation

框架为 5 种 AI agent IDE（Claude Code、Cursor、Copilot、Continue、Cline）生成对应的 slash command。这种 "write once, generate everywhere" 策略降低了框架的 vendor lock-in 风险，也暗示了 spec framework 向 multi-agent 方向发展的趋势。

---

## 9. 失败模式与局限

| # | 失败模式 | 严重度 | 说明 |
|---|----------|--------|------|
| 1 | **Delta merge 复杂度** | 高 | 多个并行 Change 修改同一 spec 时，archive/merge 过程可能产生语义冲突（非文本冲突） |
| 2 | **Schema rigidity** | 中 | YAML schema 定义了固定的 artifact type 集合，新增自定义 artifact type 需要修改 schema |
| 3 | **SHALL/MUST 关键词形式化** | 中 | 强制使用 SHALL/MUST 对非英语团队可能不自然，缺少 i18n 支持 |
| 4 | **AI Guidance 不可靠** | 中 | Schema 中的 AI guidance 仅为 prompt hint，AI 可能忽略或误解 |
| 5 | **Artifact 膨胀** | 低 | 每个 Change 都生成完整的 artifact 集合（proposal + specs + design + tasks），小变更的 overhead 较高 |
| 6 | **单人 Change 假设** | 低 | Change 目录结构暗示单人操作，多人协作同一 Change 的流程不清晰 |

---

## 10. 迁移评估

### 可迁移候选

| 机制 | 目标插件 | 可行性 | 备注 |
|------|----------|--------|------|
| Artifact Dependency Graph | `workflows/deep-plan` | ★★★ | DAG 管理 artifact 创建顺序的模式高度可移植 |
| Delta-First Spec Evolution | `workflows/issue-driven-dev` | ★★☆ | 增量修改模式可增强 issue-flow 的变更管理 |
| Context Stacking | `integrations/code-context` | ★★☆ | 逐层叠加上下文的策略可作为 code-context 的 pattern |
| Validation Constants | `meta/plugin-optimizer` | ★★★ | SHALL/MUST 校验 + section 完整性检查可直接复用 |
| Multi-IDE Skill Generation | `meta/skill-dev` | ★★☆ | "write once, generate everywhere" 可借鉴到 skill-dev |

### 建议采纳顺序

1. **Artifact Dependency Graph** → 提取 DAG 拓扑排序逻辑为通用 workflow utility
2. **Context Stacking** → 作为 code-context 的 "progressive context injection" pattern
3. **Validation Constants** → 融入 plugin-optimizer 的 spec 质量检查

---

## 11. 开放问题

1. **Delta Archive 策略**: 多个并行 Change 的 delta 如何合并？是否有自动冲突检测？
2. **Profile 切换成本**: Core (简单) 切换到 Custom (详细) 时，已有 artifact 是否需要补充内容？
3. **Non-Spec-Driven 用例**: 除了 spec-driven 模式，是否有计划支持其他 workflow schema？
4. **版本升级兼容性**: `src/core/update.ts` 的 migration 逻辑覆盖了哪些版本？是否支持跨大版本升级？
5. **社区采纳度**: Discord 社区的活跃度如何？是否有 production 使用案例？
