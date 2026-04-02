# Vendor Evolution Rubric

A discovery-first framework for reading vendor updates. Use this after generating the raw evidence report.

## Core Principle

Read updates from **problem → mechanism → evidence → reuse value**, not from keyword matches. A good workflow innovation may live in a plain `.py` file with no "skill" or "agent" in its path.

## Per-Vendor: Four Mandatory Questions

For each vendor with non-trivial changes, answer these in order:

### 1. What problem is this update solving?

- What was broken, missing, or inefficient before this change?
- Look at commit messages, issue references, and the structure of new files for clues
- If the motivation is unclear from code alone, say so — don't invent one

### 2. What operation got systematized?

Identify what manual or implicit step became explicit, automated, or structured:
- New operation boundaries (what was previously ad-hoc is now a defined step)
- Automation loops (what previously required human intervention now runs end-to-end)
- Script I/O protocols (what a script reads, produces, and how it connects to other components)
- Routing/orchestration (how work gets dispatched to the right handler)
- Validation/rollback/feedback mechanisms (how the system catches errors or confirms success)

### 3. How does the core mechanism land in code?

Cite specific evidence:
- **At least 1-3 key files or scripts** per vendor — no conclusion without a file reference
- Read the actual code, not just the commit subject
- Note: entry points, config formats, data flow, and integration boundaries

### 4. What has migration value for `1st-cc-plugin`?

Categorize findings:
- **Port now**: concrete pattern or mechanism directly applicable
- **Watch**: interesting direction, needs another cycle to mature
- **Skip**: conflicts with current repo direction or adds no value

## Cross-Vendor: Structural Convergence

After analyzing each vendor individually, answer:

> **What identical structural changes appeared across multiple vendors?**

Examples: many repos moving from single-file prompts to multi-file skills, adding script-based validation gates, adopting hook-based automation.

## What to Prioritize

Focus attention on these signals (regardless of path naming):

1. **New operation boundaries** — something that was implicit is now a named, scoped step
2. **Automation closures** — a multi-step process that now runs without human intervention
3. **Script I/O protocols** — a script's inputs, outputs, and coordination interface
4. **Routing/dispatch patterns** — how work gets directed to the right component
5. **Validation/rollback/feedback** — how the system verifies success or recovers from failure
6. **Renames** — almost always signal conceptual reframing; always investigate

## Noise Filtering

Downgrade these unless they change actual behavior:
- Formatting-only changes (JSON whitespace, linter fixes)
- README copy-edits that don't change how users enter the system
- Pure version bumps with no structural change
- Dependency updates with no API change
- CI config churn unrelated to user-facing entry points

When marking something as noise, briefly explain **why** it's noise — "formatting only" is fine; don't just skip silently.

## Surface Changes (Auxiliary)

Path-based signals (skills/, commands/, hooks/, agents/, plugins/, SKILL.md, plugin.json) are useful as **quick-locate shortcuts** for finding workflow entry points. They are NOT a relevance gate:

- If a keyword path is hit → read it, it's likely relevant
- If no keyword path is hit → still analyze structural/code changes through the four questions above
- Never conclude "no workflow evolution" solely because no keyword paths matched

## Evidence Quality Checklist

Before finalizing each vendor section, verify:

- [ ] At least 1-3 specific file paths cited as evidence
- [ ] No conclusion drawn solely from commit subjects
- [ ] Noise explicitly identified with rationale
- [ ] Migration value stated as port/watch/skip with justification
- [ ] If the update is trivial, stated explicitly with evidence for why
