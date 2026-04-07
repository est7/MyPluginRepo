# Workflow Research: claude-code-specs-generator

> 逆向工程分析报告
> 目标仓库：`vendor/claude-code-specs-generator`
> 分析日期：2026-04-06
> 仓库 commit：`6b415ed` (2025-07-27)

---

## Phase 1 — 侦察与源码清单

### Framework Profile

| 属性 | 值 |
|------|-----|
| **名称** | Claude Code Specs Generator |
| **类型** | Slash command library（纯 prompt，无代码） |
| **灵感来源** | Amazon Kiro IDE 的 steering document 模式 |
| **核心理念** | 通过 6 份结构化文档向 Claude Code 注入项目上下文，提升代码生成质量 |
| **文件总数** | 5（4 command + 1 README） |
| **总行数** | 389 行 |
| **脚本/Hook** | 0 |
| **测试文件** | 0 |
| **Git 历史** | 1 次 commit，单作者 |
| **许可证** | 无正式许可证；README:153 声明 "Whatever, use it how you like it." |

### Source Inventory

| 分类 | 文件 | 行数 |
|------|------|------|
| **Overview** | `README.md` | 153 |
| **Execution** | `.claude/commands/specs-create.md` | 41 |
| **Execution** | `.claude/commands/specs-init.md` | 37 |
| **Execution** | `.claude/commands/refresh-specs.md` | 27 |
| **Execution** | `.claude/commands/update-full-specs.md` | 131 |
| **Enforcement** | （无） | — |
| **Evolution** | 单次 commit `6b415ed`，message: "updated commands and removed git workflow" | — |

### 关键发现

- 仓库极度精简：**零代码、零脚本、零测试、零 hook**。全部内容为 4 个 Markdown 格式的 Claude Code slash command。
- 唯一的 git commit 提示曾存在 git workflow 相关命令，后被移除。当前版本是精简后的稳定形态。
- 没有 `CLAUDE.md`、`settings.json`、`plugin.json` 或任何元数据注册机制——这是一个裸 `.claude/commands/` 目录项目，不是插件。

---

## Phase 2 — 对象模型与上下文策略

### 一等公民实体

本框架定义了 **2 类 6 个文档对象** 作为核心实体：

#### Steering Documents（`.claude/steering/`）

| 实体 | 定义位置 | 角色 | 对象类型 |
|------|----------|------|----------|
| `product.md` | `specs-create.md:20` | 产品愿景、用户画像、商业目标 | Fact object |
| `tech.md` | `specs-create.md:21` | 技术栈、库、约束 | Fact object |
| `structure.md` | `specs-create.md:22` | 代码组织模式、目录布局、命名约定 | Fact object |

#### Specification Documents（`specs/`）

| 实体 | 定义位置 | 角色 | 对象类型 |
|------|----------|------|----------|
| `design.md` | `specs-create.md:25` | 技术架构和实现细节 | Fact object |
| `requirements.md` | `specs-create.md:26` | 用户故事和验收标准 | Fact object |
| `tasks.md` | `specs-create.md:27` | 当前开发任务和优先级 | Fact object |

**所有 6 个实体均为 fact object** — 没有 judgment object（审查结论）或 evidence object（测试结果）。框架不产出验证产物。

### 实体生命周期

```
Creation: /specs-create → 分析代码库 → 生成 6 份文档 → 更新 CLAUDE.md
                                                          ↓
Loading:  /specs-init → /clear → /init → 加载 steering docs 到上下文
                                                          ↓
Light update: /refresh-specs → git log -10 → 增量更新 tech/structure/tasks
                                                          ↓
Full update:  /update-full-specs → 深度分析 → 更新全部 6 份文档
```

### Context Strategy

| 维度 | 策略 |
|------|------|
| **持久化方式** | 全部持久化到文件系统（`.claude/steering/` + `specs/`） |
| **上下文注入** | 通过 CLAUDE.md 引用，Claude Code 自动加载 |
| **优先级控制** | `specs-create.md:29` — "adding document references at the TOP (for maximum weight)" |
| **上下文刷新** | 通过 `/specs-init` 手动 `/clear` + `/init` 重载 |
| **上下文压缩/丢失** | 无处理机制。依赖用户手动执行 `/specs-init` |
| **隔离策略** | 无。所有 6 份文档同时加载到同一上下文窗口 |

### Context Flow

```
┌──────────────────────────────────────────┐
│ 用户项目代码库                              │
│   ├── 源代码、package.json、git history    │
│   └── 现有文档 (PRD.md, TODO.md...)        │
└──────────────┬───────────────────────────┘
               │ /specs-create 分析
               ▼
┌──────────────────────────────────────────┐
│ 6 份结构化文档                              │
│   ├── .claude/steering/{product,tech,structure}.md │
│   └── specs/{design,requirements,tasks}.md │
└──────────────┬───────────────────────────┘
               │ CLAUDE.md 引用 (top-of-file)
               ▼
┌──────────────────────────────────────────┐
│ Claude Code 会话上下文                      │
│   每次交互自动加载 steering docs            │
└──────────────────────────────────────────┘
```

**关键设计决策**：框架选择 **文件持久化 + CLAUDE.md 引用** 而非对话内 prompt。优势是跨会话持久；劣势是 token 消耗随文档增长不可控。

---

## Phase 3 — 流程与状态机分析

### 工作流状态机

框架定义了 4 个操作，形成一个简单的生命周期：

```
[无文档] ──/specs-create──→ [已生成] ──/specs-init──→ [已加载]
                                          │
                              ┌───────────┤
                              │           │
                     /refresh-specs   /update-full-specs
                              │           │
                              └───────────┤
                                          ▼
                                      [已更新] ──/specs-init──→ [已加载]
```

### Happy Path

1. 用户在新项目中运行 `/specs-create`
2. Claude 分析代码库（`specs-create.md:13-17`）：架构、技术栈、现有文档
3. Claude 生成 6 份文档到 `.claude/steering/` 和 `specs/`（`specs-create.md:19-27`）
4. Claude 更新 CLAUDE.md，在顶部添加文档引用（`specs-create.md:29`）
5. 用户运行 `/specs-init`（`specs-init.md:9`）：`/clear` → `/init`
6. Claude 确认加载了 6 份文档（`specs-init.md:17-24`）
7. 日常维护：`/refresh-specs` 或 `/update-full-specs` → 再次 `/specs-init`

### Failure Path 1 — 文档不被识别

触发条件：Claude 未确认加载文档。
处理：`specs-init.md:33-37` 给出排查步骤：

1. 验证文件存在
2. 检查 CLAUDE.md 引用
3. 尝试 `/clear` + `/init`
4. 手动用 `@` 引用具体文件

**评估**：这是文档级的故障排除指南，**没有自动化恢复机制**。

### Failure Path 2 — tasks.md Token 膨胀

触发条件：tasks.md 无限增长导致 token 预算超支。
处理：`specs-create.md:41` 和 `README.md:131-132` 建议 "Keep tasks.md manageable" 和 "Regularly archive completed tasks"。

**评估**：纯建议，**无自动归档或大小检查**。

### 并行与门控

- **无并行执行**：4 个命令均为顺序执行
- **无质量门控**：没有任何命令包含验证步骤（校验生成文档是否准确、是否与代码一致）
- `update-full-specs.md:87-95` 包含一个 **Markdown checkbox 清单**，但这是给 Claude 的自检提示，非强制门控

---

## Phase 4 — 执行力审计

### Enforcement Matrix

| # | 约束/声明 | 来源 | 执行级别 | 证据 |
|---|----------|------|----------|------|
| 1 | 生成 6 份结构化文档 | `specs-create.md:6-8` | **Soft-enforced** | 仅 prompt 指令，无校验脚本检查文件是否真的被创建 |
| 2 | CLAUDE.md 引用放在文件顶部 | `specs-create.md:29` | **Soft-enforced** | prompt 说 "at the TOP (for maximum weight)"，但无代码验证位置 |
| 3 | 保持 tasks.md 可控大小 | `specs-create.md:41`, `README.md:131` | **Unenforced** | 两处提及，但无大小检查、无自动归档 |
| 4 | 更新时检查 git log | `refresh-specs.md:8-9` | **Soft-enforced** | prompt 指示 `git log --oneline -10`，Claude 可能执行也可能跳过 |
| 5 | 更新时检查 package.json | `refresh-specs.md:10` | **Soft-enforced** | 同上 |
| 6 | 文档间交叉引用一致性 | `update-full-specs.md:82-83` | **Soft-enforced** | 列在 checklist 中，但无自动验证 |
| 7 | 技术细节与实现一致 | `update-full-specs.md:88` | **Soft-enforced** | checklist item，无代码比对机制 |
| 8 | `/specs-init` 清除旧上下文 | `specs-init.md:9` | **Soft-enforced** | 依赖 `/clear` 命令的正确执行，框架本身不验证 |
| 9 | 文档覆盖当前架构变更 | `update-full-specs.md:11-15` | **Soft-enforced** | prompt 列出分析步骤，但 Claude 可能遗漏 |

### 审计结论

- **Hard-enforced**: 0 个
- **Soft-enforced**: 8 个
- **Unenforced**: 1 个

**100% 依赖 prompt compliance**。框架没有任何代码层面的强制执行机制。这是设计选择而非缺陷——因为框架本质是 prompt library，不是软件系统。但这意味着每一个 "步骤" 的执行都取决于 Claude 的解释和遵从度。

---

## Phase 5 — Prompt Catalog 与设计分析

### 5A. Prompt Catalog

#### P1: `/specs-create`

| 字段 | 内容 |
|------|------|
| **role** | 文档生成器（Document generator） |
| **repo_path** | `.claude/commands/specs-create.md` |
| **quote_excerpt** | "Generate Kiro IDE-style steering and specification documents to improve Claude Code's context awareness and code generation accuracy." (`specs-create.md:2`) |
| **stage** | 初始化（一次性） |
| **design_intent** | 通过分析代码库自动生成完整的项目文档集 |
| **hidden_assumption** | 代码库已经有足够的结构（package.json, 目录结构, 现有文档）供 Claude 分析。对于空项目或极简项目，分析可能产出空泛内容。 |
| **likely_failure_mode** | Claude 生成的文档内容与实际代码库不一致（幻觉）；无校验机制检测准确性。 |

#### P2: `/specs-init`

| 字段 | 内容 |
|------|------|
| **role** | 上下文加载器（Context loader） |
| **repo_path** | `.claude/commands/specs-init.md` |
| **quote_excerpt** | "Clears Claude's working memory to start fresh" / "Loads all 6 steering and specification documents into context" (`specs-init.md:12-13`) |
| **stage** | 每次上下文重载 |
| **design_intent** | 强制 Claude 读取最新文档，避免使用过时上下文 |
| **hidden_assumption** | `/clear` + `/init` 能可靠地刷新上下文。实际上 Claude Code 的 `/init` 只是重新读取 CLAUDE.md，不保证所有引用文件被完整加载到上下文窗口。 |
| **likely_failure_mode** | 文档总 token 超过上下文窗口，Claude 默默截断；用户不知道哪些文档实际被加载。 |

#### P3: `/refresh-specs`

| 字段 | 内容 |
|------|------|
| **role** | 增量更新器（Incremental updater） |
| **repo_path** | `.claude/commands/refresh-specs.md` |
| **quote_excerpt** | "Check last 10 commits: `git log --oneline -10`" / "Review modified files: `git diff --name-status HEAD~5..HEAD`" (`refresh-specs.md:8-9`) |
| **stage** | 日常维护 |
| **design_intent** | 轻量级更新，仅同步近期变更 |
| **hidden_assumption** | 最近 10 个 commit / 5 个 commit 的 diff 足以覆盖所有相关变更。 |
| **likely_failure_mode** | 对于频繁提交的项目，10 个 commit 窗口太小；对于大型 monorepo，`git diff --name-status` 输出可能非常长。 |

#### P4: `/update-full-specs`

| 字段 | 内容 |
|------|------|
| **role** | 全量更新器（Full updater） |
| **repo_path** | `.claude/commands/update-full-specs.md` |
| **quote_excerpt** | "Systematically review the current codebase state and update all documentation files to reflect the current architecture, features, and development status." (`update-full-specs.md:6`) |
| **stage** | 里程碑后 |
| **design_intent** | 深度同步所有文档与代码库现状 |
| **hidden_assumption** | Claude 能准确理解并反映整个代码库的当前状态。对于大型项目，这可能需要超过上下文窗口能处理的信息量。 |
| **likely_failure_mode** | 文档更新时引入不准确信息（幻觉），因为 Claude 无法一次性读取整个大型代码库。自检 checklist（`update-full-specs.md:87-95`）依赖 Claude 自我审查，缺乏独立验证。 |

### 5B. Design Highlights — Micro

#### Micro-1: 6 文档模型的清晰分层

**观察**：steering docs（`.claude/steering/`）与 spec docs（`specs/`）的分离。

**证据**：`README.md:9-17` 和 `specs-create.md:19-27` 明确定义两层：
- Steering = 长期稳定的项目方向（产品、技术、结构）
- Specs = 短期变化的实现细节（设计、需求、任务）

**意义**：这种分层允许对不同生命周期的文档采用不同的更新频率。steering docs 较少变化，specs 频繁更新。

**可迁移性**：高。这种分层模型可以直接适配到任何文档管理系统。

#### Micro-2: CLAUDE.md Top-of-File 优先级策略

**观察**：文档引用放在 CLAUDE.md 文件顶部。

**证据**：`specs-create.md:29` — "Update CLAUDE.md by adding document references at the TOP (for maximum weight)"

**意义**：利用 Claude Code 处理 CLAUDE.md 时对文件开头内容赋予更高权重的行为特征。这是对 Claude Code 内部机制的实战经验。

**可迁移性**：中。这依赖 Claude Code 的具体实现行为，可能随版本变化。

#### Micro-3: 4 命令分级更新策略

**观察**：`/specs-create`（全量初始化）→ `/refresh-specs`（轻量更新）→ `/update-full-specs`（深度更新）→ `/specs-init`（上下文重载）形成了完整的文档生命周期。

**证据**：
- `README.md:31-84` 描述 4 个命令的使用场景
- `refresh-specs.md:27` — "Use `/update-docs` for comprehensive updates. Use this command for routine maintenance after smaller changes."

**意义**：用户可以根据变更规模选择合适的更新粒度，避免每次都做全量更新。

**可迁移性**：高。分级更新策略是通用模式。

#### Micro-4: `update-full-specs` 内嵌自检清单

**观察**：最复杂的命令包含 8 项 checklist。

**证据**：`update-full-specs.md:87-95`：
```
- [ ] All steering documents reflect current product state
- [ ] All spec documents align with implemented features
...
- [ ] CLAUDE.md context loading directives are accurate
```

**意义**：这是框架中最接近 "质量门控" 的机制，虽然执行仍依赖 Claude 自律。

**可迁移性**：中。checklist 设计好，但缺少可自动验证的 assertion。

### 5C. Design Highlights — Macro

#### Macro-1: Process-as-Prose 纯粹主义

**观察**：整个框架 = 4 个 Markdown 文件。零代码、零脚本、零 hook。

**证据**：仓库文件列表显示仅有 `.claude/commands/*.md` 和 `README.md`，总计 389 行。

**意义**：这代表了 Claude Code 工具生态中一个极端——**完全信任 LLM 的 prompt compliance**。优势是零依赖、零维护成本、极低入门门槛。劣势是无法保证任何行为的一致性。

**可迁移性**：框架本身不可直接迁移（因为它本质是 prompt，迁移 = 复制粘贴）。但其文档模型值得借鉴。

#### Macro-2: 无 Evaluator Separation

**观察**：文档由 Claude 生成，也由 Claude 自检。没有独立审查者角色。

**证据**：
- `specs-create.md` — Claude 分析代码库并生成文档，无审查步骤
- `update-full-specs.md:87-95` — 自检 checklist 由执行者自己完成

**意义**：这违反了 "evaluator separation" 原则。自我审查的准确性天然受限于生成者的能力和偏见。

**可迁移性**：作为反面教材有参考价值。

#### Macro-3: 无 Human Approval Checkpoint

**观察**：4 个命令中没有任何一个需要用户在中间步骤确认。

**证据**：所有命令的流程都是线性执行：分析 → 生成/更新 → 完成。无 "请确认以下更改" 步骤。

**意义**：提高了执行效率，但增加了 Claude 引入不准确内容的风险。对于重要的项目文档（如产品愿景、技术约束），自动覆写可能是危险的。

**可迁移性**：作为设计警示有价值。关键文档更新应有人工审查门控。

#### Macro-4: Verification-over-Self-Report — 缺失

**观察**：框架信任 Claude 的自我报告，不做独立验证。

**证据**：
- `specs-init.md:17` — 验证方式是 "ask Claude to list loaded steering docs"，即让 Claude 自己声称加载了什么
- `update-full-specs.md:88` — "Ensure all technical details match implementation" 由 Claude 自己判断

**意义**：这是 soft enforcement 的典型弱点。如果 Claude 声称 "已更新所有文档" 但实际遗漏了某些，用户无法从流程中发现。

### 5D. Cross-Cutting Interconnections

| 维度 | 分析 |
|------|------|
| **Prompt ↔ Skill** | 4 个 command 互相引用但不 chain。`specs-create.md:39` 引用 `/clear` + `/init`；`refresh-specs.md:27` 引用 `/update-docs`。无自动链式调用。 |
| **Gate ↔ Flow** | 无质量门控。`update-full-specs.md:87-95` 的 checklist 是最接近 gate 的东西，但非阻塞。 |
| **Review ↔ Test** | 无审查、无测试。验证方式 = 用户手动检查文档内容。 |
| **Context ↔ Scope** | 无 token 预算管理。`specs-create.md:41` 仅建议 "Keep tasks.md manageable"。无大小上限。 |
| **Error ↔ Recovery** | `specs-init.md:33-37` 提供排查步骤。其他命令无错误处理。 |

---

## Phase 6 — 迁移评估

### 迁移候选清单

| # | 机制 | 可迁移性 | 工作量 | 前置条件 | 风险 | 观察到的失败模式 |
|---|------|----------|--------|----------|------|-----------------|
| M1 | **6 文档模型**（3 steering + 3 spec） | **Inspired** | S | 无 | 文档模板可能需要针对不同项目类型调整 | 生成内容可能空泛或不准确（幻觉风险） |
| M2 | **Steering/Spec 分层策略** | **Direct** | S | 插件需要支持多文档生成 | 低 | 用户可能不理解两层的区别 |
| M3 | **CLAUDE.md Top-of-File 引用注入** | **Direct** | S | 目标项目使用 Claude Code | 依赖 Claude Code 内部实现行为 | Claude Code 版本更新可能改变优先级机制 |
| M4 | **分级更新策略**（light/full/reload） | **Inspired** | M | 需要 git integration | 低 | `refresh-specs` 的 10 commit 窗口对大项目不足 |
| M5 | **自检 Checklist 模式** | **Inspired** | S | 无 | 自检 = 自我审查，准确性有限 | Claude 可能声称通过但实际遗漏 |
| M6 | **从现有文档导入**（PRD.md, TODO.md） | **Direct** | S | 检测常见文档文件名 | 低 | 导入逻辑依赖文件名约定 |

### 重点迁移建议

#### M1 — 6 文档模型 → 1st-cc-plugin 的 `project-init` 或新 `specs-gen` 插件

**价值**：为项目建立结构化上下文，解决 Claude Code "对项目缺乏深度理解" 的常见问题。

**改造要点**：
1. 将 4 个裸 command 转为插件 skill，添加 frontmatter、scoped `allowed-tools`
2. **增加校验**：生成文档后运行 assertion（文件是否存在、非空、包含必要 section）
3. **增加人工审查门控**：关键文档（product.md, tech.md）生成后 `AskUserQuestion` 确认
4. **Token 预算管理**：对 tasks.md 设置行数上限，超限时自动提醒归档
5. **独立验证**：更新后交叉检查文档声明与代码库实际状态

#### M4 — 分级更新策略

**价值**：避免每次都全量重新分析。

**改造要点**：
- `refresh` 命令的 git 窗口应可配置，而非硬编码 10/5 commit
- `update-full` 应支持分段分析（大型代码库无法一次读完），添加进度追踪

---

## 失败模式清单

| # | 失败模式 | 维度 | 严重程度 | 证据 |
|---|----------|------|----------|------|
| F1 | **幻觉风险**：Claude 生成不准确的项目文档 | 准确性 | **高** | 无校验机制；`specs-create.md` 完全信任 Claude 的分析结果 |
| F2 | **Token 膨胀**：6 份文档 + CLAUDE.md 可能占用大量上下文窗口 | 资源 | **中** | `specs-create.md:41` 仅建议控制 tasks.md 大小，无其他限制 |
| F3 | **陈旧文档**：用户忘记运行更新命令，文档与代码库脱节 | 一致性 | **中** | 无 hook 自动触发更新；完全依赖用户手动执行 |
| F4 | **自检失效**：`update-full-specs.md` 的 checklist 由生成者自己验证 | 可靠性 | **中** | `update-full-specs.md:87-95`，evaluator = implementer |
| F5 | **CLAUDE.md 覆写风险**：`specs-create` 修改用户的 CLAUDE.md | 安全性 | **中** | `specs-create.md:29`，自动在顶部添加引用，可能破坏用户现有配置 |
| F6 | **上下文加载不可验证**：`/specs-init` 无法确认哪些文档实际进入上下文 | 可观测性 | **低** | `specs-init.md:17-24`，验证方式是让 Claude 自我报告 |
| F7 | **大型项目不适配**：`refresh-specs` 的 10 commit 窗口和 `update-full-specs` 的全库扫描均不适合大型 monorepo | 可扩展性 | **低** | `refresh-specs.md:8-9`，`update-full-specs.md:58-59` |

---

## 总结

### 框架定位

`claude-code-specs-generator` 是一个**极简的 prompt library**，核心价值在于提出了 **"6 文档模型"** 的结构化上下文管理思路，灵感来自 Amazon Kiro IDE。它不是一个工程化的工具或框架，而是 4 个 Claude Code slash command，共 389 行 Markdown。

### 核心价值

1. **文档分层模型**（steering vs specs）清晰有效
2. **分级更新策略**（create → refresh → full-update → reload）实用合理
3. **零依赖、零配置**的极简入门体验

### 核心缺陷

1. **零 enforcement** — 所有行为依赖 prompt compliance
2. **零验证** — 生成内容的准确性无法保证
3. **零自动化** — 无 hook 触发文档更新，完全依赖用户主动
4. **零审查分离** — 生成者 = 审查者

### 对 1st-cc-plugin 的启示

该项目的 6 文档模型值得以 **Inspired** 方式移植——保留分层文档思路，但必须增加校验、人工门控和 token 预算管理。推荐整合到现有 `integrations/project-init` 插件中，作为 project context bootstrapping 功能的一部分。
