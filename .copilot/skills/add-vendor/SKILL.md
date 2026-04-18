---
name: add-vendor
description: "Add a new vendor reference repo to the MyPluginRepo vendor/ directory. Clones the repo as a shallow git submodule, reads its README to understand purpose, updates vendor/README.md with At a Glance entry, Detailed Summary, Patterns classification, and Suggested Reading Order placement, then stages the commit. Use when the user says 'add vendor', 'add reference repo', 'clone to vendor', provides a git repo URL and mentions vendor, or wants to research a new third-party Claude Code plugin/workflow project."
user-invocable: true
argument-hint: "<repo-url> [name]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(git:*)
  - Agent
---

# Add Vendor Reference

Automate the "Adding a New Vendor Reference" SOP for the MyPluginRepo parent repository.

## Input

The user provides:
- **repo-url** (required): Git repository URL (HTTPS or SSH)
- **name** (optional): Directory name under `vendor/`. If omitted, derive from the repo URL (last path segment, without `.git`).

## Workflow

### Step 1: Add the submodule

```bash
git submodule add --depth 1 <repo-url> vendor/<name>
```

After adding, ensure `.gitmodules` has `shallow = true` for this entry. If missing, add it:

```bash
git config -f .gitmodules submodule.vendor/<name>.shallow true
```

### Step 2: Read the new repo

Read `vendor/<name>/README.md` (and any other key files like CLAUDE.md, package.json, or plugin.json) to understand:
- What problem the project solves (Focus)
- What makes it distinct (Traits)
- The core user workflow (Flow)
- Which category it belongs to

### Step 3: Classify the project

Determine which category in vendor/README.md the project fits:
- **CLI workflow systems and agent enhancers** — orchestration, multi-agent, autopilot
- **Workflow systems and spec-driven development** — spec-first, requirements-driven
- **Project memory, planning, and team structure** — persistent memory, planning files, team coordination
- **Setup tools and skill packs** — bootstrap, distribution, plugin collections

If none fit well, propose a new category to the user.

### Step 4: Update vendor/README.md

Make **four** edits to `vendor/README.md`:

1. **At a Glance table**: Add a row under the matching category table:
   ```
   | `<name>` | <one-line description> |
   ```

2. **Detailed Summaries**: Add a new `#### \`<name>\`` section under the matching category heading with exactly this format:
   ```markdown
   #### `<name>`

   - `Focus`: <what problem the project is really solving>
   - `Traits`: <comma-separated list of distinctive traits>
   - `Flow`: <the core path a user follows, using -> arrows>
   ```

3. **Patterns Across the Collection**: Add the project name to the most relevant pattern bullet(s) in the existing classification lists.

4. **Suggested Reading Order**: Insert the project name into the appropriate numbered group based on its category.

### Step 5: Stage changes

Run `git status` to verify changes look correct, then report to the user what was added. Do NOT commit — the user will decide when to commit.

## Style Guide

Match the existing voice in vendor/README.md:
- Summaries are concise and opinionated — say what the project *is*, not what it *claims to be*
- Focus/Traits/Flow entries use sentence fragments, not full sentences
- At a Glance descriptions are ~15-25 words max
- Use backticks for project names and CLI commands in Flow
