# Failure Mode Checklist

Use this checklist during Phase 4 (Enforcement Audit) and Phase 6 (Migration Assessment). For each dimension, actively search for evidence — do not skip dimensions just because nothing is obvious.

## Structural Failure Modes

| # | Dimension | What to Look For |
|---|-----------|-----------------|
| 1 | **Enforcement gap** | Constraint claimed in docs/prompts but no code/hook/script prevents violation |
| 2 | **Reviewer bypass** | Controller can skip review steps; no mechanism forces review execution |
| 3 | **Fake verification** | System says "tests pass" but no RED→GREEN evidence captured; TDD is honor-system |
| 4 | **Token/context blowup** | Monolithic plan files, unbounded context inheritance, no token budget enforcement |
| 5 | **Context loss** | Fresh subagent loses cross-task discoveries; context compression drops critical state |
| 6 | **Unclear ownership** | Artifacts produced but no clear consumer; review verdicts that nobody reads |
| 7 | **Missing audit trail** | Decisions made but not persisted; no way to trace why a gate passed or failed |

## Methodological Failure Modes

| # | Dimension | What to Look For |
|---|-----------|-----------------|
| 8 | **Override hierarchy absent** | Framework defaults override project-level conventions; no clear priority chain |
| 9 | **Domain-review absence** | Generic quality review without domain-specific checks (security, perf, business logic) |
| 10 | **Host-platform coupling** | Mechanisms that only work on specific platforms (e.g., specific CLI, specific IDE) |
| 11 | **Stale assumptions** | Prompts reference APIs, libraries, or patterns that have changed since authoring |
| 12 | **Monolithic planning** | Plan as single document rather than task-sliced; expensive to re-read and update |

## Process Failure Modes

| # | Dimension | What to Look For |
|---|-----------|-----------------|
| 13 | **Self-report trust** | System trusts implementer's own status report instead of independent verification |
| 14 | **Missing research step** | Framework jumps to design/implementation without checking current state of external APIs/libs |
| 15 | **Context-unaware questioning** | System asks generic questions when project-specific context is already available |
| 16 | **Path hardcoding** | Output paths, file names, or directory structures baked into prompts rather than configurable |

## Per-Item Analysis Template

For each failure mode found:

```markdown
### FM-{N}: {Short Title}

- **Symptom**: What goes wrong from the user's perspective
- **Evidence**: `file:line` or issue/PR reference
- **Root cause**: Why the failure happens structurally
- **Impact**: Severity (Critical/Moderate/Low) + blast radius
- **Framework mitigation**: Does the framework already address this? How?
- **Migration implication**: If porting this mechanism, what must you add to prevent this failure?
```
