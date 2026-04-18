# Workflow Research Report: planning-with-files

> **研究日期**: 2025-07  
> **仓库**: OthmanAdi/planning-with-files  
> **文件数**: ~511  
> **版本**: v2.34.1  
> **许可证**: 未明确声明  

---

## 1. 框架概况

planning-with-files 是一个受 Meta/Manus 启发的 **file-based planning skill**，核心理念是将 AI agent 的工作记忆从 volatile context window 迁移到持久化的 Markdown 文件。通过 3 个规范化文件（`task_plan.md`, `findings.md`, `progress.md`）和 4 个 lifecycle hook 实现 attention manipulation，在 SWE-bench 风格的评估中达到 **96.7% benchmark pass rate**（baseline 6.7%），并通过 **3/3 blind A/B comparison** 验证。v2.21.0 经过安全审计修复了 indirect prompt injection 放大漏洞。

| 属性 | 值 |
|------|------|
| **类型** | Claude Code Skill (file-based planning) |
| **语言** | Markdown (skill 定义) + Bash (hooks) + Python (session recovery) |
| **入口** | 自动加载 SKILL.md + hooks.json |
| **核心文件** | `task_plan.md`, `findings.md`, `progress.md` |
| **Hook 数量** | 4 (UserPromptSubmit, PreToolUse, PostToolUse, Stop) |
| **平台支持** | 16+ IDE (Claude Code, Cursor, Copilot, Codex, Gemini CLI 等) |
| **语言变体** | 6 种 (English, Arabic, German, Spanish, 中文简体/繁体) |

---

## 2. 源清单

| 文件 | 用途 | 重要度 |
|------|------|--------|
| `SKILL.md` | 核心 skill 定义 (6 principles + 5 rules + 3-strike protocol) | ★★★ |
| `hooks.json` | 4 个 lifecycle hook 配置 | ★★★ |
| `templates/task_plan.md` | 规划文件模板 | ★★★ |
| `templates/findings.md` | 发现记录模板 | ★★★ |
| `templates/progress.md` | 进度日志模板 | ★★★ |
| `scripts/check-complete.sh` | Stop hook: 检查 Phase 完成度 | ★★☆ |
| `scripts/init-session.sh` | Session 初始化脚本 | ★★☆ |
| `docs/evals.md` | 完整 benchmark 方法论与结果 | ★★★ |
| `docs/article.md` | 安全审计分析 (v2.21.0) | ★★★ |
| `session-catchup.py` | Session 恢复脚本 (读取 IDE session store) | ★★☆ |

---

## 3. 对象模型

### 核心实体

```
TaskPlan (task_plan.md)
  ├── goal: string            # 1 句话北极星目标
  ├── current_phase: string   # 当前所处阶段
  ├── phases: Phase[]         # 3-7 个阶段
  ├── key_questions: string[]
  ├── decisions: Decision[]   # decision | rationale 表
  └── errors: Error[]         # error | attempt | resolution 表

Phase
  ├── name: string
  ├── tasks: Task[] (checkbox)
  ├── status: string          # "**Status:** complete" 格式
  └── order: number

Findings (findings.md)
  ├── requirements: string[]       # 来自用户的需求
  ├── research_findings: string[]  # 2-Action Rule 触发更新
  ├── technical_decisions: Decision[]
  ├── issues_resolutions: Issue[]
  ├── resources: URL[]
  └── visual_findings: string[]    # 多模态发现 (立即文本化)

Progress (progress.md)
  ├── session_date: string
  ├── phase_logs: PhaseLog[]
  ├── test_results: TestResult[]   # Test | Input | Expected | Actual | Status
  ├── error_log: ErrorLog[]        # Timestamp | Error | Attempt | Resolution
  └── reboot_check: 5-Question     # 在哪?去哪?目标?学到?完成?
```

### Lifecycle Hooks

```
UserPromptSubmit
  → 注入当前 plan state + 近期 progress

PreToolUse (before Write/Edit/Bash)
  → head -30 task_plan.md (attention manipulation)

PostToolUse (after Write/Edit)
  → 提醒更新 progress.md

Stop
  → 检查 Phase 完成度
  → 未完成 → 返回 followup_message 自动继续
```

### 实体关系

- **TaskPlan** 是核心控制文件，所有 hook 都读取它
- **Findings** 由 2-Action Rule 驱动更新（每 2 次 view/search 操作后强制更新）
- **Progress** 是 append-only 的 session log
- 三个文件共同构成 agent 的 "persistent working memory"

---

## 4. 流程与状态机

### Happy Path

```
[用户] 描述任务
   ↓
[UserPromptSubmit Hook] 检查是否存在 task_plan.md
   ↓
[Phase 0: 规划]
   创建 task_plan.md → 定义 goal + phases
   创建 findings.md → 记录初始需求
   创建 progress.md → 开始 session log
   ↓
[Phase 1-N: 执行]
   ├── [PreToolUse] head -30 task_plan.md (刷新注意力)
   ├── 执行动作 (Write/Edit/Bash)
   ├── [PostToolUse] 提醒更新 progress.md
   ├── 每 2 次 view/search → 更新 findings.md (2-Action Rule)
   └── 标记 Phase **Status:** complete
   ↓
[Stop Hook]
   ├── TOTAL=$(grep -c "### Phase" task_plan.md)
   ├── COMPLETE=$(grep -cF "**Status:** complete" task_plan.md)
   ├── COMPLETE < TOTAL → followup_message (自动继续)
   └── COMPLETE == TOTAL → 任务完成
```

### 3-Strike Error Protocol

```
ATTEMPT 1: Diagnose & Fix (targeted)
   ↓ 失败
ATTEMPT 2: Mutate (不同方法/工具)
   ↓ 失败
ATTEMPT 3: Rethink (质疑假设)
   ↓ 失败
ESCALATE: 请求用户帮助

规则: 绝不重复完全相同的失败操作
```

### Failure Paths

| 失败场景 | 系统响应 |
|----------|----------|
| Goal drift | PreToolUse hook 重读 plan 刷新注意力 |
| 多模态信息丢失 | 2-Action Rule 强制捕获到 findings.md |
| 错误静默重复 | Error log 记录 + 3-Strike 升级策略 |
| Session 丢失 (`/clear`) | session-catchup.py 从 IDE session store 恢复 |
| Phase 不完整时 agent 停止 | Stop hook 检测并自动 followup |

---

## 5. 执行保障审计

| 机制 | 级别 | 说明 |
|------|------|------|
| PreToolUse Hook (attention manipulation) | **Hard** | 每次 Write/Edit/Bash 前自动读取 plan |
| Stop Hook (phase completion check) | **Hard** | 未完成 phase 时自动 followup 继续 |
| UserPromptSubmit (context injection) | **Hard** | 每条消息自动注入 plan state |
| PostToolUse (progress reminder) | **Hard** | 每次工具使用后提醒更新 progress |
| 3-File Pattern | **Soft** | SKILL.md 要求创建 3 文件，但无文件存在性校验 |
| 2-Action Rule | **Soft** | Prompt 要求每 2 次 view/search 更新 findings，无 hook 强制 |
| 3-Strike Protocol | **Soft** | Prompt 指令，无自动计数器 |
| Conventional Commit / Branch 命名 | **Unenforced** | SKILL.md 未涉及 |
| Security Boundary (v2.21.0) | **Hard** | 移除 WebFetch/WebSearch 从 allowed-tools |

---

## 6. Prompt 目录

### Prompt 1: 5 Core Rules (SKILL.md 核心)

```
5 条核心规则:
1. CREATE PLAN FIRST — 绝不在没有 task_plan.md 的情况下开始
2. 2-ACTION RULE — 每 2 次 view/search 操作后更新 findings.md
3. READ BEFORE DECIDE — 重大决策前刷新目标
4. UPDATE AFTER ACT — 标记 phase 完成，立即记录错误
5. LOG ALL ERRORS — 错误表 (error | attempt | resolution)
```

### Prompt 2: 6 Context Engineering Principles (来自 Manus)

```
1. KV-Cache Design — 稳定 prompt + append-only 序列化 (~10x 成本优化)
2. Mask, Don't Remove — logit masking 替代动态工具移除
3. Filesystem as Memory — Context = RAM (volatile), Files = Disk (unlimited)
4. Attention Manipulation — 决策前重读 plan 保持目标在近期上下文
5. Keep Wrong Stuff In — 记录所有错误 (失败操作防止重复)
6. Vary Patterns — 不使用 few-shot (打破重复动作序列)
```

---

## 7. 微观设计亮点

### 7.1 PreToolUse 的 Attention Manipulation

最精巧的设计：每次 Write/Edit/Bash 操作前，hook 自动执行 `head -30 task_plan.md`。这将 plan 的前 30 行（目标 + 当前阶段）注入到 LLM 的 **recent context** 中，利用 transformer 的 recency bias 保持 agent 的目标意识。这是一种无需修改 LLM 权重的 soft attention manipulation。

### 7.2 Stop Hook 的自动续航

Stop hook 通过 `grep -c` 比较 Phase 总数和已完成数。若不相等，返回 `followup_message` 触发 agent 自动继续。这消除了 agent 过早停止的常见问题——agent 以为任务完成了，但实际上还有未完成的 Phase。

### 7.3 2-Action Rule 对抗信息衰减

要求每 2 次 view/search 操作后更新 findings.md，解决了 LLM context window 中 **信息衰减** 的问题。研究发现（从 browser/multimodal 获取的信息尤其脆弱），如果不立即持久化，LLM 会在后续 turn 中遗忘。

---

## 8. 宏观设计亮点

### 8.1 "Encoded Discipline, Not Capability Uplift"

框架的核心洞察：planning-with-files 编码的是 **纪律**（discipline），而非能力（capability）。Baseline agent 也能创建文件、写计划——但它们不会。评估数据证实：without_skill agents 0/5 次创建了 3-file pattern，尽管技术上完全有能力这么做。Skill 的价值在于让 agent **始终遵循最佳实践**。

### 8.2 A/B Verified 的工程严谨性

96.7% pass rate + 3/3 blind A/B wins + 30 objectively verifiable assertions——这是 Claude Code skill 生态中少见的严格实证验证。Token 成本 +68% 被显式记录为 "structured output 的代价"，体现了工程权衡的透明度。

---

## 9. 失败模式与局限

| # | 失败模式 | 严重度 | 说明 |
|---|----------|--------|------|
| 1 | **Token overhead** | 中 | 4 个 hook + 3 个文件导致 +68% token 成本，长任务中累积显著 |
| 2 | **Hook 固化 attention** | 中 | PreToolUse 始终读取前 30 行，若 plan 结构变化可能读到过时信息 |
| 3 | **2-Action Rule 依赖自觉** | 中 | 无 hook 强制计数，AI 可能忽略此规则 |
| 4 | **Security 残留风险** | 中 | v2.21.0 移除了 WebFetch/WebSearch，但外部文件读取仍可能引入恶意内容 |
| 5 | **Session recovery 平台依赖** | 低 | session-catchup.py 依赖特定 IDE 的 session store 路径 |
| 6 | **3-file 刚性** | 低 | 所有任务类型使用相同的 3-file template，小任务 overhead 偏高 |

---

## 10. 迁移评估

### 可迁移候选

| 机制 | 目标插件 | 可行性 | 备注 |
|------|----------|--------|------|
| PreToolUse Attention Manipulation | `workflows/deep-plan` | ★★★ | Hook 逻辑可直接复用 |
| Stop Hook Auto-Continue | `quality/meeseeks-vetted` | ★★★ | "verified work before exit" 的技术实现 |
| 3-File Template System | `integrations/utils` | ★★☆ | 可作为通用 planning template |
| 2-Action Rule | `quality/ai-hygiene` | ★★☆ | 信息持久化纪律可作为 hygiene check |
| 3-Strike Error Protocol | `quality/testing` | ★★★ | 错误升级策略对 TDD 高度有用 |
| Session Recovery | `integrations/catchup` | ★★☆ | 与 catchup 插件的功能互补 |

### 建议采纳顺序

1. **PreToolUse + Stop Hook pattern** → 作为 hook 工程的标准实践推广到多个插件
2. **3-Strike Error Protocol** → 融入 testing 插件的 error handling 指导
3. **3-File Template** → 简化后作为 deep-plan 的轻量级规划选项

---

## 11. 开放问题

1. **Hook 性能影响**: 4 个 hook 的累积延迟在大型项目中是否可测量？是否需要 hook 条件触发（而非始终触发）？
2. **动态 template**: 是否有计划根据任务类型（bugfix vs feature vs refactor）使用不同的 file template？
3. **多 agent 协作**: 当多个 agent 同时使用 planning-with-files 时，3 个文件是否会冲突？
4. **Benchmark 可复现性**: 评估使用的 5 个 task 是否公开？其他人能否用相同方法论复现结果？
5. **v2.21.0 → v2.34.1 变更**: 安全修复后的 13 个版本中，核心架构是否有重大变化？
