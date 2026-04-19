# Workflow Research Report: cc-sdd

> 生成时间：2025-07  
> 仓库：`vendor/cc-sdd/`  
> 版本：v3.0 | 许可证：MIT | npm 包：`cc-sdd`

---

## 1. 框架概况

| 维度 | 值 |
|------|-----|
| **类型** | Spec-driven development 框架，跨 8 个 AI coding agent 平台 |
| **文件数** | ~593 |
| **语言** | JavaScript（installer CLI）+ Markdown（17 skills）+ 13 种自然语言 |
| **入口** | `npx cc-sdd@latest` → 安装 17 个 skill → `/kiro-discovery <idea>` 开始 |
| **平台** | Claude Code (stable)、Codex (stable)、Cursor/Copilot/Windsurf/OpenCode/Gemini CLI/Antigravity (beta) |
| **设计哲学** | "Boundaries are not overhead. They are what lets you move freely inside while protecting the outside." |

cc-sdd 是当前调研的 vendor 中**跨平台覆盖最广**的框架——同一套 17 个 skill 通过 CLI installer 适配 8 个不同的 AI coding agent。v3.0 引入了 Kiro-inspired 的 spec-driven 方法论，以 `/kiro-discovery` 为统一入口，支持从单一 spec 到多 spec batch 的全谱系工作流。

---

## 2. 源清单

| 文件 / 目录 | 作用 |
|-------------|------|
| `README.md` | 项目概览、Quick Start、8 平台支持矩阵 |
| `CLAUDE.md` / `AGENTS.md` | AI 执行指导：路径约定、workflow 概览、skill structure |
| `tools/cc-sdd/` | npm CLI 工具（installer 核心） |
| `tools/cc-sdd/templates/agents/claude-code-skills/skills/` | 17 个 skill 目录 |
| `skills/kiro-discovery/SKILL.md` | Entry point skill：routing、idea 分析、brief/roadmap 生成 |
| `skills/kiro-impl/SKILL.md` | Autonomous TDD implementation：subagent dispatch、review、auto-debug |
| `skills/kiro-spec-batch/SKILL.md` | Multi-spec batch：roadmap → 按依赖波并行创建 spec |
| `skills/kiro-spec-init/SKILL.md` | Spec 初始化 |
| `skills/kiro-spec-requirements/SKILL.md` | Requirements 收集 |
| `skills/kiro-spec-design/SKILL.md` | Design（含 File Structure Plan） |
| `skills/kiro-spec-tasks/SKILL.md` | Task 分解（含 Boundary/Depends 注解） |
| `skills/kiro-review/SKILL.md` | Task-local adversarial review protocol |
| `skills/kiro-debug/SKILL.md` | Root-cause-first debug protocol |
| `skills/kiro-verify-completion/SKILL.md` | Fresh-evidence gate |
| `skills/kiro-validate-impl/SKILL.md` | Implementation 验证 |
| `skills/kiro-validate-gap/SKILL.md` | Gap 分析 |
| `skills/kiro-validate-design/SKILL.md` | Design review |
| `skills/kiro-steering/SKILL.md` | Project-wide steering 配置 |
| `skills/kiro-steering-custom/SKILL.md` | 自定义 steering |
| `skills/kiro-spec-quick/SKILL.md` | Quick spec（跳过分步流程） |
| `skills/kiro-spec-status/SKILL.md` | Spec 进度查询 |
| `.kiro/steering/` | Product/tech/structure steering 文件 |
| `.kiro/specs/` | 每个 feature 的 spec 目录 |
| `docs/guides/` | 多语言指南（skill-reference、migration、customization 等） |

---

## 3. 对象模型

### 核心实体关系

```
Steering (.kiro/steering/)
    ├── product.md      (产品上下文)
    ├── tech.md         (技术栈约束)
    └── structure.md    (项目结构)
         │
         ▼
Spec (.kiro/specs/<feature>/)
    ├── spec.json       (元数据 + phase approvals)
    ├── brief.md        (discovery 输出)
    ├── requirements.md (Phase 1)
    ├── design.md       (Phase 2 — 含 File Structure Plan)
    └── tasks.md        (Phase 3 — 含 Boundary/Depends 注解)
         │
         ▼
Roadmap (.kiro/steering/roadmap.md)
    └── Multi-spec dependency graph (for batch mode)
```

### Spec 作为 Contract

cc-sdd 将 spec 定位为**系统各部分之间的 contract**，而非交给 agent 的"命令文档"。Code 是 source of truth，spec 使 boundary 显式化。这是框架最核心的设计决策。

### Context 隔离

- **Steering** 在所有 skill 间共享（project-level context）
- **Spec** 按 feature 隔离，每个 spec 目录独立
- **Implementation** 中每个 task 通过 subagent 在独立 context 中执行
- **Review** 通过独立 subagent 执行，与 implementer 的 context 分离

---

## 4. 流程与状态机

### 主流程

```
/kiro-discovery <idea>
    │
    ├── Path A: 已有 spec 覆盖 → 直接指向现有 spec
    ├── Path B: 无需 spec → 直接实现
    ├── Path C: 新单一 scope → 创建 brief.md
    │       → /kiro-spec-init → /kiro-spec-requirements → /kiro-spec-design → /kiro-spec-tasks
    │       → /kiro-impl
    ├── Path D: 多 scope 分解 → 创建 roadmap.md + 多个 brief.md
    │       → /kiro-spec-batch (并行按依赖波创建 spec)
    │       → /kiro-impl (per feature)
    └── Path E: 混合分解 → 现有 spec 更新 + 直接实现 + 新 spec
```

### Spec Phase Gate

```
Requirements (Phase 1)
    ↓ [Human Approval in spec.json]
Design (Phase 2)
    ↓ [Human Approval — use -y for fast-track]
Tasks (Phase 3)
    ↓ [Human Approval]
Implementation (Phase 4)
```

### `/kiro-impl` 内部循环（Autonomous Mode）

```
For each task (1 per iteration):
    ┌─→ Re-read tasks.md
    │   Dispatch implementer subagent
    │       ├── READY_FOR_REVIEW → Dispatch reviewer subagent
    │       │       ├── APPROVED → Commit (selective staging) → Record learnings
    │       │       └── REJECTED → Re-dispatch implementer (max 2 rounds)
    │       ├── BLOCKED → Dispatch debug subagent (max 2 rounds)
    │       └── NEEDS_CONTEXT → Gather more context, re-dispatch
    └── Next task (propagate Implementation Notes)

Final: /kiro-validate-impl (bounded: max 3 remediation rounds)
```

### Feature Flag Protocol（Behavioral Tasks）

```
1. Add flag (OFF by default)
2. RED: Write tests, must FAIL with flag OFF
3. GREEN: Enable flag, implement until tests pass
4. Remove flag, confirm tests still pass
```

### 失败路径

- **Reviewer rejects twice** → 触发 auto-debug subagent
- **Debug subagent fails twice** → Task 标记 BLOCKED，escalate to human
- **Final validation fails** → Max 3 remediation rounds，然后 escalate
- **Spec batch cross-spec conflict** → Cross-spec review 阶段捕获矛盾

---

## 5. 执行保障审计

| 机制 | 级别 | 说明 |
|------|------|------|
| Phase gate（spec.json approvals） | **Hard** | Implementation 无法在 approval 缺失时启动 |
| Selective staging（禁止 `git add -A`） | **Hard** | Skill 中明确禁止，限定只能用显式路径 |
| 禁止 `git reset --hard` | **Hard** | "No Destructive Reset" 规则 |
| Bounded review（max 2 rounds） | **Hard** | 明确的 round 上限 |
| Bounded debug（max 2 rounds） | **Hard** | 明确的 round 上限 |
| Bounded remediation（max 3 rounds） | **Hard** | Final validation 的 round 上限 |
| Boundary/Depends 注解 | **Soft** | task 携带 `_Boundary:_` 和 `_Depends:_`，review 检查但非技术强制 |
| TDD cycle（RED→GREEN→REFACTOR） | **Soft** | Skill 中要求但依赖 subagent 自律 |
| Learnings propagation | **Soft** | 通过 `## Implementation Notes` 在 tasks.md 中传播，但可能被忽略 |
| "1% chance → invoke skill" 规则 | **Unenforced** | CLAUDE.md 声明"If there is even a 1% chance a skill applies, invoke it"，无法验证 |

**总评**：cc-sdd 在**流程边界**（phase gate、bounded rounds、destructive operation ban）上实现了 Hard enforcement，在**内容质量**（TDD 执行、boundary 遵守）上是 Soft enforcement。Round 上限设计是亮点——有效防止了 AI 陷入无限修复循环。

---

## 6. Prompt 目录

### Prompt 1: kiro-discovery — 5-Path Routing

```markdown
# Determine Action Path
- Path A: Existing spec covers this
- Path B: No spec needed
- Path C: New single-scope feature
- Path D: Multi-scope decomposition needed
- Path E: Mixed decomposition

# Critical Constraint
Files on disk are the source of continuity.
Do NOT leave discovery results only in conversation text.
```

**设计意图**：将"开始新工作"这个模糊的起点结构化为 5 种确定性路径，每条路径有明确的输出文件（brief.md / roadmap.md）。"文件即连续性"的约束确保了跨 session 的状态持久化。

### Prompt 2: kiro-impl — Subagent Dispatch Protocol

```markdown
# Autonomous Mode: ONE sub-task per iteration
1. Re-read tasks.md before each iteration
2. Dispatch implementer subagent
3. Parse structured handoff (READY_FOR_REVIEW | BLOCKED | NEEDS_CONTEXT)
4. Review (required/inline/off)
5. Commit with selective staging (NEVER git add -A)
6. Record learnings in Implementation Notes
7. Next task (learnings propagate forward)

# Bounded Execution
- Max 2 implementer re-dispatch rounds
- Max 2 debug rounds per task
- Max 3 remediation rounds for final validation
```

**设计意图**：通过严格的"一次一个 task"迭代和 bounded rounds，将 autonomous implementation 从"不可控的长时间运行"转变为"可预测的有界迭代"。Learnings propagation 机制使得后续 task 从前序 task 的经验中受益。

---

## 7. 微观设计亮点

### 7.1 Boundary-First Spec Discipline

v3.0 的核心创新：`design.md` 中引入 **File Structure Plan**，task 携带 `_Boundary:_`（文件范围）和 `_Depends:_`（前置依赖）注解。Review 和 validation 检查 **boundary violations** 而非仅仅样式问题。这将"spec"从"描述性文档"提升为**可验证的 contract**。

### 7.2 Learnings Propagation via `## Implementation Notes`

每个 task 完成后，实现经验记录在 `tasks.md` 的 `## Implementation Notes` section 中。后续 task 的 subagent 在启动时会读取这些 notes。这是一种**轻量级的跨 task 经验传播机制**，不依赖复杂的 memory 系统，直接利用文件系统。

### 7.3 Feature Flag Protocol 的 TDD 集成

对于行为型 task，框架要求先添加 feature flag（OFF），在 flag OFF 状态下写测试确保测试 FAIL，然后打开 flag 实现代码使测试 PASS，最后移除 flag 确认测试仍然 PASS。这种**4 步 flag-driven TDD**在确保 test 有效性方面比传统 RED-GREEN 更严格。

---

## 8. 宏观设计亮点

### 8.1 "Spec as Contract, Not Command"

cc-sdd 的核心哲学是：spec 是系统各部分之间的 **contract**，不是交给 agent 的"主命令文档"。Code 是 source of truth，spec 的作用是使 boundary 显式化，让 human 和 agent 可以并行工作而无需持续同步。这种"contract-first"的理念与 API-first 设计哲学一脉相承。

### 8.2 跨 8 平台的统一 Skill 集

17 个 skill 通过 CLI installer 适配 8 个 AI coding agent，每个平台使用**相同的 skill 内容**但不同的**安装目标路径**。这种"一次编写、多平台部署"的策略使得框架的 skill 内容可以独立于平台演化，降低了维护成本。

---

## 9. 失败模式与局限

| # | 失败模式 | 影响 | 可能性 |
|---|----------|------|--------|
| 1 | **Spec 仪式感过重** — 即使是小任务也需要经过 discovery → requirements → design → tasks 流程（除非走 Path B） | 开发者流畅度下降 | 高 |
| 2 | **跨平台一致性假设** — 8 个平台的 subagent 能力差异大（如 Cursor 的 agent 与 Claude Code 的 agent 行为不同） | 非 Claude Code 平台的 skill 执行质量不稳定 | 高 |
| 3 | **Bounded rounds 的硬编码** — 2 轮 review、2 轮 debug、3 轮 remediation 的上限是经验值，可能对复杂任务不足 | 合理修复被过早终止 | 中 |
| 4 | **Learnings 积累膨胀** — `## Implementation Notes` 随 task 增多不断增长，可能最终超出 context budget | 后期 task 的 subagent context 被 notes 占满 | 中 |
| 5 | **spec.json approval 的人工瓶颈** — 每个 phase 需要 human approval，在快速迭代场景中成为瓶颈（`-y` 可跳过但牺牲质量保障） | 开发速度受限或质量保障被绕过 | 中 |
| 6 | **Cross-spec batch 的冲突检测** — batch 模式的 cross-spec review 检查矛盾和重复，但检测深度取决于 AI 能力 | 隐含矛盾可能漏检 | 中 |

---

## 10. 迁移评估

### 可移植候选

| 机制 | 目标位置（1st-cc-plugin） | 优先级 | 改造量 |
|------|--------------------------|--------|--------|
| Boundary-first spec discipline | `workflows/deep-plan` | P1 | 引入 File Structure Plan + Boundary/Depends 注解 |
| Bounded execution rounds | 全局 skill 设计规范 | P1 | 提取 bounded rounds pattern 写入 skill-dev |
| Feature Flag TDD protocol | `quality/testing` | P1 | 直接移植 4 步 flag-driven TDD |
| 5-Path discovery routing | `workflows/deep-plan` | P2 | 将 discovery routing 逻辑移植为 plan 入口 |
| Learnings propagation | `workflows/deep-plan` | P2 | 文件级跨 task 经验传播 |
| kiro-review adversarial protocol | `quality/codex-review` | P2 | 移植 task-local review protocol |
| kiro-debug root-cause protocol | `quality/testing` | P3 | 移植 root-cause-first debug |

### 建议采纳顺序

1. **Bounded rounds + Feature Flag TDD** → 立即可用的工程纪律
2. **Boundary-first spec** → 增强 deep-plan 的 spec 质量
3. **Discovery routing** → 提供智能化的工作流入口

---

## 11. 开放问题

1. **Kiro 兼容性**：README 声称"Existing Kiro specs remain compatible and portable"，但 Kiro IDE 本身的 spec 格式是否有公开标准？兼容程度如何验证？
2. **Subagent 能力假设**：`/kiro-impl` 的 autonomous mode 假设 subagent 能够独立完成 TDD cycle，这在 Claude Code 的 Task agent 上是否可靠？failure rate 是多少？
3. **13 种语言支持的质量**：CLI 支持 13 种自然语言的 skill 生成，但非英语 skill 的内容质量（尤其是技术术语翻译）是否经过验证？
4. **`--antigravity` 平台**：这是一个"experimental beta"平台，其身份和能力不明。
5. **Legacy mode 的废弃时间线**：`--claude` / `--cursor` 等 legacy 安装方式标记为 deprecated，但未给出移除日期。

---

## 附录：Gemini Deepdive 补充信息

> 来源：`1st-cc-plugin/workflows/loaf/docs/gemini-roadmap-review/deepdive-cc-sdd.md`
> 补充内容：spec.json 数据结构、`-y` flag 实现流程、Safety & Fallback 机制的具体实现。

### A.1 `spec.json` 精确数据结构

Deepdive 揭示了 `spec.json` 的完整 approvals object 结构：

```json
{
  "phase": "requirements",
  "approvals": {
    "requirements": {
      "generated": true,
      "approved": false,
      "timestamp": null
    },
    "design": {
      "generated": false,
      "approved": false,
      "timestamp": null
    },
    "implementation": {
      "generated": false,
      "approved": false,
      "timestamp": null
    }
  }
}
```

每个 phase 的 `generated` 和 `approved` 是独立 boolean，`timestamp` 在 approve 时记录 ISO 8601 时间戳。这允许追踪"已生成但未批准"的中间状态。

### A.2 `-y` Flag 的实现链路

1. CLI 入口（`tools/cc-sdd/src/cli/args.ts`）解析 `-y` / `--yes` flag
2. 作为 `$2` 参数传递给 SKILL.md 中的 skill 文件
3. SKILL.md 中显式检查：`if [[ "$2" == "-y" ]]`
4. 当 `-y` 激活时：跳过人工 approval 确认，自动将 `approved` 设为 `true` 并填充 `timestamp`
5. 影响所有 phase transition：requirements → design → implementation

### A.3 Safety & Fallback 结构化错误响应

当用户试图执行某 phase 但前置 phase 未 approved 时，cc-sdd 不是简单报错，而是输出结构化的引导信息：
- 明确告知哪个前置 phase 尚未 approve
- 给出推荐的下一步命令（如 `cc-sdd approve requirements`）
- 这种"结构化的失败响应"模式值得参考——它将 error 转化为 guidance
