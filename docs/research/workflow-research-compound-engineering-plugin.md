# Workflow Research: compound-engineering-plugin

> 研究对象：`vendor/compound-engineering-plugin`
> 研究日期：2026-04-08
> 仓库来源：`https://github.com/EveryInc/compound-engineering-plugin`
> 版本：v2.63.0（`package.json`、`plugin.json` 均一致）

---

## §1 Framework Profile

| 维度 | 描述 |
|------|------|
| **名称** | Compound Engineering Plugin |
| **作者** | Kieran Klaassen / Every Inc |
| **许可证** | MIT |
| **核心理念** | "Each unit of engineering work should make subsequent units easier—not harder." 80% 规划与回顾，20% 执行 |
| **工作流主线** | `Ideate → Brainstorm → Plan → Work → Review → Compound → Repeat` |
| **规模** | 450 文件，50+ agents，40+ skills，跨 10+ 目标平台转换器 |
| **技术栈** | Bun/TypeScript CLI（转换器/安装器），插件本身为纯 Markdown + JSON |
| **独立功能** | 除插件外，还包含跨平台 CLI（Claude Code → Codex/Gemini/Copilot/Windsurf/Kiro/OpenClaw/Qwen/Droid/Pi/OpenCode 格式转换） |

**引用**：`README.md` L10-18, `package.json` L1-5, `plugins/compound-engineering/README.md` L1-7

---

## §2 Source Inventory

### 插件核心（`plugins/compound-engineering/`）

| 类别 | 数量 | 位置 |
|------|------|------|
| 核心工作流 Skill | 7 | `skills/ce-brainstorm/`, `ce-plan/`, `ce-work/`, `ce-review/`, `ce-compound/`, `ce-compound-refresh/`, `ce-ideate/` |
| Git Workflow Skill | 4 | `skills/git-commit/`, `git-commit-push-pr/`, `git-worktree/`, `git-clean-gone-branches/` |
| 工具类 Skill | ~30 | `skills/` 下其余目录（`agent-browser/`, `document-review/`, `todo-*` 等） |
| Beta Skill | 2 | `skills/lfg/`, `skills/slfg/`（自治工作流），`skills/ce-work-beta/` |
| Review Agent | 28 | `agents/review/` |
| Document Review Agent | 7 | `agents/document-review/` |
| Research Agent | 7 | `agents/research/` |
| Design Agent | 3 | `agents/design/` |
| Workflow Agent | 4 | `agents/workflow/` |
| Docs Agent | 1 | `agents/docs/` |

### CLI（`src/`）

| 目录 | 用途 |
|------|------|
| `src/commands/` | CLI 命令入口 |
| `src/converters/` | Claude → 各平台格式转换器 |
| `src/targets/` | 各目标平台写入器 |
| `src/parsers/` | 插件解析 |
| `src/sync/` | 个人配置同步 |
| `src/release/` | 发布自动化 |
| `src/types/` | TypeScript 类型 |
| `tests/` | 45+ 测试文件 |

### 附属插件

| 插件 | 位置 |
|------|------|
| `coding-tutor` | `plugins/coding-tutor/`（3 commands + 1 skill） |

**引用**：`AGENTS.md` L6-8, `plugins/compound-engineering/README.md` 完整组件表

---

## §3 Object Model

### Entity 1: Skill（技能单元）

每个 Skill 是一个自包含目录，核心文件为 `SKILL.md`，辅以 `references/`、`scripts/`、`assets/`。

**结构**：
```
skills/<name>/
├── SKILL.md          # YAML frontmatter + 指令正文
├── references/       # 按需加载的参考文档
├── scripts/          # 可执行脚本
└── assets/           # 模板等
```

**YAML frontmatter 必须字段**：
- `name:` — 匹配目录名（kebab-case）
- `description:` — 描述功能和触发条件

**可选字段**：
- `argument-hint:` — 参数提示
- `disable-model-invocation: true` — 禁止自动触发（Beta skill 专用）

**关键约束**：
- 引用文件必须使用反引号路径（`` `references/xxx.md` ``），不能用 Markdown 链接
- 小型结构性文件（< 150 行）可用 `@./references/xxx.json` 内联
- 脚本文件总是用反引号路径 + bash 代码块引用
- 每个 skill 目录完全自包含，禁止跨目录引用

**引用**：`plugins/compound-engineering/AGENTS.md` L73-98（Skill Compliance Checklist）

### Entity 2: Agent（子代理）

Agent 是 Markdown 文件，以 YAML frontmatter 定义身份，正文定义行为。

**结构**：
```yaml
---
name: adversarial-reviewer
description: ...
model: inherit
tools: Read, Grep, Glob, Bash
color: red
---
```

**分类体系**（5 类）：
- `agents/review/` — 代码审查 persona（28 个）
- `agents/document-review/` — 文档审查 persona（7 个）
- `agents/research/` — 研究分析（7 个）
- `agents/design/` — 设计与 UI（3 个）
- `agents/workflow/` — 工作流辅助（4 个）

**命名空间**：skill 引用 agent 时必须使用完全限定名 `compound-engineering:<category>:<agent-name>`。

**引用**：`AGENTS.md` L112-119, `agents/review/adversarial-reviewer.md` L1-8

### Entity 3: Finding（审查发现）

Review 和 Document Review 的核心数据对象，由 JSON Schema 严格定义。

**必须字段**（来自 `references/findings-schema.json`）：

| 字段 | 类型 | 语义 |
|------|------|------|
| `title` | string (≤100) | 短标题，10 词以内 |
| `severity` | enum `P0-P3` | 严重级别 |
| `file` | string | 仓库相对路径 |
| `line` | integer | 行号 |
| `why_it_matters` | string | 影响描述 |
| `autofix_class` | enum | `safe_auto` / `gated_auto` / `manual` / `advisory` |
| `owner` | enum | `review-fixer` / `downstream-resolver` / `human` / `release` |
| `requires_verification` | boolean | 是否需要后续验证 |
| `confidence` | number [0,1] | 置信度 |
| `evidence` | string[] (min 1) | 代码证据 |
| `pre_existing` | boolean | 是否为预存问题 |

**引用**：`skills/ce-review/references/findings-schema.json` 完整内容

### Entity 4: Plan（计划文档）

Plan 是结构化 Markdown 文件，位于 `docs/plans/`，带 YAML frontmatter。

**frontmatter 字段**：
```yaml
title: [Plan Title]
type: feat|fix|refactor
status: active|completed
date: YYYY-MM-DD
origin: docs/brainstorms/YYYY-MM-DD-<topic>-requirements.md
deepened: YYYY-MM-DD  # optional
```

**核心结构**：Overview → Problem Frame → Requirements Trace → Scope Boundaries → Context & Research → Key Technical Decisions → Open Questions → Implementation Units → System-Wide Impact → Risks & Dependencies

**Implementation Unit 结构**：Goal, Requirements, Dependencies, Files, Approach, Execution note, Patterns to follow, Test scenarios, Verification

**引用**：`skills/ce-plan/SKILL.md` L431-554（Core Plan Template）

### Entity 5: Requirements Document（需求文档）

`ce:brainstorm` 的输出，位于 `docs/brainstorms/`，文件名 `*-requirements.md`。是 Plan 的上游输入。

**引用**：`skills/ce-brainstorm/SKILL.md` L13, L54-56

### Entity 6: Solution Document（解决方案文档）

`ce:compound` 的输出，位于 `docs/solutions/<category>/`，带 YAML frontmatter，按问题类型分 bug track 和 knowledge track。

**分类目录**：`build-errors/`, `test-failures/`, `runtime-errors/`, `performance-issues/`, `database-issues/`, `security-issues/`, `ui-bugs/`, `integration-issues/`, `logic-errors/`

**引用**：`skills/ce-compound/SKILL.md` L346-356

---

## §4 State Machine

### 主工作流状态机

```
           ┌─────────┐
           │ ce:ideate│ (optional)
           └────┬────┘
                │ ranked ideation artifact
                v
         ┌──────────────┐
         │ ce:brainstorm │
         └──────┬───────┘
                │ *-requirements.md
                v
         ┌──────────┐
         │ ce:plan  │◄──── deepening loop (Phase 5.3)
         └────┬─────┘
              │ *-plan.md (status: active)
              v
         ┌──────────┐
         │ ce:work  │◄──── task execution loop (Phase 2)
         └────┬─────┘
              │ code changes + commits
              v
         ┌───────────┐
         │ ce:review  │◄──── fix/re-review loop (max 2 rounds)
         └────┬──────┘
              │ findings resolved / PR ready
              v
         ┌─────────────┐
         │ ce:compound  │
         └──────┬──────┘
                │ docs/solutions/<category>/*.md
                v
           [Next cycle]
```

### ce:brainstorm 内部阶段

```
Phase 0: Resume / Assess / Route
  ├─ 0.1  Resume existing work
  ├─ 0.1b Classify task domain (software / non-software / neither)
  ├─ 0.2  Assess if brainstorm needed
  └─ 0.3  Assess scope (Lightweight / Standard / Deep)
Phase 1: Understand
  ├─ 1.1  Context scan (repo + optional Slack)
  ├─ 1.2  Product pressure test
  └─ 1.3  Collaborative dialogue
Phase 2: Explore approaches (2-3 options)
Phase 3: Capture requirements document
Phase 3.5: Document review (automatic)
Phase 4: Handoff
```

**引用**：`skills/ce-brainstorm/SKILL.md` L48-198

### ce:plan 内部阶段

```
Phase 0: Resume / Source / Scope
  ├─ 0.1   Resume existing plan / Deepen fast path
  ├─ 0.1b  Classify domain
  ├─ 0.2-3 Find upstream requirements
  ├─ 0.4   No-requirements fallback (bootstrap)
  ├─ 0.5   Classify outstanding questions
  └─ 0.6   Assess depth
Phase 1: Gather context
  ├─ 1.1   Local research (parallel agents)
  ├─ 1.1b  Detect execution posture
  ├─ 1.2   Decide on external research
  ├─ 1.3   External research (conditional)
  ├─ 1.4   Consolidate
  ├─ 1.4b  Reclassify depth
  └─ 1.5   Flow/edge-case analysis (conditional)
Phase 2: Resolve planning questions
Phase 3: Structure the plan
Phase 4: Write the plan
Phase 5: Final review + Confidence check + Deepening + Handoff
```

**引用**：`skills/ce-plan/SKILL.md` L57-701

### ce:review 内部阶段

```
Stage 1: Determine scope (diff range)
Stage 2: Intent discovery
Stage 2b: Plan discovery (requirements verification)
Stage 3: Select reviewers (always-on + conditional)
Stage 3b: Discover project standards paths
Stage 4: Spawn sub-agents (parallel, mid-tier model)
Stage 5: Merge findings (validate → gate → dedup → route)
Stage 6: Synthesize and present
After: Fix → Re-review (max 2 rounds) → Artifacts → Handoff
```

**4 种模式**：Interactive（默认）、Autofix（无交互）、Report-only（只读）、Headless（程序化）

**引用**：`skills/ce-review/SKILL.md` L36-72, L162-656

### ce:work 内部阶段

```
Phase 0: Input triage (plan doc / bare prompt → complexity routing)
Phase 1: Quick start (read plan, setup env, create todo, choose strategy)
Phase 2: Execute (task loop, incremental commits, test continuously)
Phase 3: Quality check (tests, lint, review, validation plan)
Phase 4: Ship (screenshots, PR, update plan status)
```

**执行策略**：Inline / Serial subagents / Parallel subagents / Swarm Mode（Agent Teams，实验性）

**引用**：`skills/ce-work/SKILL.md` L19-476

### LFG 自治管线

```
Step 1: (optional) ralph-loop
Step 2: /ce:plan → GATE: plan file exists?
Step 3: /ce:work → GATE: code changes made?
Step 4: /ce:review mode:autofix plan:<path>
Step 5: /todo-resolve
Step 6: /test-browser
Step 7: /feature-video
Step 8: Output DONE promise
```

**引用**：`skills/lfg/SKILL.md` L1-33

---

## §5 Enforcement Audit

### Hard Enforcement（运行时阻断）

| 机制 | 位置 | 行为 |
|------|------|------|
| **LFG GATE checks** | `skills/lfg/SKILL.md` L14-19 | Plan 文件不存在则重新运行 `ce:plan`；无代码变更则不进入 review |
| **Confidence gate 0.60** | `skills/ce-review/SKILL.md` Stage 5 step 2; `findings-schema.json` `_meta.confidence_thresholds` | 低于 0.60 的 finding 被抑制（P0 例外至 0.50） |
| **Finding JSON Schema** | `references/findings-schema.json` | 必须字段缺失的 finding 被丢弃 |
| **Headless mode requires diff scope** | `skills/ce-review/SKILL.md` L63 | 无法确定 diff scope 时 emit 错误并停止 |
| **Conflicting mode flags** | `skills/ce-review/SKILL.md` L33 | 多个 mode token 时阻断审查 |
| **Report-only/Headless 禁止切换 checkout** | `skills/ce-review/SKILL.md` L56-68 | 直接停止并报错 |
| **Phase 0.5 blocking questions** | `skills/ce-plan/SKILL.md` L140-149 | 真正的产品 blocker 未解决时不继续规划 |

### Soft Enforcement（指令/约定）

| 机制 | 位置 | 行为 |
|------|------|------|
| **Review 必须执行** | `skills/ce-work/SKILL.md` L287-298 | "Every change gets reviewed" — Tier 1 需明确满足 4 条件 |
| **Repo-relative paths only** | `skills/ce-plan/SKILL.md` L29, L596 | 用指令禁止绝对路径 |
| **Protected artifacts** | `skills/ce-review/SKILL.md` L153-159 | 禁止删除 `docs/brainstorms/`, `docs/plans/`, `docs/solutions/` |
| **Agent 命名空间** | `AGENTS.md` L112-119 | 必须用完全限定名 `compound-engineering:<category>:<agent-name>` |
| **Skill 自包含** | `AGENTS.md` L122-138 | 禁止跨 skill 目录引用，解释了 3 个原因 |
| **Sub-agent permission mode** | `AGENTS.md` L148-149 | 禁止传 `mode: "auto"`，让用户配置生效 |
| **Conservative routing** | `skills/ce-review/SKILL.md` L97-99 | 分歧时保守路由，只能收紧不能放宽 |
| **Severity scale** | `skills/ce-review/SKILL.md` L76-83 | P0-P3 四级定义 |
| **Test scenario completeness** | `skills/ce-work/SKILL.md` L179-187 | 补充 plan 中缺失的测试类别 |
| **Incremental commit heuristic** | `skills/ce-work/SKILL.md` L203-231 | "能写出完整 commit message 就 commit" |
| **Cross-platform tool naming** | `AGENTS.md` L106-108, L133-141 | 按能力类描述工具，提供平台提示 |

### Unenforced（声明但无检查）

| 声明 | 位置 | 差距 |
|------|------|------|
| **Beta skill `-beta` suffix 约定** | `AGENTS.md` L176-180 | 仅文档说明，无自动检测同步状态 |
| **Plan depth classification** | `skills/ce-plan/SKILL.md` L153-159 | 模型自行判断 Lightweight/Standard/Deep，无校验 |
| **Token budget (5k for SKILL.md)** | `AGENTS.md` L88（通过 `@` inline 约 150 行限制暗示） | 无自动化 token 计数 |
| **Post-Deploy Monitoring section** | `skills/ce-work/SKILL.md` L309-318 | 标注 REQUIRED 但无 gate 检查 |
| **Operational validation plan** | `skills/ce-work/SKILL.md` L309 | 同上 |

**引用**：各文件路径见表内标注

---

## §6 Prompt Catalog

### Catalog 1: ce:brainstorm — Product Pressure Test

**位置**：`skills/ce-brainstorm/SKILL.md` L119-140

> Is this the right problem, or a proxy for a more important one? What user or business outcome actually matters here? What happens if we do nothing? ... Given the current project state, user goal, and constraints, what is the single highest-leverage move right now: the request as framed, a reframing, one adjacent addition, a simplification, or doing nothing?

**分析**：这段 prompt 实现了"在执行前挑战需求"的设计哲学。按 scope 分 3 层深度，避免过度审查小任务。

### Catalog 2: ce:review — Adversarial Reviewer Identity

**位置**：`agents/review/adversarial-reviewer.md` L12-13

> You are a chaos engineer who reads code by trying to break it. Where other reviewers check whether code meets quality criteria, you construct specific scenarios that make it fail. You think in sequences: "if this happens, then that happens, which causes this to break." You don't evaluate -- you attack.

**分析**：极具特色的 persona 设计 — 不是检查清单式审查，而是主动构造攻击场景。配合 4 种猎捕技术（Assumption violation, Composition failures, Cascade construction, Abuse cases）和 3 级深度校准。

### Catalog 3: ce:plan — Execution Posture Detection

**位置**：`skills/ce-plan/SKILL.md` L186-199

> Look for signals such as: The user explicitly asks for TDD, test-first, or characterization-first work; The origin document calls for test-first implementation; Local research shows the target area is legacy, weakly tested, or historically fragile... When the signal is clear, carry it forward silently in the relevant implementation units.

**分析**：Plan 不强制 TDD，而是检测信号并轻量传递。这避免了过度 ceremony 同时保留了测试先行的能力。

### Catalog 4: ce:work — System-Wide Test Check

**位置**：`skills/ce-work/SKILL.md` L189-198

> What fires when this runs? Callbacks, middleware, observers, event handlers — trace two levels out from your change. ... Do my tests exercise the real chain? If every dependency is mocked, the test proves your logic works *in isolation* — it says nothing about the interaction.

**分析**：5 问质量关卡，强制开发者考虑集成影响。表格式设计便于快速评估。

### Catalog 5: ce:compound — Discoverability Check

**位置**：`skills/ce-compound/SKILL.md` L223-253

> After the learning is written and the refresh decision is made, check whether the project's instruction files would lead an agent to discover and search `docs/solutions/` before starting work in a documented area. This runs every time — the knowledge store only compounds value when agents can find it.

**分析**：这是"复利"哲学的具体实现 — 不仅写文档，还确保文档能被后续 agent 发现。包含"semantic assessment, not string match"的指导。

### Catalog 6: ce:review — Model Tiering

**位置**：`skills/ce-review/SKILL.md` L380-387

> Persona sub-agents do focused, scoped work and should use a fast mid-tier model to reduce cost and latency without sacrificing review quality. The orchestrator itself stays on the default (most capable) model. Use the platform's mid-tier model for all persona and CE sub-agents. In Claude Code, pass `model: "sonnet"` in the Agent tool call.

**分析**：显式的成本优化策略 — 编排器用强模型，执行者用快模型。

### Catalog 7: LFG — Gate 强制

**位置**：`skills/lfg/SKILL.md` L8-9

> CRITICAL: You MUST execute every step below IN ORDER. Do NOT skip any required step. Do NOT jump ahead to coding or implementation. The plan phase (step 2) MUST be completed and verified BEFORE any work begins. Violating this order produces bad output.

**分析**：最强硬的指令约束 — 全大写 CRITICAL + MUST + Do NOT，配合 GATE 检查实现阶段间硬阻断。

---

## §7 Micro Design Highlights

### 7.1 Progressive Disclosure（渐进式加载）

Skill 通过反引号路径实现按需加载，避免一次性加载全部 references。典型例子：

- `ce-plan` Phase 5.3.3-5.3.7 外链到 `references/deepening-workflow.md`
- `ce-review` Stage 6 后半部分外链到 `references/plan-handoff.md`
- `ce-ideate` Phase 2 后半部分外链到 `references/post-ideation-workflow.md`

**引用**：`skills/ce-plan/SKILL.md` L696, `skills/ce-review/SKILL.md` L700, `AGENTS.md` L84-98

### 7.2 Scope-Aware Ceremony（按规模调节流程）

每个核心 skill 都实现了按任务规模分层的机制：

| Skill | 分层维度 | 层级 |
|-------|---------|------|
| `ce:brainstorm` | 工作规模 | Lightweight / Standard / Deep |
| `ce:plan` | 计划深度 | Lightweight / Standard / Deep |
| `ce:review` | Reviewer 选择 | Always-on(6) + Conditional(按 diff 内容) |
| `ce:work` | 执行策略 | Trivial / Small-Medium / Large |
| `ce:compound` | 模式 | Full / Compact-safe |

**引用**：各 SKILL.md 的 Phase 0 / scope assessment 部分

### 7.3 Overlap Dedup 机制

`ce:compound` 创建新文档前，Related Docs Finder 按 5 维度评估与现有文档的重叠度（problem statement, root cause, solution approach, referenced files, prevention rules），高重叠时更新现有文档而非创建重复。

**引用**：`skills/ce-compound/SKILL.md` L117-121, L152-163

### 7.4 Cross-Platform Abstraction

所有 skill 使用能力类描述工具，而非平台特定名称：
- "Use the platform's blocking question tool (`AskUserQuestion` in Claude Code, `request_user_input` in Codex, `ask_user` in Gemini)"
- "Use the native file-search/glob tool (e.g., Glob in Claude Code)"

**引用**：`AGENTS.md` L106-108, `skills/ce-brainstorm/SKILL.md` L33

---

## §8 Macro Design Highlights

### 8.1 Knowledge Compounding Loop

框架的核心差异化在于 `ce:compound` 和 `docs/solutions/` 构成的知识复利系统：
1. `ce:compound` 在问题解决后自动触发（"that worked", "it's fixed"）
2. 文档按类别存储，带 YAML frontmatter 便于搜索
3. `ce:plan` Phase 1.1 自动调用 `learnings-researcher` 搜索 `docs/solutions/`
4. `ce:review` 的 always-on agent 包含 `learnings-researcher`
5. `ce:compound` 的 Discoverability Check 确保项目指令文件引导 agent 发现知识库
6. `ce:compound-refresh` 维护知识库时效性

**形成闭环**：解决问题 → 记录知识 → 规划/审查时搜索知识 → 更快解决下一个问题

**引用**：`skills/ce-compound/SKILL.md` L414-429, `skills/ce-plan/SKILL.md` L171-173

### 8.2 Multi-Agent Review Pipeline

`ce:review` 实现了一个完整的多代理审查管线：
1. **Scope detection** — 支持 PR/branch/standalone 3 种入口，fork-safe remote resolution
2. **Reviewer selection** — 6 always-on + 最多 11 conditional = 最多 17 reviewer
3. **Model tiering** — orchestrator 用 capable model，reviewer 用 mid-tier model
4. **Structured output** — JSON schema 强制格式
5. **Merge pipeline** — fingerprint dedup, cross-reviewer agreement boost (+0.10), confidence gate
6. **Action routing** — `safe_auto` → `gated_auto` → `manual` → `advisory` 四级路由
7. **Fix loop** — bounded 2 rounds max
8. **4 modes** — Interactive / Autofix / Report-only / Headless 适配不同调用场景

**引用**：`skills/ce-review/SKILL.md` 完整内容

### 8.3 Cross-Platform CLI Converter

独特的工程成果 — 一套 CLI 将 Claude Code 插件格式转换为 10+ 目标平台格式：

| 目标 | 输出路径 |
|------|---------|
| OpenCode | `~/.config/opencode/` |
| Codex | `~/.codex/prompts` + `~/.codex/skills` |
| Droid | `~/.factory/` |
| Pi | `~/.pi/agent/` |
| Gemini | `.gemini/` |
| Copilot | `.github/` |
| Kiro | `.kiro/` |
| Windsurf | `~/.codeium/windsurf/` |
| OpenClaw | `~/.openclaw/extensions/` |
| Qwen | `~/.qwen/extensions/` |

每个 target 有独立的 converter + writer，并附带完整测试套件。

**引用**：`README.md` L66-126, `AGENTS.md` L86-109

### 8.4 Document-as-State 模式

框架使用文件系统作为状态存储：
- `docs/brainstorms/*-requirements.md` — 需求状态
- `docs/plans/*-plan.md` — 计划状态（YAML frontmatter `status: active/completed`，checkbox 进度）
- `docs/solutions/<category>/*.md` — 知识状态
- `docs/ideation/*.md` — 创意状态
- `.context/compound-engineering/<workflow>/` — 临时运行态

**引用**：`AGENTS.md` L28, `skills/ce-plan/SKILL.md` L431-438

---

## §9 Failure Modes

### 9.1 Context Window Exhaustion

**风险**：`ce:review` 最多 spawn 17 个 reviewer + 4 个 CE agent，每个收到完整 diff + persona + schema + 模板。大型 PR 的 diff 加上所有 sub-agent 返回的 JSON，极易耗尽 context window。

**缓解**：使用 mid-tier model 降低成本，但未见明确的 diff 大小上限或分块机制。Compact-safe mode（`ce:compound`）是对此的应急设计。

**引用**：`skills/ce-review/SKILL.md` L104-150

### 9.2 Soft Gate 绕过

**风险**：LFG 的 GATE check 依赖模型遵守 "CRITICAL/MUST/Do NOT" 指令，但无程序化 enforcement。模型在压力下（长 context、多轮交互）可能跳过 gate。同样，`ce:work` 的 "REQUIRED" review 步骤和 post-deploy monitoring section 均为 soft enforcement。

**证据**：`skills/lfg/SKILL.md` L8-9 使用全大写但本质是自然语言约束

### 9.3 Knowledge Store Drift

**风险**：`docs/solutions/` 中的文档可能逐渐过时。虽然 `ce:compound-refresh` 设计用于维护时效性，但其触发依赖 `ce:compound` 的 selective judgment（6 条规则），非自动全量检查。如果一段时间没有运行 `ce:compound`，过时文档会悄然累积。

**缓解**：`ce:compound-refresh` 存在但触发条件保守。无定期全量检查机制。

**引用**：`skills/ce-compound/SKILL.md` L177-219

### 9.4 Cross-Platform Conversion Fidelity

**风险**：10+ 目标平台格式持续演变，转换器需要持续跟进。`README.md` 标注 "All provider targets are experimental and may change"。平台特有特性（如 Codex sandbox、Gemini TOML 格式）在转换时可能丢失语义。

**引用**：`README.md` L124

### 9.5 Plan-Reality Gap

**风险**：`ce:plan` 的 Implementation Units 包含详细的 test scenarios 和 verification 标准，但 `ce:work` 执行时可能发现实际代码结构与 plan 不符。虽然 Phase 2 的 execution loop 允许发现和调整，但 plan 的 checkbox 状态可能与实际完成情况不同步。

**缓解**：`ce:work` Phase 1 要求 "read plan and clarify"，Phase 3 Final Validation 要求检查 Requirements Trace。

**引用**：`skills/ce-work/SKILL.md` L47-59, L299-308

---

## §10 Migration Assessment

### 10.1 高价值移植候选

| 来源 | 目标插件组 | 价值评估 |
|------|----------|---------|
| **ce:review 的 Finding schema + merge pipeline** | `quality/` | ★★★★★ — 结构化 JSON finding + confidence gate + dedup + action routing 是成熟的审查数据模型，可提取为独立 schema |
| **Adversarial reviewer persona** | `quality/` | ★★★★☆ — 独特的"攻击式"审查视角，4 种猎捕技术可迁移为 review 框架的一个维度 |
| **Knowledge compounding 闭环** | `quality/` 或 `workflows/` | ★★★★☆ — `docs/solutions/` + discoverability check + refresh 机制是可复用的知识管理模式 |
| **Progressive disclosure 模式** | 全局规范 | ★★★★☆ — 反引号路径按需加载 vs `@` 内联的分层策略值得借鉴 |
| **Scope-aware ceremony** | `workflows/` | ★★★☆☆ — Lightweight/Standard/Deep 三层调节可融入现有 workflow skill |
| **Cross-platform tool naming** | 全局规范 | ★★★☆☆ — 按能力类描述工具 + 平台提示的模式适合多平台插件 |
| **Model tiering** | 全局规范 | ★★★☆☆ — 编排器用强模型 + 执行者用快模型的成本优化策略 |

### 10.2 不建议移植

| 内容 | 原因 |
|------|------|
| CLI converter 体系 | 独立工程项目，与 `1st-cc-plugin` 无关 |
| 个人风格 reviewer（dhh-rails, kieran-*） | 高度绑定特定技术栈和个人偏好 |
| Figma/agent-browser 集成 | 特定产品依赖 |
| coding-tutor 插件 | 不同领域 |

### 10.3 移植风险

1. **Token budget**：`ce:review` 的 SKILL.md 极长（680+ 行 + 5 个 `@` inline reference），直接移植可能超出 5k token 限制。需拆分为 coordinator + references 架构。
2. **Agent 数量**：50+ agent 的规模在 `1st-cc-plugin` 中无先例。需评估 plugin.json 注册和市场展示的影响。
3. **`docs/` 约定差异**：Compound Engineering 使用 `docs/brainstorms/`, `docs/plans/`, `docs/solutions/`, `docs/ideation/`；`1st-cc-plugin` 和 MyPluginRepo 使用 `docs/design/`, `docs/research/`, `docs/implementation/` 等。移植时需适配目录结构。

### 10.4 推荐移植路径

1. **先提取 Finding schema**（`findings-schema.json`）为 `quality/` 组的共享 schema
2. **移植 adversarial-reviewer** persona 设计到现有 `quality/codex-review` 或新建 review 框架
3. **抽象 knowledge compounding 模式**为 `workflows/` 组的独立 skill
4. **将 progressive disclosure 和 scope-aware ceremony 纳入** `authoring/skill-dev` 的最佳实践指南
