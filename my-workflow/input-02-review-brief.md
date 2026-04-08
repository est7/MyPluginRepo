# Workflow 第三方评审简报

## 你要解决的问题

请为一个代码代理工作流系统设计一套方案。这个系统不是单一固定流程，而是覆盖 `trivial → simple → moderate → complex → harness` 的可拔插 workflow。

这里的“可拔插”有一个严格含义：

- 核心流程必须先完整定义
- 不同复杂度 profile 只能跳过、降级或关闭某些环节
- 不能依赖“以后再往流程里加一个 phase / artifact / gate”

原因很简单：对一个已经被工具、命令、hooks、state machine 识别的 workflow 来说，后续新增核心环节属于破坏性变更；而预留槽位后做减法不是。

## 设计前提

### 1. 先冻结骨架，再做裁剪

方案必须先给出完整核心逻辑，然后再说明不同 profile 如何裁剪。

### 2. spec 不是长期主记忆

我们不接受把历史 spec 持续当作主召回源的设计。

原因：

- spec 在实现完成后天然落后于代码
- spec 常含大量中间推理和临时拆解
- 这些内容会干扰后续任务

我们接受 spec 的存在，但仅限于执行期。

### 3. 任务闭环必须以 acceptance/backflow 结束

任务完成不等于“代码写完”。任务真正结束时，必须产出一个结算结果，并从中提炼长期有用的信息。

### 4. 长期文档只保留高价值、可复用信息

长期保留的内容应优先包括：

- 当前架构
- 对外接口
- 关键决策与不变量
- 验证方式
- 经验回流

不应默认长期保留：

- 中间推理过程
- 大量候选方案讨论
- 临时任务拆解

## 我们当前认可的文档角色划分

### transient artifacts

- spec
- plan
- tasks

### decision artifacts

- ADR
- decision log

### durable artifacts

- architecture docs
- interface / API docs
- invariants
- acceptance settlement / backflow summary
- lessons / retrospective summary

## 希望第三方方案回答的问题

1. 这套 workflow 的最小完整骨架应该是什么？
2. 哪些 phase 必须进入核心协议面，哪怕默认关闭？
3. acceptance/backflow 的最小 schema 应该如何定义，才能替代“spec 作为长期 source of truth”？
4. ADR 应该如何触发，才能既保留设计原因，又避免文档负担过重？
5. durable docs 应该如何组织，才能真正帮助下一个任务，而不是制造新的上下文噪音？
6. 如何让 simple 任务保持轻，而 complex / harness 任务又能严格执行完整流程？

## 希望方案明确输出的内容

第三方方案至少应包含以下内容：

### 1. 核心 phase graph

要求：

- 明确 phase 顺序
- 明确可跳过条件
- 明确哪些 profile 启用哪些 phase

### 2. artifact model

要求：

- 每个 artifact 的作用
- 生命周期
- 是否 transient / decision / durable
- 谁创建、谁消费、谁更新

### 3. gate model

要求：

- 每个 gate 的输入与输出
- hard / soft / optional 的区别
- 在不同 profile 下是否启用

### 4. acceptance/backflow design

要求：

- 任务结算文档的固定结构
- 从结算结果回流到长期文档的规则
- 后续任务默认加载哪些 durable docs

### 5. extensibility model

要求：

- core required
- core optional
- plugin extension
- out

方案必须明确哪些能力属于这四类。

## 当前我们已经倾向的机制分类

### Core Required

- Sprint contract / execution contract 槽位
- ADR / decision record 槽位
- deterministic state mutation boundary
- 三层检查点
- task-end retrospective / backflow
- prompt injection scan

### Core Optional

- 外部模型“脏原型”重构路径
- pass@k / reliability metric
- rubric evaluator

### Plugin Extension

- 平台特定反模式检查

### Out

- 固定 6 文档模型
- memory-first / journal-first 设计

## 不希望看到的方案倾向

- 把 spec 当长期 source of truth
- 通过不断往核心流程中追加 phase 解决问题
- 用大量文档层级替代清晰协议面
- 把长期记忆做成 session 日志堆积
- 用“以后再加”来回避当前必须冻结的核心契约

## 建议第三方重点评估的取舍

- spec-first 与 acceptance-first 的边界
- ADR 的收益与 ceremony 成本
- state file 自由编辑 vs deterministic mutation boundary
- 轻量 profile 的顺滑体验 vs 重型 profile 的治理强度
- durable docs 的丰富度 vs 上下文噪音

## 交付目标

我们需要的不是“更多灵感”，而是一套能落入工程系统的稳定骨架：

- 核心协议面先冻结
- profile 只做减法
- spec 服务执行
- acceptance/backflow 服务长期记忆
- durable docs 优先服务下一个任务

如果第三方方案无法正面回答这几个点，就不适合作为下一轮设计输入。
