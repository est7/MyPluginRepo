# Workflow Research Report Template

Use this structure for the final output. Every section is mandatory unless marked optional.

---

```markdown
# Workflow Research: {Framework Name}

**Date**: {YYYY-MM-DD}
**Source**: {repo URL or local path}
**Analyst mode**: {Single | Comparison | Focused}
**Focus**: {All | gates | objects | flow | prompts}

---

## 1. Framework Profile

| Attribute | Value |
|-----------|-------|
| **Type** | {skill library / workflow harness / agent orchestrator / hybrid} |
| **Total files** | {N} |
| **Prompt files** | {N} (SKILL.md, commands, agents) |
| **Scripts/hooks** | {N} |
| **Test files** | {N} |
| **Entry points** | {list of config/manifest files} |
| **Registration mechanism** | {how skills/commands are discovered} |
| **Language** | {primary languages used} |

### Directory Map

{Annotated tree output — mark key files with their role}

---

## 2. Source Inventory

### Overview Sources
| File | Type | Why It Matters |
|------|------|---------------|
| {path} | README / docs / architecture | {role in research} |

### Execution Sources
| File | Type | Why It Matters |
|------|------|---------------|
| {path} | skill / command / runbook | {role in research} |

### Prompt Sources
| File | Type | Why It Matters |
|------|------|---------------|
| {path} | prompt / agent / template | {role in research} |

### Enforcement Sources
| File | Type | Why It Matters |
|------|------|---------------|
| {path} | hook / script / validator / CI | {role in research} |

### Evolution Evidence
| Source | Type | Why It Matters |
|--------|------|---------------|
| {path or issue/PR} | test / issue / release note | {what it reveals} |

---

## 3. Object Model

### First-Class Entities

| Entity | Definition Location | Required Fields | Lifecycle | Fact/Judgment/Evidence |
|--------|-------------------|-----------------|-----------|----------------------|
| {e.g., Spec} | {file:line} | {fields} | {create → review → approve} | {fact object} |

### Entity Relationships

{Text diagram showing dependencies, reference directions, cardinality}

### Context Isolation Strategy

| Scope | What Flows | Mechanism | Evidence |
|-------|-----------|-----------|----------|
| Controller → Implementer | {task spec, background} | {fresh subagent, injected context} | {file:line} |
| Controller → Reviewer | {code diff, spec} | {independent context} | {file:line} |
| Cross-task | {discoveries, state} | {ledger file / index} | {file:line} |

---

## 4. Flow & State Machine

### Happy Path

{Numbered steps with file:line citations}

1. {Step} — `{file}:{line}`
2. {Step} — `{file}:{line}`

### Phase Transitions

| From | To | Trigger | Gate? | Evidence |
|------|----|---------|-------|----------|
| {phase} | {phase} | {condition} | {yes/no} | {file:line} |

### Failure Paths

#### Failure Path 1: {description}
{Steps and behavior when this failure occurs}

#### Failure Path 2: {description}
{Steps and behavior when this failure occurs}

### Parallelism

| Parallel Unit | What Runs | Synchronization | Evidence |
|--------------|-----------|-----------------|----------|
| {e.g., subagent dispatch} | {tasks} | {join condition} | {file:line} |

---

## 5. Enforcement Audit

### Enforcement Matrix

| # | Constraint | Source | Level | Evidence | Gap? |
|---|-----------|--------|-------|----------|------|
| 1 | {constraint text} | {file:line} | {Hard/Soft/Unenforced} | {mechanism description} | {Yes/No} |

### Enforcement Statistics

| Level | Count | Percentage |
|-------|-------|------------|
| Hard-enforced | {N} | {%} |
| Soft-enforced | {N} | {%} |
| Unenforced | {N} | {%} |

### Critical Gaps

{List gaps with severity ≥ Moderate, with recommendations}

---

## 6. Prompt Catalog

### Prompt: {Role Name}

| Field | Value |
|-------|-------|
| **repo_path** | `{relative path}` |
| **quote_excerpt** | "{key sentence(s)}" |
| **stage** | {which workflow phase uses this} |
| **design_intent** | {what behavior it induces} |
| **hidden_assumption** | {what the prompt takes for granted} |
| **likely_failure_mode** | {how it can fail or be circumvented} |
| **evidence_level** | {direct / inferred} |

{Repeat for each major prompt: implementer, reviewer, planner, spec reviewer, quality reviewer, orchestrator, calibration/rubric}

---

## 7. Design Highlights — Micro

### Highlight: {Name}

- **Observation**: {what was found}
- **Evidence**: `{file:line}`
- **Why it matters**: {design value}
- **Trade-off**: {cost or limitation}
- **Transferability**: {Direct / Inspired / Non-transferable}

{Cover: command design, prompt structure, status protocol, report format, decomposition pattern, path conventions, reviewer calibration}

---

## 8. Design Highlights — Macro

### Philosophy: {Name}

- **Observation**: {the philosophical stance}
- **Where it appears**: `{file:line}` citations showing this philosophy in practice
- **How it shapes the workflow**: {structural consequences}
- **Strengths**: {benefits observed}
- **Limitations**: {where it breaks down}
- **Adopt?**: {Yes/Modify/No — with rationale}

{Cover: TDD/BDD/spec-first, evaluator separation, context isolation, process-as-code, human checkpoints, verification-over-self-report}

---

## 9. Failure Modes & Limitations

| # | Failure Mode | Trigger | Impact | Evidence |
|---|-------------|---------|--------|----------|
| 1 | {e.g., context overflow} | {when skill chain exceeds token limit} | {degraded output} | {file:line or inference} |

### Observed vs Claimed Behavior Divergences

| Claim | Source | Actual Behavior | Evidence | Evidence Level |
|-------|--------|----------------|----------|---------------|
| {what docs/prompts say} | {file:line} | {what actually happens} | {how verified} | {direct/inferred} |

---

## 10. Migration Assessment

### Candidates

| # | Mechanism | Rating | Effort | Prerequisite | Risk | Source |
|---|----------|--------|--------|-------------|------|--------|
| 1 | {name} | {Direct/Inspired/Non-transferable} | {S/M/L} | {what must exist first} | {naive porting risk} | {file:line} |

Rating definitions:
- **Direct**: Copy-adapt with minor changes
- **Inspired**: Core idea is transferable, but implementation must be redesigned
- **Non-transferable**: Too coupled to the original host platform

### Recommended Adoption Order

{Ordered by value/effort ratio}

1. {Mechanism} — {rationale}
2. {Mechanism} — {rationale}

### Non-Transferable (with reasons)

| Mechanism | Why Not | Alternative |
|----------|---------|-------------|
| {mechanism} | {coupling reason} | {what to do instead} |

### Must-Build Enforcement

{Mechanisms where the original framework has only prompt-level enforcement but YOUR workflow should hard-enforce}

| Mechanism | Original Level | Recommended Level | How to Enforce |
|----------|---------------|-------------------|---------------|
| {e.g., TDD} | Soft (prompt) | Hard (pre-commit hook) | {implementation sketch} |

---

## 11. Open Questions

{Questions that require deeper investigation or author consultation}

1. {Question} — relevant to {which migration candidate}
2. {Question}

---

## Appendix: Source Trace Table

| # | Source Type | Repo Path | Role | Excerpt | Evidence Level | Referenced In |
|---|-----------|-----------|------|---------|---------------|--------------|
| 1 | {skill/prompt/hook/issue} | {path} | {role in framework} | {short quote} | {direct/inferred} | {§ sections} |
```

---

## Usage Notes

- **Citations are mandatory**: Every row in every table must have a file:line or explicit "inferred from {evidence}" marker.
- **Evidence levels**: Mark every claim as `direct` (found in source file) or `inferred` (concluded from multiple sources). If inferred, list the `inference_basis`.
- **Do not fill sections with "N/A"**: If a section genuinely doesn't apply (e.g., no parallelism exists), write one sentence explaining why and move on.
- **Comparison mode**: When comparing two frameworks, duplicate sections 1-9 for each, then add a Section 9b "Comparative Analysis" before the migration assessment.
- **Focused mode**: When `--focus` is used, expand the relevant section with maximum depth and abbreviate others to summaries.
