# Workflow Research: oh-my-claudecode (OMC)

> 逆向工程研究报告 | 2026-04-08
> 仓库: `Yeachan-Heo/oh-my-claudecode` v4.11.0
> 分类: Large (4728 files)

---

## 1. Source Inventory

### Overview

| 文件/路径 | 分类 | 描述 |
|-----------|------|------|
| `CLAUDE.md` | Overview | 压缩版系统提示，运行时注入 |
| `AGENTS.md` | Overview | 完整版协调器指令（含代理目录、技能、团队管线） |
| `docs/ARCHITECTURE.md` | Overview | 四大子系统架构文档 |
| `README.md` | Overview | 用户指南与安装说明 |
| `.claude-plugin/plugin.json` | Overview | Claude Code 插件清单 |
| `package.json` | Overview | npm 包配置 (oh-my-claude-sisyphus) |

### Execution

| 文件/路径 | 分类 | 描述 |
|-----------|------|------|
| `skills/ralph/SKILL.md` | Execution | PRD 驱动持久循环 |
| `skills/autopilot/SKILL.md` | Execution | 5 阶段自治管线 |
| `skills/team/SKILL.md` | Execution | N 代理协调团队 |
| `skills/ultrawork/SKILL.md` | Execution | 并行执行引擎 |
| `skills/ralplan/SKILL.md` | Execution | 共识规划入口 |
| `skills/deep-interview/SKILL.md` | Execution | 苏格拉底式歧义门控访谈 |
| `skills/cancel/SKILL.md` | Execution | 模式取消与状态清理 |
| `skills/ai-slop-cleaner/SKILL.md` | Execution | AI 代码清理工作流 |
| `agents/*.md` (19 files) | Execution | 专业化代理角色提示词 |

### Prompts

| 文件/路径 | 分类 | 描述 |
|-----------|------|------|
| `agents/executor.md` | Prompts | 执行代理提示词 |
| `agents/architect.md` | Prompts | 架构代理提示词（只读） |
| `agents/verifier.md` | Prompts | 验证代理提示词 |
| `agents/critic.md` | Prompts | 批评代理提示词 |
| `agents/planner.md` | Prompts | 规划代理提示词 |
| `agents/explore.md` | Prompts | 探索代理提示词 |

### Enforcement

| 文件/路径 | 分类 | 描述 |
|-----------|------|------|
| `hooks/hooks.json` | Enforcement | Hook 注册清单 |
| `scripts/keyword-detector.mjs` | Enforcement | 魔法关键词检测与技能注入 |
| `scripts/persistent-mode.cjs` | Enforcement | Stop hook 持久模式强制执行 |
| `scripts/pre-tool-enforcer.mjs` | Enforcement | PreToolUse 上下文注入与模型路由验证 |
| `scripts/subagent-tracker.mjs` | Enforcement | 子代理生命周期追踪 |
| `scripts/verify-deliverables.mjs` | Enforcement | SubagentStop 输出验证 |
| `scripts/context-guard-stop.mjs` | Enforcement | 上下文窗口警戒 |
| `scripts/pre-compact.mjs` | Enforcement | PreCompact 信息保存 |
| `scripts/project-memory-*.mjs` | Enforcement | 项目记忆生命周期管理 |

### Evolution

| 文件/路径 | 分类 | 描述 |
|-----------|------|------|
| `CHANGELOG.md` | Evolution | 版本变更记录 |
| `docs/MIGRATION.md` | Evolution | 版本迁移指南 |
| `.mcp.json` | Evolution | MCP 服务器配置 |
| `bridge/*.cjs` | Evolution | CLI 桥接层 (npm → Claude Code) |

---

## 2. Object Model

### 2.1 核心实体

#### Entity: Mode State

定义于 `scripts/persistent-mode.cjs` 和各 skill 的 `SKILL.md` 中。

```
ModeState {
  active: boolean
  started_at: ISO8601
  last_checked_at: ISO8601
  session_id: string
  project_path: string
  reinforcement_count: number
  awaiting_confirmation: boolean
}
```

每个模式扩展此基础结构：
- **Ralph**: `iteration`, `max_iterations`, `linked_ultrawork`, `linked_team`, `prompt`
- **Autopilot**: `current_phase`, `reinforcement_count`
- **Team**: `team_name`, `agent_count`, `agent_types`, `fix_loop_count`, `max_fix_loops`, `linked_ralph`, `stage_history`
- **Ultrawork**: `original_prompt`, `linked_to_ralph`, `max_reinforcements`
- **Ralplan**: `current_phase`

存储路径: `.omc/state/sessions/{sessionId}/{mode}-state.json`

> 引用: `scripts/keyword-detector.mjs:202-258` — `activateState()` 函数创建初始状态

#### Entity: Agent Role

定义于 `agents/*.md` 的 YAML frontmatter 中。

```
AgentRole {
  name: string          // e.g. "executor"
  description: string
  model: string         // e.g. "claude-sonnet-4-6"
  level: number         // 2-4
  disallowedTools?: string[]  // e.g. ["Write", "Edit"] for architect
}
```

19 个代理按 4 条车道组织：Build/Analysis、Review、Domain、Coordination。

> 引用: `agents/architect.md:1-7` — `disallowedTools: Write, Edit` 使架构代理为只读

#### Entity: Skill

定义于 `skills/*/SKILL.md` 的 YAML frontmatter 中。

```
Skill {
  name: string
  description: string
  argument-hint?: string
  level: number           // 2-4
  aliases?: string[]
  pipeline?: string[]     // e.g. [deep-interview, omc-plan, autopilot]
  next-skill?: string
  next-skill-args?: string
  handoff?: string        // output artifact path template
}
```

36 个技能目录，分为 Workflow、Agent Shortcuts、Utilities 三类。

> 引用: `skills/deep-interview/SKILL.md:1-9` — pipeline 元数据定义跨技能串联

#### Entity: Team Task

定义于 `skills/team/SKILL.md`，由 Claude Code 原生 TeamCreate/TaskCreate 工具管理。

```
TeamTask {
  id: string              // auto-incrementing string
  subject: string
  description: string
  activeForm: string
  owner: string           // worker name
  status: "pending" | "in_progress" | "completed" | "failed"
  blocks: string[]
  blockedBy: string[]
  metadata?: { _internal: boolean }
}
```

存储路径: `~/.claude/tasks/{team-name}/{id}.json`

> 引用: `skills/team/SKILL.md:284-306` — TaskCreate 请求/响应结构

#### Entity: PRD (Product Requirements Document)

Ralph 模式的核心驱动文件。

```
PRD {
  stories: UserStory[]
}

UserStory {
  id: string              // e.g. "US-001"
  title: string
  acceptanceCriteria: string[]
  passes: boolean
  priority: number
}
```

存储路径: `.omc/prd.json` 或项目根目录 `prd.json`

> 引用: `skills/ralph/SKILL.md:57-66` — PRD 脚手架生成与细化步骤

#### Entity: Deep Interview State

```
DeepInterviewState {
  interview_id: string
  type: "greenfield" | "brownfield"
  initial_idea: string
  rounds: Round[]
  current_ambiguity: float  // 0.0-1.0
  threshold: float          // default 0.2
  codebase_context: object | null
  challenge_modes_used: string[]
  ontology_snapshots: OntologySnapshot[]
}
```

> 引用: `skills/deep-interview/SKILL.md:74-91` — 初始化状态结构

### 2.2 实体生命周期

| 实体 | 创建 | 活跃 | 终止 |
|------|------|------|------|
| ModeState | keyword-detector hook 或 skill 显式调用 | Stop hook 反复阻断 + 递增计数器 | cancel skill 调用 `state_clear` |
| AgentRole | 静态定义于 `agents/*.md` | 被 Task tool 读取并注入 spawn_agent | 子代理完成后自动终止 |
| Skill | 用户输入匹配关键词或 `/skill` 调用 | PreToolUse 写入 `skill-active-state.json` | Stop hook 耗尽 reinforcement 配额后清除 |
| TeamTask | TeamCreate + TaskCreate 创建 | worker 领取 → in_progress | 完成/失败 → TeamDelete 清理 |
| PRD | Ralph 第一次迭代自动脚手架 | 逐 story 标记 passes:true | 所有 story 通过后进入验证 |

---

## 3. State Machine

### 3.1 Autopilot 管线状态机

```
                ┌──────────────────────────────────────────────┐
                │                                              │
                ▼                                              │
[Phase 0: Expansion] ──► [Phase 1: Planning] ──► [Phase 2: Execution]
     │                        │                       │
     │  ralplan 存在?         │  ralplan 存在?        │
     │  跳过 Phase 0+1 ──────┼──────────────────►    │
     │                        │                       ▼
     │  deep-interview 存在?  │              [Phase 3: QA Cycling]
     │  跳过 Phase 0 ────────┘                       │
     │                                                │ (max 5 cycles)
     │                                                ▼
     │                                       [Phase 4: Validation]
     │                                                │
     │                           ┌────────────────────┤
     │                           │ rejected           │ approved
     │                           ▼                    ▼
     │                     [Fix + Re-validate]  [Phase 5: Cleanup]
     │                                                │
     └────────────────────────────────────────────────┘
                        cancel
```

关键转换条件：
- Phase 0 → Phase 1: 规范文件 `.omc/autopilot/spec.md` 已生成
- Phase 1 → Phase 2: 计划文件 `.omc/plans/autopilot-impl.md` 已生成
- Phase 3 → Phase 4: 所有测试通过 (或同一错误重复 3 次则报告)
- Phase 4 → Phase 5: 所有审查者批准

> 引用: `skills/autopilot/SKILL.md:40-73`

### 3.2 Team 管线状态机

```
[team-plan] ──► [team-prd] ──► [team-exec] ──► [team-verify] ──► complete
                                     ▲               │
                                     │          fail  │
                                     │               ▼
                                     └───── [team-fix] ──► failed (max attempts)
```

阶段入口/出口条件：
- `team-plan` → `team-prd`: 任务图分解完成
- `team-prd` → `team-exec`: 验收标准明确
- `team-exec` → `team-verify`: 所有执行任务到达终态
- `team-verify` → `team-fix` | `complete`: 验证通过/失败
- `team-fix` → `team-exec`: 修复完成重新执行
- 超过 `max_fix_loops` → `failed`

终态: `complete`, `failed`, `cancelled`

每次阶段转换必须生成 Handoff 文档到 `.omc/handoffs/<stage-name>.md`。

> 引用: `skills/team/SKILL.md:93-191` 和 `AGENTS.md:252-266`

### 3.3 Ralph 持久循环状态机

```
[PRD Setup] ──► [Pick Story] ──► [Implement] ──► [Verify Story]
                     ▲                                │
                     │                    fail         │ pass
                     │               ◄────────────────┘
                     │                                │
                     │              all stories done   │
                     │                                ▼
                     │                    [Reviewer Verification]
                     │                          │
                     │              reject       │ approve
                     │         ◄────────────────┘
                     │                          ▼
                     │                    [Deslop Pass]
                     │                          │
                     │                          ▼
                     │                    [Regression Re-verify]
                     │                          │
                     │              fail         │ pass
                     │         ◄────────────────┘
                     │                          ▼
                     └──────────────────── [Cancel + Exit]
```

Stop hook 强制执行: `persistent-mode.cjs:700-738` — 每次 Claude 尝试停止时阻断并递增 iteration 计数器。

> 引用: `skills/ralph/SKILL.md:56-120`

### 3.4 Deep Interview 状态机

```
[Initialize] ──► [Interview Loop] ──► [Crystallize Spec] ──► [Execution Bridge]
                       │       ▲
                       │       │
                       │  score > threshold
                       │       │
                       ▼       │
              [Score Ambiguity]─┘
                       │
              [Challenge Agents]  (round 4: Contrarian, 6: Simplifier, 8: Ontologist)
```

门控条件: `ambiguity <= 0.2` (可配置)
硬性上限: 20 轮
提前退出: 第 3 轮起允许，附带警告

> 引用: `skills/deep-interview/SKILL.md:63-401`

---

## 4. Enforcement Audit

### Hard-enforced (代码级强制)

| 机制 | 实现位置 | 行为 |
|------|----------|------|
| **Stop hook 阻断** | `scripts/persistent-mode.cjs:700-738` | Ralph/Autopilot/Team 等活跃模式下，Stop 事件返回 `{decision: "block"}` 阻止 Claude 停止 |
| **关键词检测** | `scripts/keyword-detector.mjs:480-573` | UserPromptSubmit hook 匹配 14+ 关键词模式，注入 `[MAGIC KEYWORD: ...]` 到 system-reminder |
| **Stale state 超时** | `scripts/persistent-mode.cjs:143,179-192` | 2 小时无更新的状态自动判定为过期，不再阻断 |
| **Stop breaker 熔断器** | `scripts/persistent-mode.cjs:146-149` | Team: 最多 20 次阻断 (5 min TTL)；Ralplan: 最多 30 次 (45 min TTL) |
| **上下文限制免阻断** | `scripts/persistent-mode.cjs:519-544` | `isContextLimitStop()` 检测上下文窗口满时允许停止，防止死锁 |
| **Cancel signal 旁路** | `scripts/persistent-mode.cjs:282-319` | 30 秒 TTL 的取消信号文件让 Stop hook 立即放行 |
| **模型路由验证** | `scripts/pre-tool-enforcer.mjs:621-718` | forceInherit 模式下拒绝无效的 Bedrock/Vertex 模型 ID |
| **Team 路由强制** | `scripts/pre-tool-enforcer.mjs:317-325` | Team 活跃时不带 team_name 的 Task 调用被拒绝 |
| **Architect 只读** | `agents/architect.md:7` | `disallowedTools: Write, Edit` 硬性阻止写操作 |
| **Worker 递归防护** | `scripts/keyword-detector.mjs:455-458` | `OMC_TEAM_WORKER` 环境变量跳过关键词检测，防止无限生成 worker |
| **Skill protection** | `scripts/pre-tool-enforcer.mjs:367-401` | 各 skill 按轻/中/重三级写入 `skill-active-state.json`，Stop hook 按配额阻断 |

### Soft-enforced (提示词级约束)

| 机制 | 实现位置 | 行为 |
|------|----------|------|
| **PRD 细化要求** | `skills/ralph/SKILL.md:63-65` | `CRITICAL: Refine the scaffold` — 提示词强调替换通用验收标准 |
| **Ralplan-first 门控** | `AGENTS.md:183-186` | "Planning is complete only after both prd-*.md and test-spec-*.md exist" |
| **Verify before claim** | `AGENTS.md:289-298` | "Verify before claiming completion" — 按大小选择验证级别 |
| **Writer/Reviewer 分离** | `CLAUDE.md:62-63` | "Never self-approve in the same active context" |
| **并行执行策略** | `AGENTS.md:305-308` | "Run 2+ independent tasks in parallel when each takes >30s" |
| **Deep Interview 一问一答** | `skills/deep-interview/SKILL.md:40-41` | "Ask ONE question at a time" |
| **Executor 最小变更** | `agents/executor.md:35` | "Prefer the smallest viable change" |
| **Verifier 拒绝模糊词** | `agents/verifier.md:31` | "Reject immediately if: words like 'should/probably/seems to' used" |
| **Challenge agent 模式** | `skills/deep-interview/SKILL.md:240-254` | Contrarian (R4)、Simplifier (R6)、Ontologist (R8) 提示词注入 |
| **Team handoff 文档** | `skills/team/SKILL.md:152-174` | "Each completing stage MUST produce a handoff document" |
| **Commit protocol trailers** | `CLAUDE.md:68-95` | Constraint/Rejected/Directive/Confidence/Scope-risk trailers |

### Unenforced (声称但无强制)

| 机制 | 声称位置 | 为何未强制 |
|------|----------|-----------|
| **Handoff 文档生成** | `skills/team/SKILL.md:154` | 纯提示词要求 "MUST produce a handoff"，无 hook 验证是否实际生成 |
| **Task watchdog 超时** | `skills/team/SKILL.md:379-383` | 5 分钟/10 分钟超时是提示词建议，无定时器实现 |
| **PRD 验收标准具体性** | `skills/ralph/SKILL.md:63` | `CRITICAL` 标记但无自动检测通用标准的逻辑 |
| **Agent tier 选择** | `skills/ralph/SKILL.md:71-75` | 提示词建议 Haiku/Sonnet/Opus 分级，无运行时验证 |
| **Deep interview 数学分数** | `skills/deep-interview/SKILL.md:147-182` | 歧义分数由 LLM 自评，无独立验证机制 |
| **Visual verdict 循环** | `AGENTS.md:319-321` | "run $visual-verdict every iteration" 但无 hook 强制检查截图 |
| **3-failure escalation** | `agents/executor.md:40` | "After 3 failed attempts, escalate to architect" 纯提示词 |
| **Working agreements** | `AGENTS.md:36-45` | "Write a cleanup plan before modifying code" 等规范无强制执行 |

---

## 5. Prompt Catalog

### 5A. Key Prompts

#### P1: Persistent Mode Block Message

| 字段 | 值 |
|------|-----|
| **role** | Stop hook enforcer |
| **repo_path** | `scripts/persistent-mode.cjs:717` |
| **quote_excerpt** | `"[RALPH LOOP - ITERATION ${iteration + 1}/${maxIter}] Work is NOT done. Continue working."` |
| **stage** | Stop event handler |
| **design_intent** | 阻止 Claude 在任务完成前停止，注入迭代计数和原始任务提示 |
| **hidden_assumption** | LLM 会读取 `decision: "block"` 并继续工作而不是寻找退出路径 |
| **likely_failure_mode** | 无限循环：若任务不可完成，Claude 被困在反复阻断中直到 stale state 超时（2 小时） |

#### P2: Magic Keyword Injection

| 字段 | 值 |
|------|-----|
| **role** | UserPromptSubmit hook |
| **repo_path** | `scripts/keyword-detector.mjs:345-361` |
| **quote_excerpt** | `"[MAGIC KEYWORD: ${skillName.toUpperCase()}]\n\n${skillContent}\n\n---\nUser request:\n${originalPrompt}"` |
| **stage** | User input processing |
| **design_intent** | 将 SKILL.md 完整内容直接注入 system-reminder，无需 Skill tool 调用 |
| **hidden_assumption** | 完整 SKILL.md 内容 + 用户消息不会超出上下文窗口 |
| **likely_failure_mode** | 大型 SKILL.md（如 team 960 行）可能占用过多上下文 |

#### P3: Team Worker Preamble

| 字段 | 值 |
|------|-----|
| **role** | Team worker initialization |
| **repo_path** | `skills/team/SKILL.md:441-485` |
| **quote_excerpt** | `"You are a TEAM WORKER in team \"{team_name}\". ... NEVER spawn sub-agents or use the Task tool"` |
| **stage** | Worker spawn |
| **design_intent** | 限制 worker 只执行任务不做编排，防止递归生成 |
| **hidden_assumption** | Worker 会遵守 "NEVER" 规则而不尝试绕过 |
| **likely_failure_mode** | Worker 忽视约束，尝试使用 Task tool 导致资源浪费 |

#### P4: Verifier Evidence Requirement

| 字段 | 值 |
|------|-----|
| **role** | Verification agent |
| **repo_path** | `agents/verifier.md:31` |
| **quote_excerpt** | `"No approval without fresh evidence. Reject immediately if: words like 'should/probably/seems to' used, no fresh test output"` |
| **stage** | Post-implementation verification |
| **design_intent** | 强制验证必须基于新鲜证据，不接受假设性陈述 |
| **hidden_assumption** | Verifier 会在独立上下文中运行（非实现者自评） |
| **likely_failure_mode** | 上下文压缩后 verifier 丢失实现细节，给出空洞批准 |

#### P5: Deep Interview Ambiguity Scoring

| 字段 | 值 |
|------|-----|
| **role** | Requirements clarity gate |
| **repo_path** | `skills/deep-interview/SKILL.md:147-187` |
| **quote_excerpt** | `"Greenfield: ambiguity = 1 - (goal * 0.40 + constraints * 0.30 + criteria * 0.30)"` |
| **stage** | Interview loop scoring |
| **design_intent** | 量化歧义度，在 <= 20% 时才允许进入执行 |
| **hidden_assumption** | LLM 自评分数与人类评估者分数相关 |
| **likely_failure_mode** | LLM 膨胀评分以提前退出循环；ontology 稳定性计算因实体命名不一致而失真 |

#### P6: Executor Minimal Change Constraint

| 字段 | 值 |
|------|-----|
| **role** | Implementation agent |
| **repo_path** | `agents/executor.md:35-36` |
| **quote_excerpt** | `"Prefer the smallest viable change. Do not broaden scope beyond requested behavior."` |
| **stage** | Code implementation |
| **design_intent** | 防止执行代理过度工程化 |
| **hidden_assumption** | "smallest viable" 的判断在 LLM 能力范围内 |
| **likely_failure_mode** | Opus 模型倾向于重构，即使提示词要求最小变更 |

#### P7: Ralplan Gate Detection

| 字段 | 值 |
|------|-----|
| **role** | Pre-execution quality gate |
| **repo_path** | `skills/ralplan/SKILL.md:68-134` |
| **quote_excerpt** | `"Gate detects: execution keyword (ralph) + underspecified prompt (no files, functions, or test spec)"` |
| **stage** | Keyword detection → ralplan redirect |
| **design_intent** | 拦截模糊的执行请求，强制先规划 |
| **hidden_assumption** | 文件路径/函数名/issue 号的存在等价于请求足够具体 |
| **likely_failure_mode** | 用户说 "ralph fix src/auth" 通过门控，但 "fix src/auth" 可能仍然模糊 |

### 5B. Micro Design Highlights

#### M1: Informational Intent Filter

```javascript
// scripts/keyword-detector.mjs:167-179
const INFORMATIONAL_INTENT_PATTERNS = [
  /\b(?:what(?:'s|\s+is)|what\s+are|how\s+(?:to|do\s+i)\s+use|explain|...)\b/i,
  /(?:뭐야|뭔데|무엇(?:이야|인가요)?|어떻게|설명|...)/u,  // Korean
  /(?:とは|って何|使い方|説明)/u,  // Japanese
  /(?:什么是|什麼是|怎(?:么|樣)用|如何使用|解释|說明|说明)/u,  // Chinese
];
```

**设计亮点**: 关键词检测器在 80 字符窗口内检查是否为信息查询（"what is ralph"），避免误触发执行技能。支持韩/日/中/英四语种。这是精细化的意图消歧义。

> 引用: `scripts/keyword-detector.mjs:167-199`

#### M2: Awaiting Confirmation TTL

```javascript
// scripts/persistent-mode.cjs:211-233
const AWAITING_CONFIRMATION_TTL_MS = 2 * 60 * 1000;

function isAwaitingConfirmation(state) {
  if (!state || state.awaiting_confirmation !== true) return false;
  const setAt = state.awaiting_confirmation_set_at || state.started_at || null;
  // ...
  return Date.now() - setAtMs < AWAITING_CONFIRMATION_TTL_MS;
}
```

**设计亮点**: 状态创建时设置 `awaiting_confirmation: true`（2 分钟 TTL），在此期间 Stop hook 不阻断。这解决了一个时序问题——关键词检测器先写入状态文件，但 skill 内容可能几秒后才被 LLM 处理。若 LLM 在阅读 skill 前就尝试停止，TTL 机制避免了虚假阻断。

> 引用: `scripts/persistent-mode.cjs:211-233`

#### M3: Cancel Signal Expiration

```javascript
// scripts/persistent-mode.cjs:282-306
function isSessionCancelInProgress(stateDir, sessionId) {
  const CANCEL_SIGNAL_TTL_MS = 30000; // 30 seconds
  // ...writes cancel-signal-state.json with expires_at
}
```

**设计亮点**: Cancel 操作写入一个 30 秒 TTL 的信号文件。Stop hook 检测到此信号后立即放行。这解决了取消与持久模式之间的竞态——如果取消 skill 正在清理状态文件但 Stop hook 先触发，它会看到活跃状态并阻断，导致取消失败。信号文件充当短暂的"通行证"。

> 引用: `scripts/persistent-mode.cjs:282-319`

#### M4: Sanitize Before Keyword Detection

```javascript
// scripts/keyword-detector.mjs:150-165
function sanitizeForKeywordDetection(text) {
  return text
    .replace(/<(\w[\w-]*)[\s>][\s\S]*?<\/\1>/g, '')  // Strip XML tags
    .replace(/https?:\/\/[^\s)>\]]+/g, '')             // Strip URLs
    .replace(/(?<=^|[\s"'`(])(?:\/)?(?:[\w.-]+\/)+[\w.-]+/gm, '')  // Strip paths
    .replace(/```[\s\S]*?```/g, '')                     // Strip code blocks
    .replace(/`[^`]+`/g, '');                           // Strip inline code
}
```

**设计亮点**: 在关键词匹配前剥离 XML 标签、URL、文件路径和代码块。这防止了诸如代码块中的 `autopilot` 变量名或 URL 中的 `team` 片段触发误报。

> 引用: `scripts/keyword-detector.mjs:150-165`

### 5C. Macro Design Highlights

#### MA1: 三层技能组合架构

```
┌─ GUARANTEE LAYER (optional) ─────────────────┐
│  ralph: "Cannot stop until verified done"     │
└───────────────────────────────────────────────┘
                    │
┌─ ENHANCEMENT LAYER (0-N) ────────────────────┐
│  ultrawork | git-master | frontend-ui-ux      │
└───────────────────────────────────────────────┘
                    │
┌─ EXECUTION LAYER (primary) ──────────────────┐
│  default (build) | orchestrate | planner      │
└───────────────────────────────────────────────┘
```

**设计亮点**: 技能不是互斥的——它们按层组合。Execution 层选择做什么，Enhancement 层选择怎么做（并行/提交策略等），Guarantee 层确保完成。这意味着 `ralph + ultrawork + git-master` 是 "持久循环 + 并行执行 + 原子提交" 的叠加。

模式嵌套关系:
```
autopilot
  └── ralph (persistence)
        └── ultrawork (parallelism)
```

> 引用: `docs/ARCHITECTURE.md:183-211`

#### MA2: 三阶段质量管线 (Deep Interview → Ralplan → Autopilot)

```
Stage 1: Deep Interview        Stage 2: Ralplan           Stage 3: Autopilot
  Gate: clarity (≤20%)           Gate: feasibility          Gate: correctness
  Output: spec.md                Output: consensus-plan     Output: working code
```

**设计亮点**: 三阶段中每个阶段可独立运行，但串联时形成递进式质量门控。关键设计——autopilot 检测到 ralplan 产物后自动跳过 Phase 0+1，避免重复工作。这是一种声明式管线：下游根据上游产物的存在性自动调整入口点。

> 引用: `skills/deep-interview/SKILL.md:380-399` 和 `skills/autopilot/SKILL.md:41-42`

#### MA3: Hook 驱动的全生命周期拦截

OMC 注册了 11 个 Claude Code 生命周期事件中的 10 个:

| 事件 | Hook 数量 | 用途 |
|------|-----------|------|
| UserPromptSubmit | 2 | 关键词检测 + 技能注入 |
| SessionStart | 3 | 初始化 + 项目记忆 + wiki |
| PreToolUse | 1 | 上下文注入 + 模型路由验证 |
| PermissionRequest | 1 | Bash 权限处理 |
| PostToolUse | 2 | 结果验证 + 项目记忆更新 |
| PostToolUseFailure | 1 | 错误恢复 |
| SubagentStart | 1 | 代理追踪 |
| SubagentStop | 2 | 代理追踪 + 交付物验证 |
| PreCompact | 3 | 信息保存 + 项目记忆 + wiki |
| Stop | 3 | 上下文警戒 + 持久模式 + 代码简化 |
| SessionEnd | 2 | 会话数据清理 + wiki |

**设计亮点**: 最关键的创新是 Stop hook (`persistent-mode.cjs`) 的"阻断"能力——它返回 `{decision: "block", reason: "..."}` 直接阻止 Claude 停止执行。这是 OMC "不停止直到完成" 承诺的硬件基础。与之配合的是 stale state 超时（2 小时）和 circuit breaker（20 次上限）作为安全阀。

> 引用: `hooks/hooks.json` 和 `docs/ARCHITECTURE.md:322-388`

#### MA4: 混合团队架构 (Claude + Codex + Gemini)

Team skill 支持三种 worker 类型：
- **Claude worker**: 完整 Claude Code 工具访问，参与团队通信
- **Codex worker**: tmux 窗格中的 Codex CLI，自主一次性执行
- **Gemini worker**: tmux 窗格中的 Gemini CLI，自主一次性执行

Lead 通过不同协议管理不同 worker：
- Claude: SendMessage / TaskUpdate
- CLI (Codex/Gemini): prompt_file → spawn → output_file

**设计亮点**: 异构代理编排——不同 AI 系统通过统一的 Lead 协调，每种 worker 有独立的通信协议和能力边界。Claude worker 是持久化参与者，CLI worker 是一次性任务执行器。

> 引用: `skills/team/SKILL.md:590-646`

---

## 6. Failure Modes

### F1: Stop Hook 死循环

**证据**: `persistent-mode.cjs:726-738` — 当 Ralph 达到 max_iterations 时，代码不是终止而是自动扩展 10 轮继续：
```javascript
ralph.state.max_iterations = maxIter + 10;
ralph.state.iteration = maxIter + 1;
```

**触发条件**: 任务不可完成（缺少凭证、外部服务不可用、需求矛盾）
**缓解**: Stale state 2 小时超时；用户可发送 "cancelomc"；但若用户不在，系统可能运行 2 小时消耗 token。

### F2: 上下文窗口溢出

**证据**: `keyword-detector.mjs:345-350` — 完整 SKILL.md 内容注入 system-reminder：
```javascript
return `[MAGIC KEYWORD: ...]\n\n${skillContent}\n\n---\nUser request:\n${originalPrompt}`;
```

**触发条件**: 大型 SKILL.md（如 `team/SKILL.md` 约 970 行）+ 长用户提示 + 已有对话历史
**缓解**: `context-guard-stop.mjs` 在 Stop 时检查上下文使用率，`isContextLimitStop()` 在上下文满时放行停止。但注入发生在 UserPromptSubmit 阶段，此时上下文已经增长。

### F3: 团队 Worker 竞态条件

**证据**: `skills/team/SKILL.md:951` — 明确承认：
> "No atomic claiming — Unlike SQLite swarm, there is no transactional guarantee on TaskUpdate."

**触发条件**: Lead 未预分配 owner，两个 worker 同时 claim 同一任务
**缓解**: 提示词要求 lead 预分配 owner，但这是 soft-enforced。

### F4: Deep Interview 分数膨胀

**证据**: `skills/deep-interview/SKILL.md:147-182` — LLM 自评所有维度分数
**触发条件**: LLM 倾向于给出乐观分数以提前退出循环，特别是在用户表达不耐烦时
**缓解**: 使用 Opus + temperature 0.1 减少变异，但无独立评分者交叉验证。Ontology stability 追踪提供了间接信号但不够强。

### F5: 取消操作复杂度级联

**证据**: `skills/cancel/SKILL.md:109-121` — 11 种模式的取消优先级链：
```
1. Autopilot → ralph → ultraqa
2. Ralph → ultrawork
3-11. ...standalone modes
```

**触发条件**: 嵌套模式（Team + Ralph + Ultrawork）取消时的级联清理
**缓解**: 依赖顺序取消 + `--force` 强制清除 + bash fallback 紧急逃生。但 `--force` 对 autopilot 和 omc-teams 有特殊限制。

### F6: Handoff 文档丢失

**证据**: `skills/team/SKILL.md:152-174` — "Each completing stage MUST produce a handoff document"

**触发条件**: 上下文压缩丢失 lead 的对话历史，且 handoff 文档未被生成
**缓解**: Handoff 是 soft-enforced。`.omc/handoffs/` 目录在取消时保留，但若从未写入则恢复无从谈起。

### F7: Session ID 跨会话污染

**证据**: `persistent-mode.cjs:340-348` — session match 逻辑：
```javascript
function isSessionMatch(state, sessionId) {
  if (sessionId) return state.session_id === sessionId;
  return !state.session_id;  // 无 sessionId 时匹配无 sessionId 的状态
}
```

**触发条件**: 旧版无 sessionId 的状态文件与新会话交互
**缓解**: 严格的 session 匹配 + stale state 超时。但遗留路径 fallback 增加了复杂度。

---

## 7. Migration Assessment

### M1: Stop Hook 持久模式

| 维度 | 评价 |
|------|------|
| **Transferability** | HIGH — 机制通用：读状态文件 → 返回 block/continue |
| **Effort** | Medium — 需要实现 hooks.json 注册 + persistent-mode 脚本 + 状态文件管理 |
| **Prerequisite** | Claude Code hooks API（Stop 事件 + `decision: "block"` 返回值） |
| **Risk** | Medium — 死循环风险需要 stale state 超时 + circuit breaker 双重安全阀 |

**推荐**: 值得移植。核心创新是 `decision: "block"` 阻断机制。关键保护措施：stale state 2h 超时 + stop breaker 计数上限 + 上下文限制放行 + 用户中断放行。

### M2: 关键词检测与技能注入

| 维度 | 评价 |
|------|------|
| **Transferability** | HIGH — 模式可复用：正则匹配 → system-reminder 注入 |
| **Effort** | Low — 已有成熟参考实现 |
| **Prerequisite** | UserPromptSubmit hook + hookSpecificOutput.additionalContext |
| **Risk** | Low — 最大风险是误触发，已通过 sanitize + informational intent filter 缓解 |

**推荐**: 强烈推荐移植。四语种意图过滤器和 sanitize 函数是精心调优的产物。

### M3: 三阶段质量管线

| 维度 | 评价 |
|------|------|
| **Transferability** | MEDIUM — 概念可复用但 deep-interview 的数学评分机制依赖 LLM 自评 |
| **Effort** | High — 三个独立 skill + 产物检测逻辑 + 管线串联 |
| **Prerequisite** | Skill tool + 文件系统状态持久化 |
| **Risk** | Medium — 歧义分数可靠性未经验证；管线复杂度高 |

**推荐**: 选择性移植。Deep Interview 的苏格拉底问答框架和 ontology tracking 是独特创新。但数学评分机制的实际可靠性存疑——建议简化为二元门控（通过/需要更多信息）。

### M4: Team 协调架构

| 维度 | 评价 |
|------|------|
| **Transferability** | LOW — 深度依赖 Claude Code 原生 Team API (TeamCreate/TaskCreate/SendMessage) |
| **Effort** | Very High — 最大的 skill（970 行），包含 7 个阶段 + 通信协议 + 错误处理 |
| **Prerequisite** | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` feature flag + tmux (CLI workers) |
| **Risk** | High — 竞态条件、orphan 进程、shutdown 超时 |

**推荐**: 不建议直接移植。概念（staged pipeline + handoff docs + agent routing table）可借鉴，但实现过于耦合原生 API。

### M5: Writer/Reviewer 分离模式

| 维度 | 评价 |
|------|------|
| **Transferability** | HIGH — 纯提示词模式，与框架无关 |
| **Effort** | Low — 在代理提示词中添加角色约束即可 |
| **Prerequisite** | 支持子代理/独立上下文的运行时 |
| **Risk** | Low |

**推荐**: 立即可移植。Verifier 的 "reject immediately if 'should/probably/seems to'" 规则和 Architect 的 `disallowedTools: Write, Edit` 是简洁有效的设计。

### M6: 项目记忆系统

| 维度 | 评价 |
|------|------|
| **Transferability** | MEDIUM — MCP 工具依赖 (notepad_*, project_memory_*) |
| **Effort** | Medium — MCP server + 3 个生命周期 hook (SessionStart, PostToolUse, PreCompact) |
| **Prerequisite** | MCP server 支持 + PreCompact hook |
| **Risk** | Low — 辅助功能，不影响核心执行 |

**推荐**: 有价值但优先级次于 M1/M2。`<remember priority>` 永久标签和 PreCompact 保存机制解决了上下文压缩丢失信息的实际痛点。

### M7: Commit Protocol Trailers

| 维度 | 评价 |
|------|------|
| **Transferability** | HIGH — 纯提示词模式 |
| **Effort** | Low — 在系统提示中添加 trailer 格式规范 |
| **Prerequisite** | 无 |
| **Risk** | Low |

**推荐**: 立即可移植。`Constraint:`, `Rejected:`, `Directive:`, `Not-tested:` 等 trailer 在 commit 中保留决策上下文，对长期维护有实际价值。

---

## 8. Summary

### 核心创新

1. **Stop hook 阻断机制**: 通过 `{decision: "block"}` 返回值硬性阻止 Claude 停止——这是整个 "持久模式" 承诺的技术基础。配合 stale state 超时和 circuit breaker 防止失控。

2. **技能组合层架构**: Guarantee + Enhancement + Execution 三层叠加，使模式可以自由组合（如 ralph + ultrawork + git-master）而非互斥。

3. **声明式管线串联**: 下游 skill 根据上游产物文件的存在性自动调整入口点（如 autopilot 检测到 ralplan 产物自动跳过前两阶段），实现松耦合。

4. **苏格拉底式歧义量化**: Deep Interview 用加权维度评分 + ontology 稳定性追踪将"需求是否清楚"量化为数值，虽然自评可靠性有限，但框架本身是独特的。

### 主要弱点

1. **Soft enforcement 占比过高**: 大量关键行为（handoff 生成、PRD 具体性、agent tier 选择）仅靠提示词约束，无运行时验证。

2. **复杂度集中在 Stop hook**: `persistent-mode.cjs`（1144 行）承担了 9 种模式的持久性强制，是单点故障——任何 bug 都可能导致无限循环或提前终止。

3. **状态管理路径碎片化**: Session-scoped + legacy path + global path 三层 fallback，加上 OMC_STATE_DIR 集中存储选项，使状态查找逻辑异常复杂。

4. **Self-scoring 无交叉验证**: Deep Interview 的歧义分数和 Verifier 的批准决策都由 LLM 自评，缺乏独立验证机制。

---

## 附录：Gemini Deepdive 补充信息

> 来源：`1st-cc-plugin/workflows/loaf/docs/gemini-roadmap-review/deepdive-omc.md`
> 补充内容：统一 CLI 引擎、状态管理原子性、扩展性机制的具体实现，主报告中未覆盖到的代码级细节。

### A.1 Unified CLI Engine 实现

OMC 通过 `src/cli/index.ts` + `commander` 框架实现统一 CLI 入口：

- **子命令模块化**：每个子命令（`setup`, `team`, `doctor`, `autoresearch`）委托给 `src/cli/commands/` 下的独立文件
- **Fallback / Pass-through**：`defaultAction` 中，若无命令匹配，解析所有参数传递给 `launchCommand`，使 `omc --madmax` 等同 `claude --madmax`
- **Option 验证**：Handler 将 CLI flags（`options.json`、`options.force`）解析为强类型对象后才调用业务逻辑

### A.2 状态管理的原子性保障

OMC 通过精细的状态隔离防止并发损坏：

- **Session 隔离**：每个 CLI 进程生成唯一 `pid-{PID}-{startTimestamp}` 标识符，数据存储在 `.omc/state/sessions/{sessionId}/`
- **`_meta` 信封**：所有状态文件使用保护性信封包装：
  ```json
  {
    "iteration": 1,
    "active": true,
    "_meta": {
      "written_at": "2024-05-19T10:00:00Z",
      "sessionId": "pid-1234-1707350400000"
    }
  }
  ```
- **原子写入**：`atomicWriteJsonSync` 先写入 `.tmp` 文件，再通过 `fs.renameSync` 替换目标文件，确保进程崩溃时文件不会半写。核心实现在 `src/lib/mode-state-io.ts` 和 `src/lib/worktree-paths.ts`

### A.3 Extensibility 机制

- **Manifest-Driven Skills**：Agent prompts 和 capabilities 作为 Markdown 配置存储在 `skills/` 和 `agents/` 目录
- **Setup 同步**：`omc setup`（`src/installer/index.ts`）充当安装器，将定义同步到 `~/.claude/skills/`，让 Claude Code 原生发现
- **Hook 脚本**：OMC 在 `.claude/hooks/` 中放置 `.mjs` 文件（如 `pre-tool-use.mjs`、`session-start.mjs`），修改 `settings.json` 使 Claude Code 在触发事件时执行
- **Plugin 目录模式**：检测 `CLAUDE_PLUGIN_ROOT` 环境变量时，OMC 作为 Claude Code 插件运行，跳过文件复制，直接接入宿主运行时上下文
