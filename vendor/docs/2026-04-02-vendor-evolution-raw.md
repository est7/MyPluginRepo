# Vendor Evolution Report

- Base: `805ab186bf953d1075c7eb2c603b689833442303`
- Head: `de66d87`
- Updated vendors: `17`

## `vendor/BMAD-METHOD`

- Range: `819d373e2ecd..07d72394fdcc`
- Commit count: `22`

### Commits

- 3d8a89c feat: add .claude-plugin marketplace and plugin metadata (#2136)
- ed9dea9 refactor: consolidate plugin.json metadata into marketplace.json (#2137)
- 1040c3c fix: correctly resolve output_folder paths outside project root (#2132)
- 513f440 refactor(installer): restructure installer with clean separation of concerns (#2129)
- c91db0d fix: revert bmb module-definition path to src/module.yaml (#2146)
- e0ea6a0 fix: support skills/ folder as module source location (#2149)
- fa909a8 feat: add Junie platform support (#2142)
- abfc56b feat: add bmad-prfaq skill as alternative analysis path (#2157)
- aae6ddb fix: remove ancestor_conflict_check from all platforms (#2158)
- 04513e5 feat(installer): restore KiloCoder support and installer (#2151)
- 7dd49a4 refactor: remove bmad-init skill, standardize config loading (#2159)
- ce9c664 refactor(party-mode): consolidate into single SKILL.md with real subagents (#2160)
- 4b1026b fix(party-mode): clarify solo mode and improve response presentation (#2164)
- 3980e57 feat(quick-dev): one-shot route generates spec trace file (#2121)
- 2302d9c docs(fr): translate output folder path resolution section (#2140)
- 1f99eb0 fix: preserve local custom module sources during quick update (#2172)
- 2c5436f style: update docs theme to match bmadcode.com Ghost blog (#2176)
- 1aa0903 chore(agents): remove Barry quick-flow-solo-dev agent (#2177)
- 1b776f5 feat: add bmad-checkpoint-preview skill (#2145)
- 2ea917e fix(checkpoint): address review findings from adversarial triage (#2180)
- 7ef45d4 docs(checkpoint): add explainer page and workflow diagram (#2183)
- 07d7239 fix(checkpoint): add explicit HALT before decision menu in wrapup step (#2184)

### Workflow Signals

- `.claude-plugin/marketplace.json`
- `.github/workflows/publish.yaml`
- `src/bmm-skills/1-analysis/bmad-agent-analyst/SKILL.md`
- `src/bmm-skills/1-analysis/bmad-agent-tech-writer/SKILL.md`
- `src/bmm-skills/1-analysis/bmad-prfaq/SKILL.md`
- `src/bmm-skills/1-analysis/bmad-prfaq/agents/artifact-analyzer.md`
- `src/bmm-skills/1-analysis/bmad-prfaq/agents/web-researcher.md`
- `src/bmm-skills/1-analysis/bmad-product-brief/SKILL.md`
- `src/bmm-skills/2-plan-workflows/bmad-agent-pm/SKILL.md`
- `src/bmm-skills/2-plan-workflows/bmad-agent-ux-designer/SKILL.md`
- `src/bmm-skills/3-solutioning/bmad-agent-architect/SKILL.md`
- `src/bmm-skills/4-implementation/bmad-agent-dev/SKILL.md`
- `src/bmm-skills/4-implementation/bmad-agent-qa/SKILL.md`
- `src/bmm-skills/4-implementation/bmad-agent-quick-flow-solo-dev/SKILL.md`
- `src/bmm-skills/4-implementation/bmad-agent-sm/SKILL.md`
- `src/bmm-skills/4-implementation/bmad-checkpoint-preview/SKILL.md`
- `src/core-skills/bmad-advanced-elicitation/SKILL.md`
- `src/core-skills/bmad-distillator/SKILL.md`
- `src/core-skills/bmad-init/SKILL.md`
- `src/core-skills/bmad-party-mode/SKILL.md`

### All Changed Files

- `.claude-plugin/marketplace.json`
- `.github/workflows/publish.yaml`
- `docs/explanation/analysis-phase.md`
- `docs/explanation/checkpoint-preview.md`
- `docs/fr/how-to/non-interactive-installation.md`
- `docs/fr/reference/agents.md`
- `docs/how-to/non-interactive-installation.md`
- `docs/reference/agents.md`
- `docs/reference/commands.md`
- `docs/reference/workflow-map.md`
- `docs/tutorials/getting-started.md`
- `docs/zh-cn/how-to/non-interactive-installation.md`
- `docs/zh-cn/reference/agents.md`
- `package.json`
- `src/bmm-skills/1-analysis/bmad-agent-analyst/SKILL.md`
- `src/bmm-skills/1-analysis/bmad-agent-tech-writer/SKILL.md`
- `src/bmm-skills/1-analysis/bmad-document-project/workflow.md`
- `src/bmm-skills/1-analysis/bmad-prfaq/SKILL.md`
- `src/bmm-skills/1-analysis/bmad-prfaq/agents/artifact-analyzer.md`
- `src/bmm-skills/1-analysis/bmad-prfaq/agents/web-researcher.md`
- `src/bmm-skills/1-analysis/bmad-prfaq/assets/prfaq-template.md`
- `src/bmm-skills/1-analysis/bmad-prfaq/bmad-manifest.json`
- `src/bmm-skills/1-analysis/bmad-prfaq/references/customer-faq.md`
- `src/bmm-skills/1-analysis/bmad-prfaq/references/internal-faq.md`
- `src/bmm-skills/1-analysis/bmad-prfaq/references/press-release.md`
- `src/bmm-skills/1-analysis/bmad-prfaq/references/verdict.md`
- `src/bmm-skills/1-analysis/bmad-product-brief/SKILL.md`
- `src/bmm-skills/1-analysis/bmad-product-brief/bmad-manifest.json`
- `src/bmm-skills/1-analysis/research/bmad-domain-research/workflow.md`
- `src/bmm-skills/1-analysis/research/bmad-market-research/workflow.md`
- `src/bmm-skills/1-analysis/research/bmad-technical-research/workflow.md`
- `src/bmm-skills/2-plan-workflows/bmad-agent-pm/SKILL.md`
- `src/bmm-skills/2-plan-workflows/bmad-agent-ux-designer/SKILL.md`
- `src/bmm-skills/2-plan-workflows/bmad-create-prd/workflow.md`
- `src/bmm-skills/2-plan-workflows/bmad-create-ux-design/workflow.md`
- `src/bmm-skills/2-plan-workflows/bmad-edit-prd/steps-e/step-e-01-discovery.md`
- `src/bmm-skills/2-plan-workflows/bmad-edit-prd/steps-e/step-e-01b-legacy-conversion.md`
- `src/bmm-skills/2-plan-workflows/bmad-edit-prd/steps-e/step-e-02-review.md`
- `src/bmm-skills/2-plan-workflows/bmad-edit-prd/steps-e/step-e-03-edit.md`
- `src/bmm-skills/2-plan-workflows/bmad-edit-prd/steps-e/step-e-04-complete.md`
- ... and 140 more files

## `vendor/Claude-Code-Workflow`

- Range: `a45c672d3069..0f8e801d6e67`
- Commit count: `35`

### Commits

- 25d4764 chore: bump version to 7.2.22
- e83063b fix: enable remote dashboard access by acquiring auth cookie on startup
- 3d39ac6 chore: bump version to 7.2.23
- e7d5914 fix: quote YAML frontmatter descriptions containing colons in SKILL.md files
- 88ea7fc refactor: deep Codex v4 API conversion for all 20 team skills
- 6565502 chore: bump version to 7.2.24
- 662cff5 Remove outdated coordinator, developer, reviewer, tester roles and associated commands, along with pipeline definitions and team configuration files to streamline the iterative development process.
- 45212e1 Merge pull request #144 from bluzername/fix/yaml-frontmatter-quoting
- 4fb983c Merge remote-tracking branch 'origin/main' - resolve spec-generator SKILL.md conflict
- ffae6dd fix: quote description in team-designer scaffold template to prevent YAML parse errors
- 367466c refactor: streamline CLI tools usage documentation by consolidating sections and enhancing clarity
- 6be78cb chore: bump version to 7.2.25
- e30fc35 docs: add workflow session awareness spec to CLAUDE.md
- 55a89d6 docs: add workflow session awareness spec to AGENTS.md
- bb0346e docs: add core_memory session awareness to AGENTS.md
- bbceef3 docs: remove core_memory section from AGENTS.md
- 21a6d29 feat: add json_builder tool with schema-aware JSON construction and validation
- 92dbde6 docs: 删除 prep-cycle.md 和 prep-plan.md 文件
- 885eb18 chore: bump version to 7.2.26
- 56c0429 fix: enable dynamic inner_loop for parallel task execution across 6 team skills
- 1803f2e chore: bump version to 7.2.27
- 46d4d4b feat: add 4 new UI team skills and enhance 2 existing with Impeccable design standards
- cac126e feat: port 4 new UI team skills to Codex v4 format
- 360a031 docs: add Impeccable acknowledgment to README
- 67ff3fe feat: add investigate, security-audit, ship skills (Claude + Codex)
- de7ec94 feat: enhance skill templates, hooks, CLI routes, and settings UI
- da643e6 chore: bump version to 7.2.28
- 2ca8708 feat: refactor API calls to use fetchApi for CSRF token handling in Unsplash and Settings pages
- b88bf5e refactor: unify agent API to Codex v4 across all skills
- 4092c89 chore: bump version to 7.2.29
- 6f6d9cc chore: remove unused WeChat group QR code image
- a034e74 feat: Implement auto mode for CCW chain execution
- ca70404 Refactor code structure for improved readability and maintainability
- 902c5c2 fix: revert json_builder references from agents/skills, add schema fallback
- 0f8e801 chore: bump version to 7.2.30

### Workflow Signals

- `.ccw/workflows/cli-templates/schemas/plan-overview-base-schema.json`
- `.ccw/workflows/cli-templates/schemas/task-schema.json`
- `.ccw/workflows/cli-tools-usage.md`
- `.claude/agents/action-planning-agent.md`
- `.claude/skills/_shared/SKILL-DESIGN-SPEC.md`
- `.claude/skills/brainstorm/SKILL.md`
- `.claude/skills/ccw-chain/SKILL.md`
- `.claude/skills/ccw-chain/chains/ccw-cycle.json`
- `.claude/skills/ccw-chain/chains/ccw-exploration.json`
- `.claude/skills/ccw-chain/chains/ccw-issue.json`
- `.claude/skills/ccw-chain/chains/ccw-lightweight.json`
- `.claude/skills/ccw-chain/chains/ccw-main.json`
- `.claude/skills/ccw-chain/chains/ccw-standard.json`
- `.claude/skills/ccw-chain/chains/ccw-team.json`
- `.claude/skills/ccw-chain/chains/ccw-with-file.json`
- `.claude/skills/ccw-chain/phases/analyze-with-file.md`
- `.claude/skills/ccw-chain/phases/brainstorm-with-file.md`
- `.claude/skills/ccw-chain/phases/brainstorm/SKILL.md`
- `.claude/skills/ccw-chain/phases/brainstorm/phases/01-mode-routing.md`
- `.claude/skills/ccw-chain/phases/brainstorm/phases/02-artifacts.md`

### All Changed Files

- `.ccw/specs/architecture-constraints.md`
- `.ccw/workflows/cli-templates/schemas/plan-overview-base-schema.json`
- `.ccw/workflows/cli-templates/schemas/task-schema.json`
- `.ccw/workflows/cli-tools-usage.md`
- `.claude/CLAUDE.md`
- `.claude/agents/action-planning-agent.md`
- `.claude/skills/_shared/SKILL-DESIGN-SPEC.md`
- `.claude/skills/brainstorm/SKILL.md`
- `.claude/skills/ccw-chain/SKILL.md`
- `.claude/skills/ccw-chain/chains/ccw-cycle.json`
- `.claude/skills/ccw-chain/chains/ccw-exploration.json`
- `.claude/skills/ccw-chain/chains/ccw-issue.json`
- `.claude/skills/ccw-chain/chains/ccw-lightweight.json`
- `.claude/skills/ccw-chain/chains/ccw-main.json`
- `.claude/skills/ccw-chain/chains/ccw-standard.json`
- `.claude/skills/ccw-chain/chains/ccw-team.json`
- `.claude/skills/ccw-chain/chains/ccw-with-file.json`
- `.claude/skills/ccw-chain/phases/analyze-with-file.md`
- `.claude/skills/ccw-chain/phases/brainstorm-with-file.md`
- `.claude/skills/ccw-chain/phases/brainstorm/SKILL.md`
- `.claude/skills/ccw-chain/phases/brainstorm/phases/01-mode-routing.md`
- `.claude/skills/ccw-chain/phases/brainstorm/phases/02-artifacts.md`
- `.claude/skills/ccw-chain/phases/brainstorm/phases/03-role-analysis.md`
- `.claude/skills/ccw-chain/phases/brainstorm/phases/04-synthesis.md`
- `.claude/skills/ccw-chain/phases/collaborative-plan-with-file.md`
- `.claude/skills/ccw-chain/phases/debug-with-file.md`
- `.claude/skills/ccw-chain/phases/integration-test-cycle.md`
- `.claude/skills/ccw-chain/phases/issue-convert-to-plan.md`
- `.claude/skills/ccw-chain/phases/issue-discover.md`
- `.claude/skills/ccw-chain/phases/issue-execute.md`
- `.claude/skills/ccw-chain/phases/issue-from-brainstorm.md`
- `.claude/skills/ccw-chain/phases/issue-plan.md`
- `.claude/skills/ccw-chain/phases/issue-queue.md`
- `.claude/skills/ccw-chain/phases/refactor-cycle.md`
- `.claude/skills/ccw-chain/phases/review-cycle/SKILL.md`
- `.claude/skills/ccw-chain/phases/review-cycle/phases/review-fix.md`
- `.claude/skills/ccw-chain/phases/review-cycle/phases/review-module.md`
- `.claude/skills/ccw-chain/phases/review-cycle/phases/review-session.md`
- `.claude/skills/ccw-chain/phases/roadmap-with-file.md`
- `.claude/skills/ccw-chain/phases/spec-generator/SKILL.md`
- ... and 414 more files

## `vendor/Trellis`

- Range: `7658ba6bc8c5..868ba49f70a5`
- Commit count: `8`

### Commits

- 2175525 feat: v0.4.0-beta — self-hosted registry + new skills (#131)
- 2637023 fix(hooks): normalize .current-task path refs across platforms (#130)
- 0041a52 fix(codex): resolve {{PYTHON_CMD}} placeholder in hooks.json for Windows (#132)
- 986bc53 feat(marketplace): add frontend-fullchain-optimization skill (#110)
- 1bf9e61 docs(readme): add WeChat Work & QQ group QR codes, update WeChat group QR (#135)
- 22b1cc7 Merge pull request #134 from Lemonadeccc/frontend-fullchain-optimization
- cb842b3 feat(windsurf): add workflow support for Windsurf
- 868ba49 Merge pull request #137 from itgcl/upstream/feat/windsurf-support

### Workflow Signals

- `.claude/hooks/inject-subagent-context.py`
- `.claude/hooks/ralph-loop.py`
- `.claude/hooks/session-start.py`
- `.claude/hooks/statusline.py`
- `.claude/skills/first-principles-thinking/SKILL.md`
- `.claude/skills/first-principles-thinking/references/axiom-based-reasoning.md`
- `.claude/skills/first-principles-thinking/references/bias-and-debiasing.md`
- `.claude/skills/first-principles-thinking/references/case-studies.md`
- `.claude/skills/first-principles-thinking/references/decomposition-frameworks.md`
- `.claude/skills/first-principles-thinking/references/thinking-models-toolkit.md`
- `.codex/hooks/session-start.py`
- `marketplace/skills/frontend-fullchain-optimization/SKILL.md`
- `packages/cli/src/commands/init.ts`
- `packages/cli/src/templates/claude/hooks/inject-subagent-context.py`
- `packages/cli/src/templates/claude/hooks/ralph-loop.py`
- `packages/cli/src/templates/claude/hooks/session-start.py`
- `packages/cli/src/templates/claude/hooks/statusline.py`
- `packages/cli/src/templates/codex/hooks.json`
- `packages/cli/src/templates/codex/hooks/session-start.py`
- `packages/cli/src/templates/extract.ts`

### All Changed Files

- `.claude/hooks/inject-subagent-context.py`
- `.claude/hooks/ralph-loop.py`
- `.claude/hooks/session-start.py`
- `.claude/hooks/statusline.py`
- `.claude/skills/first-principles-thinking/SKILL.md`
- `.claude/skills/first-principles-thinking/references/axiom-based-reasoning.md`
- `.claude/skills/first-principles-thinking/references/bias-and-debiasing.md`
- `.claude/skills/first-principles-thinking/references/case-studies.md`
- `.claude/skills/first-principles-thinking/references/decomposition-frameworks.md`
- `.claude/skills/first-principles-thinking/references/thinking-models-toolkit.md`
- `.codex/hooks/session-start.py`
- `.opencode/lib/trellis-context.js`
- `.trellis/scripts/common/__init__.py`
- `.trellis/scripts/common/paths.py`
- `.trellis/scripts/common/task_utils.py`
- `.trellis/scripts/multi_agent/start.py`
- `.trellis/scripts/task.py`
- `.trellis/spec/cli/backend/quality-guidelines.md`
- `.trellis/tasks/03-26-frontend-fullchain-optimization-skill/prd.md`
- `.trellis/tasks/03-26-frontend-fullchain-optimization-skill/task.json`
- `.trellis/tasks/archive/2026-03/03-27-self-hosted-gitlab/check.jsonl`
- `.trellis/tasks/archive/2026-03/03-27-self-hosted-gitlab/debug.jsonl`
- `.trellis/tasks/archive/2026-03/03-27-self-hosted-gitlab/implement.jsonl`
- `.trellis/tasks/archive/2026-03/03-27-self-hosted-gitlab/prd.md`
- `.trellis/tasks/archive/2026-03/03-27-self-hosted-gitlab/task.json`
- `.trellis/workspace/taosu/index.md`
- `.trellis/workspace/taosu/journal-4.md`
- `README.md`
- `README_CN.md`
- `assets/qq-group-qr.jpg`
- `assets/wecom-group-qr.png`
- `assets/wx_link4.jpg`
- `docs-site`
- `marketplace/index.json`
- `marketplace/skills/frontend-fullchain-optimization/SKILL.md`
- `packages/cli/src/cli/index.ts`
- `packages/cli/src/commands/init.ts`
- `packages/cli/src/configurators/codex.ts`
- `packages/cli/src/configurators/index.ts`
- `packages/cli/src/configurators/windsurf.ts`
- ... and 40 more files

## `vendor/ccg-workflow`

- Range: `6988f6421a2c..f2ea034890a3`
- Commit count: `15`

### Commits

- 75753fe fix: force pwd/cd to resolve WORKDIR in all 20 command templates
- 9d94b6f fix: Windows ccline statusLine path use ~ instead of %USERPROFILE%
- a8377c4 fix: Gemini CLI hangs on long prompts when CWD is $HOME
- c8f831c fix: static link Linux binaries to remove GLIBC dependency
- 1262dae Merge branch 'main' into fix/gemini-cwd-hang
- 0d997f4 feat: Skill Registry + domain knowledge + impeccable tools + 3 output styles (v1.8.4)
- 93ffe1f chore: bump version to 2.0.0
- 6a6bf8f Merge branch 'main' into fix/gemini-cwd-hang
- a2c1617 feat: configurable model routing for frontend/backend (#121)
- ad56c63 fix: add YAML frontmatter to Skill Registry generated commands (#122)
- ea4cf5d fix: MCP provider preserved during update + optional Impeccable commands (#124, #125)
- ae4a774 Merge pull request #122 from Aliang1337/fix/gemini-cwd-hang
- b1a94dc docs: fix outdated numbers in README (commands 27→29+, tests 134→139)
- 9c4d3e4 docs: add star badge to README for project visibility
- f2ea034 docs: add CCG logo and multi-size assets

### Workflow Signals

- `.github/workflows/build-binaries.yml`
- `src/commands/init.ts`
- `src/commands/menu.ts`
- `templates/commands/agents/team-architect.md`
- `templates/commands/agents/team-qa.md`
- `templates/commands/agents/team-reviewer.md`
- `templates/commands/analyze.md`
- `templates/commands/backend.md`
- `templates/commands/codex-exec.md`
- `templates/commands/debug.md`
- `templates/commands/execute.md`
- `templates/commands/feat.md`
- `templates/commands/frontend.md`
- `templates/commands/optimize.md`
- `templates/commands/plan.md`
- `templates/commands/review.md`
- `templates/commands/spec-impl.md`
- `templates/commands/spec-init.md`
- `templates/commands/spec-plan.md`
- `templates/commands/spec-research.md`

### All Changed Files

- `.github/workflows/build-binaries.yml`
- `CHANGELOG.md`
- `CLAUDE.md`
- `README.md`
- `README.zh-CN.md`
- `assets/logo/ccg-favicon-128.png`
- `assets/logo/ccg-favicon-16.png`
- `assets/logo/ccg-favicon-256.png`
- `assets/logo/ccg-favicon-32.png`
- `assets/logo/ccg-favicon-48.png`
- `assets/logo/ccg-favicon-64.png`
- `assets/logo/ccg-favicon-source.png`
- `assets/logo/ccg-icon-only.png`
- `assets/logo/ccg-logo-1024.png`
- `assets/logo/ccg-logo-128.png`
- `assets/logo/ccg-logo-256.png`
- `assets/logo/ccg-logo-512.png`
- `assets/logo/ccg-logo-cropped.png`
- `assets/logo/ccg-logo-transparent.png`
- `assets/logo/ccg-npm-badge.png`
- `assets/logo/ccg-social-og.png`
- `assets/logo/ccg-social-twitter.png`
- `assets/logo/favicon.ico`
- `codeagent-wrapper/executor.go`
- `package.json`
- `src/commands/init.ts`
- `src/commands/menu.ts`
- `src/i18n/index.ts`
- `src/types/index.ts`
- `src/utils/__tests__/installer.test.ts`
- `src/utils/config.ts`
- `src/utils/installer-data.ts`
- `src/utils/installer-template.ts`
- `src/utils/installer.ts`
- `src/utils/skill-registry.ts`
- `templates/commands/agents/team-architect.md`
- `templates/commands/agents/team-qa.md`
- `templates/commands/agents/team-reviewer.md`
- `templates/commands/analyze.md`
- `templates/commands/backend.md`
- ... and 121 more files

## `vendor/claude-code-quickstart`

- Range: `ab712904655a..b3f0649466bb`
- Commit count: `3`

### Commits

- d3f4071 fix(Bootstrap,OpenSpec,Ui): 统一步骤状态文案 + OpenSpec 改用 npm list 验证
- 9ee293f feat(Ui,Bootstrap,ClaudeConfig): Unicode 边框 + Emoji 状态图标 + thinking 配置补全
- b3f0649 fix(Manage,Bootstrap,ClaudeConfig): 修正 ClaudeConfig 更新回退摘要与文案

### Workflow Signals

- No skill/workflow signal files detected.

### All Changed Files

- `installer/Manage-ClaudeEnv.ps1`
- `installer/core/Bootstrap.ps1`
- `installer/core/Process.ps1`
- `installer/core/Ui.ps1`
- `installer/steps/ClaudeConfig.ps1`
- `installer/steps/NodeJS-Detect.ps1`
- `installer/steps/OpenSpec.ps1`

## `vendor/claude-plugins-official`

- Range: `183a6ca35d5f..b091cb4179d3`
- Commit count: `211`

### Commits

- 4ca561f creating intital scaffolding for claude code plugins
- cecebb1 added readme
- c7fb157 remove readme from external plugins
- 66a9858 Merge branch 'noahz/initial_scaffold'
- 0f1535a simplified example agent
- 6ba8050 updated readme
- ef7ceef fixed readme
- 22d3def Merge pull request #2 from anthropics/noahz/official_language
- 19a119f Update plugins library to include authors (#6)
- 4fee769 Point to external figma plugin (#11)
- ab2b6d0 change to use notion external (#25)
- 75b126f swtiched to external vercel atlassian (#33)
- 68a5c36 added new partners (#36)
- be56d71 Add LSP plugins with inline lspServers configuration
- 1d99e18 Add installation instructions to LSP plugin READMEs
- 4bab8d0 Merge pull request #38 from anthropics/daisy/plugins/add-lsp-plugins
- 5f2db35 Fix hookify plugin import error: No module named 'hookify'
- 6d3752c Merge pull request #39 from anthropics/daisy/plugins/fix-hookify-imports
- 80a2049 Add Ruby LSP plugin with inline lspServers configuration
- 15b07b4 Merge pull request #114 from anthropics/fix/ralph-wiggum-newline-error
- dbc4a77 Add README and setup documentation for Greptile plugin (#122)
- 883f2ba Add Pinecone vector database plugin to marketplace (#133)
- bf48ae6 fix(ralph-wiggum): add :* to allowed-tools pattern to permit arguments (#138)
- 6703e9f Add workflow to auto-close external PRs (#140)
- 44328be Rename ralph-wiggum plugin to ralph-loop per legal guidance (#142)
- 76334d1 Add write permissions for external PR workflow (#143)
- b97f6ea Use collaborator permission check instead of org membership (#147)
- 2fee5cd Add Kotlin LSP plugin for code intelligence
- 113b335 Merge pull request #161 from clackbib/habib/add_kotlin_lsp
- ceb9b72 Add code-simplifier plugin
- 48c6726 Add huggingface-skills plugin to marketplace (#174)
- f1be96f Merge pull request #183 from anthropics/boris/code-simplifier-plugin
- f70b655 Add circleback plugin to marketplace (#209)
- ee2f726 Add superpowers plugin to marketplace (#148)
- 9627620 Add plugin directory submission form link to README (#238)
- a86e346 feat: add claude-code-setup and claude-md-management plugins
- 7d5dcb6 edit claude enablement plugins description
- 3c1e321 add marketplace.json changes
- 6efe831 fix plugin.json description
- 2c255a1 Merge pull request #263 from anthropics/isabella/enablement-plugins
- 146d478 merge slash commands and skills
- e307683 Merge pull request #266 from anthropics/isabella/enablement-plugins
- 2765dd6 Add posthog plugin to marketplace (#299)
- d49ad35 Add coderabbit plugin to marketplace (#300)
- 21256d1 Add artifact plugin
- b7d1051 Add diff-review template to artifact skill
- 09e3d78 Add code-map template to artifact skill
- 54402a7 Replace writing-tool template with document-critique template
- 64e3e0b Merge pull request #304 from anthropics/thariq/add-artifact-plugin
- 14aa275 Add instruction to open artifact in browser after creation
- 4e459fb Rename artifact plugin to playground
- 61d5cc6 Merge pull request #307 from anthropics/thariq/artifact-open-browser
- fa865ab Update marketplace.json for playground rename
- 27d2b86 Merge pull request #308 from anthropics/thariq/artifact-open-browser
- 82d0412 Fix YAML frontmatter parsing errors in agent description fields
- 25617fd Add CI workflow to validate YAML frontmatter in PRs
- 2438937 Use lower-kebab-case for SKILL.md names in hookify and plugin-dev
- 91736b9 Merge pull request #337 from anthropics/fix/yaml-frontmatter-parsing-errors
- 53b22ad Merge pull request #338 from anthropics/dickson/validate-frontmatter-ci
- 236752a Merge pull request #339 from anthropics/dickson/kebab-case-skill-names
- 92ece10 Add sonatype-guide plugin to marketplace (#350)
- 2cd88e7 Add firecrawl plugin to marketplace (#352)
- 86c54b5 feat: update Slack plugin to HTTP transport with OAuth config
- 261ce4f Merge pull request #406 from anthropics/basil/slack-oauth-config
- 30975e6 Add skill-creator plugin
- d7d9ed2 fix(ci): skip frontmatter validation for files nested inside skill content
- ff736a6 Merge pull request #408 from anthropics/kenshiro/add-skill-creator-20260217
- 587fa33 feat(marketplace): add skill-creator plugin to marketplace registry
- 452c387 Merge pull request #411 from anthropics/kenshiro/add-skill-creator-to-marketplace
- 4923f29 Add semgrep plugin to marketplace (#422)
- 8deab84 Add qodo-skills plugin to marketplace (#421)
- aecd4c8 Add Apache 2.0 LICENSE files to all internal plugins
- 6a1de65 Add license note to main README
- aa296ec Merge pull request #431 from anthropics/add-apache-licenses
- eb2cb95 Point slack plugin to Slack's official repo
- 99e11d9 Merge pull request #454 from anthropics/dickson/update-slack
- e05013d chore(skill-creator): update to latest skill-creator
- 55b58ec Merge pull request #457 from anthropics/kenshiro/export-plugins-20260224
- adfc379 fix(ralph-loop): stop hook fails when last assistant block is tool_use
- 8644df9 fix(ralph-loop): isolate loop state to the session that started it
- 028eccf address review: bound grep to tail -n 100; restore explicit error paths
- b7c995d Merge pull request #496 from anthropics/sfishman/ralph-loop-tool-use-fix
- fe41d32 Update webhook closed PR message link to clau.de
- 205b6e0 Update webhook closed PR message link to clau.de (#500)
- 8249477 Add chrome-devtools-mcp to marketplace
- 954edbd Add planetscale to marketplace
- 7657ed1 Add rc to marketplace
- 934cc3b Add adspirer-ads-agent to marketplace
- 41ac301 Add railway to marketplace
- 2a6b21d Add sourcegraph to marketplace
- 9c11aed Add sanity-plugin to marketplace
- 8a89ca3 Add data to marketplace
- 7b7e855 Add legalzoom to marketplace
- 7b67d48 Add mintlify to marketplace
- b3b3549 Add sumup to marketplace
- cdbe8cb Add wix to marketplace
- 4fa2758 Add postman to marketplace
- 7c626d2 Point posthog at consolidated PostHog/ai-plugin repo
- f71d2d9 Add amazon-location-service to marketplace
- 8fda75c Add aws-serverless to marketplace
- 038e989 Add migration-to-aws to marketplace
- b90a056 Add deploy-on-aws to marketplace
- 4fecb30 Add zapier to marketplace
- 7e94c73 Merge pull request #540 from anthropics/add-plugin/postman
- 00f13a5 Merge pull request #106 from obahareth/main
- bd04149 update(plugin-json): point to the correct Semgrep plugin directory (#584)
- b36fd4b Add pagerduty to marketplace (#566)
- aeb25ce Add Apache 2.0 LICENSE to ruby-lsp plugin
- c96abc7 Add Apache 2.0 LICENSE to ruby-lsp plugin
- 61ff000 Merge PR #542: update(plugin-json): posthog — point at consolidated repo
- d726c5e Merge PR #525: add-plugin/chrome-devtools-mcp
- 9750826 Merge PR #526: add-plugin/planetscale
- 92e9c49 Merge PR #527: add-plugin/rc
- 5a5fc14 Merge PR #528: add-plugin/adspirer-ads-agent
- 1d1f304 Merge PR #529: add-plugin/railway
- 159db46 Merge PR #530: add-plugin/sourcegraph
- e0b2429 Merge PR #531: add-plugin/sanity-plugin
- a8e8f7e Merge PR #532: add-plugin/data
- 57fe206 Merge PR #533: add-plugin/legalzoom
- b4178e8 Merge PR #534: add-plugin/mintlify
- 80d85e8 Merge PR #535: add-plugin/sumup
- 616512c Merge PR #536: add-plugin/wix
- 1f25b55 Merge PR #576: add-plugin/amazon-location-service
- fbe0386 Merge PR #577: add-plugin/aws-serverless
- 9febf87 Merge PR #578: add-plugin/migration-to-aws
- 64ce172 Merge PR #579: add-plugin/deploy-on-aws
- 9532734 Merge PR #583: add-plugin/zapier
- ad61a54 Merge pull request #517 from anthropics/claude/slack-update-webhook-link-wikTM
- 50ebf6d Merge pull request #626 from anthropics/add-ruby-lsp-license
- bf62700 Merge pull request #613 from anthropics/add-license-ruby-lsp
- d5c15b8 Merge pull request #628 from anthropics/staging
- 78497c5 updates(staging): merge staging additions into main (#677)
- 6b70f99 docs(plugin-dev): deprecate commands/ in favor of skills/<name>/SKILL.md (#717)
- 1c95fc6 Add imessage channel plugin
- 75e1c5d Add fakechat channel plugin (#738)
- 4796148 Add discord channel plugin (#736)
- 1b33c1d Add telegram channel plugin (#735)
- 3de6a94 Register telegram, discord, fakechat channel plugins (#739)
- 158ef95 Add marketplace.json validation CI workflow (#347)
- f0fdb72 Enforce alphabetical sort on marketplace.json plugins
- 55de7f6 Merge pull request #740 from anthropics/marketplace-sorted
- d53f6ca Remove telegram, discord, and fakechat plugins (#741)
- 7994c27 Revert "Remove telegram, discord, and fakechat plugins (#741)" (#753)
- 3c9bf4f Add math-olympiad skill — adversarial verification for competition math
- 8938650 Add Bun prerequisite to discord and telegram plugin READMEs
- 8908a58 Merge pull request #757 from anthropics/kenneth/add-bun-prereq
- b01fad3 README clarifications from docs walkthrough testing
- 9720278 math-olympiad: forbid web access in deep mode
- c3f6d9e Fix YAML frontmatter — quote description, replace colon with em-dash
- b664e15 Merge pull request #758 from anthropics/docs/readme-clarifications
- 8140fba Lock telegram/discord .env files to owner (chmod 600)
- d687c59 Staging → main: plugin marketplace additions (#730)
- 562a27f Merge pull request #811 from anthropics/kenneth/chmod-env-files
- 90accf6 add(plugin): mcp-server-dev — skills for building MCP servers (#731)
- 9f2a4fe telegram: add error handlers to stop silent polling death
- 2aa90a8 telegram: exit when Claude Code closes the connection
- 1daff5f telegram: retry on 409 Conflict instead of crashing
- 14927ff telegram/discord: make state dir configurable via env var
- 3d8042f Silently return when bot.stop() aborts the setup phase
- 5c58308 discord/telegram: guide assistant to send new reply on completion
- aa71c24 discord: port resilience fixes from telegram
- a7cb39c telegram: add MarkdownV2 parse_mode to reply/edit_message
- 521f858 telegram: add /start /help /status bot commands
- a9bc23d telegram: handle all inbound file types + download_attachment tool
- 9a101ba Restrict bot commands to DMs (security)
- ea382ec Tighten /start and /help copy
- 1636fed Sanitize user-controlled filenames and download path components
- 2bc9dfb Update stripe plugin to use git-subdir source
- af6b2c4 Remove local stripe external plugin
- 757480d Merge remote-tracking branch 'origin/kenneth/telegram-shutdown' into kenneth/channels-rollup
- f3fc62a Merge remote-tracking branch 'origin/kenneth/telegram-409' into kenneth/channels-rollup
- 24a170a Merge remote-tracking branch 'origin/kenneth/channels-state-dir' into kenneth/channels-rollup
- aa4f7c4 Merge remote-tracking branch 'origin/kenneth/discord-edit-notif-guidance' into kenneth/channels-rollup
- 87e0f09 Merge remote-tracking branch 'origin/kenneth/discord-resilience' into kenneth/channels-rollup
- 556b21a Merge remote-tracking branch 'origin/kenneth/telegram-bot-commands' into kenneth/channels-rollup
- 71b102d Merge remote-tracking branch 'origin/kenneth/telegram-bot-commands-795' into kenneth/channels-rollup
- 51bd7bd Merge remote-tracking branch 'origin/kenneth/telegram-all-file-types' into kenneth/channels-rollup
- 802464c Fix frontmatter validation to skip deleted files
- d56d7b6 Merge pull request #755 from anthropics/ralph/add-math-olympiad
- 272de72 Merge branch 'main' into add-imessage-channel
- 252577f Register imessage plugin in marketplace.json
- 6d0053f Add IMESSAGE_APPEND_SIGNATURE env var (default true)
- da61886 Merge pull request #823 from anthropics/claude/slack-add-claude-plugin-marketplace
- 61c0597 Merge pull request #825 from anthropics/kenneth/channels-rollup
- daa84c9 feat(telegram,discord): permission-relay capability + bidirectional handlers
- 15268f0 Merge pull request #833 from anthropics/daisy/plugin-7/channel-permissions
- 0f8c170 Merge remote-tracking branch 'origin/main' into add-imessage-channel
- bfed463 feat(imessage): port permission-relay + lifecycle fixes from telegram
- 9693fd7 Document IMESSAGE_STATE_DIR in README
- b3a0714 feat(telegram,discord): inline buttons for permission approval (#945)
- 4b1e2a2 feat(telegram,discord): compact permission messages with expandable details (#952)
- d49d339 Show input_preview only for Bash in permission prompts
- 7074ac0 Merge pull request #737 from anthropics/add-imessage-channel
- 12e9c01 Regenerate imessage bun.lock without artifactory URLs
- 79caa0d Merge pull request #957 from anthropics/kenneth/fix-imessage-lockfile
- b10b583 Add flint plugin to marketplace (#974)
- ba3a4e0 Add terraform plugin files to match marketplace.json entry
- 72b9754 Merge pull request #1031 from anthropics/dickson/add-terraform-plugin
- 03a685d imessage: restrict permission relay to self-chat only
- c29338f imessage: drop whitespace-only messages from tapbacks/receipts
- 8dfc279 imessage: harden echo filter normalization
- c427452 imessage: trim comment cruft
- 60c3fc3 imessage: drop SMS/RCS by default, opt-in via IMESSAGE_ALLOW_SMS
- 22bd61d imessage: bump to 0.1.0
- 9d468ad math-olympiad: housekeeping (#1172)
- 31e7200 Merge pull request #1055 from anthropics/kenneth/imessage-permission-selfchat-only
- 92e3c1c Update postman plugin to latest version (#1080)
- 9ed1651 Add UI5 plugins from SAP (ui5 + ui5-typescript-conversion) (#1086)
- 52e95f6 Add mongodb plugin (#1095)
- a54e529 Removing posthog pin
- b091cb4 Merge pull request #1188 from anthropics/tobinsouth-patch-1

### Workflow Signals

- `.claude-plugin/marketplace.json`
- `external_plugins/imessage/.claude-plugin/plugin.json`
- `plugins/math-olympiad/LICENSE`
- `plugins/math-olympiad/README.md`
- `plugins/math-olympiad/skills/math-olympiad/SKILL.md`
- `plugins/math-olympiad/skills/math-olympiad/references/adversarial_prompts.md`
- `plugins/math-olympiad/skills/math-olympiad/references/attempt_agent.md`
- `plugins/math-olympiad/skills/math-olympiad/references/known_constructions.md`
- `plugins/math-olympiad/skills/math-olympiad/references/model_tier_defaults.md`
- `plugins/math-olympiad/skills/math-olympiad/references/presentation_prompts.md`
- `plugins/math-olympiad/skills/math-olympiad/references/solver_heuristics.md`
- `plugins/math-olympiad/skills/math-olympiad/references/verifier_patterns.md`

### All Changed Files

- `.claude-plugin/marketplace.json`
- `external_plugins/imessage/.claude-plugin/plugin.json`
- `external_plugins/imessage/README.md`
- `external_plugins/imessage/package.json`
- `external_plugins/imessage/server.ts`
- `plugins/math-olympiad/LICENSE`
- `plugins/math-olympiad/README.md`
- `plugins/math-olympiad/skills/math-olympiad/SKILL.md`
- `plugins/math-olympiad/skills/math-olympiad/references/adversarial_prompts.md`
- `plugins/math-olympiad/skills/math-olympiad/references/attempt_agent.md`
- `plugins/math-olympiad/skills/math-olympiad/references/known_constructions.md`
- `plugins/math-olympiad/skills/math-olympiad/references/model_tier_defaults.md`
- `plugins/math-olympiad/skills/math-olympiad/references/presentation_prompts.md`
- `plugins/math-olympiad/skills/math-olympiad/references/solver_heuristics.md`
- `plugins/math-olympiad/skills/math-olympiad/references/verifier_patterns.md`

## `vendor/compound-engineering-plugin`

- Range: `78c42fcb4787..bbd4f6de5696`
- Commit count: `79`

### Commits

- 4b44a94 fix: prevent orphaned opening paragraphs in PR descriptions (#393)
- e09a742 feat: add branch-based plugin install for worktree workflows (#395)
- eb9084b chore: release main (#394)
- daddb7d fix: consolidate compound-docs into ce-compound skill (#390)
- 506ad01 fix: replace broken markdown link refs in skills (#392)
- 13aa3fa feat: add CLI agent-readiness reviewer and principles guide (#391)
- 1bd63c2 fix: consolidate local dev README and fix shell aliases (#396)
- e792166 fix: improve agent-native-reviewer with triage, prioritization, and stack-aware search (#387)
- 0877b69 fix: add strict YAML validation for plugin frontmatter (#399)
- b25480a fix: sanitize colons in skill/agent names for Windows path compatibility (#398)
- 6ddaec3 fix: document SwiftUI Text link tap limitation in test-xcode skill (#400)
- b30288c feat: add project-standards-reviewer as always-on ce:review persona (#402)
- 0863cfa feat(document-review): smarter autofix, batch-confirm, and error/omission classification (#401)
- 5e6cd5c feat: add adversarial review agents for code and documents (#403)
- da390a6 refactor: merge deepen-plan into ce:plan as automatic confidence check (#404)
- f83305e fix: harden git workflow skills with better state handling (#406)
- 4a60ee2 fix: clarify commit prefix selection for markdown product code (#407)
- b5dc9b0 docs(AGENTS): recommend component scope in commit conventions (#408)
- 914f9b0 feat(ce-review): add base: and plan: arguments, extract scope detection (#405)
- 615ec5d feat(ce-plan): strengthen test scenario guidance across plan and work skills (#410)
- 69fc503 chore: update package description and readme tweaks (#411)
- 90684c4 feat(ce-brainstorm): group requirements by logical concern, tighten autofix classification (#412)
- 31326a5 feat(onboarding): add consumer perspective and split architecture diagrams (#413)
- 7b75a9a chore: release main (#397)
- d447296 fix(document-review): enforce interactive questions and fix autofix classification (#415)
- ccb371e feat(ce-plan): add decision matrix form, unchanged invariants, and risk table format (#417)
- 16eb8b6 fix(cli-agent-readiness-reviewer): remove top-5 cap on improvements (#419)
- 4b9232b chore: release main (#416)
- d2436e7 fix(onboarding): resolve section count contradiction with skip rule (#421)
- 88e7a52 chore: release main (#422)
- 4e4a656 feat(document-review): add headless mode for programmatic callers (#425)
- de8da43 chore: release main (#426)
- 0bd29c7 fix(release): align cli and compound-engineering versions with linked-versions plugin
- 125463b chore: release main (#428)
- 3706a97 feat(ce-review): add headless mode for programmatic callers (#430)
- 0f5715d feat(document-review): collapse batch_confirm tier into auto (#432)
- 9caaf07 feat(review): make review mandatory across pipeline skills (#433)
- 6dabae6 feat(ce-work): accept bare prompts and add test discovery (#423)
- ae69680 chore: release main (#431)
- 03f5aa6 feat(ce-review): improve signal-to-noise with confidence rubric, FP suppression, and intent verification (#434)
- d2b24e0 feat(skills): clean up argument-hint across ce:* skills (#436)
- bd02ca7 feat(ce-brainstorm): add conditional visual aids to requirements documents (#437)
- 1f49948 fix(git-commit-push-pr): quiet expected no-pr gh exit (#439)
- 4c7f51f feat(ce-plan): add conditional visual aids to plan documents (#440)
- a301a08 feat(resolve-pr-feedback): add gated feedback clustering to detect systemic issues (#441)
- 35678b8 feat(testing): close the testing gap in ce:work, ce:plan, and testing-reviewer (#438)
- f93d10c feat(converters): centralize model field normalization across targets (#442)
- ca78057 feat(ce-plan): add interactive deepening mode for on-demand plan strengthening (#443)
- 44e3e77 feat(git-commit-push-pr): add conditional visual aids to PR descriptions (#444)
- 739109c feat(ce-compound): add track-based schema for bug vs knowledge learnings (#445)
- a01a8aa feat(cli-agent-readiness-reviewer): add smart output defaults criterion (#448)
- 42fa8c3 fix(ce-plan): reinforce mandatory document-review after auto deepening (#450)
- e872e15 feat(ce-work): suggest branch rename when worktree name is meaningless (#451)
- 638b38a fix(review): harden ce-review base resolution (#452)
- 7f3aba2 fix(ce-work): make code review invocation mandatory by default (#453)
- 847ce3f feat(ce-review): enforce table format, require question tool, fix autofix_class calibration (#454)
- 9bf3b07 fix(ce-compound): require question tool for "What's next?" prompt (#460)
- 2b7283d fix(document-review): show contextual next-step in Phase 5 menu (#459)
- 5ac8a2c feat(ce-compound): add discoverability check for docs/solutions/ in instruction files (#456)
- 2619ad9 fix(resolve-pr-feedback): add actionability filter and lower cluster gate to 3+ (#461)
- 6ca7aef feat(git-commit-push-pr): precompute shield badge version via skill preprocessing (#464)
- 1962f54 fix(ce-plan): route confidence-gate pass to document-review (#462)
- e372b43 feat(model): add MiniMax provider prefix for cross-platform model normalization (#463)
- 87facd0 feat(test-xcode): add triggering context to skill description (#466)
- 8ec31d7 fix(ce-brainstorm): distinguish verification from technical design in Phase 1.1 (#465)
- 1840b0c chore: release main (#435)
- 0294652 feat(skill-design): document skill file isolation and platform variable constraints (#469)
- 33a8d9d fix(ce-plan, ce-brainstorm): enforce repo-relative paths in generated documents (#473)
- 01ce065 fix(cli): exclude non-CLI paths from release-please (#472)
- c56c766 feat(cli-readiness-reviewer): add conditional review persona for CLI agent readiness (#471)
- c65a698 fix(converters): preserve user config when writing MCP servers (#479)
- 7b8265b feat(resolve-pr-feedback): add cross-invocation cluster analysis (#480)
- 804d78f feat(product-lens-reviewer): domain-agnostic activation criteria and strategic consequences (#481)
- 96345ac feat(release): document linked-versions policy (#482)
- 82d9d1d chore: release main (#474)
- 428f4fd fix(git-commit-push-pr): filter fix-up commits from PR descriptions (#484)
- 577db53 fix(converters): OpenCode subagent model and FQ agent name resolution (#483)
- afdd9d4 fix(mcp): remove bundled context7 MCP server (#486)
- bbd4f6d feat(git-commit-push-pr): pre-resolve context to reduce bash calls (#488)

### Workflow Signals

- `.claude-plugin/marketplace.json`
- `plugins/compound-engineering/.claude-plugin/plugin.json`
- `plugins/compound-engineering/.cursor-plugin/plugin.json`
- `plugins/compound-engineering/.mcp.json`
- `plugins/compound-engineering/AGENTS.md`
- `plugins/compound-engineering/CHANGELOG.md`
- `plugins/compound-engineering/README.md`
- `plugins/compound-engineering/agents/document-review/adversarial-document-reviewer.md`
- `plugins/compound-engineering/agents/document-review/coherence-reviewer.md`
- `plugins/compound-engineering/agents/document-review/product-lens-reviewer.md`
- `plugins/compound-engineering/agents/research/best-practices-researcher.md`
- `plugins/compound-engineering/agents/research/learnings-researcher.md`
- `plugins/compound-engineering/agents/research/repo-research-analyst.md`
- `plugins/compound-engineering/agents/review/adversarial-reviewer.md`
- `plugins/compound-engineering/agents/review/agent-native-reviewer.md`
- `plugins/compound-engineering/agents/review/cli-agent-readiness-reviewer.md`
- `plugins/compound-engineering/agents/review/cli-readiness-reviewer.md`
- `plugins/compound-engineering/agents/review/previous-comments-reviewer.md`
- `plugins/compound-engineering/agents/review/project-standards-reviewer.md`
- `plugins/compound-engineering/agents/review/testing-reviewer.md`

### All Changed Files

- `.claude-plugin/marketplace.json`
- `.github/.release-please-manifest.json`
- `.github/release-please-config.json`
- `AGENTS.md`
- `CHANGELOG.md`
- `README.md`
- `docs/brainstorms/2026-03-26-merge-deepen-into-plan-requirements.md`
- `docs/brainstorms/2026-03-28-ce-review-headless-mode-requirements.md`
- `docs/brainstorms/2026-03-29-testing-addressed-gate-requirements.md`
- `docs/brainstorms/2026-03-30-cli-readiness-review-persona-requirements.md`
- `docs/brainstorms/2026-04-01-cross-invocation-cluster-analysis-requirements.md`
- `docs/plans/2026-03-26-001-feat-adversarial-review-agents-plan.md`
- `docs/plans/2026-03-26-001-refactor-merge-deepen-into-plan.md`
- `docs/plans/2026-03-28-001-feat-ce-review-headless-mode-plan.md`
- `docs/plans/2026-03-29-001-feat-brainstorm-visual-aids-plan.md`
- `docs/plans/2026-03-29-001-feat-testing-addressed-gate-plan.md`
- `docs/plans/2026-03-29-002-feat-plan-visual-aids-plan.md`
- `docs/plans/2026-03-29-002-feat-pr-feedback-clustering-plan.md`
- `docs/plans/2026-03-29-003-feat-pr-description-visual-aids-plan.md`
- `docs/plans/2026-03-30-001-feat-cli-readiness-review-persona-plan.md`
- `docs/plans/2026-04-01-001-feat-cross-invocation-cluster-analysis-plan.md`
- `docs/solutions/agent-friendly-cli-principles.md`
- `docs/solutions/best-practices/conditional-visual-aids-in-generated-documents-2026-03-29.md`
- `docs/solutions/developer-experience/branch-based-plugin-install-and-testing-2026-03-26.md`
- `docs/solutions/developer-experience/local-dev-shell-aliases-zsh-and-bunx-fixes-2026-03-26.md`
- `docs/solutions/integrations/colon-namespaced-names-break-windows-paths-2026-03-26.md`
- `docs/solutions/integrations/cross-platform-model-field-normalization-2026-03-29.md`
- `docs/solutions/skill-design/discoverability-check-for-documented-solutions-2026-03-30.md`
- `docs/solutions/skill-design/git-workflow-skills-need-explicit-state-machines-2026-03-27.md`
- `docs/solutions/skill-design/pass-paths-not-content-to-subagents-2026-03-26.md`
- `package.json`
- `plugins/compound-engineering/.claude-plugin/plugin.json`
- `plugins/compound-engineering/.cursor-plugin/plugin.json`
- `plugins/compound-engineering/.mcp.json`
- `plugins/compound-engineering/AGENTS.md`
- `plugins/compound-engineering/CHANGELOG.md`
- `plugins/compound-engineering/README.md`
- `plugins/compound-engineering/agents/document-review/adversarial-document-reviewer.md`
- `plugins/compound-engineering/agents/document-review/coherence-reviewer.md`
- `plugins/compound-engineering/agents/document-review/product-lens-reviewer.md`
- ... and 112 more files

## `vendor/dotclaude`

- Range: `9d36e367dee3..be586bfc0547`
- Commit count: `41`

### Commits

- 8b5cfc7 chore(sp): prune .claude from .gitignore
- e47a754 refactor(sp): use JSON utilities for stop hook
- b73567c feat(git): update config and ignore rules
- ad5347f docs(sp): update skill docs & patterns
- e08b709 chore(sp): delete systematic debugging tests
- 69a5ca7 feat(office): add prd creation skill and templates
- 321be11 feat(utils): add shared utility functions
- d601381 feat(sp): add vet skill and update plugin metadata
- b6ac0a6 feat(devtools): enhance superpowers hooks
- 81724d6 feat(utils): add vet utilities and run haiku merge
- d375266 docs(sp): add execution task tracking design
- f34c3b6 docs(sp): update execution task tracking docs
- 90d8101 refactor(devtools): skip verification for skills
- ae200bc feat(devtools): detect slash cmd in task-start
- e068334 feat(devtools): add slash command detection tiers
- 19db833 docs(cod): update plugin list and scopes
- cda0376 fix(utils): change stop-hook exit code and output
- 463ef03 refactor(utils): enable claude auth & hook tweak
- a764790 feat(devtools): add need_vet verification flag
- 231c951 refactor(git): remove deprecated commit hooks
- 89a7098 docs(gitflow): add git-agent steps to skills
- eb0bbf5 refactor(office): update agent-browser sync script
- 4966ca5 docs(sp): update pretool hook reference
- a47c4b3 docs(git): update git commit guidance
- 11eea8c docs(git): update commit tool description
- 71df149 docs(cod): ensure tasks completed before promise
- 49cfafc fix(utils): preserve skill context, clear vet flag
- 261f415 refactor(git): add git tools to skill configs
- dbe7894 refactor(cod): add need-vet skill and update hooks
- 6dc6cf8 feat(git): add use-git-agent skill
- ddc0671 refactor(gitflow): unify workflow templates
- e3e43ef refactor(git): update skill docs and tool lists
- 64e5e3d docs(git): add install section to cli guide
- e460ce7 refactor(git): refactor plugin to agent workflow
- 8e2d370 docs(git): simplify git and skill instruction docs
- 99bc30a docs(git): update skill and agent documentation
- aae67dd docs(git): update skill and agent documentation
- 101a216 refactor(git): streamline git plugin skills
- 0ac984c docs(commit): add model arg
- 9779bf1 chore(devtools): bump version to 1.12.1
- be586bf chore(github): update changelog for v1.12.1

### Workflow Signals

- `.claude-plugin/marketplace.json`
- `git/hooks/hooks.json`
- `git/skills/commit-and-push/SKILL.md`
- `git/skills/commit/SKILL.md`
- `git/skills/config-git/SKILL.md`
- `git/skills/update-gitignore/SKILL.md`
- `gitflow/skills/finish-feature/SKILL.md`
- `gitflow/skills/finish-hotfix/SKILL.md`
- `gitflow/skills/finish-release/SKILL.md`
- `gitflow/skills/start-feature/SKILL.md`
- `gitflow/skills/start-hotfix/SKILL.md`
- `gitflow/skills/start-release/SKILL.md`
- `office/skills/create-prd/SKILL.md`
- `office/skills/create-prd/references/prd-interview-questions.md`
- `office/skills/create-prd/references/prd-template-brief.md`
- `office/skills/create-prd/references/prd-template-full.md`
- `office/skills/create-prd/references/prd-template-onepager.md`
- `office/skills/create-prd/references/prd-validation-checklist.md`
- `plugin-optimizer/skills/plugin-best-practices/references/components/hooks.md`
- `superpowers/.claude-plugin/plugin.json`

### All Changed Files

- `.claude-plugin/marketplace.json`
- `.git-agent/config.yml`
- `.gitignore`
- `CHANGELOG.md`
- `CLAUDE.md`
- `docs/plans/2026-03-25-execution-task-tracking-design/_index.md`
- `docs/plans/2026-03-25-execution-task-tracking-design/architecture.md`
- `docs/plans/2026-03-25-execution-task-tracking-design/bdd-specs.md`
- `docs/plans/2026-03-25-execution-task-tracking-design/best-practices.md`
- `git/README.md`
- `git/hooks/hooks.json`
- `git/references/cli.md`
- `git/scripts/validate-commit-pretool.sh`
- `git/skills/commit-and-push/SKILL.md`
- `git/skills/commit/SKILL.md`
- `git/skills/config-git/SKILL.md`
- `git/skills/update-gitignore/SKILL.md`
- `gitflow/skills/finish-feature/SKILL.md`
- `gitflow/skills/finish-hotfix/SKILL.md`
- `gitflow/skills/finish-release/SKILL.md`
- `gitflow/skills/start-feature/SKILL.md`
- `gitflow/skills/start-hotfix/SKILL.md`
- `gitflow/skills/start-release/SKILL.md`
- `office/scripts/sync-agent-browser.sh`
- `office/skills/create-prd/SKILL.md`
- `office/skills/create-prd/references/prd-interview-questions.md`
- `office/skills/create-prd/references/prd-template-brief.md`
- `office/skills/create-prd/references/prd-template-full.md`
- `office/skills/create-prd/references/prd-template-onepager.md`
- `office/skills/create-prd/references/prd-validation-checklist.md`
- `plugin-optimizer/skills/plugin-best-practices/references/components/hooks.md`
- `superpowers/.claude-plugin/plugin.json`
- `superpowers/.gitignore`
- `superpowers/hooks/stop-hook.sh`
- `superpowers/hooks/task-start.sh`
- `superpowers/hooks/track-changes.sh`
- `superpowers/lib/utils.sh`
- `superpowers/scripts/setup-superpower-loop.sh`
- `superpowers/skills/brainstorming/SKILL.md`
- `superpowers/skills/brainstorming/references/design-creation.md`
- ... and 15 more files

## `vendor/everything-claude-code`

- Range: `678fb6f0d37e..31525854b5fc`
- Commit count: `245`

### Commits

- 4811e8c docs(zh-CN): add prune command translation
- e22cb57 docs(zh-CN): add prune command translation
- f3cf808 Update docs/zh-CN/commands/prune.md
- aed18eb Update docs/zh-CN/commands/prune.md
- d016e68 Update docs/zh-CN/commands/prune.md
- ec921e5 Update docs/zh-CN/commands/prune.md
- d6061cf Update docs/zh-CN/commands/prune.md
- 6af7ca1 Update docs/zh-CN/commands/prune.md
- 1d0f64a feat(skills): add openclaw-persona-forge skill
- e3510f6 docs(zh-CN): fix missing newline before origin in prompt-optimizer skill
- 9c381b4 fix: move ajv to dependencies and auto-install deps in install scripts
- f7d589c feat: add agent-payment-x402 skill for autonomous agent payments
- e57ad5c fix: address all automated review feedback on code example
- 95a1435 Update skills/agent-payment-x402/SKILL.md
- 39a34e4 docs: tighten tdd workflow red-green validation
- 46f6e36 Apply suggestions from code review
- 3c59d8d adjust: clarify runtime vs compile-time red validation
- a61947b adjust: generalize refactor commit placeholder
- fee93f2 Apply suggestions from code review
- bf7ed1f docs(ja-JP): translate plain text code blocks to Japanese
- 7229e09 feat(skills): add repo-scan skill
- 9cc5d08 adjust: scope tdd checkpoints to active branch
- 369f662 fix: populate SKILL.md with actual content
- d952a07 fix: populate SKILL.md with actual content
- 57e9983 fix: address review feedback — rename sections, pin install commit, fix frontmatter
- d170cdd fix: remove redundant skill copy from sync-ecc-to-codex.sh
- a6a8149 revert(ja-JP): keep commit message examples in English in CONTRIBUTING.md
- 3fbfd7f feat: Add git-workflow skill
- dc92b5c feat: Add performance-optimizer agent for code performance analysis and optimization
- 243fae8 Add token-budget-advisor skill
- 7a17ec9 Update skills/token-budget-advisor/SKILL.md
- 0284f60 Update skills/token-budget-advisor/SKILL.md
- 9cfcfac Update skills/token-budget-advisor/SKILL.md
- 7cabf77 Update skills/token-budget-advisor/SKILL.md
- e6eb992 Update skills/token-budget-advisor/SKILL.md
- ee3f348 Update skills/token-budget-advisor/SKILL.md
- 917c35b Update skills/token-budget-advisor/SKILL.md
- 4da1fb3 Update skills/token-budget-advisor/SKILL.md
- 45baaa1 feat(skills): add laravel-plugin-discovery skill with LaraPlugins MCP
- b44ba70 feat(hooks): add pre-commit quality check hook
- b5148f1 feat(rules): add code-review.md rule to common rules
- 3f5e042 feat: add Chinese (zh-CN) translation for rules/common
- c146fae docs: add comprehensive Skill Development Guide
- da74f85 fix: address review feedback from PR #929
- c96c4d2 docs: clarify multi-model command setup
- 9348751 docs: fix rule installation examples
- 6408511 chore(deps-dev): bump picomatch
- 2243f15 fix: add execute permissions to codex sync shell scripts
- 925d830 docs: add ECC2 codebase analysis research report
- f471f27 fix: address CodeRabbit review — dependency versions, risk wording, style, security audit rec
- 2d0fddf Update research/ecc2-codebase-analysis.md
- dafc9bc Update research/ecc2-codebase-analysis.md
- 6373754 feat: add healthcare domain skills and agent
- fe6a6fc fix: move ajv to dependencies and add .yarnrc.yml for node-modules linker
- e3f2bda fix: address all CodeRabbit + Cubic review comments on PR #955
- 9b24bed fix: address Greptile review — frontmatter, CI safety, null guards
- 73c1012 Merge pull request #938 from affaan-m/dependabot/npm_and_yarn/npm_and_yarn-3f9ee708be
- 160624d Merge branch 'main' into fix/shell-script-permissions
- cc60bf6 Merge pull request #947 from chris-yyau/fix/shell-script-permissions
- 1e226ba feat(skill): ck — context-keeper v2, persistent per-project memory
- 17f6f95 fix(ck): address Greptile + CodeRabbit review bugs
- b4296c7 feat: add install catalog and project config autodetection
- 7633386 Merge pull request #878 from affaan-m/feat/install-catalog-project-config
- 8b6140d Merge pull request #956 from tae1344/fix/ajv-runtime-dependency
- 27e0d53 docs: resolve ecc2 analysis review nits
- ba09a34 docs: renumber ecc2 analysis recommendations
- 00f8628 fix(codex): add startup_timeout_sec to MCP servers to prevent first-run timeouts
- c80631f fix(observer): improve Windows compatibility for temp files and Haiku prompt
- 31af1ad fix(observer): anchor CWD to PROJECT_DIR before Claude invocation
- 1e44475 fix(codex): sync startup_timeout_sec into merge-mcp-config.js ECC_SERVERS
- 194bc00 fix(observer): guard cd failure with early return and log message
- c14765e fix(codex): add persistent_instructions to baseline and relax sanity check
- 7148d90 fix(ci): enable Corepack for yarn and relax pnpm strict mode
- d8e3b9d fix(ci): remove --ignore-engines for Yarn Berry (v4+)
- ae21a8d fix(scripts): add os.homedir() fallback for Windows compatibility
- ebd14cd fix(codex): allow leading whitespace in persistent_instructions regex
- 4517321 fix(observer): clean up temp files on cd failure early return
- 9ad4351 fix(codex): align context7-mcp package specifier with config.toml
- 8f7445a Merge pull request #976 from ymdvsymd/fix/ci-pnpm-yarn-compat-v2
- 70a96bd Merge pull request #977 from Lidang-Jiang/fix/cli-homedir-windows-fallback
- d49c95a fix(installer): show help text on error and document --profile full in README
- 24674a7 fix(installer): write error and help text to stderr for consistent stream output
- 70b65a9 fix: tighten installer error spacing
- 652f87c fix(installer): tighten error help spacing
- 87d883e Merge pull request #963 from affaan-m/fix/install-show-help-on-error
- f077975 Merge pull request #931 from KT-lcz/main
- 78c98dd fix(codex): reuse shared MCP startup timeout constant
- 4b4f077 fix(codex): allow indented persistent_instructions
- 7a4cb8c fix(observer): clean up prompt_file early and fix test for analysis_relpath
- 4fcaaf8 feat: add .trae directory with install/uninstall scripts
- 28a1fbc fix: pin 6 actions to commit SHA, extract 1 expression to env var
- 80d6a89 Merge pull request #971 from Lidang-Jiang/fix/codex-mcp-startup-timeout
- 1181d93 Merge pull request #974 from Lidang-Jiang/fix/codex-sanity-check-persistent-instructions
- 6a7a115 fix: normalize Codex Context7 naming
- 432788d fix: clean up legacy Context7 aliases on update
- 6766054 docs: use directory-level rule copy examples
- 9033f2a Merge pull request #970 from seancheick/codex/context7-consistency
- d9ec51c Merge pull request #932 from KT-lcz/readme
- 9f37a5d fix(installer): preserve existing claude hook settings
- d7e6bb2 fix(installer): reject invalid claude settings roots
- 47aa415 fix(installer): validate hooks and settings before install
- 1e7c299 Merge pull request #972 from Lidang-Jiang/fix/observer-windows-temp-files
- 55efeb7 Merge pull request #987 from dagecko/runner-guard/fix-ci-security
- a3fc90f Merge pull request #964 from affaan-m/fix/claude-hooks-settings-merge-safe
- 4e7773c docs: add repo evaluation vs current setup comparison
- 04d7eeb docs: add repo and fork assessment with setup recommendations
- 56076ed docs: add commands quick reference guide (59 commands)
- 72de19e chore: apply Claude setup improvements
- c865d4c docs: fix ECC setup reference drift
- 64847d0 Merge pull request #986 from Infiniteyieldai/claude/evaluate-repo-comparison-ASZ9Y
- d473cf8 feat(codex): add Codex native plugin manifest and fix Claude plugin.json
- 414ea90 fix(codex): correct marketplace.json plugin source path
- 23d743b fix(skills): add missing YAML frontmatter to 7 skills
- 4257c09 fix(codex): point marketplace plugin path at repo root
- 52e9bd5 fix(codex): tighten manifest docs and test guards
- f98207f Merge pull request #960 from senoldogann/feat/codex-plugin-manifest
- c6b4c71 Merge pull request #952 from anuragg-saxenaa/pr-950
- 9cde342 fix(docs): correct ecc2 analysis report facts
- 9434e07 Merge pull request #989 from affaan-m/fix/ecc2-analysis-report-facts
- 9181382 fix(ci): sync yarn lockfile
- 0d26f52 Merge pull request #990 from affaan-m/fix/yarn-lock-sync
- b3a43f3 Merge pull request #896 from ToniDonDoni/codex/tdd-workflow-red-green-guards
- e815f0d fix(docs): resolve skill guide review issues
- 71219ff Merge pull request #929 from xingzihai/feat/skill-development-guide
- dcc4d91 fix(skills): tighten repo-scan install flow
- 70b98f3 Merge pull request #911 from haibindev/main
- c1d98b0 Merge pull request #892 from chris-yyau/fix/remove-redundant-skill-sync
- dd38518 fix(docs): restore canonical runtime strings in ja-JP docs
- 766f846 Merge pull request #897 from techiro/docs/ja-JP-translate-plain-text-blocks
- 1e43639 Merge pull request #855 from Yumerain/fix/zh-cn-doc-format
- 4eaee83 fix(install): stop after npm bootstrap failures on powershell
- b6e3434 Merge pull request #858 from sliver2er/fix/install-missing-ajv-dependency
- eac0228 fix(skills): align laravel plugin discovery docs
- a8e088a Merge pull request #923 from danielpetrica/main
- 666c639 feat(skills): add laravel-plugin-discovery skill with LaraPlugins MCP
- 14a5140 fix(skills): align laravel plugin discovery docs
- ec104c9 fix(skills): wire laravel plugin discovery into installs
- 25c8a5d Merge pull request #991 from affaan-m/affaan/laravel-plugin-discovery-refresh
- e686bcb fix(trae): harden install and uninstall flow
- 0d30da1 Merge branch 'main' into feature/trae-integration
- 6f16e75 Merge pull request #985 from likzn/feature/trae-integration
- 27d71c9 fix(hooks): port doc-file-warning denylist policy to current hook runtime
- 3c3781c refactor: address reviewer feedback
- 7462168 fix(lint): prefix unused options parameter with underscore
- 1e3572b fix(docs): correct zh-CN prune frontmatter
- 00787d6 fix(ck): preserve display names and harden git helpers
- fc1ea4f Merge pull request #818 from 694344851/docs/zh-cn-prune-command
- eeeea50 Merge pull request #959 from sreedhargs89/feat/skill-context-keeper
- c5e3658 Merge pull request #955 from drkeyurpatel-wq/feat/healthcare-patterns
- 9406f35 fix(docs): repair healthcare eval harness examples
- 06a7791 Merge pull request #993 from affaan-m/fix/healthcare-eval-harness-followup
- 81acf0c fix(hooks): make pre-commit quality checks enforce staged state
- a346a30 Merge pull request #926 from xingzihai/feature/pre-commit-quality-hook
- 3ae0df7 Merge pull request #893 from up2itnow0822/feat/agent-payment-x402-skill
- f2bf72c Merge branch 'main' into fix/doc-file-warning-denylist
- d9e8305 Merge pull request #992 from Lidang-Jiang/fix/doc-file-warning-denylist
- 9a55fd0 fix(skills): harden token budget advisor skill
- b7a82cf Merge origin/main into Xabilimon1/main
- ab49c9a Merge pull request #920 from Xabilimon1/main
- 65c4a0f docs(readme): fix agent count in repo tree
- 2d27da5 Merge pull request #997 from affaan-m/fix/readme-agent-count-tree
- ebf0f13 fix(skills): clarify token-budget-advisor triggers
- 99a154a Merge pull request #998 from affaan-m/fix/token-budget-advisor-trigger-clarity
- be76918 fix(clv2): honor CLV2_CONFIG in start-observer
- bec1ebf Merge pull request #999 from affaan-m/fix/clv2-config-override-rebase
- 0ebcfc3 fix(codex): broaden context7 config checks
- 527c793 Merge pull request #1000 from affaan-m/fix/codex-context7-compat-tests
- 0c166e1 fix: skip pre-push checks on branch deletion
- 46f37ae chore: pin actions to commit SHAs and add Skills section to CLAUDE.md
- db12d3d Merge pull request #1004 from ohashi-mizuki/fix/pre-push-skip-branch-deletion
- dd675d4 Merge pull request #1007 from AndriyKalashnykov/chore/pin-actions-and-update-claude-md
- 866d9eb fix: harden unicode safety checks
- 432a452 chore: revert lockfile churn
- 7483d64 fix: narrow unicode cleanup scope
- c39aa22 fix: harden lifecycle hook launchers and mcp schema
- ae272da Merge pull request #1002 from affaan-m/fix/unicode-safety-hardening
- ded5d82 Merge pull request #1011 from affaan-m/fix/stop-hook-and-mcp-schema
- 0f065af feat: add omega-memory MCP server to mcp-configs
- b575f2e fix: align omega-memory config description
- cff28ef Merge pull request #854 from singularityjason/feat/add-omega-memory-mcp
- 8846210 fix: unblock unicode safety CI lint (#1017)
- fab80c9 fix: harden Trae install ownership (#1013)
- b9a01d3 fix: audit consumer projects from cwd (#1014)
- c90566f fix: harden codex sync CI hermeticity (#1020)
- a4d4b1d fix: resolve MINGW64 double-path conversion in install.sh (#1015)
- 118e57e feat(hooks): add WSL desktop notification support via PowerShell + BurntToast (#1019)
- 7253d0c test: isolate codex hook sync env (#1023)
- d6c7f8f fix(skills): harden openclaw persona forge
- 3f6a14a fix(clv2): resolve cwd to git root before project detection
- 7ff2f07 feat: add gitagent format for cross-harness portability
- 5a2c9f5 Merge pull request #850 from eamanc-lab/feat/add-openclaw-persona-forge-v2
- 0220202 Merge pull request #831 from dani-mezei/fix/clv2-subdirectory-project-detection
- 656cf4c Merge pull request #833 from shreyas-lyzr/feat/gitagent-format
- e68233c fix(ci): harden codex hook regression test (#1028)
- f7f91d9 fix(codex): remove duplicate agents table from reference config (#1032)
- 6cc85ef fix: CI fixes, security audit, remotion skill, lead-intelligence, npm audit (#1039)
- 5e7f657 chore(deps-dev): bump globals in the minor-and-patch group (#1062)
- cfb3476 chore(deps): bump actions/github-script from 7.1.0 to 8.0.0 (#1059)
- d1e2209 chore(deps): bump actions/cache from 4.3.0 to 5.0.4 (#1057)
- 5596159 fix(hooks): pass phase argument from hook ID to observe.sh (#1042)
- fade657 feat(team-builder): use `claude agents` command for agent discovery (#1021)
- 30ab9e2 fix: extract inline SessionStart bootstrap to separate file (#1035)
- 9b611f1 feat: add hexagonal architecture SKILL. (#1034)
- 99a44f6 feat(commands): add santa-loop adversarial review command (#1052)
- e86d3db fix: filter session-start injection by cwd/project to prevent cross-project contamination (#1054)
- 09398b4 chore(deps): bump actions/setup-node from 4.4.0 to 6.3.0 (#1058)
- a1cebd2 chore(deps): bump actions/upload-artifact from 4.6.2 to 7.0.0 (#1061)
- a41a073 fix: correct SOURCE_KIRO path in Kiro installer (#1025)
- 0c9b024 feat: install claude-hud plugin (jarrodwatts/claude-hud) (#1041)
- 4cdfe70 feat: add GAN-style generator-evaluator harness (#1029)
- 477d23a feat(agents,skills): add opensource-pipeline — 3-agent workflow for safe public releases (#1036)
- c38bc79 feat(install): add CodeBuddy(Tencent) adaptation with installation scripts (#1038)
- 6b82abe chore(deps-dev): bump c8 from 10.1.3 to 11.0.0 (#1065)
- 87363f0 chore(deps): bump actions/checkout from 4.3.1 to 6.0.2 (#1060)
- eacf3a9 fix(hooks): collapse multi-line commands in bash audit logs (#741)
- 95e606f perf(hooks): batch format+typecheck at Stop instead of per Edit (#746)
- f90f269 feat(opencode): complete OpenCode agent setup - add 10 missing agent prompts (#726)
- c02d6e9 feat: add PRP workflow commands adapted from PRPs-agentic-eng (#848)
- 0f40fd0 feat(skills): add evalview-agent-testing skill and MCP server (#828)
- a2b3cc1 feat(opencode): add changed-files tree with change indicators (#815)
- 9908610 feat(skills): add orch-runtime skill for persistent AI agent team dispatch (#559)
- d0e5cae Revert "feat(skills): add orch-runtime skill for persistent AI agent team dispatch (#559)"
- e85bc5f Revert "feat: install claude-hud plugin (jarrodwatts/claude-hud) (#1041)"
- 44dfc35 fix(security): remove evalview-agent-testing skill — external dependency
- 97d9607 chore: ignore local orchestration artifacts
- f056952 refactor: fold social graph ranking into lead intelligence
- 1744e1e feat: add gemini install target
- b41b2cb docs: add Claude Code troubleshooting workarounds
- a273c62 fix: restore ci lockfile and hook validation
- 51a87d8 docs: add working context file
- d4b5ca7 docs: tighten pr backlog classification
- 03c4a90 fix: update ecc2 ratatui dependency
- e1bc08f fix: harden install planning and sync tracked catalogs
- 43ac81f fix: harden reusable release tag validation
- 5194d20 docs: tighten voice-driven content skills
- f3db349 docs: shift repo guidance to skills-first workflows
- e134e49 docs: close bundle drift and sync plugin guidance
- 6833454 fix: dedupe managed hooks by semantic identity
- 975100d refactor: collapse legacy command bodies into skills
- 1abeff9 feat: add connected operator workflow skills
- 401966b feat: expand lead intelligence outreach channels
- dba5ae7 fix: harden install and codex sync portability
- 9a6080f feat: sync the codex baseline and agent roles
- 8f63697 fix: port safe ci cleanup from backlog
- 3152585 feat(skills): add brand voice and network ops lanes

### Workflow Signals

- `.agents/plugins/marketplace.json`
- `.agents/skills/article-writing/SKILL.md`
- `.agents/skills/backend-patterns/SKILL.md`
- `.agents/skills/brand-voice/SKILL.md`
- `.agents/skills/brand-voice/references/voice-profile-schema.md`
- `.agents/skills/coding-standards/SKILL.md`
- `.agents/skills/content-engine/SKILL.md`
- `.agents/skills/crosspost/SKILL.md`
- `.agents/skills/everything-claude-code/SKILL.md`
- `.agents/skills/frontend-patterns/SKILL.md`
- `.agents/skills/investor-outreach/SKILL.md`
- `.agents/skills/security-review/SKILL.md`
- `.agents/skills/tdd-workflow/SKILL.md`
- `.agents/skills/x-api/SKILL.md`
- `.claude-plugin/marketplace.json`
- `.claude-plugin/plugin.json`
- `.codex-plugin/plugin.json`
- `.cursor/hooks/after-file-edit.js`
- `.github/workflows/ci.yml`
- `.github/workflows/maintenance.yml`

### All Changed Files

- `.agents/plugins/marketplace.json`
- `.agents/skills/article-writing/SKILL.md`
- `.agents/skills/backend-patterns/SKILL.md`
- `.agents/skills/brand-voice/SKILL.md`
- `.agents/skills/brand-voice/references/voice-profile-schema.md`
- `.agents/skills/coding-standards/SKILL.md`
- `.agents/skills/content-engine/SKILL.md`
- `.agents/skills/crosspost/SKILL.md`
- `.agents/skills/everything-claude-code/SKILL.md`
- `.agents/skills/frontend-patterns/SKILL.md`
- `.agents/skills/investor-outreach/SKILL.md`
- `.agents/skills/security-review/SKILL.md`
- `.agents/skills/tdd-workflow/SKILL.md`
- `.agents/skills/x-api/SKILL.md`
- `.claude-plugin/PLUGIN_SCHEMA_NOTES.md`
- `.claude-plugin/README.md`
- `.claude-plugin/marketplace.json`
- `.claude-plugin/plugin.json`
- `.claude/rules/node.md`
- `.codebuddy/README.md`
- `.codebuddy/README.zh-CN.md`
- `.codebuddy/install.js`
- `.codebuddy/install.sh`
- `.codebuddy/uninstall.js`
- `.codebuddy/uninstall.sh`
- `.codex-plugin/README.md`
- `.codex-plugin/plugin.json`
- `.codex/AGENTS.md`
- `.codex/config.toml`
- `.cursor/hooks/after-file-edit.js`
- `.gemini/GEMINI.md`
- `.github/dependabot.yml`
- `.github/workflows/ci.yml`
- `.github/workflows/maintenance.yml`
- `.github/workflows/monthly-metrics.yml`
- `.github/workflows/release.yml`
- `.github/workflows/reusable-release.yml`
- `.github/workflows/reusable-test.yml`
- `.github/workflows/reusable-validate.yml`
- `.gitignore`
- ... and 473 more files

## `vendor/get-shit-done`

- Range: `604a78b30b44..94a8005f9766`
- Commit count: `90`

### Commits

- 2154e6b feat: add security-first enforcement layer with threat-model-anchored verification
- 58c9a8a test: add secure-phase validation suite (42 tests)
- 9f45682 fix: address adversarial review — tag name and verify-work gate
- 69e104d fix(windsurf): remove trailing slash from .windsurf/rules path
- 9647c71 fix(slug): add --raw flag to generate-slug callers and cap length
- b5cbd47 fix(commands): remove duplicate workstreams.md from plugin directory
- 1f34965 feat: add project_code config for phase directory prefixing
- 596ce2d feat: GSD SDK — headless CLI with init + auto commands (#1407)
- c1fd72f fix(branching): capture decimal phase numbers in commit regex
- a858c6d feat: add --sdk flag and interactive SDK prompt to installer (#1415)
- 0e63cd7 docs: update README and changelog for v1.30.0
- 0fde35a 1.30.0
- 89f95c4 feat: auto --init flag, headless prompts, and prompt sanitizer (#1417)
- 38c18ac feat: Headless prompt overhaul — SDK drives full lifecycle without interactive patterns (#1419)
- fedd9a9 fix: enforce plan file naming convention in gsd-planner agent
- 1421dc0 fix: resolve gsd-tools.cjs from repo-local installation before global fallback (#1425)
- 9ef71b0 fix(hooks): use shared cache dir and correct stale hooks path
- 655d455 fix(verifier): enforce human_needed status when human verification items exist
- e7d5c40 fix(verifier): always load ROADMAP SCs regardless of PLAN must_haves
- 2b8c95a fix(install): add .claude path replacement for Codex runtime
- e24add1 feat(researcher): add claim provenance tagging and assumptions log
- 447d17a fix(todos): rename todos/done to todos/completed in workflows and docs
- 18111f9 fix(next): remove reference to non-existent /gsd:complete-phase
- 3e8c8f6 feat(autonomous): add --only N flag for single-phase execution
- 32b2c52 fix: cmdPhaseComplete now updates Plans column and plan checkboxes in ROADMAP.md
- 39d8688 fix(sdk): skip advance step when verification finds gaps
- eeb692d fix: manager workflow delegates to Skill pipeline instead of raw Task prompts
- d1ff043 feat(config): add workflow.use_worktrees toggle to disable worktree isolation
- c5e4fea fix(sdk): verify outcome gates advance correctly + regression tests
- 88af6fd fix(reapply-patches): three-way merge and never-skip invariant for backed-up files
- 3321d48 fix(stats): require verification for Complete status, add Executed state
- e0b953d test(hooks): add structural tests for shared cache directory (#1421)
- 74cd8f2 test(config): add config-get/set roundtrip and cross-workflow structural tests for use_worktrees
- b8a1402 feat: detect and prevent silent scope reduction in planner
- ffe5319 fix(install): handle JSONC (comments) in settings.json without data loss
- c056a43 fix(discuss): incremental checkpoint saves to prevent answer loss on interrupt
- 3163378 fix(worktree): add post-execution cleanup for orphan worktrees
- 5635d71 fix(quick): enforce commit boundary between executor and orchestrator
- 0782b5b fix: prevent infinite self-discuss loop in auto/headless mode (#1426)
- c9d7ba2 Integrate CodeRabbit into review workflow
- 5217b7b feat(quick): make --full include all phases, add --validate flag
- aa6af6a docs(workflows): add CodeRabbit to review command docs
- c9fc52b docs: add CodeRabbit to cross-AI review options
- b599268 feat: add project skills discovery section to CLAUDE.md generation
- f2d6dfe fix: list all supported skill directories in fallback text
- 72038b9 docs: update CodeRabbit review command usage
- 067d411   feat: add /gsd:docs-update command for verified documentation generation (#1532)
- eecb06c Fix path replacement for ~/.claude to ~/.github (#1529)
- cdf8d08 Merge pull request #1380 from Bantuson/feat/security-first-layer
- 1dc0d90 Merge pull request #1394 from Tibsfox/fix/issue-triage-batch-1392-1391-1389
- d70ca3e Merge pull request #1397 from bshiggins/feat/project-code-prefix
- 4add6d2 Merge pull request #1408 from Tibsfox/fix/decimal-phase-regex-1402
- 89a5524 Merge pull request #1429 from Tibsfox/fix/update-cache-dir-1421
- 8502c11 Merge pull request #1501 from Tibsfox/fix/discuss-incremental-saves-1485
- 7f11543 feat: add schema drift detection to prevent false-positive verification
- 5e88db9 feat(discuss): add --chain flag for interactive discuss with auto plan+execute
- 53c7c1c Merge pull request #1518 from ElliotDrel/feat/full-flag-refactor
- 2f03830 Merge pull request #1500 from Tibsfox/fix/settings-jsonc-comments-1461
- 01fda70 fix: migrate Claude Code commands/ to skills/ format for 2.1.88+ compatibility
- 8cd6dd3 Merge pull request #1540 from gsd-build/fix/1504-claude-skills-migration
- c8cd671 Merge pull request #1427 from quangdo126/fix/enforce-plan-file-naming
- 02c4194 Merge pull request #1432 from j2h4u/fix/verifier-human-needed-status
- 6204cd6 Merge pull request #1434 from Tibsfox/fix/verifier-roadmap-sc-bypass-1418
- 77953ec Merge pull request #1436 from Tibsfox/fix/codex-path-replacement-1430
- d2f537c Merge pull request #1437 from Tibsfox/fix/researcher-assumption-tagging-1431
- dbc54b8 Merge pull request #1439 from Tibsfox/fix/todo-done-vs-completed-1438
- 1cf97fd Merge pull request #1386 from gsd-build/fix/schema-drift-detection-1381
- 1d97a03 Merge pull request #1442 from Tibsfox/fix/complete-phase-reference-1441
- dbb3239 Merge pull request #1444 from Tibsfox/feat/autonomous-only-flag-1383
- ce5fbc5 Merge pull request #1445 from Tibsfox/feat/discuss-phase-chain-1327
- 5eed697 Merge pull request #1447 from rahuljordashe/fix/phase-complete-roadmap-rollup
- 4f2db2b Merge pull request #1454 from odmrs/fix/skip-advance-on-gaps-found
- be2f99e Merge pull request #1455 from gsd-build/fix/manager-skill-pipeline-1453
- 2f16cb8 Merge pull request #1456 from Tibsfox/fix/worktree-disable-config-1451
- a96b9e2 Merge pull request #1474 from Tibsfox/fix/reapply-patches-misclassification-1469
- 4afc596 Merge pull request #1477 from Tibsfox/fix/stats-verification-status-1459
- 7b221a8 Merge pull request #1492 from grgbrasil/fix/scope-reduction-detection
- 591d535 Merge pull request #1502 from Tibsfox/fix/worktree-cleanup-1496
- bf838c0 Merge pull request #1505 from Tibsfox/fix/quick-plan-uncommitted-1503
- 35b835b Merge pull request #1508 from Ecko95/fix/infinite-self-discuss-loop
- b12f3ce Merge pull request #1519 from alexpalyan/feat/add-coderabbit-reviewer
- 89f82d5 fix(workstream): require name arg for set, add --clear flag (#1527)
- 66e3cf8 fix(autonomous): clarify phase count display to prevent misleading N/T (#1516)
- ada7d35 Merge pull request #1525 from jhonymiler/feat/skills-discovery-claude-md
- 9ddf004 fix(agents): remove permissionMode that breaks Gemini CLI agent loading (#1522)
- d7aa474 Merge pull request #1543 from Tibsfox/fix/workstream-set-requires-name-1527
- fd2e844 Merge pull request #1544 from Tibsfox/fix/autonomous-phase-count-display-1516
- 78e5c6d Merge pull request #1545 from Tibsfox/fix/remove-permissionmode-gemini-1522
- 8de750e chore: bump version to 1.31.0 for npm release
- 94a8005 docs: update documentation for v1.31.0 release

### Workflow Signals

- `agents/gsd-debugger.md`
- `agents/gsd-doc-verifier.md`
- `agents/gsd-doc-writer.md`
- `agents/gsd-executor.md`
- `agents/gsd-phase-researcher.md`
- `agents/gsd-plan-checker.md`
- `agents/gsd-planner.md`
- `agents/gsd-security-auditor.md`
- `agents/gsd-verifier.md`
- `commands/gsd/add-backlog.md`
- `commands/gsd/discuss-phase.md`
- `commands/gsd/docs-update.md`
- `commands/gsd/manager.md`
- `commands/gsd/quick.md`
- `commands/gsd/reapply-patches.md`
- `commands/gsd/secure-phase.md`
- `commands/gsd/thread.md`
- `get-shit-done/commands/gsd/workstreams.md`
- `get-shit-done/templates/SECURITY.md`
- `get-shit-done/templates/VALIDATION.md`

### All Changed Files

- `.gitignore`
- `CHANGELOG.md`
- `README.ja-JP.md`
- `README.ko-KR.md`
- `README.md`
- `README.pt-BR.md`
- `agents/gsd-debugger.md`
- `agents/gsd-doc-verifier.md`
- `agents/gsd-doc-writer.md`
- `agents/gsd-executor.md`
- `agents/gsd-phase-researcher.md`
- `agents/gsd-plan-checker.md`
- `agents/gsd-planner.md`
- `agents/gsd-security-auditor.md`
- `agents/gsd-verifier.md`
- `bin/install.js`
- `commands/gsd/add-backlog.md`
- `commands/gsd/discuss-phase.md`
- `commands/gsd/docs-update.md`
- `commands/gsd/manager.md`
- `commands/gsd/quick.md`
- `commands/gsd/reapply-patches.md`
- `commands/gsd/secure-phase.md`
- `commands/gsd/thread.md`
- `docs/COMMANDS.md`
- `docs/CONFIGURATION.md`
- `docs/FEATURES.md`
- `docs/ja-JP/COMMANDS.md`
- `docs/ja-JP/FEATURES.md`
- `docs/ko-KR/COMMANDS.md`
- `docs/ko-KR/FEATURES.md`
- `docs/zh-CN/README.md`
- `get-shit-done/bin/gsd-tools.cjs`
- `get-shit-done/bin/lib/commands.cjs`
- `get-shit-done/bin/lib/config.cjs`
- `get-shit-done/bin/lib/core.cjs`
- `get-shit-done/bin/lib/docs.cjs`
- `get-shit-done/bin/lib/init.cjs`
- `get-shit-done/bin/lib/model-profiles.cjs`
- `get-shit-done/bin/lib/phase.cjs`
- ... and 123 more files

## `vendor/gstack`

- Range: `aa7daf052ece..6169273d16b7`
- Commit count: `39`

### Commits

- 1bf888d feat: GitLab support for /retro, /ship, and /document-release (v0.11.20.0) (#508)
- 997f7b1 fix: review log architecture — close gaps, add attribution (v0.11.21.0) (#512)
- 7665adf feat: headed mode + sidebar agent + Chrome extension (v0.12.0) (#517)
- 4f435e4 feat: /land-and-deploy first-run dry run + staging-first + trust ladder (v0.12.2.0) (#518)
- 25e971b feat: voice directive for all skills (v0.12.3.0) (#520)
- de20228 fix: /ship CHANGELOG and PR body now cover all branch commits (v0.12.4.0) (#535)
- 1b60acd fix: Codex hang fixes — plan visibility, stdout buffering, reasoning effort (v0.12.4.0) (#536)
- 3d52382 feat: worktree parallelization strategy in /plan-eng-review (v0.12.5.1) (#547)
- dc0bae8 fix: sidebar agent uses real tab URL instead of stale Playwright URL (v0.12.6.0) (#544)
- b343ba2 fix: community PRs + security hardening + E2E stability (v0.12.7.0) (#552)
- 18bf424 fix: resolve codex exec -C repo root eagerly to prevent wrong-project reviews (v0.12.6.0) (#549)
- 60061d0 fix: zsh glob compatibility across all skill templates (v0.12.8.1) (#559)
- 5319b8a feat: community PRs — faster install, skill namespacing, uninstall, Codex fallback, Windows fix, Python patterns (v0.12.9.0) (#561)
- 22ad3e5 fix: Codex filesystem boundary — prevent skill-file prompt injection (v0.12.10.0) (#570)
- 43c078f feat: skill prefix is now a persistent user choice (v0.12.11.0) (#571)
- 11695e3 fix: security audit compliance — credentials, telemetry, bun pin, untrusted warning (v0.12.12.0) (#574)
- 78bc1d1 feat: design binary — real UI mockup generation for gstack skills (v0.13.0.0) (#551)
- 7450b51 fix: security audit remediation — 12 fixes, 20 tests (v0.13.1.0) (#595)
- 247fc3b feat: user sovereignty — AI models recommend, users decide (v0.13.2.0) (#603)
- cd66fc2 fix: 6 critical fixes + community PR guardrails (v0.13.2.0) (#602)
- ea7dbc9 fix: sidebar prompt injection defense (v0.13.4.0) (#611)
- 484cf1f feat: Factory Droid compatibility — works across Claude Code, Codex, and Factory (v0.13.5.0) (#621)
- 6689460 chore: gitignore .factory and remove tracked files (v0.13.5.1) (#642)
- ae0a9ad feat: GStack Learns — per-project self-learning infrastructure (v0.13.4.0) (#622)
- cdd6f78 feat: community wave — 7 fixes, relink, sidebar Write, discoverability (v0.13.5.0) (#641)
- 3cda8de fix: security audit round 2 (v0.13.4.0) (#640)
- 66c0964 feat: composable skills — INVOKE_SKILL resolver + factoring infrastructure (v0.13.7.0) (#644)
- 403637f feat: rotating founder resources in /office-hours closing (v0.13.10.0) (#652)
- 8151fcd feat: /design-html skill — Pretext-native HTML from approved mockups (v0.14.0.0) (#653)
- b2b380b docs: update README and skill deep dives for all 31 skills (#656)
- 7911b7b fix: force comparison board as default variant chooser (v0.14.1.0) (#658)
- a1a9336 feat: sidebar CSS inspector + per-tab agents (v0.13.9.0) (#650)
- a0328be feat: always-on adversarial review + scope drift + plan mode design tools (v0.14.3.0) (#694)
- a4a181c feat: Review Army — parallel specialist reviewers for /review (v0.14.3.0) (#692)
- 7ea6ead fix: ship idempotency + skill prefix name patching (v0.14.3.0) (#693)
- db35b8e feat: session intelligence roadmap + design doc (#727)
- 8115951 feat: recursive self-improvement — operational learning + full skill wiring (v0.13.8.0) (#647)
- 562a675 feat: Session Intelligence Layer — /checkpoint + /health + context recovery (v0.15.0.0) (#733)
- 6169273 feat: /design-html works from any starting point (v0.15.1.0) (#734)

### Workflow Signals

- `.agents/skills/gstack-autoplan/agents/openai.yaml`
- `.agents/skills/gstack-benchmark/agents/openai.yaml`
- `.agents/skills/gstack-browse/agents/openai.yaml`
- `.agents/skills/gstack-canary/agents/openai.yaml`
- `.agents/skills/gstack-careful/agents/openai.yaml`
- `.agents/skills/gstack-cso/agents/openai.yaml`
- `.agents/skills/gstack-design-consultation/agents/openai.yaml`
- `.agents/skills/gstack-design-review/agents/openai.yaml`
- `.agents/skills/gstack-document-release/agents/openai.yaml`
- `.agents/skills/gstack-freeze/agents/openai.yaml`
- `.agents/skills/gstack-guard/agents/openai.yaml`
- `.agents/skills/gstack-investigate/agents/openai.yaml`
- `.agents/skills/gstack-land-and-deploy/agents/openai.yaml`
- `.agents/skills/gstack-office-hours/agents/openai.yaml`
- `.agents/skills/gstack-plan-ceo-review/agents/openai.yaml`
- `.agents/skills/gstack-plan-design-review/agents/openai.yaml`
- `.agents/skills/gstack-plan-eng-review/agents/openai.yaml`
- `.agents/skills/gstack-qa-only/agents/openai.yaml`
- `.agents/skills/gstack-qa/agents/openai.yaml`
- `.agents/skills/gstack-retro/agents/openai.yaml`

### All Changed Files

- `.agents/skills/gstack-autoplan/agents/openai.yaml`
- `.agents/skills/gstack-benchmark/agents/openai.yaml`
- `.agents/skills/gstack-browse/agents/openai.yaml`
- `.agents/skills/gstack-canary/agents/openai.yaml`
- `.agents/skills/gstack-careful/agents/openai.yaml`
- `.agents/skills/gstack-cso/agents/openai.yaml`
- `.agents/skills/gstack-design-consultation/agents/openai.yaml`
- `.agents/skills/gstack-design-review/agents/openai.yaml`
- `.agents/skills/gstack-document-release/agents/openai.yaml`
- `.agents/skills/gstack-freeze/agents/openai.yaml`
- `.agents/skills/gstack-guard/agents/openai.yaml`
- `.agents/skills/gstack-investigate/agents/openai.yaml`
- `.agents/skills/gstack-land-and-deploy/agents/openai.yaml`
- `.agents/skills/gstack-office-hours/agents/openai.yaml`
- `.agents/skills/gstack-plan-ceo-review/agents/openai.yaml`
- `.agents/skills/gstack-plan-design-review/agents/openai.yaml`
- `.agents/skills/gstack-plan-eng-review/agents/openai.yaml`
- `.agents/skills/gstack-qa-only/agents/openai.yaml`
- `.agents/skills/gstack-qa/agents/openai.yaml`
- `.agents/skills/gstack-retro/agents/openai.yaml`
- `.agents/skills/gstack-review/agents/openai.yaml`
- `.agents/skills/gstack-setup-browser-cookies/agents/openai.yaml`
- `.agents/skills/gstack-setup-deploy/agents/openai.yaml`
- `.agents/skills/gstack-ship/agents/openai.yaml`
- `.agents/skills/gstack-unfreeze/agents/openai.yaml`
- `.agents/skills/gstack-upgrade/agents/openai.yaml`
- `.agents/skills/gstack/agents/openai.yaml`
- `.github/docker/Dockerfile.ci`
- `.github/workflows/skill-docs.yml`
- `.gitignore`
- `ARCHITECTURE.md`
- `BROWSER.md`
- `CHANGELOG.md`
- `CLAUDE.md`
- `CONTRIBUTING.md`
- `DESIGN.md`
- `ETHOS.md`
- `README.md`
- `SKILL.md`
- `SKILL.md.tmpl`
- ... and 216 more files

## `vendor/lean-spec`

- Range: `e76ee3d9cf19..56e37042f587`
- Commit count: `2`

### Commits

- 945c4d9 feat: add LeanSpec positioning and Codervisor vision spec (380)
- 56e3704 feat: add hierarchical export (entry points + skills) to spec 380

### Workflow Signals

- No skill/workflow signal files detected.

### All Changed Files

- `specs/380-leanspec-positioning-and-codervisor-vision/README.md`

## `vendor/oh-my-claudecode`

- Range: `8f180c662706..fae376508355`
- Commit count: `154`

### Commits

- d8fb7d0e feat(keyword-detector): add Korean transliteration alternatives to keyword patterns
- bc9a6934 feat(learner): add Korean trigger expansion for learned skills
- 990367d8 test(keyword-detector): add Korean cross-script matching tests
- d882e34e test(learner): add transliteration-map unit tests
- a413bae3 fix(test): correct hasKeyword signature in Korean tests
- e6f39386 fix(keyword-detector): remove generic Korean cancel aliases and expand informational filter
- 2e82d6bc test(keyword-detector): update Korean tests for cancel removal and informational filter
- ead06154 build(learner): rebuild skill-bridge.cjs with Korean trigger expansion
- ca8d91fe fix(keyword-detector): require question context for Korean informational filter
- de77ef9c test(keyword-detector): add imperative Korean command tests
- bca570c2 build: rebuild keyword-detector and learner dist bundles
- ea1ca388 fix(i18n): prevent Korean substring false positives
- 1438dbe8 fix(cancel): prevent stop hook infinite loop when state_clear is deferred
- 26a8e90e fix(cancel): resolve bash fallback path to worktree root
- a8c25332 fix(i18n): remove Korean anti-slop aliases and expand informational filter
- 831e7369 fix(cancel): support non-git projects in bash fallback path resolution
- 6ac0c17c fix(cancel): address Codex review — preload all state tools, scope fallback deletion
- ca164906 fix(cancel): harden bash fallback — guard root path, support CLAUDECODE_SESSION_ID
- 72cb078e fix(cancel): support OMC_STATE_DIR centralized storage in bash fallback
- 4ada57a9 fix(cancel): replicate getProjectIdentifier() for OMC_STATE_DIR path resolution
- 8ad675ed fix(cancel): comprehensive hardening from 5-agent review
- 6dc6b7aa fix(cancel): clarify bash fallback scope — emergency escape only
- 04ec073d fix(auto-slash-command): include builtin skills in command discovery
- 697bcab0 fix(i18n): keep only loanword transliterations, remove native translations
- c0e61436 docs: update featured contributors section
- 269d204c fix(i18n): narrow 딥인터뷰 to compound-only and rebuild skill-bridge
- c74fb4d2 fix(i18n): restore bare 설명 in informational intent filter
- b41799ca build: rebuild keyword-detector dist with restored 설명 token
- a4733109 fix(i18n): remove generic dev-* Korean translations from transliteration map
- 357b94b6 Restore Kotlin MCP bundle config parity with source
- e919dbe8 build: sync transliteration-map dist with source
- 44994c47 fix: consolidate isProcessAlive and add EPERM handling
- a9413e66 Merge pull request #1842 from Yeachan-Heo/issue-1841-mcp-bundle-fix
- f3b3ef84 fix(cancel): guard legacy state deletion by session ownership
- 4c33193a fix: consolidate isProcessAlive and add EPERM handling (#1843)
- 3d630227 Merge pull request #1832 from driessamyn/fix/psm-alias-discovery
- b14d7e2b Merge pull request #1830 from ehs208/fix/cancel-deferred-tool-v2
- 57618970 Merge pull request #1827 from devseunggwan/feat/cross-script-korean-trigger
- 1ef063b0 fix: resolve resource leaks, logic errors, and race conditions (#1849)
- 9e7e0030 fix(security): prevent shell injection in ralphthon tmux commands (#1848)
- ce0148b4 chore: remove unused imports and fix test assertions (#1850)
- e5cc15e3 feat(i18n): strengthen deep-interview ambiguity scoring and brownfield confirmations (#1851)
- 7eaddd55 feat: improve skill trigger guidance and install clarity (#1852)
- f5fec89f fix: harden OMC HUD transcript parsing, caching, and setup config preservation (#1853)
- e6511ece feat: improve project-memory injection with progressive disclosure (#1854)
- b8513e20 fix: brownfield planning gates with case-insensitive heading matching (#1861)
- 851380eb fix(hooks): resolve [1m] model suffix deadlock for Bedrock sub-agents (#1863)
- 66605e8b fix: codex team worker registration lookups for claim-task (#1873)
- 03691be7 feat(hud): auto-detect terminal width for responsive wrapping (#1868)
- d6333b04 fix(session-start): warn when silentAutoUpdate is set but inoperative in plugin mode (#1875)
- 7c404979 docs: expand ARCHITECTURE.md with comprehensive system documentation
- eea86be4 Merge pull request #1881 from devswha/docs/architecture
- 590b5ccc fix: resolve 6 verified bugs across MCP, hooks, CLI, and utils (#1884)
- 1d810be0 fix(security): resolve 7 verified security vulnerabilities
- 294e1ae6 fix(team): resolve race conditions and logic errors in team orchestration
- d8d52b58 fix: resolve 30 verified bugs across hooks, features, HUD, MCP, and notifications
- c056c26a fix: resolve 5 remaining bugs with test updates
- c73f39ff fix: address 9 issues from Copilot code review
- 86a6ef32 fix(verification): revert manual checks to passed:false with pending_manual_review status
- 1fad69f5 Merge pull request #1887 from riftzen-bit/fix/deep-bug-hunt-v2
- 4307148b Respect XDG-style global OMC paths on Unix without breaking legacy state
- e643aba2 Restore observability for critical best-effort failures (#1904)
- 6b807c8f Avoid repeated notepad regex compilation on stable headers (#1903)
- 7150e61c Harden standalone MCP handler registration against TS2589 regressions (#1893)
- bb7d809f fix(builtin-skills): resolve correct skills directory in bundled CLI mode (#1915)
- ec897d7f fix(tests): align idle-cooldown and doctor-conflicts tests with XDG path helpers
- 7040bd0a Keep home-directory-sensitive tests portable across CI runners
- 396ab6df Merge pull request #1898 from Yeachan-Heo/fix/issue-1897-xdg-omc-state-dir
- 5758216b feat(obsidian): integrate Obsidian tools into omc-tools-server
- 9645817e Merge pull request #1890 from 0xarkstar/feat/obsidian-integration
- 158d5666 Keep non-interactive ralplan moving through consensus stages
- f0e0c356 Merge pull request #1927 from Yeachan-Heo/fix/issue-1926-ralplan-non-interactive
- 03b2b15e Revert "Merge pull request #1890 from 0xarkstar/feat/obsidian-integration"
- 264f718e Fail closed on stale ralplan subagent counts
- 32ab33b8 Merge pull request #1931 from Yeachan-Heo/fix/issue-1930-ralplan-stale-count
- 53ad7c7e chore: bump version to 4.9.2
- aea3e320 chore: rebuild dist for 4.9.2
- 89f9452d Merge dev into main for v4.9.2 release
- e58a984c chore: remove .tmp/ from tracking
- 61b60774 fix(ci): bump marketplace.json version to 4.9.2
- a9ba72e2 fix(ci): bump marketplace.json version to 4.9.2
- 8b00d540 Keep session-start context test aligned with project-memory formatting
- 8cfb726e Merge pull request #1939 from Yeachan-Heo/fix/issue-flaky-session-start-context
- b52e3711 fix(team): run dedup check before writing worker inbox
- b4c95bd3 fix(setup): remove duplicate dev paths in plugin-setup
- 0deb1e8a chore: remove broken ask:codex and ask:gemini script entries
- a06893d8 Merge pull request #1942 from riftzen-bit/fix/pr1896-split-inbox-dedup
- 3df13af4 Merge pull request #1943 from riftzen-bit/fix/pr1896-split-plugin-paths
- 7ee877d2 Merge pull request #1944 from riftzen-bit/fix/pr1896-split-broken-scripts
- a816fef8 fix(hooks): return fresh:false for missing heartbeat file
- 8f117415 fix(lib): use atomicWriteJsonSync in mode-state-io to prevent race condition
- 493035c4 fix(team): revert task to pending when tmux pane creation fails
- 60ff2331 Merge pull request #1937 from riftzen-bit/fix/pr1896-split-heartbeat
- 65b76438 Merge pull request #1938 from riftzen-bit/fix/pr1896-split-atomic-write
- 238cb232 Merge pull request #1940 from riftzen-bit/fix/pr1896-split-task-orphan
- d754849c fix(lib): guard against prototype pollution in deepMerge
- cb34bbe7 fix(notifications): add Slack user authorization with fail-closed pattern
- 0e69579a fix(providers): include auth token in Gitea REST API fallback
- c96c980c fix(lib): add RALPLAN to mode name maps
- 825f0d7c fix(model-routing): replace require() with ESM import to prevent crash
- 34fb3ce3 fix(hud): propagate directory parameter to initializeHUDState
- 0c3bf255 fix(team): add file locking to removeWorkerWorktree metadata update
- 1b9deaf8 fix(cli): increase generateJobId entropy from 4 to 8 hex chars
- 5f379b93 fix(interop): add file locking to updateSharedTask
- 1ca20e6a fix(tools): escape $ replacement patterns in AST grep replace
- d2b8e84c fix(installer): strip corrupted markers to prevent mergeClaudeMd unbounded growth
- 4d99e3a2 Merge pull request #1955 from riftzen-bit/fix/proto-pollution-guard
- 6ec7d3b4 Merge pull request #1956 from riftzen-bit/fix/slack-auth-fail-closed
- 08f19078 Merge pull request #1957 from riftzen-bit/fix/gitea-rest-auth-token
- 970baeee Merge pull request #1959 from riftzen-bit/fix/mode-names-ralplan
- 00d2d7ff Merge pull request #1960 from riftzen-bit/fix/model-routing-esm-import
- b97f4a8c Merge pull request #1961 from riftzen-bit/fix/hud-init-directory-propagation
- 0c2277b2 fix(scripts): use tail reading in persistent-mode to prevent OOM on large transcripts
- f92d2d72 fix(hud): preserve session fields when clearing background tasks
- b102d26a fix(test): correct worktree-metadata-locking test file syntax
- 9b59e33d Merge pull request #1963 from riftzen-bit/fix/jobid-entropy-increase
- bae6280c Merge pull request #1964 from riftzen-bit/fix/shared-state-file-locking
- 5d735fd6 fix(team): add locking to teamCreateTask for safe concurrent task creation
- a4fce99d Merge pull request #1965 from riftzen-bit/fix/ast-replace-dollar-escaping
- be747f7b Merge pull request #1966 from riftzen-bit/fix/merge-claudemd-growth
- 055918bc Merge pull request #1967 from riftzen-bit/fix/persistent-mode-oom
- ef5a9be9 fix(notifications): remove Slack fallback to prevent unrelated session injection
- d15a7ef7 fix(team): count both failed and error tasks in team status
- 70add6bf fix(hud): add PID tracking to prevent session-summary process accumulation
- 23ecc11e fix(hooks): clear timeout in finally block for session-start scripts
- 594adbb2 Merge pull request #1962 from riftzen-bit/fix/worktree-metadata-locking
- 3e156775 Merge pull request #1971 from riftzen-bit/fix/team-ops-task-id-locking
- da62fcba fix(lib): accept dots in extractRepoSlug for repos like next.js
- df17f982 fix(hooks): escape regex metacharacters in detectPipelineSignal
- 7251bd70 Merge pull request #1972 from riftzen-bit/fix/slack-fallback-removal
- eef0dc89 Merge pull request #1973 from riftzen-bit/fix/team-status-failed-count
- ec263c30 Merge pull request #1974 from riftzen-bit/fix/session-summary-pid-tracking
- 33f6be69 Merge pull request #1975 from riftzen-bit/fix/session-start-timeout-cleanup
- e0171a24 Merge pull request #1976 from riftzen-bit/fix/repo-slug-dots
- 832d6bad fix(hooks): use correct field name for ralph mode in keyword-detector
- 16159d93 fix: apply enforcement.ts regex escaping source change
- 5e6c65f0 fix(hud): preserve session fields when clearing background tasks
- 6d7823f2 fix: bind server context in standalone MCP handler registration
- 8c49a9da fix(notifications): move clearTimeout to finally block in sendCustomWebhook
- 0d931860 fix(team): strip tmux- prefix and add claude to provider type
- e934491a fix(team): parse only complete lines in outbox-reader
- b7687963 Merge pull request #1970 from riftzen-bit/fix/keyword-detector-ralph-state
- 48924528 Merge pull request #1977 from riftzen-bit/fix/pipeline-signal-regex-escape
- 78003b2c Merge pull request #1978 from riftzen-bit/fix/hud-clear-preserve-session-v2
- ae3fbff7 Merge pull request #1979 from sercankaya/fix/mcp-bridge-unbound-this
- 309cb5a8 Merge pull request #1980 from riftzen-bit/fix/webhook-timeout-cleanup
- 88d6a044 Merge pull request #1981 from riftzen-bit/fix/team-status-tmux-provider
- cc71a7db Merge pull request #1982 from riftzen-bit/fix/outbox-reader-partial-lines
- f9bbb99e Merge remote-tracking branch 'origin/dev'
- 884ec78d chore: bump version to 4.9.3
- 8660d291 fix(ci): sync version markers to 4.9.3
- f93e27bc fix(release): add version sync hook + fix stale release body
- 0ec792c0 chore: gitignore release-body.md to prevent stale release notes
- fae37650 chore: update Discord invite link to OmO (Ultraworkers) server

### Workflow Signals

- `.claude-plugin/marketplace.json`
- `.claude-plugin/plugin.json`
- `.github/workflows/release.yml`
- `dist/__tests__/hooks/learner/transliteration-map.test.d.ts`
- `dist/__tests__/hooks/learner/transliteration-map.test.d.ts.map`
- `dist/__tests__/hooks/learner/transliteration-map.test.js`
- `dist/__tests__/hooks/learner/transliteration-map.test.js.map`
- `dist/agents/utils.d.ts.map`
- `dist/agents/utils.js`
- `dist/agents/utils.js.map`
- `dist/cli/commands/ralphthon.d.ts`
- `dist/cli/commands/ralphthon.d.ts.map`
- `dist/cli/commands/ralphthon.js`
- `dist/cli/commands/ralphthon.js.map`
- `dist/cli/commands/teleport.js`
- `dist/cli/commands/teleport.js.map`
- `dist/hooks/__tests__/bridge-openclaw.test.js`
- `dist/hooks/__tests__/bridge-openclaw.test.js.map`
- `dist/hooks/__tests__/bridge-routing.test.js`
- `dist/hooks/__tests__/bridge-routing.test.js.map`

### All Changed Files

- `.claude-plugin/marketplace.json`
- `.claude-plugin/plugin.json`
- `.github/release-body.md`
- `.github/workflows/release.yml`
- `.gitignore`
- `README.de.md`
- `README.es.md`
- `README.fr.md`
- `README.it.md`
- `README.ja.md`
- `README.ko.md`
- `README.md`
- `README.pt.md`
- `README.ru.md`
- `README.tr.md`
- `README.vi.md`
- `README.zh.md`
- `bridge/__pycache__/gyoshu_bridge.cpython-310.pyc`
- `bridge/cli.cjs`
- `bridge/mcp-server.cjs`
- `bridge/runtime-cli.cjs`
- `bridge/team-bridge.cjs`
- `bridge/team-mcp.cjs`
- `bridge/team.js`
- `dist/__tests__/auto-slash-aliases.test.js`
- `dist/__tests__/auto-slash-aliases.test.js.map`
- `dist/__tests__/bedrock-lm-suffix-hook.test.d.ts`
- `dist/__tests__/bedrock-lm-suffix-hook.test.d.ts.map`
- `dist/__tests__/bedrock-lm-suffix-hook.test.js`
- `dist/__tests__/bedrock-lm-suffix-hook.test.js.map`
- `dist/__tests__/doctor-conflicts.test.js`
- `dist/__tests__/doctor-conflicts.test.js.map`
- `dist/__tests__/hooks.test.js`
- `dist/__tests__/hooks.test.js.map`
- `dist/__tests__/hooks/learner/transliteration-map.test.d.ts`
- `dist/__tests__/hooks/learner/transliteration-map.test.d.ts.map`
- `dist/__tests__/hooks/learner/transliteration-map.test.js`
- `dist/__tests__/hooks/learner/transliteration-map.test.js.map`
- `dist/__tests__/hud/defaults.test.js`
- `dist/__tests__/hud/defaults.test.js.map`
- ... and 657 more files

## `vendor/ouroboros`

- Range: `896c8cb9e017..4ec0174fafab`
- Commit count: `38`

### Commits

- 0aab0e6 fix(brownfield): sort repo list by rowid and conditional Recommended label
- ac54f7f fix: review findings — add None option to setup and update docstring
- 4a5caa1 refactor: address review feedback
- 8349297 Enforce task worktrees for mutating workflows (#198)
- 47f25ea fix(interview): prevent ambiguity score override and improve empty response diagnostics
- ecc5d3d fix(worktree): harden lock lifecycle and remove monkey-patch shim
- 3e6d3bb docs: add missing commands to help & READMEs + PM mode announcement (#225)
- 5e168da Add raw verification artifacts for post-run QA (#213)
- b7e4147 fix(setup): break MCP setup infinite loop and fix stale args across install paths (#227)
- c3cde1c chore: release v0.26.2
- 4b79650 feat(cli): add ouroboros uninstall and config backend commands (#220)
- 259f63e fix(#212): degrade gracefully on claude_code JSON output (#232)
- b1d59bc fix(#233): handle null failed_attempts in lateral think (#234)
- 20eea1c chore: release v0.26.3
- 4d76245 fix(#239): show install guidance when litellm extra is missing (#246)
- be9e645 chore: release v0.26.4
- 64caad5 fix(#240): use configured clarification model for pm (#243)
- 21c06cc fix(#244): keep pm logs visible without corrupting input (#247)
- a20c103 feat(pm): return DECIDE_LATER questions to user instead of auto-skipping (#238)
- ad5ba05 fix(pm): align CLI completion scoring with MCP flow (#256)
- 7d08bc9 [codex] Fix resume retries for Codex sessions (#249)
- af7c747 fix(#242): honor configured interview adapter backend in pm (#245)
- b8968c3 Fix PM handoff into the runnable Seed workflow (#252)
- 4f1cdd6 fix(providers): adapter timeout, tool policy, factory max_turns (#259)
- a6925d2 refactor(pm): align PMSeed fields with prd.md output (#258)
- 0b34cd8 fix(#235): tolerate non-JSON QA verdict responses (#236)
- 0e7e08c chore: release v0.26.5
- 71ca57d fix(#269): prevent subprocess leak, fork bomb, and env poisoning (#271)
- bed965b fix(tui): emit execution.terminal so TUI sees session completion (#272)
- 72e9963 chore: release v0.26.6
- 8612596 fix(adapter): retry when Claude Code CLI returns prose instead of JSON (#276)
- b4f5a84 fix(evaluate): raise max_turns from 1 to 20 to fix error_max_turns (#277)
- 76626ea feat: add `ooo publish` skill — Seed to GitHub Issues bridge (#261)
- 6ec6b76 fix: add transport lifecycle tests (rebased from #263) (#278)
- efd4d74 feat(#262): wire mcp_manager through ExecuteSeedHandler to OrchestratorRunner (#279)
- 1db05be feat(#262): add MCPBridge module for MCP server-to-server communication (#280)
- 86bd241 feat(#267): wire mcp_bridge into _evolution_executor closure (#281)
- 4ec0174 chore: release v0.27.0

### Workflow Signals

- `.claude-plugin/marketplace.json`
- `.claude-plugin/plugin.json`
- `skills/brownfield/SKILL.md`
- `skills/help/SKILL.md`
- `skills/pm/SKILL.md`
- `skills/publish/SKILL.md`
- `skills/setup/SKILL.md`
- `skills/update/SKILL.md`
- `src/ouroboros/cli/commands/config.py`
- `src/ouroboros/cli/commands/init.py`
- `src/ouroboros/cli/commands/mcp.py`
- `src/ouroboros/cli/commands/pm.py`
- `src/ouroboros/cli/commands/run.py`
- `src/ouroboros/cli/commands/setup.py`
- `src/ouroboros/cli/commands/uninstall.py`
- `src/ouroboros/plugin/agents/pool.py`
- `src/ouroboros/plugin/skills/registry.py`
- `tests/integration/plugin/test_orchestration.py`
- `tests/unit/plugin/skills/test_registry.py`

### All Changed Files

- `.claude-plugin/marketplace.json`
- `.claude-plugin/plugin.json`
- `CLAUDE.md`
- `README.ko.md`
- `README.md`
- `UNINSTALL.md`
- `docs/cli-reference.md`
- `docs/guides/mcp-bridge.md`
- `pyproject.toml`
- `scripts/install.sh`
- `scripts/keyword-detector.py`
- `skills/brownfield/SKILL.md`
- `skills/help/SKILL.md`
- `skills/pm/SKILL.md`
- `skills/publish/SKILL.md`
- `skills/setup/SKILL.md`
- `skills/update/SKILL.md`
- `src/ouroboros/bigbang/pm_completion.py`
- `src/ouroboros/bigbang/pm_document.py`
- `src/ouroboros/bigbang/pm_interview.py`
- `src/ouroboros/bigbang/pm_seed.py`
- `src/ouroboros/bigbang/question_classifier.py`
- `src/ouroboros/cli/commands/config.py`
- `src/ouroboros/cli/commands/init.py`
- `src/ouroboros/cli/commands/mcp.py`
- `src/ouroboros/cli/commands/pm.py`
- `src/ouroboros/cli/commands/run.py`
- `src/ouroboros/cli/commands/setup.py`
- `src/ouroboros/cli/commands/uninstall.py`
- `src/ouroboros/cli/formatters/prompting.py`
- `src/ouroboros/cli/main.py`
- `src/ouroboros/config/models.py`
- `src/ouroboros/core/initial_context.py`
- `src/ouroboros/core/json_utils.py`
- `src/ouroboros/core/project_paths.py`
- `src/ouroboros/core/worktree.py`
- `src/ouroboros/evaluation/json_utils.py`
- `src/ouroboros/evaluation/semantic.py`
- `src/ouroboros/evaluation/verification_artifacts.py`
- `src/ouroboros/mcp/bridge/__init__.py`
- ... and 102 more files

## `vendor/planning-with-files`

- Range: `c7cc27ad5579..bb3a21ab0d3e`
- Commit count: `0`

### Commits

- No commit subjects found in range.

### Workflow Signals

- No skill/workflow signal files detected.

### All Changed Files

- `tests/__pycache__/test_session_catchup.cpython-314.pyc`

## `vendor/spec-kit`

- Range: `2c2fea8783f3..0945df9ec810`
- Commit count: `29`

### Commits

- ccc44dd Unify Kimi/Codex skill naming and migrate legacy dotted Kimi dirs (#1971)
- b22f381 chore: bump version to 0.4.3 (#1986)
- d720612 chore(deps): bump DavidAnson/markdownlint-cli2-action from 19 to 23 (#1989)
- 362868a chore(deps): bump actions/deploy-pages from 4 to 5 (#1990)
- 8520241 Add plan-review-gate to community catalog (#1993)
- 9c2481f feat: add spec-kit-onboard extension to community catalog (#1991)
- 41d1f4b feat: add MAQA extension suite (7 extensions) to community catalog (#1981)
- 8778c26 fix(scripts): honor PowerShell agent and script filters (#1969)
- 6b1f45c Fix Claude Code CLI detection for npm-local installs (#1978)
- 796b4f4 fix: prevent extension command shadowing (#1994)
- 5be705e Update README.md (#1995)
- edaa5a7 fix(scripts): add correct path for copilot-instructions.md (#1997)
- f8da535 feat(scripts): add --allow-existing-branch flag to create-new-feature (#1999)
- 9cb3f3d feat: add product-forge extension to community catalog (#2012)
- b19a7ee feat: add superpowers bridge extension to community catalog (#2023)
- 40ecd44 chore: use PEP 440 .dev0 versions on main after releases (#2032)
- 4dff63a fix: harden GitHub Actions workflows (#2021)
- 804cd10 Stage 1: Integration foundation — base classes, manifest system, and registry (#1925)
- cb16412 docs: ensure manual tests use local specify (#2020)
- b8335a5 docs: sync AGENTS.md with AGENT_CONFIG for missing agents (#2025)
- 3899dcc Stage 2: Copilot integration — proof of concept with shared template primitives (#2035)
- 3113b72 chore: release 0.4.4, begin 0.4.5.dev0 development (#2048)
- 255371d Stage 3: Standard markdown integrations — 19 agents migrated to plugin architecture (#2038)
- b606b38 feat: add 5 lifecycle extensions to community catalog (#2049)
- 682ffbf Stage 4: TOML integrations — gemini and tabnine migrated to plugin architecture (#2050)
- 4df6d96 Add fix-findings extension to community catalog (#2039)
- 97b9f0f docs: remove dead Cognitive Squad and Understanding extension links and from extensions/catalog.community.json (#2057)
- ea60efe docs: add community extensions website link to README and extensions docs (#2014)
- 0945df9 Add community content disclaimers (#2058)

### Workflow Signals

- `.github/workflows/docs.yml`
- `.github/workflows/lint.yml`
- `.github/workflows/release-trigger.yml`
- `.github/workflows/scripts/create-release-packages.ps1`
- `.github/workflows/scripts/create-release-packages.sh`
- `.github/workflows/test.yml`
- `extensions/template/extension.yml`

### All Changed Files

- `.github/ISSUE_TEMPLATE/extension_submission.yml`
- `.github/workflows/docs.yml`
- `.github/workflows/lint.yml`
- `.github/workflows/release-trigger.yml`
- `.github/workflows/scripts/create-release-packages.ps1`
- `.github/workflows/scripts/create-release-packages.sh`
- `.github/workflows/test.yml`
- `AGENTS.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `README.md`
- `TESTING.md`
- `extensions/EXTENSION-API-REFERENCE.md`
- `extensions/EXTENSION-DEVELOPMENT-GUIDE.md`
- `extensions/EXTENSION-PUBLISHING-GUIDE.md`
- `extensions/EXTENSION-USER-GUIDE.md`
- `extensions/README.md`
- `extensions/RFC-EXTENSION-SYSTEM.md`
- `extensions/catalog.community.json`
- `extensions/template/extension.yml`
- `presets/README.md`
- `pyproject.toml`
- `scripts/bash/create-new-feature.sh`
- `scripts/bash/update-agent-context.sh`
- `scripts/powershell/create-new-feature.ps1`
- `scripts/powershell/update-agent-context.ps1`
- `src/specify_cli/__init__.py`
- `src/specify_cli/agents.py`
- `src/specify_cli/extensions.py`
- `src/specify_cli/integrations/__init__.py`
- `src/specify_cli/integrations/amp/__init__.py`
- `src/specify_cli/integrations/amp/scripts/update-context.ps1`
- `src/specify_cli/integrations/amp/scripts/update-context.sh`
- `src/specify_cli/integrations/auggie/__init__.py`
- `src/specify_cli/integrations/auggie/scripts/update-context.ps1`
- `src/specify_cli/integrations/auggie/scripts/update-context.sh`
- `src/specify_cli/integrations/base.py`
- `src/specify_cli/integrations/bob/__init__.py`
- `src/specify_cli/integrations/bob/scripts/update-context.ps1`
- `src/specify_cli/integrations/bob/scripts/update-context.sh`
- ... and 96 more files

## `vendor/superpowers`

- Range: `eafe962b18f6..b7a8f76985f1`
- Commit count: `12`

### Commits

- a2964d7 fix: add Copilot CLI platform detection for sessionStart context injection
- 8b16692 feat: add Copilot CLI tool mapping, docs, and install instructions
- 2d942f3 fix(opencode): align skills path across bootstrap, runtime, and tests
- 65d760f docs: add OpenCode path fix to release notes
- 0a1124b fix(opencode): inject bootstrap as user message instead of system message
- f0df5ec docs: update release notes with OpenCode bootstrap change
- 1f20bef Release v5.0.7: Copilot CLI support, OpenCode fixes
- c0b417e Add contributor guidelines to reduce agentic slop PRs
- dd23728 Add agent-facing guardrails to contributor guidelines
- eeaf2ad Add release announcements link, consolidate Community section
- 4b1b20f Add detailed Discord description to Community section
- b7a8f76 Merge pull request #1029 from obra/readme-release-announcements

### Workflow Signals

- `.claude-plugin/marketplace.json`
- `.claude-plugin/plugin.json`
- `.cursor-plugin/plugin.json`
- `.opencode/plugins/superpowers.js`
- `hooks/session-start`
- `skills/using-superpowers/SKILL.md`
- `skills/using-superpowers/references/copilot-tools.md`

### All Changed Files

- `.claude-plugin/marketplace.json`
- `.claude-plugin/plugin.json`
- `.cursor-plugin/plugin.json`
- `.opencode/plugins/superpowers.js`
- `.version-bump.json`
- `AGENTS.md`
- `CLAUDE.md`
- `README.md`
- `RELEASE-NOTES.md`
- `gemini-extension.json`
- `hooks/session-start`
- `package.json`
- `scripts/bump-version.sh`
- `skills/using-superpowers/SKILL.md`
- `skills/using-superpowers/references/copilot-tools.md`
- `tests/opencode/setup.sh`
- `tests/opencode/test-plugin-loading.sh`
- `tests/opencode/test-priority.sh`
