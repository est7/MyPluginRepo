# PAUL 框架分析与 Issue 驱动开发设计

## PAUL 的本质定位

PAUL（Plan-Apply-Unify Loop）并不是对 GSD 的彻底否定，而是在 GSD 的执行优势基础上，针对一个更具体的失败模式构建的收束机制：执行漂移（execution drift）。

PAUL 的核心论断是：执行如果没有显式对账，就会产生漂移；漂移在多个会话中会复利累积。这不是表象问题，而是根因。大多数 AI 工作流失败，不是因为计划不够好，也不是因为生成能力不足，而是因为执行中发生了偏离、偏离没有被记录、下一个会话把"当前实际状态"误当成"原计划状态"继续推进，于是错误上下文被继承并不断放大。从系统视角看，PLAN 是目标状态定义，APPLY 是状态变更，UNIFY 是把预期状态与实际状态做 reconciliation。没有 UNIFY，系统就没有闭环；没有闭环，就没有可靠的会话连续性。

相比之下，GSD 更像是 throughput system，优化的是执行速度；PAUL 更像是 controlled delivery system，优化的是可审计、可恢复、可验证三个维度的可靠性。这是两者最根本的定位差异。

## 八个设计差异点的逐条评价

**强制对账（UNIFY）** 是 PAUL 最有价值的创新点。GSD 里的收尾是隐式的——提交了代码、归档了 milestone 就算完成，learnings 在会话结束后蒸发。PAUL 把 SUMMARY.md 作为强制产物，记录计划与实际的差异、执行中新增的决策、遗留事项、以及每条验收标准的通过状态。没有这个产物，循环就不算关闭，下一轮就不允许安全启动。这是操作语义上的根本区别，不只是"多一个文件模板"。

**in-session 执行 vs 并行 subagent** 是 PAUL 与 GSD 分歧最大的地方，但这里 PAUL 的论证有一个值得注意的盲点。PAUL 批评 subagent 的冷启动成本和上下文注入成本是对的：每个子 agent 都需要重新注入上下文，相当于重复支付固定成本；主会话里已经形成的隐式约束和历史决策，切割给多个子 agent 后会造成局部最优、接口不一致、边界理解分歧。但 PAUL 的反向立场——默认 in-session 串行跑到底——同样没有解决会话本身的 context 腐化问题。一个涵盖 20 多个任务的 APPLY 阶段跑完，主会话已经 60-70% 满，这时 Qualify 步骤的质量是否仍然可靠？PAUL 对这个问题保持沉默。

**单一下一步（Single Next Action）** 在工程上有意义，它减少决策疲劳、维持 momentum。但这条不能被讲成绝对优势。如果当前状态判断本身出错，单一推荐路径会把错误默认强化，在高不确定性阶段还会掩盖探索空间。更稳的表述是：在低不确定性阶段默认推荐单一下一步；在架构分叉或依赖冲突阶段，应该显式呈现分支选项和切换条件。

**HANDOFF-{date}.md 显式续作** 比 GSD 的 `.continue-here.md` 实质性地更强。它不只记录"停在哪里"，还记录"为什么做这件事"和"当时的决策链"。对于跨天、跨会话的项目，这是核心基础设施。

**验收标准（AC）作为一等公民** 是方法论升级，不只是格式升级。GSD 风格的任务描述通常停留在动作层面：implement X、refactor Y、add support for Z。这些是动作描述，不是完成定义。PAUL 用 AC-1 / AC-2 / AC-3 配合 Given/When/Then 结构，把完成定义转成可测试条件，同时把质量门禁前移到计划阶段。"Done"是模糊的，"AC-3: PASS"不是。这一点对任何 AI 辅助工作流都是基础设施级别的改进。

**Boundaries 硬约束** 对 AI agent 尤其重要，因为大语言模型的默认行为是"顺手改一下相关代码"。显式的 DO NOT CHANGE 声明让 scope creep 变得可见，而不是在执行过程中静默扩散。不过框架还需要补充边界冲突的处理机制：当 AC 无法在边界内满足时，必须明确记录冲突、停止静默扩展范围、在 UNIFY 中输出边界冲突说明、在下一轮 PLAN 中显式请求边界变更。没有这条规则，Boundaries 会从约束变成阻塞。

**SPECIAL-FLOWS 技能审计** 解决了"人工 checklist 会被跳过"的问题，把纪律 encode 成结构。但需要准确理解这个机制的边界：它是 workflow compliance tracking，不是 full outcome verification。跑了 linter 不代表结果合格，调用了 review-pr 不代表评论被处理。最终的完成判断仍然需要依靠 AC pass/fail，而不是 SPECIAL-FLOWS 的调用记录。

**小数 phase（8.1、8.2）** 是实用的工程细节：中途插入的紧急任务不破坏原有编号，既处理了真实项目里必然存在的打断，又保持了 roadmap 的整洁。

## Token 效率的论证方式

PAUL 提出的"token-to-value efficiency"是一个有价值的方向，但在当前形态下还是口号多于论证。要让这个概念站得住，需要半形式化地定义它。

一个更稳的工程化表达：单位 token 消耗带来的有效项目推进量，可以通过以下代理指标衡量——被验收通过的 AC 数量、被明确记录的决策数、下次会话的可恢复程度、返工率、边界违规次数。过度使用"token efficiency > speed to done"这类宣言式表述，容易被反驳为"只是用'我觉得更值'替代'更快'"。更可辩护的说法是：在 AI 辅助开发中，保持上下文完整性通常比最大化并行执行吞吐量更有价值（context-retention efficiency，rework-adjusted productivity）。

## PAUL 目前缺失的两块基础设施

要让 PAUL 从优秀论述升级为可执行规范，还需要两样东西。

**一是最小 artifact schema。** PAUL 提到了 PLAN.md、SUMMARY.md、HANDOFF-{date}.md、SPECIAL-FLOWS.md，但没有定义最小字段。没有 schema，框架就容易退化成"大家随便写"。推荐的最小结构如下：

```
## PLAN.md
- Objective
- Scope
- Boundaries
- Acceptance Criteria (AC-1, AC-2, AC-3 with Given/When/Then)
- Risks
- Next Action
```

```
## SUMMARY.md
- Planned vs Actual
- Decisions Made
- Deviations
- Deferred Issues
- AC Results (PASS/FAIL per criterion)
- Next Recommended Action
```

```
## HANDOFF-{date}.md
- Current Loop Position
- Current State
- Open Risks
- Blocking Decisions
- Ordered Resume Steps
```

**二是状态转换规则。** PAUL 有流程名，但没有 transition rules。例如：什么条件下允许从 PLAN 进入 APPLY；APPLY 中发现边界冲突时如何处理；UNIFY 失败是否允许进入下一轮 PLAN；AC 未通过但任务部分可交付时如何记录。这部分一旦写清楚，PAUL 才会从写作风格变成操作框架。

## 与当前 Issue 驱动体系的对应关系

把 PAUL 和 GSD 的概念映射到以 GitLab issue 为中心的工作流，可以看到很强的结构对应：

| 当前系统 | 等价概念 |
|---|---|
| `/issue-sync` | PAUL 的 UNIFY（强制对账，无它不关闭） |
| DELTAS 块 | SUMMARY.md 里的"计划 vs 实际" |
| task issue close criteria | PAUL 的 AC（Given/When/Then） |
| `stable_id` 匹配门 | GSD 的 plan-checker（防错误传播） |
| Pre-fetch JSONL 注入 | GSD v2 的文件路径 dispatch（传引用不传内容） |

这个对应关系说明，以 GitLab issue 为持久化层的工作流，本质上已经综合了 PAUL 和 GSD 的核心优点——只是 context 持久化层换成了 issue tracker，而不是本地文件系统。Issue 天然是比 session 和记忆文件更可靠的持久化载体，它与 review、MR、讨论紧密绑定，且不会出现真相源分裂的问题。

## 如果取两者长处重新设计

从两个框架中提取最有价值的部分，一个更稳健的设计不会是"PAUL+GSD 混合版流程名词"，而是三层清晰的协议原则：issue 作为状态源、session 作为一次性执行容器、reconcile 作为唯一关闭条件。

这个设计对应四个阶段，可以称为 Resolve → Slice → Execute → Reconcile 循环。

**Resolve** 把 issue 解析成可执行规范，输出 Objective、AC、Boundaries、Dependencies、推荐切片方式。计划是约束不是小说，AC 和边界比步骤列表更重要，引用优先于复制内容。

**Slice** 是两个框架都没有完全解决的环节。GSD 没有严格限定什么任务允许分发给 subagent；PAUL 没有定义 session 什么时候应该主动终止、上下文何时不再可信。更有效的判断标准是：

可以放在同一个 slice 的任务——修改的是同一模块或强相关模块、共享同一组 AC、需要连续推理链、中间决策彼此强耦合。

必须切片的任务——涉及多个子系统、一个任务的输出只是另一个任务的输入引用、可以独立验证、可以独立回滚、可以独立 code review。

```
触发切片重启的条件（满足任一即结束当前 slice）：
- 完成一个独立 AC 集合
- 修改文件集合超出预期边界
- 引入新设计决策
- 出现 BLOCKED / DONE_WITH_CONCERNS
- 需要跨模块扩展
- token/context 使用达到阈值
- 验证结果开始依赖长程记忆而非当前结构化状态
```

最后一条尤为关键：一旦验证在"凭印象继续"而不是"基于当前显式状态"，就应该立即停止当前 slice。

**Execute** 采用短回合主 session + 受限并行 worker 的模式，不是"全部都在一个 session"，也不是"能并行就并行"。主 session 负责读入结构化状态、做关键设计决策、执行高耦合改动、统一判断 AC 是否达成、产出 reconcile 记录。Worker 只负责 bounded research、检索引用材料、低耦合机械任务、格式转换和枚举对照、独立可验证的小改动候选。Worker 不拥有"项目真相"——issue 和 reconcile artifact 才拥有项目真相。

**Reconcile** 是唯一关闭条件。commit 不是完成，MR 不是完成，代码跑过也不是完成。没有结构化对账，任务不得标记 done。

```markdown
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
```

Reconcile 完成后，下一轮从 issue 重新 Resolve，而不是从 session 继续"接着想"。

## 需要保留与不保留的判断

从 GSD 应该保留的是：计划必须可执行而非仅是愿景的意识、goal-backward verification（从目标反推是否达成，与 AC 合并使用）、以及原子提交意识（每个 slice 的结果尽量具备独立提交和回滚能力）。

从 PAUL 应该保留的是：强制对账、AC first-class、Boundaries 显式化、Handoff 机制（但主载体应从本地文件切到 issue）、以及低不确定性阶段的 Single Next Action 默认行为。

不应该照搬的是 PAUL 的"in-session by default"强默认。更合理的默认应该是"in-slice by default"——保持在一个上下文闭包内执行，但这个闭包可以跨 session 重建，不要求依赖单个长会话。另外，PAUL 隐含的"subagent 几乎无用"态度也过于绝对。subagent 不是天然低质，问题在于是否被分配了错误类型的任务。适合 subagent 的是搜索文档、枚举调用点、对比 schema、收集失败样例、生成变更候选清单等bounded任务；不适合的是跨模块架构重构、涉及隐式约束的实现、需要连续设计判断的代码变更、以及最终验收与范围解释。

文件系统为中心的 handoff 也不应该是主机制。文件系统 handoff 的问题是容易产生分叉、真相源不唯一、与 review/MR/讨论脱节、难以和 task lifecycle 绑定。更清晰的分工是：issue 作为权威状态源，MR 作为代码与审查状态源，文件作为辅助制品而不是主状态。

## 关于 /issue-implement 的启动协议

PAUL 的 in-session 串行执行假设在整个 APPLY 过程中，会话上下文的质量保持稳定。但它没有定义何时应该主动切割会话重新注入。对应到具体工作流，/issue-implement 每次启动时应该强制重置 context，而不是依赖连续会话的累积。

原因在于连续会话累积上下文本质上是隐式状态，有三个内在问题：不可审计、不可精确重建、会被模型的近期 token 分布污染。Pre-fetch 注入是显式状态恢复，好处是可复现、可对账、可控制版本、可定位漂移来源。

更稳的启动协议应该包含：拉取 issue 当前状态、拉取关联 MR/文档/依赖 issue、注入最新结构化摘要（而非历史整段对话）、注入 slice 边界和 AC 和 open concerns、明确本轮只处理哪个 slice。这相当于把每次执行都变成从权威状态快照冷启动，而不是从聊天记忆热启动。

## 落地规则

把上述分析收束成可直接写进规范的操作规则：

**规则 1：Issue 是唯一真相源。** 任何会话内新决策，若未写回 issue/reconcile block，不视为持久状态。

**规则 2：完成的定义是 Reconcile 完成。** 没有结构化对账，任务不得标记 done。

**规则 3：执行必须按 slice 进行。** 单个执行回合只允许服务一个上下文闭包。

**规则 4：subagent 只能做 bounded task。** 不可让其拥有最终范围解释权、AC 解释权、架构决策权。

**规则 5：每次执行启动必须重新注入状态。** 不得假设上个会话的隐式上下文仍然可靠。

**规则 6：AC 和 Boundaries 比计划步骤优先级更高。** 若步骤与 AC/Boundaries 冲突，以后者为准。

**规则 7：边界冲突必须显式升级。** 若不突破边界就无法满足 AC，必须记录冲突、停止静默扩 scope、生成新的 planning/approval 动作。

**规则 8：DONE_WITH_CONCERNS 不能直接流入 CLOSED。** 只能流入 follow-up issue、explicit waiver、或由人工决策的 bounded acceptance。否则"有顾虑但先关"会变成新的漂移源。

不要让 session 承担 continuity；让 issue 承担 continuity。不要让 agent 持有项目真相；让 reconcile artifact 持有项目真相。
