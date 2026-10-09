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
  python3 1st-cc-plugin/meta/plugin-optimizer/scripts/validate-plugin.py <plugin-path>
  ```
  退出码：0 = 通过，1 = MUST 级违规，2 = token 预算超限。

- **分支策略：** `main` 是唯一的长期分支；小改动直接提交到 `main`，较大的工作在 `feat/`、`fix/` 分支完成后合并回 `main`。

- **Commit scopes：** 插件名（简写 `po` = plugin-optimizer、`cc` = Claude 配置），跨插件用 `docs`、`ci`、`release`、`marketplace`。当前插件：`enhance-prompt`, `heads-up`, `mermaid-view`, `prompt-queue`, `should-know`, `side-chat`, `tidy-chat`, `whats-next`, `plugin-optimizer`, `skill-dev`, `android`, `frontend`, `modern-android`, `swiftui`, `clarify`, `cli-design`, `github`, `jj-workflow`

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
| `integrations/enhance-prompt` | enhance-prompt | Rewrite rough user requests into clearer, implementation-ready prompts using targeted built-in codebase exploration |
| `integrations/heads-up` | heads-up | Claude Code mod: after Claude edits code, a side look at the task and the change offers one plain-language structural note above the prompt, under ⚠ 你注意到了吗？; it never enters Claude's context. |
| `integrations/mermaid-view` | mermaid-view | Claude Code mod: every ```mermaid block Claude writes is drawn as coloured box art inline in the transcript; /mermaid sets ascii, colour and sideways layout. |
| `integrations/prompt-queue` | prompt-queue | Claude Code mod: /q <text> while Claude works holds the prompt in a stack above the prompt box and sends it when the turn ends; reorder, edit, steer into the turn, or flush. |
| `integrations/should-know` | should-know | Claude Code mod: after each answered turn, a side look at the session offers one thing you should understand, explained in plain words for the reader you describe; open it, ask for simpler or deeper, or mark it known. |
| `integrations/side-chat` | side-chat | Claude Code mod: /side-chat opens a read-only side-chat pane to ask about the session so far, answered by haiku from the transcript by default (or a main-model fork); nothing goes back to the main thread. |
| `integrations/tidy-chat` | tidy-chat | Claude Code mod: draws each tool call as one compact line, keeps errors and edit diffs open, and opens a /tidy-chat pane with every call in full, a failures list, and subagents as a tree on a timeline with their prompts and answers. |
| `integrations/whats-next` | whats-next | Claude Code mod: after each reply, suggest up to 6 next steps above the prompt; tick several and Fill composes them into one detailed draft in the prompt box. |
| `meta/plugin-optimizer` | plugin-optimizer | Plugin validation and optimization — check structure, token budgets, and best practices compliance |
| `meta/skill-dev` | skill-dev | Skill/command/subagent/MCP authoring toolkit — create, optimize, test, and benchmark Claude Code extensions |
| `platforms/android` | android | Android development toolkit — Paper design-to-XML UI generation, MVI feature development, and Kotlin code review |
| `platforms/frontend` | frontend | Web frontend development toolkit — shadcn/ui, Next.js DevTools, React best practices, Supabase, DESIGN.md design system spec, and impeccable design skills |
| `platforms/modern-android` | modern-android | Modern Android & Kotlin Multiplatform skills — Compose UI, MVI presentation, data layer, Koin DI, navigation, module structure, error handling, and testing |
| `platforms/swiftui` | swiftui | SwiftUI Clean Architecture review — MVVM patterns, view composition, and iOS best practices |
| `quality/clarify` | clarify | Resolve ambiguous prompts and multi-decision specs — chat-style interviews or a brutalist HTML decision sheet |
| `quality/cli-design` | cli-design | Audit, optimize, or design shell CLI tools against clig.dev — 9 philosophy principles and 24 concrete sections covering flags, output, errors, config, interactivity, subcommands, and distribution |
| `vcs/github` | github | GitHub PR and Issue operations — create PRs with quality gates, manage issues, and run checks via gh CLI |
| `vcs/jj-workflow` | jj-workflow | Jujutsu (jj) workflow plugin — LLM-aided stack editing for jj-colocated worktrees: file-level split, multi-mode rewrite, intelligent squash, full-stack ship, op-log restore |

- 若 skill 契合某个现有插件的领域，直接添加到该插件中。
- 若开辟了全新领域且无合适归属，新建插件目录并创建 `plugin.json` 和 `SKILL.md`。

### 2. 适配 skill

- **禁止**逐字复制 vendor 内容，必须按 `1st-cc-plugin/` 规范重写。
- 遵循三层 token 预算：元数据（约 100 tokens）、指令（< 5k tokens）、资源（不限，存放于 `references/*.md`）。
- 在 `plugin.json` 中注册于 `"commands"`（用户可调用）或 `"skills"`（自动触发）。
- 遵守工具调用规范（禁用裸 `Bash`，使用限定范围的权限）。

### 3. 校验

```bash
python3 1st-cc-plugin/meta/plugin-optimizer/scripts/validate-plugin.py 1st-cc-plugin/<group>/<plugin-name>
```

### 4. 更新文档

- 更新插件自身的 `README.md`（若为新插件则创建）。
- 若插件列表或市场描述有变动，更新 `1st-cc-plugin/README.md`。

### 5. 升级版本并提交

- 在插件的 `plugin.json` 中升级版本号。
- 使用适当的 scope 提交：`feat(<scope>): add <skill-name> skill`。
