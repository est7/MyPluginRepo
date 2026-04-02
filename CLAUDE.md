# CLAUDE.md

本文件为 Claude Code（claude.ai/code）在此仓库中工作时提供指导。

## 仓库用途

这是一个用于 Claude Code 插件开发的**父级 monorepo**，包含两个顶层目录：

- `1st-cc-plugin/` — 主插件市场（git submodule），所有活跃开发均在此进行。
- `vendor/` — 只读的第三方插件/工作流项目（git submodule），仅用于研究参考，禁止修改其内容。

## 在 `1st-cc-plugin/` 中工作

`1st-cc-plugin/` submodule 内有自己详细的 `CLAUDE.md`，修改前必须先阅读。要点如下：

- **插件校验：** 提交前运行：
  ```bash
  python3 1st-cc-plugin/authoring/plugin-optimizer/scripts/validate-plugin.py <plugin-path>
  ```
  退出码：0 = 通过，1 = MUST 级违规，2 = token 预算超限。

- **分支策略：** `develop` → `main`（merge commits）

- **Commit scopes：** `git`, `gitflow`, `github`, `refactor`, `review`, `doc-gen`, `swiftui`, `po`, `project-init`, `sp`, `nd`, `issue-flow`, `simple-task`, `complex-task`, `code-context`, `shadcn`, `acpx`, `docs`, `ci`, `release`, `testing`, `ai-hygiene`, `clarify`, `android`, `plan`, `catchup`, `skill-dev`

## 架构

### 插件组件模型

`1st-cc-plugin/` 中每个插件遵循三层 token 预算：
1. **元数据（约 100 tokens）：** `plugin.json` 的 name + description — 始终加载
2. **指令（< 5k tokens）：** `SKILL.md` 正文 — 触发 skill 时加载
3. **资源（不限）：** `references/*.md` 文件 — 按需通过 bash 加载

### Skill 注册

Skill 的可见性由 `plugin.json` 中的注册位置决定：
- 列在 `"commands"` 下 → 成为用户可调用的斜杠命令（如 `/git:commit`）
- 列在 `"skills"` 下 → 仅供内部使用，由 Claude 自动加载，不显示在 `/help` 中

### 插件内容的工具调用规范

| 上下文 | 规范 |
|--------|------|
| 文件操作（Read, Write, Edit, Glob, Grep） | 直接描述动作 |
| Bash 命令 | 直接描述命令，如 "Run `git diff`" |
| Skill tool | 始终明确写出："Load X skill using the Skill tool" |
| 启动 Agent | 描述即可："Launch code-reviewer agent" |

`allowed-tools` 中禁止使用裸 `Bash`，必须限定范围（如 `Bash(git:*)`）。

## Submodule 管理

```bash
# 更新所有 submodule 到已追踪的提交（浅克隆）
git submodule update --init --depth 1

# 拉取特定 submodule 远端的最新版本
git submodule update --remote vendor/<name>
```

所有 vendor submodule 在 `.gitmodules` 中设置了 `shallow = true` 以避免拉取完整历史。`vendor/` submodule 为有意锁定版本，仅在有研究需求时才应主动更新。

## 添加新 Vendor 参考（SOP）

这是更新 `1st-cc-plugin/` 前的标准准备流程。每次添加新 vendor 仓库时，按顺序执行以下步骤：

1. **添加 git submodule：**
   ```bash
   git submodule add <repo-url> vendor/<name>
   ```

2. **阅读新仓库的 README：** 了解其用途、核心工作流和主要特征。

3. **更新 `vendor/README.md`：** 将新项目添加到：
   - "At a Glance" 表格的对应分类下
   - "Detailed Summaries" 部分，包含 `Focus`、`Traits` 和 `Flow`
   - "Patterns Across the Collection" 分类
   - "Suggested Reading Order" 列表

4. **提交变更**（submodule 添加 + vendor README 更新）为单次提交。

## 移除 Vendor 参考（SOP）

当某个 vendor 仓库不再需要时，按顺序执行以下步骤：

1. **移除 git submodule：**
   ```bash
   git submodule deinit -f vendor/<name>
   git rm -f vendor/<name>
   rm -rf .git/modules/vendor/<name>
   ```

2. **更新 `vendor/README.md`：** 从以下位置移除该项目：
   - "At a Glance" 表格
   - "Detailed Summaries" 部分
   - "Patterns Across the Collection" 分类
   - "Suggested Reading Order" 列表

3. **提交变更**（submodule 移除 + vendor README 更新）为单次提交。

## 将 Skill 移植到 1st-cc-plugin（SOP）

当用户从 vendor 仓库中发现好的 skill 并希望加入 `1st-cc-plugin/` 时，按以下步骤操作：

### 1. 确定归属位置

阅读 skill 内容，理解其领域。然后对照 `1st-cc-plugin/` 中现有插件组：

| 路径 | 插件 | 描述 |
|------|------|------|
| `version-control/git` | git | Conventional Git automation and advanced repository management |
| `version-control/gitflow` | gitflow | GitFlow workflow automation for feature, hotfix, and release branches |
| `version-control/github` | github | GitHub project operations with quality gates |
| `workflows/issue-driven-dev` | issue-flow | GitLab Issue type-aware workflow for Android teams — Bug (3-stage) and Feature (4-stage) lifecycle |
| `workflows/superpower` | superpowers | Advanced development superpowers for orchestrating complex workflows with Superpower Loop integration |
| `workflows/simple-task` | simple-task | Guided workflow for simple, single-scope tasks — quick fixes, small tweaks, and straightforward changes |
| `workflows/complex-task` | complex-task | Structured workflow for complex, multi-scope tasks — new features, cross-module refactors, and architectural changes |
| `workflows/catchup` | catchup | Context gathering and handoff tools for catching up on branch changes and generating structured work summaries |
| `workflows/deep-plan` | deep-plan | Planning workflow tools — Plan/Code mode switching for moderate-complex tasks and deep analysis with review gates |
| `quality/ai-hygiene` | ai-hygiene | Detect and remove AI-generated code slop — defensive overreach, noise comments, duplicate boilerplate, and style inconsistencies |
| `quality/clarify` | clarify | Clarify ambiguous prompts and incomplete spec documents through structured interviews |
| `quality/codex-review` | codex-review | Code review via Codex CLI — auto-collects changes and task context for AI-powered review |
| `quality/meeseeks-vetted` | meeseeks-vetted | Enforces task clarity before execution and requires verified work before exit |
| `quality/project-health` | project-health | Quantitative project health analysis with multi-role debate — tech debt scoring, improvement priorities, and roadmap generation |
| `quality/refactor` | refactor | Refactor files or modules — simplify logic, remove dead code, improve cross-file consistency |
| `quality/testing` | testing | TDD workflow and testing strategy with Red-Green-Refactor gates and implementation quality checks |
| `integrations/async-agent` | async-agent | Run Claude, Codex, or Gemini tasks asynchronously via the packaged async-agent-backend binary |
| `integrations/code-context` | code-context | 5 methods to retrieve code context: DeepWiki, Context7, Exa, git clone, and web search+fetch |
| `integrations/doc-gen` | doc-gen | Office productivity skills for patent applications, PRD generation, Feishu document creation, and browser automation |
| `integrations/jetbrains` | jetbrains | JetBrains IDE MCP integration — code navigation, refactoring, inspections, and run configurations via IDE indexes |
| `integrations/mcp-services` | mcp-services | MCP service usage guides and multi-tool collaboration patterns for Context7, GitHub, Google Developer Knowledge, and more |
| `integrations/project-init` | project-init | Initialize project configuration — environment detection, AI assistant setup, TDD options, and multi-file sync |
| `integrations/utils` | utils | General-purpose utility skills for documentation, writing, and project maintenance |
| `platforms/android` | android | Android development toolkit — MVI feature development, design-to-XML UI generation, and Kotlin code review |
| `platforms/next-devtools` | next-devtools | Next.js development tools integration via MCP server |
| `platforms/shadcn` | shadcn | Manages shadcn components and projects — adding, searching, fixing, debugging, styling, and composing UI |
| `platforms/swiftui` | swiftui | SwiftUI code review with modern API best practices |
| `authoring/acpx` | acpx | Knowledge base for acpx — a headless ACP CLI for agent-to-agent communication |
| `authoring/plugin-optimizer` | plugin-optimizer | Validates and optimizes Claude Code plugins against official best practices and file patterns |
| `authoring/skill-dev` | skill-dev | Skill development toolkit for creating, optimizing, and testing Claude Code skills, commands, and MCP servers |
| `delivery/release` | release | Release management and version control automation for GitHub releases and semantic versioning |

- 若 skill 契合某个现有插件的领域，直接添加到该插件中。
- 若开辟了全新领域且无合适归属，新建插件目录并创建 `plugin.json` 和 `SKILL.md`。

### 2. 适配 skill

- **禁止**逐字复制 vendor 内容，必须按 `1st-cc-plugin/` 规范重写。
- 遵循三层 token 预算：元数据（约 100 tokens）、指令（< 5k tokens）、资源（不限，存放于 `references/*.md`）。
- 在 `plugin.json` 中注册于 `"commands"`（用户可调用）或 `"skills"`（自动触发）。
- 遵守工具调用规范（禁用裸 `Bash`，使用限定范围的权限）。

### 3. 校验

```bash
python3 1st-cc-plugin/authoring/plugin-optimizer/scripts/validate-plugin.py 1st-cc-plugin/<group>/<plugin-name>
```

### 4. 更新文档

- 更新插件自身的 `README.md`（若为新插件则创建）。
- 若插件列表或市场描述有变动，更新 `1st-cc-plugin/README.md`。

### 5. 升级版本并提交

- 在插件的 `plugin.json` 中升级版本号。
- 使用适当的 scope 提交：`feat(<scope>): add <skill-name> skill`。
