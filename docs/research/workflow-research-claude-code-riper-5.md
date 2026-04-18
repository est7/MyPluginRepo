# Workflow Research Report: claude-code-riper-5

> 生成时间：2025-07  
> 仓库：`vendor/claude-code-riper-5/`  
> 版本：v1.0.0 | 许可证：MIT | 作者：Tony Narlock

---

## 1. 框架概况

| 维度 | 值 |
|------|-----|
| **类型** | RIPER workflow 框架 — 5 阶段结构化开发协议 |
| **文件数** | ~22 |
| **语言** | Markdown（commands/agents）+ JSON（config/settings） |
| **入口** | `.claude/` 目录复制到项目 → `/riper:strict` 启用协议 → `/riper:research` 开始 |
| **平台** | Claude Code |
| **设计哲学** | Mode-restricted phases — 每个阶段严格限制 AI 可执行的操作类型 |

RIPER（Research → Innovate → Plan → Execute → Review）是所有 vendor 中**最精简**的 workflow 框架。仅 22 个文件，通过 5 个模式和 3 个 consolidated agent 实现了从调研到验证的完整开发周期。其核心特征是**模式受限执行**——每个阶段的 AI 只能执行该模式允许的操作。

---

## 2. 源清单

| 文件 / 目录 | 作用 |
|-------------|------|
| `README.md` | 项目文档：RIPER 概述、Quick Start、命令参考、架构 |
| `.claude/riper-config.json` | 核心配置：agent 定义、command 映射、memory-bank 设置 |
| `.claude/settings.json` | Claude Code project settings |
| `.claude/project-info.md` | 项目信息模板（技术栈、目录结构、开发指南） |
| `.claude/commands/riper/strict.md` | `/riper:strict` — 启用严格协议 |
| `.claude/commands/riper/research.md` | `/riper:research` — 进入 RESEARCH 模式 |
| `.claude/commands/riper/innovate.md` | `/riper:innovate` — 进入 INNOVATE 模式 |
| `.claude/commands/riper/plan.md` | `/riper:plan` — 进入 PLAN 模式 |
| `.claude/commands/riper/execute.md` | `/riper:execute` — 进入 EXECUTE 模式 |
| `.claude/commands/riper/review.md` | `/riper:review` — 进入 REVIEW 模式 |
| `.claude/commands/riper/workflow.md` | `/riper:workflow` — 执行完整 RIPER 流程 |
| `.claude/commands/memory/save.md` | `/memory:save` — 保存 context 到 memory bank |
| `.claude/commands/memory/recall.md` | `/memory:recall` — 从 memory bank 检索 |
| `.claude/commands/memory/list.md` | `/memory:list` — 列出所有 memory |
| `.claude/commands/rebase.md` | `/rebase` — 高级 git rebase 命令 |
| `.claude/agents/research-innovate.md` | Research + Innovate 双模式 agent |
| `.claude/agents/plan-execute.md` | Plan + Execute 双模式 agent |
| `.claude/agents/review.md` | Review 专职 agent |
| `.claude/memory-bank/README.md` | Memory bank 结构文档 |

---

## 3. 对象模型

### 核心实体关系

```
RIPER Protocol
    │
    ├── 3 Consolidated Agents
    │   ├── research-innovate (sonnet) ─→ RESEARCH | INNOVATE sub-modes
    │   ├── plan-execute (sonnet) ─────→ PLAN | EXECUTE sub-modes
    │   └── review (sonnet) ───────────→ REVIEW mode
    │
    ├── 11 Slash Commands
    │   ├── riper/ namespace (7): strict, research, innovate, plan, execute, review, workflow
    │   ├── memory/ namespace (3): save, recall, list
    │   └── rebase (1)
    │
    └── Memory Bank (.claude/memory-bank/)
        └── {branch}/
            ├── plans/      ({branch}-{date}-{feature}.md)
            ├── reviews/    ({branch}-{date}-{scope}.md)
            └── sessions/   ({date}-{topic}.md)
```

### 5-到-3 的 Agent 压缩

5 个 RIPER 模式被**压缩**为 3 个 agent：
- **research-innovate** 合并了两个"只读"阶段
- **plan-execute** 合并了两个"生产"阶段
- **review** 独立——验证必须与执行分离

这种 5:3 映射体现了对**能力相似度**的精确判断。

### Context 隔离

- **Agent 级隔离**：每个 agent 在独立 context 中运行
- **Branch 级隔离**：Memory bank 按 git branch 分区
- **Mode 级限制**：每个 mode 有显式的 allowed/forbidden actions 列表

---

## 4. 流程与状态机

### RIPER 状态机

```
[NO MODE] ──→ /riper:strict
                 │
                 ▼
         ┌── RESEARCH (read-only)
         │      Only: read, analyze, search, document, ask, gather
         │      Forbidden: suggest solutions, design decisions, proposals
         │
         ├── INNOVATE (brainstorming)
         │      Only: brainstorm, explore, analyze trade-offs, question
         │      Forbidden: concrete plans, code/pseudocode, final decisions
         │
         ├── PLAN (specifications)
         │      Only: detailed specs, implementation steps, design docs
         │      Write ONLY to: .claude/memory-bank/*/plans/
         │      Forbidden: actual code, execution commands, modify existing code
         │
         ├── EXECUTE (implementation)
         │      Requires: APPROVED PLAN
         │      Only: implement EXACTLY from plan, write/modify files, run tests
         │      Forbidden: deviate from plan, add improvements, new design decisions
         │
         └── REVIEW (validation)
                Only: verify plan compliance, run tests, check quality
                Forbidden: fix issues, adjust, implement
                Output: review report to .claude/memory-bank/reviews/
```

### Mode Capabilities Matrix

| 能力 | Research | Innovate | Plan | Execute | Review |
|------|----------|----------|------|---------|--------|
| Read | ✅ | ✅ | ✅ | ✅ | ✅ |
| Write | ❌ | ❌ | Plans only | ✅ | Reports only |
| Execute | ❌ | ❌ | ❌ | ✅ | Tests only |
| Plan | ❌ | ❌ | ✅ | ❌ | ❌ |
| Validate | ❌ | ❌ | ❌ | ❌ | ✅ |

### `/riper:workflow` 完整流程

```
1. RESEARCH → research-innovate agent (RESEARCH sub-mode)
2. INNOVATE → research-innovate agent (INNOVATE sub-mode)
3. PLAN → plan-execute agent (PLAN sub-mode)
4. ⚠️ APPROVAL GATE → Pause for explicit user approval
5. EXECUTE → plan-execute agent (EXECUTE sub-mode)
6. REVIEW → review agent
```

### 失败路径

- **Mode violation** → Agent 阻止操作并输出警告：`[MODE VIOLATION]`
- **Execute 无 approved plan** → 阻止执行，要求先完成 PLAN 阶段
- **Review 发现偏差** → 按严重级分类（🔴 CRITICAL / 🟡 WARNING / 🟢 INFO），建议模式切换但**不自行修复**

### Memory Bank 策略

```
Save: /memory:save <context>
    → .claude/memory-bank/{branch}/{date}-session.md
    → Includes: date, time, branch, latest commit, working directory status

Recall: /memory:recall <topic>
    → Search .claude/memory-bank/{branch}/
    → Shows recent git history since last memory

List: /memory:list
    → All memories across all branches

CRITICAL PATH POLICY:
    ✅ {ROOT}/.claude/memory-bank/main/session.md
    ❌ packages/react/.claude/memory-bank/  (NEVER package-level)
```

---

## 5. 执行保障审计

| 机制 | 级别 | 说明 |
|------|------|------|
| Mode capabilities matrix | **Soft** | 每个 mode 有 allowed/forbidden 列表，但 AI 自律遵守 |
| Execute requires approved plan | **Soft** | EXECUTE mode 检查 plan 存在性，但"approved"状态无技术标记 |
| Review 禁止修改 | **Soft** | "Forbidden to fix, adjust, implement" — prompt 约束 |
| Agent tool restrictions | **Soft** | research-innovate 不含 Write/Edit tool，但 agent 声明非运行时强制 |
| Violation blocking | **Soft** | Mode violation 时输出 `[MODE VIOLATION]` 警告，但无技术阻断 |
| Repository root path policy | **Soft** | Memory bank 必须在 repo root，通过 `git rev-parse --show-toplevel` 定位 |
| Branch-aware storage | **Hard** | Memory bank 按 branch 物理隔离（文件系统目录） |
| `.gitignore` 保护 | **Hard** | `.claude/memory-bank/` 和 `.claude/settings.local.json` 被 ignore |

**总评**：RIPER 的保障主要依赖**prompt 级约束**（Soft enforcement）。唯一的 Hard enforcement 是文件系统级别的 branch 隔离和 gitignore 保护。这与框架的轻量级定位一致——22 个文件实现的框架不可能有复杂的运行时校验。模式限制的有效性**完全取决于 AI model 对 prompt 的遵从度**。

---

## 6. Prompt 目录

### Prompt 1: `/riper:strict` — Mode Protocol Enforcement

```markdown
# Status: [NO MODE] - Awaiting mode assignment

# Protocol Rules
- Mode declaration required before any action
- Mode transitions: explicit command only
- Mode restrictions: strictly enforced
- Violation handling: block + warning

# Mode Capabilities Matrix
| Capability | Research | Innovate | Plan | Execute | Review |
|-----------|----------|----------|------|---------|--------|
| Read      | ✅       | ✅       | ✅   | ✅      | ✅     |
| Write     | ❌       | ❌       | Plans| ✅      | Reports|
| Execute   | ❌       | ❌       | ❌   | ✅      | Tests  |
| Plan      | ❌       | ❌       | ✅   | ❌      | ❌     |
| Validate  | ❌       | ❌       | ❌   | ❌      | ✅     |
```

**设计意图**：通过能力矩阵的表格化呈现，使 AI 能够快速查阅当前模式下的权限边界。`[NO MODE]` 初始状态强制要求显式模式声明，避免"无模式下的自由行动"。

### Prompt 2: Review Agent — "Ruthless Validation"

```markdown
# Operational Rules
1. VALIDATE RUTHLESSLY: Zero tolerance comparison
2. NO MODIFICATIONS: Forbidden to fix, adjust, implement
3. Output format: [MODE: REVIEW] at start of responses

# Deviation Detection
🔴 CRITICAL: Functionality differs from plan
🟡 WARNING: Style differs from plan
🟢 INFO: Minor differences

# Forbidden Actions
Cannot fix issues found; must document and recommend mode switches
```

**设计意图**：Review agent 的核心约束是**只验证不修复**。这种"无手"设计迫使问题回流到 EXECUTE mode，保证了 Review 的独立性和客观性。

---

## 7. 微观设计亮点

### 7.1 5-to-3 Agent Consolidation

将 5 个逻辑模式映射到 3 个物理 agent（research-innovate、plan-execute、review），通过 sub-mode 区分行为。这种**模式压缩**减少了 agent 管理开销，同时保留了模式隔离的语义清晰度。关键洞察：Research 和 Innovate 共享"只读"属性，Plan 和 Execute 共享"生产"属性，Review 必须独立。

### 7.2 Branch-Aware Memory Bank

Memory bank 按 git branch 组织存储，每个 branch 有独立的 plans/、reviews/、sessions/ 目录。文件命名遵循 `{branch}-{date}-{feature}.md` 格式。这使得**并行 feature 开发**的 context 互不污染，并且 branch merge 后可以对比不同 branch 的 plan 演化。

### 7.3 Repository Root Path Policy

Memory bank 强制存储在 **repo root** 的 `.claude/memory-bank/`，明确禁止在 monorepo 的子 package 中创建 memory bank（"NEVER create package-level memory banks"）。这个看似简单的路径约束，有效防止了 monorepo 环境中 memory 分裂的问题。

---

## 8. 宏观设计亮点

### 8.1 "Mode as Discipline" 哲学

RIPER 的核心假设是：**AI 的最大风险不是能力不足，而是行动不受约束**。通过将开发过程分解为 5 个具有严格权限边界的模式，框架将"什么时候该做什么"从 AI 的自由判断变成了**协议级约束**。Research mode 中禁止提出方案、Execute mode 中禁止偏离计划、Review mode 中禁止修复——每个禁止都是对 AI "过度热心"倾向的对抗。

### 8.2 极简主义的工程表达

22 个文件实现了完整的 5-phase workflow，包含 3 个 agent、11 个 slash command 和一个 persistent memory 系统。这种**极端的文件经济性**证明了 Claude Code 的 `.claude/` 目录约定已经足够表达复杂的 workflow 语义——无需 npm 包、无需构建工具、无需运行时依赖。

---

## 9. 失败模式与局限

| # | 失败模式 | 影响 | 可能性 |
|---|----------|------|--------|
| 1 | **Mode 遵从依赖 AI 自律** — 所有 mode restriction 都是 prompt 级约束，AI model 可能在长对话后"遗忘"当前模式 | 模式泄漏（如 Research 中开始提方案） | 高 |
| 2 | **"Approved Plan" 无技术标记** — Execute mode 要求 approved plan，但"approved"状态只存在于对话历史中，无文件级标记 | AI 可能在未获批准的 plan 上执行 | 中 |
| 3 | **Memory bank 膨胀** — 每次 save 创建新文件（`{date}-session.md`），无自动清理或压缩机制 | 长期使用后 memory bank 文件过多 | 中 |
| 4 | **无 CI 集成** — 框架完全运行在 Claude Code 对话中，无法与 CI/CD pipeline 集成 | 无法自动化验证 | 确定性 |
| 5 | **单人工作流假设** — Memory bank 无并发控制，多人在同一 branch 的 memory bank 上操作可能冲突 | 团队使用时 memory 混乱 | 中 |
| 6 | **Review 偏差检测深度** — Review agent 依赖 AI 能力判断 plan 合规性，复杂逻辑偏差可能漏检 | 质量保障不足 | 中 |

---

## 10. 迁移评估

### 可移植候选

| 机制 | 目标位置（1st-cc-plugin） | 优先级 | 改造量 |
|------|--------------------------|--------|--------|
| Mode capabilities matrix | 全局 skill 设计规范 | P1 | 将"模式受限执行"作为 skill 设计 pattern |
| Branch-aware memory bank | `integrations/catchup` 或新建 `integrations/memory` | P2 | 移植 branch 隔离 + 命名约定 |
| 5-to-3 agent consolidation | 全局 agent 设计指南 | P2 | 提取"能力相似模式合并"原则 |
| `/rebase` command | `vcs/git` | P3 | 移植冲突预测 + 自动解决逻辑 |
| Repository root path policy | 全局约定 | P3 | monorepo memory bank 放置规范 |

### 建议采纳顺序

1. **Mode capabilities matrix** → 作为 skill 权限设计的参考模板
2. **Branch-aware memory** → 增强 catchup skill 的上下文管理
3. **Agent consolidation pattern** → 减少 agent 数量同时保持语义清晰

---

## 11. 开放问题

1. **Strict mode 的持久性**：`/riper:strict` 激活后，模式状态是否在 conversation 中断后保持？如果重新开始对话，是否需要重新激活？
2. **Plan approval 机制**：`/riper:workflow` 的 step 4 是"APPROVAL GATE — Pause for explicit user approval"，但 approval 如何记录？用户说"ok"是否算 approval？
3. **Memory bank 与 git 的交互**：`.claude/memory-bank/` 被 gitignore，这意味着 memory bank 不随 repo 传播——这是 intentional（本地只读）还是 limitation（无法团队共享）？
4. **`/rebase` command 的独立性**：这个 command 与 RIPER workflow 无关，似乎是一个"bonus" utility——它的存在是否暗示框架会扩展到更多 git 操作？
5. **riper-config.json 的消费者**：配置文件定义了 agent 和 command 映射，但 Claude Code 是否原生读取此文件？还是仅作为文档？
