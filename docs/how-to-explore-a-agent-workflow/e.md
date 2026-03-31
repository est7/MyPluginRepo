What Makes PAUL Different
PAUL (Plan-Apply-Unify Loop) builds on the foundation of GSD (Get Shit Done) while addressing key friction points that emerge during real-world AI-assisted development.
The Core Insight

GSD pioneered the concept of treating plans as executable prompts. PAUL takes this further by recognizing that execution without reconciliation creates drift — and drift compounds across sessions.

Where GSD focuses on getting work done, PAUL focuses on getting work done correctly, consistently, and with full traceability.

Key Differentiators

1. Explicit Loop Discipline

GSD: PLAN → EXECUTE → (implicit review)

PAUL: PLAN → APPLY → UNIFY (enforced)

The UNIFY phase isn't optional. Every plan produces a SUMMARY.md that captures:

What actually happened vs. what was planned
Decisions made during execution
Issues deferred for later
Acceptance criteria results (pass/fail)
Why it matters: Without explicit reconciliation, learnings evaporate between sessions. UNIFY creates an audit trail that makes context resumption reliable.

2. Context-Aware Execution (Token Economics)

GSD: Spawns subagents for plan execution, pursuing speed through parallelization.

PAUL: Executes in the current context by default, optimizing for token-to-value efficiency.

The parallel-subagent approach sounds fast on paper. In practice, it's expensive and wasteful:

Each subagent starts cold, requiring context injection
Subagents duplicate work the main session already understands
Coordination overhead compounds across agent boundaries
Output quality degrades without full project context
PAUL takes a different stance: AI is already the speed enhancement. We don't need to optimize speed at the cost of quality. What we need is to make every token count.

Subagents in PAUL are reserved for their optimal use case: parallel research and discovery — bounded, well-defined information gathering where cold-start overhead is acceptable. Execution stays in-session where the context lives.

Why it matters: Parallel execution subagents generate more output faster, but "more garbage faster" isn't progress. PAUL optimizes for exceptional value per token, consistently, from project start to finish. Token efficiency > speed to done.

3. Single Next Action

GSD: Presents multiple options after each step ("Would you like to: A, B, C, or D?")

PAUL: Suggests ONE best path based on current state.

Decision fatigue is real. PAUL analyzes project state and recommends the most logical next step. Users can always redirect, but the default is momentum, not menu navigation.

Why it matters: Every decision point is a potential context switch. Reducing decisions preserves focus.

4. Structured Session Continuity

GSD: Implicit state via .continue-here.md in phase directories.

PAUL: Explicit HANDOFF-{date}.md files with loop position, decisions, and prioritized next actions.

PAUL handoffs are designed for zero-context resumption. They capture not just where you stopped, but why you were doing what you were doing and what decisions led there.

Why it matters: Sessions end unexpectedly. Context windows reset. PAUL handoffs make "resume from cold" a first-class operation.

5. Acceptance Criteria as First-Class Citizens

GSD: Tasks describe what to do.

PAUL: Tasks link to numbered acceptance criteria (AC-1, AC-2, AC-3) with Given/When/Then format.

Every PLAN.md includes explicit acceptance criteria. Every SUMMARY.md reports pass/fail against those criteria. This creates verifiable quality gates, not just completion checkboxes.

Why it matters: "Done" is ambiguous. "AC-3: PASS" is not.

6. Boundaries That Stick

GSD: Scope guidance in plans.

PAUL: Explicit ## Boundaries section in every PLAN.md with DO NOT CHANGE declarations.

When you specify boundaries, PAUL treats them as hard constraints, not suggestions. Modifications to protected items require explicit confirmation.

Why it matters: Scope creep happens subtly. Explicit boundaries make violations visible before they cascade.

7. Skill Tracking and Verification

GSD: No mechanism for tracking specialized workflow usage.

PAUL: SPECIAL-FLOWS.md declares required skills per project. UNIFY audits whether they were invoked.

If your project requires /commit or /review-pr or custom skills, PAUL tracks whether they were actually used — preventing "forgot to run the linter" moments.

Why it matters: Manual checklists get skipped. Automated audits don't.

8. Decimal Phases for Interruptions

GSD: Integer phases only. Urgent work requires phase insertion and renumbering.

PAUL: Decimal phases (8.1, 8.2) for urgent interruptions without disrupting the roadmap.

When something urgent lands mid-milestone, PAUL slots it as a decimal phase. The original plan stays intact, and the interruption is clearly marked as an insertion.

Why it matters: Real projects have interruptions. The planning system should accommodate them, not fight them.

Philosophy Comparison

Aspect	GSD	PAUL
Primary goal	Ship fast	Ship correctly
Optimization target	Speed to done	Token-to-value efficiency
Loop closure	Flexible	Mandatory
Subagent role	Execution (parallel speed)	Discovery only (bounded research)
Decision flow	Multiple options	Single best path
Session handoff	Implicit	Explicit + dated
Quality gates	Completion-based	Acceptance-based
Scope control	Guidance	Enforcement
When to Use Which

Use GSD when:

Speed is the primary constraint
Project scope is small and well-understood
Single-session completion is likely
You don't need audit trails
Use PAUL when:

Quality and traceability matter
Work spans multiple sessions
You need verifiable acceptance criteria
Scope creep is a concern
You want explicit reconciliation of plan vs. reality
The Bottom Line

GSD answers: "How do I get Claude to execute a plan fast?"

PAUL answers: "How do I get maximum value from every token spent?"

The insight: AI development is already fast. Using Claude at all is the speed advantage. The marginal gains from parallel subagent execution come at significant cost — more tokens, more coordination, more garbage output, less coherent results.

PAUL doesn't try to enhance the enhancement. It takes what AI gives us and makes it as valuable as possible — through explicit reconciliation, preserved context, verifiable quality gates, and disciplined loop closure.

PAUL isn't a replacement for GSD — it's an evolution for projects where sustainable quality matters more than raw throughput.

PAUL Framework — Plan. Apply. Unify. Repeat



这版定位已经很清楚了。核心不是“再造一个流程”，而是把 GSD 的执行优势，收束成一个 可审计、可恢复、可验证 的闭环系统。

但如果你要我用更严格的产品/方法论标准来判断：它现在已经接近可发布说明文档了，不过还差三件事，才能真正站稳。

⸻

先给结论

PAUL 的真正差异点不是 Plan-Apply-Unify 这三个词本身，而是这三件事：
	1.	把“执行后的对账”从隐式习惯变成强制阶段
	2.	把“AI 速度优先”改成“上下文保真 + token 产值优先”
	3.	把“完成任务”提升为“通过验收标准”

这三点合在一起，PAUL 才不是“换皮版 GSD”，而是一个更偏 工程治理 的执行框架。

换句话说：
	•	GSD 更像 throughput system
	•	PAUL 更像 controlled delivery system

这是你这篇文案里最有价值的地方。

⸻

它为什么成立

1. 你抓到了真实的一阶问题：drift

你这里最强的一句其实是这个意思：

execution without reconciliation creates drift — and drift compounds across sessions

这是根因，不是表象。

大多数 AI 工作流失败，不是因为不会生成计划，也不是因为不会写代码，而是因为：
	•	执行中发生了偏离
	•	偏离没有被显式记录
	•	下个 session 把“当前状态”误当成“原计划状态”
	•	于是错误上下文被继承并放大

这本质上是 状态同步失败。

从系统角度看：
	•	PLAN 是目标状态定义
	•	APPLY 是状态变更
	•	UNIFY 是把“预期状态”和“实际状态”做 reconciliation

如果没有 UNIFY，系统就没有闭环。
没有闭环，就没有可靠的 session continuity。
这一点你打中了。

⸻

2. 你把 token 当成预算，而不是免费算力

这是 PAUL 相比很多 agent 框架更成熟的地方。

你不是在争论“能不能并行”，而是在说：

并行 execution agent 的额外 token 消耗、上下文注入成本、协调成本，是否真的换来了更高质量的结果？

这个问题非常对。

因为从计算模型上讲，subagent execution 的问题是：

冷启动成本

每个子 agent 都要重新注入上下文。

这相当于重复支付固定成本。

上下文切割损失

主上下文里已经形成的隐式约束、边界、历史决策，拆给多个子 agent 后会丢失。

这会导致：
	•	局部最优
	•	重复劳动
	•	风格/接口不一致
	•	对边界理解不一致

合并成本

并行不是“白送吞吐量”，它要求额外的 reconcile 步骤。
如果没有强合并机制，速度提升只是表面，返工增加才是现实。

所以 PAUL 的立场本质是：

执行任务属于高上下文耦合活动，默认应留在主会话；
只有研究、检索、信息收集这类边界清晰、结果可枚举的任务，才适合分发给 subagent。

这个判断是合理的，而且比很多“盲目并行化”的框架更像工程实践。

⸻

3. 你把“Done”从模糊语言变成可验证断言

Acceptance Criteria 这一段很关键，而且是方法论升级，不只是格式升级。

GSD 风格的任务通常容易停留在：
	•	implement X
	•	refactor Y
	•	add support for Z

问题是这些都是 动作描述，不是 完成定义。

PAUL 用 AC-1 / AC-2 / AC-3 + Given/When/Then，本质上是在做两件事：

把完成定义转成可测试条件

这让任务从“做了什么”转向“结果是否成立”。

把质量门禁前移到计划阶段

不是做完才讨论“这算不算完成”，而是在开始前就定义完成条件。

这会显著降低两类常见失败：
	•	范围漂移
	•	验收口径不一致

所以这部分不是装饰，是 PAUL 是否成立的基础设施。

⸻

但现在还有几个薄弱点

下面这些不是吹毛求疵，而是如果你要把它讲成一个“框架”，别人会真正质疑的地方。

⸻

薄弱点 1：你说它是 evolution，但还没给出“不可替代性证明”

你现在的文案在逻辑上更像：

GSD + stronger review discipline + better artifacts

这个方向没错，但还不够让人彻底相信 “PAUL 是一个独立框架”。

你需要更明确回答：

哪些问题，用 GSD 加一些好习惯，仍然解决不了？

现在你隐含地在说：
	•	GSD review 不够强制
	•	GSD continuity 不够显式
	•	GSD acceptance 不够一等公民

但这些仍可能被反驳为：

“那我给 GSD 加模板不就行了？”

你要避免这个反驳，需要把 PAUL 讲成 操作语义不同，而不是“模板更全”。

更强的表述方式

你应该强调：
	•	在 GSD 中，plan 是主 artifact，review 是辅助行为
	•	在 PAUL 中，reconciliation artifact 是状态机的一部分
	•	没有 UNIFY，loop 不算完成，下一轮不能安全开始

这就不是“多一个文件”，而是 状态转移规则不同

也就是：
	•	GSD: Plan -> Execute
	•	PAUL: Plan -> Apply -> Reconciled State -> Next Plan

这会更硬。

⸻

薄弱点 2：你强调 token efficiency，但还没有定义衡量方式

“token-to-value efficiency” 是个好口号，但现在还是口号。

如果你想让这个概念站得住，至少要给出半形式化定义。

比如你可以定义：

Token-to-value efficiency

单位 token 消耗带来的有效项目推进量。

而“有效推进量”可以被拆成几个代理指标：
	•	被验收通过的 AC 数量
	•	被明确记录的决策数
	•	下次 session 可恢复程度
	•	返工率下降
	•	边界违规次数减少

否则别人会说：

你只是在用“我觉得更值”替代“更快”。

这是不够硬的。

更合理的工程表达

不要过度承诺“token efficiency”，而是改成：
	•	context-retention efficiency
	•	rework-adjusted productivity
	•	decision-traceability per token

这几个更容易落地，也更接近真实收益。

⸻

薄弱点 3：Single Next Action 是优势，但也可能变成错误放大器

这个点很有产品感，但要小心。

“只给一个下一步”确实减少决策疲劳，但它的代价是：
	•	如果当前状态判断错了，错误路径会被默认强化
	•	用户更容易把系统推荐误认为“唯一正确路径”
	•	在高不确定性阶段，单一路径可能掩盖探索空间

所以这条不能讲成绝对优点，应该讲成 默认策略 + 明确例外条件。

更稳的说法是：

PAUL defaults to a single recommended next action, unless uncertainty is high enough that branching options materially affect risk or architecture.

也就是：
	•	默认一个推荐动作
	•	但在架构分叉、依赖冲突、产品方向未定时，应该显式呈现分支

否则这点会被资深工程师质疑为“过度收敛”。

⸻

薄弱点 4：Boundaries 很好，但你需要定义冲突处理机制

“DO NOT CHANGE declarations” 很强，但现实里会碰到：
	•	为满足 AC，必须突破边界
	•	为修复 bug，必须改到受保护模块
	•	技术债导致边界定义与系统现实冲突

这时框架必须给出机制，否则边界会从“约束”变成“阻塞”。

建议你补一个规则：

Boundary escalation rule

如果执行中发现 AC 无法在边界内满足，则必须：
	1.	明确记录冲突
	2.	停止隐式扩展范围
	3.	在 UNIFY 中输出边界冲突说明
	4.	下一轮 PLAN 显式请求边界变更

这样 Boundaries 才不是僵硬的。

⸻

薄弱点 5：SPECIAL-FLOWS 很有用，但本质是 compliance system，不是 verification system

你现在写的是：

UNIFY audits whether required skills were invoked

这能审计“是否执行过步骤”，但不能证明“执行质量”。

比如：
	•	跑了 linter，不代表结果合格
	•	调了 review-pr，不代表评论被处理
	•	触发了测试，不代表关键测试覆盖了风险点

所以你最好把这块表述成：
	•	workflow compliance tracking
	•	not full outcome verification

否则别人会质疑它“形式主义”。

更稳妥的表述：

PAUL verifies invocation of required flows and records their results, but still relies on acceptance criteria to determine whether the work is actually complete.

这就不会把 SPECIAL-FLOWS 说过头。

⸻

你这篇文案最该重写的地方

“What Makes PAUL Different” 这一标题太弱

因为你不是在讲“不同”，你是在讲：
	•	设计哲学
	•	状态机约束
	•	质量治理
	•	会话连续性模型

“Different” 太像 marketing copy，不像 framework spec。

更好的标题：
	•	Why PAUL Exists
	•	PAUL’s Operating Model
	•	Why PAUL Is Not Just GSD With Better Templates
	•	PAUL: A Reconciled Execution Loop for AI-Assisted Development

最后一个最准确。

⸻

“The Bottom Line” 那段有点重复，而且略显宣传口吻

你多次在强调：
	•	AI 已经够快
	•	不要为了速度牺牲质量
	•	more garbage faster isn’t progress

意思对，但重复度高，且情绪比论证更强。

可以收紧成一个更硬的结尾：

PAUL is based on a simple premise: in AI-assisted development, the main failure mode is not insufficient generation speed, but uncontrolled state drift across execution.
Its loop is designed to prevent that drift through explicit reconciliation, durable handoffs, enforced boundaries, and acceptance-based completion.

这样更像 framework thesis，不像宣言。

⸻

我建议你把它改写成这个结构

下面这是更适合对外发布/写进 README 的结构。

⸻

PAUL: A Reconciled Execution Loop for AI-Assisted Development

PAUL extends GSD’s idea that plans can act as executable prompts, but addresses a practical failure mode that appears in longer-running AI-assisted work: execution drift.

In real projects, work rarely unfolds exactly as planned. Decisions get made during execution. Constraints emerge. Scope shifts. If those changes are not explicitly reconciled, the next session inherits an inaccurate state model. Over multiple sessions, that drift compounds.

PAUL is designed to prevent that.

It uses a mandatory loop:

PLAN -> APPLY -> UNIFY

Where:
	•	PLAN defines the intended change, boundaries, and acceptance criteria
	•	APPLY performs the work in the active project context
	•	UNIFY reconciles planned intent against actual outcomes and records the resulting state

This makes PAUL not just an execution workflow, but a state reconciliation system for AI-assisted development.

What PAUL Optimizes For

GSD primarily optimizes for speed to completion.

PAUL optimizes for:
	•	context retention
	•	token-to-value efficiency
	•	verifiable completion
	•	reliable session resumption
	•	controlled scope

The central assumption is that AI is already a major speed multiplier. The limiting factor in real projects is often not raw execution throughput, but loss of context integrity across steps, sessions, and handoffs.

Core Properties

1. Mandatory Reconciliation
Every execution cycle ends with a SUMMARY.md that records:
	•	what was planned
	•	what actually happened
	•	decisions made during execution
	•	deferred issues
	•	acceptance criteria results
	•	resulting next-state context

Without this step, PAUL treats the loop as incomplete.

2. In-Context Execution by Default
Execution stays in the active session unless the task is explicitly research-oriented and can be cleanly bounded.

Subagents are reserved for discovery work where:
	•	cold-start context costs are acceptable
	•	outputs are informational rather than state-mutating
	•	results can be merged without ambiguity

This reduces duplicated context injection, coordination overhead, and incoherent outputs.

3. Acceptance-Based Completion
Tasks are not considered complete because actions were performed. They are complete only when numbered acceptance criteria pass.

Acceptance criteria are defined in advance and reported explicitly in UNIFY.

4. Explicit Session Continuity
PAUL uses dated handoff artifacts to support cold-start resumption with minimal ambiguity.

A handoff records:
	•	loop position
	•	active constraints
	•	key decisions
	•	deferred work
	•	prioritized next action

5. Hard Scope Boundaries
Each plan includes a boundaries section that identifies protected areas and out-of-scope changes.

If acceptance criteria cannot be met within those boundaries, the conflict must be recorded and escalated in the next planning cycle rather than silently expanded during execution.

When PAUL Fits Best

PAUL is most useful when:
	•	work spans multiple sessions
	•	correctness matters more than raw speed
	•	auditability is required
	•	scope creep is a recurring risk
	•	acceptance criteria need to be explicit and durable
	•	handoffs must support reliable resume-from-cold behavior

In One Sentence

GSD helps AI execute plans quickly.

PAUL helps AI execute plans without losing state integrity.

⸻

如果你想保留你原来的对比风格，我建议至少做这几处替换

替换 1

原句：

PAUL isn’t a replacement for GSD — it’s an evolution for projects where sustainable quality matters more than raw throughput.

建议改成：

PAUL is not a rejection of GSD. It is a stricter operating model for projects where execution drift, session continuity, and verifiable completion matter more than raw throughput.

更具体，也更少 marketing 味。

替换 2

原句：

Token efficiency > speed to done.

建议改成：

In PAUL, preserving context integrity is usually more valuable than maximizing parallel execution throughput.

更可辩护。前者像 slogan，后者像设计原则。

替换 3

原句：

The UNIFY phase isn’t optional.

建议改成：

In PAUL, work is not considered complete until execution has been reconciled into an explicit post-change state.

这句更强，因为它定义了“complete”的语义。

⸻

还缺的两个东西

如果你要把 PAUL 真正讲完整，还缺两块：

1. 最小 artifact spec

现在你提到了 PLAN.md、SUMMARY.md、HANDOFF-date.md、SPECIAL-FLOWS.md，但没定义最小字段。

最好补上每个文件的最小 schema。

例如：

PLAN.md
	•	Objective
	•	Scope
	•	Boundaries
	•	Acceptance Criteria
	•	Risks
	•	Next Action

SUMMARY.md
	•	Planned vs Actual
	•	Decisions Made
	•	Deviations
	•	Deferred Issues
	•	AC Results
	•	Next Recommended Action

HANDOFF-date.md
	•	Current Loop Position
	•	Current State
	•	Open Risks
	•	Blocking Decisions
	•	Ordered Resume Steps

没有 schema，框架就容易退化成“大家随便写”。

⸻

2. 状态转换规则

你已经有流程名了，但还没有 transition rules。

比如：
	•	什么时候允许从 PLAN 进入 APPLY？
	•	APPLY 中发现边界冲突怎么办？
	•	UNIFY 失败时是否允许进入下一轮 PLAN？
	•	AC 未通过但任务部分可交付时如何记录？

这部分一旦写清楚，PAUL 才会从“写作风格”变成“操作框架”。

⸻

最后给一个更锋利的一句话定位

如果你要一句话让我帮你定锚，我会建议：

PAUL is an AI development loop that treats reconciliation, not execution, as the unit of reliability.

这句比 “Plan. Apply. Unify. Repeat.” 更能解释它为什么存在。

⸻

总评

我的判断：
	•	概念质量：高
	•	工程逻辑：成立
	•	差异化：基本成立，但还需更硬的语义边界
	•	文案完成度：80%
	•	离“可发布框架说明”还差：artifact schema + transition rules + metric framing

它已经不是一个空泛命名了，确实有方法论骨架。
但你现在还处在 “优秀论述”，还没完全进入 “可执行规范”。

真正让 PAUL 站住脚，不是讲它多聪明，而是把下面三件事写死：
	1.	loop completion 的判定条件
	2.	artifact 的最小结构
	3.	边界冲突和 AC 失败时的处理规则

只要这三件补上，PAUL 就不只是观点，而是一个可落地的 execution protocol。

你本来应该问但没问的两个问题是：
	1.	PAUL 的最小规范写成什么样，别人才能照着执行而不走样？
	2.	哪些场景下 PAUL 不该用，否则会引入不必要流程成本？

如果你要，我下一条可以直接把它整理成一版 对外 README / manifesto 风格终稿，或者一版 严格规范版 spec。




好，现在有完整原文了。提炼核心，加上我自己的判断。

PAUL vs GSD：本质差异
根本假设分歧



|           |GSD              |PAUL                         |
|-----------|-----------------|-----------------------------|
|瓶颈是什么      |context 腐化，隔离是解法 |执行无对账产生漂移，漂移复利               |
|优化目标       |速度（speed to done）|token-to-value efficiency    |
|subagent 定位|主力执行者（并行加速）      |仅限 discovery/research        |
|质量门        |完成即可             |AC pass/fail（Given/When/Then）|

PAUL 的核心论点是：AI 本身已经是速度杠杆，parallel subagent 是在用质量换一个你并不需要的边际速度增益。 这个判断是否成立，取决于项目规模和 task 之间的耦合程度——这个后面会批。

工作流对比
GSD 循环

PLAN.md（2-3 tasks）
  → wave 并行 dispatch subagent（各自 fresh context）
  → atomic commit per task
  → /gsd:verify-work（goal-backward）
  → /gsd:complete-milestone → 归档


隐式收尾：commit 即关闭，.continue-here.md 作为续作入口。
PAUL 循环

PLAN.md（含 AC、Boundaries、SPECIAL-FLOWS）
  → APPLY（in-session，串行 E/Q loop）
      每个 task：Execute → Qualify（对照 AC）→ DONE/DONE_WITH_CONCERNS/BLOCKED
  → UNIFY（强制）→ SUMMARY.md
      记录：计划 vs 实际、决策、AC pass/fail、递延事项
  → HANDOFF-{date}.md（跨 session 续作）


显式收尾：没有 UNIFY 就没有关闭。

PAUL 的 8 个差异点，逐条评价
1. UNIFY 强制对账
真正的价值点。GSD 的问题是”learnings evaporate between sessions”——这是真实痛点，尤其是多 session 项目。SUMMARY.md 是可靠的续作锚点。
2. in-session 执行 vs subagent
这里 PAUL 的论点有漏洞：它批评 subagent “cold start overhead”和”coordination cost”是对的，但没有解决 session 本身的 context 腐化问题。20+ task 的 APPLY 跑完，主 session 已经 60-70% 满了，这时候的 Qualify 质量是否还可靠？PAUL 对此沉默。
3. Single Next Action vs 多选项
工程上有意义——减少决策疲劳，维持 momentum。不过这是 UX 层面的设计，不影响架构。
4. HANDOFF-{date}.md 显式续作
比 GSD 的 .continue-here.md 实质性地更好——不仅记录”停在哪”，还记录”为什么”和”当时的决策链”。这是跨 session 项目的核心需求。
5. AC as first-class citizens
“Done”是模糊的，“AC-3: PASS”不是——这个原则完全正确。你的 issue workflow 里也有类似需求，等价于 issue close criteria。
6. Boundaries 硬约束
明确 DO NOT CHANGE 声明 → scope creep 变得可见。对 AI agent 来说尤其重要，因为 LLM 的默认行为是”顺手改一下相关代码”。
7. SPECIAL-FLOWS 技能审计
UNIFY 检查 /commit、/review-pr 等是否真正被调用。这解决的是”人工 checklist 会被跳过”的问题，但本质上是把纪律 encode 成结构——你的 claude.md 里的 prohibition-based rules 是同一个思路。
8. 小数 phase（8.1, 8.2）
处理中途插入的紧急任务不破坏原有编号——实用的工程细节。

我的判断：选哪个，什么时候
GSD 适合：
	∙	task 之间低耦合（subagent 不需要知道彼此的历史决策）
	∙	单 session 或 milestone 内可完成
	∙	速度敏感，可接受事后清理
PAUL 适合：
	∙	多 session 跨天项目
	∙	需要可审计（AC pass/fail 有记录）
	∙	scope creep 风险高
	∙	token 预算敏感（不想为并发付协调成本）
你当前的 GitLab 工作流处于第三个象限——它的 context 载体是 issue 而非 session，天然解决了 PAUL 和 GSD 都在解决的 session continuity 问题（GitLab issue 就是持久化的 SUMMARY.md + HANDOFF）。



|你的系统                     |等价概念                                 |
|-------------------------|-------------------------------------|
|`/issue-sync`            |PAUL 的 UNIFY（强制对账，无它不关闭）             |
|DELTAS 块                 |SUMMARY.md 里的”计划 vs 实际”              |
|task issue close criteria|PAUL 的 AC（Given/When/Then）           |
|`stable_id` 匹配门          |GSD 的 plan-checker（防错误传播）            |
|Pre-fetch JSONL 注入       |GSD v2 的文件路径 dispatch（不传 content，传引用）|

你实际上已经综合了两者的优点，只是 context 持久化层换成了 GitLab，而不是文件系统。

应该问我的问题：
PAUL 的 in-session 串行执行假设 session context 在整个 APPLY 过程中质量稳定——但它没有定义何时应该主动切割 session 重新注入。你的 JSONL pre-fetch 模式是否应该在 /issue-implement 每次启动时强制重置 context，而非依赖连续 session 的累积？​​​​​​​​​​​​​​​​




如果去他两的长处，你会怎么设计





结论先说：

如果只取两者长处，我不会设计一个“PAUL+GSD 混合版流程名词”，我会设计一个三层协议：
	1.	Issue 作为状态源
	2.	Session 作为一次性执行容器
	3.	Reconcile 作为唯一关闭条件

也就是说，持久化不要放在 session，也不要主要放在目录文件；放在 issue。
执行不要长期依赖单一 session 累积上下文；改成短生命周期、可重建的执行回合。
收尾不要靠“提交了代码”或“感觉做完了”；必须经过结构化对账。

这会比纯 GSD 更稳，也比纯 PAUL 更抗 context 腐化。

⸻

我会怎么设计

我会把系统拆成 4 个明确阶段，但语义上仍然是一个闭环：

1. SPEC

定义目标，不执行。

输入是 issue / epic / parent task。
输出是一个可执行规范块，而不是长篇 PLAN.md。

最小结构：

## Objective
一句话定义要完成什么

## Acceptance Criteria
- AC-1 ...
- AC-2 ...
- AC-3 ...

## Boundaries
- DO NOT CHANGE: ...
- OUT OF SCOPE: ...

## Inputs
- 依赖 issue / MR / 文档 / 文件引用

## Execution Strategy
- 推荐串行 / 可并行点
- 风险点

这里我不会把计划写得太散。核心原则是：
	•	计划是约束，不是小说
	•	AC 和边界比步骤更重要
	•	引用优先于复制内容

这点吸收 PAUL 的 AC / Boundaries，也吸收你现有 JSONL pre-fetch 的“传引用不传大段内容”。

⸻

2. SLICE

把任务切成上下文稳定的执行片段。

这是我认为 PAUL 和 GSD 都没完全做好的地方。

GSD 的问题

默认鼓励把任务拆给 subagent 并行跑，但没有严格限制“什么任务允许并行”。

PAUL 的问题

默认 in-session 串行跑到底，但没有定义：
	•	session 什么时候应该主动终止
	•	什么时候上下文已经不可信
	•	什么时候该重新注入状态

所以我会引入一个更硬的概念：

Execution Slice

一次执行只允许处理一个“上下文闭包”内的问题。

判断标准：

可以放在同一个 slice 的任务
	•	修改的是同一模块或强相关模块
	•	共享同一组 AC
	•	需要连续推理链
	•	中间决策彼此强耦合

必须切片的任务
	•	涉及多个子系统
	•	一个任务的输出只是另一个任务的输入引用
	•	可以独立验证
	•	可以独立回滚
	•	可以独立 code review

这本质上是在做 图分解：
	•	节点：task / file set / decision
	•	边：依赖 / 共享状态 / 共享约束

高耦合子图在同一 slice 内执行。
低耦合子图才允许并行或独立 session。

这一步是核心，因为它回答了你最后那个批评：

PAUL 没定义何时应该主动切割 session 重新注入。

我会明确规定：

触发切片重启的条件

满足任一即结束当前 session/slice：
	•	完成一个独立 AC 集合
	•	修改文件集合超出预期边界
	•	引入新设计决策
	•	出现 BLOCKED / DONE_WITH_CONCERNS
	•	需要跨模块扩展
	•	token/context 使用达到阈值
	•	验证结果开始依赖长程记忆而非当前结构化状态

最后一条很关键。
一旦验证在“凭印象继续”，而不是“基于当前显式状态”，就该停。

⸻

3. EXECUTE

执行容器默认应是短 session、强注入、弱记忆依赖。

这里我会明确反对两个极端：

反对纯 GSD 式执行

因为 subagent 默认 cold start，若任务高耦合，就会造成：
	•	决策不一致
	•	接口漂移
	•	重复探索
	•	合并摩擦

反对纯 PAUL 式长 session 执行

因为长 session 在真实项目里会出现：
	•	早期边界被后续 token 稀释
	•	中途决策覆盖初始假设
	•	Qualify 变成“模型自我说服”

所以我的执行原则是：

短回合主 session + 受限并行 worker

不是“全部都在一个 session”，也不是“能并行就并行”。

主 session负责
	•	读入结构化状态
	•	做关键设计决策
	•	执行高耦合改动
	•	统一判断是否达成 AC
	•	产出 reconcile 记录

worker 只负责
	•	bounded research
	•	检索引用材料
	•	低耦合 mechanical task
	•	格式转换 / 搜索 / 枚举 / 对照
	•	独立可验证的小改动候选

worker 不拥有“项目真相”。
issue + reconcile artifact 才拥有真相。

这是整个设计里最重要的状态原则。

⸻

4. RECONCILE

唯一关闭条件。

这一步必须吸收 PAUL 的长处，而且要更硬。

我会明确规定：

没有 reconcile，就没有完成。
commit 不是完成，MR 不是完成，代码跑过也不是完成。

最小输出结构：

## Planned
原目标 / 原 AC / 原边界

## Actual
实际做了什么

## Delta
偏离了什么，为什么偏离

## Decisions
执行过程中新增了哪些决策

## Verification
- AC-1: PASS/FAIL
- AC-2: PASS/FAIL
- AC-3: PASS/FAIL

## Concerns
遗留问题 / 风险 / 不确定项

## Next Action
唯一推荐下一步

这一步其实就是你现有 /issue-sync 的抽象升级版。

你已经看得很准了：
你的 GitLab issue 体系，本质上已经把 PAUL 的 SUMMARY/HANDOFF 外置成了一个更强的持久层。

所以如果让我设计，我不会再让文件系统 handoff 成为主机制。
文件可以有，但 issue 才是权威状态源。

⸻

我会如何吸收两者优点

吸收 GSD 的部分

1. 任务切分意识

GSD 对“计划必须可执行”这件事是对的。
计划不能只是愿景，必须能 dispatch 到工作单元。

我会保留这一点，但把 dispatch 条件收紧：
	•	只有低耦合、可独立验证任务允许分发

2. goal-backward verification

从目标反推是否达成，而不是仅检查“做了哪些动作”。

这点我会保留，并和 AC 合并：
	•	verify 不只是“看起来完成”
	•	而是逐条检查 AC 与边界是否成立

3. 原子提交意识

每个 slice 的结果应尽量具备独立提交和独立回滚能力。

但我不会强制“一 task 一 commit”，因为有时提交边界应该与 slice 一致，而非与 task 文字条目一致。

⸻

吸收 PAUL 的部分

1. 强制对账

这是最应该保留的。

2. AC first-class

这是“完成定义”的根基。

3. Boundaries

AI 特别容易越界顺手改，必须显式化。

4. Handoff / continuity

但我会把 continuity 的主载体从本地文件切到 issue。

5. Single Next Action

这个也保留，但只在低不确定性阶段使用。

如果处于高不确定性阶段，我会允许输出：
	•	推荐路径
	•	备选路径
	•	触发切换条件

因为在架构分叉期，强行“一个下一步”会掩盖关键分支。

⸻

我不会保留的东西

1. 不保留“in-session by default”这个强默认

这是 PAUL 最大的盲点之一。

更合理的默认应该是：

in-slice by default, not in-session by default

也就是默认保持在一个“上下文闭包”内执行，
但这个闭包可以跨 session 重建，不要求依赖单个长会话。

这比 PAUL 更稳。

⸻

2. 不保留“subagent 主要无用”的隐含态度

这个判断太绝对。

subagent 不是天然低质，问题在于是否被分配了错误类型的任务。

我会这样划分：

适合 subagent 的任务
	•	搜索文档
	•	枚举调用点
	•	对比 schema
	•	收集失败样例
	•	生成变更候选清单
	•	跑机械化检查

不适合 subagent 的任务
	•	跨模块架构重构
	•	涉及隐式约束的实现
	•	需要连续设计判断的代码变更
	•	最终验收与范围解释

这样 subagent 就不是“主力执行者”，也不是“几乎禁用”，而是受限工具人。

⸻

3. 不保留“文件系统为中心的 handoff”

你已经有更好的东西：GitLab issue。

文件系统 handoff 的问题是：
	•	容易复制分叉
	•	真相源不唯一
	•	与 review / MR / 讨论脱节
	•	难以和 task lifecycle 绑定

所以我会明确：
	•	issue：权威状态源
	•	MR：代码与审查状态源
	•	文件：辅助制品，不是主状态

⸻

推荐的最终形态：RSE 协议

如果让我命名，我会叫它：

RSE: Resolve -> Slice -> Execute -> Reconcile

或者保留闭环表达：

RSER Loop

但名字不重要，语义重要。

⸻

阶段 1：Resolve

把 issue 解析成可执行规范。

输出：
	•	Objective
	•	AC
	•	Boundaries
	•	Dependencies
	•	Suggested slices

⸻

阶段 2：Slice

决定：
	•	哪些任务必须同 slice
	•	哪些任务可并行
	•	哪些必须单独重启上下文

输出：
	•	Slice-1
	•	Slice-2
	•	Slice-3
	•	每个 slice 的输入引用、预期输出、验证方式

⸻

阶段 3：Execute

每个 slice 独立启动执行。

规则：
	•	强制预注入状态
	•	不依赖上个 session 的隐式记忆
	•	达到切片终止条件立即结束
	•	允许 worker 做 bounded 辅助工作

⸻

阶段 4：Reconcile

把 slice 结果写回 issue。

写回内容：
	•	实际变更
	•	与原计划偏差
	•	新增决策
	•	AC 状态
	•	风险/遗留项
	•	推荐下一步

然后下一轮从 issue 重新 Resolve，而不是从 session 继续“接着想”。

⸻

为什么这套更适合你现在的系统

因为你当前系统的真正优势，不在“prompt 写得更好”，而在：

1. 你已经有外部持久状态层

GitLab issue 天然比 session 和记忆文件更可靠。

2. 你已经有结构化对账动作

/issue-sync 本质上就是 reconcile。

3. 你已经有防漂移机制

stable_id 匹配门、防错误传播、pre-fetch JSONL 引用注入，这些都是在做：
	•	状态锚定
	•	输入标准化
	•	避免幻觉性延续

所以你不需要照搬 PAUL 或 GSD。
你需要的是把你现有系统从“若干好招”提升成明确的状态机协议。

⸻

一版更具体的落地规则

下面是我会直接写进规范里的。

规则 1：Issue 是唯一真相源

任何 session 内新决策，若未写回 issue / reconcile block，不视为持久状态。

规则 2：完成的定义是 Reconcile 完成

没有结构化对账，任务不得标记 done。

规则 3：执行必须按 slice 进行

单个执行回合只允许服务一个上下文闭包。

规则 4：subagent 只能做 bounded task

不可让其拥有最终范围解释权、AC 解释权、架构决策权。

规则 5：每次执行启动必须重新注入状态

不得假设上个 session 的隐式上下文仍然可靠。

规则 6：AC 和 Boundaries 比计划步骤优先级更高

若步骤与 AC/Boundaries 冲突，以后者为准。

规则 7：边界冲突必须显式升级

若不突破边界就无法满足 AC，必须：
	•	记录冲突
	•	停止静默扩 scope
	•	生成新的 planning / approval 动作

规则 8：DONE_WITH_CONCERNS 不能直接流入 CLOSED

它只能流入：
	•	follow-up issue
	•	explicit waiver
	•	bounded acceptance by human decision

这一条很重要，否则“有顾虑但先关”会变成新的漂移源。

⸻

你最后那个问题，我的直接回答

你的 JSONL pre-fetch 模式是否应该在 /issue-implement 每次启动时强制重置 context，而非依赖连续 session 的累积？

是，应该。默认强制。

而且不只是“应该”，我认为这是你体系继续演化时最该写死的一条。

原因很简单：

连续 session 累积上下文，本质上是隐式状态

隐式状态有三个问题：
	•	不可审计
	•	不可精确重建
	•	会被模型的近期 token 分布污染

pre-fetch 注入是显式状态恢复

显式恢复的好处是：
	•	可复现
	•	可对账
	•	可控制版本
	•	可定位漂移来源

所以更稳的默认应该是：

/issue-implement 启动协议
	1.	拉取 issue 当前状态
	2.	拉取关联 MR / 文档 / 依赖 issue
	3.	注入最新结构化摘要（而不是历史整段对话）
	4.	注入 slice 边界、AC、open concerns
	5.	明确本轮只处理哪个 slice

这相当于把每次执行都变成：
从权威状态快照冷启动，而不是从聊天记忆热启动。

这比 PAUL 稳，也比 GSD 更适合长期项目。

⸻

我最终推荐的设计一句话

不要让 session 承担 continuity；让 issue 承担 continuity。不要让 agent 持有项目真相；让 reconcile artifact 持有项目真相。

这才是把 GSD 和 PAUL 的优点抽出来之后，最稳的工程化形态。

⸻

如果要再进一步，我会建议你下一步做什么

不是再取名字，而是直接补三份规范：
	1.	Issue 状态 schema
	2.	Slice 切分规则
	3.	Reconcile 写回模板

这三份一旦写出来，你的系统就会从“经验型工作流”升级为“可验证协议”。

你本来还应该继续追问的两个问题是：
	1.	Slice 的自动切分启发式应该怎么定义，才能既不过碎也不过粗？
	2.	Reconcile 写回 issue 时，哪些字段必须结构化，哪些允许自然语言，以免后续自动化失真？
