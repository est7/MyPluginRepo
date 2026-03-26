---
name: vendor-evolution-sop
description: "Refresh vendor reference repositories in MyPluginRepo and summarize how their skill surfaces and workflows evolved. Use when updating `vendor/*` submodules, reviewing the latest upstream changes, generating a per-vendor evolution report from submodule diffs, or deciding which external workflow ideas are worth porting into `1st-cc-plugin`."
user-invocable: true
argument-hint: "[vendor-name ...|all]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(git:*)
  - Bash(python3:*)
  - Agent
---

# Vendor Evolution SOP

Refresh `vendor/*` deliberately, then convert raw git diffs into a research report about workflow evolution.

The goal is not "update everything blindly". The goal is to answer:
- Which upstream workflow systems actually evolved?
- Which new skills, commands, hooks, agents, or plugin surfaces appeared?
- Which workflow ideas are converging across repos and are worth importing into `1st-cc-plugin`?

## Inputs

Accept either:
- `all`: update every clean vendor submodule
- One or more vendor names: update only `vendor/<name>`
- No argument: default to every clean vendor submodule

## Workflow

### Step 1: Snapshot the current vendor state

Capture the current parent-repo HEAD before touching submodules:

```bash
git rev-parse HEAD
git status --short
```

Do not mix unrelated local work into the vendor refresh commit.

If the parent repo already contains unrelated staged changes, keep them unstaged or restore them from the index before staging vendor updates.

### Step 2: Identify which vendor repos are safe to update

Enumerate vendor submodules from `.gitmodules`. For each candidate:
- Check `git -C vendor/<name> status --porcelain`
- If the submodule is dirty, inspect the changes
- If the changes are trivial cache or generated files, discard them explicitly
- If the changes are real local work, skip that vendor and report it

Prefer updating only clean submodules.

### Step 3: Pull the latest upstream commits

Update the selected clean vendors:

```bash
git submodule update --init --remote --recursive -- vendor/<name> ...
```

After update, stage only the vendor gitlink changes that belong to this refresh.

### Step 4: Generate the raw evolution report

Run the bundled report script against the root commit range that contains the vendor updates:

```bash
python3 .claude/skills/vendor-evolution-sop/scripts/vendor_evolution_report.py \
  --base <before-refresh-commit> \
  --head <after-refresh-commit-or-HEAD> \
  --write vendor/docs/<date>-vendor-evolution.md
```

If the refresh is still uncommitted, either:
- generate the report after making a dedicated vendor refresh commit, or
- stage only the vendor gitlink updates and compare against `HEAD`

The script extracts, per updated vendor:
- old and new submodule commits
- commit subjects between the two refs
- changed files
- workflow-signal files such as `skills/`, `commands/`, `agents/`, `hooks/`, `plugins/`, `workflows/`, `templates/`, `SKILL.md`, `plugin.json`, `marketplace.json`

### Step 5: Write the human summary

Read the generated report and summarize each updated vendor from the perspective of workflow evolution.

For each vendor, answer these questions:
- What new skill/plugin/command surface appeared?
- What existing workflow was renamed, reorganized, split, or simplified?
- Did the repo move toward stronger orchestration, stronger docs, stronger tooling, or stronger distribution?
- Which changes are just formatting or packaging noise and should be ignored?
- What is the actionable takeaway for `1st-cc-plugin`?

Use the rubric in `references/evolution-rubric.md`.

### Step 6: Update local vendor research docs

Keep the vendor research trail near the code:
- Write or update a dated report in `vendor/docs/`
- Update `vendor/docs/index.md` to point at the newest report

Do this whenever the refresh reveals non-trivial workflow evolution.

### Step 7: Commit cleanly

Use separate commits for separate intents:
- Vendor refresh commit: only `vendor/*` gitlink updates
- Vendor onboarding commit: new submodule + `.gitmodules` + `vendor/README.md`
- Research/doc commit: new SOP skill, scripts, and `vendor/docs/*`

Do not mix unrelated root docs or `1st-cc-plugin` work into the vendor refresh commit.

## Output Expectations

When using this skill, produce:
- The list of updated vendors
- The list of skipped vendors and why they were skipped
- A per-vendor evolution summary focused on skills and workflows
- A short cross-vendor synthesis: what patterns are emerging across the ecosystem
- Clear notes on which ideas are worth porting into `1st-cc-plugin`

## Quality Bar

Good output is selective.

Do:
- prioritize skills, commands, hooks, agents, workflow entry points, plugin packaging, and orchestration changes
- ignore pure version bumps and formatting churn unless they indicate a packaging or distribution shift
- call out renames because they often signal conceptual reframing
- compare the workflow shape before and after, not just the file list

Do not:
- dump raw commit logs without interpretation
- treat README-only churn as workflow evolution unless it changes how users enter the system
- mix new vendor onboarding work with routine vendor refresh analysis

## Resources

- `scripts/vendor_evolution_report.py`: generate structured markdown from vendor submodule diffs
- `references/evolution-rubric.md`: checklist for writing the human summary
