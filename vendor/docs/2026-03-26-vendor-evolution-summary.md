# 2026-03-26 Vendor Evolution Summary

- Base root commit: `HEAD^` of vendor refresh commit `fd9d388`
- Head root commit: `HEAD` at `fd9d388`
- Raw source: [2026-03-26-vendor-evolution-raw.md](./2026-03-26-vendor-evolution-raw.md)
- Scope: 15 updated `vendor/*` submodules

This summary filters for skill surface changes, workflow entry-point changes, orchestration model changes, and packaging shifts. It intentionally ignores pure release churn unless it changes how users actually work.

## Emerging Patterns

- Multi-agent workflow repos are converging on thinner orchestrators plus more specialized subagents. `get-shit-done`, `Claude-Code-Workflow`, and `compound-engineering-plugin` all moved in that direction.
- Codex support is becoming first-class instead of a side path. `Trellis`, `Claude-Code-Workflow`, `BMAD-METHOD`, and `spec-kit` all show stronger Codex-aware skill packaging or execution semantics.
- Workflow quality loops are getting more explicit. Verification, audit, compliance, review personas, canary checks, and diagnostics are now first-class workflow phases rather than ad hoc advice.
- Plugin ecosystems are shifting from "bag of prompts" to versioned workflow products with schema, config, status lines, and install-time metadata.

## Per Vendor

## `vendor/BMAD-METHOD`

- Surface: `quick-dev` was hardened and `bmad-help` was rewritten as a more outcome-oriented core skill.
- Evolution: the repo is reducing prompt ambiguity and tightening the path from spec naming to task completion tracking.
- Relevance: useful reference for turning helper skills into stronger execution entry points, especially around self-check gates.

## `vendor/Claude-Code-Workflow`

- Surface: added `workflow-research-agent`, expanded `analyze-with-file`, introduced universal team task schema, and moved Codex agent definitions to TOML.
- Evolution: the system is standardizing agent coordination around `spawn_agent + wait_agent`, adding delegation locks, and making traceability part of analysis workflows.
- Relevance: strong reference for any future multi-agent orchestration plugin in `1st-cc-plugin`, especially around coordination contracts and anti-ambiguity guards.

## `vendor/Trellis`

- Surface: added shared agent skills, Codex agent support, status line hooks, and branch-aware session records.
- Evolution: moved from a session helper toward a fuller agent operating layer with persistent session state and cross-runtime support.
- Relevance: valuable for session memory, status line, and lightweight cross-agent coordination patterns.

## `vendor/ccg-workflow`

- Surface: command templates and wrapper behavior were refined around progress output, Gemini transport, and resume semantics.
- Evolution: mostly reliability work, but it clearly strengthens execution continuity for long-running or resumed workflows.
- Relevance: useful if we want stronger CLI/session handoff behavior; lower signal for skill design itself.

## `vendor/claude-code-quickstart`

- Surface: portable Node.js detection and bootstrap dependency cleanup.
- Evolution: bootstrap ergonomics improved, but there was no major new workflow surface in this update.
- Relevance: minor reference for setup hardening, not a workflow direction setter.

## `vendor/compound-engineering-plugin`

- Surface: `ce:review-beta` and planning betas were promoted, document review became persona-driven, git helper skills were added, and a new onboarding skill appeared.
- Evolution: the repo is consolidating around stable conductor-led review/planning flows, with more structured persona pipelines and less manual agent wiring.
- Relevance: high-value reference for review workflow design, especially stable-vs-beta lifecycle and persona review lanes.

## `vendor/everything-claude-code`

- Surface: added `skill-comply`, six gap-closing skills, a Kiro agent/skill layer, and major ECC2 control-plane features.
- Evolution: the repo is evolving from a large skill pack into a true control plane with observability, risk scoring, live streaming, recovery, and platform-specific runtime surfaces.
- Relevance: useful as a watchlist repo for breadth and instrumentation, but many changes are product-platform heavy rather than directly portable.

## `vendor/get-shit-done`

- Surface: major additions around codebase mapping, research, requirements, roadmap generation, execute/verify loops, milestone audit, debugger/researcher/executor/verifier agents, and parallel execution.
- Evolution: this is the clearest example of a workflow system becoming a disciplined operating system: thin orchestrator commands, explicit artifacts, dedicated subagents, verification loops, and dependency-aware execution.
- Relevance: one of the strongest upstream references for workflow evolution. Especially worth studying for plan-to-execute-to-verify loops and parallelization-aware planning.

## `vendor/gstack`

- Surface: stronger autoplan/canary/benchmark surfaces, Codex compatibility work, outside-voice design critique, and tighter office-hours/review flows.
- Evolution: the repo is deepening its "software factory" model through cross-model critique and sharper release/readiness gates.
- Relevance: high signal for leadership-review, outside-voice critique, and shipping-readiness workflow patterns.

## `vendor/lean-spec`

- Surface: `github-integration` and `parallel-worktrees` skill surfaces matured; CI tracking was moved into `/watch-ci`; MCP was removed.
- Evolution: the repo is narrowing toward stronger GitHub/project execution flows and less dependency on its earlier MCP path.
- Relevance: useful reference for parallel worktree coordination and for slimming repo-level guidance into focused skills.

## `vendor/oh-my-claudecode`

- Surface: the range is large, but the visible signal is broad expansion of slash commands, background tasking, plugin metadata, and agent runtime layers.
- Evolution: it appears to have grown from a smaller command pack into a much richer plugin-and-agent platform with stronger execution surfaces.
- Relevance: keep as a watchlist repo; this update range is too large for precise conclusions without a narrower diff window.

## `vendor/ouroboros`

- Surface: multi-agent plugin packaging remains active, but this range leans more toward release, build, and security hardening than new workflow concepts.
- Evolution: the workflow model looks stable; the notable change is supply-chain defensiveness and release pipeline hardening.
- Relevance: moderate reference for secure packaging, lower signal for new skill ideas this cycle.

## `vendor/paul`

- Surface: `init-project`, `plan-phase`, `apply-phase`, `unify-phase`, and `verify-work` were touched together under a v1.2 "Quality & Depth" push.
- Evolution: the repo is deepening its internal quality loop rather than adding many new surfaces.
- Relevance: good compact reference for strengthening phase transitions without blowing up surface area.

## `vendor/planning-with-files`

- Surface: added analytics workflow templates.
- Evolution: small but clear expansion from generic planning into analytics-specific planning artifacts.
- Relevance: modest signal, but a good example of adding domain-specific workflow templates without changing the core system.

## `vendor/spec-kit`

- Surface: `analyze`/`clarify` templates, checkpoint extension, native Codex fallback, and spec template fixes all changed.
- Evolution: the repo is improving spec execution continuity and Codex compatibility while tightening the base template contract.
- Relevance: important for spec workflow interoperability, especially if we want spec templates that behave well across runtimes.

## Port Candidates

- Thin orchestrator + dedicated specialist agents: strongest references are `get-shit-done` and `Claude-Code-Workflow`.
- Persona-based review lanes: strongest reference is `compound-engineering-plugin`.
- Cross-model outside voice / second-opinion workflow: strongest reference is `gstack`.
- Session context plus status line as workflow primitives: strongest reference is `Trellis`.
- Parallel-aware planning and execution metadata: strongest references are `get-shit-done`, `lean-spec`, and `spec-kit`.

## Watch List

- `vendor/everything-claude-code`: very active, but many changes are platform/control-plane level; revisit after another cycle.
- `vendor/oh-my-claudecode`: update range was too wide this cycle; next time compare a narrower commit window.
- `vendor/claude-code-quickstart`: useful bootstrap repo, but not currently a major source of workflow evolution.

## Notes

- `vendor/dotclaude` is not included in this report because it is currently a new vendor onboarding change, not part of the committed vendor refresh range.
- For the next cycle, keep the report window narrow per vendor so large historical jumps do not dilute the workflow signal.
