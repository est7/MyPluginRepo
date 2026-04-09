# Codex 进化意见

> 目标：基于 `docs/how-to-explore-a-agent-workflow/` 的 11 份文档与 `docs/research/` 的 8 份研究，共 19 份材料，提炼成熟框架里真正可迁移的设计技巧，用于升级当前 `my-workflow` 骨架。

## 1. 本轮研究后的核心判断

这 19 份材料虽然表面差异很大，但底层反复收敛到 8 条工程规律：

1. **phase 只是骨架，真正的控制面是 artifact + gate + transition rule**
2. **状态必须外部化，且最好是协议化，而不是散落在对话记忆里**
3. **完成不能靠 agent 自报，必须靠 verify 证据和 reconcile/settlement 关闭**
4. **plan 不只是说明文档，更应该是 agent 间通信协议**
5. **并行不是默认权利，只能发生在切片清晰、依赖显式、可独立验证的边界内**
6. **长任务稳定性的关键不是“继续聊”，而是 fresh-context + 结构化 handoff**
7. **软约束只能塑形，关键路径必须有硬门禁**
8. **复杂流程必须支持 ceremony compression，否则 simple 任务一定绕开系统**

## 2. 这些判断主要来自哪些框架

为了避免“结论正确但来源模糊”，这里把高价值结论按来源簇归一下：

- **GSD / FlowSpec / Trellis**
  - 强调 gate taxonomy、artifact-driven transition、plan validator、stall detection、dispatcher/worker 分层
- **PAUL / OpenSpec / Spec Kit**
  - 强调 AC-first、reconcile closure、spec delta、change 审计、分层 artifact 生命周期
- **ECC-Mobile / Anthropic Harness / yoyo-evolve**
  - 强调 fresh-context、checkpoint/handoff、评估器分离、plan-as-protocol、boundary nonce
- **Superpowers / CCG / OMC**
  - 强调 anti-rationalization、工艺纪律、subagent 角色边界、worktree/并行施工约束

这意味着当前 `my-workflow` 不需要“再发明一套 phase”，而是要把这些已经被反复验证的控制技巧补到协议层。

## 3. 当前 `my-workflow` 已经吸收得不错的部分

当前方案已经抓住了 5 个正确的大方向：

- 固定 6 phase 骨架，profile 只做减法
- transient / decision / durable 分层清楚
- Delta re-entry、3-layer checkpoint、settlement/backflow 已经成型
- 认可 verification-over-self-report
- 明确排斥 memory-first / journal-first / 动态加 phase

这些判断是对的，不建议推倒重来。

## 4. 当前方案还缺的关键能力

对照 19 份材料，当前骨架还缺 7 个真正影响可靠性的点：

### 4.1 缺少“切片协议”

当前有 phase，但还没有 **slice** 这一层。  
这会导致 Complex/Harness 任务在 `EXECUTE` 内继续膨胀，最后变成长会话承压。

建议新增：

- `slice.md`：本轮只处理的 AC、边界、涉及模块、退出条件
- `wave.json`：并行任务分组及依赖关系
- `handoff.md`：fresh-context 恢复时只交接当前 slice 的结构化状态

### 4.2 缺少“Reconcile 是唯一关闭条件”

现在 `SETTLE` 很强，但还没有把“对账失败则不得关闭”定义成更强的协议。

建议强化为：

- `SETTLE` 不是收尾说明，而是 **Planned vs Actual** 的强制对账
- `DONE_WITH_CONCERNS` 不得直接进入 `DONE`
- 没有 AC 逐条 PASS/FAIL 结果，不允许 task close

### 4.3 缺少“Plan as Protocol”的硬化版本

当前 `spec.md` / `plan.md` schema 已经比很多框架好，但还不够协议化。

建议补齐：

- `plan.json` 作为 machine-checkable 协议
- `plan-validator` 作为 `G2` 前的硬校验
- `dependsOn`、`owner`、`verification`、`rollback`、`allowed_paths` 成为必填字段

### 4.4 缺少“失败路由 taxonomy”

现在有 failure path，但还没统一成一套故障分类。

建议把 gate 失败统一分成 4 类：

- `preflight`：前置条件不满足，阻断
- `revision`：可修复，回生产者
- `escalation`：需要用户决策
- `abort`：继续执行会扩大损害，直接停

这样 `TRIAGE` 到 `SETTLE` 的失败处理会更一致。

### 4.5 缺少“inner loop / outer loop”分层

当前 `VERIFY` 已经吸收了 reviewer 思路，但还没有把角色边界写透。

建议明确：

- `inner loop`：discover / implement / bug-fix / local verify
- `outer loop`：spec review / architecture check / acceptance / settle

原则：inner loop 不能改目标函数，outer loop 不直接写实现。

### 4.6 缺少“fresh-context 优先”的恢复策略

当前 `07-cross-cutting.md` 已经有 pause/resume，但还偏“继续会话”。

建议升级为：

- Complex+ 默认优先 `checkpoint + fresh-context resume`
- `resume` 加载顺序固定：`state -> durable -> current slice -> last verify evidence`
- 恢复不依赖历史对话，只依赖结构化产物

### 4.7 缺少“反漂移微协议”

成熟框架普遍用了很多小而硬的行为约束，当前骨架还没有显式吸收。

建议加入：

- completion markers：`DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT`
- bounded revision loop：最大迭代次数 + stall detection
- anti-rationalization checklist：提前封堵“先跳过测试/先不写计划/先不回填文档”这类偷跑理由

## 5. 三个演进选项

### Option A：Guardrail-First

思路：不改 6 phase，只补硬门禁和微协议。

新增重点：

- `plan.json` + validator
- gate taxonomy
- completion markers
- bounded revision loop
- stronger settle/reconcile schema

优点：

- 改动最小
- 能快速提高稳定性
- 不会破坏现有文档结构

代价：

- 并行编排、fresh-context、slice 控制仍然偏弱
- 更像 v1.5，不是 v2

适用：

- 你想先把当前骨架补强，而不是重设计

### Option B：Protocol-First

思路：保留 6 phase，但在 phase 之下新增 `slice -> wave -> reconcile` 控制层。

新增重点：

- `slice.md` 作为执行闭包
- `wave.json` 作为并行协议
- `plan.json` 作为 agent 通信协议
- `handoff.md` 作为 fresh-context 恢复载体
- `reconcile.md/json` 作为唯一 closure artifact

优点：

- 最平衡
- 既吸收 GSD/ECC-Mobile/Trellis/PAUL 的强项，又不把系统做成重型 harness
- 能真正解决长任务漂移、并行越界、恢复不稳

代价：

- 文档和 hooks 会比现在多一层
- Moderate 以下 profile 需要设计 ceremony compression

适用：

- 这是我建议的主路线

### Option C：Harness-First

思路：把 `my-workflow` 从“文档骨架”升级为“控制平面 + 执行平面”双层架构。

新增重点：

- pure dispatcher
- planner / implementer / evaluator / synthesizer 分工
- state namespace（按 task-id/slice-id 隔离）
- full checkpoint/restart orchestration

优点：

- 最接近 Trellis / Anthropic Harness / ECC 这类高强度系统
- 最有利于 Harness profile

代价：

- 复杂度显著上升
- 对 hooks、工具、runner 的实现要求更高
- simple/moderate 任务容易被拖重

适用：

- 只适合把 `my-workflow` 做成长期运行的 agent harness 时再上

## 6. 推荐路线

推荐采用 **B 为主，A 先落，C 只做远期预留**。

具体顺序：

1. **先落 A**
   - 强化 `plan.json`
   - 强化 `reconcile`
   - 引入 gate taxonomy、completion markers、stall detection
2. **再落 B**
   - 在 `EXECUTE/VERIFY/SETTLE` 下引入 `slice / wave / handoff`
   - 把复杂任务从“长 phase”变成“多个可关闭 slice”
3. **最后只为 Harness 预留 C**
   - 不直接让所有 profile 都背负 dispatcher/harness 成本

## 7. 对现有文档的具体改造建议

如果按推荐路线继续演进，建议后续按下面方式修改现有文件：

- `03-spec-and-plan.md`
  - 新增 `plan.json` schema
  - 新增 `execution contract` / `slice contract`
- `04-execute.md`
  - 新增 `slice`、`wave`、`owner`、`allowed_paths`
  - 新增 `bounded revision loop` 和 `stall detection`
- `05-verify.md`
  - 拆分 `spec fit` 与 `quality fit`
  - 把 `completion markers` 和 verify evidence 写成协议
- `06-settle.md`
  - 强化 `reconcile`，要求逐条 AC 对账
  - 增加 `DONE_WITH_CONCERNS` 的禁止直闭规则
- `07-cross-cutting.md`
  - 增加 `fresh-context resume`
  - 增加 `state namespace`
  - 增加 `gate taxonomy`

## 8. 最终判断

当前 `my-workflow` 的问题不是骨架错了，而是**协议层还偏薄**。  
下一步最值得做的，不是再加 phase，也不是再堆 artifact，而是把下面 4 个东西做硬：

1. `plan` 变协议
2. `execute` 变切片
3. `verify` 变证据
4. `settle` 变对账

这 4 件事一旦补上，当前设计会从“结构清楚的 workflow 文档”升级成“更接近成熟 harness 的可执行协议面”。
