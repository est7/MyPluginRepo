# Workflow Research Report: CaludeSkills-Web-Gstack

> 生成时间：2025-07  
> 仓库：`vendor/CaludeSkills-Web-Gstack/`  
> 版本：无显式版本号 | 许可证：MIT | 作者：HruthikKommuru

---

## 1. 框架概况

| 维度 | 值 |
|------|-----|
| **类型** | Claude Web App 专用工程 workflow skill 包 |
| **文件数** | ~33 |
| **语言** | 纯 Markdown（SKILL.md 文件） |
| **入口** | 直接上传 SKILL.md 文件到 claude.ai Web 界面 |
| **平台** | Claude Web App（**无终端要求**） |
| **设计哲学** | 完整工程生命周期覆盖，从 ideation 到 retrospective |

这是从 gstack CLI 工具链**适配**而来的 12 个工程 workflow skill，专为 Claude Web 界面设计。与其他 vendor 不同的是，本框架**不需要终端环境**，所有 skill 通过文件上传激活，面向的是非工程师或无本地开发环境的用户群体。

---

## 2. 源清单

| 文件 / 目录 | 作用 |
|-------------|------|
| `README.md` | 项目概览、安装方式、推荐 workflow 顺序 |
| `gstack-web-skills/office-hours/SKILL.md` | YC Office Hours — idea 压力测试 |
| `gstack-web-skills/design-consultation/SKILL.md` | Design system 构建 |
| `gstack-web-skills/plan-ceo-review/SKILL.md` | CEO/Founder 模式战略审查 |
| `gstack-web-skills/plan-eng-review/SKILL.md` | Engineering Manager 架构审查 |
| `gstack-web-skills/plan-design-review/SKILL.md` | Designer 视角计划审查 |
| `gstack-web-skills/review/SKILL.md` | Pre-landing code review |
| `gstack-web-skills/investigate/SKILL.md` | 系统化 debugging |
| `gstack-web-skills/design-review/SKILL.md` | Visual QA audit |
| `gstack-web-skills/qa/SKILL.md` | QA 测试与修复 |
| `gstack-web-skills/ship/SKILL.md` | Ship workflow（merge → test → PR） |
| `gstack-web-skills/document-release/SKILL.md` | 发布后文档同步 |
| `gstack-web-skills/retro/SKILL.md` | 工程 retrospective |
| `gstack-web-skills.zip` | 全部 skill 的打包下载 |

---

## 3. 对象模型

### 核心实体

```
Skill Pack (12 skills)
    │
    ├── Ideation: office-hours
    ├── Planning: design-consultation, plan-ceo-review, plan-eng-review, plan-design-review
    ├── Review: review, investigate, design-review
    ├── Quality: qa, ship, document-release
    └── Retrospective: retro
```

每个 skill 是一个**独立的 SKILL.md 文件**，无跨 skill 依赖，无共享状态，无配置文件。这是所有 vendor 中**最扁平的对象模型**。

### Context 隔离

完全隔离——每个 skill 上传时作为独立 conversation context 存在。不同 skill 之间无状态传递机制。

---

## 4. 流程与状态机

### 推荐 Workflow 顺序

```
office-hours (ideation)
    → design-consultation (design system)
    → plan-ceo-review (strategic review)
    → plan-eng-review (technical review)
    → plan-design-review (design review)
    → [Build Phase — 用户自行编码]
    → review (code review)
    → design-review (visual QA)
    → qa (test & fix)
    → ship (merge + PR)
    → document-release (docs sync)
    → retro (retrospective)
```

### 每个 Skill 内部的 Phase 结构

以 `/office-hours` 为例：

```
Phase 1: Context Gathering (项目描述、目标选择)
Phase 2A: YC Product Diagnostic (6 Forcing Questions) [startup mode]
Phase 2B: Design Partner (generative questions) [builder mode]
Phase 3: Premise Challenge
Phase 4: Alternatives Generation (MANDATORY — 2-3 approaches)
Phase 5: Design Doc Generation
Phase 6: Handoff with Reflection
```

### 状态输出

每个 skill 在完成时输出标准化状态：
- `DONE` — 完成
- `DONE_WITH_CONCERNS` — 完成但有保留
- `NEEDS_CONTEXT` — 需要更多信息

**没有 phase gate 或 approval 机制**——skill 内部的 phase 流转是 AI 自主驱动的。

---

## 5. 执行保障审计

| 机制 | 级别 | 说明 |
|------|------|------|
| `/review` 的 Fix-First 策略 | **Soft** | "Every finding gets action" — 每个发现必须产出修复或 ASK |
| `/investigate` 的 Iron Law | **Soft** | "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST" — 仅为文本约束 |
| `/qa` 的 Self-Regulation 风险上限 | **Soft** | 每 5 个 fix 评估风险，风险 >20% 停止，硬上限 50 fixes |
| `/ship` 的 Verification Gate | **Soft** | "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION" — 代码变更后必须重跑测试 |
| `/plan-design-review` 的 7-Pass 评分 | **Soft** | 7 个维度 0-10 评分，提供 before/after 对比 |
| Alternatives Generation | **Soft** | `/office-hours` 要求 "MANDATORY — 2-3 distinct approaches"，但 AI 可能忽略 |
| 跨 skill 状态传递 | **Unenforced** | 无机制在 skill 间传递审查结论或文档 |

**总评**：所有保障均为 **Soft** 级别——通过 prompt 文本约束 AI 行为，无技术强制手段。这与"纯 Web 界面、无终端"的定位一致——没有 hook 或 CI 可以依赖。

---

## 6. Prompt 目录

### Prompt 1: Office Hours — Six Forcing Questions

```markdown
# YC Product Diagnostic (Startup Mode)
1. Demand Reality — evidence someone wants this
2. Status Quo — what are users doing now?
3. Desperate Specificity — name the actual user
4. Narrowest Wedge — smallest version someone would pay for
5. Observation & Surprise — what surprised you watching users?
6. Future-Fit — does the product become more essential in 3 years?
```

**设计意图**：借鉴 YC（Y Combinator）的 office hours 方法论，通过 6 个结构化"强迫性问题"将 AI 变成严格的产品思维教练。

### Prompt 2: QA — Self-Regulation Risk Protocol

```markdown
# Self-Regulation
- Every 5 fixes, evaluate risk
- Each revert: +15% risk
- Each fix touching >3 files: +5% risk
- After fix 15: +1% per additional fix
- If risk > 20%: STOP and ask user
- Hard cap: 50 fixes
```

**设计意图**：这是一个精巧的 **AI 行为熔断器**——通过量化风险积累模型，防止 AI 在 QA 过程中过度修改导致系统崩溃。revert 的 15% 惩罚权重尤其体现了对"修复导致新问题"循环的警惕。

---

## 7. 微观设计亮点

### 7.1 AI Slop Detection 作为 Design Audit 维度

`/design-review` 和 `/plan-design-review` 中将 **AI slop**（AI 生成的视觉通病）列为独立审查维度。具体 pattern 包括：purple/violet gradients、3-column feature grids、centered everything、uniform bubbly border-radius、decorative blobs。这种**用 AI 检测 AI 生成痕迹**的自反性设计极具前瞻性。

### 7.2 Health Score 量化模型

`/qa` 为测试结果计算 0-100 分的 Health Score，使用加权公式（Console 15%、Functional 20%、Accessibility 15% 等）。这将主观的"质量感受"转化为**可比较的量化指标**，使得跨项目/跨时间的质量对比成为可能。

### 7.3 Fix-First Review 模式

`/review` 的核心原则是"Fix-First, not Read-Only"——每个发现必须归类为 `AUTO-FIX`（机械性修复，直接执行）或 `ASK`（需要判断，提交用户）。这将 code review 从**发现问题**推进到**解决问题**，极大提升了 review 的 ROI。

---

## 8. 宏观设计亮点

### 8.1 "No Terminal Required" 的极致简化

通过将所有 skill 设计为纯 Markdown 上传格式，框架将目标用户扩展到**无开发环境的用户群体**。这种设计牺牲了自动化能力（无 hook、无 CI、无 bash），但换来了**零配置的即时可用性**。

### 8.2 工程生命周期的完整映射

12 个 skill 覆盖了从 ideation（office-hours）到 retrospective（retro）的完整工程生命周期，且每个 skill 都带有**强烈的工程管理方法论**（YC office hours、7-pass design review、TDD）。这不是一个技术工具集，而是一个**编码为 AI 指令的工程管理框架**。

---

## 9. 失败模式与局限

| # | 失败模式 | 影响 | 可能性 |
|---|----------|------|--------|
| 1 | **无状态传递** — skill 间无法传递上下文（如 office-hours 的 design doc 无法自动流入 plan-ceo-review） | 用户需手动复制粘贴前序 skill 的输出 | 高 |
| 2 | **Web 界面限制** — 无法执行 bash 命令、无法读写文件、无法运行测试 | `/ship`、`/qa` 等需要终端的 skill 功能大打折扣 | 高 |
| 3 | **Framework-specific QA 失效** — `/qa` 包含 Next.js、Rails、SPA 的特定检查，但 Web 界面无法访问项目代码 | QA 退化为建议列表而非实际检测 | 高 |
| 4 | **Retro 依赖 git log** — `/retro` 要求用户手动执行 4 条 git 命令并粘贴输出 | 非技术用户无法使用 | 中 |
| 5 | **单 SKILL.md 文件大小** — 部分 skill（如 `/qa`、`/design-review`）内容极长，可能超出 Web 界面的单次上传 token 限制 | Skill 被截断 | 中 |

---

## 10. 迁移评估

### 可移植候选

| Skill | 目标位置（1st-cc-plugin） | 优先级 | 改造量 |
|-------|--------------------------|--------|--------|
| `review`（Fix-First code review） | `quality/refactor` 或 `quality/codex-review` | P1 | 提取 AUTO-FIX / ASK 分类机制 |
| `investigate`（Iron Law debugging） | 新建或扩展 `quality/testing` | P1 | Root cause 优先的 debug 协议 |
| `qa`（Self-Regulation + Health Score） | `quality/testing` | P2 | 风险熔断器 + 量化评分模型 |
| `design-review`（AI Slop Detection） | `quality/ai-hygiene` | P2 | AI slop pattern 列表直接可用 |
| `office-hours`（6 Forcing Questions） | `quality/clarify` | P3 | 产品思维压力测试 |

### 建议采纳顺序

1. **Fix-First review protocol** + **Root-cause debugging** → 直接增强现有 quality skill
2. **QA risk circuit breaker** → 作为通用 pattern 写入 skill-dev 规范
3. **AI Slop Detection** → 扩展 `quality/ai-hygiene` 的检测维度

---

## 11. 开放问题

1. **gstack CLI 与 Web skill 的功能差异**：Web 版是 CLI 版的子集还是独立设计？CLI 版是否有更多自动化能力？
2. **SKILL.md 大小上限**：Claude Web 界面上传 SKILL.md 的实际 token 处理上限是多少？较长的 skill（如 `/qa` 超过 400 行）是否会被截断？
3. **Completion Status 的消费方**：`DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` 状态输出后由谁消费？在 Web 界面中似乎无下游消费者。
4. **Font blacklist 的维护**：`/design-consultation` 中的字体黑名单（Papyrus, Comic Sans 等）和过度使用字体列表（Inter, Roboto 等）是静态列表，如何应对设计趋势变化？
