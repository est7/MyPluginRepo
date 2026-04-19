# Workflow Research: ralph-orchestrator

**Date**: 2026-04-12
**Source**: `vendor/ralph-orchestrator` (https://github.com/mikeyobrien/ralph-orchestrator)
**Analyst mode**: Single
**Focus**: All

---

## 1. Framework Profile

| Attribute | Value |
|-----------|-------|
| **Type** | Agent Orchestrator + Workflow Harness hybrid |
| **Total files** | 1036 |
| **Prompt files** | 18 (3 agents + 13 internal skills + 2 public skills) |
| **Scripts/hooks** | 8 (2 git hooks + 6 scripts) |
| **Test files** | ~30+ (smoke, E2E, BDD, unit, integration, web) |
| **Entry points** | `CLAUDE.md`, `AGENTS.md`, `Cargo.toml`, `Justfile`, `package.json` |
| **Registration mechanism** | `.claude/agents/*.md` (agents), `.claude/skills/*/SKILL.md` (internal skills), `skills/*/SKILL.md` (public skills), `presets/*.yml` (hat collections) |
| **Language** | Rust (core), TypeScript (web dashboard), YAML (presets/config) |

### Directory Map

```
ralph-orchestrator/
├── CLAUDE.md / AGENTS.md          ← 设计哲学 + 开发指引
├── Cargo.toml                     ← workspace 根配置
├── Justfile                       ← 构建/CI recipes
├── ralph.reviewer.yml             ← PR review preset
├── crates/
│   ├── ralph-cli/                 ← CLI 入口 (run, plan, task, loops, web, wave)
│   │   ├── src/loop_runner.rs     ← 🔑 主循环执行器
│   │   └── presets/               ← 12 个内置 hat collection presets
│   ├── ralph-core/                ← 核心编排逻辑
│   │   ├── src/hatless_ralph.rs   ← 🔑 hat 系统 + prompt 构建 (2982 行)
│   │   ├── src/event_loop/        ← 🔑 事件循环
│   │   ├── src/wave_*.rs          ← Wave 并行系统
│   │   ├── src/memory*.rs         ← 记忆系统
│   │   ├── src/task*.rs           ← 任务系统
│   │   └── data/                  ← 嵌入式 prompt 模板
│   ├── ralph-adapters/            ← 后端集成 (Claude, Kiro, Gemini, Codex...)
│   ├── ralph-telegram/            ← Telegram 人机交互
│   ├── ralph-tui/                 ← 终端 UI (ratatui)
│   ├── ralph-e2e/                 ← E2E 测试框架 + BDD features
│   ├── ralph-proto/               ← 协议定义
│   └── ralph-bench/               ← 基准测试
├── .claude/
│   ├── agents/                    ← 3 个 agent 定义
│   └── skills/                    ← 13 个内部 skill
├── skills/                        ← 2 个公共 skill (ralph-hats, ralph-loop)
├── scripts/                       ← CI gate 脚本
├── .hooks/                        ← git hooks (pre-commit, pre-push)
├── backend/                       ← Web 后端 (Fastify + tRPC + SQLite)
└── frontend/                      ← Web 前端 (React + Vite + TailwindCSS)
```

---

## 2. Source Inventory

### Overview Sources

| File | Type | Why It Matters |
|------|------|---------------|
| `README.md` | 项目文档 | 安装、Quick Start、架构概览、功能列表 |
| `CLAUDE.md` / `AGENTS.md` | 设计哲学 | 6 条 Ralph Tenets、Anti-Patterns、开发规范 |
| `CONTRIBUTING.md` | 贡献指南 | 开发环境、测试策略、PR 流程 |
| `.agents/summary/*.md` | 架构摘要 | 自动生成的架构、组件、数据模型、接口文档 |

### Execution Sources

| File | Type | Why It Matters |
|------|------|---------------|
| `crates/ralph-cli/src/loop_runner.rs` | 循环执行器 | 主循环逻辑，hat 调度，wave 执行 |
| `crates/ralph-core/src/event_loop/mod.rs` | 事件循环 | 事件路由，hat 选择，迭代控制 |
| `crates/ralph-core/src/hatless_ralph.rs` | hat 系统 | prompt 构建，objective 注入，topology 管理 |
| `presets/code-assist.yml` | 工作流 preset | 4-hat TDD 工作流 (Planner→Builder→Critic→Finalizer) |
| `presets/*.yml` | hat collection | 12 个内置 preset（TDD、review、debug 等） |

### Prompt Sources

| File | Type | Why It Matters |
|------|------|---------------|
| `.claude/agents/code-assist.md` | agent | TDD 实现伙伴 + 代码教练 |
| `.claude/agents/ralph-e2e-verifier.md` | agent | E2E 诊断分析师 |
| `.claude/agents/ralph-loop-runner.md` | agent | 循环执行观察者 |
| `.claude/skills/pdd/SKILL.md` | skill | Prompt-Driven Development 规划 |
| `.claude/skills/code-assist/SKILL.md` | skill | TDD 实现流程 |
| `.claude/skills/test-driven-development/SKILL.md` | skill | RED-GREEN-REFACTOR 执行 |
| `.claude/skills/review-pr/SKILL.md` | skill | 回归感知 PR review |
| `crates/ralph-core/data/ralph-tools.md` | 嵌入式 prompt | 工具命令参考 |

### Enforcement Sources

| File | Type | Why It Matters |
|------|------|---------------|
| `.hooks/pre-commit` | git hook | 调用 `ci-rust-gate.sh --skip-hooks-bdd --skip-mock-e2e` |
| `.hooks/pre-push` | git hook | 调用完整 `ci-rust-gate.sh` |
| `scripts/ci-rust-gate.sh` | 中央 gate 脚本 | fmt + clippy + test + BDD + mutation |
| `scripts/hooks-bdd-gate.sh` | BDD enforcer | 18 条验收标准 (AC-01..AC-18) |
| `scripts/hooks-mutation-gate.sh` | mutation gate | 55% 操作分数阈值 |
| `scripts/sync-embedded-files.sh` | 同步校验 | 嵌入文件漂移检测 |
| `.github/workflows/ci.yml` | CI | 5 个 jobs: embedded-files, fmt, test, web, package |
| `Cargo.toml` | workspace 配置 | `forbid(unsafe_code)`, `clippy -D warnings` |

### Evolution Evidence

| Source | Type | Why It Matters |
|--------|------|---------------|
| `CHANGELOG.md` | 版本历史 | v2.2.1 (2025-01) → v2.9.2 (2026-04)，记录所有架构演进 |
| `crates/ralph-e2e/features/hooks/TRACEABILITY.md` | 追溯矩阵 | AC-01..AC-18 到测试用例的映射 |
| `crates/ralph-e2e/features/hooks/*.feature` | BDD scenarios | Gherkin 验收场景 |

---

## 3. Object Model

### First-Class Entities

| Entity | Definition Location | Required Fields | Lifecycle | Fact/Judgment/Evidence |
|--------|-------------------|-----------------|-----------|----------------------|
| **Hat** | `ralph-proto` + preset YAML | name, triggers, publishes, instructions | 定义 → 注册 → 事件触发 → 执行 → 发布事件 → 退出 | Fact (角色定义) |
| **Event** | `ralph-proto` (Event type) | topic, payload | 发布 → 路由 → 消费 | Evidence (执行信号) |
| **Loop** | `loop_runner.rs` + `.ralph/loop.lock` | PID, prompt, config | 启动 → 迭代 → LOOP_COMPLETE/超限 → 终止 | Evidence (执行实例) |
| **Memory** | `memory.rs` + `.ralph/agent/memories.md` | content (markdown) | 创建 → 持久化 → 跨 session 读取 | Fact (学习记录) |
| **Task** | `task.rs` + `.ralph/agent/tasks.jsonl` | key, description, status | pending → in_progress → completed/blocked | Fact (工作单元) |
| **Wave** | `wave_tracker.rs` + `wave_detection.rs` | wave_id, payloads, concurrency | 发射 → 并行执行 → 结果合并 → 聚合 | Evidence (并行执行) |
| **Spec** | `.ralph/specs/*.md` | 设计文档 | 创建 → 审批 → 引用 → 归档 | Fact (需求规格) |
| **Code Task** | `.ralph/tasks/*.code-task.md` | YAML frontmatter + Given-When-Then | pending → in_progress → completed | Fact (可执行任务) |

### Entity Relationships

```
Spec (.ralph/specs/)
  └──▶ Code Task (.code-task.md)  [1:N]
         └──▶ Runtime Task (tasks.jsonl)  [1:1]
                └──▶ Hat (via Event routing)  [N:1]
                       ├──▶ Event (publishes)  [1:N]
                       └──▶ Memory (writes)  [1:N]

Loop
  ├──▶ Hat Collection (preset YAML)  [1:N]
  ├──▶ Event Bus (routes events)  [1:1]
  ├──▶ Wave (parallel hat instances)  [1:N]
  └──▶ Worktree (parallel loops)  [1:N]
```

### Context Isolation Strategy

| Scope | What Flows | Mechanism | Evidence |
|-------|-----------|-----------|----------|
| Orchestrator → Hat | objective, pending events, topology table | prompt 注入（每次迭代重建） | `hatless_ralph.rs:351-401` |
| Hat → Hat | event topic + payload | EventBus pub/sub，磁盘持久化 | `event_loop/mod.rs` |
| Iteration → Iteration | memories.md, tasks.jsonl | 磁盘文件，每次迭代 re-read | `CLAUDE.md:77` (Tenet #1) |
| Loop → Loop | symlinked memories/specs/tasks | git worktree + symlink | `CLAUDE.md:122-135` |
| Agent → Human | question/guidance | Telegram bot (`human.interact` → block) | `ralph-telegram/` |

**Token 预算策略**: 目标 40-60% of ~176K usable tokens（"smart zone"）。每次迭代仅注入 active hats 的 instructions，非活跃 hats 仅显示 topology table（`hatless_ralph.rs:344-348`）。

---

## 4. Flow & State Machine

### Happy Path (code-assist preset)

1. 用户执行 `ralph run -c presets/code-assist.yml -p "..."` — `ralph-cli/src/loops.rs`
2. 解析配置，创建 EventLoop + HatlessRalph — `event_loop/mod.rs`
3. 检测 fresh start，发布 `build.start` — `hatless_ralph.rs:426-443`
4. **Planner hat** 激活：读取 prompt，分解为 step-wave，创建 runtime tasks，发布 `tasks.ready` — `presets/code-assist.yml (planner)`
5. **Builder hat** 激活：执行一个 runtime task（RED→GREEN→REFACTOR），发布 `review.ready` — `presets/code-assist.yml (builder)`
6. **Critic hat** 激活：fresh-eyes review，运行 harness，发布 `review.passed` 或 `review.rejected` — `presets/code-assist.yml (critic)`
7. **Finalizer hat** 激活：全局完成度检查，发布 `queue.advance`（还有未完成 step）或 `LOOP_COMPLETE`（全部完成） — `presets/code-assist.yml (finalizer)`
8. 循环回到步骤 4（Planner 推进下一 step wave）或终止

### Phase Transitions

| From | To | Trigger | Gate? | Evidence |
|------|----|---------|-------|----------|
| Idle | Fresh Start | `ralph run` | No | `hatless_ralph.rs:426-443` |
| Fresh Start | Planner | `build.start` event | No | `presets/code-assist.yml` |
| Planner | Builder | `tasks.ready` event | No | event routing |
| Builder | Critic | `review.ready` event | No | event routing |
| Critic | Builder | `review.rejected` event | Yes (review gate) | critic instructions |
| Critic | Finalizer | `review.passed` event | Yes (review passed) | critic instructions |
| Finalizer | Planner | `queue.advance` event | Yes (completion gate) | finalizer instructions |
| Finalizer | Builder | `finalization.failed` event | Yes (rework needed) | finalizer instructions |
| Finalizer | Done | `LOOP_COMPLETE` | Yes (all steps done) | `event_loop` completion_promise |

### Failure Path 1: Review Rejection Loop

Builder 提交代码 → Critic 发现 bug → 发布 `review.rejected` → Builder 重新激活修复同一 task → 再次提交 → Critic 重新 review。循环直到通过或达到 `max_iterations`（默认 100）。

### Failure Path 2: Context Exhaustion

单次迭代 token 使用超过 smart zone (>60% of 176K) → LLM 输出质量下降 → 解析错误增加 → 下一迭代 fresh context 自动恢复（Tenet #1）。若持续失败，`max_runtime_seconds`（4 小时）后强制终止。

### Failure Path 3: Stale Loop Lock

进程崩溃但 `.ralph/loop.lock` 未清理 → 新 `ralph run` 被阻塞 → 需手动 `rm .ralph/loop.lock` 后重启。

### Parallelism

| Parallel Unit | What Runs | Synchronization | Evidence |
|--------------|-----------|-----------------|----------|
| Worktree Loops | 独立 git worktree 中的完整循环 | merge-queue.jsonl (event-sourced) | `CLAUDE.md:122-135` |
| Agent Waves | 同一 hat 的 N 个并行实例 | `aggregate: wait_for_all` + timeout | `AGENTS.md:152-200` |
| Merge Queue | Primary loop 完成后处理 queued loops | Primary loop holds lock | `merge_queue.rs` |

---

## 5. Enforcement Audit

### Enforcement Matrix

| # | Constraint | Source | Level | Evidence | Gap? |
|---|-----------|--------|-------|----------|------|
| 1 | 代码格式化 | `Cargo.toml` | **Hard** | `cargo fmt --check` in pre-commit + CI | No |
| 2 | Clippy 零警告 | `Cargo.toml` | **Hard** | `-D warnings` in pre-commit + CI | No |
| 3 | 禁用 unsafe | `Cargo.toml` | **Hard** | `forbid(unsafe_code)` workspace lint | No |
| 4 | 单元/集成测试 | `.hooks/pre-commit` | **Hard** | `cargo test` exit code 阻止提交 | No |
| 5 | BDD 18 条验收标准 | `hooks-bdd-gate.sh` | **Hard** | 解析 summary，任一 AC 失败 exit 1 | No |
| 6 | Mutation 测试阈值 | `hooks-mutation-gate.sh` | **Hard** | 操作分数 ≥ 55%，critical path 禁止 MISS | No |
| 7 | 嵌入文件同步 | `sync-embedded-files.sh` | **Hard** | `diff -q` 检测漂移，CI job | No |
| 8 | Web 测试 | `.github/workflows/ci.yml` | **Hard** | npm test exit code in CI | No |
| 9 | 提交前运行 cargo test | `CLAUDE.md:18` | **Soft** | 仅文字指令，无独立 gate 阻止不合规提交 | Yes |
| 10 | 禁止提交临时文件 | `CLAUDE.md:51` | **Soft** | `.gitignore` 被动屏障，无 pre-commit lint | Yes |
| 11 | Spec 先于实现 | `CLAUDE.md:99` | **Soft** | 仅 prompt 指令 | Yes |
| 12 | TDD (先写测试) | Builder hat instructions | **Soft** | prompt 指令 "MUST NOT write implementation before tests" | Yes |
| 13 | Hat 单一职责 | presets YAML | **Soft** | prompt 指令 "Do not implement" / "Do not review" | Yes |
| 14 | Fresh context per iteration | Tenet #1 | **Hard** | `hatless_ralph.rs` 每次重建 prompt | No |
| 15 | Claude Code Review | `claude-code-review.yml` | **Soft** | AI 反馈，无 exit code enforcement | Yes |

### Enforcement Statistics

| Level | Count | Percentage |
|-------|-------|------------|
| Hard-enforced | 9 | 60% |
| Soft-enforced | 6 | 40% |
| Unenforced | 0 | 0% |

### Critical Gaps

1. **TDD 纪律 (Soft)**: Builder hat 的 "先写测试再实现" 仅靠 prompt 指令，无硬性 gate 检测实现代码是否在测试之前提交。Critic hat 提供间接 review gate，但非确定性。
2. **Spec-before-implementation (Soft)**: `CLAUDE.md:99` 要求先创建 spec，但无代码阻止直接实现。
3. **Hat 越权 (Soft)**: Planner "MUST NOT start implementing"、Critic "MUST NOT rewrite" 等仅靠 prompt 约束，hat 可能违反角色边界。

---

## 6. Prompt Catalog

### Prompt: HatlessRalph (Orchestrator Core)

| Field | Value |
|-------|-------|
| **repo_path** | `crates/ralph-core/src/hatless_ralph.rs` |
| **quote_excerpt** | "This is your primary goal. All work must advance this objective." / "You MUST handle these events in this iteration" |
| **stage** | 每次迭代（始终活跃） |
| **design_intent** | 构建完整 prompt：objective → skill index → robot guidance → pending events → hat instructions → event writing → completion |
| **hidden_assumption** | 每次迭代 prompt 重建成本可接受；176K token 足够容纳 topology + active hat instructions + context |
| **likely_failure_mode** | topology table + instructions 超过 smart zone 时 LLM 输出质量下降 |
| **evidence_level** | direct |

### Prompt: Planner Hat (code-assist preset)

| Field | Value |
|-------|-------|
| **repo_path** | `presets/code-assist.yml` (planner section) |
| **quote_excerpt** | "You own decomposition and queue progression. Do not implement. Do not review." |
| **stage** | `build.start` / `queue.advance` 触发 |
| **design_intent** | 将请求分解为 step-wave，通过 runtime tasks 驱动 Builder，拥有 plan.md + progress.md |
| **hidden_assumption** | Planner 能准确分解任务且不越权实现；step-wave 粒度适中 |
| **likely_failure_mode** | 过度分解导致 wave 过多；或分解不足导致 Builder 收到过大 task |
| **evidence_level** | direct |

### Prompt: Builder Hat

| Field | Value |
|-------|-------|
| **repo_path** | `presets/code-assist.yml` (builder section) |
| **quote_excerpt** | "You write code following strict TDD: RED → GREEN → REFACTOR. Tests first, always." |
| **stage** | `tasks.ready` / `review.rejected` / `finalization.failed` 触发 |
| **design_intent** | 严格 TDD 实现单个 runtime task，通过 Confidence Protocol 处理歧义 |
| **hidden_assumption** | LLM 能在单次迭代内完成 RED-GREEN-REFACTOR 循环；confidence scoring 有效 |
| **likely_failure_mode** | 跳过 RED 阶段直接写实现（prompt 指令无硬性 gate）；单次迭代 token 不足完成 TDD 循环 |
| **evidence_level** | direct |

### Prompt: Critic Hat

| Field | Value |
|-------|-------|
| **repo_path** | `presets/code-assist.yml` (critic section) |
| **quote_excerpt** | "You are not the builder. That separation matters. Be skeptical, concrete, and adversarial." |
| **stage** | `review.ready` 触发 |
| **design_intent** | fresh-eyes adversarial review，运行真实 harness（Playwright/tmux），不信任 Builder 声称 |
| **hidden_assumption** | Critic 能有效发现 Builder 遗漏；`default_publishes: review.rejected` 偏向拒绝 |
| **likely_failure_mode** | 过度拒绝导致循环卡住；或橡皮图章通过 |
| **evidence_level** | direct |

### Prompt: Finalizer Hat

| Field | Value |
|-------|-------|
| **repo_path** | `presets/code-assist.yml` (finalizer section) |
| **quote_excerpt** | "Your job is to decide whether the whole requested outcome is complete." / "MUST prefer one more iteration over a premature completion signal" |
| **stage** | `review.passed` 触发 |
| **design_intent** | 全局完成度 gate，防止单个 task 通过就宣告 LOOP_COMPLETE |
| **hidden_assumption** | Finalizer 能区分"当前 task 完成"和"整体目标完成" |
| **likely_failure_mode** | 过早发出 LOOP_COMPLETE（未检查所有 steps）；或永远不满足导致达到 max_iterations |
| **evidence_level** | direct |

### Prompt: PDD Skill

| Field | Value |
|-------|-------|
| **repo_path** | `.claude/skills/pdd/SKILL.md` |
| **quote_excerpt** | "This SOP produces planning artifacts. You MUST NOT implement code." |
| **stage** | 规划阶段（`ralph plan` 触发） |
| **design_intent** | 将粗略想法转化为 requirements.md → research/ → design.md → plan.md，严格不实现 |
| **hidden_assumption** | 规划和实现可以完全分离；用户会遵循 spec-first 流程 |
| **likely_failure_mode** | 用户跳过 PDD 直接 `ralph run`；规划产出过于理论化不可执行 |
| **evidence_level** | direct |

---

## 7. Design Highlights — Micro

### Highlight: Hat Topology 的 Token 优化

- **Observation**: `hatless_ralph.rs:344-348` 仅注入 active hats 的完整 instructions，非活跃 hats 仅显示 topology table（name + triggers + publishes）
- **Evidence**: `hatless_ralph.rs:380-391`
- **Why it matters**: 在多 hat preset（12+ hats）中显著减少 token 消耗，保持在 smart zone
- **Trade-off**: 非活跃 hat 看不到自己的 instructions，依赖事件路由正确性
- **Transferability**: Direct — 任何多角色 prompt 系统都可采用

### Highlight: Event-Driven Hat 路由

- **Observation**: Hat 通过 `triggers` 订阅事件 topic，EventBus 自动路由。每个 hat 发布的事件通过 `publishes` 声明
- **Evidence**: `presets/code-assist.yml` (hat definitions), `event_loop/mod.rs`
- **Why it matters**: 解耦 hat 间依赖，新增 hat 只需声明 triggers/publishes，无需修改路由逻辑
- **Trade-off**: 事件链难以静态分析；orphaned events 需要 fallback (HatlessRalph)
- **Transferability**: Inspired — 需要事件总线基础设施

### Highlight: Step-Wave 分解模式

- **Observation**: Planner numbered steps，每个 step 包含一个 task wave。Builder 一次只执行一个 task。当前 step 的 wave 全部完成后才推进到下一 step
- **Evidence**: `presets/code-assist.yml` (planner instructions)
- **Why it matters**: 避免过早创建未来 task（YAGNI），确保增量交付和验证
- **Trade-off**: step 推进慢于并行；Planner 重新激活的 overhead
- **Transferability**: Direct — 适用于任何分步骤执行系统

### Highlight: Confidence-Based Decision Protocol

- **Observation**: Builder/Critic 使用 0-100 置信度评分：>80 自主行动，50-80 行动但记录到 `decisions.md`，<50 选安全默认并记录
- **Evidence**: `presets/code-assist.yml` (builder/critic confidence protocol)
- **Why it matters**: 在不阻塞人类输入的情况下处理歧义，同时保留审计轨迹
- **Trade-off**: 置信度评分本身是主观的；低置信度时的"安全默认"可能不是最优选择
- **Transferability**: Direct — 可移植到任何 agent 决策场景

### Highlight: Replay-Based Smoke Tests

- **Observation**: 使用录制的 JSONL fixture 代替 live API 调用进行测试。`--record-session session.jsonl` 录制，`smoke_runner` 回放
- **Evidence**: `AGENTS.md:207-216`, `crates/ralph-core/tests/fixtures/`
- **Why it matters**: CI 中无需 API key/网络，确定性测试，快速反馈
- **Trade-off**: fixture 可能过时；不捕获 API 行为变化
- **Transferability**: Direct — 适用于任何 LLM 编排系统的测试

### Highlight: `default_publishes` 偏向安全

- **Observation**: Critic 的 `default_publishes: review.rejected`，Finalizer 的 `default_publishes: finalization.failed`
- **Evidence**: `presets/code-assist.yml`
- **Why it matters**: 当 hat 未明确发布事件时，默认走拒绝/失败路径，偏向安全而非过度乐观
- **Trade-off**: 可能导致不必要的循环迭代
- **Transferability**: Direct — 良好的 fail-safe 模式

---

## 8. Design Highlights — Macro

### Philosophy: Fresh Context Is Reliability (Tenet #1)

- **Observation**: 每次迭代清空上下文，从磁盘重读所有状态。不依赖对话历史中的"记忆"
- **Where it appears**: `CLAUDE.md:77`, `hatless_ralph.rs` (prompt 每次重建), `presets/code-assist.yml` (所有 hat 要求 "Re-read")
- **How it shapes the workflow**: 无需复杂重试逻辑（Tenet: "fresh context handles recovery"）；memories.md 和 tasks.jsonl 成为唯一跨迭代状态
- **Strengths**: 自动故障恢复；消除上下文污染；长循环中输出质量稳定
- **Limitations**: 每次迭代的 I/O 开销；依赖磁盘文件的完整性；无法利用对话内的短期记忆
- **Adopt?**: Yes — 核心理念直接可用，对任何多迭代 agent 系统都有价值

### Philosophy: Backpressure Over Prescription (Tenet #2)

- **Observation**: 不告诉 agent "如何做"，而是设置 gates 拒绝坏的产出。tests、lint、typecheck 是硬 gates；LLM-as-judge 用于主观标准
- **Where it appears**: `CLAUDE.md:79`, `scripts/ci-rust-gate.sh` (硬 gates), `presets/code-assist.yml` (Critic hat = 软 gate), `.claude/skills/tui-validate/SKILL.md` (LLM-as-judge)
- **How it shapes the workflow**: 反模式 "detailed step-by-step instructions"；agent 在 guardrails 内自由发挥
- **Strengths**: agent 可以创新；gate 是可测试的客观标准；减少 prompt 复杂度
- **Limitations**: gate 设计质量决定系统质量；主观标准的 LLM-as-judge 可能不一致
- **Adopt?**: Yes — 哲学层面完全可采用；具体 gate 实现需按项目定制

### Philosophy: Disk Is State, Git Is Memory (Tenet #4)

- **Observation**: 所有协调通过文件系统完成（memories.md, tasks.jsonl, loop.lock, merge-queue.jsonl）。无数据库、无 API、无进程间通信
- **Where it appears**: `CLAUDE.md:83`, 所有 `.ralph/` 文件, worktree symlinks
- **How it shapes the workflow**: 并行循环通过 git worktree + symlink 实现；状态可人工检查和修改
- **Strengths**: 极简部署（只需文件系统）；可调试性强；git 提供自然审计轨迹
- **Limitations**: 无分布式一致性；文件锁粒度粗；并发写入风险（JSONL append-only 缓解）
- **Adopt?**: Yes — 对 Claude Code 插件完全适用，已有类似模式

### Philosophy: Evaluator Separation (Critic Hat)

- **Observation**: 实现者 (Builder) 和评审者 (Critic) 是独立 hat，各自在 fresh context 中运行。Critic 被要求不信任 Builder 的声称并独立运行 harness
- **Where it appears**: `presets/code-assist.yml` (critic instructions): "You are not the builder. That separation matters."
- **How it shapes the workflow**: 类似 code review 的两人制；default_publishes = rejected 偏向安全
- **Strengths**: 减少自我确认偏差；fresh eyes 更容易发现 bug
- **Limitations**: 2x iteration overhead；Critic 可能产生 false negative（过度拒绝）
- **Adopt?**: Modify — 原则可用，但需控制 rejection 循环的 max 次数避免卡死

---

## 9. Failure Modes & Limitations

| # | Failure Mode | Trigger | Impact | Evidence |
|---|-------------|---------|--------|----------|
| 1 | **Same-iteration hat switching** | hat 在单次迭代中发布事件后继续工作，而非 STOP | 违反 fresh context；多 hat 在脏上下文中运行 | `evaluate-presets/SKILL.md` (检测: iterations << events) |
| 2 | **Context pressure degradation** | 单次迭代 token >60% of 176K | 输出质量下降，解析错误增加 | `CLAUDE.md:77` (smart zone 40-60%) |
| 3 | **Stale loop lock** | 进程崩溃但 `.ralph/loop.lock` 未清理 | 新循环无法启动 | `ralph-loop/SKILL.md` (recovery principle) |
| 4 | **Review rejection loop** | Critic 持续拒绝 Builder 输出 | 消耗 iteration budget 直到 max_iterations | `presets/code-assist.yml` (default_publishes: rejected) |
| 5 | **Plan attachment** | Builder 重复尝试同一失败方案而非重新规划 | 浪费迭代；Tenet #3 未被 enforce | `CLAUDE.md:81` (Tenet #3, soft only) |
| 6 | **Worktree orphans** | git worktree 未在 loop 完成后清理 | 磁盘空间浪费；merge 混乱 | `ralph-loop/SKILL.md` |
| 7 | **Merge queue deadlock** | queued loop 完成但 primary loop 已死 | merge-queue.jsonl 堆积 | `.ralph/merge-queue.jsonl` |
| 8 | **Hat role violation** | Planner 开始实现代码或 Critic 重写实现 | 破坏职责分离，浪费迭代 | Soft enforcement only (prompt instructions) |
| 9 | **TDD bypass** | Builder 先写实现后补测试 | 违反 RED-GREEN-REFACTOR，测试可能成为 afterthought | Soft enforcement only |

### Observed vs Claimed Behavior Divergences

| Claim | Source | Actual Behavior | Evidence | Evidence Level |
|-------|--------|----------------|----------|---------------|
| "Run `cargo test` before declaring done" | `CLAUDE.md:18` | 无 gate 阻止未测试的提交（pre-commit hook 运行 test，但不阻止 `--no-verify`） | `.hooks/pre-commit` 可被 bypass | direct |
| "Create specs before implementation" | `CLAUDE.md:99` | 纯文字指令，无代码阻止直接 `ralph run` | 无 enforcement 代码 | direct |
| "Tests first, always" (Builder TDD) | `presets/code-assist.yml` | prompt 指令，Critic 间接 review，但无确定性 gate 检测顺序 | Soft enforcement | direct |

---

## 10. Migration Assessment

### Candidates

| # | Mechanism | Rating | Effort | Prerequisite | Risk | Source |
|---|----------|--------|--------|-------------|------|--------|
| 1 | Fresh Context per iteration | Direct | S | 迭代式执行模型 | Low — 增加 I/O 但提高稳定性 | `CLAUDE.md:77` |
| 2 | Backpressure gates (test/lint/typecheck) | Direct | S | pre-commit hooks 基础设施 | Low | `scripts/ci-rust-gate.sh` |
| 3 | Confidence-based decision protocol | Direct | S | agent prompt 模板 | Low — 置信度评分主观但有价值 | `presets/code-assist.yml` |
| 4 | default_publishes 偏向安全 | Direct | S | 事件/状态机模型 | Low | `presets/code-assist.yml` |
| 5 | Replay-based smoke tests | Direct | M | JSONL 录制/回放基础设施 | Medium — 需要维护 fixtures | `AGENTS.md:207-216` |
| 6 | Step-Wave 分解模式 | Inspired | M | task 队列 + 分步执行 | Medium — 需适配到非 EventBus 架构 | `presets/code-assist.yml` |
| 7 | Evaluator Separation (Critic hat) | Inspired | M | 多角色 prompt 或 subagent | Medium — iteration overhead | `presets/code-assist.yml` |
| 8 | LLM-as-judge (tui-validate) | Direct | S | LLM API 调用 | Low — 已有类似模式 | `.claude/skills/tui-validate/SKILL.md` |
| 9 | BDD acceptance criteria (18 ACs) | Inspired | L | BDD 框架 + Gherkin scenarios | High — 需要大量前期投入 | `hooks-bdd-gate.sh` |
| 10 | Mutation testing gate | Inspired | L | `cargo mutants` 或等价物 | High — 运行慢，需要调阈值 | `hooks-mutation-gate.sh` |
| 11 | Hat-based event routing | Non-transferable | L | Rust EventBus 基础设施 | High — 过度耦合原框架 | `event_loop/mod.rs` |
| 12 | Wave 并行执行 | Non-transferable | L | Rust async + pty spawning | High — 需要完整运行时 | `wave_tracker.rs` |

### Recommended Adoption Order

1. **Fresh Context per iteration** — 投入最小，回报最大。任何多迭代 skill 都应在每次迭代开始时重读状态而非依赖对话记忆
2. **Backpressure gates** — 直接利用现有 hooks 基础设施，设置 pre-commit/CI gates
3. **Confidence-based decision protocol** — 添加到 agent/skill prompt 模板，零基础设施成本
4. **default_publishes 偏向安全** — 在 skill 设计中默认走安全路径
5. **LLM-as-judge** — 对 TUI/UI 类验证，利用 vision model 做 semantic validation
6. **Evaluator Separation** — 在 complex 任务中使用独立 review subagent
7. **Step-Wave 分解** — 对大型实现任务，先分解为步骤再逐步执行
8. **Replay-based tests** — 为 skill 创建录制/回放测试 fixture

### Non-Transferable (with reasons)

| Mechanism | Why Not | Alternative |
|----------|---------|-------------|
| Hat-based event routing | 需要 Rust EventBus 运行时，与 Claude Code 插件架构不兼容 | 使用 skill 链式调用 + subagent 模拟角色分离 |
| Wave 并行执行 | 需要 pty spawning + async Rust，过于重量级 | 使用 Claude Code Agent tool 并行调度 |
| Telegram RObot | 需要外部 bot 基础设施 | 利用 Claude Code 原生 AskUserQuestion |
| Web Dashboard | 完整的 React+Fastify+SQLite 栈 | 超出插件范畴 |

### Must-Build Enforcement

| Mechanism | Original Level | Recommended Level | How to Enforce |
|----------|---------------|-------------------|---------------|
| TDD (先写测试) | Soft (prompt) | Hard (hook) | PreToolUse hook 检测：若 Edit 目标是实现文件但同 session 内未先 Edit 对应测试文件 → 警告 |
| Spec-before-implementation | Soft (prompt) | Hard (gate) | 在 skill 入口检查 `.ralph/specs/` 或等价目录是否有对应 spec |
| Hat 角色边界 | Soft (prompt) | Soft (加强) | 在 prompt 中增加具体违规示例；无法硬性 enforce |

---

## 11. Open Questions

1. **Hat 选择算法的确定性**: `event_loop/mod.rs` 中的 hat routing 是否保证每个事件精确匹配一个 hat？多个 hat 订阅同一 topic 时的优先级规则是什么？ — 影响 migration candidate #6 (Step-Wave)
2. **Smart zone 阈值的校准**: 40-60% of 176K 是经验值还是有实验数据支撑？不同 model (Sonnet vs Opus) 的最优 zone 是否不同？ — 影响 migration candidate #1 (Fresh Context)
3. **Critic rejection 循环上限**: `max_iterations: 100` 是全局上限，但 review rejection 循环内无独立上限。是否存在实践中 Critic 永远拒绝的案例？ — 影响 migration candidate #7 (Evaluator Separation)
4. **Mutation testing 的 ROI**: 55% 阈值 + critical path no-MISS 的设定依据是什么？mutation test 运行时长对开发体验的影响？ — 影响 migration candidate #10
5. **Wave 系统的稳定性**: Wave 于 v2.9.0 (2026-04) 引入，是否已有足够生产使用数据验证其可靠性？ — 了解即可，不影响迁移

---

## 附录：Gemini Deepdive 补充信息

> 来源：`1st-cc-plugin/workflows/loaf/docs/gemini-roadmap-review/deepdive-ralph-orchestrator.md`
> 补充内容：Fresh Context 的具体实现细节、Worktree WIP 同步、反模式文档。

### A.1 Scratchpad 清理与 Fresh Context

主报告已描述 fresh context 理念，Deepdive 揭示了具体实现：
- 在非 `!resume` 路径中，`event_loop` 在每次 iteration 开始时**删除 scratchpad 文件**
- `event_loop.build_prompt(&hat_id)` 从零构建 prompt——不复用前次 prompt 内容
- 这确保每次 agent 调用看到的是"当前状态快照"而非"历史累积"

### A.2 Worktree 自动创建与 WIP 同步

`worktree.rs` 的关键机制（主报告未详述）：
- 当 agent 尝试获取 worktree 锁但遭遇 `EWOULDBLOCK` 时，自动创建新 worktree
- **WIP 同步**：使用 `rsync` 将主 worktree 中未提交的文件同步到新 worktree，确保 agent 在最新状态上工作
- `flock()` advisory locking：防止多个 agent 同时修改同一 worktree

### A.3 显式反模式文档

Deepdive 指出 Ralph 的 `AGENTS.md` 中记录了一个显式反模式：**"Scoping work at task selection time"**——即不在 task 被选中时决定 scope，而是在每次 loop iteration 时重新评估。这确保 agent 始终基于最新代码状态（而非过时的 plan）做决策。
