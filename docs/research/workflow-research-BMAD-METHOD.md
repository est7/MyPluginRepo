# Workflow Research Report: BMAD-METHOD

> 生成时间：2025-07  
> 仓库：`vendor/BMAD-METHOD/`  
> 版本：v6.3.0 | 许可证：MIT | 组织：bmad-code-org

---

## 1. 框架概况

| 维度 | 值 |
|------|-----|
| **类型** | 企业级 AI-driven Agile 开发框架 |
| **文件数** | ~671 |
| **语言** | JavaScript/YAML（构建工具）+ Markdown（skill/workflow/agent 定义）|
| **入口** | `npm install -g bmad-method` → `bmad` CLI → 交互式 agent 选择 → workflow 执行 |
| **平台** | Node.js ≥20、Python ≥3.10（uv）|
| **设计哲学** | "Human Amplification, Not Replacement" — AI 作为协作专家而非替代者 |

BMAD（Build More Architect Dreams）是目前调研的 vendor 中**规模最大、结构最复杂**的框架。它实现了从 brainstorming 到 deployment 的完整 SDLC，通过 12+ 专业化 agent persona 和 34+ workflow skill 覆盖全生命周期。

---

## 2. 源清单

| 文件 / 目录 | 作用 |
|-------------|------|
| `package.json` | npm 包定义，`bmad` CLI 入口 |
| `src/bmm-skills/1-analysis/` | Phase 1 skill：brainstorming、market research、product brief、PRFAQ |
| `src/bmm-skills/2-plan-workflows/` | Phase 2 skill：PRD 创建/验证/编辑、UX 设计 |
| `src/bmm-skills/3-solutioning/` | Phase 3 skill：architecture、epics/stories、readiness check |
| `src/bmm-skills/4-implementation/` | Phase 4 skill：dev story、code review、sprint planning、retrospective |
| `src/core-skills/` | 通用 skill：brainstorming（62 种技法）、help 等 |
| `tools/installer/bmad-cli.js` | CLI 安装器 |
| `tools/` | 构建脚本、validator |
| `test/` | 测试套件（含 adversarial review tests） |
| `.husky/pre-commit` | Git hook：lint-staged + npm test + doc validation |
| `docs/` | 多语言文档（en, zh-cn, vi-vn, fr, cs） |
| `website/` | Astro 文档站点 |
| `eslint.config.mjs` | 代码质量（flat config, ESLint 9+） |
| `prettier.config.mjs` | 格式化（140 字符宽、单引号、分号） |
| `.coderabbit.yaml` | CodeRabbit AI review 配置 |

---

## 3. 对象模型

### 核心实体关系

```
Module (bmm)
  │
  ├── Agent Persona ──→ Menu Triggers ──→ Skill
  │   (Mary/John/       (BP,MR,CP...)     │
  │    Winston/Amelia/                     ├── SKILL.md (frontmatter + body)
  │    Sally/Paige)                        ├── workflow.md (orchestration)
  │                                        ├── bmad-manifest.json (metadata)
  │                                        ├── steps/ (step-01.md ...)
  │                                        ├── prompts/ (subagent instructions)
  │                                        ├── agents/ (persona definitions)
  │                                        └── templates/ (output templates)
  │
  └── Configuration
      ├── module.yaml (module registry)
      └── config.yaml (project-level settings)
```

### 六大 Agent Persona

| Agent | 代号 | 角色 |
|-------|------|------|
| **Analyst (Mary)** | `bmad-analyst` | 研究与分析 |
| **Product Manager (John)** | `bmad-pm` | 需求与计划 |
| **Architect (Winston)** | `bmad-architect` | 技术设计 |
| **Developer (Amelia)** | `bmad-agent-dev` | 开发与测试 |
| **UX Designer (Sally)** | `bmad-ux-designer` | 用户体验 |
| **Technical Writer (Paige)** | `bmad-tech-writer` | 文档 |

### Context 隔离

每个 skill 采用 **micro-file architecture**：step 文件按需加载（just-in-time），禁止同时加载多个 step 文件。Workflow 状态通过 YAML frontmatter 的 `stepsCompleted: [1, 2, 3]` 持久化。

---

## 4. 流程与状态机

### Phase 流转

```
Phase 1: Analysis (Optional)
    Brainstorming → Research → Product Brief → PRFAQ
        │
        ▼
Phase 2: Planning
    Create PRD → Validate PRD → Edit PRD → UX Design
        │
        ▼
Phase 3: Solutioning
    Architecture → Epics & Stories → Implementation Readiness
        │
        ▼
Phase 4: Implementation
    Sprint Planning → Create Story → Dev Story → Code Review → Retrospective
```

### Story 状态机

```
Epic:   backlog → in-progress → done
Story:  backlog → ready-for-dev → in-progress → review → done
Retro:  optional ↔ done
```

### Dev Story 的 TDD 子流程

```
Find next ready-for-dev story
    → Load context
    → Mark in-progress
    → RED (write failing tests)
    → GREEN (implement minimal code)
    → REFACTOR (improve, keep tests green)
    → Author comprehensive tests
    → Run validations
    → Mark review
    → Code Review (ideally different LLM)
    → Mark done
```

### 失败路径

- Story 实现中遇到 blocker → HALT，等待人工干预
- Code review 发现问题 → `[AI-Review]` 前缀标记 → 回到 Dev Agent Record → 修复后重新进入 review
- Sprint 偏离 → `Correct Course` workflow 介入

### Quick Flow 旁路

`bmad-quick-dev` 跳过 Phase 1-3，直接产出 spec + working code，适用于小型、明确的任务。

---

## 5. 执行保障审计

| 机制 | 级别 | 说明 |
|------|------|------|
| Micro-file sequential loading | **Hard** | `🛑 NEVER load multiple step files simultaneously` — workflow.md 中强制要求 |
| Step 顺序执行 | **Hard** | `🚫 NEVER skip steps or optimize sequence` |
| Menu halt 等待用户 | **Hard** | `⏸️ ALWAYS halt at menus and wait for user input` |
| SKILL.md frontmatter 校验 | **Hard** | `tool/skill-validator.md` 定义 SKILL-01~07 规则 |
| `.husky/pre-commit` | **Hard** | lint-staged + npm test + doc link validation |
| Append-only document building | **Soft** | workflow.md 中声明"never overwrite, only append"，但无技术强制 |
| Phase gate（human review） | **Soft** | 各 phase 间建议人工审核，但可被 `--yolo` 跳过 |
| TDD cycle（RED→GREEN→REFACTOR） | **Soft** | Dev story 中要求但无强制校验 |
| Definition of Done checklist | **Soft** | 10 项检查清单，依赖 agent 自律 |
| 62 种 brainstorming 技法选择 | **Unenforced** | 从 CSV 加载，由 AI 自主选择 |

**总评**：BMAD 在**结构层面**（文件加载顺序、step 隔离）实现了 Hard enforcement，但在**内容层面**（TDD 实际执行、DoD 检查）仍依赖 AI 自律。`.husky` hook 提供了真正的 CI 级保障。

---

## 6. Prompt 目录

### Prompt 1: Product Brief — Autonomous Mode 子代理扇出

```markdown
# Activation Modes
1. Autonomous Mode (--autonomous): Ingest inputs, fan out subagents, produce brief without interaction
   - artifact-analyzer: Scans project docs, extracts key insights
   - web-researcher: Performs market research
   - skeptic-reviewer: Challenges assumptions
   - opportunity-reviewer: Identifies growth opportunities

# Design Rationale
Always understand intent BEFORE scanning artifacts
```

**设计意图**：通过 4 个专职 subagent 并行执行，实现"理解意图 → 收集证据 → 挑战假设 → 发现机会"的完整分析闭环。

### Prompt 2: Brainstorming — Anti-Bias Protocol

```markdown
# Critical Mindset
Keep user in generative exploration mode; resist organizing

# Anti-Bias Protocol
Consciously shift creative domain every 10 ideas to avoid semantic clustering

# Techniques (62 total)
Categories: Collaborative, Creative, Deep, Introspective, Structured,
            Theatrical, Wild, Biomimetic, Quantum, Cultural
```

**设计意图**：通过强制"每 10 个想法切换创意领域"来对抗 LLM 的语义聚类倾向，这是对 LLM 生成偏差的深刻理解。

---

## 7. 微观设计亮点

### 7.1 Micro-file Architecture 的 Token 经济学

每个 workflow 将步骤拆分为独立的 step 文件（`step-01.md`, `step-02.md`...），运行时按需加载单个文件。这不仅是代码组织手段，更是**显式的 token budget 管理策略**——确保任一时刻 context window 中只有当前 step 的内容，避免整个 workflow 一次性占满 window。

### 7.2 bmad-manifest.json 的依赖图谱

每个 skill 的 manifest 声明 `after`/`before` 关系（如 product brief `after: ["brainstorming"]`, `before: ["create-prd"]`），构成了一个显式的 skill 依赖 DAG。这使得框架可以**在运行时验证 workflow 顺序的合理性**。

### 7.3 62 种 Brainstorming 技法的 CSV 数据驱动

brainstorming skill 将 62 种创意技法存储在 `brain-methods.csv` 中，运行时从数据文件加载而非硬编码在 prompt 中。这种**数据与指令分离**的模式使得技法库可以独立扩展，不影响 skill 的 token 预算。

---

## 8. 宏观设计亮点

### 8.1 "Scale-Domain-Adaptive" 规划

BMAD 不假设所有项目都需要完整的 4-phase 流程。通过 Quick Flow（`bmad-quick-dev`）和 autonomous/yolo/guided 三种模式，框架**根据任务规模自适应调整仪式感**。小任务跳过 planning，大项目走完整 phase gate。这体现了"仪式感应与复杂度成正比"的成熟工程直觉。

### 8.2 Agent Persona 作为组织知识载体

六个 agent persona 不仅是角色扮演，更是**组织最佳实践的编码容器**。Mary（Analyst）内化了市场研究方法论，Amelia（Developer）内化了 TDD 实践和 DoD 标准。这种设计使得"团队规范"从文档变成了**可执行的 agent 行为**。

---

## 9. 失败模式与局限

| # | 失败模式 | 影响 | 可能性 |
|---|----------|------|--------|
| 1 | **Workflow 复杂度过高** — 34+ skill × 6 agent × 4 phase，新用户面临陡峭的学习曲线 | 采纳率低 | 高 |
| 2 | **Step 文件串行加载延迟** — 严格的"一次一个 step"策略在长 workflow 中导致大量 round-trip | 用户等待时间长 | 中 |
| 3 | **Agent persona 固化** — 6 个预定义 agent 的行为模式难以定制，不适配所有团队文化 | 企业定制成本高 | 中 |
| 4 | **Status YAML 与实际状态不同步** — sprint-status.yaml 的状态依赖 AI 主动更新，遗漏更新导致 sprint 视图失真 | 项目管理混乱 | 高 |
| 5 | **多语言文档维护负担** — 5 种语言的文档需要同步更新，容易出现版本漂移 | 非英语用户获得过时信息 | 中 |
| 6 | **`--yolo` 模式风险** — 跳过所有 phase gate 的"快速通道"在复杂项目中可能产生低质量输出 | 质量下降 | 中 |

---

## 10. 迁移评估

### 可移植候选

| 机制 | 目标位置（1st-cc-plugin） | 优先级 | 改造量 |
|------|--------------------------|--------|--------|
| Micro-file step architecture | 全局 skill 设计规范 | P1 | 提取 pattern，写入 skill-dev 指南 |
| Code review 的 parallel review layers | `quality/refactor` 或 `quality/codex-review` | P1 | 提取 Blind Hunter / Edge Case Hunter 模式 |
| Sprint status 状态机 | `workflows/issue-driven-dev` | P2 | 移植 Epic/Story 状态流转逻辑 |
| Product brief 的 subagent 扇出 | `workflows/deep-plan` | P2 | 移植 4-subagent 分析模式 |
| Anti-Bias brainstorming protocol | `quality/clarify` | P3 | 提取"每 10 想法切换领域"机制 |

### 建议采纳顺序

1. **Micro-file pattern** → 写入 `meta/skill-dev` 作为 skill 设计最佳实践
2. **Code review layers** → 增强 `quality/codex-review` 的 review 深度
3. **Sprint 状态机** → 丰富 `workflows/issue-driven-dev` 的状态管理

---

## 11. 开放问题

1. **Party Mode**：README 提到"Party Mode for multi-agent sessions"，但未找到具体实现细节——这是一个值得深入调研的多 agent 并发执行机制。
2. **bmad-manifest.json 的 `after`/`before` 验证**：依赖关系声明在 manifest 中，但不清楚运行时是否真正校验这些依赖是否满足。
3. **Adversarial review tests**：`test/` 目录中存在 adversarial review 测试，其测试策略（如何模拟对抗性输入）值得研究。
4. **Config YAML 的环境差异**：`config.yaml` 中的 `planning_artifacts` / `implementation_artifacts` 路径如何在不同项目结构间适配？

---

## 附录：Gemini Deepdive 补充信息

> 来源：`1st-cc-plugin/workflows/loaf/docs/gemini-roadmap-review/deepdive-bmad-method.md`
> 补充内容：DQR 验证器实现、HALT token 机制、模块发现系统的具体代码级细节。

### A.1 Deterministic Quality Review (DQR) 验证器

BMAD 的质量保证不仅是 checklist，还有可执行的验证脚本：

1. **`tools/validate-skills.js`**：
   - 遍历 `src/skills/` 目录中的所有 `.md` 文件
   - 正则检查 kebab-case 命名（`/^[a-z0-9]+(-[a-z0-9]+)*\.md$/`）
   - 验证 frontmatter 完整性（必须包含 `title`, `description`, `category`）
   - 检查内容结构（必须包含 `## Purpose`、`## Instructions` 等 section）

2. **`tools/validate-file-refs.js`**：
   - 扫描所有 Markdown 文件中的文件引用
   - 检测断裂引用（引用文件不存在）
   - **伪路径映射**：`{_bmad}/core/` → `src/core-skills/`，允许 skill 使用 portable 路径
   - **绝对路径泄漏检测**：报告任何包含 `/Users/` 或 `C:\` 的硬编码路径

3. **聚合管线**：`npm run quality` = `prettier --check` → `eslint` → `markdownlint` → `validate:refs` → `validate:skills`

### A.2 HALT Token 语义控制

HALT 不是简单的停止信号，而是**语义控制机制**：
- Agent 在 skill 执行过程中输出 `HALT` token 表示"我需要用户决策才能继续"
- HALT 后 agent 暂停当前 skill，yield 控制权回用户
- 区别于 error（不可恢复）和 completion（已完成），HALT 是第三种退出语义

### A.3 确定性上下文发现

- **`module.yaml`**：每个模块的元数据清单，包含依赖声明、角色标签、质量要求
- **`module-help.csv`**：快速查找表（module-name → one-line-description → primary-skill-path），使 agent 无需遍历文件系统即可定位能力

### A.4 CLI 安装器

`tools/installer/bmad-cli.js` 实现符号链接式安装：
- 在 `~/.local/bin/bmad` 创建 symlink 指向实际脚本
- 注册 `bmad init`（项目初始化）和 `bmad doctor`（环境检查）子命令
- 支持 `--global` 和 `--local` 安装模式
