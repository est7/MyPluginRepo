# Workflow Research: dotclaude (FradSer/dotclaude)

**Date**: 2025-07-17
**Source**: `vendor/dotclaude` / `1st-cc-plugin/` (https://github.com/FradSer/dotclaude)
**Analyst mode**: Single
**Focus**: All

---

## 1. 框架概况

| 属性 | 值 |
|------|-----|
| **类型** | Claude Code 插件市场 — 15 个独立插件的 monorepo |
| **总文件数** | 357 |
| **Prompt 文件** | 15+ `SKILL.md` + 多个 `references/*.md` |
| **脚本/钩子** | Bash hooks（`task-start.sh`, `track-changes.sh`, `stop-hook.sh`）+ Python 校验脚本 |
| **测试文件** | 0 独立测试文件；校验通过 `validate-plugin.py` 实现 |
| **入口** | `.claude-plugin/marketplace.json`（主注册表），各插件 `plugin.json` |
| **注册机制** | `claude plugin install <plugin>@frad-dotclaude` |
| **语言** | Markdown + Bash + Python |

### 目录结构

```
dotclaude/
├── .claude-plugin/
│   └── marketplace.json              # 全局插件注册表
├── vcs/
│   ├── git/                          # v0.4.6 — Conventional Git 自动化
│   ├── gitflow/                      # v1.0.2 — GitFlow 工作流
│   └── github/                       # v0.2.2 — GitHub 项目操作
├── quality/
│   ├── refactor/                     # v1.5.4 — 代码重构 + Agent
│   ├── meeseeks-vetted/              # 任务明确性守卫
│   └── ...
├── workflows/
│   └── superpowers/                  # v2.1.0 — 高级工作流编排
├── integrations/
│   ├── code-context/                 # 5 种代码上下文获取方法
│   ├── utils/                        # 通用工具
│   └── ...
├── platforms/
│   ├── swiftui/                      # SwiftUI 代码审查
│   ├── shadcn/                       # shadcn UI 组件管理
│   └── next-devtools/                # Next.js 开发工具
├── meta/
│   ├── plugin-optimizer/             # v0.11.5 — 插件校验与优化
│   ├── acpx/                         # ACP CLI 知识库
│   └── ...
└── CLAUDE.md                         # 插件结构标准、开发规范
```

15 个插件分为两大类别：**development**（11 个）和 **productivity**（4 个），覆盖版本控制、代码质量、工作流编排、外部集成、平台特化和元工具等领域。

---

## 2. 源清单

### Overview Sources

| 文件 | 大小/行数 | 角色 |
|------|----------|------|
| `CLAUDE.md` | ~200+ 行 | 插件结构标准、skill 注册模型、token 预算策略、hooks 系统、开发规范 |
| `.claude-plugin/marketplace.json` | ~100 行 | 全局插件注册表 — 所有 15 个插件的元数据 |
| 各插件 `README.md` | 各 50-200 行 | 单插件功能说明与使用指南 |

### Execution Sources

| 文件 | 大小/行数 | 角色 |
|------|----------|------|
| 各插件 `plugin.json` | 各 30-80 行 | 插件元数据、commands/skills 注册、hooks 声明、allowed-tools |
| 各插件 `skills/*/SKILL.md` | 各 100-500 行 | Skill 指令正文（< 5K tokens） |
| 各插件 `references/*.md` | 各 200-2000 行 | 按需加载的详细参考资料 |
| 各插件 `agents/*.md` | 各 50-200 行 | Agent 定义（如 refactor 的 code-simplifier.md） |
| 各插件 `scripts/*.sh` | 各 20-100 行 | Hook 脚本（task-start.sh, track-changes.sh, stop-hook.sh） |

### Validation Sources

| 文件 | 大小/行数 | 角色 |
|------|----------|------|
| `meta/plugin-optimizer/scripts/validate-plugin.py` | ~500+ 行 | 插件校验脚本 — MUST 违规检测 + token 预算计算 |

### Hook Sources

| 文件 | 大小/行数 | 角色 |
|------|----------|------|
| `workflows/superpowers/scripts/task-start.sh` | ~50 行 | UserPromptSubmit hook — 任务启动时触发 |
| `workflows/superpowers/scripts/track-changes.sh` | ~80 行 | PostToolUse async hook — 异步追踪文件变更 |
| `workflows/superpowers/scripts/stop-hook.sh` | ~30 行 | Stop hook — 会话结束时触发 |

---

## 3. 对象模型

### 一等实体

| 实体 | 定义位置 | 必要字段 | 生命周期 | 分类 |
|------|---------|---------|---------|------|
| **Plugin** | `plugin.json` | name, version, description, author, license, keywords | install → configure → use | fact |
| **Skill** | `skills/*/SKILL.md` | name（文件名即 ID） | register → trigger → execute | fact |
| **Command** | `plugin.json` "commands" | name, skill reference | register → invoke via slash command | fact |
| **InternalSkill** | `plugin.json` "skills" | name, skill reference | register → auto-load by Claude | fact |
| **Agent** | `agents/*.md` | agent definition markdown | define → launch | fact |
| **Hook** | `plugin.json` "hooks" | event type, script path | register → trigger on event | fact |
| **Reference** | `references/*.md` | markdown content | create → load on demand via bash | resource |
| **Marketplace** | `.claude-plugin/marketplace.json` | plugins[] | static registry | fact |

### 三层 Token 预算模型

dotclaude 的核心设计创新在于三层 token 预算模型，这是一个经 RFC 强制的架构约束：

| 层级 | 内容 | Token 预算 | 加载时机 | 证据 |
|------|------|-----------|---------|------|
| **Level 1 — 元数据** | `plugin.json` 的 name + description | ~100 tokens | 始终加载 | CLAUDE.md |
| **Level 2 — 指令** | `SKILL.md` 正文 | < 5K tokens | 触发 skill 时加载 | CLAUDE.md, validate-plugin.py |
| **Level 3 — 资源** | `references/*.md` | 不限 | 按需通过 bash 读取 | CLAUDE.md |

此模型确保 15 个插件共存时不会因 token 溢出而相互干扰：Level 1 总计约 1500 tokens（15 × ~100），Level 2 仅在需要时加载，Level 3 完全按需。

### Skill 注册二分法

| 注册位置 | 可见性 | 使用方式 | 示例 |
|---------|--------|---------|------|
| `plugin.json` → `"commands"` | 用户可见 | 通过斜杠命令调用（如 `/git:commit`） | git 插件的 commit, review 命令 |
| `plugin.json` → `"skills"` | 用户不可见 | Claude 自动加载，不显示在 `/help` | refactor 插件的 best-practices skill |

### 实体关系

```
Marketplace (1) ──registers──> Plugin (15)
Plugin (1) ──declares──> Command (N)    # 用户可见
Plugin (1) ──declares──> InternalSkill (N)    # 内部使用
Plugin (1) ──declares──> Hook (N)
Plugin (1) ──contains──> Agent (N)
Command/InternalSkill ──points-to──> Skill (SKILL.md)
Skill (1) ──references──> Reference (N)    # 按需加载
Hook (1) ──executes──> Script (*.sh)
```

### 上下文隔离策略

| 范围 | 流向 | 机制 | 证据 |
|------|------|------|------|
| Claude → Plugin | marketplace.json 枚举 | 安装时注册 | `claude plugin install` |
| Claude → Skill | SKILL.md 加载 | trigger 时按需 | plugin.json commands/skills |
| Skill → Reference | bash 读取 | 按需加载不自动注入 | `references/*.md` |
| Hook → 文件系统 | bash script 执行 | 事件驱动异步 | `scripts/*.sh` |
| 插件间 | 无直接通信 | 各插件独立 context | 无跨插件依赖声明 |

---

## 4. 流程与状态机

### Happy Path: 插件安装与使用

1. **Install** — `claude plugin install git@frad-dotclaude` → 下载 plugin.json + 关联文件
2. **Register** — Claude 读取 plugin.json，注册 commands（斜杠命令）和 skills（内部）
3. **Load L1** — 始终加载 plugin.json 的 name + description（~100 tokens）
4. **Trigger** — 用户输入 `/git:commit` 或 Claude 自动匹配 skill
5. **Load L2** — 加载对应 `SKILL.md`（< 5K tokens）
6. **Execute** — Skill 指令引导 Claude 执行操作
7. **Load L3 (optional)** — 若需要详细参考，通过 bash 读取 `references/*.md`

### Happy Path: SuperPowers 工作流

1. **UserPromptSubmit** → `task-start.sh` 触发 — 初始化任务追踪
2. **用户下达任务** — Claude 加载 superpowers skills
3. **PostToolUse** → `track-changes.sh` 异步触发 — 追踪每次工具调用的文件变更
4. **循环执行** — Claude 使用 superpowers 的 4 commands + 4 internal skills 完成复杂工作流
5. **Stop** → `stop-hook.sh` 触发 — 会话结束收尾

### Happy Path: GitFlow 工作流

```
/gitflow:start-feature → 创建 feature/xxx 分支 → 开发 →
/gitflow:finish-feature → merge 回 develop → 清理分支

/gitflow:start-hotfix → 创建 hotfix/xxx 分支 → 修复 →
/gitflow:finish-hotfix → merge 回 main + develop → 打 tag

/gitflow:start-release → 创建 release/xxx 分支 → 准备 →
/gitflow:finish-release → merge 回 main + develop → 打 tag
```

6 个对称命令（start/finish × feature/hotfix/release）完整覆盖 GitFlow 模型。

### Happy Path: Refactor 工作流

1. **触发** — 用户请求重构或 Claude 识别重构需求
2. **加载 best-practices** — 内部 skill 自动加载重构最佳实践
3. **分析** — Claude 分析代码问题
4. **启动 code-simplifier agent** — 使用 Opus 模型的专用 agent 执行重构
5. **验证** — 2 commands 引导用户确认重构结果

### 插件校验流程

```
python3 validate-plugin.py <plugin-path>
  ├── 检查 plugin.json 必要字段 (name, version, description, author, license, keywords)
  ├── 检查 SKILL.md token 数 (< 5K)
  ├── 检查 allowed-tools 无裸 Bash
  ├── Exit 0 → PASS
  ├── Exit 1 → MUST 级违规
  └── Exit 2 → Token 预算超限
```

### Hooks 事件模型

| Hook 类型 | 触发时机 | 执行模式 | 示例 |
|----------|---------|---------|------|
| **PreToolUse** | 工具调用前 | 同步 | 命令前置校验 |
| **UserPromptSubmit** | 用户提交 prompt 时 | 同步 | `task-start.sh` |
| **PostToolUse** | 工具调用后 | 异步 | `track-changes.sh` |
| **Stop** | 会话结束时 | 同步 | `stop-hook.sh` |

---

## 5. 执行保障审计

| # | 约束 | 来源 | 等级 | 证据 | 缺口? |
|---|------|------|------|------|-------|
| 1 | Token 预算 L2 < 5K | `validate-plugin.py` | Hard — 脚本校验，Exit 2 违规 | validate-plugin.py 退出码 | No |
| 2 | plugin.json 必要字段 | `validate-plugin.py` | Hard — 脚本校验，Exit 1 违规 | name, version, description, author, license, keywords | No |
| 3 | 禁止裸 Bash | `validate-plugin.py` + CLAUDE.md | Hard — allowed-tools 校验 | 必须用 `Bash(git:*)` 等限定形式 | No |
| 4 | Skill 注册二分法 | plugin.json schema | Hard — commands vs skills 结构 | plugin.json 字段定义 | No |
| 5 | 三层加载隔离 | Claude Code runtime | Hard — 运行时按需加载 | L1 始终 / L2 触发时 / L3 按需 | No |
| 6 | Hook 事件契约 | plugin.json hooks 声明 | Hard — 事件类型匹配 | PreToolUse, UserPromptSubmit, PostToolUse, Stop | No |
| 7 | SKILL.md 指令质量 | 人工审查 | Soft — 无自动化语义校验 | 仅 token 数量校验，不检查内容质量 | Yes |
| 8 | references/ 内容准确性 | 人工维护 | Soft — 无自动化验证 | 参考资料可能过时 | Yes |
| 9 | 跨插件一致性 | CLAUDE.md 约定 | Soft — 依赖开发者遵守 | 无自动化跨插件一致性检查 | Yes |
| 10 | Agent 行为约束 | agents/*.md prompt | Unenforced — 纯 prompt 引导 | agent 可能偏离指令 | Yes |

### 执行保障统计

| 等级 | 数量 | 百分比 |
|------|------|--------|
| Hard-enforced | 6 | 60% |
| Soft-enforced | 3 | 30% |
| Unenforced | 1 | 10% |

---

## 6. Prompt 目录

### Prompt 1: SuperPowers task-start hook

| 字段 | 值 |
|------|-----|
| **repo_path** | `workflows/superpowers/scripts/task-start.sh` |
| **quote_excerpt** | 在 UserPromptSubmit 事件触发时初始化任务追踪上下文："记录当前时间、工作目录、分支信息，建立变更追踪基线" |
| **stage** | 任务启动 |
| **design_intent** | 自动建立任务执行的起始快照，为后续 track-changes 提供 diff 基线 |
| **hidden_assumption** | 用户的每次 prompt 提交对应一个独立任务单元 |
| **likely_failure_mode** | 连续多个 prompt 属于同一任务时，频繁重建基线导致追踪碎片化 |
| **evidence_level** | inferred |

### Prompt 2: plugin-optimizer validate-plugin.py

| 字段 | 值 |
|------|-----|
| **repo_path** | `meta/plugin-optimizer/scripts/validate-plugin.py` |
| **quote_excerpt** | "Check MUST-level violations: missing required fields in plugin.json (name, version, description, author, license, keywords). Count SKILL.md tokens against 5K budget. Verify allowed-tools contains no bare Bash." |
| **stage** | 插件校验 |
| **design_intent** | 在提交前自动捕获违反插件规范的错误，防止不合规插件进入市场 |
| **hidden_assumption** | 所有开发者在提交前运行校验脚本 |
| **likely_failure_mode** | 开发者跳过校验直接提交；CI 未集成校验步骤时缺少自动化保障 |
| **evidence_level** | direct |

---

## 7. 微观设计亮点

### Highlight 1: 三层 Token 预算模型

- **观察**: 通过 L1（~100 tokens 元数据，始终加载）、L2（< 5K tokens SKILL.md，触发时加载）、L3（不限 references/，按需 bash 读取）三层架构，在 15 个插件共存时将 token 消耗控制在合理范围
- **证据**: CLAUDE.md; `validate-plugin.py` Exit 2 强制执行 token 限制
- **价值**: 15 个插件的 L1 总计仅 ~1500 tokens，不会显著消耗 context window。L2 按需加载避免无关 skill 占用空间。L3 彻底解耦大量参考资料
- **权衡**: L2 的 5K token 硬限制可能对复杂 skill 造成表达压力，迫使将内容拆分至 references/
- **可迁移性**: N/A — 此即 1st-cc-plugin 的原生模型（dotclaude 是 1st-cc-plugin 的上游）

### Highlight 2: Hook 四事件模型

- **观察**: 四种 hook 事件（PreToolUse, UserPromptSubmit, PostToolUse, Stop）覆盖工具调用和会话生命周期的关键节点，支持同步和异步两种执行模式
- **证据**: SuperPowers 插件完整使用三种 hook（UserPromptSubmit → task-start.sh, PostToolUse → track-changes.sh async, Stop → stop-hook.sh）
- **价值**: 将横切关注点（任务追踪、变更监控、收尾清理）从 skill 主逻辑中解耦，通过事件驱动实现自动化
- **权衡**: async hook（如 track-changes.sh）的执行时序不可控，可能与主流程产生竞态
- **可迁移性**: N/A — 此为 Claude Code 平台原生能力

### Highlight 3: GitFlow 对称命令设计

- **观察**: 6 个命令（start-feature, finish-feature, start-hotfix, finish-hotfix, start-release, finish-release）形成完美的 3×2 对称矩阵
- **证据**: `vcs/gitflow/plugin.json` commands 注册
- **价值**: 对称性降低认知负担——用户学会 start/finish 模式后，三种分支类型的操作完全一致
- **权衡**: 对称性可能掩盖各分支类型的差异（如 hotfix 需要 cherry-pick 到 develop）
- **可迁移性**: Already ported — gitflow 已存在于 1st-cc-plugin

---

## 8. 宏观设计亮点

### Philosophy 1: Plugin-as-Skill-Container 架构

- **观察**: 每个 plugin 不是单一功能，而是一个 skill 容器——包含 commands（用户可调用）、skills（内部自动加载）、agents（专用 sub-agent）、hooks（事件处理）和 references（知识库）的完整包
- **出现位置**: CLAUDE.md 插件结构标准; 所有 15 个 plugin.json
- **塑造方式**: `plugin.json` 作为声明式清单，将异构组件（prompt、script、agent、reference）统一注册。Claude Code runtime 根据清单按需加载，开发者无需关心加载机制
- **优势**: 单一 plugin 可同时提供命令行交互、自动化 skill、专家 agent 和事件钩子，表达力极强
- **局限**: 组件类型多导致学习曲线陡；plugin.json 的声明式清单缺乏跨组件的依赖验证
- **采纳?**: N/A — 此即 1st-cc-plugin 的原生架构

### Philosophy 2: Prompt-as-Code 纪律

- **观察**: 所有 skill 指令以 Markdown 文件形式版本化管理，像代码一样经过 review、校验（validate-plugin.py）和发布。token 预算作为硬性工程约束而非建议
- **出现位置**: CLAUDE.md token 预算策略; validate-plugin.py
- **塑造方式**: 将 prompt 工程从"随意写 prompt"提升为有约束、可校验、可度量的工程实践
- **优势**: 防止 prompt 膨胀；确保可复现性；团队协作有章可循
- **局限**: 校验仅覆盖格式和 token 数量，不覆盖语义质量
- **采纳?**: N/A — 此即 1st-cc-plugin 的核心理念

---

## 9. 失败模式与局限

| # | 失败模式 | 触发 | 影响 | 证据 |
|---|---------|------|------|------|
| 1 | 无自动化测试 | 仓库 0 测试文件 | 插件回归风险完全依赖人工 review | `find . -name "test_*"` 为空 |
| 2 | 校验脚本可跳过 | 开发者不运行 validate-plugin.py | 不合规插件可能进入市场 | 无 CI 强制校验（可选配置） |
| 3 | Agent prompt 无保障 | agents/*.md 为纯文本 | Agent 可能偏离预期行为 | refactor/code-simplifier.md |
| 4 | async hook 竞态 | PostToolUse async 执行 | track-changes.sh 可能在下一工具调用后才完成 | superpowers hooks |
| 5 | 跨插件冲突 | 多插件注册相似 skill | Claude 可能加载错误的 skill | 无跨插件去重机制 |
| 6 | references/ 陈旧 | 参考资料长期不更新 | Skill 引导 Claude 使用过时信息 | 无自动过时检测 |

### 声明 vs 实际行为偏差

| 声明 | 来源 | 实际行为 | 证据 | 证据等级 |
|------|------|---------|------|---------|
| "Token budget enforced" | CLAUDE.md | 仅 L2 有硬性校验，L1 和 L3 无自动化检查 | validate-plugin.py 仅检查 SKILL.md | direct |
| "Hooks system" | CLAUDE.md | 仅 SuperPowers 使用完整 hook 链，多数插件无 hook | 各 plugin.json 对比 | direct |

---

## 10. 迁移评估

### 候选机制

| # | 机制 | 评级 | 工作量 | 前提 | 风险 | 来源 |
|---|------|------|--------|------|------|------|
| 1 | 三层 Token 预算模型 | Already adopted | — | — | — | CLAUDE.md |
| 2 | Skill 注册二分法 | Already adopted | — | — | — | plugin.json |
| 3 | Hook 四事件模型 | Already adopted | — | — | — | SuperPowers |
| 4 | GitFlow 6 命令 | Already adopted | — | — | — | vcs/gitflow/ |
| 5 | validate-plugin.py 校验 | Already adopted | — | — | — | meta/plugin-optimizer/ |
| 6 | Plugin-as-Skill-Container | Already adopted | — | — | — | 全局架构 |
| 7 | L1 token 自动校验 | Enhancement | S | 扩展 validate-plugin.py | 无 | 当前仅校验 L2 |
| 8 | CI 集成校验 | Enhancement | S | GitHub Actions | 无 | 当前校验为手动步骤 |
| 9 | 跨插件去重检测 | New | M | 全局 skill 索引 | 误报 | 无现有实现 |
| 10 | references/ 过时检测 | New | M | 内容版本戳或 checksum | 维护成本 | 无现有实现 |

### 推荐采纳顺序

dotclaude 作为 1st-cc-plugin 的上游，核心机制（#1-#6）已全部采纳。增强建议：

1. **CI 集成校验**（#8）— 在 GitHub Actions 中自动运行 validate-plugin.py，杜绝不合规插件合入
2. **L1 token 自动校验**（#7）— 扩展 validate-plugin.py 检查 plugin.json description 的 token 数
3. **跨插件去重检测**（#9）— 随插件数量增长，避免 skill 命名冲突和功能重叠
4. **references/ 过时检测**（#10）— 为长期维护提供内容新鲜度保障

---

## 11. 开放问题

1. `marketplace.json` 是否有 schema 校验？当前似乎依赖人工维护一致性。
2. SuperPowers 的 async hook（track-changes.sh）在高频工具调用场景下是否存在性能瓶颈或竞态问题？
3. 15 个插件全部安装时的实际 L1 token 消耗是否经过测量？是否存在 description 过长的插件？
4. Agent 定义（agents/*.md）是否有类似 SKILL.md 的 token 预算约束？当前似乎无限制。
5. 跨插件 skill 触发的优先级规则是什么？当多个插件的 skill trigger 条件重叠时 Claude 如何选择？
6. `claude plugin install` 的版本锁定机制如何工作？是否支持 semver range 安装？
