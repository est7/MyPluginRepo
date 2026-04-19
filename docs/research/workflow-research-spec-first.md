# Workflow Research Report: spec-first

> 逆向工程研究报告 — 生成时间：2025-07-18

---

## 1. 框架概况

| 维度 | 说明 |
|------|------|
| **类型** | AI Workflow CLI + Plugin 系统 |
| **文件数** | ~1045 files |
| **语言** | JavaScript (Node.js)，中文优先文档 |
| **包名** | `spec-first`（npm package）|
| **入口** | `bin/spec-first.js`（CLI）、`bin/postinstall.js`（安装后钩子）|
| **范式** | 6 阶段闭环开发流程 |
| **架构** | CLI + Adapter Pattern + Skill System + Agent Personas |

spec-first 是一个**中文优先**的开源 AI 工作流 CLI 工具，实现了六阶段闭环开发方法论：候选发散（Ideate）→ 需求澄清（Clarify）→ 方案规划（Plan）→ 实施执行（Execute）→ 结构化评审（Review）→ 知识沉淀（Compound）。框架通过 Adapter 模式支持多种 AI agent 后端，通过 Skill 系统实现阶段逻辑，通过 Agent persona 系统实现角色化协作。

---

## 2. 源清单

| 文件/目录 | 角色 |
|-----------|------|
| `bin/spec-first.js` | CLI 入口，命令调度 |
| `bin/postinstall.js` | npm install 后的初始化脚本 |
| `src/cli/` | 核心 CLI 实现（commands, adapters, state） |
| `skills/` | 43+ workflow skill 定义（spec-bootstrap, spec-ideate 等）|
| `agents/` | 47+ agent persona 定义（review, research, design 等）|
| `templates/` | Runtime 命令模板 |
| `.claude-plugin/` | Claude Code 插件配置 |
| `docs/` | 完整文档站（中文为主）|
| `website/` | 项目官网源码 |
| `package.json` | npm 包定义与依赖声明 |
| `src/cli/adapters/` | AI agent 后端适配器 |
| `src/cli/state/` | 状态管理模块 |

---

## 3. 对象模型

### 核心实体

1. **Skill**：工作流阶段的执行单元，每个 skill 定义了一个阶段的输入/输出/上下文要求和 prompt 模板。43+ 个 skill 覆盖完整开发生命周期。

2. **Agent Persona**：角色化的 AI 代理配置，47+ 个 persona 分别适配不同任务（review, research, design, document-review 等）。每个 persona 定义了身份、专长和行为约束。

3. **Adapter**：AI agent 后端的抽象层，通过 Adapter Pattern 支持 Claude、GPT 等多种 backend。适配器负责将通用指令翻译为 backend 特定的 API 调用。

4. **State**：工作流执行状态，持久化于本地文件系统，跟踪当前阶段、已完成产出物和 context。

5. **Template**：运行时命令模板，在 skill 执行时注入上下文变量生成最终 prompt。

### 实体关系

```
CLI Command → Skill (阶段逻辑)
    ↓
Skill → Agent Persona (角色选择)
    ↓
Agent Persona → Adapter (后端调用)
    ↓
Adapter → AI Backend (Claude/GPT/etc.)
    ↓
AI Response → State (状态更新)
```

### Context Isolation

- 每个 skill 维护独立的 context scope
- Agent persona 之间通过 state 共享上下文，而非直接通信
- Adapter 层隔离了 AI backend 的差异

---

## 4. 流程与状态机

### 六阶段闭环流程

```
Phase 1: 候选发散 (Ideate)
    ↓ spec-ideate skill — 发散思考，生成候选方案
Phase 2: 需求澄清 (Clarify)
    ↓ spec-clarify skill — 结构化需求，消除歧义
Phase 3: 方案规划 (Plan)
    ↓ spec-plan skill — 技术方案设计与任务分解
Phase 4: 实施执行 (Execute)
    ↓ spec-execute skill — 按 task 逐步实现代码
Phase 5: 结构化评审 (Review)
    ↓ spec-review skill — 多角色评审代码与文档
Phase 6: 知识沉淀 (Compound)
    ↓ spec-compound skill — 提炼经验，更新知识库
    ↓
    → 回到 Phase 1（闭环迭代）
```

### Happy Path 状态转移

| From | To | 触发 | 产出物 |
|------|----|------|--------|
| Init | Ideate | `spec-bootstrap` | 项目初始化 |
| Ideate | Clarify | `spec-ideate` → 方案确定 | 候选方案列表 |
| Clarify | Plan | `spec-clarify` → 需求明确 | 需求文档 |
| Plan | Execute | `spec-plan` → 方案审批 | 技术设计 + 任务列表 |
| Execute | Review | 任务全部完成 | 实现代码 |
| Review | Compound | 评审通过 | 评审报告 |
| Compound | Ideate (next) | 知识沉淀完成 | 经验文档 |

### Failure Path

- **Clarify 阶段回退**：需求不清晰时循环 Clarify，不推进到 Plan
- **Review 驳回**：评审发现问题时回退到 Execute 或 Plan
- **Compound 反馈**：知识沉淀阶段发现系统性问题时影响下一轮 Ideate 方向

---

## 5. 执行保障审计

| 机制 | 级别 | 说明 |
|------|------|------|
| 阶段顺序执行 | **Soft** | CLI 引导顺序推进，但用户可跳过阶段 |
| Skill prompt 注入 | **Hard** | 每个 skill 的 prompt 模板在运行时自动注入，不可绕过 |
| Agent persona 约束 | **Soft** | Persona 定义行为边界，但 LLM 可偏离 |
| Adapter 抽象 | **Hard** | 所有 AI 调用必须经过 adapter 层，统一接口 |
| State 持久化 | **Hard** | 状态变更自动写入文件系统，确保断点恢复 |
| Postinstall 初始化 | **Hard** | npm install 后自动配置运行环境 |
| 文档完整性 | **Unenforced** | 各阶段产出物的质量由 LLM 自评，无硬性校验 |

---

## 6. Prompt 目录

### Prompt 1: spec-ideate（候选发散）

**角色**：创意发散专家

**核心指令摘要**：
> 基于用户描述的功能需求，从多个维度发散思考，生成 3-5 个候选方案。每个方案包含：核心思路、技术路线、优劣分析、风险评估。最终推荐最优方案并说明理由。

**上下文要求**：项目背景、现有架构、约束条件

### Prompt 2: spec-review（结构化评审）

**角色**：多角色评审团（可切换 code-reviewer, security-reviewer, architecture-reviewer 等 persona）

**核心指令摘要**：
> 按评审 checklist 逐项检查实现代码。分别从代码质量、安全性、架构一致性、性能、可维护性五个维度评分并给出具体改进建议。输出结构化评审报告。

---

## 7. 微观设计亮点

### 7.1 Adapter Pattern 解耦 AI Backend

通过 `src/cli/adapters/` 实现 adapter 抽象，使 skill 逻辑完全不感知底层 AI backend。新增 backend 只需实现 adapter 接口，不影响现有 skill 和 workflow。

### 7.2 Persona 系统实现角色化协作

47+ 个 agent persona 不仅是 prompt 前缀，而是完整的角色配置（身份、专长、行为约束、输出格式）。这使得同一 skill 可以通过切换 persona 获得不同专业视角的输出。

### 7.3 中文优先但不排斥英文

框架的文档、skill 描述、CLI 输出均以中文为主，但技术术语保留英文。这是针对中文开发者社区的精准定位，降低了使用门槛。

---

## 8. 宏观设计亮点

### 8.1 "闭环即进化"

六阶段闭环不是线性管道而是螺旋上升。Phase 6（知识沉淀）的输出直接影响下一轮 Phase 1（候选发散）的上下文，形成**组织级学习循环**。这超越了单次任务完成，追求团队知识的持续积累。

### 8.2 "Skill 是可组合的原子操作"

43+ 个 skill 既是阶段执行单元，也是可独立调用的原子操作。用户可以跳过完整流程，直接调用特定 skill 完成局部任务。这种设计平衡了流程的完整性和灵活性。

---

## 9. 失败模式与局限

| # | 失败模式 | 严重度 | 说明 |
|---|---------|--------|------|
| 1 | **阶段跳过无阻断** | Medium | CLI 建议但不强制顺序执行，用户可跳过 Ideate 直接进入 Execute |
| 2 | **Persona 漂移** | Medium | LLM 在长对话中可能逐渐偏离 persona 设定的行为约束 |
| 3 | **知识沉淀质量不可控** | High | Phase 6 的输出质量依赖 LLM 自评，无外部验证机制 |
| 4 | **Adapter 兼容性** | Medium | 不同 AI backend 的能力差异可能导致 skill 在某些 backend 上效果不佳 |
| 5 | **状态文件损坏** | Low | 文件系统 crash 可能导致 state 不一致，缺少事务性保证 |
| 6 | **1045 文件的维护负担** | High | 大量 skill 和 persona 文件增加了版本管理和一致性维护的成本 |

---

## 10. 迁移评估

### 可迁移候选

| 候选 | 价值 | 迁移难度 | 目标位置 |
|------|------|---------|---------|
| **六阶段闭环方法论** | 完整的开发生命周期模型 | 中 | `workflows/deep-plan` 扩展 |
| **Agent persona 系统** | 角色化 AI 协作模式 | 中 | `1st-cc-plugin/` 全局 persona registry |
| **知识沉淀阶段** | 组织级学习循环 | 高 | `integrations/catchup` 扩展 |
| **中文优先文档模式** | 中文开发者友好 | 低 | 所有插件的中文文档规范 |

### 建议采纳顺序

1. **六阶段方法论** → 参考丰富 `deep-plan` 的阶段覆盖
2. **Persona 系统** → 为 `quality/` 插件引入角色化评审
3. **知识沉淀机制** → 长期建设，扩展 `catchup` 的经验积累能力

---

## 11. 开放问题

1. **Skill 粒度**：43+ 个 skill 是否粒度过细？部分 skill 之间的边界是否模糊？
2. **Adapter 测试**：不同 AI backend 的 adapter 是否有自动化兼容性测试？
3. **闭环度量**：Phase 6 知识沉淀的效果如何度量？团队知识是否真正在迭代中增长？
4. **社区扩展**：网站和文档已就绪，但社区贡献的 skill/persona 如何质量把关？
5. **Token 预算**：47 个 persona + 43 个 skill 的 prompt 总量是否超出 context window 限制？

---

## 附录：Gemini Deepdive 补充信息

> 来源：`1st-cc-plugin/workflows/loaf/docs/gemini-roadmap-review/deepdive-spec-first.md`
> 补充内容：动态生成机制和语言策略注入的具体实现，主报告中未覆盖。

### A.1 动态 Command & Skill 生成机制

`spec-first` 的核心不是静态文件拷贝，而是**动态转换管线**：

1. **Asset 同步**：CLI `init.js` 调用 `syncBundledAssets()`，按 manifest 逐一处理 bundled assets。
2. **Adapter 转换**（`adapters/base.js` 接口）：
   - **Claude adapter** (`claude.js`)：Claude Code 要求扁平 agent 命名空间，adapter 去除 `spec-first:category:name` 前缀，重写为裸 `name` 标识符。
   - **Codex adapter** (`codex.js`)：skills 放置到 `.agents/skills`，agents 放置到 `.codex/agents`，动态重写模板中的路径引用，并通过 `rewriteSkillName` 设置 skill 名称。
3. **State 管理**（`state.js`）：在 `.claude/spec-first/` 或 `.codex/spec-first/` 下维护 `state.json`，追踪生成的 asset 路径，使 `spec-first clean` 能安全移除 managed 文件而不影响用户文件。

### A.2 语言策略注入（`lang-policy.js`）

Language Policy 通过**幂等 marker 注入**实现，无需覆盖整个 system prompt：

- **Magic markers**：`<!-- spec-first:lang:start -->` 和 `<!-- spec-first:lang:end -->`
- **`applyManagedBlock(existing, block)`**：
  - 若两个 marker 都存在 → 原地替换（in-place substring replacement）
  - 若 marker 缺失或损坏 → 安全追加到文件末尾
- **策略内容**：
  - 强制所有自然语言输出（状态更新、文档、review 评论）使用指定语言（如 `zh`）
  - 禁止翻译技术标识符（变量名、函数名、API 名、命令）
  - 附加 Changelog Governance Iron Law

### A.3 Cross-Harness Adapter 模式的迁移价值

`spec-first` 的 `HarnessAdapter` 模式（`ClaudeAdapter` / `CodexAdapter`）证明了**"一次编写、多平台部署"**的可行路径。关键设计决策：
- 每个 adapter 实现 `transformSkillContent` 和 `transformAgentContent` 接口
- 转换在文件写入前执行，确保目标平台看到的始终是原生格式
- 这为 `1st-cc-plugin` 未来支持多平台提供了直接可参考的架构
