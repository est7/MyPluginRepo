# Enforcement Matrix Template

Use this matrix for Phase 4 output. Every constraint discovered in prompts, docs, or code must be classified.

## Enforcement Levels

| Level | Definition | Evidence Required |
|-------|-----------|-------------------|
| **Hard** | Code/hook/script prevents violation. Framework fails or blocks if constraint is violated. | Script path, hook type, exit code behavior |
| **Soft** | Prompt or doc instructs the behavior. No mechanism prevents violation. Agent compliance is voluntary. | Prompt file:line where instruction appears |
| **Unenforced** | Mentioned in README/docs but absent from both prompts and code. Pure aspiration. | Doc location; absence of any enforcement mechanism |

## Matrix Format

```markdown
| # | Constraint | Source | Enforcement | Evidence | Gap? |
|---|-----------|--------|-------------|----------|------|
| 1 | "Always run tests before commit" | CLAUDE.md:42 | Soft — prompt instruction only | No pre-commit hook found | YES |
| 2 | "Commit messages must be conventional" | hooks/pre-commit.sh | Hard — hook validates format | Exit 1 on regex mismatch | No |
| 3 | "Use TDD for all features" | README.md:15 | Unenforced — not in any prompt | Absent from SKILL.md files | YES |
```

## Gap Analysis Rules

A gap exists when:
- A constraint is claimed but enforcement level is Soft or Unenforced
- A Hard enforcement mechanism has bypass paths (e.g., `--no-verify` flag)
- Enforcement exists but is incomplete (e.g., validates format but not content)

For each gap, note:
1. **Severity**: Critical (safety/correctness) / Moderate (quality) / Low (style)
2. **Exploitability**: How easily an agent or user can violate the constraint
3. **Recommendation**: How to close the gap if porting to your system
