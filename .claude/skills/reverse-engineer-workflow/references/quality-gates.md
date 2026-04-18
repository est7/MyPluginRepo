# Quality Gates — Report Self-Validation

After generating the forensics report, verify it passes ALL gates below. A report that fails any MUST gate is incomplete.

## MUST Gates

| # | Gate | Pass Condition |
|---|------|---------------|
| A | **Source Inventory** | Report contains a classified source inventory (overview / execution / prompt / enforcement / evolution) |
| B | **Prompt Traceability** | Every major role (implementer, reviewer, planner, orchestrator) has a prompt catalog entry with `repo_path` and `quote_excerpt` |
| C | **Object Model** | At least 3 first-class entities identified with producer, consumer, and lifecycle |
| D | **State Machine** | Workflow reconstructed as phases with entry/exit conditions, not a flat step list |
| E | **Enforcement Audit** | Every key constraint classified as Hard / Soft / Unenforced with evidence |
| F | **Micro + Macro Split** | Report contains BOTH micro design highlights AND macro philosophy analysis |
| G | **Failure Modes** | At least 3 failure modes identified with evidence — report is not praise-only |
| H | **Migration Output** | Transfer recommendations present with Direct / Inspired / Non-transferable ratings and rationale |

## SHOULD Gates

| # | Gate | Pass Condition |
|---|------|---------------|
| I | **Evidence Level** | Claims marked as `direct` or `inferred`; inferred claims list their basis |
| J | **Context Strategy** | Context isolation between controller / implementer / reviewer analyzed |
| K | **Cross-Cutting Map** | Interconnections between prompt ↔ skill ↔ gate ↔ test documented |
| L | **Must-Build Enforcement** | Mechanisms that are soft-enforced upstream but should be hard-enforced in your system are flagged |

## How to Use

Run this checklist as the final step before writing the report to `docs/research/`. If a MUST gate fails, go back to the relevant phase and fill the gap before outputting.
