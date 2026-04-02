# Directory Mapping: est7/dotclaude -> 1st-cc-plugin

## Plugin Path Mapping

| est7/dotclaude (flat) | 1st-cc-plugin (grouped) | Notes |
|----------------------|------------------------|-------|
| `git/` | `version-control/git/` | |
| `gitflow/` | `version-control/gitflow/` | |
| `github/` | `version-control/github/` | |
| `superpowers/` | `workflows/superpower/` | Singular in 1st-cc-plugin |
| `refactor/` | `quality/refactor/` | |
| `claude-config/` | `integrations/project-init/` | Different plugin name |
| `office/` | `integrations/doc-gen/` | Different plugin name |
| `plugin-optimizer/` | `authoring/plugin-optimizer/` | |
| `next-devintegrations/` | `platforms/next-devintegrations/` | |
| `swiftui/` | `platforms/swiftui/` | |
| `code-context/` | `integrations/code-context/` | |
| `acpx/` | `authoring/acpx/` | |
| `shadcn/` | `platforms/shadcn/` | |
| `utils/` | `integrations/utils/` | |
| `meeseeks-vetted/` | `quality/meeseeks-vetted/` | |

## Skill Path Mapping (detailed)

One-to-one mapping of every skill between the two repos. Use this table
to locate the exact file when syncing a specific skill.

### version-control/git

| est7/dotclaude | 1st-cc-plugin |
|----------------|---------------|
| `git/skills/commit/` | `version-control/git/skills/commit/` |
| `git/skills/commit-and-push/` | `version-control/git/skills/commit-and-push/` |
| `git/skills/config-git/` | `version-control/git/skills/config-git/` |
| `git/skills/update-gitignore/` | `version-control/git/skills/update-gitignore/` |
| `git/scripts/validate-commit-pretool.sh` | `version-control/git/scripts/validate-commit-pretool.sh` |
| `git/hooks/hooks.json` | (inline in `version-control/git/.claude-plugin/plugin.json`) |

### version-control/gitflow

| est7/dotclaude | 1st-cc-plugin |
|----------------|---------------|
| `gitflow/skills/start-feature/` | `version-control/gitflow/skills/start-feature/` |
| `gitflow/skills/finish-feature/` | `version-control/gitflow/skills/finish-feature/` |
| `gitflow/skills/start-release/` | `version-control/gitflow/skills/start-release/` |
| `gitflow/skills/finish-release/` | `version-control/gitflow/skills/finish-release/` |
| `gitflow/skills/start-hotfix/` | `version-control/gitflow/skills/start-hotfix/` |
| `gitflow/skills/finish-hotfix/` | `version-control/gitflow/skills/finish-hotfix/` |
| `gitflow/references/invariants.md` | `version-control/gitflow/references/invariants.md` |
| `gitflow/references/changelog-generation.md` | `version-control/gitflow/references/changelog-generation.md` |

### version-control/github

| est7/dotclaude | 1st-cc-plugin |
|----------------|---------------|
| `github/skills/create-issues/` | `version-control/github/skills/create-issues/` |
| `github/skills/create-pr/` | `version-control/github/skills/create-pr/` |
| `github/skills/resolve-issues/` | `version-control/github/skills/resolve-issues/` |
| `github/skills/references/` | `version-control/github/skills/references/` |

### workflows/superpower (upstream: superpowers)

| est7/dotclaude | 1st-cc-plugin |
|----------------|---------------|
| `superpowers/skills/brainstorming/` | `workflows/superpower/skills/brainstorming/` |
| `superpowers/skills/writing-plans/` | `workflows/superpower/skills/writing-plans/` |
| `superpowers/skills/executing-plans/` | `workflows/superpower/skills/executing-plans/` |
| `superpowers/skills/systematic-debugging/` | `workflows/superpower/skills/systematic-debugging/` |
| `superpowers/skills/behavior-driven-development/` | `workflows/superpower/skills/behavior-driven-development/` |
| `superpowers/skills/agent-team-driven-development/` | `workflows/superpower/skills/agent-team-driven-development/` |
| `superpowers/skills/build-like-iphone-team/` | `workflows/superpower/skills/build-like-iphone-team/` |
| `superpowers/skills/references/` | `workflows/superpower/skills/references/` |
| `superpowers/hooks/stop-hook.sh` | (inline in `workflows/superpower/.claude-plugin/plugin.json`) |

### quality/refactor

| est7/dotclaude | 1st-cc-plugin | Notes |
|----------------|---------------|-------|
| `refactor/skills/refactor/` | `quality/refactor/skills/refactor-file/` | Renamed to clarify scope |
| `refactor/skills/refactor-project/` | `quality/refactor/skills/refactor-module/` | Renamed to clarify scope |
| `refactor/skills/best-practices/` | (no direct port — 1st-cc-plugin uses external rules) | Different approach |

### integrations/project-init (upstream: claude-config)

| est7/dotclaude | 1st-cc-plugin |
|----------------|---------------|
| `claude-config/skills/init-config/` | `integrations/project-init/skills/init-config/` |
| `claude-config/assets/` | `integrations/project-init/assets/` |
| `claude-config/scripts/render-claude-config.sh` | `integrations/project-init/scripts/render-claude-config.sh` |

### integrations/doc-gen (upstream: office)

| est7/dotclaude | 1st-cc-plugin |
|----------------|---------------|
| `office/skills/agent-browser/` | `integrations/doc-gen/skills/agent-browser/` |
| `office/skills/create-feishu-doc/` | `integrations/doc-gen/skills/create-feishu-doc/` |
| `office/skills/create-prd/` | `integrations/doc-gen/skills/create-prd/` |
| `office/skills/patent-architect/` | `integrations/doc-gen/skills/patent-architect/` |
| `office/lib/utils.sh` | `integrations/doc-gen/lib/utils.sh` |
| `office/scripts/` | `integrations/doc-gen/scripts/` |

### integrations/code-context

| est7/dotclaude | 1st-cc-plugin |
|----------------|---------------|
| `code-context/skills/code-context/` | `integrations/code-context/skills/code-context/` |
| `code-context/skills/get-context/` | `integrations/code-context/skills/get-context/` |
| `code-context/agents/context-researcher.md` | `integrations/code-context/agents/context-researcher.md` |
| `code-context/.mcp.json` | `integrations/code-context/.mcp.json` |

### integrations/utils

| est7/dotclaude | 1st-cc-plugin |
|----------------|---------------|
| `utils/skills/update-readme/` | `integrations/utils/skills/update-readme/` |

### authoring/plugin-optimizer

| est7/dotclaude | 1st-cc-plugin |
|----------------|---------------|
| `plugin-optimizer/skills/optimize-plugin/` | `authoring/plugin-optimizer/skills/optimize-plugin/` |
| `plugin-optimizer/skills/plugin-best-practices/` | `authoring/plugin-optimizer/skills/plugin-best-practices/` |
| `plugin-optimizer/agents/plugin-optimizer.md` | `authoring/plugin-optimizer/agents/plugin-optimizer.md` |
| `plugin-optimizer/scripts/validate-plugin.py` | `authoring/plugin-optimizer/scripts/validate-plugin.py` |
| `plugin-optimizer/examples/` | `authoring/plugin-optimizer/examples/` |

### authoring/acpx

| est7/dotclaude | 1st-cc-plugin |
|----------------|---------------|
| `acpx/skills/use-acpx/` | `authoring/acpx/skills/use-acpx/` |

### platforms/next-devtools

| est7/dotclaude | 1st-cc-plugin |
|----------------|---------------|
| `next-devintegrations/skills/next-devtools-guide/` | `platforms/next-devintegrations/skills/next-devtools-guide/` |

### platforms/swiftui

| est7/dotclaude | 1st-cc-plugin |
|----------------|---------------|
| `swiftui/skills/swiftui-review/` | `platforms/swiftui/skills/swiftui-review/` |

### platforms/shadcn

| est7/dotclaude | 1st-cc-plugin |
|----------------|---------------|
| `shadcn/skills/shadcn/` | `platforms/shadcn/skills/shadcn/` |

### quality/meeseeks-vetted

| est7/dotclaude | 1st-cc-plugin |
|----------------|---------------|
| `meeseeks-vetted/skills/vet/` | `quality/meeseeks-vetted/skills/vet/` |
| `meeseeks-vetted/hooks/` | `quality/meeseeks-vetted/hooks/` |
| `meeseeks-vetted/lib/utils.sh` | `quality/meeseeks-vetted/lib/utils.sh` |

## Plugins only in 1st-cc-plugin (no upstream equivalent)

These plugins are unique to `1st-cc-plugin` and must never be modified during upstream sync:

| Plugin | Path | Origin |
|--------|------|--------|
| issue-driven-dev | `workflows/issue-driven-dev/` | Baitu Android team |
| simple-task | `workflows/simple-task/` | est7 |
| complex-task | `workflows/complex-task/` | est7 |
| catchup | `workflows/catchup/` | est7 |
| deep-plan | `workflows/deep-plan/` | est7 |
| todo-sdd-workflow | `workflows/todo-sdd-workflow/` | est7 |
| codex-review | `quality/codex-review/` | est7 |
| testing | `quality/testing/` | est7 |
| ai-hygiene | `quality/ai-hygiene/` | est7 |
| clarify | `quality/clarify/` | est7 |
| project-health | `quality/project-health/` | est7 |
| async-agent | `integrations/async-agent/` | est7 |
| jetbrains | `integrations/jetbrains/` | est7 |
| mcp-services | `integrations/mcp-services/` | est7 |
| knowledge-vault | `integrations/knowledge-vault/` | est7 |
| android | `platforms/android/` | est7 |
| skill-dev | `authoring/skill-dev/` | est7 |
| release | `delivery/release/` | est7 |

## Files to always skip

These files are est7/dotclaude repo-level files and should never be ported:

- `.claude-plugin/marketplace.json` — `1st-cc-plugin` has its own
- `.git-agent/config.yml` — CI/CD config
- `.claude/commands/bump-version.md` — repo-level command
- `.claude/git.local.md` — repo-level local config
- `.claude/settings.json` — repo-level settings
- `CHANGELOG.md` — release history
- `CLAUDE.md` — diff for new sections worth porting, but never overwrite
- `README.md` / `README.zh-CN.md` — `1st-cc-plugin` has its own
- `LICENSE` — already present

## Content adaptation checklist

When porting any file:

- [ ] Author: `Frad LEE / fradser@gmail.com` -> `est7 / t4here@gmail.com`
- [ ] Version: keep `1st-cc-plugin`'s existing version, ignore upstream's
- [ ] Install commands: `@frad-dotclaude` -> `@1st-cc-plugin`
- [ ] URLs: `FradSer/dotclaude` -> `est7/1st-cc-plugin`
- [ ] Flat paths: `plugin-name/` -> `group/plugin-name/`
- [ ] Validation script path from `MyPluginRepo` root: `1st-cc-plugin/authoring/plugin-optimizer/scripts/`
