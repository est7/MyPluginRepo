# Workflow Research Report: recursive-mode

> **研究日期**: 2025-07  
> **仓库**: recursive-mode  
> **文件数**: ~215  
> **许可证**: 未明确声明  

---

## 1. 框架概况

recursive-mode 是一个 **file-backed structured workflow** 系统，用持久化的 Markdown 文件替代 chat history 作为 AI agent 的工作记忆。系统定义了 7 个有序阶段的状态机（requirements → planning → implementation → testing → review → closeout → memory），并提供 7 个可独立安装的 subskill。核心设计理念是 **context window 不可靠，文件系统才是真正的持久存储**。

| 属性 | 值 |
|------|------|
| **类型** | File-Backed Structured Workflow (Claude Code Skill Collection) |
| **语言** | Markdown (skill 定义) + Bash (hooks) |
| **入口** | 7 个可安装 subskill |
| **核心目录** | `.workflow/` (artifact 存储) |
| **阶段数** | 7 (requirements → memory) |
| **Subskill 数** | 7 (recursive-mode + 6 specialized) |

---

## 2. 源清单

| 文件/目录 | 用途 | 重要度 |
|-----------|------|--------|
| `recursive-mode/SKILL.md` | 主 workflow skill (7-phase 状态机) | ★★★ |
| `recursive-spec/SKILL.md` | 需求规约 subskill | ★★★ |
| `recursive-worktree/SKILL.md` | Git worktree 隔离 subskill | ★★☆ |
| `recursive-debugging/SKILL.md` | 结构化调试 subskill | ★★☆ |
| `recursive-tdd/SKILL.md` | TDD 工作流 subskill | ★★☆ |
| `recursive-review-bundle/SKILL.md` | Review bundle 生成 subskill | ★★☆ |
| `recursive-subagent/SKILL.md` | 子 agent 编排 subskill | ★★☆ |
| `.workflow/` | Workflow artifact 存储目录 | ★★★ |
| `README.md` | 安装指南与 skill 概览 | ★★☆ |

---

## 3. 对象模型

### 核心实体

```
Workflow (.workflow/ 目录)
  ├── requirements.md         # 需求文档
  ├── plan.md                 # 实施计划
  ├── implementation-log.md   # 实现日志
  ├── test-results.md         # 测试结果
  ├── review-bundle.md        # Review 摘要
  ├── closeout.md             # 收尾记录
  └── memory.md               # 跨 session 记忆

Phase (7 个有序阶段)
  ├── name: string
  ├── order: number (1-7)
  ├── artifact: string        # 对应的 .workflow/ 文件
  ├── entry_condition: string # 进入条件
  ├── exit_condition: string  # 退出条件
  └── allowed_transitions: Phase[]

SubSkill (7 个可安装组件)
  ├── name: string
  ├── skill_file: SKILL.md
  ├── domain: string          # 覆盖的 workflow 阶段
  └── standalone: bool        # 是否可独立使用
```

### 实体关系

- **Workflow** 由 7 个 **Phase** 组成（严格顺序）
- 每个 **Phase** 产出一个 **Artifact** 文件
- 7 个 **SubSkill** 分别覆盖 workflow 的不同阶段
- `recursive-mode` 是主 skill，其他 6 个为可选增强

### Context 隔离

所有 workflow state 持久化到 `.workflow/` 目录。每个 subskill 独立加载自己的 SKILL.md，通过读取 `.workflow/` 文件获取上下文，不依赖 chat history。

---

## 4. 流程与状态机

### 7-Phase State Machine

```
[Phase 1: Requirements]
   收集需求 → 写入 .workflow/requirements.md
   ↓
[Phase 2: Planning]
   基于需求制定计划 → 写入 .workflow/plan.md
   ↓
[Phase 3: Implementation]
   按计划逐步实现 → 更新 .workflow/implementation-log.md
   ↓
[Phase 4: Testing]
   运行测试 → 写入 .workflow/test-results.md
   ├── 通过 → Phase 5
   └── 失败 → 回退 Phase 3 修复
   ↓
[Phase 5: Review]
   生成 review bundle → 写入 .workflow/review-bundle.md
   ↓
[Phase 6: Closeout]
   收尾记录 → 写入 .workflow/closeout.md
   ↓
[Phase 7: Memory]
   提取跨 session 记忆 → 写入 .workflow/memory.md
```

### 状态转移规则

| 当前 Phase | 触发条件 | 下一 Phase | 可回退 |
|------------|----------|------------|--------|
| Requirements | 需求文档完成 | Planning | 否 |
| Planning | 计划审核通过 | Implementation | → Requirements |
| Implementation | 代码完成 | Testing | → Planning |
| Testing | 测试通过 | Review | → Implementation |
| Testing | 测试失败 | Implementation | 强制回退 |
| Review | Review 通过 | Closeout | → Implementation |
| Closeout | 收尾完成 | Memory | 否 |
| Memory | 记忆提取完成 | Done | 否 |

### SubSkill Happy Path

```
recursive-spec:
  收集需求 → 结构化为 requirements.md → 明确 scope + constraints

recursive-worktree:
  创建 git worktree → 隔离分支工作 → 完成后 merge + cleanup

recursive-tdd:
  Red (写失败测试) → Green (最小实现) → Refactor (优化) → 循环

recursive-debugging:
  复现问题 → 假设 → 验证 → 修复 → 回归测试

recursive-review-bundle:
  收集 diff → 生成结构化 review summary → 标注风险点

recursive-subagent:
  拆解任务 → 分配给 sub-agent → 收集结果 → 合并
```

### Failure Paths

| 失败场景 | 系统响应 |
|----------|----------|
| 测试失败 | 强制回退 Implementation，不允许跳过 |
| Review 发现问题 | 回退 Implementation，附带 review feedback |
| 计划与需求不匹配 | 回退 Requirements 阶段 |
| Session 中断 | 从 `.workflow/` 文件恢复状态 |

---

## 5. 执行保障审计

| 机制 | 级别 | 说明 |
|------|------|------|
| File-backed state persistence | **Hard** | 所有状态写入 `.workflow/` 文件，可审计可恢复 |
| Phase 顺序强制 | **Soft** | SKILL.md prompt 要求顺序执行，无 hook 阻断跳过 |
| Test failure → Implementation 回退 | **Soft** | Prompt 指令，非自动化检测 |
| Review bundle 必须生成 | **Soft** | SKILL.md 要求但无 gate |
| Memory extraction | **Soft** | 最后阶段，容易被跳过 |
| Git worktree 隔离 | **Hard** | recursive-worktree 使用真实 git worktree 命令 |
| TDD Red-Green-Refactor 顺序 | **Soft** | 仅 prompt 引导 |
| Artifact 完整性 | **Unenforced** | 不检查 `.workflow/` 文件是否为空或缺失 |

---

## 6. Prompt 目录

### Prompt 1: recursive-mode 主 skill（7-Phase 调度）

```
你正在执行结构化开发工作流。所有状态保存在 .workflow/ 目录。

阶段流程:
1. Requirements — 读取或创建 .workflow/requirements.md
2. Planning — 基于需求制定 .workflow/plan.md
3. Implementation — 按计划实现，日志写入 implementation-log.md
4. Testing — 运行测试，结果写入 test-results.md
   - 失败 → 回退 Implementation
5. Review — 生成 review-bundle.md
6. Closeout — 写入 closeout.md
7. Memory — 提取记忆到 memory.md

规则:
- 每个阶段开始前读取前置 artifact
- 每个阶段结束时更新对应 artifact
- 测试失败必须回退，不可跳过
- Session 恢复: 读取 .workflow/ 确定当前阶段
```

### Prompt 2: recursive-tdd（TDD 子流程）

```
TDD 工作流:
1. RED — 编写一个失败的测试 (验证测试确实失败)
2. GREEN — 编写最小代码使测试通过 (不多不少)
3. REFACTOR — 优化代码 (保持测试通过)
4. 重复

规则:
- 不写不被测试驱动的代码
- 每个 Green 步骤只添加使当前测试通过的最小代码
- Refactor 后必须重新运行全部测试
```

---

## 7. 微观设计亮点

### 7.1 `.workflow/` 作为 State Machine 的持久化层

每个 Phase 的产出对应一个具体文件，agent 可以通过检查文件存在性和内容来推断当前阶段。这是一种 "implicit state machine"——状态不存储为枚举值，而是通过 artifact 的存在与否来推导。

### 7.2 Memory Phase 的跨 Session 知识提取

独特的第 7 阶段 "Memory" 要求 agent 在任务完成后主动提取有价值的知识点（决策理由、发现的 pattern、踩过的坑）到 `memory.md`。这为下一个 session 的 agent 提供了结构化的知识传递通道。

### 7.3 SubSkill 的可组合性

7 个 subskill 可以独立安装和使用。用户可以只安装 `recursive-tdd` 而不需要完整的 7-phase workflow。这种模块化设计降低了采纳门槛——用户可以从单个 subskill 开始，逐步扩展到完整 workflow。

---

## 8. 宏观设计亮点

### 8.1 "File System is the Real Memory" 哲学

recursive-mode 建立在一个关键洞察之上：**LLM 的 context window 是 volatile memory（会被清空），而文件系统是 persistent storage（始终可读）**。通过将所有工作状态写入文件，agent 获得了跨 session 的持久记忆能力。这与 planning-with-files 的 "Filesystem as Memory" 原则一脉相承，但 recursive-mode 将其推向了更结构化的 7-phase 框架。

### 8.2 Full Lifecycle Coverage with Progressive Adoption

从需求到记忆的 7 个阶段覆盖了软件开发的完整生命周期。但通过 subskill 机制，用户不必一次性采纳全部阶段。这种 "progressive adoption" 策略平衡了框架的全面性和用户的接受度。

---

## 9. 失败模式与局限

| # | 失败模式 | 严重度 | 说明 |
|---|----------|--------|------|
| 1 | **Phase 跳过无阻断** | 高 | 顺序执行仅由 prompt 约束，agent 可以直接跳到 Implementation |
| 2 | **Artifact 质量不可验证** | 中 | `.workflow/` 文件的内容质量无自动检查（可能为空或低质量） |
| 3 | **Memory Phase 易被忽略** | 中 | 作为最后阶段，agent 容易在 Closeout 后停止而跳过 Memory |
| 4 | **无 hook enforcement** | 中 | 与 planning-with-files 不同，recursive-mode 未见 lifecycle hook 定义 |
| 5 | **SubSkill 间协调缺失** | 低 | 7 个 subskill 各自独立，同时使用时可能产生 prompt 冲突 |
| 6 | **单线程假设** | 低 | 7-phase workflow 假设单 agent 顺序执行，不支持并行实现 |

---

## 10. 迁移评估

### 可迁移候选

| 机制 | 目标插件 | 可行性 | 备注 |
|------|----------|--------|------|
| 7-Phase State Machine | `workflows/deep-plan` | ★★★ | Phase 定义可对齐 deep-plan 的 mode switching |
| Memory Phase (知识提取) | `integrations/catchup` | ★★★ | 跨 session 记忆与 catchup 的 handoff 互补 |
| recursive-tdd SubSkill | `quality/testing` | ★★★ | TDD 工作流可直接增强 testing 插件 |
| recursive-debugging SubSkill | `quality/testing` | ★★☆ | 结构化调试与 testing 的 bug 定位互补 |
| recursive-worktree SubSkill | `vcs/git` | ★★★ | Worktree 管理 skill 高度可复用 |
| recursive-review-bundle | `quality/codex-review` | ★★☆ | Review bundle 生成可增强 code review 流程 |
| recursive-subagent | `integrations/async-agent` | ★★☆ | 子 agent 编排与 async-agent 功能互补 |

### 建议采纳顺序

1. **recursive-tdd** → 直接移植为 testing 插件的 TDD workflow skill
2. **Memory Phase pattern** → 提取 "knowledge extraction at end of task" 为通用 skill
3. **recursive-worktree** → 合并到 git 插件的 worktree 管理能力
4. **7-Phase State Machine** → 简化为 deep-plan 的可选 workflow template

---

## 11. 开放问题

1. **Hook 缺失原因**: 与 planning-with-files 相比，recursive-mode 为何没有 lifecycle hook？是设计选择还是技术限制？
2. **SubSkill 组合冲突**: 当多个 subskill 同时加载时，SKILL.md 之间的 prompt 优先级如何处理？
3. **Memory.md 的消费者**: `.workflow/memory.md` 由谁、在什么时候读取？是否有自动注入下一 session 的机制？
4. **Artifact 模板**: `.workflow/` 文件是否有标准化模板？还是完全由 agent 自由发挥？
5. **与 recursive-spec 的关系**: recursive-spec 的 spec 格式与 human-in-loop 的 .spec/ 目录有何异同？

---

## 附录：Gemini Deepdive 补充信息

> 来源：`1st-cc-plugin/workflows/loaf/docs/gemini-roadmap-review/deepdive-recursive-mode.md`
> 补充内容：TDD Compliance Log、LockHash 防篡改、Review Bundle 脚本和证据日志结构的实现细节。

### A.1 TDD Compliance Log 详细结构

TDD Compliance Log 不仅记录测试结果，还强制执行 TDD 纪律：

- **模式声明**：`TDD Mode: strict` 或 `TDD Mode: pragmatic`
  - `strict`：RED phase 中测试**必须**失败，若测试立即通过则违规
  - `pragmatic`：允许对已有功能跳过 RED phase，但需要记录 exception rationale
- **Evidence log 目录结构**：
  ```
  /.recursive/run/<run-id>/evidence/logs/
  ├── red/
  │   └── <test-file>.log    # RED phase 输出（测试失败证据）
  └── green/
      └── <test-file>.log    # GREEN phase 输出（测试通过证据）
  ```
- **RED Phase 强制**（strict 模式）：若新写的测试立即通过，agent 必须停止并报告——这意味着测试没有测到新行为

### A.2 `recursive-lock.py` LockHash 防篡改

`scripts/recursive-lock.py` 实现工件完整性验证：
- 对 `.recursive/run/<run-id>/` 下的所有 artifact 计算 SHA-256 content hash
- 生成 `LockHash`（所有 hash 的聚合摘要）
- 用途：检测 agent 是否在 review 后偷偷修改了已提交的工件
- 时间线：在 review bundle 生成前锁定，review 后再次验证

### A.3 Review Bundle 完整结构

`scripts/recursive-review-bundle.py` 生成结构化的 review 包：
- **Diff Basis**：`baseline` 和 `comparison` commit SHA，确保 reviewer 看到精确的变更范围
- **Changed Files**：过滤掉 transient 文件（`.log`、`.tmp`、lock 文件）
- **Upstream Artifacts**：从 `.recursive/run/` 拉取 spec、plan、evidence
- **Addenda**：附加上下文（设计决策记录、已知限制）
- **Prior Evidence**：前次 review 的结论（如有）
- **Audit Questions**：自动生成的审查焦点问题
- **Artifact Content Hash**：每个 artifact 的 SHA-256，供 reviewer 验证完整性

### A.4 Subagent Action Logger

`scripts/recursive-subagent-action.py` 记录 subagent 的操作日志：
- 追踪 subagent 何时被启动、执行了什么任务、输出了什么
- 日志存储在 `.recursive/run/<run-id>/subagent-actions.log`
- 为 review 提供 subagent 行为的审计轨迹
