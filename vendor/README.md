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
| `yoyo-evolve` | Self-evolving Rust CLI agent that autonomously reads its own source, implements improvements, and commits if tests pass — running 24/7 on GitHub Actions. |
| `ralph-orchestrator` | Hat-based orchestration framework that loops AI agents until done, with backpressure gates, parallel worktrees, wave parallelism, and Telegram HITL. |
| `ralph` | Minimal bash implementation of the Ralph pattern — PRD.json drives a fresh-context agent loop until all user stories pass quality checks. |
| `agents` | Massive plugin marketplace with 184 agents, 150 skills, 98 commands across 78 focused Claude Code plugins. |
| `gastown` | Multi-agent workspace orchestrator coordinating 20-30 AI agents with persistent git-backed work state and Beads integration. |
| `claude-code-workflows` | Curated code review, security review, and design review workflows for Claude Code with GitHub Actions integration. |
| `Hephaestus` | Semi-structured agentic framework where AI agents dynamically create tasks across phases as they discover new work. |
| `claude-code-riper-5` | RIPER workflow enforcing Research→Innovate→Plan→Execute→Review phases with memory bank and subagent architecture. |

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
| `flowspec` | SDD CLI with complexity scoring, specialized AI subagents, and backlog integration via backlog.md + beads. |
| `recursive-mode` | Audited, file-backed development workflow with draft→audit→lock phase gates, subskills for TDD/worktrees/review, and a durable memory layer. |
| `agent-spec` | Contract-first BDD/spec verification CLI that turns task contracts into executable planning, lifecycle gates, and acceptance evidence. |
| `claude-task-master` | AI-driven task management system for structured development with MCP server, CLI, and multi-model support. |
| `aegisFlow` | Multi-agent CLI orchestrator turning ideas into structured delivery via PRD, design, review, and roundtable stages. |
| `human-in-loop` | Specification-driven Claude Code plugin enforcing human review gates from idea through plan, tasks, and implementation. |
| `spec-orch` | Seven-plane control plane for spec-driven software delivery with gate enforcement, evidence collection, and self-evolution. |

### Project memory, planning, and team structure

| Project | Short take |
| --- | --- |
| `planning-with-files` | Persistent Markdown planning workflow modeled after Manus-style working memory on disk. |
| `Trellis` | Multi-platform framework built around repo-shared specs, tasks, journals, and worktree-based parallelism. |
| `beads` | Dolt-powered distributed graph issue tracker designed for AI agent workflows with dependency-aware task graphs. |

### Setup tools and skill packs

| Project | Short take |
| --- | --- |
| `claude-code-quickstart` | Windows-first bootstrap and management system for Claude Code environments, vendors, and MCPs. |
| `CaludeSkills-Web-Gstack` | Web-app adaptation of gstack skills for claude.ai, no terminal required. |
| `happy-skills` | Skills bundle covering feature work, issue-to-PR pipelines, screenshot analysis, and media generation. |
| `BMAD-METHOD` | Large AI-agile framework with domain specialists, structured workflows, and scale-adaptive planning. |
| `claude-code-cookbook` | Multilingual plugin collection with slash commands, expert roles, and automation hooks for Claude Code. |
| `compound-engineering-plugin` | Compound engineering workflow plugin with brainstorm-plan-work-review-compound cycle and cross-platform CLI converter. |
| `everything-claude-code` | Full-stack harness performance system with 28 agents, 116 skills, 60 commands, hooks, rules, and cross-platform support (Claude Code/Cursor/Codex/OpenCode). |
| `dotclaude` | 15-plugin marketplace covering git, gitflow, github, refactoring, SwiftUI, shadcn, Next.js, office docs, and plugin optimization. |
| `superpowers` | Official cross-platform skills system centered on automatic workflow activation, TDD discipline, and subagent execution. |
| `claude-plugins-official` | Anthropic's official plugin directory with internal and community plugins covering LSP, MCP, code review, and dev workflows. |
| `yao-meta-skill` | Rigorous skill engineering system for creating, evaluating, packaging, and governing reusable agent skills with a full toolchain and eval suite. |
| `everything-claude-code-mobile` | Mobile-focused skill pack with 27 agents, 48 skills, and 35 commands for Android, iOS, and KMP development with end-to-end feature builder. |
| `claude-code-best-practice` | Curated best-practice encyclopedia with 69 tips, workflow comparisons, orchestration examples, and community-sourced patterns for Claude Code. |
| `Agent-Skills-for-Context-Engineering` | Platform-agnostic collection of 14 skills teaching context engineering principles for production AI agent systems. |
| `zcf` | Zero-config CLI for one-click Claude Code and Codex setup with bilingual support and API provider presets. |
| `spec-first` | Bilingual CLI installing governed workflow assets (skills, agents, commands) into Claude Code and Codex projects. |
| `claude-skills` | Curated skill collection featuring multi-agent TDD orchestration with context-isolated subagents, plus 40+ utility skills. |

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

#### `yoyo-evolve`

- `Focus`: Build a coding agent that autonomously improves itself by reading its own source and committing working changes.
- `Traits`: 31k+ lines of self-written Rust, ~3 evolution sessions/day via GitHub Actions cron, community-directed via GitHub Issues voting, two-layer memory (append-only JSONL + synthesized daily context), and 12-provider multi-model support.
- `Flow`: install via `cargo install yoyo-agent` -> run `yoyo` in REPL or `-p` one-shot -> open a GitHub Issue with `agent-input` label to direct future evolution -> agent reads issues, plans, implements, tests, commits or reverts automatically.

#### `ralph-orchestrator`

- `Focus`: Keep AI agents looping until a task is provably complete, using backpressure gates instead of prescriptive steps.
- `Traits`: Hat system for specialized personas, multi-backend support (Claude/Kiro/Gemini/Codex/Amp/Copilot), wave parallelism for intra-loop fan-out, parallel worktree loops, Telegram HITL via RObot, PDD planning integration, and web dashboard.
- `Flow`: `ralph init --backend claude` -> `ralph plan "<feature>"` -> `ralph run -p "Implement the feature"` -> agent iterates until `LOOP_COMPLETE`; monitor with `ralph loops` or `ralph web`.

#### `ralph`

- `Focus`: Implement the Ralph fresh-context loop in the simplest possible form — a bash script and a JSON task list.
- `Traits`: Zero-framework approach, PRD.json as the task contract, `progress.txt` for accumulated learnings, quality-check gate before each commit, Amp and Claude Code backend support, and Claude Code marketplace installable.
- `Flow`: `/prd` skill -> `/ralph` skill to produce `prd.json` -> `./ralph.sh [--tool claude]` -> agent loop picks next failing story, implements, checks, commits, and updates `prd.json` until `<promise>COMPLETE</promise>`.

#### `agents`

- `Focus`: Provide a comprehensive, composable agent marketplace with progressive disclosure and minimal token overhead.
- `Traits`: 78 granular plugins, 184 agents, 150 skills, 98 commands, multi-agent orchestration, skill-based progressive disclosure, model-tier strategy.
- `Flow`: Add marketplace -> browse plugins -> install needed plugins -> agents/skills auto-load on trigger.

#### `gastown`

- `Focus`: Scale multi-agent coordination beyond 4-10 agents with persistent identity, mailboxes, and crash-resilient state.
- `Traits`: Mayor coordinator, Rigs/Polecats/Hooks model, git worktree persistence, convoy tracking, three-tier watchdog, merge queue, federation.
- `Flow`: Mayor assigns work -> Rigs dispatch Polecats -> Hooks persist state -> Refinery merges -> Deacon monitors health.

#### `claude-code-workflows`

- `Focus`: Automate the blocking-and-tackling of PR reviews — code, security, and design — so humans focus on strategy.
- `Traits`: Dual-loop review architecture, GitHub Actions CI integration, Playwright-based design review, OWASP Top 10 security checks.
- `Flow`: PR opened -> slash command or GH Action triggers -> automated review (code/security/design) -> findings report.

#### `Hephaestus`

- `Focus`: Let agent workflows branch themselves — agents spawn new investigation/implementation/validation tasks based on runtime discoveries.
- `Traits`: Self-branching task tree, 3-phase model (analyze/implement/validate), Guardian coherence monitoring, PRD-to-software pipeline.
- `Flow`: Define phase types -> agents execute tasks -> discover new work -> spawn cross-phase tasks -> tree grows organically.

#### `claude-code-riper-5`

- `Focus`: Prevent premature implementation by separating research, planning, and execution into mode-restricted phases.
- `Traits`: 5-phase RIPER protocol, strict mode enforcement, memory bank persistence, 3 consolidated agents, per-branch memory isolation.
- `Flow`: `/riper:strict` -> Research (read-only) -> Innovate -> Plan (write to memory) -> Execute (full access) -> Review (validate).

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

#### `flowspec`

- `Focus`: Give every feature the right level of spec rigor by scoring complexity first and scaling the SDD process accordingly.
- `Traits`: `flowspec-cli` Python package, 8-dimension complexity scoring, three workflow tiers (Simple/Medium/Full SDD), specialized backend/frontend/QA/security subagents, backlog.md + beads task tracking, and rigorous quality gates enforced per phase.
- `Flow`: `flowspec init` -> `/flow:assess` to score complexity -> `/flow:specify` -> `/flow:plan` (Full SDD only) -> `/flow:implement` -> `/flow:validate`.

#### `recursive-mode`

- `Focus`: Replace chat-only context with durable, file-backed phase artifacts that survive sessions and accumulate project knowledge.
- `Traits`: 9-phase run lifecycle (requirements → AS-IS → plan → implementation → review → test → QA → decisions → closeout), draft→audit→repair→lock progression, installable subskills (worktrees, TDD, review bundles, subagent verification), and file-based memory layer separated from run-local state.
- `Flow`: `npx skills add try-works/recursive-mode` -> invoke "Implement the run" -> agent bootstraps `/.recursive/` scaffold -> phases advance through audited locks -> closeout promotes learnings to `/.recursive/memory/`.

#### `agent-spec`

- `Focus`: Turn task specifications into executable contracts that agents implement against and machines verify.
- `Traits`: Task Contract DSL, BDD completion criteria with explicit test selectors, contract/plan/lifecycle/guard CLI, AI-agent skill pack, and contract acceptance in place of code review.
- `Flow`: `agent-spec init` -> write Task Contract (`Intent`/`Decisions`/`Boundaries`/`Completion Criteria`) -> `agent-spec contract` or `plan` -> implement -> `agent-spec lifecycle` -> `agent-spec guard` -> `agent-spec explain`.

#### `claude-task-master`

- `Focus`: Break down PRDs into granular tasks with dependency tracking and AI-powered decomposition for iterative development.
- `Traits`: MCP server, multi-LLM provider support, task dependency DAG, PRD-to-tasks pipeline, Cursor/Claude Code integration.
- `Flow`: PRD input -> task decomposition -> dependency ordering -> iterative implementation -> task completion tracking.

#### `aegisFlow`

- `Focus`: Automate the full idea-to-delivery pipeline with multi-agent review consensus and roundtable decision-making.
- `Traits`: 8-stage pipeline, multi-engine support (codex/claude/gemini), independent review + roundtable, session persistence, resumable stages.
- `Flow`: Idea intake -> requirement gate -> PRD -> tech design -> multi-agent reviews -> roundtable -> task plan -> execution -> integration.

#### `human-in-loop`

- `Focus`: Ensure architectural decisions are made by humans before AI writes code, via DAG-based deterministic workflow infrastructure.
- `Traits`: DAG-based workflow engine, 6-stage pipeline, human review checkpoints, constitution-governed, Pydantic entity models, MCP write gate.
- `Flow`: Setup constitution -> Specify requirements -> Plan architecture -> Generate tasks -> Audit artifacts -> Implement with tracking.

#### `spec-orch`

- `Focus`: Make AI-driven software delivery orchestratable, verifiable, and self-improving through spec-first gate-first methodology.
- `Traits`: Seven-plane architecture, spec freeze, task DAG with waves, context contracts, gate evaluation, evidence-driven, evolution plane.
- `Flow`: Discuss & freeze spec -> generate plan DAG -> harness execution -> collect evidence at gates -> evolve policies from learnings.

### Project Memory, Planning, and Team Structure

#### `planning-with-files`

- `Focus`: Use Markdown files as persistent working memory so plans survive context resets and long-running work.
- `Traits`: Manus-inspired planning model, wide IDE support, hooks for re-reading and recovery, and strong session catch-up behavior.
- `Flow`: install the skill -> start `/planning-with-files:plan` or `/plan` -> keep progress in planning files -> recover after `/clear` through session catch-up.

#### `Trellis`

- `Focus`: Standardize AI workflow structure across many platforms with shared specs, task context, and personal memory.
- `Traits`: `.trellis/` as the canonical workspace, auto-injected specs, git worktree parallelism, and per-user journals alongside team-shared process.
- `Flow`: `trellis init` -> define rules in `.trellis/spec/` -> manage work from `.trellis/tasks/` -> use journals and worktrees to execute in parallel.

#### `beads`

- `Focus`: Give coding agents a persistent, structured, version-controlled memory for long-horizon task tracking.
- `Traits`: Dolt SQL backend, hash-based IDs, dependency graph, semantic compaction, hierarchical epics, stealth mode, messaging.
- `Flow`: `bd init` -> `bd create` tasks -> `bd dep add` links -> `bd ready` finds unblocked work -> `bd close`.

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

#### `claude-code-cookbook`

- `Focus`: Extend Claude Code with a curated set of slash commands, expert roles, and automation hooks across multiple languages.
- `Traits`: Multilingual plugin system (JA/EN/KO/ZH-CN/ZH-TW/ES/FR/PT), role-based expertise switching, PR management and code quality commands, safety hooks, and Apache 2.0 licensed.
- `Flow`: `/plugin marketplace add wasabeef/claude-code-cookbook` -> `/plugin install cook-zh-cn@claude-code-cookbook` -> use `/pr-create`, `/refactor`, `/role security`, etc.

#### `compound-engineering-plugin`

- `Focus`: Make each unit of engineering work easier than the last through a compounding brainstorm-plan-work-review cycle.
- `Traits`: 80/20 planning-to-execution ratio, cross-platform CLI converter (OpenCode/Codex/Gemini/Copilot/Kiro/Windsurf/Droid/Pi/Qwen/OpenClaw), worktree-based task execution, multi-agent review, learnings codification, and personal config sync across tools.
- `Flow`: `/ce:ideate` (optional) -> `/ce:brainstorm` -> `/ce:plan` -> `/ce:work` -> `/ce:review` -> `/ce:compound` -> repeat.

#### `everything-claude-code`

- `Focus`: Provide a comprehensive agent harness performance system with production-ready agents, skills, hooks, rules, and cross-platform support.
- `Traits`: 28 agents, 116 skills, 60 commands across 12 language ecosystems; continuous learning with instinct-based pattern extraction; AgentShield security scanning; cross-platform parity (Claude Code, Cursor, Codex, OpenCode); token optimization and strategic compaction; selective install architecture.
- `Flow`: `/plugin marketplace add` -> `/plugin install` -> install language rules via `./install.sh` -> use `/plan`, `/tdd`, `/code-review`, `/learn` -> `/evolve` to compound learnings.

#### `dotclaude`

- `Focus`: Provide a curated, well-structured plugin marketplace with domain-specific skills for common development workflows.
- `Traits`: 15 plugins, clean per-plugin structure with agents/skills/scripts separation, PreToolUse hooks for commit validation, plugin-optimizer for self-validation, office document generation (patents, Feishu, PRDs), and marketplace-based distribution.
- `Flow`: `claude plugin install <name>@frad-dotclaude` -> use domain commands like `/git:commit`, `/refactor:refactor`, `/swiftui:review` -> validate with `/plugin-optimizer:optimize-plugin`.

#### `superpowers`

- `Focus`: Turn coding agents into disciplined implementation workers by auto-invoking planning, TDD, review, debugging, and branch-finishing workflows.
- `Traits`: Official Claude marketplace availability, cross-platform install paths (Claude Code, Cursor, Codex, OpenCode, Gemini CLI), mandatory skill activation, subagent-driven execution, and strong test-first posture.
- `Flow`: install plugin/extension -> let `brainstorming` refine the goal -> run `writing-plans` and `using-git-worktrees` after design approval -> execute via `subagent-driven-development` or `executing-plans` -> finish with code review and branch wrap-up skills.

#### `claude-plugins-official`

- `Focus`: Provide the canonical reference for Claude Code plugin structure, conventions, and available first-party plugins.
- `Traits`: Anthropic-maintained, split into internal and external plugin directories, covers LSP integrations (12 languages), MCP server dev, code review, feature dev, skill creation, and output style presets.
- `Flow`: browse `plugins/` and `external_plugins/` -> study `plugin.json` and skill structure -> install via `/plugin install <name>@claude-plugins-official` -> adapt patterns for your own plugins.

#### `yao-meta-skill`

- `Focus`: Turn rough workflows, prompts, and runbooks into governed, reusable skill packages with rigorous trigger quality and portability guarantees.
- `Traits`: Unified `yao.py` CLI, train/dev/holdout/blind/adversarial eval loop, judge-backed blind eval, promotion policy with lifecycle states, cross-platform packaging (openai/claude/generic), governance maturity scoring, and context budget tracking.
- `Flow`: `yao.py init my-skill` -> `yao.py validate` -> `yao.py workspace-flow` -> `yao.py review` -> `yao.py release-snapshot` -> `yao.py package --platform claude --zip`.

#### `everything-claude-code-mobile`

- `Focus`: Provide a comprehensive mobile development harness with specialized agents, skills, and an end-to-end feature builder pipeline for Android, iOS, and KMP.
- `Traits`: 27 agents across 7 roles (review, build, architecture, UI, implementation, testing, learning), 7-phase feature builder with DAG-ordered layer agents, platform-specific MCP memory servers, continuous learning with instinct extraction, Material 3 Expressive and Liquid Glass design system support, and strict TDD enforcement with 80% coverage gates.
- `Flow`: `/feature-build <description>` -> planner + architect -> layer agents (architecture -> network + UI -> data -> wiring) -> test writers -> build fix -> quality gate (review + security + perf) -> verify -> learn.

#### `claude-code-best-practice`

- `Focus`: Aggregate and curate Claude Code configuration best practices, community tips, and workflow patterns into a single reference.
- `Traits`: 69 tips from Boris Cherny and community, 10+ workflow comparisons table, Command->Agent->Skill orchestration demo, best-practice docs per feature, cross-model workflow guides, and hook/sound notification system.
- `Flow`: read CONCEPTS table -> study `best-practice/` docs -> clone and run `/weather-orchestrator` demo -> apply patterns to your own project.

#### `Agent-Skills-for-Context-Engineering`

- `Focus`: Teach the discipline of curating context windows — compression, degradation patterns, memory systems, tool design.
- `Traits`: Platform-agnostic, progressive disclosure, academic citations, foundational/architectural/operational skill tiers, BDI cognitive models.
- `Flow`: Load skill names -> activate relevant skill -> apply principles (compression, memory, evaluation) -> optimize context.

#### `zcf`

- `Focus`: Eliminate manual configuration friction for Claude Code environments — workflows, MCP, API keys, and IDE detection.
- `Traits`: Zero-config, bilingual i18n, API provider presets, interactive menu, multi-platform (incl. Termux), consolidated template architecture.
- `Flow`: `npx zcf i` -> detect environment -> install workflows + API config + MCP -> ready to code.

#### `spec-first`

- `Focus`: Package AI-assisted development into an installable, governed system with explicit artifacts, structured review, and knowledge compounding.
- `Traits`: npm CLI, bilingual (zh/en), doctor diagnostics, asset sync to .claude/.codex, language policy injection, developer profiles.
- `Flow`: `spec-first init` -> doctor check -> bootstrap assets -> ideate -> clarify -> plan -> execute -> review -> compound knowledge.

#### `claude-skills`

- `Focus`: Provide ready-to-install specialized skills — especially a deeply engineered TDD workflow with context-isolated subagents.
- `Traits`: Multi-agent TDD with context isolation, RED/GREEN/REFACTOR gates, 7 framework support, Google Workspace skill, 40+ utility skills.
- `Flow`: Copy skill to `~/.claude/skills/` -> invoke via `/tdd` or `/gws` -> agent orchestration handles phases automatically.

## Patterns Across the Collection

### Most common workflow shapes

- `Spec-first`: `cc-sdd`, `spec-kit`, `OpenSpec`, `LeanSpec`, `spec-workflow-mcp`, `claude-code-spec-workflow`, `ouroboros`, `flowspec`, `recursive-mode`, `agent-spec`, `claude-task-master`, `aegisFlow`, `human-in-loop`, `spec-orch`, `spec-first`
- `Role-orchestration first`: `gstack`, `oh-my-claudecode`, `Claude-Code-Workflow`, `ccg-workflow`, `BMAD-METHOD`, `agents`, `gastown`, `claude-code-workflows`, `Hephaestus`, `aegisFlow`
- `Context/memory first`: `claude-reflect`, `planning-with-files`, `Trellis`, `claude-code-specs-generator`, `recursive-mode`, `beads`, `claude-task-master`, `claude-code-riper-5`, `Agent-Skills-for-Context-Engineering`
- `Backpressure-loop first`: `ralph-orchestrator`, `ralph`, `claude-code-workflows`, `human-in-loop`, `spec-orch`, `claude-skills`, `claude-code-riper-5`
- `Self-evolution first`: `yoyo-evolve`, `gastown`, `Hephaestus`, `spec-orch`
- `Environment/bootstrap first`: `claude-code-quickstart`, `happy-skills`, `CaludeSkills-Web-Gstack`, `claude-code-cookbook`, `compound-engineering-plugin`, `everything-claude-code`, `everything-claude-code-mobile`, `dotclaude`, `claude-plugins-official`, `claude-code-best-practice`, `zcf`, `spec-first`
- `Skill engineering and governance first`: `yao-meta-skill`, `agents`, `Agent-Skills-for-Context-Engineering`, `claude-skills`

### Key differentiators worth watching

- `gstack` is strongest on end-to-end sprint coverage and shipping discipline.
- `ccg-workflow` is strongest on explicit cross-model role separation.
- `paul` is strongest on loop closure and anti-drift execution.
- `OpenSpec` and `LeanSpec` both fight process overhead, but `OpenSpec` is more artifact/workflow oriented while `LeanSpec` is more document-size/context-economy oriented.
- `spec-workflow-mcp` and `claude-code-spec-workflow` both add dashboard visibility, but the former is MCP-first while the latter is Claude-Code-first.
- `planning-with-files` and `Trellis` both treat files as durable memory, but `planning-with-files` is planning-centric while `Trellis` is broader team structure plus multi-platform wiring.
- `claude-reflect` stands out because it improves the agent itself from corrections, not just the project.
- `ralph-orchestrator` stands out because it treats the loop itself as the reliability mechanism: fresh context every iteration, gates instead of prescriptions, and disk as the handoff medium.
- `ralph` stands out as the minimal-viable implementation of the same pattern: a single bash script, a JSON task list, and nothing else.
- `recursive-mode` stands out because every phase is both file-recorded and audit-locked, making the agent's work explicitly verifiable rather than trust-based.
- `agent-spec` stands out because it treats the spec itself as the task contract, then replaces subjective code review with contract acceptance backed by explicit verification.
- `superpowers` stands out because it treats skills as mandatory runtime policy, not optional slash-command helpers.

## Suggested Reading Order

If the goal is to compare approaches quickly, read in this order:

1. `gstack`, `get-shit-done`, `oh-my-claudecode`, `ccg-workflow`, `yoyo-evolve`, `ralph-orchestrator`, `ralph`, `agents`, `gastown`, `claude-code-workflows`, `Hephaestus`, `claude-code-riper-5`
2. `cc-sdd`, `spec-kit`, `OpenSpec`, `LeanSpec`, `flowspec`, `recursive-mode`, `agent-spec`, `claude-task-master`, `aegisFlow`, `human-in-loop`, `spec-orch`
3. `planning-with-files`, `Trellis`, `claude-reflect`, `beads`
4. `claude-code-quickstart`, `happy-skills`, `CaludeSkills-Web-Gstack`, `BMAD-METHOD`, `claude-code-cookbook`, `compound-engineering-plugin`, `everything-claude-code`, `everything-claude-code-mobile`, `dotclaude`, `superpowers`, `claude-plugins-official`, `yao-meta-skill`, `claude-code-best-practice`, `Agent-Skills-for-Context-Engineering`, `zcf`, `spec-first`, `claude-skills`

That sequence moves from execution systems, to specification systems, to memory systems, to setup and distribution layers.
