# Workflow Research: claude-reflect

> Reverse-engineering research of `vendor/claude-reflect` (BayramAnnakov/claude-reflect v3.1.0)
> Date: 2026-04-08

---

## Phase 0 — Research Scoping

| Metric | Value |
|--------|-------|
| Total files (excl. `.git`) | 36 |
| Size classification | **Small** (<50) |
| Framework type | Claude Code plugin — self-learning memory system |
| Language | Python 3.6+ (scripts), Markdown (commands/skills) |
| License | MIT |

Repository structure (depth 2):

```
claude-reflect/
├── .claude-plugin/
│   ├── marketplace.json
│   └── plugin.json
├── commands/
│   ├── reflect.md           # Main /reflect command (~1500 lines)
│   ├── reflect-skills.md    # /reflect-skills command
│   ├── skip-reflect.md      # /skip-reflect command
│   └── view-queue.md        # /view-queue command
├── hooks/
│   └── hooks.json           # 4 hook definitions
├── scripts/
│   ├── lib/
│   │   ├── reflect_utils.py # Core utilities (1174 lines)
│   │   └── semantic_detector.py # AI-powered analysis (562 lines)
│   ├── capture_learning.py
│   ├── check_learnings.py
│   ├── post_commit_reminder.py
│   ├── session_start_reminder.py
│   ├── extract_session_learnings.py
│   ├── extract_tool_rejections.py
│   ├── extract_tool_errors.py
│   ├── compare_detection.py
│   ├── read_queue.py
│   └── legacy/              # Deprecated bash scripts
├── tests/                   # 160 tests (5 files)
├── SKILL.md
├── CLAUDE.md
├── README.md
├── CHANGELOG.md
└── RELEASING.md
```

---

## Phase 1 — Source Inventory

### Overview

| File | Role |
|------|------|
| `README.md` | User-facing documentation, installation, feature matrix |
| `CLAUDE.md` | Developer guide: architecture, data flow, session format, detection methods |
| `SKILL.md` | Plugin context loaded when claude-reflect is active |
| `CHANGELOG.md` | Version history from v1.3.4 to v3.1.0 |
| `.claude-plugin/plugin.json` | Plugin manifest (name, version, author, keywords) |
| `.claude-plugin/marketplace.json` | Marketplace registration |

### Execution

| File | Role |
|------|------|
| `hooks/hooks.json` | Hook event-to-script binding (4 hooks) |
| `scripts/capture_learning.py` | **UserPromptSubmit** hook: regex detection + queue append |
| `scripts/check_learnings.py` | **PreCompact** hook: backup queue before compaction |
| `scripts/post_commit_reminder.py` | **PostToolUse(Bash)** hook: remind after git commit |
| `scripts/session_start_reminder.py` | **SessionStart** hook: show pending learnings count |
| `scripts/lib/reflect_utils.py` | Core library: paths, queue ops, pattern detection, session extraction, memory hierarchy |
| `scripts/lib/semantic_detector.py` | AI validation via `claude -p`: learning classification, contradiction detection |
| `scripts/extract_session_learnings.py` | CLI wrapper for session message extraction |
| `scripts/extract_tool_rejections.py` | CLI wrapper for tool rejection extraction |
| `scripts/extract_tool_errors.py` | CLI for repeated tool error extraction |
| `scripts/read_queue.py` | Helper: print current project queue as JSON |
| `scripts/compare_detection.py` | Diagnostic: regex vs semantic detection comparison |

### Prompts

| File | Role |
|------|------|
| `commands/reflect.md` | Main `/reflect` workflow (~1500 lines) — 10-step process with full prompt instructions |
| `commands/reflect-skills.md` | `/reflect-skills` — AI-powered pattern discovery from session history |
| `commands/view-queue.md` | `/view-queue` — display queue with formatting |
| `commands/skip-reflect.md` | `/skip-reflect` — discard queue with confirmation |

### Enforcement

| File | Role |
|------|------|
| `hooks/hooks.json` | Hard enforcement: hooks auto-fire on events |
| `scripts/capture_learning.py` | Hard enforcement: automatic capture to queue on every prompt |
| `tests/` (5 files, 160 tests) | Development-time enforcement: pattern detection, extraction, memory hierarchy |

### Evolution

| File | Role |
|------|------|
| `CHANGELOG.md` | Full version history with breaking changes |
| `scripts/legacy/` | Deprecated bash scripts preserved for reference |
| `RELEASING.md` | Version bump checklist |

---

## Phase 2 — Object Model & Context Strategy

### Entity Definitions

#### 1. Queue Item (`scripts/lib/reflect_utils.py:752-771`)

核心数据实体，代表一条待处理的"学习"。

```json
{
  "type": "auto|explicit|positive|guardrail",
  "message": "user's original text",
  "timestamp": "ISO8601",
  "project": "/path/to/project",
  "patterns": "matched pattern names",
  "confidence": 0.75,
  "sentiment": "correction|positive",
  "decay_days": 90
}
```

**Lifecycle:** Created by `capture_learning.py` (UserPromptSubmit hook) or historical scan -> stored in per-project queue file -> loaded by `/reflect` -> validated semantically -> presented to user -> applied to memory targets or discarded -> queue cleared.

**Classification:** **Fact object** (captures what the user said) + **Judgment object** (confidence score is a computed assessment).

#### 2. Memory Target (`scripts/lib/reflect_utils.py:190-276`, `commands/reflect.md:27-43`)

代表一个可以写入 learning 的目标文件。

```python
{
    "path": str,           # Absolute path
    "relative_path": str,  # Display path (e.g., "~/.claude/CLAUDE.md")
    "type": str,           # 'global' | 'root' | 'local' | 'subdirectory' | 'rule' | 'user-rule'
    "frontmatter": dict,   # Optional: parsed YAML for rule files
}
```

**Discovery:** `find_claude_files()` walks the project tree, discovers 9 memory tiers:
- `~/.claude/CLAUDE.md` (global)
- `./CLAUDE.md` (project root)
- `./CLAUDE.local.md` (personal, gitignored)
- `./**/CLAUDE.md` (subdirectories)
- `./.claude/rules/*.md` (project rules, optional path-scoping)
- `~/.claude/rules/*.md` (user rules)
- `~/.claude/projects/<project>/memory/*.md` (auto memory)
- `./commands/*.md` (skill files)
- `./AGENTS.md` (cross-tool standard)

**Classification:** **Fact object** (filesystem state).

#### 3. Semantic Analysis Result (`scripts/lib/semantic_detector.py:46-67`)

AI 验证的结果对象。

```python
{
    "is_learning": bool,
    "type": "correction" | "positive" | "explicit" | None,
    "confidence": float,  # 0.0-1.0
    "reasoning": str,
    "extracted_learning": str | None,
}
```

**Lifecycle:** Created on-demand during `/reflect` processing -> merged into Queue Item -> used for filtering and confidence boosting.

**Classification:** **Judgment object** (LLM-computed assessment of whether something is a learning).

#### 4. Skill Candidate (implicit in `commands/reflect-skills.md`)

从会话历史中发现的可复用模式，没有显式 schema，由 Claude 在 `/reflect-skills` 执行过程中动态构建。

**Properties (inferred from prompt):**
- skill name
- description
- confidence (High/Medium)
- source project
- evidence count
- correction history
- suggested file path

**Classification:** **Evidence object** (aggregated from session analysis).

#### 5. Tool Error Aggregate (`scripts/lib/reflect_utils.py:1114-1173`)

```python
{
    "error_type": str,
    "count": int,
    "suggested_guideline": str,
    "confidence": float,
    "decay_days": 180,
    "sample_errors": list[str],
}
```

**Classification:** **Evidence object** (statistical aggregation of repeated failures).

### Context Isolation Strategy

claude-reflect 使用 **per-project queue scoping** 实现上下文隔离：

1. **Queue 按项目隔离** (`reflect_utils.py:17-30`): Queue file 存储在 `~/.claude/projects/<encoded-cwd>/learnings-queue.json`，防止跨项目污染。
2. **Legacy migration** (`reflect_utils.py:42-95`): 旧版全局 queue 在首次访问时按 `item.project` 字段分发到各项目 queue。
3. **Cross-project filtering** (`commands/reflect.md` Step 3): `/reflect` 执行时，不同项目的 learning 会被区分处理 — 同项目正常显示，异项目但看起来全局的建议写入全局 CLAUDE.md，异项目且项目特定的自动跳过。
4. **Memory tier routing** (`reflect_utils.py:279-337`): `suggest_claude_file()` 根据 learning 内容（模型名 -> 全局、guardrail -> rules、路径提及 -> 对应子目录）推荐目标文件。

---

## Phase 3 — Flow & State Machine Analysis

### Primary State Machine: Learning Lifecycle

```
[User Prompt]
    │
    ▼
┌─────────────────────┐
│ CAPTURE              │  Hook: UserPromptSubmit
│ capture_learning.py  │  - should_include_message() filter
│                      │  - MAX_CAPTURE_PROMPT_LENGTH guard
│                      │  - detect_patterns() regex engine
└────────┬────────────┘
         │ item_type != None
         ▼
┌─────────────────────┐
│ QUEUED               │  Per-project JSON file
│ learnings-queue.json │  - Persists across sessions
│                      │  - Backed up before compaction
└────────┬────────────┘
         │ User runs /reflect
         ▼
┌─────────────────────┐
│ VALIDATED            │  Step 1.5: Semantic validation
│ semantic_detector.py │  - claude -p --output-format json
│                      │  - Filter false positives
│                      │  - Boost/merge confidence
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ FILTERED             │  Step 3: Project-aware filtering
│ Cross-project check  │  - Same project -> show
│                      │  - Different + global -> show with warning
│                      │  - Different + specific -> auto-skip
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ DEDUPLICATED         │  Step 3.5 + Step 4
│ Within-batch + cross │  - Semantic similarity grouping
│ -tier dedup          │  - Cross-tier duplicate check
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ PRESENTED            │  Step 5: Summary table
│ AskUserQuestion      │  - Apply all / Select / Review / Skip
└────────┬────────────┘
         │ User approves
         ▼
┌─────────────────────┐
│ APPLIED              │  Step 7: Write to targets
│ Edit/Write tools     │  - CLAUDE.md files
│                      │  - Rule files
│                      │  - Skill files
│                      │  - AGENTS.md
│                      │  - Auto memory
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ CLEARED              │  Step 8: Queue emptied
│ Queue reset to []    │  - Confirmation displayed
└─────────────────────┘
```

### Trigger Map

| Event | Hook Script | Transition |
|-------|-------------|------------|
| `SessionStart` | `session_start_reminder.py` | None (informational only) |
| `UserPromptSubmit` | `capture_learning.py` | `[Prompt] -> QUEUED` |
| `PreCompact` | `check_learnings.py` | None (backup only) |
| `PostToolUse(Bash)` | `post_commit_reminder.py` | None (reminder only) |
| `/reflect` command | `commands/reflect.md` | `QUEUED -> ... -> APPLIED/CLEARED` |
| `/reflect-skills` | `commands/reflect-skills.md` | `[Sessions] -> Skill Files` |
| `/skip-reflect` | `commands/skip-reflect.md` | `QUEUED -> CLEARED` |

### Happy Path

1. 用户在对话中发出修正（如 "no, use gpt-5.1 not gpt-5"）
2. `capture_learning.py` 通过 regex 检测到修正模式，写入 queue（confidence 0.70-0.90）
3. 后续 git commit 时，`post_commit_reminder.py` 提醒运行 `/reflect`
4. 用户运行 `/reflect`
5. Queue items 经过 semantic validation 过滤误报
6. 用户通过 AskUserQuestion 审批
7. Learning 写入对应的 CLAUDE.md / rule file / skill file
8. Queue 清空

### Failure Paths

**F1: False positive capture**
- Trigger: system content (XML tags, session continuation) 触发 regex
- Mitigation: `should_include_message()` 前置过滤 + `MAX_CAPTURE_PROMPT_LENGTH` 500 字符限制
- Evidence: `reflect_utils.py:856-876` 定义了 skip_patterns；`CHANGELOG.md` v2.5.1 记录了此修复

**F2: Semantic validation failure**
- Trigger: `claude -p` CLI 不可用、超时、API key 缺失
- Mitigation: Fallback 保留原始 regex 结果 (`semantic_detector.py:213-217`)
- Evidence: `validate_queue_items()` 中 `if result is None: validated.append(item)`

**F3: Cross-project queue leakage (legacy)**
- Trigger: v3.1.0 之前使用全局 queue
- Mitigation: `migrate_global_queue()` 在首次访问时按 project 字段分发 (`reflect_utils.py:42-95`)

**F4: Context compaction loses queue**
- Trigger: Claude Code compaction 清除上下文
- Mitigation: `check_learnings.py` (PreCompact hook) 在 compaction 前备份到 `~/.claude/learnings-backups/`
- Evidence: `check_learnings.py:27-31`

### Parallelism vs Sequential Gates

整个 `/reflect` workflow 是**严格顺序执行**的（10 步），通过 TodoWrite 跟踪进度。没有并行分支。

唯一的"并行"是 4 个 hooks 独立运行在不同事件上，互不依赖。

---

## Phase 4 — Enforcement Audit

### Hard-Enforced

| Behavior | Mechanism | Evidence |
|----------|-----------|----------|
| Auto-capture on every user prompt | `hooks.json` UserPromptSubmit event | `hooks/hooks.json:3-12` — Claude Code 自动执行，用户无法绕过 |
| Queue backup before compaction | `hooks.json` PreCompact event | `hooks/hooks.json:14-23` |
| Post-commit reminder | `hooks.json` PostToolUse(Bash) with "git commit" check | `hooks/hooks.json:25-35`, `post_commit_reminder.py:35` |
| Session start reminder | `hooks.json` SessionStart event | `hooks/hooks.json:37-47` |
| System content filtering | `should_include_message()` in capture pipeline | `reflect_utils.py:843-876` — XML tags, JSON, tool results 被硬过滤 |
| Long prompt rejection | `MAX_CAPTURE_PROMPT_LENGTH = 500` check | `capture_learning.py:49` |
| `remember:` bypass length limit | Explicit check before length guard | `capture_learning.py:49` — `"remember:" not in prompt.lower()` |
| Per-project queue isolation | Path encoding in `get_queue_path()` | `reflect_utils.py:17-30` |
| False positive rejection | `FALSE_POSITIVE_PATTERNS` + `NON_CORRECTION_PHRASES` regex lists | `reflect_utils.py:568-592` |

### Soft-Enforced (Prompt-Instructed)

| Behavior | Mechanism | Evidence |
|----------|-----------|----------|
| TodoWrite progress tracking | `commands/reflect.md` says "MANDATORY: Initialize Task Tracking" | `commands/reflect.md:82-133` — 仅靠 prompt 指示，无代码强制 |
| Human review before apply | Prompt instructs to use AskUserQuestion | `commands/reflect.md:1077-1161` — 如果 Claude 跳过确认步骤，无机制阻止 |
| Hierarchy-aware routing | `suggest_claude_file()` 提供建议，prompt 说 "Let users override" | `commands/reflect.md:66-73`, `reflect_utils.py:279-337` |
| Semantic validation during /reflect | Prompt says "use semantic analysis" | `commands/reflect.md:749-800` — 依赖 Claude 执行 Python 代码 |
| `remember:` items never filtered | Prompt says "NEVER filter out remember: items" | `commands/reflect.md:593` — 仅在 prompt 中声明 |
| Tool rejections always shown | Prompt says "MUST be shown to user" | `commands/reflect.md:561-565` — CRITICAL 标注但无代码强制 |
| Skill improvement routing | Prompt instructs AI reasoning about skill context | `commands/reflect.md:934-976` — 完全依赖 Claude 的推理能力 |
| `/reflect-skills` semantic analysis | Prompt says "DO NOT use hardcoded patterns, regex" | `commands/reflect-skills.md:24` — 仅靠 prompt 禁止 |
| Guardrail routing to rules/ | `suggest_claude_file()` suggests + prompt reinforces | `reflect_utils.py:298-304`, `commands/reflect.md:1470-1503` |

### Unenforced

| Behavior | Claim Source | Evidence of Absence |
|----------|-------------|---------------------|
| "150-line threshold" for CLAUDE.md | `commands/reflect.md:142` | 只在 `--targets` 显示时检查，不阻止写入超过 150 行的文件 |
| Decay mechanism | Queue items 有 `decay_days` 字段 | **无任何代码读取或使用此字段**。`reflect_utils.py` 中 `decay_days` 仅在创建时赋值，从未在加载/过滤时检查。`commands/reflect.md:77` 说 "flagged as stale" 但无实现 |
| Skill file validation | `commands/reflect-skills.md:287-300` 说 "validate skills" | 仅检查文件存在和 frontmatter head，不验证内容质量或工具权限 |
| AGENTS.md section marker preservation | `commands/reflect.md:1373-1389` | 完全依赖 Claude 理解标记格式，无 parser/validator |
| Auto memory promotion | `commands/reflect.md:802-842` 描述 promotion 机制 | `read_auto_memory()` 只读取，没有 "promotion" 逻辑 — 完全依赖 `/reflect --organize` 的 prompt 指示 |

---

## Phase 5 — Prompt Catalog & Design Analysis

### 5A. Prompt Catalog

#### P1: `ANALYSIS_PROMPT` — Semantic Learning Classifier

| Field | Value |
|-------|-------|
| **Role** | Learning classifier |
| **repo_path** | `scripts/lib/semantic_detector.py:21-43` |
| **quote_excerpt** | `"Analyze this user message from a coding session. Determine if it contains a reusable learning, correction, or preference that should be remembered for future sessions."` |
| **Stage** | Validation (Step 1.5) |
| **Design intent** | 将 regex 无法捕获的多语言修正交给 LLM 判断，同时提取 actionable learning 文本 |
| **Hidden assumption** | `claude -p` CLI 可用且 API key 有效；sonnet 模型足以做分类任务 |
| **Likely failure mode** | CLI 不可用时 fallback 到 regex-only，丢失多语言修正检测能力 |

#### P2: `CONTRADICTION_PROMPT` — Entry Conflict Detector

| Field | Value |
|-------|-------|
| **Role** | Contradiction detector |
| **repo_path** | `scripts/lib/semantic_detector.py:433-458` |
| **quote_excerpt** | `"Find pairs that give OPPOSITE advice about the same topic. A contradiction is when: Two entries give conflicting instructions"` |
| **Stage** | Dedup (`/reflect --dedupe`) |
| **Design intent** | 在 CLAUDE.md 膨胀后发现互相矛盾的条目 |
| **Hidden assumption** | LLM 能在单次调用中可靠地检测所有矛盾对 |
| **Likely failure mode** | 条目数量大时 prompt 过长；最多返回 10 对限制了完整性 |

#### P3: `ERROR_TO_GUIDELINE_PROMPT` — Error Pattern Converter

| Field | Value |
|-------|-------|
| **Role** | Error-to-guideline converter |
| **repo_path** | `scripts/lib/semantic_detector.py:247-270` |
| **quote_excerpt** | `"You are analyzing repeated tool execution errors to extract CLAUDE.md guidelines."` |
| **Stage** | Tool error processing (Step 0.5g) |
| **Design intent** | 将重复出现的工具错误转化为项目特定的指南 |
| **Hidden assumption** | 错误消息中包含足够上下文推断项目结构 |
| **Likely failure mode** | 截断的错误消息（500 char limit）丢失关键路径信息 |

#### P4: `/reflect` Command Prompt

| Field | Value |
|-------|-------|
| **Role** | Workflow orchestrator (10-step process) |
| **repo_path** | `commands/reflect.md` (entire file, ~1500 lines) |
| **quote_excerpt** | `"MANDATORY: Initialize Task Tracking (Step 0) — BEFORE starting any work, use TodoWrite to create a task list for the entire workflow."` |
| **Stage** | Full processing pipeline |
| **Design intent** | 通过极其详细的 step-by-step 指令控制 Claude 执行完整的 learning 处理流程 |
| **Hidden assumption** | Claude 会忠实执行 1500 行指令中的每一步；TodoWrite 能有效防止步骤遗漏 |
| **Likely failure mode** | 指令过长导致后期步骤被遗忘（long-tail forgetting）；context window 压力 |

#### P5: `/reflect-skills` Command Prompt

| Field | Value |
|-------|-------|
| **Role** | Pattern discovery engine |
| **repo_path** | `commands/reflect-skills.md` (entire file, ~360 lines) |
| **quote_excerpt** | `"DO NOT use hardcoded patterns, regex, or keyword matching. Your job is to reason about the sessions and identify: Workflow patterns, Misunderstanding patterns, Prompt sequences"` |
| **Stage** | Skill discovery |
| **Design intent** | 利用 Claude 的语义理解能力从会话历史中发现可复用模式 |
| **Hidden assumption** | Claude 能在单次会话中分析大量 session 数据并发现非平凡模式 |
| **Likely failure mode** | Session 数据量大时 context overflow；pattern quality 完全取决于 LLM 推理质量 |

### 5B. Micro Design Highlights

#### M1: Hybrid Detection (Regex + Semantic)

**Pattern:** 两层检测 — 实时 regex 作快速过滤（UserPromptSubmit），AI semantic 做精确验证（/reflect 时）。

**Evidence:** `reflect_utils.py:629-749`（regex）+ `semantic_detector.py:46-125`（semantic）

**Why it works:** Regex 零延迟、零成本捕获高置信度修正；semantic 在异步审查时补充多语言和上下文理解。两层 confidence 取最大值 (`semantic_detector.py:235`)。

#### M2: Never-Crash Hook Philosophy

**Pattern:** 所有 hook 脚本都用 `try/except` 包裹 main()，异常时 `sys.exit(0)` 而非崩溃。

**Evidence:**
- `capture_learning.py:86-90`: `except Exception as e: ... sys.exit(0)`
- `check_learnings.py:46-51`: same pattern
- `post_commit_reminder.py:60-65`: same pattern
- `session_start_reminder.py:58-64`: same pattern

**Why it matters:** Hook 失败不应阻塞用户工作流。这是插件开发的关键原则。

#### M3: Confidence-Length Correlation

**Pattern:** 短消息 confidence boost (+0.10)，长消息 confidence penalty (-0.10 to -0.15)。

**Evidence:** `reflect_utils.py:740-745`:
```python
if text_length < MIN_SHORT_CORRECTION_LENGTH:
    confidence = min(0.90, confidence + 0.10)
elif text_length > 300:
    confidence = max(0.50, confidence - 0.15)
```

**Insight:** 短消息 ("no, use X") 更可能是直接修正；长消息更可能是任务请求。这是一个简洁有效的启发式。

#### M4: Explicit > Auto > Positive Classification Hierarchy

**Pattern:** 检测优先级：`remember:` (explicit, 0.90) > guardrail (0.85-0.90) > false positive rejection > positive feedback (0.70) > CJK corrections > English corrections。

**Evidence:** `reflect_utils.py:629-749` — `detect_patterns()` 的检查顺序。

**Why it works:** 用户显式标记永远最高优先；guardrail 模式（"don't do X unless"）代表用户挫败感，需要高置信度；false positive 在 correction 之前检查防止误报。

#### M5: Per-Project Queue with Migration

**Pattern:** Queue 从全局迁移到按项目隔离，保留向后兼容。

**Evidence:** `reflect_utils.py:42-95` — `migrate_global_queue()` 在 `load_queue()` 中自动调用，按 item 的 `project` 字段分发，迁移后删除全局文件。

**Why it works:** 零配置迁移，用户无需手动操作。

### 5C. Macro Design Highlights

#### Philosophy 1: Two-Stage Architecture (Automatic Capture + Manual Review)

核心设计哲学是将 "捕获" 和 "应用" 分离。Hook 自动捕获所有可能的修正到 queue，但永远不直接修改 CLAUDE.md。只有用户显式运行 `/reflect` 并审批后才写入。

**Rationale:** 自动捕获消除了用户需要记住"我刚才纠正了什么"的认知负担。手动审查防止误报污染长期记忆。这比完全自动或完全手动都更平衡。

**Evidence:** `CLAUDE.md:8-9`, `README.md:17-23`

#### Philosophy 2: Memory as a Tiered System

claude-reflect 将 Claude Code 的记忆视为 9 层层次结构，从全局到项目到路径级别，从高置信到低置信（auto memory）。每条 learning 根据内容和置信度路由到最合适的层级。

**Evidence:** `CLAUDE.md:30-42`, `commands/reflect.md:27-43`

#### Philosophy 3: Prompt as Orchestrator, Code as Infrastructure

代码层（Python scripts）负责数据操作：regex 检测、queue I/O、session 解析、semantic API 调用。流程编排（10 步审查工作流）完全在 prompt 中定义。这意味着工作流逻辑可以通过修改 markdown 文件迭代，无需改代码。

**Evidence:** `commands/reflect.md` 是 1500 行的纯 prompt 指令，而 `scripts/` 是无状态工具函数。

#### Philosophy 4: Graceful Degradation

每个外部依赖都有 fallback：
- `claude -p` 不可用 → 退回 regex-only 检测
- Queue 文件损坏 → 返回空列表
- Session 文件不存在 → 返回空列表
- 全局 queue 遗留 → 自动迁移

### 5D. Cross-Cutting Interconnections

1. **Capture → Queue → Reflect pipeline:** `capture_learning.py` 写入 queue，`/reflect` 读取 queue。两者通过 `reflect_utils.py` 共享路径计算和 queue 操作。

2. **Regex ↔ Semantic dual path:** `detect_patterns()`（regex）和 `semantic_analyze()`（AI）产生独立 confidence 分数，在 `validate_queue_items()` 中合并（取最大值）。

3. **Session files → Multiple consumers:** 同一 JSONL session 文件被 `extract_user_messages()`、`extract_tool_rejections()`、`extract_tool_errors()` 从不同角度解析。

4. **Memory hierarchy → Routing logic:** `find_claude_files()` 发现目标文件，`suggest_claude_file()` 建议路由，`/reflect` prompt 中的 Step 3/Step 7 执行实际写入。三者必须对 tier 定义保持一致。

5. **Skill improvement loop:** `/reflect` 检测到修正与 skill 相关时（Step 3.3），可以将 learning 路由回 skill file（Step 7b），形成 skill 自我改进的闭环。`/reflect-skills` 从 session 历史中发现新 skill 候选，形成第二个闭环。

---

## Phase 6 — Migration Assessment

### M1: Hybrid Detection Engine (Regex + Semantic)

| Dimension | Assessment |
|-----------|------------|
| **Transferability** | High |
| **Effort** | Medium (2-3 days) |
| **Prerequisite** | Python 3.6+, `claude -p` CLI |
| **Risk** | Low |
| **Failure modes** | Regex patterns 是 English-centric，CJK patterns 需要单独维护 |

**Detail:** `reflect_utils.py` 的 pattern detection 系统（CORRECTION_PATTERNS, GUARDRAIL_PATTERNS, FALSE_POSITIVE_PATTERNS, CJK_CORRECTION_PATTERNS）和 `semantic_detector.py` 的 AI validation 可以直接移植。核心约 300 行 Python。需要适配为 1st-cc-plugin 的 `references/` 资源文件模式。

### M2: Two-Stage Capture + Review Architecture

| Dimension | Assessment |
|-----------|------------|
| **Transferability** | High |
| **Effort** | Medium (3-5 days) |
| **Prerequisite** | Claude Code hooks API (UserPromptSubmit, PreCompact, PostToolUse, SessionStart) |
| **Risk** | Medium — hooks.json 格式需要适配 `${CLAUDE_PLUGIN_ROOT}` 变量 |
| **Failure modes** | Hook 执行环境差异（PATH、Python 版本）；per-project queue 路径编码差异 |

**Detail:** 架构模式（自动捕获到 queue + 手动 `/reflect` 审查）是 claude-reflect 的核心价值。移植时需要：(1) hooks.json 适配、(2) queue I/O 适配、(3) reflect command 精简（1500 行太长，应拆分为 SKILL.md + references/）。

### M3: Memory Hierarchy Routing

| Dimension | Assessment |
|-----------|------------|
| **Transferability** | Medium |
| **Effort** | Low (1-2 days) |
| **Prerequisite** | Claude Code 的多层 CLAUDE.md 支持 |
| **Risk** | Low |
| **Failure modes** | `suggest_claude_file()` 的启发式可能不匹配用户实际的文件组织方式 |

**Detail:** `find_claude_files()` 和 `suggest_claude_file()` 是独立的工具函数，可以直接复用。9 层 memory tier 的路由逻辑对任何需要"将知识写入正确位置"的 skill 都有价值。

### M4: Session History Analysis

| Dimension | Assessment |
|-----------|------------|
| **Transferability** | Medium |
| **Effort** | Low (1 day) |
| **Prerequisite** | `~/.claude/projects/` session JSONL 格式 |
| **Risk** | Medium — 依赖 Claude Code 内部 session 文件格式，可能在版本更新时变化 |
| **Failure modes** | Session 文件格式变更；`cleanupPeriodDays` 默认 30 天删除旧 session |

**Detail:** `extract_user_messages()`, `extract_tool_rejections()`, `extract_tool_errors()` 是有价值的 session 解析工具。但它们依赖 Claude Code 的 JSONL 内部格式（`type: "user"`, `isMeta`, `tool_result` 等），这不是公开 API。

### M5: `/reflect-skills` Pattern Discovery

| Dimension | Assessment |
|-----------|------------|
| **Transferability** | Low |
| **Effort** | High (5+ days) |
| **Prerequisite** | 大量 session 历史数据；`/reflect-skills` 的效果高度依赖 LLM 推理质量 |
| **Risk** | High — 完全 soft-enforced，输出质量不可预测 |
| **Failure modes** | Context overflow（大量 session 数据）；生成的 skill 质量不稳定；需要人工审查每个生成的 skill |

**Detail:** 概念有趣但实现全靠 prompt 驱动。1st-cc-plugin 已有 `skill-dev:create-skill` 提供更结构化的 skill 创建流程。`/reflect-skills` 的"从历史发现模式"理念可以作为 skill-dev 的输入源，而非独立移植。

### M6: Never-Crash Hook Pattern

| Dimension | Assessment |
|-----------|------------|
| **Transferability** | High |
| **Effort** | Trivial (< 1 hour) |
| **Prerequisite** | None |
| **Risk** | None |
| **Failure modes** | None |

**Detail:** 所有 hook 脚本使用 `try/except: sys.exit(0)` 包裹的模式应作为 1st-cc-plugin hook 开发的标准实践。

### Migration Priority Ranking

| Rank | Mechanism | Value | Effort | Priority |
|------|-----------|-------|--------|----------|
| 1 | Never-crash hook pattern (M6) | High | Trivial | **Immediate** |
| 2 | Hybrid detection engine (M1) | High | Medium | **High** |
| 3 | Memory hierarchy routing (M3) | Medium | Low | **High** |
| 4 | Two-stage architecture (M2) | High | Medium | **Medium** — 需要设计适配 |
| 5 | Session history analysis (M4) | Medium | Low | **Medium** — 有格式依赖风险 |
| 6 | Pattern discovery (M5) | Low | High | **Low** — 现有 skill-dev 更适合 |

---

## Appendix A — Key File Reference

| File | Lines | Purpose |
|------|-------|---------|
| `scripts/lib/reflect_utils.py` | 1174 | Core library: all shared functions |
| `scripts/lib/semantic_detector.py` | 562 | AI-powered analysis via claude CLI |
| `commands/reflect.md` | ~1500 | Main /reflect workflow prompt |
| `commands/reflect-skills.md` | ~360 | Skill discovery prompt |
| `hooks/hooks.json` | 48 | 4 hook event bindings |
| `scripts/capture_learning.py` | 91 | UserPromptSubmit hook entry |
| `tests/test_reflect_utils.py` | 1075 | Core utility tests |
| `tests/test_semantic_detector.py` | 729 | Semantic detector tests |
| `tests/test_memory_hierarchy.py` | 405 | Memory tier tests |

## Appendix B — Pre-Submit Checklist

| Check | Status |
|-------|--------|
| A. Source Inventory classified (Overview/Execution/Prompts/Enforcement/Evolution) | PASS |
| B. Prompt Traceability with repo_path + quote_excerpt (5 prompts cataloged) | PASS |
| C. Object Model with 3+ entities (5 entities: QueueItem, MemoryTarget, SemanticResult, SkillCandidate, ToolErrorAggregate) | PASS |
| D. State Machine with transitions (7-state lifecycle + trigger map) | PASS |
| E. Enforcement Audit: Hard (9) / Soft (11) / Unenforced (5) | PASS |
| F. Micro (5) + Macro (4) design highlights | PASS |
| G. 3+ failure modes with evidence (F1-F4 documented) | PASS |
| H. Migration candidates with ratings (M1-M6 with priority ranking) | PASS |
