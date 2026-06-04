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

1. Get the COMPLETE changed-file set. **Do NOT rely on the compare API alone — it
   caps `files` at 300 and silently truncates** (a real sync can be 700+ files;
   the truncated tail also returns bogus `+0/-0` stats). Use recursive git trees
   and diff the blob SHAs:
   ```bash
   gh api "repos/est7/dotclaude/git/trees/main?recursive=1" --jq '.tree[]|select(.type=="blob")|[.path,.sha]|@tsv' > /tmp/est7.tsv
   gh api "repos/FradSer/dotclaude/git/trees/main?recursive=1" --jq '.tree[]|select(.type=="blob")|[.path,.sha]|@tsv' > /tmp/frad.tsv
   # verify .truncated == false for both, then diff: added (in frad not est7),
   # removed (in est7 not frad), modified (same path, different sha)
   ```
   The compare API is fine for a quick top-line summary
   (`--jq '{total_commits, ahead_by}'`) but never for the file list.

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
- `author` -> `{"name": "est7", "email": "t4here@gmail.com"}` (also per-plugin `LICENSE` copyright holder)
- `version` -> default: keep target's. On an explicit "全盘接受上游" (wholesale-accept) for a plugin, adopt upstream's version AND sync it into BOTH marketplace files (see Phase 6). Never leave plugin.json and marketplace versions out of sync.
- installation commands: `<name>@frad-dotclaude` -> `<name>@1st-cc-plugin` — use the TARGET plugin name (e.g. `project-init@1st-cc-plugin`, not the upstream `claude-config@...`)
- homepage URLs: `FradSer/dotclaude/tree/main/<plugin>` -> `est7/1st-cc-plugin/tree/main/<group>/<plugin>`
- flat example paths: the validator lives at `meta/plugin-optimizer/scripts/` (NOT `authoring/`)

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
5. **New plugins** — create structure, adapt content, register in BOTH marketplace files (see Phase 6)
6. **Deletions** — only after explicit user confirmation
7. **Documentation** — update `README.md`, `README.zh-CN.md`, `CLAUDE.md`, and BOTH `.claude-plugin/marketplace.json` AND `.agents/plugins/marketplace.json` (see Phase 6)

For each batch:
- edit files under `"$TARGET_REPO"`
- prefer `Edit` for existing files; for large/new plugins use the sparse-clone bulk-copy in `references/directory-mapping.md`
- validate each affected plugin (exit 0 = pass):
  ```bash
  python3 "$TARGET_REPO/meta/plugin-optimizer/scripts/validate-plugin.py" "$TARGET_REPO/<plugin-path>"
  ```
- **Registration gate:** a skill path must appear in EXACTLY ONE of `commands` (user-invocable slash command, frontmatter `user-invocable: true`) or `skills` (internal auto-load, `user-invocable: false`) — never both. Upstream sometimes dual-registers the same path; that is invalid here (CLAUDE.md contract) and will fail review. Pick one to match intent, and keep the SKILL.md `user-invocable` flag consistent with it.

## Phase 5: New Plugin Creation

When porting a new plugin from upstream:

1. Determine the target group (the repo's ACTUAL 7 groups):
   - version control -> `vcs/`
   - workflows -> `workflows/`
   - code quality -> `quality/`
   - integrations -> `integrations/`
   - platform-specific -> `platforms/`
   - plugin authoring / meta tooling -> `meta/`
   - CI/CD / delivery -> `cicd/`

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

## Phase 6: Update Documentation & Registries

Marketplace + docs sync discipline. Every version bump / add / delete touches
MULTIPLE files that must stay consistent.

**Two marketplace files (keep in lock-step):**
1. `$TARGET_REPO/.claude-plugin/marketplace.json` — Claude Code reads this (has `description`, `homepage`)
2. `$TARGET_REPO/.agents/plugins/marketplace.json` — Codex reads this (minimal: name/version/source/category)

A version lives in THREE places that must match: the plugin's `plugin.json`,
its `.claude-plugin/marketplace.json` entry, and its `.agents/plugins/marketplace.json`
entry. Bump all three together.

**Docs in `$TARGET_REPO`:**
3. `CLAUDE.md` — group table, commit-scope list, plugin COUNT ("contains N plugins"), and any hook/example references that point at a plugin you changed
4. `README.md` + `README.zh-CN.md` — per-plugin entry blocks AND the plugin COUNT line ("collection of N plugins"); keep EN/ZH in sync

**Parent repo `$REPO_ROOT/CLAUDE.md`** (MyPluginRepo, not the submodule):
5. has its own commit-scope list AND a "skill-porting SOP" table that references
   plugin paths/names — sync these when you add/rename/remove a plugin.

**Count math:** when adding N and removing M plugins, update the count by `+N-M`
in CLAUDE.md + both READMEs. Reconcile at the end:
```bash
# disk plugin.json count must equal marketplace entry count
find "$TARGET_REPO" -name plugin.json -path '*/.claude-plugin/*' | wc -l
python3 -c "import json;print(len(json.load(open('$TARGET_REPO/.claude-plugin/marketplace.json'))['plugins']))"
```
A mismatch means a registered plugin has no manifest (or vice-versa) — investigate.

**Preserving est7-unique validator checks:** the validator (`meta/plugin-optimizer/
scripts/validate-plugin.py`) is itself a sync target. If you wholesale-accept the
upstream one, it may DROP est7-added checks (e.g. `check_descriptions` / the CSO
description-length gate). After porting it, diff old-vs-new for est7-only
`check_*` functions and graft them back (they register via `CHECKS` dict +
`CHECK_ORDER` list). Then re-run the grafted validator across ALL synced plugins.

## Phase 7: Verification

1. Run validation on all modified plugins (exit 0 = pass):
   ```bash
   for p in <modified-plugin-paths>; do
     python3 "$TARGET_REPO/meta/plugin-optimizer/scripts/validate-plugin.py" "$TARGET_REPO/$p"
   done
   ```

2. Run the cross-cutting gates (all must be clean):
   ```bash
   # a. identity leakage — must be empty
   grep -rIl -e 'Frad LEE' -e 'fradser@' -e 'frad-dotclaude' -e 'FradSer/dotclaude' "$TARGET_REPO/<changed-paths>"
   # b. duplicate registration — same path in commands AND skills (must be empty)
   for pj in $(find "$TARGET_REPO" -name plugin.json -path '*/.claude-plugin/*'); do
     python3 -c "import json;d=json.load(open('$pj'));[print('DUP $pj',x) for x in set(d.get('commands',[]))&set(d.get('skills',[]))]"
   done
   # c. count reconciliation — disk plugin.json count == marketplace entries (see Phase 6)
   ```

3. Review the resulting diff:
   ```bash
   git -C "$TARGET_REPO" status --short
   git -C "$TARGET_REPO" diff --stat
   ```

4. Report back with:
   - plugins affected
   - files modified / created / deleted
   - validation + gate results
   - recommended next commit split

## References

- `references/directory-mapping.md` — path mapping between dotclaude and `1st-cc-plugin`
