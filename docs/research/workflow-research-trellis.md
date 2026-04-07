# Workflow Research: Trellis

## 1. Framework Profile

### 基本信息

| 属性 | 值 |
|------|-----|
| **项目名称** | Trellis (Mindfold Trellis) |
| **仓库** | mindfold-ai/Trellis |
| **版本** | v0.3.6 (latest), v0.4.0-beta.5 (in development) |
| **许可证** | AGPL-3.0 |
| **主要语言** | TypeScript (CLI), Python (scripts/hooks), Markdown (prompts) |
| **发布方式** | npm package `@mindfoldhq/trellis` |
| **目标平台** | Claude Code (full), Cursor (partial), OpenCode, Codex, 13+ AI coding tools |

### 框架类型

**Hybrid: Workflow Harness + Multi-Agent Orchestrator + Spec Library**

- **Workflow Harness**: 通过 hooks 强制注入 context，控制 agent 行为
- **Multi-Agent Orchestrator**: 支持 parallel worktree sessions 和 phase-based pipeline
- **Spec Library**: 项目级 coding guidelines 的持久化和自动注入

### 核心设计哲学

引用自 Anthropic 的 "Effective Harnesses for Long-Running Agents"：

> **Specs Injected, Not Remembered**
> Hook 系统确保 agent 总是接收到完整的 context，而不是依赖 AI 的"记忆"

关键原则：
1. **Read Before Write** — 强制在编码前读取 guidelines
2. **Human Commits** — AI 永不执行 `git commit`，人类验证后提交
3. **Pure Dispatcher** — dispatch agent 只负责编排，不做决策
4. **Layered Context** — 通过 JSONL 文件精确控制每个 agent 接收的 context
5. **Verification Before Exit** — Ralph Loop 机制阻止 check agent 在验证通过前退出

### 文件统计

| 类型 | 数量 | 说明 |
|------|------|------|
| **总文件数** | ~816 | 不含 docs-site, node_modules, dist, archive |
| **Python 脚本** | 88 | 核心自动化逻辑 |
| **Markdown 文档** | 450 | Prompts, specs, docs |
| **TypeScript 源码** | 75 | CLI 实现 |
| **Shell 脚本** | 40 | 已归档的 bash 版本 (scripts-shell-archive/) |
| **测试文件** | 28 | 单元测试和集成测试 |
| **模板文件** | 166 | CLI templates/ 目录中的 .md 模板 |

### 架构层次

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERACTION LAYER                    │
│  /trellis:start  /trellis:parallel  /trellis:finish-work   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                      COMMAND LAYER                           │
│  .claude/commands/trellis/*.md  (21 slash commands)         │
│  .claude/agents/*.md            (6 agent definitions)       │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                       HOOK LAYER                             │
│  SessionStart    → session-start.py                         │
│  PreToolUse      → inject-subagent-context.py               │
│  SubagentStop    → ralph-loop.py                            │
│  StatusLine      → statusline.py                            │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    PERSISTENCE LAYER                         │
│  .trellis/workspace/  (journals, developer identity)        │
│  .trellis/tasks/      (task tracking, JSONL context)        │
│  .trellis/spec/       (coding guidelines)                   │
│  .trellis/scripts/    (Python automation)                   │
└─────────────────────────────────────────────────────────────┘
```


## 2. Source Inventory

### Overview 类

| 文件 | 分类 | 用途 |
|------|------|------|
| `README.md` | Overview | 项目介绍，支持平台列表，安装指南 |
| `AGENTS.md` | Overview | AI assistant 指令（含 `TRELLIS:START/END` 标记，可被 `trellis update` 刷新） |
| `CONTRIBUTING.md` | Overview | 贡献指南 |
| `.trellis/workflow.md` | Overview | 核心工作流文档，开发流程，最佳实践 |

### Execution 类 — Commands (21个)

| 命令 | 文件 | 功能 | 触发时机 |
|------|------|------|----------|
| `/trellis:start` | `commands/trellis/start.md` | 初始化 session，读取 context，分类任务 | Session 开始 |
| `/trellis:before-dev` | `commands/trellis/before-dev.md` | 读取 spec guidelines | 编码前 |
| `/trellis:brainstorm` | `commands/trellis/brainstorm.md` | 需求发现，PRD 编写 | 复杂任务开始 |
| `/trellis:check` | `commands/trellis/check.md` | 代码质量检查 | 编码后 |
| `/trellis:check-cross-layer` | `commands/trellis/check-cross-layer.md` | 跨层验证 | 多层修改后 |
| `/trellis:finish-work` | `commands/trellis/finish-work.md` | 提交前 checklist | 提交前 |
| `/trellis:commit` | `commands/trellis/commit.md` | Conventional Commits 生成 | 提交时 |
| `/trellis:record-session` | `commands/trellis/record-session.md` | 记录 session 到 journal | Session 结束 |
| `/trellis:break-loop` | `commands/trellis/break-loop.md` | 深度 bug 分析 | Debug 后 |
| `/trellis:update-spec` | `commands/trellis/update-spec.md` | 更新 code-spec 文档 | 学到新知识时 |
| `/trellis:parallel` | `commands/trellis/parallel.md` | Multi-agent pipeline 编排 | 并行任务 |
| `/trellis:onboard` | `commands/trellis/onboard.md` | 新成员引导 | 首次使用 |
| `/trellis:improve-ut` | `commands/trellis/improve-ut.md` | 改进单元测试覆盖 | 代码变更后 |
| `/trellis:create-command` | `commands/trellis/create-command.md` | 创建新 slash command | 扩展时 |
| `/trellis:create-manifest` | `commands/trellis/create-manifest.md` | 创建发布 manifest | 发布时 |
| `/trellis:integrate-skill` | `commands/trellis/integrate-skill.md` | 集成外部 skill 到 spec | 扩展时 |
| `/trellis:publish-skill` | `commands/trellis/publish-skill.md` | 发布 skill 到 docs site | 发布时 |

### Execution 类 — Agents (6个)

| Agent | 文件 | 模型 | 工具权限 | 限制 |
|-------|------|------|----------|------|
| `dispatch` | `agents/dispatch.md` | opus | Read, Bash | 纯编排，不读 spec |
| `plan` | `agents/plan.md` | opus | Read, Bash, Glob, Grep, Task | 可拒绝不合理需求 |
| `research` | `agents/research.md` | opus | Read, Glob, Grep, Skill | 只读，不修改文件 |
| `implement` | `agents/implement.md` | opus | Read, Write, Edit, Bash, Glob, Grep | 禁止 git commit |
| `check` | `agents/check.md` | opus | Read, Write, Edit, Bash, Glob, Grep | Ralph Loop 控制 |
| `debug` | `agents/debug.md` | opus | Read, Write, Edit, Bash, Glob, Grep | 精确修复，禁止 git commit |

### Enforcement 类 — Hooks (4个)

| Hook | 文件 | 事件 | 机制 |
|------|------|------|------|
| `session-start.py` | `.claude/hooks/session-start.py` | SessionStart, clear, compact | 注入 workflow + context + guidelines + start.md |
| `inject-subagent-context.py` | `.claude/hooks/inject-subagent-context.py` | PreToolUse (Task/Agent) | 读取 JSONL → 注入 spec 到 subagent prompt |
| `ralph-loop.py` | `.claude/hooks/ralph-loop.py` | SubagentStop (check) | 验证 completion markers 或 verify commands |
| `statusline.py` | `.claude/hooks/statusline.py` | StatusLine | 显示 task/model/context/branch 状态 |

### Enforcement 类 — Scripts (核心)

| 脚本 | 用途 |
|------|------|
| `scripts/get_context.py` | 获取 session context（developer, git, tasks） |
| `scripts/task.py` | 任务 CRUD（create, archive, list, start, finish, init-context, add-context, validate） |
| `scripts/add_session.py` | 一键记录 session 到 journal |
| `scripts/init_developer.py` | 初始化开发者身份 |
| `scripts/multi_agent/start.py` | 启动 worktree agent |
| `scripts/multi_agent/status.py` | 监控 agent 状态 |
| `scripts/multi_agent/create_pr.py` | 创建 PR（含 submodule 支持） |
| `scripts/multi_agent/cleanup.py` | 清理 worktree |

### Configuration 类

| 文件 | 用途 |
|------|------|
| `.claude/settings.json` | Hook 注册（SessionStart, PreToolUse, SubagentStop） |
| `package.json` | monorepo root，husky + lint-staged |
| `pnpm-workspace.yaml` | pnpm workspace 配置 |
| `.lintstagedrc` | lint-staged 规则（eslint + prettier） |
| `pyrightconfig.json` | Python 类型检查配置 |
| `.trellis/config.yaml` | 项目级配置（packages, default_package, spec_scope） |

### Skills (4个)

| Skill | 文件 | 用途 |
|-------|------|------|
| `trellis-meta` | `.claude/skills/trellis-meta/` | Trellis 架构文档（含 17 个 reference docs） |
| `contribute` | `.claude/skills/contribute/` | 贡献指南 |
| `python-design` | `.claude/skills/python-design/` | Python 设计原则 |
| `first-principles-thinking` | `.claude/skills/first-principles-thinking/` | 第一性原理思维 |


## 3. Object Model & Context Strategy

### 实体类型定义

#### 3.1 Task（核心实体）

定义位置：`.trellis/scripts/common/types.py:21-53`（`TaskData` TypedDict）

| 字段 | 类型 | 必填 | 用途 |
|------|------|------|------|
| `id` | string | N | 唯一标识 |
| `name` | string | N | 任务名称 |
| `title` | string | Y | 显示标题 |
| `status` | string | Y | 状态：`planning` / `in_progress` / `review` / `completed` / `rejected` |
| `dev_type` | string | Y | 开发类型：`backend` / `frontend` / `fullstack` / `test` / `docs` |
| `priority` | string | Y | 优先级：`P0` - `P3`，默认 `P2` |
| `assignee` | string | N | 分配的开发者 |
| `package` | string | N | monorepo 中的目标 package |
| `branch` | string | N | Git 分支名 |
| `base_branch` | string | N | PR 目标分支 |
| `worktree_path` | string | N | worktree 绝对路径 |
| `current_phase` | int | Y | 当前执行阶段编号 |
| `next_action` | list[dict] | Y | 阶段执行序列，每项含 `phase` + `action` |
| `children` | list[str] | N | 子任务目录名列表 |
| `parent` | string | N | 父任务目录名 |
| `pr_url` | string | N | 创建的 PR URL |
| `submodule_prs` | dict | N | submodule PR URL 映射 |

生命周期：`create` → `planning` → `in_progress` → `review` → `completed`（或 `rejected`）

存储位置：`.trellis/tasks/{MM}-{DD}-{slug}/task.json`

#### 3.2 Agent（执行实体）

定义位置：`.claude/agents/*.md`（6 个 agent 定义文件）

| Agent | 模型 | 工具权限 | 角色 | 关键约束 |
|-------|------|----------|------|----------|
| `dispatch` | opus | Read, Bash | 纯编排器，按 phase 顺序调用 subagent | 不读 spec，不做决策 |
| `plan` | opus | Read, Bash, Glob, Grep, Task | 需求评估 + 任务配置 | 可拒绝不合理需求 |
| `research` | opus | Read, Glob, Grep, Skill | 只读搜索 | 禁止修改文件、禁止建议改进 |
| `implement` | opus | Read, Write, Edit, Bash, Glob, Grep | 按 spec 实现功能 | 禁止 git commit |
| `check` | opus | Read, Write, Edit, Bash, Glob, Grep | 代码审查 + 自修复 | Ralph Loop 控制退出 |
| `debug` | opus | Read, Write, Edit, Bash, Glob, Grep | 精确修复 bug | 禁止 git commit，禁止重构 |

生命周期：由 dispatch 按 `next_action` 数组顺序启动 → 执行 → 输出结果 → 下一个 agent

#### 3.3 Hook（强制注入实体）

定义位置：`.claude/settings.json:1-75`（注册），`.claude/hooks/*.py`（实现）

| Hook | 事件 | 触发条件 | 输出类型 |
|------|------|----------|----------|
| `session-start.py` | SessionStart, clear, compact | 每次 session 启动/清除/压缩 | `additionalContext`（注入 workflow + guidelines + context） |
| `inject-subagent-context.py` | PreToolUse (Task/Agent) | 调用 Task 或 Agent 工具时 | `updatedInput`（重写 prompt，注入 JSONL context） |
| `ralph-loop.py` | SubagentStop (check) | check agent 尝试停止时 | `decision: allow/block`（控制是否允许退出） |
| `statusline.py` | StatusLine | 持续 | 状态栏显示（task/model/ctx/branch） |

#### 3.4 Spec（知识实体）

定义位置：`.trellis/spec/<package>/<layer>/index.md`

结构：
- `spec/<package>/<layer>/index.md` — 入口，含 Pre-Development Checklist 和 Quality Check
- `spec/<package>/<layer>/*.md` — 具体 guideline 文件
- `spec/guides/index.md` — 跨 package 的通用指南

生命周期：人工创建 → session-start hook 注入 index → implement/check agent 按需读取具体文件 → finish agent 检测新模式时更新

#### 3.5 JSONL Context（上下文配置实体）

定义位置：`.trellis/tasks/{task}/implement.jsonl`、`check.jsonl`、`debug.jsonl`、`research.jsonl`、`finish.jsonl`

Schema（每行一个 JSON 对象）：
```json
{"file": "path/to/file.md", "reason": "Why needed"}
{"file": "path/to/dir/", "type": "directory", "reason": "Why needed"}
```

来源：`task_context.py:41-84`

生命周期：`init-context` 生成默认条目 → `add-context` 追加研究发现 → hook 读取并注入到 agent prompt

#### 3.6 Workspace / Journal（记忆实体）

定义位置：`.trellis/workspace/{developer}/journal-N.md`

结构：
- `.trellis/.developer` — 开发者身份文件（gitignored）
- `.trellis/workspace/{developer}/index.md` — 个人索引（含 `@@@auto` 标记）
- `.trellis/workspace/{developer}/journal-N.md` — 顺序编号的日志文件（上限 2000 行）

生命周期：`init_developer.py` 创建 → `add_session.py` 追加 session 记录 → 自动轮转

#### 3.7 Registry（运行时实体）

定义位置：`.trellis/scripts/common/types.py:102-112`（`AgentRecord` TypedDict）

| 字段 | 用途 |
|------|------|
| `id` | agent 标识 |
| `pid` | 进程 ID |
| `task_dir` | 关联的 task 目录 |
| `worktree_path` | worktree 路径 |
| `platform` | 运行平台（claude/cursor/opencode 等） |
| `status` | 运行状态 |

### 实体关系图

```
                    ┌──────────────┐
                    │   config.yaml │ ← packages, hooks, update skip
                    └──────┬───────┘
                           │ defines packages
                    ┌──────▼───────┐
                    │    Spec      │ ← spec/<pkg>/<layer>/*.md
                    └──────┬───────┘
                           │ referenced by
                    ┌──────▼───────┐
         ┌─────────│    Task       │──────────┐
         │         └──────┬───────┘           │
         │ parent/child   │ contains          │ branch
         │                │                   │
    ┌────▼────┐    ┌──────▼───────┐    ┌──────▼───────┐
    │ Subtask  │    │  JSONL Ctx   │    │  Worktree    │
    └─────────┘    └──────┬───────┘    └──────┬───────┘
                          │ injected by       │ runs in
                   ┌──────▼───────┐    ┌──────▼───────┐
                   │    Hook       │    │   Agent      │
                   └──────────────┘    └──────┬───────┘
                                              │ records to
                                       ┌──────▼───────┐
                                       │  Journal     │
                                       └──────────────┘
```

### Fact / Judgment / Evidence 分类

| 分类 | 实体 | 说明 |
|------|------|------|
| **Fact** | `task.json`, `config.yaml`, `.developer`, `registry.json` | 结构化数据，机器可读 |
| **Judgment** | `prd.md`, `info.md`, `REJECTED.md`, `spec/*.md` | 人/AI 编写的决策和规范 |
| **Evidence** | `implement.jsonl`, `check.jsonl`, `journal-N.md`, `.agent-log`, `codex-review-output.txt` | 执行过程的可追溯记录 |

### Context 隔离策略

Trellis 的核心设计是 **JSONL-driven context isolation**：每个 agent 只接收其专属 JSONL 文件中列出的文件内容。

| 角色 | 接收的 Context | 隔离机制 | 证据 |
|------|---------------|----------|------|
| **Dispatch** | 仅 `task.json`（`next_action` 数组） | 不读 spec，不读 JSONL | `dispatch.md:29-31` |
| **Implement** | `implement.jsonl` + `prd.md` + `info.md` | Hook 注入，agent 不自行搜索 | `inject-subagent-context.py:297-325` |
| **Check** | `check.jsonl` + `prd.md`（或 fallback 到 hardcoded check files） | Hook 注入 | `inject-subagent-context.py:328-368` |
| **Debug** | `debug.jsonl` + `codex-review-output.txt` | Hook 注入 | `inject-subagent-context.py:418-456` |
| **Research** | spec 目录结构概览 + 可选 `research.jsonl` | 最小 context，自行搜索 | `inject-subagent-context.py:601-654` |
| **Finish** | `finish.jsonl`（或 fallback）+ `update-spec.md` + `prd.md` | Hook 注入，轻量级 | `inject-subagent-context.py:371-415` |

关键设计：`[finish]` 标记在 prompt 中触发不同的 context 注入路径（`inject-subagent-context.py:757-758`），使同一个 check agent 在不同阶段接收不同 context。


## 4. Flow & State Machine Analysis

### 4.1 主执行路径（Happy Path）

Trellis 有两条主要执行路径：**Single-Session**（`/trellis:start`）和 **Multi-Agent Pipeline**（`/trellis:parallel`）。

#### Single-Session Flow（`/trellis:start`）

```
User Input
  │
  ▼
[SessionStart Hook] ─── session-start.py 注入 workflow + context + guidelines + start.md
  │
  ▼
Task Classification ─── Question / Trivial / Simple / Complex
  │
  ├─ Question/Trivial → 直接回答/修复 → finish-work checklist → 结束
  │
  ├─ Simple → Phase 1B: Create Task + Write PRD
  │            │
  │            ▼
  │          Phase 2: Research → init-context → add-context → start task
  │            │
  │            ▼
  │          Phase 3: implement agent → check agent → Complete
  │
  └─ Complex → Brainstorm (Step 0-8)
               │
               ▼
             Phase 2: Code-Spec Depth Check → Research → Configure Context → Activate
               │
               ▼
             Phase 3: implement agent → check agent → Complete
```

证据：`start.md:64-94`（分类逻辑），`start.md:144-330`（Task Workflow 三阶段）

#### Multi-Agent Pipeline Flow（`/trellis:parallel`）

```
User Input
  │
  ▼
[Orchestrator] ─── parallel.md 在主仓库运行
  │
  ├─ Option A: plan.py → Plan Agent（评估需求，可拒绝）
  │                         │
  │                         ▼
  │                       Research Agent → 分析代码库
  │                         │
  │                         ▼
  │                       配置 task directory（prd.md + JSONL files）
  │
  └─ Option B: 手动配置 task directory
  │
  ▼
start.py ─── 创建 worktree + 复制环境文件 + 初始化 submodule + 启动 dispatch agent
  │
  ▼
[Dispatch Agent in Worktree]
  │
  ├─ Phase 1: implement → [PreToolUse Hook 注入 implement.jsonl context]
  │                         │
  │                         ▼
  │                       Implement Agent 自主工作
  │
  ├─ Phase 2: check → [PreToolUse Hook 注入 check.jsonl context]
  │                     │
  │                     ▼
  │                   Check Agent 自修复 ←──┐
  │                     │                    │
  │                     ▼                    │
  │                   [SubagentStop Hook] ───┘ (Ralph Loop: 验证未通过则 block)
  │
  ├─ Phase 3: finish → [PreToolUse Hook 注入 finish context]
  │                      │
  │                      ▼
  │                    Finish Agent（验证需求 + 更新 spec）
  │
  └─ Phase 4: create-pr → create_pr.py
                            │
                            ▼
                          Stage + Commit + Push + gh pr create --draft
                            │
                            ▼
                          task.json status → "completed"
```

证据：`dispatch.md:36-153`（phase handling），`start.py:182-535`（worktree 创建流程），`create_pr.py:318-616`（PR 创建流程）

### 4.2 Phase 状态机

```
                    ┌──────────┐
                    │ planning │ ← task.py create
                    └────┬─────┘
                         │ start.py
                    ┌────▼──────────┐
                    │ in_progress   │ ← start.py:411
                    └────┬──────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
     ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
     │implement│   │  check  │   │  debug  │  ← current_phase 自动更新
     └────┬────┘   └────┬────┘   └────┬────┘    (inject-subagent-context.py:114-168)
          │              │              │
          └──────────────┼──────────────┘
                         │
                    ┌────▼─────┐
                    │  finish  │
                    └────┬─────┘
                         │
                    ┌────▼──────┐
                    │ create-pr │
                    └────┬──────┘
                         │
                    ┌────▼──────────┐
                    │  completed    │ ← create_pr.py:593
                    └───────────────┘

                    ┌──────────┐
                    │ rejected │ ← plan agent 拒绝 (plan.md:55-96)
                    └──────────┘
```

Phase 推进机制：Hook 自动更新 `current_phase`，dispatch 不需要手动管理（`inject-subagent-context.py:114-168`）。只有 `implement` 和 `check` 会推进 phase，`debug` 和 `research` 不更新（`AGENTS_NO_PHASE_UPDATE = {"debug", "research"}`，`inject-subagent-context.py:55`）。

### 4.3 Failure Path 1: Plan Agent 拒绝需求

```
User Requirement
  │
  ▼
Plan Agent 评估
  │
  ├─ 不清晰/不完整/范围过大/有害 → REJECT
  │   │
  │   ├─ task.json.status = "rejected"
  │   ├─ 写入 REJECTED.md（原因 + 建议）
  │   └─ start.py 检测到 rejected 状态 → 拒绝启动 (start.py:255-267)
  │
  └─ 接受 → 继续正常流程
```

证据：`plan.md:19-103`（5 类拒绝条件），`start.py:255-267`（rejected 状态检查）

### 4.4 Failure Path 2: Ralph Loop 超时

```
Check Agent 执行
  │
  ▼
SubagentStop 触发
  │
  ▼
ralph-loop.py 检查
  │
  ├─ verify commands 配置 → 运行命令
  │   ├─ 全部通过 → allow stop
  │   └─ 失败 → block + 错误信息 → Check Agent 继续修复
  │
  └─ 无 verify commands → 检查 completion markers
      ├─ 全部存在 → allow stop
      └─ 缺失 → block + 列出缺失 markers → Check Agent 继续
  │
  ▼
iteration >= MAX_ITERATIONS (5)
  │
  └─ 强制 allow stop + 重置状态 → 防止无限循环
```

证据：`ralph-loop.py:253-391`（完整决策逻辑），`ralph-loop.py:44`（`MAX_ITERATIONS = 5`），`ralph-loop.py:45`（`STATE_TIMEOUT_MINUTES = 30`）

### 4.5 Failure Path 3: Dispatch Timeout

```
Dispatch 调用 subagent
  │
  ▼
TaskOutput(block=true, timeout=300000) 轮询
  │
  ├─ 完成 → 继续下一 phase
  │
  └─ 超时 → 通知用户，提供选项：
      ├─ 1. 重试同一 phase
      ├─ 2. 跳到下一 phase
      └─ 3. 中止 pipeline
```

证据：`dispatch.md:176-197`（timeout 设置和错误处理）

### 4.6 并行 vs 顺序

| 维度 | 策略 | 证据 |
|------|------|------|
| **Pipeline 内部** | 严格顺序（implement → check → finish → create-pr） | `dispatch.md:55-57`："Execute each step in phase order" |
| **多任务之间** | 并行（每个 task 独立 worktree + 独立 agent 进程） | `start.py` 创建独立 worktree，`registry.json` 跟踪多个 agent |
| **Research 调用** | 可在任意阶段并行调用（不更新 phase） | `AGENTS_NO_PHASE_UPDATE` 集合 |
| **Submodule PR** | 顺序处理每个 submodule，但与主仓库 PR 串行 | `create_pr.py:75-256`（先处理 submodule，再处理主仓库） |


## 5. Enforcement Audit

### 强制级别分类

| 行为声明 | 级别 | 机制 | 证据 |
|----------|------|------|------|
| **Session 启动时注入 workflow + guidelines** | Hard | `session-start.py` 通过 SessionStart hook 自动执行，输出 `additionalContext` | `settings.json:7-37`（3 个 matcher: startup/clear/compact），`session-start.py:291-393` |
| **Subagent 接收 JSONL context** | Hard | `inject-subagent-context.py` 通过 PreToolUse hook 拦截 Task/Agent 调用，重写 prompt | `settings.json:39-59`（matcher: Task + Agent），`inject-subagent-context.py:717-798` |
| **Check agent 必须完成所有验证才能退出** | Hard | `ralph-loop.py` 通过 SubagentStop hook 拦截，检查 completion markers 或 verify commands | `settings.json:61-72`（matcher: check），`ralph-loop.py:253-391` |
| **Ralph Loop 最大迭代限制** | Hard | `MAX_ITERATIONS = 5`，超过后强制 allow stop | `ralph-loop.py:44`，`ralph-loop.py:321-328` |
| **Ralph Loop 状态超时重置** | Hard | `STATE_TIMEOUT_MINUTES = 30`，超时后重置迭代计数 | `ralph-loop.py:45`，`ralph-loop.py:295-311` |
| **Phase 自动推进** | Hard | Hook 在注入 context 时自动更新 `task.json.current_phase` | `inject-subagent-context.py:114-168` |
| **debug/research 不推进 phase** | Hard | `AGENTS_NO_PHASE_UPDATE = {"debug", "research"}` 硬编码排除 | `inject-subagent-context.py:55` |
| **AI 不执行 git commit** | Soft | 仅在 agent prompt 中声明禁止，无 hook 拦截 | `implement.md:30-36`："Do NOT execute these git commands"，`check.md` 无显式禁止 |
| **只有 create-pr 可以 commit** | Soft | `dispatch.md:211` 声明，但无 PreToolUse hook 拦截 Bash(git commit) | `dispatch.md:211`，`create_pr.py:474-476`（实际执行 commit 的唯一位置） |
| **Read Before Write** | Soft | `workflow.md:83` 声明为核心原则，`start.md` 要求读 spec，但无 hook 验证是否真的读了 | `workflow.md:83`，`start.md:55-67` |
| **Spec 必须在编码前读取** | Soft | `workflow.md:55-68` 标记为 `[!] CRITICAL`，session-start hook 注入 index，但不验证 agent 是否读了具体文件 | `workflow.md:55-68`，`session-start.py:328-365`（只注入 index.md，不注入具体 guideline） |
| **Journal 不超过 2000 行** | Soft | `config.yaml:15`（`max_journal_lines: 2000`），`add_session.py` 检查并轮转，但无 hook 阻止手动写入 | `config.yaml:15`，`workflow.md:86` |
| **Plan Agent 可拒绝需求** | Soft | 在 `plan.md` prompt 中定义 5 类拒绝条件，但 agent 是否真的执行取决于 LLM 遵从度 | `plan.md:19-103` |
| **Research Agent 不修改文件** | Soft | `research.md:6` 工具列表不含 Write/Edit，但 Skill 工具可能间接修改 | `research.md:6`（tools 列表），`research.md:46-50`（Forbidden 列表） |
| **Conventional Commits 格式** | Soft | `create_pr.py:379-390` 使用 `prefix_map` 自动生成前缀，但用户手动 commit 不受约束 | `create_pr.py:379-390`，`workflow.md:356-361` |
| **Dispatch 是纯编排器** | Unenforced | `dispatch.md:29-31` 声明 "pure dispatcher"，但无机制阻止 dispatch 读取 spec 或做决策 | `dispatch.md:29-31` |
| **所有 subagent 使用 opus 模型** | Unenforced | `dispatch.md:213` 声明，`parallel.md:201` 重复，但 model 参数由调用者指定，无验证 | `dispatch.md:213`，agent frontmatter 中 `model: opus` |
| **一次只开发一个任务** | Unenforced | `workflow.md:338` 声明 "Don't develop multiple unrelated tasks simultaneously"，无机制限制 | `workflow.md:338` |
| **Task lifecycle hooks** | Hard（配置时） | `config.yaml:59-65` 定义 `after_create`/`after_start`/`after_archive` hooks，由 `task_utils.py` 的 `run_task_hooks()` 执行 | `config.yaml:59-65`，`task.py:97`（`run_task_hooks("after_start", ...)`) |
| **Worktree post_create hooks** | Hard（配置时） | `worktree.yaml:30-36` 定义 `post_create` 命令列表，失败则中止 | `start.py:370-385`（`if ret.returncode != 0: return 1`） |
| **非交互模式跳过注入** | Hard | `CLAUDE_NON_INTERACTIVE=1` 或 `OPENCODE_NON_INTERACTIVE=1` 时跳过 session-start | `session-start.py:28-32` |

### 关键发现

1. **git commit 禁令是 Soft-enforced**：这是 Trellis 最重要的安全约束之一（"Human Commits"），但仅通过 prompt 声明实现。没有 PreToolUse hook 拦截 `Bash(git commit)` 调用。`create_pr.py` 是唯一合法的 commit 路径，但 agent 技术上可以绕过。

2. **Spec 读取是 Soft-enforced**：session-start hook 注入 spec index，但不验证 agent 是否真的读了具体 guideline 文件。这是一个 "trust but inject" 模型。

3. **Ralph Loop 是唯一的 Hard-enforced 质量门**：通过 SubagentStop hook 实现真正的程序化验证（运行 verify commands 或检查 completion markers），是整个框架中最强的强制机制。


## 6. Prompt Catalog & Design Analysis

### 6A. 关键 Prompt 目录

| 角色 | 文件路径 | 关键摘录 | 阶段 | 设计意图 | 隐含假设 | 可能失败模式 |
|------|----------|----------|------|----------|----------|-------------|
| Dispatch | `.claude/agents/dispatch.md` | "You are a pure dispatcher. Only responsible for calling subagents and scripts in order" | Pipeline 全程 | 最小权限原则，防止 dispatch 做超出编排的事 | LLM 会遵守 "pure dispatcher" 约束 | Dispatch 可能自行读取 spec 或尝试修复问题 |
| Plan | `.claude/agents/plan.md` | "You have the power to reject — If a requirement is unclear, incomplete, unreasonable, or potentially harmful, you MUST refuse" | 需求评估 | 前置质量门，防止垃圾需求进入 pipeline | LLM 能准确判断需求质量 | 过度拒绝合理需求，或放过模糊需求 |
| Research | `.claude/agents/research.md` | "You do one thing: find and explain information. You are a documenter, not a reviewer" | 研究阶段 | 严格限制 research 的角色边界 | LLM 能区分 "描述" 和 "建议" | Research 可能在报告中夹带改进建议 |
| Implement | `.claude/agents/implement.md` | "Do NOT execute these git commands: git commit, git push, git merge" | 实现阶段 | 防止 AI 自行提交代码 | LLM 会遵守工具使用禁令 | Agent 可能通过 Bash 间接执行 git 命令 |
| Check | `.claude/agents/check.md` | "Fix issues yourself, don't just report them" + "The loop will NOT stop until you output ALL required completion markers" | 检查阶段 | 自修复 + 强制完成所有检查 | Agent 不会伪造 completion markers | Agent 可能输出 markers 而不实际运行检查 |
| Ralph Loop | `.claude/hooks/ralph-loop.py` | "IMPORTANT: You must ACTUALLY run the checks, not just output the markers" | SubagentStop | 防止 agent 通过输出 markers 逃逸循环 | 文字警告足以阻止 marker 伪造 | 当 verify commands 未配置时，仍依赖 marker 检查 |
| Session Start | `.claude/hooks/session-start.py` | "Steps 1-3 (workflow, context, guidelines) are already injected above — do NOT re-read them" | Session 启动 | 避免重复读取已注入的内容 | Agent 会遵守 "不重复读取" 指令 | Agent 可能忽略注入内容，重新读取文件 |
| Brainstorm | `.claude/commands/trellis/brainstorm.md` | "One question per message. Never overwhelm the user with a list of questions" | 需求发现 | 控制交互节奏，提高用户体验 | LLM 能自律地一次只问一个问题 | Agent 可能一次抛出多个问题 |
| Finish | `inject-subagent-context.py` (build_finish_prompt) | "You MAY update spec files when gaps are detected" | 完成阶段 | 主动维护 spec 文档的新鲜度 | Agent 能准确判断何时需要更新 spec | 过度更新 spec，或遗漏重要模式 |
| Context Injection | `inject-subagent-context.py` (build_implement_prompt) | "All the information you need has been prepared for you" | PreToolUse | 给 agent 信心，减少不必要的文件搜索 | JSONL 配置完整覆盖了所需 context | JSONL 遗漏关键文件，agent 盲目实现 |

### 6B. Design Highlights — Micro（具体模式）

#### Pattern 1: JSONL-Driven Context Injection

```python
# inject-subagent-context.py:227-271
def read_jsonl_entries(base_path: str, jsonl_path: str) -> list[tuple[str, str]]:
    # 每行一个 JSON 对象，支持 file 和 directory 两种类型
    item = json.loads(line)
    file_path = item.get("file") or item.get("path")
    entry_type = item.get("type", "file")
    if entry_type == "directory":
        dir_contents = read_directory_contents(base_path, file_path)
    else:
        content = read_file_content(base_path, file_path)
```

设计意图：将 "agent 需要什么 context" 从 prompt 中解耦到数据文件中。Plan agent 或人类可以精确控制每个 agent 的视野，而不需要修改 agent 定义。

#### Pattern 2: Prompt Rewriting via Hook

```python
# inject-subagent-context.py:789-798
output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow",
        "updatedInput": {**tool_input, "prompt": new_prompt},
    }
}
```

设计意图：Hook 不是阻止工具调用，而是透明地重写 prompt。Dispatch 发出简单指令（"start working"），Hook 将其扩展为包含完整 context 的详细 prompt。Dispatch 完全不知道注入了什么。

#### Pattern 3: Ralph Loop（Completion Markers）

```python
# ralph-loop.py:173-210
def get_completion_markers(repo_root, task_dir):
    # 从 check.jsonl 的 reason 字段动态生成 markers
    marker = f"{reason.upper().replace(' ', '_')}_FINISH"
    # 例如 {"reason": "TypeCheck"} → "TYPECHECK_FINISH"
```

设计意图：Completion markers 从 JSONL 数据动态生成，而非硬编码。添加新的检查项只需在 `check.jsonl` 中添加条目，Ralph Loop 自动要求对应的 marker。

#### Pattern 4: Dual Verification Strategy

```python
# ralph-loop.py:333-391
verify_commands = get_verify_commands(repo_root)
if verify_commands:
    # 程序化验证：运行实际命令
    passed, message = run_verify_commands(repo_root, commands)
else:
    # Marker 验证：检查 agent 输出中的 completion markers
    markers = get_completion_markers(repo_root, task_dir)
    all_complete, missing = check_completion(agent_output, markers)
```

设计意图：优先使用程序化验证（`worktree.yaml` 中的 verify commands），fallback 到 marker 检查。这允许项目逐步从 "信任 agent" 过渡到 "程序化验证"。

#### Pattern 5: `[finish]` Marker 路由

```python
# inject-subagent-context.py:757-758
is_finish_phase = "[finish]" in original_prompt.lower()
# 同一个 check agent，根据 prompt 中的标记接收不同 context
```

设计意图：复用 check agent 定义，通过 prompt 中的标记切换 context 注入策略。避免为 finish 阶段创建独立的 agent 定义。

#### Pattern 6: Scope-Aware Spec Injection

```python
# session-start.py:232-288
def _resolve_spec_scope(is_mono, packages, scope, task_pkg, default_pkg):
    if scope == "active_task":
        return {task_pkg}  # 只注入当前任务 package 的 spec
    if isinstance(scope, list):
        return set(scope)  # 注入指定 package 列表的 spec
```

设计意图：monorepo 中避免注入所有 package 的 spec（token 浪费），通过 `config.yaml` 的 `spec_scope` 配置精确控制。

### 6C. Design Highlights — Macro（哲学/方法论）

#### Philosophy 1: "Specs Injected, Not Remembered"

核心理念：不依赖 AI 的 "记忆" 来遵守规范，而是通过 Hook 系统在每次 agent 调用时强制注入完整 context。

体现：
- SessionStart hook 注入 workflow + guidelines（`session-start.py:291-393`）
- PreToolUse hook 注入 JSONL context（`inject-subagent-context.py:717-798`）
- `start.md:380-384`："Code-spec context is injected, not remembered"

#### Philosophy 2: "Pure Dispatcher" 模式

Dispatch agent 被设计为零知识编排器：只知道 phase 顺序，不知道 spec 内容，不做任何决策。所有智能都在 subagent 和 hook 中。

体现：
- `dispatch.md:29-31`："You are a pure dispatcher"
- `dispatch.md:210`："Do not read spec/requirement files directly"
- Hook 自动更新 `current_phase`，dispatch 不需要管理状态

#### Philosophy 3: "Human Commits" 原则

AI 永远不应该执行 `git commit`。唯一的 commit 路径是 `create_pr.py`，且只在 pipeline 的最后阶段执行。

体现：
- `implement.md:30-36`：显式禁止 git commit/push/merge
- `workflow.md:342`："Don't execute git commit - AI should not commit code"
- `create_pr.py:17`："This is the only action that performs git commit"

#### Philosophy 4: Task-Centered Context

所有 context 围绕 task directory 组织。每个 task 是一个自包含的工作单元，包含需求（prd.md）、技术设计（info.md）、context 配置（*.jsonl）、和状态（task.json）。

体现：
- `.trellis/.current-task` 指向当前 task directory
- Hook 从 task directory 读取 JSONL 文件
- `create_pr.py` 从 task directory 读取 prd.md 作为 PR body

#### Philosophy 5: Progressive Verification

验证从 "信任 agent 输出" 逐步升级到 "程序化验证"：
1. 无 verify commands → 依赖 completion markers（信任 agent）
2. 配置 verify commands → 运行实际命令（程序化验证）
3. Ralph Loop 最大迭代限制 → 安全阀（防止无限循环）

### 6D. Cross-cutting Interconnections

| 连接 | 组件 A | 组件 B | 交互方式 |
|------|--------|--------|----------|
| Context 注入链 | `task.py init-context` → JSONL files | `inject-subagent-context.py` → agent prompt | JSONL 文件是桥梁，plan 阶段写入，hook 阶段读取 |
| Phase 追踪 | `dispatch.md`（调用 subagent） | `inject-subagent-context.py`（更新 phase） | Hook 自动推进 phase，dispatch 无需管理 |
| Ralph Loop ↔ JSONL | `check.jsonl`（reason 字段） | `ralph-loop.py`（生成 markers） | JSONL 的 reason 字段同时服务于 context 注入和退出验证 |
| Finish ↔ Spec | `finish` phase（检测新模式） | `spec/*.md`（更新 guideline） | Finish agent 是 spec 的主动维护者 |
| Worktree ↔ Task | `start.py`（创建 worktree） | `task.json`（记录 worktree_path） | Task 和 worktree 双向绑定 |
| Submodule ↔ PR | `config.yaml`（packages + type: submodule） | `create_pr.py`（submodule PR flow） | Monorepo 中 submodule 变更触发独立 PR 流程 |
| StatusLine ↔ Task | `statusline.py`（读取 .current-task） | `task.json`（title, status, priority） | 实时显示当前任务状态 |
| Lifecycle Hooks ↔ External | `config.yaml`（hooks.after_create 等） | `linear_sync.py`（同步到 Linear） | Task 生命周期事件触发外部系统同步 |


## 7. Migration Assessment

### 迁移到 1st-cc-plugin 的可行性评估

| 机制 | 可迁移性 | 工作量 | 前置条件 | 风险 | 失败模式 |
|------|----------|--------|----------|------|----------|
| **JSONL-Driven Context Injection** | Direct | M | 需要 PreToolUse hook 支持（Claude Code plugin hooks API） | Plugin hook 的 `updatedInput` 能力可能受限 | Hook timeout 导致 context 注入失败；JSONL 文件路径在不同项目中不通用 |
| **Ralph Loop（SubagentStop 验证）** | Direct | M | 需要 SubagentStop hook 支持 | 不同项目的 verify commands 差异大 | MAX_ITERATIONS 设置不当导致过早退出或无限循环；completion markers 被 agent 伪造 |
| **Session Start Context Injection** | Direct | S | SessionStart hook 已被 Claude Code plugin 支持 | Token 预算限制可能截断注入内容 | Spec 文件过多导致 context window 溢出 |
| **Task-Centered Workflow** | Inspired | L | 需要完整的 task.py 脚本生态 | 与现有 1st-cc-plugin 的 skill/command 模型冲突 | 用户不愿维护 .trellis/ 目录结构；task.json schema 演进困难 |
| **Pure Dispatcher Pattern** | Inspired | S | 需要 multi-agent Task 工具支持 | 依赖 Claude Code 的 Task/Agent 工具 API | Dispatch agent 不遵守 "pure" 约束；phase 推进逻辑与 hook 耦合 |
| **Brainstorm → PRD → Research → Implement Pipeline** | Inspired | M | 需要 task directory 结构 | 流程过重，简单任务不需要 | 用户跳过 brainstorm 直接实现；PRD 质量低导致后续 agent 产出差 |
| **Worktree-Based Parallel Execution** | Direct | M | 需要 git worktree 支持 + registry 管理 | Worktree 中 submodule 初始化复杂 | Worktree 清理不干净；多个 agent 竞争同一分支 |
| **Spec Library（分层 spec 目录）** | Inspired | S | 需要项目有 spec 目录结构 | 每个项目的 spec 结构不同 | Spec 文件过时不更新；index.md 与实际文件不同步 |
| **StatusLine Hook** | Direct | S | StatusLine hook 支持 | 低风险 | 信息过多导致状态栏拥挤 |
| **Dual Verification Strategy** | Direct | S | 需要 SubagentStop hook | 低风险 | Verify commands 在不同环境中行为不一致 |
| **`[finish]` Marker 路由** | Direct | S | 需要 PreToolUse hook | 低风险 | Marker 格式变化导致路由失败 |
| **Plan Agent 拒绝机制** | Inspired | S | 需要 agent 定义支持 | 依赖 LLM 遵从度 | 过度拒绝或放过不合理需求 |
| **Task Lifecycle Hooks（外部同步）** | Non-transferable | - | 依赖 config.yaml + 自定义脚本 | 与 plugin 架构不兼容 | - |
| **Developer Identity System** | Non-transferable | - | 依赖 .developer 文件 + workspace 目录 | 与 plugin 的无状态模型冲突 | - |
| **Journal / Session Recording** | Non-transferable | - | 依赖 workspace 目录结构 | 与 plugin 的无状态模型冲突 | - |

### 优先迁移建议

**第一优先级（Direct, S/M effort, 高价值）：**

1. **JSONL-Driven Context Injection** — 这是 Trellis 最核心的创新。将 "agent 需要什么 context" 从 prompt 解耦到数据文件，使 context 配置可编程、可版本化。可以作为 `1st-cc-plugin` 的 hook 机制实现。

2. **Ralph Loop** — 唯一的 Hard-enforced 质量门。SubagentStop hook + completion markers / verify commands 的双重验证策略，直接可移植。

3. **`[finish]` Marker 路由** — 极低成本的 prompt 路由技巧，通过 prompt 中的标记切换 context 注入策略。

**第二优先级（Inspired, 需要适配）：**

4. **Pure Dispatcher Pattern** — 将编排逻辑与执行逻辑分离的思想，可以启发 `superpowers` 或 `complex-task` workflow 的设计。

5. **Brainstorm → PRD Pipeline** — 结构化的需求发现流程，可以启发 `clarify` 或 `deep-plan` skill 的增强。

**不建议迁移：**

- Task Lifecycle Hooks、Developer Identity、Journal System — 这些是 Trellis 作为 "项目级 harness" 的特性，与 `1st-cc-plugin` 的 "可插拔 skill" 模型不兼容。


## 8. Failure Modes

### FM-1: Context Window 溢出

**触发条件**：monorepo 中 spec 文件过多，session-start hook 注入所有 package 的 index.md + workflow.md + start.md，加上 JSONL context 注入的具体文件。

**影响**：Agent 接收的 context 超过 context window 限制，导致早期注入的内容被截断或遗忘。

**现有缓解**：`spec_scope` 配置（`session-start.py:232-288`）限制注入的 package 范围。但 JSONL context 注入没有 token 预算控制。

**残余风险**：JSONL 文件中引用的文件总量无上限，`read_jsonl_entries` 的 `max_files=20` 限制仅针对目录类型条目（`inject-subagent-context.py:185`）。

### FM-2: Completion Marker 伪造

**触发条件**：Check agent 输出 `TYPECHECK_FINISH` 等 markers 但未实际运行对应命令。

**影响**：Ralph Loop 被绕过，未验证的代码进入 PR。

**现有缓解**：`ralph-loop.py:376-388` 在 block 消息中警告 "You must ACTUALLY run the checks, not just output the markers"。`worktree.yaml` 的 `verify` 配置提供程序化验证替代方案。

**残余风险**：当 verify commands 未配置时（默认状态），完全依赖 agent 自律。警告文本的有效性取决于 LLM 的指令遵从度。

### FM-3: Git Commit 禁令绕过

**触发条件**：Implement 或 Check agent 通过 Bash 工具执行 `git commit`。

**影响**：违反 "Human Commits" 原则，未经人类验证的代码被提交。

**现有缓解**：仅 prompt 级声明（`implement.md:30-36`），无 PreToolUse hook 拦截。

**残余风险**：高。这是 Trellis 声称的核心安全原则，但缺乏 Hard enforcement。建议添加 PreToolUse hook 拦截 `Bash(git commit)` / `Bash(git push)` 调用。

### FM-4: Plan Agent 误判

**触发条件**：Plan agent 错误地拒绝合理需求，或接受模糊需求。

**影响**：合理需求被阻塞（false reject），或垃圾需求进入 pipeline 导致后续 agent 产出低质量代码（false accept）。

**现有缓解**：`plan.md:19-103` 定义了 5 类拒绝条件和示例。`REJECTED.md` 提供拒绝原因和重试建议。

**残余风险**：中。LLM 的判断力有限，特别是对 "Too Large / Should Be Split" 的判断高度主观。

### FM-5: JSONL 配置不完整

**触发条件**：`init-context` 生成的默认 JSONL 条目不覆盖任务所需的关键 spec 文件，且 research agent 未发现遗漏。

**影响**：Implement agent 在缺少关键 context 的情况下编码，产出不符合项目规范的代码。

**现有缓解**：`task.py validate` 验证 JSONL 中引用的文件是否存在（`task_context.py`），但不验证是否 "足够"。

**残余风险**：中。"足够" 是语义判断，无法程序化验证。Research agent 的搜索质量直接影响 JSONL 配置质量。

### FM-6: Worktree 状态泄漏

**触发条件**：多个 parallel agent 在不同 worktree 中工作，但 worktree 清理不完整，或 submodule 状态不一致。

**影响**：残留的 worktree 占用磁盘空间；submodule HEAD 被意外 detach。

**现有缓解**：`cleanup.py` 提供 worktree 清理功能。`start.py:76-174` 的 `_init_submodules_for_task` 检查 submodule 状态前缀（`-`/` `/`+`/`U`）并做相应处理。

**残余风险**：低。但 `cleanup.py` 需要手动调用，无自动清理机制。

### FM-7: Ralph Loop 状态文件竞争

**触发条件**：多个 check agent 同时运行（不同 task），共享同一个 `.trellis/.ralph-state.json` 文件。

**影响**：迭代计数被错误重置或递增，导致 Ralph Loop 行为异常。

**现有缓解**：状态文件按 `task` 字段区分（`ralph-loop.py:296`），task 变化时重置状态。

**残余风险**：低。每个 worktree 有独立的 `.trellis/` 目录，parallel agent 不共享状态文件。但在 single-session 模式下快速切换 task 可能触发竞争。

### FM-8: Hook Timeout

**触发条件**：`session-start.py` 的 `get_context.py` 子进程超时（5 秒限制），或 `inject-subagent-context.py` 读取大量 JSONL 文件超过 30 秒 timeout。

**影响**：Context 注入失败，agent 在无 context 的情况下工作。

**现有缓解**：`session-start.py:59`（`timeout=5`），`settings.json` 中 `inject-subagent-context` 的 `timeout: 30`。失败时 `run_script` 返回 "No context available"（`session-start.py:63`）。

**残余风险**：中。大型 monorepo 中 spec 文件多时，5 秒可能不够。注入失败是静默的（返回 fallback 文本），agent 不知道自己缺少 context。
