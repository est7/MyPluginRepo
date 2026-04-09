# 17. 可拔插路由层：评分不是唯一入口

> **定位**：在 `16` 的基础上，专门收敛 workflow 的路由层设计。  
> 目标不是再发明更多 profile，而是让同一套骨架具备**足够灵活、可拔插、可解释的路由能力**。

---

## 0. 先给结论

一个好的 workflow，不应该只有“复杂度评分”这一条入口。

评分很重要，但它只解决：

- 这个任务大概有多重

它解决不了：

- 这是一个明确的小 UI 补丁，还是一个连续增量任务
- 这是一个新接口落地任务，还是在旧 baseline 上继续追加
- 用户已经显式要求走某条 lane
- 当前任务是否应该沿已有 state / delta 继续，而不是重新 triage

所以更合理的设计不是：

> **score -> profile**

而是：

> **router -> lane**  
> 其中 score 只是 router 的一个输入。

---

## 1. 当前问题

`01-triage.md` 现在主要支持两条路：

1. 模糊请求 -> 打分 -> 推荐 profile
2. 显式命令 -> 跳过打分

这对早期够用，但还不够灵活。

因为真实使用中至少还有另外两种常见入口：

3. **场景模板路由**
   - “UI 字段补逻辑”
   - “新接口落地 + 后续微调”
   - “跨模块方案设计”
4. **Continuation 路由**
   - 这不是新任务，而是在已有 baseline / delta 上继续补

如果这两类入口不进入正式设计，实际使用就会退化为：

- 要么每次都重新打分
- 要么全靠用户口头指定
- 要么 agent 自己即兴判断

这三种都不够稳。

---

## 2. 路由层应该长什么样

推荐把路由层定义成：

```text
input
  -> routing signals
    -> lane selection
      -> profile + mode + constraints
```

### 2.1 routing signals

路由层不只看分数，而是同时看 4 类信号：

1. **Explicit**
   - 显式命令
   - 用户明确说“按 complex 走”

2. **Scenario**
   - 是否命中已定义场景模板
   - 例如 UI 小补丁 / 新接口落地 / 跨模块设计

3. **Continuation**
   - 是否存在当前 baseline / delta
   - 是否是同一任务方向上的后续补充

4. **Score**
   - 复杂度评分
   - 风险 / 影响范围 / 依赖变化

### 2.2 lane selection

路由结果不直接只输出 profile，而是输出一条 lane，例如：

- `simple/patch`
- `moderate/semi-auto`
- `moderate/full`
- `complex/full`
- `harness/orchestrated`

这样 lane 天然就能承载“同 profile 内不同治理强度”。

---

## 3. 推荐的四类路由入口

### 3.1 Score Route

用途：

- 模糊请求
- 没有历史上下文
- 没有显式命令

特点：

- 默认入口
- 给出推荐 profile/lane
- 适合作为兜底

补充实现参考：

- **Compound Engineering** 的 `ce:work` Phase 0 实现了三级 complexity routing（trivial/small-medium/large），比纯评分更接近工程语义。[来源: workflow-research-compound-engineering-plugin.md §4]
- **Ouroboros** 的 Ambiguity Gate 公式可以作为 score 的一个维度：模糊度 ≤ 0.2 才允许进入执行，否则强制先做 clarification。[来源: workflow-research-ouroboros.md §3]

### 3.2 Explicit Route

用途：

- 用户明确知道自己要哪条 lane
- 例如 `/simple`, `/moderate`, `/complex`

特点：

- 优先级高于 score
- 但不能绕过 hard guard

也就是说，用户可以显式选 lane，但如果命中新依赖 / 跨模块 / 新协议等硬升级条件，系统仍可提示升级。

### 3.3 Scenario Route

用途：

- 命中高频已知场景

你当前至少已经有这 3 个模板：

1. **UI 字段补逻辑**
   - 默认 `simple/patch`
2. **新接口落地 + UI 对接 + 后续微调**
   - 默认 `moderate/semi-auto`
3. **跨模块方案设计 / 重构 / 工程文档**
   - 默认 `complex/full`

特点：

- 最贴日常
- 比 score 更符合真实工程语义
- 适合做成”推荐 lane 模板”

补充实现参考：

- **oh-my-claudecode** 的 `UserPromptSubmit` hook 用 14+ 关键词检测用户意图，匹配后直接注入对应 skill 内容。这是 scenario detection 的一种成熟实现方式。[来源: workflow-research-oh-my-claudecode.md §5]

### 3.4 Continuation Route

用途：

- 已存在 baseline / delta
- 当前请求是“继续补”“继续修”“再加一个点”

特点：

- 优先判断是否沿当前任务继续
- 避免无意义重 triage

这是你现在最需要补上的路由能力之一。

---

## 4. 推荐的路由优先级

建议固定优先级为：

```text
1. Hard constraints
2. Continuation route
3. Explicit route
4. Scenario route
5. Score route
```

解释：

### 4.1 Hard constraints 最高

如果命中这些，不能因为用户想走轻路径就强压下去：

- 新依赖
- 跨模块扩散
- 新公共协议
- 架构边界变化
- 高风险敏感路径

### 4.2 Continuation 要高于 explicit 和 score

因为“是否沿当前 baseline 继续”比“重新评估复杂度”更关键。  
否则你每次补一个小 delta 都会被重新当成新任务。

### 4.3 Explicit 高于 scenario 和 score

用户明确指定 lane，原则上应尊重。

### 4.4 Scenario 高于 score

场景模板比抽象评分更接近日常使用语义。  
比如“新接口落地 + 后续微调”这一类，单靠 score 很容易被误判成普通 moderate。

### 4.5 Score 作为兜底

当没有 continuation、没有显式命令、也没命中模板时，再用评分做默认推荐。

---

## 5. lane 比 profile 更适合真实使用

profile 解决的是治理层级：

- simple
- moderate
- complex

但 lane 解决的是使用方式：

- patch
- semi-auto
- full
- orchestrated

如果只有 profile，你会遇到两个问题：

1. `moderate` 过宽
2. 日常高频任务无法压缩路径

所以我的建议是：

```text
profile = 治理强度
lane    = 使用方式
```

例如：

| Lane | 含义 |
|------|------|
| `simple/patch` | 入口明确、影响集中的小补丁 |
| `moderate/semi-auto` | 新接口落地、逐步补 UI/逻辑、持续 delta |
| `moderate/full` | 需要完整理解/plan/verify，但还没到 complex |
| `complex/full` | 跨模块方案、重构、spec-first、TDD 优先 |
| `harness/orchestrated` | 强编排、并行 worker、完整隔离 |

---

## 6. 针对你三个真实场景的路由矩阵

### 6.1 UI 字段补逻辑

**输入特征**：

- 后台补一个字段
- UI 按字段补显式逻辑
- 入口明确
- 影响集中

**默认路由**：

```text
scenario route -> simple/patch
```

**升级条件**：

- 影响多个页面/模块
- 需要改公共协议
- 触及敏感路径

### 6.2 新接口落地 + UI dump/xml + data/ui 连接 + 持续微调

**输入特征**：

- 新接口
- UI 骨架生成
- data 层和 UI 层逐步连接
- 后续大量 delta 微调

**默认路由**：

```text
scenario route -> moderate/semi-auto
```

**continuation 入口**：

后续“再补一点 UI / 逻辑 / 测试”不重 triage，优先：

```text
continuation route -> continue current baseline
```

**升级条件**：

- 引入新依赖
- 数据模型被推翻
- 跨模块扩散
- 需要新架构决策

### 6.3 跨模块方案设计 / 路由重构 / 工程设计文档

**输入特征**：

- 多模块牵连
- 先设计后实现
- TDD 优先
- BDD / E2E / 设计文档

**默认路由**：

```text
scenario route -> complex/full
```

**附带要求**：

- spec-first
- ADR / 设计文档
- TDD
- 可能需要 slice / handoff / fresh session

---

## 7. 什么叫“可拔插”

这里的可拔插，不该理解为：

- 想走哪条就随便走

而应该理解为：

- 可以替换路由信号来源
- 可以替换 lane 模板
- 可以按项目启用/关闭某些入口

### 7.1 可拔插的层

推荐拆成三层：

1. **Signals**
   - score
   - explicit command
   - scenario detector
   - continuation detector

2. **Policy**
   - 优先级
   - 升级条件
   - fallback

3. **Lane templates**
   - simple/patch
   - moderate/semi-auto
   - complex/full

这样以后要改的只是：

- 替换场景模板
- 调整优先级
- 调整升级条件

而不是重写整个 workflow。

---

## 8. 推荐的最小路由结果结构

建议 triage 的输出不要只写 profile，而是写成：

```json
{
  "profile": "moderate",
  "lane": "moderate/semi-auto",
  "route_source": "scenario",
  "continuation": true,
  "ambiguity_score": 0.15,
  "hard_constraints": [],
  "upgrade_triggers": [
    "new_dependency",
    "cross_module_spread",
    "contract_change"
  ]
}
```

这里最关键的是 5 个字段：

- `lane`
- `route_source`
- `continuation`
- `ambiguity_score` — 补充：来自 Ouroboros 的 Ambiguity Gate，≤ 0.2 允许进入执行 [来源: workflow-research-ouroboros.md §3]
- `upgrade_triggers`

这样后续 phase 才知道自己为什么被路由到这里，以及什么情况下必须升级。

---

## 9. 对当前设计最值得补的改动

### P0

1. 把 triage 结果从 `profile only` 升级为 `profile + lane`
2. 增加 continuation route
3. 增加 scenario route

### P1

4. 固定路由优先级
5. 定义 lane 模板
6. 把 upgrade triggers 写成确定性规则

### P2

7. 再决定是否做成 command / hook / config 实现

---

## 10.5 补充：新 research 提供的路由实现参考

以下来自 7 份新 vendor research，补充 §9 的实施建议：

| 路由能力 | 参考 Vendor | 具体机制 | 如何借鉴 |
|---------|------------|---------|---------|
| Scope-aware ceremony | Compound Engineering | `ce:work` Phase 0 三级路由（trivial/small-medium/large）| Score route 的实现参考——按"信号量"而非"分数"路由 |
| Scenario keyword detection | oh-my-claudecode | `UserPromptSubmit` hook 14+ 关键词 → skill 注入 | Scenario route 的 keyword matching 实现 |
| Ambiguity quantification | Ouroboros | Ambiguity Gate（0-1 分，≤ 0.2 才执行）| Score route 新增 ambiguity 维度 |
| Single next action | PAUL | resume/status 命令只返回一个建议 | 路由结果简化——输出一个 action，不是一堆选项 |
| Task Schema 统一 | Claude-Code-Workflow | 统一 JSON 任务模型消费 plan/issue/review 输出 | 路由结果结构标准化 |
| Resume existing work | Compound Engineering | Phase 0.1 检测已有 brainstorm/plan → confirm → resume | Continuation route 的成熟实现 |

---

## 10. 最终裁决

workflow 的灵活性，不来自“只有一个评分器”，而来自：

- 多信号输入
- 稳定的优先级
- 可切换的 lane 模板
- 明确的升级条件

所以我支持的不是：

- “打分足够聪明就行”

我支持的是：

> **评分只是 router 的一个插件；真正好的 workflow，需要一个可拔插的 routing layer。**

一句话收束：

> 同一个骨架可以稳定，但入口必须灵活；真正可用的 workflow，不是只有 profile，而是 `profile × lane × route_source` 的组合。  
