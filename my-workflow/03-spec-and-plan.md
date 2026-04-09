# Phase 2: SPEC & PLAN — 规格 + 方案 + ADR + 任务拆解

## 目的

将"理解"转化为"可执行的协议"。产出 machine-checkable 的 `tasks.json` 和可选的 spec/ADR/slice/wave。

**核心约束**：
- Spec 是 transient artifact，只服务于当前任务执行期。Phase 5 后归档销毁。
- Plan 不是自由文本，是结构化的 `tasks.json`（schema 见 [09-schemas.md](./09-schemas.md) §1）。
- Spec 结构按 SDD→BDD→TDD 漏斗递减（见下方）。

---

## 内部步骤

```
[来自 Phase 1 的 code-understanding.md + clarification + context.jsonl(Complex+)]
    │
    ▼
[Step 2.1] Spec 生成（SDD→BDD→TDD 漏斗）
    │   Simple: 跳过 spec，仅定义 verify_cmd
    │   Standard: BDD 场景 + 轻量 spec
    │   Complex: SDD 约束 + BDD 场景 + Full spec
    │   Orchestrated: 完整 SDD + BDD + Rubric
    │
    ▼
[Step 2.2] ADR 触发评估 (G3)
    │   检查：是否引入新依赖？是否跨架构边界？是否新接口？
    │   → YES: 强制生成 ADR（1 页：Context, Decision, Consequences）
    │   → NO: 跳过
    │
    ▼
[Step 2.3] tasks.json 生成 ← 核心协议产物
    │   基于 spec + code-understanding → 生成 tasks.json
    │   每个 task 绑定：goal, covers_ac, verify_cmd
    │   Complex+: 加 allowed_paths, depends_on, rollback, wave
    │
    ▼
[Step 2.4] Slice / Wave 定义 (Complex+)
    │   Complex: 定义 slice.md（执行闭包边界）
    │   Orchestrated: 定义 wave.json（并行分组）
    │
    ▼
[G2: Spec/Plan Review Gate]
    │   人类审查 spec + tasks.json (+ slice/wave)
    │   通过 → Phase 3
    │   打回 → 回到对应 step 修正
    │
    ▼
[Step 2.5] Execution Contract (可选, G4)
    │   Orchestrated only: 生成器和评估器协商完成标准
    │
    ▼
[Step 2.6] Plan 锁定为 Baseline
    │   确认后的 tasks.json + spec 成为 Baseline Plan
    │   后续变更走 Delta 处理
```

---

## 输入产物

| 产物 | 来源 | 必需？ |
|------|------|--------|
| code-understanding.md | Phase 1 | Standard+ |
| context.jsonl | Phase 1 | Complex+ |
| clarification-log | Phase 1 | YES |
| triage-result (profile) | Phase 0 | YES |
| Durable docs | Phase 0 加载 | 如果存在 |

## 输出产物

| 产物 | 类型 | 生命周期 | Profile |
|------|------|---------|---------|
| `tasks.json` | **Transient** (协议) | Phase 5 归档 | Simple+ |
| `spec.md` | **Transient** | Phase 5 归档 | Standard+ |
| `slice.md` | **Transient** | Phase 5 归档 | Complex+ |
| `wave.json` | **Transient** | Phase 5 归档 | Orchestrated 必须, Complex 可选 |
| `docs/adr/XXXX-title.md` | **Decision** (条件触发) | 永久 | Standard+ 条件触发 |
| `execution-contract.md` | **Transient** (Orchestrated only) | Phase 5 归档 | Orchestrated |

所有 schema 定义见 [09-schemas.md](./09-schemas.md)。

---

## SDD→BDD→TDD 漏斗

Spec 结构按 profile 递减，不是所有层级都走完整漏斗。

### 漏斗模型

```
SDD: 定义边界、不变量、契约、错误模型、non-goals
  ↓
BDD: 定义 Given/When/Then 验收场景
  ↓
TDD: 绑定 verify_cmd，Red→Green→Refactor 循环
```

### Profile 裁剪

| Profile | SDD | BDD | TDD (verify_cmd) |
|---------|-----|-----|-------------------|
| quick | skip | skip | skip |
| simple | skip | skip | ✅ verify_cmd 必须 |
| standard | skip | ✅ Given/When/Then 场景 | ✅ verify_cmd 必须 |
| complex | ✅ Constraints + Boundaries + Non-goals | ✅ 完整 BDD 场景 | ✅ Red→Green→Refactor |
| orchestrated | ✅ 完整 SDD | ✅ 完整 BDD + Rubric | ✅ 严格 TDD + pass@k |

### spec.md 结构

#### Standard 版

```markdown
## 修改目标
[1-3 句话]

## 验收场景 (BDD)
### Scenario 1: [名称]
Given [前置条件]
When [动作]
Then [期望结果]

## Scope / Non-goals
- In scope: ...
- Out of scope: ...
```

#### Complex+ 版

```markdown
## SDD 约束 (Constraints & Boundaries)
- Scope: [本次只修改的模块]
- Non-goals: [明确不做的事]
- Invariants: [不可打破的规则]
- Contracts: [接口契约]
- Error Model: [错误分类与处理]

## BDD 验收场景
### Scenario 1: [名称]
Given ...
When ...
Then ...

## 功能性需求
- FR-001: ...

## 非功能约束
- 性能 / 安全 / 兼容性
```

---

## tasks.json — 核心协议产物

tasks.json 是连接 Spec 和 Execute 的桥梁。每个 task 是 machine-checkable 的执行单元。

### Profile 裁剪

| Profile | tasks.json 要求 |
|---------|----------------|
| quick | 无（直接执行） |
| simple | 单条 task，仅 `id` + `goal` + `verify_cmd` |
| standard | 完整 tasks.json，`covers_ac` 必填 |
| complex+ | 完整 + `allowed_paths` + `depends_on` + `rollback` + `wave` |

完整 schema 见 [09-schemas.md](./09-schemas.md) §1。

---

## ADR 触发条件

| 条件 | Simple | Standard | Complex+ |
|------|--------|----------|----------|
| 引入新依赖 | ❌ 禁止生成 | ⚠️ 可选 | ✅ 强制 |
| 跨架构边界 | ❌ | ✅ 强制 | ✅ 强制 |
| 新公共接口 | ❌ | ⚠️ 可选 | ✅ 强制 |
| 新数据模型 | ❌ | ⚠️ 可选 | ✅ 强制 |

ADR 模板约束为 1 页：Context, Decision, Consequences。

---

## Gate 定义

### G2: Spec/Plan Review Gate

| 属性 | 值 |
|------|-----|
| 类型 | Skip (Quick/Simple), Hard (Standard+) |
| 触发 | spec + tasks.json (+ slice/wave) 全部产出后 |
| 行为 | 人类审查，可分别打回 spec 或 tasks |
| Revision loop | Plan-checker agent 审查 → max 3 次 + stall detection |
| Stall | 连续 2 次 issue count 不减 → `escalation` |
| 最终打回 | → `escalation`: 暂停，等用户重新定义需求 |

### G3: ADR Trigger

| 属性 | 值 |
|------|-----|
| 类型 | Conditional |
| 触发 | Step 2.2，分析 plan 的依赖/边界变更 |
| 行为 | 满足触发条件 → 强制生成 ADR → 纳入 review |

### G4: Pre-Execute Contract (Orchestrated only)

| 属性 | 值 |
|------|-----|
| 类型 | Soft (可选) |
| 触发 | Step 2.5，Orchestrated profile |
| 行为 | 生成器和评估器协商 sprint contract → 双方签字 → 记录 |

---

## Profile 行为矩阵

| Step | Quick | Simple | Standard | Complex | Orchestrated |
|------|---------|--------|----------|---------|---------|
| 2.1 Spec (SDD→BDD→TDD) | ⏭️ 透传 | ⏭️ 仅 verify_cmd | BDD 场景 + 轻量 spec | SDD + BDD + Full spec | 完整 SDD + BDD + Rubric |
| 2.2 ADR | ⏭️ | ❌ 禁止 | 条件触发 | 条件触发(低阈值) | 强制评估 |
| 2.3 tasks.json | ⏭️ | 单条 task | 完整 tasks.json | Task DAG + covers_ac | DAG + allowed_paths + rollback |
| 2.4 Slice/Wave | ⏭️ | ⏭️ | ⏭️ | slice.md 定义 | slice.md + wave.json |
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
| Sprint contract | Anthropic harness | Orchestrated only |
| SDD→BDD→TDD 漏斗 | SDD 实践指南 + 10-Gemini 建议 | 按 profile 递减 |
| Plan as agent protocol | ECC-Mobile plan.json + 12-Codex 主链 | tasks.json schema |
| 测试显式进入流程 | 真实场景 优化点 5 | Plan 必须标注 verify_cmd |
| Slice 判据 | PAUL 框架 | 独立 AC 集合 / 独立模块 / 独立验证 |

---

## Hooks

| Hook | 事件 | 行为 |
|------|------|------|
| `spec-complete` | 自定义 | 触发 ADR 评估 |
| `plan-review-start` | 自定义 | 启动 plan-checker agent (如启用) |
| `plan-locked` | 自定义 | 将 tasks.json + spec 标记为 Baseline，启用 Delta 保护 |
| `tasks-validate` | plan-locked 后 | 校验 tasks.json schema 合法性（字段完整性） |

---

## 失败路径

| 场景 | Gate Taxonomy | 处理 |
|------|--------------|------|
| Spec 被打回 | `revision` | 回 Step 2.1，带修正指令重新生成 |
| Plan 被打回 3 次 | `escalation` | 暂停，可能需要回 Phase 1 重新理解 |
| ADR 写得太重 (ceremony 过高) | `revision` | 约束 ADR 为 1 页：Context, Decision, Consequences |
| plan-checker stall | `escalation` | 连续 2 次 issue count 不减 → 直接 escalate 给用户 |
| tasks.json schema 校验失败 | `preflight` | 阻断进入 Phase 3，修正后重试 |

---

## Open Questions

1. **Baseline 锁定的技术实现**：是文件权限？Git tag？还是仅靠 prompt 约束？早期用 prompt + Delta Log append-only 可能够用。
2. **tasks.json 的 plan-validator**：P1 项——用脚本校验 tasks.json 字段完整性（covers_ac 非空、verify_cmd 可执行等）。何时引入？
