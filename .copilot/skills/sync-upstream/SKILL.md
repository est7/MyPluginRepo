---
name: sync-upstream
description: "Sync upstream changes from FradSer/dotclaude into `1st-cc-plugin/` from the MyPluginRepo root. Use when the user asks to sync upstream, update from FradSer, compare est7/dotclaude with FradSer/dotclaude, or selectively port upstream plugin changes into the local marketplace repo."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(gh:*)
  - Bash(git:*)
  - Bash(python3:*)
  - Bash(rm:*)
  - Bash(mkdir:*)
  - Bash(chmod:*)
  - Bash(base64:*)
  - Agent
---

# Upstream Sync: FradSer/dotclaude -> 1st-cc-plugin

Sync upstream changes from FradSer's dotclaude fork into the local `1st-cc-plugin/` marketplace repo, handling directory mapping, content adaptation, and selective porting.

## Context

This skill is for the **MyPluginRepo parent repository**, not the published marketplace itself.

- **Workspace root**: `MyPluginRepo/`
- **Target repo**: `MyPluginRepo/1st-cc-plugin/`
- **Upstream**: `FradSer/dotclaude` (`main`)
- **Origin fork**: `est7/dotclaude` (`main`)

At the start of execution, resolve:

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
TARGET_REPO="$REPO_ROOT/1st-cc-plugin"
```

All file edits, validation commands, and documentation updates must target `"$TARGET_REPO"`.

## Phase 1: Fetch and Analyze Diff

Compare the two upstream forks to identify all changes.

1. Fetch the compare diff:
   ```bash
   gh api repos/est7/dotclaude/compare/main...FradSer:main \
     --jq '.files | unique_by(.filename) | map({filename, status, additions, deletions, changes})'
   ```

2. Categorize each changed file into one of these buckets:
   - **Port** — content improvements to existing plugins
   - **New Plugin** — entirely new plugin directories
   - **Deletion** — plugins removed upstream; evaluate case-by-case
   - **Skip** — FradSer-specific repo files such as `CHANGELOG`, `README`, `CLAUDE.md`, `.git-agent`, author info

3. Present the categorized list to the user and explicitly call out:
   - what is safe to port directly
   - what requires adaptation
   - what should stay local-only

## Phase 2: Map Directories

Apply the directory mapping from flat dotclaude structure to the grouped `1st-cc-plugin/` structure.

See `references/directory-mapping.md` for the full mapping table.

For each file to port:
- resolve the logical plugin path inside `1st-cc-plugin/`
- convert it to an actual filesystem path under `"$TARGET_REPO"`
- if a mapped plugin does not exist yet, flag it for Phase 5

## Phase 3: Content Adaptation Rules

When porting content, apply these adaptations:

**Always change:**
- `author` -> `{"name": "est7", "email": "t4here@gmail.com"}`
- `version` -> keep the existing `1st-cc-plugin` version; do not adopt FradSer's version blindly
- installation commands: `@frad-dotclaude` -> `@1st-cc-plugin`
- homepage URLs: `FradSer/dotclaude/tree/main/<plugin>` -> `est7/1st-cc-plugin/tree/main/<group>/<plugin>`
- flat example paths: `plugin-optimizer/scripts/` -> `1st-cc-plugin/authoring/plugin-optimizer/scripts/` when showing executable paths from the parent repo

**Never change:**
- skill logic, workflow steps, and reference content unless the target repo already diverged intentionally
- existing `1st-cc-plugin`-only plugins such as `issue-driven-dev`, `testing`, `ai-hygiene`, `clarify`, `android`, `plan`, `catchup`

**Evaluate case-by-case:**
- cross-plugin agent references
- upstream deletions
- repo-level docs whose wording is marketplace-specific

## Phase 4: Execute Changes

Batch the work deliberately:

1. **Format fixes** — `allowed-tools` normalization, manifest field alignment, indentation
2. **Description improvements** — trigger phrase and discovery improvements
3. **plugin.json updates** — keywords, descriptions, metadata changes
4. **Skill content updates** — logic improvements, workflow changes, new sections
5. **New plugins** — create structure, adapt content, register in marketplace
6. **Deletions** — only after explicit user confirmation
7. **Documentation** — update `README.md`, `README.zh-CN.md`, `CLAUDE.md`, and `.claude-plugin/marketplace.json`

For each batch:
- edit files under `"$TARGET_REPO"`
- prefer `Edit` for existing files
- validate each affected plugin:
  ```bash
  python3 "$TARGET_REPO/authoring/plugin-optimizer/scripts/validate-plugin.py" "$TARGET_REPO/<plugin-path>"
  ```

## Phase 5: New Plugin Creation

When porting a new plugin from upstream:

1. Determine the target group:
   - version control -> `version-control/`
   - workflows -> `workflows/`
   - code quality -> `quality/`
   - integrations -> `integrations/`
   - platform-specific -> `platforms/`
   - plugin authoring -> `authoring/`
   - delivery -> `delivery/`

2. Create the target structure under `"$TARGET_REPO"`:
   ```bash
   mkdir -p "$TARGET_REPO/<group>/<plugin>/.claude-plugin"
   mkdir -p "$TARGET_REPO/<group>/<plugin>/skills/<skill-name>"
   ```

3. Fetch upstream content:
   ```bash
   gh api repos/FradSer/dotclaude/contents/<path> --jq '.content' | base64 -d
   ```

4. Adapt content per Phase 3.

5. If hook scripts reference shared libraries, verify whether those libraries exist upstream and whether the target repo needs corresponding files.

6. Make scripts executable:
   ```bash
   chmod +x "$TARGET_REPO/<script-path>"
   ```

## Phase 6: Update Documentation

After all changes are applied inside `1st-cc-plugin/`:

1. `.claude-plugin/marketplace.json`
2. `CLAUDE.md`
3. `README.md`
4. `README.zh-CN.md`

All four live under `"$TARGET_REPO"`.

## Phase 7: Verification

1. Run validation on all modified plugins:
   ```bash
   for p in <modified-plugin-paths>; do
     python3 "$TARGET_REPO/authoring/plugin-optimizer/scripts/validate-plugin.py" "$TARGET_REPO/$p"
   done
   ```

2. Review the resulting diff:
   ```bash
   git -C "$TARGET_REPO" status --short
   git -C "$TARGET_REPO" diff --stat
   ```

3. Report back with:
   - plugins affected
   - files modified / created / deleted
   - validation results
   - recommended next commit split

## References

- `references/directory-mapping.md` — path mapping between dotclaude and `1st-cc-plugin`
