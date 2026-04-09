# Codex 追加实现解释方案

> 定位：这是 `my-workflow/IMPLEMENTATION.md` 的旁路补充说明。  
> 目的：先把当前实现前会卡住的冲突点、建议裁决、未来回写点写清楚。  
> 边界：**本文件不替代、也不修改现有 SSOT**。`IMPLEMENTATION.md` 仍是当前主线实现文档。

---

## 使用方式

1. 实现时仍以 `IMPLEMENTATION.md` 为主。
2. 如果实现者在以下几类问题上遇到歧义，先查本文件：
   - 状态机字段语义冲突
   - gate 强弱边界不一致
   - 同一 lane 在不同章节里要求不一致
   - 附录里有定义但主体未排期
3. 如果后续决定正式收敛到 SSOT，再按本文的“建议回写点”回写 `IMPLEMENTATION.md`。

---

## 现阶段建议

我的判断是：**先不动 SSOT 是对的**。

原因不是这些问题不重要，而是：

- 现有 `IMPLEMENTATION.md` 已经足够当主线入口
- 现在更缺的是“冲突裁决记录”，不是再做一次大规模重写
- 先把分歧和建议写成旁路解释，能避免你还没开始实现就反复改主线文档

换句话说，当前更稳的做法是：

```text
IMPLEMENTATION.md 继续当主线
  +
codex-追加实现解释方案.md 记录冲突、裁决建议、回写点
```

---

## 冲突点与建议裁决

### 1. `state.json` 里的 `phase` / `status` / `completion_status` 语义还没完全收死

**现状**

- `state.json` 示例把 `allowed_transitions` 写成了 `EXECUTE->VERIFY`、`EXECUTE->DELTA`、`EXECUTE->BLOCKED`
- 同时字段说明又把 `phase` 限定为 `TRIAGE/DISCOVER/SPEC_PLAN/EXECUTE/VERIFY/SETTLE/DONE`
- `status` 和 `completion_status` 里又已经有 `blocked` / `BLOCKED`

**风险**

- 实现 transition validator 时，会不清楚 `BLOCKED` 到底是不是一个 phase
- 实现 hook 时，会不清楚“阻断”是 phase 迁移，还是当前 phase 下的状态变化

**建议裁决**

- `phase` 只表示工作流阶段：`TRIAGE/DISCOVER/SPEC_PLAN/EXECUTE/VERIFY/SETTLE/DONE`
- `status` 表示当前推进状态，如 `pending/in_progress/blocked/needs_context`
- `completion_status` 表示结束语义，如 `DONE/DONE_WITH_CONCERNS/BLOCKED/NEEDS_CONTEXT`
- `BLOCKED` 不进入 phase graph，只进入 `status/completion_status`
- `delta` 不是 phase，而是经由 gate 判定后触发的重入动作

**建议回写点**

- `IMPLEMENTATION.md` 的 `P0.1 state.json`
- `IMPLEMENTATION.md` 的 `P0.3 transitions.json`
- `IMPLEMENTATION.md` 的附录 A7 / A27

### 2. `simple` 路径对 `verify-evidence` 的要求前后不一致

**现状**

- `P1.4 Evidence Gate Tests` 写的是 `Quick/Simple` 不要求 evidence
- `P2.2 Simple Path` 又写成了 `verify-evidence is collected after VERIFY`

**风险**

- 实现 `simple` 的 schema、fixture、Stop hook 时会出现双重口径
- `VERIFY` 是否只是执行 `verify_cmd`，还是必须沉淀结构化 evidence，不清楚

**建议裁决**

- `simple` 保留 `VERIFY` 和 `verify_cmd`
- `simple` 可以产出 `verify-evidence.json`，但它不是 hard gate
- `G8 Ralph Loop` 的硬阻断只对 `standard+` 生效
- `quick` 继续不要求 `verify-evidence`

**推荐解释**

```text
quick    = 不要求 verify_cmd，不要求 evidence
simple   = 要求 verify_cmd，evidence 可选
standard+= 要求 verify_cmd，evidence 必须
```

**建议回写点**

- `IMPLEMENTATION.md` 的 `P1.4 Evidence Gate Tests`
- `IMPLEMENTATION.md` 的 `P2.2 Simple Path`
- `IMPLEMENTATION.md` 的附录 A1 / A2

### 3. `standard/semi-auto` 的 `verify-review` 契约有冲突

**现状**

- `P2.3 Standard/Semi-Auto Path` 写的是 `verify-review contains spec_fit`
- 附录 A33 又明确说 `standard/semi-auto` 只做 `quality_fit`，跳过完整 `spec-fit` AC 覆盖分析

**风险**

- `verify-review.json` 的最小字段集无法冻结
- 实现者不知道 semi-auto 到底是轻量 review，还是完整双审查

**建议裁决**

- `standard/semi-auto` 只要求轻量 `quality_fit`
- `spec_fit` 的完整 AC 覆盖分析留给 `standard/full` 与 `complex+`
- `standard/semi-auto` 的 AC 覆盖压力放在 `reconcile-settlement.json.ac_results`

**推荐解释**

```text
standard/semi-auto
  = 轻量 quality gate
  + reconcile 中做 AC 对账

standard/full
  = spec_fit + quality_fit

complex+
  = 更强 review pipeline
```

**建议回写点**

- `IMPLEMENTATION.md` 的 `P2.3 Standard/Semi-Auto Path`
- `IMPLEMENTATION.md` 的 `A4 verify-review.json`
- `IMPLEMENTATION.md` 的 `A33 Light Quality Gate`

### 4. `event-log` 和 `checkpoint` 已经被当成核心能力引用，但主体排期还偏弱

**现状**

- 附录 A28/A29 已经把 `event-log.schema.json` 和 `event-log.jsonl` 定义出来
- vendor 参考也把 observability / checkpoint 当成明确能力
- 但主体里它们更像“顺手提到”，不是已经排死的 core 实施项

**风险**

- 实现时容易先做 schema 和 gate，后做 event log，导致可观测性又变成可选项
- `checkpoint` 容易被误解成要新增一套独立协议，而不是恢复动作

**建议裁决**

- `event-log.schema.json` 和 `event-log.jsonl` 应视为 core runtime asset
- `checkpoint` 不必单独再发明一个 schema
- `checkpoint` 的实质是：
  - `standard` 生成 `resume-pack.json`
  - `complex+` 生成 `handoff.md`
  - 同时写入 `event-log.jsonl`

**建议回写点**

- `IMPLEMENTATION.md` 的 `P0.1 JSON Schema 可执行化`
- `IMPLEMENTATION.md` 的 `P0 验收`
- `IMPLEMENTATION.md` 的 `P3 PostToolUse / SessionStart`

### 5. “可拔插路由层”目前冻结了结果结构，但还没冻结最小接口分层

**现状**

- 当前主线已经有 `profile + lane + route_source + continuation + ambiguity_score`
- 也已经有 route priority 和 3 个 scenario template
- 但还没把“可拔插”落实成最小接口层次

**风险**

- 后续实现者会各自定义自己的 scenario detector / policy evaluator / lane template loader
- 同样叫“可拔插”，最后可能长成完全不同的三套实现

**建议裁决**

- 路由层至少分 3 层：
  - `Signals`: `explicit / scenario / continuation / score`
  - `Policy`: priority / upgrade triggers / fallback
  - `Lane templates`: `simple/patch`、`standard/semi-auto`、`standard/full`、`complex/full`、`orchestrated`
- `triage-result.json` 继续只承载“结果”，不把整个 policy 内联进去

**建议回写点**

- `IMPLEMENTATION.md` 的术语速查
- `IMPLEMENTATION.md` 的 `P0 triage-result.json`
- `IMPLEMENTATION.md` 的 `A21 Routing Priority + 3 个 Scenario Template`

### 6. 一些附录项已经足够重要，但还不适合现在就升格为主线改动

**现状**

- 附录里还有 `Deliver Gate`、`Config 系统三层优先级`、`Review Pipeline — Confidence Gating`
- 它们都重要，但不属于当前“先把 workflow 内核跑起来”的第一波阻塞项

**风险**

- 如果现在就一起回写 SSOT，主线文档会继续膨胀
- 如果完全不记，又容易让后面误以为这些已经排进第一阶段

**建议裁决**

- 这些项先保留在附录层和本补充文档里
- 默认归类为：
  - `v1 core 之后马上做`
  - 不是“以后再说”，也不是“现在就必须改 SSOT”

**建议暂定分层**

```text
v1 core
  - state/transition
  - schema/fixture
  - G0-G9
  - event log
  - resume/handoff
  - routing core

v1.1
  - Deliver Gate
  - Config precedence
  - confidence-gated review pipeline

reserved
  - 更重的注入扫描
  - 更复杂的多 reviewer 自动分流
```

---

## 如果现在立刻开工，建议先口头遵循的实现解释

为了避免实现者再次回到归档里判案，我建议在真正写代码前，先默认采用下面这组解释：

1. `IMPLEMENTATION.md` 继续是主线，不在本轮改动
2. `BLOCKED` 不是 phase
3. `simple` 执行 `verify_cmd`，但 `verify-evidence` 不是 hard requirement
4. `standard/semi-auto` 只做 light `quality_fit`
5. `event-log` 视作 runtime core，不视作可有可无的附录
6. `checkpoint` 不是新协议，只是恢复动作加日志
7. 路由层默认按 `Signals / Policy / Lane templates` 三层实现

---

## 结论

不改 `IMPLEMENTATION.md` 没问题，前提是不要假装它已经没有歧义。

当前最稳的做法不是继续改 SSOT，而是：

- 保留现有 `IMPLEMENTATION.md` 作为主线
- 用本文件把实现前会卡住的几处冲突先钉住
- 等真正实现过一轮，再决定哪些裁决值得正式回写

这比现在直接动主线更稳，也更符合“先实现、再收敛 SSOT”的节奏。
