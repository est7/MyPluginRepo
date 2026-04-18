# Workflow Research Report: Hephaestus

> **研究日期**: 2025-07  
> **仓库**: Hephaestus  
> **文件数**: ~467  
> **许可证**: AGPL-3.0  

---

## 1. 框架概况

Hephaestus 是一个 **Python 3.11+** 编写的 self-writing AI workflow framework，核心理念是 **agents 在执行过程中动态发现并创建 task**——区别于传统 DAG 的预定义拓扑。框架通过 FastAPI MCP Server 提供 API，每个 agent 运行在独立的 tmux session + git worktree 中，由 Guardian（个体监控）和 Conductor（集体协调）两层监控系统保障执行质量。

| 属性 | 值 |
|------|------|
| **类型** | Semi-Structured Agentic Orchestration System |
| **语言** | Python 3.11+ (后端) + React/TypeScript (前端) |
| **入口** | FastAPI MCP Server (port 8000) |
| **核心模块** | `src/core/`, `src/mcp/`, `src/monitoring/`, `sub_agents/` |
| **存储** | SQLite (SQLAlchemy ORM) + Qdrant (vector DB, RAG) |
| **部署模式** | Headless CLI / TUI (Textual) / Web UI (React + Vite, port 3000) |

---

## 2. 源清单

| 文件/目录 | 用途 | 重要度 |
|-----------|------|--------|
| `src/mcp/server.py` | FastAPI MCP Server，所有 agent↔系统的 API 入口 | ★★★ |
| `src/core/models.py` | SQLAlchemy ORM 模型 (Agent, Task, Workflow, Phase, Memory) | ★★★ |
| `src/core/worktree_manager.py` | Git worktree 隔离管理 | ★★★ |
| `src/monitoring/guardian.py` | 个体 agent trajectory thinking 监控 | ★★★ |
| `src/monitoring/conductor.py` | 集体 agent 协调与冲突检测 | ★★★ |
| `src/core/queue_service.py` | Task 优先级队列与去重 | ★★☆ |
| `src/core/agent_manager.py` | Agent 生命周期管理 (spawn/terminate) | ★★☆ |
| `src/memory/rag.py` | Qdrant RAG 跨 agent 知识检索 | ★★☆ |
| `sub_agents/` | Agent 类型定义 (phase/validator/monitor) | ★★☆ |
| `frontend/` | React Web UI (dashboard, task board, agent monitor) | ★☆☆ |

---

## 3. 对象模型

### 核心实体与字段

```
Agent
  ├── id, status: idle|working|stuck|terminated
  ├── agent_type: phase|validator|result_validator|monitor|diagnostic
  ├── tmux_session_name, system_prompt, cli_type
  ├── current_task_id, health_check_failures
  └── kept_alive_for_validation: bool

Task
  ├── id, raw_description, enriched_description, done_definition
  ├── status: pending → queued → blocked → assigned → in_progress
  │          → under_review → validation_in_progress → needs_work → done|failed|duplicated
  ├── priority, phase_id, workflow_id
  ├── created_by_agent_id, assigned_agent_id, parent_task_id
  ├── embedding, related_task_ids, duplicate_of_task_id, similarity_score
  └── validation_enabled, validation_iteration, review_done

Workflow
  ├── id, name, status: active|completed|failed|paused
  ├── phases_folder_path
  └── phases: Phase[]

Phase
  ├── name, description, done_definitions[]
  ├── cli_tool, cli_model (per-phase override)
  └── validation: ValidationCriteria?

Memory
  ├── id, content, memory_type: error_fix|discovery|decision|learning|warning|codebase_knowledge
  ├── agent_id, task_id, workflow_id
  └── embedding (Qdrant vector indexed)
```

### 实体关系

- **Workflow** 1:N **Phase**（有序）
- **Phase** 1:N **Task**（动态生成）
- **Agent** 1:1 **Task**（当前分配）
- **Agent** N:N **Task**（通过 `created_by_agent_id` 可创建多个 task）
- **Task** 1:N **ValidationReview**（多轮验证）
- **Task** 1:N **AgentResult**（交付物）
- **Memory** 多对多关联 Agent/Task/Workflow

### Context 隔离

每个 agent 运行在独立的 **git worktree** + **tmux session** 中，具有隔离的文件系统和 CLI 环境。Agent 间通过 MCP API + Qdrant Memory 间接通信，无直接 IPC。

---

## 4. 流程与状态机

### Happy Path

```
[用户] 定义 Workflow YAML (phases + done_definitions)
   ↓
[系统] 启动 Workflow → 创建 Phase 1 初始 Task
   ↓
[Phase 1 Agent] 分析需求 → 调用 create_task API 动态创建 Task
   ↓
[Task Enrichment Pipeline]
   raw → LLM enrichment → queued → similarity dedup → assigned
   ↓
[Phase 2 Agent] 在独立 worktree 中实现 → save_memory → report_results
   ↓
[Validator Agent] 验证 → give_validation_review
   ├── pass → Task done
   └── fail → needs_work → 重新分配
   ↓
[Phase 3 Agent] 提交 submit_result → ResultValidator 检查
   ↓
[Conductor] 检测 on_result_found == "stop_all" → Workflow completed
```

### Task 状态机

```
pending → queued → assigned → in_progress
                                  ↓
                         under_review → validation_in_progress
                                  ↓              ↓
                               done          needs_work → in_progress (循环)
                                              failed
                                              duplicated
```

### Failure Paths

| 失败场景 | 系统响应 |
|----------|----------|
| Agent stuck | Guardian 检测 health_check_failures → steering intervention |
| Agent drift | Guardian trajectory analysis → 发送 nudge 指令 |
| Duplicate work | TaskSimilarityService 检测 → 标记 duplicated |
| Validation fail | Task → needs_work → 重新分配修复 agent |
| Agent crash | tmux session 异常 → AgentManager 重新 spawn |

---

## 5. 执行保障审计

| 机制 | 级别 | 说明 |
|------|------|------|
| Git Worktree 隔离 | **Hard** | 每个 agent 独立分支，物理隔离文件系统 |
| Task Dedup (Embedding) | **Hard** | Qdrant cosine similarity 自动检测重复 task |
| Validation Loop | **Hard** | validator agent 必须 approve 才能标记 done |
| Guardian Trajectory Monitoring | **Hard** | LLM 分析 agent output，检测 drift/stuck |
| Conductor Coherence Analysis | **Hard** | 跨 agent 协调，检测 duplicate work |
| Phase done_definitions | **Soft** | Phase 完成条件由 LLM 判定，无 deterministic check |
| Task Priority Queue | **Soft** | 优先级排序但无严格 blocking |
| Memory RAG | **Soft** | 跨 agent 知识共享依赖 embedding 质量 |
| Result Validator Protection | **Hard** | result_validator 类型的 agent 不可被 Conductor terminate |

---

## 6. Prompt 目录

### Prompt 1: Agent System Prompt（动态生成）

每个 agent 的 system prompt 由 LLM 根据以下输入动态生成：

```
输入:
  - Task description + done_definition
  - Phase context (name, constraints, position in workflow)
  - Relevant Memories (RAG retrieval from Qdrant)
  - Available MCP tools (create_task, save_memory, report_results...)

输出:
  - 定制化的 system prompt，包含任务目标、约束、可用工具说明
```

**特征**: 无固定 prompt 模板，完全由 LLM 根据上下文动态构建。

### Prompt 2: Guardian Trajectory Analysis

```
分析以下 agent 的工作轨迹:
- Agent output: {tmux_output}
- Accumulated context: {past_summaries}
- Task info: {task_dict}
- Phase constraints: {phase_info}

判断:
1. current_phase: agent 当前处于什么阶段
2. trajectory_aligned: 是否与任务目标对齐
3. alignment_issues: 具体偏离问题
4. steering_recommendation: 纠正建议
```

---

## 7. 微观设计亮点

### 7.1 Task Enrichment Pipeline

原始 task description 经过 LLM enrichment 后产出结构化描述、完成标准、复杂度估算和能力需求。这一 pipeline 弥补了 agent 创建 task 时描述不精确的问题。

### 7.2 Trajectory Thinking 监控

Guardian 不是简单的 heartbeat 检测，而是使用 LLM 分析 agent 的 **完整工作轨迹**（accumulated context + past summaries），实现语义级别的 drift 检测和 steering。

### 7.3 Protected Validator Agents

`result_validator` 类型的 agent 被系统保护，Conductor 在执行 terminate 决策时会跳过这类 agent，避免验证流程被意外中断。

---

## 8. 宏观设计亮点

### 8.1 "Agent 自我发现 Task" 的动态 DAG

传统 workflow engine 要求预定义所有 task 和依赖关系。Hephaestus 允许 agent 在执行过程中 **发现新工作并创建 task**——例如测试 agent 发现 caching 优化机会后，通过 `create_task` API 将其路由回 Phase 1 重新分析。这使 workflow 拓扑在运行时动态扩展。

### 8.2 双层监控 (Guardian + Conductor)

Guardian 关注**个体轨迹**（单 agent 是否偏离目标），Conductor 关注**集体协调**（多 agent 是否做重复工作、是否有资源冲突）。这种分层设计避免了单层监控的信息过载问题。

---

## 9. 失败模式与局限

| # | 失败模式 | 严重度 | 说明 |
|---|----------|--------|------|
| 1 | **Task explosion** | 高 | Agent 可无限创建 task，缺少 budget 或 rate limit |
| 2 | **LLM 判定的 Phase 完成** | 高 | done_definitions 由 LLM 语义判断，非 deterministic，可能误判 |
| 3 | **Guardian/Conductor LLM 依赖** | 高 | 监控系统本身依赖 LLM 分析，LLM 出错则监控失效 |
| 4 | **Qdrant 单点故障** | 中 | Memory RAG 和 Task Dedup 均依赖 Qdrant，服务不可用时降级策略不明确 |
| 5 | **tmux session 管理复杂度** | 中 | 大量并发 agent 时 tmux session 管理可能成为瓶颈 |
| 6 | **AGPL-3.0 限制** | 中 | 商业集成需要开源修改版本，影响采纳 |
| 7 | **前端与后端耦合** | 低 | React 前端与 FastAPI 后端通过 WebSocket 紧密绑定 |

---

## 10. 迁移评估

### 可迁移候选

| 机制 | 目标插件 | 可行性 | 备注 |
|------|----------|--------|------|
| Dynamic Task Discovery API | `workflows/superpower` | ★★☆ | 概念可借鉴，但需简化为 file-based |
| Guardian Trajectory Monitoring | `quality/ai-hygiene` | ★★☆ | Drift 检测逻辑可移植为 review skill |
| Git Worktree Isolation | `vcs/git` | ★★★ | worktree 管理 skill 高度可复用 |
| Task Enrichment Pipeline | `workflows/deep-plan` | ★★☆ | 任务描述增强可作为 planning 辅助 |
| RAG Memory System | `integrations/utils` | ★☆☆ | 过于重量级，需 Qdrant 依赖 |

### 建议采纳顺序

1. **Git Worktree Isolation** → 提取 worktree 创建/清理逻辑为独立 skill
2. **Guardian Drift Detection** → 简化为 prompt-based 的 review checklist
3. **Dynamic Task Discovery** → 研究是否可用 file-based task list 替代 API

---

## 11. 开放问题

1. **Task explosion 防护**: 是否有 task 创建速率限制或 budget 控制？文档中未见相关配置。
2. **Agent 间直接通信**: 当前 agent 只能通过 MCP API 间接通信，是否考虑 agent-to-agent 直接消息机制？
3. **Workflow 恢复**: 系统崩溃后 Workflow 恢复策略是什么？SQLite 数据是否包含足够的重启信息？
4. **LLM 成本控制**: Guardian + Conductor + Enrichment 三层均消耗 LLM API，长时间运行的 workflow 成本如何控制？
5. **AGPL 合规**: 是否有计划提供更宽松的许可证选项？
