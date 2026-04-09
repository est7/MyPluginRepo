# Claude-Code-Workflow (CCW) 逆向工程研究报告

> **目标仓库**: `vendor/Claude-Code-Workflow` (catlog22/Claude-Code-Workflow v7.2.30)
> **分析日期**: 2026-04-08
> **文件总数**: 2502（Large 级别）
> **框架类型**: JSON 驱动的多 Agent 工作流编排框架，含 CLI 工具、技能系统、团队协调、会话管理

---

## 目录

1. [Source Inventory](#1-source-inventory)
2. [Object Model](#2-object-model)
3. [State Machine & Flow Analysis](#3-state-machine--flow-analysis)
4. [Enforcement Audit](#4-enforcement-audit)
5. [Prompt Catalog & Design Analysis](#5-prompt-catalog--design-analysis)
6. [Migration Assessment](#6-migration-assessment)

---

## 1. Source Inventory

### 1.1 Overview（概述层）

| 文件 | 用途 |
|------|------|
| `README.md` | 项目概述，v7.0 特性列表，安装指南 |
| `WORKFLOW_GUIDE.md` | 完整工作流文档：Skills vs Commands、Session Lifecycle、Team Architecture v2 |
| `SPEC.md` | Symphony 服务规范——长时运行的 issue-to-PR 自动化守护进程设计（语言无关） |
| `package.json` | npm 包定义，v7.2.30，依赖 better-sqlite3、MCP SDK、tree-sitter 等 |
| `.claude/CLAUDE.md` | Claude 指令：CLI 使用规范、会话感知、工件位置表 |

### 1.2 Execution（执行层）

| 路径 | 用途 |
|------|------|
| `.claude/skills/workflow-plan/SKILL.md` | 四阶段规划主流程（Session → Context → Conflict → TaskGen） |
| `.claude/skills/workflow-execute/SKILL.md` | 自治执行引擎：会话发现 → TodoWrite 跟踪 → Agent 编排 → 完成 |
| `.claude/skills/workflow-lite-plan/SKILL.md` | 轻量规划：explore → clarify → plan → confirm → handoff |
| `.claude/skills/team-coordinate/SKILL.md` | 通用团队协调：动态角色生成 + team-worker 架构 |
| `.claude/agents/team-worker.md` | 统一 Worker Agent：Phase 1(任务发现) → Phase 2-4(角色规范) → Phase 5(报告) |
| `.claude/agents/universal-executor.md` | 通用执行 Agent：任务评估 → 执行 → 质量门控 |
| `.claude/agents/code-developer.md` | 代码开发专用 Agent |
| `ccw/src/` | CLI 工具源码（TypeScript）：命令、服务、MCP server |

### 1.3 Prompts（提示词层）

| 路径 | 用途 |
|------|------|
| `.ccw/workflows/coding-philosophy.md` | 编码哲学：极致简洁、不隐藏问题、学习现有代码 |
| `.ccw/workflows/cli-tools-usage.md` | CLI 工具执行规范：模式定义、提示构建、自动调用触发器 |
| `.ccw/workflows/cli-templates/prompts/*.txt` | 24+ 模板化提示词（分析、开发、文档、验证等） |
| `.ccw/workflows/cli-templates/planning-roles/*.md` | 10 种规划角色定义（产品经理、架构师、UX 专家等） |

### 1.4 Enforcement（强制层）

| 路径 | 用途 |
|------|------|
| `ccw/src/core/hooks/stop-handler.ts` | 停止事件处理器：soft enforcement，注入续航消息 |
| `ccw/src/core/hooks/keyword-detector.ts` | 魔法关键词检测：15 种模式（autopilot、tdd、team 等） |
| `ccw/src/core/hooks/context-limit-detector.ts` | 上下文限制检测：防止 compact 死锁 |
| `ccw/src/core/hooks/recovery-handler.ts` | PreCompact 恢复：checkpoint + 互斥锁 |
| `.ccw/workflows/cli-templates/schemas/*.json` | 23 个 JSON Schema 定义所有数据结构 |

### 1.5 Evolution（演化层）

| 路径 | 用途 |
|------|------|
| `.claude/skills/_shared/SKILL-DESIGN-SPEC.md` | Skill 设计规范 v1.0：目录结构、质量门控、Completion Status Protocol |
| `.claude/skills/_shared/COMMAND-TO-SKILL-CONVERSION.md` | Command 到 Skill 的转换规范 |
| `.claude/skills/wf-composer/SKILL.md` | 语义工作流编排器：自然语言 → DAG → 可复用模板 |
| `.claude/skills/wf-player/SKILL.md` | 工作流模板播放器：加载 → 实例化 → 执行 → 完成 |
| `.claude/skills/skill-generator/SKILL.md` | 元技能：从需求生成新 Skill |
| `.claude/skills/team-designer/SKILL.md` | 元团队：自动生成团队技能包 |

---

## 2. Object Model

### 2.1 核心实体

#### Entity 1: Task（任务）

**Schema**: `.ccw/workflows/cli-templates/schemas/task-schema.json`

```json
{
  "id": "IMPL-001",
  "title": "动词+目标",
  "description": "目标+原因",
  "depends_on": ["IMPL-000"],
  "convergence": {
    "criteria": ["可测试的完成条件"],
    "verification": "验证命令"
  },
  "files": [{ "path": "...", "action": "modify", "change": "..." }],
  "implementation": [{ "step": 1, "description": "..." }],
  "meta": { "agent": "@code-developer", "execution_config": { "method": "agent" } },
  "status": "pending | in_progress | completed | failed | skipped | blocked"
}
```

**分类**: Fact Object（事实对象）+ Judgment Object（`rationale`、`risks` 字段含决策判断）

**生命周期**: `pending` → `in_progress`（Agent 认领）→ `completed`/`failed` → 可通过 `replan` 回退

#### Entity 2: Workflow Session（工作流会话）

**路径**: `.workflow/active/WFS-*/workflow-session.json`

```json
{
  "session_id": "WFS-auth-2026-04-01",
  "status": "planning | active | completed | archived",
  "project": "项目名",
  "execution_started_at": "ISO8601"
}
```

**分类**: Fact Object（纯状态容器）

**生命周期**: `planning`（workflow-plan 创建）→ `active`（workflow-execute 激活）→ `completed`（session:complete 归档）→ `archived`

#### Entity 3: Team Session（团队会话）

**路径**: `.workflow/.team/TC-<slug>-<date>/team-session.json`

**Schema**: 定义于 `.claude/skills/team-coordinate/SKILL.md`

```json
{
  "session_id": "TC-<slug>-<date>",
  "status": "active | paused | completed",
  "team_name": "<team-name>",
  "roles": [{ "name": "...", "prefix": "...", "role_spec": "role-specs/<name>.md" }],
  "pipeline": { "dependency_graph": {}, "tasks_total": 0, "tasks_completed": 0 }
}
```

**分类**: Evidence Object（记录团队协作过程的证据链）

#### Entity 4: Plan（计划）

**Schema**: `.ccw/workflows/cli-templates/schemas/plan-json-schema.json`（标记为 deprecated，迁移到 `plan-overview-base-schema.json` + `task-schema.json`）

核心字段：`summary`、`approach`、`tasks[]`、`complexity`、`flow_control`、`design_decisions[]`

**分类**: Judgment Object（包含方案选择、替代方案对比、风险评估）

#### Entity 5: Queue（执行队列）

**Schema**: `.ccw/workflows/cli-templates/schemas/queue-schema.json`

支持 solution-level（S-N）和 task-level（T-N）粒度，包含冲突检测、执行分组（parallel/sequential）

**分类**: Fact Object（调度状态容器）

#### Entity 6: Verification Findings（验证发现）

**Schema**: `.ccw/workflows/cli-templates/schemas/verify-json-schema.json`

8 维验证（用户意图对齐、需求覆盖、一致性、依赖完整性等），4 级严重度，4 级质量门控推荐（BLOCK_EXECUTION → PROCEED）

**分类**: Judgment Object（人工评审判断的结构化编码）

### 2.2 实体关系

```
Plan 1:N Task (plan.task_ids[] → .task/TASK-*.json)
Session 1:N Task (session 内 .task/ 目录)
Task N:N Task (depends_on[] 形成 DAG)
Queue 1:N Task/Solution (调度容器)
Team Session 1:N Role-Spec (session/role-specs/)
Team Session 1:N Artifact (session/artifacts/)
Verification → Plan (session_id 关联)
```

### 2.3 上下文隔离策略

| 隔离机制 | 实现方式 | 证据 |
|----------|----------|------|
| **会话目录隔离** | 每个工作流有独立的 `.workflow/` 子目录 | `.claude/CLAUDE.md` Artifact Locations 表 |
| **Phase 渐进加载** | SKILL.md 仅在 Phase 即将执行时才 `Read()` 对应文件 | `workflow-plan/SKILL.md:201` "Progressive Phase Loading" |
| **任务 JSON 懒加载** | 执行阶段才读取 task JSON，不预加载 | `workflow-execute/SKILL.md:51` "Lazy Loading" |
| **角色前缀隔离** | Worker 只处理自己前缀的 Task | `team-worker.md:99` "Filter tasks matching ALL criteria" |
| **Compact 保护** | TodoWrite `in_progress` 的 Phase 不可压缩 | `workflow-plan/SKILL.md:122-125` Compact Directive |
| **跨 Skill 上下文隔离** | lite-plan 明确声明与 analyze-with-file 的上下文完全切断 | `workflow-lite-plan/SKILL.md:16` "CRITICAL: Context Isolation" |

---

## 3. State Machine & Flow Analysis

### 3.1 主流程状态机：workflow-plan → workflow-execute

```
                        ┌──────────────────────────────────────────────────┐
                        │              workflow-plan SKILL                    │
                        │                                                    │
                        │  User Input                                        │
                        │    │                                               │
                        │    ▼                                               │
                        │  [Mode Detection: plan | verify | replan]          │
                        │    │                                               │
                        │    ├─ plan ─────────────────────────────┐          │
                        │    │   Phase 1: Session Discovery       │          │
                        │    │     │                              │          │
                        │    │   Phase 2: Context Gathering       │          │
                        │    │     │ (output: contextPath +       │          │
                        │    │     │  conflictRisk)               │          │
                        │    │     │                              │          │
                        │    │   [conflictRisk ≥ medium?]         │          │
                        │    │     ├─ Yes → Phase 3: Conflict     │          │
                        │    │     │         Resolution           │          │
                        │    │     └─ No ──┐                     │          │
                        │    │             │                      │          │
                        │    │   Phase 4: Task Generation         │          │
                        │    │     │                              │          │
                        │    │   [User Decision Gate]             │          │
                        │    │     ├─ Verify → Phase 5            │          │
                        │    │     ├─ Execute → workflow-execute  │          │
                        │    │     └─ Review → inline display     │          │
                        │    │                                    │          │
                        │    ├─ verify → Phase 5                  │          │
                        │    └─ replan → Phase 6                  │          │
                        └──────────────────────────────────────────────────┘

                        ┌──────────────────────────────────────────────────┐
                        │           workflow-execute SKILL                   │
                        │                                                    │
                        │  Phase 1: Discovery (session selection)            │
                        │    │                                               │
                        │  Phase 2: Planning Document Validation             │
                        │    │                                               │
                        │  Phase 3: TodoWrite Generation                     │
                        │    │                                               │
                        │  Phase 4: Strategy Parse + Task Execution Loop     │
                        │    │   ┌──────────────────────┐                   │
                        │    │   │ get next in_progress  │                   │
                        │    │   │ lazy load task JSON   │                   │
                        │    │   │ launch Agent          │                   │
                        │    │   │ mark completed        │                   │
                        │    │   │ [with-commit] commit  │                   │
                        │    │   │ advance next          │                   │
                        │    │   └──────┬───────────────┘                   │
                        │    │          │ (loop until all done)              │
                        │    │                                               │
                        │  Phase 5: Completion                               │
                        │    ├─ Enter Review → Phase 6                      │
                        │    └─ Complete Session → archive                   │
                        └──────────────────────────────────────────────────┘
```

**证据**: `workflow-plan/SKILL.md:127-175`, `workflow-execute/SKILL.md:78-135`

### 3.2 团队协调状态机：team-coordinate

```
User Task Description
  │
  ▼
Phase 1: Task Analysis
  (signal detection, capability mapping, dependency graph)
  │ → task-analysis.json
  ▼
Phase 2: Role-Spec Generation + Session Init
  (max 5 roles, generate .md role-specs)
  │ → role-specs/<role>.md, team-session.json
  ▼
Phase 3: Task Chain Creation
  (DAG from dependency graph, TaskCreate entries)
  │
  ▼
Phase 4: Worker Spawning ← ── ── ── ── ── ── ┐
  (spawn team-worker agents, background)       │
  │                                             │
  ▼                                             │
Worker Executes → SendMessage callback          │
  │                                             │
  ▼                                             │
Coordinator advances next step ─── ── ── ── ── ┘
  │
  (loop until pipeline complete)
  │
  ▼
Phase 5: Completion
  ├─ Archive & Clean
  ├─ Keep Active
  └─ Export Results
```

**证据**: `team-coordinate/SKILL.md:84-92`, `team-coordinate/specs/pipelines.md`

### 3.3 Worker 内循环状态机

```
Entry (role, role_spec, session, inner_loop)
  │
  ▼
Load Role Spec (YAML frontmatter + Phase 2-4 body)
Load Wisdom Files
Initialize context_accumulator (inner_loop only)
  │
  ▼
┌─ Main Loop ──────────────────────────────┐
│ Phase 1: Task Discovery (built-in)        │
│   filter tasks by prefix + pending        │
│   claim task (TaskUpdate in_progress)     │
│   │                                       │
│   ▼                                       │
│ Phase 2-4: Role Spec Execution            │
│   (domain-specific logic from .md)        │
│   │                                       │
│   ▼                                       │
│ Phase 5: Report                           │
│   ├─ 5-L (loop): update + accumulate     │
│   │   → back to Phase 1                  │
│   └─ 5-F (final): SendMessage            │
│       to coordinator → STOP              │
└──────────────────────────────────────────┘

Interrupt: consensus_blocked HIGH or errors >= 3 → STOP
```

**证据**: `team-worker.md:59-75`

### 3.4 Happy Path 与 Failure Path

**Happy Path**: `workflow-plan` (4 phases) → `workflow-execute` (auto loop) → `session:complete`

**Failure Paths**:

| 失败场景 | 恢复机制 | 证据 |
|----------|----------|------|
| Agent 执行失败 | 重试 2 次，简化上下文 | `workflow-execute/SKILL.md:583` |
| Worker crash (team) | Coordinator 检测孤立 in_progress，重置为 pending 后重新 spawn | `team-worker.md:396` |
| 3 次假设失败 | 3-Strike 升级，输出诊断转储 | `investigate/SKILL.md:27`, `SKILL-DESIGN-SPEC.md:749-797` |
| Context compact | Checkpoint 创建 + TodoWrite 保护 | `recovery-handler.ts:1-13`, `workflow-plan/SKILL.md:122` |
| 会话损坏 | JSON 文件原子更新 + 备份策略 | `workflow-execute/SKILL.md:588-589` |

### 3.5 并行 vs 串行门控

| 机制 | 类型 | 证据 |
|------|------|------|
| task `depends_on[]` DAG | 串行门控 | `task-schema.json:67-71` |
| `parallel_group` 字段 | 并行标记 | `task-schema.json:75-76` |
| execution_groups (P*/S*) | 显式并行/串行分组 | `queue-schema.json:47-49` |
| `blockedBy` (Team Tasks) | 串行门控 | `team-coordinate/specs/pipelines.md:46-49` |
| inner_loop (Worker) | 同角色任务串行执行 | `team-worker.md:77` |
| `flow_control.execution_order` | Plan 级并行/串行声明 | `plan-json-schema.json:353-393` |

---

## 4. Enforcement Audit

### 4.1 Hard-Enforced（代码/Hook 强制）

| 行为声明 | 强制机制 | 证据 |
|----------|----------|------|
| CLI `--mode analysis` 为只读 | `--mode` 参数控制实际权限，CLI 工具层面限制写操作 | `cli-tools-usage.md:36-38` "mode is the authoritative permission control" |
| 上下文限制时允许停止 | `context-limit-detector.ts` 检测 9 种模式，`stop-handler.ts` 始终返回 `continue: true` | `context-limit-detector.ts:41-51`, `stop-handler.ts:11` |
| Magic Keyword 模式触发 | `keyword-detector.ts` 15 种正则 + 优先级排序 | `keyword-detector.ts:47-63` |
| PreCompact checkpoint | `recovery-handler.ts` 在 compact 前创建 checkpoint + 互斥锁 | `recovery-handler.ts:7-9` |
| JSON Schema 结构验证 | 23 个 Schema 文件定义所有数据格式 | `.ccw/workflows/cli-templates/schemas/` |

### 4.2 Soft-Enforced（提示词指令但无代码强制）

| 行为声明 | 指令位置 | 为什么是 Soft |
|----------|----------|-------------|
| "ALWAYS use `run_in_background: false` for Agent tool calls" | `.claude/CLAUDE.md:15` | 纯提示词指令，无 hook 拦截违规调用 |
| "ONE AGENT = ONE TASK JSON" | `workflow-execute/SKILL.md:63` | 提示词约束，Agent 技术上可批量处理多个 |
| Phase 渐进加载（不提前读取） | `workflow-plan/SKILL.md:47,201` | 只是 SKILL.md 中的设计原则指令 |
| TodoWrite `in_progress` 不可压缩 | `workflow-plan/SKILL.md:122-125` | Compact Directive 是给 Claude 的指令，无 hook 强制 |
| Worker 不可调用 Agent() | `team-worker.md:127-130` | 文档声明 + 工具限制（Worker 上下文无 Agent 权限），但非显式 hook |
| Coordinator MUST NOT 读源码 | `team-coordinate/roles/coordinator/role.md:29` | 纯角色定义约束 |
| "No fix without confirmed root cause" (Iron Law) | `investigate/SKILL.md:9-10` | Phase 4 有 GATE 标记但无代码验证 |
| 3-Strike escalation | `SKILL-DESIGN-SPEC.md:749-757` | 设计规范指导，每个 Skill 自行实现 |

### 4.3 Unenforced（文档提及但实际缺失）

| 行为声明 | 声称位置 | 缺失分析 |
|----------|----------|----------|
| "Atomic Updates: Update JSON files atomically" | `workflow-execute/SKILL.md:589` | 实际使用 `jq ... > tmp.json && mv tmp.json` 模式，非真正原子操作（mv 跨 fs 非原子） |
| Quality Gate 自动评分 | `SKILL-DESIGN-SPEC.md:554-589` | 定义了 `runQualityChecks()` 函数模板但为伪代码，未找到实际实现 |
| Completion Status Protocol（4 状态终止） | `SKILL-DESIGN-SPEC.md:674-744` | 规范完善但多数 Skill 未显式输出结构化状态块 |
| "Prefer `mcp__ide__getDiagnostics`" | `.claude/CLAUDE.md:60` | 偏好指令，无阻止使用 shell 编译的机制 |
| `review` mode 为 Codex only | `cli-tools-usage.md:37` | 文档声明但无明确校验其他工具不使用此 mode |

---

## 5. Prompt Catalog & Design Analysis

### 5A. Key Prompt Catalog

#### Prompt 1: workflow-plan 编排器

| 字段 | 值 |
|------|-----|
| **role** | 纯编排器（Pure Orchestrator） |
| **repo_path** | `.claude/skills/workflow-plan/SKILL.md` |
| **quote_excerpt** | `"Pure Orchestrator: SKILL.md routes and coordinates only; execution detail lives in phase files"` |
| **stage** | plan / verify / replan (tri-mode) |
| **design_intent** | 将规划拆分为 4 个独立 Phase 文件，编排器只做路由和数据传递 |
| **hidden_assumption** | 假设 Phase 输出可靠解析——parsing failure 仅重试一次 |
| **likely_failure_mode** | Phase 间数据传递丢失（compact 后 planning-notes.md 被压缩），sentinel 恢复机制依赖 Claude 遵守 compact directive |

#### Prompt 2: team-worker 统一 Worker

| 字段 | 值 |
|------|-----|
| **role** | 动态角色 Worker |
| **repo_path** | `.claude/agents/team-worker.md` |
| **quote_excerpt** | `"Built-in phases (Phase 1, Phase 5): Task discovery, reporting, pipeline notification, inner loop — defined below. Role-specific phases (Phase 2-4): Loaded from a role_spec markdown file."` |
| **stage** | Phase 1(built-in) → Phase 2-4(role-spec) → Phase 5(built-in) |
| **design_intent** | 所有角色共享 Phase 1/5 的任务发现和报告逻辑，中间层完全由外部 .md 文件注入 |
| **hidden_assumption** | role_spec .md 文件格式正确（YAML frontmatter + 正文），且 prefix 唯一 |
| **likely_failure_mode** | Agent 名称后缀问题——文档明确指出 "Do NOT filter by owner name" 因为系统会追加数字后缀（如 `profiler` → `profiler-4`） |

#### Prompt 3: workflow-execute 自治引擎

| 字段 | 值 |
|------|-----|
| **role** | 自治执行引擎 |
| **repo_path** | `.claude/skills/workflow-execute/SKILL.md` |
| **quote_excerpt** | `"Execute entire workflow without user interruption (except initial session selection if multiple active sessions exist)"` |
| **stage** | Discovery → Validation → TodoWrite → Execution Loop → Completion |
| **design_intent** | 全自治执行，用户仅在多会话选择和最终完成时介入 |
| **hidden_assumption** | Agent 会正确更新 TODO_LIST.md，编排器不做此更新 |
| **likely_failure_mode** | Agent 崩溃后 TODO_LIST.md 状态不一致，resume 时发现 in_progress 任务无法自动恢复 |

#### Prompt 4: investigate Iron Law

| 字段 | 值 |
|------|-----|
| **role** | 系统调试员 |
| **repo_path** | `.claude/skills/investigate/SKILL.md` |
| **quote_excerpt** | `"No fix without confirmed root cause. Violation of the Iron Law (skipping to Phase 4 without Phase 3 confirmation) is prohibited."` |
| **stage** | Evidence → Pattern → Hypothesis → Fix → Verify |
| **design_intent** | 强制 5 阶段调试流程，防止跳过根因分析直接修复 |
| **hidden_assumption** | 3-Strike 规则能有效防止无限重试 |
| **likely_failure_mode** | Phase 4 GATE 仅为提示词标记，Claude 可在压力下跳过 |

#### Prompt 5: coding-philosophy 全局约束

| 字段 | 值 |
|------|-----|
| **role** | 全局行为约束 |
| **repo_path** | `.ccw/workflows/coding-philosophy.md` |
| **quote_excerpt** | `"NEVER: Generate reports, summaries, or documentation files without explicit user request"` |
| **stage** | 跨所有 Skill 全局生效 |
| **design_intent** | 防止 AI 过度生成无用文档和报告 |
| **hidden_assumption** | 通过 `@~/.ccw/workflows/coding-philosophy.md` 引用始终被 Claude 加载 |
| **likely_failure_mode** | `@` 路径引用在某些 Claude Code 版本中可能不被展开 |

### 5B. Micro Design Highlights（微观设计亮点）

#### Pattern 1: Task Attachment/Collapse（任务附着/折叠）

**位置**: `workflow-plan/SKILL.md:296-351`

```
Phase 开始 → sub-tasks ATTACHED to TodoWrite
sub-tasks 执行中 → 显示详细进度
Phase 完成 → sub-tasks COLLAPSED to summary
```

**价值**: 解决了长时运行 Phase 的 TodoWrite 可读性问题。Phase 2 可能有 3 个 sub-task，展开显示时用户看到细粒度进度；完成后折叠为一行，保持 TodoWrite 整洁。

#### Pattern 2: Compact 双重保险（TodoWrite + Sentinel）

**位置**: `workflow-plan/SKILL.md:120-125, 184-191`

```
保险 1: TodoWrite in_progress → Compact MUST 保留完整内容
保险 2: Phase 4 包含 sentinel 标记 → compact 后仅存 sentinel 时
         必须 Read() 恢复完整 Phase 文件
```

**价值**: 多层防御解决了长对话中 compact 丢失关键 Phase 指令的问题。

#### Pattern 3: 动态角色生成 + team-worker 统一 Agent

**位置**: `team-coordinate/SKILL.md:109-137`

```
Coordinator 分析任务 → 生成 role-spec .md 文件
  → 所有 Worker 都使用同一个 team-worker agent
  → Worker 读取 role-spec 获取 Phase 2-4 指令
```

**价值**: 将角色多样性与 Agent 定义解耦。无需为每种角色定义独立 Agent，一个 team-worker Agent + N 个轻量 .md 文件即可实现任意团队组合。

#### Pattern 4: Pre-Analysis Flow Control

**位置**: `task-schema.json:413-430`, `workflow-execute/SKILL.md:496-525`

```json
"pre_analysis": [
  { "step": "Read existing patterns", "action": "Grep ...", "on_error": "skip_optional" }
]
```

`[FLOW_CONTROL]` 标记触发 Agent 在实现前自动执行上下文收集步骤。编排器不执行这些步骤——完全由 Agent 自主解释。

**价值**: 让每个 Task 自带上下文准备指令，而非依赖全局上下文注入。

#### Pattern 5: Magic Keyword Priority Chain

**位置**: `keyword-detector.ts:47-74`

15 种关键词按优先级排序：`cancel > ralph > autopilot > ultrapilot > team > ultrawork > swarm > pipeline > ...`

**价值**: 单一输入框支持多种工作模式切换，且冲突时有明确优先级。

### 5C. Macro Design Highlights（宏观设计哲学）

#### Philosophy 1: JSON-Driven Everything

所有中间产物都有 JSON Schema 定义（23 个 Schema），从 Task 到 Plan 到 Queue 到 Discovery State。这不仅是数据格式标准化，更是 **跨 Agent/CLI/Session 的通信协议**。

**证据**: `task-schema.json:569-578` `_field_usage_by_producer` 字段明确记录哪些生产者使用哪些字段。

#### Philosophy 2: Skill 即最小完整执行单元

**证据**: `ccw.md:36-40`
```
"每个 Skill 内部处理完整流水线，是天然的最小执行单元。
单次 Skill 调用即完成一个有意义的工作里程碑。"
```

CCW 不是传统的"步骤 1、2、3"线性流程，而是 **Skill Composition**——每个 Skill 自包含完整 pipeline，Skill 之间通过文件系统（`.workflow/` 目录）传递上下文。

#### Philosophy 3: Soft Enforcement over Hard Gates

`stop-handler.ts:11` 明确写道：
```typescript
// ALWAYS returns continue: true (Soft Enforcement)
// Injects continuation message instead of blocking
```

CCW 选择注入消息引导而非阻断执行。这反映了一种 **实用主义的 AI 治理观**：与其强制阻止（可能导致死锁），不如注入足够的上下文让模型自行修正。

#### Philosophy 4: Multi-CLI Orchestration

CCW 不锁定单一 AI 后端。`ccw cli --tool gemini|qwen|codex|claude|opencode` 支持多种 CLI 工具，且有 fallback chain。这是框架的核心差异化：**将 AI 编码工具视为可互换的执行资源**。

### 5D. Cross-Cutting Interconnections

| 横切关注 | 涉及组件 | 机制 |
|----------|----------|------|
| **会话持久化** | 所有 Skill + Commands | `.workflow/` 目录树 + JSON 文件 |
| **TodoWrite 进度跟踪** | workflow-plan, workflow-execute, lite-plan, brainstorm | TodoWrite API + Attachment/Collapse 模式 |
| **Memory 跨会话** | memory-manage, memory-capture | `memory/MEMORY.md` + `.workflow/` 引用 |
| **CLI 分析反馈** | 所有包含 CLI 调用的 Skill | `ccw cli --mode analysis` + hook callback |
| **Quality Gates** | team-coordinate, review-code, spec-generator | 统一 4 维评分 + 3 级门控（Pass/Review/Fail） |
| **Compact Recovery** | 长时 Skill (workflow-plan, brainstorm) | TodoWrite 保护 + sentinel + PreCompact checkpoint |

---

## 6. Migration Assessment

### 6.1 可移植机制评估

#### Mechanism 1: Task Schema 统一任务模型

| 维度 | 评级 |
|------|------|
| **可迁移性** | ★★★★★ |
| **工作量** | Low |
| **前置条件** | JSON Schema 验证能力 |
| **风险** | Schema 字段过多可能导致认知负担 |
| **失败模式** | 过度设计——多数 Skill 只使用少量字段 |

**评估**: task-schema.json 是 CCW 最有价值的可迁移资产。统一的任务模型让不同生产者（plan、issue、review）的输出都能被同一个执行引擎消费。建议精简后采用。

#### Mechanism 2: Skill Phase 渐进加载模式

| 维度 | 评级 |
|------|------|
| **可迁移性** | ★★★★☆ |
| **工作量** | Low |
| **前置条件** | Skill 文件结构（SKILL.md + phases/） |
| **风险** | 低——纯提示词设计模式 |
| **失败模式** | Phase 间数据传递丢失（需要 planning-notes.md 或 TodoWrite 配合） |

**评估**: `phases/` 目录 + 按需 `Read()` 是轻量可靠的上下文管理方式。直接可用。

#### Mechanism 3: TodoWrite Attachment/Collapse

| 维度 | 评级 |
|------|------|
| **可迁移性** | ★★★★☆ |
| **工作量** | Low |
| **前置条件** | TodoWrite API 可用 |
| **风险** | 依赖 Claude Code 特有 API |
| **失败模式** | TodoWrite API 不稳定时退化为纯文本跟踪 |

**评估**: 设计模式价值极高，但强依赖 Claude Code 的 TodoWrite API。可以在支持类似 API 的环境中直接使用。

#### Mechanism 4: team-worker 统一 Agent + 动态 role-spec

| 维度 | 评级 |
|------|------|
| **可迁移性** | ★★★☆☆ |
| **工作量** | Medium |
| **前置条件** | 多 Agent 并行能力 + SendMessage 机制 |
| **风险** | 高度依赖 Claude Code 的 Agent/SendMessage/TaskCreate API |
| **失败模式** | 消息传递不可靠（Worker 无法接收 callback）、Agent 名称后缀导致路由错误 |

**评估**: 架构设计优秀但强绑定 Claude Code 原生 API。适合学习其角色分离思想，不适合直接搬运。1st-cc-plugin 已有 async-agent 插件，可以借鉴 role-spec 模板思想。

#### Mechanism 5: Compact 双重保险机制

| 维度 | 评级 |
|------|------|
| **可迁移性** | ★★★★☆ |
| **工作量** | Low |
| **前置条件** | 长时运行 Skill |
| **风险** | Sentinel 恢复依赖 Claude 遵守提示词 |
| **失败模式** | Compact 算法升级可能导致 sentinel 模式失效 |

**评估**: 两层防御（TodoWrite 保护 + sentinel）是处理长对话 compact 问题的实用方案。值得在 complex-task / deep-plan 等 Skill 中采用。

#### Mechanism 6: 23 JSON Schema 数据模型

| 维度 | 评级 |
|------|------|
| **可迁移性** | ★★★☆☆ |
| **工作量** | Medium (选择性采用) |
| **前置条件** | Schema 校验工具 |
| **风险** | 过度形式化可能降低灵活性 |
| **失败模式** | Schema 版本漂移——plan-json-schema.json 已标记 deprecated |

**评估**: task-schema.json 和 verify-json-schema.json 值得参考。但 23 个 Schema 整体迁移不现实——CCW 自身已出现 deprecated Schema 管理问题。

#### Mechanism 7: CLI Multi-Tool Orchestration

| 维度 | 评级 |
|------|------|
| **可迁移性** | ★★☆☆☆ |
| **工作量** | High |
| **前置条件** | ccw CLI 工具安装 + 多 CLI 后端配置 |
| **风险** | 强绑定 CCW npm 包、依赖 Gemini/Codex CLI |
| **失败模式** | CLI 版本不兼容、API 密钥管理复杂 |

**评估**: CCW 的核心差异化在于多 CLI 编排，但这也是其最难迁移的部分。1st-cc-plugin 已有 code-context 插件提供类似多源搜索能力，CCW 的 CLI orchestration 层过重，不建议直接引入。

#### Mechanism 8: Completion Status Protocol

| 维度 | 评级 |
|------|------|
| **可迁移性** | ★★★★★ |
| **工作量** | Low |
| **前置条件** | 无 |
| **风险** | 极低——纯约定 |
| **失败模式** | 无强制机制导致 Skill 不遵守 |

**评估**: 4 状态终止协议（DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT）+ 3-Strike Escalation 是可直接采用的通用模式。建议纳入 1st-cc-plugin 的 Skill 开发规范。

---

## Appendix: Pre-Submit Checklist

| 检查项 | 状态 |
|--------|------|
| A. Source Inventory classified (Overview/Execution/Prompts/Enforcement/Evolution) | PASS — Section 1 |
| B. Prompt Traceability with repo_path + quote_excerpt | PASS — Section 5A (5 prompts) |
| C. Object Model with 3+ entities | PASS — Section 2 (6 entities) |
| D. State Machine with transitions | PASS — Section 3 (3 state machines) |
| E. Enforcement Audit with Hard/Soft/Unenforced | PASS — Section 4 (5/8/5 items) |
| F. Micro + Macro design highlights | PASS — Section 5B (5 patterns) + 5C (4 philosophies) |
| G. 3+ failure modes with evidence | PASS — Section 3.4 (5 failure paths) + 5A (5 likely_failure_mode) |
| H. Migration candidates with ratings | PASS — Section 6 (8 mechanisms with ratings) |
