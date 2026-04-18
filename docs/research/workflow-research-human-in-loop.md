# Workflow Research Report: human-in-loop

> **研究日期**: 2025-07  
> **仓库**: human-in-loop  
> **文件数**: ~263  
> **许可证**: 未明确声明  

---

## 1. 框架概况

human-in-loop 是一个面向 Claude Code 的 **Specification-Driven Development (SDD)** 基础设施，核心思想是 **人类控制架构决策，AI 执行实现**。系统结合了 Python 编写的 deterministic DAG 执行引擎 (`humaninloop_brain`) 和一套 Claude Code skill/command 定义，强制执行 Setup → Specify → Plan → Tasks → Implement 的 5 阶段流程，每个关键转换点都有 human approval gate。

| 属性 | 值 |
|------|------|
| **类型** | Spec-Driven Development Infrastructure + Claude Code Plugin |
| **语言** | Python (DAG engine) + Markdown (skill 定义) |
| **入口** | Claude Code commands (`/setup`, `/specify`, `/plan`, `/tasks`, `/implement`) |
| **核心模块** | `humaninloop_brain/` (Python DAG), `.spec/` (artifact 存储), `commands/` |
| **Artifact 目录** | `.spec/` 项目级目录 |
| **文档** | ROADMAP.md 详述演进计划 |

---

## 2. 源清单

| 文件/目录 | 用途 | 重要度 |
|-----------|------|--------|
| `CLAUDE.md` | Claude Code 总配置入口 | ★★★ |
| `commands/setup.md` | Phase 1: 项目初始化 command | ★★★ |
| `commands/specify.md` | Phase 2: 需求规约 command | ★★★ |
| `commands/plan.md` | Phase 3: 架构规划 command | ★★★ |
| `commands/tasks.md` | Phase 4: 任务分解 command | ★★★ |
| `commands/implement.md` | Phase 5: 实现 command | ★★★ |
| `humaninloop_brain/` | Python DAG 执行引擎 | ★★★ |
| `.spec/` | 规约 artifact 存储目录 | ★★★ |
| `ROADMAP.md` | 项目演进路线图 | ★★☆ |
| `skills/` | 辅助 skill 定义 | ★★☆ |

---

## 3. 对象模型

### 核心实体

```
Project
  ├── .spec/ directory (artifact 根目录)
  ├── setup_complete: bool
  └── current_phase: enum

Specification (.spec/specs/)
  ├── id: string
  ├── title, description
  ├── requirements: Requirement[]
  ├── status: draft|approved|implemented
  └── approval: HumanApproval?

Plan (.spec/plans/)
  ├── architecture_decisions: Decision[]
  ├── component_breakdown: Component[]
  ├── dependency_graph: DAG
  └── approval: HumanApproval?

TaskList (.spec/tasks/)
  ├── tasks: Task[]
  ├── execution_order: number[]
  └── approval: HumanApproval?

Task
  ├── id, title, description
  ├── status: pending|in_progress|done|blocked
  ├── depends_on: TaskId[]
  ├── spec_ref: SpecId
  └── implementation_notes: string?

HumanApproval
  ├── approved: bool
  ├── feedback: string?
  ├── timestamp: datetime
  └── approver: string
```

### 实体关系

- **Project** 1:N **Specification**
- **Specification** 1:1 **Plan**（一个 spec 对应一个架构方案）
- **Plan** 1:N **Task**
- **Task** N:N **Task**（通过 depends_on 形成 DAG）

### Context 隔离

所有 artifact 持久化到 `.spec/` 目录，每个 phase 的输出作为下一 phase 的输入。Phase 间通过文件系统传递上下文，不依赖 LLM 的 context window。

---

## 4. 流程与状态机

### Happy Path (5-Phase Pipeline)

```
[Phase 1: Setup]
   /setup → 检测项目环境 → 创建 .spec/ 目录结构
   → 生成项目 metadata
   ↓
[Phase 2: Specify]  ← Human Approval Gate
   /specify → AI 辅助编写需求规约
   → 人类审核 spec → approve / request changes
   ↓
[Phase 3: Plan]  ← Human Approval Gate
   /plan → AI 基于 approved spec 生成架构方案
   → 人类审核 plan → approve / request changes
   ↓
[Phase 4: Tasks]  ← Human Approval Gate
   /tasks → AI 将 plan 分解为有序 task 列表
   → 人类审核 task 列表 → approve / request changes
   ↓
[Phase 5: Implement]
   /implement → AI 按 DAG 顺序逐个实现 task
   → 每个 task 完成后更新 status
   → 全部 done → 项目完成
```

### Phase 状态转移

```
Setup ──(setup_complete)-→ Specify
Specify ──(spec_approved)-→ Plan
Specify ←─(changes_requested)── Plan [回退]
Plan ──(plan_approved)-→ Tasks
Plan ←─(changes_requested)── Tasks [回退]
Tasks ──(tasks_approved)-→ Implement
Implement ──(all_tasks_done)-→ Complete
Implement ──(task_blocked)-→ [等待依赖 / 人工介入]
```

### Failure Paths

| 失败场景 | 系统响应 |
|----------|----------|
| Spec 未通过审核 | 返回 Specify phase，AI 根据 feedback 修改 |
| Plan 不合理 | 返回 Plan phase，可能级联回 Specify |
| Task 依赖阻塞 | DAG engine 跳过 blocked task，继续可执行项 |
| 实现偏离 spec | 人工在 review 中发现，触发修正 |

---

## 5. 执行保障审计

| 机制 | 级别 | 说明 |
|------|------|------|
| Phase 顺序强制 | **Hard** | DAG engine 严格阻止跳过 phase |
| Human Approval Gate | **Hard** | Specify/Plan/Tasks 三个阶段需人类 approve 才能继续 |
| `.spec/` 文件持久化 | **Hard** | 所有 artifact 写入文件系统，可审计、可回溯 |
| Task DAG 依赖 | **Hard** | DAG engine 尊重 depends_on 顺序 |
| Spec-Implementation 对齐 | **Soft** | Implement 阶段的 prompt 引用 spec，但无自动 diff 校验 |
| Task completion criteria | **Soft** | done 状态由 AI 自行判定 |
| Feedback loop | **Soft** | 人类 feedback 通过文本传递，无结构化 schema |

---

## 6. Prompt 目录

### Prompt 1: /specify（需求规约）

```
基于项目上下文 (.spec/metadata)，编写详细的需求规约：
1. 功能需求 (Functional Requirements)
2. 非功能需求 (Non-Functional Requirements)
3. 约束条件 (Constraints)
4. 验收标准 (Acceptance Criteria)

输出到 .spec/specs/{name}.md
等待人类审核并处理 feedback。
```

**特征**: 结构化输出要求 + 人类审核门控 + 文件持久化。

### Prompt 2: /implement（DAG 实现）

```
读取 .spec/tasks/ 中的 approved task 列表。
按 DAG 顺序执行:
  1. 选择无未完成依赖的下一个 pending task
  2. 读取对应的 spec 和 plan 作为上下文
  3. 实现 task
  4. 标记 status: done
  5. 重复直到所有 task 完成

遵循 plan 中的架构决策，不偏离 spec 要求。
```

---

## 7. 微观设计亮点

### 7.1 Python DAG Engine (`humaninloop_brain`)

用 Python 实现的 deterministic DAG 执行器，不依赖 LLM 进行拓扑排序和依赖解析。这确保了 task 执行顺序的确定性——即使 LLM 输出不稳定，DAG 引擎的行为也是可预测的。

### 7.2 `.spec/` 作为 Single Source of Truth

所有阶段产出（spec、plan、task list）均以 Markdown 文件形式存储在 `.spec/` 目录。这实现了：
- **可审计**: git diff 可追踪所有变更
- **可恢复**: context window 清空后可从文件重建上下文
- **可协作**: 多人可通过 git 共同编辑 spec

### 7.3 三级审批门控

Specify、Plan、Tasks 三个阶段各设一个 human approval gate，形成渐进式承诺（progressive commitment）——用户在 scope 逐步收窄的过程中保持控制权。

---

## 8. 宏观设计亮点

### 8.1 "Human Controls Architecture, AI Executes" 分权模型

框架将创造性决策（需求定义、架构选择、任务分解）留给人类审批，将机械性执行（代码实现）交给 AI。这种分权模型承认了当前 LLM 在高层决策上的不可靠性，同时最大化了 AI 在实现层面的效率。

### 8.2 Spec 作为合约

`.spec/` 目录中的 approved spec 作为 AI 实现的"合约"——AI 必须在 spec 定义的边界内工作。这种 contract-driven development 思路与传统的 Design by Contract 一脉相承，但将 contract 的形式从代码注解扩展到了自然语言规约。

---

## 9. 失败模式与局限

| # | 失败模式 | 严重度 | 说明 |
|---|----------|--------|------|
| 1 | **Approval bottleneck** | 高 | 三个 human gate 意味着每个功能至少需要 3 次人工审核，小型任务的 overhead 过高 |
| 2 | **Spec-Implementation drift** | 中 | Implement 阶段无自动化对齐检查，AI 可能在实现中偏离 approved spec |
| 3 | **DAG 粒度固定** | 中 | Task 分解后不支持动态新增 task，发现新需求需回退到 Tasks phase |
| 4 | **无增量 spec 更新** | 中 | Spec 修改需重走 Specify → Plan → Tasks 流程，变更成本高 |
| 5 | **Python engine 安装成本** | 低 | `humaninloop_brain` 需要 Python 环境，增加了非 Python 项目的安装摩擦 |
| 6 | **单线程实现** | 低 | 当前设计为顺序执行 task，不支持并行实现 |

---

## 10. 迁移评估

### 可迁移候选

| 机制 | 目标插件 | 可行性 | 备注 |
|------|----------|--------|------|
| 5-Phase Pipeline | `workflows/deep-plan` | ★★★ | 阶段定义可直接对齐 deep-plan 的 Plan/Code mode |
| Human Approval Gate | `quality/meeseeks-vetted` | ★★★ | 审批机制与 meeseeks 的 "verified work" 门控互补 |
| `.spec/` Artifact Structure | `integrations/project-init` | ★★☆ | 可作为项目初始化的 spec 目录模板 |
| DAG Task Execution | `workflows/issue-driven-dev` | ★★☆ | DAG 顺序执行可增强 issue-flow 的依赖管理 |
| Progressive Commitment | 新增 skill | ★☆☆ | 理念可借鉴但需框架级支持 |

### 建议采纳顺序

1. **Human Approval Gate pattern** → 提取为可复用的 review checkpoint skill
2. **`.spec/` Artifact Structure** → 标准化 spec 目录模板供多个插件复用
3. **5-Phase Pipeline** → 简化后融入 deep-plan 的 workflow 定义

---

## 11. 开放问题

1. **轻量级模式**: 是否有计划提供跳过部分审批门的"快速模式"，适用于小型 bugfix？
2. **Spec 版本控制**: `.spec/` 目录的变更是否有语义化版本管理？多人协作时如何处理冲突？
3. **DAG 可视化**: 是否提供 task DAG 的可视化工具？复杂项目中 task 依赖难以纯文本理解。
4. **与 CI/CD 集成**: 是否有计划将 spec 验证集成到 CI pipeline（如 PR 时自动检查 spec 对齐）？
5. **ROADMAP 优先级**: ROADMAP.md 中的哪些功能是下一个 release 的重点？
