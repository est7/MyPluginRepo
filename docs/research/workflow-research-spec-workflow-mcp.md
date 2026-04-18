# Workflow Research Report: spec-workflow-mcp

> 逆向工程研究报告 — 生成时间：2025-07-18

---

## 1. 框架概况

| 维度 | 说明 |
|------|------|
| **类型** | MCP Server + Real-time Dashboard + VSCode Extension |
| **文件数** | ~453 files |
| **语言** | TypeScript (Node.js)，React (Dashboard Frontend) |
| **包名** | `@pimzino/spec-workflow-mcp` (npm) |
| **版本** | 2.2.6 |
| **入口** | `src/index.ts`（CLI 调度器）、`src/server.ts`（MCP Server）|
| **许可证** | GPL-3.0 |
| **范式** | MCP-native spec-driven dev，Human-In-Loop Approval |

spec-workflow-mcp 是一个基于 Model Context Protocol (MCP) 的 specification-driven 开发服务器，提供三位一体的开发体验：MCP Server（与 AI agent 通信）、Real-time Web Dashboard（Fastify + React）、VSCode Extension（侧边栏集成）。核心特征是**顺序阶段 + 人工审批 + 实施日志**的闭环流程。

---

## 2. 源清单

| 文件/目录 | 角色 |
|-----------|------|
| `src/index.ts` | CLI 入口，参数解析，双模式调度（MCP/Dashboard）|
| `src/server.ts` | MCP Server 类，工具/prompt 注册 |
| `src/types.ts` | 核心 TypeScript 接口定义 |
| `src/config.ts` | 配置加载与校验 |
| `src/tools/index.ts` | Tool registry 与调度器（5 个 tool）|
| `src/tools/spec-workflow-guide.ts` | Workflow 指引工具（含 mermaid 图）|
| `src/tools/approvals.ts` | 审批管理（request/status/delete）|
| `src/tools/log-implementation.ts` | 实施日志记录（强制 artifact）|
| `src/prompts/index.ts` | Prompt registry（7 个 prompt）|
| `src/prompts/create-spec.ts` | 创建 spec 文档 prompt |
| `src/core/task-parser.ts` | Task 解析与 prompt 提取 |
| `src/core/path-utils.ts` | 跨平台路径处理与安全校验 |
| `src/core/security-utils.ts` | Localhost 绑定校验 |
| `src/dashboard/approval-storage.ts` | JSON 文件持久化，事件驱动更新 |
| `src/dashboard/multi-server.ts` | 多项目 Fastify Server + WebSocket |
| `src/dashboard_frontend/` | React Dashboard UI（Vite 构建）|
| `vscode-extension/` | VSCode Extension 源码 |
| `docs/WORKFLOW.md` | 完整 workflow 指引 |
| `docs/technical-documentation/` | 架构、dashboard、文件结构文档 |
| `e2e/` | Playwright 端到端测试 |
| `containers/` | Docker 配置 |
| `package.json` | 项目清单（v2.2.6）|

---

## 3. 对象模型

### 核心实体

| 实体 | TypeScript 接口 | 说明 |
|------|----------------|------|
| **SpecData** | `SpecData` | Requirements/Design/Tasks 三阶段内容 + phase status |
| **PhaseStatus** | `PhaseStatus` | 跟踪 phase 存在性、审批状态、修改记录 |
| **ApprovalRequest** | `ApprovalRequest` | 审批请求：Pending/Approved/Rejected/Needs-Revision |
| **TaskInfo** | `TaskInfo` | 单个 task：ID, checkbox state, leverage, requirements 元数据 |
| **ImplementationLogEntry** | `ImplementationLogEntry` | 实施日志：code artifacts（APIs, components, functions, classes）|
| **SecurityConfig** | `SecurityConfig` | Rate limiting, audit logging, CORS 配置 |

### 实体关系

```
SpecData
├── Requirements (Phase 1: WHAT)
│   └── ApprovalRequest → Pending → Approved/Rejected/Needs-Revision
├── Design (Phase 2: HOW)
│   └── ApprovalRequest (依赖 Requirements Approved)
├── Tasks (Phase 3: STEPS)
│   ├── ApprovalRequest (依赖 Design Approved)
│   └── TaskInfo[] (checkbox: [ ], [-], [x])
└── Implementation (Phase 4: EXECUTION)
    └── ImplementationLogEntry[] (强制 artifact 记录)
```

### Context Isolation

- 每个项目在 dashboard 中独立管理
- Multi-project 架构：单个 dashboard 实例服务所有项目
- 数据存储为 JSON 文件，project path 作为 key
- WebSocket + file watching 实现实时同步

---

## 4. 流程与状态机

### Happy Path（4 阶段顺序推进）

```
Phase 1: Requirements (WHAT)
    ↓ AI 基于 prompt 生成 requirements 文档
    ↓ spec-status 工具检查状态
    ↓ approvals 工具 → request approval
    ↓ Dashboard 中人工审批 → Approved
Phase 2: Design (HOW)
    ↓ Requirements Approved 后自动解锁
    ↓ AI 生成 design 文档
    ↓ approvals → request approval → Approved
Phase 3: Tasks (STEPS)
    ↓ Design Approved 后自动解锁
    ↓ AI 生成 task list（checkbox 格式）
    ↓ approvals → request approval → Approved
Phase 4: Implementation (EXECUTION)
    ↓ Tasks Approved 后开始执行
    ↓ AI 逐个 task 实现代码
    ↓ log-implementation 记录 artifact（REQUIRED）
    ↓ task checkbox: [ ] → [-] → [x]
```

### Approval 状态机

```
ApprovalRequest:
  (不存在) → Pending (request approval)
  Pending → Approved ✓ (proceed to next phase)
  Pending → Rejected ✗ (archive)
  Pending → Needs-Revision (AI 根据 comment 修改，循环回 Pending)
```

### Task 状态机

```
Task Status:
  [ ] (pending) → [-] (in-progress) → [x] (completed)
```

### Failure Path

- **Approval Rejected**：spec 被归档，需重新创建
- **Needs-Revision Loop**：审批者要求修改 → AI 更新 → 重新提交审批。若审批者持续不满意，可能陷入无限循环
- **Artifact 缺失**：`log-implementation` 工具强制要求 artifact，空记录被拒绝
- **Path 安全违规**：绝对路径、path traversal (`..`)、root 目录被路径校验拦截

---

## 5. 执行保障审计

| 机制 | 级别 | 说明 |
|------|------|------|
| Phase 顺序强制 | **Hard** | 前一 phase 未 approved 时后续 phase 不可开始 |
| 人工审批 (approval) | **Hard** | 所有 phase 转换必须经过人工审批，不可自动通过 |
| Artifact 强制记录 | **Hard** | `log-implementation` 要求 artifact 字段非空 |
| Path 安全校验 | **Hard** | 拒绝绝对路径、`..` path traversal、root 目录 |
| Markdown MDX 校验 | **Hard** | 审批前校验文档格式兼容性 |
| Task checkbox 格式 | **Hard** | 严格校验 `1.0`, `1.1` 格式 + checkbox 语法 |
| Rate limiting | **Hard** | 120 req/min per client（可配置）|
| Localhost 绑定 | **Hard** | 默认只绑定 localhost，external 需显式 opt-in |
| Security headers | **Hard** | CSP, X-Frame-Options, X-Content-Type-Options |
| Audit logging | **Soft** | 可选开启，记录所有操作 |
| Steering documents | **Unenforced** | 引导性文档，影响 AI 行为但不阻断执行 |

---

## 6. Prompt 目录

### Prompt 1: create-spec（创建 Spec 文档）

**注册位置**：`src/prompts/create-spec.ts`

**核心指令摘要**：
> 基于用户描述创建结构化的 spec 文档。按 Requirements → Design → Tasks 三阶段模板生成内容。Requirements 聚焦 WHAT（用户需求），Design 聚焦 HOW（技术方案），Tasks 聚焦 STEPS（可执行任务列表，checkbox 格式）。每个阶段完成后引导用户通过 approvals 工具提交审批。

### Prompt 2: implement-task（实施任务）

**注册位置**：`src/prompts/index.ts`

**核心指令摘要**：
> 读取已审批的 tasks，识别下一个 `[ ]` 状态的 task，执行实现。实现完成后必须调用 `log-implementation` 工具记录 artifact（APIs, components, functions, classes, integrations）。将 task 状态从 `[ ]` 更新为 `[-]`（进行中）再到 `[x]`（完成）。

---

## 7. 微观设计亮点

### 7.1 Artifact-Mandatory Implementation Logging

`log-implementation` 工具**强制要求**记录 code artifact。不允许只说"我实现了 X"而不提供具体产物。这将实施日志从"文字记录"提升为"可搜索的 artifact registry"，防止代码重复和知识遗失。

### 7.2 Multi-project Single Dashboard

一个 dashboard 实例可以服务多个项目。项目自动发现通过扫描工作区目录完成。WebSocket 实现实时同步——一个项目的审批状态变更立即反映在 dashboard 上。

### 7.3 MCP-native 设计（零自定义 UI 依赖）

5 个 MCP tool + 7 个 MCP prompt 构成完整的 AI 交互接口。AI agent 通过标准 MCP 协议与 server 通信，无需 agent-specific 的自定义集成。Dashboard 和 VSCode extension 是锦上添花，不是必需品。

---

## 8. 宏观设计亮点

### 8.1 "Human-In-Loop as First Class"

审批系统不是事后添加的 feature，而是架构的核心组成部分。每个 phase 转换**必须**经过人工审批——这是对"AI 全自动"趋势的有意对抗。框架的立场是：AI 负责生成，人类负责决策。

### 8.2 "File-Based, Database-Free"

整个系统使用 JSON 文件持久化，无需数据库。这降低了部署复杂度，使数据人类可读（可 `cat`、可 `grep`），且天然支持 version control。

---

## 9. 失败模式与局限

| # | 失败模式 | 严重度 | 说明 |
|---|---------|--------|------|
| 1 | **Infinite revision loop** | High | Needs-Revision 状态可能导致无限循环——审批者持续不满意，AI 持续修改但无法收敛 |
| 2 | **Root directory protection failure** | Critical | Path 安全校验是关键防线，若被绕过可能影响系统文件 |
| 3 | **Single dashboard bottleneck** | Medium | 多项目共享单一 dashboard，高并发场景下 WebSocket 可能成为瓶颈 |
| 4 | **Port conflict** | Low | Dashboard 固定端口，多实例运行时冲突 |
| 5 | **Docker path mismatch** | Medium | 容器内外路径映射不一致可能导致 spec 文件定位失败 |
| 6 | **审批延迟阻塞全流程** | Medium | 人工审批是顺序依赖的，一个 phase 的审批延迟会阻塞整个 pipeline |
| 7 | **JSON 文件并发写入** | Low | 高并发场景下 JSON 文件可能出现写入竞争 |

---

## 10. 迁移评估

### 可迁移候选

| 候选 | 价值 | 迁移难度 | 目标位置 |
|------|------|---------|---------|
| **MCP tool/prompt 设计模式** | 标准化 AI 交互接口 | 中 | `1st-cc-plugin/` MCP 集成模式 |
| **Artifact-mandatory logging** | 可审计的实施记录 | 低 | `quality/` 插件组 |
| **Approval 状态机** | Human-in-loop 审批流程 | 中 | `workflows/deep-plan` |
| **Multi-project dashboard 概念** | 全局项目管理视图 | 高 | 长期建设目标 |
| **Path security validation** | 路径安全校验最佳实践 | 低 | 所有涉及文件操作的插件 |

### 建议采纳顺序

1. **Artifact-mandatory logging** → 简单高效，立即提升实施记录质量
2. **Path security validation** → 安全最佳实践，应用于文件操作插件
3. **Approval 状态机** → 丰富 `deep-plan` 的 human-in-loop 能力

---

## 11. 开放问题

1. **Revision 收敛策略**：Needs-Revision loop 是否有最大重试次数？如何避免 AI 和审批者之间的"无限乒乓"？
2. **Offline 支持**：Dashboard + WebSocket 架构在网络不稳定环境下的表现如何？是否有 offline-first 降级策略？
3. **审批权限**：当前审批是"任何能访问 dashboard 的人都可以审批"——是否需要 RBAC（角色权限控制）？
4. **MCP 标准演进**：MCP 协议尚在快速演进中，spec-workflow-mcp 如何跟进协议变更？
5. **Scale 上限**：单个 dashboard 管理的项目数量上限是多少？大规模使用时的性能基线？
