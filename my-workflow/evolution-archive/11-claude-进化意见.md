# Claude 进化意见

> 我的角色定位：作为主持这次对比实验的 Team Lead，我既读完了 19 份研究材料，也读完了 Codex 和 Gemini 已经提交的意见。
> 本文不做摘要，不做综合，只写**我自己的判断**——包括我在哪里同意它们，在哪里不同意，以及我认为它们都没说到位的地方。

---

## 1. 我的核心立场

先把结论摆在最前面：

**当前 `my-workflow` 最大的问题不是缺功能，而是缺"执行力保障"。**

Codex 的意见侧重"协议层补薄"，Gemini 的意见侧重"v2 具体实现应并回主线"。两者都是对的，但我认为它们共同忽略了一个更根本的问题：

> **workflow 文档写得再好，如果没有 enforcement 机制，agent 会系统性地绕开它。**

这不是猜测。这是 19 份材料里反复出现的事实。Trellis 用 JSONL hook 强制注入；GSD 用 stall detection 强制检出；Superpowers 用 Ralph Loop 强制证据；PAUL 用 reconcile 强制闭环。这些机制不是"锦上添花"，它们存在的原因，是**软约束在 agent 压力下一定会被侵蚀**。

因此我的进化方向，比 Codex 和 Gemini 更偏向**把关键路径从"文档约定"变成"物理不可绕"**。

---

## 2. 我在哪里同意 Codex

Codex 的 8 条工程规律，我全部同意。尤其是：

- **"plan 不只是说明文档，更应该是 agent 间通信协议"** — 这是当前骨架最值得改的单点
- **"软约束只能塑形，关键路径必须有硬门禁"** — 这是我整个进化方案的基础假设
- **"复杂流程必须支持 ceremony compression，否则 simple 任务一定绕开系统"** — 这是 profile 减法矩阵的正确方向

Codex 提出的 7 个 gap 我也认同，但我认为 4.1（切片协议）和 4.3（Plan as Protocol）的优先级应该对调。**Plan as Protocol 是前提，切片协议是 Plan as Protocol 成熟后的自然延伸**。先做切片而不做协议化 plan，切片会退化成又一层文档。

---

## 3. 我在哪里同意 Gemini

Gemini 给出的 7 个具体实现清单很准：

1. `context.jsonl` 最小 schema
2. `SDD → BDD → TDD` 漏斗
3. `spec.md` 的"约束 + 场景"结构
4. `tasks.json` 强制要求 `verify_cmd`
5. `Red → Green → Refactor` 执行循环
6. `stdout evidence` 版 Ralph Loop
7. `reconcile-settlement.json` 作为唯一 closure artifact

这 7 项我都支持并回主线。但 Gemini 的整个意见都建立在一个前提上：**agent 会主动遵守这些实现要求**。这个前提我不接受。

---

## 4. 我认为两者都没说到位的地方

这是本文的核心部分。

### 4.1 Enforcement 层几乎缺失

当前骨架描述了**应该做什么**，但几乎没有描述**如果不做会怎样**。

成熟框架的 enforcement 机制通常分三层：

| 层级 | 机制 | 在当前骨架的状态 |
|------|------|-----------------|
| 物理层 | hook 拦截、文件写保护、工具调用限制 | `07-cross-cutting.md` 有概述，但无协议 |
| 协议层 | gate hard-block、completion marker、plan validator | gate 有定义，但 hard block 条件不清晰 |
| 行为层 | anti-rationalization、bounded revision、stall detection | 基本缺失 |

**具体建议：**

`07-cross-cutting.md` 应新增 `enforcement.md` 子节，明确列出：

```text
物理写保护文件清单（PreToolUse hook 级别）
Gate hard-block 触发条件（vs soft 警告条件）
Anti-rationalization 检查清单（封堵"先跳过"借口）
Stall detection 阈值（同一 task revision 超过 N 次 → escalation）
```

这不是文档风格问题，是**骨架能否在真实 agent 压力下维持完整性**的问题。

### 4.2 Verification 的证据链缺少结构化标准

两份意见都提到了 Ralph Loop 和"stdout evidence"，但都没有定义**证据链应该长什么样**。

当前 `05-verify.md` 要求 agent 提供验证证据，但没有定义证据的最小结构。这导致 agent 很容易用"测试通过"这句话来代替实际证据。

**具体建议：**

定义 `verify-evidence` 结构：

```json
{
  "task_id": "task-003",
  "verify_cmd": "npm test -- --testPathPattern=auth",
  "stdout_hash": "sha256:abc123",
  "stdout_excerpt": "PASS src/auth/login.test.ts (3 tests)",
  "result": "PASS",
  "timestamp": "2026-04-08T10:30:00Z"
}
```

Ralph Loop 的触发条件应精确到：**`verify-evidence` 缺失或 `result` 不为 PASS → task 不得标记 closed**。

这比"必须提供证据"这种软要求强得多。

### 4.3 AC 与 Task 的绑定关系缺失

当前 `spec.md` 有 BDD 场景，`plan.md` 有 task list，但两者之间**没有显式的映射关系**。

这带来的具体问题是：到了 VERIFY 和 SETTLE 阶段，"AC 逐条 PASS/FAIL"变成了无法机械执行的要求，因为没有人知道哪个 task 覆盖哪个 AC。

**具体建议：**

在 `tasks.json` 的每个 task 中增加 `covers_ac` 字段：

```json
{
  "id": "task-003",
  "description": "Implement JWT validation in auth middleware",
  "covers_ac": ["AC-1", "AC-3"],
  "verify_cmd": "npm test -- --testPathPattern=auth",
  "rollback": "git revert HEAD"
}
```

SETTLE 阶段的 reconcile 才能真正做到"逐条 AC 对账"，而不是一段总结性文字。

### 4.4 Profile 减法矩阵与 Enforcement 的交叉设计缺失

两份意见都没有处理一个张力：**profile 减法做得越激进，enforcement 机制越容易被跳过**。

比如 `trivial` profile 跳过了 spec/plan，但 enforcement 机制（gate、Ralph Loop、reconcile）是否也被跳过？如果跳过了，trivial 任务里的 agent 等于完全无约束；如果不跳过，trivial 任务的 ceremony 成本和 moderate 相差无几。

**具体建议：**

在 `00-overview.md` 的 profile 矩阵里，增加"enforcement 减法"的显式设计：

```text
| Profile    | Gate hard-block | Ralph Loop | Reconcile     | Anti-rat checklist |
|------------|-----------------|------------|---------------|--------------------|
| trivial    | G0 only         | skip       | skip          | skip               |
| simple     | G0, G1, G9      | lightweight| summary only  | skip               |
| moderate   | G0-G9 (soft)    | required   | required      | required           |
| complex    | G0-G11 (hard)   | required   | full AC audit | required           |
| harness    | G0-G11 + custom | required   | full AC audit | required           |
```

这让 enforcement 和 profile 一起做减法，而不是让 enforcement 在简单任务里变成负担。

### 4.5 Thin Orchestrator 原则没有落成结构约束

GSD 的"Thin Orchestrator + Fat Worker"原则在 Codex 的 Option C 里出现，但被归类为"只适合 Harness profile 时再上"。

我不同意这个判断。

Thin Orchestrator 的核心不是"要不要有 dispatcher 进程"，而是一条行为约束：**Orchestrator 不写代码，Worker 不改目标函数**。这条约束对 moderate 以上的任务都应该成立。

**具体建议：**

在 `04-execute.md` 的执行角色约定里增加：

```text
Orchestrator 职责（边界清单）：
  ✓ 分配 task 给 Worker
  ✓ 读取 verify-evidence
  ✓ 决定是否触发 delta re-entry
  ✗ 不直接写业务代码
  ✗ 不修改 spec 的目标函数

Worker 职责（边界清单）：
  ✓ 执行单个 task
  ✓ 生成 verify-evidence
  ✗ 不主动修改其他 task 的范围
  ✗ 不自行决定跳过 verify_cmd
```

这不需要实现 dispatcher 进程，只需要在文档里把角色边界写成协议。

### 4.6 Fresh-context Resume 的加载顺序未定义

Codex 提到了"fresh-context 优先"的恢复策略，Gemini 没有专门提。但两者都没有定义**恢复时加载文件的顺序和边界**。

当前 `07-cross-cutting.md` 的 pause/resume 机制定义了状态文件，但没有定义新 session 启动时的 bootstrap 顺序。这导致恢复的质量完全依赖 agent 的即兴判断。

**具体建议：**

定义 `resume-bootstrap` 协议：

```text
Step 1: 加载 .workflow/state.json（当前 phase、task 指针、delta 计数）
Step 2: 加载 durable artifacts（architecture.md, invariants.md, interfaces.md）
Step 3: 加载当前 slice 的 context.jsonl 指向文件（只加载 JSONL 声明的，不全量加载）
Step 4: 加载最近一条 verify-evidence（不加载历史对话）
Step 5: 就绪，继续当前 task

禁止：
- 依赖历史对话恢复状态
- 全量加载代码库
- 从 settle 记录反推当前任务
```

这让 fresh-context resume 变成可重复执行的确定性流程，而不是"agent 尽力回忆"。

---

## 5. 我的优先级排序

综合上述 6 个点，我的建议优先级如下：

### P0：立刻补（不补就是骨架空转）

1. **`tasks.json` 增加 `covers_ac` + `verify_cmd` 字段**（AC 绑定）
2. **定义 `verify-evidence` schema 并把 Ralph Loop 硬绑到它**（证据链结构化）
3. **Gate hard-block 触发条件的显式化**（enforcement 协议化）

### P1：下一轮补（提升可靠性的关键）

4. **Profile × Enforcement 交叉矩阵**（减法对齐）
5. **`resume-bootstrap` 协议**（fresh-context 确定性）
6. **Orchestrator/Worker 角色边界写入 `04-execute.md`**（行为约束）

### P2：再下一轮（扩展能力）

7. **`slice.md` + `wave.json` 切片协议**（Codex 的 4.1，但先做 P0/P1）
8. **`plan.json` 协议化 + validator**（Codex 的 4.3，值得做但不急）
9. **Anti-rationalization 清单**（Gemini 有具体内容，可直接并入）

---

## 6. 对 Codex 和 Gemini 意见的综合判断

| 维度 | Codex | Gemini | 我的判断 |
|------|-------|--------|----------|
| 整体方向 | 协议层补薄 | v2 具体实现并回 | 两者都对，但缺 enforcement 视角 |
| 优先项 | 切片协议优先 | 7 项具体实现并回 | P0 应是证据链 + AC 绑定，不是切片 |
| 骨架态度 | 保留 6 phase + 加子层 | v1 骨架保留，v2 方法论并入 | 同意，不推倒重来 |
| Plan 协议化 | 建议 plan.json + validator | 建议 tasks.json + verify_cmd | 两者结合，但 verify_cmd 优先于 plan.json |
| Enforcement | 提到 hard-block，不够深 | 基本未提 | 这是最大的共同盲区 |
| Fresh-context | 提到，未定义顺序 | 未专门提 | 需要 bootstrap 顺序协议 |
| Profile 减法 | 未处理与 enforcement 的交叉 | 未处理 | 两者都遗漏了这个张力 |

---

## 7. 一句话总结

Codex 说"把协议层做硬"，Gemini 说"把具体实现并回主线"，都是对的。

我的补充是：**这两件事做完之后，如果 agent 仍然可以不留证据就关 task、不对账就关 phase，那整个骨架依然是纸老虎。**

真正的进化方向是：**每一条规则，要么有 hook 拦截，要么有 schema 校验，要么有 gate hard-block——三选一，没有第四选项。**

文档描述的，是理想路径。Enforcement 保障的，是最坏情况下的下限。骨架的可靠性，取决于下限，不取决于理想路径。
