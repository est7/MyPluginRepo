# 执行层与治理层：Agent 工作流框架横向对比

## 三个框架的定位

在 AI 辅助工程领域，Superpowers、OpenSpec 和 Oh My Claudecode 三个框架各自解决的是不同层级的问题，理解它们的根本定位差异，是选型的前提。

Superpowers 本质上是一条**工程主干流**，它的主线是 `brainstorming → worktree → writing-plans → executing-plans`，后续还有 `test-driven-development → requesting-code-review → finishing-a-development-branch`。它强调的是"先对齐、再隔离、再分解、再执行"，各阶段之间有明显的 gate 约束。它最突出的设计决定是把 git worktree 作为核心阶段之一，用环境隔离来保障上下文不串线。它更像一支带工序感的施工队：每一步做什么、能拿出什么产物，都有显式规定。

OpenSpec 的定位是**变更规格流**，它的核心数据结构不是"执行阶段"，而是 `change + artifacts + spec delta`。项目初始化后，它会在仓库中生成 `openspec/specs/`（系统行为的事实来源）和 `openspec/changes/<change-name>/`（每个变更的 proposal、design、tasks 和 spec delta）。官方明确反对 rigid phase gates，主张你可以在实现过程中回头更新前置产物——这和 Superpowers 的门禁心智有根本区别。它的默认简路径是 `/opsx:propose → /opsx:apply → /opsx:archive`，扩展完整路径是 `/opsx:new → /opsx:ff or /opsx:continue → /opsx:apply → /opsx:verify → /opsx:archive`。

Oh My Claudecode（OMC）的定位是**模式编排流**，它不是一条固定的工程流水线，而是一个 orchestration-first 的多 agent 调度系统。官方把它描述为具备 team-first orchestration、automatic parallelization、persistent execution 和 smart model routing 的编排引擎。它的工作流有两个层级：mode 内部已经封装了子流程（比如 Autopilot 自带 expand → plan → execute → QA），而推荐的 workflow 则是把不同 mode 串起来使用。它没有唯一的固定主线，而是根据任务类型切换组合策略。

## 关键设计差异

三者在设计哲学上的分歧集中在以下几个维度。

**阶段门禁的强度。** Superpowers 的 gate 是强约束：设计批准前禁止进入实现阶段，worktree 隔离是显式必须执行的步骤。OpenSpec 官方明确反对这种刚性门禁，它允许 artifact 在实现过程中被回溯修改，强调 action-based 而不是 phase-based。OMC 居中，普通模式偏自治编排，但 Team 模式有显式的 stage pipeline：`team-plan → team-prd → team-exec → team-verify`，文档里说"transitions are strictly defined to ensure quality gates"。

**核心对象的不同。** Superpowers 的核心对象是执行阶段与技能触发；OpenSpec 的核心对象是 change 与 artifacts，它更像在维护一个变更知识图谱，而不是组织一个线性施工队列；OMC 的核心对象是 mode、team 和 agent orchestration，它调度的是 agent 之间的协作关系。

**worktree 的地位。** Superpowers 把 git worktree 作为工作流核心阶段，这一步不是可选项。OpenSpec 的官方主流程里不强调 worktree 隔离，它更偏规格与变更管理，而不是工程执行隔离。OMC 在并行 issue/ticket 流里会明确提到 separate worktrees，但它不像 Superpowers 那样把它作为初始显式阶段。

**验证机制的差异。** Superpowers 强调 TDD、两阶段 review 和 branch finishing，质量门禁是内嵌在工程主干里的强约束。OpenSpec 的 `/opsx:verify` 会从 Completeness（任务完成度、需求覆盖）、Correctness（是否符合 spec intent）、Coherence（设计决策是否体现在代码结构上）三个维度校验，但官方文档明确说它不会阻塞 archive，只是把问题暴露出来，属于软约束。OMC 有 ultraqa、Architect 验收和 Team 的 verify/fix pipeline，验证是持续闭环而不是单次 gate。

**并行能力的差异。** Superpowers 支持 subagent，但重点仍在阶段推进，偏单线执行。OpenSpec 明确支持多 change 并行推进，可以中断一个 change、处理另一个后再回来，但它不是靠 agent 并发来实现的。OMC 的并行能力是核心卖点，automatic parallelization 是它的基础能力，Ultrawork 模式会把任务 aggressively delegate 给多个后台 agent 并发处理。

**计划产物的形态。** Superpowers 的 writing-plans 是核心阶段，产出的计划必须包含目标、约束、关键决策、分阶段交付、风险点、验证方式和回滚点，是有强结构要求的执行图。OpenSpec 的计划（tasks.md）是 change artifacts 的一部分，它和 proposal、design、spec delta 共同构成变更的知识体系，计划不是唯一中心。OMC 的 Plan 模式和 /ralplan 产出的是给编排系统的执行蓝图，支持 `--consensus`（多角色共识规划）和 `--deliberate`（高风险任务的 pre-mortem 分析），更偏向协同规划。

下面是三者的直接对照：

| 维度 | Superpowers | OpenSpec | Oh My Claudecode |
|------|-------------|----------|------------------|
| 核心对象 | 工程执行阶段与技能触发 | change + artifacts + spec delta | mode + team + agent orchestration |
| 官方主心智 | gate-based engineering workflow | action-based workflow | orchestration-first workflow |
| 默认主线 | brainstorming → worktree → writing-plans → executing-plans → TDD → code-review → finishing-branch | propose → apply → archive（简）；new → ff/continue → apply → verify → archive（扩展） | 无唯一固定主线；常见组合如 autopilot → ultrawork → ralph、plan → ralph → ultraqa |
| 阶段门禁 | 强，设计批准前禁止实现 | 弱，官方反对 rigid phase gates | 中等，Team 模式有显式 stage pipeline |
| worktree 地位 | 核心阶段之一 | 主流程不强调 | 并行 issue 流里明确提到 |
| specs 作为事实来源 | 不是主轴 | 是，openspec/specs/ 是 source of truth | 不是主轴 |
| 并行与多 agent | 有 subagent，但偏阶段推进 | 支持多 change 并行，非 agent 并发 | 核心卖点，automatic parallelization |
| 验证机制 | 强门禁（TDD + review + branch finishing） | 软约束（verify 不阻塞 archive） | 持续闭环（ultraqa + Architect 验收） |
| 更像什么 | AI 工程施工流 | AI 变更规格流 | AI 多 agent 作战编排流 |
| 主要短板 | 省掉后半段会退化成"计划驱动写代码" | 对日常编码推进体感未必轻；工程隔离感不强 | 过程黑箱感强，显式产物与人工掌控感偏弱 |

## 选型标准

如何在三者之间选择，取决于你当前任务的几个核心特征。

**优先选 Superpowers 的情况：** 你的主要诉求是快速推进实现、过程清楚、每一步都想显式控制。你偏好知道"下一步该干什么"，重视 worktree 隔离和计划驱动执行，主要任务是单人或小团队的 feature、refactor、bugfix，任务导向明确、重点在代码落地。Superpowers 对"工程动作"做了强约束，适合高频迭代且不想上重规格治理的场景。

**优先选 OpenSpec 的情况：** 你的主要诉求是需求对齐、规格演进、变更留痕、多人协作可审阅。任务具备以下特征时 OpenSpec 开始有价值：跨团队协作（前后端、QA、产品都参与时口头计划不够）；变更影响大（数据模型升级、API breaking change、权限模型调整、大范围架构迁移等需要明确不变量、兼容策略、rollout plan 和回滚方案）；需要长期追责或审计（合规、隐私、安全、核心商业规则场景中"我当时脑子里想的"不算文档）；一个 change 未来还会被反复追溯。

**优先选 OMC 的情况：** 你的主要诉求是大任务自动编排、多 agent 并发、批量 tickets 一起推。适合场景包括：可以强并行的任务；希望系统自动分兵；有很多相似 tickets 或子任务；以及你愿意牺牲一些过程透明度来换取执行吞吐。OMC 提供的四种推荐工作流——Full-Auto from PRD（`/ralplan → /teams → /ralph`）、No-Brainer（`/autopilot → /ultrawork → /ralph`）、Fix/Debugging（`/plan → /ralph → /ultraqa`）、Parallel Issue Handling（`/omc-teams → /ralplan → /ralph + /ultrawork → /ultraqa`）——覆盖了从需求驱动开发到多 ticket 并发处理的典型场景。

## 最佳实践组合

三者不是互斥关系，在成熟的工程实践里，分层使用通常是更合理的策略。

**分层使用的基本原则是：默认轻，按风险升级。** 日常开发默认走 Superpowers 的 `brainstorming → worktree → writing-plans → executing-plans` 主干，这是对大多数 feature/bugfix/refactor 任务最顺手的流。遇到高风险变更或跨团队协作场景，在此基础上叠加 OpenSpec 的 change 管理能力，让 proposal/spec delta/design/tasks 留存可追踪的变更记录。遇到大规模并行 ticket 或需要批量推进的任务，让 OMC 接管执行面的编排。

**一个具体的分层方案：**

- **默认开发流**：Superpowers 的工程主干（brainstorming → worktree → writing-plans → executing-plans → review → verification → ship）
- **高风险 change 管理**：在 brainstorming 阶段结束后，用 OpenSpec 的 `/opsx:propose` 或 `/opsx:new` 把 change intent、spec delta、design 显式化，归档后回写到 openspec/specs/
- **批量并行施工**：任务可以强并行时，用 OMC 的推荐 workflow（如 `/ralplan → /teams → /ralph`）接管执行面

**在 Superpowers 工作流内部可以做的两个最小补强：** 其一是在 brainstorming 和 writing-plans 之间加一个轻量的 decision-log 环节，只记三类内容——选了什么、为什么这么选、明确没做什么/延后什么。格式可以极简：

```
# Decision Log

## Context
这次改动解决什么问题

## Decision
采用什么方案

## Why
为什么不用另外几个候选方案

## Deferred
这次明确不处理什么
```

其二是在 executing-plans 之后加一个显式的 verification 环节，明确区分它和 code-review 的边界：code-review 偏静态审查（设计是否兑现、接口是否过宽、命名是否准确、测试是否覆盖关键路径），verification 偏动态验收（测试/构建通过、需求已覆盖、无明显回归、PR 描述材料齐全）。这样 writing-plans 里"如何证明完成"的部分才能真正被执行，而不是停留在文档里。

最终，Superpowers 适合"工程执行效率优先"的日常开发，OpenSpec 适合"变更意图与规格演进需要显式留存"的协作场景，OMC 适合"多 agent 并行与自动编排"的大规模执行场景。三者的优化目标不在同一维度，这也是为什么它们可以共存而不需要三选一。
