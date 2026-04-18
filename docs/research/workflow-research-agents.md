# Workflow Research: agents (wshobson/agents)

**Date**: 2026-04-18
**Source**: `vendor/agents` (https://github.com/wshobson/agents)
**Analyst mode**: Single
**Focus**: All

---

## 1. 框架概况

| 属性 | 值 |
|------|-----|
| **类型** | 插件市场（Plugin Marketplace）— 大规模 skill library + agent orchestrator |
| **总文件数** | 698 |
| **Prompt 文件** | 184 agents (.md) + 151 skills (SKILL.md) + 98 commands (.md) |
| **脚本/钩子** | 3（`run-tests.sh`, `verify-fixtures.sh`, `validate-chart.sh`） |
| **测试文件** | 12（全在 `plugins/plugin-eval/tests/`） |
| **入口** | `.claude-plugin/marketplace.json` |
| **注册机制** | marketplace.json 集中注册 → 每个 plugin 有 `plugin.json` → 内部 agents/commands/skills 按目录结构自动发现 |
| **语言** | Markdown (prompts), Python (plugin-eval), Bash (少量脚本) |

### 目录结构

```
agents/
├── .claude-plugin/marketplace.json   # 全局注册表，v1.6.0
├── CLAUDE.md                         # 项目 meta 文档（154 行）
├── README.md                         # 用户文档（19K）
├── Makefile                          # 开发工具
├── plugins/                          # 78 个插件目录
│   └── <plugin-name>/
│       ├── .claude-plugin/plugin.json
│       ├── agents/*.md               # agent prompt
│       ├── commands/*.md             # 命令 prompt
│       └── skills/<name>/SKILL.md    # skill prompt + references/
├── docs/                             # 架构/评估文档
│   ├── architecture.md
│   ├── plugin-eval.md
│   └── ...
└── tools/                            # yt-design-extractor 等工具
```

---

## 2. 源清单

### Overview Sources
| 文件 | 类型 | 价值 |
|------|------|------|
| `README.md` | 用户文档 | 安装流程、插件列表、model tier 策略 |
| `CLAUDE.md` | 开发者 meta | 仓库结构、plugin 编写规范、PluginEval 框架 |
| `docs/architecture.md` | 架构文档 | 设计原则 |

### Execution Sources
| 文件 | 类型 | 价值 |
|------|------|------|
| `plugins/*/agents/*.md` | agent prompt (184) | 每个 agent 的角色定义、工具权限、model tier |
| `plugins/*/commands/*.md` | command prompt (98) | 用户可调用的斜杠命令 |
| `plugins/*/skills/*/SKILL.md` | skill prompt (151) | 知识包，progressive disclosure |

### Prompt Sources
| 文件 | 类型 | 价值 |
|------|------|------|
| `plugins/conductor/agents/conductor-validator.md` | 验证 agent | Context-Driven Development 验证 |
| `plugins/full-stack-orchestration/agents/*.md` | 编排 agents | 多 agent 全栈开发工作流 |
| `plugins/comprehensive-review/agents/*.md` | 审查 agents | 多角度代码审查（architect + security + reviewer） |

### Enforcement Sources
| 文件 | 类型 | 价值 |
|------|------|------|
| `plugins/block-no-verify/skills/block-no-verify-hook/SKILL.md` | PreToolUse hook | 阻止 `--no-verify` 等绕过标志 |
| `plugins/signed-audit-trails/skills/*/SKILL.md` | 审计技能 | Ed25519 签名审计 + Cedar policy gate |
| `plugins/protect-mcp/test/run-tests.sh` | 测试脚本 | MCP 保护测试 |
| `plugins/plugin-eval/` | Python 评估框架 | 三层评估：Static → LLM Judge → Monte Carlo |

### Evolution Evidence
| 来源 | 类型 | 价值 |
|------|------|------|
| `marketplace.json` version 1.6.0 | 版本号 | 表明经历多次迭代 |
| `plugins/plugin-eval/tests/` (12 files) | pytest 测试 | 评估框架有自动化测试覆盖 |

---

## 3. 对象模型

### 一等实体

| 实体 | 定义位置 | 必要字段 | 生命周期 | 分类 |
|------|---------|---------|---------|------|
| **Plugin** | `plugins/*/plugin.json` | `name` | 注册 → 安装 → 加载 → 卸载 | fact |
| **Agent** | `plugins/*/agents/*.md` | `name`, `description`, `model` | 定义 → 发现 → 触发 → 执行 | fact |
| **Skill** | `plugins/*/skills/*/SKILL.md` | `name`, `description` | 定义 → 注册 → 按需激活 → 渐进加载 | fact |
| **Command** | `plugins/*/commands/*.md` | `description` | 定义 → 注册 → 用户调用 → 执行 | fact |
| **Marketplace** | `.claude-plugin/marketplace.json` | `name`, `plugins[]` | 添加 → 浏览 → 安装插件 | fact |

### 实体关系

```
Marketplace (1) ──contains──> Plugin (78)
Plugin (1) ──bundles──> Agent (0..N)
Plugin (1) ──bundles──> Command (0..N)
Plugin (1) ──bundles──> Skill (0..N)
Skill (1) ──may-ref──> references/*.md (0..N)
Agent ──declares──> model tier (opus/sonnet/haiku/inherit)
Agent ──declares──> tools (Read, Grep, Glob, Bash...)
```

### 上下文隔离策略

| 范围 | 流向 | 机制 | 证据 |
|------|------|------|------|
| Marketplace → Claude | 仅已安装 plugin 的 agents/commands/skills | 按需加载，未安装不进入上下文 | `README.md:43-46` |
| Plugin → Agent | agent frontmatter 限定工具和 model | `tools:` 字段限制可用工具 | `CLAUDE.md:32-38` |
| Skill → 上下文 | progressive disclosure：仅触发时加载知识 | SKILL.md 的 `description` 作为触发器 | `CLAUDE.md:43-57` |

---

## 4. 流程与状态机

### Happy Path

1. 用户添加 marketplace — `CLAUDE.md:1-3`
2. 浏览可用插件 — `/plugin` 命令
3. 安装所需插件 — `/plugin install <name>` — `README.md:62-80`
4. 插件加载 agents/commands/skills 到上下文 — 自动发现机制
5. 用户通过命令或对话触发 agent — agent frontmatter 中 `description` 包含触发条件
6. Agent 执行专业任务 — 使用 `tools` 字段限定的工具集
7. 必要时 skill 被渐进加载提供知识 — progressive disclosure

### 阶段转换

| From | To | 触发 | Gate? | 证据 |
|------|----|------|-------|------|
| 未安装 | 已安装 | `/plugin install` | No | `README.md:62` |
| 空闲 | 执行中 | 用户消息匹配 agent description | No | agent frontmatter `description` |
| 单 agent | 多 agent 编排 | orchestrator 插件协调 | No | `plugins/full-stack-orchestration/` |

### 失败路径

#### 失败路径 1：Token 预算溢出
安装过多插件导致上下文 token 过高。框架通过 "粒度化插件" 设计缓解但无硬性限制。

#### 失败路径 2：Agent 工具越权
Agent frontmatter 中 `tools` 字段仅是声明性的，Claude Code 平台是否强制执行取决于宿主平台实现。

### 并行

| 并行单元 | 内容 | 同步 | 证据 |
|---------|------|------|------|
| 多 agent orchestration | full-stack-orchestration 等 | 编排 agent 协调 | `plugins/full-stack-orchestration/` |

---

## 5. 执行保障审计

### 执行保障矩阵

| # | 约束 | 来源 | 等级 | 证据 | 缺口? |
|---|------|------|------|------|-------|
| 1 | 插件单一职责 | `CLAUDE.md:72-73` | Soft — 开发者规范 | 无自动化检查 | Yes |
| 2 | Agent 工具限制 | agent frontmatter `tools:` | Soft — 声明性 | 依赖宿主平台执行 | Yes |
| 3 | Model tier 分配 | agent frontmatter `model:` | Soft — 建议性 | 无强制选择机制 | Yes |
| 4 | 阻止 --no-verify | `plugins/block-no-verify/` | Hard — PreToolUse hook | 检测并阻止绕过标志 | No |
| 5 | 签名审计 | `plugins/signed-audit-trails/` | Soft — 教学 skill | Cookbook 指南，非自动执行 | Yes |
| 6 | 插件质量标准 | `plugins/plugin-eval/` | Hard — 自动评估 | pytest 测试 + 3 层评分 | No |
| 7 | Progressive disclosure | `CLAUDE.md:43-57` | Soft — 编写规范 | 无 token 预算强制 | Yes |

### 执行保障统计

| 等级 | 数量 | 百分比 |
|------|------|--------|
| Hard-enforced | 2 | 29% |
| Soft-enforced | 5 | 71% |
| Unenforced | 0 | 0% |

### 关键缺口

1. **Agent 工具隔离仅为声明性** — `tools:` 字段无法由框架本身强制执行，依赖 Claude Code 平台
2. **Token 预算无硬限制** — progressive disclosure 是规范性的，无编译时或运行时检查
3. **Model tier 不可强制** — `model:` 字段为建议性

---

## 6. Prompt 目录

### Prompt: conductor-validator

| 字段 | 值 |
|------|-----|
| **repo_path** | `plugins/conductor/agents/conductor-validator.md` |
| **quote_excerpt** | "Validates Conductor project artifacts for completeness, consistency, and correctness" |
| **stage** | 项目设置验证 |
| **design_intent** | 在实现前验证 Conductor 项目结构完整性 |
| **hidden_assumption** | 假设 `conductor/` 目录结构已标准化 |
| **likely_failure_mode** | 项目未使用 Conductor 体系时触发无意义 |
| **evidence_level** | direct |

### Prompt: deployment-engineer

| 字段 | 值 |
|------|-----|
| **repo_path** | `plugins/full-stack-orchestration/agents/deployment-engineer.md` |
| **quote_excerpt** | "Expert deployment engineer specializing in modern CI/CD pipelines, GitOps workflows, and advanced deployment automation" |
| **stage** | 全栈编排 - 部署阶段 |
| **design_intent** | 提供 CI/CD、GitOps、容器化专业知识 |
| **hidden_assumption** | 假设 Kubernetes 生态为目标平台 |
| **likely_failure_mode** | 知识面过宽导致输出泛泛，缺乏项目特定深度 |
| **evidence_level** | direct |

### Prompt: block-no-verify

| 字段 | 值 |
|------|-----|
| **repo_path** | `plugins/block-no-verify/skills/block-no-verify-hook/SKILL.md` |
| **quote_excerpt** | "PreToolUse hook that prevents AI agents from using --no-verify, --no-gpg-sign, and other bypass flags" |
| **stage** | 全局 git 操作拦截 |
| **design_intent** | 防止 AI agent 绕过 git hooks |
| **hidden_assumption** | 依赖 Claude Code PreToolUse hook 机制 |
| **likely_failure_mode** | agent 使用非标准命令格式绕过正则匹配 |
| **evidence_level** | direct |

---

## 7. 微观设计亮点

### Highlight: 三层 PluginEval 评估框架

- **观察**: 提供 Static → LLM Judge → Monte Carlo 三层评估，10 个加权维度
- **证据**: `CLAUDE.md:92-134`, `plugins/plugin-eval/`
- **价值**: 将 skill 质量从主观评价变为可量化、可重复的评分体系
- **权衡**: 第 2/3 层需要 LLM API 调用，成本和时间开销大
- **可迁移性**: Inspired — 评分维度和权重可复用，Monte Carlo 实现需适配

### Highlight: Model Tier 分层策略

- **观察**: 4 级 model 分配（Opus/Inherit/Sonnet/Haiku），按任务复杂度分配
- **证据**: `CLAUDE.md:83-89`
- **价值**: 平衡成本与质量，高风险任务用 Opus，快速操作用 Haiku
- **权衡**: 实际执行依赖宿主平台，且 model 更新后 tier 可能需重新校准
- **可迁移性**: Direct — model tier 概念直接适用于任何多 model 系统

### Highlight: PreToolUse Hook 安全防护

- **观察**: `block-no-verify` 使用 PreToolUse hook 拦截危险 git 标志
- **证据**: `plugins/block-no-verify/`
- **价值**: 唯一的真正 "硬执行" 安全机制，阻止 agent 绕过 git hooks
- **权衡**: 仅覆盖 git 命令，其他工具调用无类似防护
- **可迁移性**: Direct — PreToolUse hook 模式可直接复用

---

## 8. 宏观设计亮点

### Philosophy: 渐进披露 + 粒度化安装

- **观察**: 78 个小插件而非少数大插件，skill 仅在触发时加载知识
- **出现位置**: `README.md:38-45`, `CLAUDE.md:43-57`
- **塑造方式**: 用户按需组装工具链，token 使用最小化，每个 plugin 平均 3.6 组件
- **优势**: 避免 context 膨胀，安装体验灵活
- **局限**: 78 个插件的发现成本高，缺少推荐/依赖解析系统
- **采纳?**: Yes — 粒度化和 progressive disclosure 是成熟的模式

### Philosophy: 知识即 Prompt

- **观察**: 整个框架由 Markdown prompt 构成，无运行时代码（除 plugin-eval 外）
- **出现位置**: 全 `plugins/` 目录
- **塑造方式**: 每个 agent/skill/command 都是独立的 Markdown 文件，无依赖链
- **优势**: 零运行时依赖，版本控制简单，贡献门槛低
- **局限**: 无法在 prompt 间共享状态，无法构建动态工作流
- **采纳?**: Modify — prompt-only 适合技能库，但编排型工作流需要状态管理

---

## 9. 失败模式与局限

| # | 失败模式 | 触发 | 影响 | 证据 |
|---|---------|------|------|------|
| 1 | Context 膨胀 | 安装过多插件 | 所有 agent prompt 进入上下文 | `README.md:38`（仅声明"minimal"） |
| 2 | Agent 角色重叠 | 184 agents 间职责边界模糊 | Claude 困惑应该调用哪个 agent | 多个 plugin 覆盖相似领域 |
| 3 | 编排深度不足 | orchestrator 是 prompt-only | 无状态跟踪、无 DAG、无 gate | `plugins/full-stack-orchestration/` |
| 4 | 评估断层 | PluginEval 仅评估 skill 质量，不评估运行时效果 | 高评分 skill 实际输出可能不佳 | `CLAUDE.md:119-127` |

### 声明 vs 实际行为偏差

| 声明 | 来源 | 实际行为 | 证据 | 证据等级 |
|------|------|---------|------|---------|
| "Minimal token usage" | `README.md:38` | 安装 10+ 插件后 token 可能超 50K | 无 token 预算限制机制 | inferred |
| "Model tier strategy" | `CLAUDE.md:83-89` | model 选择为建议性，非强制 | frontmatter `model:` 无执行保障 | direct |

---

## 10. 迁移评估

### 候选机制

| # | 机制 | 评级 | 工作量 | 前提 | 风险 | 来源 |
|---|------|------|--------|------|------|------|
| 1 | PluginEval 三层评估 | Inspired | L | Python 工具链 | 维护成本 | `plugins/plugin-eval/` |
| 2 | Model Tier 分层 | Direct | S | 多 model 支持 | tier 边界模糊 | `CLAUDE.md:83-89` |
| 3 | PreToolUse Hook 防护 | Direct | S | Claude Code hook API | 覆盖范围有限 | `plugins/block-no-verify/` |
| 4 | Progressive Disclosure 模式 | Direct | S | skill 体系 | 已在用 | `CLAUDE.md:43-57` |
| 5 | 签名审计 skill | Inspired | M | Ed25519 + Cedar | 集成复杂度 | `plugins/signed-audit-trails/` |

### 推荐采纳顺序

1. **PreToolUse Hook 防护** — 低成本高价值，直接防止 agent 误操作
2. **Model Tier 分层** — 已有类似概念，可以标准化
3. **PluginEval 评分维度** — 10 个维度的权重设计值得参考
4. **签名审计** — 长期安全需求

### 不可迁移

| 机制 | 原因 | 替代方案 |
|------|------|---------|
| Marketplace 注册体系 | 依赖 Claude Code marketplace 平台功能 | 使用 plugin.json 自有注册 |
| 698 文件的插件库 | 领域覆盖面过宽，非通用需求 | 按需挑选特定领域 skill |

### 必须硬化的执行保障

| 机制 | 原始等级 | 建议等级 | 硬化方式 |
|------|---------|---------|---------|
| Token 预算 | Soft (规范) | Hard (验证脚本) | 在 validate-plugin.py 中强制 5K token 上限 |
| Agent 工具限制 | Soft (声明) | Hard (allowed-tools) | 使用 `allowed-tools` 限定范围 |

---

## 11. 开放问题

1. 78 个插件是否有依赖关系图？多个插件协作时是否有冲突检测？
2. PluginEval 在 Monte Carlo 层的成本/效益比如何？是否值得 50-100 次 LLM 调用？
3. Orchestrator 类插件（如 full-stack-orchestration）是否有实际多 agent 协作测试数据？
