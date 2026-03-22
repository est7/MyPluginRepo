# Vendor Project Landscape

This repository collects AI coding workflow projects, spec-driven development systems, multi-agent orchestration frameworks, bootstrap tools, and skill packs.

The summary below focuses on three things for each project:

- `Focus`: what problem the project is really solving
- `Traits`: what makes it distinct from similar tools
- `Flow`: the core path a user is expected to follow

## At a Glance

### CLI workflow systems and agent enhancers

| Project | Short take |
| --- | --- |
| `gstack` | Garry Tan's software-factory workflow with specialist roles across idea, review, QA, shipping, and release. |
| `get-shit-done` | Context-engineering-heavy system optimized for solo builders who want minimal ceremony and strong execution. |
| `Claude-Code-Workflow` | JSON-driven multi-CLI orchestration framework with sessions, dashboards, and semantic tool routing. |
| `oh-my-claudecode` | Team-first orchestration for Claude Code with autopilot, team pipelines, worker panes, and reusable skills. |
| `ccg-workflow` | Claude as orchestrator, Codex for backend, Gemini for frontend, with security isolation and OPSX integration. |
| `paul` | Plan-Apply-Unify loop emphasizing loop closure, acceptance criteria, and in-session context quality. |
| `claude-reflect` | Learns from user corrections and turns repeated behavior into durable memory and reusable commands. |
| `skill-router` | Low-presence runtime for reducing skill-selection waste in crowded skill environments. |

### Workflow systems and spec-driven development

| Project | Short take |
| --- | --- |
| `cc-sdd` | Cross-agent spec-driven workflow inspired by Kiro, centered on requirements, design, tasks, and implementation. |
| `spec-kit` | GitHub's broad SDD toolkit with constitution, specify, plan, tasks, and implement phases. |
| `OpenSpec` | Lightweight, iterative spec framework built around artifact folders and flexible change workflows. |
| `lean-spec` | LeanSpec, a small-spec system designed to keep humans and AI aligned without heavy process overhead. |
| `spec-workflow-mcp` | MCP-based spec workflow with dashboard, approvals, logs, and VS Code integration. |
| `claude-code-spec-workflow` | Claude Code specific spec workflow with feature and bug-fix tracks plus dashboard support. |
| `ouroboros` | Specification-first system using Socratic questioning and ontological analysis before execution. |
| `claude-code-specs-generator` | Context and documentation generator that builds steering plus spec documents for Claude Code. |
| `spec-based-claude-code` | Implementation guide for building a custom slash-command-based SDD workflow yourself. |

### Project memory, planning, and team structure

| Project | Short take |
| --- | --- |
| `planning-with-files` | Persistent Markdown planning workflow modeled after Manus-style working memory on disk. |
| `Trellis` | Multi-platform framework built around repo-shared specs, tasks, journals, and worktree-based parallelism. |

### Setup tools and skill packs

| Project | Short take |
| --- | --- |
| `claude-code-quickstart` | Windows-first bootstrap and management system for Claude Code environments, vendors, and MCPs. |
| `CaludeSkills-Web-Gstack` | Web-app adaptation of gstack skills for claude.ai, no terminal required. |
| `happy-skills` | Skills bundle covering feature work, issue-to-PR pipelines, screenshot analysis, and media generation. |
| `BMAD-METHOD` | Large AI-agile framework with domain specialists, structured workflows, and scale-adaptive planning. |

## Detailed Summaries

### CLI Workflow Systems and Agent Enhancers

#### `gstack`

- `Focus`: Turn Claude Code into a full software factory with specialist roles across the whole sprint.
- `Traits`: Strong role design, real browser QA, release automation, docs sync, and explicit sprint sequencing.
- `Flow`: `/office-hours` -> `/plan-ceo-review` -> `/plan-eng-review` -> build -> `/review` -> `/qa` -> `/ship` -> `/land-and-deploy` -> `/retro`.

#### `get-shit-done`

- `Focus`: Make AI-assisted shipping reliable through context engineering rather than enterprise ceremony.
- `Traits`: Strong anti-context-rot positioning, multi-runtime support, solo-builder orientation, and minimal user-facing complexity.
- `Flow`: install -> `/gsd:new-project` or `/gsd:map-codebase` -> structured questioning and planning -> implementation -> verification.

#### `Claude-Code-Workflow`

- `Focus`: Provide a configurable multi-agent, multi-CLI workflow framework with semantic invocation and session lifecycle control.
- `Traits`: JSON-driven workflows, queue scheduler, terminal dashboard, orchestrator editor, and semantic routing across Gemini, Codex, Qwen, and Claude.
- `Flow`: install `ccw` -> choose a workflow skill such as `workflow-plan` or `workflow-lite-plan` -> execute -> manage state with `/workflow/session:*`.

#### `oh-my-claudecode`

- `Focus`: Hide orchestration complexity behind natural language and team-centric execution surfaces.
- `Traits`: Team pipeline as the main runtime, tmux worker support for Codex and Gemini, autopilot modes, skill learning, and HUD visibility.
- `Flow`: plugin install -> `/setup` and `/omc-setup` -> use `autopilot:` or `/team` -> verify/fix loop until completion.

#### `ccg-workflow`

- `Focus`: Use Claude as the safe orchestrator while Codex and Gemini handle backend and frontend work respectively.
- `Traits`: Zero-config routing, patch-return security model, 27 slash commands, OPSX-backed constraint planning, and optional agent teams.
- `Flow`: `npx ccg-workflow` -> `/ccg:plan` or `/ccg:workflow` -> `/ccg:execute` or `/ccg:codex-exec` -> `/ccg:review` -> git and release commands.

#### `paul`

- `Focus`: Keep AI development disciplined through a closed execution loop with explicit reconciliation.
- `Traits`: Acceptance-driven development, strong anti-subagent stance for implementation, required closure via UNIFY, and persistent state.
- `Flow`: `/paul:init` -> `/paul:plan` -> `/paul:apply` -> `/paul:unify` -> `/paul:progress`.

#### `claude-reflect`

- `Focus`: Convert user corrections and repeated workflows into lasting memory and reusable skills.
- `Traits`: Hook-based capture, queued human review, multi-target sync to `CLAUDE.md` or `AGENTS.md`, and AI-powered pattern mining.
- `Flow`: install plugin -> automatic hook capture -> run `/reflect` to approve learnings -> run `/reflect-skills` to generate reusable commands.

#### `skill-router`

- `Focus`: Reduce the cost of skill discovery and routing in environments with too many overlapping skills.
- `Traits`: Default-first resolution, minimal commentary, low-presence runtime philosophy, and explicit anti-taxonomy positioning.
- `Flow`: decide if routing is needed -> prefer installed defaults -> discover only real gaps -> stay silent if routing does not change the next action.

### Workflow Systems and Spec-Driven Development

#### `cc-sdd`

- `Focus`: Bring Kiro-style spec-driven development to many AI agents with one command.
- `Traits`: Requirements/design/tasks pipeline, project memory, template customization, parallel-ready task decomposition, and wide agent support.
- `Flow`: install with `npx cc-sdd` -> `/kiro:spec-init` -> `/kiro:spec-requirements` -> `/kiro:spec-design` -> `/kiro:spec-tasks` -> `/kiro:spec-impl`.

#### `spec-kit`

- `Focus`: Provide a broad, opinionated SDD toolkit centered on executable specifications.
- `Traits`: Constitution phase, strong CLI tooling, broad agent compatibility, extensions/presets, and full lifecycle from spec to implementation.
- `Flow`: `specify init` -> `/speckit.constitution` -> `/speckit.specify` -> `/speckit.plan` -> `/speckit.tasks` -> `/speckit.implement`.

#### `OpenSpec`

- `Focus`: Add a lightweight, iterative spec layer that fits many AI tools and both greenfield and brownfield work.
- `Traits`: Artifact-guided workflow, change folders per feature, fluid rather than rigid process, and support for 20+ tools.
- `Flow`: `openspec init` -> `/opsx:propose` -> `/opsx:apply` -> `/opsx:archive`, with optional expanded workflows via profile selection.

#### `lean-spec`

- `Focus`: Keep specs small enough to stay current and effective for both humans and AI.
- `Traits`: Lean documents under token discipline, Kanban and stats views, MCP plus CLI support, and strong context-economy philosophy.
- `Flow`: `lean-spec init` -> create/manage small specs -> inspect with `board`, `stats`, or `ui` -> use MCP or skills during implementation.

#### `spec-workflow-mcp`

- `Focus`: Run spec-driven development through an MCP server with operational visibility.
- `Traits`: Real-time dashboard, approval workflow, implementation logs, VS Code extension, and multilingual support.
- `Flow`: add MCP server -> start dashboard -> ask the client to create specs, list progress, and execute tasks through MCP tools.

#### `claude-code-spec-workflow`

- `Focus`: Automate spec and bug-fix workflows specifically inside Claude Code.
- `Traits`: Separate feature and bug tracks, task command generation, specialized agents, dashboard with tunnel support, and steering docs.
- `Flow`: install globally -> run setup -> `/spec-create` for new features or `/bug-create` for fixes -> execute tasks -> monitor via dashboard.

#### `ouroboros`

- `Focus`: Improve AI output by forcing deeper clarity through questioning before any code is written.
- `Traits`: Socratic interview, ambiguity scoring, immutable seed specs, double-diamond execution, and convergence-based evolution.
- `Flow`: install plugin -> `ooo setup` -> `ooo interview` -> `ooo seed` -> `ooo run` -> `ooo evaluate` -> repeat with `ooo ralph` until convergence.

#### `claude-code-specs-generator`

- `Focus`: Generate and maintain the key context documents Claude Code needs for better decisions.
- `Traits`: Six-document system, automatic `CLAUDE.md` updates, light and full refresh modes, and context reload support.
- `Flow`: `/specs-create` -> `/specs-init` -> use `/refresh-specs` after minor changes or `/update-full-specs` after major changes.

#### `spec-based-claude-code`

- `Focus`: Show how to build a custom spec-driven workflow in Claude Code from slash commands and file conventions.
- `Traits`: Educational implementation guide, explicit file structure, approval gates, and command templates for each phase.
- `Flow`: create `.claude/commands/spec` and `spec/` -> `/spec:new` -> `/spec:requirements` -> `/spec:approve` -> `/spec:design` -> `/spec:tasks` -> `/spec:implement`.

### Project Memory, Planning, and Team Structure

#### `planning-with-files`

- `Focus`: Use Markdown files as persistent working memory so plans survive context resets and long-running work.
- `Traits`: Manus-inspired planning model, wide IDE support, hooks for re-reading and recovery, and strong session catch-up behavior.
- `Flow`: install the skill -> start `/planning-with-files:plan` or `/plan` -> keep progress in planning files -> recover after `/clear` through session catch-up.

#### `Trellis`

- `Focus`: Standardize AI workflow structure across many platforms with shared specs, task context, and personal memory.
- `Traits`: `.trellis/` as the canonical workspace, auto-injected specs, git worktree parallelism, and per-user journals alongside team-shared process.
- `Flow`: `trellis init` -> define rules in `.trellis/spec/` -> manage work from `.trellis/tasks/` -> use journals and worktrees to execute in parallel.

### Setup Tools and Skill Packs

#### `claude-code-quickstart`

- `Focus`: Bootstrap and manage a full Claude Code environment on Windows with minimal manual setup.
- `Traits`: Two-stage PowerShell architecture, vendor profiles, MCP credential vault, update snapshots, and integrated workflow tool installation.
- `Flow`: run bootstrap script in PowerShell 5.1 -> run install/manage script in PowerShell 7 -> manage updates, providers, and MCP servers through `ccq`.

#### `CaludeSkills-Web-Gstack`

- `Focus`: Bring gstack-style engineering workflows to the Claude web app without terminal usage.
- `Traits`: Folder-upload skill packaging, 12 curated engineering skills, and a simplified web-native workflow order.
- `Flow`: upload skill folders to claude.ai -> trigger skills like `/office-hours`, `/review`, `/qa`, and `/ship` directly in the web app.

#### `happy-skills`

- `Focus`: Offer a practical skills bundle spanning product development, issue automation, screenshot analysis, and media generation.
- `Traits`: Mix of dev skills and creative/video skills, `skills` CLI distribution, and strong issue-to-PR emphasis.
- `Flow`: install via `npx skills add` -> use `/issue-flow`, `/feature-analyzer`, `/feature-pipeline`, `/feature-dev`, or media skills as needed.

#### `BMAD-METHOD`

- `Focus`: Provide a large AI-agile framework with structured workflows and specialist agents from ideation to deployment.
- `Traits`: Scale-adaptive planning, many domain experts, modular ecosystem, party mode, and a full lifecycle orientation.
- `Flow`: `npx bmad-method install` -> choose modules -> use guided workflows and expert agents, with `bmad-help` as the next-step navigator.

## Patterns Across the Collection

### Most common workflow shapes

- `Spec-first`: `cc-sdd`, `spec-kit`, `OpenSpec`, `LeanSpec`, `spec-workflow-mcp`, `claude-code-spec-workflow`, `ouroboros`
- `Role-orchestration first`: `gstack`, `oh-my-claudecode`, `Claude-Code-Workflow`, `ccg-workflow`, `BMAD-METHOD`
- `Context/memory first`: `claude-reflect`, `planning-with-files`, `Trellis`, `claude-code-specs-generator`
- `Environment/bootstrap first`: `claude-code-quickstart`, `happy-skills`, `CaludeSkills-Web-Gstack`

### Key differentiators worth watching

- `gstack` is strongest on end-to-end sprint coverage and shipping discipline.
- `ccg-workflow` is strongest on explicit cross-model role separation.
- `paul` is strongest on loop closure and anti-drift execution.
- `OpenSpec` and `LeanSpec` both fight process overhead, but `OpenSpec` is more artifact/workflow oriented while `LeanSpec` is more document-size/context-economy oriented.
- `spec-workflow-mcp` and `claude-code-spec-workflow` both add dashboard visibility, but the former is MCP-first while the latter is Claude-Code-first.
- `planning-with-files` and `Trellis` both treat files as durable memory, but `planning-with-files` is planning-centric while `Trellis` is broader team structure plus multi-platform wiring.
- `claude-reflect` stands out because it improves the agent itself from corrections, not just the project.

## Suggested Reading Order

If the goal is to compare approaches quickly, read in this order:

1. `gstack`, `get-shit-done`, `oh-my-claudecode`, `ccg-workflow`
2. `cc-sdd`, `spec-kit`, `OpenSpec`, `LeanSpec`
3. `planning-with-files`, `Trellis`, `claude-reflect`
4. `claude-code-quickstart`, `happy-skills`, `CaludeSkills-Web-Gstack`, `BMAD-METHOD`

That sequence moves from execution systems, to specification systems, to memory systems, to setup and distribution layers.
