---
name: vendor-evolution-sop
description: "Discovery-first research tool for vendor reference repositories. Refreshes vendor/* submodules and produces a code-level evolution research report. Use when updating vendor submodules, observing how external repos evolved, extracting reusable workflow mechanisms from upstream changes, researching code-level patterns worth porting into 1st-cc-plugin, or generating a per-vendor evolution report from submodule diffs."
user-invocable: true
argument-hint: "[vendor-name ...|all]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(git:*)
  - Bash(python3:*)
  - Agent
---

# Vendor Evolution SOP

Refresh `vendor/*` deliberately, then produce a discovery-first research report about how each vendor's workflows, mechanisms, and code boundaries evolved.

The goal is NOT keyword matching. The goal is to answer four questions per vendor:

1. **What problem is this update solving?** — What was broken, missing, or inefficient before?
2. **What operation got systematized?** — What manual or implicit step became explicit, automated, or structured?
3. **How does the core mechanism land in code?** — What scripts, entry points, config formats, or I/O protocols implement it?
4. **What has migration value for `1st-cc-plugin`?** — Which patterns, mechanisms, or structural ideas are worth porting?

And one cross-vendor question:

5. **What identical structural changes appeared across multiple vendors?** — e.g., many repos moving from single-file prompts to multi-file skill systems.

## Anti-Pattern: Keyword Gating

**Do NOT** use path keywords (skills/, commands/, hooks/, agents/) as the primary filter for "worth reading". Good ideas that haven't formed mature naming conventions MUST still be captured through structural changes, new scripts, renamed paths, and code boundary shifts. Keyword matches are a quick-locate shortcut, NOT a relevance gate.

## Inputs

Accept either:
- `all`: update every clean vendor submodule
- One or more vendor names: update only `vendor/<name>`
- No argument: default to every clean vendor submodule

## Workflow

### Phase 1: Refresh

#### Step 1: Snapshot the current vendor state

Capture the current parent-repo HEAD before touching submodules:

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
git rev-parse HEAD
git status --short
```

Do not mix unrelated local work into the vendor refresh commit.

#### Step 2: Identify which vendor repos are safe to update

Enumerate vendor submodules from `.gitmodules`. For each candidate:
- Check `git -C vendor/<name> status --porcelain`
- If dirty with trivial cache/generated files, discard explicitly
- If dirty with real local work, skip and report

#### Step 3: Pull the latest upstream commits

```bash
git submodule update --init --remote --recursive -- vendor/<name> ...
```

Stage only the vendor gitlink changes that belong to this refresh.

#### Step 4: Generate the raw evidence report

Run the bundled report script:

```bash
python3 "$REPO_ROOT/.claude/skills/vendor-evolution-sop/scripts/vendor_evolution_report.py" \
  --base <before-refresh-commit> \
  --head <after-refresh-commit-or-HEAD> \
  --write "$REPO_ROOT/vendor/docs/<date>-vendor-evolution.md"
```

The script outputs structured evidence buckets per vendor — not conclusions. It identifies:
- New paths, renamed paths, largest-churn files (by lines changed)
- Executable/entry-point files, repeatedly touched files
- Top deep-read candidates ranked by coverage priority

### Phase 2: Discovery Analysis

#### Step 5A: Per-vendor evolution analysis

For each vendor with non-trivial changes, read the evidence report and the top deep-read candidates. Then write a research section answering the four mandatory questions.

Rules:
- Every conclusion MUST cite at least 1-3 file paths or code snippets as evidence
- Do not infer mechanisms solely from commit subjects — read the actual files
- Explicitly call out noise (formatting, version bumps, README copy-edits) and explain why it's noise
- If a vendor's update is entirely noise, say so directly with evidence

Use the rubric in `references/evolution-rubric.md`.

#### Step 5B: Cross-vendor synthesis

After all per-vendor sections, write the cross-vendor analysis:
- Common structural trends across repos
- New mechanism candidates worth evaluating
- Directions worth tracking in the next refresh cycle

#### Step 6: Update local vendor research docs

- Write or update a dated report in `$REPO_ROOT/vendor/docs/`
- Update `$REPO_ROOT/vendor/docs/index.md` to point at the newest report

#### Step 7: Commit cleanly

Separate commits for separate intents:
- Vendor refresh: only `vendor/*` gitlink updates
- Vendor onboarding: new submodule + `.gitmodules` + `vendor/README.md`
- Research/doc: new reports and `vendor/docs/*`

## Chinese Markdown Output Template

Final output in Chinese. Repo names, paths, commands, and commit refs stay in original form.

```markdown
# Vendor 演进研究报告

## 更新概览

- 更新时间：<YYYY-MM-DD>
- 更新的 vendor：`<vendor-a>`、`<vendor-b>`
- 跳过的 vendor：`<vendor-c>`（原因：<reason>）

## Vendor 逐项分析

### `<vendor-name>`

#### 变化概述

<本次更新的范围和规模，commit 数、文件数、主要变化区域>

#### 问题与动机

<这次更新在解决什么问题？之前的状态是什么？>

#### 实现机制

<把什么操作系统化了？核心机制如何在代码中落地？>

- 关键脚本/入口：`path/to/script.py`
- I/O 协议：<输入什么、输出什么、如何与其他组件交互>
- 自动化闭环：<是否形成了完整的自动化链路>

#### 关键证据

- `path/to/file1.md` — <这个文件为什么重要，它揭示了什么>
- `path/to/script.sh` — <这个脚本做了什么，机制要点>

#### 噪音与非结论

<哪些变化是格式化、版本号、包装层改动？为什么不值得迁移？>

#### 对 `1st-cc-plugin` 的启发

<值得迁移的模式、值得观察的方向、明确不适合的点>

## 横向结论

### 共同趋势

- <跨 vendor 重复出现的结构性变化 1>
- <跨 vendor 重复出现的结构性变化 2>

### 新机制候选

- <值得评估并可能移植的具体机制 1>
- <值得评估并可能移植的具体机制 2>

### 继续追踪

- <值得在下次 refresh 中关注的方向 1>
- <值得在下次 refresh 中关注的方向 2>
```

## Quality Bar

Good output is evidence-driven, not signal-driven.

Do:
- Deep-read top candidates identified by the evidence report
- Cite specific file paths and code patterns for every conclusion
- Identify new operation boundaries, automation loops, script I/O protocols, routing/orchestration patterns, and validation/rollback mechanisms
- Call out renames — they signal conceptual reframing
- Compare the workflow shape before and after

Do not:
- Dump raw commit logs without interpretation
- Treat keyword path matches as the sole relevance filter
- Draw conclusions only from commit subjects without reading code
- Treat README-only churn as evolution unless it changes user entry points
- Mix vendor onboarding with refresh analysis

## Resources

- `scripts/vendor_evolution_report.py`: generate structured evidence from vendor submodule diffs
- `references/evolution-rubric.md`: framework for writing the per-vendor analysis
