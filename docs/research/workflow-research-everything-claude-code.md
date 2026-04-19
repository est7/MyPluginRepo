# Workflow Research: Everything Claude Code (ECC)

> Reverse-engineering research report for `vendor/everything-claude-code`
> 研究日期: 2026-04-08
> 仓库版本: v1.10.0
> 仓库规模: **Large** (1914 files, 237 directories)

---

## Table of Contents

1. [Research Scoping](#1-research-scoping)
2. [Source Inventory](#2-source-inventory)
3. [Object Model & Context Strategy](#3-object-model--context-strategy)
4. [Flow & State Machine Analysis](#4-flow--state-machine-analysis)
5. [Enforcement Audit](#5-enforcement-audit)
6. [Prompt Catalog & Design Analysis](#6-prompt-catalog--design-analysis)
7. [Migration Assessment](#7-migration-assessment)

---

## 1. Research Scoping

### 1.1 Framework Type

ECC 定位为 **agent harness performance system**——不是单个工作流框架，而是一个覆盖全生命周期的插件生态。它包含 47 个 agents、179+ skills、79 commands、自动化 hooks、跨平台安装系统（Claude Code / Cursor / Codex / OpenCode / Gemini），以及一个 alpha 阶段的 Rust 控制面板（`ecc2/`）。

### 1.2 Core Positioning

> "Not just configs. A complete system: skills, instincts, memory optimization, continuous learning, security scanning, and research-first development."
> — `README.md:37`

关键区分点：ECC 不声称提供一个固定的工作流管道，而是提供一个**组件市场 + 钩子运行时 + 自学习系统**的组合，用户按需组装。

---

## 2. Source Inventory

### 2.1 Classified Source Map

| Category | Paths | Description |
|----------|-------|-------------|
| **Overview** | `README.md`, `CLAUDE.md`, `AGENTS.md`, `SOUL.md`, `WORKING-CONTEXT.md`, `RULES.md` | 项目定位、核心原则、活跃工作上下文 |
| **Execution** | `hooks/hooks.json`, `scripts/hooks/*.js`, `scripts/hooks/run-with-flags.js`, `scripts/lib/hook-flags.js`, `install.sh`, `scripts/install-plan.js`, `scripts/install-apply.js` | Hook 运行时、安装管道、脚本基础设施 |
| **Prompts** | `agents/*.md` (47 files), `skills/*/SKILL.md` (179+ files), `commands/*.md` (79 files), `contexts/*.md` (3 files) | Agent 角色定义、技能指令、斜杠命令、上下文模式 |
| **Enforcement** | `hooks/hooks.json` (26 hook entries), `rules/common/*.md`, `rules/{typescript,python,golang,...}/*.md`, `schemas/*.json` (10 schemas) | Hook 硬执行、规则软执行、Schema 校验 |
| **Evolution** | `skills/continuous-learning-v2/`, `skills/continuous-learning/`, `schemas/state-store.schema.json`, `schemas/provenance.schema.json`, `CHANGELOG.md` | 自学习系统、状态存储、技能溯源 |

### 2.2 Component Counts (from `WORKING-CONTEXT.md`)

```
agents:   47 specialized subagents
skills:   179 workflow skills
commands: 79 slash commands (legacy surface, migrating to skills-first)
hooks:    26 registered hook entries across 6 lifecycle events
rules:    15+ language ecosystems (common + per-language)
schemas:  10 JSON schemas
```

---

## 3. Object Model & Context Strategy

### 3.1 Entity Definitions

ECC 的对象模型由 `schemas/state-store.schema.json` 定义，包含 6 个核心实体：

#### Entity 1: Session

```json
// schemas/state-store.schema.json:77-117
{
  "id": "nonEmptyString",
  "adapterId": "nonEmptyString",
  "harness": "nonEmptyString",     // claude | cursor | codex | opencode
  "state": "nonEmptyString",       // active | ended | compacted
  "repoRoot": "nullableString",
  "startedAt": "nullableString",
  "endedAt": "nullableString",
  "snapshot": "object|array"        // session state at capture point
}
```

- **分类**: Fact object（事实记录）
- **生命周期**: SessionStart hook 创建 → Stop hooks 更新 snapshot → SessionEnd hook 标记结束

#### Entity 2: Instinct (from continuous-learning-v2)

```yaml
# skills/continuous-learning-v2/SKILL.md:52-71
id: prefer-functional-style
trigger: "when writing new functions"
confidence: 0.7              # 0.3=tentative → 0.9=near-certain
domain: "code-style"
source: "session-observation"
scope: project               # project | global
project_id: "a1b2c3d4e5f6"
```

- **分类**: Judgment object（判断记录）
- **生命周期**: observation → pattern detection → instinct creation → confidence update → promotion (project→global) → evolution (instinct→skill/command/agent)

#### Entity 3: SkillRun

```json
// schemas/state-store.schema.json:119-169
{
  "id": "nonEmptyString",
  "skillId": "nonEmptyString",
  "skillVersion": "nonEmptyString",
  "sessionId": "nonEmptyString",
  "taskDescription": "nonEmptyString",
  "outcome": "nonEmptyString",        // success | failure | partial
  "failureReason": "nullableString",
  "tokensUsed": "nullableInteger",
  "durationMs": "nullableInteger",
  "userFeedback": "nullableString",
  "createdAt": "nonEmptyString"
}
```

- **分类**: Evidence object（证据记录）
- **用途**: 追踪技能执行效果，供自进化系统评估

#### Entity 4: SkillVersion

```json
// schemas/state-store.schema.json:171-202
{
  "skillId": "nonEmptyString",
  "version": "nonEmptyString",
  "contentHash": "nonEmptyString",
  "amendmentReason": "nullableString",
  "promotedAt": "nullableString",
  "rolledBackAt": "nullableString"
}
```

- **分类**: Fact object
- **用途**: 技能版本追踪、回滚支持

#### Entity 5: Decision

```json
// schemas/state-store.schema.json:203-242
{
  "id": "nonEmptyString",
  "sessionId": "nonEmptyString",
  "title": "nonEmptyString",
  "rationale": "nonEmptyString",
  "alternatives": "jsonArray",
  "supersedes": "nullableString",
  "status": "nonEmptyString",
  "createdAt": "nonEmptyString"
}
```

- **分类**: Judgment object
- **用途**: 架构决策记录（ADR），支持 `supersedes` 链式覆盖

#### Entity 6: GovernanceEvent

```json
// schemas/state-store.schema.json:279-314
{
  "id": "nonEmptyString",
  "sessionId": "nullableString",
  "eventType": "nonEmptyString",    // secret_detected | policy_violation | approval_request
  "payload": "jsonValue",
  "resolvedAt": "nullableString",
  "resolution": "nullableString",
  "createdAt": "nonEmptyString"
}
```

- **分类**: Evidence object
- **用途**: 安全治理审计，由 `governance-capture.js` hook 采集

### 3.2 Entity Relationships

```
Session 1──* SkillRun
Session 1──* Decision
Session 1──* GovernanceEvent
SkillRun *──1 SkillVersion (via skillId + skillVersion)
Instinct *──1 Project (via project_id)
Instinct ──evolves-to──> Skill | Command | Agent
```

### 3.3 Context Isolation Strategy

ECC 采用**三层上下文隔离**：

1. **Hook profile gating** (`ECC_HOOK_PROFILE=minimal|standard|strict`)
   - 每个 hook 注册时声明激活 profile（如 `"standard,strict"`）
   - `run-with-flags.js:97` 调用 `isHookEnabled(hookId, { profiles: profilesCsv })` 进行运行时过滤
   - 证据: `scripts/hooks/run-with-flags.js:89-100`

2. **Project-scoped instinct isolation** (continuous-learning-v2.1)
   - 每个项目基于 git remote URL 生成 12 字符 hash ID
   - observations、instincts、evolved artifacts 均按项目隔离
   - 证据: `skills/continuous-learning-v2/SKILL.md:130-135`

3. **Agent subagent context isolation** (Santa Method)
   - 双独立审查者无共享上下文
   - "Each review round uses **fresh agents**. Reviewers must not carry memory from previous rounds."
   - 证据: `skills/santa-method/SKILL.md:203`

---

## 4. Flow & State Machine Analysis

### 4.1 Session Lifecycle State Machine

```
[New Session]
    │
    ▼
SessionStart hook → session-start-bootstrap.js
    │  loads previous context
    │  detects package manager
    │  registers session lease
    ▼
[Active Session]
    │
    ├─── PreToolUse hooks fire ──→ (block / warn / pass)
    │       │
    │       ▼
    │    Tool executes
    │       │
    │       ▼
    │    PostToolUse hooks fire ──→ (log / warn / learn)
    │       │
    │       ▼
    │    Stop hooks fire ──→ (format/typecheck, console.log check,
    │                         session persist, pattern extract, cost track,
    │                         desktop notify)
    │
    ├─── PreCompact hook ──→ save state before compaction
    │
    ▼
SessionEnd hook → session-end-marker.js
    │  removes session lease
    │  stops observer if last lease
    ▼
[Ended]
```

来源: `hooks/hooks.json` 完整 hook 注册; `hooks/README.md:7-16`

### 4.2 Development Workflow (Happy Path)

```
1. Plan    → planner agent (Opus model)
                │  requirements analysis
                │  architecture review
                │  step breakdown
                ▼
2. TDD     → tdd-guide agent
                │  RED: write failing test → checkpoint commit
                │  GREEN: minimal fix → checkpoint commit
                │  REFACTOR: cleanup → checkpoint commit
                ▼
3. Review  → code-reviewer agent (Sonnet model)
                │  CRITICAL / HIGH / MEDIUM / LOW findings
                │  confidence-based filtering (>80% threshold)
                ▼
4. Verify  → verification-loop skill
                │  Build → Types → Lint → Tests → Security → Diff
                │  produces VERIFICATION REPORT
                ▼
5. Commit  → conventional commits format
```

来源: `AGENTS.md:107-117`

### 4.3 Continuous Learning Flow (Instinct Pipeline)

```
Tool Call (in git repo)
    │
    ▼
observe.sh (PreToolUse + PostToolUse hooks)
    │  5-layer guard against self-loops:
    │    L1: entrypoint filter (cli|sdk-ts only)
    │    L2: minimal profile suppression
    │    L3: ECC_SKIP_OBSERVE env var
    │    L4: subagent session filter (agent_id)
    │    L5: known observer-session path exclusions
    │
    │  project detection (git remote → hash)
    │  secret scrubbing (regex-based)
    ▼
observations.jsonl (project-scoped)
    │  max 10MB, auto-archive + 30-day purge
    ▼
Background Observer (Haiku model)
    │  signal throttle: every N observations (default 20)
    ▼
Pattern Detection
    │  user corrections → instinct
    │  error resolutions → instinct
    │  repeated workflows → instinct
    ▼
Instinct (confidence 0.3-0.9)
    │
    ├── /evolve → cluster → skill/command/agent
    └── /promote → project → global (when seen in 2+ projects, avg confidence ≥ 0.8)
```

来源: `skills/continuous-learning-v2/SKILL.md:82-124`; `skills/continuous-learning-v2/hooks/observe.sh`

### 4.4 Selective Install Pipeline

```
User selects profile (core | developer | security | research | full)
    │
    ▼
install-plan.js
    │  resolves profile → module list
    │  resolves dependencies between modules
    │  generates operation plan
    ▼
install-apply.js
    │  copies paths per module
    │  replaces ${CLAUDE_PLUGIN_ROOT} in hooks
    │  writes install-state.json
    ▼
[Installed State]
    │  tracks: target, request, resolution, source, operations
    │  schema: schemas/install-state.schema.json
```

来源: `manifests/install-profiles.json`; `manifests/install-modules.json`; `schemas/install-state.schema.json`

### 4.5 Failure Paths

| Failure | Handling | Source |
|---------|----------|--------|
| Hook script not found | Warning to stderr, passthrough stdin, exit 0 | `run-with-flags.js:113-117` |
| Plugin root unresolvable | Warning + passthrough (never blocks session) | `session-start-bootstrap.js:158-161` |
| Stdin parsing failure | Fallback: log raw input with secret scrubbing | `observe.sh:212-231` |
| Observer self-loop | 5-layer guard prevents recursive observation | `observe.sh:101-129` |
| Observation file >10MB | Auto-archive with timestamp suffix | `observe.sh:234-241` |
| Max Santa iterations exceeded | Escalate to human | `santa-method/SKILL.md:198-200` |

---

## 5. Enforcement Audit

### 5.1 Hard-Enforced (code/hook prevents violation)

| Behavior | Mechanism | Evidence |
|----------|-----------|----------|
| **Block `--no-verify` in git** | PreToolUse hook on Bash, `npx block-no-verify@1.1.2` | `hooks/hooks.json:9-10` |
| **Block linter config modifications** | PreToolUse hook on Write/Edit/MultiEdit, exit code 2 | `scripts/hooks/config-protection.js:96-103` |
| **Block MCP calls to unhealthy servers** | PreToolUse hook `*` matcher, `mcp-health-check.js` | `hooks/hooks.json:120-129` |
| **Secret scrubbing in observations** | Regex-based scrubbing in `observe.sh` before any persist | `observe.sh:264-276` |
| **Observer self-loop prevention** | 5-layer guard (entrypoint, profile, env, agent_id, path) | `observe.sh:101-129` |
| **Hook path traversal prevention** | `scriptPath.startsWith(resolvedRoot + path.sep)` check | `run-with-flags.js:107-111` |
| **Stdin size limit** | 1MB max with truncation tracking | `run-with-flags.js:18, config-protection.js:81-89` |

### 5.2 Soft-Enforced (prompt instructs but nothing prevents)

| Behavior | Instruction Location | Why Soft |
|----------|---------------------|----------|
| **TDD: write tests before code** | `AGENTS.md:100-104`, `skills/tdd-workflow/SKILL.md:22-23` | 无 hook 检测是否先写了测试 |
| **80% test coverage** | `AGENTS.md:93`, `tdd-workflow/SKILL.md:30` | 无 hook 阻止低覆盖率提交 |
| **Immutability (never mutate)** | `AGENTS.md:77`, `SOUL.md:10` | 纯 prompt 指令 |
| **Agent-first delegation** | `AGENTS.md:48-56`, `SOUL.md:7` | Claude 自行决定是否派遣 agent |
| **Security review before commit** | `AGENTS.md:59-68` | 无 hook 强制安全审查 |
| **Code reviewer must be used** | `agents/code-reviewer.md:3` "MUST BE USED" | 纯 description，无强制机制 |
| **Conventional commits format** | `AGENTS.md:127` | hook 中的 `pre-bash-commit-quality.js` 仅 validates format "when provided via `-m/--message`" |
| **Santa Method dual review** | `skills/santa-method/SKILL.md` | 纯 skill 指令，无 hook 强制双审 |

### 5.3 Unenforced (docs mention but absent from prompts/code)

| Behavior | Where Mentioned | Status |
|----------|----------------|--------|
| **Rate limiting on all endpoints** | `AGENTS.md:67` | 无 hook、无 rule、无 skill 实现 |
| **CSRF protection enabled** | `AGENTS.md:65` | 仅 AGENTS.md 提及 |
| **Authentication/authorization verified** | `AGENTS.md:66` | 仅清单项 |
| **File size limit 800 lines** | `AGENTS.md:79`, `hooks/README.md:176-184` | README 中仅作为 **recipe 示例**，未注册为实际 hook |
| **Small functions <50 lines** | `AGENTS.md:87` | 纯 prompt 建议 |
| **Auto-promotion criteria (2+ projects, ≥0.8 confidence)** | `continuous-learning-v2/SKILL.md:293-295` | 条件在文档中描述，但 `instinct-cli.py` 的实现未在仓库中可见 |

---

## 6. Prompt Catalog & Design Analysis

### 6A. Prompt Catalog

#### Prompt 1: Planner Agent

| Field | Value |
|-------|-------|
| **Role** | Expert planning specialist |
| **repo_path** | `agents/planner.md` |
| **quote_excerpt** | `"Analyze requirements and create detailed implementation plans... Break down complex features into manageable steps"` |
| **Stage** | Pre-implementation (Phase 1 of dev workflow) |
| **design_intent** | 强制 plan-before-code，降低方向性错误 |
| **hidden_assumption** | 假设 Claude 能准确评估 risk 等级和复杂度 |
| **likely_failure_mode** | 计划过度详细导致 token 浪费；或对小任务强制全流程规划 |

#### Prompt 2: Code Reviewer Agent

| Field | Value |
|-------|-------|
| **Role** | Senior code reviewer |
| **repo_path** | `agents/code-reviewer.md` |
| **quote_excerpt** | `"Do not flood the review with noise. Apply these filters: Report if you are >80% confident it is a real issue. Skip stylistic preferences unless they violate project conventions."` |
| **Stage** | Post-implementation (Phase 3 of dev workflow) |
| **design_intent** | 信噪比优化——通过置信度阈值减少虚假警报 |
| **hidden_assumption** | 假设 LLM 能校准自己的置信度到 80% 阈值 |
| **likely_failure_mode** | LLM 置信度校准不可靠，导致该过滤形同虚设或过度过滤 |

#### Prompt 3: Config Protection Hook

| Field | Value |
|-------|-------|
| **Role** | PreToolUse enforcement gate |
| **repo_path** | `scripts/hooks/config-protection.js` |
| **quote_excerpt** | `"BLOCKED: Modifying ${basename} is not allowed. Fix the source code to satisfy linter/formatter rules instead of weakening the config."` |
| **Stage** | Any (fires on every Write/Edit/MultiEdit) |
| **design_intent** | 防止 agent 走捷径修改 linter 配置而非修复代码 |
| **hidden_assumption** | 所有 linter 配置修改都是可疑的 |
| **likely_failure_mode** | 合法的 linter 配置变更被阻断，需要用户临时禁用 hook |

#### Prompt 4: Continuous Learning Observer

| Field | Value |
|-------|-------|
| **Role** | Background observation pipeline |
| **repo_path** | `skills/continuous-learning-v2/hooks/observe.sh` |
| **quote_excerpt** | `"Hooks fire 100% of the time, deterministically. This means: Every tool call is observed. No patterns are missed."` (from `SKILL.md:336-339`) |
| **Stage** | Cross-cutting (every tool call) |
| **design_intent** | 确定性观察替代概率性 skill 触发 |
| **hidden_assumption** | Background Haiku 分析足以提取有意义模式 |
| **likely_failure_mode** | 观察数据量过大但模式提取质量低；token 成本与价值不匹配 |

#### Prompt 5: Santa Method Reviewer

| Field | Value |
|-------|-------|
| **Role** | Independent adversarial verifier |
| **repo_path** | `skills/santa-method/SKILL.md` |
| **quote_excerpt** | `"You are an independent quality reviewer. You have NOT seen any other review of this output... Be rigorous. Your job is to find problems, not to approve."` |
| **Stage** | Post-generation verification |
| **design_intent** | 通过双盲审打破单 agent 自审偏差 |
| **hidden_assumption** | Subagent 之间真正实现了上下文隔离 |
| **likely_failure_mode** | 如使用 sequential inline pattern 替代 subagent，上下文泄漏导致审查无效 |

### 6B. Micro Design Highlights

#### Pattern 1: Hook Profile Gating (run-with-flags)

```javascript
// scripts/hooks/run-with-flags.js:89-100
const [, , hookId, relScriptPath, profilesCsv] = process.argv;
if (!isHookEnabled(hookId, { profiles: profilesCsv })) {
  process.stdout.write(raw);
  process.exit(0);
}
```

**设计亮点**: 所有 hook 通过统一的 `run-with-flags.js` 运行，实现：
- 运行时 profile 过滤（`ECC_HOOK_PROFILE` 环境变量）
- 单个 hook 禁用（`ECC_DISABLED_HOOKS` 逗号分隔）
- 路径遍历防护
- in-process `require()` 优化（节省 50-100ms spawn 开销）

#### Pattern 2: Observer 5-Layer Self-Loop Guard

```bash
# observe.sh:101-129
# Layer 1: entrypoint (cli|sdk-ts only)
# Layer 2: minimal profile suppression
# Layer 3: cooperative skip env var
# Layer 4: subagent session filter
# Layer 5: known path exclusions
```

**设计亮点**: 深度防御——任何单层失效不会导致观察自循环。这是从实际的 memory explosion bug (#521) 中总结出来的。

#### Pattern 3: Install Module Dependency DAG

```json
// manifests/install-modules.json (simplified)
"security" → depends on → "workflow-quality"
"social-distribution" → depends on → "business-content"
"orchestration" → depends on → "commands-core" + "platform-configs"
```

**设计亮点**: 模块化安装，每个模块有 `cost` (light/medium/heavy)、`stability` (stable/beta)、`targets` (支持的 harness 列表) 元数据。

#### Pattern 4: Dual-path Hook Execution

```javascript
// run-with-flags.js:125-176
// Fast path: require() + run(rawInput) for hooks with module.exports
// Slow path: spawnSync for legacy hooks with stdin listeners
```

**设计亮点**: 向后兼容的性能优化——新 hook 可以 export `run()`，老 hook 仍可通过 stdin/stdout 工作。

### 6C. Macro Design Highlights

#### Philosophy 1: Skills-First, Commands-Legacy

> `"skills/ is the canonical workflow surface. commands/ is a legacy slash-entry compatibility surface."` — `AGENTS.md:121-123`

ECC 正在从 commands 迁移到 skills，因为 skills 可以被 Claude 自动触发（不需要用户记住斜杠命令），且内容更丰富。Commands 保留为向后兼容的 shim。

#### Philosophy 2: Harness-Agnostic Plugin Model

ECC 的设计目标是跨 harness 工作：Claude Code、Cursor、Codex、OpenCode、Gemini、Antigravity、CodeBuddy。`manifests/install-modules.json` 中每个模块声明 `targets` 支持列表，安装脚本按目标 harness 过滤组件。

#### Philosophy 3: Self-Improving System

Instinct pipeline 是 ECC 最独特的设计：observation → pattern detection → instinct → evolution → skill。这试图将临时的会话知识转化为持久的可复用行为。但目前 observer 默认关闭（`"observer.enabled": false`），说明这仍是实验性功能。

#### Philosophy 4: Prompt-as-Code with Hook-as-Enforcement

ECC 将 prompt 指令（agents、skills、rules）作为"期望行为"，将 hooks 作为"强制行为"。这是一个务实的分层：大部分行为通过 prompt 引导（成本低、灵活），关键行为通过 hooks 硬执行（成本高、可靠）。

### 6D. Cross-Cutting Interconnections

| Connection | Description |
|------------|-------------|
| **TDD ↔ Verification Loop** | TDD 产出 → verification-loop 校验 build/types/lint/tests/security |
| **Continuous Learning ↔ Santa Method** | "Santa findings become instincts. Repeated failures → learned behavior." (`santa-method/SKILL.md:284`) |
| **Strategic Compact ↔ All Skills** | compact 时机影响所有 skill 的上下文存活；compact 前需运行 Santa、保存 session 状态 |
| **Config Protection ↔ Code Reviewer** | hook 阻止配置弱化 + reviewer agent 检查代码质量，双重保障 |
| **Session Start ↔ Continuous Learning** | SessionStart 创建 session lease → observe.sh 基于 lease 决定是否启动 observer → SessionEnd 释放 lease |
| **Install Modules ↔ Hook Runtime** | `hooks-runtime` 模块是其他模块的隐式依赖；hook 脚本路径依赖 `${CLAUDE_PLUGIN_ROOT}` 解析 |

---

## 7. Migration Assessment

### 7.1 High-Value Migration Candidates

#### Candidate 1: Hook Profile Gating System

| Dimension | Assessment |
|-----------|-----------|
| **Transferability** | High — 纯 Node.js，无 ECC 特有依赖 |
| **Effort** | Low (1-2 days) |
| **Prerequisite** | Claude Code hooks 系统 |
| **Risk** | Low |
| **Failure Mode** | Profile 配置名称冲突 |
| **Key Files** | `scripts/hooks/run-with-flags.js`, `scripts/lib/hook-flags.js` |

核心价值: 通过 `ECC_HOOK_PROFILE` 和 `ECC_DISABLED_HOOKS` 环境变量实现运行时 hook 控制，无需修改 hooks.json。`run()` export 模式节省 50-100ms/hook。

#### Candidate 2: Config Protection Hook Pattern

| Dimension | Assessment |
|-----------|-----------|
| **Transferability** | High — 独立 hook，可直接移植 |
| **Effort** | Trivial (< 1 hour) |
| **Prerequisite** | PreToolUse hook support |
| **Risk** | Low |
| **Failure Mode** | 合法配置变更被阻断 |
| **Key Files** | `scripts/hooks/config-protection.js` |

核心价值: 防止 agent 修改 linter/formatter 配置以绕过检查——这是一个已知的 agent 行为反模式。

#### Candidate 3: Santa Method (Dual Independent Review)

| Dimension | Assessment |
|-----------|-----------|
| **Transferability** | Medium — 概念可移植，但需要 subagent 支持 |
| **Effort** | Medium (2-3 days) |
| **Prerequisite** | Agent 工具支持并行 subagent |
| **Risk** | Medium — 2-3x token 成本 |
| **Failure Mode** | Sequential inline 模式下上下文泄漏；rubric 设计不当导致 rubber stamping |
| **Key Files** | `skills/santa-method/SKILL.md` |

核心价值: 打破单 agent 自审偏差。关键设计点：(1) 双盲，(2) 相同 rubric，(3) 每轮 fresh agents，(4) 结构化 verdict 输出。

#### Candidate 4: Instinct-Based Learning Pipeline

| Dimension | Assessment |
|-----------|-----------|
| **Transferability** | Low-Medium — 概念可移植，但实现复杂 |
| **Effort** | High (1-2 weeks) |
| **Prerequisite** | Hook 系统、background agent、持久化存储 |
| **Risk** | High — observer 默认关闭说明系统仍不成熟 |
| **Failure Mode** | 观察噪声淹没信号；instinct 质量低；self-loop 风险 |
| **Key Files** | `skills/continuous-learning-v2/` (整个目录) |

核心价值: 将会话知识转化为持久行为。最有价值的子组件是 **project-scoped isolation**（基于 git remote hash）和 **5-layer self-loop guard**。

#### Candidate 5: Selective Install Architecture

| Dimension | Assessment |
|-----------|-----------|
| **Transferability** | Medium — manifest 格式可参考，安装逻辑需适配 |
| **Effort** | Medium (3-5 days) |
| **Prerequisite** | 插件系统支持模块化安装 |
| **Risk** | Low |
| **Failure Mode** | 依赖解析不完整导致部分安装失败 |
| **Key Files** | `manifests/install-modules.json`, `manifests/install-profiles.json`, `schemas/install-state.schema.json` |

核心价值: Profile-based 安装（core/developer/security/research/full）+ 模块依赖 DAG + 安装状态持久化。

#### Candidate 6: Strategic Compact Pattern

| Dimension | Assessment |
|-----------|-----------|
| **Transferability** | High — 概念和 hook 脚本均可直接复用 |
| **Effort** | Low (< 1 day) |
| **Prerequisite** | PreToolUse hook support |
| **Risk** | Low |
| **Failure Mode** | 阈值不适配导致过早/过晚提醒 |
| **Key Files** | `skills/strategic-compact/SKILL.md`, 相关 suggest-compact.js |

核心价值: 基于工具调用计数的 compact 提醒，配合相位转换决策表（research→plan: compact; mid-implementation: don't compact）。

### 7.2 Patterns Not Worth Migrating

| Pattern | Reason |
|---------|--------|
| **Stop hook inline `node -e "..."` pattern** | 已被 ECC 自己视为遗留问题（`session-start-bootstrap.js:10-11` 的注释明确说了为什么提取到文件）；巨大的单行 JS 字符串在 hooks.json 中不可维护 |
| **179 个 domain skills** | 大部分是静态知识文档（如 kotlin-patterns、django-security），本质是 prompt 参考材料而非可执行工作流 |
| **Cross-harness packaging** (Cursor/Codex/OpenCode) | 与我们的 Claude Code 专用插件体系无关 |
| **ecc2 Rust 控制面板** | Alpha 阶段，且与我们的架构方向不同 |

---

## Appendix A: Failure Modes Summary

| # | Failure Mode | Evidence | Severity |
|---|-------------|----------|----------|
| 1 | **Observer memory explosion**: rapid tool calls trigger runaway parallel Claude analysis processes | `observe.sh:384-387` 注释引用 issue #521; throttle 机制（`SIGNAL_EVERY_N=20`）是修复 | High |
| 2 | **Stop hook `!` shell expansion**: inline `node -e "..."` 中的 `!` 字符触发 bash history expansion | `session-start-bootstrap.js:10-11` 文档化了该问题 | Medium |
| 3 | **Hook profile fragmentation**: 26 个 hooks 分布在 6 个 lifecycle events，单个 hook 失败的调试成本高 | `hooks/hooks.json` (384 lines); Stop hooks 使用巨大的 inline 脚本包含完整的 root resolution 逻辑 | Medium |
| 4 | **Instinct confidence calibration**: 0.3-0.9 的置信度评分依赖 Haiku 模型的判断质量 | `continuous-learning-v2/SKILL.md:313-330` 描述了增减规则，但无量化校准机制 | Medium |
| 5 | **TDD enforcement gap**: "mandatory" TDD 仅靠 prompt 和 agent description，无 hook 阻止跳过测试的提交 | `AGENTS.md:100` "TDD workflow (mandatory)" vs 实际无 blocking hook | High |
| 6 | **Skill surface bloat**: 179 skills, 大量 domain-specific 知识文档（supply-chain, healthcare, blockchain），增加 token 基线成本 | `manifests/install-modules.json` 中 `supply-chain-domain` 等模块标记为 `"cost": "heavy"` | Low-Medium |

---

## Appendix B: Schema Registry

| Schema | Path | Purpose |
|--------|------|---------|
| Hooks | `schemas/hooks.schema.json` | Hook 配置格式（支持 command/http/prompt 三种 hook 类型） |
| State Store | `schemas/state-store.schema.json` | SQLite state store（session, skillRun, skillVersion, decision, installState, governanceEvent） |
| Plugin | `schemas/plugin.schema.json` | 插件元数据（name, version, skills, agents, features） |
| Install State | `schemas/install-state.schema.json` | 安装状态（target, request, resolution, source, operations） |
| Provenance | `schemas/provenance.schema.json` | Skill 溯源（source, created_at, confidence, author） |
| Install Config | `schemas/ecc-install-config.schema.json` | 安装配置 |
| Install Components | `schemas/install-components.schema.json` | 安装组件定义 |
| Install Modules | `schemas/install-modules.schema.json` | 安装模块定义 |
| Install Profiles | `schemas/install-profiles.schema.json` | 安装 profile 定义 |
| Package Manager | `schemas/package-manager.schema.json` | 包管理器配置 |

---

## Appendix C: Pre-Submit Checklist

| # | Requirement | Status |
|---|-------------|--------|
| A | Source Inventory classified (Overview/Execution/Prompts/Enforcement/Evolution) | PASS — Section 2.1 |
| B | Prompt Traceability with repo_path + quote_excerpt | PASS — Section 6A (5 prompts) |
| C | Object Model with 3+ entities | PASS — Section 3.1 (6 entities) |
| D | State Machine with transitions | PASS — Section 4.1-4.4 |
| E | Enforcement Audit with Hard/Soft/Unenforced | PASS — Section 5 (7 hard, 8 soft, 6 unenforced) |
| F | Micro + Macro design highlights | PASS — Section 6B (4 micro) + 6C (4 macro) |
| G | 3+ failure modes with evidence | PASS — Appendix A (6 failure modes) |
| H | Migration candidates with ratings | PASS — Section 7.1 (6 candidates) |

---

## 附录 D：Gemini Deepdive 补充信息

> 来源：`1st-cc-plugin/workflows/loaf/docs/gemini-roadmap-review/deepdive-everything-claude-code.md`
> 补充内容：ECC 多 Agent 编排的具体实现机制，主报告中未覆盖。

### D.1 Git Worktree + tmux 多 Agent 编排架构

ECC 通过 `scripts/orchestrate-worktrees.js` 实现并行 agent 隔离。该脚本：

1. 解析 `plan.json`（定义 session name、base branch、launcher command 和 workers 数组）
2. 为每个 worker 创建独立的 `git worktree`（`.orchestration/<session>/`）
3. 生成 `task.md`、`handoff.md`、`status.md` 文件用于 file-based 通信
4. 启动隔离的 `tmux` session，每个 worker 一个 pane

**关键数据结构** — `plan.json`：
```json
{
  "session": "feature-auth",
  "base_branch": "main",
  "launcher": "claude",
  "workers": [
    { "name": "backend", "task": "Implement auth API" },
    { "name": "frontend", "task": "Build login UI" }
  ]
}
```

### D.2 Prompt-Level Security Injection

`scripts/orchestrate-codex-worker.sh` 作为 tmux pane 内的入口脚本，在 agent 看到任务前注入安全规则：

- "Work only in the current git worktree."
- "Do not touch sibling worktrees or the parent repo checkout."
- "Do not spawn subagents or external agents for this task."
- "Report progress and final results in stdout only."

该 wrapper 将 LLM 的 stdout 重定向到 `handoff.md` 文件，并附加 `git status` 信息。

### D.3 Confidence-Based Review 的完整流程

Deepdive 揭示了 review agent 的完整工作模式：不仅是 `>80%` 置信度过滤（主报告已提及），还要求输出严格格式化为 **Summary → Files Changed → Validation → Remaining Risks** 四段结构，使得解析脚本或人工审查者可快速做出 gatekeeping 决策。

### D.4 File-Based State Machine 的可调试性

ECC 的 `.orchestration/<session>/<worker>/` 目录结构（`task.md` + `handoff.md` + `status.md`）构成了高度可调试、可重启的状态机。如果 agent 崩溃或 `handoff.md` 未被正确写入，orchestrator 直接注册失败。这比基于内存或数据库的状态管理更透明。
