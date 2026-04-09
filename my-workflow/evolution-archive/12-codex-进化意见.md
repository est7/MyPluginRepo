# Codex 进化意见 v2

> 这不是对 `09/10/11` 的摘要，也不是“再来一份并列观点”。
> 这份文档的目标是直接替当前讨论做裁决：哪些方向现在就该定，哪些先预留，哪些不值得继续摇摆。

## 1. 我的总判断

`my-workflow` 下一步最该进化的，不是 phase 数量，不是 agent 数量，也不是先做完整 harness。

最该做的是把它从“结构清楚的工作流骨架”推进成“关键路径可校验的协议面”。

一句话说清：

- **先把 `AC -> Task -> Evidence -> Reconcile` 这条链做硬**
- **再把复杂任务切成 `slice / wave / fresh-context`**
- **最后才考虑更重的 harness 编排**

这意味着我对当前几个分歧点的裁决是：

1. `protocol-first` 优先于 `enforcement-first`
2. `task/ac/evidence` 现在就要 machine-checkable
3. `slice/wave` 重要，但不是 P0
4. `trivial/simple` 可以压 ceremony，但不能失去最小 closure
5. 当前阶段应以 **repo 内结构化 artifact** 作为真相源

---

## 2. 对五个分歧点的正式裁决

### 2.1 `protocol-first` vs `enforcement-first`

我的裁决：**先协议，后硬化；但关键路径上的 enforcement 要同步落。**

原因很简单：

- 没有协议，enforcement 不知道该检查什么
- 没有 enforcement，协议会退化成“建议文档”

但在顺序上，还是应该先定义清楚下面这些结构：

- `AC` 长什么样
- `task` 长什么样
- `verify-evidence` 长什么样
- `reconcile` 长什么样

然后只对关键路径做第一批硬门禁：

- 无 `verify-evidence` 不得完成 verify
- 无 AC 对账不得关闭 settle
- 超 scope 修改自动触发 delta/re-entry

所以我的答案不是二选一，而是：

> **先把协议定义到可校验，再把关键 gate 做成不可绕过。**

### 2.2 `plan/task` 要不要现在 machine-checkable

我的裁决：**要，而且现在就要。**

如果这一步继续拖，后面的所有“验证优于自报告”都会缺支点。

我建议的最低字段不是很重，但必须有：

```json
{
  "id": "task-003",
  "goal": "实现登录态校验",
  "covers_ac": ["AC-1", "AC-3"],
  "verify_cmd": "npm test -- --testPathPattern=auth",
  "allowed_paths": ["src/auth/**", "tests/auth/**"],
  "depends_on": ["task-002"],
  "rollback": "git restore --source=HEAD~1 -- src/auth"
}
```

这里最关键的不是 JSON 本身，而是这 4 个关系被显式化：

- `task` 覆盖哪些 `AC`
- `task` 怎么验证
- `task` 允许改哪里
- `task` 依赖谁

没有这层，`SETTLE` 里的逐条 AC 对账会永远停留在自然语言总结。

### 2.3 `slice/wave` 现在是不是过早

我的裁决：**不是过早，但不是第一优先级。**

我同意 `09` 里的判断：复杂任务如果没有 `slice`，`EXECUTE` 会不断膨胀，最后把 long-session 压力全留给模型。

但如果在 `task/ac/evidence` 还没硬化前就上 `slice/wave`，大概率会出现两个问题：

- `slice` 只是新文档，不是新控制面
- 并行发生了，但 closure 和 verify 还是软的

所以我的排序是：

- **P0**：`task/ac/evidence/reconcile`
- **P1**：`slice.md`、`wave.json`、`handoff.md`
- **P2**：更重的 worktree orchestration / dispatcher runtime

也就是说：

> `slice/wave` 该做，但应该建立在协议化 task 之上，而不是替代它。

### 2.4 `trivial/simple` 应该压缩到什么程度

我的裁决：**压 ceremony，但不压 closure。**

我不赞成让轻任务直接变成“改完就算结束”。那样系统很快会形成两个世界：

- 重任务有闭环
- 轻任务没有闭环

这会导致 durable knowledge 永远只沉淀“大任务”，而大量日常真实变更没有可追溯结果。

我建议引入 **Minimum Closure Contract**：

| Profile | 最低关闭要求 |
|---------|--------------|
| `trivial` | `actual` + `verify` + `touched_files` |
| `simple` | `actual` + `verify` + `touched_files` + `concern?` |
| `moderate` | 轻量 reconcile + AC 对账 |
| `complex+` | 完整 reconcile + 人类 acceptance |

这样保住两件事：

- ceremony compression 仍然成立
- “完成”仍然有可追溯定义

### 2.5 真相源到底放在哪

我的裁决：**当前阶段先选 repo 内结构化 artifact 作为唯一真相源。**

我理解 PAUL 那种 issue-centered 设计的价值，但对你这个仓库现在的阶段来说，它会把问题提前带到 GitHub integration、双向同步、review lifecycle 绑定上，成本太高。

现阶段更稳的做法是：

- `spec / plan / tasks / delta / verify-evidence / reconcile` 都先在 repo 内定义
- `docs/` 和 `.workflow/` 承担主要状态
- 以后如果接 issue / PR，再做“外部状态镜像”或“双源桥接”

所以我不接受“现在就上 issue-as-source-of-truth”。

我接受的是：

> **先把仓库内部状态做成可重建、可对账、可恢复；外部系统后接。**

---

## 3. 我赞同 `09/10/11` 的部分

### 3.1 我赞同 `09` 的地方

我赞同 `09` 的三个主张：

- 当前问题在协议层，而不在 phase 结构
- 复杂任务需要 `slice / wave / handoff`
- `reconcile` 应该成为唯一 closure artifact

但我不同意把 `slice` 的优先级放得高于 `task/ac/evidence`。

### 3.2 我赞同 `10` 的地方

我赞同 `10` 里最具体的 7 个实现点：

1. `context.jsonl`
2. `SDD -> BDD -> TDD`
3. `spec.md` 的“约束 + 场景”结构
4. `tasks.json` 强制 `verify_cmd`
5. `Red -> Green -> Refactor`
6. `stdout evidence`
7. `reconcile-settlement.json`

但我不同意让这些具体实现挤掉 `v1` 里已有的 `profile/gate/state/observability`。

### 3.3 我赞同 `11` 的地方

我几乎完全赞同 `11` 对 enforcement 的诊断。

尤其是这 4 点：

- `verify-evidence` 要结构化
- `covers_ac` 必须补
- profile 要和 enforcement 一起做减法
- fresh-context resume 需要固定 bootstrap 顺序

但我不同意把 `plan.json` 的重要性放到比 `verify_cmd` 更后。  
我的判断是：两者都该尽快进入主线，只是 `verify_cmd` 更容易先落。

---

## 4. 这轮我新增的 6 个进化点

这 6 个点不是对 `09/10/11` 的重复，而是我认为还可以再补的控制面。

### 4.1 AC Traceability Matrix

不只是在 `task` 里写 `covers_ac`，还要在 verify 和 settle 时能反查：

```text
AC-1 -> task-001, task-003 -> verify-evidence-001, 004 -> PASS
AC-2 -> task-002 -> verify-evidence-002 -> FAIL
```

这样 `SETTLE` 才能做真正的逐条 AC closure，而不是总结性 closure。

### 4.2 Scope Guard

在 task 协议中加入：

- `allowed_paths`
- `expected_modules`
- `forbidden_paths`（可选）

执行结果一旦超界：

- 轻则记 delta
- 重则自动触发 re-entry

这比“请不要越界修改”有效得多。

### 4.3 Evidence Bundle

`stdout evidence` 还不够完整。  
我建议定义最小 `verify-evidence.json`：

```json
{
  "task_id": "task-003",
  "verify_cmd": "npm test -- --testPathPattern=auth",
  "exit_code": 0,
  "stdout_hash": "sha256:abc123",
  "stdout_excerpt": "PASS src/auth/login.test.ts",
  "artifact_paths": ["coverage/coverage-summary.json"],
  "timestamp": "2026-04-08T10:30:00Z"
}
```

这会让 `Ralph Loop` 真正有抓手。

### 4.4 Review Split: `spec-fit` vs `quality-fit`

当前 `VERIFY` 里“审查”还是偏混。

我建议明确拆成两个结果：

- `spec-fit`: 有没有按 spec / AC / boundaries 做对
- `quality-fit`: 有没有代码味道 / 风险 / 性能 / 安全问题

这样 review 才不会混成一句“整体还行，但是有点问题”。

### 4.5 Minimum Closure Contract

这是我认为必须补的 profile 级设计。

重点不是把 trivial/simple 拉重，而是避免“简单任务无结算”。

如果这条不补，长期 durable knowledge 一定会偏科。

### 4.6 Protocol Overlay

我不建议马上大改 `00-07` 所有文档。  
更稳的方式是先补一层独立协议文档或在 `12` 中先冻结新增协议：

- `tasks.json` schema
- `verify-evidence.json` schema
- `reconcile-settlement.json` schema
- `resume-bootstrap` 顺序
- `closure by profile`

等协议冻结后，再逐个回写主线文档。

这会明显降低重构风险。

---

## 5. 我的优先级排序

### P0：现在就该定

1. `tasks.json` 最小 schema
2. `covers_ac`
3. `verify_cmd`
4. `verify-evidence` schema
5. `reconcile-settlement.json`
6. `minimum closure contract`

### P1：下一轮补强

7. `context.jsonl`
8. `resume-bootstrap`
9. `spec-fit / quality-fit` 双审查
10. `Scope Guard`
11. `gate taxonomy`
12. `completion markers`

### P2：复杂任务扩展

13. `slice.md`
14. `wave.json`
15. `handoff.md`
16. worktree-based parallel execution
17. thin orchestrator / fat worker 的结构约束

### P3：Harness 预留

18. dispatcher runtime
19. DAG dependency checker
20. pass@k
21. 多模型 reviewer 并行

---

## 6. 对现有主线文档的改造建议

### `00-overview.md`

补 3 件事：

- `Profile × Closure` 矩阵
- `AC -> Task -> Evidence -> Reconcile` 主链
- 当前阶段的唯一真相源声明

### `03-spec-and-plan.md`

补 4 件事：

- `tasks.json` 最小 schema
- `covers_ac`
- `verify_cmd`
- `allowed_paths`

### `04-execute.md`

补 4 件事：

- `Scope Guard`
- worker 不得越 task scope
- delta 触发条件中的“超 allowed_paths”
- thin orchestrator 的角色边界

### `05-verify.md`

补 4 件事：

- `verify-evidence` schema
- `spec-fit / quality-fit`
- Ralph Loop 的硬触发条件
- evidence 缺失时的失败路由

### `06-settle.md`

补 3 件事：

- `reconcile-settlement.json`
- AC traceability matrix
- `DONE_WITH_CONCERNS` 不得直接关闭

### `07-cross-cutting.md`

补 4 件事：

- `resume-bootstrap`
- `completion markers`
- `gate taxonomy`
- protected file / scope / verify 相关的 enforcement 分级

---

## 7. 最终结论

我的最终立场很明确：

当前 `my-workflow` 不该继续在“phase 怎么命名”或“要不要直接上 harness”上消耗讨论。

下一步最值钱的，是先冻结下面这条主链：

```text
AC
  -> tasks.json
  -> verify-evidence.json
  -> reconcile-settlement.json
  -> durable backflow
```

只要这条链没硬起来：

- `verify over self-report` 就只是口号
- `reconcile is closure` 就只是态度
- `fresh-context resume` 就缺少恢复支点
- `slice/wave` 也只是更复杂的 ceremony

所以我的裁决是：

> **先把闭环协议做硬，再把复杂执行做强。**

这比直接扩 phase、扩 agent、扩 harness，更符合当前 `my-workflow` 的成熟度。
