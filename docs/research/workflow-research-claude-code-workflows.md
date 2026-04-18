# Workflow Research Report: claude-code-workflows

> **研究对象：** claude-code-workflows（by Patrick Ellis）
> **研究日期：** 2025-07
> **分类：** Pure-markdown review workflow templates

---

## 1. 框架概况

`claude-code-workflows` 是一个由 Patrick Ellis 开发的 **纯 Markdown/YAML 模板集合**，采用 MIT license 发布。整个仓库仅包含 **16 个文件**，不包含任何 `package.json` 或编程语言代码 — 所有逻辑完全通过 prompt 工程和 GitHub Actions YAML 配置实现。

框架的核心设计采用 **Dual-loop 架构**：

| 循环层 | 机制 | 触发方式 |
|--------|------|----------|
| Inner Loop | Slash commands + Subagents | 开发者在 Claude Code 中手动调用 |
| Outer Loop | GitHub Actions CI workflows | PR 事件自动触发 |

框架覆盖三个独立的 review 领域：**Code Review**（代码质量审查）、**Security Review**（安全漏洞扫描）和 **Design Review**（UI/UX 设计评审）。三者共享 dual-loop 架构但各自独立运作，无交叉依赖。

---

## 2. 源清单

| 路径 | 规模 | 职责 |
|------|------|------|
| `code-review/claude-code-review.yml` | GitHub Actions | 标准 code review CI workflow，PR 触发，使用 claude-opus-4-1 模型 |
| `code-review/claude-code-review-custom.yml` | GitHub Actions | 可定制版 code review CI workflow |
| `code-review/pragmatic-code-review-slash-command.md` | Slash command | Inner loop code review 的 prompt 定义，包含 Pragmatic Quality Framework |
| `code-review/code-review-subagent.md` | Subagent 定义 | Code review subagent 的角色和行为约束 |
| `security-review/security.yml` | GitHub Actions | 安全审查 CI workflow，引用 `anthropics/claude-code-security-review@main` |
| `security-review/security-review-slash-command.md` | Slash command | Inner loop 安全审查的 prompt 定义 |
| `design-review/design-review-slash-command.md` | Slash command | Design review 的 7 阶段 Playwright-based 审查流程 |
| `design-review/design-review-agent.md` | Subagent 定义 | Design review agent 的角色和评审标准 |
| `design-review/design-principles.md` | 参考文档 | 可定制的设计原则文档，供 design review 参考 |

整个框架 **零运行时依赖** — 不需要安装任何 npm 包或编译任何代码。用户只需将对应的 YAML 文件复制到 `.github/workflows/`，将 slash command 复制到 `.claude/commands/`，即可立即使用。

---

## 3. 对象模型

### 核心实体

由于框架本身不包含编程逻辑，其"对象模型"完全由 prompt 结构和 YAML 配置定义：

- **Review（审查）：** 逻辑上的顶层概念，分为 Code Review、Security Review 和 Design Review 三类。每类 review 独立运作，拥有各自的评判标准和输出格式。
- **Quality Framework：** Code review 的核心评判框架，定义了 7 级优先级层次：Architecture > Functionality > Security > Maintainability > Testing > Performance > Dependencies。该层次决定了审查意见的排序和重要性权重。
- **Vulnerability Category：** Security review 定义了 5 个漏洞分类，基于 OWASP Top 10 映射。每个发现的漏洞需要标注置信度分数，仅 >80% 的发现才会被报告。
- **Design Phase：** Design review 包含 7 个顺序执行的阶段：Preparation → Interaction → Responsiveness → Visual → Accessibility (WCAG 2.1 AA) → Robustness → Summary。
- **False-Positive Exclusion：** Security review 硬编码了 17 条 false-positive 排除规则，防止已知的误报噪音干扰审查结果。

### 上下文隔离

三个 review 系统完全独立，不共享状态或配置。Inner loop（slash command）和 outer loop（GitHub Actions）之间也没有状态传递 — 它们是同一审查逻辑的两种独立触发方式，分别适用于开发阶段（本地）和集成阶段（CI）。

---

## 4. 流程与状态机

### Code Review — Happy Path

```
PR 提交 → GitHub Actions 触发 / 开发者调用 /review
    ↓
上下文收集（diff、文件列表、PR 描述）
    ↓
Pragmatic Quality Framework 7 级评估
    Architecture → Functionality → Security →
    Maintainability → Testing → Performance → Dependencies
    ↓
生成 inline comments（通过 gh CLI）
    ↓
汇总审查意见
```

Inner loop 通过 slash command 触发，Claude 直接在终端输出审查意见。Outer loop 通过 GitHub Actions 触发，Claude 以 PR comment 形式提交审查意见，工具约束限制为 `gh` CLI + inline comments。模型指定为 `claude-opus-4-1`。

### Security Review — Happy Path

```
PR 提交 → GitHub Actions 触发 / 开发者调用 slash command
    ↓
三阶段分析：
  Phase 1: Context（收集变更上下文）
  Phase 2: Comparative（与 OWASP Top 10 对照）
  Phase 3: Assessment（评估严重性和置信度）
    ↓
置信度过滤（>80% threshold）
    ↓
17 条 false-positive exclusion 规则过滤
    ↓
输出：HIGH / MEDIUM / LOW 严重性分级
```

安全审查的三阶段分析（Context → Comparative → Assessment）确保了判断的系统性。17 条 hard false-positive exclusion 在最终输出前移除已知误报，显著提高信噪比。

### Design Review — Happy Path

```
目标 URL/组件 → Playwright 启动浏览器
    ↓
7 阶段顺序执行：
  1. Preparation（准备，加载设计原则文档）
  2. Interaction（交互测试，点击/输入/导航）
  3. Responsiveness（响应式测试，多断点）
  4. Visual（视觉一致性检查）
  5. Accessibility（WCAG 2.1 AA 合规检查）
  6. Robustness（健壮性，错误状态/边界输入）
  7. Summary（汇总报告）
```

Design review 独特之处在于它是 **活体审查** — 通过 Playwright 真实操作浏览器，而非静态代码分析。

### 失败路径

- **置信度不足：** Security review 中置信度 ≤80% 的发现被静默丢弃，不产生审查意见。这可能导致真正的低置信度漏洞被遗漏。
- **Playwright 环境缺失：** Design review 依赖 Playwright 和浏览器环境，在 CI 或无头环境中可能因缺少依赖而失败。
- **Tool constraint 违反：** 如果 Claude 尝试调用 allowed-tools 白名单之外的工具，GitHub Actions 配置会拒绝执行。

---

## 5. 执行保障审计

| 保障机制 | Hard Gate | Soft Check | Unenforced |
|----------|-----------|------------|------------|
| Tool constraint 白名单（`allowed-tools` in YAML） | ✅ GitHub Actions 配置层强制限制可用工具集 | | |
| GitHub Actions trigger gates（PR 事件触发） | ✅ 仅在指定事件（如 `pull_request`）时触发，无法手动绕过 | | |
| 置信度阈值（>80%）| ✅ 低于阈值的 security finding 被硬过滤 | | |
| 17 条 false-positive exclusion | ✅ 硬编码排除列表，匹配即过滤 | | |
| OWASP Top 10 覆盖 | | ✅ Prompt 指导覆盖 OWASP Top 10，但不验证是否完整覆盖 | |
| Review 哲学 "Net Positive > Perfection" | | ✅ Prompt 引导优先提供建设性意见，但无量化执行 | |
| Nitpick 前缀 "Nit:" | | ✅ Prompt 要求小问题加 "Nit:" 前缀，但无格式校验 | |
| 假设 CI 已通过 | | ✅ Prompt 指示不要重复 CI 已覆盖的检查 | |
| Pragmatic Quality Framework 7 级层次 | | ✅ 作为 prompt 指导，不强制输出必须覆盖所有层次 | |
| WCAG 2.1 AA 合规 | | ✅ Design review 检查无障碍性，但依赖 Playwright 的运行环境 | |
| 模型选择（claude-opus-4-1） | ✅ YAML 中硬编码模型版本 | | |
| Design principles 对齐 | | | 设计原则文档可自定义但无校验机制确保其被实际参考 |

---

## 6. Prompt 目录

### 6.1 Pragmatic Code Review（核心摘录）

Code review slash command 的 prompt 定义了审查哲学和优先级框架：

> "Apply the Pragmatic Quality Framework. Prioritize issues in this order: Architecture > Functionality > Security > Maintainability > Testing > Performance > Dependencies. Focus on SOLID, DRY, KISS, YAGNI principles. Your review should be net-positive — improve the code, don't just criticize it. Prefix minor nitpicks with 'Nit:' to clearly distinguish them from significant concerns. Assume CI checks have already passed; do not duplicate their work."

该 prompt 通过明确的优先级层次和"Net Positive"哲学，将 Claude 的审查行为从"找错误"引导为"提升代码质量"。

### 6.2 Security Review False-Positive Exclusion（核心摘录）

Security review 的 prompt 包含一份详细的 false-positive 排除清单：

> "Hard false-positive exclusions (DO NOT report these): [17 specific patterns]. Apply 3-phase analysis: Phase 1 Context — gather all relevant changed code and understand the change intent. Phase 2 Comparative — map findings against OWASP Top 10 categories. Phase 3 Assessment — assign severity (HIGH/MEDIUM/LOW) and confidence score. Only report findings with confidence >80%."

17 条排除规则是该框架最具实用价值的工程产物之一，将作者在实际安全审查中积累的经验固化为可复用的过滤规则。

---

## 7. 微观设计亮点

### 7.1 Confidence Scoring 的信噪比优化

Security review 引入的 >80% confidence threshold 是一个精妙的设计选择。安全扫描工具的最大痛点是误报泛滥，开发者逐渐对告警产生"狼来了"效应。通过要求 Claude 对每个发现自评置信度并过滤低置信度结果，框架在覆盖率和可操作性之间取得了务实的平衡。

### 7.2 Tool Constraint 作为行为边界

Code review 的 GitHub Actions 配置通过 `allowed-tools` 白名单将 Claude 的能力限制为 `gh` CLI + inline comments。这不仅是安全措施，更是一种 **行为边界设计** — 通过限制工具来约束 agent 的行为空间，确保 code review 只产生评论而不意外修改代码。

### 7.3 Design Review 的 7 阶段 Playwright 集成

将 design review 拆分为 7 个明确的阶段（从 Preparation 到 Summary），并通过 Playwright 进行实际的浏览器交互，是一种将 **结构化审查方法论** 与 **自动化测试工具** 结合的创新尝试。这使得设计审查不再依赖截图或主观描述，而是基于真实的交互行为。

---

## 8. 宏观设计亮点

### 8.1 Zero-Dependency 纯 Prompt 工程

整个框架没有一行运行时代码，完全通过 Markdown prompt 和 YAML 配置实现。这是 **prompt-as-code** 理念的极端实践 — 所有审查逻辑、质量标准、行为约束都编码在自然语言中。这种方式的优势在于极低的采纳成本（复制文件即可）和极高的可定制性（修改文本即可调整行为），但代价是缺乏类型安全和程序化验证。

### 8.2 Dual-Loop 互补架构

Inner loop（本地 slash command）和 outer loop（CI GitHub Actions）的设计体现了 **开发阶段互补** 的理念：开发者在编码时通过 slash command 获得即时反馈，代码提交后通过 CI 获得标准化的自动审查。两个循环使用相同的审查标准但触发方式不同，确保审查覆盖了从开发到集成的完整流程。

---

## 9. 失败模式与局限

### 9.1 Prompt 遵从性的不可靠性

所有审查逻辑都通过 prompt 指令实现，而 LLM 对 prompt 的遵从性是概率性的。在复杂代码变更中，Claude 可能跳过低优先级层次的检查，或在 security review 中忽略某些 false-positive exclusion 规则。没有程序化的后置验证来确保 prompt 中的每条规则都被正确执行。

### 9.2 Confidence Scoring 的主观性

Security review 的 >80% confidence threshold 依赖 Claude 自身的置信度评估。然而，LLM 的"置信度"与实际准确率之间没有校准保证 — Claude 可能对一个错误判断给出 95% 的置信度，也可能对一个正确发现给出 70% 的置信度。这使得 threshold 机制在理论上合理但在实践中可能产生不可预测的过滤结果。

### 9.3 Design Review 的环境依赖

Playwright-based design review 要求目标应用正在运行且可访问，同时需要 Playwright 和浏览器环境正确安装。这在 CI 环境中通常可以配置，但在本地开发环境中可能因各种环境差异而产生问题，降低了该模块的可移植性。

### 9.4 False-Positive Exclusion 的维护成本

17 条 false-positive exclusion 规则是基于特定时间点的经验总结。随着安全态势的演变和新攻击向量的出现，这份列表需要持续维护和更新。硬编码在 prompt 中的排除规则缺乏版本管理和变更追踪机制，容易逐渐过时。

### 9.5 缺乏 Review 结果的持久化和趋势分析

框架仅关注单次 review 的执行，不提供 review 结果的聚合、趋势分析或历史对比。团队无法回答"过去一个月最常见的代码质量问题是什么"或"安全问题的修复率如何"等管理问题。

---

## 10. 迁移评估

### 值得移植到 1st-cc-plugin 的候选项

| 候选项 | 目标插件 | 优先级 | 理由 |
|--------|----------|--------|------|
| Pragmatic Quality Framework（7 级层次） | `quality/refactor` 或 `quality/codex-review` | 高 | 现有 codex-review 缺乏结构化的优先级框架，该 7 级层次可显著提升审查意见的组织性 |
| Security review 三阶段分析 + confidence scoring | 新建 `quality/security-review` | 高 | 1st-cc-plugin 目前缺少专用的安全审查插件，该方案提供了成熟的方法论 |
| 17 条 false-positive exclusion 规则 | 随 security review 一同移植 | 高 | 这是经过实战验证的工程产物，直接提升安全审查的信噪比 |
| Dual-loop 架构模式（slash cmd + CI） | 通用模式参考 | 中 | 作为插件设计的参考模式，指导其他插件同时提供本地和 CI 两种触发方式 |
| Design review 7 阶段模型 | 扩展 `platforms/shadcn` 或新建 `quality/design-review` | 低 | Playwright 依赖增加了采纳门槛，且 shadcn 已部分覆盖 UI 审查需求 |
| "Nit:" 前缀约定和 "Net Positive" 审查哲学 | `quality/codex-review` | 中 | 提升审查意见的可操作性，区分关键问题和小建议 |

### 建议采纳顺序

1. **首先移植 Pragmatic Quality Framework** 到 codex-review — 这是最高 ROI 的改进，仅需修改 prompt 文本，无运行时依赖。
2. **其次新建 security-review 插件** — 将三阶段分析、confidence scoring 和 false-positive exclusion 打包为独立插件。
3. **然后将 "Net Positive" 哲学和 "Nit:" 约定** 融入 codex-review 的 SKILL.md。
4. **最后评估 design review** — 仅在团队有 Playwright 基础设施时考虑。

---

## 11. 开放问题

1. **Confidence threshold 80% 的校准依据是什么？** 该阈值是基于经验选择还是有量化实验支持？是否需要根据项目类型（Web app vs CLI tool vs library）调整阈值？
2. **17 条 false-positive exclusion 的完整列表是否公开？** 需要完整列表才能评估其覆盖范围和可移植性。
3. **Dual-loop 架构中，inner loop 和 outer loop 的审查结果是否一致？** 由于触发上下文不同（本地 diff vs PR diff），两个循环可能对相同代码给出不同意见。是否存在一致性测试？
4. **`anthropics/claude-code-security-review@main` 的版本稳定性如何？** Security review 的 GitHub Actions 引用了 `@main` 分支，这意味着上游的任何 breaking change 都会立即影响下游用户。
5. **Design review 的 Playwright 操作是否有超时和容错机制？** 7 个阶段的顺序执行中，如果某个阶段因网络超时或元素不可达而失败，是否会中止整个审查还是跳过该阶段继续？
6. **Code review 指定 `claude-opus-4-1` 模型是否为硬性要求？** 对于大型 PR 的 review，opus 模型的 token 成本可能过高。是否有使用 sonnet 等更经济模型的降级方案？
