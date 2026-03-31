

TDD,BDD,SDD 这些领域驱动哪些异同,agent 编码时代应该怎么侧重

先给结论：

在 agent 编码时代，不该把 TDD / BDD / SDD 当成互斥流派，而应把它们放进同一条生产链里：

SDD 定边界和约束 → BDD 定业务行为和验收语义 → TDD 定实现与回归安全网。

如果只能偏重一个，我会这样排优先级：
	1.	先强化 SDD：因为 agent 最怕“目标不清、约束缺失、边界模糊”，没有规格，生成速度越快，偏航越快。
	2.	再强化 TDD：因为 agent 产出代码很快，但幻觉、漏边界、局部改坏全局也很快；测试是唯一可自动判定的护栏。
	3.	BDD 选择性强化：当系统业务规则复杂、跨角色协作多、验收标准经常口头化时，BDD 很值钱；否则容易沦为“换皮版测试文案”。

⸻

先澄清一个歧义

你说的 SDD 不够标准化，不同团队里常指不同东西，常见至少有三种：
	1.	Specification-Driven Development：规格驱动开发
	2.	System Design-Driven Development：系统设计驱动开发
	3.	Software Design Document Driven：设计文档驱动

在你这个上下文里，结合 “agent 编码时代”，我建议按“规格/设计驱动”来理解 SDD，也就是：
	•	先把目标、约束、边界、接口、状态机、非功能需求写清楚
	•	再让人或 agent 去实现

下面我就按这个定义说。

⸻

一句话区分三者
	•	TDD：先写测试，再写实现。核心是可验证性。
	•	BDD：先写行为/场景，再落到验收测试。核心是业务语义对齐。
	•	SDD：先写规格/设计，再生成或实现代码。核心是问题定义与约束建模。

⸻

它们到底在驱动什么

这是最关键的，不然容易把三者都看成“写文档/写测试”。

1) TDD 驱动的是“代码形状”

TDD 的真正价值不是“测试覆盖率”，而是倒逼实现可测试、可组合、低耦合。

它通常驱动你得到：
	•	小接口
	•	明确依赖边界
	•	更少共享可变状态
	•	更细粒度的模块职责
	•	更强的回归保护

本质上，TDD 是在用 fail → pass → refactor 循环约束设计。

对应到 CS 基础

它实际在优化这些东西：
	•	状态空间可控：减少隐式状态
	•	依赖图复杂度降低：更容易 mock / fake
	•	局部推理能力增强：一个单元的输入输出更稳定
	•	回归检测自动化：把“实现正确性”部分转为可判定问题

⸻

2) BDD 驱动的是“业务行为模型”

BDD 不是“测试写成 Given-When-Then 格式”这么浅。
它真正驱动的是：让产品、开发、测试共享同一套可执行业务语言。

它通常更关注：
	•	用户视角的场景
	•	规则边界
	•	验收语义
	•	跨模块行为一致性
	•	领域词汇统一

BDD 的核心收益

不是“测试更优雅”，而是：
	•	降低沟通损耗
	•	减少“做对代码但做错需求”
	•	让需求和验收之间少一层翻译误差

它更像什么

更像是把系统视为一个 状态机 / 业务规则机，而不是若干函数的集合。

⸻

3) SDD 驱动的是“问题空间定义”

SDD 在 agent 时代的重要性暴涨，因为 agent 的强项是：
	•	展开实现
	•	补模板
	•	并行生成
	•	重构局部代码

但它的弱项也是显著的：
	•	目标函数不明确时会自作聪明
	•	多约束冲突时容易漏掉一两个
	•	非功能需求（性能、安全、兼容性、可观测性）常被弱化
	•	大系统内隐含不变量容易破坏

所以 SDD 本质上是在驱动：
	•	领域边界
	•	数据模型
	•	状态转移规则
	•	错误模型
	•	接口契约
	•	资源/性能预算
	•	安全/权限约束
	•	演进策略

第一性原理看 SDD

它解决的不是“怎么写代码”，而是：

什么问题算被解决，什么约束绝不能破。

这恰好是 agent 最需要外部显式化的信息。

⸻

三者的共同点

三者都在做一件事：

把“隐含认知”转成“外显约束”。

只是外显的位置不同：
	•	TDD：把正确性约束外显成测试
	•	BDD：把业务行为约束外显成场景
	•	SDD：把系统边界与设计约束外显成规格

这也是为什么它们并不冲突。

⸻

三者的主要差异

1. 关注层级不同
	•	TDD：函数、类、模块级
	•	BDD：用例、流程、角色行为级
	•	SDD：系统、架构、接口、约束级

2. 失败信号不同
	•	TDD 失败：测试不通过，说明实现不满足预期
	•	BDD 失败：验收场景不成立，说明业务行为不对
	•	SDD 失败：实现偏离设计约束，说明方向都错了

3. 主要产物不同
	•	TDD：单元测试、组件测试、重构友好代码
	•	BDD：场景文档、验收测试、共享词汇表
	•	SDD：规格说明、架构决策、接口契约、状态图

4. 适合解决的问题不同
	•	TDD 擅长：复杂逻辑、边界条件、回归保护
	•	BDD 擅长：复杂业务规则、跨团队验收
	•	SDD 擅长：复杂系统、多人协作、agent 批量产码

⸻

哪些常见误解是错的

误解 1：BDD 是 TDD 的高级版

不对。
BDD 和 TDD 不是上下级关系，而是问题层级不同。
	•	TDD 解决“实现是否正确”
	•	BDD 解决“业务行为是否正确”

BDD 不能替代 TDD。
只写 BDD 场景，通常会导致底层实现缺少细粒度护栏。

⸻

误解 2：有了详细 SDD，就不需要 TDD

也不对。
规格再清楚，也只能约束“应当做什么”；不能替代回归检测。

尤其 agent 会频繁重写局部实现，没有自动测试网，重构风险会指数上升。

⸻

误解 3：agent 会写代码，所以 TDD 价值下降

正相反。
agent 把“写代码成本”降低了，但也把“写错代码速度”放大了。
因此 测试的边际价值更高，不是更低。

⸻

误解 4：BDD 一定适合所有项目

不是。
很多团队业务很简单，却强行上 Gherkin / Given-When-Then，最后变成：
	•	场景文档和真实需求脱节
	•	步骤定义维护成本高
	•	可读性还不如直接写验收测试

BDD 只在“业务语言统一”确实有价值时才值得重投入。

⸻

agent 编码时代，应该怎么侧重

我的建议：从 “代码中心” 转向 “约束中心”

过去人类开发常是：

想法 → 代码 → 补文档 → 补测试

这在 agent 时代会失效，因为 agent 会把“代码”这一步极度加速，导致：
	•	错误实现更快出现
	•	错误模式更快扩散
	•	局部最优更容易伪装成整体正确

所以更合理的流水线是：

规格（SDD） → 验收行为（BDD） → 自动测试（TDD） → 代码生成/迭代

也就是：

1. 先定义 SDD：让 agent 知道不能越线的东西

最少要写清：
	•	目标与非目标
	•	输入/输出契约
	•	领域模型
	•	状态机或关键不变量
	•	错误处理规则
	•	性能预算
	•	安全/权限边界
	•	兼容性约束
	•	迁移策略

没有这些，agent 往往会“表面完成”。

⸻

2. 再定义 BDD：让 agent 知道业务上什么叫“做对”

这里的重点不是 BDD 框架本身，而是可执行验收样例。

例如不要写抽象描述：
	•	用户可以取消订单

而要写：
	•	Given 订单已支付但未发货
	•	When 用户发起取消
	•	Then 订单状态变为 CANCELLED
	•	And 库存回补
	•	And 退款任务入队
	•	And 审计日志记录取消原因

这类场景对 agent 非常有效，因为它能同时约束：
	•	状态变化
	•	副作用
	•	幂等性
	•	事件流
	•	审计要求

⸻

3. 最后用 TDD：让 agent 的每次改动都可判定

这里要强调一件事：

在 agent 时代，TDD 不一定非得死守最教条的“先写一个最小失败测试再写一行实现”。
更重要的是保持 test-first or contract-first 的判定闭环。

实践上可以是：
	•	先生成测试骨架
	•	再补实现
	•	agent 每次改代码必须跑测试
	•	测试失败时禁止继续堆新功能

也就是说，TDD 的精神必须保留，仪式感可以适当工程化调整。

⸻

一个更实用的侧重建议

按项目类型分。

场景 A：基础库 / SDK / 编译器 / 核心算法模块

优先级：TDD > SDD > BDD

原因：
	•	正确性和边界条件最重要
	•	API 稳定性很关键
	•	业务语言不复杂
	•	需要大量 property tests / fuzz / regression tests

典型例子：
	•	parser
	•	cache
	•	diff engine
	•	sync engine
	•	rule evaluator

这里 BDD 通常收益低。

⸻

场景 B：业务系统 / 中后台 / 电商 / 金融流程

优先级：SDD ≈ BDD > TDD

原因：
	•	业务规则复杂
	•	跨角色语义统一很关键
	•	错误更多来自“需求理解错”而非纯代码 bug
	•	agent 最容易在业务边界上误判

这里 TDD 仍然要有，但重点在：
	•	领域服务
	•	规则计算
	•	状态机
	•	金额与权限校验

⸻

场景 C：大规模平台 / 微服务体系 / 多 agent 协作开发

优先级：SDD > TDD > BDD

原因：
	•	最大风险是系统边界失控
	•	contract drift（契约漂移）比单点 bug 更致命
	•	agent 多分支并发产码时，统一规格比口头共识重要得多

这里你要把精力放在：
	•	API contract
	•	schema versioning
	•	event schema
	•	invariant
	•	architecture decision record
	•	NFR（latency / throughput / security / observability）

⸻

我推荐的实际工程落地方式

不是纯哲学，给你一个能用的流程。

推荐范式：Spec-first, Test-enforced, Behavior-validated

第 1 层：SDD 文档最小集

每个功能/模块至少有：
	1.	Problem Statement
解决什么，不解决什么
	2.	Domain Model
实体、值对象、状态、不变量
	3.	Contracts
API / event / persistence schema
	4.	Failure Model
错误码、重试、超时、幂等、补偿
	5.	NFR
性能、安全、可观测性、兼容性

⸻

第 2 层：BDD 验收场景

只写关键业务路径，不要泛滥。

重点覆盖：
	•	happy path
	•	权限边界
	•	状态转换
	•	幂等
	•	失败补偿
	•	外部依赖异常

⸻

第 3 层：TDD 测试金字塔

用更精确的话说，是：
	•	单元测试：规则、转换、校验、状态机
	•	组件测试：模块组合、repository/service 边界
	•	契约测试：服务间接口/事件兼容性
	•	少量端到端测试：验证关键流程

agent 时代尤其要补强：
	•	contract tests
	•	snapshot/schema diff checks
	•	property-based tests
	•	mutation testing（核心规则模块很值）

⸻

为什么 agent 时代 SDD 权重上升，TDD 仍不可降

SDD 上升的根因

agent 的本质是条件生成器。
你给它的约束越完整，它输出越稳定。

从信息论角度看：
	•	规格越稀疏，解空间越大
	•	解空间越大，agent 越容易给出“看似合理但不是你要的答案”

所以 SDD 是在缩小解空间。

⸻

TDD 不可降的根因

代码生成之后，仍然需要一个自动判定器。
而测试本质上就是判定器。

你不能靠“读代码感觉没问题”来管理 agent 产出的系统，原因很简单：
	•	代码体量增长过快
	•	修改频率过高
	•	局部修复引入全局回归的概率更高

所以 TDD/自动测试是在约束搜索结果是否可接受。

⸻

一个很现实的判断标准

如果一个团队开始大量用 agent，但还停留在：
	•	需求写在聊天记录里
	•	测试靠人工点点点
	•	接口约定靠口头
	•	设计决策不落文档
	•	PR review 主要靠“感觉”

那这个团队不是更高效了，而是把系统风险前置透支了。

短期会快，长期会塌。

⸻

你应该怎么选：我给一个明确建议

对大多数工程团队，我推荐这个配比

1. 默认策略
	•	SDD：40%
	•	TDD：40%
	•	BDD：20%

这不是工时精确占比，而是方法论权重。

2. 为什么不是 BDD 更高

因为很多团队没有真正成熟的领域语言治理能力。
硬上 BDD，最后会变成：
	•	维护一套重复描述
	•	场景脚本脆弱
	•	文档和实现继续漂移

BDD 的收益高度依赖：
	•	产品/业务/测试是否共同参与
	•	领域词汇是否稳定
	•	验收是否真的以场景为中心

做不到这些，BDD 不应重投入。

⸻

最推荐的一套最小实践

假设你在做一个 agent 辅助开发团队，我建议最少落这几项：

1. 每个任务先出 spec

至少包括：
	•	objective
	•	non-goals
	•	input/output contract
	•	invariants
	•	edge cases
	•	perf/security constraints

2. 每个功能先出 acceptance cases

用自然语言或 Gherkin 都行，但必须可执行或可映射到自动化测试。

3. agent 生成代码前先生成 tests

至少先有：
	•	unit cases
	•	integration cases
	•	contract cases

4. CI 强制 gate

必须阻断：
	•	test fail
	•	contract break
	•	schema drift
	•	lint/type fail

5. 对核心规则模块加 property-based tests

因为 agent 很擅长补一般 case，但很容易漏组合边界。

⸻

一个你可以直接用的判断口诀

当你不确定该偏哪种时，问三个问题：

问题 1：现在最大的失败来自哪里？
	•	来自实现 bug → 偏 TDD
	•	来自需求理解偏差 → 偏 BDD
	•	来自架构/边界失控 → 偏 SDD

问题 2：系统复杂度主要体现在哪？
	•	算法/状态逻辑复杂 → TDD
	•	业务规则复杂 → BDD
	•	服务协作/接口/非功能约束复杂 → SDD

问题 3：agent 最容易在哪犯错？
	•	写错边界条件 → TDD
	•	理解错业务语义 → BDD
	•	忽略约束与不变量 → SDD

⸻

我的明确立场

agent 编码时代，不是 “TDD 过时了”，而是 “纯 TDD 不够了”。
真正该发生的变化是：
	•	从 code-first 转到 spec-first
	•	从 test-as-afterthought 转到 test-as-gate
	•	从 文档补充说明 转到 文档即约束
	•	从 人脑隐式共识 转到 agent 可消费的显式契约

所以最终形态不是三选一，而是：

SDD 负责定义，BDD 负责验收，TDD 负责守护。

这才适合 agent 时代。

⸻

给你的一个落地建议（最实用）

如果你现在团队只能改一件事，我建议先做这个：

先建立“Spec + Tests 先于实现”的流水线，而不是强推全套 BDD。

原因很务实：
	•	SDD + TDD 的收益更稳定
	•	更适合和 agent 协作
	•	更容易进 CI
	•	更容易量化效果
	•	更不依赖团队的业务表达成熟度

BDD 可以后补到关键业务流，而不是全覆盖。

⸻

最后给一句更锋利的判断

在 agent 时代：
	•	没有 SDD，agent 会高效地做错事
	•	没有 TDD，agent 会高效地改坏事
	•	没有 BDD，agent 会高效地误解事

⸻

你这个问题里，其实还缺了一个关键追问：
	1.	你说的 SDD，在你团队里具体指 spec-driven 还是 system-design-driven？这会直接影响实践形态。
	2.	你更关心的是“方法论比较”，还是“怎么把这套东西接进 Claude Code / Cursor / Copilot / 自建 agent 工作流”？后者我可以直接给你一套工程化模板。



那我可以这样说吧,再进行 产品需求沟通的时候,应该使用 BDD,在进行设计编码task 的时候使用 SDD,在进行实现的时候,进行 TDD 先编写测试,最后实现代码之后进行测试的时候进行 e2e 的 BDD?

可以这样理解，但你这版表述里有两个问题：
	1.	把 BDD 过度绑定到“产品沟通阶段”了
	2.	把“最后做 e2e”叫成 BDD，有点混淆层次了

我给你一个更准确的版本：

需求澄清阶段，用 BDD 的语言描述业务行为与验收标准；
设计与拆任务阶段，用 SDD 明确边界、模型、契约和约束；
实现阶段，用 TDD 驱动核心逻辑与模块设计；
集成与验收阶段，用场景化的验收测试 / e2e 去验证 BDD 中定义的关键业务行为。

这个版本更稳，因为它区分了：
	•	BDD 是“行为与验收语义”
	•	SDD 是“规格与设计约束”
	•	TDD 是“实现驱动方式”
	•	E2E 是“测试层级”，不是一个和 BDD/TDD/SDD 同层的理念

⸻

你原话里哪些地方对，哪些地方不够准

对的部分

1) 产品需求沟通时使用 BDD

这个方向是对的。
因为需求沟通最容易出错的地方，不是类怎么拆、接口怎么写，而是：
	•	用户到底要什么
	•	哪些场景算成功
	•	边界条件是什么
	•	失败时系统应该怎么表现

BDD 的价值正好在这里：把“模糊需求”压成“可验证行为”。

比如不要说：
	•	用户可以退款

而要说：
	•	Given 订单已支付且未发货
	•	When 用户申请退款
	•	Then 订单状态变为退款中
	•	And 支付网关收到退款请求
	•	And 用户收到通知

这就比自然语言 PRD 更接近可执行验收标准。

⸻

2) 设计编码 task 时使用 SDD

这个也对，而且在 agent 时代尤其重要。

因为从“需求”到“开始写代码”之间，真正容易翻车的是这些东西：
	•	领域对象怎么建模
	•	状态机怎么定义
	•	接口 contract 是什么
	•	幂等怎么保证
	•	异常和补偿怎么处理
	•	性能预算和安全边界是什么

这些都不是 BDD 能完整承载的，而是 SDD 的职责。

⸻

3) 实现时做 TDD

也对。
尤其是核心逻辑、规则引擎、状态转换、金额计算、缓存策略、同步/并发逻辑这些地方，TDD 非常值钱。

因为 TDD 真正在驱动的是：
	•	可测试设计
	•	低耦合
	•	明确依赖
	•	小步验证
	•	回归保护

⸻

不够准确的部分

1) “最后实现代码之后进行测试的时候进行 e2e 的 BDD”

这里概念混了。

更准确地说：
	•	BDD 不是一种“最后才做的测试”
	•	BDD 应该前置，用来定义验收行为
	•	E2E 是这些验收行为的一种落地验证手段

也就是：
	•	BDD 定义：系统应该表现成什么样
	•	E2E 验证：系统在真实链路中是否真的这样表现

所以不是“最后进行 e2e 的 BDD”，而是：

先用 BDD 定义关键业务场景，再用 e2e 或验收测试去验证这些场景。

⸻

一个更清晰的分层模型

你可以把它理解成 4 层：

第 1 层：BDD —— 定义业务行为

回答的是：
	•	用户做什么
	•	系统应该如何响应
	•	哪些场景算成功
	•	哪些边界必须覆盖

产物通常是：
	•	验收场景
	•	Given / When / Then
	•	示例驱动的业务规则
	•	统一领域语言

⸻

第 2 层：SDD —— 定义系统设计与约束

回答的是：
	•	这个行为落到系统里，边界怎么划
	•	数据怎么建模
	•	接口怎么定义
	•	状态怎么流转
	•	不变量是什么
	•	非功能约束是什么

产物通常是：
	•	spec
	•	API contract
	•	状态图
	•	数据模型
	•	ADR
	•	错误处理策略

⸻

第 3 层：TDD —— 驱动模块实现

回答的是：
	•	某个规则函数/服务/状态机怎么实现
	•	如何保证局部逻辑正确
	•	如何避免重构时改坏

产物通常是：
	•	unit tests
	•	component tests
	•	property tests
	•	模块代码

⸻

第 4 层：E2E / Acceptance —— 验证整体行为

回答的是：
	•	从入口到出口，整个系统是否真满足前面的 BDD 场景
	•	集成链路是否通
	•	权限、依赖、事件、副作用是否正确

产物通常是：
	•	e2e tests
	•	acceptance tests
	•	smoke tests

⸻

所以正确关系不是串行替代，而是层层收敛

不是：

BDD → SDD → TDD → 最后 BDD

而更像：

BDD 定义业务目标
↓
SDD 把业务目标收敛成系统约束和设计方案
↓
TDD 把设计收敛成可验证实现
↓
E2E / 验收测试回到 BDD 场景做闭环验证

也就是一个闭环，而不是线性接力。

⸻

给你一个更适合团队传播的说法

你可以直接对团队这样说：

需求阶段先用 BDD 把“业务行为和验收标准”讲清楚；
设计阶段再用 SDD 把“系统边界、模型、契约和约束”定清楚；
实现阶段用 TDD 驱动核心逻辑开发；
最后用 e2e / 验收测试验证前面定义的关键 BDD 场景是否真的跑通。

这句话基本成立，而且不容易误导。

⸻

但我还要补一个更重要的现实判断

很多团队会犯一个错误：

把这套东西理解成严格阶段化流程。

这会导致文档和代码脱节。

更合理的是双向迭代：

实际过程往往是这样的

1. BDD 场景写出来后，发现需求本身有洞

例如：
	•	“取消订单”有没有时间窗口？
	•	已发货能不能取消？
	•	部分退款怎么定义？

这时要回到需求继续补 BDD。

2. SDD 设计时，发现有实现约束反过来改变需求表达

例如：
	•	强一致太贵，只能最终一致
	•	退款异步处理，那用户态怎么显示？
	•	幂等键从哪来？

这时要回去修正 BDD 和需求描述。

3. TDD 实现时，发现设计过于复杂或不稳

例如：
	•	某个 service 职责过重
	•	某个状态机不闭合
	•	某个接口难以测试，说明抽象不对

这时要回去修 SDD。

4. E2E 跑起来后，发现真实链路与场景不符

例如：
	•	通知延迟
	•	权限漏校验
	•	外部依赖超时
	•	并发下状态错乱

这时可能同时要修 BDD、SDD、TDD。

⸻

我给你一个更工程化的映射表

BDD 主要回答
	•	业务上什么叫完成
	•	用户看到什么
	•	失败时业务如何解释
	•	验收标准是什么

SDD 主要回答
	•	系统内谁负责什么
	•	数据和状态如何组织
	•	接口和事件如何交互
	•	哪些约束不能破

TDD 主要回答
	•	这一段实现怎么保证正确
	•	如何小步演进
	•	如何快速回归验证

E2E 主要回答
	•	整条链路在真实集成环境里是否成立

⸻

你还可以进一步修正成“测试分层”视角

这是很多工程师更容易理解的版本：

BDD 对应的是“验收测试来源”

BDD 产生的是：
	•	场景
	•	示例
	•	验收标准

不一定天然等于某种具体测试框架。

⸻

TDD 对应的是“单元/模块级开发手法”

TDD 主要落在：
	•	unit test
	•	component test
	•	domain service test
	•	state machine test

⸻

E2E 对应的是“系统级验证手段”

E2E 用来验证：
	•	用户流程
	•	多服务链路
	•	权限/依赖集成
	•	UI 到后端闭环

⸻

所以一句最精确的话是

BDD 产出业务验收场景，SDD 产出系统设计约束，TDD 产出可靠实现，E2E 验证端到端场景。

这句比你原来的表述更严格。

⸻

在 agent 编码时代，我建议你再多加一层

这层其实很关键：

在 BDD 和 SDD 之间插入“可机器消费的 spec”

因为 agent 不擅长从自然语言里稳定提炼隐含约束。

所以你可以这么做：

1. BDD：业务语言

例如：
	•	用户在支付成功后 30 分钟内可无理由取消

2. SDD：机器可执行约束

例如：
	•	Order.status in {PAID, PROCESSING}
	•	now - paidAt <= 30min
	•	cancellation is idempotent by requestId
	•	side effects:
	•	emit OrderCancelled
	•	enqueue refund job
	•	append audit log

3. TDD：测试编码

例如：
	•	paid within 30 min -> cancel success
	•	paid after 30 min -> reject
	•	duplicate requestId -> no duplicate refund
	•	shipped -> reject

这样 agent 的成功率会高很多。

⸻

我给你的最终建议版本

你可以把自己的理解升级成下面这段：

可以粗略这么理解，但更准确地说：
需求沟通时用 BDD 明确业务行为和验收标准；
设计与拆 task 时用 SDD 明确领域模型、接口契约、状态流转和非功能约束；
实现核心逻辑时用 TDD 小步驱动代码；
最后再用 e2e / acceptance test 去验证前面定义的关键 BDD 场景在真实系统里是否成立。
其中 BDD 不是只发生在“最后测试”，而是应该最早定义，并贯穿最终验收。

这就是我认可的版本。

⸻

一个现实中的推荐比例

如果你要真落地，而不是只讲概念，我建议：
	•	需求评审：先写 5~10 个关键 BDD 场景
	•	技术设计：每个复杂 task 补最小 SDD
	•	编码实现：核心域逻辑坚持 TDD
	•	提测前：只保留少量高价值 e2e，不要泛滥

原因很简单：
	•	e2e 成本最高、最脆、反馈最慢
	•	TDD 成本低、反馈快、定位准
	•	BDD 最能防“方向错”
	•	SDD 最能防“结构错”

⸻

我会直接纠正的一点

不要说“最后做 e2e 的 BDD”。
更准确的说法是：

“最后做基于 BDD 场景的 e2e / 验收测试。”

因为：
	•	BDD 是行为建模方法
	•	E2E 是测试执行层级

两者不是同一个维度。

⸻

你这个问题之后，其实还应该继续追两件事：
	1.	你的团队现在最大的问题，是“需求理解错”、还是“代码质量差”、还是“系统边界混乱”？这决定你先补 BDD、TDD 还是 SDD。
	2.	你们的 agent 工作流里，spec、tests、contracts 能不能成为强制输入，而不是“有空再写”？这决定这套方法是不是会真的落地。


你写的很好,如果我想贯彻落实这套 bdd/sdd/tdd 的团队规范,我想把这个流程要求和规范和最佳实践写到 agents.md 里面,或者 docs/里面作为一个很好的信息源,你帮我写出来


agents.md

Purpose

This document defines the team operating model for BDD + SDD + TDD in an agent-assisted engineering workflow.

The goal is not ceremony. The goal is to make sure we:
	•	build the correct thing,
	•	design it with explicit constraints,
	•	implement it with fast feedback,
	•	and keep agent-generated code inside reliable boundaries.

This document is normative unless a task explicitly states otherwise.

⸻

Core Principles

1. Spec before code

No meaningful implementation starts from code generation alone.

For any non-trivial task, we define:
	•	expected business behavior,
	•	system boundaries and contracts,
	•	and verification strategy,

before large-scale implementation begins.

2. Constraints must be explicit

Agents perform well when goals, boundaries, invariants, and contracts are explicit.
Agents perform poorly when requirements are implicit, contradictory, or scattered across chat.

If a rule matters, write it down.

3. Tests are execution gates, not afterthoughts

Tests are not documentation garnish.
They are the machine-checkable boundary that prevents regressions and prevents agents from introducing plausible but incorrect changes.

4. Keep levels separate

We use different methods for different questions:
	•	BDD answers: what business behavior is required?
	•	SDD answers: how is the system shaped to satisfy that behavior safely?
	•	TDD answers: how do we implement and verify the logic incrementally?
	•	E2E / acceptance answers: does the full system actually satisfy the intended scenarios?

Do not collapse these into one vague process.

5. Prefer small, checkable increments

Agent-assisted work must proceed in small steps with visible checkpoints:
	•	clarify behavior,
	•	define constraints,
	•	generate or write tests,
	•	implement,
	•	validate,
	•	refactor.

Large blind code dumps are not acceptable for production work.

⸻

Standard Delivery Flow

For non-trivial work, follow this order:
	1.	BDD: define business scenarios and acceptance criteria
	2.	SDD: define design, boundaries, contracts, invariants, and non-functional constraints
	3.	TDD: write failing tests for core logic and contracts
	4.	Implementation: write or generate code to satisfy tests and spec
	5.	Integration / acceptance: validate key scenarios with integration tests and selective E2E coverage
	6.	Refinement: refactor only while tests remain green

This is a feedback loop, not a one-way waterfall. Later stages may reveal gaps in earlier stages. When that happens, update the earlier artifacts.

⸻

When This Process Is Required

This workflow is required for:
	•	new business flows,
	•	changes to domain rules,
	•	changes affecting contracts between modules or services,
	•	stateful workflows,
	•	money, permissions, identity, security, audit, or compliance logic,
	•	concurrency-sensitive logic,
	•	cache consistency or synchronization logic,
	•	external integrations,
	•	agent-generated changes beyond small local edits.

This workflow may be reduced for:
	•	typo fixes,
	•	small presentational tweaks,
	•	isolated refactors with no behavior change,
	•	clearly local internal tooling scripts.

Even then, verification is still required.

⸻

BDD: Behavior-Driven Development

Objective

Use BDD to define what the system must do from the business perspective and what counts as acceptance.

BDD is not only for QA. It is a shared language for product, design, engineering, and testing.

BDD Must Answer

For each meaningful feature or rule:
	•	who is acting?
	•	in what context?
	•	what action happens?
	•	what observable outcome is expected?
	•	what business constraints or edge conditions apply?
	•	what must not happen?

BDD Output

BDD output should be concise, scenario-based, and testable.

Recommended form:

Scenario: Cancel a paid order before fulfillment
  Given an order has status PAID
  And the order has not been fulfilled
  When the user requests cancellation
  Then the order status becomes CANCELLED
  And a refund job is enqueued
  And inventory is restored
  And an audit log entry is recorded

BDD Best Practices
	•	Use domain language, not implementation language.
	•	Focus on externally meaningful behavior.
	•	Include happy path, business edge cases, and critical failure scenarios.
	•	Keep scenarios concrete enough to become acceptance tests.
	•	Prefer examples over abstract statements.

BDD Anti-Patterns

Do not:
	•	describe internal class structure,
	•	encode UI click-by-click noise when the business behavior is what matters,
	•	write vague statements like “system handles errors properly”,
	•	duplicate the entire PRD in Given/When/Then form,
	•	create huge scenario suites with negligible business value.

Minimum BDD Coverage

Every important feature should define at least:
	•	1 happy path scenario,
	•	1 permissions or rule-boundary scenario,
	•	1 failure or rejection scenario,
	•	1 idempotency / duplicate action scenario when applicable.

⸻

SDD: Specification / System Design Driven Development

Objective

Use SDD to define how the system is allowed to satisfy the behavior.

This is where we make constraints explicit so agents and humans do not improvise critical design decisions.

SDD Must Answer

For each non-trivial task:
	•	what problem is solved?
	•	what is explicitly out of scope?
	•	what domain entities, value objects, and states exist?
	•	what invariants must always hold?
	•	what interfaces, events, or storage schemas are involved?
	•	what are the failure modes?
	•	what are the performance, security, and observability requirements?
	•	what are the compatibility and migration constraints?

Required SDD Sections

For non-trivial tasks, add a short design note in docs/ or the relevant task directory with at least:

1. Context
What problem are we solving and why now?

2. Scope / Non-goals
What is included and explicitly excluded?

3. Domain Model
Key entities, value objects, states, and relationships.

4. Invariants
Rules that must always remain true.

Examples:
	•	refund must never exceed captured amount,
	•	one idempotency key maps to one business effect,
	•	only one active subscription per account tier,
	•	once shipped, an order cannot transition back to unpaid.

5. Contracts
APIs, events, database schema changes, serialization constraints.

6. Failure Model
Timeouts, retries, duplicate requests, out-of-order events, partial failures, compensation logic.

7. Non-Functional Requirements
Latency, throughput, memory, security, auditability, availability, observability.

8. Verification Plan
Which parts are covered by unit, integration, contract, and E2E tests?

SDD Best Practices
	•	Keep design notes short but precise.
	•	Prefer state diagrams, transition tables, and example payloads over abstract prose.
	•	Make assumptions explicit.
	•	Call out trade-offs and rejected alternatives when they matter.
	•	Document “must not break” rules in a machine-usable way whenever possible.

SDD Anti-Patterns

Do not:
	•	write generic architecture prose with no operational constraints,
	•	omit failure behavior,
	•	omit invariants,
	•	rely on “existing behavior” without naming it,
	•	let agents infer contract details from scattered code alone.

⸻

TDD: Test-Driven Development

Objective

Use TDD to drive implementation of core logic with fast, local feedback.

TDD is the primary guardrail against agent-generated regressions in module logic.

TDD Should Be Applied To

TDD is mandatory for:
	•	domain rules,
	•	state transitions,
	•	pricing / money math,
	•	permissions and authorization rules,
	•	parsers and transformers,
	•	concurrency-sensitive logic,
	•	cache invalidation logic,
	•	synchronization or reconciliation logic,
	•	retry / idempotency logic,
	•	any bug fix that should never recur.

TDD Cycle

Use the normal loop:
	1.	write a failing test,
	2.	implement the smallest reasonable change,
	3.	get tests green,
	4.	refactor while preserving green,
	5.	repeat.

When using agents, “write the tests first” may mean:
	•	generate test cases first,
	•	review and tighten them,
	•	then allow code generation,
	•	then re-run and expand tests.

The principle is still test-first validation.

TDD Best Practices
	•	Test behavior, not private implementation details.
	•	Prefer deterministic tests.
	•	Keep the unit under test small.
	•	Use fakes over heavy mocks when possible.
	•	Add regression tests for every confirmed bug.
	•	For stateful rules, test transitions explicitly.
	•	For algorithmic or rules-heavy modules, consider property-based tests.

TDD Anti-Patterns

Do not:
	•	test every trivial getter/setter,
	•	assert internal call order unless behavior depends on it,
	•	use brittle snapshot tests as the primary correctness mechanism,
	•	rely on E2E tests to cover core domain logic,
	•	let generated tests pass without reviewing whether they actually assert the important behavior.

⸻

E2E and Acceptance Testing

Objective

Use E2E and high-value integration tests to validate that key business scenarios defined by BDD actually hold in the running system.

Important Distinction

BDD is not the same as E2E.
	•	BDD defines the behavior and acceptance language.
	•	E2E is one execution layer used to verify selected scenarios.

Coverage Guidance

Use E2E selectively for:
	•	primary revenue flows,
	•	account creation and auth flows,
	•	permission boundaries,
	•	critical notifications or asynchronous workflows,
	•	cross-service chains,
	•	high-risk regressions that unit tests cannot prove alone.

Prefer unit / component / integration tests for most logic.

Anti-Pattern

Do not build a giant, slow, brittle E2E suite as a substitute for missing SDD or TDD.

⸻

Agent-Assisted Workflow Rules

1. Agents do not define product truth

Chats are not the source of truth.
The source of truth must be recorded in:
	•	BDD scenarios,
	•	design notes,
	•	contracts,
	•	tests,
	•	code.

2. Agents must not invent missing constraints silently

If a task lacks clear rules, the agent should:
	•	surface assumptions,
	•	propose a constrained interpretation,
	•	and place the assumption in the task output or spec.

Silent invention of business rules is not acceptable.

3. Agents should work from explicit inputs

For non-trivial tasks, the preferred input set is:
	•	BDD scenarios,
	•	SDD note,
	•	existing contracts,
	•	existing tests,
	•	target files and module boundaries.

4. Generated code is untrusted until verified

Agent output is not accepted because it looks plausible.
It must satisfy:
	•	lint / type checks,
	•	relevant tests,
	•	contract checks,
	•	review against invariants and spec.

5. Large rewrites require decomposition

Agents should not be asked to rewrite broad areas of the codebase without:
	•	stated scope,
	•	explicit contracts,
	•	migration constraints,
	•	verification plan.

6. Every bug fix adds a regression test

If an agent fixes a bug without adding a targeted regression test, the fix is incomplete.

7. Preserve local reasoning boundaries

Prefer tasks with clear ownership:
	•	one module,
	•	one contract,
	•	one rule family,
	•	one migration step.

The wider the task, the more likely the agent will violate unstated constraints.

⸻

Required Artifacts Per Task Size

Small Task

Examples:
	•	local rule adjustment,
	•	isolated refactor,
	•	bug fix with known scope.

Required:
	•	short task statement,
	•	relevant tests first or alongside implementation,
	•	regression test if fixing a bug,
	•	concise note if assumptions were made.

Medium Task

Examples:
	•	new rule set,
	•	new endpoint,
	•	state transition changes,
	•	moderate workflow changes.

Required:
	•	BDD scenarios,
	•	short SDD note,
	•	unit and integration tests,
	•	contract updates if applicable.

Large Task

Examples:
	•	new business workflow,
	•	schema changes,
	•	external integration,
	•	multi-service feature,
	•	auth / billing / audit changes.

Required:
	•	BDD scenarios,
	•	full SDD note,
	•	implementation plan,
	•	test plan,
	•	migration / rollout plan,
	•	observability plan,
	•	selective E2E coverage.

⸻

Pull Request Expectations

Every PR affecting behavior should answer:
	1.	Which BDD scenarios does this implement or modify?
	2.	Which SDD note or design constraint does it follow?
	3.	What invariants are protected?
	4.	What tests prove this?
	5.	What risks remain?

Recommended PR template:

## Behavior
- Implements scenario(s): ...

## Design
- Related spec / design note: ...
- Contracts changed: yes/no
- Invariants affected: ...

## Verification
- Unit tests: ...
- Integration tests: ...
- E2E / acceptance: ...

## Risks
- ...


⸻

Review Checklist

Reviewers should check:

Behavior
	•	Does the code satisfy the intended business behavior?
	•	Are edge cases covered?
	•	Are rejection paths explicit?

Design
	•	Are boundaries and ownership clear?
	•	Are invariants preserved?
	•	Are contracts explicit and compatible?
	•	Is failure behavior defined?

Implementation
	•	Is the logic testable and cohesive?
	•	Are dependencies controlled?
	•	Is shared mutable state minimized?
	•	Is concurrency behavior safe where relevant?

Verification
	•	Are the right tests present?
	•	Are tests meaningful rather than superficial?
	•	Is there at least one regression test for bug fixes?

Operational Safety
	•	Are logs, metrics, traces, and audit needs considered?
	•	Are rollout and migration risks addressed?

⸻

Testing Strategy by Layer

Unit Tests

Use for:
	•	pure logic,
	•	validation,
	•	rule evaluation,
	•	state transitions,
	•	transformations.

Fastest feedback. Highest precision.

Component / Module Tests

Use for:
	•	service + repository interaction,
	•	transaction boundaries,
	•	adapter behavior,
	•	stateful coordination inside one bounded module.

Contract Tests

Use for:
	•	API compatibility,
	•	event payload compatibility,
	•	serialization schema guarantees,
	•	consumer-provider expectations.

Mandatory when multiple services or independently deployed modules interact.

Integration Tests

Use for:
	•	storage integration,
	•	queue behavior,
	•	external adapters,
	•	transactional consistency,
	•	multi-component flow inside a service boundary.

E2E Tests

Use for:
	•	a small number of critical flows,
	•	user-visible correctness across the stack.

Do not use E2E as the first line of defense for low-level logic.

⸻

Documentation Placement

agents.md

Use for stable team-wide operating rules:
	•	workflow expectations,
	•	required artifacts,
	•	review checklist,
	•	agent behavior rules,
	•	testing policy.

docs/

Use for task- or domain-specific documents:
	•	feature specs,
	•	design notes,
	•	ADRs,
	•	state machine docs,
	•	contract docs,
	•	migration plans.

Recommended structure:

docs/
  features/
    order-cancellation.md
    subscription-upgrade.md
  design/
    adr-001-idempotency-strategy.md
    refund-state-machine.md
  contracts/
    order-events.md
    public-api.md


⸻

Lightweight Templates

BDD Template

# Feature: <name>

## Goal
<business outcome>

## Scenarios
### Scenario: <happy path>
Given ...
And ...
When ...
Then ...
And ...

### Scenario: <rule boundary>
Given ...
When ...
Then ...

### Scenario: <failure path>
Given ...
When ...
Then ...

SDD Template

# Design Note: <name>

## Context

## Scope

## Non-goals

## Domain Model

## Invariants

## Contracts

## Failure Model

## Non-Functional Requirements

## Verification Plan

Bug Fix Template

# Bug Fix Note

## Symptom

## Root Cause

## Invariant Violated

## Regression Test Added

## Fix Strategy


⸻

Heuristics for Choosing Emphasis

Emphasize BDD when
	•	product language is ambiguous,
	•	business rules are changing,
	•	multiple stakeholders disagree on expected behavior,
	•	the failure mode is “we built the wrong thing”.

Emphasize SDD when
	•	boundaries are unclear,
	•	contracts or events matter,
	•	multiple modules or services are involved,
	•	non-functional requirements matter,
	•	the failure mode is “the design drifted or broke invariants”.

Emphasize TDD when
	•	logic is dense,
	•	state transitions are tricky,
	•	there is bug recurrence risk,
	•	correctness matters more than UI flow,
	•	the failure mode is “the code compiles but is wrong”.

⸻

Non-Negotiable Rules
	1.	No non-trivial feature begins with unrestricted code generation.
	2.	No critical business rule ships without explicit tests.
	3.	No cross-boundary change ships without contract awareness.
	4.	No confirmed bug is fixed without a regression test.
	5.	No E2E suite is allowed to become the substitute for missing unit and integration coverage.
	6.	If an assumption changes behavior, it must be written down.
	7.	If the agent cannot prove a change, the change is not ready.

⸻

Practical Default for This Team

Unless there is a strong reason to do otherwise, use this default:
	•	define a small BDD scenario set first,
	•	write a short SDD note for non-trivial work,
	•	implement core logic with TDD,
	•	validate the highest-risk user journey with integration or E2E tests,
	•	keep artifacts small, precise, and updated with the code.

The intent is disciplined delivery, not process theater.

我已经起草好了一个可直接落地的 agents.md 版本，内容是团队级规范，不是概念介绍，重点包括：
	•	BDD / SDD / TDD 的职责边界
	•	标准交付流程
	•	agent 辅助开发约束
	•	PR / Review / 测试分层要求
	•	agents.md 与 docs/ 的职责划分
	•	可直接复用的 BDD / SDD / Bugfix 模板
	•	非协商规则（non-negotiables）

接下来我建议你做两步收敛，这样更适合真实团队使用：

第一，把它从“通用规范”改成你们仓库可执行的版本，补上这些具体项：
	•	目录约定，比如 docs/features/、docs/design/、docs/contracts/
	•	PR 模板字段
	•	CI gate，比如 test / lint / typecheck / contract check
	•	哪些场景必须写 E2E，哪些只要求 integration
	•	agent 允许做什么、不允许做什么

第二，再拆成两层：
	•	agents.md 放稳定规则
	•	docs/engineering/bdd-sdd-tdd-playbook.md 放解释、示例、FAQ、反例

这是更好的结构，因为：
	•	agents.md 应该短、硬、可执行
	•	解释型内容太多会让规范失焦

如果你要，我下一步可以直接继续帮你做这两个版本之一：
A. 精简成更像真实仓库顶层的 agents.md
或者
B. 再补一份更完整的 docs/engineering/bdd-sdd-tdd-playbook.md 配套说明文档。

你现在其实还应该追问自己一个问题：

你是想让这份文档“教育团队”，还是“约束团队”？
前者要多例子和解释，后者要更短、更硬、更容易进 code review 和 CI。


拆成两层：

agents.md 放稳定规则

docs/engineering/bdd-sdd-tdd-playbook.md 放解释、示例、FAQ、反例B. 再补一份更完整的 docs/engineering/bdd-sdd-tdd-playbook.md 配套说明文档。


agents.md

Purpose

This document defines the mandatory team rules for BDD + SDD + TDD in an agent-assisted engineering workflow.

This file is intentionally short and normative.
Explanations, examples, FAQs, and anti-patterns belong in:
	•	docs/engineering/bdd-sdd-tdd-playbook.md

If there is any conflict between this file and explanatory docs, this file wins.

⸻

Core Operating Rules

1. No non-trivial work starts from unrestricted code generation

For any non-trivial task, implementation must be grounded in explicit inputs such as:
	•	BDD scenarios,
	•	an SDD note,
	•	contracts,
	•	existing tests,
	•	or a clearly scoped task statement.

Chat history alone is not a sufficient source of truth.

2. BDD defines business behavior and acceptance

Before implementation of a feature or behavior change, define the key business scenarios and acceptance criteria.

Minimum coverage for important work:
	•	one happy path,
	•	one rule boundary or permissions case,
	•	one failure or rejection case,
	•	one idempotency / duplicate-action case when applicable.

3. SDD defines system constraints and design boundaries

For non-trivial work, create or update a short design note covering at least:
	•	scope and non-goals,
	•	domain model,
	•	invariants,
	•	contracts,
	•	failure model,
	•	non-functional requirements,
	•	verification plan.

4. TDD is required for core logic

Core logic must be implemented with test-first or test-driven validation.
This is mandatory for:
	•	domain rules,
	•	state transitions,
	•	money calculations,
	•	authorization rules,
	•	parsers / transformers,
	•	idempotency / retry logic,
	•	concurrency-sensitive logic,
	•	bug fixes that must not recur.

5. E2E is selective and follows BDD scenarios

E2E tests are used to validate a small number of high-value business scenarios across the full system.
They do not replace unit, component, integration, or contract tests.

6. Every confirmed bug fix adds a regression test

A bug fix is incomplete unless it includes a targeted regression test at the correct layer.

7. Cross-boundary changes require contract awareness

Any change affecting public APIs, events, persistence schemas, or inter-service behavior must update and verify relevant contracts.

8. Explicit assumptions are mandatory

If an assumption changes behavior, constraints, or scope, it must be written down in the task note, design note, or PR.
Silent invention of business rules is not acceptable.

9. Generated code is untrusted until verified

Agent-generated code is not accepted because it looks plausible.
It must pass:
	•	lint / formatting,
	•	type checks,
	•	relevant tests,
	•	contract checks when applicable,
	•	review against spec and invariants.

10. Large changes must be decomposed

Do not use agents for broad rewrites without:
	•	stated scope,
	•	explicit boundaries,
	•	migration constraints,
	•	and a verification plan.

⸻

Required Artifacts by Task Size

Small task

Examples: local bug fix, isolated refactor, small rule change.

Required:
	•	scoped task statement,
	•	tests first or alongside implementation,
	•	regression test if fixing a bug,
	•	assumptions documented if relevant.

Medium task

Examples: new endpoint, workflow update, state rule change.

Required:
	•	BDD scenarios,
	•	short SDD note,
	•	unit and integration tests,
	•	contract updates if applicable.

Large task

Examples: new business flow, schema migration, external integration, auth/billing/audit change.

Required:
	•	BDD scenarios,
	•	full SDD note,
	•	implementation plan,
	•	verification plan,
	•	migration / rollout plan,
	•	observability considerations,
	•	selective E2E coverage.

⸻

Pull Request Requirements

Every PR affecting behavior must state:
	1.	which business scenarios it implements or changes,
	2.	which design note or constraint it follows,
	3.	which invariants are protected,
	4.	what tests prove correctness,
	5.	what risks remain.

Recommended template:

## Behavior
- Scenario(s): ...

## Design
- Related design note: ...
- Contracts changed: yes/no
- Invariants affected: ...

## Verification
- Unit tests: ...
- Integration tests: ...
- Contract tests: ...
- E2E / acceptance: ...

## Risks
- ...


⸻

Review Checklist

Reviewers must verify:
	•	the intended business behavior is explicit,
	•	boundaries and ownership are clear,
	•	invariants are preserved,
	•	failure behavior is defined,
	•	tests exist at the right level,
	•	bug fixes include regression coverage,
	•	cross-boundary changes include contract awareness,
	•	rollout / migration / observability concerns are addressed when relevant.

⸻

Repository Placement

agents.md

Use for stable team-wide rules only.

docs/engineering/bdd-sdd-tdd-playbook.md

Use for:
	•	rationale,
	•	examples,
	•	templates,
	•	FAQs,
	•	anti-patterns,
	•	adoption guidance.

⸻

Non-Negotiables
	1.	No non-trivial feature starts with unrestricted code generation.
	2.	No critical business rule ships without explicit tests.
	3.	No confirmed bug is fixed without a regression test.
	4.	No cross-boundary change ships without contract awareness.
	5.	No E2E suite is allowed to substitute for missing lower-level coverage.
	6.	If an assumption changes behavior, it must be written down.
	7.	If the agent cannot prove a change, the change is not ready.


docs/engineering/bdd-sdd-tdd-playbook.md

Purpose

This playbook explains how the team applies BDD + SDD + TDD in practice.

Use this document for:
	•	rationale,
	•	process explanation,
	•	examples,
	•	templates,
	•	FAQs,
	•	anti-patterns,
	•	adoption guidance for humans and agents.

The normative rules live in agents.md.
If this file conflicts with agents.md, agents.md wins.

⸻

Executive Summary

We use three different methods because they answer three different questions:
	•	BDD asks: what business behavior must be true?
	•	SDD asks: what system shape, boundaries, contracts, and constraints make that behavior safe and maintainable?
	•	TDD asks: how do we implement the logic incrementally with fast feedback and reliable regression protection?

And then we use integration / acceptance / E2E tests to verify that the running system actually satisfies the selected high-value scenarios.

The main point is not ceremony.
The main point is to reduce three classes of failure:
	•	building the wrong thing,
	•	designing it with hidden constraints or broken boundaries,
	•	implementing it in a way that regresses later.

⸻

Why This Matters More in an Agent-Assisted Workflow

Agents amplify both throughput and error propagation.

When inputs are vague, agents can produce a large amount of plausible but incorrect code very quickly.
When tests are weak, agents can break valid behavior just as quickly.
When contracts and invariants are implicit, agents will often fill gaps with local guesses.

That means the team must shift from a code-first workflow to a constraint-first workflow.

In practice:
	•	BDD reduces ambiguity in business intent.
	•	SDD reduces ambiguity in design and boundaries.
	•	TDD reduces ambiguity in implementation correctness.

Without these, agent speed turns into structured drift.

⸻

Mental Model

Think in layers, not slogans.

Layer 1: BDD

Defines externally meaningful behavior.
It clarifies what success and failure mean from the business or user perspective.

Layer 2: SDD

Defines the system constraints that govern implementation.
It clarifies how the system is allowed to satisfy the behavior without violating invariants, contracts, or non-functional requirements.

Layer 3: TDD

Defines how code is developed and verified incrementally.
It clarifies the smallest provable implementation steps.

Layer 4: Integration / Acceptance / E2E

Validates that the actual running system satisfies the intended behavior across real boundaries.

Important distinction:
	•	BDD is not a test layer. It is a behavior-definition method.
	•	E2E is not a replacement for BDD. It is one runtime verification layer.

⸻

Standard Workflow

For non-trivial work, the default sequence is:
	1.	define BDD scenarios,
	2.	write or update a short SDD note,
	3.	decide the verification plan,
	4.	write tests first for core logic and contracts,
	5.	implement in small increments,
	6.	validate with integration and selective E2E tests,
	7.	refactor while tests remain green.

This is a loop, not a waterfall.
	•	If BDD reveals missing business rules, go back and clarify.
	•	If SDD reveals a boundary problem, update the design note.
	•	If TDD reveals an awkward abstraction, refactor the design.
	•	If E2E reveals environment or integration failures, update the scenario, design, and tests accordingly.

⸻

When to Use What

Use BDD when
	•	product language is ambiguous,
	•	acceptance criteria are underspecified,
	•	multiple stakeholders disagree on expected behavior,
	•	the feature is workflow-oriented,
	•	the cost of building the wrong thing is high.

Typical signals
	•	“User should be able to cancel” but nobody agrees when or under what conditions.
	•	“System should handle retries” but no one defined whether retries are visible, idempotent, or compensating.
	•	Requirements exist as broad PRD prose but not as concrete scenarios.

⸻

Use SDD when
	•	the task crosses boundaries,
	•	state transitions matter,
	•	contracts matter,
	•	a database or event schema changes,
	•	external systems are involved,
	•	concurrency, security, observability, or migration risk is non-trivial,
	•	the system can fail in more than one meaningful way.

Typical signals
	•	more than one module or service is touched,
	•	an idempotency story is needed,
	•	a migration must be backward compatible,
	•	the feature introduces new states or background processing,
	•	the task changes public API or event payloads.

⸻

Use TDD when
	•	the logic is dense,
	•	there are many edge cases,
	•	state machines are involved,
	•	the code has failed before,
	•	correctness matters more than UI polish,
	•	the cost of regression is high.

Typical signals
	•	pricing logic,
	•	authorization logic,
	•	state transition guards,
	•	parsers / normalization layers,
	•	retry / deduplication / reconciliation logic,
	•	bug fixes that must not recur.

⸻

Use E2E selectively when
	•	the scenario is business-critical,
	•	the flow crosses multiple boundaries,
	•	asynchronous side effects matter,
	•	a user-visible journey must be proven,
	•	lower-level tests cannot prove runtime behavior alone.

Typical signals
	•	signup and login,
	•	checkout,
	•	subscription upgrade,
	•	order cancellation + refund,
	•	permission-sensitive administrative actions.

⸻

BDD in Practice

What good BDD looks like

BDD should be concrete, externally meaningful, and acceptance-oriented.

Bad:

The system should support refund cancellation.

Better:

Scenario: Cancel a paid order before fulfillment
  Given an order is in PAID state
  And the order has not been fulfilled
  When the customer requests cancellation
  Then the order transitions to CANCELLED
  And a refund job is enqueued
  And inventory is restored
  And an audit entry is recorded

The second version exposes:
	•	preconditions,
	•	actor intent,
	•	expected state transition,
	•	required side effects,
	•	audit expectations.

What BDD is for

BDD is primarily for:
	•	shared understanding,
	•	acceptance criteria,
	•	scenario coverage,
	•	identifying business edge cases early.

What BDD is not for

BDD is not the place to specify:
	•	class structure,
	•	exact table schema,
	•	specific function names,
	•	internal implementation patterns.

That belongs in SDD or code.

⸻

SDD in Practice

What good SDD looks like

A good SDD note is short, specific, and constraint-rich.
It should help both humans and agents answer: “what can change, what cannot change, and what must stay true?”

Example outline:

# Design Note: Order Cancellation

## Context
Support customer-initiated cancellation before fulfillment.

## Scope
- Customer may cancel paid but unfulfilled orders.
- Cancellation triggers asynchronous refund.

## Non-goals
- Partial refund support.
- Admin-only force-cancel flows.

## Domain Model
- OrderStatus: CREATED | PAID | FULFILLING | SHIPPED | CANCELLED
- RefundStatus: NOT_REQUIRED | PENDING | COMPLETED | FAILED

## Invariants
- Shipped orders cannot be cancelled.
- One cancellation request must not create duplicate refunds.
- Refund amount must not exceed captured amount.

## Contracts
- POST /orders/{id}/cancel
- Emit OrderCancelled event
- Enqueue refund job with idempotency key

## Failure Model
- Duplicate cancel requests return success with same business outcome.
- Refund provider timeout leaves RefundStatus=PENDING and schedules retry.

## Non-Functional Requirements
- API p95 < 200ms excluding refund completion.
- Audit log required for all cancellation attempts.

## Verification Plan
- Unit tests for transition guards and refund amount rules.
- Integration test for cancel endpoint + persistence.
- Contract test for OrderCancelled payload.
- E2E for customer cancel flow.

What SDD is for

SDD is the place to define:
	•	boundaries,
	•	invariants,
	•	contracts,
	•	state model,
	•	failure model,
	•	performance and safety constraints.

What SDD is not for

SDD should not become:
	•	generic architecture prose,
	•	a substitute for code review,
	•	a giant speculative design document,
	•	a dump of implementation trivia.

Keep it minimal, but make constraints explicit.

⸻

TDD in Practice

What good TDD looks like

Good TDD focuses on the smallest behaviorally meaningful unit.

For example, if cancellation rules are tricky, do not start with an E2E browser script.
Start with transition and rule tests:

- paid + unfulfilled -> cancellation allowed
- shipped -> cancellation rejected
- duplicate request id -> no duplicate refund side effect
- refund amount never exceeds captured amount

These tests are:
	•	fast,
	•	local,
	•	diagnostic,
	•	stable under UI and infrastructure churn.

TDD loop
	1.	write a failing test,
	2.	write the smallest implementation that passes,
	3.	refactor with tests green,
	4.	add edge cases,
	5.	repeat.

What TDD is for

TDD is best for:
	•	dense logic,
	•	transformations,
	•	state transitions,
	•	business rule evaluation,
	•	idempotency handling,
	•	regression prevention.

What TDD is not for

TDD is not a requirement to force trivial tests around every line of code.
Do not write pointless tests for passive structure or framework glue if the value is negligible.

⸻

Testing Pyramid Mapping

A frequent confusion is treating BDD, SDD, and TDD as if they were all test levels.
They are not.

Here is the practical mapping:

BDD influences
	•	acceptance tests,
	•	E2E scenario selection,
	•	integration scenario selection,
	•	review criteria.

SDD influences
	•	contract tests,
	•	migration checks,
	•	state-machine tests,
	•	observability checks,
	•	performance and failure-path validation.

TDD influences
	•	unit tests,
	•	component tests,
	•	focused integration tests for module behavior.

E2E validates
	•	a limited number of critical, cross-boundary flows.

This distinction matters because otherwise teams over-invest in slow system tests and under-invest in precise local tests.

⸻

Concrete End-to-End Example

Example feature: Customer cancels a paid order

Step 1: BDD

Scenario: Customer cancels a paid unfulfilled order
  Given an order is PAID
  And the order is not fulfilled
  When the customer cancels the order
  Then the order becomes CANCELLED
  And refund processing starts
  And inventory is restored
  And an audit entry is recorded

Scenario: Customer cannot cancel a shipped order
  Given an order is SHIPPED
  When the customer cancels the order
  Then the request is rejected
  And no refund is created

Step 2: SDD

Key details:
	•	allowed order states,
	•	idempotency key strategy,
	•	async refund behavior,
	•	event schema,
	•	audit requirements,
	•	timeout and retry handling,
	•	backward compatibility for existing order events.

Step 3: TDD

Write tests for:
	•	transition guard rules,
	•	duplicate cancel requests,
	•	refund amount calculation,
	•	audit entry creation contract,
	•	event emission payload integrity.

Step 4: Integration tests

Validate:
	•	cancel endpoint updates persistence correctly,
	•	refund job is enqueued,
	•	event is emitted.

Step 5: E2E

Validate one or two top-level flows:
	•	customer cancels eligible order successfully,
	•	customer cannot cancel shipped order.

This example shows that BDD is not “the last E2E step”.
BDD starts first; E2E closes the loop later.

⸻

Anti-Patterns

Anti-pattern 1: BDD only during product meetings

Problem:
BDD becomes a meeting ritual instead of an executable behavior source.

Consequence:
The team still implements from ambiguous tickets and later discovers that acceptance is unclear.

Correction:
Carry BDD scenarios into development, PR review, and acceptance tests.

⸻

Anti-pattern 2: SDD as architecture theater

Problem:
Teams write long design docs with no explicit invariants, no failure model, and no verification plan.

Consequence:
The document sounds sophisticated but does not constrain implementation.

Correction:
Keep SDD short and operational. Prefer:
	•	states,
	•	invariants,
	•	contracts,
	•	failure modes,
	•	rollout constraints.

⸻

Anti-pattern 3: TDD only after code exists

Problem:
Tests are written after implementation merely to ratify the current code.

Consequence:
The tests mirror implementation structure and fail to guide design or catch hidden edge cases.

Correction:
Start with behaviorally meaningful failing tests, especially around rules and boundaries.

⸻

Anti-pattern 4: E2E as a substitute for everything else

Problem:
Teams rely on slow end-to-end tests because lower-level tests are missing.

Consequence:
Feedback is slow, failures are hard to diagnose, and coverage remains weak.

Correction:
Push logic down into unit / component / integration tests, and keep E2E selective.

⸻

Anti-pattern 5: Letting the agent infer business truth

Problem:
The agent receives a vague prompt like “implement cancellation support” and fills in hidden rules.

Consequence:
The system looks complete but violates business expectations or existing invariants.

Correction:
Provide explicit scenarios, constraints, contracts, and test expectations first.

⸻

FAQ

Q1. Do we always need all three: BDD, SDD, and TDD?

Not always at the same weight.

For a tiny local change, a full write-up may be unnecessary.
But the logic still applies:
	•	behavior should be understood,
	•	constraints should be clear,
	•	verification should exist.

For non-trivial work, yes: all three concerns must be addressed, even if the artifacts stay lightweight.

⸻

Q2. Is BDD just Given/When/Then syntax?

No.
Given/When/Then is only a format.
BDD is about behavior clarity and acceptance semantics.
A badly written Given/When/Then scenario is still bad BDD.

⸻

Q3. Is SDD just a design doc?

No.
A design doc can be descriptive or speculative.
SDD is useful only when it constrains implementation with explicit boundaries, invariants, contracts, and failure behavior.

⸻

Q4. Is TDD still worth it when agents can generate tests?

Yes, and arguably more so.
Generated tests are valuable only if they are reviewed and used as gates.
The key value of TDD is not “humans typed the test by hand”.
The key value is that implementation is constrained by executable checks before code is trusted.

⸻

Q5. Should every BDD scenario become an E2E test?

No.
That would be expensive and brittle.
Some scenarios should be proven via:
	•	unit tests,
	•	component tests,
	•	integration tests,
	•	contract tests.

Reserve E2E for a narrow set of critical flows.

⸻

Q6. What should live in agents.md versus docs/engineering/...?

Use agents.md for:
	•	mandatory rules,
	•	non-negotiables,
	•	PR requirements,
	•	review requirements,
	•	artifact requirements.

Use the playbook for:
	•	rationale,
	•	examples,
	•	templates,
	•	anti-patterns,
	•	FAQs,
	•	adoption guidance.

⸻

Q7. What if the product requirement is still changing?

Then BDD becomes even more important, not less.
Write provisional scenarios with explicit assumptions.
Changing behavior is manageable if the scenarios and constraints are visible.
Unwritten behavior changes are what create drift.

⸻

Q8. What if a design note feels too heavy?

Reduce the size, not the precision.
A good short SDD note is often enough.
The point is not volume.
The point is explicit constraints.

⸻

Recommended Templates

Feature template

# Feature: <name>

## Goal
<business outcome>

## Scenarios
### Scenario: <happy path>
Given ...
When ...
Then ...

### Scenario: <rule boundary>
Given ...
When ...
Then ...

### Scenario: <failure path>
Given ...
When ...
Then ...

Design note template

# Design Note: <name>

## Context

## Scope

## Non-goals

## Domain Model

## Invariants

## Contracts

## Failure Model

## Non-Functional Requirements

## Verification Plan

PR template snippet

## Behavior
- Scenario(s): ...

## Design
- Related design note: ...
- Invariants: ...
- Contracts changed: yes/no

## Verification
- Unit: ...
- Integration: ...
- Contract: ...
- E2E / acceptance: ...

## Risks
- ...


⸻

Agent Prompting Guidance

For non-trivial tasks, a good agent prompt should include:
	•	the target scenario or BDD summary,
	•	the relevant design note,
	•	the module boundary,
	•	constraints or invariants,
	•	the required test layer,
	•	files to avoid changing unless necessary.

Example:

Implement order cancellation for paid but unfulfilled orders.
Follow docs/features/order-cancellation.md and docs/design/order-cancellation.md.
Preserve invariants:
- shipped orders cannot be cancelled
- duplicate requests must not create duplicate refunds
Add unit tests for transition guards and idempotency.
Add integration coverage for the cancel endpoint.
Do not modify unrelated checkout flow files.

Bad prompt:

Add order cancellation support.

The second prompt invites drift.

⸻

Adoption Guidance for Teams

Phase 1: Establish minimum discipline

Start with:
	•	short BDD scenarios for important features,
	•	short SDD notes for non-trivial changes,
	•	mandatory regression tests for bug fixes,
	•	PR template fields for behavior / design / verification.

Do not attempt a giant process rollout all at once.

⸻

Phase 2: Strengthen verification

Add:
	•	contract tests for cross-boundary changes,
	•	explicit state-machine tests,
	•	better integration coverage,
	•	selective E2E for the most critical user journeys.

⸻

Phase 3: Make agent workflows spec-first

Require non-trivial agent tasks to start from:
	•	scenario reference,
	•	design note reference,
	•	explicit invariants,
	•	test expectations.

At this phase, the team gets the real leverage of agent assistance without uncontrolled drift.

⸻

Review Heuristics

When reviewing work, ask:
	1.	Is the intended business behavior explicit?
	2.	Are the design boundaries and invariants explicit?
	3.	Is the implementation verified at the right layer?
	4.	Are edge cases and failure paths covered?
	5.	Would an agent or a new team member understand what must not change?

If the answer to the last question is “no”, the spec is still too implicit.

⸻

Final Guidance

Use this playbook to keep the team aligned on one principle:

Behavior must be explicit, constraints must be explicit, and correctness must be provable.

That is the operating model.
BDD, SDD, and TDD are simply the three tools we use to achieve it at different layers.




已经拆好了，两层职责现在是清晰的：
	•	agents.md：只保留稳定规则 / mandatory rules / non-negotiables
	•	docs/engineering/bdd-sdd-tdd-playbook.md：放解释、示例、FAQ、反例、落地建议

我这次做了两个关键收敛：

agents.md

现在是偏“仓库根规则”的硬约束版本，重点是：
	•	非 trivial task 不能直接无约束让 agent 开写
	•	BDD / SDD / TDD 各自什么时候是必需的
	•	bug fix 必须带 regression test
	•	cross-boundary change 必须有 contract awareness
	•	PR 和 review 最低要求
	•	agents.md 与 playbook 的边界

docs/engineering/bdd-sdd-tdd-playbook.md

现在是偏“团队操作手册”的解释型版本，重点是：
	•	为什么 agent 时代这套方法更重要
	•	BDD / SDD / TDD / E2E 的边界与关系
	•	一个完整 feature 的端到端示例
	•	常见反模式
	•	FAQ
	•	agent prompt 写法建议
	•	团队 adoption 的分阶段建议

这套结构已经适合进真实仓库了，但还差最后一步“仓库化”收口。真正要落地，我建议你下一步继续做这 3 个配套件，否则文档会变成“看起来很对，但无法强执行”：
	1.	PR_TEMPLATE.md
把 Behavior / Design / Verification / Risks 变成强制字段。
	2.	docs/engineering/templates/
把我写在 playbook 里的几个模板拆成单独文件，比如：

	•	feature-template.md
	•	design-note-template.md
	•	bugfix-template.md

	3.	CI / review policy 对应项
例如把这些变成明确检查项：

	•	非 trivial 改动没有 design note 时阻断 review
	•	bugfix 没 regression test 不过
	•	改 API / event 没 contract 说明不通过

你现在真正应该追问自己的两个问题是：
	1.	你想让这套规范主要服务 人类协作，还是主要服务 agent 提示与约束？这会影响文档写法。
	2.	你们团队最常失败的是 需求错、设计漂移、还是回归 bug？这个决定 agents.md 里哪条规则要写得更硬。
