# Workflow Research: ccg-workflow

> Reverse-engineering report for [fengshao1227/ccg-workflow](https://github.com/fengshao1227/ccg-workflow) v1.8.0
> Generated: 2026-04-03

---

## 1. Framework Profile

| Field | Value |
|-------|-------|
| **Name** | CCG — Claude + Codex + Gemini Multi-Model Collaboration |
| **Version** | v1.8.0 (npm `ccg-workflow`) |
| **Type** | Multi-model orchestrator harness + CLI installer |
| **License** | MIT |
| **Language** | TypeScript (CLI installer) + Go (codeagent-wrapper binary) |
| **Runtime** | Node.js 20+ (installer), Go stdlib (wrapper) |
| **Framework** | cac (CLI) + inquirer (interactive) + unbuild (build) |
| **Size** | 216 files, ~27 slash commands, 13 expert prompts, 6 skills, 4 agents |
| **Architecture** | Claude Code = orchestrator; Codex = backend worker; Gemini = frontend worker |
| **Install mechanism** | `npx ccg-workflow` copies templates to `~/.claude/{commands,agents,skills,rules}/ccg/` + binary to `~/.claude/bin/` |
| **Core innovation** | Go binary (`codeagent-wrapper`) as process-level proxy for external CLI backends |

**Framework type hypothesis confirmed**: Hybrid — CLI installer (TypeScript) + process-level proxy (Go binary) + prompt-driven orchestration (Markdown templates). The "framework" is largely **process-as-prose**: the workflow logic lives in prompt Markdown files injected into Claude's context, not in programmatic code.

---

## 2. Source Inventory

### Overview

| File | Role |
|------|------|
| `README.md` | User-facing documentation, command tables, architecture diagram |
| `CLAUDE.md` | Project instructions for Claude Code sessions — changelog, module responsibilities, release rules |
| `CONTRIBUTING.md` | Contribution guidelines |
| `docs/` | VitePress documentation site (guide pages in Chinese + English) |

### Execution (commands, agents, prompts, skills)

| Category | Count | Path | Description |
|----------|-------|------|-------------|
| **Slash commands** | 27 | `templates/commands/*.md` | Core workflow templates installed to `~/.claude/commands/ccg/` |
| **Sub-agents** | 4 | `templates/commands/agents/*.md` | planner, ui-ux-designer, init-architect, get-current-datetime |
| **Codex prompts** | 6 | `templates/prompts/codex/` | analyzer, architect, debugger, optimizer, reviewer, tester |
| **Gemini prompts** | 7 | `templates/prompts/gemini/` | analyzer, architect, debugger, frontend, optimizer, reviewer, tester |
| **Claude prompts** | 6 | `templates/prompts/claude/` | analyzer, architect, debugger, optimizer, reviewer, tester |
| **Skills** | 6+1 | `templates/skills/` | verify-security, verify-quality, verify-change, verify-module, gen-docs, multi-agent + root SKILL.md |
| **OpenSpec skills** | 10 | `.agents/skills/openspec-*` | OPSX integration for spec-driven development |
| **Output styles** | 5 | `templates/output-styles/` | Personality-themed output styles (abyss-cultivator, engineer-professional, etc.) |
| **Rules** | 1 | `templates/rules/ccg-skills.md` | Quality gate auto-trigger rules injected to `~/.claude/rules/` |

### Enforcement

| File | Role | Type |
|------|------|------|
| `src/utils/installer.ts` | Template copy + variable injection + binary download | Hard (exit on failure) |
| `src/utils/installer-template.ts` | `{{WORKDIR}}`, `{{MCP_SEARCH_TOOL}}`, `{{LITE_MODE_FLAG}}` variable replacement | Hard |
| `codeagent-wrapper/main.go` | Process-level proxy for Codex/Gemini/Claude CLI backends | Hard (exit codes) |
| `codeagent-wrapper/backend.go` | Backend interface + arg building for codex/gemini/claude | Hard |
| `codeagent-wrapper/executor.go` | Concurrent task execution with topological sort + dependency skip | Hard |
| `.github/workflows/ci.yml` | TypeScript lint + typecheck + test + build; Go build + test | Hard (CI gate) |
| `.github/workflows/build-binaries.yml` | Cross-compile Go binary + upload to GitHub Release + R2 mirror | Hard |
| `templates/rules/ccg-skills.md` | Quality gate trigger rules injected as Claude rules | Soft (prompt only) |

### Evolution

| File | Role |
|------|------|
| `CHANGELOG.md` | Full version history |
| `.github/ISSUE_TEMPLATE/` | bug_report, feature_request, good_first_issue templates |
| `.github/pull_request_template.md` | PR template |
| `src/utils/__tests__/` | 6 test files (config, injectConfigVariables, installWorkflows, installer, platform, version) |
| `codeagent-wrapper/*_test.go` | 14 Go test files (backend, bench, concurrent_stress, executor_concurrent, filter, logger, main, parser, process_check, path_normalization, wrapper_name, utils, log_writer_limit, logger_additional_coverage) |

---

## 3. Object Model & Context Strategy

### First-Class Entities

| Entity | Definition location | Required fields | Lifecycle |
|--------|-------------------|-----------------|-----------|
| **Command** (slash command) | `templates/commands/<name>.md` — YAML frontmatter `description` | description, body with `$ARGUMENTS` | Created at install → injected with config vars → copied to `~/.claude/commands/ccg/` → invoked by user via `/ccg:<name>` |
| **Agent** (sub-agent) | `templates/commands/agents/<name>.md` | YAML frontmatter | Created at install → copied to `~/.claude/agents/ccg/` → spawned by Claude during workflow phases |
| **Prompt** (expert role) | `templates/prompts/{codex,gemini,claude}/<role>.md` | Role description, constraints, checklist | Created at install → copied to `~/.claude/.ccg/prompts/` → injected via `ROLE_FILE:` directive in codeagent-wrapper calls |
| **Skill** | `templates/skills/**/SKILL.md` — YAML frontmatter | name, description, allowed-tools | Created at install → copied to `~/.claude/skills/ccg/` → auto-triggered per rules or manually invoked |
| **Rule** | `templates/rules/ccg-skills.md` | Trigger conditions | Created at install → copied to `~/.claude/rules/` → always loaded into Claude context |
| **Backend** | `codeagent-wrapper/backend.go` — Go interface | Name(), Command(), BuildArgs() | Selected at runtime via `--backend` flag → builds CLI args → spawns subprocess |
| **TaskSpec** | `codeagent-wrapper/executor.go` | ID, Task, Backend, Dependencies | Created by parallel mode config → topologically sorted → concurrently executed |
| **InstallConfig** | `src/utils/installer.ts:59-68` | routing, liteMode, mcpProvider | Created during init → drives template variable injection |

### Entity Relationships

```
Command ──references──> Prompt (via ROLE_FILE path)
Command ──calls──> codeagent-wrapper (via Bash tool)
Command ──may trigger──> Skill (via rules)
Skill ──chains to──> Skill (verify-module → verify-security)
Backend <──selected by──> codeagent-wrapper (via --backend flag)
TaskSpec ──depends on──> TaskSpec (via Dependencies array)
Agent ──spawned by──> Command (during workflow phases)
```

### Context Flow Strategy

**Context isolation model**: Claude = orchestrator with full context; Codex/Gemini = workers in isolated sandboxes.

| Flow | Mechanism | Evidence |
|------|-----------|----------|
| Controller → Worker | Task text piped via stdin to `codeagent-wrapper` → Codex/Gemini CLI | `executor.go:1133-1139` |
| Worker → Controller | stdout JSON stream parsed by `codeagent-wrapper` → aggregated message returned to Claude | `executor.go:1089-1110` |
| Cross-phase state | `SESSION_ID` returned by wrapper → reused via `resume <SESSION_ID>` in subsequent calls | `workflow.md:86-87`, `plan.md:57` |
| Plan persistence | Plan saved to `.claude/plan/<name>.md` → read by `/ccg:execute` or `/ccg:codex-exec` | `plan.md:196-197` |
| Context persistence | `.context/` directory for project prefs, coding style, commit history | `CLAUDE.md:70-73` |
| Token budget | No explicit token counting; relies on command template size (~1-3k tokens each) + prompt sizes (~200-500 tokens each) | No enforcement mechanism found |

### Object Classification

| Object | Type | Rationale |
|--------|------|-----------|
| Plan file (`.claude/plan/*.md`) | **Fact object** | Input data for execution |
| Codex/Gemini raw output | **Evidence object** | "Dirty prototype" to be refactored |
| Review score report | **Judgment object** | Review verdict with PASS/NEEDS_IMPROVEMENT |
| Quality gate report | **Judgment object** | Security/quality scan results |
| SESSION_ID | **Evidence object** | Execution proof for session continuity |

---

## 4. Flow & State Machine

### Primary Flow: `/ccg:workflow` (6-phase)

```
[研究] ──gate(score≥7)──> [构思] ──user-confirm──> [计划] ──user-confirm──> [执行] ──> [优化] ──> [评审]
  │                          │                        │                       │          │          │
  │ Prompt enhancement       │ Codex∥Gemini           │ Codex∥Gemini          │ Claude   │ Codex∥   │ Final
  │ MCP search               │ parallel analysis      │ parallel planning     │ writes   │ Gemini   │ check
  │ Completeness score       │ Cross-validate          │ Save to plan file     │ code     │ review   │
  │                          │ User selects option     │ User approves          │          │          │
  ↓                          ↓                        ↓                       ↓          ↓          ↓
  score<7 → STOP           Wait for both models     Plan → .claude/plan/    Implement  Optimize   Deliver
```

**Phase transitions**: Each phase ends with user confirmation via `AskUserQuestion`. Score < 7 or user rejection → forced stop. (`workflow.md:107-111`)

### Plan → Execute Split Flow

```
/ccg:plan ────────> .claude/plan/<name>.md
                          │
                ┌─────────┼─────────┐
                ↓                   ↓
         /ccg:execute        /ccg:codex-exec
         (Claude refactors)  (Codex implements)
                │                   │
                ↓                   ↓
         Phase 3: Prototype   Phase 1: Codex executes
         Phase 4: Claude impl Phase 2: Claude reviews
         Phase 5: Audit       Phase 3: Multi-model audit
                │                   │
                └─────────┬─────────┘
                          ↓
                    Multi-model review
                    (Codex ∥ Gemini)
```

### Agent Teams Flow

```
/ccg:team-research → constraints file
     ↓ /clear
/ccg:team-plan → .claude/team-plan/<name>.md (subtask decomposition)
     ↓ /clear
/ccg:team-exec → TeamCreate → spawn Builders → parallel execution → collect results
     ↓ /clear
/ccg:team-review → Codex ∥ Gemini cross-review
```

**Key state transitions in codeagent-wrapper**:

```
parseArgs() → selectBackend() → buildArgs() → Start() → [stdin pipe] → parseJSONStream()
     │                                                          │
     │ Parallel mode:                                           │
     │ parseParallelConfig() → topologicalSort()                │
     │ → executeConcurrent() → [layer-by-layer]                 │
     │                                                          ↓
     │                                              messageSeen / completeSeen
     │                                              → postMessageDelay → terminate
     ↓
Exit: 0=success, 1=error, 124=timeout, 127=not-found, 130=interrupted
```

### Failure Paths

**Failure path 1: External model timeout**
- `codeagent-wrapper` has 2-hour default timeout (`defaultTimeout = 7200`)
- Claude templates instruct `TaskOutput(timeout: 600000)` (10 min) then poll
- Templates **prohibit** killing Codex process; mandate `AskUserQuestion` to confirm
- Evidence: `workflow.md:97-101`

**Failure path 2: Gemini call failure**
- Templates mandate retry: max 2 retries with 5s interval
- Only after 3 total failures: degrade to single-model
- Evidence: `workflow.md:100`, repeated across 20 command templates (`CLAUDE.md:45`)

**Failure path 3: Parallel task dependency failure**
- `executor.go:527-544`: `shouldSkipTask()` checks if any dependency failed → skip with error
- Layer-by-layer execution: failed tasks propagate to dependents
- Evidence: `executor.go:436-440`

---

## 5. Enforcement Audit

### Enforcement Matrix

| Constraint | Claimed in | Enforcement level | Evidence |
|-----------|------------|-------------------|----------|
| **External models have zero write access** | `workflow.md:192`, `plan.md:15`, `execute.md:14` | **Soft** — prompt instruction only. codeagent-wrapper does NOT restrict Codex/Gemini file access. Codex runs with `--dangerously-bypass-approvals-and-sandbox` (`executor.go:777`). | The "security by design" claim in README is **rhetoric, not code enforcement**. |
| **Phase order cannot be skipped** | `workflow.md:190` | **Soft** — prompt instruction only. No code prevents phase skipping. | No validator checks phase sequence. |
| **Score < 7 forces stop** | `workflow.md:191` | **Soft** — prompt instruction only. No hook or validator. | Score is generated and evaluated by Claude itself. |
| **Codex results must be waited for** | `workflow.md:101` | **Soft** — prompt instruction only. Emphasized with bold + ban emoji across 20 templates. | No technical mechanism prevents Claude from proceeding. |
| **Quality gates auto-trigger** | `ccg-skills.md` (rules file) | **Soft** — rules file loaded into Claude context; triggers are prompt-based "should" not "must". | `ccg-skills.md:53`: "Non-blocking — Quality gates produce reports but do NOT block delivery unless Critical issues are found" |
| **Binary version match** | `installer.ts:53`, `main.go:17` | **Hard** — installer checks `EXPECTED_BINARY_VERSION` vs installed binary `--version` output; mismatch triggers re-download. | `installer.ts:473-483` |
| **CI type-check + test + build** | `.github/workflows/ci.yml` | **Hard** — PR/push to main triggers Node 20/22 matrix test + Go build + Go test. | `ci.yml:1-54` |
| **Template variable injection** | `installer-template.ts` | **Hard** — `injectConfigVariables()` replaces `{{WORKDIR}}`, `{{MCP_SEARCH_TOOL}}`, etc. at install time. | `installer.ts:191-192` |
| **codeagent-wrapper exit codes** | `main.go:581-587` | **Hard** — structured exit codes (0/1/124/127/130) propagated to Claude. | `main.go:581-587`, `executor.go:1270-1280` |
| **Parallel task dependency enforcement** | `executor.go:287-351` | **Hard** — topological sort with cycle detection; failed deps → skip downstream. | `executor.go:339-347` |
| **Skills namespace isolation** | `installer.ts:344-375` | **Hard** — skills installed to `skills/ccg/` subdirectory; uninstall only removes `skills/ccg/`, preserving user skills. | `installer.ts:736-746` |
| **Auto-authorization hook** | `README.md:257-282` | **Hard** — PreToolUse hook auto-approves `codeagent-wrapper` Bash commands via `jq` script. Also: `permissions.allow` with `Bash(*codeagent-wrapper*)` pattern. | `CLAUDE.md:36-38` |
| **Plan-only mode: no code writes** | `plan.md:17`, `plan.md:215-219` | **Soft** — prompt instruction: "禁止修改产品代码", "绝对禁止对产品代码进行任何写操作". No hook prevents writes. | No `PostToolUse` hook validates this. |
| **File ownership in Agent Teams** | `team-exec.md:14`, `multi-agent/SKILL.md:379-389` | **Soft** — prompt instruction to Builders: "严禁修改任何其他文件". No technical enforcement. | Builders operate as standard Claude agents with full file access. |

### Key Enforcement Gap

**The most critical gap**: The README claims "Security by design — External models have no write access" but:

1. Codex is invoked with `--dangerously-bypass-approvals-and-sandbox` (`executor.go:777`)
2. Gemini is invoked with `-y` (auto-approve) (`backend.go:133`)
3. Claude backend disables all setting sources: `--setting-sources ""` (`backend.go:96`)
4. The "zero write" constraint exists only as prompt text in command templates

This is **soft enforcement at best** — the external models CAN write files; the prompt merely instructs Claude to treat their output as "dirty prototypes" and apply changes itself. A more honest framing: "Claude reviews before applying external model suggestions" rather than "external models have no write access".

---

## 6. Prompt Catalog

### 6A. Key Prompts

| Role | repo_path | quote_excerpt | Stage | Design intent | Hidden assumption | Likely failure mode |
|------|-----------|---------------|-------|--------------|-------------------|---------------------|
| **Orchestrator** | `templates/commands/workflow.md:23-29` | "你是**编排者**，协调多模型协作系统（研究 → 构思 → 计划 → 执行 → 优化 → 评审），用中文协助用户" | All phases | Define Claude's role as coordinator not implementer | User speaks Chinese; task is full-stack | Non-Chinese speakers get poor UX; language is hardcoded |
| **Codex Reviewer** | `templates/prompts/codex/reviewer.md:7-9` | "You are a senior code reviewer specializing in backend code quality, security, and best practices. ZERO file system write permission - READ-ONLY sandbox" | Phase 5/6 review | Backend-focused quality gate | Codex respects READ-ONLY instruction | Codex may still write files if not sandboxed; prompt is not technical enforcement |
| **Gemini Reviewer** | `templates/prompts/gemini/reviewer.md:7-9` | "You are a senior UI reviewer specializing in frontend code quality, accessibility, and design system compliance. ZERO file system write permission" | Phase 5/6 review | Frontend-focused quality gate | Same as above | Same as above |
| **Plan guardrail** | `templates/commands/plan.md:192-219` | "⚠️ 绝对禁止：❌ 问用户 Y/N 然后自动执行 ❌ 对产品代码进行任何写操作 ❌ 自动调用 /ccg:execute" | Plan delivery | Prevent Claude from auto-executing after planning | Claude follows instructions consistently | Claude may still attempt execution if user is ambiguous |
| **Codex-exec one-shot** | `templates/commands/codex-exec.md:170-231` | "You are a full-stack execution agent. Implement the following plan end-to-end." | Codex execution | Offload MCP search + implementation + testing entirely to Codex | Codex has MCP tool access; plan is sufficiently detailed | If MCP not configured, Codex falls back to guessing |
| **Multi-agent Lead** | `templates/skills/orchestration/multi-agent/SKILL.md:249-267` | "你是天罗主修（蚁后），负责协调多 Agent 协同任务。铁律：每个文件只能分配给一个 Agent" | Team execution | File-level ownership isolation | Agents respect file boundaries | No technical file lock; agents can still write anywhere |
| **Verify-security** | `templates/skills/tools/verify-security/SKILL.md:15-20` | "安全即道基，破则劫败。Critical/High 问题必须修复后才能交付" | Post-implementation | Security quality gate | `security_scanner.js` script exists and works | Script references `scripts/security_scanner.js` in skill dir — must be installed alongside SKILL.md |

### 6B. Prompt Design Observation

All command templates share a **repeated boilerplate block** (~40 lines) for "多模型调用规范" (multi-model invocation spec). This is copy-pasted across 20+ command files with minor variations (`CLAUDE.md:45-46`). This creates:
- **Maintenance burden**: Bug fixes must be applied to 20+ files simultaneously (evidenced by v1.7.87 fixing Gemini retry rules across "20 个命令模板")
- **Consistency risk**: Templates can drift out of sync

---

## 7. Design Highlights — Micro

### 7.1 `codeagent-wrapper` as Process-Level Proxy

**Observation**: The Go binary is the system's most sophisticated component — a multi-backend process proxy with JSON stream parsing, session management, parallel execution, and structured output.

**Evidence**: `codeagent-wrapper/main.go`, `backend.go`, `executor.go` — ~1500 lines of Go with 14 test files, Backend interface pattern, topological sort for parallel tasks.

**Why it matters**: This is the only component with real engineering rigor (typed interfaces, tests, error handling, cross-platform support). It solves a real problem: reliably invoking external CLI tools from a background Bash command and capturing their structured output.

**Transferability**: High — the process proxy pattern is reusable for any multi-CLI orchestration. The parallel execution with dependency graph is particularly valuable.

### 7.2 Template Variable Injection System

**Observation**: `installer-template.ts` replaces `{{WORKDIR}}`, `{{MCP_SEARCH_TOOL}}`, `{{LITE_MODE_FLAG}}`, `{{GEMINI_MODEL_FLAG}}` in templates at install time.

**Evidence**: `installer.ts:191-192` — `injectConfigVariables(content, ctx.config)` + `replaceHomePathsInTemplate(content, ctx.installDir)`.

**Why it matters**: Allows templates to be environment-agnostic in source but environment-specific at install time. However, the `{{WORKDIR}}` token in command templates is replaced at install time, which means it's baked to a static path — commands instruct Claude to detect `WORKDIR` dynamically at runtime, creating a two-layer variable system.

**Transferability**: Direct — simple string replacement pattern.

### 7.3 `ROLE_FILE:` Directive for Prompt Injection

**Observation**: Command templates instruct Claude to include `ROLE_FILE: <path>` as the first line of the stdin task text. The `codeagent-wrapper` then calls `injectRoleFile()` to read the referenced file and prepend its content.

**Evidence**: `main.go:272-276` — `injectRoleFile(cfg.Tasks[i].Task)`, `main.go:394-397`.

**Why it matters**: This is a clever mechanism to inject expert prompts into external model calls without bloating the command template. The prompt file is read at wrapper execution time, not at install time, so it's always current.

**Transferability**: Direct — elegant pattern for separating role definitions from workflow definitions.

### 7.4 Session Continuity via `resume <SESSION_ID>`

**Observation**: codeagent-wrapper captures `SESSION_ID` from backend's JSON stream output and returns it to Claude. Subsequent calls use `resume <SESSION_ID>` to continue the same conversation.

**Evidence**: `executor.go:1300-1301` — `result.SessionID = threadID`, `plan.md:57`, `execute.md:98`.

**Why it matters**: Enables multi-phase workflows where Codex/Gemini maintain context across plan→execute transitions. Without this, each phase would start from scratch.

**Transferability**: Inspired — requires backend CLI support for session resumption.

### 7.5 Dual-Source Binary Download with CDN Fallback

**Observation**: Binary download tries Cloudflare R2 CDN first (30s timeout, China-friendly), then falls back to GitHub Release (120s timeout).

**Evidence**: `installer.ts:86-89` — `BINARY_SOURCES` array with two entries.

**Why it matters**: Pragmatic solution for users in China where GitHub is slow/blocked. Shows attention to real deployment constraints.

---

## 8. Design Highlights — Macro

### 8.1 Process-as-Prose Architecture

**Observation**: The entire workflow logic — phase sequencing, quality gates, model routing, error handling — is encoded in Markdown prompt files, not in code. The code (installer + wrapper) only handles template deployment and process management.

**Evidence**: Compare `workflow.md` (193 lines of workflow logic) with `installer.ts` (793 lines of file copying) — the installer has no awareness of workflow semantics.

**Why it matters**: This is a fundamentally different architecture from code-driven workflow engines. Strengths: rapid iteration (edit a .md file), no build step for workflow changes. Weaknesses: zero enforcement, no type safety on workflow logic, difficult to test workflow behavior, prone to prompt drift across templates.

**Transferability**: Philosophical — the tradeoff between "workflow-as-code" (enforcement, testability) vs "workflow-as-prose" (flexibility, speed) is a key design decision for any agent workflow system.

### 8.2 Fixed Routing: Frontend → Gemini, Backend → Codex

**Observation**: Model routing is hardcoded. Gemini always handles frontend; Codex always handles backend. No dynamic model selection, no fallback routing (beyond Gemini retry).

**Evidence**: `CLAUDE.md:261-268` — "v1.7.0 起，以下配置不再支持自定义" with fixed frontend=Gemini, backend=Codex.

**Why it matters**: Simplicity over flexibility. Removes configuration surface but also removes user choice. If Gemini becomes better at backend (or vice versa), the system cannot adapt without template changes.

### 8.3 "Dirty Prototype" Refactoring Pattern

**Observation**: External models produce "dirty prototypes" (Unified Diff patches); Claude reviews and refactors before applying. This is the core safety model.

**Evidence**: `execute.md:15-16` — "将 Codex/Gemini 的 Unified Diff 视为'脏原型'，必须重构为生产级代码".

**Why it matters**: This is a thoughtful human-in-the-loop-adjacent pattern where Claude acts as a "senior developer" reviewing junior developers' (Codex/Gemini) output. However, in `/ccg:codex-exec` mode, Codex writes directly and Claude only reviews after the fact — the refactoring step is skipped.

### 8.4 Multi-Agent Coordination: Ant Colony Metaphor

**Observation**: The multi-agent skill uses an ant colony metaphor with Scout (explorer), Worker (implementer), Soldier (reviewer), Lead (coordinator) roles, and a "pheromone" system using TaskCreate metadata for indirect communication.

**Evidence**: `templates/skills/orchestration/multi-agent/SKILL.md:1-494` — 494 lines of orchestration design.

**Why it matters**: This is the most ambitious design in the system. The pheromone concept (encoding `discovery`/`progress`/`warning`/`repellent` signals in task metadata) is creative. However, it's entirely prompt-based — the TaskCreate API doesn't actually enforce pheromone semantics.

---

## 9. Failure Modes

### FM-1: Prompt Boilerplate Drift

**Observed**: v1.7.87 changelog: "20 个命令模板新增 Gemini 调用失败重试规则" and "20 个命令模板新增 Codex 等待规则" — manual patching across 20 files.

**Root cause**: No shared include mechanism. Each command template contains a full copy of the "多模型调用规范" block.

**Impact**: High — a fix missed in one template creates inconsistent behavior. Already evidenced by multiple "补漏" (patch-missing) entries in changelog.

### FM-2: False Security Claim

**Observed**: README claims "Security by design — External models have no write access" while `executor.go:777` passes `--dangerously-bypass-approvals-and-sandbox` to Codex.

**Root cause**: The "security" is prompt-level instruction, not process-level sandboxing.

**Impact**: Medium — users may trust the security claim and use CCG in sensitive environments where actual sandboxing is needed.

### FM-3: No Enforcement of Plan-Execute Boundary

**Observed**: `/ccg:plan` includes elaborate guardrails ("⚠️ 绝对禁止：❌ 对产品代码进行任何写操作") but no hook validates that no writes occurred.

**Root cause**: Process-as-prose architecture — no `PostToolUse` hook checks for file writes during plan phase.

**Impact**: Low-medium — Claude generally follows instructions, but under complex interactions may inadvertently write files.

### FM-4: Binary Version Coupling

**Observed**: `CLAUDE.md:461-464` documents that wrapper Go version and `installer.ts` EXPECTED_BINARY_VERSION must match manually. Mismatch → users can't download correct binary.

**Root cause**: No automated version sync between Go source and TypeScript installer.

**Impact**: Medium — release process requires manual vigilance.

### FM-5: Session-ID Fragility

**Observed**: Session continuity depends on Claude correctly parsing and storing `SESSION_ID` from wrapper output, then correctly injecting it into subsequent `resume` calls.

**Root cause**: No structured session handoff mechanism — SESSION_ID is embedded in free-text output and depends on prompt instructions for propagation.

**Impact**: Medium — if Claude fails to capture SESSION_ID (context compression, prompt drift), the workflow degrades to stateless mode.

### FM-6: Hardcoded Chinese Language

**Observed**: All command templates are in Chinese. `CLAUDE.md:261` documents: "语言 | 固定值 | 中文 | 所有模板为中文". i18n added in v1.7.69 but only for CLI, not templates.

**Root cause**: Templates were written for Chinese-speaking users first; i18n for templates not implemented.

**Impact**: High for non-Chinese users — the workflow instructions, phase labels, and error messages are all Chinese.

---

## 10. Migration Assessment

### Migration Candidates

| Mechanism | Source | Transferability | Effort | Prerequisite | Risk |
|-----------|--------|----------------|--------|--------------|------|
| **codeagent-wrapper process proxy** | `codeagent-wrapper/` (Go) | Direct | L | Go build infrastructure | Over-engineering for single-backend use |
| **ROLE_FILE: directive** | `main.go` injectRoleFile | Direct | S | Wrapper-like process proxy | None — elegant and simple |
| **Session continuity (resume)** | `executor.go`, command templates | Inspired | M | Backend CLI support for sessions | Session ID capture fragility |
| **Parallel execution with toposort** | `executor.go:287-515` | Direct | M | Go binary or equivalent | Complexity of dependency graph management |
| **Template variable injection** | `installer-template.ts` | Direct | S | Installer pipeline | Two-layer variable system confusion |
| **Quality gate skills** | `templates/skills/tools/verify-*` | Inspired | M | Skill infrastructure | Scripts referenced in SKILL.md may not exist |
| **Multi-agent pheromone system** | `multi-agent/SKILL.md` | Inspired | L | Agent Teams support | Purely prompt-based; no real enforcement |
| **Dual-source binary download** | `installer.ts:86-89` | Direct | S | CDN + GitHub Release setup | CDN maintenance burden |
| **Plan→Execute split** | `plan.md`, `execute.md`, `codex-exec.md` | Inspired | M | Plan file format + session handoff | Plan format coupling |
| **Output styles (personality)** | `templates/output-styles/` | Non-transferable | - | Cultural context | Niche appeal |

### Recommended Adoption Order

1. **ROLE_FILE: directive** (S) — Immediately useful for any multi-model skill. Zero risk.
2. **Template variable injection** (S) — Useful if building a similar installer.
3. **Plan→Execute split design** (M) — The concept of separating planning from execution, with plan persistence to files, is broadly valuable. Adapt the format, not the templates.
4. **Quality gate skill pattern** (M) — The trigger-based auto-invocation of verification skills is a good pattern. Needs hard enforcement (hooks) to be meaningful.
5. **codeagent-wrapper proxy** (L) — Only if building a multi-backend orchestration system. The Go binary is well-engineered but heavy.

### Must-Build Enforcement (if porting patterns)

| Gap in CCG | What to build | Why |
|-----------|---------------|-----|
| No phase enforcement | `PostToolUse` hook that validates phase transitions | Prevent phase skipping |
| No write-protection in plan mode | `PreToolUse` hook blocking Write/Edit during plan phase | Enforce plan-only semantics |
| No file ownership enforcement | `PreToolUse` hook checking file paths against agent assignments | Prevent cross-agent file conflicts |
| No template deduplication | Shared include mechanism for common blocks | Prevent boilerplate drift |
| No session handoff validation | Structured session state file instead of free-text SESSION_ID | Prevent session loss on context compression |

---

## 11. Open Questions

1. **`security_scanner.js` existence**: `verify-security/SKILL.md` references `scripts/security_scanner.js` but no such file was found in the template directory. Is it generated at install time or expected to be user-provided?

2. **`run_skill.js` runner**: `SKILL.md` references `~/.claude/skills/ccg/run_skill.js` as a unified skill runner. What does it do? Is it a thin wrapper or does it have logic?

3. **OPSX integration depth**: 10 OpenSpec skills exist in `.agents/skills/openspec-*` but they appear to be pass-through wrappers for the OPSX CLI. How deep is the integration — does CCG add value beyond forwarding, or is it purely a command alias?

4. **`.context/` directory lifecycle**: Introduced in v1.7.80, this persistence mechanism is referenced by 13 role prompts. How widely is it actually adopted? Does it conflict with Claude Code's own memory system?

5. **Test coverage gap**: The 6 TypeScript test files test installer mechanics, not workflow behavior. No tests validate that command templates produce correct wrapper invocations, that SESSION_ID is correctly propagated, or that phase transitions work as documented. Is this intentional (untestable prompt behavior) or a coverage gap?

---

## Pre-Submit Checklist

| # | Gate | Pass? |
|---|------|-------|
| A | Source Inventory: classified as overview/execution/prompt/enforcement/evolution | Yes |
| B | Prompt Traceability: every major role has catalog entry with repo_path + quote_excerpt | Yes |
| C | Object Model: at least 3 first-class entities with lifecycle | Yes (8 entities) |
| D | State Machine: phases with transitions, not a flat step list | Yes (3 flow diagrams) |
| E | Enforcement Audit: every key constraint classified as Hard/Soft/Unenforced | Yes (14 entries) |
| F | Micro + Macro split: both design highlight levels present | Yes (5 micro + 4 macro) |
| G | Failure Modes: at least 3 with evidence | Yes (6 failure modes) |
| H | Migration Output: candidates with ratings, adoption order, must-build enforcement | Yes |
