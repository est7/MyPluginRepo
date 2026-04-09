# 13. Gemini 专属工作流进化意见 (v3)

> 基于 Superpowers 的软性约束哲学、Flowspec 的产物门控与分层治理，结合 Gemini CLI 的独有特性（无 Subagent、原生 Plan Mode、交互 Tool），对 `my-workflow` 在 Gemini 平台上的落地提出进化方案。

## 1. 核心适配哲学：从多 Agent 编排走向「单 Agent 强约束」与「原生 Plan Mode」

Gemini CLI 的最大约束是**不支持 Subagent**（不支持使用 `Task` tool 派生子 Agent），这意味着 Superpowers 和 Flowspec 中依赖子 Agent 隔离上下文（如独立的 Spec Reviewer、Security Reviewer）的架构无法直接搬用。

**进化策略**：
- **原生 Plan Mode 对齐 Phase 1 & 2**：将 `DISCOVER` 和 `SPEC & PLAN` 严格映射为 Gemini 的 Plan Mode（只读模式）。在 Plan 阶段结束时，必须利用 `exit_plan_mode` 强制进行人类审批（硬门控）。在退出 Plan Mode 前，任何试图修改代码的意图都会被系统阻断。
- **Persona Shifting 代替 Subagent**：在 `EXECUTE` 和 `VERIFY` 阶段，通过在 Prompt 层注入特定角色指令（如 Flowspec 的 Quality Guardian "三层批评"结构），强制单一 Agent 进行角色的自我切换自审，而不是派生新的子 Agent。

## 2. 关键机制进化 (汲取 Superpowers & Flowspec)

### 2.1 强化 Anti-Rationalization (防合理化借口)
Superpowers 最成功的实践是预判 LLM 的合理化借口。在 Gemini 的 `EXECUTE` 阶段，注入针对单 Agent 的反借口清单：
- **借口**："这是一个简单的文字修改，不需要走 BDD/TDD 流程"
  - **反驳**："任何行为变更必须有 BDD/TDD 约束支持，没有例外。"
- **借口**："我看了一下文件，逻辑应该没问题"
  - **反驳**："必须提供实际的验证命令 `stdout` 输出作为证据，禁止凭空断言 (Verification-Before-Completion)。"
- **借口**："这个步骤做起来太繁琐，我一次性把文件改完吧"
  - **反驳**："简单事物极易变复杂，执行纪律不可妥协。必须单步验证。"

### 2.2 产物门控状态转换 (Artifact-Gated Transitions)
吸收 Flowspec 的教训，不能仅仅依靠 Prompt 的软性约束。在 Gemini 中，利用对具体物理文件的读取作为阶段转换的硬性凭证：
- **进入 Phase 3 (EXECUTE) 前**：必须读取到 `context.jsonl` 和 `spec.md`。如果文件不存在，或 `spec.md` 中不包含 `Given/When/Then` 的验收场景，Gemini 必须拒绝编写业务代码，并退回需求澄清阶段。
- **进入 Phase 5 (SETTLE) 前**：强制要求当前对话或任务执行输出中存在实际的测试输出日志（作为通过 Ralph Loop 的证据），没有执行证据不能声明完成。

### 2.3 引入 Quality Guardian 的「三层批评模式」
在单 Agent 架构中，Agent 容易陷入「顺从偏见」或「盲目自信」。在没有同僚 Reviewer 的情况下，引入 Flowspec 的三层批评框架。在完成编码后的 `VERIFY` 阶段，强制 Gemini 必须严格按以下三步输出审查意见：
1. **Acknowledge Value**（认可当前实现的价值，它解决了什么问题）
2. **Identify Risk**（指出潜在的代码腐化、性能瓶颈、安全隐患或未考虑的边界风险）
3. **Suggest Mitigation**（针对识别的风险，提出具体的重构或缓解建议）
这有效打破了单 Agent "我写得很好" 的幻觉。

### 2.4 深度整合 Gemini 专属 Tools
- **`ask_user` Tool**：
  - 在 **Phase 0 (TRIAGE)** 复杂度评估，或 **Phase 2** 遇到架构分歧时，不再自行武断猜测，而是调用 `ask_user` 构造带详细描述的结构化多选选项（Multi-select），实现高质量的 Human-in-the-loop 介入。
- **`tracker_create_task` Tool**：
  - 在 **Phase 2 (SPEC & PLAN)** 拆解任务后，强制调用此工具将 `tasks.json` 里的条目同步到 Gemini 的原生任务跟踪面板中，实现可观测的进度管理。
- **`save_memory` Tool**：
  - 仅在 **Phase 5 (SETTLE)** 的 PAUL 强制对账之后，将全局不变量（Invariants）、高层架构决策和跨项目偏好提取出来，调用 `save_memory` 固化到 `GEMINI.md` 中。**严禁**在执行期使用该工具存储临时的上下文或报错信息。

## 3. Gemini 专属六阶段映射表 (The Gemini Implementation)

| 阶段 | 核心目标 | Gemini 专属实现机制与约束 |
|------|----------|-------------------------|
| **0. TRIAGE** | 复杂度评估、路由与上下文管控 | 使用 `ask_user` 向用户提供结构化问卷，确定 `Full SDD / Light / Skip` 级别。 |
| **1. DISCOVER** | 探索与理解 | **必须进入 `enter_plan_mode` (Plan Mode)**。利用 `read_file` 和 `grep_search` 高效探索，输出 `context.jsonl`，划定上下文边界。 |
| **2. SPEC & PLAN**| 约束建模 (SDD/BDD) | 继续保持 Plan Mode。产出 `spec.md` (包含 Gherkin 场景) 和 `plan.md`。完成时必须调用 `exit_plan_mode` 提交计划，等待人类硬审批。审批未通过前，处于只读环境，无法执行破坏性写操作。 |
| **3. EXECUTE** | TDD 循环与精确注入 | 脱离 Plan Mode。每步执行严格遵循 `context.jsonl` 的隔离范围。单 Agent 执行时强制附带 Anti-Rationalization 借口防范清单，保持极小步的增量修改。 |
| **4. VERIFY** | 证据驱动与强制自审 | 使用 `run_shell_command` 运行测试/Lint，强制输出实际的 `stdout` 证据（Ralph Loop）。必须使用「三层批评模式」执行自我代码审查。 |
| **5. SETTLE** | PAUL 强制对账与知识回流 | 依据 `spec.md` 生成 `reconcile-settlement.json` 进行对账。针对提炼出的长期不变量，调用 `save_memory` 固化，最后清理销毁瞬态产物。 |

## 4. 总结

在缺乏多 Agent 相互监督的 Gemini CLI 环境中，**“Plan Mode 的前置隔离（天然的 Hard Gate）”** 和 **“结构化防幻觉 Prompt（三层批评 + Anti-Rationalization）”** 以及 **“专属 Tools（ask_user, tracker_create_task, save_memory）的精准使用”** 是实现高质量工作流的最核心抓手。通过将工作流的软约束转化为对 `exit_plan_mode` 和物理文件存在的硬依赖，我们可以在单 Agent 限制下达到与多 Agent 编排同样严谨的落地效果。