# Workflow Research Report: claude-code-spec-workflow

> **研究对象：** npm package `@pimzino/claude-code-spec-workflow` v1.5.9
> **研究日期：** 2025-07
> **分类：** Spec-driven development workflow framework

---

## 1. 框架概况

`claude-code-spec-workflow` 是一套基于 TypeScript + Node.js 构建的 **规格驱动开发工作流框架**，以 npm package 形式发布（`@pimzino/claude-code-spec-workflow`，当前版本 v1.5.9）。整个代码库包含 **198 个文件**，涵盖 CLI 入口、slash command 定义、模板系统、dashboard 可视化等模块。

框架提供两条主要入口：

| 入口类型 | 路径 | 说明 |
|----------|------|------|
| CLI 入口 | `src/cli.ts` | 通过 commander 注册的命令行工具，支持 setup、create、execute 等子命令 |
| Slash commands | `.claude/commands/` | 共 10 条：`spec-create`、`spec-execute`、`spec-status`、`spec-list`、`spec-steering-setup`、`bug-create`、`bug-analyze`、`bug-fix`、`bug-verify`、`bug-status` |

框架设计了两条独立工作流：**Spec workflow**（需求 → 设计 → 任务 → 实现，四阶段）和 **Bug workflow**（报告 → 分析 → 修复 → 验证，四阶段），各自拥有完整的状态机和阶段门控。值得注意的是，该项目的开发重心已向 MCP 版本迁移，Claude Code 版本的更新频率明显降低。

---

## 2. 源清单

以下为框架核心文件列表：

| 路径 | 规模 | 职责 |
|------|------|------|
| `src/cli.ts` | 主入口 | CLI 命令注册与分发，基于 commander 库 |
| `src/setup.ts` | 中型 | 项目初始化，创建 `.claude/` 目录结构，写入 spec-config.json |
| `src/commands.ts` | 大型 | 核心命令逻辑实现，包含 spec 和 bug 两套工作流的所有操作 |
| `src/task-generator.ts` | 中型 | 任务拆分引擎，将 design 转化为原子任务（1-3 文件，15-30 分钟） |
| `src/file-cache.ts` | 小型 | 文件缓存层，1 小时 TTL，减少重复读取 |
| `.claude/spec-config.json` | 配置 | 全局配置：`enforce_approval_workflow: true`, `agents_enabled: true` |
| `.claude/commands/spec-create.md` | slash cmd | 创建新 spec 的 slash command 定义 |
| `.claude/commands/spec-execute.md` | slash cmd | 执行 spec 任务的 slash command 定义 |
| `.claude/commands/bug-create.md` | slash cmd | 创建 bug 报告的 slash command 定义 |
| `.claude/templates/` | 目录 | 包含 requirements、design、tasks 等阶段模板 |
| `src/dashboard/` | 目录 | Fastify + WebSocket 实时仪表板 |

主要外部依赖包括：`fastify`（HTTP 服务）、`commander`（CLI 框架）、`inquirer`（交互式提示）、`chalk`（终端着色）、`simple-git`（Git 操作）、`chokidar`（文件监听）、`@ngrok/ngrok`（隧道穿透）。

---

## 3. 对象模型

### 核心实体

框架围绕以下实体组织：

- **Spec（规格）：** 顶层工作单元，包含 requirements、design、tasks 三份文档，存放在 `.claude/specs/<spec-name>/` 目录下。每个 Spec 拥有独立的状态（draft → requirements → design → tasks → implementation → completed）。
- **Task（任务）：** 由 task-generator 从 design 文档拆分而来的原子工作单元。每个 task 限制影响 1-3 个文件、预估耗时 15-30 分钟，确保变更的可审查性。
- **Bug：** 独立于 Spec 的缺陷追踪实体，包含 report、analysis、fix、verification 四个阶段产物。
- **Steering Documents（导航文档）：** 包含 `product.md`（产品方向）、`tech.md`（技术栈约定）、`structure.md`（目录结构说明），为所有 Spec 提供全局上下文。
- **Agent（验证代理）：** 四个专用代理 — `spec-requirements-validator`、`spec-design-validator`、`spec-task-validator`、`spec-task-executor`，各自负责对应阶段的质量门控。

### 关系与上下文隔离

Spec 之间相互独立，各自维护自己的文档目录。Steering documents 作为全局共享的只读上下文，通过 `getSteeringContext()` 函数加载，注入到所有 Spec 的处理流程中。任务执行采用 **one-task-at-a-time** 模式，避免并行执行导致的状态冲突。Agent 与 Spec 之间是多对一关系 — 四个 agent 按阶段依次介入同一个 Spec 的生命周期。

---

## 4. 流程与状态机

### Spec Workflow — Happy Path

```
Requirements → Design → Tasks → Implementation
    ↓              ↓          ↓           ↓
  起草需求      架构设计    任务拆分    逐任务执行
    ↓              ↓          ↓           ↓
  Agent 验证    Agent 验证  Agent 验证  Agent 执行
    ↓              ↓          ↓           ↓
  "✅ APPROVED"  "✅ APPROVED" "✅ APPROVED"  完成标记
```

1. **Requirements 阶段：** 用户通过 `spec-create` 发起，填充 requirements 模板。`spec-requirements-validator` agent 审查完整性，通过后在文档中标记 `✅ APPROVED`。
2. **Design 阶段：** 基于已批准的 requirements 编写架构设计。`spec-design-validator` agent 审查设计与需求的对齐性。
3. **Tasks 阶段：** `task-generator` 将设计文档拆分为原子任务列表，每个任务标注 `_Requirements: X.Y`（需求追溯）和 `_Leverage: path`（代码库复用提示）。`spec-task-validator` agent 验证任务完整性。
4. **Implementation 阶段：** `spec-task-executor` agent 按序执行任务，严格遵循 one-task-at-a-time 约束。每完成一个任务更新状态。

### Bug Workflow — Happy Path

```
Report → Analyze → Fix → Verify
```

Bug workflow 结构更简洁：`bug-create` 记录缺陷 → `bug-analyze` 定位根因 → `bug-fix` 实施修复 → `bug-verify` 验证结果。

### 失败路径

- **阶段审批被拒：** Agent 返回拒绝意见，用户必须修改文档后重新提交审批。流程停留在当前阶段，不允许跳过。
- **任务执行失败：** 单个 task 失败后整个 implementation 暂停，不会继续执行后续 task。
- **目录结构缺失：** `isInstallationComplete` 检查不通过时，所有工作流命令拒绝执行，强制用户先完成 setup。

---

## 5. 执行保障审计

| 保障机制 | Hard Gate | Soft Check | Unenforced |
|----------|-----------|------------|------------|
| 阶段审批门控（`✅ APPROVED` marker） | ✅ 必须在文档中出现 APPROVED 标记才能进入下一阶段 | | |
| 目录结构验证（`isInstallationComplete`） | ✅ 缺少 `.claude/` 结构时所有命令拒绝运行 | | |
| One-task-at-a-time 约束 | ✅ Agent 执行逻辑中硬编码的串行执行 | | |
| 任务原子性（1-3 文件，15-30 min） | | ✅ task-generator 生成时检查，但不阻止手动覆盖 | |
| Dashboard 只读访问控制 | ✅ Dashboard 端不暴露写操作接口 | | |
| 模板结构合规 | | ✅ 模板提供结构引导但不强制校验每个字段 | |
| 需求追溯（`_Requirements: X.Y`） | | ✅ task-generator 自动添加，但不验证引用有效性 | |
| 代码库复用提示（`_Leverage: path`） | | ✅ 提示性注解，不验证路径是否存在 | |
| Steering document 对齐 | | ✅ Agent 在验证时参考，但无量化一致性检测 | |
| `enforce_approval_workflow` 配置 | ✅ 当设为 true 时启用阶段审批 | | 当设为 false 时所有阶段门控被跳过 |
| Agent 启用控制（`agents_enabled`） | | | 关闭后退化为无验证的纯模板流程 |

---

## 6. Prompt 目录

### 6.1 spec-create slash command（关键摘录）

Spec 创建命令的核心 prompt 引导 Claude 按模板收集需求，并强调阶段性：

> "Create a new specification following the structured workflow. Start with requirements gathering using the provided template. Do NOT proceed to design until requirements are explicitly approved with ✅ APPROVED marker."

该 prompt 将阶段门控嵌入到自然语言指令中，依赖 Claude 的遵从性而非代码强制。

### 6.2 spec-task-executor agent prompt（关键摘录）

任务执行 agent 的 prompt 强调原子性和串行约束：

> "Execute exactly ONE task at a time. Each task should modify 1-3 files maximum. After completing a task, update its status before moving to the next. Never execute tasks in parallel."

这是 one-task-at-a-time 约束的 prompt 层实现，配合代码逻辑中的状态检查形成双重保障。

---

## 7. 微观设计亮点

### 7.1 Context Loading 的三层分离

框架将上下文加载拆分为三个独立函数：`getSteeringContext()`（产品/技术/结构的全局上下文）、`getSpecContext()`（当前 Spec 的需求/设计/任务文档）、`getTemplateContext()`（阶段模板）。这种分离使得不同粒度的上下文可以按需组合，避免了一次性加载所有内容导致的 token 浪费。

### 7.2 File Cache 的 1-hour TTL 策略

`file-cache.ts` 实现了一个简洁的文件级缓存，TTL 设为 1 小时。对于 Spec 工作流而言，文档在阶段内通常稳定不变（修改集中在阶段转换时），1 小时的 TTL 恰好覆盖了一个典型的任务执行周期，在性能和新鲜度之间取得了合理平衡。

### 7.3 任务原子性约束的量化标准

task-generator 为每个 task 设定了明确的量化边界 — **1-3 个文件**和 **15-30 分钟**的预估耗时。这不是模糊的"保持任务小"指导，而是可验证的具体指标，使得审查者和执行者都有清晰的预期。

---

## 8. 宏观设计亮点

### 8.1 Specification-as-Source-of-Truth 理念

整个框架的核心哲学是 **将规格文档作为唯一事实来源**。需求、设计、任务都以 Markdown 文件形式持久化在 `.claude/specs/` 中，所有状态转换都通过修改这些文件来记录。这种 document-centric 的设计意味着项目状态在任何时刻都是可读、可审计、可版本控制的，不依赖外部数据库或内存状态。

### 8.2 渐进式约束 — 从模板引导到 Agent 验证

框架采用了 **渐进式约束策略**：最外层是模板（提供结构化引导）、中间层是 prompt 指令（通过自然语言施加约束）、最内层是 agent 验证（通过代码逻辑实施检查）。这三层从"建议"到"强制"逐级升级，既不会在初始阶段过度限制用户，又在关键节点（阶段转换）确保质量门控。

---

## 9. 失败模式与局限

### 9.1 APPROVED Marker 的脆弱性

阶段门控依赖在 Markdown 文档中搜索 `✅ APPROVED` 字符串。用户可以手动插入该标记来绕过 agent 验证，系统没有签名或加密机制来防止这种篡改。这在协作环境中是一个显著的安全隐患。

### 9.2 Agent 验证的非确定性

四个 validator agent 的判断基于 LLM 推理，相同输入可能产生不同的审批结果。在边界情况下（例如需求描述模糊但技术上可行），agent 可能在不同运行中给出相反结论，导致工作流的可预测性降低。

### 9.3 开发重心迁移导致的维护风险

框架开发者已将重心转向 MCP 版本，Claude Code 版本的更新频率明显下降。这意味着该版本可能无法及时适配 Claude Code 的 API 变更或新功能，长期使用存在兼容性风险。

### 9.4 Dashboard 的运维复杂度

实时 dashboard 依赖 Fastify + WebSocket + ngrok/Cloudflare 隧道穿透，引入了大量运行时依赖和网络配置。对于大多数开发场景而言，这增加了不必要的运维复杂度，且隧道穿透可能引发安全顾虑。

### 9.5 单人工作流假设

One-task-at-a-time 约束和串行执行模型隐含了**单一开发者**的假设。在多人协作场景下，该框架缺乏并发控制和冲突解决机制，多个开发者无法同时在同一 Spec 的不同任务上工作。

---

## 10. 迁移评估

### 值得移植到 1st-cc-plugin 的候选项

| 候选项 | 目标插件 | 优先级 | 理由 |
|--------|----------|--------|------|
| 四阶段 Spec workflow 状态机 | `workflows/deep-plan` | 高 | deep-plan 当前缺少从需求到实现的完整工作流，Spec workflow 的阶段门控模式可补充其 Plan/Code 切换机制 |
| 任务原子性约束（1-3 文件 / 15-30 min） | `quality/meeseeks-vetted` | 中 | meeseeks-vetted 强调任务清晰度但缺少量化的原子性标准，该约束可增强其"verified work"检查 |
| Context loading 三层分离模式 | 通用模式（跨插件） | 中 | Steering / Spec / Template 的上下文分层策略可作为插件内上下文管理的参考架构 |
| Bug workflow 四阶段模型 | 新建 `workflows/bug-flow` 或扩展 `workflows/issue-driven-dev` | 低 | issue-flow 已有 Bug 三阶段支持，可评估是否需要增加 Verify 阶段 |

### 建议采纳顺序

1. **先移植设计理念**：将阶段门控和任务原子性的概念融入 deep-plan 和 meeseeks-vetted 的 SKILL.md 中，无需引入 TypeScript 依赖。
2. **再评估 Bug workflow**：对比 issue-flow 现有 Bug 流程与 spec-workflow 的 Bug 流程，决定是否需要补充 Verify 阶段。
3. **Dashboard 不建议移植**：运维复杂度高，与 Claude Code 的终端交互模式不契合。

---

## 11. 开放问题

1. **MCP 版本与 Claude Code 版本的功能差异有多大？** 如果 MCP 版本已实现更成熟的阶段门控机制，是否应直接研究 MCP 版本而非当前版本？
2. **APPROVED marker 是否可以用更可靠的机制替代？** 例如基于 Git commit hash 的阶段快照，或基于文件校验和的防篡改验证。
3. **任务原子性的 "1-3 文件 / 15-30 分钟" 标准是否经过实证验证？** 该标准是否适用于不同规模和类型的项目，还是仅适用于作者的特定场景？
4. **四个 validator agent 的 prompt 是否公开？** 如果能获取完整的 validator prompt，可以更精确地评估其验证覆盖范围和盲点。
5. **`enforce_approval_workflow: false` 的使用场景是什么？** 关闭审批流程后框架退化为纯模板系统，这种模式是否被视为正式支持的用法？
