# Workflow Research Report: skill-router

> **研究日期**: 2025-07  
> **仓库**: skill-router  
> **文件数**: ~70  
> **版本**: v0.5.0  
> **许可证**: 未明确声明  

---

## 1. 框架概况

skill-router 是一个 **low-presence runtime**，专注于减少 AI agent 环境中的 skill selection waste。核心理念："Use installed defaults first, discover only when genuinely insufficient." 系统通过 cluster-based routing 在拥挤的 skill 环境（50-100 个 skill）中保持沉默，仅在 routing 决策会改变下一步行动时才发声。v0.5 版本被称为 "ruthless reset"——大幅删减了旧版的 routing 逻辑，聚焦于 waste reduction 的本质。

| 属性 | 值 |
|------|------|
| **类型** | Low-Presence Skill Selection Runtime |
| **语言** | Markdown (skill 定义 + policy 文档) |
| **入口** | SKILL.md (自动加载) |
| **核心文件** | SKILL.md + docs/ + references/ |
| **设计哲学** | Anti-waste, silence as feature |
| **Decision Classes** | 11 种 (no_route, use_installed, discover_candidates...) |

---

## 2. 源清单

| 文件 | 用途 | 重要度 |
|------|------|--------|
| `SKILL.md` | 核心 runtime skill (4-step main path + output style) | ★★★ |
| `docs/how-it-works.md` | Main path 详解 (5 gates) | ★★★ |
| `docs/skill-router-v0.5-ruthless-reset.md` | v0.5 设计哲学 | ★★★ |
| `docs/why-skill-router.md` | Anti-waste 理论基础 | ★★☆ |
| `docs/public-surface.md` | Public contract 定义 | ★★☆ |
| `docs/skill-router-v0.5-gold-set-schema.md` | Gold-set 测试 schema | ★★★ |
| `docs/skill-router-v0.5-evaluator-spec.md` | 评估标准 + pass/fail 规则 | ★★☆ |
| `references/sufficiency-policy.md` | Genuine insufficiency 测试 | ★★★ |
| `references/crowded-environment-policy.md` | 拥挤环境过滤策略 | ★★☆ |
| `references/publish-safe-runtime-contract.md` | 5-point vetting checklist | ★★☆ |
| `references/task-to-skill-map.md` | 本地 default 记录 | ★★☆ |
| `references/default-update-policy.md` | Default 更新策略 | ★★☆ |
| `references/ambiguity-fallback-policy.md` | 歧义处理 fallback | ★★☆ |

---

## 3. 对象模型

### 核心实体

```
Task
  ├── description: string
  ├── quality_bar: default|low|high|production
  ├── explicit_skill_name: string?    # 用户显式指定
  └── allow_clarification: bool

Skill
  ├── name: string
  ├── description: string
  ├── trusted: bool
  ├── scope: string                   # 能力域
  ├── source_type: self|trusted_registry|third_party_unknown
  └── permissions: string[]

LocalDefault
  ├── scope: string                   # task 类型或 overlap cluster
  ├── skill: string                   # 首选 skill
  └── confidence: high|medium

LocalOverride
  ├── scope: string                   # 窄范围 task 类型
  ├── skill: string
  ├── source: explicit_user_preference
  └── durable: bool

DecisionClass (11 种)
  └── no_route | use_installed | use_active_skill | use_local_default
      | use_override | discover_candidates | vet_candidate
      | ask_one_clarification | allow_reasoned_comparison
      | allow_extended_reasoning | use_combination
```

### 实体关系

- **Task** 被 router 评估后产出一个 **DecisionClass**
- **Skill** 被分组为 **overlap cluster**（能力重叠的 skill 集合）
- **LocalDefault** 记录 recurring overlap cluster 的 stable decision
- **LocalOverride** 覆盖 default（仅限窄范围，不泄漏到不相关 task）

### Context 隔离

Router 本身是 stateless 的——每次评估独立进行。**LocalDefault** 和 **LocalOverride** 通过 `task-to-skill-map.md` 文件持久化，但仅用于加速决策，不影响 correctness。

---

## 4. 流程与状态机

### Main Path (5 Gates)

```
[Gate 0] 是否需要 routing?
   ├── 否 → disappear (no output)
   └── 是 ↓

[Gate 1] 已安装 skill 有 obvious match?
   ├── 是 → "Use X." (stop)
   └── 否 ↓

[Gate 2] Genuine Insufficiency Test
   ├── 已安装 skill sufficient → use installed (stop)
   │   (input compatible? output correct? quality sufficient?)
   └── 全部 No → genuine gap ↓

[Gate 3] Discover for real gap
   └── 候选列表 ↓

[Gate 4] Vet unfamiliar candidates
   ├── Pass → recommend
   ├── Conditional Pass → recommend with concern
   └── Fail → reject, suggest alternatives
```

### Genuine Insufficiency Test (3 条件全 Yes → sufficient)

```
1. Can installed skill accept the task INPUT?    (input compatibility)
2. Can installed skill produce the needed OUTPUT? (output type)
3. Is quality SUFFICIENT for user's purpose?      (quality bar)

任一 No → discovery justified
全部 Yes → use installed, stop
```

### 5-Point Vetting Checklist (Gate 4)

```
1. Stated Purpose Clarity — 描述是否具体、非模糊
2. Scope-to-Purpose Ratio — permissions 是否匹配 purpose
3. Source Accountability — 可追溯作者、仓库、版本
4. Behavioral Boundaries — 是否在 scope 内工作
5. Non-Technical User Test — 是否可以推荐给非技术用户
```

### Failure Paths

| 失败场景 | 系统响应 |
|----------|----------|
| Router 频繁发声但不改变决策 | "Routing theater" → 应用 "No default change, no voice" |
| 重复 discovery 相同 gap | 记录 stable default → 不再重新比较 |
| Override 泄漏到不相关 task | 检查 scope 边界 → 限制 override 范围 |
| 用户表达不信任 | 检查是否实际提高了 quality bar → 相应调整 |

---

## 5. 执行保障审计

| 机制 | 级别 | 说明 |
|------|------|------|
| "No default change, no voice" 规则 | **Hard** (policy) | Router 不改变决策时完全沉默 |
| Genuine Insufficiency Test (3 条件) | **Hard** (policy) | 必须全部 fail 才能触发 discovery |
| 5-Point Vetting Checklist | **Hard** (policy) | Unfamiliar candidate 必须通过 5 项检查 |
| Override scope 限制 | **Soft** | 文档要求窄 scope，但无自动 scope 检测 |
| Default 持久化 (task-to-skill-map.md) | **Soft** | 文件存在但手动维护 |
| Gold-set regression test | **Hard** | 100 个 test case 覆盖 11 个 decision class |
| Output 简洁性要求 | **Soft** | 文档要求短输出，但无 token 限制 hard check |
| Noise filtering (crowded env) | **Soft** | 策略文档完善，但过滤逻辑由 LLM 判断 |

---

## 6. Prompt 目录

### Prompt 1: Main Path Decision (SKILL.md 核心)

```
你是 Skill Router v0.5。沉默是特性，不是缺陷。

4 步主路径:
Step 0: Routing 是否会改变下一步行动? No → 不说话
Step 1: 已安装 skill 有明显匹配? Yes → "Use X." 然后停止
Step 2: Genuine insufficiency? No → 使用已安装 skill
Step 3: Discover 仅为真实 gap
Step 4: Vet unfamiliar candidates

输出规范:
- NO ROUTE: "This task does not need skill-router."
- OBVIOUS: "Use X."
- INSUFFICIENT: "The installed set is not enough; discover candidates."
- UNFAMILIAR: "Candidate is unfamiliar; vet before recommendation."
- RECURRING OVERLAP: "Use X." (记录为 default)

规则: 不解释未被请求的决策。
```

### Prompt 2: Sufficiency vs Technical Possibility

```
技术上可行 ≠ 充分

不充分的例子:
- 静态前端 skill → 实时协作产品 (不匹配)
- 通用自动化 skill → 生产级 K8s 部署 (质量不足)
- 弱格式化 skill → 专业出版流程 (质量不足)

Quality bar 信号词:
- 低信号: rough, okay, acceptable, quick draft, good enough
- 高信号: best possible, highest quality, professional, production-ready
```

---

## 7. 微观设计亮点

### 7.1 "Disappearing Router" Pattern

skill-router 最激进的设计决策：**最好的 routing 是看不见的 routing**。如果决策不改变下一步行动，router 完全沉默（不输出任何内容）。这与多数 AI 系统 "always respond" 的默认行为截然相反。

### 7.2 Quality Bar 语义分析

通过分析用户输入中的 signal words（"rough draft" vs "production-ready"）来动态调整 sufficiency 阈值。这是一种轻量级的 intent parsing——不需要复杂 NLU，仅靠关键词判断。

### 7.3 Gold-Set Schema (100 Cases × 11 Decision Classes)

定义了完整的 regression test schema，覆盖 no_route (15)、installed_default (20)、sufficiency_boundary (15)、discovery (10)、vetting (10)、override_governance (10)、crowded_environment (8)、ambiguity_clarification (7)、explanation_boundary (3)、combination_path (2)。这是在纯 prompt-based 系统中少见的严格测试规范。

---

## 8. 宏观设计亮点

### 8.1 "Anti-Waste" 作为核心价值主张

skill-router 将 routing waste 分解为 5 种具体形式：repeated discovery、repeated comparison、repeated installation、routing token waste、environmental entropy。每项设计决策都必须 **可衡量地减少** 至少一种 waste，否则不属于框架范畴。这种 "value must be measurable" 的纪律性在 AI agent 生态中极为罕见。

### 8.2 "Installed Beats Imagined" 原则

拒绝与假想工具比较——所有决策基于实际安装的 skill，不考虑 "可能存在更好的工具"。这防止了 routing 进入无限探索的 rabbit hole，也与实际工程中 "use what you have" 的实用主义一致。

---

## 9. 失败模式与局限

| # | 失败模式 | 严重度 | 说明 |
|---|----------|--------|------|
| 1 | **Routing theater** | 高 | Router 频繁发声但不改变决策，消耗 token 但无价值 |
| 2 | **Taxonomy creep** | 高 | 持续扩展分类体系，偏离 "focus on conflicts that change action" 目标 |
| 3 | **Repeated discovery** | 中 | 未记录 stable default，同一 gap 反复触发 discovery |
| 4 | **Noise-driven routing** | 中 | 大量已安装 skill 触发不必要的 routing 升级 |
| 5 | **Override leakage** | 中 | 窄范围 override 意外应用到不相关 task |
| 6 | **Vetting bypass** | 中 | Unfamiliar 第三方 skill 未经 5-point check 即被推荐 |
| 7 | **Explanation sprawl** | 低 | 输出长度超出决策应有的解释量 |
| 8 | **Ambiguity theater** | 低 | 呈现多选项而非提出 1 个最小澄清问题 |

---

## 10. 迁移评估

### 可迁移候选

| 机制 | 目标插件 | 可行性 | 备注 |
|------|----------|--------|------|
| Genuine Insufficiency Test | `meta/skill-dev` | ★★★ | Skill 选择逻辑可直接用于 skill 开发指导 |
| 5-Point Vetting Checklist | `meta/plugin-optimizer` | ★★★ | 第三方 skill 安全检查与 plugin-optimizer 完美互补 |
| Gold-Set Regression Schema | `quality/testing` | ★★☆ | 测试 schema 模式可作为 prompt testing 的范例 |
| "No default change, no voice" | 全局 hook | ★★★ | 减少不必要输出的原则适用于所有 skill |
| Crowded Environment Policy | `meta/skill-dev` | ★★☆ | 多 skill 环境的过滤策略 |

### 建议采纳顺序

1. **5-Point Vetting Checklist** → 直接集成到 plugin-optimizer 的 security review
2. **Genuine Insufficiency Test** → 作为 skill-dev 的 skill selection guide
3. **Gold-Set Schema** → 提取为通用 prompt regression test 模板

---

## 11. 开放问题

1. **Runtime overhead**: 在 50-100 skill 环境中，router 本身消耗多少 token？是否有 benchmark？
2. **Default convergence 速度**: 新环境中 LocalDefault 需要多少次交互才能 converge？
3. **Multi-router 冲突**: 如果多个插件各自包含 routing 逻辑，skill-router 如何处理？
4. **LLM 依赖**: 所有 policy 均由 LLM 执行判断，非 Claude 模型的 instruction-following 质量是否足以支撑这套复杂规则？
5. **v0.5 → v1.0 路线图**: "ruthless reset" 之后，哪些被删减的功能可能在 v1.0 回归？
