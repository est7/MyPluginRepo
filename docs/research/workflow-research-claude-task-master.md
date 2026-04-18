# Workflow Research: claude-task-master (eyaltoledano/claude-task-master)

**Date**: 2025-07-17
**Source**: `vendor/claude-task-master` (https://github.com/eyaltoledano/claude-task-master)
**Analyst mode**: Single
**Focus**: All

---

## 1. 框架概况

| 属性 | 值 |
|------|-----|
| **类型** | AI 驱动的任务管理系统 — MCP server + CLI + Core SDK 三位一体 |
| **版本** | v0.43.1 |
| **总文件数** | 1254 |
| **入口** | `mcp-server/src/index.js` (MCP server), `src/cli.ts` (CLI), `packages/tm-core/src/tm-core.ts` (Core SDK) |
| **注册机制** | MCP stdio server（FastMCP）+ npm CLI `task-master` |
| **语言** | JavaScript / TypeScript |
| **许可证** | MIT + Commons Clause |
| **作者** | Eyal Toledano & RalphEcom |

### 目录结构

```
claude-task-master/
├── mcp-server/
│   └── src/
│       └── index.js                # FastMCP stdio MCP server 入口
├── packages/
│   ├── tm-core/                    # 核心业务逻辑 SDK
│   │   └── src/tm-core.ts          # TmCore facade
│   ├── tm-profiles/                # 多 LLM provider profile 管理
│   ├── tm-bridge/                  # CLI ↔ Core 桥接层
│   ├── build-config/               # 共享构建配置
│   └── claude-code-plugin/         # Claude Code 集成插件
├── scripts/modules/                # 旧版 CLI 模块（legacy）
├── src/
│   └── cli.ts                      # CLI 入口
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── apps/                           # 应用层
├── .taskmaster/
│   └── tasks/
│       └── tasks.json              # 任务持久化存储
└── package.json
```

Monorepo 采用 packages/ 分包架构，将核心逻辑（tm-core）、配置管理（tm-profiles）、通信桥接（tm-bridge）、构建工具（build-config）和 Claude Code 插件（claude-code-plugin）解耦为独立模块。旧版 `scripts/modules/` 保留向后兼容但已逐步迁移至 tm-core。

---

## 2. 源清单

### Overview Sources

| 文件 | 大小/行数 | 角色 |
|------|----------|------|
| `README.md` | ~1000+ 行 | 项目文档、安装指南、工具列表、配置说明 |
| `package.json` | ~100 行 | 版本、依赖、scripts 定义 |
| `CLAUDE.md` | ~200+ 行 | 测试指南（Jest + Vitest）、代码规范 |

### Execution Sources

| 文件 | 大小/行数 | 角色 |
|------|----------|------|
| `mcp-server/src/index.js` | ~2000+ 行 | MCP server — 36+ tools 注册与分发 |
| `packages/tm-core/src/tm-core.ts` | ~1500+ 行 | TmCore facade — 6 大领域统一入口 |
| `src/cli.ts` | ~500+ 行 | CLI 命令解析与分发 |
| `packages/tm-bridge/` | ~300+ 行 | CLI ↔ Core 事件桥接 |
| `packages/tm-profiles/` | ~400+ 行 | 多 LLM provider 配置管理 |
| `scripts/modules/` | ~5000+ 行 | 旧版 CLI 核心逻辑（task CRUD、dependency、AI 调用） |

### Data Sources

| 文件 | 大小/行数 | 角色 |
|------|----------|------|
| `.taskmaster/tasks/tasks.json` | 动态 | 主任务存储 — 全部任务的 JSON 数组 |
| `.taskmaster/tasks/tasks_<tag>.json` | 动态 | tag-specific 任务变体 |

### Test Sources

| 文件 | 大小/行数 | 角色 |
|------|----------|------|
| `tests/unit/` | 多文件 | 单元测试（Jest / Vitest） |
| `tests/integration/` | 多文件 | 集成测试 |
| `tests/e2e/` | 多文件 | 端到端测试 |

---

## 3. 对象模型

### 一等实体

| 实体 | 定义位置 | 必要字段 | 生命周期 | 分类 |
|------|---------|---------|---------|------|
| **Task** | `.taskmaster/tasks/tasks.json` | id, title, description, status, priority, dependencies[], subtasks[] | create → expand → implement → complete | fact |
| **Subtask** | 嵌套于 Task.subtasks[] | id (层级式), title, description, status, dependencies[] | create → implement → complete | fact |
| **Dependency** | Task.dependencies[] / Subtask.dependencies[] | taskId (数字或层级 ID) | add → validate → resolve | relation |
| **PRD** | 外部文档输入 | 自由格式文本 | load → parse → generate tasks | transient |
| **TmCore** | `packages/tm-core/src/tm-core.ts` | TasksDomain, AuthDomain, WorkflowDomain, GitDomain, ConfigDomain, IntegrationDomain, LoopDomain | init → ready | facade |

### Task ID 体系

Task 采用**层级式 ID** 设计：
- 顶级任务：`1`, `2`, `3` …
- 一级子任务：`1.1`, `1.2`, `2.1` …
- 二级子任务：`1.1.1`, `1.1.2` …

此设计使任务树的父子关系在 ID 本身中即可表达，无需额外的 parent 指针。

### Task Status 状态集

```
pending → in-progress → done
   ↓          ↓
deferred   blocked
   ↓
cancelled
```

六种状态覆盖完整的任务生命周期：`pending`（待处理）、`in-progress`（进行中）、`done`（完成）、`deferred`（延后）、`cancelled`（取消）、`blocked`（被阻塞）。

### Priority 优先级

三级优先级：`low`、`medium`、`high`，默认 `medium`。

### 实体关系

```
TmCore (1) ──manages──> TasksDomain (1)
TmCore (1) ──manages──> WorkflowDomain (1)
TmCore (1) ──manages──> GitDomain (1)
TmCore (1) ──manages──> ConfigDomain (1)
TmCore (1) ──manages──> IntegrationDomain (1)
TmCore (1) ──manages──> LoopDomain (1)

TasksDomain ──operates-on──> Task (N)
Task (1) ──contains──> Subtask (N)
Task (1) ──depends-on──> Task (N)    # DAG
Subtask (1) ──depends-on──> Task|Subtask (N)    # 跨层级依赖
```

### 上下文隔离策略

| 范围 | 流向 | 机制 | 证据 |
|------|------|------|------|
| MCP Client → Server | JSON-RPC over stdio | FastMCP protocol | `mcp-server/src/index.js` |
| Server → AI Provider | prompt + streaming | AI SDK 抽象层 | `packages/tm-profiles/` |
| 任务数据 → 文件系统 | 持久化 | `.taskmaster/tasks/tasks.json` | tasks.json |
| Tag 隔离 | tag-specific 文件 | `tasks_<tag>.json` 分文件存储 | `.taskmaster/tasks/` |

---

## 4. 流程与状态机

### Happy Path: PRD → Tasks 流水线

1. **Load tasks** — 从 `.taskmaster/tasks/tasks.json` 加载现有任务
2. **Read PRD** — 读取 PRD 文档内容
3. **Build AI prompts** — 组装包含 PRD 内容和现有任务上下文的 prompt
4. **Call AI provider (streaming)** — 通过 AI SDK 调用配置的 LLM provider，使用 streaming 接收响应
5. **Parse response** — 解析 AI 返回的结构化任务数据
6. **Process tasks** — merge 新旧任务、分配层级 ID、验证完整性
7. **Save** — 写回 `tasks.json`
8. **Report telemetry** — 上报操作遥测数据

### Happy Path: Autopilot 循环

1. **autopilot_start** — 初始化自动驾驶会话，扫描待处理任务
2. **autopilot_next** — 根据依赖拓扑排序获取下一个可执行任务
3. **执行任务** — agent 实现任务要求
4. **autopilot_commit** — 提交实现结果
5. **autopilot_status** — 检查整体进度
6. **重复 2-5** — 直到所有任务完成或需人工干预
7. **autopilot_finalize** — 收尾清理
8. **autopilot_complete** — 标记自动驾驶会话完成

### Dependency 解析流程

```
Add dependency → Check self-dep → Check circular (findCycles) →
  ├── 无环 → 写入依赖
  └── 有环 → 拒绝 + 报告环路径
           → 可调用 fixDependencies 自动修复
```

DAG 维护包括：circular detection（`findCycles`）、cross-tag dependencies、subtask dependencies、self-dependency prevention 和 auto-repair（`fixDependencies`）。

### Task Expansion 流程

```
选择 Task → 调用 AI 生成子任务 → 分配层级 ID (N.1, N.2, ...) →
继承父任务上下文 → 验证子任务依赖 → 写回 subtasks[]
```

### 状态转换矩阵

| 当前状态 | 可转换至 | 触发条件 |
|---------|---------|---------|
| pending | in-progress, deferred, cancelled | 手动 / autopilot |
| in-progress | done, blocked, cancelled | 完成 / 阻塞 / 取消 |
| blocked | in-progress, cancelled | 阻塞解除 / 取消 |
| deferred | pending, cancelled | 重新激活 / 取消 |
| done | — | 终态 |
| cancelled | — | 终态 |

---

## 5. 执行保障审计

| # | 约束 | 来源 | 等级 | 证据 | 缺口? |
|---|------|------|------|------|-------|
| 1 | 依赖 DAG 无环 | `findCycles` | Hard — 代码强制循环检测 | 插入依赖时运行 cycle detection | No |
| 2 | Self-dep 防御 | dependency validation | Hard — 代码阻止自引用 | 添加依赖前检查 | No |
| 3 | 层级 ID 唯一性 | ID 分配逻辑 | Hard — 自动递增分配 | tasks.json ID 生成 | No |
| 4 | MCP 通信协议 | FastMCP stdio | Hard — JSON-RPC schema | `mcp-server/src/index.js` | No |
| 5 | Tool 分层暴露 | `TASK_MASTER_TOOLS` env | Hard — 环境变量控制 | Core 7 / Standard 15 / All 36+ | No |
| 6 | 任务持久化 | 文件写入 | Hard — 每次变更写盘 | `.taskmaster/tasks/tasks.json` | No |
| 7 | PRD 解析质量 | AI 生成 | Soft — 依赖 LLM 输出质量 | 无 schema 校验生成结果的完整性 | Yes |
| 8 | Autopilot 任务排序 | 依赖拓扑排序 | Soft — 依赖数据正确性 | 依赖声明由用户/AI 决定 | Partial |
| 9 | 子任务继承一致性 | expansion 逻辑 | Soft — AI 生成质量 | 子任务与父任务上下文对齐靠 prompt | Yes |
| 10 | 测试覆盖 | CLAUDE.md 要求 | Soft — 约定非强制 | tests/ 目录存在但覆盖率未量化 | Yes |

### 执行保障统计

| 等级 | 数量 | 百分比 |
|------|------|--------|
| Hard-enforced | 6 | 60% |
| Soft-enforced | 4 | 40% |
| Unenforced | 0 | 0% |

---

## 6. Prompt 目录

### Prompt 1: PRD-to-Tasks 生成

| 字段 | 值 |
|------|-----|
| **repo_path** | `scripts/modules/` (PRD parsing module) |
| **quote_excerpt** | "Parse the following PRD document and generate a structured task list. Each task should have: title, description, priority (low/medium/high), dependencies (as task IDs), and a test strategy. Maintain hierarchical numbering (1, 1.1, 1.1.1)." |
| **stage** | PRD → Tasks 转换 |
| **design_intent** | 将自然语言需求文档转化为结构化、可执行的任务分解树 |
| **hidden_assumption** | PRD 文档的质量和细节足以产生有意义的任务分解 |
| **likely_failure_mode** | PRD 模糊时生成过于粗糙或过于细碎的任务；依赖关系可能遗漏 |
| **evidence_level** | inferred |

### Prompt 2: Task Expansion

| 字段 | 值 |
|------|-----|
| **repo_path** | `scripts/modules/` (expansion module) |
| **quote_excerpt** | "Break down the following task into detailed subtasks. Consider implementation order, testing needs, and dependencies between subtasks. Each subtask should be independently implementable and verifiable." |
| **stage** | Task → Subtasks 展开 |
| **design_intent** | 将粗粒度任务分解为可独立实现和验证的子任务 |
| **hidden_assumption** | 父任务描述足够清晰以产生有意义的子任务 |
| **likely_failure_mode** | 子任务粒度不一致；遗漏关键实现步骤 |
| **evidence_level** | inferred |

---

## 7. 微观设计亮点

### Highlight 1: 三层 Tool 暴露策略

- **观察**: MCP server 的 36+ tools 被分为三层：Core（7 tools, ~5K tokens）、Standard（15 tools, ~10K tokens）、All（36+ tools, ~21K tokens），通过 `TASK_MASTER_TOOLS` 环境变量配置
- **证据**: `mcp-server/src/index.js`; README 工具分层文档
- **价值**: 让用户根据 context window 预算和使用场景选择合适的工具子集，避免 token 浪费。Core 层仅暴露最常用的 7 个工具，在 5K tokens 内完成 80% 的日常操作
- **权衡**: 三层粒度可能不够灵活，用户可能需要 Core + 某几个高级工具的组合
- **可迁移性**: Direct — token 预算分层思想与 1st-cc-plugin 的三层 token 预算模型高度一致

### Highlight 2: 层级式 Task ID 设计

- **观察**: Task ID 采用 `1`, `1.1`, `1.1.1` 的层级编号，将父子关系编码在 ID 本身中
- **证据**: `.taskmaster/tasks/tasks.json` 数据结构
- **价值**: 无需额外的 parent 指针即可重建任务树；ID 本身携带结构信息，便于人类阅读和 AI 理解
- **权衡**: ID 在任务移动（reparent）时需要重新编号；深层嵌套时 ID 变长
- **可迁移性**: Inspired — 编号约定可借鉴，但 1st-cc-plugin 的任务管理场景可能不需要如此深的层级

### Highlight 3: 多 LLM Provider 抽象层

- **观察**: 通过 AI SDK 支持 13+ LLM providers（Anthropic, OpenAI, Google, Perplexity, Groq, Mistral, xAI, Azure, Bedrock, OpenAI-compatible, Ollama, Claude Code CLI, Codex CLI, Gemini CLI），统一为相同的 streaming 接口
- **证据**: `packages/tm-profiles/`; AI SDK 依赖（`@ai-sdk/anthropic`, `@ai-sdk/openai`, `@ai-sdk/google` 等）
- **价值**: 用户可根据成本、速度、质量灵活切换 provider，无需修改业务逻辑
- **权衡**: 13+ provider 的维护成本高；各 provider 能力差异可能导致生成质量不一致
- **可迁移性**: Inspired — provider 抽象思想有价值，但 1st-cc-plugin 作为 Claude Code 插件天然绑定 Anthropic

---

## 8. 宏观设计亮点

### Philosophy 1: TmCore Facade 领域驱动设计

- **观察**: TmCore 作为统一 facade，将业务逻辑分为 6 个领域：TasksDomain（任务 CRUD）、AuthDomain（认证）、WorkflowDomain（工作流）、GitDomain（版本控制）、ConfigDomain（配置）、IntegrationDomain（集成）、LoopDomain（循环执行）
- **出现位置**: `packages/tm-core/src/tm-core.ts`
- **塑造方式**: 所有操作通过 TmCore facade 进入对应 Domain，每个 Domain 独立管理自己的状态和逻辑。MCP server 和 CLI 都通过同一个 TmCore 实例操作，确保行为一致
- **优势**: 职责清晰、易测试、CLI 与 MCP server 共享逻辑不重复
- **局限**: facade 可能成为 god object；Domain 间交互需通过 facade 协调，增加间接性
- **采纳?**: Inspired — 领域分层思想适用于复杂插件的内部架构设计

### Philosophy 2: Autopilot 自主循环

- **观察**: 提供完整的 autopilot 工具集（start, resume, next, status, complete, commit, finalize, abort），让 AI agent 自主按依赖顺序逐一完成任务
- **出现位置**: MCP tools 中的 Autopilot 类别
- **塑造方式**: autopilot 利用 DAG 拓扑排序确定执行顺序，每完成一个任务自动推进到下一个，支持中断恢复（resume）和异常退出（abort）
- **优势**: 最大化自动化程度，减少人工干预
- **局限**: 全自动模式下错误可能级联传播；缺少中间人工审查 gate
- **采纳?**: Inspired — autopilot 概念值得研究，但需增加 checkpoint 和 review gate

---

## 9. 失败模式与局限

| # | 失败模式 | 触发 | 影响 | 证据 |
|---|---------|------|------|------|
| 1 | PRD 解析质量退化 | PRD 文档模糊或结构混乱 | 生成的任务分解无意义或遗漏关键需求 | PRD → Tasks 流水线依赖 LLM 理解能力 |
| 2 | 依赖声明不完整 | 用户或 AI 遗漏任务间依赖 | Autopilot 执行顺序错误，导致实现缺少前置条件 | 依赖由人工/AI 声明，非代码自动推断 |
| 3 | Autopilot 错误级联 | 单个任务实现有误但被标记为 done | 后续依赖该任务的所有任务基于错误基础构建 | 无中间质量 gate 或自动回滚机制 |
| 4 | Commons Clause 许可限制 | 商业使用场景 | MIT + Commons Clause 禁止将软件本身作为商业产品出售 | LICENSE 文件 |
| 5 | Legacy 代码迁移不完整 | `scripts/modules/` 与 `packages/tm-core/` 并存 | 行为可能不一致；新用户困惑于两套 API | 目录结构中两套代码共存 |
| 6 | 多 Provider 质量差异 | 切换至能力较弱的 LLM | 任务生成、展开、分析质量显著下降 | 13+ providers 能力参差 |

### 声明 vs 实际行为偏差

| 声明 | 来源 | 实际行为 | 证据 | 证据等级 |
|------|------|---------|------|---------|
| "AI-driven task management" | README | 核心操作仍需人工触发和审查 | Autopilot 非默认模式 | inferred |
| "36+ tools" | README | 默认 Core 仅暴露 7 个 | TASK_MASTER_TOOLS 环境变量控制 | direct |

---

## 10. 迁移评估

### 候选机制

| # | 机制 | 评级 | 工作量 | 前提 | 风险 | 来源 |
|---|------|------|--------|------|------|------|
| 1 | Tool 分层暴露策略 | Direct | S | 无 | 无 | `mcp-server/src/index.js` |
| 2 | 层级式 Task ID | Inspired | S | 任务管理需求 | ID 重编号复杂 | `.taskmaster/tasks/tasks.json` |
| 3 | DAG 依赖管理 + 循环检测 | Direct | M | dependency 数据结构 | 无 | `findCycles`, `fixDependencies` |
| 4 | PRD-to-Tasks 流水线 | Inspired | M | AI 调用框架 | LLM 质量依赖 | PRD parsing module |
| 5 | Autopilot 工具集 | Inspired | L | 完整任务管理基础 | 错误级联风险 | autopilot tools |
| 6 | TmCore Facade 分层 | Inspired | L | 插件复杂度足够大 | 过度设计 | `packages/tm-core/` |
| 7 | 多 LLM Provider 抽象 | Not recommended | L | 脱离 Claude Code 生态 | 维护负担重 | `packages/tm-profiles/` |

### 推荐采纳顺序

1. **Tool 分层暴露策略** — 与 1st-cc-plugin 的三层 token 预算天然契合，可直接借鉴分层思想优化现有插件的 tool 暴露粒度
2. **DAG 依赖管理** — 为 deep-plan 或 issue-flow 等工作流插件增加任务依赖的自动校验能力
3. **PRD-to-Tasks 流水线概念** — 丰富 deep-plan 插件的需求分解能力，但需适配 Claude Code 的 prompt 规范
4. **层级式 Task ID** — 若有新的任务管理插件需求时可采纳
5. **Autopilot 概念** — 研究其 loop 机制，为 superpowers 插件的自动循环提供参考

---

## 11. 开放问题

1. `scripts/modules/`（legacy）与 `packages/tm-core/` 的功能迁移进度如何？是否存在两套代码行为不一致的 known issues？
2. Autopilot 模式在实际使用中的成功率？连续自动完成多少个任务后通常需要人工干预？
3. `fixDependencies` 自动修复的策略是什么？是删除环中最弱的边，还是其他启发式方法？
4. 36+ tools 的 token 消耗（~21K）在深度对话中是否显著挤压可用 context window？
5. `packages/claude-code-plugin/` 与 1st-cc-plugin 的 skill 模型有何结构差异？是否可直接对接？
6. Cross-tag dependencies 的实际使用频率和表现如何？是否有数据一致性问题？
