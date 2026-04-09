# 15. Hooks + State Machine + Fresh Session 讨论稿

> **定位**：针对 `14-thatall.md` 之后的下一层控制面讨论。
>
> **问题**：
> 1. 在 `TRIAGE` 确认复杂度之后，是否应该显式切到由 hooks 驱动的状态机强约束？
> 2. 对 `complex+`，是否应该强制 `fresh session per unit`？

---

## 0. 先给结论

我的判断是：

1. **应该引入显式状态机强约束**，但**状态机才是真相源，hooks 只是事件入口和阻断器**。
2. `TRIAGE` 一旦锁定 profile，后续 phase/gate/closure 要切到该 profile 对应的状态机，不应继续靠 prompt 自觉执行。
3. `complex+` 应该引入 **fresh session per unit**，但默认 unit 不应是最小 task，而应是 **slice**。
4. **task 级 fresh session** 适合 worker/subagent 隔离执行，不适合做 orchestrator 的默认粒度，否则 handoff 成本会压垮吞吐。

换句话说，不是 “hook-first”，而是：

```text
profile locked at triage
  -> choose workflow state machine
    -> hooks enforce transition and boundary
      -> session reset happens at unit boundary
```

---

## 1. 为什么现在该讨论这个

`14-thatall.md` 已经把主链冻结成：

```text
AC -> tasks.json -> verify-evidence.json -> reconcile-settlement.json
```

但它仍然有一个空位没有完全落死：

- 谁来阻止 phase 越界？
- 谁来阻止“没证据先宣布完成”？
- 谁来决定什么时候必须 fresh context？

如果这些问题继续只放在 prompt 里，协议会再次退化成“写得很严，但可绕过”。

所以现在真正该补的不是再发明新文档，而是把：

- **状态**
- **事件**
- **转换**
- **阻断**

变成明确控制面。

---

## 2. 对用户想法的裁决

你的方向基本对，但需要收一下：

### 2.1 对的部分

- **用 hooks 显式驱动流程约束** 是对的。没有运行时入口，状态机只是纸面设计。
- **复杂任务做 fresh session** 也是对的。高复杂度任务的主要敌人就是长会话漂移、上下文污染和隐性范围扩张。

### 2.2 需要修正的部分

- **不要让 hooks 本身承担“流程真相源”角色。**
  hook 适合监听、校验、阻断、触发 transition；不适合自己携带完整业务状态。
- **不要默认 per-task fresh session。**
  如果每个 task 都切新 session，很多强相关小任务会被过度切碎，handoff 成本、恢复成本、对账成本都上升。

更强的版本应该是：

> **状态机定义流程，hooks 执行门禁，slice 决定 fresh-session 边界。**

---

## 3. 研究材料给出的启示

### 3.1 Flowspec：状态机和产物门控是对的，但软规则太多

从 [docs/research/workflow-research-flowspec.md](/Users/est8/MyPluginRepo/docs/research/workflow-research-flowspec.md) 和 Flowspec 自身文档可以提炼出两件事：

- 它已经有明确的 **DAG state model** 和 **artifact-gated transition**。
- 但大量关键纪律仍停留在 soft rule，导致“规则写了，不等于真的拦住”。

这说明：

1. **显式状态机是必要的**。
2. **只靠规则文案不够，必须有 hook / validator / hard-block**。
3. 但 **hook 也不能替代状态定义本身**，否则会散落成一堆事件脚本。

### 3.2 Superpowers：fresh context 和角色隔离很有价值，但 gate 过软

从 [docs/research/workflow-research-superpowers.md](/Users/est8/MyPluginRepo/docs/research/workflow-research-superpowers.md) 看，Superpowers 最有价值的是：

- session 启动时显式注入控制上下文
- controller 和 implementer / reviewer 的上下文隔离
- 每个 task 走独立执行与审查链

但它的问题也很清楚：

- 除少数 session-level hook 外，大部分 gate 是 soft 的
- “task 完成”更多依赖流程纪律，而不是结构化 transition

启示是：

> **fresh context 值得要，但必须挂在 machine-checkable task/evidence/reconcile 上。**

### 3.3 Get Shit Done：hook 很多，但如果是 advisory，强度仍然不够

从 [docs/research/workflow-research-get-shit-done.md](/Users/est8/MyPluginRepo/docs/research/workflow-research-get-shit-done.md) 可以看出：

- PreToolUse / PostToolUse / SessionStart 这些事件很适合作为 guard 点
- 但 advisory hook 只能提醒，不能真正把流程收住

所以不能满足于“加了 hook 就算硬化”。关键在于：

- hook 返回什么阻断语义
- 是否接入统一状态转换器
- 失败是 `revision`、`escalation` 还是 `abort`

### 3.4 PAUL：handoff / resume 证明 fresh-session 需要显式恢复协议

从 [vendor/paul/src/commands/handoff.md](/Users/est8/MyPluginRepo/vendor/paul/src/commands/handoff.md) 和 [vendor/paul/src/commands/resume.md](/Users/est8/MyPluginRepo/vendor/paul/src/commands/resume.md) 可以看出：

- fresh session 要成立，必须有 handoff artifact
- resume 不能靠历史聊天，还原必须走固定 bootstrap

这和 `14` 里的 `handoff.md`、`Resume-Bootstrap` 完全一致，说明方向是稳的。

### 3.5 补充：Everything Claude Code — Hook Profile Gating 证明 hook 需要分层运行

[来源: workflow-research-everything-claude-code.md §7, §10]

ECC 有 26 个 hooks 分布在 6 个 lifecycle events。为了避免全量 hooks 拖慢每次操作，它引入了 **Hook Profile Gating**（`run-with-flags.js`）：

- 通过 `ECC_HOOK_PROFILE` 环境变量选择激活哪组 hooks
- `ECC_DISABLED_HOOKS` 可禁用特定 hook
- 每个 hook 内部用 `require()` 优化避免冷启动

启示：

> **hooks 不应全量运行，应该按 profile 选择子集。** 这和 §4 的"profile 锁定后选状态机"完全一致——profile 不仅决定 phase 集合，还应决定 hook 集合。

### 3.6 补充：claude-reflect — never-crash hook pattern 是 hook 实现的基线标准

[来源: workflow-research-claude-reflect.md §7, §10]

claude-reflect 的所有 hook（4 个 Python 脚本）都用同一模式：

```python
try:
    # hook logic
except Exception:
    sys.exit(0)  # never crash the main Claude process
```

启示：

> **hook 内部错误绝不能阻断主流程。** 除非 hook 被显式标记为 Hard gate，否则任何 hook 崩溃都应该被吞掉。这应该成为我们所有 hook 的第零条规则。

### 3.7 补充：Claude-Code-Workflow — Completion Status Protocol 给出了最完整的终止状态定义

[来源: workflow-research-claude-code-workflow.md §3, §10]

CCW 定义了 4 种终止状态 + 3-Strike 升级：

- `DONE` — 正常完成
- `DONE_WITH_CONCERNS` — 完成但有遗留
- `BLOCKED` — 需要外部解除
- `NEEDS_CONTEXT` — 信息不足

3-Strike：连续 3 次相同类别的非 DONE 状态 → 自动升级为 escalation。

启示：

> **我们的 Completion Markers 可以直接采用这 4 个状态。** 比现有的 `## TASK COMPLETE / ## BLOCKED` 更完整，补上了 `DONE_WITH_CONCERNS` 和 `NEEDS_CONTEXT` 两个中间状态。

### 3.8 补充：oh-my-claudecode — Stop hook 硬阻断证明"出口门禁"可以做到 hard enforcement

[来源: workflow-research-oh-my-claudecode.md §5, §10]

OMC 的 `persistent-mode.cjs`（1144 行）通过 `{decision: "block"}` 在 Stop 事件上硬性阻止 Claude 结束。这是真正的 hard enforcement——不是提醒，是阻断。

但它也暴露了风险：1144 行的单点 all-in-one hook，任何 bug 都可能导致 Claude 永远无法停止。

启示：

> **Stop hook 阻断能力很有价值，但必须拆分成小的专责 hooks**（evidence-check、settlement-check、completion-marker-check），每个独立失败，而不是一个巨型 hook 承担所有出口检查。

### 3.9 补充：PAUL — anti-rationalization 是 prompt 层最有价值的 soft enforcement

[来源: workflow-research-paul.md §5A, §7]

PAUL 没有 hard enforcement，但它的 prompt discipline 比所有其他 vendor 都深：

- **evidence-before-claims**：要求先列证据再给结论
- **diagnostic failure routing**：失败分 intent / spec / code 三路
- **"confidence without evidence is the #1 cause"** — 直接命名 LLM 核心失败模式

启示：

> §9.5 的"default no-memory + deterministic triggers"方向是对的，PAUL 给出了更具体的 prompt patterns 可以直接注入 Phase 3-4。这些 patterns 成本极低（几行 markdown），收益很高。

### 3.10 补充：Ouroboros — Stagnation Detection 比"连续 2 次相同错误"更完整

[来源: workflow-research-ouroboros.md §3, §7]

Ouroboros 的 Stateless Stagnation Detection 识别 4 种停滞模式：

1. **循环重复** — 相同输出反复出现
2. **无进展** — 指标不变
3. **漂移过大** — 偏离目标方向
4. **收敛假阳性** — 看似收敛但质量不够

启示：

> 当前 §4 的 stall detection 只看"连续 2 次 revision 错误描述相同"，这只覆盖了模式 1。应该补上模式 2（issue count 不减）和模式 3（修改超出 allowed_paths），让 stall detection 更完整。

---

## 4. 推荐的控制面：状态机先于 hooks

### 4.1 唯一真相源

建议新增一个显式状态文件：

```json
{
  "profile": "complex",
  "phase": "EXECUTE",
  "current_unit": "S-003",
  "unit_type": "slice",
  "current_task": "task-014",
  "session_policy": "fresh-per-slice",
  "status": "in_progress",
  "allowed_transitions": [
    "EXECUTE -> VERIFY",
    "EXECUTE -> DELTA",
    "EXECUTE -> BLOCKED"
  ],
  "delta_count": 1,
  "stall_count": 0
}
```

文件名可以是：

- `.workflow/state.json`

这里最重要的不是字段多少，而是：

- `profile` 在 `TRIAGE` 后锁定
- `phase` 和 `unit` 分离
- 所有状态变更都通过统一 transition 入口

### 4.2 hooks 的职责

hooks 不直接“定义流程”，只做 4 件事：

1. **读取当前状态**
2. **校验当前操作是否合法**
3. **必要时阻断**
4. **调用统一 transition CLI / validator**

也就是：

```text
hook = event adapter
state machine = workflow law
transition CLI = only mutator
```

### 4.3 不建议的做法

不建议：

- 让每个 hook 直接编辑 `state.json`
- 在不同 hook 里各自维护 phase 判断逻辑
- 让 prompt 和 hook 同时成为两套流程真相源

否则很快会出现：

- 同一事件在不同 hook 中解释不一致
- 状态变更不可追踪
- “看起来有强约束，实际仍然可漂移”

### 4.4 补充：Completion Status Protocol — 终止状态应标准化为 4 类

[来源: workflow-research-claude-code-workflow.md §3]

建议 `state.json` 的 `status` 字段采用 CCW 的 4 状态协议：

```json
{
  “status”: “DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT”
}
```

加上 3-Strike 升级规则：连续 3 次相同类别的非 DONE 状态 → 自动升级为 `escalation`。

这比当前设计里 `in_progress / done / blocked` 三态更完整，补上了 `DONE_WITH_CONCERNS`（有遗留但可关闭）和 `NEEDS_CONTEXT`（信息不足，需人工补充）两个关键中间态。

---

## 5. 建议的 hook 布局

### 5.1 SessionStart

职责：

- 读取 `.workflow/state.json`
- 校验当前 session 是否允许继续当前 unit
- 如果是 `complex+` 且没有 handoff / bootstrap 产物，拒绝直接恢复执行
- 把当前 `phase/profile/unit` 注入上下文

### 5.2 PreToolUse

职责：

- 如果当前 phase 不允许写代码，则阻断 Write/Edit/Bash
- 在 `EXECUTE` 中校验写入目标是否超出 `allowed_paths`
- 在 `VERIFY` 中阻断无关业务修改
- 对 `complex+` 检查当前 session 是否已经越过 unit 边界

这类 hook 应该是最主要的“硬门”。

### 5.3 PostToolUse

职责：

- 更新 `actual_scope`
- 检查是否触发 `delta re-entry`
- 记录 evidence 候选信息
- 检测 context 消耗与 unit 完整度

PostToolUse 更适合做：

- 侦测偏航
- 生成诊断
- 触发下一步 gate

不适合单独承担最终 closure 判定。

### 5.4 Stop / SubagentStop

职责：

- 没有 `verify-evidence` 时，不允许把 task 标成完成
- 没有 `reconcile-settlement` 时，不允许把 unit 标成 closed
- `DONE_WITH_CONCERNS` 时阻止伪装成 DONE

也就是说，Stop hook 的职责不是“提醒一下”，而是：

> **在最后出口处拒绝无证据完成。**

---

## 6. `TRIAGE` 之后的强约束应该怎么切入

### 6.1 复杂度一旦确认，就切 profile-specific 状态机

`TRIAGE` 不应该只是打个标签，而应该产生：

```text
profile = trivial | simple | moderate | complex | harness
```

并立刻决定：

- 允许的 phase 集
- 允许的 transition 集
- 强制产物集
- session policy
- enforcement level

这一步之后，不再允许“同一任务里随意切 workflow 规则”。

如果后面发现复杂度判断错了，只能走：

- `delta`
- `re-triage`
- 人工升级/降级

而不是 silently switch。

### 6.2 推荐的 profile 对应关系

| Profile | 状态机强度 | hooks 强度 | session policy |
|---------|-----------|-----------|----------------|
| trivial | 最小 | 轻 | 单 session |
| simple | 最小 + closure | 轻 | 单 session |
| moderate | 完整 phase state + verify/settle gate | 中 | 默认单 session，必要时 fresh on delta |
| complex | 完整 phase + unit state + hard gates | 高 | **fresh per slice** |
| harness | 完整 phase + slice + wave + handoff | 最高 | **fresh per slice / worker per task** |

---

## 7. `fresh session per unit` 到底该怎么定义

这里要先区分 3 个概念：

### 7.1 task

最小执行单元，绑定：

- `covers_ac`
- `verify_cmd`
- `allowed_paths`

适合作为 worker 的执行边界，不适合作为 orchestrator 默认的 session 边界。

### 7.2 slice

一个可独立关闭的执行闭包，通常覆盖：

- 一个独立 AC 集
- 一组强耦合文件
- 一次明确的 verify + reconcile

**这才是 complex 默认应该 fresh session 的 unit。**

### 7.3 wave

并行编排分组，主要是 harness 层能力，不适合拿来做默认 session 粒度。

---

## 8. 为什么不建议默认 `fresh session per task`

表面上看，per-task 最干净；但默认这么做会带来 4 个问题：

1. **handoff 爆炸**
   每个 task 都要 bootstrap / restore / settle，一旦 task 很碎，流程会比代码还重。
2. **局部连续性被切断**
   很多 task 是同一 slice 内的连贯编辑，硬切 session 反而增加恢复误差。
3. **orchestrator 负担过高**
   要不断生成和消费 handoff，吞吐下降明显。
4. **对账噪声增加**
   `reconcile` 会被拆得过细，最后很难保留真正有价值的 closure。

因此更合理的默认是：

- **orchestrator: fresh per slice**
- **worker/subagent: fresh per task（按需）**

这是比“所有高复杂度都 per-task fresh”更稳、更经济的做法。

---

## 9. 推荐方案

### 9.1 Complex

建议策略：

- `TRIAGE` 后锁 `profile=complex`
- `EXECUTE` 以 `slice` 为主 unit
- 每个 slice 开始前启动 fresh session
- slice 内可顺序完成多个 task
- slice 结束必须有：
  - 全量 `verify-evidence`
  - `handoff.md`（跨 session 时）
  - `reconcile-settlement` 或 slice-level closure

### 9.2 Harness

建议策略：

- orchestrator 不长期携带执行细节
- **每个 slice 都 fresh session**
- slice 内如果有并行 wave，**每个 worker task 使用独立 fresh worker session**
- orchestrator 只消费：
  - task completion markers
  - verify-evidence
  - reconcile artifacts

### 9.3 Moderate

不建议强制 fresh per unit。更合适的是：

- 默认单 session
- 出现以下任一条件再强制重启：
  - context 使用过高
  - 出现 delta re-entry
  - 出现新设计决策
  - 同一问题 revision 两轮无进展

---

## 9.4 Simple / Trivial 的 closure 语义不要和 memory/backflow 混在一起

这里需要把 3 件事拆开，否则状态机会自相矛盾：

1. **任务是否完成**
2. **是否需要 durable backflow**
3. **是否存在需要人工决策的未决风险**

Simple / Trivial 的问题不在于“要不要完整 settle”，而在于：

- 它们通常**不值得**做重型 reconcile
- 但这不等于可以把“轻量备注”混成 `DONE_WITH_CONCERNS`

更稳的规则应该是：

- Simple / Trivial 默认只做 **minimum closure**
- 可以有 `notes` / `lessons`
- 但仅因为“有一点说明”**不进入** `DONE_WITH_CONCERNS`
- `DONE_WITH_CONCERNS` 只保留给**真正需要处理**的情况：
  - 有 follow-up
  - 有 waiver
  - 有用户可见风险
  - 有 AC 未闭合 / FAIL / SKIP

也就是说：

```text
DONE + notes        != DONE_WITH_CONCERNS
light closure       != unresolved risk
```

这比让 trivial/simple “带一点备注也能直接 close concern”更一致，因为后者会破坏状态名本身的语义。

---

## 9.5 不要让 AI 判断“是否值得记忆”，改成 default no-memory + deterministic triggers

这里最容易设计过头的地方是：

> 让 AI 判断一个 simple task 是否“足够重要，值得回流 durable docs”。

这在真实运行里不稳，因为这种判断太抽象、太依赖语气和上下文。

更好的做法是：

- **默认不回流**
- **默认不要求 durable memory**
- **只有命中确定性触发器时才 backflow / 升级状态**

推荐触发器：

- 改了公开接口或 API 契约
- 新增依赖
- 改了既有 invariant
- 命中敏感路径
- 产生 follow-up / waiver / residual risk
- 存在 AC FAIL / SKIP

这样工作分成两层：

1. **AI 负责提取事实**
   - 改了哪些文件
   - 是否新增依赖
   - 哪些 AC 失败
   - 是否有 follow-up / risk
2. **规则层负责决定动作**
   - 是否 backflow
   - 是否进入 `DONE_WITH_CONCERNS`
   - 是否要求人工决策

换句话说：

> 能规则化的就规则化；不能规则化的，不要让它决定状态机走向。

这意味着 simple/trivial 的推荐策略应当是：

- 默认 `DONE`
- 可选 `notes/lessons`
- 无 durable backflow
- 只有命中确定性触发器时，才升级为 concern/backflow 路径

---

## 10. 一个更可落地的最小实现顺序

如果要真做，我建议顺序不是“先堆 hook”，而是：

### P0

1. 定义 `.workflow/state.json` 最小 schema
2. 定义 transition 表
3. 为 schema / transition / gate 写**先失败**的校验测试
4. 实现统一 `transition` 校验入口
5. 让 `TRIAGE` 输出 profile + session policy

### P0.5 补充：Hook 容错基线

[来源: workflow-research-claude-reflect.md + workflow-research-everything-claude-code.md]

在写任何业务 hook 之前，先建立两个基线：

6. **never-crash wrapper**：所有 hook 共用的 try/catch 包裹器，确保任何 hook 内部错误不阻断主流程
7. **hook profile gating**：根据当前 `state.json` 的 `profile` 字段决定激活哪些 hooks，避免 trivial 任务跑全量 hooks

### P1

6. 接 `SessionStart`：恢复与 bootstrap
7. 接 `PreToolUse`：phase 写保护 + `allowed_paths`
8. 接 `Stop/SubagentStop`：evidence / reconcile 出口门禁
9. 为每个 hook 增加阻断/放行测试，避免 advisory 漂移

### P2

10. 建立按 profile 分层的 e2e fixture：
    - trivial/simple: minimum closure
    - moderate: verify-evidence + reconcile
    - complex/harness: slice handoff + fresh-session + boundary enforcement
11. 对 `complex+` 引入 `slice` 级 fresh-session
12. 对 `harness` 引入 `wave` + worker session 隔离
13. 最后再做 commands/skills 编排层

这条顺序比“先实现一堆 hook，再想状态语义”更短，也更稳。

---

## 10.1 我更支持的实现原则：Gate-First TDD，而不是 Command-First

你提的方向我基本赞成，但我会把表述改成：

> **先测协议内核，再测 hook 门禁，再跑跨 profile e2e，最后才封装 command/skill workflow。**

原因是 command/skill 只是入口层；如果底层 gate 还没被测试锁死，越早写 command，越容易把软约束包装成“看起来能跑”的假工作流。

推荐顺序：

1. **Schema tests**
   先让这些失败：
   - 非法 `state.json`
   - 非法 transition
   - 缺失 `verify-evidence`
   - 缺失 `reconcile-settlement`
2. **Hook gate tests**
   先让这些失败：
   - 错 phase 仍允许写代码
   - 超出 `allowed_paths` 未触发阻断
   - 无 evidence 仍允许完成
3. **Profile e2e tests**
   用不同复杂度 fixture 跑完整路径：
   - simple 能闭环
   - moderate 能过 verify/reconcile
   - complex 能在 slice 边界 fresh resume
   - harness 能处理 wave / worker 隔离
4. **Commands/skills**
   最后才写 slash command / skill prompt / orchestration 文案。

也就是说，这个 workflow 的实现顺序应该是：

```text
state machine + schema
  -> gate hooks
    -> profile e2e
      -> commands / skills
```

这比“先写 command，再补 gate”更可靠，因为前者会把工作流的正确性绑定在测试上，后者通常会把正确性绑定在 prompt 自觉上。

---

## 11. 对 `00-08` 主线的影响

如果采纳本讨论，主线至少要新增这些内容：

- `00-overview.md`
  - 增加“状态机是真相源，hooks 是 enforcement adapter”
- `01-triage.md`
  - 增加 `profile lock` 与 `session policy` 决策
- `03-spec-and-plan.md`
  - 为 `slice` 定义 unit 边界，而不是只定义 task
- `04-execute.md`
  - 增加 hook 事件布局与 transition 触发规则
- `05-verify.md`
  - 增加 Stop/SubagentStop 的 evidence gate
- `06-settle.md`
  - 增加 unit closure 与 session handoff 关系
- `07-cross-cutting.md`
  - 增加状态机、transition taxonomy、fresh-session policy
- `09-schemas.md`
  - 应新增 `state.json` 与 transition schema

---

## 12. 最终裁决

最终我支持的不是：

- “用 hooks 代替 workflow”
- “高复杂度一律 per-task fresh session”

我支持的是：

1. **状态机显式化**
2. **hooks 事件化、门禁化**
3. **complex+ 采用 fresh session**
4. **默认以 slice 作为 fresh-session unit**
5. **task 级 fresh session 留给 worker 隔离执行**

一句话收束：

> 下一轮进化不该是“再多一些规则”，而该是“让 profile 锁定后的流程进入可阻断、可恢复、可重建的状态机运行模式”。  
