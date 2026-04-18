# Workflow Research Report: spec-based-claude-code

> 逆向工程研究报告 — 生成时间：2025-07-18

---

## 1. 框架概况

| 维度 | 说明 |
|------|------|
| **类型** | Methodology Framework / 流程执行系统 |
| **文件数** | ~83 files（含示例 todo-app 实现） |
| **语言** | Markdown（模板与命令）+ Bash（命令脚本）|
| **入口** | `.claude/commands/spec/*.md`（10 个 slash commands）|
| **范式** | Spec-Driven Development (SDD)，四阶段顺序推进 |
| **状态存储** | 文件系统：marker files (`.requirements-approved` 等) |

这是一个**纯方法论框架**而非传统软件库。它通过 Claude Code 的 slash command 系统实施结构化开发流程，用文件系统中的 marker 文件作为 phase gate 的实体化凭证，强制 Requirements → Design → Tasks → Implementation 的顺序推进。

---

## 2. 源清单

| 文件 | 角色 | 行数 |
|------|------|------|
| `README.md` | 用户指南与方法论说明 | ~970 |
| `CLAUDE.md` | Claude Code 框架引导 | ~64 |
| `.claude/commands/spec/new.md` | 创建新 specification | — |
| `.claude/commands/spec/requirements.md` | 生成 requirements 模板 | — |
| `.claude/commands/spec/design.md` | 生成 design 文档 | — |
| `.claude/commands/spec/tasks.md` | 创建 task list | — |
| `.claude/commands/spec/approve.md` | 审批 phase | — |
| `.claude/commands/spec/implement.md` | 启动实现 | — |
| `.claude/commands/spec/status.md` | 显示项目状态 | — |
| `.claude/commands/spec/switch.md` | 切换活跃 spec | — |
| `.claude/commands/spec/update-task.md` | 更新 task 完成状态 | — |
| `.claude/commands/spec/review.md` | 审查当前 phase | — |
| `templates/requirements.md` | Requirements 模板 | — |
| `templates/design.md` | Design 模板 | — |
| `templates/tasks.md` | Tasks 模板 | — |
| `spec/.current-spec` | 活跃 spec 追踪器（纯文本） | 1 |

---

## 3. 对象模型

### 核心实体

```
Specification（spec/[ID]-[name]/）
├── README.md          — 元数据与状态概览
├── requirements.md    — WHAT：业务需求文档
├── design.md          — HOW：技术设计文档
├── tasks.md           — WHEN：实施任务清单
├── .requirements-approved  — Phase 1 gate marker
├── .design-approved        — Phase 2 gate marker
└── .tasks-approved         — Phase 3 gate marker
```

### 实体关系

- **Spec → Phase Documents**: 一对多，每个 spec 包含 3 个阶段文档
- **Phase → Approval Marker**: 一对一，marker file 是 gate 的物理凭证
- **Active Spec Tracker** (`spec/.current-spec`): 全局单例，决定所有命令的工作上下文
- **Task**: 嵌入 `tasks.md` 中的 Markdown checkbox (`- [ ]` / `- [x]`)

### Context Isolation

每个 spec 通过编号目录（`001-xxx`, `002-xxx`）隔离。`spec/.current-spec` 充当"焦点指针"，同一时刻只有一个活跃 spec。切换通过 `/spec:switch` 命令完成。

---

## 4. 流程与状态机

### Happy Path

```
/spec:new "feature-name"
    ↓ 创建 spec/001-feature-name/，设置 .current-spec
/spec:requirements
    ↓ 生成 requirements.md
/spec:approve requirements
    ↓ 创建 .requirements-approved marker
/spec:design
    ↓ 校验 .requirements-approved 存在 → 生成 design.md
/spec:approve design
    ↓ 创建 .design-approved marker
/spec:tasks
    ↓ 校验 .design-approved 存在 → 生成 tasks.md
/spec:approve tasks
    ↓ 创建 .tasks-approved marker
/spec:implement [phase]
    ↓ 校验 .tasks-approved → 按 task 逐步实现
/spec:update-task "task desc"
    ↓ 将 - [ ] 改为 - [x]
/spec:review
    ↓ 全面审查实现与 spec 的一致性
```

### 状态转移

| 当前状态 | 触发 | 目标状态 | 阻塞条件 |
|---------|------|---------|---------|
| Spec Created | `/spec:requirements` | Requirements Written | 无 |
| Requirements Written | `/spec:approve requirements` | Requirements Approved | 文档不完整 |
| Requirements Approved | `/spec:design` | Design Written | 缺少 `.requirements-approved` |
| Design Written | `/spec:approve design` | Design Approved | 文档不完整 |
| Design Approved | `/spec:tasks` | Tasks Written | 缺少 `.design-approved` |
| Tasks Written | `/spec:approve tasks` | Tasks Approved | 文档不完整 |
| Tasks Approved | `/spec:implement` | Implementation | 缺少 `.tasks-approved` |

### Failure Path

- **Phase 跳跃**：命令通过 `test -f` 检查 marker 文件，若前置 marker 不存在则拒绝执行并提示用户
- **Active spec 丢失**：`spec/.current-spec` 为空或不存在时，所有命令报错
- **Task 匹配失败**：`/spec:update-task` 使用模糊匹配，可能找不到目标 task

---

## 5. 执行保障审计

| 机制 | 级别 | 说明 |
|------|------|------|
| Phase gating（marker file 检查）| **Hard** | 命令前置 `test -f` 检查，缺失则拒绝执行 |
| `allowed-tools` frontmatter | **Hard** | 限定每个命令可用的 tool scope |
| Template 结构一致性 | **Soft** | 模板引导内容结构，但 LLM 可偏离 |
| 单活跃 spec 约束 | **Soft** | `.current-spec` 可被手动编辑绕过 |
| Task checkbox 格式 | **Soft** | 约定 `- [ ]` / `- [x]`，但无 parser 校验 |
| Review 流程 | **Unenforced** | `/spec:review` 纯建议性，无阻断能力 |
| Git commit 规范 | **Unenforced** | README 中建议但未强制 |

---

## 6. Prompt 目录

### Prompt 1: `/spec:design`（设计文档生成）

**触发条件**：用户调用 `/spec:design`，`.requirements-approved` 存在

**核心指令摘要**：
> 读取当前 spec 的 requirements.md，基于其内容创建全面的技术设计文档。包含 Architecture Overview（使用 ASCII art 或 mermaid 图表）、Technology Stack Decisions、Data Model and Schema、API Design、Security Considerations、Performance Considerations、Deployment Architecture、Technical Risks and Mitigations。

**工具约束**：`Bash(cat, test, ls), Write`

### Prompt 2: `/spec:approve`（阶段审批）

**触发条件**：用户调用 `/spec:approve [phase-name]`

**核心指令摘要**：
> 验证指定 phase 的文档存在，通过 `touch` 创建 `.${ARGUMENTS}-approved` marker 文件。完成后提示下一步骤（requirements → design, design → tasks, tasks → implementation）。

---

## 7. 微观设计亮点

### 7.1 Marker File 作为 Gate 凭证

审批状态不存于数据库或 JSON 中，而是物化为文件系统中的空文件（如 `.requirements-approved`）。这带来三重优势：
- **可 `git diff`**：审批事件自然进入版本控制
- **零依赖校验**：`test -f` 即可，无需 runtime
- **人类可读**：`ls -a` 即可看到全部审批状态

### 7.2 编号目录作为 Spec Registry

`001-feature-name` 的命名约定将 spec 的创建顺序编码进文件系统，提供了全局有序的 spec 注册表，且不需要任何元数据文件。

### 7.3 `allowed-tools` 精确限权

每个 slash command 在 frontmatter 中声明可用 tool 范围（如 `Bash(touch, test, cat)`），实现了最小权限原则——approve 命令只能创建 marker 文件，不能修改文档内容。

---

## 8. 宏观设计亮点

### 8.1 "文件系统即数据库"

整个框架没有引入任何运行时依赖——不需要 Node.js、Python 或数据库。所有状态都是文件系统中的 Markdown 文件和空 marker 文件。这使得框架可以在任何支持 Claude Code 的环境中即用。

### 8.2 "模板驱动，而非代码驱动"

框架的核心产出是一组 Markdown 模板和 slash command 定义。它不生成代码，而是生成**结构化文档**——Requirements、Design、Tasks——让 AI agent 在约束明确的上下文中工作。这是一种"先约束后生成"的哲学。

---

## 9. 失败模式与局限

| # | 失败模式 | 严重度 | 说明 |
|---|---------|--------|------|
| 1 | **Marker file 可手动创建** | Medium | 用户可直接 `touch .design-approved` 绕过 phase gate，无内容完整性校验 |
| 2 | **无并行 spec 支持** | Low | `.current-spec` 是全局单例，无法同时处理多个 spec |
| 3 | **Task 进度无聚合** | Medium | 缺少全局 dashboard，只能逐 spec 查看 task 完成度 |
| 4 | **文档质量无校验** | High | Approve 仅检查文件存在，不校验内容质量（空文件也可通过）|
| 5 | **无回退机制** | Medium | 一旦 approve 后发现错误，需手动删除 marker 文件才能"反审批" |
| 6 | **模板偏离无感知** | Low | LLM 生成的文档可能不完全遵循模板结构，但无机制检测偏离度 |

---

## 10. 迁移评估

### 可迁移候选

| 候选 | 价值 | 迁移难度 | 目标位置 |
|------|------|---------|---------|
| **Marker file gate 机制** | 零依赖的 phase 控制 | 低 | `1st-cc-plugin/` 中需要 phase gating 的 workflow |
| **Spec 目录编号约定** | 自然排序 + 全局 registry | 低 | 任何需要有序文档管理的插件 |
| **模板三件套**（requirements/design/tasks）| 结构化文档模板 | 中 | `workflows/deep-plan` 或新 SDD 插件 |
| **`allowed-tools` 限权模式** | 最小权限实践 | 低 | 所有 `1st-cc-plugin/` 插件的 slash command 定义 |

### 建议采纳顺序

1. **`allowed-tools` 精确限权** → 立即可用，改善现有插件安全性
2. **Marker file gate** → 适合引入 `workflows/deep-plan` 作为轻量 phase gate
3. **模板结构** → 参考其 requirements/design/tasks 三层模板丰富现有 SDD 流程

---

## 11. 开放问题

1. **Gate 质量校验**：marker file 仅证明"人类点了 approve"，能否引入内容完整性检查（如校验 requirements.md 包含必填 section）？
2. **多 spec 并行**：团队协作场景下 `.current-spec` 单点约束是否过强？是否需要引入 workspace 或 branch-aware 机制？
3. **Review 闭环**：`/spec:review` 的发现如何回流到文档修改？当前是纯输出，无结构化 feedback loop。
4. **与 CI 集成**：marker file 能否作为 CI 触发条件（如 `.tasks-approved` 存在时自动运行 scaffolding）？
