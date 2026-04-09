# Workflow Research: Ouroboros

> **对象**: [Q00/ouroboros](https://github.com/Q00/ouroboros) v0.26.0
> **类型**: Specification-first AI workflow engine（Python >= 3.12）
> **规模**: Large（657 文件，~170 Python 源文件）
> **日期**: 2026-04-08

---

## 0 · Research Scoping

| 维度 | 值 |
|------|-----|
| 文件总数 | 657 |
| Python 源文件 | ~170（`src/ouroboros/`） |
| 技术栈 | Python 3.12+, Pydantic v2, SQLAlchemy async, LiteLLM, Typer, Textual TUI |
| 框架类型 | Specification-first evolutionary workflow engine，支持 Claude Code / Codex CLI 等多 runtime |
| 核心循环 | Interview → Seed → Execute → Evaluate → Evolve（Wonder → Reflect） |

---

## 1 · Source Inventory

### 1.1 Overview

| 文件 | 分类 | 内容 |
|------|------|------|
| `README.md` | Overview | 项目定位、Quick Start、命令列表、哲学阐述 |
| `CLAUDE.md` | Overview | Claude Code 插件路由表（`ooo <cmd>` → SKILL.md）+ 系统提示嵌入 |
| `project-context.md` | Overview | 开发规范：async/sync 规则、命名、import 层级、事件命名、反模式 |
| `docs/architecture.md` | Overview | 6 层 + 6 阶段架构文档 |

### 1.2 Execution

| 路径 | 分类 | 角色 |
|------|------|------|
| `src/ouroboros/bigbang/` | Execution | Phase 0: Interview + Ambiguity Scoring + Seed Generation |
| `src/ouroboros/routing/` | Execution | Phase 1: PAL Router（Frugal/Standard/Frontier 三级） |
| `src/ouroboros/execution/` | Execution | Phase 2: Double Diamond + AC 递归分解 |
| `src/ouroboros/resilience/` | Execution | Phase 3: 4 种停滞模式检测 + 5 种 Persona 横向思维 |
| `src/ouroboros/evaluation/` | Execution | Phase 4: 三阶段评估流水线 |
| `src/ouroboros/secondary/` | Execution | Phase 5: TODO 注册表 + 批量调度 |
| `src/ouroboros/evolution/` | Execution | 演化循环：Wonder → Reflect → 收敛检测 |
| `src/ouroboros/orchestrator/` | Execution | 运行时抽象、并行执行器、会话管理 |

### 1.3 Prompts

| 路径 | 分类 | 角色 |
|------|------|------|
| `src/ouroboros/agents/socratic-interviewer.md` | Prompts | 苏格拉底式访谈者 |
| `src/ouroboros/agents/evaluator.md` | Prompts | 三阶段评估者 |
| `src/ouroboros/agents/seed-architect.md` | Prompts | Seed 规格晶化者 |
| `src/ouroboros/agents/ontologist.md` | Prompts | 本体论分析者 |
| `src/ouroboros/agents/contrarian.md` | Prompts | 假设挑战者 |
| `src/ouroboros/agents/hacker.md` | Prompts | 非常规路径探索者 |
| `src/ouroboros/agents/simplifier.md` | Prompts | 复杂度消减者 |
| `src/ouroboros/agents/researcher.md` | Prompts | 证据调查者 |
| `src/ouroboros/agents/architect.md` | Prompts | 结构性重构者 |
| `skills/interview/SKILL.md` | Prompts | Interview skill 完整指令 |
| `skills/run/SKILL.md` | Prompts | Execution skill 完整指令 |
| `skills/ralph/SKILL.md` | Prompts | 持久化循环 skill 指令 |
| `skills/evaluate/SKILL.md` | Prompts | 评估 skill 指令 |

### 1.4 Enforcement

| 路径 | 分类 | 角色 |
|------|------|------|
| `hooks/hooks.json` | Enforcement | SessionStart / UserPromptSubmit / PostToolUse 钩子 |
| `scripts/drift-monitor.py` | Enforcement | PostToolUse（Write/Edit）后的漂移监控 |
| `scripts/keyword-detector.py` | Enforcement | UserPromptSubmit 关键词检测 |
| `scripts/session-start.py` | Enforcement | SessionStart 初始化脚本 |
| `src/ouroboros/core/security.py` | Enforcement | 输入长度限制（DoS 防护） |

### 1.5 Evolution / Persistence

| 路径 | 分类 | 角色 |
|------|------|------|
| `src/ouroboros/core/lineage.py` | Evolution | Ontology 血统追踪（GenerationRecord, OntologyDelta） |
| `src/ouroboros/evolution/convergence.py` | Evolution | 收敛判定（5 信号 + 多门控） |
| `src/ouroboros/evolution/loop.py` | Evolution | EvolutionaryLoop 主循环 + evolve_step |
| `src/ouroboros/persistence/event_store.py` | Evolution | EventStore（SQLite + WAL + append-only） |
| `src/ouroboros/persistence/schema.py` | Evolution | 数据库 schema |

---

## 2 · Object Model & Context Strategy

### 2.1 Core Entities

```
Seed (frozen Pydantic)
├── goal: str
├── task_type: str  ("code" | "research" | "analysis")
├── constraints: tuple[str, ...]
├── acceptance_criteria: tuple[str, ...]
├── ontology_schema: OntologySchema
│   ├── name, description
│   └── fields: tuple[OntologyField, ...]  (name, type, description, required)
├── evaluation_principles: tuple[EvaluationPrinciple, ...]
├── exit_conditions: tuple[ExitCondition, ...]
├── brownfield_context: BrownfieldContext
│   ├── project_type: "greenfield" | "brownfield"
│   ├── context_references: tuple[ContextReference, ...]
│   └── existing_patterns, existing_dependencies
└── metadata: SeedMetadata
    ├── seed_id, version, created_at
    ├── ambiguity_score: float  (0.0-1.0)
    ├── interview_id, parent_seed_id
```

> **Citation**: `src/ouroboros/core/seed.py:155-273`

```
ACNode (frozen dataclass)
├── id, content, depth, parent_id
├── status: ACStatus  (PENDING → ATOMIC → EXECUTING → COMPLETED | FAILED | DECOMPOSED)
├── is_atomic: bool
├── children_ids: tuple[str, ...]
└── execution_id: str | None

ACTree (mutable container)
├── root_id, nodes: dict[str, ACNode]
├── max_depth: int = 5  (hard limit)
└── methods: add_node, can_decompose, is_cyclic, get_leaves...
```

> **Citation**: `src/ouroboros/core/ac_tree.py:21-401`

```
OntologyLineage (frozen Pydantic, read model)
├── lineage_id, goal
├── generations: tuple[GenerationRecord, ...]
│   └── GenerationRecord
│       ├── generation_number, seed_id, parent_seed_id
│       ├── ontology_snapshot: OntologySchema
│       ├── evaluation_summary: EvaluationSummary | None
│       ├── wonder_questions: tuple[str, ...]
│       ├── phase: GenerationPhase
│       ├── seed_json: str | None  (for cross-session reconstruction)
│       └── seed_quality_canary_feedback
├── rewind_history: tuple[RewindRecord, ...]
├── status: LineageStatus  (ACTIVE | CONVERGED | EXHAUSTED | ABORTED)
└── methods: with_generation, rewind_to, current_ontology
```

> **Citation**: `src/ouroboros/core/lineage.py:372-442`

```
BaseEvent (frozen Pydantic)
├── id: str (UUID)
├── type: str  (dot.notation.past_tense)
├── timestamp: datetime
├── aggregate_type, aggregate_id
└── data: dict[str, Any]
```

> **Citation**: `project-context.md:139-153`

```
WorkflowContext (mutable dataclass)
├── seed_summary, current_ac
├── history: list[dict], key_facts: list[str]
└── created_at, metadata

FilteredContext (frozen dataclass)  ← SubAgent isolation
├── current_ac, relevant_facts
├── parent_summary, recent_history
```

> **Citation**: `src/ouroboros/core/context.py:71-148`

### 2.2 Artifact Classification

| 对象 | 分类 | 说明 |
|------|------|------|
| Seed | **Fact** | 不可变规格，frozen=True 强制 |
| OntologySchema | **Fact** | 结构定义，每代快照 |
| ACNode/ACTree | **Fact** | 分解树，状态机驱动 |
| AmbiguityScore | **Judgment** | LLM 评分（temperature=0.1），含权重理由 |
| EvaluationSummary | **Judgment** | 三阶段评估聚合结果 |
| DriftMetrics | **Judgment** | 加权漂移测量 |
| ConvergenceSignal | **Judgment** | 收敛/停滞判定 |
| BaseEvent | **Evidence** | 事件溯源，append-only |
| GenerationRecord | **Evidence** | 代际快照（含 seed_json 全量） |
| ExecutionHistory | **Evidence** | 停滞检测输入 |

### 2.3 Context Isolation Strategy

Ouroboros 使用 **FilteredContext** 实现 SubAgent 上下文隔离：

- `create_filtered_context()` 从完整 `WorkflowContext` 提取子集
- `FilteredContext` 是 frozen dataclass，阻止 SubAgent 修改主上下文
- 关键字过滤：可按 keyword 选择性传递 `key_facts`
- 历史限制：仅传递最近 3 条 `recent_history`
- 上下文压缩：token 超 100K 或时间超 6h 时触发 LLM 摘要，失败回退到截断

> **Citation**: `src/ouroboros/core/context.py:431-478`（create_filtered_context）, `src/ouroboros/core/context.py:30-32`（阈值常量）

---

## 3 · Flow & State Machine Analysis

### 3.1 主循环状态机

```
                    ┌──────────────────────────────────────────────────────────┐
                    │                    OUROBOROS LOOP                         │
                    │                                                          │
  User Input        │   Phase 0        Phase 1        Phase 2                 │
  ─────────►  [Interview] ──► [PAL Router] ──► [Double Diamond]               │
              Ambiguity≤0.2    Tier Select      Discover→Define→Design→Deliver│
                    │                                                          │
                    │   Phase 3        Phase 4        Phase 5                 │
                    │   [Resilience] ◄── [Evaluation] ──► [Secondary Loop]    │
                    │   Stagnation?     Mech→Sem→Cons    TODO batch           │
                    │       │                │                                  │
                    │       │     ┌──────────┘                                 │
                    │       ▼     ▼                                            │
                    │   [Wonder] ──► [Reflect] ──► [New Seed]                 │
                    │       │                          │                       │
                    │       └──── Convergence? ◄───────┘                      │
                    │              │       │                                    │
                    │         Yes  │       │ No                                │
                    │              ▼       └──► Next Generation                │
                    │            DONE                                          │
                    └──────────────────────────────────────────────────────────┘
```

### 3.2 Generation Lifecycle（Per-Generation 状态机）

```
               Gen 1                              Gen 2+
              ┌────┐                           ┌────────────────────┐
              │    │                           │ WONDERING          │
              │    │                           │ Wonder(Oₙ, Eₙ)    │
              │    │                           └─────────┬──────────┘
              │    │                                     │
              │    │                           ┌─────────▼──────────┐
              │    │                           │ REFLECTING         │
              │    │                           │ Reflect → mutations│
              │    │                           └─────────┬──────────┘
              │    │                                     │
              │    │                           ┌─────────▼──────────┐
              │    │                           │ SEEDING            │
              │    │                           │ Generate new Seed  │
              │    │                           └─────────┬──────────┘
              │    │                                     │
              ▼    ▼                           ┌─────────▼──────────┐
        ┌─────────────────┐                   │ EXECUTING          │
        │ EXECUTING       │◄──────────────────│ Double Diamond     │
        │ Double Diamond  │                   └─────────┬──────────┘
        └────────┬────────┘                             │
                 │                            ┌─────────▼──────────┐
        ┌────────▼────────┐                   │ EVALUATING         │
        │ EVALUATING      │◄──────────────────│ 3-stage pipeline   │
        │ 3-stage eval    │                   └─────────┬──────────┘
        └────────┬────────┘                             │
                 │                                      │
        ┌────────▼────────┐                    ┌────────▼────────┐
        │ COMPLETED       │                    │ COMPLETED/FAILED │
        └─────────────────┘                    └─────────────────┘
```

> **Citation**: `src/ouroboros/evolution/loop.py:954-1473`（`_run_generation_phases`），`src/ouroboros/core/lineage.py:33-44`（GenerationPhase 枚举）

### 3.3 Convergence Criteria（收敛判定逻辑）

5 个信号按优先级检查：

| # | 信号 | 条件 | 类型 |
|---|------|------|------|
| 4 | Hard Cap | completed_generations ≥ 30 | 强制终止 |
| 1 | Ontology Stability | similarity(Oₙ, Oₙ₋₁) ≥ 0.95 | 正常收敛 |
| 2 | Stagnation | similarity ≥ 0.95 连续 3 代 | 停滞收敛 |
| 2.5 | Oscillation | A→B→A→B 周期-2 模式 | 振荡收敛 |
| 3 | Repetitive Feedback | Wonder 问题 ≥ 70% 重叠连续 2 代 | 反馈重复 |

**门控层**（在 Signal 1 通过后仍可阻止收敛）：

- **Eval Gate**: `final_approved=false` 或 `score < 0.7` → 阻止
- **AC Gate**: 模式 "all"（任一 AC 失败阻止）或 "ratio"（通过率低于阈值）
- **Regression Gate**: AC 回归检测 → 阻止
- **Evolution Gate**: 如果 ontology 从未实际变化（evolved_count=0）→ 阻止
- **Validation Gate**: 如果 validation 被跳过或出错 → 阻止

> **Citation**: `src/ouroboros/evolution/convergence.py:38-369`

### 3.4 ACNode Status Transitions

```
PENDING ──► ATOMIC ──► EXECUTING ──► COMPLETED
   │                                    │
   │                                    └──► FAILED
   │
   └──► DECOMPOSED (split into children)
```

> **Citation**: `src/ouroboros/core/ac_tree.py:21-30`

### 3.5 Parallelism vs Sequential Gates

- **Sequential gates**: Phase 0→1→2→3→4→5 严格顺序；评估流水线 Stage 1→2→3 顺序（failure 终止）
- **并行**: AC 树中同层 AC 依赖排序后并行执行（`orchestrator/parallel_executor.py`）；Wonder 失败不阻止循环继续（降级为"无 Wonder"模式）

### 3.6 Failure Paths

| 失败点 | 行为 |
|--------|------|
| Interview 中 LLM 失败 | 自适应 token + 重试（最多 10 次）|
| Ambiguity 评分解析失败 | 截断检测 → double tokens 重试 |
| Reflect 失败 | 重试 2 次，失败则 generation 失败 |
| Execution 超时 | `OUROBOROS_GENERATION_TIMEOUT` 控制，generation 标记 FAILED |
| 评估 Stage 1 失败 | 管道终止，返回失败 |
| Wonder 失败 | 降级（发出 `wonder_degraded` 事件，继续不发问） |
| SIGINT | 优雅中断：保存 partial_state 到事件，下次 resume 跳过已完成阶段 |
| EventStore 锁冲突 | 指数退避重试 3 次 |

---

## 4 · Enforcement Audit

### 4.1 Hard-Enforced（代码阻止违规）

| 行为 | 机制 | 证据 |
|------|------|------|
| Seed 不可变 | `frozen=True` Pydantic model | `src/ouroboros/core/seed.py:155` |
| ACNode 不可变 | `frozen=True` dataclass，`with_*()` 返回新实例 | `src/ouroboros/core/ac_tree.py:32` |
| AC 树最大深度 5 | `ACTree.add_node()` 抛出 `ValueError` | `src/ouroboros/core/ac_tree.py:195-197` |
| 输入长度限制 | `InputValidator` 硬编码常量 | `src/ouroboros/core/security.py:19-22` |
| EventStore 仅接受 BaseEvent | `append()` 类型检查 + 拒绝原始流事件 | `src/ouroboros/persistence/event_store.py:165-183` |
| 事件 append-only | SQLite 表无 UPDATE/DELETE 操作暴露 | `src/ouroboros/persistence/event_store.py` |
| Generation Phase 枚举 | StrEnum 限制合法值 | `src/ouroboros/core/lineage.py:33-44` |
| SubAgent 上下文隔离 | `FilteredContext` frozen dataclass | `src/ouroboros/core/context.py:129-148` |
| 路径遍历防护 | `InputValidator.validate_path_containment()` | `src/ouroboros/core/security.py:313-337` |
| 结果类型安全 | `Result[T, E]` frozen dataclass | `src/ouroboros/core/types.py:15-196` |
| 收敛门控层 | 代码中多层 `if` gate 在 similarity ≥ 0.95 后仍可阻止 | `src/ouroboros/evolution/convergence.py:104-191` |

### 4.2 Soft-Enforced（提示指令但无代码阻止）

| 行为 | 指令位置 | 证据 |
|------|----------|------|
| Ambiguity ≤ 0.2 才生成 Seed | SKILL.md 指令 + LLM 评分 | `skills/interview/SKILL.md`; 评分本身是 LLM 输出 |
| Interviewer 不写代码 | Agent MD 角色边界 | `src/ouroboros/agents/socratic-interviewer.md:6-8` |
| 评估 3 阶段顺序 | Agent MD 指令 | `src/ouroboros/agents/evaluator.md:6-12` |
| 问题路由（PATH 1/2/3/4） | SKILL.md 详细指令 | `skills/interview/SKILL.md:109-170` |
| Dialectic Rhythm Guard（3 连 auto-answer 后强制问用户） | SKILL.md 指令 | `skills/interview/SKILL.md:197-201` |
| 广度控制（不陷入单一子主题） | Agent MD 指令 | `src/ouroboros/agents/socratic-interviewer.md:39-44` |
| Drift ≤ 0.3 可接受 | 代码计算但不阻止执行 | `src/ouroboros/observability/drift.py:57` |

### 4.3 Unenforced（文档提及但代码/提示均缺失）

| 行为 | 文档位置 | 缺失原因 |
|------|----------|----------|
| "Frugal First" 策略 | `docs/architecture.md:500` | PAL Router 实现了升级/降级逻辑，但初始 tier 选择依赖配置而非强制 |
| `drift-monitor.py` 实际漂移计算 | `hooks/hooks.json` PostToolUse | 脚本仅检查 session 文件是否存在，不计算实际漂移值，输出仅为提示消息 |
| "Lateral Over Vertical" 原则 | `docs/architecture.md:504` | 停滞检测后 persona 推荐是建议性的，不强制切换 |

---

## 5 · Prompt Catalog & Design Analysis

### 5A · Prompt Catalog

#### Prompt 1: Socratic Interviewer

| 字段 | 值 |
|------|-----|
| **Role** | 苏格拉底式需求访谈者 |
| **repo_path** | `src/ouroboros/agents/socratic-interviewer.md` |
| **quote_excerpt** | `"You are ONLY an interviewer. You gather information through questions. NEVER say 'I will implement X'"` |
| **stage** | Phase 0 (Big Bang) |
| **design_intent** | 通过问题暴露隐藏假设，将 LLM 限制为纯问题生成器 |
| **hidden_assumption** | 假设 LLM 能严格遵守"只问不做"的角色边界 |
| **likely_failure_mode** | LLM 在长对话后角色漂移，开始承诺实现 |

#### Prompt 2: Interview Skill（4-Path Routing）

| 字段 | 值 |
|------|-----|
| **Role** | 访谈路由器（主会话） |
| **repo_path** | `skills/interview/SKILL.md:109-201` |
| **quote_excerpt** | `"PATH 1 — Code Confirmation... PATH 2 — Human Judgment... PATH 3 — Code + Judgment... PATH 4 — Research Interlude"` |
| **stage** | Phase 0 |
| **design_intent** | 将访谈问题分流为代码事实确认 vs 人类判断，减少用户负担 |
| **hidden_assumption** | LLM 能准确判断"事实"与"判断"的边界 |
| **likely_failure_mode** | PATH 1 auto-answer 错误地代替了需要人类判断的 PATH 2 |

#### Prompt 3: Dialectic Rhythm Guard

| 字段 | 值 |
|------|-----|
| **Role** | 节奏控制器 |
| **repo_path** | `skills/interview/SKILL.md:197-201` |
| **quote_excerpt** | `"If 3 consecutive questions were answered via PATH 1 or PATH 4, the next question MUST be routed to PATH 2"` |
| **stage** | Phase 0 |
| **design_intent** | 防止 auto-answer 链排挤人类参与，保持苏格拉底辩证节奏 |
| **hidden_assumption** | LLM 能正确计数连续 PATH 类型 |
| **likely_failure_mode** | 上下文过长时 LLM 丢失计数状态 |

#### Prompt 4: Evaluator Agent

| 字段 | 值 |
|------|-----|
| **Role** | 三阶段评估者 |
| **repo_path** | `src/ouroboros/agents/evaluator.md` |
| **quote_excerpt** | `"Stage 1: Mechanical ($0)... Stage 2: Semantic (Standard Tier)... Stage 3: Consensus (Frontier Tier - Triggered)"` |
| **stage** | Phase 4 |
| **design_intent** | 渐进式验证：先免费机械检查，再语义评估，最后共识（仅触发时） |
| **hidden_assumption** | 机械检查覆盖了基本质量，语义评估能判断 AC 合规性 |
| **likely_failure_mode** | Stage 1 检测不到的质量问题（如逻辑正确但设计错误）；Stage 2 评分主观性 |

#### Prompt 5: Ralph Persistent Loop

| 字段 | 值 |
|------|-----|
| **Role** | 持久化演化循环 |
| **repo_path** | `skills/ralph/SKILL.md` |
| **quote_excerpt** | `"The boulder never stops. Ralph does not give up: Each failure is data for the next attempt"` |
| **stage** | 跨阶段（Execute → Evaluate → loop） |
| **design_intent** | 跨会话持久化演化，EventStore 重建完整血统 |
| **hidden_assumption** | EventStore 能在会话间完整重建状态 |
| **likely_failure_mode** | seed_json 缺失导致无法 resume（旧版血统无 seed_json） |

### 5B · Micro Design Highlights（具体模式）

#### Pattern 1: Ambiguity Gate 公式

```python
# src/ouroboros/bigbang/ambiguity.py:30-43
AMBIGUITY_THRESHOLD = 0.2
GOAL_CLARITY_WEIGHT = 0.40
CONSTRAINT_CLARITY_WEIGHT = 0.30
SUCCESS_CRITERIA_CLARITY_WEIGHT = 0.30

# Ambiguity = 1 - Sum(clarity_i * weight_i)
# Brownfield 额外维度: Context Clarity (15%), 其他权重相应调整
```

量化模糊度并设定阈值。不是"感觉差不多就行"，而是 LLM 以 temperature=0.1 评分各维度，加权计算后与 0.2 阈值比较。Brownfield 项目增加第四维度"上下文清晰度"。

> **Citation**: `src/ouroboros/bigbang/ambiguity.py:29-43`, `src/ouroboros/bigbang/ambiguity.py:530-546`

#### Pattern 2: Ontology Delta 加权相似度

```python
# src/ouroboros/core/lineage.py:246-302
similarity = 0.5 * name_score + 0.3 * type_score + 0.2 * exact_score
```

收敛判定不是简单的"相同/不同"，而是基于三层匹配的加权分数：名称存在(50%) + 类型一致(30%) + 完全一致(20%)。这允许"字段重命名但本质不变"与"完全相同"之间的灰度。

> **Citation**: `src/ouroboros/core/lineage.py:231-309`

#### Pattern 3: Stateless Stagnation Detection

```python
# src/ouroboros/resilience/stagnation.py:153-196
class StagnationDetector:
    # 所有状态通过 ExecutionHistory 传入，检测器本身无状态
    # 4 种模式独立检测：SPINNING, OSCILLATION, NO_DRIFT, DIMINISHING_RETURNS
    # SHA-256 hash 比较实现 O(1) 检测
```

停滞检测完全无状态——所有历史通过 `ExecutionHistory` 传入。这意味着检测器可以在任何时刻、从任何会话调用，无需维护内部状态。

> **Citation**: `src/ouroboros/resilience/stagnation.py:153-245`

#### Pattern 4: evolve_step() 跨会话无状态设计

```python
# src/ouroboros/evolution/loop.py:467-814
async def evolve_step(self, lineage_id, initial_seed=None, ...):
    # Step 1: Replay events to reconstruct state
    events = await self.event_store.replay_lineage(lineage_id)
    lineage = projector.project(events)
    # Step 2: Run one generation
    # Step 3: Emit events
    # Step 4: Check convergence
```

每次 `evolve_step` 调用都从 EventStore 完整重放事件重建状态。这使得 Ralph 可以在不同会话间执行，机器重启后从中断处恢复。

> **Citation**: `src/ouroboros/evolution/loop.py:467-814`

#### Pattern 5: Graceful Shutdown + Resume

```python
# src/ouroboros/evolution/loop.py:867-952
# SIGINT 处理：第一次设置 _shutdown_requested，第二次 raise KeyboardInterrupt
# 每个 phase 之间检查 _shutdown_requested
# 中断时保存 partial_state（wonder_questions, reflect_output, execution_output...）
# Resume 时根据 interrupted_at_phase 跳过已完成阶段
```

Generation 内每个 phase 之间都有 shutdown 检查点。中断时序列化部分状态到事件，下次 resume 自动跳过已完成的 phase。

> **Citation**: `src/ouroboros/evolution/loop.py:867-952`, `src/ouroboros/evolution/loop.py:974-984`

#### Pattern 6: Consensus Trigger Matrix

6 个触发条件按优先级检查：

1. Seed 修改（Seed 不可变，任何变更需共识）
2. Ontology 演化
3. 目标重新解读
4. Seed drift > 0.3
5. Stage 2 不确定性 > 0.3
6. 横向思维采纳

> **Citation**: `docs/architecture.md:271-278`

### 5C · Macro Design Highlights（哲学）

#### Philosophy 1: 苏格拉底方法 + 本体论分析

Ouroboros 的核心洞见是：AI 编码的瓶颈不是 AI 能力，而是人类输入的模糊性。解决方案不是更好的 AI，而是更好的问题——通过苏格拉底追问暴露隐藏假设，通过本体论分析找到根本问题而非表面症状。

> `README.md:59`: "Most AI coding fails at the **input**, not the output."

#### Philosophy 2: 不可变方向 + 可变路径

Seed 一旦生成不可修改（frozen=True），但实现路径可以自适应。这是"宪法"隐喻——目标和约束是不可协商的，只有达成方式可以演化。

> `docs/architecture.md:502`: "Immutable Direction - The Seed cannot change; only the path to achieve it adapts"

#### Philosophy 3: 事件溯源作为第一等公民

所有状态变更都是不可变事件。这不仅是持久化策略，更是架构决策：任何会话都可以通过回放事件重建完整状态。Ralph 跨会话循环和 TUI 实时可视化都建立在这一基础上。

> `project-context.md:131-153`

#### Philosophy 4: 渐进式成本优化

"Frugal First"贯穿整个系统：PAL Router 从最便宜的 tier 开始、评估从免费的机械检查开始、共识仅在触发时运行。成本意识不是事后优化，而是架构约束。

> `docs/architecture.md:146-185`（PAL Router tier 定义）

### 5D · Cross-Cutting Interconnections

```
Ambiguity Score ──────────► Seed Generation Gate
                                │
Seed (frozen) ─────────────────►│──► Execution (Double Diamond)
                                │         │
                                │         ▼
OntologySchema ◄───── Reflect ◄─── Wonder ◄─── Evaluation
      │                                          │
      │                                          ▼
      └──────► OntologyDelta ──► Convergence ──► Loop Termination
                                     │
                                     ▼
               StagnationDetector ──► Persona Selection
                                          │
                                          ▼
                                    Lateral Thinking Prompt

DriftMeasurement ─────► Consensus Trigger (drift > 0.3)
       │
       └──► drift-monitor.py (PostToolUse hook, advisory only)
```

关键耦合点：
1. **Seed ↔ Evaluation**: Seed 的 AC 和 ontology 直接驱动评估标准
2. **Evaluation ↔ Evolution**: EvaluationSummary 同时传入 Wonder 和 Convergence
3. **Convergence ↔ Evolution**: 收敛信号决定循环终止，但受多层门控
4. **Drift ↔ Consensus**: Drift > 0.3 触发 Stage 3 共识（最昂贵的评估）

---

## 6 · Migration Assessment

### 6.1 High Value / Low Effort

| 机制 | 可迁移性 | 工作量 | 前提 | 风险 |
|------|----------|--------|------|------|
| **Ambiguity Gate 公式** | 高 — 纯算法，可直接移植 | 低 — 已有完整实现 | 需要 LLM 评分接口 | LLM 评分一致性（temperature=0.1 不保证确定性） |
| **Stateless Stagnation Detection** | 高 — 4 种模式 + 纯函数 | 低 — ~200 行独立模块 | 需要 ExecutionHistory 数据结构 | 误报：短序列可能触发假阳性 |
| **Result[T, E] 类型** | 高 — 通用模式 | 极低 — ~100 行 | 无 | 无 |
| **FilteredContext 隔离** | 高 — 简洁模式 | 低 | 需要 SubAgent 架构 | 过度过滤导致 SubAgent 缺少必要上下文 |

### 6.2 Medium Value / Medium Effort

| 机制 | 可迁移性 | 工作量 | 前提 | 风险 |
|------|----------|--------|------|------|
| **Ontology Delta + Convergence** | 中 — 需要 ontology schema 概念 | 中 — ~500 行 | 需要定义"什么在演化" | 对非 ontology 驱动的工作流可能过度设计 |
| **3-Stage Evaluation Pipeline** | 中 — 概念可迁移，实现需适配 | 中 — 需要语言检测 + 机械检查 | 项目需要有可执行的测试/lint | Stage 2/3 的 LLM 评分主观性 |
| **4-Path Interview Routing** | 中 — 需要 MCP 或 Skill 基础设施 | 中 — SKILL.md 逻辑复杂 | 需要 AskUserQuestion 工具 | PATH 1/PATH 2 误分类 |
| **Event Sourcing + evolve_step** | 中 — 架构模式，非组件 | 高 — 完整 EventStore + Projector | SQLite/aiosqlite 依赖 | 事件 schema 演化管理 |

### 6.3 Low Value / High Effort (for plugin context)

| 机制 | 可迁移性 | 工作量 | 前提 | 风险 |
|------|----------|--------|------|------|
| **PAL Router (3-tier cost)** | 低 — 需要多模型支持 | 高 — 复杂度估算 + 升降级 | LiteLLM 或多 provider | 过度工程化 for single-model use |
| **Runtime Abstraction Layer** | 低 — 针对 multi-runtime | 高 — adapter protocol | 支持 ≥2 runtime backend | 不需要 if 仅用 Claude Code |
| **TUI Dashboard** | 低 — 展示层 | 高 — Textual 框架 | 长时运行会话需求 | 对 CLI 插件无必要 |

### 6.4 Failure Modes Summary

| # | 失败模式 | 证据 | 影响 |
|---|----------|------|------|
| 1 | **LLM 角色漂移**: Interviewer 开始承诺实现 | Agent MD 仅通过提示约束（`socratic-interviewer.md:6-8`），无代码阻止 | 用户接收到错误承诺，期望管理失败 |
| 2 | **Auto-answer 误判**: PATH 1 回答了需要人类判断的问题 | Interview routing 完全依赖 LLM 判断（`skills/interview/SKILL.md:109-170`） | 需求遗漏，下游 Seed 不准确 |
| 3 | **Ambiguity 评分不一致**: 相同输入不同次评分结果差异大 | temperature=0.1 降低但不消除随机性（`src/ouroboros/bigbang/ambiguity.py:43`） | Gate 结果不可预测，可能过早或过晚生成 Seed |
| 4 | **seed_json 缺失导致 resume 失败** | 旧版本事件无 seed_json 字段（`src/ouroboros/evolution/loop.py:614-617`） | 跨会话 Ralph 无法恢复 |
| 5 | **drift-monitor.py 名不副实** | 仅检查文件存在，不计算实际漂移（`scripts/drift-monitor.py:18-48`） | 给用户虚假的漂移监控安全感 |
| 6 | **评估 Stage 2 语义评分主观性** | LLM 对 AC 合规性的判断无标准答案 | 同一产出可能在不同次评估中通过/失败 |
| 7 | **Evolution Gate 死锁可能性** | 若 Wonder/Reflect 持续失败导致 ontology 从未变化，evolution_gate 永远阻止收敛 | 循环消耗到 max_generations 才停止（`convergence.py:160-171`） |

---

## 7 · Pre-Submit Checklist

| 项目 | 状态 | 位置 |
|------|------|------|
| A. Source Inventory 分类 | ✓ | Section 1（5 类：Overview / Execution / Prompts / Enforcement / Evolution） |
| B. Prompt Traceability | ✓ | Section 5A（5 prompts, 含 repo_path + quote_excerpt） |
| C. Object Model ≥ 3 entities | ✓ | Section 2.1（Seed, ACNode/ACTree, OntologyLineage, BaseEvent, WorkflowContext, FilteredContext） |
| D. State Machine with transitions | ✓ | Section 3.1-3.4（主循环、Generation Lifecycle、ACNode Status、Convergence） |
| E. Enforcement Audit | ✓ | Section 4（11 Hard / 7 Soft / 3 Unenforced） |
| F. Micro + Macro highlights | ✓ | Section 5B（6 patterns）+ 5C（4 philosophies） |
| G. ≥ 3 failure modes | ✓ | Section 6.4（7 failure modes with evidence） |
| H. Migration candidates | ✓ | Section 6.1-6.3（12 mechanisms with ratings） |
