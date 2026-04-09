# 16. 面向半自动真实场景的贴合优化

> **定位**：不是推翻 `14` 的骨架，也不是继续做通用平台能力扩展。  
> 这篇文档只回答一个问题：**当前 workflow 如何更贴合“已有代码库上的半自动中小需求迭代”这个真实场景。**

> **适配对象**：见 [input-01-real-world-scenario.md](./input-01-real-world-scenario.md)。

---

## 0. 先给结论

当前 `00-09` 主线已经能覆盖这个真实场景，但还没有做到“低摩擦贴合”。

它现在的问题不是约束不够，而是：

1. **`moderate` 仍偏重**
2. **spec 之前的背景对齐还不是显式槽位**
3. **连续补小需求的快路径不够自然**
4. **中等复杂度跨 session 恢复还不够轻**

所以这轮优化不该继续加 phase，也不该新增一个完全独立 profile。  
更好的方向是：

> **保留 6 phase 骨架，在 `moderate` 内增加一个“半自动迭代模式（semi-auto lane）”的压缩路径。**

一句话说：

```text
同一个骨架
  + 更轻的 moderate 进入方式
  + pre-spec 背景对齐包
  + 小需求增量快路径
  + 轻量跨 session 恢复
```

---

## 1. 当前设计和真实场景的错位点

真实场景要的是：

- 程序员保留边界定义、纠偏和验收权
- Agent 做高频分析与实现
- 中小需求迭代能持续往前，不被 ceremony 压垮
- 补一个小需求时，不需要整套重来

而当前主线更像是：

- 面向“完整任务闭环”的通用骨架
- 对 `moderate+` 的治理能力已经比较完整
- 但对“半自动中小迭代”的连续节奏还不够顺手

最具体的错位有 4 个：

### 1.1 `moderate` 太像“轻量 complex”，而不像“真实日常迭代”

当前 `moderate` 已经要求：

- 理解摘要 + 人类确认
- BDD 场景
- 完整 tasks.json
- verify-evidence
- reconcile

这在原则上没错，但对很多“已有入口、已知模块、只是连续补几个点”的任务，心智成本还是偏高。

### 1.2 pre-spec 背景资料没有显式成为一等产物

真实场景里，在 spec 之前，程序员经常会补：

- 设计稿
- 对照行为
- API 文档
- 团队约定
- 已知坑点

当前设计允许补这些，但它们只是 Discover 的输入项，不是显式协议槽位。  
结果是：

- 有时会被遗漏
- 有时会混进自由文本
- 有时进入不了后续恢复链

### 1.3 “补一个小需求”没有独立的 continuation 入口

真实开发里经常不是新任务，而是：

- 在已确认方向上再补一个角标
- 多一个异常分支
- 再补一个埋点
- 再补一个空态

当前主线虽然有 Delta 模型，但还没有一个明确的“这是同一 Baseline 下的小增量补丁，不要整套重走”的入口。

### 1.4 中等复杂度任务的恢复能力偏弱

现在 `handoff / slice / fresh-context` 更偏向 `complex+`。
但真实场景里很多 moderate 任务一样会：

- 今天看完理解，明天再补 plan
- 先做功能，晚点再做验证
- 被更高优任务打断后回来接着做

这些不一定值得进入完整 slice/handoff 模型，但又不能完全依赖对话历史。

### 1.5 补充：新 research 佐证

7 份新 vendor research 从不同角度验证了以上 4 个错位点：

- **Compound Engineering** 的 `ce:work` Phase 0 证明 scope-aware ceremony 是可行的——trivial 直接执行，small/medium 建 task list，large 建议先 brainstorm/plan。这正是 §1.1 "moderate 太像轻量 complex" 的解法。[来源: workflow-research-compound-engineering-plugin.md §4]
- **PAUL** 的 context quality degradation curve 设定了 50% token budget 阈值——超过就触发 aggressive atomicity。这给 §1.4 的恢复问题提供了量化依据。[来源: workflow-research-paul.md §7]
- **Ouroboros** 的 Ambiguity Gate（模糊度 ≤ 0.2 才执行）证明 §1.2 "背景资料作为显式槽位"是对的——如果模糊度太高，应该阻断进入 spec，而不是带着模糊继续。[来源: workflow-research-ouroboros.md §3]

---

## 2. 优化目标

这篇 `16` 的目标不是“让流程更强”，而是让它更**贴日常工程节奏**：

1. **简单事不过载**
2. **小增量不重跑**
3. **背景资料可对齐、可继承**
4. **状态足够可观测，但不要求每次重仪式**
5. **中断恢复轻量可用**
6. **经验回流按需触发，而不是默认重型沉淀**

---

## 3. 推荐方案：在 `moderate` 内增加 Semi-Auto Lane

### 3.1 不新增 profile，新增 lane

不建议引入一个新的 `semi_auto` profile。  
那会把骨架复杂度再抬高一层，并且让 profile 语义变乱。

更稳的做法是：

- profile 仍然是 `trivial/simple/moderate/complex/harness`
- 在 `moderate` 内定义两条执行车道：
  - `moderate/full`
  - `moderate/semi-auto`

这样好处是：

- 骨架不变
- schema 不炸裂
- 真实场景能获得更轻路径
- 以后实现时也更容易做配置开关

### 3.2 `moderate/semi-auto` 适用条件

满足大多数条件时可走：

- 已有明确代码入口
- 影响范围集中在 1 个模块或同一功能面
- 不引入新依赖
- 不改架构边界
- 不改公共协议
- 验收方式清楚

补充量化参考：**Ouroboros 的 Ambiguity Gate** 可以作为进入 semi-auto 的前置条件——如果模糊度 > 0.2（即需求不够清晰），应该先走 clarification 而不是直接进入 semi-auto。这比纯主观判断更稳。[来源: workflow-research-ouroboros.md §3]

只要命中下面任一项，就退出该 lane，回 `moderate/full` 或更高层：

- 新增依赖
- 跨模块扩散
- 验收标准变化
- 主调用链理解被推翻
- 需要新 ADR

---

## 4. 优化 1：在 spec 之前显式加入 `background-alignment.md`

### 4.1 为什么要加

这是当前最值得补的缺口。

真实场景里的“补背景资料”不是附属信息，而是：

- 限定 spec 的前提
- 限定理解的边界
- 决定后续 review 的依据

如果它只存在于对话里，恢复时就容易丢；如果它混在 spec 里，又会污染 transient 设计。

### 4.2 它应该放在哪里

建议放在 Discover 末尾、Spec 之前：

```text
clarification
  -> minimal implementation context
    -> background alignment
      -> code understanding
        -> spec/plan
```

### 4.3 它的职责

`background-alignment.md` 不负责定义方案，只负责对齐前提：

- 参考设计稿 / 对照行为
- 相关 API 文档
- 团队约定 / 已知限制
- 本次要继承的历史决定
- 明确“不在本次讨论范围”的背景噪声

### 4.4 为什么它适合你的场景

因为你的真实节奏不是“纯从 PRD 到实现”，而是经常会说：

- “这里参考旧页面”
- “这个接口先按已有行为”
- “这次先别动另一个模块”
- “这个坑之前踩过，先沿旧做法”

这些都更像 background alignment，不是 spec 本体。

---

## 5. 优化 2：给“小需求补丁”一个显式 continuation path

### 5.1 不要把它当新任务重跑整套

当前 Delta 模型已经足够强，但对真实场景来说还差一个“入口语义”：

> 这是同一方向下的小补丁，不是一次新的完整 spec/plan 生命周期。

建议增加一个 continuation 判定：

```text
continue-on-baseline = true | false
```

### 5.2 满足这些条件时，允许 continuation

- 基线目标不变
- 验收锚点不变
- 不新增一级模块
- 不新增依赖
- 不改架构决策
- 只是 task patch / AC patch / UI patch / test patch

### 5.3 continuation 的最小动作

如果判定为 continuation，不要重做整套：

- 不重做完整 Discover
- 不重写完整 spec
- 只追加 delta
- 按需生成新的 effective view
- 只补充受影响的 task / AC / verify

补充实现参考：**Compound Engineering** 的 `ce:brainstorm` 和 `ce:plan` 都有 Phase 0.1 "Resume Existing Work" 逻辑——检测 `docs/brainstorms/` 或 `docs/plans/` 下是否有匹配的已有文档，如果有就 confirm 后 resume，而不是从头开始。这是 continuation 的成熟实现。[来源: workflow-research-compound-engineering-plugin.md §4, §6]

### 5.4 这会直接改善什么

它会让“后续补充小需求”从：

- “再走一遍任务”

变成：

- “沿已确认基线追加一个受控 patch”

这对半自动真实场景非常关键。

---

## 6. 优化 3：给 `moderate` 一个轻量恢复模型，而不是要么继续聊，要么上 complex handoff

### 6.1 当前缺口

现在恢复能力分布大概是：

- trivial/simple：默认继续会话
- complex+：有 handoff / resume-bootstrap
- moderate：夹在中间

但真实场景里，moderate 才是最常被打断的。

### 6.2 推荐补法

不要让 moderate 强制进入 `slice/handoff` 完整体系。  
更好的做法是加一个轻量恢复包：

```text
resume-pack.md
```

它只需要 5 件事：

- 当前 phase
- 当前目标
- 当前 Baseline / latest Delta
- 下一步动作
- 当前未决问题

补充量化阈值：**PAUL 的 context quality degradation curve** 给了具体数字——超过 **50% token budget** 就应该触发 aggressive atomicity（强制拆小任务），超过 **70%** 就应该强制写 resume-pack 并结束当前 session。这比定性判断"context 使用过高"更可操作。[来源: workflow-research-paul.md §7]

### 6.3 为什么这比直接上 handoff 更好

- ceremony 低
- 恢复质量比“继续对话”高
- 不会把 moderate 弄得像 complex

也就是说：

- `complex+` 用 `handoff.md`
- `moderate/semi-auto` 用 `resume-pack.md`

---

## 7. 优化 4：把记忆回流从“默认沉淀”改成“触发式沉淀”

这点承接 `15` 的讨论。

真实场景的大多数小需求，不值得每次都问：

- 这件事值不值得写进 durable docs？

这类判断太抽象，不适合交给 AI。

所以针对半自动真实场景，应该明确：

- 默认无 durable backflow
- 默认无重型 lessons 提炼
- 只有命中确定性触发器才回流

例如：

- 改公共接口
- 引入新依赖
- 新增 invariant
- 产生 follow-up / waiver / risk
- 有 AC FAIL / SKIP

补充路由机制：**claude-reflect 的 9 层 Memory Routing**（`find_claude_files()` + `suggest_claude_file()`）可以作为"触发式沉淀到哪里"的参考——它不让 AI 判断"值不值得记"，而是用启发式规则自动路由到正确的 CLAUDE.md 层级（global → project → module）。我们的 backflow 也可以用类似逻辑：改了 API → 路由到 `docs/interfaces.md`，改了架构决策 → 路由到 `docs/architecture.md`，新增 invariant → 路由到 `docs/invariants.md`。[来源: workflow-research-claude-reflect.md §3]

这会让你的日常节奏轻很多，也更稳。

---

## 8. 优化 5：把“轻量质量 gate”正式压进 `moderate/semi-auto`

真实场景文档非常强调一个点：

> E2E 只能验证功能，不会自动拦住结构性技术债。

当前主线已经有 `quality-fit`，但它更偏完整 Verify 体系。  
对于 `moderate/semi-auto`，更合适的是：

- 不做完整 code review 编排
- 只做 4 项轻量 gate

也就是直接固定成：

1. 架构越层
2. 不必要依赖
3. 漏测试
4. 明显坏味道

这正是你的真实场景需要的那种“拦大坑，不做重审查”。

---

## 9. 推荐的半自动真实场景路径

建议把它明确写成一条 lane：

```text
TRIAGE
  -> DISCOVER
     - clarification
     - minimal context
     - background alignment
     - code understanding
  -> SPEC & PLAN
     - light spec
     - tasks.json
     - verify plan
  -> EXECUTE
     - sequential task loop
     - delta append / continuation
  -> VERIFY
     - verify-evidence
     - light quality gate
     - human E2E/UAT
  -> SETTLE
     - minimum closure
     - triggered backflow only
```

这个路径保住了你要的 7 个点：

- 不复杂
- 可补小需求
- 有约束
- 有状态
- 可中断恢复
- 有经验总结能力
- spec 前可补背景资料

---

## 10. 对当前主线最值得做的最小改造

如果只改最有价值的部分，我建议顺序是：

### P0

1. 在 Discover 增加 `background-alignment.md` 槽位
2. 在 Moderate 下增加 `semi-auto lane` 判定条件（参考 CE 的 scope-aware ceremony + Ouroboros 的 ambiguity gate 量化）
3. 定义 continuation path（沿 Baseline 追加小需求，参考 CE 的 Phase 0.1 resume existing work）

### P1

4. 为 moderate 增加轻量 `resume-pack.md`
5. 把轻量质量 gate 固定成 4 项检查
6. 把回流改成 deterministic trigger

### P2

7. 再决定是否把这些能力统一并入状态机 / hook / command 实现

---

## 11. 最终裁决

当前 workflow **不是不兼容**真实场景，而是**还偏“通用治理骨架”，没有完全压到“半自动日常迭代”的摩擦水平**。

因此这轮优化最重要的不是继续加硬能力，而是补 4 个贴合点：

1. **给 spec 前背景资料一个显式位置**
2. **给小需求补丁一个 continuation 入口**
3. **给 moderate 一个轻量恢复模型**
4. **把经验回流改成触发式，而不是默认重型沉淀**

一句话收束：

> 真正适合半自动真实场景的 workflow，不是“更强的 complex”，而是“更轻的 moderate，但仍保留可验证、可观测、可恢复的骨架”。  
