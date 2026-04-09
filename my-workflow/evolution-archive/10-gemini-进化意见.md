# Gemini 进化意见

> 本文保留原 `my-workflow-v2/` 里的具体实现要点，不只讲抽象差异。目标是：以后只维护 `my-workflow/`，但 `v2` 的机制、schema、phase 改写和关键片段都还能在这里查到。

## 1. 总体判断

`v2` 不是在 `v1` 上修修补补，而是一次明显的重心迁移：

- `v1` 的主轴：**冻结 6 phase 骨架 + artifact/gate/profiles**
- `v2` 的主轴：**约束驱动 + 精确上下文注入 + 强制对账闭环**

一句话概括：

- `v1` 更像“workflow protocol skeleton”
- `v2` 更像“agent-era implementation philosophy”

## 2. 总体层面的具体变化

## 2.1 总纲改写

`v1` 的总纲强调：

- 固定 6 phase
- profile 只做减法
- transient / durable / decision 分层
- verify over self-report

`v2` 的总纲直接替换成下面这组设计哲学：

```md
1. 约束驱动 (SDD -> BDD -> TDD)
2. 上下文精确注入 (JSONL-Driven Context)
3. 强制对账防漂移 (PAUL Reconcile)
4. 验证优先于自报告 (Ralph Loop)
5. 产物分层与生命周期
```

这不是措辞变化，而是控制面的变化。

## 2.2 六阶段名称的具体变化

`v1`：

```text
Phase 0: TRIAGE        — 复杂度评估与路由
Phase 1: DISCOVER      — 需求澄清 + 代码理解 + 人类确认理解
Phase 2: SPEC & PLAN   — 规格化 + 技术方案 + 任务拆解 + ADR
Phase 3: EXECUTE       — 编码 + 内循环修复 + Delta 处理
Phase 4: VERIFY        — 三层检查点 + 质量 gate + 人类验收
Phase 5: SETTLE        — 结算 + Backflow + Transient 归档/销毁
```

`v2`：

```text
Phase 0: TRIAGE        — 复杂度评估、路由与上下文预算管控
Phase 1: DISCOVER      — 需求澄清 + 探索 + JSONL 上下文配置
Phase 2: SPEC & PLAN   — 约束建模(SDD) + 验收场景(BDD) + 测试计划(TDD)
Phase 3: EXECUTE       — JSONL 精确注入 + TDD 循环 + Delta 处理
Phase 4: VERIFY        — 三层检查点 + Ralph Loop 防逃逸 + 人类验收
Phase 5: SETTLE        — PAUL 强制对账(Reconcile) + 知识回流 + 归档
```

这里最重要的不是名字，而是每个 phase 的责任重新定义了。

## 2.3 产物模型的具体变化

`v1` 的 transient 核心是：

- `code-understanding.md`
- `spec.md`
- `plan.md` / `tasks.md`
- `delta-log.jsonl`

`v2` 把其中 3 个产物的含义改了：

```md
| Artifact | 核心作用 | Schema 特征 |
|----------|----------|-------------|
| context.jsonl | 决定 Agent 能看到什么代码/文档 | {"file": "...", "reason": "..."} |
| spec.md | SDD 约束与 BDD 场景 | Invariants, Contracts, Given/When/Then |
| plan.md / tasks.json | 任务拆解与 TDD 测试计划 | 单步 Action + Verify Command |
| delta-log.jsonl | 执行期变更与偏差记录 | Append-only 增量 |
```

另外，`v2` 把结算产物显式换成：

```text
reconcile-settlement.json
```

它不只是 settlement 记录，而是 PAUL 风格的 planned-vs-actual 对账单。

## 3. 分文件差异与具体实现

## 3.1 `00-overview.md`

### v1 的结构重点

- profile 裁剪矩阵
- artifact 生命周期表
- gate 模型表
- extension model

### v2 保留的具体实现

`v2` 在 overview 里增加了 3 个明确的实现重心：

```md
1. 约束驱动 (SDD -> BDD -> TDD)
2. 上下文精确注入 (JSONL-Driven Context)
3. 强制对账防漂移 (PAUL Reconcile)
```

以及下面这组 durable 产物定义：

```md
| Artifact | 核心作用 | 更新时机 |
|----------|----------|----------|
| docs/adr/ | 跨边界/新依赖的架构决策记录 | Phase 2 条件触发 |
| reconcile-settlement.json | 任务结算与防漂移对账单 | Phase 5 强制生成 |
| docs/architecture.md | 当前架构高层视图 | Phase 5 Backflow |
| docs/interfaces.md | 对外接口契约 | Phase 5 Backflow |
| docs/invariants.md | 项目铁律/不变量 | Phase 5 Backflow |
| lessons.jsonl | 经验教训回流 | Phase 5 Backflow |
```

### 判断

这部分值得保留的是：

- 用 `reconcile-settlement.json` 明确替换泛化的 settlement
- 把 `spec.md` 从普通规格文档升级为“约束 + 场景”的载体

不值得保留的是：

- `v2` 把原先很有价值的 profile/gate/artifact 表压缩得太狠

## 3.2 `02-discover.md`

### v1 的重点

- 代码理解摘要
- `G1: Understanding Confirm`

### v2 的具体实现

`v2` 里 Discover 被重写成“上下文配置阶段”，核心输出是：

```md
context.jsonl
```

它的角色定义是：

```md
- 生成：在 Phase 1，输出 context.jsonl，明确声明所需文件集
- 注入：通过 PreToolUse hook 或外层 runner，把 JSONL 指向的文件内容注入 prompt
- 隔离：不同 Worker 可以有不同的 JSONL，切断并行 Agent 的上下文污染
```

`v2` 对 `context.jsonl` 的最小 schema 也给得很明确：

```json
{"file": "src/auth/login.ts", "reason": "需要修改验证逻辑"}
```

### 判断

这块是 `v2` 必须保留的具体实现，不该只写成一句“精确注入上下文”。

## 3.3 `03-spec-and-plan.md`

### v1 的重点

- spec / plan / tasks / ADR
- plan 固定 schema

### v2 的具体实现

`v2` 不是抽象说“更重视约束”，而是把这一 phase 改成了明确的三步：

```text
Step 2.1 SDD: 定义边界、不变量、契约、错误模型、non-goals
Step 2.2 BDD: 定义 Given/When/Then 场景
Step 2.3 TDD: 生成 plan.md 和 tasks.json，并绑定测试与 verify command
```

`v2` 给出的 `spec.md` 结构是具体可用的：

```md
## SDD 约束 (Constraints & Boundaries)
- Scope: 本次只修改 auth 模块
- Non-goals: 不涉及 session 存储迁移
- Invariants: 用户状态转移必须通过状态机，不可直接改 DB 字段
- Contracts: POST /api/login 响应格式不变

## BDD 验收场景 (Acceptance Scenarios)
### Scenario 1: 正常登录
Given 用户在白名单中
When 提交正确密码
Then 返回 JWT Token
And 记录登录成功日志
```

同时，`tasks.json` 的要求也被具体化为：

```md
每个 Task 必须包含：
- 对应的 TDD 单元测试/集成测试
- 实现步骤
- 明确的验证命令 (Verify Command)
```

### 判断

这部分是 `v2` 最值得保留的实现，因为它把“约束驱动”真正落成了文档协议。

## 3.4 `04-execute.md`

### v1 的重点

- baseline plan
- task execution loop
- build-fix loop
- delta re-entry

### v2 的具体实现

`v2` 没有泛泛说“加强执行纪律”，而是把执行循环重写成：

```text
Step 3.1 Pre-Execute Context Injection
  根据 context.jsonl，只向当前 worker 注入必要上下文

Step 3.2 TDD 执行循环 (Red-Green-Refactor)
  a. 读取 task 的 BDD/SDD 约束
  b. RED: 先写或更新测试，运行确认失败
  c. GREEN: 写业务代码，运行确认通过
  d. REFACTOR: 优化实现，保持测试为绿
```

`v2` 还把禁止项写得很明确：

```md
禁止 Agent 凭记忆写大段代码
要求严格按 task 进行小步提交与验证
```

### 判断

这块值得并回主线的不是“TDD”三个字，而是这条具体执行协议。

## 3.5 `05-verify.md`

### v1 的重点

- 三层检查点
- 轻量工程质量审查
- Ralph Loop
- 人类验收

### v2 的具体实现

`v2` 的三层检查点写成了更具体的形式：

```text
Quick: Lint / Format / Typecheck
Standard: Unit Tests + 覆盖率检查
Full: Integration / Contract / BDD 场景验收测试
```

同时把独立审查写成了明确的双角色：

```text
Spec Reviewer:
  对照 spec.md 检查业务与边界

Quality Reviewer:
  检查坏味道、性能、安全性
```

`Ralph Loop` 在 `v2` 里也不是概念，而是很具体的拦截条件：

```md
必须在回答中包含验证命令的实际标准输出 (stdout)
无证据 -> 打回
```

### 判断

这部分不需要重写骨架，但值得把 `stdout evidence` 这种硬条件并回 `v1`。

## 3.6 `06-settle.md`

### v1 的重点

- settlement schema
- backflow
- transient cleanup
- deliver

### v2 的具体实现

`v2` 把这一 phase 直接替换成 PAUL 风格的 reconcile：

```text
Step 5.1 PAUL 强制对账
  基于 spec, plan, delta-log 对比结果
  输出 reconcile-settlement.json

Step 5.2 Backflow
  更新 architecture / interfaces / invariants / lessons

Step 5.3 Transient Cleanup
  销毁或归档 spec.md, plan.md, context.jsonl, delta-log
```

这里的关键句应该保留原样的力度：

```md
没有对账，就没有闭环；没有闭环，就会产生历史漂移。
```

### 判断

这块也不是抽象理念，而是一个明确的 closure 协议。应该并入主线。

## 3.7 `07-cross-cutting.md`

### v1 的重点

- 状态管理
- 可观测
- 安全
- hooks
- config

### v2 的具体实现

`v2` 在横切层里重点补了三类“行为约束”：

1. Trellis 风格 JSONL 注入
2. Deny-first 写保护
3. Anti-rationalization

其中最具体的是 anti-rationalization 清单：

```md
常见借口与反驳：
- "This is just a simple string change." -> 只要是行为变更，必须有 BDD/TDD 支持
- "I can check git/files quickly." -> 不，必须先阅读 context.jsonl
- "The skill is overkill." -> 简单事物容易变复杂，执行纪律不可妥协
```

### 判断

这部分的微协议值得保留，但 `v2` 不该因此弱化 `v1` 原有的状态/配置/可观测体系。

## 3.8 `08-reference-map.md`

### v1 的重点

- 按 phase 索引设计来源

### v2 的具体实现

`v2` 把 reference map 改成了按机制索引：

```md
| 机制/模式 | 参考框架 / 来源 | 解决的痛点 | 在本工作流的位置 |
|----------|----------------|-----------|-----------------|
| JSONL-Driven Context | Trellis | 减少 Context Rot | Phase 1 / Phase 3 / Cross-cutting |
| PAUL Reconcile | PAUL | 防止 Execution Drift | Phase 5 |
| SDD/BDD/TDD 漏斗 | TDD/BDD/SDD 研究 | 缩小幻觉空间 | Phase 2 / Phase 3 |
| Anti-Rationalization | Superpowers | 封堵跳步借口 | Cross-cutting |
```

### 判断

这个改法是对的，因为它更适合未来继续演进。

## 4. `v2` 里最值得保留的具体实现清单

如果只保留最有价值、最具体、最可并回主线的部分，我建议是这 7 项：

1. `context.jsonl` 及其最小 schema
2. `SDD -> BDD -> TDD` 这条 phase 2 的具体漏斗
3. `spec.md` 的“约束 + 场景”结构
4. `tasks.json` 里强制要求 `verify command`
5. `Red -> Green -> Refactor` 的执行循环
6. `stdout evidence` 版 Ralph Loop
7. `reconcile-settlement.json` 作为唯一 closure artifact

## 5. 不建议直接照搬的部分

不建议原样照搬的，是这 4 项：

1. 用 `v2` 全量替换 `v1`
   - `v2` 强化了方法论，但删掉了很多 `v1` 已有的协议细节
2. 弱化 `v1` 的 profile 矩阵
   - `v1` 的 profile 设计更完整
3. 弱化 `07-cross-cutting.md` 的状态/配置/可观测层
   - 这些是骨架级基础设施，不该被削薄
4. 保留一个 `my-workflow-v2/` 平行目录
   - 这会让骨架和方法论版本长期漂移

## 6. 最终建议

最合理的处理方式不是保留 `my-workflow-v2/`，而是：

1. 保留 `my-workflow/` 作为唯一主目录
2. 用本文保存 `v2` 的具体实现
3. 后续把本文中的高价值机制逐步回写到主线文档

一句话总结：

`v1` 是骨架版，`v2` 是方法论增强版；  
应该做的是“把 v2 的具体实现并回 v1 主线”，而不是长期维护一个平行目录。
