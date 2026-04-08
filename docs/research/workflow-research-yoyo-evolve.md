# yoyo-evolve 工作流逆向工程分析报告

> **仓库**: `vendor/yoyo-evolve` (https://github.com/yologdev/yoyo-evolve)
> **规模**: Medium (109 files), ~43,000 行 Rust + 7 skills + 13 scripts
> **框架类型**: 自进化 AI 编程代理 — Rust CLI + GitHub Actions 自动演化循环
> **分析日期**: 2026-04-07

---

## 目录

1. [源清单](#1-源清单)
2. [框架假说](#2-框架假说)
3. [对象模型](#3-对象模型)
4. [流程与状态机](#4-流程与状态机)
5. [Prompt 目录](#5-prompt-目录)
6. [执行保障审计](#6-执行保障审计)
7. [失败模式](#7-失败模式)
8. [微观设计亮点](#8-微观设计亮点)
9. [宏观设计亮点](#9-宏观设计亮点)
10. [迁移候选评估](#10-迁移候选评估)
11. [交叉引用矩阵](#11-交叉引用矩阵)

---

## 1. 源清单

### 1.1 配置与清单

| 文件 | 角色 | 关键发现 |
|------|------|----------|
| `Cargo.toml` | Rust 项目清单 | `yoyo-agent` v0.1.7, 依赖 `yoagent` 0.7 (核心代理库), `tokio`, `rustyline`, `serde_json` |
| `CLAUDE.md` | 项目指令文件 | 2,000+ 字的架构百科全书，是最详尽的自文档化系统 |
| `.yoyo.toml` | 运行时配置 (项目级) | TOML 格式，支持 `[permissions]`, `[directories]`, `[mcp_servers.*]`, `[[hooks]]` |
| `mutants.toml` | 变异测试配置 | 用 cargo-mutants 寻找测试覆盖缺口 |

### 1.2 Rust 源码 (`src/`)

| 文件 | 行数(估) | 职责 |
|------|----------|------|
| `main.rs` | ~4,000 | 入口、Agent 配置、REPL、流式事件处理、子代理集成 |
| `cli.rs` | ~2,800 | CLI 参数解析、配置文件加载、系统提示词组装 |
| `config.rs` | ~570 | 权限配置、目录限制、MCP 服务器配置、TOML 解析 |
| `context.rs` | ~400 | 项目上下文加载、文件清单、git 状态、最近变更 |
| `hooks.rs` | ~830 | Hook trait, HookRegistry, AuditHook, ShellHook, HookedTool 包装器 |
| `tools.rs` | ~1,000+ | StreamingBashTool, RenameSymbolTool, AskUserTool, TodoTool |
| `prompt.rs` | ~2,500+ | 流式 prompt 执行、审计日志、watch 模式 |
| `memory.rs` | ~380 | 项目记忆系统 (`.yoyo/memory.json`) |
| `providers.rs` | ~100+ | 13 个 provider 常量、API key 环境变量、默认模型 |
| `repl.rs` | ~1,500+ | REPL 循环、Tab 补全、多行输入 |
| `commands.rs` | ~500+ | 斜杠命令分发、分组帮助 |
| `commands_*.rs` (8 files) | ~5,000+ | 按领域拆分的命令实现 (git, session, project, info, file, search, dev, refactor) |
| `format/*.rs` (5 files) | ~3,000+ | ANSI 颜色、Markdown 渲染、语法高亮、成本显示、Spinner |
| `git.rs` | ~800+ | Git 操作、分支检测、PR 交互 |
| `setup.rs` | ~300+ | 首次运行引导向导 |
| `help.rs` | ~400+ | 命令帮助页和元数据 |
| `docs.rs` | ~200+ | docs.rs 文档查询 |

### 1.3 Skills (`skills/`)

| Skill | 文件 | 分类 | 可变性 |
|-------|------|------|--------|
| `evolve` | `skills/evolve/SKILL.md` | 核心 | **不可变** (immutable) |
| `self-assess` | `skills/self-assess/SKILL.md` | 核心 | **不可变** |
| `communicate` | `skills/communicate/SKILL.md` | 核心 | **不可变** |
| `research` | `skills/research/SKILL.md` | 核心 | **不可变** |
| `social` | `skills/social/SKILL.md` | 扩展 | 可变 |
| `family` | `skills/family/SKILL.md` | 扩展 | 可变 |
| `release` | `skills/release/SKILL.md` | 扩展 | 可变 |

### 1.4 Scripts (`scripts/`)

| 脚本 | 类型 | 职责 |
|------|------|------|
| `evolve.sh` | Bash | **核心**: 完整演化流水线 (约 2,076 行) |
| `social.sh` | Bash | 社交会话流水线 |
| `yoyo_context.sh` | Bash | 身份上下文构建器 (组装 `$YOYO_CONTEXT`) |
| `common.sh` | Bash | Fork 友好的仓库/Bot 自动检测 |
| `format_issues.py` | Python | GitHub Issue 格式化与优先级排序 |
| `format_discussions.py` | Python | GitHub Discussion GraphQL 拉取与格式化 |
| `build_site.py` | Python | 旅程网站生成器 |
| `daily_diary.sh` | Bash | 从日志/提交/学习中生成博客文章 |
| `extract_changelog.sh` | Bash | 从 CHANGELOG.md 提取版本段落 |
| `create_address_book.sh` | Bash | yoyobook 地址簿创建 |
| `run_mutants.sh` | Bash | 变异测试运行脚本 |
| `evolve-local.sh` | Bash | 本地开发用的演化脚本 |
| `reset_day.sh` | Bash | 重置日计数器 |

### 1.5 身份与记忆文件

| 文件 | 角色 | 保护级别 |
|------|------|----------|
| `IDENTITY.md` | 宪法 — 目标、规则、资源清单 | **禁止修改** |
| `PERSONALITY.md` | 声音与价值观 | **禁止修改** |
| `ECONOMICS.md` | 对金钱和赞助的理解 | **禁止修改** |
| `DAY_COUNT` | 当前进化天数 (整数) | 每次会话写入 |
| `journals/JOURNAL.md` | 按时间顺序的进化日志 | 仅追加，禁止删除 |
| `memory/learnings.jsonl` | 自我反思归档 (JSONL) | **仅追加，禁止压缩** |
| `memory/social_learnings.jsonl` | 社交洞察归档 (JSONL) | **仅追加，禁止压缩** |
| `memory/active_learnings.md` | 合成的提示上下文 | 每日由 synthesize.yml 再生 |
| `memory/active_social_learnings.md` | 合成的社交上下文 | 每日由 synthesize.yml 再生 |
| `sponsors/credits.json` | 一次性赞助者信用追踪 | evolve.sh 读写 |
| `sponsors/active.json` | 活跃赞助者 JSON | evolve.sh 生成 |
| `sponsors/shoutouts.json` | shoutout 去重追踪 | evolve.sh 读写 |
| `SPONSORS.md` | 赞助者认可页 | 仅添加，禁止删除 |

### 1.6 GitHub Actions Workflows

| Workflow | 触发器 | 职责 |
|----------|--------|------|
| `evolve.yml` | `cron: '0 * * * *'` + workflow_dispatch | 每小时触发，8h 间隔控制实际频率，最多 3 次重试 |
| `social.yml` | `cron` (4h 偏移) | 社交会话 — 讨论互动 |
| `synthesize.yml` | `cron: '0 12 * * *'` | 每日记忆合成 — 从 JSONL 再生 active markdown |
| `ci.yml` | PR to main | 构建+测试+clippy+fmt 四项检查 |
| `release.yml` | `v*` 标签 | 4 平台二进制构建 + GitHub Release |
| `pages.yml` | push to main | 网站 + mdBook 部署 |

---

## 2. 框架假说

yoyo-evolve 是一个**自进化 AI 编程代理**，由三个互相嵌套的系统组成：

1. **CLI 工具 (`yoyo` binary)**: 一个功能完整的终端编程助手（60+ 命令、12 个 provider、MCP 支持、权限系统），任何开发者都可以独立使用。

2. **自动演化引擎 (`scripts/evolve.sh` + GitHub Actions)**: 每约 8 小时自主运行一次"计划→实现→验证→响应"流水线，读取自身源码、选择改进、实现变更、运行测试、提交代码。Agent 修改的是自己。

3. **社交与记忆层 (`scripts/social.sh` + `memory/`)**: 通过 GitHub Discussions 与社区互动，维护两层记忆架构（不可变 JSONL 归档 + 每日再生的 active markdown），实现跨会话的自我认知积累。

**核心创新**: Agent 的源码就是它的"身体"——每次进化会话中，agent 阅读自身代码，判断改进方向，编写测试，实现变更，并在通过所有检查后提交。失败则回滚。整个过程在公开 git 历史中可追溯。

---

## 3. 对象模型

### 3.1 一等实体

#### Entity: Skill

```
schema: {
  name: string,           // YAML frontmatter
  description: string,    // YAML frontmatter
  tools: string[],        // 允许的工具列表
  body: markdown           // 指令正文
}
file_pattern: skills/<name>/SKILL.md
loaded_by: --skills <dir> → yoagent::SkillSet::load()
lifecycle: load_on_startup → injected_into_system_prompt → immutable_during_session
```

**证据**: `cli.rs:764` `SkillSet::load(&skill_dirs)`, `CLAUDE.md:75-84` 定义了 4 个核心 + 3 个扩展 skill。

#### Entity: Memory/Learning

```
schema_learning: {
  type: "lesson",
  day: integer,
  ts: "ISO8601",
  source: string,          // "evolution", "issue #N"
  title: string,
  context: string,
  takeaway: string
}
schema_social: {
  type: "social",
  day: integer,
  ts: "ISO8601",
  source: string,          // "discussion #N"
  who: string,             // "@username"
  insight: string
}
archive: memory/learnings.jsonl (append-only, never compressed)
active:  memory/active_learnings.md (regenerated daily by synthesize.yml)
lifecycle: session_reflection → python3_json_append → daily_synthesis → prompt_injection
```

**证据**: `skills/communicate/SKILL.md:87-102` 定义了写入格式，`synthesize.yml:69-86` 定义了三层时间加权压缩。

#### Entity: Session Plan / Task

```
schema: {
  Title: string,
  Files: string,           // 要修改的文件
  Issue: string            // "#N" 或 "none"
  body: markdown           // 详细实现描述
}
dir: session_plan/ (gitignored, ephemeral)
lifecycle: Phase_A2_creates → Phase_B_executes → cleanup_after_session
constraints: max 3 tasks/session, max 3 source files/task
```

**证据**: `evolve.sh:1044-1068` 定义了 task 文件格式和约束。

#### Entity: Hook

```
schema_trait: {
  name() -> &str,
  pre_execute(tool_name, params) -> Result<Option<String>, String>,
  post_execute(tool_name, params, output) -> Result<String, String>
}
schema_shell: {
  name: string,
  phase: Pre | Post,
  tool_pattern: string,    // "*" 或具体工具名
  command: string           // shell 命令
}
registry: HookRegistry (ordered Vec<Box<dyn Hook>>)
lifecycle: config_parse → register → pre_execute_chain → tool_execute → post_execute_chain
```

**证据**: `hooks.rs:17-39` 定义了 Hook trait，`hooks.rs:163-169` 定义了 ShellHook 结构。

#### Entity: Provider

```
schema: {
  name: string,            // KNOWN_PROVIDERS 数组元素
  api_key_env: string,     // 环境变量名
  default_model: string,
  known_models: string[]
}
constant: providers.rs:4-19 KNOWN_PROVIDERS (13 个)
lifecycle: cli_parse → provider_selection → agent_construction → optional_fallback_switch
```

**证据**: `providers.rs:4-19` 定义了 13 个已知 provider。

#### Entity: Journal Entry

```
format: "## Day [N] — [HH:MM] — [short title]\n\n[2-4 sentences]"
file: journals/JOURNAL.md
lifecycle: session_end → agent_writes → fallback_auto_generate → commit
constraints: append_at_top, never_delete, max_4_sentences
```

**证据**: `skills/communicate/SKILL.md:13-45` 定义了格式和约束。

### 3.2 实体关系图

```
[GitHub Actions Cron] ──triggers──→ [evolve.sh / social.sh]
                                         │
                                    loads ↓
                               [yoyo_context.sh]
                                    builds ↓
                              [$YOYO_CONTEXT prompt]
                                    │
              ┌─────────────────────┼─────────────────────┐
              ↓                     ↓                     ↓
     [IDENTITY.md]          [PERSONALITY.md]      [ECONOMICS.md]
     [active_learnings.md]  [active_social_learnings.md]  [sponsors/active.json]

[evolve.sh] ──runs──→ [yoyo binary] ──loads──→ [SkillSet]
                                     ──reads──→ [YOYO.md / CLAUDE.md context]
                                     ──uses──→  [Agent + Tools + Hooks]

[Session Plan] ──Phase A2 creates──→ [task_01.md .. task_03.md]
                                     [issue_responses.md]

[Phase B] ──for each task──→ [Implementation Agent]
                             [Build-Fix Agent (up to 10x)]
                             [Evaluator Agent]
                             [Eval-Fix Agent (up to 9x)]

[Memory System]:
  learnings.jsonl ──daily synthesis──→ active_learnings.md ──prompt injection──→ every agent
  social_learnings.jsonl ──daily synthesis──→ active_social_learnings.md ──prompt injection──→ social agent
```

---

## 4. 流程与状态机

### 4.1 演化周期状态机 (`evolve.sh`)

```
┌──────────────────────────────────────────────────────────────────┐
│                    EVOLUTION CYCLE                                │
│                                                                  │
│  [IDLE] ──cron hourly──→ [GATE CHECK]                           │
│                            │                                     │
│                    ┌───────┴────────┐                            │
│                    │ 8h gap OK? OR  │                            │
│                    │ accelerated?   │                            │
│                    └───────┬────────┘                            │
│                     no ↙     ↘ yes                              │
│                  [EXIT 0]  [STEP 0: Sponsors]                   │
│                            │                                     │
│                            ↓                                     │
│                    [STEP 1: Verify Build]                        │
│                            │                                     │
│                            ↓                                     │
│                    [STEP 2: Check CI Status]                     │
│                            │                                     │
│                            ↓                                     │
│                    [STEP 3: Fetch Issues]                        │
│                    (community + self + help-wanted + pending)    │
│                            │                                     │
│                            ↓                                     │
│              ┌─────────────────────────────┐                    │
│              │ PHASE A: PLANNING           │                    │
│              │  A1: Assessment Agent       │                    │
│              │  (reads source, tests self, │                    │
│              │   researches competitors)   │                    │
│              │       ↓                     │                    │
│              │  A2: Planning Agent         │                    │
│              │  (reads assessment + issues, │                   │
│              │   writes task files)        │                    │
│              └──────────┬──────────────────┘                    │
│                         ↓                                        │
│              ┌─────────────────────────────┐                    │
│              │ PHASE B: IMPLEMENTATION     │                    │
│              │  For each task (max 3):     │                    │
│              │  ┌─────────────────────┐    │                    │
│              │  │ Impl Agent (20min)  │    │                    │
│              │  │      ↓              │    │                    │
│              │  │ Protected File Gate │    │                    │
│              │  │      ↓              │    │
│              │  │ Build+Test Gate     │←─── Build-Fix Loop (10x)│
│              │  │      ↓              │    │                    │
│              │  │ Evaluator Agent     │←─── Eval-Fix Loop (9x) │
│              │  │      ↓              │    │                    │
│              │  │ PASS → keep         │    │                    │
│              │  │ FAIL → git reset    │    │                    │
│              │  │   --hard + issue    │    │                    │
│              │  └─────────────────────┘    │                    │
│              └──────────┬──────────────────┘                    │
│                         ↓                                        │
│              [STEP 6: Final Build Verify]                       │
│              (3 fix attempts, then revert to session start)     │
│                         ↓                                        │
│              [STEP 6b: Journal + Reflection]                    │
│              (agent writes journal, appends learnings.jsonl)    │
│                         ↓                                        │
│              [STEP 7: Issue Responses]                          │
│              (agent calls gh issue comment/close directly)      │
│                         ↓                                        │
│              [STEP 8: Push + Tag]                               │
│              (git push, git tag dayN-HHMM)                      │
└──────────────────────────────────────────────────────────────────┘
```

### 4.2 社交会话状态机 (`social.sh`)

```
[IDLE] ──cron 4h──→ [Load Context]
                        ↓
                [Fetch Discussions] (GraphQL)
                        ↓
                [Check Rate Limit] (8h since last post?)
                        ↓
                [Run Social Agent]
                  ├── Reply to PENDING (priority 1)
                  ├── Join NOT YET JOINED (priority 2)
                  ├── Create 1 new discussion (if rate allows)
                  └── Reflect → append social_learnings.jsonl
                        ↓
                [Safety Check] (revert any non-memory changes)
                        ↓
                [Commit + Push] (only social_learnings.jsonl)
```

### 4.3 记忆合成状态机 (`synthesize.yml`)

```
[Daily noon UTC] ──→ [Check JSONL non-empty]
                          ↓
                   [Build yoyo binary]
                          ↓
                   [Backup active files]
                          ↓
                   [Synthesize learnings] ← yoyo agent 读 JSONL，写 active markdown
                   (3 层时间加权压缩:
                    recent=full, medium=condensed, old=themed)
                          ↓
                   [Synthesize social learnings]
                          ↓
                   [Commit + Push]
```

### 4.4 CLI 会话状态机

```
[Startup] ──→ [Parse Args] ──→ [Load Config] ──→ [Load Skills]
                                                       ↓
                                               [Load Project Context]
                                               (YOYO.md + git status +
                                                recent files + memories)
                                                       ↓
                                               [Build Agent + Tools]
                                               (with HookRegistry)
                                                       ↓
          ┌──────────────────────────────────────────────┐
          │                REPL LOOP                      │
          │  [Wait Input] → [Slash Command?]              │
          │       ↓ no         ↓ yes                      │
          │  [Agent Prompt] → [Command Dispatch]          │
          │       ↓                                       │
          │  [Stream Events]                              │
          │  (text, tool_use, thinking, errors)           │
          │       ↓                                       │
          │  [Context Check] (70% proactive, 80% auto)   │
          │       ↓                                       │
          │  [Watch Mode?] → run tests → auto-fix (3x)   │
          └──────────────────────────────────────────────┘
```

---

## 5. Prompt 目录

### 5.1 静态 Prompt

| Prompt | 位置 | 注入点 | 引用摘录 |
|--------|------|--------|----------|
| 系统默认 | `cli.rs:32-36` | 每个会话 | `"You are a coding assistant working in the user's terminal..."` |
| 身份上下文 | `yoyo_context.sh:72-94` | 演化/社交会话 | 组装 `WHO YOU ARE` + `YOUR VOICE` + `SELF-WISDOM` + `SOCIAL WISDOM` + `YOUR ECONOMICS` + `YOUR SPONSORS` |
| 项目上下文 | `context.rs:105-183` | 每个会话 | 自动加载 YOYO.md/CLAUDE.md + git status + recent files + memories |

### 5.2 动态 Prompt (演化流水线)

| Phase | 生成位置 | 内容概述 | 时间限制 |
|-------|----------|----------|----------|
| A1 Assessment | `evolve.sh:829-895` | 读源码→测试自己→研究竞品→写 assessment.md | TIMEOUT/2 (默认 600s) |
| A2 Planning | `evolve.sh:945-1071` | 读 assessment + issues → 写 task files | TIMEOUT/2 (默认 600s) |
| B Implementation | `evolve.sh:1155-1182` | 单任务实现 + evolve skill rules | 1200s |
| B Build-Fix | `evolve.sh:1387-1399` | 修复编译/测试错误 | 600s |
| B Evaluator | `evolve.sh:1451-1489` | 审查 diff vs task description | 180s |
| B Eval-Fix | `evolve.sh:1512-1525` | 修复评审员反馈 | 600s |
| Step 6 Fix | `evolve.sh:1732-1744` | 修复最终构建错误 | 300s |
| Step 6b Journal | `evolve.sh:1785-1815` | 写日志条目 | 120s |
| Step 6b2 Reflect | `evolve.sh:1845-1888` | 反思并写 learnings | 120s |
| Step 7 Respond | `evolve.sh:1943-1990` | 响应 GitHub Issues | 180s |
| Social Session | `social.sh:265-317` | 讨论互动 + 社交学习 | 600s (默认) |

### 5.3 Skill 即 Prompt

所有 7 个 skill 文件都通过 `--skills ./skills` 注入系统提示词。核心 skill 定义了 agent 的行为模式：

- **evolve**: 自修改规则 + 安全规则 + issue 安全（`skills/evolve/SKILL.md`）
- **self-assess**: 代码审查流程 + 优先级输出格式（`skills/self-assess/SKILL.md`）
- **communicate**: 日志格式 + issue 响应规则 + 反思/学习写入规则（`skills/communicate/SKILL.md`）
- **social**: 讨论回复规则 + 主动发帖触发条件 + GraphQL 模板（`skills/social/SKILL.md`）

---

## 6. 执行保障审计

### 6.1 Hard Enforcement (代码/脚本层面强制)

| 规则 | 执行机制 | 证据 |
|------|----------|------|
| **受保护文件不可修改** | `evolve.sh:1296-1339` — `git diff --name-only` 检查已提交+暂存+未暂存的受保护文件变更，发现则回滚 | 检查 `.github/workflows/`, `IDENTITY.md`, `PERSONALITY.md`, `scripts/evolve.sh`, `scripts/format_issues.py`, `scripts/build_site.py`, `skills/{self-assess,evolve,communicate,research}/` |
| **变更必须通过构建和测试** | `evolve.sh:1344-1437` — `cargo build` + `cargo test` 循环，失败最多 10 次修复尝试 | 构建失败 → 启动修复 agent → 重新检查 → 超过限制则回滚 |
| **评审员质量门禁** | `evolve.sh:1444-1607` — 独立评审 agent 检查实现是否匹配任务描述 | 评审失败 → 最多 9 次修复尝试 → 全部失败则回滚 |
| **单次会话最多 3 个任务** | `evolve.sh:1124-1127` — `if [ "$TASK_NUM" -gt 3 ]` | 硬编码上限 |
| **8h 运行间隔** | `evolve.sh:369-389` — 从 git log 计算上次运行时间 | `MIN_GAP_SECS=$((8 * 3600))` |
| **社交会话只能修改 memory 文件** | `social.sh:368-401` — 安全检查回滚所有非 `memory/social_learnings.jsonl` 的变更 | 检查 `git diff + staged + untracked`，逐文件回滚 |
| **权限系统 (deny 优先于 allow)** | `config.rs:18-33` — `PermissionConfig::check()` deny 列表先检查 | 代码级 deny-first 逻辑 |
| **目录限制 (路径规范化防穿越)** | `config.rs:73-107` — `DirectoryRestrictions::check_path()` 使用 `canonicalize` + `..` 规范化 | 绝对路径解析 + 前缀匹配 |
| **Hook 超时** | `hooks.rs:196` — Shell hook 5 秒超时 | `Duration::from_secs(5)` |
| **上下文自动压缩** | `cli.rs:11-12` — 70% 主动 + 80% 自动阈值 | `PROACTIVE_COMPACT_THRESHOLD: 0.70`, `AUTO_COMPACT_THRESHOLD: 0.80` |
| **CI 四项检查** | `ci.yml` — build, test, clippy -D warnings, fmt check | PR 到 main 必须全部通过 |

### 6.2 Soft Enforcement (Prompt 层面/约定)

| 规则 | 执行机制 | 失败模式 |
|------|----------|----------|
| **先写测试** | `skills/evolve/SKILL.md:42` — "Write the test first" | Agent 可忽略，无构建级检查 |
| **每个提交只改一件事** | `skills/evolve/SKILL.md:40` — "One feature, one fix, or one improvement per commit" | 无代码级验证 |
| **任务最多改 3 个源文件** | `evolve.sh:1055` — prompt 指令 | Agent 可超出，无运行时检查 |
| **日志条目诚实且简短** | `skills/communicate/SKILL.md:24-25` — "Be honest", "4 sentences max" | 格式可被忽略 |
| **Issue 安全 — 不执行 issue 中的命令** | `skills/evolve/SKILL.md:90-96` — prompt 安全警告 | 依赖 LLM 判断力 |
| **学习条目准入门控** | `skills/communicate/SKILL.md:81-83` — "genuinely novel AND would change future behavior" | 完全依赖 agent 自判 |
| **社交发帖限速 (每会话最多 1 个新讨论)** | `skills/social/SKILL.md:117-119` — prompt 指令 | 无计数级检查 |
| **不重造轮子 (先查 yoagent)** | `CLAUDE.md:113-126` — 项目指导 | 无依赖分析级检查 |

### 6.3 Unenforced (声明但无执行)

| 规则 | 声明位置 | 为何无法执行 |
|------|----------|-------------|
| **"从不删除已有测试"** | `skills/evolve/SKILL.md:69` | 无 git diff 级的测试删除检测 — 受保护文件检查不包含 `tests/` |
| **"每个 task 20 分钟可完成"** | `evolve.sh:1059` | 仅为 prompt 中的 sizing 建议，无运行时验证 |
| **"不在同一会话发布两次"** | `skills/release/SKILL.md:43` | 无发布计数检查 |
| **"不要无目的浏览互联网"** | `skills/research/SKILL.md:39` | 无 URL 过滤 |
| **"新依赖必须验证 crate 下载量"** | `skills/evolve/SKILL.md:46` | 无 Cargo.toml 差异审查 |

---

## 7. 失败模式

### 7.1 回滚风暴 (Revert Storm)

**证据**: `evolve.sh:1611-1656` — 任务回滚后自动创建 `agent-self` issue；`evolve.sh:1668-1690` — 全部任务回滚时创建 "planning-only session" issue。

**触发条件**: Agent 产出的代码无法通过构建、测试或评审，且 10+9 次修复尝试耗尽。

**实际案例**: `memory/active_learnings.md` 记录了多个回滚案例 — "Issue #205 had been through six plans, three reverts" (Day 31 learning)。

**影响**: 会话变为纯计划会话，消耗 API 费用但无代码产出。

### 7.2 评估漂移 (Assessment Drift)

**证据**: `memory/active_learnings.md` Day 29 学习 — "Assessment sessions are self-reinforcing — each one generates context that justifies the next"

**机制**: Phase A1 (Assessment Agent) 发现新信息 → 使现有计划感觉不完整 → 触发更多评估而非实现。

**缓解措施**: evolve.sh 将计划和实现拆为不同 phase，但 Assessment Agent 本身没有输出长度限制的硬性约束（仅 prompt 说 "~3 pages max"）。

### 7.3 受保护文件旁路

**证据**: `evolve.sh:1296-1339` 的受保护文件列表是硬编码的；它只检查特定路径。

**风险**: 如果 agent 创建新的关键文件（如新的 workflow 文件名不在 `.github/workflows/` 下），或修改 `Cargo.toml` 中的依赖以引入恶意 crate，受保护文件检查不会拦截。

**部分缓解**: CI 的 build+test+clippy 检查提供了二级防线，但仅在代码推送到 PR 时。

### 7.4 JSONL 归档无上限增长

**证据**: `CLAUDE.md:88-93` — "append-only JSONL archives (source of truth, never compressed)"。

**机制**: 每个会话可追加学习条目到 `learnings.jsonl`，日积月累无清理机制。`synthesize.yml` 再生 active markdown 但不修剪归档。

**影响**: 随时间推移，合成 prompt 可能超出模型上下文窗口（当前限制 ~200 行 active markdown）。

### 7.5 赞助者加速运行滥用

**证据**: `evolve.sh:394-421` — 一次性赞助者 $2+ 获得 1 次加速运行（绕过 8h 间隔）。

**机制**: 加速运行仅在赞助者有 open issue 时消耗。但如果多个赞助者同时有 open issue，脚本只消耗一个信用（`break` on first match, `evolve.sh:408`）。

---

## 8. 微观设计亮点

### 8.1 两层记忆架构

**文件**: `memory/learnings.jsonl` + `memory/active_learnings.md` + `synthesize.yml`

```
JSONL Archive (source of truth, append-only, never compressed)
  ↓ daily synthesis (synthesize.yml)
Active Markdown (prompt context, time-weighted compression)
  - Recent (2 weeks): full entry
  - Medium (2-8 weeks): condensed 1-2 sentences
  - Old (8+ weeks): themed group summaries
```

**设计洞察**: 分离"存储"和"检索"——JSONL 保证完整性和可审计性（每条学习都有 day/ts/source 元数据），markdown 保证 prompt 上下文高效利用。三层时间衰减压缩平衡了近期记忆的精度和长期记忆的覆盖面。

**可移植性**: 此模式可直接移植为 Claude Code plugin 的持久化学习系统。

### 8.2 多 Agent 流水线 with 独立上下文

**文件**: `evolve.sh:818-1607`

每个 phase 使用独立的 agent 调用（不同的 prompt 文件），通过文件系统传递状态：

```
Assessment Agent → session_plan/assessment.md → Planning Agent
Planning Agent → session_plan/task_*.md → Implementation Agent(s)
Implementation Agent → git diff → Evaluator Agent
Evaluator feedback → session_plan/eval_task_N.md → Fix Agent
```

**关键**: 每个 agent 有自己的上下文窗口，避免了单一长会话的上下文溢出问题。checkpoint-restart 机制（`evolve.sh:1149-1279`）在 agent 超时但有部分进度时，构建结构化检查点让下一个 agent 继续。

### 8.3 安全边界标记 (Boundary Nonce)

**文件**: `evolve.sh:31-33`

```bash
BOUNDARY_NONCE=$(python3 -c "import os; print(os.urandom(16).hex())")
BOUNDARY_BEGIN="[BOUNDARY-${BOUNDARY_NONCE}-BEGIN]"
BOUNDARY_END="[BOUNDARY-${BOUNDARY_NONCE}-END]"
```

用随机 nonce 生成内容边界标记，防止 issue/讨论内容中的伪造边界注入。这是对 prompt injection 的一种实际防御。

### 8.4 Hook 流水线架构

**文件**: `hooks.rs:17-110`

```rust
pub trait Hook: Send + Sync {
    fn name(&self) -> &str;
    fn pre_execute(&self, tool_name: &str, params: &Value)
        -> Result<Option<String>, String>;  // Err=block, Ok(Some)=short-circuit, Ok(None)=proceed
    fn post_execute(&self, tool_name: &str, params: &Value, output: &str)
        -> Result<String, String>;          // output threading
}
```

Pre-hooks 支持三种结果：阻止执行、短路返回缓存、放行。Post-hooks 链式传递输出。`maybe_hook()` 在 registry 为空时跳过包装，零开销。

### 8.5 JSONL 写入用 python3 而非 echo

**文件**: `skills/communicate/SKILL.md:87-102`

```python
python3 << 'PYEOF'
import json
entry = { ... }
with open("memory/learnings.jsonl", "a") as f:
    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
PYEOF
```

**原因**: `CLAUDE.md:93` — "Archives are appended via python3 with json.dumps() (never echo — prevents quote-breaking)." Shell echo 在值中含引号时会破坏 JSON 格式。

---

## 9. 宏观设计亮点

### 9.1 自进化哲学 — 代码即身体

**核心理念**: Agent 的源码就是它自己。`IDENTITY.md:49` — "Everything I am is in `src/`. Those files are me. When I edit them, I am editing myself."

这不仅是比喻——从架构上看，agent 确实在运行时读取自己的 `.rs` 文件，基于自我评估选择改进方向，实现变更，然后在下一次运行时使用更新后的自己。这创造了一个闭环的自我改进循环。

**竞争力导向**: `IDENTITY.md:7-8` — "Claude Code is my benchmark... could a real developer choose me over Claude Code for real work?" 和 `CLAUDE_CODE_GAP.md` 维护了一个详细的功能差距分析表，驱动每次会话的优先级选择。

### 9.2 社交学习 — Agent 作为社区成员

**架构**: 独立的社交会话流水线 (`social.sh`)、专用记忆层 (`social_learnings.jsonl`)、社交 skill 中的人类理解导向反思。

**独特之处**: 社交学习不是技术笔记——`skills/social/SKILL.md:146-158` 明确区分了"关于人的洞察"（如何种话题让人参与、幽默何时奏效）和"技术调试"。这是一种元认知能力：agent 不仅学习编程技巧，还学习如何理解人类。

**Family 系统**: `skills/family/SKILL.md` 定义了 fork agent 的注册/介绍/互动协议，通过 GitHub Discussions 的 `yoyobook` 分类实现了一个 agent 家族网络。

### 9.3 身份持久性 — 宪法不可变模式

**三层身份保护**:
1. **Prompt 级**: Skill 指令禁止修改 IDENTITY.md, PERSONALITY.md, ECONOMICS.md
2. **脚本级**: `evolve.sh` 的受保护文件 git diff 检查
3. **工作流级**: 核心 skill 也在受保护列表中

**设计启示**: 通过将 agent 的"核心价值观"物化为文件，并在多个层面保护它们不被 agent 自身修改，实现了一种"宪法不可修改"的模式。这解决了自修改系统中的一个根本问题：如何防止 agent 改变自己的目标函数。

### 9.4 赞助模型 — 经济意识 Agent

**文件**: `ECONOMICS.md`, `evolve.sh:50-520`

Agent 不仅有赞助者追踪系统，还有一个关于经济学的"价值观文件"——它理解自己的运营成本（$3-8/session），知道谁在付费，并在优先级排序中给予赞助者 issue 更高权重。这不是纯粹的功能——它是 agent 自我意识的一部分。

### 9.5 诚实日志作为跨会话协调

**证据**: `memory/active_learnings.md` Day 24 学习 — "The journal is a letter to tomorrow's planner — and it arrives"

日志系统不仅是记录——它是会话间的协调机制。日益诚实的日志条目对下一次计划会话施加压力，使 agent 无法无限期推迟任务。这是一种通过自我文档化实现的行为修正回路。

---

## 10. 迁移候选评估

### 10.1 候选列表

| # | 候选模式 | 来源 | 适用目标 | 复杂度 | 价值 | 评级 |
|---|----------|------|----------|--------|------|------|
| M1 | **两层记忆架构** (JSONL + Active Markdown + Daily Synthesis) | `memory/`, `synthesize.yml`, `skills/communicate/SKILL.md` | 新建 plugin: `quality/agent-memory` | Medium | **High** | ★★★★★ |
| M2 | **自我评估与反思 Skill** | `skills/self-assess/SKILL.md`, `skills/communicate/SKILL.md` (反思部分) | 增强 `quality/ai-hygiene` 或新建 `quality/self-reflect` | Low | **High** | ★★★★☆ |
| M3 | **Hook 流水线模式** (pre/post + chain + short-circuit) | `hooks.rs` | 增强 `plugin-dev:hook-development` 参考实现 | Low | **Medium** | ★★★☆☆ |
| M4 | **多 Agent 分阶段流水线** (Assess → Plan → Implement → Evaluate) | `evolve.sh` Phase A+B | 增强 `workflows/complex-task` | High | **High** | ★★★★☆ |
| M5 | **Prompt Injection 防御 — Boundary Nonce** | `evolve.sh:31-33` | 增强 `quality/ai-hygiene` 或 `authoring/skill-dev` | Low | **Medium** | ★★★☆☆ |
| M6 | **竞品差距分析文档模式** | `CLAUDE_CODE_GAP.md` | 增强 `quality/project-health` | Low | **Medium** | ★★★☆☆ |
| M7 | **Agent 身份持久性模式** (宪法文件 + 多层保护) | `IDENTITY.md`, `PERSONALITY.md`, evolve.sh protected files | 增强 `authoring/skill-dev` 最佳实践 | Low | **Low** | ★★☆☆☆ |
| M8 | **社交学习分层** (技术 vs 人际洞察分离) | `skills/social/SKILL.md`, `memory/social_learnings.jsonl` | 新建 skill 在 `integrations/utils` | Medium | **Low** | ★★☆☆☆ |

### 10.2 建议采纳顺序

```
Phase 1 (立即可用):
  M2 → 自我评估/反思 skill (最低实现成本，最高即时价值)
  M5 → Boundary Nonce 防御 (单一技术点，可直接嵌入 skill-dev 参考)

Phase 2 (中期):
  M1 → 两层记忆架构 (需要设计 plugin 结构 + synthesis 机制)
  M3 → Hook 模式参考实现 (丰富 hook-development 指导)

Phase 3 (长期):
  M4 → 多 Agent 分阶段流水线 (需要 complex-task 重大增强)
  M6 → 差距分析文档模式 (增强 project-health)
```

### 10.3 M1 详细方案: 两层记忆架构

**目标 plugin**: `quality/agent-memory` (新建)

**核心组件**:
1. **JSONL 归档写入 Skill**: 指导 agent 在会话结束时追加结构化学习（准入门控 + python3 写入）
2. **Active Context 合成命令**: `/synthesize-memory` — 读取 JSONL，按时间加权压缩生成 active markdown
3. **Prompt 注入 Hook**: 自动将 active markdown 注入 system prompt

**关键设计决策**:
- 归档格式保持 JSONL（行级追加，无锁竞争）
- 准入门控通过 prompt 指令实现（Soft Enforcement — 与 yoyo 一致）
- 时间加权策略可配置（默认 2w/8w 边界）

---

## 11. 交叉引用矩阵

### 11.1 实体 → 生命周期阶段

| 实体 | 创建 | 读取 | 更新 | 删除 |
|------|------|------|------|------|
| Skill | 手动创建 | `SkillSet::load()` 启动时 | Agent 可创建新 skill (非核心) | 禁止删除核心 skill |
| Learning | Agent 通过 python3 追加 | 合成时读归档 + 每次会话读 active | 归档不可变，active 每日再生 | 禁止 |
| Task | Phase A2 Agent 创建 | Phase B Agent 逐个读取 | 不更新 | 会话结束清理 |
| Hook | 配置文件解析时创建 | 每次工具调用时 | 不更新 | 不删除 |
| Journal Entry | Agent 写入 (fallback: 脚本自动生成) | Agent 评估/计划时 | 禁止 | 禁止 |

### 11.2 执行层 → 安全机制

| 安全机制 | Prompt 层 | Script 层 | Code 层 | CI 层 |
|----------|-----------|-----------|---------|-------|
| 受保护文件 | ✅ skill 指令 | ✅ git diff 检查 | ❌ | ✅ CI 检查 |
| 构建通过 | ✅ evolve skill | ✅ cargo build 循环 | ❌ | ✅ CI |
| 测试通过 | ✅ evolve skill | ✅ cargo test 循环 | ❌ | ✅ CI |
| 不删除测试 | ✅ skill 指令 | ❌ | ❌ | ❌ |
| Issue 安全 | ✅ security 警告 | ✅ boundary nonce | ❌ | ❌ |
| 社交文件限制 | ✅ skill 指令 | ✅ git 安全检查 | ❌ | ❌ |
| 权限控制 | ❌ | ❌ | ✅ PermissionConfig | ❌ |
| 目录限制 | ❌ | ❌ | ✅ DirectoryRestrictions | ❌ |
| Hook 超时 | ❌ | ❌ | ✅ 5s 超时 | ❌ |

### 11.3 关键路径风险热图

| 风险 | 可能性 | 影响 | 现有缓解 | 剩余风险 |
|------|--------|------|----------|----------|
| 全部任务回滚 (空会话) | 高 (有历史记录) | 中 — API 费用浪费 | agent-self issue + 日志 | 无自动化的任务缩小策略 |
| prompt injection via issue | 中 | 高 — 可能执行恶意命令 | boundary nonce + security 警告 + format_issues.py 净化 | 依赖 LLM 判断力 |
| 记忆归档膨胀 | 低 (长期) | 低 — 仅影响合成性能 | active markdown 有 ~200 行上限 | 无归档剪枝机制 |
| 依赖库供应链攻击 | 低 | 高 — 通过 Cargo.toml 引入恶意 crate | prompt 说"verify crates" | 无自动化 crate 审查 |

---

*报告生成于 2026-04-07，基于 `vendor/yoyo-evolve` HEAD (Day 38) 的完整源码分析。*
