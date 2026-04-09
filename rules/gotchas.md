# Gotchas

## 2026-04-07

- When adding a new skill under a plugin in `1st-cc-plugin`, update the plugin's `.claude-plugin/plugin.json` registration and the plugin README in the same change. Adding only the skill directory leaves the capability undiscoverable and the public interface documentation stale.
- When the user asks for workflow design advice based on reference materials, start from the research reports and upstream source/README for those references. Do not anchor the analysis on local in-progress workflow docs first, especially when those local docs are incomplete or derivative.

## 2026-04-08

- When collapsing an alternate workflow draft into a diff document, preserve the draft's concrete mechanisms, schemas, and phase-level implementation snippets. Do not replace a concrete design with only abstract summaries of “what changed”; the diff document must still be implementation-useful.

## 2026-04-09

- When judging whether a legacy docs directory can be deleted, verify semantic absorption, not just filename alignment. First confirm the new docs carry the old directory's concrete mechanisms and only block deletion for real unmatched content or live references.
