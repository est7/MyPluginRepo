# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a **parent monorepo** for Claude Code plugin development. It has two top-level directories:

- `1st-cc-plugin/` — The primary plugin marketplace (git submodule). This is where all active development happens.
- `vendor/` — Read-only third-party plugin/workflow projects (git submodules) used as research references. Do not modify vendor contents.

## Working in `1st-cc-plugin/`

The `1st-cc-plugin/` submodule contains its own detailed `CLAUDE.md` — read it before making any changes there. Key points:

- **Plugin validation:** Run before committing:
  ```bash
  python3 1st-cc-plugin/plugin-optimizer/scripts/validate-plugin.py <plugin-path>
  ```
  Exit codes: 0 = pass, 1 = MUST violations, 2 = token budget critical.

- **Branch strategy:** `develop` → `main` (merge commits)

- **Commit scopes:** `git`, `gitflow`, `github`, `refactor`, `review`, `office`, `swiftui`, `po`, `cc`, `sp`, `nd`, `docs`, `ci`

## Architecture

### Plugin Component Model

Each plugin in `1st-cc-plugin/` follows a 3-tier token budget:
1. **Metadata (~100 tokens):** `plugin.json` name + description — always loaded
2. **Instructions (<5k tokens):** `SKILL.md` body — loaded when skill is triggered
3. **Resources (unlimited):** `references/*.md` files — loaded on demand via bash

### Skill Registration

A skill's visibility is determined by its registration in `plugin.json`:
- Listed under `"commands"` → becomes a user-invocable slash command (e.g., `/git:commit`)
- Listed under `"skills"` → internal-only, auto-loaded by Claude when relevant, never shown in `/help`

### Tool Invocation Convention in Plugin Content

| Context | Convention |
|---------|-----------|
| File operations (Read, Write, Edit, Glob, Grep) | Describe the action directly |
| Bash commands | Describe the command directly: "Run `git diff`" |
| Skill tool | Always explicit: "Load X skill using the Skill tool" |
| Agent launch | Describe it: "Launch code-reviewer agent" |

Never use bare `Bash` in `allowed-tools`; always scope it (e.g., `Bash(git:*)`).

## Submodule Management

```bash
# Update all submodules to tracked commits (shallow)
git submodule update --init --depth 1

# Pull latest from a specific submodule remote
git submodule update --remote vendor/<name>
```

All vendor submodules use `shallow = true` in `.gitmodules` to avoid pulling full history. The `vendor/` submodules are intentionally pinned and should only be updated deliberately for research purposes.

## Adding a New Vendor Reference (SOP)

This is the standard preparation workflow before updating `1st-cc-plugin/`. Every time a new vendor repo is added, follow these steps in order:

1. **Add the git submodule:**
   ```bash
   git submodule add <repo-url> vendor/<name>
   ```

2. **Read the new repo's README:** Understand what it does, its core workflow, and key traits.

3. **Update `vendor/README.md`:** Add the new project to:
   - The "At a Glance" table under the appropriate category
   - The "Detailed Summaries" section with `Focus`, `Traits`, and `Flow`
   - The "Patterns Across the Collection" classification
   - The "Suggested Reading Order" list

4. **Commit the changes** (submodule addition + vendor README update) as a single commit.

## Removing a Vendor Reference (SOP)

When a vendor repo is no longer needed, follow these steps in order:

1. **Remove the git submodule:**
   ```bash
   git submodule deinit -f vendor/<name>
   git rm -f vendor/<name>
   rm -rf .git/modules/vendor/<name>
   ```

2. **Update `vendor/README.md`:** Remove the project from:
   - The "At a Glance" table
   - The "Detailed Summaries" section
   - The "Patterns Across the Collection" classification
   - The "Suggested Reading Order" list

3. **Commit the changes** (submodule removal + vendor README update) as a single commit.

## Porting a Skill to 1st-cc-plugin (SOP)

When the user identifies a good skill from a vendor repo and wants it added to `1st-cc-plugin/`, follow these steps:

### 1. Decide where it belongs

Read the skill's content and understand its domain. Then check existing plugins in `1st-cc-plugin/`:

```
git, gitflow, github, refactor, review, office, swiftui, claude-config,
code-context, shadcn, superpowers, next-devtools, acpx,
todo-issue-workflow, todo-sdd-workflow, 1st-simple-task, 1st-complex-task
```

- If the skill fits an existing plugin's domain, add it there.
- If it opens a new domain with no good fit, create a new plugin directory with `plugin.json` and `SKILL.md`.

### 2. Adapt the skill

- Do NOT copy vendor content verbatim. Rewrite to match `1st-cc-plugin/` conventions.
- Follow the 3-tier token budget: metadata (~100 tokens), instructions (<5k tokens), resources (unlimited `references/*.md`).
- Register in `plugin.json` under `"commands"` (user-invocable) or `"skills"` (auto-triggered).
- Respect tool invocation conventions (no bare `Bash`, scoped permissions).

### 3. Validate

```bash
python3 1st-cc-plugin/plugin-optimizer/scripts/validate-plugin.py 1st-cc-plugin/<plugin-name>
```

### 4. Update documentation

- Update the plugin's own `README.md` (or create one if new plugin).
- Update `1st-cc-plugin/README.md` if the plugin list or marketplace description changed.

### 5. Bump version and commit

- Bump the version in the plugin's `plugin.json`.
- Commit with an appropriate scope: `feat(<scope>): add <skill-name> skill`.
