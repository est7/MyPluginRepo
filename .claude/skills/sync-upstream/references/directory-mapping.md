# Directory Mapping: FradSer/dotclaude -> 1st-cc-plugin

Reflects the ACTUAL `1st-cc-plugin/` structure (verified, not aspirational).
The repo uses 7 groups: `vcs/`, `workflows/`, `quality/`, `integrations/`,
`platforms/`, `meta/`, `cicd/`. There is NO `version-control/`, `authoring/`,
or `delivery/` group — earlier versions of this doc were wrong about that.

## Plugin Path Mapping

| Upstream (flat) | 1st-cc-plugin (grouped) | Notes |
|-----------------|-------------------------|-------|
| `git/` | `vcs/git/` | |
| `gitflow/` | `vcs/gitflow/` | |
| `github/` | `vcs/github/` | |
| `superpowers/` | `workflows/superpowers/` | name stays plural — 40+ internal `superpowers:` cross-refs break if renamed |
| `refactor/` | `quality/refactor/` | skills renamed: `refactor`->`refactor-file`, `refactor-project`->`refactor-module` |
| `claude-config/` | `integrations/project-init/` | renamed plugin; keep `name: project-init` in plugin.json, install cmd `project-init@1st-cc-plugin` |
| `code-context/` | `integrations/code-context/` | est7 SUPERSET (added GitHub MCP + Google Dev Knowledge methods + 3 refs) — upstream changes usually regress it; sync with care |
| `acpx/` | `integrations/acpx/` | |
| `utils/` | `integrations/doc-tools/` | utils was renamed `doc-tools` and merged with office skills (see below) |
| `office/` | `integrations/doc-tools/` | office plugin DISSOLVED into `doc-tools`; its agent-browser/create-prd/patent-architect/tropes live under `doc-tools/skills/`; `lark` (huge vendored Lark API lib) NOT ported; `create-feishu-doc` deleted |
| `plugin-optimizer/` | `meta/plugin-optimizer/` | the validator lives here: `meta/plugin-optimizer/scripts/validate-plugin.py` |
| `swiftui/` | `platforms/swiftui/` | |
| `frontend/` | `platforms/frontend/` | absorbs shadcn + next-devtools-guide; contains impeccable-* design skills, react-best-practices, supabase |

### Plugins upstream REMOVED that we folded/dropped

| Upstream (removed) | Disposition in 1st-cc-plugin |
|--------------------|------------------------------|
| `shadcn/` | deleted as standalone `platforms/shadcn`; now a skill inside `platforms/frontend` |
| `next-devtools/` | deleted as standalone `platforms/next-devtools`; now `next-devtools-guide` skill inside `platforms/frontend` |
| `meeseeks-vetted/` | not present (already removed our side) |
| `office/skills/lark/` | intentionally NOT ported (+364-file vendored lib) |
| `office/skills/create-feishu-doc/` | deleted |

## Validate script path (IMPORTANT)

```bash
python3 1st-cc-plugin/meta/plugin-optimizer/scripts/validate-plugin.py <plugin-path>
```

NOT `authoring/...`. Exit 0 = pass, 1 = MUST violation, 2 = token budget critical.
The validator output says `PASSED  no issues` / `FAILED  N must, M should` (not `Result: PASSED`).

## Plugins only in 1st-cc-plugin (NEVER modify during sync)

These are est7-original (no upstream equivalent). Never touch unless the user
explicitly asks; they are NOT sync targets:

`workflows/`: issue-driven-dev, loaf, deep-plan, multi-collab, sc-loop, todo-sdd-workflow
`quality/`: agent-review, ai-hygiene, clarify, cli-design, gotcha, project-health, testing, workflow-research
`integrations/`: async-agent, catchup, enhance-prompt, jetbrains, local-context, orchestrator
`platforms/`: android, modern-android
`meta/`: skill-dev
`cicd/`: release
`vcs/`: git-worktree, git-worktree-submodule, jj-workflow
`integrations/doc-tools/skills/`: dialogue-rewriter, update-readme (est7-original skills inside the merged doc-tools plugin)

**Deletion rule:** "upstream removed it -> we drop it" applies ONLY to things that
were once shared and upstream later deleted (shadcn, next-devtools, meeseeks-vetted).
It does NOT mean "anything upstream lacks" — never delete est7-original plugins.

## Files to always skip (FradSer repo-level)

- `.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json` — we maintain our own
- `.git-agent/`, `.github/workflows/ci.yml`, `.gitignore`, `CHANGELOG.md`
- `README.md` / `README.zh-CN.md`, `CLAUDE.md` — diff for portable sections only, never overwrite
- `LICENSE` — adapt copyright holder to `est7` when porting a plugin's own LICENSE
- `docs/` — FradSer-internal plans/retros

## Content adaptation checklist

- [ ] Author: `Frad LEE` / `fradser@gmail.com` -> `est7` / `t4here@gmail.com` (plugin.json + README author line + per-plugin LICENSE copyright)
- [ ] Install: `<name>@frad-dotclaude` -> `<name>@1st-cc-plugin` (use the TARGET plugin name, e.g. `project-init@`, not `claude-config@`)
- [ ] URLs: `FradSer/dotclaude/tree/main/<plugin>` -> `est7/1st-cc-plugin/tree/main/<group>/<plugin>`; any `FradSer/dotclaude` -> `est7/1st-cc-plugin`
- [ ] Version: default keep target's; on explicit "全盘接受上游" adopt upstream's AND sync both marketplace files (see SKILL.md Phase 6)
- [ ] `displayName`: only present on synced plugins; do not invent for est7-only ones
- [ ] Vendored sync tooling (e.g. agent-browser `SYNC.md`, `scripts/sync-*.sh`): rewrite `office/...` / flat self-paths to the grouped target path

## Efficient bulk-copy for large/new plugins

For a big new plugin (frontend ~183 files, superpowers ~50), do NOT fetch file
by file. Sparse-clone once and `cp -r`, then sed-adapt identity across the tree:

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/FradSer/dotclaude /tmp/frad-clone
cd /tmp/frad-clone && git sparse-checkout set <plugin> [<plugin2> ...]
cp -r <plugin> "$TARGET_REPO/<group>/<plugin>"
# then sed: FradSer/dotclaude -> est7/1st-cc-plugin, @frad-dotclaude -> @1st-cc-plugin, Frad LEE -> est7, fradser@gmail.com -> t4here@gmail.com
```
