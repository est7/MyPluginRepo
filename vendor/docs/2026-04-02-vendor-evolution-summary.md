# Vendor Evolution Summary — 2026-04-02

Base: `805ab18` → Head: `de66d87`
Updated: **17 vendors** | Skipped: **14 vendors** (no changes) + **yoyo-evolve** (dirty/self-referential)

---

## Per-Vendor Evolution

### BMAD-METHOD (22 commits)

- **Surface**: New `bmad-prfaq` skill (PR/FAQ analysis with sub-agents), new `bmad-checkpoint-preview` skill (mid-workflow preview with HALT gates). Removed `bmad-init` skill (consolidated into config loading).
- **Evolution**: Moved toward plugin marketplace distribution (added `marketplace.json`, GitHub publish workflow). Party-mode consolidated into single SKILL.md with real subagents. Installer restructured with platform-specific separation (now supports Junie/KiloCoder).
- **Signal vs noise**: The marketplace scaffolding and multi-platform installer are the real evolution. Doc translations and theme changes are noise.
- **Relevance**: The checkpoint-preview pattern (HALT before decision menu) is a workflow discipline idea worth watching. The PRFAQ skill with dedicated sub-agents (artifact-analyzer, web-researcher) shows a trend toward decomposed analysis workflows.

### Claude-Code-Workflow (35 commits, v7.2.22→7.2.30)

- **Surface**: New skills: `json_builder`, `investigate`, `security-audit`, `ship`, 4 new UI team skills. New `ccw-chain` auto mode for chain execution. Deep Codex v4 API conversion across all 20 team skills. Removed coordinator/developer/reviewer/tester legacy roles.
- **Evolution**: Major shift toward chain-based orchestration. `ccw-chain` now has JSON chain definitions (`ccw-cycle.json`, `ccw-standard.json`, `ccw-team.json`, etc.) with discrete phases. Added session awareness spec. Unified agent API to Codex v4 format across all skills.
- **Signal vs noise**: The chain execution model (JSON-defined skill pipelines) and the removal of legacy role-based commands in favor of skill-driven workflows are significant. Version bumps and YAML quoting fixes are noise.
- **Relevance**: The JSON chain definition pattern for multi-skill orchestration is worth studying. Potential port: chain-based workflow sequencing for `1st-cc-plugin`.

### Trellis (8 commits)

- **Surface**: New `first-principles-thinking` skill (with 5 reference docs). New `frontend-fullchain-optimization` skill in marketplace. Added Windsurf workflow support. Self-hosted registry (v0.4.0-beta).
- **Evolution**: Moving toward multi-platform support (Windsurf added alongside Claude/Codex/OpenCode). Self-hosted registry signals a shift toward decentralized skill distribution.
- **Signal vs noise**: The first-principles-thinking skill is a reasoning-methodology skill (novel). Windsurf support shows platform diversification.
- **Relevance**: The first-principles-thinking skill with structured references (axiom-based reasoning, decomposition frameworks, bias/debiasing, case studies) is a novel reasoning-aid concept. Watch list.

### ccg-workflow (15 commits, v1.8→2.0)

- **Surface**: New Skill Registry with domain knowledge and 3 output styles. Configurable model routing for frontend/backend. Impeccable tools integration.
- **Evolution**: Major version bump to 2.0. Added skill registry — a dynamic system that generates commands with YAML frontmatter. Model routing allows different models for frontend vs backend tasks.
- **Signal vs noise**: The skill registry (auto-generating commands from domain knowledge) is the key evolution. Logo assets and README badges are noise.
- **Relevance**: Configurable model routing per task domain (frontend/backend) is a pattern worth considering for `1st-cc-plugin`.

### claude-code-quickstart (3 commits)

- **Surface**: No workflow signal changes. PowerShell installer improvements (Unicode borders, emoji status icons, thinking config).
- **Evolution**: Installer UX polish only.
- **Signal vs noise**: All noise for our purposes.
- **Relevance**: None.

### claude-plugins-official (211 commits)

- **Surface**: Massive marketplace expansion. New internal plugins: `math-olympiad` (adversarial verification), `playground` (renamed from artifact), `mcp-server-dev`, `skill-creator`. New channel plugins: `telegram`, `discord`, `imessage`, `fakechat` — with permission-relay, inline approval buttons, file handling. `ralph-wiggum` renamed to `ralph-loop`. Deprecated `commands/` in favor of `skills/<name>/SKILL.md`.
- **Evolution**: Three major themes: (1) Marketplace exploded — 40+ new external plugins added (AWS, Zapier, Postman, Stripe, etc.). (2) Channel plugins emerged as a new category (messaging integrations with bidirectional permission handling). (3) Official deprecation of `commands/` in favor of `skills/` structure.
- **Signal vs noise**: The `commands/ → skills/` deprecation is the most important signal for the ecosystem. The channel plugin architecture (permission-relay, inline buttons) is novel. Marketplace expansion is expected growth.
- **Relevance**: **Critical**: The official `commands/ → skills/` migration in `plugin-dev` documentation affects our plugin structure conventions. The `math-olympiad` adversarial verification pattern could inspire testing/review skills. Channel plugins are a new category not in `1st-cc-plugin`.

### compound-engineering-plugin (79 commits, v2.60→2.61)

- **Surface**: New agents: `adversarial-document-reviewer`, `adversarial-reviewer`, `cli-agent-readiness-reviewer`, `cli-readiness-reviewer`, `product-lens-reviewer`, `project-standards-reviewer`, `testing-reviewer`. New headless mode for `ce-review` and `document-review`. Merged `deepen-plan` into `ce:plan` as automatic confidence check. New visual aids generation in plans/brainstorms/PRs. Cross-invocation cluster analysis for PR feedback.
- **Evolution**: Strongest evolution in the fleet. Key themes: (1) Adversarial review army — multiple specialized reviewer agents running in parallel. (2) Headless mode for programmatic callers. (3) Confidence-gated workflow with automatic deepening. (4) Branch-based plugin install for worktree workflows. (5) Mandatory review gates across pipeline skills. (6) Cross-platform model normalization (added MiniMax, OpenCode).
- **Signal vs noise**: Almost everything is signal. The adversarial multi-reviewer pattern, headless mode, and confidence-gated deepening are all significant workflow innovations.
- **Relevance**: **High port value**: (1) Adversarial review with multiple specialized agents is directly applicable to `quality/review`. (2) Headless mode for skills enables programmatic composition. (3) Confidence-gated plan deepening could enhance `workflow/plan`. (4) Cross-invocation cluster analysis for detecting systemic review issues.

### dotclaude (41 commits, v1.12.1)

- **Surface**: New `create-prd` skill (with 4 reference templates + validation checklist). New `use-git-agent` skill. New `vet` skill for verification. Refactored git plugin to agent workflow model. Unified gitflow workflow templates.
- **Evolution**: Significant restructuring — moved from command-based git operations to agent-based workflow model. Added execution task tracking design docs. Enhanced superpowers hooks (need_vet flag, slash command detection tiers).
- **Signal vs noise**: The git-to-agent-workflow refactoring and PRD creation skill with structured templates are real evolution. Hook tweaks are incremental.
- **Relevance**: The PRD creation skill with template variants (brief/full/onepager) and validation checklist is a good candidate for `tools/doc-gen`. The verification flag pattern (need_vet) is interesting for quality gates.

### everything-claude-code (245 commits)

- **Surface**: Many new skills: `openclaw-persona-forge`, `agent-payment-x402`, `repo-scan`, `token-budget-advisor`, `context-keeper`, `git-workflow`, `performance-optimizer`, `laravel-plugin-discovery`, `hexagonal-architecture`, `GAN-style generator-evaluator harness`, `opensource-pipeline` (3-agent workflow), `brand-voice`, `content-engine`, `lead-intelligence`, `connected-operator`. Added gitagent format for cross-harness portability. New platform support: Trae, CodeBuddy (Tencent), Gemini, Kiro.
- **Evolution**: Explosive growth in two directions: (1) Skills-first architecture — collapsed legacy command bodies into skills, shifted repo guidance to skills-first workflows. (2) Multi-platform portability — added install targets for Trae, CodeBuddy, Gemini, OpenCode alongside Claude/Codex. The gitagent format and `.agents/` directory structure show convergence toward cross-harness skill definitions.
- **Signal vs noise**: The cross-harness portability trend and skills-first collapse are the key signals. Many of the new skills (healthcare, lead-intelligence, brand-voice) are domain-specific and less relevant. The GAN-style evaluator harness is interesting.
- **Relevance**: The `.agents/` directory with cross-platform skill definitions and the gitagent format are important ecosystem signals. The token-budget-advisor could inform `meta/plugin-optimizer` improvements.

### get-shit-done (90 commits, v1.30→1.31)

- **Surface**: New commands: `gsd:docs-update`, `gsd:secure-phase`, `gsd:reapply-patches`. New GSD SDK for headless CLI operation. New agents: `gsd-security-auditor`, `gsd-doc-verifier`, `gsd-doc-writer`. Security-first enforcement layer. Schema drift detection. Scope reduction detection in planner. Worktree isolation toggle. CodeRabbit integration.
- **Evolution**: Three major themes: (1) SDK/headless mode — GSD can now be driven programmatically without interactive patterns. (2) Security hardening — dedicated security phase, verification artifacts, threat-model-anchored verification. (3) Autonomous execution — `--only N` flag for single-phase, `--chain` for discuss+plan+execute, `--full` for all phases.
- **Signal vs noise**: The headless SDK and autonomous execution flags are significant. Security-first enforcement with verification artifacts is a strong pattern. Commands → skills migration for Claude Code 2.1.88+ compatibility is an ecosystem signal.
- **Relevance**: The headless SDK pattern and autonomous execution flags could inspire `workflow/complex-task` improvements. The scope reduction detection is a valuable planning guardrail idea.

### gstack (39 commits, v0.11→0.15)

- **Surface**: New skills: `/design-html` (Pretext-native HTML from mockups), `/checkpoint`, `/health`. New features: Session Intelligence Layer (context recovery), Review Army (parallel specialist reviewers), design binary for UI mockup generation, composable skills (INVOKE_SKILL resolver), GStack Learns (per-project self-learning). Added Factory Droid compatibility. Chrome extension + sidebar agent. GitLab support.
- **Evolution**: Fastest-evolving vendor. Key shifts: (1) Composable skills with INVOKE_SKILL resolver — skills can invoke other skills. (2) Session Intelligence — checkpoint + health + context recovery. (3) User sovereignty — AI recommends, users decide. (4) Headed mode with browser sidebar agent. (5) Recursive self-improvement infrastructure (operational learning).
- **Signal vs noise**: Almost all signal. Composable skills, session intelligence, and recursive self-improvement are leading-edge patterns.
- **Relevance**: **High**: (1) Composable skills via INVOKE_SKILL is a fundamental architecture pattern. (2) Session Intelligence (/checkpoint + /health) could be ported to `workflow/catchup`. (3) Review Army (parallel specialist reviewers) aligns with compound-engineering's adversarial review. (4) User sovereignty principle is worth adopting.

### lean-spec (2 commits)

- **Surface**: LeanSpec positioning spec and Codervisor vision. Hierarchical export.
- **Evolution**: Strategic positioning docs only.
- **Signal vs noise**: No workflow evolution. Noise.
- **Relevance**: None.

### oh-my-claudecode (154 commits, v4.9.2→4.9.3)

- **Surface**: Major focus on bug fixes and hardening. Korean i18n expansion (transliteration maps). Obsidian integration (added then reverted). XDG path support. Progressive disclosure for project-memory injection. Auto-detect terminal width for HUD.
- **Evolution**: Stability and correctness phase — extensive bug hunting (30+ verified bugs fixed), race condition fixes, file locking across team operations, security hardening (shell injection prevention, prototype pollution guards). The team orchestration system received significant hardening.
- **Signal vs noise**: The team orchestration hardening and progressive disclosure for memory injection are the key signals. Korean i18n and dist rebuilds are noise.
- **Relevance**: Low immediate porting value, but the team orchestration patterns (file locking, inbox dedup, worker registration) are reference material for any future multi-agent work.

### ouroboros (38 commits, v0.26→0.27)

- **Surface**: New `publish` skill (Seed → GitHub Issues bridge). New `config` and `uninstall` CLI commands. New MCPBridge module for MCP server-to-server communication. Task worktrees enforced for mutating workflows.
- **Evolution**: Two key shifts: (1) MCP server-to-server communication via MCPBridge — enables skill-to-MCP composition. (2) PM (Product Manager) mode maturation — completion scoring, DECIDE_LATER question routing, interview adapter backends.
- **Signal vs noise**: MCPBridge and task worktree enforcement are real architectural evolution. PM mode improvements are incremental but directionally significant.
- **Relevance**: The MCPBridge pattern (MCP server-to-server communication) is a novel integration approach worth monitoring. Task worktree enforcement for mutating workflows aligns with our worktree usage.

### planning-with-files (0 commits)

- **Surface**: Only a `.pyc` cache file changed.
- **Evolution**: None.
- **Relevance**: None.

### spec-kit (29 commits, v0.4.3→0.4.4)

- **Surface**: New community extensions: `plan-review-gate`, `spec-kit-onboard`, `MAQA` (7 extensions), `product-forge`, `superpowers bridge`, 5 lifecycle extensions, `fix-findings`. Built full extension/plugin architecture: Stage 1 (base classes + registry), Stage 2 (Copilot integration), Stage 3 (19 agents migrated to plugin architecture), Stage 4 (TOML integrations — Gemini + Tabnine).
- **Evolution**: The defining shift: built a formal extension system with manifest, registry, and staged migration of all agents into plugins. Now supports Copilot, Gemini, Tabnine, AMP, Auggie, Bob, and more through integration plugins. Community extension catalog growing rapidly.
- **Signal vs noise**: The 4-stage plugin architecture migration is the most important evolution. Community catalog growth is organic validation.
- **Relevance**: The extension system architecture (manifest + registry + staged migration) is a reference pattern for `1st-cc-plugin`'s plugin system if we ever need cross-tool integration support.

### superpowers (12 commits, v5.0.7)

- **Surface**: Added Copilot CLI platform detection and tool mapping. OpenCode path fixes. Contributor guidelines with anti-slop guardrails.
- **Evolution**: Platform expansion (Copilot CLI added alongside Claude/Codex/OpenCode). The anti-slop contributor guidelines are notable — they include agent-facing guardrails to prevent low-quality agentic PRs.
- **Signal vs noise**: The Copilot CLI support and anti-slop guidelines are the real signals. Version bump and README edits are noise.
- **Relevance**: We already use superpowers as an upstream. The Copilot CLI tool mapping could be useful if we ever target Copilot. The anti-slop contributor guidelines are a good practice to adopt.

---

## Cross-Vendor Synthesis

### Emerging Patterns

1. **Skills-first architecture**: Multiple vendors (claude-plugins-official, everything-claude-code, get-shit-done) are migrating from `commands/` to `skills/`. This is now the official Anthropic direction. Skills are the primary workflow surface.

2. **Multi-platform portability**: Repos are racing to support Claude Code, Codex, Copilot CLI, OpenCode, Gemini, Windsurf, Factory, Trae, CodeBuddy, Kiro. The `.agents/` directory and `gitagent` format signal convergence toward a cross-harness skill standard.

3. **Adversarial multi-reviewer patterns**: Both compound-engineering and gstack independently developed parallel specialist reviewer armies. This is converging as a best practice for quality gates.

4. **Headless/SDK mode**: get-shit-done and compound-engineering both added headless modes for programmatic invocation. Skills are becoming composable primitives, not just interactive commands.

5. **Session intelligence**: gstack (checkpoint + health + recovery) and oh-my-claudecode (progressive memory disclosure) are both building session awareness infrastructure.

6. **Composable skill invocation**: gstack's INVOKE_SKILL resolver and compound-engineering's headless mode both point toward skills-calling-skills as a fundamental pattern.

### Port Candidates

| Idea | Source | Target in 1st-cc-plugin | Priority |
|------|--------|------------------------|----------|
| Adversarial multi-reviewer agents | compound-engineering, gstack | `quality/review` | High |
| Headless mode for skills | compound-engineering, get-shit-done | Cross-cutting pattern | High |
| Confidence-gated plan deepening | compound-engineering | `workflow/plan` | Medium |
| Session checkpoint + health | gstack | `workflow/catchup` | Medium |
| Scope reduction detection | get-shit-done | `workflow/complex-task` | Medium |
| PRD creation with template variants | dotclaude | `tools/doc-gen` | Medium |
| Token budget advisor | everything-claude-code | `meta/plugin-optimizer` | Low |

### Watch List

1. **Cross-harness skill standards**: The `.agents/` directory, `gitagent` format, and multi-platform plugin manifests are still fragmented. Wait for convergence before porting.
2. **MCP server-to-server (MCPBridge)**: ouroboros's approach is novel but unproven. Monitor adoption.
3. **First-principles thinking skill**: Trellis's reasoning-methodology skill is a unique concept. Wait to see if it proves useful before porting.
4. **Chain-based orchestration**: Claude-Code-Workflow's JSON chain definitions are interesting but tightly coupled to their system. Watch for patterns that generalize.
5. **Self-hosted skill registries**: Both Trellis and spec-kit are building decentralized distribution. This may become important if the official marketplace evolves.
