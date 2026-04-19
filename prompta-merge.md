这是你(claude)根据我们的计划出的从 1.6-2.0 的方案
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/claude-roadmap-review/v1_6-draft
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/claude-roadmap-review/claude-00-executive-and-baseline.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/claude-roadmap-review/claude-01-source-findings.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/claude-roadmap-review/claude-02-vendor-comparison.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/claude-roadmap-review/claude-03-roadmap-v1.6.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/claude-roadmap-review/claude-04-roadmap-v1.7.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/claude-roadmap-review/claude-05-roadmap-v1.8.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/claude-roadmap-review/claude-06-roadmap-v1.9.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/claude-roadmap-review/claude-07-roadmap-v2.0.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/claude-roadmap-review/claude-08-tdd-implementation-plan.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/claude-roadmap-review/claude-09-docs-rewrites.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/claude-roadmap-review/claude-10-appendix.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/claude-roadmap-review/README.md


,这是 codex 出的方案: /Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/codex-roadmap-review/codex-00-executive-and-baseline.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/codex-roadmap-review/codex-01-source-findings.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/codex-roadmap-review/codex-02-vendor-comparison.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/codex-roadmap-review/codex-03-roadmap-v1.6.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/codex-roadmap-review/codex-04-roadmap-v1.7.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/codex-roadmap-review/codex-05-roadmap-v1.8.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/codex-roadmap-review/codex-06-roadmap-v1.9.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/codex-roadmap-review/codex-07-roadmap-v2.0.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/codex-roadmap-review/codex-08-tdd-implementation-plan.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/codex-roadmap-review/codex-09-docs-rewrites.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/codex-roadmap-review/codex-10-appendix.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/codex-roadmap-review/README.md


,这是 gemini 出的方案:

/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/gemini-roadmap-review/README.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/gemini-roadmap-review/gemini-00-executive-and-baseline.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/gemini-roadmap-review/gemini-01-source-findings.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/gemini-roadmap-review/gemini-02-vendor-comparison.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/gemini-roadmap-review/gemini-03-roadmap-v1.6.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/gemini-roadmap-review/gemini-04-roadmap-v1.7.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/gemini-roadmap-review/gemini-05-roadmap-v1.8.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/gemini-roadmap-review/gemini-06-roadmap-v1.9.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/gemini-roadmap-review/gemini-07-roadmap-v2.0.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/gemini-roadmap-review/gemini-08-tdd-implementation-plan.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/gemini-roadmap-review/gemini-09-docs-rewrites.md
/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs/gemini-roadmap-review/gemini-10-appendix.md




我想我们应该把这三份方案进行合并,我应该怎么写 prompt


 <task>
  Merge the three roadmap review sets into one synthesized review set.

  Create exactly these 11 files inside merged-roadmap-review:
  - README.md
  - merged-00-executive-and-baseline.md
  - merged-01-source-findings.md
  - merged-02-vendor-comparison.md
  - merged-03-roadmap-v1.6.md
  - merged-04-roadmap-v1.7.md
  - merged-05-roadmap-v1.8.md
  - merged-06-roadmap-v1.9.md
  - merged-07-roadmap-v2.0.md
  - merged-08-tdd-implementation-plan.md
  - merged-09-docs-rewrites.md
  - merged-10-appendix.md

  Each merged file must preserve the purpose of the corresponding chapter while synthesizing the Claude, Codex, and Gemini versions into one
  reviewable document.
  </task>

  <constraints>
  - Read all corresponding source files before writing each merged chapter.
  - Merge shared conclusions into one clean canonical narrative.
  - Do not silently resolve material disagreements.
  - When the three plans materially differ, add an explicit section named "Divergence" with this structure:
    - Claude:
    - Codex:
    - Gemini:
    - Decision needed:
  - Only mark divergences that change scope, sequencing, implementation strategy, testing strategy, docs rewrites, vendor conclusions, or
  delivery risk. Ignore wording-only differences.
  - Do not invent roadmap items, milestones, evidence, or rationale not present in at least one source document.
  - Do not add extra files beyond the 11 requested.
  - Keep the documents concise, technical, and review-ready.
  - Prefer traceability over stylistic polish when those conflict.
  - Only make changes directly requested. Do not add extra files, abstractions, or features.
  </constraints>

  <process>
  1. Read the three README files and all matching 00-10 chapter files.
  2. Build an internal chapter-by-chapter map of consensus vs material divergence.
  3. Write the 11 merged files in merged-roadmap-review.
  4. In README.md, explain the merge method, file mapping, and where unresolved divergences remain.
  5. Self-review the merged set for missing chapters, unsupported claims, and any silent arbitration.
  </process>

  <output_format>
  When finished, report in under 250 words:
  1. The exact files created.
  2. A chapter-by-chapter list of unresolved divergences.
  3. Any chapter where the source material was structurally inconsistent or insufficient.
  </output_format>

  <stop_conditions>
  Stop and ask before:
  - modifying any file outside merged-roadmap-review
  - deleting or renaming any existing file
  - collapsing a material disagreement into a single recommendation without attribution
  - adding any roadmap phase or version not present in the source sets
  </stop_conditions>

  <success_criteria>
  A successful result is:
  - all 11 merged files created
  - consensus content merged cleanly
  - real disagreements preserved explicitly
  - no unsupported decisions made on my behalf
  - no edits outside the new output directory
  </success_criteria>
