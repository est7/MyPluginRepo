# Workflow Research Report — PAUL (Plan-Apply-Unify Loop)

**研究目标：** 对 `vendor/paul` 进行结构化逆向工程分析，提取其对象模型、状态机、强制机制、设计模式与可迁移工程价值。
**研究日期：** 2026-04-08
**仓库位置：** `/Users/est8/MyPluginRepo/vendor/paul`
**版本：** `paul-framework@1.2.0`（`vendor/paul/package.json:3`）

---

## Phase 0 — Research Scoping

### 规模与分类

- **文件总数：** 103（含 `.git`），核心源文件约 94（`vendor/paul` 顶层 `find` 输出）
- **规模分类：** Medium（50-200 files）
- **顶层结构：**
  ```
  vendor/paul/
  ├── bin/install.js           # npm 安装器（Node ≥16.7）
  ├── src/
  │   ├── carl/                # CARL 动态规则注入集成
  │   ├── commands/            # 28 个用户可见 slash command 薄壳
  │   ├── workflows/           # 23 个厚实工作流（命令委派目标）
  │   ├── templates/           # 18 个文档模板（PLAN/STATE/PROJECT/SUMMARY…）
  │   ├── references/          # 12 个概念文档（懒加载）
  │   └── rules/               # 5 个编辑层元规则（路径作用域）
  ├── README.md
  ├── PAUL-VS-GSD.md           # 与 GSD 框架的对比定位
  └── package.json
  ```

### 框架类型识别

PAUL 是一个 **AI-assisted 开发流程框架**，以 npm 包形式发布（`vendor/paul/package.json:5`：`"bin": {"paul-framework": "bin/install.js"}`），通过 `npx paul-framework` 安装进 `~/.claude/commands/paul/` 或 `./.claude/`。它并不是插件（plugin）也非 MCP server，而是一套"commands + workflows + templates + references + rules"的文件协议，配合 Claude Code 原生 slash command 机制与可选的 **CARL**（Context Augmentation & Reinforcement Layer，`vendor/paul/src/carl/PAUL`）规则注入。

其核心主张（见 `vendor/paul/README.md:41-49`）是三条：
1. **Loop integrity** — 每个 PLAN 必须以 UNIFY 闭环
2. **In-session context** — 实现工作保留在主会话中，subagent 只用于 discovery/research
3. **Acceptance-driven development** — AC 是一等公民，BDD 格式 Given/When/Then

---

## Phase 1 — Reconnaissance & Source Inventory

### 入口点与注册机制

- **npm 入口：** `vendor/paul/bin/install.js:122-168`，`install(isGlobal)` 将 `src/commands/` 拷贝到 `{claudeDir}/commands/paul/`，`src/{templates,workflows,references,rules}` 拷贝到 `{claudeDir}/paul-framework/`；安装过程中会对所有 `.md` 做 `~/.claude/` → 目标路径前缀的字符串替换（`install.js:108-117`），解决 global/local 路径差异。
- **命令注册：** 依赖 Claude Code 原生约定——`commands/paul/{name}.md` 自动注册为 `/paul:{name}` slash command（frontmatter 示例见 `vendor/paul/src/commands/plan.md:1-6`）。无自定义 registry。
- **CARL 集成：** `vendor/paul/src/carl/PAUL` 与 `PAUL.manifest` 定义 14 条环境变量式规则（`PAUL_RULE_1` 至 `PAUL_RULE_12`，`vendor/paul/src/carl/PAUL:9-25`），通过 `.paul/` 目录存在与否触发域激活（`PAUL_STATE=active`、`PAUL_ALWAYS_ON=false`）。CARL 是 **可选** 增强，PAUL 文件协议本身不依赖它。

### Source Inventory（分类）

| 类别 | 文件示例 | 用途 |
|------|---------|------|
| **Overview** | `README.md`, `PAUL-VS-GSD.md` | 对外宣传与定位，未被 workflow 加载 |
| **Execution — Commands**（薄壳）| `src/commands/{init,plan,apply,unify,progress,resume,pause,audit,verify,research,...}.md` | 28 个 slash command，frontmatter + `<objective>` + `<execution_context>` @引用 + `Follow workflow:` 委派 |
| **Execution — Workflows**（厚实）| `src/workflows/{init-project,plan-phase,apply-phase,unify-phase,transition-phase,quality-gate,verify-work,audit-plan,discovery,research,resume-project,pause-work,...}.md` | 23 个工作流文件，包含 `<purpose>/<when_to_use>/<loop_context>/<required_reading>/<process>/<step>/<error_handling>/<anti_patterns>` 语义 XML |
| **Prompts — Templates** | `src/templates/{PROJECT,STATE,ROADMAP,PLAN,SUMMARY,HANDOFF,CONTEXT,DEBUG,DISCOVERY,RESEARCH,ISSUES,UAT-ISSUES,MILESTONES,SPECIAL-FLOWS,paul-json,config,milestone-archive,milestone-context}.md`、`src/templates/codebase/{stack,architecture,structure,conventions,integrations,testing,concerns}.md` | 18+ 个生成文档的结构模板，含字段说明、anti-patterns |
| **Prompts — References** | `src/references/{loop-phases,checkpoints,work-units,subagent-criteria,context-management,quality-principles,plan-format,git-strategy,tdd,research-quality-control,sonarqube-integration,specialized-workflow-integration}.md` | 12 个懒加载概念文档，workflow 按需 `@` 引用 |
| **Enforcement — Rules**（元规则）| `src/rules/{workflows,commands,templates,references,style}.md` | 对 `src/*/**.md` 的编辑规则，有 `paths:` frontmatter 声明作用域；约束 PAUL 自身文件的结构、命名、语气 |
| **Enforcement — CARL** | `src/carl/PAUL`, `src/carl/PAUL.manifest` | 14 条 MUST/SHOULD/MAY 规则，由外部 CARL 动态注入 |
| **Evolution** | `src/templates/milestone-archive.md`, `pause-work.md`, `resume-project.md`, `transition-phase.md`, `complete-milestone.md` | 长周期演化：HANDOFF 生命周期、PROJECT.md 进化、phase/milestone 转换 |

---

## Phase 2 — Object Model & Context Strategy

### 核心实体

| 实体 | 位置 | 性质 | 生命周期 |
|------|------|------|---------|
| **PROJECT.md** | `.paul/PROJECT.md` | judgment（需求+约束+决策） | init 创建 → transition-phase 持续"进化"（`vendor/paul/src/workflows/transition-phase.md:62-95`：shipped requirements 从 Active 移至 Validated） |
| **ROADMAP.md** | `.paul/ROADMAP.md` | judgment（阶段分解） | init 骨架 → plan 过程填充 → transition 标记完成 |
| **STATE.md** | `.paul/STATE.md` | fact+judgment（当前位置+累积上下文） | 每步必写；每个 workflow 的第一步与最后一步都读写（`<required_reading>` 含 `@.paul/STATE.md`），目标 <100 行（`vendor/paul/src/templates/STATE.md:181-191`） |
| **PLAN.md** | `.paul/phases/{NN}-{name}/{NN}-{NN}-PLAN.md` | judgment（可执行 prompt） | plan-phase 创建 → apply-phase 消费 → unify-phase 归档，**plan 即 prompt**（`vendor/paul/src/references/quality-principles.md:13-24`：`<plans_are_prompts>`） |
| **SUMMARY.md** | `.paul/phases/{NN}-{name}/{NN}-{NN}-SUMMARY.md` | evidence（已构建内容+AC 结果+偏差） | unify-phase 唯一产出，关闭循环的证据 |
| **HANDOFF-{date}.md** | `.paul/HANDOFF-*.md` → `.paul/handoffs/archive/` | evidence（会话交接） | pause-work 创建 → resume-project 消费后归档/删除（`vendor/paul/src/workflows/resume-project.md:145-168`） |
| **AUDIT.md** | `.paul/phases/.../{NN}-{NN}-AUDIT.md` | judgment+evidence | audit-plan 工作流产出（可选，由 `enterprise_plan_audit: enabled: true` 触发） |
| **paul.json** | `.paul/paul.json` | fact（机器可读卫星清单） | init 创建，workflow 同步（`vendor/paul/src/templates/paul-json.md:61-73`）；供外部系统（BASE）发现项目 |
| **SPECIAL-FLOWS.md** | `.paul/SPECIAL-FLOWS.md` | judgment（技能需求声明） | 可选；apply-phase 阻塞执行直到声明的 skill 被加载（`vendor/paul/src/workflows/apply-phase.md:50-87`） |
| **UAT-{plan}.md** | `.paul/phases/.../{NN}-{NN}-UAT.md` | evidence（手工验收问题） | verify-work 创建（`vendor/paul/src/workflows/verify-work.md:130-151`） |
| **DISCOVERY.md / RESEARCH.md** | `.paul/phases/.../DISCOVERY.md`, `.paul/research/{slug}.md` | evidence（前期调研） | discovery/research workflow 产出 |

### 实体关系

```
PROJECT.md ──────────┐
   (constraints)     │
                     ▼
ROADMAP.md ──► PLAN.md ──► APPLY ──► SUMMARY.md
   (phases)     │              ▲           │
                │              │           ▼
                └── STATE.md ◄─┴───── STATE.md (updated)
                       ▲                    │
                       │                    ▼
                  HANDOFF.md ◄── pause   PROJECT.md (evolved)
                       │                    ▲
                       └────► resume ───────┘
```

### 事实/判断/证据分类

- **事实对象（immutable facts）：** `paul.json` 的 timestamps、SUMMARY.md 的 "Files Created/Modified" 表、git commit hash
- **判断对象（mutable judgments）：** PROJECT.md 的 Requirements 表、ROADMAP.md 的 phase 状态、PLAN.md 的 acceptance criteria
- **证据对象（proofs）：** SUMMARY.md 的 AC 结果表、AUDIT.md 的 findings、UAT.md 的 issue 列表、verify 命令输出

这三类的严格分离使 UNIFY 阶段能够进行"plan vs actual"对比（`vendor/paul/src/workflows/unify-phase.md:46-57`）。

### 上下文隔离策略

PAUL **反 subagent**（参见 `vendor/paul/README.md:407-423`、`PAUL-VS-GSD.md:32-50`），对比 GSD 的并行 subagent 执行策略：

| 策略 | 实现 |
|------|------|
| **In-session 优先** | subagent 仅在 research/discovery 时使用，执行一律主会话内（`vendor/paul/src/references/subagent-criteria.md:91-101`） |
| **上下文预算 50%** | `work-units.md:24-33` 明确目标是 plan 执行控制在 50% 以内，而非 80%，避免"completion mode 退化" |
| **渐进式加载** | `context-management.md:81-89` 的 "Progressive Detail"：先 STATE.md → 再 SUMMARY.md → 最后源文件 |
| **避免反射性链接** | `context-management.md:108-134`：`depends_on` 必须是真实依赖，禁止"Plan 02 依赖 01 just because" |
| **懒加载 @-references** | `vendor/paul/src/rules/style.md:72-87`：`@` 引用是懒加载信号，不是预加载内容 |
| **SUMMARY 替代 PLAN** | 完成后优先引用 SUMMARY（结果）而非 PLAN（意图）（`context-management.md:66-79`） |
| **上下文括号（bracket）** | FRESH/MODERATE/DEEP/CRITICAL 四档（`context-management.md:6-17`），驱动不同加载策略 |

---

## Phase 3 — Flow & State Machine Analysis

### 主循环状态机

```
            ┌──────────────────────────┐
            │                          │
            ▼                          │
   ┌─────────────┐                     │
   │  init-      │   （一次性）          │
   │  project    │                     │
   └──────┬──────┘                     │
          │                            │
          ▼                            │
   ┌─────────────┐                     │
   │    PLAN     │◄────────┐           │
   │ (plan-phase)│         │           │
   └──────┬──────┘         │           │
          │ user approval  │           │
          ▼                │           │
   ┌─────────────┐    ┌────┴─────┐     │
   │   [AUDIT]   │───▶│  APPLY   │     │
   │  optional   │    │ (apply-  │     │
   │ audit-plan  │    │  phase)  │     │
   └─────────────┘    └────┬─────┘     │
                           │           │
                           ▼           │
                    ┌──────────────┐   │
                    │    UNIFY     │   │
                    │(unify-phase) │   │
                    └──────┬───────┘   │
                           │           │
                ┌──────────┼──────────┐│
                ▼          ▼          ▼│
           [more plans  [last plan  [last plan
            in phase]    in phase]   in milestone]
                │           │           │
                │           ▼           ▼
                │    ┌──────────────┐  ┌──────────────┐
                │    │  transition- │  │  complete-   │
                │    │    phase     │  │  milestone   │
                │    └──────┬───────┘  └──────┬───────┘
                │           │                 │
                └───────────┴─────────────────┘
                    (route back to PLAN)
```

### 状态机门控（gates）

定义于 `vendor/paul/src/references/loop-phases.md:188-213`：

| 转换 | 触发条件 | 验证门 |
|------|---------|--------|
| PLAN → APPLY | 用户显式批准（"approved"/"execute"/"go ahead"） | 4 项：所有 sections 存在、AC 可测试、task 有 Files+Action+Verify+Done、boundaries 清晰（`loop-phases.md:193-198`） |
| APPLY → UNIFY | 所有 task 完成或记录 blocker | 3 项：每个 verify 通过或 blocker 记录、无跳过、偏差已记录（`loop-phases.md:200-204`） |
| UNIFY → PLAN | SUMMARY.md 创建、STATE.md 更新 | 3 项：SUMMARY 含 AC 结果、STATE 反映新位置、ROADMAP 在阶段完成时更新（`loop-phases.md:206-213`） |
| 阶段完成 → transition | unify-phase.md 检测 "last plan in phase" | 强制（`vendor/paul/src/workflows/unify-phase.md:228-252`：`gate="blocking"`，⚠️ NEVER skip）|
| transition 完成 | 状态一致性验证通过 | 硬门（`transition-phase.md:236-290`：三文件字段对齐检查） |

### Happy Path

`init → plan → [audit] → apply → unify → (transition) → plan → ...`

每个 phase 结束（最后一个 plan）附带：PROJECT.md 进化、ROADMAP.md 更新、git commit、feature branch 合并（若存在）、stale handoff 清理、**STATE 一致性硬验证**。

### 失败路径

1. **Pre-APPLY：** required skill 未加载 → BLOCK（`apply-phase.md:50-87`），用户必须输入 `ready` 或 `override`（后者记录 deviation）
2. **Task 执行：** 4 种状态 DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED（`apply-phase.md:102-116`），非 DONE 都触发特殊路径
3. **Qualify failure：** GAP/DRIFT 触发 fix-and-requalify 循环，最多 3 次后升级给用户（`apply-phase.md:136-158`）
4. **Checkpoint failure：** 诊断分类 intent/spec/code 后路由到 `/paul:plan`、`/paul:plan-fix`、或原地修复（`apply-phase.md:215-250`）
5. **UAT failure：** verify-work 同样执行诊断分类（`verify-work.md:197-228`）
6. **State consistency fail：** transition 阶段硬门阻断（`transition-phase.md:263-279`）
7. **Audit "not acceptable"：** audit-plan 拒绝路由到 APPLY（`audit-plan.md:291-301`）

### 并行性

PAUL **默认串行**。并行仅体现在：
- PLAN.md frontmatter 的 `wave: N` 与 `depends_on: []`（`vendor/paul/src/templates/PLAN.md:190-193`），`depends_on: []` 且 `autonomous: true` 的 plans 理论上可并行，但 apply-phase 工作流并未实现真正的并行执行器
- research workflow 中的 "multiple topics (parallel)" — 单次 message 中 spawn 多个 Task agent（`vendor/paul/src/workflows/research.md:147-151`）

其余所有 workflow 都是串行顺序门控。

---

## Phase 4 — Enforcement Audit

| 宣称行为 | 类别 | 证据 |
|---------|------|------|
| "NEVER execute without approval" | **Soft** | `apply-phase.md:30-37` 文字要求 "Do NOT assume approval"，但无 hook/script 阻止；仅靠 LLM 自律 |
| "Every PLAN closes with UNIFY" | **Soft (loop-phases) + Hard-ish (unify detects + transition gates)** | `unify-phase.md:228-252` `gate="blocking"`、`priority="required"`，并显式 `"⚠️ NEVER skip this step"`；但执行器仍是 LLM，真正的"硬"来自 CARL `PAUL_RULE_3`（`src/carl/PAUL:12`）在外部规则引擎注入约束 |
| "Respect PLAN.md boundaries (DO NOT CHANGE)" | **Soft** | `apply-phase.md:98-101` 反合理化话术 + `error_handling:353-356` 要求立即停止；CARL `PAUL_RULE_4` 再次提醒；但文件系统层面无 read-only 保护 |
| "BLOCKING: required skills must be loaded before APPLY" | **Soft（但结构化）** | `apply-phase.md:50-87` 的 `verify_required_skills` step 有 `priority="blocking"` 属性，工作流检查 `session` 内 skill 是否被 invoke；依然是 LLM 自报告 |
| "Every task has Files + Action + Verify + Done" | **Soft** | `PLAN.md:210-218` 声明 "If you can't specify all four, the task is too vague"，无 schema validator |
| "STATE consistency verified at transition" | **Soft-Strong** | `transition-phase.md:236-290` 规定了字段对齐表、要求 "Fix ALL misalignments before proceeding"，有 "BLOCKING" 语言但仍由 LLM 比对 |
| "Execute/Qualify loop" 质量护栏 | **Soft（反合理化模式）** | `apply-phase.md:162-189` 的 "Before claiming any task is complete, check yourself" 表格（6 行反合理化 prompt）；设计非常工程化但执行依然靠 LLM 自觉 |
| "Commands are thin wrappers, workflows contain logic" | **Hard（元规则）** | `src/rules/commands.md:30-36` 与 `src/rules/workflows.md:80-85` 通过 `paths:` frontmatter 作用于 `src/commands/**` 和 `src/workflows/**`，结合 Claude Code 的 rules-by-path 机制做编辑期约束 |
| "No frontmatter in workflows/references" | **Hard（元规则）** | `src/rules/workflows.md:11-13`、`src/rules/references.md:11-13` |
| "Imperative voice, no filler/sycophancy, temporal ban" | **Soft** | `src/rules/style.md:12-27`，纯语气约束 |
| "Handoffs archived after resume" | **Soft** | `resume-project.md:145-168` 明确 `mkdir -p .paul/handoffs/archive && mv`，bash 脚本化程度高但仍在 LLM prompt 里 |
| "Claude automates everything CLI/API can do" | **Soft** | `quality-principles.md:101-114` `<claude_automates>`，是原则陈述 |
| "Audit must-have findings auto-applied to PLAN" | **Soft** | `audit-plan.md:158-183` 要求修改 PLAN.md，由 LLM 执行 Edit 操作 |
| "≤ 3 tasks per plan, ~50% context" | **Unenforced** | `work-units.md`、`quality-principles.md:86-99` 有建议但无计数检查 |
| "Plan validator runs before approval" | **Unenforced** | `plan-phase.md:220-232` 的 `validate_plan` 步是 LLM 自检，无外部脚本 |

**结论：** PAUL 的强制力几乎全部来自 prompt-level self-discipline + 反合理化话术 + 结构化步骤命名。唯一接近"硬"强制的是：
1. **元规则（rules layer）**——利用 Claude Code 路径作用域编辑规则
2. **CARL 规则注入**（外部可选）
3. **状态机门控**（`gate="blocking"` + `priority="required"` + 显式 "NEVER skip" 话术）

没有 pre-commit hook、没有 schema validator、没有 JSON Schema、没有脚本化 lint。这是一个 **prompt engineering framework**，不是代码驱动的 harness。

---

## Phase 5 — Prompt Catalog & Design Analysis

### 5A. 关键 Prompt 目录

| # | role | repo_path | quote_excerpt | stage | design_intent | hidden_assumption | likely_failure_mode |
|---|------|-----------|--------------|-------|--------------|-----------------|-------------------|
| 1 | Loop discipline enforcer | `src/references/quality-principles.md:26-40` | "Every PLAN must complete the full loop: PLAN ▶ APPLY ▶ UNIFY. Never leave a loop incomplete. UNIFY closes the loop and updates state." | Foundational principle | 通过原则命名（loop_first）让 LLM 内化三段式闭环 | Claude 会在同一个 session 保持注意力、不会因上下文压缩遗忘 loop 位置 | 长会话或 subagent spawn 后，LLM 忘记当前 loop 位置，误入下一个 PLAN |
| 2 | Anti-rationalization table | `src/workflows/apply-phase.md:162-171` | "If you're thinking 'Should work now' STOP. Instead... Run the verify command and read its output. Because... Confidence is not evidence — you must see proof before claiming success" | Qualify step in APPLY | 对抗 LLM 的乐观倾向，通过命名常见自我欺骗话术强迫二次验证 | LLM 会识别自己的 "should work" 等话术并自我纠正 | 微妙的自我欺骗（比如 "it looks right"）不在表格内，被漏过 |
| 3 | Execute/Qualify loop | `src/workflows/apply-phase.md:89-189` | "Trust the output, not your memory of producing it. Re-read actual output — instead of trusting what you remember writing, because execution memory is optimistic" | APPLY task loop | 将"执行"和"验证"解耦，强制 fresh 读取 | verify 命令本身是正确且足够的；re-read 的文件准确反映实际写入 | verify 命令本身有缺陷（passing on wrong cases）、或者 LLM 只走流程不深度比对 |
| 4 | Diagnostic failure routing | `src/workflows/apply-phase.md:215-250`、`src/references/checkpoints.md:135-156` | "Before fixing, let's classify the root cause: [1] Intent issue — I need to build something different [2] Spec issue — The plan was missing something [3] Code issue — The plan was right" | Checkpoint failure / UAT failure | 防止"无脑打补丁"，把失败向上游归因 | 用户能准确做出 intent/spec/code 分类 | 用户选错分类，或 LLM 诱导式措辞让用户选 code（最快路径） |
| 5 | Boundaries enforcement | `src/templates/PLAN.md:317-328`、`apply-phase.md:98-101` | "If a task would modify a protected file, STOP — instead of rationalizing 'it's a small change', because boundary violations cascade into untraceable changes" | Any APPLY task | 防止 scope creep，让 DO NOT CHANGE 成为硬约束 | LLM 会在写文件前检查 boundaries 清单 | 间接修改（如修改 import 导致依赖文件行为变化）不触发显式 boundary 检查 |
| 6 | Single next action | `src/workflows/resume-project.md:96-108`、`src/commands/progress.md:70-90` | "Do NOT offer multiple options. Pick the ONE correct action." | Resume / progress | 减少决策疲劳，强制 framework 做出判断 | 单一建议总是"正确"或接近正确 | 当 state 模糊时，单一建议可能是错的，而用户已习惯接受 |
| 7 | Context quality curve | `src/references/work-units.md:10-22` | "0-30% PEAK / 30-50% GOOD / 50-70% DEGRADING / 70%+ POOR. The 40-50% inflection point: Claude sees context mounting and thinks 'I'd better conserve now.' Result: quality crash." | Plan sizing | 基于观察的 LLM 行为特征，强制 aggressive atomicity | Claude 的质量退化行为可量化并由 50% 阈值描述 | 实际退化模式因任务类型/model 版本差异，固定 50% 阈值不普适 |
| 8 | Subagent strategic gate | `src/references/subagent-criteria.md:9-89`、`169-177` | "Subagents are APPROPRIATE when ALL of the following are true: Task Independence, Clear Scope, Parallel Value, Complexity Sweet Spot, Token Efficiency, State Compatibility" + "When criteria are borderline, prefer working in the main session" | Pre-spawn | 反 GSD 的 subagent 默认倾向，要求 6 项全满足 | 6 项检查可以客观判断 | LLM 会为了"保持简单"把几乎所有工作都留在主会话，过度保守 |
| 9 | Acceptance-driven verify | `src/references/quality-principles.md:59-83` (`<evidence_before_claims>`) | "Execute → Verify (run command) → Read output → Compare to spec → THEN claim. Breaking any link in the chain produces false completion" | Universal | 建立证据链，断链即退化为 hope | 四环每一环都会被 LLM 老实执行 | LLM 可能省略"Compare to spec" 只做 "test passed" |
| 10 | Enterprise audit role-play | `src/workflows/audit-plan.md:62-138` | "You are acting as a senior principal engineer + compliance reviewer... Perform a hard, honest audit. Do not validate or encourage. Assume this system will be... Used in a regulated environment / Reviewed by auditors (SOC 2 / ISO / legal)" | Optional audit between PLAN and APPLY | 通过角色扮演+高压语境（合规/法律审计）提升批判性输出质量 | LLM 能脱离讨好倾向并做出严格挑错 | LLM 仍有阿谀倾向；或反过来过度挑剔造成虚假 findings |
| 11 | One-liner SUMMARY requirement | `src/templates/SUMMARY.md:187-198` | "Good: 'JWT auth with refresh rotation using jose library' / Bad: 'Phase complete'" | UNIFY output | 强制具体化，防止"已完成"式无信息摘要 | 作者会参考这些 good/bad 范例 | 被省略或被弱化为模板填空 |
| 12 | State consistency field table | `src/workflows/transition-phase.md:248-258` | "Verify alignment across these fields: Version/Phase/Status/Focus across STATE.md / PROJECT.md / ROADMAP.md" | Phase transition | 硬性三文件字段对齐表 | LLM 能准确读取并比对 4×3 矩阵 | 字段名不一致时 LLM 容易"差不多就行" |
| 13 | Quick continuation prompts | `plan-phase.md:329-363`、`apply-phase.md:325-338`、`unify-phase.md:203-225` | "[1] Approved, run APPLY \| [2] Questions first \| [3] Pause here. Accept quick inputs: '1', 'approved', 'yes', 'go'" | All loop transitions | 低摩擦推进，但明确打断点 | 用户偏好极短输入 | 用户误按 "1" 时跳过审阅 |
| 14 | No temporal language ban | `src/rules/style.md:22-27` | "Never write: 'We changed X to Y', 'Previously', 'No longer', 'Instead of'. Always: Describe current state only." | Editing PAUL files | 防止文档历史化、积累临时性叙事 | 作者能记住例外（SUMMARY deviations、git commits） | 重构任务需要解释"从前"时难以遵守 |

### 5B. 微观设计亮点（Concrete Patterns）

1. **Rules-by-path 元层** — `src/rules/*.md` 的 frontmatter `paths: - "src/workflows/**/*.md"`（`vendor/paul/src/rules/workflows.md:1-4`）利用 Claude Code 原生的路径作用域规则机制，把"编辑 workflow 时必须遵守的格式"作为硬编辑期约束，而非运行期 prompt。这是 PAUL 唯一真正"Hard"的强制层。

2. **反合理化 prompt 表格** — `apply-phase.md:164-171` 的 6 行表格直接命名 Claude 的常见自欺话术（"Should work now"、"It's close enough"、"The test passes"、"I'm confident it works"），并给出"STOP. Instead..."反应方案。这是针对 LLM 具体失败模式的工程化 prompt 补丁，远优于抽象的"要仔细"。

3. **Execute/Qualify 三阶段独立化** — `apply-phase.md:89-189` 将单个 task 拆为 EXECUTE → REPORT STATUS → QUALIFY，每阶段独立产物。REPORT STATUS 的 4 档（DONE/DONE_WITH_CONCERNS/NEEDS_CONTEXT/BLOCKED）通过命名让"带保留意见的完成"成为一等公民，对抗 pass/fail 二元退化。

4. **Diagnostic failure routing 三分类** — `apply-phase.md:215-250` 在 checkpoint 失败时强制分类 intent/spec/code，每类映射到不同的修复 workflow（re-plan / plan-fix spec / plan-fix code）。这防止了"code patch first"的默认惰性。

5. **@-reference 作为懒加载信号** — `src/rules/style.md:72-87` 明确 `@` 只是"读取时加载"的信号，不是预加载内容。配合 references/ 目录的自包含设计（`src/rules/references.md:96-98`：references 应独立可读），形成按需加载图。

6. **Phase 两种 track：quick-fix vs standard/complex** — `plan-phase.md:51-96` 的 `classify_scope` 步在 plan 前自动路由 ceremony 等级，quick-fix 压缩为单 AC+单 task 无 boundaries，避免"一行修复也要写 boundary 章节"。

7. **paul.json 卫星清单** — `src/templates/paul-json.md` 作为机器可读的项目发现文件，与人类可读的 STATE.md 并存。明确声明 "never hand-edited"、"Machine-readable only"，职责分离。

8. **Handoff 生命周期** — `pause-work.md` 创建 `HANDOFF-{date}.md`，`resume-project.md:145-168` 在 resume 后执行 `mkdir -p .paul/handoffs/archive && mv`。避免 handoff 文件无限堆积。

9. **Enterprise audit 角色扮演** — `audit-plan.md:62-138` 通过极其高压的合规/法律/SOC2 语境强迫 LLM 脱离讨好模式；附加 "Do NOT invent requirements / Do NOT say 'this is fine for v1'"  等反合理化注解。

10. **HANDOFF 中的 "READ THIS FIRST"** — `pause-work.md:72` 的 handoff 模板第一行即 "You have no prior context. This document tells you everything."，把 zero-context resumption 作为一等需求。

### 5C. 宏观设计亮点（Philosophy）

1. **Quality over speed-for-speed's-sake** — PAUL 是 GSD 的哲学对立（`PAUL-VS-GSD.md:32-50`）。GSD 追求"并行 subagent 最快"，PAUL 认为"AI 已经是速度增强，再优化速度收益递减，收益应来自每 token 的质量"。这是一个反潮流立场，但在 PAUL 的整个设计中一以贯之。

2. **Plans are prompts** — `quality-principles.md:13-24`：PLAN.md 不是会被转化为 prompt 的文档，它**本身就是 prompt**。这个立场影响了所有模板的写法（imperative voice、explicit boundaries、BDD AC）。

3. **Loop integrity as heartbeat** — `README.md:43`："Every plan closes with UNIFY. No orphan plans. UNIFY reconciles what was planned vs what happened, updates state, logs decisions. This is the heartbeat." Loop 的闭合不是流程洁癖，是学习/traceability 的前提。

4. **In-session context over subagent sprawl** — 明确对抗 subagent 默认倾向（`README.md:407-423`），将 subagent 重新定位为"discovery/research 专用工具"。

5. **Single next action 反决策疲劳** — `PAUL-VS-GSD.md:54-63`："Decision fatigue is real. PAUL analyzes project state and recommends the most logical next step." 几乎每个工作流的最后都只呈现一个建议。

6. **No enterprise theater** — `quality-principles.md:139-150` `<anti_enterprise>`：禁止"Team structures, RACI matrices, Sprint ceremonies, Human dev time estimates"。PAUL 为 solo developer + Claude 一个实现者的二人组优化。

7. **Fact/judgment/evidence 分层** — PROJECT.md（需求+约束）、PLAN.md（意图）、SUMMARY.md（结果）的严格区分，使 plan-vs-actual 对比有据可依。

8. **Aggressive atomicity** — `work-units.md:151-158`："More plans, smaller scope, consistent quality."  优先切细而不是大而全。

9. **Context economics 内嵌于所有决策** — 从 50% budget 到 progressive loading 到 aggressive atomicity 到 FRESH/MODERATE/DEEP/CRITICAL brackets，上下文被视为一等资源。

10. **Anti-rationalization 是设计目标而非装饰** — PAUL 对 LLM 自欺的针对性 prompt engineering 水平显著高于大多数同类框架，这是其最具工程价值的部分。

### 5D. 横切互联

- **quality-principles.md `<evidence_before_claims>` 表格**（10 & 11 行）被 `apply-phase.md:162-171` **字面复用**为 qualify step 的反合理化表。文档中明确声明 "This table is the canonical reference. It is embedded inline in the APPLY phase qualify step for operational enforcement."（`quality-principles.md:81-83`）—— 一处规范、一处内嵌，避免 drift。
- **checkpoints.md 的 Diagnostic routing 表** 同时被 `apply-phase.md`（checkpoint failure）和 `verify-work.md`（UAT failure）引用执行（`checkpoints.md:146-149`）—— 单一分类体系跨多个失败入口复用。
- **loop-phases.md** 被几乎所有 loop workflow 的 `<references>` 引用，作为共享的 loop 语义字典。
- **subagent-criteria.md** 被 `research.md`、`discovery.md` 引用，作为 pre-spawn gate。
- **work-units.md** 既被 `plan-phase.md` 引用（sizing 决策），又与 `context-management.md` 共享 quality degradation 曲线数据，形成一致的 context economics 叙事。
- **STATE.md** 是通用读写点 —— 21 个 workflow 中 15+ 个将其列入 `<required_reading>`。
- **PROJECT.md 的 "进化"** 是跨 phase 的长期事实，`transition-phase.md:62-95` 是唯一合法的修改入口，形成数据所有权边界。
- **paul.json 同步协议** 跨 init/unify/create-milestone/complete-milestone 四个 workflow（`src/templates/paul-json.md:61-73`），形成机器可读状态的收敛。

---

## Phase 6 — Migration Assessment

对可迁移到 `1st-cc-plugin/` 的机制做评估：

| 机制 | Transferability | Effort | Prerequisite | Risk | Failure modes |
|------|-----------------|--------|--------------|------|--------------|
| **Execute/Qualify loop + 反合理化话术** | **高** | **低**（纯 prompt 复制+改写） | 无 | 极低 | LLM 在非 PAUL 项目中缺少 STATE/PLAN 锚点，self-check 触发频率下降 |
| **Diagnostic failure routing（intent/spec/code）** | **高** | **低** | 需存在"spec 文件"（PRD、issue、plan 类载体）作为 spec 层分类对象 | 低 | 用户倾向选 code（最快），绕过分类价值 |
| **Plan vs Actual 双文件对比（PLAN+SUMMARY）** | **高** | **中**（需模板+最小 workflow） | 需要确立"不可跳过的闭环"约定 | 中 | 现有 plan 类 skill（如 `complex-task`）已部分实现，需避免重复造轮子 |
| **反合理化 prompt 表** | **极高** | **极低**（几行 markdown） | 无 | 无 | 无 |
| **Single next action 原则** | **高** | **低** | 适合 resume/status 类命令 | 低 | 单一建议错判时用户会被误导 |
| **Boundaries "DO NOT CHANGE" section** | **高** | **低** | plan 文档模板需新增 section | 低 | LLM 仍需自律遵守 |
| **Lazy @-reference 加载模式** | **中** | **低**（已是 Claude Code 约定） | 无 | 低 | 与现有插件混用时可能加载规则不一致 |
| **Rules-by-path 元规则（`src/rules/*.md` 的 `paths:` frontmatter）** | **中** | **中** | 需 Claude Code 识别同样的规则机制；验证是否适用于 plugin 内部结构 | 中 | 插件发布后用户侧规则作用域可能与开发侧不一致 |
| **STATE.md 作为项目单一事实源** | **中** | **中** | 需插件组约定一个 `.state/` 或等价位置；现有 1st-cc-plugin 并无跨 skill 的 state 约定 | 高 | 与 catchup/handoff 现有机制重叠，需先做去重 |
| **paul.json 卫星清单** | **低** | **高** | 需要外部发现系统（BASE 等）作为消费者 | 高 | 无消费者的情况下成为纯 overhead |
| **Enterprise audit 角色扮演工作流** | **高** | **低** | 无 | 低 | 可直接作为 quality/audit skill 或增强 review skill |
| **Anti-subagent 哲学** | **中** | **低**（philosophy 文档化） | 与 1st-cc-plugin 现有 parallel agent 实践冲突 | 中 | 可能违反部分插件的设计假设，需选择性应用 |
| **Context quality degradation 曲线 + aggressive atomicity** | **高** | **低** | 无 | 低 | 50% 阈值可能过于保守，需经验调整 |
| **Handoff 生命周期（create → consume → archive）** | **高** | **低** | 已与 catchup:handoff 目标重合，可增强 | 低 | 与现有 `catchup:handoff` skill 功能重叠，需评估是否合并 |
| **Type-adapted init walkthrough（Application/Campaign/Workflow/Other）** | **中** | **中** | 需 `project-init` 插件扩展 | 低 | 现有 `project-init` 插件可能已涵盖 |
| **BDD Given/When/Then AC format** | **高** | **极低** | 无 | 无 | 无 |

**推荐移植候选（按优先级）：**

1. **反合理化表 + Execute/Qualify 三阶段模式** → 并入 `quality/testing`、`quality/review`、`workflow/complex-task` 的验证步骤。这是 PAUL 最"工程化"的部分。
2. **Diagnostic failure routing** → 并入 `quality/review`、`workflow/issue-driven-dev` 的失败处理路径。
3. **Plan/Summary 双文件闭环 + "No orphan plans"** → 评估与现有 `workflow/deep-plan`、`workflow/complex-task` 的合流方式；**避免另起炉灶**。
4. **Boundaries section 硬约束** → 并入 `workflow/complex-task` 的 plan 模板。
5. **Enterprise audit 角色扮演** → 作为 `quality/` 组的新 skill 或并入 `quality/codex-review`。
6. **Single next action 原则** → 并入 `workflow/catchup` 的 resume 路径。

**不推荐移植：**
- **paul.json 卫星清单**：无消费者。
- **完整 PAUL loop 替代现有 workflow 插件**：与 `workflow/simple-task`、`workflow/complex-task`、`workflow/deep-plan` 严重重叠，迁移成本高且会造成插件功能混乱。

---

## 附录：Failure Modes（基于证据）

1. **Loop 遗忘 / orphan plans** — 证据：`unify-phase.md:228-252` 反复强调 "NEVER skip" 并设 `gate="blocking"`，说明在实际使用中确实会出现 LLM 在 UNIFY 前跳到下一个 PLAN 的倾向。anti-pattern 章节（`unify-phase.md:250-252`）明确命名此为 "closing UNIFY and immediately offering `/paul:plan` for next phase WITHOUT running transition"。

2. **STATE 三文件漂移** — 证据：`transition-phase.md:236-290` 整个 `verify_state_consistency` 步骤的存在本身就是证据；作者必定观察到 STATE.md/PROJECT.md/ROADMAP.md 在长会话后会出现字段不一致（version、phase、status、focus 漂移），才会引入 4×3 硬对齐表和 "BLOCKING: fix ALL misalignments" 话术。

3. **False completion / optimistic execution memory** — 证据：整个 Execute/Qualify loop（`apply-phase.md:118-189`）的存在就是针对这个失败模式；`quality-principles.md:59-83` 的 `<evidence_before_claims>` 表格直接命名"confidence without evidence is the #1 cause of false completion claims"。

4. **Boundary 违反的 silent cascade** — 证据：`apply-phase.md:98-101`、`353-356`、`383-390` 多处强调 "boundary violations cascade into untraceable changes"，以及 CARL `PAUL_RULE_4`（`src/carl/PAUL:13`）单独为此立规。暗示 boundary 违反是频发且难以追踪的失败模式。

5. **Diagnostic mis-classification（偷懒选 code）** — 证据：`apply-phase.md:388-390` anti-pattern "Patching without diagnosing"；`checkpoints.md:156-157` "Claude's default under pressure is to patch code because it's the fastest visible action"。作者显式命名 LLM 会在压力下默认选 code 修复路径。

6. **DONE 报告过于乐观** — 证据：`apply-phase.md:113-114` 的 "NEVER silently produce work you're unsure about — instead report DONE_WITH_CONCERNS" 明确要求对抗"假装自信"，引入 DONE_WITH_CONCERNS 这个状态本身就是对抗失败模式。

7. **Subagent 过度使用导致 context 碎片化 + 70% 质量** — 证据：`README.md:407-423` 的对比表，作者测得 subagent 输出质量约为 in-session 的 70%。

8. **Quick-fix 也要求走完 loop，但模板被过度简化时失去价值** — 证据：`plan-phase.md:144-187` 的 quick-fix track 仍保留 AC 和 verify，却去掉 boundaries/verification checklist。潜在失败模式是 quick-fix 误判为非 quick-fix 范围的任务，或反之。

---

## 总结

PAUL 是一个**纯 prompt engineering 的流程框架**，通过以下手段在 Claude Code 中建立结构化开发闭环：

- **Object model：** PROJECT（长期）+ STATE（即时）+ ROADMAP（phase）+ PLAN（意图）+ SUMMARY（证据）五件套；paul.json 提供机器侧视图
- **State machine：** PLAN → APPLY → UNIFY 三段闭环 + phase/milestone transition 顶层循环，靠 gate 话术和 CARL 规则施加 soft enforcement
- **Enforcement：** 主要靠 anti-rationalization prompt engineering、rules-by-path 元层、结构化步骤命名；极少量硬约束
- **Context strategy：** aggressive atomicity（2-3 task/plan、50% 预算）、progressive loading、lazy `@`、反 subagent 倾向
- **设计灵魂：** quality-over-speed + anti-rationalization + single next action + loop integrity 四大原则一以贯之

**工程价值最高的可迁移部分**是**反合理化 prompt 模式**（Execute/Qualify、Diagnostic routing、evidence-before-claims 表格、anti-optimism 状态枚举）。这些模式针对 LLM 的具体失败模式而设计，比抽象的"要仔细"有效得多，且与任何流程框架正交，可无损嫁接。

**工程价值最低的可迁移部分**是完整的 PAUL loop 替代方案——与 `1st-cc-plugin/workflow/*` 现有插件严重重叠，应做合流而非复制。

---

## 附录：Gemini Deepdive 补充信息

> 来源：`1st-cc-plugin/workflows/loaf/docs/gemini-roadmap-review/deepdive-paul.md`
> 补充内容：Token 预算启发式、Lean Injection 原则、两级 Continuity 区分、Session 命令流。

### A.1 显式 Token Budget 启发式

Deepdive 给出了 PAUL 各阶段的参考 token 消耗（主报告未量化）：

| 阶段 | 估算 Token |
|------|-----------|
| PLAN.md 读取 | ~3-5k |
| 源码上下文读取 | ~1-3k |
| 任务执行 | ~5-15k |
| 验证 | ~2-5k |
| SUMMARY.md 更新 | ~2-3k |

总计单次循环约 13-30k tokens，留出余量确保不超出 context window。

### A.2 Lean Injection 原则

主报告提到了 context 管理但未提取出这组设计原则：
- **渐进式详细度**：STATE.md（最简摘要）→ SUMMARY.md（结构化状态）→ 源文件（按需读取）
- **"Summaries Over Plans"**：agent 应优先读取结果摘要而非原始 plan——plan 是写给人的，摘要是优化给 LLM 的
- **避免反射式链接**：不自动加载所有相关文件，仅按当前任务需求精确加载

### A.3 两级 Continuity 机制

| 级别 | 文件 | 适用场景 | 内容 |
|------|------|----------|------|
| Light | `STATE.md` | 同天恢复 | 最小化当前任务状态 |
| Full | `HANDOFF-{date}.md` | 零上下文恢复（跨天/跨人） | 完整项目状态 + 决策历史 + 下一步 |

### A.4 Session 命令流的细节

- `/paul:pause`：agent 写入 STATE.md 后停止
- `/paul:handoff`：agent 生成 HANDOFF-{date}.md（完整上下文快照）
- `/paul:resume`：读取最新 STATE 或 HANDOFF，**建议唯一一个下一步行动**（非列表）
- `/paul:progress`：mid-session 路由——检查当前 bracket，决定是继续、切换任务还是 handoff
