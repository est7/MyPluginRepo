# Phase 5: SETTLE — 结算 + AC 对账 + Backflow + Transient 归档

## 目的

任务不在"代码写完、测试过了"时结束。任务在**输出结算结果并完成知识回流**时结束。

这个阶段解决一个根本问题：如果没有显式结算，项目知识只存在于 git log 和人的记忆里。下一个任务（可能是另一个 session 或另一个人）无法高效继承。

**核心原则**：
1. Spec 是 transient，Acceptance Settlement 是 durable
2. `reconcile-settlement.json` 是任务的唯一闭环凭证——没有它，任务不得标记 DONE
3. Planned-vs-actual 强制对账，不是可选总结

---

## 内部步骤

```
[来自 Phase 4 的 human acceptance = pass]
    │
    ▼
[Step 5.1] Reconcile Settlement 生成
    │   Agent 基于执行产物生成 reconcile-settlement.json
    │   (schema 见 09-schemas.md §3)
    │   核心三部分：
    │   a. planned_vs_actual: 计划范围 vs 实际范围的偏差
    │   b. ac_results: 逐条 AC 对账 (AC Traceability Matrix)
    │   c. concerns / residual_risks: 残余问题
    │   → Minimum Closure Contract 校验（按 profile）
    │
    ▼
[Step 5.2] Backflow 提炼
    │   从 settlement 中提取 durable 信息：
    │   a. API/接口变更 → patch docs/interfaces.md
    │   b. 新不变量发现 → patch docs/invariants.md
    │   c. 架构变化 → patch docs/architecture.md
    │   d. 经验教训 → append lessons.jsonl
    │
    ▼
[Step 5.3] ADR 归档确认
    │   Phase 2 产出的 ADR 是否需要更新？
    │   执行过程中决策有变？→ 更新或追加 ADR
    │
    ▼
[Step 5.4] Transient 归档/销毁
    │   spec.md, tasks.json, delta-log.jsonl,
    │   code-understanding.md, effective-plan.md,
    │   context.jsonl, slice.md, wave.json,
    │   verify-evidence.json, verify-review.json
    │   → 移入 .archive/{task-id}/ 或删除
    │   → 从后续任务的默认上下文加载列表中移除
    │
    ▼
[Step 5.5] Deliver (提交 + PR)
    │   Quick/Simple: 直接 commit
    │   Standard: commit + optional PR
    │   Complex+: branch + PR + CI gate
    │   Orchestrated: branch + PR + CI + 人工合并确认
    │
    ▼
[Step 5.6] Event Log 记录
    │   完整任务生命周期写入 event-log.jsonl
    │   包含：triage score, profile, phases executed,
    │         gates passed/failed, duration, delta count
    │
    ▼
[完成]
```

---

## Minimum Closure Contract

无论任务多简单，都需要结构化闭环。闭环强度按 profile 递减：

| Profile | 最低关闭要求 |
|---------|-------------|
| quick | `summary` + `verification_done` + `actual_scope`（可内联到 commit message） |
| simple | quick + `concerns?` + `lessons?` |
| standard | `planned_vs_actual` + `ac_results` + `verification_done` + `backflow_targets` |
| complex+ | 全字段 `reconcile-settlement.json`，逐条 AC 对账 |

### Enforcement

- 无 `reconcile-settlement` → 任务不得标记 DONE
- `ac_results` 存在 FAIL 且 `concerns` 为空 → 状态锁定为 `DONE_WITH_CONCERNS`
- `DONE_WITH_CONCERNS` 不得直接进入 DONE，需人工决策（close / follow-up / waiver）

---

## AC 对账（AC Traceability Matrix）

Standard+ 任务必须逐条对账 AC：

```
AC-1 → task-001, task-003 → verify-evidence-001, verify-evidence-004 → PASS
AC-2 → task-002           → verify-evidence-002                     → PASS
AC-3 → task-003           → verify-evidence-004                     → FAIL (reason: ...)
```

**规则**：
- 每个 `covers_ac` 声明的 AC 必须有对应 `verify-evidence`
- 无 evidence 的 AC → 标记 `SKIP`，必须在 `concerns` 中说明原因
- AC 全 PASS → `execution_status: "success"`
- AC 部分 FAIL → `execution_status: "partial"`，`concerns` 必须非空

详见 [09-schemas.md §9 AC Traceability Matrix](./09-schemas.md)。

---

## 输入产物

| 产物 | 来源 | 必需？ |
|------|------|--------|
| Human acceptance = pass | Phase 4 | YES |
| 源代码变更 (staged/committed) | Phase 3 | YES |
| `tasks.json` (Baseline + Delta) | Phase 2-3 | Simple+ |
| `spec.md` | Phase 2 | 参考 |
| `verify-evidence.json` | Phase 4 | Standard+ |
| `verify-review.json` | Phase 4 | Standard+ |
| `delta-log.jsonl` | Phase 3 | 如果存在 |
| ADRs (如有) | Phase 2 | 参考 |

## 输出产物

| 产物 | 类型 | Schema | 生命周期 |
|------|------|--------|---------|
| `reconcile-settlement.json` | **Durable** | [09-schemas.md §3](./09-schemas.md) | 永久，作为历史记录 |
| `docs/architecture.md` (patch) | **Durable** | — | 随项目存在 |
| `docs/interfaces.md` (patch) | **Durable** | — | 随项目存在 |
| `docs/invariants.md` (patch) | **Durable** | — | 随项目存在 |
| `lessons.jsonl` (append) | **Durable** | — | 随项目存在 |
| `.archive/{task-id}/` | Archive | — | 不加载到后续上下文 |
| `event-log.jsonl` (append) | **Durable** | — | 可观测记录 |
| Git commit / PR | — | — | 代码交付 |

---

## Backflow 规则

| Settlement 字段 | 目标 Durable Doc | 操作 |
|----------------|-----------------|------|
| `api_contract_changes` | `docs/interfaces.md` | 增量 patch (add/modify/remove) |
| `architecture_changes` | `docs/architecture.md` | 增量 patch |
| `new_invariants` | `docs/invariants.md` | Append |
| `lessons` | `lessons.jsonl` | Append |
| `decisions_confirmed` | `docs/adr/` (如有对应 ADR) | 更新 status |

### Backflow 执行方式

- **早期（轻量）**：Agent 直接 patch markdown 文件
- **成熟期（确定性）**：脚本读取 reconcile-settlement.json → 自动 patch
- **规则**：如果 `backflow_targets.X = false`，跳过对应 doc 的更新

### 后续任务的 Context 加载

| 优先级 | 文档 | 加载时机 |
|--------|------|---------|
| 1 | `docs/architecture.md` | Phase 0 Always |
| 2 | `docs/invariants.md` | Phase 0 Always |
| 3 | `docs/interfaces.md` | Phase 1 按需 |
| 4 | `lessons.jsonl` (近期合成) | Phase 0 如存在 |
| **不加载** | 旧 spec.md / tasks.json | 除非显式追溯 |

---

## Gate 定义

### Settlement Validation Gate (内嵌)

| 属性 | 值 |
|------|-----|
| 类型 | Hard (Standard+) |
| 触发 | reconcile-settlement.json 产出后 |
| 行为 | Schema 校验 + Minimum Closure Contract 检查 |
| 失败 | 打回重生成，max 3 次 → escalation |

### Deliver Gate (内嵌)

| Profile | 行为 |
|---------|------|
| Quick | 直接 commit，无 PR |
| Simple | 直接 commit，可选 PR |
| Standard | Branch + PR |
| Complex | Branch + PR + CI 必须通过 |
| Orchestrated | Branch + PR + CI + 人工合并确认 |

### Conventional Commits Gate

| 属性 | 值 |
|------|-----|
| 类型 | Hard |
| 触发 | PreToolUse (git commit) |
| 行为 | 正则校验 commit message 格式 |
| 失败 | exit 2 阻断 |

---

## Profile 行为矩阵

| Step | Quick | Simple | Standard | Complex | Orchestrated |
|------|---------|--------|----------|---------|---------|
| 5.1 Settlement | ⬇️ commit msg 即 settlement | ⬇️ minimum + concerns | ✅ 标准 reconcile + AC 对账 | ✅ 完整 reconcile + AC 对账 | ✅ 完整 + retrospective |
| AC 对账 | 无 | 无 | ✅ 逐条 AC | ✅ 逐条 AC + traceability | ✅ 逐条 AC + traceability |
| Minimum Closure | summary + verify + scope | + concerns + lessons | planned_vs_actual + AC | 全字段 | 全字段 |
| DONE_WITH_CONCERNS | 允许直接 close | 允许直接 close | 需人工决策 | 需人工决策 | 需人工决策 |
| 5.2 Backflow | ⏭️ | ⬇️ 无 backflow | ✅ 接口+不变量 | ✅ 全量 patch | ✅ 全量 + lessons 合成 |
| 5.3 ADR 归档 | ⏭️ | ⏭️ | 条件触发 | ✅ | ✅ |
| 5.4 Transient 归档 | 无 transient | 无 | ✅ 移入 .archive | ✅ | ✅ |
| 5.5 Deliver | direct commit | direct commit | branch+PR | branch+PR+CI | +人工合并 |
| 5.6 Event log | ✅ 最小 | ✅ 最小 | ✅ 标准 | ✅ 完整 | ✅ 完整 |

---

## 参考框架

| 机制 | 来源 | 如何使用 |
|------|------|---------|
| PAUL reconcile | PAUL 框架 planned-vs-actual | 强制对账作为闭环条件 |
| Settlement schema | workflow-design-proposal.md §4.1 | 改造为 reconcile-settlement.json |
| Backflow rules | workflow-design-proposal.md §4.2 | 增量 patch 模式 |
| Spec 销毁 | workflow-design-proposal.md §4.2 | 归档到 .archive/ |
| Conventional Commits hook | GSD `gsd-validate-commit.sh` | PreToolUse hard gate |
| Event logging (JSONL) | FlowSpec | 完整生命周期记录 |
| Lessons append-only | yoyo-evolve `learnings.jsonl` | 经验回流 |
| 下续任务 context 加载 | Trellis JSONL injection | 精确注入 durable docs |
| Minimum Closure Contract | 12-Codex 建议 + PAUL | 按 profile 递减的最低闭环 |
| AC Traceability Matrix | 09-schemas.md §9 | 逐条 AC → Task → Evidence → Result |

---

## Hooks

| Hook | 事件 | 行为 |
|------|------|------|
| `settlement-generate` | Phase 5 进入 | 触发 reconcile-settlement 生成 |
| `settlement-validate` | settlement 产出 | Schema 校验 + Minimum Closure 检查 |
| `backflow-execute` | settlement 校验通过 | 执行 durable docs patch |
| `archive-transient` | backflow 完成 | 移动 transient 到 .archive/ |
| `commit-validate` | PreToolUse (git commit) | Conventional Commits 校验 |
| `event-log-close` | Phase 5 结束 | 写入完整任务记录 |

---

## 失败路径

| 场景 | Gate Taxonomy | 处理 |
|------|--------------|------|
| Settlement 生成质量差（遗漏字段） | `preflight` | Schema 校验 → 必填字段缺失时打回重生成 |
| Minimum Closure 不满足 | `preflight` | 阻断 DONE 标记，补充缺失字段 |
| ac_results 有 FAIL 但 concerns 为空 | `preflight` | 锁定为 DONE_WITH_CONCERNS，需人工决策 |
| Backflow patch 冲突 (并发任务) | `revision` | 乐观锁：检测 durable doc 版本 → 冲突时人工合并 |
| CI 失败 | `revision` | 回 Phase 3 修复 → 重跑 Phase 4 → 重入 Phase 5 |
| PR review 被拒 | `revision` | 按 reviewer 意见分类为 delta → 回对应 phase |
| Settlement 重生成 3 次仍不合格 | `escalation` | 暂停，用户介入补充信息 |

---

## Open Questions

1. **Transient 是否真的删除？还是移到 .archive？** — 当前设计：移到 `.archive/{task-id}/`。物理删除有审计风险，但 .archive 必须从默认 context 加载路径中排除。
2. **lessons.jsonl 的合成频率**：yoyo-evolve 每天合成一次。建议：Complex+ 任务结束时合成，其他累积到阈值再合成。
3. **durable docs 的注入策略**：全局加载 vs 按任务相关性过滤？Trellis 用 JSONL 做精确注入。早期可以全量加载 architecture + invariants（通常很短），interfaces 按需。
4. **DONE_WITH_CONCERNS 的自动化处理**：是否支持 `waiver` 策略让用户批量处理 quick/simple 层级的 concerns？还是统一要求人工逐条确认？
