# Workflow Research: ccg-workflow

> 逆向工程报告，目标：[fengshao1227/ccg-workflow](https://github.com/fengshao1227/ccg-workflow) v1.8.0
> 生成日期：2026-04-03

---

## 1. 框架概览

| Field | Value |
|-------|-------|
| **Name** | CCG — Claude + Codex + Gemini 多模型协作 |
| **Version** | v1.8.0 (npm `ccg-workflow`) |
| **Type** | 多模型编排框架 + CLI 安装器 |
| **License** | MIT |
| **Language** | TypeScript（CLI 安装器）+ Go（codeagent-wrapper 二进制） |
| **Runtime** | Node.js 20+（安装器）、Go stdlib（wrapper） |
| **Framework** | cac（CLI）+ inquirer（交互式）+ unbuild（构建） |
| **Size** | 216 个文件，约 27 个斜杠命令，13 个专家 prompt，6 个 skill，4 个 agent |
| **Architecture** | Claude = 编排器；Codex = 后端 worker；Gemini = 前端 worker |
| **Install mechanism** | `npx ccg-workflow` 将模板复制到 `~/.claude/{commands,agents,skills,rules}/ccg/` + 二进制到 `~/.claude/bin/` |
| **Core innovation** | Go 二进制（`codeagent-wrapper`）作为外部 CLI 后端的进程级代理 |

**框架类型假设已确认**：混合型 — CLI 安装器（TypeScript）+ 进程级代理（Go 二进制）+ Prompt 驱动编排（Markdown 模板）。该"框架"本质上是 **process-as-prose**：工作流逻辑存在于注入 Claude 上下文的 Markdown prompt 文件中，而非程序化代码。

---

## 2. 源文件清单

### 概览

| File | Role |
|------|------|
| `README.md` | 面向用户的文档，命令表，架构图 |
| `CLAUDE.md` | Claude Code 会话的项目指令 — 变更日志、模块职责、发布规则 |
| `CONTRIBUTING.md` | 贡献指南 |
| `docs/` | VitePress 文档站点（中英文指南页面） |

### 执行层（commands, agents, prompts, skills）

| Category | Count | Path | Description |
|----------|-------|------|-------------|
| **Slash commands** | 27 | `templates/commands/*.md` | 安装到 `~/.claude/commands/ccg/` 的核心工作流模板 |
| **Sub-agents** | 4 | `templates/commands/agents/*.md` | planner, ui-ux-designer, init-architect, get-current-datetime |
| **Codex prompts** | 6 | `templates/prompts/codex/` | analyzer, architect, debugger, optimizer, reviewer, tester |
| **Gemini prompts** | 7 | `templates/prompts/gemini/` | analyzer, architect, debugger, frontend, optimizer, reviewer, tester |
| **Claude prompts** | 6 | `templates/prompts/claude/` | analyzer, architect, debugger, optimizer, reviewer, tester |
| **Skills** | 6+1 | `templates/skills/` | verify-security, verify-quality, verify-change, verify-module, gen-docs, multi-agent + 根级 SKILL.md |
| **OpenSpec skills** | 10 | `.agents/skills/openspec-*` | 用于规范驱动开发的 OPSX 集成 |
| **Output styles** | 5 | `templates/output-styles/` | 人格主题输出风格（abyss-cultivator, engineer-professional 等） |
| **Rules** | 1 | `templates/rules/ccg-skills.md` | 注入到 `~/.claude/rules/` 的质量门自动触发规则 |

### 强制执行层

| File | Role | Type |
|------|------|------|
| `src/utils/installer.ts` | 模板复制 + 变量注入 + 二进制下载 | Hard（失败即退出） |
| `src/utils/installer-template.ts` | `{{WORKDIR}}`、`{{MCP_SEARCH_TOOL}}`、`{{LITE_MODE_FLAG}}` 变量替换 | Hard |
| `codeagent-wrapper/main.go` | Codex/Gemini/Claude CLI 后端的进程级代理 | Hard（退出码） |
| `codeagent-wrapper/backend.go` | Backend 接口 + codex/gemini/claude 参数构建 | Hard |
| `codeagent-wrapper/executor.go` | 基于拓扑排序的并发任务执行 + 依赖跳过 | Hard |
| `.github/workflows/ci.yml` | TypeScript lint + 类型检查 + 测试 + 构建；Go 构建 + 测试 | Hard（CI 门禁） |
| `.github/workflows/build-binaries.yml` | Go 二进制交叉编译 + 上传至 GitHub Release + R2 镜像 | Hard |
| `templates/rules/ccg-skills.md` | 作为 Claude rules 注入的质量门触发规则 | Soft（仅 prompt） |

### 演进层

| File | Role |
|------|------|
| `CHANGELOG.md` | 完整版本历史 |
| `.github/ISSUE_TEMPLATE/` | bug_report, feature_request, good_first_issue 模板 |
| `.github/pull_request_template.md` | PR 模板 |
| `src/utils/__tests__/` | 6 个测试文件（config, injectConfigVariables, installWorkflows, installer, platform, version） |
| `codeagent-wrapper/*_test.go` | 14 个 Go 测试文件（backend, bench, concurrent_stress, executor_concurrent, filter, logger, main, parser, process_check, path_normalization, wrapper_name, utils, log_writer_limit, logger_additional_coverage） |

---

## 3. 对象模型与上下文策略

### 一等实体

| Entity | Definition location | Required fields | Lifecycle |
|--------|-------------------|-----------------|-----------|
| **Command**（斜杠命令） | `templates/commands/<name>.md` — YAML frontmatter `description` | description, body with `$ARGUMENTS` | 安装时创建 → 注入配置变量 → 复制到 `~/.claude/commands/ccg/` → 用户通过 `/ccg:<name>` 调用 |
| **Agent**（子 agent） | `templates/commands/agents/<name>.md` | YAML frontmatter | 安装时创建 → 复制到 `~/.claude/agents/ccg/` → 工作流阶段中由 Claude 生成 |
| **Prompt**（专家角色） | `templates/prompts/{codex,gemini,claude}/<role>.md` | 角色描述、约束、检查清单 | 安装时创建 → 复制到 `~/.claude/.ccg/prompts/` → 在 codeagent-wrapper 调用中通过 `ROLE_FILE:` 指令注入 |
| **Skill** | `templates/skills/**/SKILL.md` — YAML frontmatter | name, description, allowed-tools | 安装时创建 → 复制到 `~/.claude/skills/ccg/` → 按规则自动触发或手动调用 |
| **Rule** | `templates/rules/ccg-skills.md` | 触发条件 | 安装时创建 → 复制到 `~/.claude/rules/` → 始终加载到 Claude 上下文 |
| **Backend** | `codeagent-wrapper/backend.go` — Go interface | Name(), Command(), BuildArgs() | 运行时通过 `--backend` 标志选择 → 构建 CLI 参数 → 生成子进程 |
| **TaskSpec** | `codeagent-wrapper/executor.go` | ID, Task, Backend, Dependencies | 由并行模式配置创建 → 拓扑排序 → 并发执行 |
| **InstallConfig** | `src/utils/installer.ts:59-68` | routing, liteMode, mcpProvider | 初始化时创建 → 驱动模板变量注入 |

### 实体关系

```
Command ──references──> Prompt (via ROLE_FILE path)
Command ──calls──> codeagent-wrapper (via Bash tool)
Command ──may trigger──> Skill (via rules)
Skill ──chains to──> Skill (verify-module → verify-security)
Backend <──selected by──> codeagent-wrapper (via --backend flag)
TaskSpec ──depends on──> TaskSpec (via Dependencies array)
Agent ──spawned by──> Command (during workflow phases)
```

### 上下文流转策略

**上下文隔离模型**：Claude = 拥有完整上下文的编排器；Codex/Gemini = 在隔离沙箱中的 worker。

| Flow | Mechanism | Evidence |
|------|-----------|----------|
| Controller → Worker | 任务文本通过 stdin 管道传入 `codeagent-wrapper` → Codex/Gemini CLI | `executor.go:1133-1139` |
| Worker → Controller | stdout JSON 流由 `codeagent-wrapper` 解析 → 聚合消息返回给 Claude | `executor.go:1089-1110` |
| Cross-phase state | wrapper 返回 `SESSION_ID` → 后续调用通过 `resume <SESSION_ID>` 复用 | `workflow.md:86-87`, `plan.md:57` |
| Plan persistence | 计划保存到 `.claude/plan/<name>.md` → 由 `/ccg:execute` 或 `/ccg:codex-exec` 读取 | `plan.md:196-197` |
| Context persistence | `.context/` 目录存储项目偏好、编码风格、提交历史 | `CLAUDE.md:70-73` |
| Token budget | 无显式 token 计数；依赖命令模板大小（每个约 1-3k tokens）+ prompt 大小（每个约 200-500 tokens） | 未发现强制执行机制 |

### 对象分类

| Object | Type | Rationale |
|--------|------|-----------|
| 计划文件（`.claude/plan/*.md`） | **Fact object** | 执行的输入数据 |
| Codex/Gemini 原始输出 | **Evidence object** | 需要重构的"脏原型" |
| 评审评分报告 | **Judgment object** | 包含 PASS/NEEDS_IMPROVEMENT 的评审结论 |
| 质量门报告 | **Judgment object** | 安全/质量扫描结果 |
| SESSION_ID | **Evidence object** | 用于会话连续性的执行凭证 |

---

## 4. 流程与状态机

### 主流程：`/ccg:workflow`（6 阶段）

```
[研究] ──gate(score≥7)──> [构思] ──user-confirm──> [计划] ──user-confirm──> [执行] ──> [优化] ──> [评审]
  │                          │                        │                       │          │          │
  │ Prompt enhancement       │ Codex∥Gemini           │ Codex∥Gemini          │ Claude   │ Codex∥   │ Final
  │ MCP search               │ parallel analysis      │ parallel planning     │ writes   │ Gemini   │ check
  │ Completeness score       │ Cross-validate          │ Save to plan file     │ code     │ review   │
  │                          │ User selects option     │ User approves          │          │          │
  ↓                          ↓                        ↓                       ↓          ↓          ↓
  score<7 → STOP           Wait for both models     Plan → .claude/plan/    Implement  Optimize   Deliver
```

**阶段转换**：每个阶段以 `AskUserQuestion` 的用户确认结束。评分 < 7 或用户拒绝 → 强制停止。（`workflow.md:107-111`）

### Plan → Execute 分离流程

```
/ccg:plan ────────> .claude/plan/<name>.md
                          │
                ┌─────────┼─────────┐
                ↓                   ↓
         /ccg:execute        /ccg:codex-exec
         (Claude refactors)  (Codex implements)
                │                   │
                ↓                   ↓
         Phase 3: Prototype   Phase 1: Codex executes
         Phase 4: Claude impl Phase 2: Claude reviews
         Phase 5: Audit       Phase 3: Multi-model audit
                │                   │
                └─────────┬─────────┘
                          ↓
                    Multi-model review
                    (Codex ∥ Gemini)
```

### Agent Teams 流程

```
/ccg:team-research → constraints file
     ↓ /clear
/ccg:team-plan → .claude/team-plan/<name>.md (subtask decomposition)
     ↓ /clear
/ccg:team-exec → TeamCreate → spawn Builders → parallel execution → collect results
     ↓ /clear
/ccg:team-review → Codex ∥ Gemini cross-review
```

**codeagent-wrapper 中的关键状态转换**：

```
parseArgs() → selectBackend() → buildArgs() → Start() → [stdin pipe] → parseJSONStream()
     │                                                          │
     │ Parallel mode:                                           │
     │ parseParallelConfig() → topologicalSort()                │
     │ → executeConcurrent() → [layer-by-layer]                 │
     │                                                          ↓
     │                                              messageSeen / completeSeen
     │                                              → postMessageDelay → terminate
     ↓
Exit: 0=success, 1=error, 124=timeout, 127=not-found, 130=interrupted
```

### 失败路径

**失败路径 1：外部模型超时**
- `codeagent-wrapper` 默认超时 2 小时（`defaultTimeout = 7200`）
- Claude 模板指定 `TaskOutput(timeout: 600000)`（10 分钟）然后轮询
- 模板**禁止**杀死 Codex 进程；要求通过 `AskUserQuestion` 让用户确认
- 依据：`workflow.md:97-101`

**失败路径 2：Gemini 调用失败**
- 模板要求重试：最多 2 次重试，间隔 5 秒
- 仅在总共 3 次失败后：降级为单模型模式
- 依据：`workflow.md:100`，在 20 个命令模板中重复出现（`CLAUDE.md:45`）

**失败路径 3：并行任务依赖失败**
- `executor.go:527-544`：`shouldSkipTask()` 检查是否有依赖失败 → 跳过并报错
- 逐层执行：失败的任务会传播到下游依赖
- 依据：`executor.go:436-440`

---

## 5. 强制执行审计

### 强制执行矩阵

| Constraint | Claimed in | Enforcement level | Evidence |
|-----------|------------|-------------------|----------|
| **外部模型零写入权限** | `workflow.md:192`, `plan.md:15`, `execute.md:14` | **Soft** — 仅 prompt 指令。codeagent-wrapper 并未限制 Codex/Gemini 的文件访问。Codex 以 `--dangerously-bypass-approvals-and-sandbox` 运行（`executor.go:777`）。 | README 中的"Security by design"声明**是修辞，非代码强制**。 |
| **阶段顺序不可跳过** | `workflow.md:190` | **Soft** — 仅 prompt 指令。无代码阻止阶段跳过。 | 无验证器检查阶段序列。 |
| **评分 < 7 强制停止** | `workflow.md:191` | **Soft** — 仅 prompt 指令。无 hook 或验证器。 | 评分由 Claude 自身生成和评估。 |
| **必须等待 Codex 结果** | `workflow.md:101` | **Soft** — 仅 prompt 指令。在 20 个模板中以粗体 + 禁止 emoji 强调。 | 无技术机制阻止 Claude 继续执行。 |
| **质量门自动触发** | `ccg-skills.md`（rules 文件） | **Soft** — rules 文件加载到 Claude 上下文中；触发器是基于 prompt 的"should"而非"must"。 | `ccg-skills.md:53`："Non-blocking — Quality gates produce reports but do NOT block delivery unless Critical issues are found" |
| **二进制版本匹配** | `installer.ts:53`, `main.go:17` | **Hard** — 安装器检查 `EXPECTED_BINARY_VERSION` 与已安装二进制的 `--version` 输出；不匹配则触发重新下载。 | `installer.ts:473-483` |
| **CI 类型检查 + 测试 + 构建** | `.github/workflows/ci.yml` | **Hard** — PR/push 到 main 触发 Node 20/22 矩阵测试 + Go 构建 + Go 测试。 | `ci.yml:1-54` |
| **模板变量注入** | `installer-template.ts` | **Hard** — `injectConfigVariables()` 在安装时替换 `{{WORKDIR}}`、`{{MCP_SEARCH_TOOL}}` 等。 | `installer.ts:191-192` |
| **codeagent-wrapper 退出码** | `main.go:581-587` | **Hard** — 结构化退出码（0/1/124/127/130）传播到 Claude。 | `main.go:581-587`, `executor.go:1270-1280` |
| **并行任务依赖强制** | `executor.go:287-351` | **Hard** — 带环检测的拓扑排序；依赖失败 → 跳过下游。 | `executor.go:339-347` |
| **Skills 命名空间隔离** | `installer.ts:344-375` | **Hard** — skill 安装到 `skills/ccg/` 子目录；卸载仅移除 `skills/ccg/`，保留用户 skill。 | `installer.ts:736-746` |
| **自动授权 hook** | `README.md:257-282` | **Hard** — PreToolUse hook 通过 `jq` 脚本自动批准 `codeagent-wrapper` Bash 命令。同时：`permissions.allow` 中的 `Bash(*codeagent-wrapper*)` 模式。 | `CLAUDE.md:36-38` |
| **Plan-only 模式：禁止写代码** | `plan.md:17`, `plan.md:215-219` | **Soft** — prompt 指令："禁止修改产品代码"，"绝对禁止对产品代码进行任何写操作"。无 hook 阻止写入。 | 无 `PostToolUse` hook 验证此约束。 |
| **Agent Teams 文件所有权** | `team-exec.md:14`, `multi-agent/SKILL.md:379-389` | **Soft** — 给 Builder 的 prompt 指令："严禁修改任何其他文件"。无技术强制。 | Builder 作为标准 Claude agent 运行，拥有完整文件访问权限。 |

### 关键强制执行缺口

**最关键的缺口**：README 声称"Security by design — External models have no write access"，但实际上：

1. Codex 以 `--dangerously-bypass-approvals-and-sandbox` 调用（`executor.go:777`）
2. Gemini 以 `-y`（自动批准）调用（`backend.go:133`）
3. Claude 后端禁用所有设置源：`--setting-sources ""`（`backend.go:96`）
4. "零写入"约束仅作为命令模板中的 prompt 文本存在

这**充其量是 Soft 强制** — 外部模型确实能写入文件；prompt 只是指示 Claude 将其输出视为"脏原型"并由自己应用更改。更诚实的表述应为："Claude 在应用外部模型建议前进行审查"，而非"外部模型无写入权限"。

---

## 6. Prompt 目录

### 6A. 关键 Prompt

| Role | repo_path | quote_excerpt | Stage | Design intent | Hidden assumption | Likely failure mode |
|------|-----------|---------------|-------|--------------|-------------------|---------------------|
| **Orchestrator** | `templates/commands/workflow.md:23-29` | "你是**编排者**，协调多模型协作系统（研究 → 构思 → 计划 → 执行 → 优化 → 评审），用中文协助用户" | 所有阶段 | 定义 Claude 的角色为协调者而非实现者 | 用户说中文；任务是全栈的 | 非中文用户体验差；语言硬编码 |
| **Codex Reviewer** | `templates/prompts/codex/reviewer.md:7-9` | "You are a senior code reviewer specializing in backend code quality, security, and best practices. ZERO file system write permission - READ-ONLY sandbox" | 第 5/6 阶段评审 | 面向后端的质量门 | Codex 遵守 READ-ONLY 指令 | 如果未沙箱化，Codex 仍可能写入文件；prompt 不是技术强制 |
| **Gemini Reviewer** | `templates/prompts/gemini/reviewer.md:7-9` | "You are a senior UI reviewer specializing in frontend code quality, accessibility, and design system compliance. ZERO file system write permission" | 第 5/6 阶段评审 | 面向前端的质量门 | 同上 | 同上 |
| **Plan guardrail** | `templates/commands/plan.md:192-219` | "⚠️ 绝对禁止：❌ 问用户 Y/N 然后自动执行 ❌ 对产品代码进行任何写操作 ❌ 自动调用 /ccg:execute" | 计划交付 | 防止 Claude 在规划后自动执行 | Claude 始终遵循指令 | 如果用户表述模糊，Claude 仍可能尝试执行 |
| **Codex-exec one-shot** | `templates/commands/codex-exec.md:170-231` | "You are a full-stack execution agent. Implement the following plan end-to-end." | Codex 执行 | 将 MCP 搜索 + 实现 + 测试完全卸载给 Codex | Codex 有 MCP 工具访问权限；计划足够详细 | 如果 MCP 未配置，Codex 退化为猜测 |
| **Multi-agent Lead** | `templates/skills/orchestration/multi-agent/SKILL.md:249-267` | "你是天罗主修（蚁后），负责协调多 Agent 协同任务。铁律：每个文件只能分配给一个 Agent" | 团队执行 | 文件级所有权隔离 | Agent 遵守文件边界 | 无技术文件锁；agent 仍可在任意位置写入 |
| **Verify-security** | `templates/skills/tools/verify-security/SKILL.md:15-20` | "安全即道基，破则劫败。Critical/High 问题必须修复后才能交付" | 实现后 | 安全质量门 | `security_scanner.js` 脚本存在且可用 | 脚本引用 skill 目录下的 `scripts/security_scanner.js` — 必须随 SKILL.md 一起安装 |

### 6B. Prompt 设计观察

所有命令模板共享一个**重复的样板块**（约 40 行）用于"多模型调用规范"。该块在 20+ 命令文件中复制粘贴，仅有少量变化（`CLAUDE.md:45-46`）。这导致：
- **维护负担**：Bug 修复必须同时应用到 20+ 文件（v1.7.87 修复 Gemini 重试规则跨"20 个命令模板"即为证据）
- **一致性风险**：模板可能逐渐不同步

---

## 7. 设计亮点 — 微观

### 7.1 `codeagent-wrapper` 作为进程级代理

**观察**：Go 二进制是系统中最精密的组件 — 一个支持 JSON 流解析、会话管理、并行执行和结构化输出的多后端进程代理。

**依据**：`codeagent-wrapper/main.go`、`backend.go`、`executor.go` — 约 1500 行 Go 代码，14 个测试文件，Backend 接口模式，用于并行任务的拓扑排序。

**重要性**：这是唯一具有真正工程严谨性的组件（类型化接口、测试、错误处理、跨平台支持）。它解决了一个实际问题：从后台 Bash 命令中可靠地调用外部 CLI 工具并捕获其结构化输出。

**可迁移性**：高 — 进程代理模式可复用于任何多 CLI 编排。带依赖图的并行执行尤其有价值。

### 7.2 模板变量注入系统

**观察**：`installer-template.ts` 在安装时替换模板中的 `{{WORKDIR}}`、`{{MCP_SEARCH_TOOL}}`、`{{LITE_MODE_FLAG}}`、`{{GEMINI_MODEL_FLAG}}`。

**依据**：`installer.ts:191-192` — `injectConfigVariables(content, ctx.config)` + `replaceHomePathsInTemplate(content, ctx.installDir)`。

**重要性**：使模板在源码中保持环境无关，在安装时变为环境特定。但命令模板中的 `{{WORKDIR}}` token 在安装时被替换，意味着它被固化为静态路径 — 而命令又指示 Claude 在运行时动态检测 `WORKDIR`，形成了双层变量系统。

**可迁移性**：Direct — 简单的字符串替换模式。

### 7.3 `ROLE_FILE:` 指令用于 Prompt 注入

**观察**：命令模板指示 Claude 在 stdin 任务文本的首行包含 `ROLE_FILE: <path>`。`codeagent-wrapper` 随后调用 `injectRoleFile()` 读取引用的文件并将其内容前置。

**依据**：`main.go:272-276` — `injectRoleFile(cfg.Tasks[i].Task)`，`main.go:394-397`。

**重要性**：这是一种巧妙的机制，在不膨胀命令模板的情况下将专家 prompt 注入外部模型调用。Prompt 文件在 wrapper 执行时读取而非安装时，因此始终是最新的。

**可迁移性**：Direct — 将角色定义与工作流定义分离的优雅模式。

### 7.4 通过 `resume <SESSION_ID>` 实现会话连续性

**观察**：codeagent-wrapper 从后端的 JSON 流输出中捕获 `SESSION_ID` 并返回给 Claude。后续调用使用 `resume <SESSION_ID>` 延续同一对话。

**依据**：`executor.go:1300-1301` — `result.SessionID = threadID`，`plan.md:57`，`execute.md:98`。

**重要性**：使多阶段工作流中 Codex/Gemini 能在 plan→execute 转换间保持上下文。没有此机制，每个阶段都将从零开始。

**可迁移性**：Inspired — 需要后端 CLI 支持会话恢复。

### 7.5 双源二进制下载与 CDN 回退

**观察**：二进制下载优先尝试 Cloudflare R2 CDN（30 秒超时，对中国友好），失败后回退到 GitHub Release（120 秒超时）。

**依据**：`installer.ts:86-89` — `BINARY_SOURCES` 数组包含两个条目。

**重要性**：针对 GitHub 慢/被屏蔽的中国用户的务实解决方案。体现了对实际部署约束的关注。

---

## 8. 设计亮点 — 宏观

### 8.1 Process-as-Prose 架构

**观察**：整个工作流逻辑 — 阶段排序、质量门、模型路由、错误处理 — 编码在 Markdown prompt 文件中，而非代码中。代码（安装器 + wrapper）仅处理模板部署和进程管理。

**依据**：对比 `workflow.md`（193 行工作流逻辑）与 `installer.ts`（793 行文件复制）— 安装器对工作流语义一无所知。

**重要性**：这是与代码驱动工作流引擎根本不同的架构。优势：快速迭代（编辑 .md 文件即可），工作流更改无需构建步骤。劣势：零强制执行，工作流逻辑无类型安全，难以测试工作流行为，模板间 prompt 漂移。

**可迁移性**：Philosophical — "workflow-as-code"（强制执行、可测试性）与"workflow-as-prose"（灵活性、速度）之间的取舍，是任何 agent 工作流系统的关键设计决策。

### 8.2 固定路由：前端 → Gemini，后端 → Codex

**观察**：模型路由是硬编码的。Gemini 始终处理前端；Codex 始终处理后端。无动态模型选择，无回退路由（除 Gemini 重试外）。

**依据**：`CLAUDE.md:261-268` — "v1.7.0 起，以下配置不再支持自定义"，其中 frontend=Gemini, backend=Codex。

**重要性**：简洁优先于灵活。减少了配置面，但也剥夺了用户选择。如果 Gemini 在后端表现更好（或反之），系统无法在不修改模板的情况下适应。

### 8.3 "脏原型"重构模式

**观察**：外部模型产出"脏原型"（Unified Diff 补丁）；Claude 审查并重构后再应用。这是核心安全模型。

**依据**：`execute.md:15-16` — "将 Codex/Gemini 的 Unified Diff 视为'脏原型'，必须重构为生产级代码"。

**重要性**：这是一种类似 human-in-the-loop 的模式，Claude 扮演"高级开发者"审查初级开发者（Codex/Gemini）的输出。但在 `/ccg:codex-exec` 模式中，Codex 直接写入，Claude 仅在事后审查 — 重构步骤被跳过。

### 8.4 多 Agent 协作：蚁群隐喻

**观察**：multi-agent skill 使用蚁群隐喻，包含 Scout（探索者）、Worker（实现者）、Soldier（审查者）、Lead（协调者）角色，以及使用 TaskCreate 元数据进行间接通信的"信息素"系统。

**依据**：`templates/skills/orchestration/multi-agent/SKILL.md:1-494` — 494 行编排设计。

**重要性**：这是系统中最有野心的设计。信息素概念（在任务元数据中编码 `discovery`/`progress`/`warning`/`repellent` 信号）很有创意。然而，这完全是基于 prompt 的 — TaskCreate API 实际上并未强制信息素语义。

---

## 9. 失败模式

### FM-1：Prompt 样板漂移

**已观察到**：v1.7.87 变更日志："20 个命令模板新增 Gemini 调用失败重试规则"和"20 个命令模板新增 Codex 等待规则"— 手动在 20 个文件中逐一修补。

**根因**：无共享 include 机制。每个命令模板包含"多模型调用规范"块的完整副本。

**影响**：高 — 一个模板中遗漏的修复会造成行为不一致。变更日志中多个"补漏"条目已证明此问题。

### FM-2：虚假安全声明

**已观察到**：README 声称"Security by design — External models have no write access"，而 `executor.go:777` 向 Codex 传递 `--dangerously-bypass-approvals-and-sandbox`。

**根因**："安全性"是 prompt 级指令，非进程级沙箱。

**影响**：中 — 用户可能信任该安全声明，在需要实际沙箱的敏感环境中使用 CCG。

### FM-3：Plan-Execute 边界无强制

**已观察到**：`/ccg:plan` 包含精心设计的护栏（"⚠️ 绝对禁止：❌ 对产品代码进行任何写操作"），但无 hook 验证是否确实未发生写入。

**根因**：Process-as-prose 架构 — 无 `PostToolUse` hook 在计划阶段检查文件写入。

**影响**：中低 — Claude 通常遵循指令，但在复杂交互中可能无意写入文件。

### FM-4：二进制版本耦合

**已观察到**：`CLAUDE.md:461-464` 记录 wrapper Go 版本和 `installer.ts` 的 EXPECTED_BINARY_VERSION 必须手动匹配。不匹配 → 用户无法下载正确的二进制。

**根因**：Go 源码与 TypeScript 安装器之间无自动版本同步。

**影响**：中 — 发布流程需要手动注意。

### FM-5：Session-ID 脆弱性

**已观察到**：会话连续性依赖 Claude 正确解析并存储 wrapper 输出中的 `SESSION_ID`，然后正确注入后续的 `resume` 调用。

**根因**：无结构化会话交接机制 — SESSION_ID 嵌入在自由文本输出中，依赖 prompt 指令进行传播。

**影响**：中 — 如果 Claude 未能捕获 SESSION_ID（上下文压缩、prompt 漂移），工作流退化为无状态模式。

### FM-6：硬编码中文语言

**已观察到**：所有命令模板为中文。`CLAUDE.md:261` 记录："语言 | 固定值 | 中文 | 所有模板为中文"。v1.7.69 添加了 i18n 但仅限 CLI，不含模板。

**根因**：模板最初为中文用户编写；模板的 i18n 未实现。

**影响**：对非中文用户影响大 — 工作流指令、阶段标签和错误消息全部为中文。

---

## 10. 迁移评估

### 迁移候选

| Mechanism | Source | Transferability | Effort | Prerequisite | Risk |
|-----------|--------|----------------|--------|--------------|------|
| **codeagent-wrapper 进程代理** | `codeagent-wrapper/`（Go） | Direct | L | Go 构建基础设施 | 单后端使用场景下过度工程 |
| **ROLE_FILE: 指令** | `main.go` injectRoleFile | Direct | S | 类 wrapper 的进程代理 | 无 — 优雅且简单 |
| **会话连续性（resume）** | `executor.go`，命令模板 | Inspired | M | 后端 CLI 支持会话 | Session ID 捕获脆弱性 |
| **带拓扑排序的并行执行** | `executor.go:287-515` | Direct | M | Go 二进制或等价物 | 依赖图管理的复杂性 |
| **模板变量注入** | `installer-template.ts` | Direct | S | 安装器管线 | 双层变量系统的混乱 |
| **质量门 skill** | `templates/skills/tools/verify-*` | Inspired | M | Skill 基础设施 | SKILL.md 引用的脚本可能不存在 |
| **多 agent 信息素系统** | `multi-agent/SKILL.md` | Inspired | L | Agent Teams 支持 | 纯 prompt 驱动；无真正强制 |
| **双源二进制下载** | `installer.ts:86-89` | Direct | S | CDN + GitHub Release 配置 | CDN 维护负担 |
| **Plan→Execute 分离** | `plan.md`, `execute.md`, `codex-exec.md` | Inspired | M | 计划文件格式 + 会话交接 | 计划格式耦合 |
| **输出风格（人格化）** | `templates/output-styles/` | Non-transferable | - | 文化背景 | 受众面窄 |

### 建议采用顺序

1. **ROLE_FILE: 指令**（S）— 对任何多模型 skill 立即有用。零风险。
2. **模板变量注入**（S）— 如果要构建类似的安装器则有用。
3. **Plan→Execute 分离设计**（M）— 将规划与执行分离、计划持久化到文件的概念具有广泛价值。适配格式而非模板。
4. **质量门 skill 模式**（M）— 基于触发器自动调用验证 skill 的模式很好。需要 Hard 强制（hook）才有实际意义。
5. **codeagent-wrapper 代理**（L）— 仅在构建多后端编排系统时需要。Go 二进制工程质量高但较重。

### 必须构建的强制机制（如果移植模式）

| Gap in CCG | What to build | Why |
|-----------|---------------|-----|
| 无阶段强制 | 验证阶段转换的 `PostToolUse` hook | 防止阶段跳过 |
| Plan 模式无写保护 | 在计划阶段阻止 Write/Edit 的 `PreToolUse` hook | 强制 plan-only 语义 |
| 无文件所有权强制 | 根据 agent 分配检查文件路径的 `PreToolUse` hook | 防止跨 agent 文件冲突 |
| 无模板去重 | 通用块的共享 include 机制 | 防止样板漂移 |
| 无会话交接验证 | 结构化会话状态文件替代自由文本 SESSION_ID | 防止上下文压缩时会话丢失 |

---

## 11. 待解问题

1. **`security_scanner.js` 是否存在**：`verify-security/SKILL.md` 引用 `scripts/security_scanner.js`，但在模板目录中未找到该文件。是在安装时生成的，还是期望用户自行提供？

2. **`run_skill.js` 运行器**：`SKILL.md` 引用 `~/.claude/skills/ccg/run_skill.js` 作为统一 skill 运行器。它的功能是什么？是薄包装还是包含逻辑？

3. **OPSX 集成深度**：`.agents/skills/openspec-*` 中有 10 个 OpenSpec skill，但它们似乎是 OPSX CLI 的透传包装。集成深度如何 — CCG 在转发之外是否增加了价值，还是纯粹的命令别名？

4. **`.context/` 目录生命周期**：v1.7.80 引入，被 13 个角色 prompt 引用。实际采用范围有多广？是否与 Claude Code 自身的记忆系统冲突？

5. **测试覆盖缺口**：6 个 TypeScript 测试文件测试安装器机制，而非工作流行为。没有测试验证命令模板是否产生正确的 wrapper 调用、SESSION_ID 是否正确传播、或阶段转换是否按文档工作。这是有意为之（prompt 行为不可测试）还是覆盖缺口？

---

## 提交前检查清单

| # | Gate | Pass? |
|---|------|-------|
| A | Source Inventory：按 overview/execution/prompt/enforcement/evolution 分类 | Yes |
| B | Prompt Traceability：每个主要角色有目录条目，包含 repo_path + quote_excerpt | Yes |
| C | Object Model：至少 3 个一等实体有生命周期 | Yes（8 个实体） |
| D | State Machine：有转换的阶段，非扁平步骤列表 | Yes（3 个流程图） |
| E | Enforcement Audit：每个关键约束标记为 Hard/Soft/Unenforced | Yes（14 个条目） |
| F | Micro + Macro split：两个设计亮点层级均存在 | Yes（5 微观 + 4 宏观） |
| G | Failure Modes：至少 3 个有依据 | Yes（6 个失败模式） |
| H | Migration Output：候选项有评级、采用顺序、必须构建的强制机制 | Yes |
