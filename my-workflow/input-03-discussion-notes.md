# Workflow 设计讨论纪要

## 目的

记录当前关于可拔插 workflow 的关键讨论结论，作为后续第三方评审和方案对比的输入材料。本文不是最终设计稿，也不是执行规范；它的作用是固定共识、暴露分歧、减少重复讨论。

## 当前目标

设计一套覆盖 `trivial → simple → moderate → complex → harness` 的可拔插 workflow。

核心约束不是“先做最小流程，以后再慢慢加”，而是：

- 先定义完整骨架
- 后续只允许按 profile 做减法
- 不允许未来再往核心流程里临时加 phase / artifact / gate，因为这会改变流程协议面并破坏兼容性

换句话说，simple 任务可以跳过环节，但那些环节在核心骨架里必须已经有正式槽位。

## 讨论中形成的主要判断

### 1. 可拔插的前提是先冻结完整骨架

workflow 应先冻结这些稳定契约：

- `phase graph`
- `artifact schema`
- `gate result schema`
- `checkpoint schema`
- `acceptance/backflow schema`

profile 只是在这个完整骨架上裁剪启用项，而不是定义另一套流程。

### 2. 不把 spec 当长期主记忆

spec 在任务执行期有价值，但在任务完成后天然会落后于代码实现。继续把历史 spec 当主召回材料，会把后续任务拖回陈旧上下文。

因此更合适的分层是：

- `spec / plan / tasks` = 执行期文档
- `ADR / decision log` = 决策期文档
- `acceptance result / backflow docs` = 长期记忆文档

结论：

- 需要 spec，但 spec 不是长期 source of truth
- spec 是 transient artifact
- acceptance 结束后的结算结果才是 durable artifact

### 3. 验收结束后的“结算结果”必须是一等公民

任务不应在“代码写完 / 测试过了”时结束，而应在“输出结算结果并完成知识回流”时结束。

这个结算结果至少应回答：

- 改了什么
- 当前行为是什么
- 对外接口有无变化
- 架构边界有无变化
- 哪些决策被确认
- 验证做了什么
- 还有哪些残余风险
- 哪些信息要进入长期文档
- 下一个任务应该继承什么知识

### 4. 长期保留的文档应该只保留高价值信息

长期文档优先保留：

- 当前代码架构
- 对外接口契约
- 关键决策与不变量
- 失败模式 / 验证策略 / 可复用经验

不应默认保留为长期主记忆的内容：

- 中间推理过程
- 已放弃方案的大段讨论
- 临时任务拆解
- 已被最终代码完全覆盖的描述性 spec

### 5. 后续任务默认加载 durable docs，而不是历史 spec

后续任务默认应优先读取：

- 当前架构文档
- 当前接口文档
- ADR / decision log
- 经验回流摘要

只有在这些场景下才回查旧 spec：

- 追溯某次变更历史
- 验收争议
- 回滚分析
- 审计 / 合规

## 对候选机制的阶段性判断

这里的分类不是简单的 `ADOPT / REJECT`，而是按是否进入核心协议面来划分。

### Core Required

- `D4` Sprint contract：核心里必须有 execution contract 槽位，默认在 harness 启用
- `D5` ADR：核心里必须有 decision record 槽位，复杂变更启用
- `E5` Deterministic state ops：共享状态修改必须经过确定性边界，哪怕早期实现很轻
- `F7` 三层检查点：核心安全网
- `J5` Session/task evaluation：核心里必须有 retrospective/backflow 槽位
- `K5` Prompt injection scan：核心安全预检

### Core Optional

- `E7` 脏原型重构模式：外部模型路径启用
- `F3` pass@k：verifier 能力预留，但默认关闭
- `G3` rubric：evaluator 输出结构预留，但不是所有任务启用

### Plugin Extension

- `F9` Kotlin/Swift 反模式 grep：保留 hook 槽位，不进通用 workflow 内核

### Out

- `B3` 的固定 6 文档形态：不进入核心
- `J1` 两层记忆
- `J2` instinct 衰减
- `J3` journal

## 对 spec / ADR / 验收文档的最新定位

### Spec

作用：

- 约束当前任务的目标、边界、验收条件
- 为 plan 和 implementation 提供执行上下文

特性：

- 临时
- 可在执行中修正
- 默认不进入长期主上下文

### ADR / Decision Log

作用：

- 记录为什么这样设计
- 记录哪些 trade-off 已确认
- 记录哪些边界后续任务不能破坏

特性：

- 长期保留
- 但只记录关键决策，不记录整段实现推理

### Acceptance Result / Backflow

作用：

- 作为任务闭环的最终产物
- 从一次变更中提炼 durable knowledge

特性：

- 长期保留
- 是未来任务的高价值召回源

## 当前推荐的文档分层

### 1. transient

- `spec`
- `plan`
- `tasks`

### 2. decision

- `ADR`
- `decision log`

### 3. durable

- architecture docs
- interface / API docs
- invariants
- lessons / retrospective summary
- acceptance settlement / backflow summary

## 需要第三方重点评审的问题

1. 对一个可拔插 workflow 来说，哪些 phase / artifact 必须进入核心协议面，哪些只该作为 profile 或插件扩展？
2. 如果不把 spec 作为长期 source of truth，acceptance/backflow 的最小 schema 应该是什么？
3. ADR 应该在什么触发条件下生成，才能避免 spec theater？
4. “完整骨架先冻结，profile 只做减法” 这个原则下，哪些机制必须现在预留槽位，即使默认关闭？
5. durable docs 的最小集合应该是什么，才能对下一个任务真正有帮助？

## 当前未决问题

- acceptance result 和 retrospective 是一个文档还是两个文档
- architecture docs 与 module README 的边界如何划分
- durable docs 的注入策略是全局加载、按任务匹配加载，还是两者结合
- deterministic state ops 的最小实现应该是脚本、CLI，还是约束少数受保护文件

## 结论

当前讨论已经形成一个方向明确的共识：

- 先冻结完整 workflow 骨架
- profile 只做减法
- spec 保留，但只作为执行期文档
- acceptance/backflow 才是长期记忆中心
- ADR 保留“为什么”，durable docs 保留“现在是什么”

后续第三方方案应围绕这个前提展开，而不是重新回到“spec 是否应该长期主导一切”的旧路径。
