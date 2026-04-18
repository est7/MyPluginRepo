---
name: reverse-engineer-workflow
description: "Structural reverse-engineering of any agent workflow framework, harness, or skills repo. Extracts object models, state machines, enforcement mechanisms, and cross-cutting relationships — outputs traceable evidence with migration recommendations. Use when researching a workflow framework, analyzing an agent repo's architecture, comparing workflow systems, extracting transferable engineering patterns from external repos, or doing source-level research on how a framework actually enforces its claimed behavior."
---

# Workflow Research: Reverse-Engineer Workflow

Structured reverse-engineering of workflow frameworks. Not a summarizer — a research tool that distinguishes claims from enforcement and produces traceable, migration-ready analysis.

## Core Principle

Every conclusion must cite file-level evidence (`file` or `file:line` when available). Separate **declared behavior** (what prompts/docs say) from **enforced behavior** (what code/hooks/gates actually check). Flag gaps explicitly.

## Output Conventions

**Language (MANDATORY)**: Report prose in **Chinese** (简体中文). All code blocks, file paths, table headers, and technical terms remain in English. This is non-negotiable — an English report is a failed report.

**File naming**: `docs/research/workflow-research-{framework-name}.md`
- `{framework-name}` = repo directory name, kebab-case
- Comparison mode: `workflow-research-{name1}-vs-{name2}.md`

**Citation standard**: Cite as `file:line` when line numbers are available (direct reading). When summarizing from subagent research, `file` or `file (section)` is acceptable. Never cite without a file path.

**Template**: Use `references/output-template.md` for the full report structure.

## Input Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Single repo** | `<path>` | Full 7-phase analysis (Phase 0-6) |
| **Comparison** | `<path> --compare <path2>` | Phase 0-5 on each, then cross-compare |
| **Focused** | `<path> --focus <aspect>` | Deep-dive one dimension only |

If the target is a URL, clone it to a temporary directory first.

## Phase 0 — Research Scoping

Objective: Assess repo scale and choose research strategy.

1. Quick-scan: `find <path> -type f | wc -l` and directory listing
2. Classify repo size and choose strategy:

| Size | Files | Strategy |
|------|-------|----------|
| **Small** | <50 | **Fast path**: skip subagents, read files directly in main context. Merge Phase 1+2 into one pass. |
| **Medium** | 50-200 | Dispatch 3 parallel subagents for Phase 1 exploration. |
| **Large** | 200+ | Dispatch 3 parallel subagents. Partition by concern. |

3. Identify framework type from top-level files only (README, manifest, config).

**Subagent dispatch (Medium/Large only)**: Launch all three in a **single message** for concurrency:

- **`workflow-research:config-explorer`** — config, hooks, validators, enforcement
- **`workflow-research:prompt-explorer`** — skills, commands, agents, prompts
- **`workflow-research:docs-explorer`** — README, docs, version history, tests, claims

**Output**: Size classification, framework type hypothesis, research plan.

### Phase 0.5 — Subagent Output Triage (Medium/Large only)

After subagents return, validate before trusting:

1. **Check "Files Actually Read" section** — if missing or empty, the agent likely hallucinated. Discard its output.
2. **Spot-check file paths** — Glob 2-3 paths the agent claims to have read. If they don't exist, discard that agent's output.
3. **Identify coverage gaps** — which file categories (config, prompts, docs) have reliable data vs need manual reads.
4. **Fill gaps** — do targeted reads in main context for any category where subagent output is unreliable.

The triage step is essential — subagents may return plausible-looking but fabricated content. Trust only entries backed by verifiable file paths.

## Phase 1 — Reconnaissance & Source Inventory

Objective: Map the framework's surface area and classify all sources.

1. Read top-level README, CLAUDE.md, AGENTS.md, any manifest/config files
2. Map directory structure (Glob patterns)
3. Identify: entry points, config schemas, registration mechanisms
4. Count: total files, prompts, scripts, hooks, test files
5. Confirm or revise framework type: skill library / workflow harness / agent orchestrator / hybrid
6. Build **Source Inventory** — classify every key file as: Overview / Execution / Prompts / Enforcement / Evolution

Phase 1 stays at surface: what exists and where. Do NOT analyze internal logic yet.

**Stopping rule**: Stop collecting when you have: (a) all top-level config/manifest files, (b) all SKILL.md files, (c) hook scripts, (d) changelog skimmed. Do NOT read every reference file during reconnaissance — those are read on-demand in Phase 2-5.

**Output**: Framework Profile table + classified Source Inventory.

## Phase 2 — Object Model & Context Strategy

Objective: Identify first-class entities and context flow.

1. Scan config schemas for entity definitions (skills, commands, agents, hooks, gates, phases, roles)
2. For each entity: definition location, required fields, lifecycle
3. Map relationships: dependency direction, cardinality
4. Classify artifacts as **fact** / **judgment** / **evidence** objects
5. Identify context isolation strategy: what flows between controller ↔ worker ↔ reviewer, what's persisted vs in-memory

**Output**: Entity catalog + context flow diagram (text-based).

## Phase 3 — Flow & State Machine Analysis

Objective: Reconstruct the operational state machine.

1. Trace execution from user input to final output
2. Identify phases/stages and transitions — what triggers each?
3. Map branching: conditionals, fallbacks, error paths, retries
4. Document **happy path** + at least 2 **failure paths**
5. Identify parallelism vs sequential vs blocking gates

**Output**: State flow with file citations for each transition.

## Phase 4 — Enforcement Audit

Objective: Distinguish rhetoric from reality. The most critical phase.

For each claimed constraint: classify as **Hard** (code prevents) / **Soft** (prompt instructs) / **Unenforced** (docs only). Search for hooks, validators, scripts, CI checks. See `references/enforcement-matrix.md` for the template.

**Output**: Enforcement matrix with level + evidence for each constraint.

## Phase 5 — Prompt Catalog & Design Analysis

Objective: Catalog key prompts and analyze design patterns.

For each important prompt/agent/reviewer, record: role, repo_path, quote_excerpt, stage, design_intent, hidden_assumption, likely_failure_mode. See `references/output-template.md` §6 for the full field list.

Then identify **micro highlights** (concrete patterns: command design, state files, hook scripts) and **macro highlights** (philosophy: process-as-code vs process-as-prose, context isolation, evaluator separation). For each: observation → evidence → why it matters → transferability.

**Output**: Prompt catalog + micro/macro highlights.

## Phase 6 — Migration Assessment

For each significant mechanism: transferability (Direct/Inspired/Non-transferable), effort (S/M/L), prerequisite, risk, observed failure modes.

**Output**: Migration candidates table. Adoption order. Must-build enforcement list.

## Report Writing

Write using `references/output-template.md` structure. **All prose in Chinese.** Technical terms, code, file paths stay English.

For large reports (>3000 words): write skeleton + first 3 sections, then Edit to append remaining sections incrementally to prevent truncation.

## Pre-Submit Checklist

ALL 8 gates must pass. A report that fails any gate is incomplete.

| # | Gate |
|---|------|
| A | Source Inventory classified as overview / execution / prompt / enforcement / evolution |
| B | Every major role has prompt catalog entry with `repo_path` + `quote_excerpt` |
| C | At least 3 first-class entities with lifecycle |
| D | Phases with transitions, not a flat step list |
| E | Every key constraint classified as Hard / Soft / Unenforced |
| F | Both micro + macro design highlights present |
| G | At least 3 failure modes with evidence (not praise-only) |
| H | Migration candidates with ratings, adoption order, must-build enforcement |

See `references/quality-gates.md` for SHOULD gates.

## Comparison Mode

When `--compare` is used: run Phase 0-5 independently, then add Comparative Analysis (object model diff, enforcement ratio, flow complexity, context strategy, which mechanisms to adopt from each).

## Red Flags — Do NOT

- Summarize without file-level citations
- Treat README as the whole framework
- Quote prompts without repo_path
- Present "stated intent" as "actual behavior"
- Skip failure modes — mandatory
- **Write the report in English** — report prose must be Chinese

See `references/failure-mode-checklist.md` for required failure-mode search dimensions.
