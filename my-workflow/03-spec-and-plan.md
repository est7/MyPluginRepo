# Phase 2: SPEC & PLAN — 规格 + 方案 + ADR + 任务拆解

## 目的

将"理解"转化为"可执行的契约"。产出三个 transient 产物（spec, plan, tasks）和可选的 decision 产物（ADR）。

**核心约束**：Spec 是 transient artifact，只服务于当前任务执行期。Phase 5 后归档销毁，不进入后续任务上下文。

---

## 内部步骤

```
[来自 Phase 1 的 code-understanding.md + clarification]
    │
    ▼
[Step 2.1] Spec 生成
    │   基于理解摘要 + 用户需求 → 生成 spec.md
    │   Moderate: 轻量 spec (修改目标 + 验收条件)
    │   Complex+: Full spec (PRD + BDD scenarios + scope/non-goals)
    │
    ▼
[Step 2.2] ADR 触发评估 (G3)
    │   检查：是否引入新依赖？是否跨架构边界？是否新接口？
    │   → YES: 强制生成 ADR
    │   → NO: 跳过
    │
    ▼
[Step 2.3] Plan 生成
    │   基于 spec + code-understanding → 生成 plan.md
    │   固定 schema (修改目标/影响范围/实现思路/风险/测试计划/不确定点)
    │
    ▼
[Step 2.4] Task 分解
    │   plan → tasks.md (或 plan.json with task DAG)
    │   Complex+: wave-based parallel decomposition (D3)
    │   包含每个 task 的: files, dependencies, verification method
    │
    ▼
[G2: Spec/Plan Review Gate]
    │   人类审查 spec + plan + tasks
    │   通过 → Phase 3
    │   打回 → 回到对应 step 修正
    │
    ▼
[Step 2.5] Execution Contract (可选, G4)
    │   Harness only: 生成器和评估器协商完成标准
    │
    ▼
[Step 2.6] Plan 锁定为 Baseline
    │   确认后的 plan 成为 Baseline Plan
    │   后续变更走 Delta 处理
```

---

## 输入产物

| 产物 | 来源 | 必需？ |
|------|------|--------|
| code-understanding.md | Phase 1 | Moderate+ |
| clarification-log | Phase 1 | YES |
| triage-result (profile) | Phase 0 | YES |
| Durable docs | Phase 0 加载 | 如果存在 |

## 输出产物

| 产物 | 类型 | 生命周期 |
|------|------|---------|
| `spec.md` | **Transient** | Phase 5 归档 |
| `plan.md` | **Transient** (Baseline) | Phase 5 归档 |
| `tasks.md` / `plan.json` | **Transient** | Phase 5 归档 |
| `docs/adr/XXXX-title.md` | **Decision** (条件触发) | 永久 |
| `execution-contract.md` | **Transient** (Harness only) | Phase 5 归档 |

### spec.md 最小 Schema (Moderate)

```markdown
## 修改目标
[1-3 句话]

## 验收条件
- [ ] 条件 1
- [ ] 条件 2

## Scope / Non-goals
- In scope: ...
- Out of scope: ...
```

### spec.md 完整 Schema (Complex+)

```markdown
## 修改目标

## 用户故事 / BDD 场景
- Given ... When ... Then ...

## 功能性需求
- FR-001: ...

## 非功能约束
- 性能 / 安全 / 兼容性

## 验收条件

## Scope / Non-goals / Dependencies
```

### plan.md Schema (固定)

```markdown
## 修改目标

## 影响范围
- [模块] → [新增 / 修改 / 删除]
- [调用方] → [是否受影响]

## 实现思路

## 风险项
- [风险] → [触发条件] → [应对]

## 测试与验证
- 单测：[哪些点]
- 集成测试：[哪些点]
- E2E：[哪些点]

## 不确定点
```

### ADR 触发条件

| 条件 | Simple | Moderate | Complex+ |
|------|--------|----------|----------|
| 引入新依赖 | ❌ 禁止生成 | ⚠️ 可选 | ✅ 强制 |
| 跨架构边界 | ❌ | ✅ 强制 | ✅ 强制 |
| 新公共接口 | ❌ | ⚠️ 可选 | ✅ 强制 |
| 新数据模型 | ❌ | ⚠️ 可选 | ✅ 强制 |

---

## Gate 定义

### G2: Spec/Plan Review Gate

| 属性 | 值 |
|------|-----|
| 类型 | Skip (Trivial/Simple), Hard (Moderate+) |
| 触发 | spec + plan + tasks 全部产出后 |
| 行为 | 人类审查，可分别打回 spec 或 plan |
| Revision loop | Plan-checker agent (D2) 审查 → max 3 次 + stall detection |
| 最终打回 | → Escalation: 暂停，等用户重新定义需求 |

### G3: ADR Trigger

| 属性 | 值 |
|------|-----|
| 类型 | Conditional |
| 触发 | Step 2.2，分析 plan 的依赖/边界变更 |
| 行为 | 满足触发条件 → 强制生成 ADR → 纳入 review |

### G4: Pre-Execute Contract (Harness only)

| 属性 | 值 |
|------|-----|
| 类型 | Soft (可选) |
| 触发 | Step 2.5，Harness profile |
| 行为 | 生成器和评估器协商 sprint contract → 双方签字 → 记录 |

---

## Profile 行为矩阵

| Step | Trivial | Simple | Moderate | Complex | Harness |
|------|---------|--------|----------|---------|---------|
| 2.1 Spec | ⏭️ 透传 | ⏭️ 透传 | 轻量 spec | Full spec | Full + BDD |
| 2.2 ADR | ⏭️ | ❌ 禁止 | 条件触发 | 条件触发(低阈值) | 强制评估 |
| 2.3 Plan | ⏭️ | ⏭️ | 单节点 plan | Full plan | Full + 架构师审 |
| 2.4 Tasks | ⏭️ | ⏭️ | 单任务 | Task DAG + waves | DAG + worktree 分配 |
| G2 Review | ⏭️ | ⏭️ | ✅ 人类审查 | ✅ + plan-checker | ✅ + 架构师 agent |
| 2.5 Contract | ⏭️ | ⏭️ | ⏭️ | ⏭️ | ✅ 协商 |
| 2.6 Baseline | ⏭️ | ⏭️ | ✅ 锁定 | ✅ 锁定 | ✅ 锁定 |

---

## 参考框架

| 机制 | 来源 | 如何使用 |
|------|------|---------|
| Plan 固定 schema | 真实场景 优化点 3 | 直接采用 |
| Plan-checker + revision loop | GSD `plan-checker` | max 3 + stall detection |
| Wave-based parallel decomposition | GSD | tasks 按 wave 分组 |
| ADR (条件触发) | FlowSpec | 边界分析触发 |
| Sprint contract | Anthropic harness | Harness only |
| PRD → Plan → Tasks | FlowSpec, SDD 实践指南 | 三层规格 |
| BDD/Gherkin 场景 | SDD 实践指南 | Complex+ |
| Plan as agent protocol | ECC-Mobile plan.json | Task DAG schema |
| 测试显式进入流程 | 真实场景 优化点 5 | Plan 必须标注测试计划 |

---

## Hooks

| Hook | 事件 | 行为 |
|------|------|------|
| `spec-complete` | 自定义 | 触发 ADR 评估 |
| `plan-review-start` | 自定义 | 启动 plan-checker agent (如启用) |
| `plan-locked` | 自定义 | 将 plan 标记为 Baseline，启用 Delta 保护 |

---

## 失败路径

| 场景 | 处理 |
|------|------|
| Spec 被打回 | → 回 Step 2.1，带修正指令重新生成 |
| Plan 被打回 3 次 | → Escalation: 暂停，可能需要回 Phase 1 重新理解 |
| ADR 写得太重 (ceremony 过高) | → 约束 ADR 为 1 页：Context, Decision, Consequences |
| plan-checker stall | → 连续 2 次 issue count 不减 → 直接 escalate 给用户 |

---

## Open Questions

1. **Spec 和 Plan 是否应该合并成一个文档？** 真实场景中 Phase A 产出"实现 PRD"，Phase B 产出"结构化 Plan"。但对 moderate 任务，两者内容高度重叠。考虑 moderate 合并为 `spec-plan.md`，complex+ 分开？
2. **plan.json vs plan.md？** JSON 对 agent 解析更友好（DAG、dependency），但人类可读性差。考虑 plan.md 面向人类 + 内嵌 YAML frontmatter 面向机器？
3. **Baseline 锁定的技术实现**：是文件权限？Git tag？还是仅靠 prompt 约束？早期用 prompt + Delta Log append-only 可能够用。
