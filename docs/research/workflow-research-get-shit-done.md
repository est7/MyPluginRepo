# Workflow Research: Get Shit Done (GSD)

> 逆向工程分析报告 | 源仓库: `vendor/get-shit-done` | 版本: v1.34.2 | 分析日期: 2026-04-07

---

## 1. Executive Summary

GSD (Get Shit Done) 是一个面向 solo 开发者的 **meta-prompting + context engineering + spec-driven development** 框架，以 npm 包形式分发 (`get-shit-done-cc`)，支持 12 种 AI 编程运行时（Claude Code、Gemini CLI、OpenCode、Kilo、Codex、Copilot、Cursor、Windsurf、Antigravity、Augment、Trae、Cline）。

**核心问题域：** 解决 **context rot** —— 当 LLM 上下文窗口逐渐填满时，代码生成质量不断下降的现象。

**解法架构：** 通过 thin orchestrator + fresh subagent pattern 实现上下文隔离。每个执行阶段的 subagent 获得全新 200k token 上下文窗口；orchestrator 仅做路由、状态更新和结果收集，自身上下文消耗保持在 30-40%。

**规模指标：**

| 维度 | 数量 |
|------|------|
| Agent definitions | 24 (`agents/*.md`) |
| Slash commands | 68 (`commands/gsd/*.md`) |
| Workflow files | 68 (`get-shit-done/workflows/*.md`) |
| Reference docs | 35+ (`get-shit-done/references/*.md`) |
| Templates | 33+ (`get-shit-done/templates/*.md`) |
| Hooks | 9 (`hooks/`) |
| CLI library modules | 21 (`get-shit-done/bin/lib/*.cjs`) |
| SDK source files | 45 (`sdk/src/`) |
| Test files | 40k+ lines (`tests/*.test.cjs` + `sdk/src/*.test.ts`) |

**关键发现：**
1. 四层架构（Command → Workflow → Agent → CLI Tools）实现了关注点分离
2. 大部分 "enforcement" 是 soft/advisory，仅 Conventional Commits 验证和 research gate 是 hard-enforced
3. `gsd-tools.cjs` 是真正的状态管理核心，所有 STATE.md/ROADMAP.md 变更都应通过它
4. SDK（`@gsd-build/sdk`）提供了 headless 自主执行能力，使用 `@anthropic-ai/claude-agent-sdk`
5. 项目从 2025-12-14 到 2026-04-06 经历了 ~90 个版本，演化速度极快

---

## 2. Source Inventory

### 2.1 File Classification

| 类别 | 路径模式 | 文件数 | 角色 |
|------|----------|--------|------|
| **Manifest/Config** | `package.json`, `tsconfig.json`, `vitest.config.ts` | 5 | 项目配置、构建、测试 |
| **Installer** | `bin/install.js` | 1 | 多运行时安装器（交互 + CLI 模式） |
| **Slash Commands** | `commands/gsd/*.md` | 68 | 用户入口点，Markdown prompt 文件 |
| **Workflows** | `get-shit-done/workflows/*.md` | 68 | orchestrator 逻辑，分步骤流程定义 |
| **Agent Definitions** | `agents/*.md` | 24 | subagent 系统提示词 + frontmatter 配置 |
| **References** | `get-shit-done/references/*.md` | 35+ | agent/workflow 按需加载的知识文档 |
| **Templates** | `get-shit-done/templates/*.md` | 33+ | 生成 artifact 的模板 |
| **Contexts** | `get-shit-done/contexts/*.md` | 3 | 执行环境配置（dev/research/review） |
| **CLI Core** | `get-shit-done/bin/gsd-tools.cjs` | 1 | 43KB 主入口，命令分发器 |
| **CLI Libs** | `get-shit-done/bin/lib/*.cjs` | 21 | 按域拆分的库模块 |
| **Hooks** | `hooks/*.js`, `hooks/*.sh` | 9 | PreToolUse/PostToolUse/SessionStart 钩子 |
| **Scripts** | `scripts/*.js`, `scripts/*.sh` | 5 | 构建、测试、安全扫描 |
| **SDK** | `sdk/src/*.ts` | 45 | TypeScript headless SDK |
| **SDK Prompts** | `sdk/prompts/**/*.md` | 20+ | SDK 专用 agent/workflow 定义 |
| **Tests** | `tests/*.test.cjs`, `sdk/src/*.test.ts` | 100+ | 40k+ 行测试代码 |
| **Docs** | `docs/*.md` | 15+ | 用户指南、架构文档、特性参考 |
| **i18n** | `README.*.md`, `docs/{ja-JP,ko-KR,pt-BR,zh-CN}/` | 20+ | 多语言文档 |

### 2.2 Key Entry Points

```
User Input
  → commands/gsd/<name>.md          # 用户可见的斜杠命令
    → workflows/<name>.md           # orchestrator 流程
      → gsd-tools.cjs init <op>     # 上下文组装
      → Task(gsd-<agent>)           # subagent 派遣
        → gsd-tools.cjs <command>   # 状态变更
      → file system (.planning/)    # 持久化
```

---

## 3. Object Model

### 3.1 First-Class Entities

#### 3.1.1 Project

- **Schema**: `PROJECT.md`（Markdown）+ `config.json`（JSON）
- **Location**: `.planning/PROJECT.md`, `.planning/config.json`
- **Lifecycle**: `new-project` 创建 → 每个 milestone 更新 → 项目结束
- **Key Fields**: Core Value, Goals, Constraints, Tech Stack, Key Decisions

**Evidence**: `get-shit-done/templates/project.md:1-20`

#### 3.1.2 Milestone

- **Schema**: `ROADMAP.md` 中的 milestone section + `MILESTONES.md` 归档
- **Lifecycle**: `new-project`/`new-milestone` 创建 → phases 执行 → `complete-milestone` 归档
- **Key Fields**: version, name, phases[], requirements[], definition of done

**Evidence**: `get-shit-done/templates/milestone.md`, `get-shit-done/workflows/complete-milestone.md`

#### 3.1.3 Phase

- **Schema**: 磁盘目录 `.planning/phases/XX-name/` + ROADMAP.md 中的条目
- **Lifecycle**: discuss → research → plan → execute → verify → complete
- **Artifacts**: `{N}-CONTEXT.md`, `{N}-RESEARCH.md`, `{N}-{M}-PLAN.md`, `{N}-{M}-SUMMARY.md`, `{N}-VERIFICATION.md`, `{N}-UAT.md`
- **States**: `not_started` → `context_gathered` → `researched` → `planned` → `in_progress` → `executed` → `verified` → `complete`

**Evidence**: `get-shit-done/references/artifact-types.md:30-45`, `sdk/src/types.ts:217-223` (`PhaseType` enum: Discuss, Research, Plan, Execute, Verify)

#### 3.1.4 Plan

- **Schema**: YAML frontmatter + XML task body
- **Location**: `.planning/phases/XX-name/XX-YY-PLAN.md`
- **Lifecycle**: planner 创建 → plan-checker 验证 → executor 执行 → SUMMARY.md 产出
- **Key Fields** (frontmatter):

```typescript
// sdk/src/types.ts:50-62
interface PlanFrontmatter {
  phase: string;
  plan: string;
  type: string;
  wave: number;
  depends_on: string[];
  files_modified: string[];
  autonomous: boolean;
  requirements: string[];
  must_haves: MustHaves;
}
```

- **Task Body** (XML):

```xml
<task type="auto">
  <name>...</name>
  <files>...</files>
  <read_first>...</read_first>
  <action>...</action>
  <verify>...</verify>
  <acceptance_criteria>...</acceptance_criteria>
  <done>...</done>
</task>
```

**Evidence**: `sdk/src/types.ts:50-85`, `README.md:492-504`

#### 3.1.5 STATE.md (Project State)

- **Schema**: Markdown with YAML frontmatter
- **Location**: `.planning/STATE.md`
- **Lifecycle**: 持续更新，每个显著操作后写入
- **Sections**: Project Reference, Current Position, Performance Metrics, Accumulated Context, Session Continuity
- **Size Constraint**: < 100 lines（digest，非 archive）

**Evidence**: `get-shit-done/templates/state.md:1-177`

#### 3.1.6 Agent

- **Schema**: Markdown with YAML frontmatter (`name`, `description`, `tools`, `color`)
- **Location**: `agents/gsd-<name>.md`
- **Lifecycle**: installer 部署 → runtime 通过 `subagent_type` 自动加载 → 完成后输出 completion marker
- **Completion Protocol**: 每个 agent 有定义好的 completion markers（如 `## PLANNING COMPLETE`、`## PLAN COMPLETE`）

**Evidence**: `get-shit-done/references/agent-contracts.md:1-80`

### 3.2 Agent Registry (24 Agents)

| Agent | Role | Completion Markers | Size |
|-------|------|--------------------|------|
| `gsd-planner` | 计划创建 | `## PLANNING COMPLETE` | 46KB |
| `gsd-executor` | 计划执行 | `## PLAN COMPLETE`, `## CHECKPOINT REACHED` | 22KB |
| `gsd-verifier` | 相位验证 | `## Verification Complete` | 30KB |
| `gsd-debugger` | 问题诊断 | `## DEBUG COMPLETE`, `## ROOT CAUSE FOUND` | 43KB |
| `gsd-phase-researcher` | 相位研究 | `## RESEARCH COMPLETE` | 29KB |
| `gsd-project-researcher` | 项目研究 | `## RESEARCH COMPLETE` | 18KB |
| `gsd-plan-checker` | 计划校验 | `## VERIFICATION PASSED`, `## ISSUES FOUND` | 30KB |
| `gsd-roadmapper` | 路线图创建 | `## ROADMAP CREATED` | 18KB |
| `gsd-codebase-mapper` | 代码库分析 | (无标记，直接写文件) | 17KB |
| `gsd-doc-writer` | 文档生成 | (无标记) | 37KB |
| `gsd-doc-verifier` | 文档校验 | (无标记) | 11KB |
| `gsd-code-reviewer` | 代码审查 | (varies) | 14KB |
| `gsd-code-fixer` | 代码修复 | (varies) | 20KB |
| `gsd-ui-auditor` | UI 审计 | `## UI REVIEW COMPLETE` | 16KB |
| `gsd-ui-checker` | UI 校验 | `## ISSUES FOUND` | 10KB |
| `gsd-ui-researcher` | UI 研究 | `## UI-SPEC COMPLETE` | 13KB |
| `gsd-research-synthesizer` | 研究综合 | `## SYNTHESIS COMPLETE` | 7KB |
| `gsd-integration-checker` | 集成检查 | `## Integration Check Complete` | 13KB |
| `gsd-nyquist-auditor` | 采样审计 | `## PARTIAL`, `## ESCALATE` | 5KB |
| `gsd-security-auditor` | 安全审计 | `## OPEN_THREATS` | 4KB |
| `gsd-intel-updater` | 代码智能更新 | `## INTEL UPDATE COMPLETE` | 11KB |
| `gsd-user-profiler` | 用户画像 | (返回 JSON) | 9KB |
| `gsd-advisor-researcher` | 顾问研究 | (无标记) | 4KB |
| `gsd-assumptions-analyzer` | 假设分析 | (返回 sections) | 4KB |

### 3.3 Context Isolation Strategy

GSD 的核心设计原则是 **每个 subagent 获得独立的 200k token 上下文**。具体实现：

1. **Orchestrator 只传递路径，不传递内容** —— 告诉 agent 去读 `<files_to_read>` 列表中的文件
2. **Context budget rules** 根据 context window 大小调整读取深度：
   - `< 500k`: 仅读 frontmatter
   - `>= 500k`: 允许全文读取
3. **Anti-pattern 强制规则** (`references/universal-anti-patterns.md`): 禁止读 `agents/*.md`、禁止内联大文件到 subagent prompt
4. **Context degradation tiers**: PEAK (0-30%) → GOOD (30-50%) → DEGRADING (50-70%) → POOR (70%+)

**Evidence**: `get-shit-done/references/context-budget.md:1-49`, `get-shit-done/references/universal-anti-patterns.md:1-27`

---

## 4. State Machine & Flow

### 4.1 Phase Lifecycle State Machine

```
                    ┌──────────────────────────────────────────────┐
                    │              PHASE LIFECYCLE                 │
                    │                                              │
 /gsd-discuss-phase │  ┌─────────┐   ┌──────────┐   ┌──────────┐ │
 ─────────────────>─┤  │ DISCUSS │──>│ RESEARCH │──>│   PLAN   │ │
                    │  │(optional)│   │(optional)│   │          │ │
                    │  └─────────┘   └──────────┘   └────┬─────┘ │
                    │                                     │       │
                    │  ┌──────────┐   Research Gate       │       │
                    │  │PLAN-CHECK│<──────────────────────┘       │
                    │  │(optional)│                                │
                    │  └──┬───────┘                                │
                    │     │ max 3 revisions                       │
                    │     v                                        │
                    │  ┌──────────┐   ┌──────────┐   ┌──────────┐ │
                    │  │ EXECUTE  │──>│  VERIFY  │──>│ COMPLETE │ │
                    │  │(waves)   │   │(optional)│   │          │ │
                    │  └──────────┘   └──────────┘   └──────────┘ │
                    └──────────────────────────────────────────────┘
```

**状态转换证据** (`sdk/src/phase-runner.ts:90-310`):

```
run(phaseNumber):
  Step 1: Discuss   → if !has_context && !skip_discuss
  Step 2: Research  → if config.workflow.research
  Step 2.5: Research Gate → if has_research → checkResearchGate()
  Step 3: Plan      → always
  Step 3.5: Plan Check → if config.workflow.plan_check (max 1 re-plan + re-check)
  Step 4: Execute   → always
  Step 5: Verify    → if config.workflow.verifier
  Step 6: Advance   → if verify passed
```

### 4.2 Wave Execution Model

Plans 按 `wave` 字段分组并行执行：

```
Wave 1 (parallel):  Plan 01 ─┐    Plan 02 ─┐
                              │              │
Wave 2 (parallel):  Plan 03 <─┘    Plan 04 <─┘
                     │              │
Wave 3 (sequential): Plan 05 <────┘
```

**依赖解析规则**:
- `depends_on` 字段声明前置依赖
- `files_modified` 重叠检测 → 强制排入后续 wave
- 无依赖的 plan → 同一 wave 并行执行
- Worktree 隔离（`workflow.use_worktrees: true`）为每个并行 agent 提供独立工作目录

**Evidence**: `get-shit-done/workflows/execute-phase.md:1-100`, `README.md:346-372`

### 4.3 Milestone Lifecycle

```
/gsd-new-project
  → Questions → Research → Requirements → Roadmap → STATE.md
    → for each phase:
        /gsd-discuss-phase N
        /gsd-plan-phase N
        /gsd-execute-phase N
        /gsd-verify-work N
        /gsd-ship N
    → /gsd-complete-milestone
        → Archive ROADMAP.md + REQUIREMENTS.md
        → Tag release
    → /gsd-new-milestone
        → Fresh cycle
```

### 4.4 Quick Mode (Bypass)

`/gsd-quick` 提供一个跳过完整 phase lifecycle 的快速通道：
- 默认跳过 research、plan-check、verifier
- `--full` 启用全部阶段
- `--validate` 启用 plan-check + verification
- `--discuss` 启用轻量讨论
- `--research` 启用研究
- 输出保存在 `.planning/quick/` 目录，不影响主 phase 序列

**Evidence**: `README.md:435-462`, `get-shit-done/workflows/quick.md`

---

## 5. Enforcement Audit

### 5.1 Hard-Enforced (exit 2 / blocks execution)

| Claim | Mechanism | File | Evidence |
|-------|-----------|------|----------|
| Conventional Commits 格式 | `gsd-validate-commit.sh` PreToolUse hook，exit 2 阻断 | `hooks/gsd-validate-commit.sh:36-44` | 正则 `^(feat\|fix\|docs\|...)(\(.+\))?:[[:space:]].+`，subject <=72 chars |
| Research Gate 阻断 | `checkResearchGate()` 检测未解决的 Open Questions | `sdk/src/research-gate.ts:29-94` | 存在未解决问题时 `pass: false`，SDK `phase-runner.ts:191-204` 调用 blocker callback |
| Plan-check revision loop | max 3 iterations 后 escalate | `get-shit-done/references/gates.md:20-22` | "Bounded by iteration cap... After max iterations, escalates unconditionally" |
| Phase pre-flight checks | 检查 REQUIREMENTS.md、ROADMAP.md、PLAN.md 存在性 | `get-shit-done/references/gates.md:48-52` | "Block with missing-file message" |

**注意**: `gsd-validate-commit.sh` 和 `gsd-phase-boundary.sh` 都需要 `hooks.community: true` 才启用（opt-in），所以实际上只有在显式开启社区钩子后才是 hard-enforced。

### 5.2 Soft-Enforced (advisory warnings, does not block)

| Claim | Mechanism | File | Evidence |
|-------|-----------|------|----------|
| Workflow guard (直接编辑警告) | `gsd-workflow-guard.js` PreToolUse, `additionalContext` advisory | `hooks/gsd-workflow-guard.js:78-85` | "This is a SOFT guard -- it advises, not blocks" (line 8) |
| Prompt injection detection | `gsd-prompt-guard.js` PreToolUse, advisory only | `hooks/gsd-prompt-guard.js:80-88` | "Advisory warning -- does not block the operation" (line 80) |
| Context window monitoring | `gsd-context-monitor.js` PostToolUse, warning injection | `hooks/gsd-context-monitor.js:132-148` | WARNING (<=35%) / CRITICAL (<=25%), debounced |
| Read-before-edit guard | `gsd-read-guard.js` PreToolUse, advisory | `hooks/gsd-read-guard.js:61-68` | "Advisory guidance -- does not block the operation" |
| State file mutation guard | `references/universal-anti-patterns.md` rule 15 | `references/universal-anti-patterns.md:37` | "Always use gsd-tools.cjs CLI commands for mutations" -- prompt instruction only |
| Non-GSD agent type ban | `references/universal-anti-patterns.md` rule 10 | `references/universal-anti-patterns.md:24` | "NEVER use non-GSD agent types" -- prompt instruction only |
| Phase boundary detection | `gsd-phase-boundary.sh` PostToolUse, opt-in | `hooks/gsd-phase-boundary.sh:7-8` | "OPT-IN: no-op unless hooks.community: true" |

### 5.3 Unenforced (declared in docs but no runtime enforcement)

| Claim | Where Declared | Why Unenforced |
|-------|---------------|----------------|
| "No `git add .` or `git add -A`" | `references/universal-anti-patterns.md:44` | 仅 prompt 指令，无 hook 拦截 |
| Context budget read-depth rules | `references/context-budget.md:23-28` | 依赖 agent 自律，无运行时检测 |
| Plan file naming convention | `references/universal-anti-patterns.md:57` | 依赖 `gsd-tools` 检测，非 hook 级拦截 |
| Scope reduction detection | `CHANGELOG.md:138` (v1.31.0) | 在 plan-checker agent 的 prompt 中检查，非确定性 |
| Schema drift detection | `CHANGELOG.md:136` (v1.31.0) | 在 verifier agent prompt 中，非确定性 |
| CLAUDE.md compliance | `CHANGELOG.md:218` (v1.28.0) | plan-checker Dimension 10，prompt-based |

### 5.4 Enforcement Summary

```
                    Hard    Soft    Unenforced
Hooks:               1       4        1 (opt-in)
SDK gates:           1       -        -
Prompt rules:        -       2        6+
Agent checks:        1       -        3+
```

**核心发现**: GSD 的 enforcement 策略高度依赖 **prompt engineering**（让 LLM 遵守规则），而非 **deterministic runtime checks**（代码强制执行）。只有 Conventional Commits 验证是真正不可绕过的硬门槛（exit 2 阻断 git commit），但即使它也是 opt-in。

---

## 6. Prompt Catalog

### 6.1 Command → Workflow → Agent Prompt Chain

典型 prompt 链（以 `/gsd-execute-phase 3` 为例）：

```
1. commands/gsd/execute-phase.md (用户入口)
   ├── frontmatter: allowed-tools, argument-hint
   ├── <objective>: "Execute all plans in a phase"
   ├── <execution_context>: @workflows/execute-phase.md, @references/ui-brand.md
   └── <process>: "Execute the workflow end-to-end"

2. workflows/execute-phase.md (orchestrator 逻辑)
   ├── <purpose>: orchestrator 协调
   ├── <required_reading>: @references/agent-contracts.md, @references/context-budget.md, @references/gates.md
   ├── <available_agent_types>: 12 agent types listed
   └── <process>: 多步骤流程（parse_args → initialize → wave grouping → spawn → verify）

3. agents/gsd-executor.md (subagent prompt)
   ├── frontmatter: name, description, tools, color
   ├── <role>: "You are a GSD plan executor"
   ├── <execution_flow>: load_project_state → load_plan → execute_tasks → write_summary
   └── 内联 references: @references/thinking-models-execution.md
```

### 6.2 Key Prompt Patterns

| Pattern | 描述 | 使用位置 | 效果 |
|---------|------|---------|------|
| `<files_to_read>` | 指定 subagent 必须先读的文件列表 | 所有 agent prompts | 确保 fresh context 加载正确内容 |
| `<available_agent_types>` | 显式列出可用 agent 类型 | workflow 文件 | 防止 fallback 到 `general-purpose` |
| `gsd-tools.cjs init <workflow>` | 一次性加载所有上下文 | 每个 workflow 入口 | 减少多次 bash 调用的 token 消耗 |
| Completion markers | `## PLANNING COMPLETE` 等 | 每个 agent 输出 | orchestrator 检测 agent 完成状态 |
| `<if mode>` tags | 条件分支（yolo/interactive） | workflow 文件 | 根据配置选择不同行为路径 |
| Goal-backward verification | 从目标反推验证条件 | `gsd-verifier` | "Task completion ≠ Goal achievement" |
| `must_haves` frontmatter | truths + artifacts + key_links | PLAN.md | 提供可验证的交付物规格 |

---

## 7. Design Highlights

### 7.1 Micro-level (Component Design)

#### M1: gsd-tools.cjs 作为确定性操作层

**问题**: LLM 直接操作 Markdown 文件（STATE.md, ROADMAP.md）时容易出错——格式不一致、字段丢失、并发写冲突。

**解法**: 所有状态变更都通过 `gsd-tools.cjs` 的确定性 CLI 命令执行（如 `state advance-plan`、`roadmap update-status`、`phase complete`），而非让 LLM 用 Write/Edit 工具直接修改。

**证据**: `get-shit-done/references/universal-anti-patterns.md:37` — "No direct Write/Edit to STATE.md or ROADMAP.md for mutations."

**亮点**: 将不可靠的 LLM 文件操作替换为可靠的 Node.js 脚本，这是整个系统中最重要的工程决策。

#### M2: Revision Loop with Stall Detection

**问题**: plan-checker 和 planner 之间的 revision loop 可能无限循环或在不收敛时浪费资源。

**解法**: 上限 3 次 revision，且增加 stall detection——如果连续两次迭代 issue count 未减少，立即 escalate 到用户。

**证据**: `get-shit-done/references/gates.md:20-22` — "The loop also escalates early if issue count does not decrease between consecutive iterations (stall detection)."

#### M3: Research Gate with Conservative Fail

**问题**: RESEARCH.md 中存在未解决的 open questions 时，直接进入 planning 会导致计划基于不完整信息。

**解法**: `checkResearchGate()` 解析 `## Open Questions` section，检测未标记 RESOLVED 的条目。对于无法解析的自由文本问题，保守地 fail。

**证据**: `sdk/src/research-gate.ts:92-93` — "Section has content but no parseable question lines → fail conservatively"

#### M4: Context Window Bridge (Statusline → Context Monitor)

**问题**: statusline hook 能看到 context 使用量但 agent 看不到；context-monitor hook 需要数据但在不同事件循环中。

**解法**: statusline 将 metrics 写入 `/tmp/claude-ctx-{session_id}.json`，context-monitor 读取这个 bridge file。session_id 经过 path traversal 验证。

**证据**: `hooks/gsd-statusline.js:40-53`, `hooks/gsd-context-monitor.js:69-75`

### 7.2 Macro-level (Architecture Design)

#### A1: Four-Layer Architecture

```
Command Layer    → 用户入口，thin wrapper（~1-5KB each）
  ↓ @-reference
Workflow Layer   → orchestrator 逻辑（~5-50KB each）
  ↓ Task(subagent_type)
Agent Layer      → 专业化 agent prompt（~5-46KB each）
  ↓ Bash(gsd-tools.cjs)
CLI Tools Layer  → 确定性操作（~500KB total）
  ↓ fs.writeFileSync
File System      → .planning/ 目录持久化
```

**设计优势**:
- Command 和 Workflow 分离：command 仅声明 allowed-tools 和入口参数，所有逻辑在 workflow 中
- Agent 和 Workflow 分离：orchestrator 不做重活，保持 lean context
- CLI Tools 和 Agent 分离：状态变更的确定性保证

#### A2: Multi-Runtime Abstraction

GSD 通过 installer (`bin/install.js`) 实现同一套 prompts 部署到 12 种运行时。关键适配策略：

- **Claude Code**: `commands/gsd/*.md` + `agents/*.md` + `hooks/*.js`
- **Gemini CLI**: 替换 hook 事件名（`PreToolUse` → `BeforeTool`、`PostToolUse` → `AfterTool`）
- **Codex**: skills + TOML config
- **Copilot**: `vscode_askquestions` 替代 `AskUserQuestion`
- **Cline**: `.clinerules` 配置

**路径替换**: installer 将 `~/.claude/` 路径替换为目标运行时路径（如 `~/.gemini/`、`~/.config/opencode/`）。

#### A3: SDK as Headless Execution Engine

`@gsd-build/sdk` (`sdk/` 目录) 使用 `@anthropic-ai/claude-agent-sdk` 的 `query()` 函数直接调用 Claude API，无需 Claude Code CLI：

```typescript
// sdk/src/session-runner.ts:8
import { query } from '@anthropic-ai/claude-agent-sdk';
```

SDK 实现了完整的 `PhaseRunner` 状态机 (`discuss → research → plan → plan-check → execute → verify → advance`)，支持：
- Event stream（`GSDEventType` enum 覆盖 29 种事件）
- Human gate callbacks（blocker 时调用用户决策回调）
- 自动 retry（每步 retryOnce）
- Context engine（文件解析、上下文裁剪）

#### A4: Config-Driven Behavior Toggle

所有可选 workflow 步骤都通过 `.planning/config.json` 控制，遵循 **absent = enabled** 原则：

| Config Key | Default | Controls |
|-----------|---------|----------|
| `workflow.research` | `true` | 是否在 planning 前做 research |
| `workflow.plan_check` | `true` | 是否在 execution 前验证 plan |
| `workflow.verifier` | `true` | 是否在 execution 后验证 |
| `workflow.auto_advance` | `false` | 是否自动 chain discuss→plan→execute |
| `workflow.skip_discuss` | `false` | 是否跳过 discuss phase |
| `workflow.use_worktrees` | `true` | 是否使用 worktree 隔离 |
| `parallelization.enabled` | `true` | 是否并行执行 plans |
| `hooks.context_warnings` | `true` | 是否显示 context 用量警告 |
| `hooks.workflow_guard` | `false` | 是否警告非 GSD 直接编辑 |
| `hooks.community` | `false` | 是否启用社区钩子 |

**Evidence**: `docs/ARCHITECTURE.md:91-93` — "Absent = Enabled"

---

## 8. Cross-Cutting Analysis

### 8.1 Failure Modes (Evidence-Based)

#### F1: Subagent Completion Signal Loss

**症状**: orchestrator 无法检测 subagent 完成。
**证据**: `get-shit-done/workflows/execute-phase.md:22-23` — "If a spawned agent completes its work (commits visible, SUMMARY.md exists) but the orchestrator never receives the completion signal, treat it as successful based on spot-checks"
**缓解**: filesystem + git state 作为 fallback 完成检测。

#### F2: Context Window Exhaustion in Orchestrator

**症状**: orchestrator 积累过多 context 后质量下降。
**证据**: `get-shit-done/references/context-budget.md:43-48` — "Silent partial completion", "Increasing vagueness", "Skipped steps"
**缓解**: context degradation tiers + context-monitor hook warnings。

#### F3: Infinite Retry Loops (Non-Claude Runtimes)

**症状**: 非 Claude 模型不遵守 read-before-edit 模式，Write/Edit 被 runtime 拒绝后无限重试。
**证据**: `hooks/gsd-read-guard.js:8-15` — "Non-Claude models... attempt to Write/Edit an existing file without reading it, the runtime rejects... The model retries without reading, creating an infinite loop"
**缓解**: `gsd-read-guard.js` advisory hook。

#### F4: Plan Checker False Positives / Stall

**症状**: plan-checker 和 planner 在 revision loop 中不收敛。
**证据**: `get-shit-done/references/gates.md:22` — stall detection mechanism
**缓解**: max 3 iterations + stall detection + escalation to user。

#### F5: Parallel Worktree STATE.md Overwrites

**症状**: 多个并行 executor 同时写 STATE.md 导致数据丢失。
**证据**: `CHANGELOG.md:111` (v1.32.0) — "Parallel worktree STATE.md overwrites — Orchestrator owns STATE.md/ROADMAP.md writes"
**缓解**: Orchestrator 独占 STATE.md 写权限，使用 atomic writes。

#### F6: Windows Path Compatibility

**症状**: 多种 Windows 路径问题（8.3 短路径、反斜杠、HOME 环境变量）。
**证据**: `CHANGELOG.md:113,235-240` — 多个 Windows-specific fixes across versions
**缓解**: 逐版本修复，使用 `realpathSync.native`、forward slash normalization。

#### F7: Hook Stdin Timeout

**症状**: Hook 进程在 Windows/Git Bash 上因 stdin 管道问题 hang 住。
**证据**: `hooks/gsd-context-monitor.js:31-35` — "Timeout guard: if stdin doesn't close within 10s... exit silently instead of hanging"
**缓解**: 所有 JS hooks 都有 `stdinTimeout`（3-10 秒）。

### 8.2 Evolution Velocity

从 CHANGELOG.md 分析：

| 时期 | 版本范围 | 关键演化 |
|------|---------|---------|
| 2025-12-14 ~ 2026-01-15 | v1.0 → v1.5.18 | 核心 workflow 建立：phases, plans, execution, verification |
| 2026-01-15 ~ 2026-02-08 | v1.5.18 → v1.17.0 | Agent 系统成熟：planner, executor, verifier, debugger agents 独立化 + gsd-tools CLI |
| 2026-02-08 ~ 2026-03-20 | v1.17.0 → v1.27.0 | Multi-runtime 扩展：Codex, Copilot, Gemini, Cursor + security hardening |
| 2026-03-20 ~ 2026-04-06 | v1.27.0 → v1.34.2 | 企业级能力：workstreams, SDK, workspace, codebase intelligence, 12 runtimes |

**速度**: ~90 版本 / 4 个月 = ~22 版本/月，极其高频的迭代速度。

### 8.3 Test Coverage

- **Core CJS tests**: `tests/*.test.cjs` — 40,380 行，使用 `node:test` + `node:assert/strict`
- **SDK tests**: `sdk/src/*.test.ts` — Vitest，unit + integration 分离
- **Coverage requirement**: `c8 --check-coverage --lines 70` (70% line coverage)
- **CI matrix**: Ubuntu + macOS, Node 22 + 24
- **Security scans**: `scripts/prompt-injection-scan.sh`, `scripts/base64-scan.sh`, `scripts/secret-scan.sh`

---

## 9. Gates Taxonomy

GSD 定义了四种 canonical gate types（`get-shit-done/references/gates.md`）：

| Gate Type | Purpose | Behavior | Example |
|-----------|---------|----------|---------|
| **Pre-flight** | 验证前置条件 | 不满足则阻断，无部分工作产出 | plan-phase 检查 REQUIREMENTS.md 存在性 |
| **Revision** | 评估输出质量 | 循环回到生产者修改，有迭代上限 | plan-checker 审查 PLAN.md（max 3） |
| **Escalation** | 无法自动解决的问题 | 暂停 workflow，呈现选项给用户 | revision loop 耗尽后 |
| **Abort** | 防止损害或浪费 | 立即停止，保存状态 | context window 严重不足 |

**Gate Matrix** (`gates.md:48-58`):

| Workflow | Phase | Gate Type | Failure |
|----------|-------|-----------|---------|
| plan-phase | Entry | Pre-flight | Block |
| plan-phase | Step 12 | Revision | Loop (max 3) |
| plan-phase | Post-revision | Escalation | Surface to dev |
| execute-phase | Entry | Pre-flight | Block |
| execute-phase | Completion | Revision | Re-run tasks |
| verify-work | Entry | Pre-flight | Block |
| verify-work | Evaluation | Escalation | Surface gaps |
| next | Entry | Abort | Stop with diagnostic |

---

## 10. Migration Assessment

### 10.1 Migration Candidates

| 编号 | 机制 | 适配难度 | 移植价值 | 目标插件 | 说明 |
|------|------|---------|---------|---------|------|
| **MC-1** | Gates taxonomy (4 types) | Low | High | `quality/testing` or new `workflow/gates` | 通用的验证门控模型，可用于任何 workflow |
| **MC-2** | Context budget rules + degradation tiers | Low | High | `workflows/complex-task` | 可嵌入 references，指导 agent 按 context 用量调整行为 |
| **MC-3** | Agent completion markers + contracts | Low | Medium | `authoring/skill-dev` | 标准化 agent 完成协议，避免 orchestrator 检测失败 |
| **MC-4** | gsd-tools 确定性操作模式 | Medium | High | `workflows/complex-task` | 将状态变更从 LLM Write/Edit 迁移到确定性脚本 |
| **MC-5** | Wave execution model | High | High | `workflows/complex-task` | 依赖图 + 并行 wave 分组 + worktree 隔离 |
| **MC-6** | Research gate (open questions check) | Low | Medium | `workflows/deep-plan` | 阻止带未解决问题进入 planning |
| **MC-7** | Revision loop + stall detection | Medium | High | `quality/testing`, `quality/refactor` | 通用的 produce → check → revise bounded loop |
| **MC-8** | Context monitor hook pattern | Medium | Medium | `integrations/utils` | 跨运行时的 context 用量警告 |
| **MC-9** | Thin orchestrator pattern | Low | High | (design principle) | 所有 workflow 的架构原则 |
| **MC-10** | must_haves verification schema | Medium | High | `quality/testing` | 结构化的可验证交付物规格 |

### 10.2 Recommended Adoption Order

1. **MC-9** (Thin orchestrator) — 设计原则，零开发成本
2. **MC-1** (Gates taxonomy) — 创建 reference doc 即可
3. **MC-2** (Context budget rules) — 创建 reference doc
4. **MC-3** (Agent completion markers) — 添加到 skill-dev 指南
5. **MC-7** (Revision loop) — 在 testing/refactor workflow 中实现
6. **MC-6** (Research gate) — 在 deep-plan 中实现
7. **MC-10** (must_haves schema) — 在 testing skill 中实现
8. **MC-4** (确定性操作) — 需要为 1st-cc-plugin 开发类似 gsd-tools 的脚本
9. **MC-5** (Wave execution) — 最复杂，依赖 Task API + worktree
10. **MC-8** (Context monitor) — 需要 hook 开发

### 10.3 Anti-Patterns to Avoid

从 GSD 的演化历史中提取的教训：

1. **不要依赖 `general-purpose` subagent** —— 必须使用专用 agent type（v1.5.7 教训）
2. **不要让 agent 直接写状态文件** —— 所有变更走确定性脚本（v1.12.0 教训）
3. **不要用 heredoc 传递大 payload** —— Windows 兼容性差，用 temp file（v1.22.4 教训）
4. **不要假设 hook stdin 会及时关闭** —— 必须有 timeout guard（v1.22.2 教训）
5. **不要在 agent prompt 中内联文件内容** —— 传路径让 agent 自己读（v1.15.0 教训）

---

## 11. Quality Gate Checklist

| Gate | Status | Evidence |
|------|--------|---------|
| A. Source Inventory classified | PASS | Section 2 — 17 categories |
| B. Prompt traceability with repo_path + quote | PASS | Section 6 — command→workflow→agent chain with file paths |
| C. At least 3 first-class entities with lifecycle | PASS | Section 3 — 6 entities (Project, Milestone, Phase, Plan, STATE.md, Agent) |
| D. State machine with phases and transitions | PASS | Section 4 — Phase lifecycle + SDK PhaseRunner code |
| E. Enforcement audit with Hard/Soft/Unenforced | PASS | Section 5 — 4 hard, 7 soft, 6+ unenforced |
| F. Both micro and macro design highlights | PASS | Section 7 — 4 micro (M1-M4) + 4 macro (A1-A4) |
| G. At least 3 failure modes with evidence | PASS | Section 8.1 — 7 failure modes (F1-F7) |
| H. Migration candidates with ratings and order | PASS | Section 10 — 10 candidates with adoption order |
