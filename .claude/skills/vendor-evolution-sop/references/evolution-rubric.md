# Vendor Evolution Rubric

Use this rubric after generating the raw diff report.

## What to extract per vendor

### 1. Surface changes

Look for new or renamed:
- skills
- commands
- agents
- hooks
- plugins
- templates
- orchestration entry points

Useful path signals:
- `skills/`
- `commands/`
- `agents/`
- `hooks/`
- `plugins/`
- `workflows/`
- `templates/`
- `SKILL.md`
- `plugin.json`
- `marketplace.json`

### 2. Workflow evolution

Ask how the repo's operating model changed:
- More execution-oriented or more planning-oriented?
- More modular or more bundled?
- More automation or more documentation?
- More plugin-marketplace driven or more monolithic?
- More agent orchestration or more single-agent guidance?

### 3. Noise filtering

Usually downgrade these unless they change behavior:
- formatting-only JSON changes
- README copy edits
- dependency or version bumps with no workflow signal
- CI churn unrelated to user entry points

### 4. Porting value

For `1st-cc-plugin`, note:
- ideas worth porting directly
- ideas worth watching but not porting yet
- ideas that conflict with current repo direction

## Recommended summary template

```markdown
## <vendor-name>

- Surface: <new/renamed skills, commands, hooks, plugins>
- Evolution: <how the workflow model changed>
- Signal vs noise: <what mattered, what did not>
- Relevance: <what this means for 1st-cc-plugin>
```

## Cross-vendor synthesis

End the report with 3 concise sections:
- `Emerging Patterns`: repeated shifts across multiple vendor repos
- `Port Candidates`: concrete ideas to import into `1st-cc-plugin`
- `Watch List`: promising directions that need another update cycle before acting on them
