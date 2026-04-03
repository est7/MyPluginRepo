# Workflow Research: Superpowers

**Date**: 2026-04-03
**Source**: `vendor/superpowers` (obra/superpowers, v5.0.7)
**Analyst mode**: Single
**Focus**: All

---

## 1. Framework Profile

| Attribute | Value |
|-----------|-------|
| **Type** | Workflow harness + skill library hybrid |
| **Total files** | 143 |
| **Prompt files** | 20 (14 SKILL.md + 3 reviewer prompts + 1 implementer prompt + 1 agent + 1 GEMINI.md) |
| **Scripts/hooks** | 9 (session-start, run-hook.cmd, start-server.sh, stop-server.sh, server.cjs, helper.js, frame-template.html, bump-version.sh, find-polluter.sh) |
| **Test files** | 26 (across 5 test suites) |
| **Entry points** | `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.cursor-plugin/plugin.json`, `gemini-extension.json`, `hooks/hooks.json`, `hooks/hooks-cursor.json`, `.opencode/plugins/superpowers.js` |
| **Registration mechanism** | Claude Code plugin system (auto-discovery via plugin.json) + SessionStart hook 注入 `using-superpowers` |
| **Language** | Markdown (skills), Bash (hooks/scripts), JavaScript/CJS (brainstorm server), Python (token analysis) |

### Directory Map

```
vendor/superpowers/
├── .claude-plugin/
│   ├── plugin.json              # Plugin manifest (v5.0.7)
│   └── marketplace.json         # Dev marketplace definition
├── .cursor-plugin/plugin.json   # Cursor plugin manifest
├── .opencode/
│   ├── plugins/superpowers.js   # OpenCode native plugin
│   └── INSTALL.md
├── .codex/INSTALL.md
├── hooks/
│   ├── hooks.json               # Claude Code hook config
│   ├── hooks-cursor.json        # Cursor hook config
│   ├── session-start            # SessionStart hook script (extensionless)
│   └── run-hook.cmd             # Windows polyglot wrapper
├── skills/
│   ├── using-superpowers/       # 元技能：skill 发现与调用规则
│   ├── brainstorming/           # 需求探索与设计
│   ├── writing-plans/           # 实施计划编写
│   ├── executing-plans/         # 内联执行（无 subagent）
│   ├── subagent-driven-development/  # Subagent 驱动执行
│   ├── test-driven-development/ # TDD 纪律
│   ├── systematic-debugging/    # 系统化调试
│   ├── dispatching-parallel-agents/  # 并行 agent 调度
│   ├── requesting-code-review/  # 请求代码审查
│   ├── receiving-code-review/   # 接收代码审查
│   ├── verification-before-completion/ # 完成前验证
│   ├── using-git-worktrees/     # Git worktree 隔离
│   ├── finishing-a-development-branch/ # 分支完成流程
│   └── writing-skills/          # 元技能：创建新 skill
├── agents/
│   └── code-reviewer.md         # 代码审查 agent 定义
├── commands/
│   ├── brainstorm.md            # 已废弃，指向 brainstorming skill
│   ├── write-plan.md            # 已废弃
│   └── execute-plan.md          # 已废弃
├── tests/                       # 5 个测试套件
├── docs/                        # 设计文档、计划、规格说明
├── CLAUDE.md                    # 贡献者指南
├── GEMINI.md                    # Gemini CLI 入口（@imports）
├── README.md
├── CHANGELOG.md
├── RELEASE-NOTES.md
└── package.json                 # OpenCode npm 入口
```

---

## 2. Source Inventory

### Overview Sources

| File | Type | Why It Matters |
|------|------|---------------|
| `README.md` | 项目介绍 | 定义核心工作流序列（brainstorm → plan → execute → finish） |
| `CLAUDE.md` | 贡献者指南 | 94% PR 拒绝率声明，揭示项目对质量的极端要求 |
| `RELEASE-NOTES.md` | 版本演化 | 记录从 v2.0 → v5.0.7 的架构演变轨迹 |
| `CHANGELOG.md` | 变更日志 | v5.0.5 核心修复细节 |

### Execution Sources

| File | Type | Why It Matters |
|------|------|---------------|
| `skills/brainstorming/SKILL.md` | Skill | 设计探索的强制流程门控 |
| `skills/writing-plans/SKILL.md` | Skill | 计划编写的结构化模板 |
| `skills/subagent-driven-development/SKILL.md` | Skill | 核心执行引擎：per-task subagent + 双阶段审查 |
| `skills/executing-plans/SKILL.md` | Skill | 备选执行路径（无 subagent 平台） |
| `skills/test-driven-development/SKILL.md` | Skill | TDD 纪律的强制执行 |
| `skills/systematic-debugging/SKILL.md` | Skill | 四阶段调试流程 |
| `skills/using-git-worktrees/SKILL.md` | Skill | 隔离工作区的标准化流程 |
| `skills/finishing-a-development-branch/SKILL.md` | Skill | 分支完成的四选项决策 |

### Prompt Sources

| File | Type | Why It Matters |
|------|------|---------------|
| `skills/using-superpowers/SKILL.md` | 元 prompt | SessionStart 注入的根指令，控制 skill 调用行为 |
| `skills/subagent-driven-development/implementer-prompt.md` | 子 agent prompt | 实现者的完整指令模板（含自审、上报协议） |
| `skills/subagent-driven-development/spec-reviewer-prompt.md` | 子 agent prompt | 规格符合性审查者（强调不信任实现者报告） |
| `skills/subagent-driven-development/code-quality-reviewer-prompt.md` | 子 agent prompt | 代码质量审查者 |
| `skills/brainstorming/spec-document-reviewer-prompt.md` | 子 agent prompt | 规格文档审查者（已被 v5.0.6 内联自审取代） |
| `skills/writing-plans/plan-document-reviewer-prompt.md` | 子 agent prompt | 计划文档审查者（已被 v5.0.6 内联自审取代） |
| `agents/code-reviewer.md` | Agent 定义 | 代码审查 agent 的系统 prompt |
| `skills/requesting-code-review/code-reviewer.md` | Prompt 模板 | 审查请求的变量填充模板 |

### Enforcement Sources

| File | Type | Why It Matters |
|------|------|---------------|
| `hooks/hooks.json` | Hook 配置 | SessionStart 钩子的唯一硬执行点 |
| `hooks/session-start` | Shell 脚本 | 读取 using-superpowers 并注入 session context |
| `hooks/run-hook.cmd` | Polyglot wrapper | Windows 兼容性 |

### Evolution Evidence

| Source | Type | Why It Matters |
|--------|------|---------------|
| `RELEASE-NOTES.md` | 完整版本历史 | 揭示 v2→v5 的架构演变方向和失败模式 |
| `tests/claude-code/` | 集成测试 | 用 `claude -p` 验证 skill 合规性 |
| `tests/skill-triggering/` | 触发测试 | 验证 description 能否正确触发 skill |
| `tests/explicit-skill-requests/` | 显式请求测试 | 验证用户点名请求时 skill 被正确调用 |
| `tests/subagent-driven-dev/` | E2E 测试 | 完整 SDD 工作流的端到端验证 |
| `tests/brainstorm-server/` | 单元/集成测试 | Brainstorm 可视化服务器的功能验证 |

---

## 3. Object Model

### First-Class Entities

| Entity | Definition Location | Required Fields | Lifecycle | Type |
|--------|-------------------|-----------------|-----------|------|
| **Skill** | `skills/*/SKILL.md` | name, description (YAML frontmatter) | 注册 → SessionStart 展示 → 按需调用 → 跟随 | Fact object |
| **Spec (Design)** | `skills/brainstorming/SKILL.md:29` | 架构、组件、数据流、错误处理、测试 | 探索 → 设计 → 自审 → 用户审批 → 写入文件 | Fact object |
| **Plan** | `skills/writing-plans/SKILL.md:46-104` | Goal, Architecture, Tech Stack, Tasks[] | 从 spec 生成 → 自审 → 用户选择执行方式 | Fact object |
| **Task** | `skills/writing-plans/SKILL.md:66-104` | Files, Steps[], 每步含代码和验证命令 | Pending → In-progress → Review → Complete | Fact object |
| **Implementer Report** | `skills/subagent-driven-development/implementer-prompt.md:100-113` | Status, 实现内容, 测试结果, 变更文件, 自审发现 | 实现 → 自审 → 提交报告 | Evidence object |
| **Spec Review Verdict** | `skills/subagent-driven-development/spec-reviewer-prompt.md:59-61` | ✅ Compliant / ❌ Issues (带 file:line) | 审查 → 通过或驳回 → 修复循环 | Judgment object |
| **Code Quality Verdict** | `agents/code-reviewer.md:65-93` | Strengths, Issues (Critical/Important/Minor), Assessment | 审查 → 评级 → 通过或驳回 | Judgment object |
| **Worktree** | `skills/using-git-worktrees/SKILL.md` | 路径, 分支名, 测试基线 | 创建 → 安装依赖 → 验证基线 → 使用 → 清理 | Fact object |

### Entity Relationships

```
User Request
    ↓
  Spec (brainstorming → design doc)
    ↓
  Plan (writing-plans → task list)
    ↓ contains 1..N
  Task
    ↓ per task
  Implementer Report ← Implementer Subagent
    ↓
  Spec Review Verdict ← Spec Reviewer Subagent
    ↓ (pass required)
  Code Quality Verdict ← Code Reviewer Subagent
    ↓ (pass required)
  [next Task]
    ↓ (all done)
  Final Code Review → Branch Completion
```

依赖方向：单向，从 Spec → Plan → Task → Review 形成线性流水线。Worktree 在 Plan 之后、Task 执行之前创建。

### Context Isolation Strategy

| Scope | What Flows | Mechanism | Evidence |
|-------|-----------|-----------|----------|
| Controller → Implementer | 完整 task 文本 + 场景上下文 | 新建 subagent，注入精确上下文 | `subagent-driven-development/SKILL.md:10-11`, `implementer-prompt.md:13` |
| Controller → Spec Reviewer | 需求规格全文 + 实现者声明 | 独立 subagent，不信任实现者报告 | `spec-reviewer-prompt.md:22-30` |
| Controller → Code Reviewer | git diff (BASE_SHA..HEAD_SHA) + 计划引用 | 独立 subagent，基于 SHA 范围 | `code-reviewer.md:26-28` |
| Cross-task | TodoWrite 状态 | Claude 内置 task 追踪 | `subagent-driven-development/SKILL.md:133` |
| Session → Subagent | 无继承 | SUBAGENT-STOP 阻断 using-superpowers 在子 agent 中激活 | `using-superpowers/SKILL.md:6-8` |

---

## 4. Flow & State Machine

### Happy Path

1. **Session 启动** → SessionStart hook 执行 `hooks/session-start`，读取 `using-superpowers/SKILL.md`，注入 `<EXTREMELY_IMPORTANT>` 上下文 — `hooks/session-start:17-35`
2. **用户提出请求** → using-superpowers 要求检查是否有适用 skill（1% 规则）— `using-superpowers/SKILL.md:46`
3. **触发 brainstorming** → 探索上下文 → 一次一个问题 → 提出 2-3 方案 → 分段展示设计 → 用户审批 — `brainstorming/SKILL.md:22-33`
4. **写入 spec 文件** → `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` → 自审（占位符/一致性/范围/歧义）→ 用户审查 spec — `brainstorming/SKILL.md:109-131`
5. **调用 writing-plans** → 文件结构映射 → 拆分为 2-5 分钟的 bite-sized task → 含完整代码/命令/预期输出 → 自审 — `writing-plans/SKILL.md:38-44`
6. **用户选择执行方式** → Subagent-driven（推荐）或 Inline Execution — `writing-plans/SKILL.md:136-153`
7. **SDD 执行**（per task）：
   - 7a. 调度实现者 subagent（含完整 task 文本 + 上下文）— `subagent-driven-development/SKILL.md:48`
   - 7b. 实现者可提问、实现、测试、提交、自审 — `implementer-prompt.md:29-37`
   - 7c. 调度 spec 审查者（独立验证代码是否匹配规格）— `subagent-driven-development/SKILL.md:72`
   - 7d. spec 审查通过后，调度代码质量审查者 — `subagent-driven-development/SKILL.md:76`
   - 7e. 两阶段均通过 → 标记 task 完成 → 下一个 task — `subagent-driven-development/SKILL.md:79`
8. **所有 task 完成** → 调度最终代码审查 → 调用 finishing-a-development-branch — `subagent-driven-development/SKILL.md:82-83`
9. **分支完成** → 验证测试 → 呈现 4 选项（merge/PR/keep/discard）→ 执行 → 清理 worktree — `finishing-a-development-branch/SKILL.md:18-150`

### Phase Transitions

| From | To | Trigger | Gate? | Evidence |
|------|----|---------|-------|----------|
| Session Start | Skill Check | 用户消息到达 | Hard (SessionStart hook) | `hooks/hooks.json:3-14` |
| Skill Check | Brainstorming | 创造性工作（feature/component/行为修改） | Soft (1% 规则) | `using-superpowers/SKILL.md:46` |
| Brainstorming | Writing Plans | 用户审批 spec | Soft (checklist step 9) | `brainstorming/SKILL.md:32` |
| Writing Plans | Execution Choice | 计划完成并保存 | Soft (用户选择) | `writing-plans/SKILL.md:136-153` |
| SDD: Implement | Spec Review | 实现者报告 DONE | Soft (流程图) | `subagent-driven-development/SKILL.md:71-73` |
| SDD: Spec Review | Code Review | Spec ✅ 通过 | Soft (流程图顺序) | `subagent-driven-development/SKILL.md:76` |
| SDD: Code Review | Next Task | Code ✅ 通过 | Soft (流程图顺序) | `subagent-driven-development/SKILL.md:79` |
| All Tasks Done | Finishing | 最后一个 task 完成 | Soft | `subagent-driven-development/SKILL.md:82-83` |

### Failure Paths

#### Failure Path 1: Implementer BLOCKED

实现者无法完成 task → 报告 BLOCKED 状态 → Controller 评估原因：
- 上下文不足 → 补充上下文重新调度（同模型）
- 超出能力 → 升级到更强模型重新调度
- Task 太大 → 拆分为更小的 task
- 计划本身有误 → 升级到用户

Evidence: `subagent-driven-development/SKILL.md:110-118`

#### Failure Path 2: Spec Reviewer 发现不一致

Spec 审查者报告 ❌ → 原实现者 subagent 修复 → 再次审查 → 循环直到通过。
**不跳过再审。** 审查者发现问题 = 实现者修复 = 审查者再次审查。

Evidence: `subagent-driven-development/SKILL.md:255-259`

#### Failure Path 3: 3+ 修复失败（调试场景）

systematic-debugging 中，如果 3 次修复尝试均失败 → 停止修复 → 质疑架构 → 与用户讨论。

Evidence: `systematic-debugging/SKILL.md:196-213`

### Parallelism

| Parallel Unit | What Runs | Synchronization | Evidence |
|--------------|-----------|-----------------|----------|
| Dispatching-parallel-agents | 多个 subagent 分别处理独立失败 | 所有 agent 返回后合并结果，运行完整测试套件 | `dispatching-parallel-agents/SKILL.md:50-83` |
| SDD task 执行 | 严格串行（禁止并行实现 subagent） | 一次一个 task，上一个完成后才开始下一个 | `subagent-driven-development/SKILL.md:240` |

---

## 5. Enforcement Audit

### Enforcement Matrix

| # | Constraint | Source | Level | Evidence | Gap? |
|---|-----------|--------|-------|----------|------|
| 1 | SessionStart 注入 using-superpowers | `hooks/hooks.json:3-14` | **Hard** | Bash hook 在 session 启动时自动执行 | No |
| 2 | 1% 规则：可能适用就必须调用 skill | `using-superpowers/SKILL.md:10-15` | **Soft** | 仅 prompt 指令，无代码阻止跳过 | Yes |
| 3 | Brainstorming 必须在实现前完成 | `brainstorming/SKILL.md:12-14` `<HARD-GATE>` | **Soft** | XML 标签增加说服力，但无 hook 阻止跳过 | Yes |
| 4 | 设计需用户审批后才能进入 writing-plans | `brainstorming/SKILL.md:31-32` | **Soft** | Checklist step 8，仅 prompt 要求 | Yes |
| 5 | TDD：生产代码前必须有失败测试 | `test-driven-development/SKILL.md:32-36` | **Soft** | "Iron Law"仅为 prompt 指令 | Yes |
| 6 | 写代码在测试之前？删除重来 | `test-driven-development/SKILL.md:37-45` | **Soft** | 极其强硬的措辞（"Delete means delete"），但无 hook 执行 | Yes |
| 7 | 调试：修复前必须完成根因调查 | `systematic-debugging/SKILL.md:16-18` | **Soft** | "Iron Law"仅为 prompt 指令 | Yes |
| 8 | 完成声明前必须运行验证命令 | `verification-before-completion/SKILL.md:21-23` | **Soft** | "Iron Law"仅为 prompt 指令 | Yes |
| 9 | Spec 审查者必须独立验证代码 | `spec-reviewer-prompt.md:22-30` | **Soft** | Prompt 说"DO NOT trust report"，但审查者行为不受 hook 约束 | Yes |
| 10 | Code quality 审查必须在 spec 审查之后 | `subagent-driven-development/SKILL.md:247` | **Soft** | Red Flag 列表中提及，流程图显示顺序 | Yes |
| 11 | Worktree 目录必须被 .gitignore | `using-git-worktrees/SKILL.md:55-68` | **Soft** | 脚本指导检查但无自动执行 | Yes |
| 12 | 不在 main 分支上实现（需用户明确同意） | `subagent-driven-development/SKILL.md:237`, `executing-plans/SKILL.md:63` | **Soft** | 仅 prompt 指令 | Yes |
| 13 | Subagent 不继承 session context | `subagent-driven-development/SKILL.md:10-11` | **Soft** | 架构原则，依赖 controller 正确调度 | Yes |
| 14 | SUBAGENT-STOP：子 agent 跳过 using-superpowers | `using-superpowers/SKILL.md:6-8` | **Soft** | XML 标签指令，无代码强制 | Yes |
| 15 | Slash commands 已废弃 | `commands/brainstorm.md:5` | **Soft** | 命令文件存在但内容是废弃提示 | No |
| 16 | Receiving code review：禁止表演性赞同 | `receiving-code-review/SKILL.md:30-33` | **Soft** | "NEVER: You're absolutely right!" 仅为 prompt | Yes |

### Enforcement Statistics

| Level | Count | Percentage |
|-------|-------|------------|
| Hard-enforced | 1 | 6.25% |
| Soft-enforced | 15 | 93.75% |
| Unenforced | 0 | 0% |

### Critical Gaps

**核心发现：Superpowers 几乎完全依赖 prompt 级软执行。** 唯一的硬执行点是 SessionStart hook 注入 using-superpowers 内容。所有工作流约束（TDD、审查顺序、brainstorming-before-coding、验证门控）均为 prompt 指令，理论上可被 agent 跳过。

框架作者显然意识到这一点，并通过以下手段弥补：
1. **极端措辞**："Iron Law", "EXTREMELY IMPORTANT", "non-negotiable"
2. **反合理化表**：预封堵 agent 可能的借口
3. **Red Flags 列表**：自我检查清单
4. **流程图作为权威定义**：DOT graph 比散文更难被 agent 忽略
5. **CSO (Claude Search Optimization)**：description 字段优化以确保触发

这是一种 **"说服力即执行力"** 的设计哲学——框架无法从代码层面阻止违规，但通过精心设计的 prompt 心理学来最大化合规率。

---

## 6. Prompt Catalog

### Prompt: Using-Superpowers (Orchestrator)

| Field | Value |
|-------|-------|
| **role** | 元 orchestrator：控制 skill 发现和调用 |
| **repo_path** | `skills/using-superpowers/SKILL.md` |
| **quote_excerpt** | "If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill. IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT." |
| **stage** | Session 启动时注入（通过 SessionStart hook） |
| **design_intent** | 确保 agent 在每个用户消息前都检查可用 skill，消除跳过 skill 的合理化借口 |
| **hidden_assumption** | Claude 的 Skill tool 能正确列出和加载 skill；agent 会阅读并遵循 `<EXTREMELY-IMPORTANT>` 标签 |
| **likely_failure_mode** | Context 压缩后 using-superpowers 内容被截断；agent 在长对话中逐渐忘记 1% 规则 |
| **evidence_level** | direct |

### Prompt: Brainstorming

| Field | Value |
|-------|-------|
| **role** | 设计探索者 |
| **repo_path** | `skills/brainstorming/SKILL.md` |
| **quote_excerpt** | "Do NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action until you have presented a design and the user has approved it." |
| **stage** | 实现前的设计阶段 |
| **design_intent** | 阻止 agent 跳过设计直接写代码；强制一次一个问题的探索节奏 |
| **hidden_assumption** | 用户愿意参与多轮对话式设计探索；"简单"项目也需要设计 |
| **likely_failure_mode** | 用户说"这很简单直接做就行"时，agent 可能顺从跳过设计 |
| **evidence_level** | direct |

### Prompt: Implementer Subagent

| Field | Value |
|-------|-------|
| **role** | 实现者 |
| **repo_path** | `skills/subagent-driven-development/implementer-prompt.md` |
| **quote_excerpt** | "It is always OK to stop and say 'this is too hard for me.' Bad work is worse than no work. You will not be penalized for escalating." |
| **stage** | SDD per-task 执行 |
| **design_intent** | 鼓励实现者提问和上报而非猜测；含自审清单防止低质量输出 |
| **hidden_assumption** | 计划中的 task 描述足够完整（含代码、路径、命令）；实现者有足够的工具权限 |
| **likely_failure_mode** | 实现者总是报告 DONE 而非 DONE_WITH_CONCERNS（过度自信） |
| **evidence_level** | direct |

### Prompt: Spec Reviewer Subagent

| Field | Value |
|-------|-------|
| **role** | 规格符合性审查者 |
| **repo_path** | `skills/subagent-driven-development/spec-reviewer-prompt.md` |
| **quote_excerpt** | "The implementer finished suspiciously quickly. Their report may be incomplete, inaccurate, or optimistic. You MUST verify everything independently. DO NOT: Take their word for what they implemented." |
| **stage** | SDD 每 task 实现后的第一阶段审查 |
| **design_intent** | 培养怀疑论审查者——不信任实现者的自述，独立阅读代码验证 |
| **hidden_assumption** | 审查者有能力阅读和理解实现代码；git diff 足以判断是否匹配规格 |
| **likely_failure_mode** | 审查者仍然信任实现者报告（prompt 心理学不够强）；对大量代码审查疲劳导致漏检 |
| **evidence_level** | direct |

### Prompt: Verification-Before-Completion

| Field | Value |
|-------|-------|
| **role** | 完成门控 |
| **repo_path** | `skills/verification-before-completion/SKILL.md` |
| **quote_excerpt** | "Claiming work is complete without verification is dishonesty, not efficiency. If you haven't run the verification command in this message, you cannot claim it passes." |
| **stage** | 任何完成声明之前 |
| **design_intent** | 阻止 agent 说"should work"/"looks good"而不实际运行验证命令 |
| **hidden_assumption** | 存在可运行的验证命令（测试、构建、lint）；agent 有权限执行 |
| **likely_failure_mode** | Agent 运行测试但选择性报告（只报告通过的，忽略失败的） |
| **evidence_level** | direct |

### Prompt: Receiving-Code-Review

| Field | Value |
|-------|-------|
| **role** | 审查反馈接收者 |
| **repo_path** | `skills/receiving-code-review/SKILL.md` |
| **quote_excerpt** | "Code review requires technical evaluation, not emotional performance. NEVER: 'You're absolutely right!' / 'Great point!' / 'Excellent feedback!'" |
| **stage** | 收到代码审查反馈后 |
| **design_intent** | 消除 AI agent 的"表演性认同"倾向——要求技术验证而非社交性赞同 |
| **hidden_assumption** | Agent 有能力区分正确反馈和错误反馈；push back 不会冒犯审查者 |
| **likely_failure_mode** | Agent 在避免表演性认同的同时走向另一个极端——过度 push back |
| **evidence_level** | direct |

---

## 7. Design Highlights — Micro

### Highlight: Anti-Rationalization Tables

- **Observation**: 几乎每个纪律性 skill（TDD, debugging, verification）都包含一个 "Common Rationalizations" 表，列出 agent 可能用来跳过流程的借口，并逐一反驳
- **Evidence**: `test-driven-development/SKILL.md:256-270`, `systematic-debugging/SKILL.md:245-257`, `verification-before-completion/SKILL.md:63-75`, `using-superpowers/SKILL.md:80-95`
- **Why it matters**: 这是对 LLM agent 行为的深度理解——agent 不会直接拒绝指令，而是通过"合理化"来绕过指令。预封堵这些借口是有效的软执行策略
- **Trade-off**: 占用 token 预算（每个表约 150-200 tokens），且需要持续维护（新的合理化模式出现时需要更新）
- **Transferability**: **Direct** — 这是最容易直接移植的模式

### Highlight: DOT Flowchart 作为权威流程定义

- **Observation**: 关键 skill 使用 Graphviz DOT 语法定义流程图，流程图是权威定义，散文是辅助说明
- **Evidence**: `brainstorming/SKILL.md:36-63`, `subagent-driven-development/SKILL.md:16-84`, `test-driven-development/SKILL.md:49-69`, `using-superpowers/SKILL.md:48-75`
- **Why it matters**: v4.0 release notes 记录了一个关键发现——当散文和流程图冲突时，Claude 更倾向于遵循流程图。DOT graph 的结构化格式比自然语言散文更难被误解或忽略
- **Trade-off**: DOT 语法增加了 skill 编写的复杂度；渲染需要工具（`render-graphs.js`）
- **Transferability**: **Direct** — 我们的 skill 也可以直接使用 DOT flowchart

### Highlight: 四状态实现者报告协议

- **Observation**: 实现者 subagent 报告四种状态：DONE, DONE_WITH_CONCERNS, BLOCKED, NEEDS_CONTEXT
- **Evidence**: `subagent-driven-development/SKILL.md:104-118`, `implementer-prompt.md:103`
- **Why it matters**: 比简单的 success/fail 更细粒度——特别是 DONE_WITH_CONCERNS 允许实现者完成工作但标记疑虑，避免 "silent failure"（静默低质量输出）
- **Trade-off**: 增加了 controller 的分支逻辑复杂度
- **Transferability**: **Direct** — 可直接用于任何 subagent 调度系统

### Highlight: CSO (Claude Search Optimization) for Descriptions

- **Observation**: description 字段的设计有一个关键发现——如果 description 包含工作流摘要，Claude 会直接跟随 description 而不读 skill body。因此 description 必须只包含触发条件
- **Evidence**: `writing-skills/SKILL.md:150-172`
- **Why it matters**: 这是一个经验教训——description 的措辞直接影响 skill 是否被正确执行。"陷阱"是 description 越详细越好的直觉是错的
- **Trade-off**: 限制了 description 的信息密度
- **Transferability**: **Direct** — 我们的 plugin-optimizer validator 可以检查这一规则

### Highlight: Bite-Sized Task 粒度（2-5 分钟）

- **Observation**: 每个 plan task 被分解为 2-5 分钟的步骤，每步恰好是一个动作："写失败测试"→"运行确认失败"→"写最小代码"→"运行确认通过"→"提交"
- **Evidence**: `writing-plans/SKILL.md:38-44`
- **Why it matters**: 极细粒度确保 subagent 不会偏离轨道——每步足够小以至于难以出错
- **Trade-off**: 计划文档变得冗长；对"资深开发者"来说可能过于啰嗦
- **Transferability**: **Inspired** — 粒度原则可借鉴，但需要根据项目复杂度调整

### Highlight: 双阶段审查（Spec → Quality）

- **Observation**: 每个 task 完成后经过两轮独立审查：先验证是否匹配规格（防止 over/under-building），再验证代码质量。顺序不可逆
- **Evidence**: `subagent-driven-development/SKILL.md:7-8`, `spec-reviewer-prompt.md`, `code-quality-reviewer-prompt.md`
- **Why it matters**: 分离"做对了吗"和"做好了吗"两个正交关注点——代码可以很优雅但完全偏离需求
- **Trade-off**: 成本高（每 task 需要 3 个 subagent：实现者 + 2 审查者）
- **Transferability**: **Inspired** — 概念优秀但成本高，可考虑轻量化变体

---

## 8. Design Highlights — Macro

### Philosophy: Process-as-Prose（说服力即执行力）

- **Observation**: 整个框架除 SessionStart hook 外零硬执行——所有约束通过精心设计的 prompt 语言实现
- **Where it appears**: 贯穿所有 skill——`<HARD-GATE>`标签 (`brainstorming/SKILL.md:12`), `<EXTREMELY-IMPORTANT>` (`using-superpowers/SKILL.md:10`), Iron Law pattern (`test-driven-development/SKILL.md:32`, `systematic-debugging/SKILL.md:16`, `verification-before-completion/SKILL.md:21`)
- **How it shapes the workflow**: 框架的"执行力"完全取决于 prompt 的说服力。作者投入大量精力在反合理化、措辞强度、格式选择（DOT > prose）上，本质上是在进行 LLM prompt 心理学研究
- **Strengths**: 零依赖、跨平台（Claude Code/Cursor/Codex/OpenCode/Gemini/Copilot CLI）、无需修改宿主系统
- **Limitations**: 合规率永远 <100%；长对话中 context 压缩可能丢失关键指令；模型更新可能改变合规行为
- **Adopt?**: **Modify** — 我们的 1st-cc-plugin 也主要是 prompt 级执行，但可以在关键路径上增加 hook 级硬执行（如 PreToolUse hook 验证 commit 格式）

### Philosophy: TDD-First（测试驱动一切）

- **Observation**: TDD 不仅用于代码，还用于 skill 本身的创建（RED-GREEN-REFACTOR 映射到 skill 文档开发）
- **Where it appears**: `test-driven-development/SKILL.md` (代码 TDD), `writing-skills/SKILL.md:374-393` (skill TDD)
- **How it shapes the workflow**: 每个 task 的步骤结构天然是 TDD 序列（写测试→确认失败→写代码→确认通过→提交）
- **Strengths**: 高测试覆盖率；subagent 产出的代码质量有保障
- **Limitations**: 对不需要测试的工作（配置、文档、基础设施脚本）增加不必要的仪式感
- **Adopt?**: **Modify** — 我们已有 testing skill，可借鉴 "TDD for skill creation" 概念和 rationalization table

### Philosophy: Verification-Over-Self-Report

- **Observation**: 系统从不信任 agent 的自我报告——spec 审查者被明确告知"不要信任实现者的报告"，completion 声明需要实际运行验证命令的输出作为证据
- **Where it appears**: `spec-reviewer-prompt.md:22-30`, `verification-before-completion/SKILL.md:21-23`
- **How it shapes the workflow**: 创建了一种"证据优先"文化——每个完成声明都需要命令输出作为背书
- **Strengths**: 显著减少"虚假完成"——RELEASE-NOTES 记录了历史上因信任 agent 报告而出现的问题 (`verification-before-completion/SKILL.md:111-115`)
- **Limitations**: 增加了交互轮次和 token 消耗
- **Adopt?**: **Yes** — 我们的 `meeseeks-vetted` 和 `testing` plugin 已有类似理念，可以强化

### Philosophy: 对话式设计探索

- **Observation**: Brainstorming 强调"一次一个问题"的苏格拉底对话模式，而非一次性要求用户提供所有需求
- **Where it appears**: `brainstorming/SKILL.md:76-78`
- **How it shapes the workflow**: 降低了用户的认知负担，但增加了对话轮次
- **Strengths**: 更好的需求发现——用户不需要预先想清楚所有需求
- **Limitations**: 对已经清楚需求的用户来说过于啰嗦；simple task 也被迫经历完整设计流程
- **Adopt?**: **Modify** — 我们的 `clarify` plugin 已有类似功能，但不如 brainstorming 的流程图那么结构化

### Philosophy: 上下文隔离与 Subagent 架构

- **Observation**: Controller 精心构造 subagent 的输入上下文，不让 subagent 继承 session 历史；SUBAGENT-STOP 标签阻止子 agent 激活 using-superpowers
- **Where it appears**: `subagent-driven-development/SKILL.md:10-11`, `using-superpowers/SKILL.md:6-8`
- **How it shapes the workflow**: 每个 subagent 都是"零上下文"启动，只获得精确需要的信息
- **Strengths**: 防止 context 污染；controller 保持轻量级用于协调
- **Limitations**: Controller 需要做大量准备工作（提取 task 文本、构造上下文）
- **Adopt?**: **Yes** — 这与我们的 `async-agent` 和 `superpowers` plugin 的 subagent 理念一致

---

## 9. Failure Modes & Limitations

| # | Failure Mode | Trigger | Impact | Evidence |
|---|-------------|---------|--------|----------|
| 1 | **Context 压缩丢失 using-superpowers** | 长对话中系统自动压缩 context | Agent 停止检查 skill，退化为默认行为 | Inferred: SessionStart hook 同步注入 (`hooks/hooks.json:9, async: false`) 仅在 session 开始时执行一次；v5.0.3 修复了 `--resume` 时重复注入的问题 (`RELEASE-NOTES.md:83`)，但 compact 后的恢复依赖 hook matcher 包含 `compact` (`hooks/hooks.json:6`) |
| 2 | **Description 陷阱** | Skill description 包含工作流摘要 | Agent 跟随 description 摘要而不读 skill body，导致流程不完整 | Direct: `writing-skills/SKILL.md:150-172`，v4.0 release notes 记录了 SDD 只做一次审查而非两次的案例 |
| 3 | **Brainstorming 绕过** | 用户说"这很简单直接做" | Agent 顺从用户跳过设计阶段 | Inferred: brainstorming 的 Anti-Pattern 段落 (`brainstorming/SKILL.md:16-18`) 和 HARD-GATE (`brainstorming/SKILL.md:12-14`) 存在说明这是已知问题 |
| 4 | **SDD 成本爆炸** | 每 task 3 个 subagent + 审查循环 | Token 消耗高，大 plan（10+ tasks）可能消耗数百万 token | Direct: `subagent-driven-development/SKILL.md:228-232` 承认了成本问题 |
| 5 | **Plan 文档冗长** | Bite-sized task 粒度要求完整代码 | Plan 文件可能达到数千行，超过 subagent 的有效 context | Inferred: 从 plan 模板结构推断 (`writing-plans/SKILL.md:66-104`) |
| 6 | **Subagent 审查疲劳** | Spec 审查者需要逐行对比代码和规格 | 大 task 中审查者可能遗漏不一致 | Inferred: 审查者 prompt 虽然要求"DO NOT trust"，但实际合规率取决于 context 大小 |
| 7 | **跨平台适配碎片化** | 支持 6 个平台（Claude Code/Cursor/Codex/OpenCode/Gemini/Copilot CLI） | 维护负担重；不同平台的 tool 等价映射可能不完整 | Direct: RELEASE-NOTES 大量篇幅用于修复平台特定问题（Windows hooks, OpenCode bootstrap, Codex paths） |

### Observed vs Claimed Behavior Divergences

| Claim | Source | Actual Behavior | Evidence | Evidence Level |
|-------|--------|----------------|----------|---------------|
| "Mandatory workflows, not suggestions" | `README.md:124` | 除 SessionStart hook 外所有约束均为 soft-enforced prompt 指令 | `hooks/hooks.json`（唯一硬执行点） | direct |
| "Skills trigger automatically" | `README.md:106` | 取决于 using-superpowers 的 1% 规则是否被遵循，无代码保证 | `using-superpowers/SKILL.md:10-15`（仅 prompt） | direct |
| Spec 审查者"独立验证" | `spec-reviewer-prompt.md:22` | 审查者是否真的独立读代码取决于 prompt 合规率 | 无自动化验证机制 | inferred |
| "Review loops repeat until approved" | `subagent-driven-development/SKILL.md:255-259` | 无最大迭代次数限制或超时机制（可能无限循环） | 流程图中无终止条件 | inferred |

---

## 10. Migration Assessment

### Candidates

| # | Mechanism | Rating | Effort | Prerequisite | Risk | Source |
|---|----------|--------|--------|-------------|------|--------|
| 1 | Anti-Rationalization Tables | Direct | S | 无 | 需要针对每个 skill 定制具体借口 | `test-driven-development/SKILL.md:256-270` |
| 2 | DOT Flowchart 作为权威流程 | Direct | S | Graphviz 语法知识 | 需要 render-graphs.js 或等价工具验证 | `brainstorming/SKILL.md:36-63` |
| 3 | 四状态 Subagent 报告协议 | Direct | S | Subagent 调度系统 | 需要 controller 处理所有四种状态 | `implementer-prompt.md:103` |
| 4 | CSO Description 规范 | Direct | S | plugin-optimizer validator | 规则简单但容易忘记 | `writing-skills/SKILL.md:150-172` |
| 5 | Verification-Before-Completion 门控 | Direct | S | 无 | 增加交互轮次 | `verification-before-completion/SKILL.md` |
| 6 | SUBAGENT-STOP 标签 | Direct | S | Subagent 调度系统 | 仅 prompt 级，可能被忽略 | `using-superpowers/SKILL.md:6-8` |
| 7 | 双阶段审查（Spec → Quality） | Inspired | M | SDD 基础设施 | 成本高（3x subagent/task），需要轻量化 | `subagent-driven-development/SKILL.md:7-8` |
| 8 | 对话式设计探索（一次一问） | Inspired | M | Brainstorming skill | 需要与现有 clarify plugin 整合 | `brainstorming/SKILL.md:76-78` |
| 9 | SessionStart Context 注入模式 | Direct | S | Hook 系统 | 已有类似实现 | `hooks/session-start` |
| 10 | Visual Brainstorm Companion | Inspired | L | Node.js + WebSocket | 零依赖服务器复杂；可能不符合我们的使用场景 | `brainstorming/visual-companion.md` |
| 11 | Skill TDD（RED-GREEN-REFACTOR for docs） | Inspired | M | 测试基础设施 | 需要 `claude -p` 或等价 headless 测试能力 | `writing-skills/SKILL.md:374-393` |
| 12 | Iron Law + Red Flags 模式 | Direct | S | 无 | 需要持续维护 | `test-driven-development/SKILL.md:32-36` |

### Recommended Adoption Order

1. **Anti-Rationalization Tables** (#1) + **Iron Law + Red Flags** (#12) — 投入最小、收益最大，可立即应用到现有纪律性 skill（testing, ai-hygiene, meeseeks-vetted）
2. **CSO Description 规范** (#4) — 在 plugin-optimizer validator 中增加检查：description 不应包含工作流摘要
3. **DOT Flowchart** (#2) — 在复杂流程 skill 中引入 DOT graph 作为权威定义
4. **四状态报告协议** (#3) + **SUBAGENT-STOP** (#6) — 在 async-agent 和 superpowers plugin 的 subagent 调度中引入
5. **Verification-Before-Completion** (#5) — 我们的 meeseeks-vetted 已有类似理念，可以强化措辞
6. **双阶段审查** (#7) — 先以轻量化形式引入（单 reviewer 同时检查 spec 和 quality），根据效果决定是否拆分

### Non-Transferable (with reasons)

| Mechanism | Why Not | Alternative |
|----------|---------|-------------|
| Visual Brainstorm Companion (#10) | 零依赖 WebSocket 服务器增加大量复杂度，我们的用户场景以 CLI 为主 | 如需可视化，使用 AskUserQuestion 的 preview 功能或外部工具 |
| 完整 SDD 流水线 | 3 subagent/task 的成本对大多数使用场景过高 | 保留概念（controller/implementer/reviewer 分离），降低审查频率 |
| 跨 6 平台适配 | 维护负担极重，我们专注 Claude Code 单一平台 | 无需替代 |

### Must-Build Enforcement

| Mechanism | Original Level | Recommended Level | How to Enforce |
|----------|---------------|-------------------|---------------|
| TDD 纪律 | Soft (prompt) | Medium (PreToolUse hook) | 在 git commit hook 中检查是否有对应测试文件变更 |
| Brainstorming before coding | Soft (prompt) | Soft (prompt，但可加强) | 在 skill 中使用 `<HARD-GATE>` 标签 + 流程图双重保障 |
| CSO description 规范 | Soft (skill 编写指南) | Hard (validator) | 在 plugin-optimizer validate-plugin.py 中增加 description 内容检查 |
| Commit 前验证 | Soft (prompt) | Hard (PreToolUse hook) | 已有 git plugin 的 PreToolUse hook，可扩展检查 |

---

## 11. Open Questions

1. **Superpowers v5.0.6 内联自审取代 subagent 审查**：release notes 声称"identical quality scores regardless of whether the review loop ran"——这是否意味着 subagent 审查的 ROI 被高估了？需要在我们的 codex-review plugin 中验证。
2. **Context 压缩后的 skill 恢复**：hooks.json 的 matcher 包含 `compact`，但 v5.0.3 修复了 `--resume` 时的重复注入。compact 后是否真的重新注入了 using-superpowers？需要实际测试验证。
3. **DOT graph 的实际合规率**：v4.0 声称"Claude 更倾向于遵循流程图"——这是否有定量数据支撑？我们是否应该投入精力将现有 skill 的散文流程改写为 DOT？
4. **Anti-rationalization table 的边际收益**：每个表占约 150-200 tokens。在多个 skill 同时加载时，累计 token 成本是否值得？Superpowers 的 `analyze-token-usage.py` 工具可能有相关数据。

---

## Appendix: Source Trace Table

| # | Source Type | Repo Path | Role | Excerpt | Evidence Level | Referenced In |
|---|-----------|-----------|------|---------|---------------|--------------|
| 1 | Hook config | `hooks/hooks.json` | SessionStart 触发 | `"matcher": "startup\|clear\|compact"` | direct | §4, §5 |
| 2 | Hook script | `hooks/session-start` | 注入 using-superpowers | `session_context="<EXTREMELY_IMPORTANT>..."` | direct | §4, §5 |
| 3 | Skill | `skills/using-superpowers/SKILL.md` | 元 orchestrator | "1% chance...ABSOLUTELY MUST" | direct | §3, §5, §6 |
| 4 | Skill | `skills/brainstorming/SKILL.md` | 设计门控 | `<HARD-GATE>` | direct | §4, §5, §6 |
| 5 | Skill | `skills/writing-plans/SKILL.md` | Plan 模板 | "2-5 minutes each" | direct | §4, §7 |
| 6 | Skill | `skills/subagent-driven-development/SKILL.md` | 执行引擎 | "Fresh subagent per task + two-stage review" | direct | §3, §4, §6, §7 |
| 7 | Prompt | `skills/subagent-driven-development/implementer-prompt.md` | 实现者指令 | "Bad work is worse than no work" | direct | §3, §6 |
| 8 | Prompt | `skills/subagent-driven-development/spec-reviewer-prompt.md` | 审查者指令 | "DO NOT: Take their word" | direct | §5, §6 |
| 9 | Skill | `skills/test-driven-development/SKILL.md` | TDD 纪律 | "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST" | direct | §5, §7, §8 |
| 10 | Skill | `skills/systematic-debugging/SKILL.md` | 调试流程 | "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST" | direct | §4, §5 |
| 11 | Skill | `skills/verification-before-completion/SKILL.md` | 完成门控 | "Evidence before claims, always" | direct | §5, §6 |
| 12 | Skill | `skills/writing-skills/SKILL.md` | Skill TDD | "Creating skills IS TDD for process documentation" | direct | §7, §8 |
| 13 | Skill | `skills/receiving-code-review/SKILL.md` | 反表演性认同 | "NEVER: You're absolutely right!" | direct | §6 |
| 14 | Agent | `agents/code-reviewer.md` | 代码审查 agent | "Senior Code Reviewer" | direct | §3, §6 |
| 15 | Release notes | `RELEASE-NOTES.md` | 演化证据 | v2.0→v5.0.7 完整历史 | direct | §1, §9 |
| 16 | Skill | `skills/writing-skills/SKILL.md:150-172` | CSO 发现 | "Description Trap" | direct | §7 |
