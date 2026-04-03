# Workflow Research Report: Flowspec

> **Framework**: flowspec (Spec-Driven Development platform)
> **Repository**: `vendor/flowspec/` (jpoley/flowspec)
> **Version**: 0.4.008 (CLI) | 0.0.20 (plugin manifest)
> **Research Date**: 2026-04-02
> **Evidence Level**: Direct（源码级访问）

---

## 1. 框架概览

| Dimension | Value |
|-----------|-------|
| **Type** | Workflow harness + Agent orchestrator（混合型） |
| **Primary Language** | Python 3.11+（CLI：typer + rich） |
| **Target Platforms** | Claude Code, GitHub Copilot, Codex, Gemini CLI, Cursor, Windsurf |
| **Core Concept** | Spec-Driven Development (SDD) — 先写正式规格，再写代码 |
| **License** | MIT |
| **Dependencies** | typer, rich, httpx, pyyaml, jsonschema, mcp, node-pty |
| **Test Framework** | pytest（目标覆盖率 >80%） |
| **Linter/Formatter** | Ruff（替代 Black + Flake8 + isort） |
| **Package Manager** | UV |

### 目录结构

```
vendor/flowspec/
├── .agents/               # 15 specialized agent personas (markdown)
├── .beads/                # Issue tracking config for AI agents
├── .claude/               # Claude Code integration layer
│   ├── agents/            # 5 dispatchable agent files
│   ├── agents-config.json # Agent→workflow mapping (14 agents × 6 workflows)
│   ├── commands/flow/     # 22 slash commands (markdown)
│   ├── rules/             # 8 auto-loaded rule files
│   ├── settings.json      # Permissions, hooks, preferences
│   └── skills/            # 20 internal skills
├── .flowspec/             # Event logging & active work tracking
├── .languages/            # Language-specific guidance (C++, Go, Rust)
├── .stacks/               # 8 pre-configured tech stacks
├── build-docs/            # 150+ research, ADR, platform docs
├── docs/                  # User-facing guides & specs
├── examples/              # MCP integration examples
├── memory/                # Durable state (constitution, decisions, learnings)
├── schemas/               # JSON schemas for workflow config
├── scripts/               # Bash/Python/PowerShell utilities
├── src/flowspec_cli/      # Python source code
│   ├── workflow/          # State machine, validator, orchestrator (14 files)
│   ├── backlog/           # Backlog.md parsing, dep graphs (6 files)
│   ├── memory/            # Task memory store, lifecycle (8 files)
│   ├── security/          # Triage engine, fixer, SAST/DAST/SCA (20+ files)
│   ├── quality/           # Complexity scorer (3 files)
│   └── hooks/             # Event emitter, runner, config (8 files)
├── templates/             # 50+ templates (constitutions, docs, agents, memory)
├── tests/                 # 50+ test files
└── utils/                 # flowspec-netlog utility
```

### 文件统计

| Category | Count |
|----------|-------|
| 文件总数 | 500+ |
| Python SLOC（workflow 模块） | ~18,000 |
| 文档（markdown） | 150+ |
| 模板 | 50+ |
| 测试文件 | 50+ |
| 配置文件 | 8 个主要 |
| 斜杠命令 | 22 |
| Skills（内部） | 20 |
| Agent 人设 | 15 |

---

## 2. 源文件清单

### 概述

| File | Purpose |
|------|---------|
| `README.md` | 框架概述、快速上手、功能矩阵 |
| `CLAUDE.md` | Claude Code 集成指南（规则、工作流、agents） |
| `memory/constitution.md` (55K) | 全面的项目治理文件 — 层级、严格度、标准 |
| `memory/WORKFLOW_DESIGN_SPEC.md` | 工作流执行规格 |
| `build-docs/adr/`（60+ 文件） | 架构决策记录 |
| `build-docs/platform/` | 平台工程文档 |
| `.stacks/*/README.md` | 技术栈专属指南 |

### 执行层

| File | Purpose |
|------|---------|
| `.claude/commands/flow/*.md`（22 文件） | 每个工作流阶段的斜杠命令定义 |
| `.claude/skills/*/SKILL.md`（20 目录） | 内部 skill 定义 |
| `src/flowspec_cli/workflow/orchestrator.py` | 自定义工作流执行引擎 |
| `src/flowspec_cli/workflow/executor.py` | Agent 上下文中的工作流步骤执行器 |
| `src/flowspec_cli/workflow/transition.py` | 基于产物门控的状态转换 |
| `flowspec_workflow.yml` | 状态机 + 工作流 + agent 定义 |

### Prompt 层

| File | Purpose |
|------|---------|
| `.agents/*.md`（15 文件） | 专业化 agent 人设定义 |
| `.claude/agents/*.md`（5 文件） | Claude Code 可调度的 agent 定义 |
| `.claude/agents-config.json` | Agent→workflow 路由表 |
| `.languages/*/agent-personas.md` | 语言专属的专家指导 |
| `templates/agents/*.md` | Agent 模板文件 |

### 强制执行层

| File | Purpose |
|------|---------|
| `.claude/settings.json` | Hook 定义、权限拒绝列表、偏好设置 |
| `.claude/rules/critical.md` | 不可违反的规则（测试保护、DCO、PR 前检查） |
| `.claude/rules/rigor.md` | 4 阶段严格度强制执行（SETUP/EXEC/VALID/PR） |
| `.pre-commit-config.yaml` | Ruff lint + format hooks |
| `scripts/bash/pre-pr-check.sh` | PR 前校验（DCO + lint + format + tests） |
| `src/flowspec_cli/workflow/validator.py`（718 SLOC） | DAG 校验、环路检测、可达性分析 |
| `src/flowspec_cli/hooks/runner.py` | Hook 执行（含超时 + 环境净化） |
| `src/flowspec_cli/hooks/config.py` | Hook 配置校验（路径穿越、元字符） |
| `schemas/flowspec-workflow-schema.json` | 工作流配置的 JSON Schema |

### 演进层

| File | Purpose |
|------|---------|
| `tests/`（50+ 文件） | pytest 测试套件，覆盖 workflow、memory、security |
| `CHANGELOG.md` | 版本历史 |
| `build-docs/adr/decision-tracker.md` | 决策日志 |
| `.github/` | CI/CD 工作流 |
| `memory/learnings/` | 累积的项目经验 |
| `memory/decisions/` | 已记录的架构决策 |

---

## 3. 对象模型与上下文策略

### 一等实体

#### 3.1 工作流状态 (`flowspec_workflow.yml:1-52`)

```yaml
states:
  - name: "To Do"         # initial: true
  - name: "Assessed"
  - name: "Specified"
  - name: "Planned"
  - name: "In Implementation"
  - name: "Validated"
  - name: "Done"           # terminal: true
```

- **定义**：`flowspec_workflow.yml` states 数组
- **Schema**：`schemas/flowspec-workflow-schema.json`
- **生命周期**：初始化时创建 → 通过工作流执行进行转换 → 在 Done 时终止
- **校验**：`validator.py` 确保 DAG（无环路）、所有状态从初始状态可达、存在终止状态
- **分类**：**Fact object** — 表示当前任务进度

#### 3.2 工作流 (`flowspec_workflow.yml:54-180`)

```yaml
workflows:
  assess:
    command: "/flow:assess"
    agents: ["Workflow Assessor"]
    input_states: ["To Do"]
    output_state: "Assessed"
```

6 个核心工作流：assess, specify, plan, implement, validate, submit-n-watch-pr

- **定义**：`flowspec_workflow.yml` workflows map
- **必填字段**：command, agents, input_states, output_state
- **生命周期**：由斜杠命令调用 → 分发给 agents → 产出产物 → 转换状态
- **分类**：**Fact object** — 静态工作流定义

#### 3.3 转换 (`transition.py:1-624`)

```python
WORKFLOW_TRANSITIONS = [
    TransitionSchema(name="assess", from_state="To Do", to_state="Assessed",
                     input_artifacts=[...], output_artifacts=[Artifact("assessment_report", ...)]),
    # ... 7 total transitions
]
```

- **定义**：在 `transition.py` 中硬编码，带有产物要求
- **产物**：输入/输出产物定义，含路径模式（`{feature}`、`{NNN}`）
- **校验模式**：NONE, KEYWORD, PULL_REQUEST
- **分类**：**Evidence object** — 在转换边界强制验证产物存在性

#### 3.4 Agent 人设 (`.agents/*.md`, `.claude/agents-config.json`)

15 个 agent 人设映射到工作流：

| Agent | Loop | Workflows |
|-------|------|-----------|
| Software Architect | outer | plan |
| Platform Engineer | outer | plan |
| PM Planner | outer | specify |
| Frontend/Backend/AI-ML Engineer | inner | implement |
| Frontend/Backend Code Reviewer | inner | implement |
| Quality Guardian | outer | validate |
| Secure-by-Design Engineer | outer | validate |
| Tech Writer | outer | validate |
| Release Manager | outer | validate |
| SRE Agent | outer | operate |

- **定义**：`.agents/` 中的 Markdown 文件，包含专长、方法论、输出格式
- **路由**：`agents-config.json` 将 agent 名称映射到工作流列表
- **分类**：**Fact object** — 静态人设定义

#### 3.5 任务记忆 (`src/flowspec_cli/memory/store.py`)

```
backlog/memory/task-XXX.md  (active)
backlog/memory/archive/task-XXX.md  (archived)
```

- **定义**：带有 YAML frontmatter 的 Markdown 文件
- **生命周期**：在 `To Do → In Progress` 时创建 → 工作期间更新 → 在 `→ Done` 时归档 → 在 `→ Archive` 时删除
- **必含内容**：What, Why, Constraints, AC Status, Key Decisions（≤500 字）
- **Token 感知**：注入器（`injector.py`）截断至约 2000 tokens，保留近期上下文
- **分类**：**Judgment object** — 记录决策和进度

#### 3.6 宪章 (`memory/constitution.md`, `templates/constitutions/`)

3 个层级：Light / Medium / Heavy — 项目治理原则

- **定义**：在 `/flow:init` 时根据复杂度评分生成
- **内容**：核心原则、编码标准、质量门禁、工作流规则
- **生命周期**：创建一次 → 在所有工作流中被引用 → 通过 `/flow:reset` 更新
- **分类**：**Fact object** — 项目级治理

#### 3.7 严格度规则 (`.claude/rules/rigor.md`)

4 个阶段 × N 条规则，带强制执行模式（strict/warn/off）：

| Phase | Rules |
|-------|-------|
| SETUP | SETUP-001（明确计划）, SETUP-002（依赖项）, SETUP-003（可测试的 AC） |
| EXEC | EXEC-001（worktree）, EXEC-002（分支命名）, EXEC-003（决策日志）, EXEC-004（backlog 关联）, EXEC-006（状态跟踪） |
| VALID | VALID-002（lint/SAST）, VALID-004（无冲突）, VALID-005（AC 达成）, VALID-007（本地 CI） |
| PR | PR-001（DCO 签名） |

- **分类**：**Fact object** — 但强制执行力度各异（见第 4 节）

### 上下文流转策略

```
                    ┌─────────────────────────┐
                    │   constitution.md        │ ← Project-level (created at init)
                    │   (Light/Medium/Heavy)   │
                    └──────────┬──────────────┘
                               │ inherits
                    ┌──────────▼──────────────┐
                    │   .claude/rules/*.md     │ ← Session-level (auto-loaded)
                    │   (8 rule files)         │
                    └──────────┬──────────────┘
                               │ scopes
                    ┌──────────▼──────────────┐
                    │   task memory            │ ← Task-level (per task-XXX.md)
                    │   (≤500 words, ≤2K tok)  │
                    └──────────┬──────────────┘
                               │ injected via
                    ┌──────────▼──────────────┐
                    │   CLAUDE.md @import      │ ← Active context injection
                    │   (backlog/CLAUDE.md)    │
                    └──────────────────────────┘
```

**上下文隔离**：Agent 人设仅接收其领域相关的上下文。Security reviewer 为**只读**——报告发现，不可修改代码（`.claude/rules/agents.md`）。

**上下文压缩**：Token 感知截断（`injector.py`）保留近期上下文和关键决策，优先裁剪最旧的笔记。每个任务记忆硬限制约 2000 tokens。

**持久化**：宪章和规则持久化于文件中。任务记忆持久化于 `backlog/memory/`。决策记录至 `.flowspec/logs/decisions/`。事件记录至 `.flowspec/logs/events/`。

---

## 4. 流程与状态机

### 正常路径

```
User Request
    │
    ▼
/flow:init ──────────► constitution.md created
    │                   (complexity scoring → tier selection)
    ▼
/flow:assess ────────► docs/assess/{feature}-assessment.md
    │                   (scores: effort, components, integration, risk)
    │                   (recommendation: Full SDD / Spec-Light / Skip)
    ▼
/flow:specify ───────► docs/prd/{feature}-prd.md
    │                   (10-section PRD via PM Planner agent)
    │                   (creates backlog tasks via CLI)
    ▼
/flow:plan ──────────► docs/adr/ + docs/platform/
    │                   (parallel: Architect + Platform Engineer)
    │                   (ADRs, infrastructure design, DevSecOps)
    ▼
/flow:implement ─────► source code + tests
    │                   (parallel: Frontend + Backend + AI engineers)
    │                   (code review by dedicated reviewers)
    │                   (pre-PR validation: lint + format + tests)
    ▼
/flow:validate ──────► QA report + security report + docs
    │                   (parallel: QA + Security + Tech Writer + Release Mgr)
    │                   (4-stage parallel issue collection → batch report)
    ▼
/flow:submit-n-watch-pr ► PR created, CI monitored
    │
    ▼
  Done
```

**状态转换** (`flowspec_workflow.yml:182-260`)：

| Transition | From | To | Required Artifacts |
|------------|------|----|--------------------|
| assess | To Do | Assessed | → assessment_report |
| specify | Assessed | Specified | assessment_report → prd |
| plan | Specified | Planned | prd → adr |
| implement | Planned | In Implementation | adr → source_code |
| validate | In Implementation | Validated | source_code → qa_report |
| operate | Validated | Done | qa_report → (none) |
| complete | Done | Done | (terminal) |

### 失败路径 1：严格度规则违规

```
/flow:implement
    │
    ├─ EXEC-001 check: not in worktree?
    │   └─ rigor.md prescribes: create worktree first
    │      (Soft enforcement — prompt instruction, no code gate)
    │
    ├─ EXEC-002 check: branch naming wrong?
    │   └─ rigor.md prescribes: rename branch
    │      (Soft enforcement — prompt instruction only)
    │
    └─ Pre-PR check fails (lint/format/tests)
        └─ pre-pr-check.sh returns exit code 1
           (Hard enforcement — script blocks PR creation)
```

### 失败路径 2：规格质量门禁失败

```
/flow:specify
    │
    ├─ /flow:gate runs spec quality scoring
    │   └─ Score < 70/100?
    │       ├─ exit code 1 (failure)
    │       ├─ Provides improvement suggestions
    │       └─ User must improve spec and re-run
    │          (Hard enforcement — CLI exit code)
    │
    └─ --force flag available to bypass
        (Soft escape hatch — documented as "not recommended")
```

### 并行模型

| Phase | Parallel Agents | Sequential Dependencies |
|-------|-----------------|------------------------|
| plan | Architect ∥ Platform Engineer | 两者均需完成才能进入 implement |
| implement | Frontend ∥ Backend ∥ AI-ML | 全部完成才能进入 validate |
| validate | QA ∥ Security ∥ Tech Writer ∥ Release Mgr | 全部完成才能创建 PR |

并行执行通过 `backlog task edit <id> -l "parallel-work:frontend,backend"` 标签协调（`.claude/rules/agents.md`）。

### 自定义工作流 (`flowspec_workflow.yml:262-340`)

3 个预定义的自定义序列：

| Name | Steps | Description |
|------|-------|-------------|
| `quick_build` | assess → implement | 小任务跳过 specify/plan |
| `full_design` | assess → specify → plan | 完整设计，在 implement 前停止 |
| `ship_it` | assess → specify → plan → implement → validate | 端到端 |

自定义工作流支持：条件（`complexity >= 7`）、检查点（在 "spec-ing" 模式下暂停等待批准）、每步的严格度强制执行。

---

## 5. 强制执行审计

### 强制执行矩阵

| # | Constraint | Declared In | Enforcement Level | Mechanism | Evidence |
|---|-----------|-------------|-------------------|-----------|----------|
| E1 | 禁止删除测试 | `rules/critical.md` | **Soft** | 仅 prompt 指令 | 无 hook 或 pre-commit 检查阻止测试删除。规则引用 PR #545 作为警示但无代码强制执行。 |
| E2 | PR 前校验（lint+format+tests） | `rules/critical.md`, `scripts/bash/pre-pr-check.sh` | **Hard**（部分） | 脚本检查 4 项；Claude hooks 在 PostToolUse 时自动格式化 | `pre-pr-check.sh` 失败时返回退出码 1。但无 git hook 强制运行此脚本——agent 需自愿调用。 |
| E3 | 禁止直接提交到 main | `rules/git-workflow.md`, `rules/critical.md` | **Soft** | 仅 prompt 指令 | `.claude/settings.json` 中无分支保护 hook。依赖 GitHub 分支保护（外部）。 |
| E4 | DCO 签名 | `rules/critical.md`, `rules/git-workflow.md` | **Hard**（部分） | `pre-pr-check.sh` 检查 DCO；`settings.json` PreToolUse hook 检查 git 安全性 | 脚本检查签名。但无 pre-commit hook 强制使用 `-s` 标志。 |
| E5 | Ruff lint/format | `.pre-commit-config.yaml`, `settings.json` PostToolUse hook | **Hard** | Pre-commit hook 对暂存文件运行 ruff；PostToolUse 自动格式化 Python | `pre-commit-config.yaml:3-11` 配置 ruff v0.8.2。`settings.json` PostToolUse hook 运行自动格式化。 |
| E6 | 工作流状态 DAG（无环路） | `validator.py:400-520` | **Hard** | 代码：DFS 环路检测 + BFS 可达性分析 | `validator.py` 在检测到环路时抛出 ValidationError。在配置加载时运行。 |
| E7 | 产物门控转换 | `transition.py:1-624` | **Hard** | 代码：TransitionSchema 要求输入/输出产物 | `transition.py` WORKFLOW_TRANSITIONS 定义了每次转换所需的产物。 |
| E8 | 任务记忆 ≤500 字 | `rules/critical.md`, `memory/constitution.md` | **Soft** | Prompt 指令。注入器在约 2000 tokens 处截断，但写入时不强制 500 字限制。 | `injector.py` 在读取时截断。无写入时校验。 |
| E9 | 实现阶段使用 git worktree | `rules/rigor.md` EXEC-001 | **Soft** | 仅 prompt 指令 | 无 hook 在允许代码修改前检查是否处于 worktree 中。 |
| E10 | 分支命名规范 | `rules/rigor.md` EXEC-002, `rules/git-workflow.md` | **Soft** | 仅 prompt 指令 | 无校验脚本检查分支名格式。 |
| E11 | Hook 超时强制执行 | `hooks/runner.py` | **Hard** | 代码：SIGTERM → SIGKILL，可配置超时（最长 10 分钟） | `runner.py` 实现了基于信号的硬超时终止。 |
| E12 | Hook 脚本路径限制 | `hooks/config.py` | **Hard** | 代码：在脚本路径中阻止 `..` 和绝对路径；校验环境变量中的元字符 | `config.py` 在路径穿越或 shell 元字符时抛出 HooksSecurityError。 |
| E13 | 敏感文件访问拒绝 | `settings.json` 拒绝列表 | **Hard** | Claude Code 权限系统拒绝读取 secrets、constitution、lock 文件 | `settings.json` 拒绝规则覆盖 `Read(secrets/*)`、`Read(memory/constitution.md)` 等。 |
| E14 | Security reviewer 只读 | `rules/agents.md` | **Soft** | Prompt 指令："reports findings only, implementation agents address them" | 无代码阻止 security-reviewer agent 写入文件。 |
| E15 | Backlog.md 仅通过 CLI 编辑 | `rules/critical.md` | **Soft** | Prompt 指令："Never edit backlog.md directly — use CLI commands only" | 无文件写入 hook 阻止直接编辑 backlog.md。 |
| E16 | >80% 测试覆盖率 | `rules/testing.md` | **Soft** | Prompt 指令。pre-commit 或 pre-PR 脚本中无覆盖率门禁。 | `pre-pr-check.sh` 运行 pytest 但不检查覆盖率百分比。 |

### 强制执行汇总

| Level | Count | Percentage |
|-------|-------|-----------|
| Hard | 6（E2 部分, E4 部分, E5, E6, E7, E11, E12, E13） | ~50% |
| Soft | 8（E1, E3, E8, E9, E10, E14, E15, E16） | ~50% |
| Unenforced | 0 | 0% |

### 差距分析

**关键差距**：

1. **测试删除保护（E1）**：尽管被标记为"不可违反"，但没有任何机制阻止 `rm tests/*.py`。PR #545 事件被引用但此后并未添加 hook。**严重度：High** — 该规则正是为了防止此类情况而创建的，但它仍然可能发生。

2. **PR 前脚本需自愿执行（E2）**：脚本存在但必须手动调用。没有 git pre-push hook 或 CI 门禁确保其运行。**严重度：Medium** — Claude hooks 通过自动格式化部分缓解了此问题。

3. **覆盖率目标未验证（E16）**：声明了 80% 目标但无任何脚本检查。**严重度：Low** — 属于愿景性目标，非阻断性。

4. **Backlog.md 直接编辑（E15）**：关键规则但强制执行机制为零。**严重度：Medium** — 可能破坏任务状态。

---

## 6. Prompt 目录

### 6.1 关键 Prompt

#### P1: Software Architect Enhanced

| Field | Value |
|-------|-------|
| **role** | 架构规划者 |
| **repo_path** | `.agents/software-architect-enhanced.md` |
| **quote_excerpt** | "Uses Gregor Hohpe's principles (Software Architect Elevator, Enterprise Integration Patterns, Cloud Strategy, Platform Strategy)" |
| **stage** | plan |
| **design_intent** | 将架构决策根植于成熟的企业模式（Hohpe 框架），而非临时推理 |
| **hidden_assumption** | Agent 熟悉 Hohpe 的著作并能正确应用 EIP 术语 |
| **likely_failure_mode** | 对小型项目过度工程化；EIP 模式适用于企业级场景，可能不适合简单应用 |

#### P2: Quality Guardian

| Field | Value |
|-------|-------|
| **role** | 建设性质疑者 / QA 审查者 |
| **repo_path** | `.agents/quality-guardian.md` |
| **quote_excerpt** | "Three-Layer Critique: Acknowledge Value → Identify Risk → Suggest Mitigation" |
| **stage** | validate |
| **design_intent** | 通过将批评结构化为"先肯定后指风险"来防止"橡皮图章式"审查 |
| **hidden_assumption** | Agent 会遵循三层结构，而非默认为浅层认同 |
| **likely_failure_mode** | AI agent 倾向于附和；"Acknowledge Value"步骤可能占主导地位，削弱风险识别 |

#### P3: PM Planner（通过 `/flow:specify`）

| Field | Value |
|-------|-------|
| **role** | 产品需求创建者 |
| **repo_path** | `.claude/commands/flow/specify.md` |
| **quote_excerpt** | "10 sections: Executive Summary, User Stories, DVF+V Risk Assessment, Functional Requirements, Non-Functional Requirements, Task Breakdown, Discovery/Validation Plan, Acceptance Criteria/Testing, Dependencies/Constraints, Success Metrics" |
| **stage** | specify |
| **design_intent** | 通过结构化 PRD 模板在实现前强制进行全面的需求思考 |
| **hidden_assumption** | PRD 各节将填充真实的产品洞察，而非模板化内容 |
| **likely_failure_mode** | AI 可能为"Success Metrics"等章节生成看似合理但实质空洞的通用内容，缺乏真正的产品知识 |

#### P4: Assess Command

| Field | Value |
|-------|-------|
| **role** | 复杂度/风险评估者 |
| **repo_path** | `.claude/commands/flow/assess.md` |
| **quote_excerpt** | "Scores each dimension 1-10. Full SDD if any score ≥7 or total ≥18, Spec-Light if any ≥4 or total ≥10, else Skip SDD" |
| **stage** | assess |
| **design_intent** | 自适应工作流——简单任务跳过仪式，复杂任务强制完整流程 |
| **hidden_assumption** | AI agent 的 1-10 评分能产生有意义的、校准过的结果 |
| **likely_failure_mode** | 分数膨胀（AI 在模糊维度上默认给出中偏高分数）或跨会话校准不一致 |

#### P5: Secure-by-Design Engineer

| Field | Value |
|-------|-------|
| **role** | 安全审查者 |
| **repo_path** | `.agents/secure-by-design-engineer.md` |
| **quote_excerpt** | "Risk Assessment → Apply Security-First Principles → Comprehensive Reviews (threat modeling, architecture, code, config, access control, data flow, dependencies, monitoring)" |
| **stage** | validate |
| **design_intent** | 将安全融入每个审查周期，而非事后补充 |
| **hidden_assumption** | AI agent 仅凭项目上下文就能进行有意义的威胁建模 |
| **likely_failure_mode** | 给出不考虑实际部署环境或威胁模型的通用安全建议 |

#### P6: Workflow Executor Skill

| Field | Value |
|-------|-------|
| **role** | 自动化工作流步骤调用者 |
| **repo_path** | `.claude/skills/workflow-executor/SKILL.md` |
| **quote_excerpt** | "Load config → Get execution plan → Invoke each command → Update backlog via MCP" |
| **stage** | Any（元编排器） |
| **design_intent** | 实现无需手动命令调用的自主多步骤工作流执行 |
| **hidden_assumption** | MCP backlog 服务器正在运行且可访问；Skill tool 在 agent 上下文中可用 |
| **likely_failure_mode** | 工作流执行中 MCP 连接失败导致状态不一致；无回滚机制 |

### 6.2 设计亮点 — 微观

#### M1: 复杂度自适应工作流选择

**观察**：`/flow:assess` 在 8 个维度上评分（effort、components、integration、risk、security、compliance、data sensitivity、architecture impact），并路由到不同的仪式级别。

**证据**：`commands/flow/assess.md` — "Full SDD if any score ≥7 or total ≥18, Spec-Light if any ≥4 or total ≥10, else Skip SDD"

**重要性**：防止对小任务过度工程化，同时确保复杂任务获得适当的规格说明。三层体系（Full/Light/Skip）是该框架的核心价值主张。

**可迁移性**：**Direct** — 复杂度评分 → 工作流层级选择是一个清晰、可移植的模式。具体阈值（≥7/≥18/≥4/≥10）需要按项目校准。

#### M2: 产物门控状态转换

**观察**：每次状态转换都需要特定的输入产物并产生输出产物。转换由代码校验（`transition.py` TransitionSchema）。

**证据**：`transition.py:WORKFLOW_TRANSITIONS` — 7 个转换，含 Artifact 对象指定路径模式如 `docs/assess/{feature}-assessment.md`

**重要性**：防止"空转换"——即状态推进但实际上没有工作产出。这是对"展示你的成果"的 Hard 强制执行。

**可迁移性**：**Inspired** — 产物概念很好，但与 flowspec 的文件路径约定紧密耦合。若目录结构不同则需重新设计。

#### M3: Inner/Outer Loop Agent 分类

**观察**：Agent 被分为 "inner loop"（快速迭代：工程师、审查者）和 "outer loop"（治理：架构师、规划者、QA）。

**证据**：`flowspec_workflow.yml:340-380` — `agent_loops: { inner: [frontend-engineer, backend-engineer, ...], outer: [software-architect, platform-engineer, ...] }`

**重要性**：将速度关注与治理关注分离。Inner loop agent 不做架构决策；outer loop agent 不写实现代码。

**可迁移性**：**Direct** — 清晰的概念分离，适用于任何多 agent 工作流。

#### M4: Token 感知记忆注入

**观察**：任务记忆在注入 agent 上下文前被截断至约 2000 tokens。截断保留近期上下文和关键决策，优先裁剪最旧的笔记。

**证据**：`src/flowspec_cli/memory/injector.py` — `truncate_memory_content()` 含章节感知截断策略

**重要性**：防止上下文窗口膨胀，同时维持跨会话的决策连续性。

**可迁移性**：**Direct** — 带优先级章节的 Token 感知截断是一个普遍适用的模式。

#### M5: 三层批评模式

**观察**：Quality Guardian 使用结构化批评：Acknowledge Value → Identify Risk → Suggest Mitigation。

**证据**：`.agents/quality-guardian.md` — "Three-Layer Critique framework"

**重要性**：对抗 AI 的附和偏见。通过将"identify risk"设为中间步骤（而非第一步），审查显得建设性而非对抗性。

**可迁移性**：**Direct** — 可用于任何代码审查 prompt。

#### M6: 宪章层级体系

**观察**：项目治理随复杂度缩放：Light（最小规则）、Medium（标准）、Heavy（完整仪式）。

**证据**：`templates/constitutions/` — 三个独立模板文件；`/flow:init` 根据复杂度评分自动选择

**重要性**：一刀切的治理必然失败。CLI 工具不需要与分布式微服务相同的流程。

**可迁移性**：**Inspired** — 分层治理的概念非常优秀。具体的宪章模板是 flowspec 特有的。

### 6.3 设计亮点 — 宏观

#### X1: Spec-Driven Development 作为方法论

**观察**：Flowspec 的核心论点是正式规格（PRD → ADR → 实现）能改善 AI 辅助开发的成果。这不是 TDD 或 BDD，而是 "spec-first"——先写你想要什么，再写如何构建。

**证据**：README、`skills/sdd-methodology/SKILL.md`、宪章层级全部围绕 assess→specify→plan→implement→validate 管线

**强制执行级别**：**Soft** — 工作流被推荐和跟踪，但没有任何机制阻止未经 `/flow:specify` 就执行 `/flow:implement`。状态转换已定义，但像 `quick_build` 这样的自定义工作流会跳过步骤。

**重要性**：将规格说明定位为首要质量杠杆，而非测试。测试验证规格；规格定义要构建什么。

#### X2: 流程即代码（部分实现）

**观察**：工作流状态机在 YAML（`flowspec_workflow.yml`）中定义，由 Python 代码（`validator.py`）校验。转换有产物要求。自定义工作流可组合。

**证据**：`validator.py`（718 SLOC）运行 DAG 校验、环路检测、可达性分析。`orchestrator.py`（441 SLOC）执行自定义工作流序列。

**强制执行级别**：工作流配置有效性为 **Hard**，实际工作流执行顺序为 **Soft**。

**重要性**：配置经过校验，但工作流执行依赖 agent 自愿按正确顺序调用命令。没有运行时编排器阻止乱序执行。

#### X3: 评审者分离 — 部分实现

**观察**：代码审查者与实现者是独立的 agent。Security reviewer 为只读。但审查结果并非由代码门控——而是通过 prompt 强制执行。

**证据**：`.claude/rules/agents.md` — "Security reviewer: read-only access, reports findings only" | `.claude/agents/security-reviewer.md` — 独立的 agent 文件

**强制执行级别**：**Soft** — 无代码阻止 security-reviewer 写入。无门禁在安全审查失败时阻止合并。

**重要性**：真正的评审者分离要求审查者的输出作为进展门禁。此处审查仅为建议性的。

#### X4: 验证优于自我报告 — 混合实现

**观察**：PR 前脚本（`pre-pr-check.sh`）独立验证 lint/format/tests。但许多严格度规则（worktree、分支命名、backlog 关联）信任 agent 自我报告。

**证据**：`pre-pr-check.sh` 硬检查 4 项。`rigor.md` 定义了 12+ 条规则，但大多数无验证机制。

**强制执行级别**：4 条规则为 **Hard**，8+ 条规则为 **Soft**

**重要性**：该框架有正确的直觉（验证，而非信任）但应用不一致。Hard 强制执行的项目（lint、format、tests）是最容易自动化的；更难验证的项目（worktree 使用、决策记录）仍然基于信任。

#### X5: 人工审批检查点

**观察**：自定义工作流支持 "spec-ing" 模式，含暂停等待用户批准的检查点。assess 命令的 `--mode` 覆盖标志赋予人类对工作流路由的控制权。

**证据**：`commands/flow/custom.md` — "supports checkpoints (spec-ing mode)"；`commands/flow/assess.md` — "`--mode full|light|skip` override"

**重要性**：在一个否则高度自主的管线中维持人类主导权。用户可以覆盖 AI 复杂度评分并在任何步骤暂停。

### 6.4 交叉关联分析

| Dimension | Analysis |
|-----------|----------|
| **Prompt ↔ Skill** | 命令（`.claude/commands/flow/`）通过 Skill tool 调用 skills（`.claude/skills/`）。Skills 之间不直接链式调用——由编排器编排顺序。 |
| **Gate ↔ Flow** | 质量门禁位于 specify→plan 之间（`/flow:gate` 检查规格质量 ≥70/100）和 implement→validate 之间（pre-PR 检查）。plan→implement 之间无门禁。 |
| **Review ↔ Test** | 审查基于 agent（建议性）。测试通过 `pre-pr-check.sh` 门控（Hard）。无自动化审查门禁。 |
| **Context ↔ Scope** | 三层：constitution（项目级）→ rules（会话级）→ task memory（任务级）。Token 预算：每任务约 2000 tokens。规则自动加载。 |
| **Error ↔ Recovery** | Hook 故障为 fail-safe（记录日志，不崩溃工作流）。工作流故障需手动 `/flow:reset`。无自动重试。 |

---

## 7. 失败模式

### F1: 规格表演

**症状**：PRD 和 ADR 生成内容看似合理但实质通用。每个章节都被填充，但缺乏真正的产品洞察。

**证据**：`/flow:specify` 要求 10 个 PRD 章节，包括"Success Metrics"和"Discovery/Validation Plan"。AI agent 可以为这些章节生成结构上有效但实质空洞的内容。

**根因**：没有质量门禁校验规格说明的语义质量——仅校验结构完整性。`/flow:gate` 以 70/100 评分但评分标准在源码中不可见。

**影响**：虚假的就绪感。团队带着看似完整但未约束设计空间的规格进入实现阶段。

**框架缓解**：宪章层级（Light 层级跳过重量级规格章节）。覆盖模式（`--mode skip`）允许用户绕过。

**迁移启示**：如果移植 spec-driven 工作流，必须构建语义质量检查，而非仅结构检查。

### F2: 评估中的分数膨胀

**症状**：`/flow:assess` 持续将任务路由到 Full SDD 或 Spec-Light，因为 AI agent 在模糊维度上默认给出中偏高分数。

**证据**：评估评分使用 8 个维度，每个 1-10 分。阈值：任意单项 ≥7 → Full SDD，任意单项 ≥4 → Spec-Light。在 8 个维度中，即使只有一个评 4+（低于中位数），就触发 Spec-Light。

**根因**：低阈值与 AI 倾向于中等分数的组合。一个所有维度评 3（低复杂度）的任务总分为 24，远超 ≥10 的 Spec-Light 阈值。实际上，Skip SDD 要求所有维度低于 4 且总分低于 10。

**影响**："Skip SDD"路径在正常 AI 评分下几乎不可达，违背了自适应工作流的初衷。

**框架缓解**：`--mode` 覆盖允许用户强制跳过。但这破坏了自动适应。

**迁移启示**：基于实际任务分布校准评分阈值，而非理论范围。

### F3: 关键规则的 Soft 强制执行

**症状**：标记为"不可违反"的规则（测试删除、backlog.md 编辑、worktree 使用）被违反，因为强制执行仅通过 prompt。

**证据**：`rules/critical.md` 声明"Never delete tests — no exceptions except with explicit human approval"，但无 hook、pre-commit 检查或文件写入保护阻止 `rm tests/*.py`。同样，"Never edit backlog.md directly"也无写入保护机制。

**根因**：规则声明与强制执行实现之间的差距。该框架在基于 prompt 的规则上投入很大，但未对其最关键的约束闭合代码级门控。

**影响**：在高速度或多 agent 场景下，prompt 指令可能被忽略或遗忘。最需要最强强制执行的规则却拥有最弱的强制执行。

**框架缓解**：宪章和规则在每个会话中自动加载。Claude Code hooks 在 PreToolUse 和 PostToolUse 时运行。但 hooks 不检查测试删除或直接编辑 backlog。

**迁移启示**：对关键规则，始终构建代码级强制执行（hooks、校验器、CI 门禁）——prompt 指令是必要的但不充分。

### F4: 状态管理的 MCP 依赖

**症状**：当 MCP backlog 服务器不可用时工作流状态更新失败，导致任务处于不一致状态。

**证据**：`executor.py` 通过 MCP 更新 backlog 任务。`.mcp.json` 配置了 9 个 MCP 服务器。如果 backlog MCP 宕机，任务状态与实际工作状态产生分歧。

**根因**：状态管理依赖外部服务（MCP）而非本地文件操作。无回退或离线模式用于状态跟踪。

**影响**：MCP 不可用时工作流静默中断。Agent 继续工作但状态未被跟踪。

**框架缓解**：Backlog CLI 提供本地文件操作作为替代（`backlog task edit`）。但工作流执行器专门使用 MCP。

**迁移启示**：状态管理应具备本地优先回退。不要依赖网络服务来管理核心工作流状态。

### F5: Agent 交接中的上下文丢失

**症状**：当并行 agent（如 implement 阶段的 Frontend + Backend）完成工作后，它们各自的上下文不合并。后续阶段可能遗漏跨 agent 的决策。

**证据**：`rules/agents.md` 描述通过标签进行并行执行。每个 agent 获得自己的上下文。任务记忆（≤500 字、≤2000 tokens）是唯一的共享状态。

**根因**：Token 预算约束（每任务 ≤2000 tokens）限制了跨 agent 边界可保留的内容。一个 agent 的关键决策可能无法放入共享记忆。

**影响**：后端 agent 做出的架构决策可能与前端 agent 的假设冲突。validate 阶段可能无法看到完整画面。

**框架缓解**：决策记录至 `.flowspec/logs/decisions/` 提供审计线索。但这不会自动注入 agent 上下文。

**迁移启示**：多 agent 工作流需要在并行阶段之间进行显式的决策聚合，而非仅依赖共享记忆文件。

---

## 8. 迁移评估

### 候选机制

| # | Mechanism | Transferability | Effort | Prerequisite | Risk |
|---|-----------|----------------|--------|-------------|------|
| M1 | 复杂度自适应工作流路由 | **Direct** | S | 评分标准定义 | 未校准时的分数膨胀 |
| M2 | 产物门控状态转换 | **Inspired** | M | 定义产物类型和路径约定 | 对简单任务过度约束 |
| M3 | Inner/outer loop agent 分类 | **Direct** | S | Agent 定义机制 | 实践中的边界违反 |
| M4 | Token 感知记忆注入 | **Direct** | M | 记忆存储 + 截断算法 | 截断时丢失关键上下文 |
| M5 | 三层批评模式 | **Direct** | S | 审查 prompt 模板 | AI 仍然倾向附和 |
| M6 | 宪章层级体系 | **Inspired** | L | 模板系统 + 初始化工作流 | 层级选择准确度 |
| M7 | PR 前校验脚本 | **Direct** | S | Linter + 测试运行器已配置 | 自愿调用（非强制） |
| M8 | 自定义工作流组合 | **Inspired** | L | 工作流引擎 + YAML schema | 编排代码的复杂度 |
| M9 | 决策/事件日志 | **Direct** | S | 日志目录 + 格式约定 | 日志审查纪律 |
| M10 | Fail-safe hook 执行 | **Direct** | M | Hook 运行器 + 超时 + 信号处理 | Hook 静默失败时遗漏关键事件 |

### 建议采纳顺序

1. **M5 三层批评模式**（S，零前置条件，立即提升审查质量）
2. **M3 Inner/outer loop 分类**（S，概念性，改善 agent 设计纪律）
3. **M7 PR 前校验脚本**（S，具体可操作，立即获得质量门禁）
4. **M9 决策/事件日志**（S，轻量级，提升可审计性）
5. **M4 Token 感知记忆注入**（M，需要记忆基础设施，长期价值高）
6. **M1 复杂度自适应路由**（概念上 S，但需要校准工作）
7. **M2 产物门控转换**（M，需要产物 schema 设计）
8. **M10 Fail-safe hooks**（M，需要 hook 基础设施）
9. **M6 宪章层级**（L，需要模板系统 + 初始化工作流）
10. **M8 自定义工作流组合**（L，需要工作流引擎）

### 必须构建的强制执行机制

如果移植 flowspec 模式，以下**代码级强制执行机制**是必需的（flowspec 本身缺少这些）：

| Mechanism | What It Protects | Implementation |
|-----------|-----------------|----------------|
| 测试删除保护 | 防止 `rm tests/*` | PreToolUse hook 检查文件路径 |
| Backlog 写入保护 | 防止直接编辑 `backlog.md` | PreToolUse hook 拦截 Write/Edit tool |
| 覆盖率门禁 | 强制 >80% 阈值 | 测试后 hook 检查覆盖率输出 |
| 审查门禁 | 无审查完成则阻止合并 | CI 检查或 pre-merge hook |
| 分支保护 | 强制禁止直接提交到 main | Git hook 或 GitHub 分支保护 |

---

## 9. 待解问题

1. **规格质量评分算法**：`/flow:gate` 检查规格质量（目标 70/100），但评分标准在源码中不可见。100 分如何分配？是结构性的还是语义性的？

2. **Outer loop 实现**：README 提到"Promote/Observe/Operate/Feedback" outer loop，但指出该部分"handled by falcondev。"它如何与 inner loop 状态机集成？

3. **MCP backlog 服务器实现**：Backlog MCP 服务器被引用但其源码不在仓库中。它是单独的包吗？如果不可用，工作流状态会怎样？

4. **Agent 人设效果**：15 个专业化 agent 人设是否比一个精心提示的通用 agent 效果可衡量地更好？该框架假定专业化能提升质量，但未提供评估数据。

5. **自定义工作流采纳情况**：3 个预定义的自定义工作流（quick_build、full_design、ship_it）——实践中是否真正被使用，还是所有人都默认使用标准序列？

---

## 附录：来源可追溯性

| Claim | Source | Line/Section |
|-------|--------|-------------|
| 7 个工作流状态 | `flowspec_workflow.yml` | states array (lines 1-52) |
| 6 个核心工作流 | `flowspec_workflow.yml` | workflows map (lines 54-180) |
| DAG 环路检测 | `validator.py` | lines 400-520 (DFS algorithm) |
| 产物门控转换 | `transition.py` | WORKFLOW_TRANSITIONS constant (lines 1-624) |
| 15 个 agent 人设 | `.agents/*.md` | 15 markdown files |
| Agent→workflow 路由 | `.claude/agents-config.json` | 13 agents × 6 workflows |
| 22 个斜杠命令 | `.claude/commands/flow/*.md` | 22 markdown files |
| 20 个内部 skills | `.claude/skills/*/SKILL.md` | 20 directories |
| 8 个自动加载规则 | `.claude/rules/*.md` | 8 markdown files |
| Pre-commit hooks | `.pre-commit-config.yaml` | ruff v0.8.2 lint + format |
| PR 前脚本 | `scripts/bash/pre-pr-check.sh` | 4-item check (DCO, lint, format, tests) |
| Claude Code hooks | `.claude/settings.json` | SessionStart, PreToolUse, PostToolUse, Stop |
| Hook 安全性（路径穿越） | `hooks/config.py` | HooksSecurityError on `..` or absolute paths |
| Hook 超时强制执行 | `hooks/runner.py` | SIGTERM → SIGKILL with configurable limit |
| 任务记忆截断 | `memory/injector.py` | ~2000 token limit, section-aware truncation |
| 任务记忆生命周期 | `memory/lifecycle.py` | State-driven create/archive/restore/delete |
| 宪章层级 | `templates/constitutions/` | light.md, medium.md, heavy.md |
| Token 感知上下文注入 | `memory/injector.py` | @import directive in CLAUDE.md |
| 三层批评模式 | `.agents/quality-guardian.md` | Acknowledge → Risk → Mitigate |
| 分数膨胀风险 | `commands/flow/assess.md` | any ≥4 → Spec-Light, total ≥10 → Spec-Light |
| 测试删除未强制执行 | `.claude/rules/critical.md` + settings.json | Rule exists, no hook implements it |
| Security reviewer 只读声明 | `.claude/rules/agents.md` | Prompt-only, no code enforcement |
