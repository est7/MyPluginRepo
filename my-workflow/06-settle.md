# Phase 5: SETTLE — 结算 + Backflow + Transient 归档

## 目的

任务不在"代码写完、测试过了"时结束。任务在**输出结算结果并完成知识回流**时结束。

这个阶段解决一个根本问题：如果没有显式结算，项目知识只存在于 git log 和人的记忆里。下一个任务（可能是另一个 session 或另一个人）无法高效继承。

**核心原则**：Spec 是 transient，Acceptance Settlement 是 durable。

---

## 内部步骤

```
[来自 Phase 4 的 human acceptance = pass]
    │
    ▼
[Step 5.1] Settlement 生成
    │   Agent 基于执行产物生成结构化 settlement
    │   必须回答 9 个问题（来自 discussion-notes）
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
    │   spec.md, plan.md, tasks.md, delta-log.jsonl,
    │   code-understanding.md, effective-plan.md
    │   → 移入 .archive/{task-id}/ 或删除
    │   → 从后续任务的默认上下文加载列表中移除
    │
    ▼
[Step 5.5] Deliver (提交 + PR)
    │   Trivial/Simple: 直接 commit
    │   Moderate: commit + optional PR
    │   Complex+: branch + PR + CI gate
    │   Harness: branch + PR + CI + 人工合并确认
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

## 输入产物

| 产物 | 来源 | 必需？ |
|------|------|--------|
| Human acceptance = pass | Phase 4 | YES |
| 源代码变更 (staged/committed) | Phase 3 | YES |
| Baseline Plan + Delta Log | Phase 2-3 | 参考 |
| spec.md | Phase 2 | 参考 |
| verify-report.md | Phase 4 | 参考 |
| ADRs (如有) | Phase 2 | 参考 |

## 输出产物

| 产物 | 类型 | 生命周期 |
|------|------|---------|
| `settlement.json` | **Durable** (归档) | 永久，作为历史记录 |
| `docs/architecture.md` (patch) | **Durable** | 随项目存在 |
| `docs/interfaces.md` (patch) | **Durable** | 随项目存在 |
| `docs/invariants.md` (patch) | **Durable** | 随项目存在 |
| `lessons.jsonl` (append) | **Durable** | 随项目存在 |
| `.archive/{task-id}/` | Archive | 不加载到后续上下文 |
| `event-log.jsonl` (append) | **Durable** | 可观测记录 |
| Git commit / PR | — | 代码交付 |

---

## Settlement Schema

```json
{
  "task_id": "T-1024",
  "profile": "moderate",
  "execution_status": "success | partial | failed",
  "summary": "一句话描述改了什么",

  "changes": {
    "files_modified": ["src/a.ts", "src/b.ts"],
    "files_added": ["src/c.ts"],
    "files_deleted": []
  },

  "api_contract_changes": [
    { "type": "added | modified | removed", "entity": "UserService.getUser", "detail": "..." }
  ],

  "architecture_changes": [
    "新增 module-c，负责缓存层，依赖 module-a"
  ],

  "new_invariants": [
    "User ID must be UUID v4; integer IDs are deprecated"
  ],

  "decisions_confirmed": [
    "选择 Redis 替代本地缓存，原因：OOM 风险"
  ],

  "verification_done": {
    "unit_tests": "12 passed, 0 failed",
    "integration_tests": "3 passed",
    "e2e": "manual verification by developer",
    "coverage_delta": "+2.3%"
  },

  "residual_risks": [
    "Redis 连接池大小未调优，高并发下可能需要调整"
  ],

  "lessons": [
    "本地缓存在多实例部署下会导致不一致，早期应评估部署拓扑"
  ],

  "backflow_targets": {
    "architecture": true,
    "interfaces": true,
    "invariants": true
  }
}
```

### 9 个必答问题（来自 discussion-notes）

1. 改了什么 → `changes`
2. 当前行为是什么 → `summary`
3. 对外接口有无变化 → `api_contract_changes`
4. 架构边界有无变化 → `architecture_changes`
5. 哪些决策被确认 → `decisions_confirmed`
6. 验证做了什么 → `verification_done`
7. 还有哪些残余风险 → `residual_risks`
8. 哪些信息要进入长期文档 → `backflow_targets`
9. 下一个任务应该继承什么知识 → `lessons`

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
- **成熟期（确定性）**：脚本读取 settlement.json → 自动 patch
- **规则**：如果 `backflow_targets.X = false`，跳过对应 doc 的更新

### 后续任务的 Context 加载

| 优先级 | 文档 | 加载时机 |
|--------|------|---------|
| 1 | `docs/architecture.md` | Phase 0 Always |
| 2 | `docs/invariants.md` | Phase 0 Always |
| 3 | `docs/interfaces.md` | Phase 1 按需 |
| 4 | `lessons.jsonl` (近期合成) | Phase 0 如存在 |
| **不加载** | 旧 spec.md / plan.md | 除非显式追溯 |

---

## Gate 定义

### Deliver Gate (内嵌)

| Profile | 行为 |
|---------|------|
| Trivial | 直接 commit，无 PR |
| Simple | 直接 commit，可选 PR |
| Moderate | Branch + PR |
| Complex | Branch + PR + CI 必须通过 |
| Harness | Branch + PR + CI + 人工合并确认 |

### Conventional Commits Gate (G, from F8)

| 属性 | 值 |
|------|-----|
| 类型 | Hard |
| 触发 | PreToolUse (git commit) |
| 行为 | 正则校验 commit message 格式 |
| 失败 | exit 2 阻断 |

---

## Profile 行为矩阵

| Step | Trivial | Simple | Moderate | Complex | Harness |
|------|---------|--------|----------|---------|---------|
| 5.1 Settlement | ⏭️ 透传 | ⬇️ commit msg 即 settlement | ✅ 标准 schema | ✅ 完整 schema | ✅ 完整 + retrospective |
| 5.2 Backflow | ⏭️ | ⬇️ 无 backflow | ✅ 接口+不变量 | ✅ 全量 patch | ✅ 全量 + lessons 合成 |
| 5.3 ADR 归档 | ⏭️ | ⏭️ | 条件触发 | ✅ | ✅ |
| 5.4 Transient 归档 | 无 transient | 无 | ✅ 移入 .archive | ✅ | ✅ |
| 5.5 Deliver | direct commit | direct commit | branch+PR | branch+PR+CI | +人工合并 |
| 5.6 Event log | ✅ 最小 | ✅ 最小 | ✅ 标准 | ✅ 完整 | ✅ 完整 |

---

## 参考框架

| 机制 | 来源 | 如何使用 |
|------|------|---------|
| Settlement schema | workflow-design-proposal.md §4.1 | 改造为 9 必答 |
| Backflow rules | workflow-design-proposal.md §4.2 | 增量 patch 模式 |
| Spec 销毁 | workflow-design-proposal.md §4.2 | 归档到 .archive/ |
| Conventional Commits hook | GSD `gsd-validate-commit.sh` | PreToolUse hard gate |
| Event logging (JSONL) | FlowSpec | 完整生命周期记录 |
| Lessons append-only | yoyo-evolve `learnings.jsonl` | 经验回流 |
| 下续任务 context 加载 | Trellis JSONL injection | 精确注入 durable docs |

---

## Hooks

| Hook | 事件 | 行为 |
|------|------|------|
| `settlement-generate` | Phase 5 进入 | 触发 settlement 生成 |
| `backflow-execute` | settlement 完成 | 执行 durable docs patch |
| `archive-transient` | backflow 完成 | 移动 transient 到 .archive/ |
| `commit-validate` | PreToolUse (git commit) | Conventional Commits 校验 |
| `event-log-close` | Phase 5 结束 | 写入完整任务记录 |

---

## 失败路径

| 场景 | 处理 |
|------|------|
| Settlement 生成质量差（遗漏字段） | Schema 校验 → 必填字段缺失时打回重生成 |
| Backflow patch 冲突 (并发任务) | 乐观锁：检测 durable doc 版本 → 冲突时人工合并 |
| CI 失败 | → 回 Phase 3 修复 → 重跑 Phase 4 → 重入 Phase 5 |
| PR review 被拒 | → 按 reviewer 意见分类为 delta → 回对应 phase |

---

## Open Questions

1. **acceptance result 和 retrospective 是一个文档还是两个？**（来自 discussion-notes 未决问题）— 当前设计：合并为一个 `settlement.json`，其中 `lessons` 字段承载 retrospective。如果 harness 层需要更深度的回顾，可以额外生成 `retrospective.md`。
2. **Transient 是否真的删除？还是移到 .archive？** — 当前设计：移到 `.archive/{task-id}/`。物理删除有审计风险，但 .archive 必须从默认 context 加载路径中排除。
3. **lessons.jsonl 的合成频率**：yoyo-evolve 每天合成一次。我们是每个任务结束合成，还是按天？考虑到任务频率可能远高于每天一次，按任务合成可能更及时。但如果一天做 10 个 trivial 任务，每次合成就太频繁了。建议：Complex+ 任务结束时合成，其他累积到阈值再合成。
4. **durable docs 的注入策略**：全局加载 vs 按任务相关性过滤？Trellis 用 JSONL 做精确注入。早期可以全量加载 architecture + invariants（通常很短），interfaces 按需。
