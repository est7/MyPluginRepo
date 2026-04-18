# Workflow Research Report: Agent-Skills-for-Context-Engineering

> 生成时间：2025-07  
> 仓库：`vendor/Agent-Skills-for-Context-Engineering/`  
> 版本：v2.1.0 | 许可证：MIT | 作者：Muratcan Koylan

---

## 1. 框架概况

| 维度 | 值 |
|------|-----|
| **类型** | Claude Code plugin marketplace — context engineering 教学 skill 集合 |
| **文件数** | ~242 |
| **语言** | Markdown（SKILL.md）+ TypeScript/Python（examples）|
| **入口** | `.claude-plugin/marketplace.json` → 单一 `context-engineering` plugin → 14 个 skill 目录 |
| **平台** | 平台无关（Claude Code / Cursor / Copilot / Open Plugins 均可） |
| **设计哲学** | Progressive disclosure + 学术级 context engineering 教学 |

框架本身**不是工作流引擎**，而是一个**知识型 skill 集合**，将 context engineering 理论编码为可被 AI 按需加载的结构化指令。每个 skill 独立可用，也可组合使用。

---

## 2. 源清单

| 文件 / 目录 | 作用 |
|-------------|------|
| `.claude-plugin/marketplace.json` | Claude Code marketplace manifest，注册 1 个 plugin 含 14 skills |
| `.plugin/plugin.json` | Open Plugins v2.0.0 标准元数据 |
| `CLAUDE.md` | 项目级 AI 指导：结构、authoring rules、build commands |
| `SKILL.md`（root） | Collection skill — 全局入口，列出 skill map 和激活条件 |
| `skills/context-fundamentals/SKILL.md` | 基础 skill：context window anatomy、attention budget、U-shaped recall |
| `skills/context-degradation/SKILL.md` | 降级识别：context 质量下降的 pattern 检测 |
| `skills/context-compression/SKILL.md` | 压缩策略：token 预算优化 |
| `skills/multi-agent-patterns/SKILL.md` | 多 agent 协调模式 |
| `skills/memory-systems/SKILL.md` | 记忆系统设计 |
| `skills/tool-design/SKILL.md` | Tool 设计：tool-agent interface、consolidation principle |
| `skills/filesystem-context/SKILL.md` | 基于文件系统的 context 管理 |
| `skills/hosted-agents/SKILL.md` | 托管 agent 基础设施 |
| `skills/latent-briefing/SKILL.md` | Latent KV sharing between agents |
| `skills/evaluation/SKILL.md` | 评估框架 |
| `skills/advanced-evaluation/SKILL.md` | 高级评估（LLM-as-judge） |
| `skills/project-development/SKILL.md` | 项目开发方法论 |
| `skills/bdi-mental-states/SKILL.md` | BDI（Belief-Desire-Intention）认知架构 |
| `skills/context-optimization/SKILL.md` | Context 优化策略 |
| `examples/` | 5 个完整示例项目（digital-brain, x-to-book, llm-as-judge 等） |
| `template/SKILL.md` | Canonical skill 模板 |

---

## 3. 对象模型

### 核心实体

```
Marketplace ─── 1:1 ──→ Plugin ─── 1:N ──→ Skill
                                              │
                                              ├── SKILL.md (YAML frontmatter + body)
                                              ├── references/ (optional)
                                              └── scripts/ (optional)
```

- **Marketplace**（`marketplace.json`）：注册入口，定义 owner 和版本
- **Plugin**（`context-engineering`）：单一 plugin 容器，包裹全部 14 skills
- **Skill**：独立可加载单元，由 YAML frontmatter（`name`, `description`）和 Markdown 指令体组成
- **Example**：完整应用项目，展示 skill 组合使用

### Context 隔离

所有 14 个 skill 打包在**同一个 plugin** 中（"single plugin to avoid cache duplication"），skill 之间通过**纯文本引用**（"skills reference each other via plain text"）互相关联，无运行时耦合。每个 skill 的 SKILL.md 控制在 500 行以内。

---

## 4. 流程与状态机

本框架**没有强制执行的状态机**。其"流程"是概念性的知识层级关系：

```
Foundational           Architectural           Operational
    │                      │                       │
    ▼                      ▼                       ▼
context-fundamentals → multi-agent-patterns → context-optimization
context-degradation  → memory-systems        → latent-briefing
context-compression  → tool-design           → evaluation
                     → filesystem-context     → advanced-evaluation
                     → hosted-agents
```

**Happy Path**：
1. 用户触发 context 相关问题 → AI 加载 `context-fundamentals`
2. 深入特定子领域 → 按需加载专项 skill
3. 需要评估 → 加载 `evaluation` / `advanced-evaluation`

**没有 phase gate 或 approval 机制**——skill 加载是完全按需的。

---

## 5. 执行保障审计

| 机制 | 级别 | 说明 |
|------|------|------|
| SKILL.md 500 行限制 | **Soft** | 仅在 CLAUDE.md 中声明，无自动校验 |
| YAML frontmatter 必需 | **Soft** | 约定要求 `name` + `description`，无 schema 校验 |
| 平台无关原则 | **Soft** | Authoring rule #5，靠人工遵守 |
| Token 意识写作 | **Soft** | 指导原则，无量化 token 预算检查 |
| Marketplace manifest 完整性 | **Soft** | 需手动同步新 skill 到 manifest |
| 内容质量 | **Unenforced** | 无 linting/测试对 skill 内容的校验 |
| Skill 触发条件 | **Unenforced** | README 列出 trigger 词，但 AI 自行判断何时加载 |

**总评**：保障层级整体偏软，依赖作者自律和 review 流程。examples 目录中的项目有独立测试（vitest、pytest），但 skill 内容本身缺乏自动化验证。

---

## 6. Prompt 目录

### Prompt 1: Context Fundamentals — Attention Budget 模型

```markdown
# When to Activate
Designing new agent systems, debugging context issues, optimizing context usage

# Core Teaching
- 将 context 视为有限的 attention budget
- 有效容量仅为标称窗口的 60-70%
- U-shaped attention curve：开头/结尾 recall 85-95%，中间仅 76-82%
- Progressive disclosure 三级策略
```

**设计意图**：通过"budget"隐喻让 AI 理解 context 是稀缺资源，从而自主控制 context 使用策略。

### Prompt 2: Tool Design — Consolidation Principle

```markdown
# Core Principle
Design every tool as contract between deterministic system and non-deterministic agent.
If humans can't disambiguate tool purposes, agents can't either.
Tool descriptions ARE prompt engineering that shapes agent behavior.
```

**设计意图**：将 tool 设计提升为 prompt engineering 的延伸，强调描述质量直接影响 agent 行为。

---

## 7. 微观设计亮点

### 7.1 Gotchas Section 反模式库

每个 skill 末尾包含 **Gotchas** 小节，列举 5-8 个常见陷阱。例如 `context-fundamentals` 列出"nominal window ≠ effective capacity"、"tool schemas inflate 2-3x after JSON serialization"等。这种**先教原理再列反模式**的结构极大降低了 AI 犯错的概率。

### 7.2 学术引用嵌入

框架在 README 和 skill 中直接引用学术论文（Meta Context Engineering via Agentic Skill Evolution、Peking University SKAI），并将论文结论转化为可操作的 skill 指令。这种**学术→工程**的转化路径在同类项目中罕见。

### 7.3 Single Plugin 架构

14 个 skill 刻意打包在单一 plugin 中而非分散注册，原因是"避免 cache 重复"。这体现了对**运行时 token 成本**的深度理解——多 plugin 会导致每个 plugin 的元数据独立占用 context 空间。

---

## 8. 宏观设计亮点

### 8.1 "Context as Finite Attention Budget" 统一隐喻

整个框架围绕一个核心隐喻构建：**context 是有限的注意力预算**。这不仅是教学工具，更是设计约束——所有 skill 的写作本身都受此约束（500 行限制、progressive disclosure、token-conscious authoring）。框架**以身作则**地实践了它所教授的原则。

### 8.2 Platform Agnosticism 作为一等公民

同时维护 `.claude-plugin/marketplace.json`（Claude Code 专用）和 `.plugin/plugin.json`（Open Plugins 标准），加上 Cursor indexing ignore 文件，显示出对**跨平台可移植性**的战略性投入。这在 Claude Code plugin 生态中极为少见。

---

## 9. 失败模式与局限

| # | 失败模式 | 影响 | 可能性 |
|---|----------|------|--------|
| 1 | **Skill 过载** — 14 个 skill 注册在单一 plugin 中，AI 可能频繁误触发不相关 skill | 浪费 token、干扰任务 | 中 |
| 2 | **纯教学无执行** — skill 提供知识但不执行具体操作（无 bash command、无文件修改），用户期望"做事"时只得到"建议" | 用户体验落差 | 高 |
| 3 | **内容老化** — 学术引用和 best practice 会随 LLM 发展过时，但无自动化更新机制 | 误导性指导 | 中 |
| 4 | **无验证闭环** — skill 教授了"如何评估 context 质量"，但自身无法验证 AI 是否正确执行了建议 | 效果不可测量 | 高 |
| 5 | **Examples 维护负担** — 5 个独立项目（TypeScript + Python）各有独立依赖，容易 bitrot | 示例失效 | 中 |

---

## 10. 迁移评估

### 可移植候选

| Skill | 目标位置（1st-cc-plugin） | 优先级 | 改造量 |
|-------|--------------------------|--------|--------|
| `context-fundamentals` | 新建 `quality/context-engineering` | P1 | 需从教学体裁改写为操作指令 |
| `tool-design` | `meta/skill-dev` 扩展 | P2 | 提取 tool naming / consolidation 部分 |
| `context-compression` | `quality/context-engineering` | P2 | 压缩策略可操作化 |
| `evaluation` | `quality/testing` 扩展 | P3 | LLM-as-judge 评估模式移植 |

### 建议采纳顺序

1. **先提取原则**：将 context budget、U-shaped attention、progressive disclosure 写入 `1st-cc-plugin` 全局 CLAUDE.md 的设计规范中
2. **再移植 skill**：选择 `context-fundamentals` + `tool-design` 作为首批，改写为操作型指令
3. **最后引入评估**：将 `evaluation` 模式整合到 `quality/testing` 中

---

## 11. 开放问题

1. **Skill 触发冲突**：14 个 skill 的 trigger 词存在大量重叠（如 "agent architecture" 同时匹配 `context-fundamentals`、`multi-agent-patterns`、`hosted-agents`），AI 如何确定加载优先级？
2. **知识 vs 执行边界**：本框架定位为"教学"，但 AI 在实际任务中何时应用知识、何时忽略知识的决策权完全委托给模型，缺乏显式控制机制。
3. **版本漂移**：`.claude-plugin/marketplace.json` 版本为 2.1.0，root `SKILL.md` 版本为 1.3.0，`.plugin/plugin.json` 版本为 2.1.0——多版本号之间缺乏同步策略。
4. **BDI Mental States skill** 引入了认知科学概念（Belief-Desire-Intention），其在实际 agent 系统中的可操作性有待验证。
