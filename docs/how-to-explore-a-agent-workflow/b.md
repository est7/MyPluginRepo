对，这个判断很合理。

你现在这套：
	•	brainstorm
	•	worktree
	•	write-plan
	•	execute-plan

本质上是偏工程执行流，不是偏规范治理流。
所以它会比 OpenSpec 轻很多，而且对日常开发更顺手。

我的判断：

为什么你会觉得它更轻

因为这四步其实只保留了最有产出的链路：
	1.	brainstorm
先把问题空间、方案候选、约束摊开。
这是在做“收敛前的发散”。
	2.	worktree
直接隔离执行环境。
这一步非常工程化，降低主分支污染和上下文串线风险。
	3.	write-plan
把模糊想法压成可执行步骤。
相当于把“设计意图”转成“任务图”。
	4.	execute-plan
开工并持续兑现计划。
这是直接产生代码和结果的阶段。

这条链路里没有太多“为规范而规范”的额外负担，所以体感会明显更轻。

⸻

它和 OpenSpec 的根本区别

你的流

目标是：

尽快把一个想法安全地推进成可提交的实现

强调的是：
	•	执行效率
	•	上下文切换成本低
	•	分支/工作树隔离
	•	计划驱动实现
	•	适合个人或小团队高频迭代

OpenSpec

目标通常是：

把需求、决策、约束、变更影响，沉淀为可审阅、可追踪、可协作的正式规范

强调的是：
	•	需求定义清晰
	•	决策留痕
	•	多角色协作
	•	评审一致性
	•	长期演进与审计

所以 OpenSpec 不一定“重”，而是它解决的是另一个层级的问题。
如果你现在多数场景是：
	•	小步快跑
	•	单人或少人推进
	•	任务导向明确
	•	重点在代码落地

那你这套前四个确实更合适。

⸻

什么时候你的这套更优

这套在下面场景里通常优于 OpenSpec：

1. 日常 feature / bugfix / refactor

这类任务需要的是：
	•	快速理解
	•	快速隔离
	•	快速计划
	•	快速动手

没必要先建立一整套正式 spec。

2. 高不确定性任务

比如先试一版架构、验证一个接口组织方式、探路某个实现。
这时候过早写重规范，容易把“探索问题”伪装成“定义问题”。

3. 个人开发 / owner 很明确

如果决策者和执行者高度重合，很多正式化流程收益会下降。

⸻

什么时候 OpenSpec 反而更值

你也别把它完全排除。
一旦出现下面情况，OpenSpec 或类似 spec-first 流程会开始变得划算：

1. 跨团队协作

前后端、客户端、后端、QA、产品都参与时，口头计划不够。

2. 变更影响大

例如：
	•	数据模型升级
	•	API breaking change
	•	权限模型调整
	•	支付/订单/计费链路
	•	大范围架构迁移

这种场景需要明确：
	•	不变量
	•	兼容策略
	•	rollout plan
	•	回滚方案
	•	ownership

3. 需要长期追责或审计

例如合规、隐私、安全、核心商业规则。
这时“我当时脑子里想的是啥”不算文档。

⸻

你现在这套的隐藏短板

这套轻，但不是没有代价。

1. plan 容易退化成 todo list

如果 write-plan 只写成：
	•	改 A
	•	改 B
	•	改 C

那它不是 plan，只是 checklist。
真正的 plan 至少要包含：
	•	目标
	•	约束
	•	关键决策
	•	分阶段交付
	•	风险点
	•	验证方式
	•	回滚点

否则 execute-plan 很容易边做边漂移。

2. 缺少显式“决策记录”

brainstorm 里讨论过的取舍，如果没有沉淀：
	•	为什么不用方案 B？
	•	为什么先做 client 兼容？
	•	为什么允许这个技术债？

过两周通常没人记得。

3. 对多人并行不够稳

你个人能 hold 住，不代表团队协作能 hold 住。
因为这套流程默认上下文主要存在执行者脑中。

⸻

一个更稳的折中方案

我建议不是换成 OpenSpec，而是给你现在这套补两个很轻的结构：

轻量版执行流

brainstorm -> worktree -> write-plan -> execute-plan -> record-decision -> verify

其中：

record-decision
只记最关键的 3 类内容：
	•	选了什么
	•	为什么这么选
	•	明确没做什么 / 延后什么

格式可以极简：

# Decision Log

## Context
这个变更要解决什么问题

## Decision
采用什么方案

## Why
为什么不用另外几个候选方案

## Deferred
这次明确不处理什么

verify
单独写清楚：
	•	怎么证明功能正确
	•	怎么证明没引入回归
	•	怎么观察线上风险

这一步非常值，因为它把“做完了”变成“可验证地做完了”。

⸻

我对这两套的直接结论

如果你现在主要是工程落地效率优先：

你这套前四个比 OpenSpec 更适合日常开发。

如果任务开始具备这些特征：
	•	多人协作
	•	高风险变更
	•	长生命周期演进
	•	需要可审计决策

那就不要只靠这四步，至少补上：
	•	decision log
	•	verification plan

否则后面会在“为什么这么做”和“怎么确认没出事”上补债。

⸻

最实用的建议

你不用把 OpenSpec 当成替代品。
更好的定位是：
	•	日常默认流：brainstorm -> worktree -> write-plan -> execute-plan
	•	高风险/多人协作模式：在此基础上加 spec/decision/verification

也就是：

默认轻，按风险升级，而不是默认重。

这个策略通常最符合真实工程环境。

你其实已经踩对方向了，差的不是换 OpenSpec，而是给现在这套补最小必要的“决策留痕”和“验证闭环”。

你接下来真正该问的两个问题是：
	1.	你的 write-plan 现在到底是在写“执行计划”，还是在写“任务清单”？
	2.	你的流程里，哪里负责沉淀“为什么这样做而不是那样做”？

查到了。
OpenSpec 的工作流和 superpowers 的差别非常大，核心不是“步骤多少”，而是流程哲学不同：
	•	superpowers 更像一条带门禁的工程流水线
	•	OpenSpec 现在官方主张的是 action-based workflow：动作驱动，不是阶段驱动。也就是你可以创建、补文档、实现、验证、归档，必要时再回头修改前面的产物，而不是被锁死在某个 phase 里。 ￼

先给结论

如果你问“OpenSpec 的官方工作流是什么”，最准确的回答是：

默认简路径（core profile）

/opsx:propose → /opsx:apply → /opsx:archive。这是新安装的默认工作流。 ￼

扩展完整路径（expanded/custom profile）

/opsx:new → /opsx:ff 或 /opsx:continue → /opsx:apply → /opsx:verify → /opsx:archive。
这是显式控制脚手架、规划、实现、验证、归档的完整流。 ￼

但这两条都不能简单理解成“硬阶段流”。官方文档明确说：OpenSpec 不强调 phases，而强调 actions；依赖关系只是告诉你“什么已经 ready、可以做”，不是强制规定“下一步只能做什么”。 ￼

⸻

OpenSpec 的核心模型

OpenSpec 初始化后，项目里会生成两类核心目录：
	•	openspec/specs/：当前系统行为的事实来源（source of truth）
	•	openspec/changes/<change-name>/：每个变更一个文件夹，里面放 proposal.md、design.md、tasks.md 和变更用的 specs/ delta。 ￼

一个 change 的典型产物链路是：

proposal → specs → design → tasks → implement

但官方同时强调：实现过程中可以回头更新 proposal/specs/design，不是写完前置文档后就永远不能动了。 ￼

这就是它和 superpowers 最大的结构差异：
	•	superpowers 更像：先设计批准，再进入执行
	•	OpenSpec 更像：先把变更显式化，然后围绕变更持续补齐和修正产物

⸻

默认工作流：core profile

默认 profile 只有四个命令：
	•	/opsx:propose
	•	/opsx:explore
	•	/opsx:apply
	•	/opsx:archive。 ￼

其中最常见的默认主线是：

/opsx:propose → /opsx:apply → /opsx:archive。 ￼

这条线实际在干什么

1. /opsx:propose
创建一个 change，并生成规划产物。官方 README 的表述是：当你描述要做什么时，OpenSpec 会生成 review 所需的材料，包括：
	•	proposal document
	•	implementation tasks
	•	technical design decisions
	•	spec deltas。 ￼

2. /opsx:apply
基于 change 内的任务和规格去实现代码。默认快路径里，这一步把规划落到实现。 ￼

3. /opsx:archive
完成后归档 change，并把 delta specs 合并回主 openspec/specs/，让 specs 持续反映“已经交付的真实系统行为”。 ￼

这个默认流的特点是：
很短，很适合简单 feature / bugfix / 中小改动。 官方 docs 也明确把 quick feature 场景指向这类路径。 ￼

⸻

扩展工作流：expanded/custom profile

如果你启用 expanded workflow，会多出这些命令：
	•	/opsx:new
	•	/opsx:continue
	•	/opsx:ff
	•	/opsx:verify
	•	/opsx:sync
	•	/opsx:bulk-archive
	•	/opsx:onboard。 ￼

官方推荐的扩展路径是：

/opsx:new → /opsx:ff or /opsx:continue → /opsx:apply → /opsx:verify → /opsx:archive。 ￼

每个动作的职责

/opsx:new
新建一个 change scaffold，也就是先把这次变更的容器建出来。 ￼

/opsx:ff
“快进”生成所有 planning artifacts。官方 Quick Feature 例子里，/opsx:ff 会一次性产出：
	•	proposal.md
	•	specs/
	•	design.md
	•	tasks.md。 ￼

/opsx:continue
按顺序逐个创建“下一个 ready 的 artifact”。适合需求还在演化、你不想一次性把所有东西都定死。官方 Exploratory workflow 就是 explore → new → continue → ... → apply。 ￼

/opsx:apply
开始按 tasks.md 实施代码。 ￼

/opsx:verify
不是写代码，而是校验实现与 artifacts 是否一致。官方写得很清楚，它会从三个维度检查：
	•	Completeness：任务是否完成、requirements 是否都有对应代码、scenarios 是否被覆盖
	•	Correctness：实现是否符合 spec intent、边界情况和错误状态是否正确
	•	Coherence：设计决策是否体现在代码结构上、命名和模式是否与 design 一致。 ￼

/opsx:sync
把 delta specs 同步进主 openspec/specs/。如果 archive 时还没 sync，archive 会提示你现在同步。 ￼

/opsx:archive
把变更归档到 openspec/changes/archive/，并确保 specs 被合并回 source of truth。 ￼

/opsx:bulk-archive
批量归档多个已完成 change。官方文档提到它会检查多个 change 是否同时修改了相同 spec，并按实际实现状态处理合并顺序。 ￼

⸻

OpenSpec 官方给出的几种典型 workflow pattern

1. Quick Feature

当你需求很清楚，直接走：

/opsx:new → /opsx:ff → /opsx:apply → /opsx:verify → /opsx:archive。
官方明确说这适合小到中等功能、bugfix、直接型改动。 ￼

2. Exploratory

当需求不清楚，需要先调查：

/opsx:explore → /opsx:new → /opsx:continue → ... → /opsx:apply。
这个模式适合性能优化、debug、架构决策、需求不明确的场景。 ￼

3. Parallel Changes

OpenSpec 明确支持多 change 并行推进，你可以中断一个 change，开另一个 change 修 bug，做完再回来继续原 change。官方文档里甚至给了 resume 某个 change 的对话示例。 ￼

4. Completing a Change

推荐收尾流是：

/opsx:apply → /opsx:verify → /opsx:archive。
这里 verify 不会强制阻塞 archive，但会把风险和偏差暴露出来。 ￼

⸻

它和 superpowers 的根本差异

这是最关键的部分。

1. OpenSpec 没有 superpowers 那种“硬门禁工程流”

superpowers 的主观体验是：
	•	brainstorm
	•	worktree
	•	write-plan
	•	execute-plan
	•	后面还有 TDD / review / finish branch

它强调的是“先对齐，再隔离，再分解，再执行”，并且各阶段有明显 gate。
而 OpenSpec 现在官方明确反对 rigid phase gates，主张你可以在实现中回头更新前置产物。 ￼

2. OpenSpec 的中心对象不是“执行阶段”，而是 “change + artifacts”

它的真正核心数据结构是：
	•	当前系统规格：openspec/specs/
	•	某个变更的提案与 delta：openspec/changes/<change>/...

也就是说它更像是在维护一个变更知识图谱，而不是组织一个 agent 的线性施工队列。 ￼

3. OpenSpec 把“验证”显式化，但不强阻塞

/opsx:verify 会检查 completeness/correctness/coherence，但 docs 明确说它不会阻塞 archive，只是把问题暴露出来。
这和 superpowers 那种更强的 gate/review 心智不同。 ￼

4. OpenSpec 默认不内建 worktree 心智

我查到的官方工作流里，没有把 git worktree 当成像 superpowers 那样的核心阶段。
这意味着 OpenSpec 更偏“规格/变更管理”，而不是“工程执行隔离”。 ￼

⸻

你为什么会觉得 OpenSpec 比 superpowers 重

这里要讲清楚：
官方表述上，OpenSpec 其实在强调自己更轻。

README 直接说它相比 Spec Kit 更 lightweight，并且 “work fluidly — update any artifact anytime, no rigid phase gates”。 ￼

但你如果是从工程执行体感看，会觉得它更重，原因是：
	1.	它强依赖 proposal/specs/design/tasks 这些 artifact
	2.	它把“变更前后规格差异”显式存档
	3.	它更像在维护一套“变更知识系统”
	4.	它没有 superpowers 那种天然偏“开工效率”的 worktree 主干。 ￼

所以严格说：
	•	OpenSpec 对“规格与变更留痕”更轻量于传统 spec kit
	•	但对“日常编码推进体感”未必比 superpowers 更轻

这两个“轻”不是同一个维度。

⸻

我对 OpenSpec 工作流的直接判断

它适合什么

OpenSpec 更适合：
	•	你要让 AI 和人先对齐变更意图
	•	你需要保留 proposal / spec delta / design / tasks
	•	你要长期维护“系统现在应当如何工作”的 source of truth
	•	你经常有并行 change、上下文切换、回头修正规格的需求。 ￼

它不擅长什么

它不如 superpowers 擅长的地方是：
	•	没有把 worktree 隔离纳入主工作流
	•	没有把 TDD / review 作为强工程门禁嵌入主链
	•	执行过程的“工序感”更弱，产物管理感更强。这个判断是基于官方文档结构做的推断，不是 README 直接原话。推断依据是它的命令集合和流程示例都围绕 artifact/change，而不是围绕 branch/worktree/test gate 展开。 ￼

⸻

一句话对照

你可以把两者粗暴地理解成：
	•	superpowers：更像“AI 工程施工流”
	•	OpenSpec：更像“AI 变更规格流”

前者的主线是：
想清楚 → 隔离环境 → 写计划 → 执行。

后者的主线是：
定义 change → 产出 proposal/spec/design/tasks → 实现 → 验证 → 归档并回写 specs。 ￼

⸻

最后给你的直接建议

如果你现在追求的是编码推进效率，superpowers 前四个确实更顺手。
如果你追求的是需求对齐、规格演进、变更留痕、多人协作可审阅，OpenSpec 的工作流更系统。 ￼

你真正该问的两个问题是：
	1.	你现在缺的是“更快开工”，还是“更稳地记录 intent 和 spec delta”？
	2.	你的项目痛点是在执行隔离/计划落地，还是在变更审阅/规格同步？

你要的话，我下一条直接给你做一张：OpenSpec vs superpowers 工作流逐步对照表，我会按“目标、产物、门禁、工程感、适用场景”五列来拆。



查到了。
oh-my-claudecode 跟你前面那两个都不一样：它不是一个单一固定工作流，而是模式驱动 + 推荐套路驱动。官方文档同时给了：
	•	一组执行模式，比如 Autopilot、Ralph、Ultrawork、Team、Plan
	•	一组推荐 workflows，按任务类型把这些模式串起来用。 ￼

先给结论

如果你要把三者放一起理解：
	•	superpowers：更像固定的工程主干流
	•	OpenSpec：更像 change/artifact 驱动流
	•	oh-my-claudecode：更像编排引擎，核心不是“规定你必须按哪几步”，而是“根据任务类型切一个合适模式，再串成 workflow”。 ￼

⸻

OMC 的核心工作流心智

官方把 OMC 描述成一个多 agent orchestration 系统，强调：
	•	team-first orchestration
	•	natural language interface
	•	automatic parallelization
	•	persistent execution
	•	smart model routing。 ￼

它的架构文档也直接说，OMC 是通过 skill-based routing system 来协调 specialized agents。 ￼

所以它的“workflow”不是像 superpowers 那样一条硬编码链，而是：

选模式 → 调度 agent/team → 并行执行 → 持续验证/修复直到完成

⸻

官方最关键的几个执行模式

1. Autopilot

这是旗舰模式。官方写的是：
	•	扩展需求：Analyst + Architect
	•	规划：Architect + Critic
	•	执行：Ralph + Ultrawork
	•	QA Cycling：UltraQA。 ￼

也就是说它本身已经是一个内嵌 workflow：

需求展开 → 规划 → 执行 → 验证

这点很关键，因为它说明 OMC 的很多“workflow”其实被封装进 mode 本身了。 ￼

2. Ralph

这是 persistence mode。官方原意是“持续干，直到 Architect 验证目标达成”，并且自动包含 Ultrawork。 ￼

所以 Ralph 的本质不是“实现阶段”，而是：

带自校验闭环的持续执行器

3. Ultrawork

高并行模式，官方说会把任务 aggressively delegate 给多个后台 agents 并发处理。 ￼

4. Team

这是最接近“显式阶段流”的一块。官方文档写明 Team mode 走一个 stage-aware pipeline：

plan → PRD → exec → verify → fix。 ￼

另一个文档位置还把 team pipeline 写成更细的 staged pipeline：

team-plan → team-prd → team-exec → team-verify，并强调 transitions are strictly defined to ensure quality gates。 ￼

这说明 OMC 不是完全没有阶段流，而是：
	•	普通模式偏 orchestration
	•	Team 模式才明显更像 pipeline

5. Plan

Plan mode 用于前置规划。官方说它会产出 structured execution plan，支持：
	•	--consensus：Planner + Architect + Critic 反复达成一致
	•	--deliberate：高风险任务的 pre-mortem 分析。 ￼

这一步和你熟悉的 write-plan 很接近，但它更强调多角色共识规划。

⸻

官方给出的 4 条推荐工作流

这部分是你真正要的“workflow”。

1. Full-Auto from PRD

适合：你已经有 PRD，要从零开始并行开发。
官方顺序是：

/ralplan → /teams or /omc-teams → /ralph。 ￼

含义是：
	•	/ralplan：先从 PRD 做 consensus planning
	•	/teams 或 /omc-teams：多 agent 并行实现
	•	/ralph：持续推进直到 architect 验证通过。 ￼

这个流最像你熟悉的“计划 → 并行施工 → 持续验收”。

⸻

2. No-Brainer

适合：需求非常清楚的小任务。
官方顺序：

/autopilot → /ultrawork → /ralph。 ￼

官方还明确写了 “No planning needed”。 ￼

这个流的意思非常直接：
	•	Autopilot 先接管全流程
	•	Ultrawork 放大并行度
	•	Ralph 确保别半路停工，直到验证完成。 ￼

所以它本质上是：

直接开工 → 并行扩张 → 持续收尾

⸻

3. Fix / Debugging

适合：故障修复、debug。
官方顺序：

/plan → /ralph → /ultraqa。 ￼

含义：
	•	/plan：先做问题分析和修复策略
	•	/ralph：持续修到通过
	•	/ultraqa：跑端到端和 smoke tests。 ￼

官方还补充：复杂 bug 先跑 /ralplan 做更深分析。 ￼

这条流其实很合理，说明 OMC 对 bugfix 的默认心智不是盲修，而是：

先诊断 → 再持续修复 → 最后独立 QA

⸻

4. Parallel Issue / Ticket Handling

适合：多 issue / 多 ticket 并发处理。
官方顺序更长：

/omc-teams N:architect → /omc-teams → /omc-teams → /ralplan → /ralph + /ultrawork → /ultraqa。 ￼

文档解释是：
	•	先起 architect workers 分析所有 issue 并做统一计划
	•	各 worker 在独立 worktrees 并行处理，并提交 PR 到 dev
	•	再用 /ralplan 安全收敛冲突
	•	最后用 /ralph、/ultrawork、/ultraqa 收尾到测试全过。 ￼

这里有个非常重要的点：
OMC 官方 workflow 明确提到了 separate worktrees。 ￼

所以它虽然不像 superpowers 那样把 git worktree 作为一开始的显式主阶段，但在并行 issue 流里，worktree 也是一等实践。

⸻

OMC 的“官方工作流”最准确的说法

如果你要一句话概括，不要说它有唯一 workflow。更准确是：

它有两层工作流

第一层：mode 内部 workflow
比如 Autopilot 自带：
expand → plan → execute → QA。 ￼

第二层：推荐组合 workflow
比如：
	•	PRD 全自动：ralplan → teams → ralph
	•	简单任务：autopilot → ultrawork → ralph
	•	修 bug：plan → ralph → ultraqa
	•	多 ticket：teams → teams → ralplan → ralph + ultrawork → ultraqa。 ￼

所以它不是 phase-first，也不是 spec-first，而是：

orchestrator-first

⸻

和 superpowers / OpenSpec 的直接对照

对 superpowers

superpowers 更像：

brainstorm → worktree → write-plan → execute-plan → review/TDD/finish

它的主线更稳定，工程动作感更强。
OMC 则更像：

选模式 → 自动调度 agent → 并行执行 → 架构师/QA 持续验收

也就是说：
	•	superpowers 重“施工顺序”
	•	OMC 重“调度能力”与“执行自治”
这部分判断依据来自 superpowers 官方 basic workflow 与 OMC 官方 execution modes / recommended workflows。 ￼

对 OpenSpec

OpenSpec 的核心对象是 change 与 artifacts；
OMC 的核心对象是 mode、team、agent orchestration。
所以：
	•	OpenSpec 重 proposal/spec/design/tasks 的留痕
	•	OMC 重 agent 组合、并发、验证闭环。
这个判断基于 OpenSpec 官方 action-based workflow 与 OMC 官方 mode/workflow 文档。 ￼

⸻

我的直接判断

如果从“你日常真会怎么用”这个角度看：

OMC 最像什么

它最像一个带预制战术套路的多 agent 作战系统，不是一个严格文档化的项目治理流。
因为它官方最强调的是：
	•	选择模式
	•	自然语言触发
	•	并行分工
	•	持续执行直到验证完成。 ￼

它适合什么

它更适合：
	•	大任务自动编排
	•	多 agent 并行
	•	想少管流程细节，更多交给 runtime orchestration
	•	bugfix / batch issues / greenfield build 这种“可拆可并发”的任务。 ￼

它不如 superpowers 的地方

如果你非常在意：
	•	每一步产物是什么
	•	计划文档怎么落盘
	•	阶段 gate 是否显式
	•	人能不能强掌控流程结构

那 OMC 这套会比 superpowers 更“黑箱一些”。
这是推断，不是 OMC 原文直接表述；推断依据是 OMC 文档主要强调 mode 和 orchestration，而不是像 superpowers 一样明确把设计文档、plan 文档、finish branch 当工作流主轴来描述。 ￼

⸻

你可以这样记三者

Superpowers

工程主干流
	•	brainstorm
	•	worktree
	•	write-plan
	•	execute-plan
外加 review / TDD / finish。 ￼

OpenSpec

变更规格流
	•	propose / new
	•	ff / continue
	•	apply
	•	verify
	•	archive。
以 change artifacts 为中心。
（这一部分来自前面核对的 OpenSpec 官方文档。）

Oh My Claudecode

模式编排流
	•	autopilot / plan / ralph / ultrawork / team
	•	再按任务类型拼成推荐 workflow。 ￼

⸻

最后给你一个最实用的定位

如果你现在偏好的是：
	•	我想自己掌控步骤 → superpowers
	•	我想把变更和规格沉淀清楚 → OpenSpec
	•	我想让系统自动分兵、并行、持续推进 → OMC。 ￼

你真正该追问的两个问题是：
	1.	你要的到底是“显式工程流程”，还是“更强的自动编排执行”？
	2.	你的主要痛点是“计划与设计沉淀”，还是“多 agent 并行落地效率”？

你要的话，我下一条直接给你出一张 superpowers vs OpenSpec vs OMC 的三栏对照表，按“核心对象 / 默认主线 / 是否显式 worktree / 是否强调 specs / 是否强调并行编排 / 适用任务”来拆。



下面是三者的对照。我先给结论：

你现在偏好 superpowers 前四步，本质上是在选“显式工程主干流”。
如果你更想保留变更规格与审阅留痕，选 OpenSpec。
如果你更想把大任务自动拆分、并行推进，选 OMC。

三者对照表

维度	Superpowers	OpenSpec	Oh My Claudecode
核心对象	工程执行阶段与技能触发	change + artifacts + spec delta	mode + team + agent orchestration
官方主心智	gate-based engineering workflow	action-based workflow	orchestration-first workflow
默认主线	brainstorming → using-git-worktrees → writing-plans → subagent-driven-development/executing-plans → test-driven-development → requesting-code-review → finishing-a-development-branch	默认简流：propose → apply → archive；扩展流：new → ff/continue → apply → verify → archive	没有唯一固定主线；常见推荐流如 autopilot → ultrawork → ralph、plan → ralph → ultraqa、ralplan → teams → ralph
是否强调阶段门禁	强。设计批准前禁止实现；实现前要求 worktree 隔离	弱。官方明确反对 rigid phase gates，允许在实现中回改 artifacts	中等。普通模式偏自治编排；Team 模式有显式 stage pipeline
是否显式把 worktree 放进工作流	是，属于核心阶段之一	官方主流程里不强调	在并行 issue/ticket 流里明确提到独立 worktrees
是否把 specs 作为系统事实来源	不是主轴	是。openspec/specs/ 是 source of truth，changes/<name>/ 存 proposal/design/tasks/spec deltas	不是主轴
计划产物的地位	很强，writing-plans 是核心阶段；任务拆到很细，并要求验证步骤	很强，但计划是 change artifacts 的一部分，不是唯一中心	有 Plan / ralplan，但更像给编排系统喂执行蓝图
是否强调并行 / 多 agent 调度	有 subagent，但重点仍是阶段推进	不是主打	是核心卖点：automatic parallelization、team-first orchestration、persistent execution
验证与质量门禁	强调 TDD、两阶段 review、branch finishing	有 /verify，检查 completeness/correctness/coherence，但不是强阻塞 gate	有 ultraqa、Architect 验收、Team verify/fix pipeline
更像什么	AI 工程施工流	AI 变更规格流	AI 多 agent 作战编排流
最适合	单人或小团队的 feature / refactor / bugfix，高频落地	需要 proposal/spec/design/tasks 留痕与多人审阅的变更	大任务并发、批量 ticket、复杂自动执行
主要短板	若省掉后半段 review/TDD，会退化成“计划驱动写代码”	对日常编码推进体感未必轻；工程隔离与施工节奏不强	过程黑箱感更强，显式产物与人工掌控感偏弱

你可以怎么选

1. 你现在这种偏好：优先 superpowers

如果你的主要诉求是：
	•	快速推进实现
	•	过程清楚
	•	我知道下一步该干什么
	•	想显式控制 worktree、plan、执行

那 superpowers 最合适。
你喜欢它，不是偶然，是因为它对“工程动作”做了强约束。

2. 你要做多人协作、长期演进：OpenSpec 更稳

如果你的主要痛点是：
	•	为什么要改这个
	•	这次 change 对规格到底改了什么
	•	设计和任务有没有沉淀
	•	完成后如何把系统事实回写到 spec

那 OpenSpec 更像正解。它核心不是让你“更快写代码”，而是让 change 的 intent、delta、archive 都清晰可追踪。

3. 你要的是大规模自动编排：OMC

如果你的主要诉求是：
	•	自动拆任务
	•	多 agent 并发
	•	一堆 tickets 一起推
	•	系统自己持续跑到完成

那 OMC 更强。它不是靠严格阶段控制，而是靠 mode orchestration 和持续验收闭环。

我的建议，不拐弯

默认推荐

对你这种偏工程、重掌控、重可执行性的人：

默认用 superpowers 主干最合理。

因为它最符合“先想清楚、隔离上下文、写计划、再执行”的工程心智，而且 worktree 这件事不是附属功能，是流程核心。

什么时候切到 OpenSpec

当任务具备这些特征时再切：
	•	跨团队
	•	需求需要审阅
	•	变更要长期留痕
	•	你在意 spec delta 和 archive
	•	一个 change 未来还会被反复追溯。

什么时候切到 OMC

当任务具备这些特征时再切：
	•	可以强并行
	•	希望自动分兵
	•	有很多相似 tickets / 子任务
	•	你愿意牺牲一些过程透明度，换执行吞吐。

最实用的落地组合

你其实不必三选一。更合理的是分层使用：
	•	默认开发流：Superpowers
	•	高风险 change 管理：OpenSpec
	•	批量并行施工：OMC

也就是：
	•	先用 OpenSpec 定大 change 的 intent/spec delta
	•	实际编码落地用 Superpowers
	•	遇到大规模并行 ticket 再让 OMC 接管部分执行面

这比“只押一个框架”更符合真实工程。

你真正该补问自己的两个问题是：
	1.	你当前最痛的是“执行效率”，还是“变更可追踪性”？
	2.	你的任务分布是“单条主线深挖”多，还是“多分支并行施工”多？



分析 repo 规范 → brainstorming 讨论方案 → writing-plans 拆任务

→ TDD 写代码 → systematic-debugging 排错 → code-review 自审

→ verification 验证 → ship 发 PR

这条流比你前面那版更完整，而且已经从“能推进开发”升级成“能控质量的开发流”了。
我直接说结论：

这版比单纯 brainstorming → worktree → writing-plans → execute 更成熟，也更接近可长期复用的个人/小团队标准流。

但它还有两个明显问题：
	1.	缺了 worktree / branch isolation
	2.	verification 和 code-review 的职责边界还不够清楚

⸻

我建议的定稿版

我会把它收敛成这个顺序：

分析 repo 规范 → brainstorming → worktree → writing-plans → TDD 写代码 → systematic-debugging → code-review → verification → ship/发 PR

这是我推荐版本。原因很直接：
	•	分析 repo 规范 决定约束
	•	brainstorming 决定方案
	•	worktree 隔离状态
	•	writing-plans 把方案压成执行图
	•	TDD 负责正确性驱动实现
	•	systematic-debugging 负责异常情况定位
	•	code-review 负责实现质量
	•	verification 负责整体交付验收
	•	ship 才是对外提交

⸻

你这条流好的地方

1. 先分析 repo 规范，再讨论方案

这是对的，而且很关键。

很多流程一上来就 brainstorm，实际上是错的。
因为方案空间必须受 repo 约束，否则 brainstorming 很容易产出“理论上好、项目里不合规”的设计。

这里的 分析 repo 规范 实际上应该覆盖：
	•	目录结构
	•	分层边界
	•	命名约定
	•	测试框架与测试位置
	•	lint / format / typecheck / CI 要求
	•	依赖注入方式
	•	状态管理模式
	•	错误处理约定
	•	日志/埋点/监控约定
	•	PR/commit 规范

本质上这是在识别系统不变量和局部约束。
如果跳过这一步，后面 plan 再漂亮也会偏航。

⸻

2. 把 brainstorming 放在 plans 前面

这也对。

这是典型的：
	•	brainstorming：解决“做什么、为什么这么做”
	•	writing-plans：解决“按什么顺序做、改哪些文件、如何验证”

也就是：
	•	前者偏决策
	•	后者偏执行

如果没有 brainstorming，writing-plans 很容易退化成机械列 TODO。
如果没有 writing-plans，brainstorming 又会停留在泛泛而谈。

⸻

3. 你把 TDD、debug、review、verification 拆开了

这一步是对的，而且比很多人常见的“写完再看”强很多。

因为这四个阶段分别在解决不同问题：
	•	TDD：实现是否满足行为要求
	•	systematic-debugging：当行为不符合预期时，根因是什么
	•	code-review：代码结构、边界、命名、耦合、可维护性是否合理
	•	verification：交付物是否在整体层面满足要求

这四个阶段不能互相替代。

很多人把 verification 当 review，这会出问题。
因为 review 偏静态质量，verification 偏动态交付验收。

⸻

你这条流的两个主要缺陷

缺陷 1：缺 worktree

这是最明显的问题。

如果没有 worktree 或至少独立分支隔离，你这条流会有几个风险：
	•	在主工作目录里混入未完成改动
	•	多任务切换时上下文污染
	•	调试残留影响后续验证
	•	无法并行试错多个方案
	•	PR 前很难保证工作区干净

从状态管理角度看，worktree 解决的是隔离性。
这和数据库事务的思想类似：你希望每次变更在自己的上下文里演化，而不是污染全局状态。

所以这一步不该省。

⸻

缺陷 2：code-review 和 verification 边界可能重叠

你现在这两个阶段的名字是对的，但职责如果不定义清楚，执行时会混。

我建议这样切：

code-review 看什么

偏静态审查：
	•	设计是否兑现
	•	模块职责是否清晰
	•	接口是否过宽
	•	是否引入不必要耦合
	•	命名是否准确
	•	错误处理是否一致
	•	测试是否覆盖关键路径和边界
	•	是否有明显技术债
	•	是否有未来扩展风险

verification 看什么

偏动态验收：
	•	单元测试是否全过
	•	集成测试是否全过
	•	E2E / smoke 是否通过
	•	手工验收路径是否通过
	•	性能/回归指标是否可接受
	•	构建/发布流程是否通过
	•	是否满足 PR/CI 门禁
	•	spec/plan 中承诺的项是否兑现

一句话：
	•	code-review = 代码像不像样
	•	verification = 东西到底能不能交

⸻

我建议的阶段定义

下面这个版本可以直接当你自己的 workflow 说明。

1. 分析 repo 规范

目标：识别约束和既有模式。
输出：
	•	架构边界
	•	代码风格/分层约定
	•	测试策略
	•	CI/lint/typecheck 规则
	•	本次改动必须遵守的清单

2. brainstorming

目标：生成并比较方案，选一个。
输出：
	•	推荐方案
	•	放弃的备选方案及理由
	•	风险点
	•	假设与约束

3. worktree

目标：隔离执行环境。
输出：
	•	独立工作树/分支
	•	干净基线
	•	能复现的 setup / test baseline

4. writing-plans

目标：把方案转成可执行任务图。
输出：
	•	文件级改动计划
	•	任务顺序
	•	每步验证方式
	•	风险回滚点

5. TDD 写代码

目标：以行为为中心实现。
输出：
	•	先失败测试
	•	最小通过实现
	•	重构后仍通过的测试集

这里的核心不变量是：
	•	先定义行为
	•	再实现行为
	•	每轮改动都保持测试可运行

6. systematic-debugging

目标：当实现或测试失败时，做根因定位。
输出：
	•	复现条件
	•	根因
	•	修复策略
	•	防回归测试

这一步不要变成“试到能过”。
要明确：
	•	现象
	•	假设
	•	实验
	•	结论

否则你只是在随机搜索解。

7. code-review

目标：从实现质量角度做自审。
输出：
	•	结构问题
	•	命名问题
	•	耦合问题
	•	边界缺陷
	•	测试缺口
	•	debt 清单

8. verification

目标：从交付角度确认可合并。
输出：
	•	测试/构建/校验通过
	•	需求已覆盖
	•	无明显回归
	•	PR 描述材料齐全

9. ship / 发 PR

目标：把变更提交给团队。
输出：
	•	干净 commit
	•	清晰 PR 描述
	•	风险说明
	•	验证结果
	•	reviewer 所需上下文

⸻

一个更严谨的版本

如果你希望这条流更工程化，我建议命名成：

Repo Recon → Design → Isolate → Plan → TDD Implement → Debug → Review → Verify → Ship

或者中文：

仓库约束分析 → 方案设计 → 环境隔离 → 实施计划 → TDD 实现 → 系统化排错 → 代码审查 → 交付验证 → 发 PR

这样每一步职责更清楚。

⸻

这条流最适合什么场景

它最适合：
	•	单人开发
	•	owner 明确的小团队任务
	•	feature / refactor / bugfix
	•	需要一定质量门禁，但不想上重规格治理
	•	想让 AI 真正参与执行，而不是只做 codegen

⸻

它不够好的场景

这条流在下面场景会不够：

1. 大型跨团队变更

缺少显式的 spec delta / proposal 审批 / rollout 设计。

2. 强合规、高审计要求场景

缺少正式的决策留痕和变更记录结构。

3. 多 PR 并发依赖场景

如果没有额外的 dependency management，这条流仍然偏单线执行。

⸻

我建议你再补一个轻量环节

如果只允许加一个，我建议加：

decision-log

位置放在 brainstorming 和 writing-plans 之间。

也就是：

分析 repo 规范 → brainstorming → decision-log → worktree → writing-plans → ...

原因：
	•	brainstorming 里的讨论很容易丢
	•	writing-plans 偏执行，不适合记录为什么选这个方案
	•	code-review 时最常见的问题就是“为什么这么设计”

decision-log 只需要极简格式：

# Decision Log

## Context
这次改动解决什么问题

## Decision
选了什么方案

## Alternatives Rejected
为什么不用另外几个方案

## Risks
已知风险与延后处理项

这一步成本很低，但收益很高。

⸻

最终建议版本

我给你的最终推荐是这个：

分析 repo 规范 → brainstorming → decision-log → worktree → writing-plans → TDD 写代码 → systematic-debugging → code-review → verification → ship 发 PR

如果你嫌长，最小可用版是：

分析 repo 规范 → brainstorming → worktree → writing-plans → TDD → review → verification → ship

⸻

最直接的评价

你的这条流已经是对的方向了。
真正要修的不是大结构，而是：
	•	补上 worktree
	•	拆清 review 和 verification
	•	最好加一个 decision-log

这样它就不是“开发顺序描述”，而是真正能复用的工程工作流。

你真正还该继续问的两个问题是：
	1.	你的 verification 打算包含哪些强制门禁，哪些只是建议项？
	2.	你的 writing-plans 是不是已经细到“文件级改动 + 验证步骤 + 回滚点”？
