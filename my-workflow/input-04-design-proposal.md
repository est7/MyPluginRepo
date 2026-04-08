# 第三方评审与工作流核心骨架设计方案

> **文档定位**: 响应 `workflow-design-third-party-review-brief.md` 的架构设计提案。
> **设计基准**: 严格遵循“先冻结最大完整骨架，Profile 只做减法”的原则，彻底摒弃“Spec 作为长期记忆”的模式，采用以 Acceptance/Backflow 为核心的持久化策略。综合了 GSD、Trellis、Flowspec、Yoyo-Evolve 等 8 份前沿 Agent 框架的研究报告。

---

## 1. 核心 Phase Graph (最大完整骨架)

我们定义一个包含 6 个阶段的**最大状态机 (Maximal Skeleton)**。所有的复杂性 Profile (`trivial`, `simple`, `moderate`, `complex`, `harness`) 都在这个固定骨架上运行，低复杂度 Profile 仅通过“状态透传 (Pass-through)”或“降级执行 (Downgrade)”来跳过或简化特定阶段，**系统绝不动态增加新的 Phase**。

### 1.1 骨架阶段定义

1. **Phase 0: Triage & Setup (前置收容)**
   *   **职责**: 评估任务复杂度 (借鉴 Flowspec 的 Assess 机制)，确定对应的 Profile，加载必需的 Durable Docs。
2. **Phase 1: Discovery & Spec (规格探索 - Transient)**
   *   **职责**: 澄清需求，生成执行期专用的临时 Spec。
3. **Phase 2: Architecture & Plan (架构与计划 - Decision & Transient)**
   *   **职责**: 基于 Spec 触发必要的 ADR 编写，并生成结构化的任务分解图 (借鉴 Everything Mobile 的 Task DAG / Plan JSON)。
4. **Phase 3: Execute & Check (执行与内循环 - Mutation)**
   *   **职责**: 具体的代码生成、外部模型脏原型重构 (Dirty Prototype Refactoring)。核心约束：**状态扭转必须通过确定性 CLI 工具** (借鉴 GSD 的 Deterministic State Mutation Boundary)。
5. **Phase 4: Verify & Gate (验证门控 - Hard Gate)**
   *   **职责**: 运行三层检查点 (Quick/Standard/Full)，执行 Pass@k 验证，以及 Ralph Loop 防逃逸检查 (借鉴 Trellis)。
6. **Phase 5: Settlement & Backflow (结算与回流 - Durable)**
   *   **职责**: 任务验收，生成 Acceptance Settlement，萃取知识更新 Durable Docs，销毁/归档 Transient 产物 (Spec/Plan)。

### 1.2 Profile 裁剪矩阵 (The Subtraction Model)

| Phase | Trivial (例如: 拼写修正) | Simple (例如: 新增单一函数) | Moderate (例如: 新增 CRUD API) | Complex (例如: 跨模块重构) | Harness (例如: 大型史诗特性) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **0. Triage** | ✅ 自动极速定级 | ✅ 自动定级 | ✅ 自动定级 | ✅ 强制人工确认 | ✅ 强制人工确认 |
| **1. Spec** | ⏭️ 透传 (Skip) | ⬇️ 降级 (仅 1 句话目标) | ✅ 标准 Spec | ✅ Full Spec + Rubric 打分 | ✅ 强制多次 Review |
| **2. Plan** | ⏭️ 透传 (Skip) | ⏭️ 透传 (无 ADR/DAG) | ⬇️ 降级 (单节点 Plan) | ✅ ADR 评估 + Task DAG | ✅ 架构师 Agent 强审 |
| **3. Execute** | ✅ 直接修改 | ✅ 单步修改 | ✅ 顺序执行 | ✅ 依据 DAG 编排/并发 | ✅ Worktree 隔离并发 |
| **4. Verify** | ⬇️ Quick Check | ✅ Standard Check | ✅ Full Check | ✅ Full + Pass@k | ✅ 强制人工 UAT |
| **5. Backflow**| ⏭️ 透传 (无沉淀) | ⬇️ 仅记录 Commit | ✅ 结算接口变更 | ✅ 深度提炼架构与不变量 | ✅ 完整 Retrospective |

> **机制借鉴**: 参考 *Flowspec* 的复杂度自适应工作流，但以固定骨架+掩码 (Masking) 的方式实现，确保状态机的绝对刚性。

---

## 2. Artifact Model (产物模型)

严格执行 Brief 要求的文档分级。**所有 Transient 产物在 Phase 5 结束后对后续任务隐身**。

### 2.1 Transient Artifacts (执行期临时产物)
*   **包含**: `spec.md`, `plan.json` (借鉴 *Everything Mobile* 的 Plan JSON as Protocol)。
*   **生命周期**: Phase 1/2 创建 -> Phase 3 消费 -> Phase 5 彻底销毁或移入不可见的 `.archive/`。
*   **核心作用**: 作为 Agent 间的短期通信协议。**绝不作为下一次任务的 Context 召回源**，杜绝 Spec 腐化造成的上下文噪音。

### 2.2 Decision Artifacts (决策产物)
*   **包含**: `docs/adr/XXXX-title.md`, `decision-log.jsonl`
*   **生命周期**: Phase 2 创建 (仅当检测到跨越预定架构边界或引入新依赖时) -> 永久保留，但置于低权重上下文或由专门脚本按需加载。
*   **生成规则**: 引入“ADR 触发器”。Simple 任务禁止生成 ADR；Complex 任务只有当 Plan 涉及到核心边界改变时才强制生成 ADR，避免 Ceremony 成本过高。

### 2.3 Durable Artifacts (长期记忆产物)
*   **包含**: `docs/architecture.md`, `docs/interfaces.md`, `docs/invariants.md` (不变量), `active_learnings.md`
*   **生命周期**: 随项目存在，在 Phase 5 (Backflow) 被**增量 Patch 更新**。
*   **消费方式**: 在 Phase 0 通过类似 *Trellis* 的 `JSONL-driven Context Injection` 机制，按需精确注入给下一个任务的 Agent，绝不依赖全量堆积的 Session 日志。

---

## 3. Gate & Enforcement Model (门控与强制模型)

依据对 GSD 和 Trellis 的逆向工程，纯 Prompt 的软约束最终都会失效，必须引入拦截维度的 Hard Gate。

| Gate 节点 | 类型 | 触发时机 | 执行机制与要求 | Profile 启用情况 |
| :--- | :--- | :--- | :--- | :--- |
| **G1: State Mutation Boundary** | **Hard** | Any Phase | **核心必选项**: 借鉴 *GSD*，AI 绝对禁止直接使用 Write/Edit 工具修改工作流状态文件。任务状态推进必须通过确定性的 CLI 命令 (如 `workflow advance`) 触发。 | All Profiles |
| **G2: Prompt Injection Scan** | **Hard** | P0/P1 | **核心必选项**: 借鉴 *Yoyo-Evolve* 的 Boundary Nonce，在读取外部 Issue、第三方代码或未授信 Spec 前进行扫描，切断越权注入。 | All Profiles |
| **G3: Spec Rubric Evaluator** | Soft/Opt | P1 结束 | **核心可选项**: 使用 LLM 作为一个独立 Evaluator 对生成的 Spec 进行 10 项基准打分，低于阈值打回重写。 | Moderate, Complex |
| **G4: 3-Layer Checkpoints** | **Hard** | P3 -> P4 | **核心必选项**: `Quick` (Lint/Format) -> `Standard` (Unit Tests) -> `Full` (Integration/Coverage)。根据 Profile 必须跑通对应的 Checkpoint 脚本。 | All (按层级降级) |
| **G5: Ralph Loop 逃逸检查** | **Hard** | P4 结束 | 借鉴 *Trellis*：Agent 不能仅仅回复 "Looks good / Done"，必须由 SubagentStop Hook 拦截，检测到实际的 Verify Command 成功执行的 Evidence 才能退出内循环。 | Moderate, Complex |

---

## 4. Acceptance & Backflow Design (验收与知识回流方案)

这是解决“Spec 作为长期记忆导致 Context Rot”的终极解药，也是对 Brief 中第 3 和第 4 个问题的核心回应。

### 4.1 任务结算契约 (Acceptance Settlement Schema)
在 Phase 5，系统强制要求 Agent 生成一份标准的 `settlement.json` (或 YAML)。这彻底取代了长篇大论的旧 Spec。

```json
{
  "task_id": "T-1024",
  "execution_status": "success",
  "api_contract_changes": [
    { "type": "added", "entity": "UserService.getUser", "signature": "..." }
  ],
  "new_invariants_discovered": [
    "User ID must now always be UUID v4, integer IDs are deprecated."
  ],
  "dependencies_added": ["zod@3.21.0"],
  "retrospective_lessons": "Previous assumption about local caching was wrong, shifted to Redis to avoid OOM."
}
```

### 4.2 回流规则 (Backflow Rules)
1. **API & 不变量提炼**: 独立的 `Backflow Agent` (或确定的 Python/TS 脚本) 读取 `settlement.json`，并将 `api_contract_changes` 和 `new_invariants_discovered` **定向 Patch** 到全局的 `docs/interfaces.md` 和 `docs/invariants.md` 中。
2. **经验降维压缩 (借鉴 Yoyo-Evolve)**: 将 `retrospective_lessons` 写入 `lessons.jsonl` (Append-only)，并通过 Daily/Task-end Synthesis 压缩成高密度的 `active_learnings.md`，剔除中间的推理噪音。
3. **Spec 销毁**: Backflow 完成后，原始的 `spec.md` 与 `plan.json` 被彻底归档或删除，**永远不会出现在下一次任务的 Context 中**。

### 4.3 下续任务的 Context 加载
当下一个任务 (Phase 0) 开始时，系统默认加载：
*   `docs/architecture.md` (高层视点)
*   `docs/invariants.md` (项目铁律)
*   `active_learnings.md` (近期经验萃取)

以此保证，Durable Docs 永远是干净、无推导过程的“当前世界真相 (Source of Truth)”。

---

## 5. Extensibility Model (扩展性模型)

明确回答“哪些属于核心框架，哪些属于插件扩展，哪些坚决排斥”。

### 5.1 Core Required (必须硬编码进入核心引擎的逻辑)
*   **状态机引擎与 Phase Graph**: 6 阶段的流转逻辑不可更改，仅支持跳过和降级。
*   **Deterministic State Mutation Boundary**: 状态推进的确定性 CLI 工具接口。
*   **Sprint/Execution Contract Slot**: Plan 阶段的 DAG Schema 和 Settlement 阶段的 Schema 解析器。
*   **3-Layer Checkpoints**: 基础的门控拦截器框架 (执行的具体脚本可以外置)。
*   **Task-end Backflow Engine**: 结算数据的抽取与 Durable Docs 的更新器。
*   **Prompt Injection Scan**: 基础输入防御机制。

### 5.2 Core Optional (核心引擎支持，但可通过 Profile 选项关闭)
*   **外部模型“脏原型”重构路径**: (借鉴 *ccg-workflow*) 允许使用较弱模型生成代码，强模型 (Claude) 执行审查与重构。
*   **Pass@k / Reliability Metric**: 在 P4 验证阶段多次运行测试以排除 Flaky Tests。
*   **Rubric Evaluator**: P1/P2 阶段对 Spec/Plan 的结构化质量打分。

### 5.3 Plugin Extension (通过插件向外围扩展的能力)
*   **平台特定反模式检查**: (例如针对 Android, React, Rust 的具体 Lint/Grep Hook)。
*   **自定义 Checkpoint 验证脚本**: (例如定制的测试套件命令，覆盖率上报逻辑)。
*   **自定义 Agent 人设与 Prompt 增强**: 面向特定领域 (如 DBA, 客户端架构师) 的角色定义。

### 5.4 Out (坚决排斥的反模式，永远不支持)
*   ❌ **固定 6 文档模型**: 拒绝 *claude-code-specs-generator* 那种静态、死板的文件堆砌，改为轻量 JSON 驱动的 Settlement。
*   ❌ **Memory-first / Journal-first 设计**: 拒绝将会话日志原样堆积作为主要上下文，强制走 Backflow 萃取降维。
*   ❌ **通过追加 Phase 来解决问题**: 一切流程必须映射到预定义的 6 个核心阶段中，只做减法不做加法。

---

## 6. 对第三方审查简报中 6 个核心问题的正面回应

1. **这套 workflow 的最小完整骨架应该是什么？**
   **答**：`Triage -> Spec -> Plan -> Execute -> Verify -> Settlement(Backflow)`。这就是不可改变的最大刚性边界。
2. **哪些 phase 必须进入核心协议面，哪怕默认关闭？**
   **答**：`Plan (ADR/DAG 生成)`、`Verify (三层检查点)`、`Settlement (回流与销毁)` 必须在核心协议面中定义好。即使在 Trivial/Simple 任务中直接跳过它们，其对应的协议槽位和状态机扭转接口也永存。
3. **acceptance/backflow 的最小 schema 应该如何定义，才能替代 Spec？**
   **答**：必须包含 `task_id`, `api_contract_changes` (接口变更), `new_invariants_discovered` (新不变量发现), 和 `retrospective_lessons`。以结构化的增量变更取代冗长、容易过时的宏观 Spec，成为架构演进的驱动力。
4. **ADR 应该如何触发，才能避免文档负担过重？**
   **答**：通过 Plan 阶段的**依赖与边界分析**触发。如果 Plan 没有引入新依赖或跨越预定义的架构边界，系统强制跳过 ADR 生成。坚决拒绝为日常 CRUD 工作滥写 ADR。
5. **durable docs 应该如何组织，避免上下文噪音？**
   **答**：Durable Docs 仅包含**现状 (Architecture/Interfaces)** 和 **红线 (Invariants)**。彻底剔除所有的 "Why" 和 "How we tried" (这些作为历史日志保留，默认不加载)。依靠 Backflow Agent 增量 Patch 文档，供下一个任务使用 Trellis 的 JSONL 模式定向精确注入读取。
6. **如何让 simple 任务保持轻，而 complex 任务严格执行？**
   **答**：依赖 **Profile 裁剪矩阵** 和 **状态机透传**。Simple 任务在 Triage 阶段被标记，后续的 Spec 生成退化为一句话目标，Plan 退化为单节点直通，Verify 退化为只跑 Linter，Backflow 仅做一条 Git Commit 级别的记录。状态机运转速度极快，但依然走在同样安全的核心轨道上。
