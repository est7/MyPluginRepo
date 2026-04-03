# Workflow Research Report: Flowspec

> **Framework**: flowspec (Spec-Driven Development platform)
> **Repository**: `vendor/flowspec/` (jpoley/flowspec)
> **Version**: 0.4.008 (CLI) | 0.0.20 (plugin manifest)
> **Research Date**: 2026-04-02
> **Evidence Level**: Direct (source code access)

---

## 1. Framework Profile

| Dimension | Value |
|-----------|-------|
| **Type** | Workflow harness + Agent orchestrator (hybrid) |
| **Primary Language** | Python 3.11+ (CLI: typer + rich) |
| **Target Platforms** | Claude Code, GitHub Copilot, Codex, Gemini CLI, Cursor, Windsurf |
| **Core Concept** | Spec-Driven Development (SDD) — formal specs before code |
| **License** | MIT |
| **Dependencies** | typer, rich, httpx, pyyaml, jsonschema, mcp, node-pty |
| **Test Framework** | pytest (>80% coverage target) |
| **Linter/Formatter** | Ruff (replaces Black + Flake8 + isort) |
| **Package Manager** | UV |

### Directory Map

```
vendor/flowspec/
├── .agents/               # 15 specialized agent personas (markdown)
├── .beads/                # Issue tracking config for AI agents
├── .claude/               # Claude Code integration layer
│   ├── agents/            # 5 dispatchable agent files
│   ├── agents-config.json # Agent→workflow mapping (14 agents × 6 workflows)
│   ├── commands/flow/     # 22 slash commands (markdown)
│   ├── rules/             # 8 auto-loaded rule files
│   ├── settings.json      # Permissions, hooks, preferences
│   └── skills/            # 20 internal skills
├── .flowspec/             # Event logging & active work tracking
├── .languages/            # Language-specific guidance (C++, Go, Rust)
├── .stacks/               # 8 pre-configured tech stacks
├── build-docs/            # 150+ research, ADR, platform docs
├── docs/                  # User-facing guides & specs
├── examples/              # MCP integration examples
├── memory/                # Durable state (constitution, decisions, learnings)
├── schemas/               # JSON schemas for workflow config
├── scripts/               # Bash/Python/PowerShell utilities
├── src/flowspec_cli/      # Python source code
│   ├── workflow/          # State machine, validator, orchestrator (14 files)
│   ├── backlog/           # Backlog.md parsing, dep graphs (6 files)
│   ├── memory/            # Task memory store, lifecycle (8 files)
│   ├── security/          # Triage engine, fixer, SAST/DAST/SCA (20+ files)
│   ├── quality/           # Complexity scorer (3 files)
│   └── hooks/             # Event emitter, runner, config (8 files)
├── templates/             # 50+ templates (constitutions, docs, agents, memory)
├── tests/                 # 50+ test files
└── utils/                 # flowspec-netlog utility
```

### File Statistics

| Category | Count |
|----------|-------|
| Total files | 500+ |
| Python SLOC (workflow module) | ~18,000 |
| Documentation (markdown) | 150+ |
| Templates | 50+ |
| Test files | 50+ |
| Configuration files | 8 major |
| Slash commands | 22 |
| Skills (internal) | 20 |
| Agent personas | 15 |

---

## 2. Source Inventory

### Overview

| File | Purpose |
|------|---------|
| `README.md` | Framework overview, quickstart, feature matrix |
| `CLAUDE.md` | Claude Code integration guide (rules, workflows, agents) |
| `memory/constitution.md` (55K) | Comprehensive project governance — tiers, rigor, standards |
| `memory/WORKFLOW_DESIGN_SPEC.md` | Workflow execution specification |
| `build-docs/adr/` (60+ files) | Architecture Decision Records |
| `build-docs/platform/` | Platform engineering docs |
| `.stacks/*/README.md` | Stack-specific guidance |

### Execution

| File | Purpose |
|------|---------|
| `.claude/commands/flow/*.md` (22 files) | Slash command definitions for each workflow phase |
| `.claude/skills/*/SKILL.md` (20 dirs) | Internal skill definitions |
| `src/flowspec_cli/workflow/orchestrator.py` | Custom workflow execution engine |
| `src/flowspec_cli/workflow/executor.py` | Agent-context workflow step runner |
| `src/flowspec_cli/workflow/transition.py` | Artifact-gated state transitions |
| `flowspec_workflow.yml` | State machine + workflow + agent definitions |

### Prompts

| File | Purpose |
|------|---------|
| `.agents/*.md` (15 files) | Specialized agent persona definitions |
| `.claude/agents/*.md` (5 files) | Claude Code dispatchable agent definitions |
| `.claude/agents-config.json` | Agent→workflow routing table |
| `.languages/*/agent-personas.md` | Language-specific expert guidance |
| `templates/agents/*.md` | Agent template files |

### Enforcement

| File | Purpose |
|------|---------|
| `.claude/settings.json` | Hook definitions, permission denials, preferences |
| `.claude/rules/critical.md` | Non-negotiable rules (test protection, DCO, pre-PR) |
| `.claude/rules/rigor.md` | 4-phase rigor enforcement (SETUP/EXEC/VALID/PR) |
| `.pre-commit-config.yaml` | Ruff lint + format hooks |
| `scripts/bash/pre-pr-check.sh` | Pre-PR validation (DCO + lint + format + tests) |
| `src/flowspec_cli/workflow/validator.py` (718 SLOC) | DAG validation, cycle detection, reachability |
| `src/flowspec_cli/hooks/runner.py` | Hook execution with timeout + env sanitization |
| `src/flowspec_cli/hooks/config.py` | Hook config validation (path traversal, metachar) |
| `schemas/flowspec-workflow-schema.json` | JSON Schema for workflow config |

### Evolution

| File | Purpose |
|------|---------|
| `tests/` (50+ files) | pytest suite covering workflow, memory, security |
| `CHANGELOG.md` | Version history |
| `build-docs/adr/decision-tracker.md` | Decision log |
| `.github/` | CI/CD workflows |
| `memory/learnings/` | Accumulated project learnings |
| `memory/decisions/` | Logged architectural decisions |

---

## 3. Object Model & Context Strategy

### First-Class Entities

#### 3.1 Workflow State (`flowspec_workflow.yml:1-52`)

```yaml
states:
  - name: "To Do"         # initial: true
  - name: "Assessed"
  - name: "Specified"
  - name: "Planned"
  - name: "In Implementation"
  - name: "Validated"
  - name: "Done"           # terminal: true
```

- **Definition**: `flowspec_workflow.yml` states array
- **Schema**: `schemas/flowspec-workflow-schema.json`
- **Lifecycle**: Created at init → transitions via workflow execution → terminal at Done
- **Validation**: `validator.py` ensures DAG (no cycles), all states reachable from initial, terminal states exist
- **Classification**: **Fact object** — represents current task progress

#### 3.2 Workflow (`flowspec_workflow.yml:54-180`)

```yaml
workflows:
  assess:
    command: "/flow:assess"
    agents: ["Workflow Assessor"]
    input_states: ["To Do"]
    output_state: "Assessed"
```

6 core workflows: assess, specify, plan, implement, validate, submit-n-watch-pr

- **Definition**: `flowspec_workflow.yml` workflows map
- **Required fields**: command, agents, input_states, output_state
- **Lifecycle**: Invoked by slash command → dispatches to agents → produces artifacts → transitions state
- **Classification**: **Fact object** — static workflow definition

#### 3.3 Transition (`transition.py:1-624`)

```python
WORKFLOW_TRANSITIONS = [
    TransitionSchema(name="assess", from_state="To Do", to_state="Assessed",
                     input_artifacts=[...], output_artifacts=[Artifact("assessment_report", ...)]),
    # ... 7 total transitions
]
```

- **Definition**: Hardcoded in `transition.py` with artifact requirements
- **Artifacts**: Input/output artifact definitions with path patterns (`{feature}`, `{NNN}`)
- **Validation modes**: NONE, KEYWORD, PULL_REQUEST
- **Classification**: **Evidence object** — enforces artifact existence at transition boundaries

#### 3.4 Agent Persona (`.agents/*.md`, `.claude/agents-config.json`)

15 agent personas mapped to workflows:

| Agent | Loop | Workflows |
|-------|------|-----------|
| Software Architect | outer | plan |
| Platform Engineer | outer | plan |
| PM Planner | outer | specify |
| Frontend/Backend/AI-ML Engineer | inner | implement |
| Frontend/Backend Code Reviewer | inner | implement |
| Quality Guardian | outer | validate |
| Secure-by-Design Engineer | outer | validate |
| Tech Writer | outer | validate |
| Release Manager | outer | validate |
| SRE Agent | outer | operate |

- **Definition**: Markdown files in `.agents/` with expertise, methodology, output formats
- **Routing**: `agents-config.json` maps agent name → workflow list
- **Classification**: **Fact object** — static persona definitions

#### 3.5 Task Memory (`src/flowspec_cli/memory/store.py`)

```
backlog/memory/task-XXX.md  (active)
backlog/memory/archive/task-XXX.md  (archived)
```

- **Definition**: Markdown files with YAML frontmatter
- **Lifecycle**: Created on `To Do → In Progress` → updated during work → archived on `→ Done` → deleted on `→ Archive`
- **Required content**: What, Why, Constraints, AC Status, Key Decisions (≤500 words)
- **Token-aware**: Injector (`injector.py`) truncates to ~2000 tokens, preserving recent context
- **Classification**: **Judgment object** — records decisions and progress

#### 3.6 Constitution (`memory/constitution.md`, `templates/constitutions/`)

3 tiers: Light / Medium / Heavy — project governance principles

- **Definition**: Generated at `/flow:init` based on complexity scoring
- **Content**: Core principles, coding standards, quality gates, workflow rules
- **Lifecycle**: Created once → referenced throughout all workflows → updated via `/flow:reset`
- **Classification**: **Fact object** — project-level governance

#### 3.7 Rigor Rules (`.claude/rules/rigor.md`)

4 phases × N rules with enforcement modes (strict/warn/off):

| Phase | Rules |
|-------|-------|
| SETUP | SETUP-001 (clear plan), SETUP-002 (deps), SETUP-003 (testable ACs) |
| EXEC | EXEC-001 (worktree), EXEC-002 (branch naming), EXEC-003 (decision log), EXEC-004 (backlog link), EXEC-006 (state tracking) |
| VALID | VALID-002 (lint/SAST), VALID-004 (no conflicts), VALID-005 (ACs met), VALID-007 (local CI) |
| PR | PR-001 (DCO sign-off) |

- **Classification**: **Fact object** — but enforcement varies (see Phase 4)

### Context Flow Strategy

```
                    ┌─────────────────────────┐
                    │   constitution.md        │ ← Project-level (created at init)
                    │   (Light/Medium/Heavy)   │
                    └──────────┬──────────────┘
                               │ inherits
                    ┌──────────▼──────────────┐
                    │   .claude/rules/*.md     │ ← Session-level (auto-loaded)
                    │   (8 rule files)         │
                    └──────────┬──────────────┘
                               │ scopes
                    ┌──────────▼──────────────┐
                    │   task memory            │ ← Task-level (per task-XXX.md)
                    │   (≤500 words, ≤2K tok)  │
                    └──────────┬──────────────┘
                               │ injected via
                    ┌──────────▼──────────────┐
                    │   CLAUDE.md @import      │ ← Active context injection
                    │   (backlog/CLAUDE.md)    │
                    └──────────────────────────┘
```

**Context isolation**: Agent personas receive only their domain-relevant context. Security reviewer is **read-only** — reports findings, cannot modify code (`.claude/rules/agents.md`).

**Context compression**: Token-aware truncation (`injector.py`) preserves recent context + key decisions, trims oldest notes first. Hard limit at ~2000 tokens per task memory.

**Persistence**: Constitution and rules persist in files. Task memory persists in `backlog/memory/`. Decisions logged to `.flowspec/logs/decisions/`. Events logged to `.flowspec/logs/events/`.

---

## 4. Flow & State Machine

### Happy Path

```
User Request
    │
    ▼
/flow:init ──────────► constitution.md created
    │                   (complexity scoring → tier selection)
    ▼
/flow:assess ────────► docs/assess/{feature}-assessment.md
    │                   (scores: effort, components, integration, risk)
    │                   (recommendation: Full SDD / Spec-Light / Skip)
    ▼
/flow:specify ───────► docs/prd/{feature}-prd.md
    │                   (10-section PRD via PM Planner agent)
    │                   (creates backlog tasks via CLI)
    ▼
/flow:plan ──────────► docs/adr/ + docs/platform/
    │                   (parallel: Architect + Platform Engineer)
    │                   (ADRs, infrastructure design, DevSecOps)
    ▼
/flow:implement ─────► source code + tests
    │                   (parallel: Frontend + Backend + AI engineers)
    │                   (code review by dedicated reviewers)
    │                   (pre-PR validation: lint + format + tests)
    ▼
/flow:validate ──────► QA report + security report + docs
    │                   (parallel: QA + Security + Tech Writer + Release Mgr)
    │                   (4-stage parallel issue collection → batch report)
    ▼
/flow:submit-n-watch-pr ► PR created, CI monitored
    │
    ▼
  Done
```

**State transitions** (`flowspec_workflow.yml:182-260`):

| Transition | From | To | Required Artifacts |
|------------|------|----|--------------------|
| assess | To Do | Assessed | → assessment_report |
| specify | Assessed | Specified | assessment_report → prd |
| plan | Specified | Planned | prd → adr |
| implement | Planned | In Implementation | adr → source_code |
| validate | In Implementation | Validated | source_code → qa_report |
| operate | Validated | Done | qa_report → (none) |
| complete | Done | Done | (terminal) |

### Failure Path 1: Rigor Rule Violation

```
/flow:implement
    │
    ├─ EXEC-001 check: not in worktree?
    │   └─ rigor.md prescribes: create worktree first
    │      (Soft enforcement — prompt instruction, no code gate)
    │
    ├─ EXEC-002 check: branch naming wrong?
    │   └─ rigor.md prescribes: rename branch
    │      (Soft enforcement — prompt instruction only)
    │
    └─ Pre-PR check fails (lint/format/tests)
        └─ pre-pr-check.sh returns exit code 1
           (Hard enforcement — script blocks PR creation)
```

### Failure Path 2: Spec Quality Gate Failure

```
/flow:specify
    │
    ├─ /flow:gate runs spec quality scoring
    │   └─ Score < 70/100?
    │       ├─ exit code 1 (failure)
    │       ├─ Provides improvement suggestions
    │       └─ User must improve spec and re-run
    │          (Hard enforcement — CLI exit code)
    │
    └─ --force flag available to bypass
        (Soft escape hatch — documented as "not recommended")
```

### Parallelism Model

| Phase | Parallel Agents | Sequential Dependencies |
|-------|-----------------|------------------------|
| plan | Architect ∥ Platform Engineer | Both complete before implement |
| implement | Frontend ∥ Backend ∥ AI-ML | All complete before validate |
| validate | QA ∥ Security ∥ Tech Writer ∥ Release Mgr | All complete before PR |

Parallel execution coordinated via `backlog task edit <id> -l "parallel-work:frontend,backend"` labels (`.claude/rules/agents.md`).

### Custom Workflows (`flowspec_workflow.yml:262-340`)

3 predefined custom sequences:

| Name | Steps | Description |
|------|-------|-------------|
| `quick_build` | assess → implement | Skip specify/plan for small tasks |
| `full_design` | assess → specify → plan | Full design, stop before implement |
| `ship_it` | assess → specify → plan → implement → validate | End-to-end |

Custom workflows support: conditions (`complexity >= 7`), checkpoints (pause for approval in "spec-ing" mode), and rigor enforcement per step.

---

## 5. Enforcement Audit

### Enforcement Matrix

| # | Constraint | Declared In | Enforcement Level | Mechanism | Evidence |
|---|-----------|-------------|-------------------|-----------|----------|
| E1 | Never delete tests | `rules/critical.md` | **Soft** | Prompt instruction only | No hook or pre-commit check prevents test deletion. Rule cites PR #545 as cautionary tale but no code enforces it. |
| E2 | Pre-PR validation (lint+format+tests) | `rules/critical.md`, `scripts/bash/pre-pr-check.sh` | **Hard** (partial) | Script checks 4 items; Claude hooks run auto-format on PostToolUse | `pre-pr-check.sh` returns exit code 1 on failure. But no git hook forces running it — agent must voluntarily invoke. |
| E3 | No direct commits to main | `rules/git-workflow.md`, `rules/critical.md` | **Soft** | Prompt instruction only | No branch protection hook in `.claude/settings.json`. Relies on GitHub branch protection (external). |
| E4 | DCO sign-off | `rules/critical.md`, `rules/git-workflow.md` | **Hard** (partial) | `pre-pr-check.sh` checks DCO; `settings.json` PreToolUse hook for git safety | Script checks sign-off. But no pre-commit hook forces `-s` flag. |
| E5 | Ruff lint/format | `.pre-commit-config.yaml`, `settings.json` PostToolUse hook | **Hard** | Pre-commit hook runs ruff on staged files; PostToolUse auto-formats Python | `pre-commit-config.yaml:3-11` configures ruff v0.8.2. `settings.json` PostToolUse hook runs auto-format. |
| E6 | Workflow state DAG (no cycles) | `validator.py:400-520` | **Hard** | Code: DFS cycle detection + BFS reachability analysis | `validator.py` raises ValidationError on cycles. Runs on config load. |
| E7 | Artifact-gated transitions | `transition.py:1-624` | **Hard** | Code: TransitionSchema requires input/output artifacts | `transition.py` WORKFLOW_TRANSITIONS defines required artifacts per transition. |
| E8 | Task memory ≤500 words | `rules/critical.md`, `memory/constitution.md` | **Soft** | Prompt instruction. Injector truncates at ~2000 tokens but doesn't enforce 500-word limit at write time. | `injector.py` truncates on read. No write-time validation. |
| E9 | Git worktree for implementation | `rules/rigor.md` EXEC-001 | **Soft** | Prompt instruction only | No hook checks for worktree presence before allowing code changes. |
| E10 | Branch naming convention | `rules/rigor.md` EXEC-002, `rules/git-workflow.md` | **Soft** | Prompt instruction only | No validation script checks branch name format. |
| E11 | Hook timeout enforcement | `hooks/runner.py` | **Hard** | Code: SIGTERM → SIGKILL with configurable timeout (max 10 min) | `runner.py` implements hard timeout with signal-based kill. |
| E12 | Hook script path restriction | `hooks/config.py` | **Hard** | Code: Blocks `..` and absolute paths in script paths; validates env vars for metacharacters | `config.py` raises HooksSecurityError on path traversal or shell metacharacters. |
| E13 | Sensitive file access denial | `settings.json` deny list | **Hard** | Claude Code permission system denies reads of secrets, constitution, lock files | `settings.json` deny rules for `Read(secrets/*)`, `Read(memory/constitution.md)`, etc. |
| E14 | Security reviewer read-only | `rules/agents.md` | **Soft** | Prompt instruction: "reports findings only, implementation agents address them" | No code prevents security-reviewer agent from writing files. |
| E15 | Backlog.md edit via CLI only | `rules/critical.md` | **Soft** | Prompt instruction: "Never edit backlog.md directly — use CLI commands only" | No file-write hook blocks direct backlog.md edits. |
| E16 | >80% test coverage | `rules/testing.md` | **Soft** | Prompt instruction. No coverage gate in pre-commit or pre-PR script. | `pre-pr-check.sh` runs pytest but doesn't check coverage percentage. |

### Enforcement Summary

| Level | Count | Percentage |
|-------|-------|-----------|
| Hard | 6 (E2 partial, E4 partial, E5, E6, E7, E11, E12, E13) | ~50% |
| Soft | 8 (E1, E3, E8, E9, E10, E14, E15, E16) | ~50% |
| Unenforced | 0 | 0% |

### Gap Analysis

**Critical gaps**:

1. **Test deletion protection (E1)**: Despite being called "non-negotiable", nothing prevents `rm tests/*.py`. The PR #545 incident is cited but no hook was added afterward. **Severity: High** — the very thing the rule was created to prevent can still happen.

2. **Pre-PR script voluntary (E2)**: The script exists but must be manually invoked. No git pre-push hook or CI gate ensures it runs. **Severity: Medium** — Claude hooks partially mitigate this by auto-formatting.

3. **Coverage target unverified (E16)**: 80% target stated but never checked by any script. **Severity: Low** — aspirational, not blocking.

4. **Backlog.md direct edit (E15)**: Critical rule with zero enforcement mechanism. **Severity: Medium** — could corrupt task state.

---

## 6. Prompt Catalog

### 6.1 Key Prompts

#### P1: Software Architect Enhanced

| Field | Value |
|-------|-------|
| **role** | Architecture planner |
| **repo_path** | `.agents/software-architect-enhanced.md` |
| **quote_excerpt** | "Uses Gregor Hohpe's principles (Software Architect Elevator, Enterprise Integration Patterns, Cloud Strategy, Platform Strategy)" |
| **stage** | plan |
| **design_intent** | Ground architecture decisions in established enterprise patterns (Hohpe framework) rather than ad hoc reasoning |
| **hidden_assumption** | Agent is familiar with Hohpe's books and can apply EIP terminology correctly |
| **likely_failure_mode** | Over-engineering for small projects; EIP patterns are enterprise-scale and may not fit simple apps |

#### P2: Quality Guardian

| Field | Value |
|-------|-------|
| **role** | Constructive skeptic / QA reviewer |
| **repo_path** | `.agents/quality-guardian.md` |
| **quote_excerpt** | "Three-Layer Critique: Acknowledge Value → Identify Risk → Suggest Mitigation" |
| **stage** | validate |
| **design_intent** | Prevent "rubber stamp" reviews by structuring critique as value-then-risk |
| **hidden_assumption** | Agent will follow three-layer structure rather than defaulting to surface-level approval |
| **likely_failure_mode** | AI agents tend toward agreement; the "Acknowledge Value" step may dominate, weakening the risk identification |

#### P3: PM Planner (via `/flow:specify`)

| Field | Value |
|-------|-------|
| **role** | Product requirements creator |
| **repo_path** | `.claude/commands/flow/specify.md` |
| **quote_excerpt** | "10 sections: Executive Summary, User Stories, DVF+V Risk Assessment, Functional Requirements, Non-Functional Requirements, Task Breakdown, Discovery/Validation Plan, Acceptance Criteria/Testing, Dependencies/Constraints, Success Metrics" |
| **stage** | specify |
| **design_intent** | Force comprehensive requirements thinking before implementation via structured PRD template |
| **hidden_assumption** | PRD sections will be filled with genuine product insight, not boilerplate |
| **likely_failure_mode** | AI may generate plausible-sounding but generic content for sections like "Success Metrics" without real product knowledge |

#### P4: Assess Command

| Field | Value |
|-------|-------|
| **role** | Complexity/risk evaluator |
| **repo_path** | `.claude/commands/flow/assess.md` |
| **quote_excerpt** | "Scores each dimension 1-10. Full SDD if any score ≥7 or total ≥18, Spec-Light if any ≥4 or total ≥10, else Skip SDD" |
| **stage** | assess |
| **design_intent** | Adaptive workflow — skip ceremony for simple tasks, enforce full process for complex ones |
| **hidden_assumption** | 1-10 scoring by an AI agent produces meaningful, calibrated results |
| **likely_failure_mode** | Score inflation (AI defaults to moderate-high scores) or inconsistent calibration across sessions |

#### P5: Secure-by-Design Engineer

| Field | Value |
|-------|-------|
| **role** | Security reviewer |
| **repo_path** | `.agents/secure-by-design-engineer.md` |
| **quote_excerpt** | "Risk Assessment → Apply Security-First Principles → Comprehensive Reviews (threat modeling, architecture, code, config, access control, data flow, dependencies, monitoring)" |
| **stage** | validate |
| **design_intent** | Bake security into every review cycle, not bolt-on afterward |
| **hidden_assumption** | AI agent can perform meaningful threat modeling with project context alone |
| **likely_failure_mode** | Generic security advice that doesn't account for actual deployment environment or threat model |

#### P6: Workflow Executor Skill

| Field | Value |
|-------|-------|
| **role** | Automated workflow step invoker |
| **repo_path** | `.claude/skills/workflow-executor/SKILL.md` |
| **quote_excerpt** | "Load config → Get execution plan → Invoke each command → Update backlog via MCP" |
| **stage** | Any (meta-orchestrator) |
| **design_intent** | Enable autonomous multi-step workflow execution without manual command invocation |
| **hidden_assumption** | MCP backlog server is running and accessible; Skill tool available in agent context |
| **likely_failure_mode** | MCP connection failure mid-workflow leaves state inconsistent; no rollback mechanism |

### 6.2 Design Highlights — Micro

#### M1: Complexity-Adaptive Workflow Selection

**Observation**: `/flow:assess` scores tasks on 8 dimensions (effort, components, integration, risk, security, compliance, data sensitivity, architecture impact) and routes to different ceremony levels.

**Evidence**: `commands/flow/assess.md` — "Full SDD if any score ≥7 or total ≥18, Spec-Light if any ≥4 or total ≥10, else Skip SDD"

**Why it matters**: Prevents over-engineering small tasks while ensuring complex tasks get proper specification. The three-tier system (Full/Light/Skip) is the framework's core value proposition.

**Transferability**: **Direct** — Complexity scoring → workflow tier selection is a clean, portable pattern. The specific thresholds (≥7/≥18/≥4/≥10) need calibration per project.

#### M2: Artifact-Gated State Transitions

**Observation**: Each state transition requires specific input artifacts and produces output artifacts. Transitions are validated by code (`transition.py` TransitionSchema).

**Evidence**: `transition.py:WORKFLOW_TRANSITIONS` — 7 transitions with Artifact objects specifying path patterns like `docs/assess/{feature}-assessment.md`

**Why it matters**: Prevents "empty" transitions where state advances without actual work products. This is a hard enforcement of "show your work."

**Transferability**: **Inspired** — The artifact concept is good but tightly coupled to flowspec's file path conventions. Would need redesign for different directory structures.

#### M3: Inner/Outer Loop Agent Classification

**Observation**: Agents are classified as "inner loop" (fast iteration: engineers, reviewers) vs "outer loop" (governance: architects, planners, QA).

**Evidence**: `flowspec_workflow.yml:340-380` — `agent_loops: { inner: [frontend-engineer, backend-engineer, ...], outer: [software-architect, platform-engineer, ...] }`

**Why it matters**: Separates velocity concerns from governance concerns. Inner loop agents don't make architectural decisions; outer loop agents don't write implementation code.

**Transferability**: **Direct** — Clean conceptual separation applicable to any multi-agent workflow.

#### M4: Token-Aware Memory Injection

**Observation**: Task memory is truncated to ~2000 tokens before injection into agent context. Truncation preserves recent context and key decisions, trims oldest notes first.

**Evidence**: `src/flowspec_cli/memory/injector.py` — `truncate_memory_content()` with section-aware truncation strategy

**Why it matters**: Prevents context window bloat while maintaining decision continuity across sessions.

**Transferability**: **Direct** — Token-aware truncation with priority sections is a universally applicable pattern.

#### M5: Three-Layer Critique Pattern

**Observation**: Quality Guardian uses structured critique: Acknowledge Value → Identify Risk → Suggest Mitigation.

**Evidence**: `.agents/quality-guardian.md` — "Three-Layer Critique framework"

**Why it matters**: Counteracts AI tendency toward agreement bias. By mandating "identify risk" as a middle step (not first), reviews feel constructive rather than adversarial.

**Transferability**: **Direct** — Can be used in any code review prompt.

#### M6: Constitution Tier System

**Observation**: Project governance scales with complexity: Light (minimal rules), Medium (standard), Heavy (full ceremony).

**Evidence**: `templates/constitutions/` — three separate template files; `/flow:init` auto-selects based on complexity score

**Why it matters**: One-size-fits-all governance fails. A CLI tool doesn't need the same process as a distributed microservice.

**Transferability**: **Inspired** — The concept of tiered governance is excellent. The specific constitution templates are flowspec-specific.

### 6.3 Design Highlights — Macro

#### X1: Spec-Driven Development as Methodology

**Observation**: Flowspec's core thesis is that formal specifications (PRD → ADR → Implementation) improve AI-assisted development outcomes. This is not TDD or BDD but "spec-first" — write what you want before writing how to build it.

**Evidence**: README, `skills/sdd-methodology/SKILL.md`, constitution tiers all center on the assess→specify→plan→implement→validate pipeline

**Enforcement level**: **Soft** — The workflow is recommended and tracked, but nothing prevents `/flow:implement` without prior `/flow:specify`. State transitions are defined but custom workflows like `quick_build` skip steps.

**Why it matters**: Positions specification as the primary quality lever, not testing. Testing validates specs; specs define what to build.

#### X2: Process-as-Code (Partial)

**Observation**: Workflow state machine is defined in YAML (`flowspec_workflow.yml`) and validated by Python code (`validator.py`). Transitions have artifact requirements. Custom workflows are composable.

**Evidence**: `validator.py` (718 SLOC) runs DAG validation, cycle detection, reachability analysis. `orchestrator.py` (441 SLOC) executes custom workflow sequences.

**Enforcement level**: **Hard** for workflow config validity, **Soft** for actual workflow execution order.

**Why it matters**: The config is validated, but workflow execution relies on agents voluntarily invoking the right commands in order. There's no runtime orchestrator that blocks out-of-order execution.

#### X3: Evaluator Separation — Partial

**Observation**: Code reviewers are separate agents from implementers. Security reviewer is read-only. But review outcomes are not gated by code — they're prompt-enforced.

**Evidence**: `.claude/rules/agents.md` — "Security reviewer: read-only access, reports findings only" | `.claude/agents/security-reviewer.md` — separate agent file

**Enforcement level**: **Soft** — No code prevents security-reviewer from writing. No gate blocks merging if security review fails.

**Why it matters**: True evaluator separation requires the reviewer's output to gate progression. Here, review is advisory.

#### X4: Verification-Over-Self-Report — Mixed

**Observation**: Pre-PR script (`pre-pr-check.sh`) verifies lint/format/tests independently. But many rigor rules (worktree, branch naming, backlog linkage) trust agent self-reporting.

**Evidence**: `pre-pr-check.sh` hard-checks 4 items. `rigor.md` defines 12+ rules but most have no verification mechanism.

**Enforcement level**: 4 rules **Hard**, 8+ rules **Soft**

**Why it matters**: The framework has the right instinct (verify, don't trust) but applies it inconsistently. The hard-enforced items (lint, format, tests) are the easiest to automate; the harder-to-verify items (worktree usage, decision logging) remain trust-based.

#### X5: Human Approval Checkpoints

**Observation**: Custom workflows support "spec-ing" mode with checkpoints that pause for user approval. The assess command's `--mode` override flag gives humans control over workflow routing.

**Evidence**: `commands/flow/custom.md` — "supports checkpoints (spec-ing mode)"; `commands/flow/assess.md` — "`--mode full|light|skip` override"

**Why it matters**: Maintains human agency in an otherwise autonomous pipeline. Users can override AI complexity scores and pause at any step.

### 6.4 Cross-Cutting Interconnections

| Dimension | Analysis |
|-----------|----------|
| **Prompt ↔ Skill** | Commands (`.claude/commands/flow/`) invoke skills (`.claude/skills/`) via Skill tool. Skills don't chain directly — orchestrator sequences them. |
| **Gate ↔ Flow** | Quality gates sit between specify→plan (`/flow:gate` checks spec quality ≥70/100) and implement→validate (pre-PR checks). No gate between plan→implement. |
| **Review ↔ Test** | Reviews are agent-based (advisory). Tests gate via `pre-pr-check.sh` (hard). No automated review gate. |
| **Context ↔ Scope** | Three levels: constitution (project) → rules (session) → task memory (task). Token budget: ~2000 tokens per task. Rules auto-loaded. |
| **Error ↔ Recovery** | Hook failures are fail-safe (logged, don't crash workflow). Workflow failures require manual `/flow:reset`. No automatic retry. |

---

## 7. Failure Modes

### F1: Specification Theatre

**Symptom**: PRDs and ADRs are generated with plausible but generic content. Each section is filled but lacks genuine product insight.

**Evidence**: `/flow:specify` mandates 10 PRD sections including "Success Metrics" and "Discovery/Validation Plan". AI agents can generate structurally valid but substantively empty content for these sections.

**Root cause**: No quality gate validates semantic quality of specifications — only structural completeness. `/flow:gate` scores to 70/100 but scoring criteria are not visible in source.

**Impact**: False sense of readiness. Team proceeds to implementation with specs that look complete but don't constrain design space.

**Framework mitigation**: Constitution tiers (Light tier skips heavy spec sections). Override mode (`--mode skip`) lets users bypass.

**Migration implication**: If porting spec-driven workflow, must build semantic quality checks, not just structural ones.

### F2: Score Inflation in Assessment

**Symptom**: `/flow:assess` consistently routes tasks to Full SDD or Spec-Light because AI agents default to moderate-high scores on ambiguous dimensions.

**Evidence**: Assessment scoring uses 8 dimensions scored 1-10. Thresholds: any single ≥7 → Full SDD, any ≥4 → Spec-Light. With 8 dimensions, scoring even one at 4+ (which is below midpoint) triggers Spec-Light.

**Root cause**: Low threshold combined with AI tendency toward moderate scores. A task where every dimension scores 3 (low complexity) would total 24, well above the ≥10 threshold for Spec-Light. In practice, Skip SDD requires all dimensions below 4 AND total below 10.

**Impact**: The "Skip SDD" path is nearly unreachable through normal AI scoring, defeating the adaptive workflow purpose.

**Framework mitigation**: `--mode` override lets users force skip. But this defeats automatic adaptation.

**Migration implication**: Calibrate scoring thresholds based on actual task distribution, not theoretical ranges.

### F3: Soft Enforcement of Critical Rules

**Symptom**: Rules labeled "non-negotiable" (test deletion, backlog.md edits, worktree usage) are violated because enforcement is prompt-only.

**Evidence**: `rules/critical.md` states "Never delete tests — no exceptions except with explicit human approval" but no hook, pre-commit check, or file-write guard prevents `rm tests/*.py`. Similarly, "Never edit backlog.md directly" has no write-protection mechanism.

**Root cause**: Gap between rule declaration and enforcement implementation. The framework invested heavily in prompt-based rules but didn't close the loop with code-level gates for its most critical constraints.

**Impact**: In high-velocity or multi-agent scenarios, prompt instructions can be ignored or forgotten. The very rules that need the strongest enforcement have the weakest.

**Framework mitigation**: Constitution and rules are auto-loaded into every session. Claude Code hooks run on PreToolUse and PostToolUse. But hooks don't check for test deletion or direct backlog edits.

**Migration implication**: For critical rules, always build code-level enforcement (hooks, validators, CI gates) — prompt instructions are necessary but not sufficient.

### F4: MCP Dependency for State Management

**Symptom**: Workflow state updates fail when MCP backlog server is unavailable, leaving tasks in inconsistent state.

**Evidence**: `executor.py` updates backlog tasks via MCP. `.mcp.json` configures 9 MCP servers. If backlog MCP is down, task state diverges from actual work state.

**Root cause**: State management depends on an external service (MCP) rather than local file operations. No fallback or offline mode for state tracking.

**Impact**: Workflow breaks silently when MCP is unavailable. Agent continues working but state isn't tracked.

**Framework mitigation**: Backlog CLI provides local file operations as alternative (`backlog task edit`). But workflow executor specifically uses MCP.

**Migration implication**: State management should have local-first fallback. Don't depend on network services for core workflow state.

### F5: Context Loss Across Agent Handoffs

**Symptom**: When parallel agents (e.g., Frontend + Backend in implement phase) complete work, their individual contexts don't merge. Subsequent phases may miss inter-agent decisions.

**Evidence**: `rules/agents.md` describes parallel execution via labels. Each agent gets its own context. Task memory (≤500 words, ≤2000 tokens) is the only shared state.

**Root cause**: Token budget constraint (≤2000 tokens per task) limits what can be preserved across agent boundaries. Key decisions from one agent may not fit in shared memory.

**Impact**: Architectural decisions made by backend agent may conflict with frontend agent's assumptions. The validate phase may not see the full picture.

**Framework mitigation**: Decision logging to `.flowspec/logs/decisions/` provides audit trail. But this isn't injected into agent context automatically.

**Migration implication**: Multi-agent workflows need explicit decision aggregation between parallel phases, not just shared memory files.

---

## 8. Migration Assessment

### Candidates

| # | Mechanism | Transferability | Effort | Prerequisite | Risk |
|---|-----------|----------------|--------|-------------|------|
| M1 | Complexity-adaptive workflow routing | **Direct** | S | Scoring rubric definition | Score inflation without calibration |
| M2 | Artifact-gated state transitions | **Inspired** | M | Define artifact types and path conventions | Over-constraining for simple tasks |
| M3 | Inner/outer loop agent classification | **Direct** | S | Agent definition mechanism | Boundary violations in practice |
| M4 | Token-aware memory injection | **Direct** | M | Memory store + truncation algorithm | Losing critical context during truncation |
| M5 | Three-layer critique pattern | **Direct** | S | Review prompt template | AI still gravitating toward agreement |
| M6 | Constitution tier system | **Inspired** | L | Template system + init workflow | Tier selection accuracy |
| M7 | Pre-PR validation script | **Direct** | S | Linter + test runner configured | Voluntary invocation (not enforced) |
| M8 | Custom workflow composition | **Inspired** | L | Workflow engine + YAML schema | Complexity of orchestration code |
| M9 | Decision/event logging | **Direct** | S | Log directory + format convention | Log review discipline |
| M10 | Fail-safe hook execution | **Direct** | M | Hook runner with timeout + signal handling | Missing critical events if hooks fail silently |

### Recommended Adoption Order

1. **M5 Three-layer critique** (S, zero prereqs, immediate review quality improvement)
2. **M3 Inner/outer loop classification** (S, conceptual, improves agent design discipline)
3. **M7 Pre-PR validation script** (S, concrete, immediate quality gate)
4. **M9 Decision/event logging** (S, lightweight, improves auditability)
5. **M4 Token-aware memory injection** (M, requires memory infra, high long-term value)
6. **M1 Complexity-adaptive routing** (S conceptually, but needs calibration work)
7. **M2 Artifact-gated transitions** (M, requires artifact schema design)
8. **M10 Fail-safe hooks** (M, requires hook infrastructure)
9. **M6 Constitution tiers** (L, requires template system + init workflow)
10. **M8 Custom workflow composition** (L, requires workflow engine)

### Must-Build Enforcement

If porting flowspec patterns, these **code-level enforcement mechanisms** are required (flowspec itself lacks them):

| Mechanism | What It Protects | Implementation |
|-----------|-----------------|----------------|
| Test deletion guard | Prevent `rm tests/*` | PreToolUse hook checking file paths |
| Backlog write guard | Prevent direct edits to `backlog.md` | PreToolUse hook on Write/Edit tool |
| Coverage gate | Enforce >80% threshold | Post-test hook checking coverage output |
| Review gate | Block merge without review completion | CI check or pre-merge hook |
| Branch protection | Enforce no direct main commits | Git hook or GitHub branch protection |

---

## 9. Open Questions

1. **Spec quality scoring algorithm**: `/flow:gate` checks spec quality (target 70/100) but the scoring rubric is not visible in source. How are the 100 points distributed? Is it structural or semantic?

2. **Outer loop implementation**: README references "Promote/Observe/Operate/Feedback" outer loop but states it's "handled by falcondev." How does this integrate with the inner loop state machine?

3. **MCP backlog server implementation**: The backlog MCP server is referenced but its source isn't in the repository. Is it a separate package? What happens to workflow state if it's unavailable?

4. **Agent persona effectiveness**: Are the 15 specialized agent personas measurably better than a single well-prompted general agent? The framework assumes specialization improves quality but provides no evaluation data.

5. **Custom workflow adoption**: The 3 predefined custom workflows (quick_build, full_design, ship_it) — are they actually used in practice, or does everyone default to the standard sequence?

---

## Appendix: Source Traceability

| Claim | Source | Line/Section |
|-------|--------|-------------|
| 7 workflow states | `flowspec_workflow.yml` | states array (lines 1-52) |
| 6 core workflows | `flowspec_workflow.yml` | workflows map (lines 54-180) |
| DAG cycle detection | `validator.py` | lines 400-520 (DFS algorithm) |
| Artifact-gated transitions | `transition.py` | WORKFLOW_TRANSITIONS constant (lines 1-624) |
| 15 agent personas | `.agents/*.md` | 15 markdown files |
| Agent→workflow routing | `.claude/agents-config.json` | 13 agents × 6 workflows |
| 22 slash commands | `.claude/commands/flow/*.md` | 22 markdown files |
| 20 internal skills | `.claude/skills/*/SKILL.md` | 20 directories |
| 8 auto-loaded rules | `.claude/rules/*.md` | 8 markdown files |
| Pre-commit hooks | `.pre-commit-config.yaml` | ruff v0.8.2 lint + format |
| Pre-PR script | `scripts/bash/pre-pr-check.sh` | 4-item check (DCO, lint, format, tests) |
| Claude Code hooks | `.claude/settings.json` | SessionStart, PreToolUse, PostToolUse, Stop |
| Hook security (path traversal) | `hooks/config.py` | HooksSecurityError on `..` or absolute paths |
| Hook timeout enforcement | `hooks/runner.py` | SIGTERM → SIGKILL with configurable limit |
| Task memory truncation | `memory/injector.py` | ~2000 token limit, section-aware truncation |
| Task memory lifecycle | `memory/lifecycle.py` | State-driven create/archive/restore/delete |
| Constitution tiers | `templates/constitutions/` | light.md, medium.md, heavy.md |
| Token-aware context injection | `memory/injector.py` | @import directive in CLAUDE.md |
| Three-layer critique | `.agents/quality-guardian.md` | Acknowledge → Risk → Mitigate |
| Score inflation risk | `commands/flow/assess.md` | any ≥4 → Spec-Light, total ≥10 → Spec-Light |
| Test deletion non-enforcement | `.claude/rules/critical.md` + settings.json | Rule exists, no hook implements it |
| Security reviewer read-only claim | `.claude/rules/agents.md` | Prompt-only, no code enforcement |
