# ralph (snarktank) 工作流逆向工程分析报告

> **仓库**: `vendor/ralph` (https://github.com/snarktank/ralph)
> **规模**: Small (~15 files), 113 行 Bash + 2 skills + 1 markdown prompt
> **框架类型**: 最小可行 Ralph-pattern 实现 — bash loop + PRD.json 任务合约
> **分析日期**: 2026-04-11

---

## 目录

1. [源清单](#1-源清单)
2. [框架假说](#2-框架假说)
3. [对象模型](#3-对象模型)
4. [流程与状态机](#4-流程与状态机)
5. [Prompt 目录](#5-prompt-目录)
6. [执行保障审计](#6-执行保障审计)
7. [失败模式](#7-失败模式)
8. [微观设计亮点](#8-微观设计亮点)
9. [宏观设计亮点](#9-宏观设计亮点)
10. [迁移候选评估](#10-迁移候选评估)
11. [交叉引用矩阵](#11-交叉引用矩阵)

---

## 1. 源清单

### 1.1 配置与清单

| 文件 | 角色 | 关键发现 |
|------|------|---------|
| `.claude-plugin/plugin.json` | Claude Code marketplace 清单 | name: `ralph-skills`, version: 1.0.0, skills: `./skills/` |
| `.claude-plugin/marketplace.json` | marketplace 元数据 | 无额外配置 |
| `prd.json.example` | PRD schema 示例 | `{project, branchName, description, userStories[{id,title,description,acceptanceCriteria[],priority,passes,notes}]}` |

### 1.2 核心脚本

| 文件 | 角色 | 关键发现 |
|------|------|---------|
| `ralph.sh` | 主循环驱动 (113 行) | bash `for` loop，fork 新进程，`|| true` 吞所有错误 |
| `CLAUDE.md` | Claude Code prompt 模板 (104 行) | 直接作为 stdin 传给 `claude` CLI |
| `prompt.md` | Amp prompt 模板 (108 行) | 通过 `cat` pipe 传给 `amp` |

### 1.3 Skills

| 文件 | 角色 |
|------|------|
| `skills/prd/SKILL.md` | PRD 生成 skill (242 行) — 通过对话生成 markdown PRD |
| `skills/ralph/SKILL.md` | PRD 转换 skill (259 行) — 将 markdown PRD 转为 prd.json |

### 1.4 支撑文件

| 文件 | 角色 |
|------|------|
| `AGENTS.md` | 框架行为说明 (48 行) |
| `README.md` | 用户文档 (240 行) |
| `flowchart/` | React 可视化 (仅前端展示，无逻辑) |

---

## 2. 框架假说

**类型**: 最小执行循环 (Minimal Execution Loop)

**核心主张**: 每个 AI iteration 拿到新鲜 context，读取 `prd.json` 中未完成的最高优先级 story，实现并通过质量检查后提交，更新 `prd.json` 标记完成，直到所有 story 通过。

**实际情况**: 框架在"新鲜 context"（hard-enforced，bash fork）和"任务列表"（prd.json 硬 schema）上确实兑现了承诺。质量检查和单 story 约束则仅靠 prompt 指令，无代码强制。

---

## 3. 对象模型

### 3.1 一等实体

#### Entity: PRD (`prd.json`)

- **定义位置**: `prd.json.example`
- **Schema**:
  ```json
  {
    "project": "string",
    "branchName": "ralph/kebab-case",
    "description": "string",
    "userStories": [
      {
        "id": "US-NNN",
        "title": "string",
        "description": "As a ... I want ... so that ...",
        "acceptanceCriteria": ["string"],
        "priority": 1,
        "passes": false,
        "notes": ""
      }
    ]
  }
  ```
- **生命周期**: 由 `/ralph` skill 创建 → 每次 iteration 更新 `passes` 字段 → 分支切换时整体存档到 `archive/`

#### Entity: User Story

- **定义位置**: `prd.json` 内嵌
- **生命周期**: `passes=false` → AI 选中 → 实现 → 质量检查 → `passes=true`
- **注意**: 无 `dependsOn` 字段，依赖关系隐含于 `priority` 排序

#### Entity: Progress Entry (`progress.txt`)

- **定义位置**: `prompt.md:18-31`, `CLAUDE.md:18-31`
- **Schema** (free-form markdown):
  ```
  ## [Date/Time] - [Story ID]
  Thread: https://ampcode.com/threads/$AMP_CURRENT_THREAD_ID
  - What was implemented
  - Files changed
  - **Learnings for future iterations:**
    - Patterns discovered
    - Gotchas encountered
  ---
  ```
- **生命周期**: append-only，永不替换；分支切换时重置（但旧文件存档）

#### Entity: Archive

- **定义位置**: `ralph.sh:39,49-58`
- **Schema**: `archive/YYYY-MM-DD-[branch-name]/` 包含 `prd.json` + `progress.txt` 快照
- **生命周期**: 分支切换时自动触发

### 3.2 实体关系图

```
prd.json ──── 包含 ──── userStories[] ──── priority sort ──── 选取 ──── AI iteration
    │                                                                        │
    └── branchName ──── .last-branch (分支追踪) ──── 切换触发 ──── archive/
    
progress.txt ──── AI 读取 (patterns section first) ──── AI 写入 (append)
git history  ──── AI 读取 (git log) ──── AI 写入 (feat: [ID] - [Title])
```

---

## 4. 流程与状态机

### 4.1 主循环状态机 (`ralph.sh`)

```
[START]
  ├─ 解析参数: --tool (amp|claude), max_iterations
  ├─ 验证 TOOL 合法性 (hard gate: exit 1 if invalid)
  │
  ├─ 分支变更检测 (ralph.sh:43-73)
  │   ├─ 读取 prd.json.branchName
  │   ├─ 读取 .last-branch
  │   └─ 不同? → 存档旧 prd.json+progress.txt → 重置 progress.txt
  │
  ├─ 初始化 progress.txt (若不存在)
  │
  └─ FOR i in 1..MAX_ITERATIONS:
       │
       ├─ 实例化 AI (ralph.sh:91-96)
       │   ├─ Amp:    cat prompt.md | amp --dangerously-allow-all || true
       │   └─ Claude: claude --dangerously-skip-permissions < CLAUDE.md || true
       │
       ├─ 检查完成信号 (ralph.sh:99-104)
       │   └─ grep "<promise>COMPLETE</promise>"
       │       ├─ 匹配 → exit 0 (SUCCESS)
       │       └─ 不匹配 → sleep 2 → 继续
       │
       └─ [到达 MAX_ITERATIONS] → exit 1 (FAILURE)
```

### 4.2 AI 迭代内部状态机 (`CLAUDE.md:1-16`)

```
[NEW AI INSTANCE — 无跨迭代记忆]
  │
  ├─ 读取 prd.json (理解全部 stories + 当前 passes 状态)
  ├─ 读取 progress.txt (Codebase Patterns section first)
  ├─ 检查/切换到 branchName
  │
  ├─ 选择最高 priority 且 passes=false 的 story
  │
  ├─ 实现该 story (PROMPT: "仅一个")
  │
  ├─ 运行质量检查 (typecheck/lint/test)
  │   └─ PASS? → commit "feat: [ID] - [Title]"
  │             → prd.json.passes = true
  │             → 追加 progress.txt
  │   └─ FAIL? → (prompt 说不提交，但无 hard gate)
  │
  ├─ 更新 AGENTS.md (若发现可复用 patterns)
  │
  └─ 全部 passes=true?
       ├─ YES → 输出 <promise>COMPLETE</promise>
       └─ NO  → 正常结束 (下一迭代接手)
```

**转换触发器**:

| 触发器 | 类型 | 来源 |
|--------|------|------|
| `<promise>COMPLETE</promise>` in OUTPUT | Hard | `ralph.sh:99` grep |
| MAX_ITERATIONS 耗尽 | Hard | `ralph.sh:84` for 循环边界 |
| branchName 变更 | Hard | `ralph.sh:47` 字符串比较 |
| 质量检查失败 | Soft | prompt 指示，无代码强制 |

---

## 5. Prompt 目录

### 5.1 主迭代 Prompt (`CLAUDE.md`)

| 字段 | 内容 |
|------|------|
| **role** | 自主编码 agent |
| **repo_path** | `CLAUDE.md` |
| **quote_excerpt** | `"4. Pick the highest priority user story where passes: false. 5. Implement that single user story."` |
| **stage** | 每次 ralph.sh 迭代 |
| **design_intent** | 强制单 story 粒度，防止 agent 同时处理多任务 |
| **hidden_assumption** | story 已被人工拆分到合适大小；质量检查命令存在且有效 |
| **likely_failure_mode** | agent 实现不完整后仍输出 COMPLETE；或质量检查无命令可运行 |

**关键指令摘录** (`CLAUDE.md:76-79`):
```
- ALL commits must pass your project's quality checks (typecheck, lint, test)
- Do NOT commit broken code
- Keep changes focused and minimal
- Follow existing code patterns
```

### 5.2 Learnings 格式 Prompt (`CLAUDE.md:18-31`)

```markdown
APPEND to progress.txt (never replace, always append):
## [Date/Time] - [Story ID]
- What was implemented
- Files changed
- **Learnings for future iterations:**
  - Patterns discovered
  - Gotchas encountered
---
```

**design_intent**: 构建跨迭代的增量知识库，靠 progress.txt 的 "Codebase Patterns" section 积累可复用信息。

**hidden_assumption**: AI 会如实、有用地填写 learnings；patterns 不会随时间退化为噪声。

### 5.3 PRD 生成 Skill (`skills/prd/SKILL.md`)

| 字段 | 内容 |
|------|------|
| **role** | 产品经理 + 技术架构师 |
| **stage** | ralph 运行前（规划阶段） |
| **design_intent** | 通过对话式澄清将模糊需求结构化为可执行的 user stories |
| **hidden_assumption** | 用户能描述清楚功能意图；stories 会被拆分到单 context window 可完成的粒度 |

### 5.4 PRD 转换 Skill (`skills/ralph/SKILL.md`)

| 字段 | 内容 |
|------|------|
| **role** | 格式转换器 |
| **stage** | markdown PRD → prd.json |
| **design_intent** | 将人类可读的 PRD 规范化为 ralph.sh 可消费的 JSON 任务合约 |
| **likely_failure_mode** | acceptanceCriteria 太模糊，AI 无法判断 passes=true 条件 |

---

## 6. 执行保障审计

### 6.1 Hard Enforcement (代码/脚本层面强制)

| 约束 | 位置 | 机制 |
|------|------|------|
| **新鲜 context** | `ralph.sh:92,95` | bash 每次 fork 新进程，无跨迭代进程内存 |
| **完成信号检测** | `ralph.sh:99` | `grep -q "<promise>COMPLETE</promise>"` 精确字符串匹配 |
| **迭代上限** | `ralph.sh:84,111-113` | `for i in $(seq 1 $MAX_ITERATIONS)` → `exit 1` |
| **工具参数验证** | `ralph.sh:32-34` | `if [[ "$TOOL" != "amp" && "$TOOL" != "claude" ]]` → `exit 1` |
| **分支切换存档** | `ralph.sh:47-58` | `CURRENT_BRANCH != LAST_BRANCH` → `mkdir + cp` |

### 6.2 Soft Enforcement (Prompt 层面/约定)

| 约束 | 位置 | 说明 |
|------|------|------|
| **单 story per iteration** | `CLAUDE.md:105` | `"Work on ONE story per iteration"` — 无代码阻止多 story |
| **质量检查必须通过** | `CLAUDE.md:76-79` | `"Do NOT commit broken code"` — 无 pre-commit hook |
| **prd.json 更新** | `CLAUDE.md:9` | 指示更新 passes=true，但 ralph.sh 只检查 COMPLETE 输出 |
| **最高优先级优先** | `CLAUDE.md:4` | 文本描述，无 JSON 排序强制 |
| **progress.txt 仅追加** | `CLAUDE.md:20` | `"never replace, always append"` — 无 append-only 锁 |

### 6.3 Unenforced (声明但无执行)

| 约束 | 位置 | 说明 |
|------|------|------|
| **浏览器验证** | `CLAUDE.md:85-92` | `"MUST verify it works in the browser"` for UI stories — 无自动触发 |
| **AGENTS.md 更新** | `CLAUDE.md:50-74` | 建议添加可复用 patterns — 无强制 |
| **Story 大小限制** | `README.md:170-179` | 仅建议拆分，无检查机制 |

**关键发现**: `ralph.sh:92,95` 的 `|| true` 吞掉 AI 进程的所有错误。测试失败、typecheck 报错、工具崩溃——bash 全部静默忽略，循环照常继续。这是框架最危险的设计决策。

---

## 7. 失败模式

### 7.1 质量检查静默绕过

**根本原因**: `ralph.sh:92,95` — `|| true` 捕获所有退出码

**场景**: AI 运行了质量检查，命令返回非零退出码（测试失败），但 bash 将 `OUTPUT` 设为包含错误信息的字符串，循环继续。

**后果**: 坏代码进入分支 → 后续 iteration 继承破损基础 → 复合错误 → CI 最终失败但时机已晚。

**证据**: `ralph.sh:92`
```bash
OUTPUT=$(cat "$SCRIPT_DIR/prompt.md" | amp --dangerously-allow-all 2>&1 | tee /dev/stderr) || true
```

### 7.2 Story 过大导致隐性截断

**根本原因**: 无 token 计数或 story 大小检查机制

**场景**: PRD 中有 "Add authentication" 类型的大 story → AI 在 context 窗口末尾实现不完整 → 仍输出 `passes=true` → 下一 iteration 不会再处理该 story。

**后果**: 部分实现被标记为完成，且无法回溯（passes=true 的 story 不再被选中）。

**证据**: `README.md:170-179` 仅有口头建议，`ralph.sh` 无检查。

### 7.3 完成信号误触发

**根本原因**: `ralph.sh:99` — 简单 `grep -q` 字符串匹配

**场景**: AI 的错误消息、注释或调试输出中包含 `<promise>COMPLETE</promise>` 字符串 → 循环在任务未完成时退出。

**证据**: `ralph.sh:99`
```bash
if echo "$OUTPUT" | grep -q "<promise>COMPLETE</promise>"; then
    exit 0
fi
```

无校验 prd.json 是否真正全部 passes=true。

### 7.4 progress.txt 无限增长导致 context 膨胀

**根本原因**: append-only 设计 + 无清理机制

**场景**: 长期运行项目 → progress.txt 数万行 → AI prompt context 大量占用 → 有效 context 窗口缩小 → 后期 iteration 质量下降。

**证据**: `CLAUDE.md:20` `"APPEND to progress.txt (never replace)"` — 无轮转、截断、总结机制。

### 7.5 分支检测失败导致数据丢失

**根本原因**: `ralph.sh:47` 依赖 `jq` 和 `branchName` 字段正确

**场景**: prd.json 格式错误 → `jq` 失败 → `CURRENT_BRANCH=""` → `[ -z "$CURRENT_BRANCH" ]` 跳过存档检测 → 旧 progress.txt 被 `>` 覆盖 (`ralph.sh:61`)。

**证据**: `ralph.sh:44`
```bash
CURRENT_BRANCH=$(jq -r '.branchName // empty' "$PRD_FILE" 2>/dev/null || echo "")
```
`// empty` 和 `|| echo ""` 静默处理错误而非报警。

---

## 8. 微观设计亮点

### 8.1 bash fork 作为 context 隔离机制

每次 iteration 是独立的 OS 进程，没有任何内存泄漏或状态污染的可能。相比于在同一进程内"清除"上下文，这是最可靠的 fresh context 实现。

**观察**: `ralph.sh:92` `cat prompt.md | amp` — 每次都是新的 CLI 调用。
**证据**: `ralph.sh:92,95`
**为何重要**: 确保了 Ralph 模式的核心不变量，代价只是进程启动开销。
**可迁移性**: Direct — 任何 bash/shell 脚本都可复用。

### 8.2 prd.json 作为状态机合约

`passes` 字段将任务列表变成了一个可持久化的状态机快照。任何时候中断，都可以从 prd.json 恢复确切进度。

**观察**: `prd.json.example` — `"passes": false` 是任务的初始态。
**为何重要**: 不依赖 AI 的记忆或上下文来维持进度状态。
**可迁移性**: Direct — JSON 状态文件模式。

### 8.3 Codebase Patterns 作为跨迭代知识传递

`progress.txt` 顶部的 `## Codebase Patterns` section 是一个显式的知识摘要层，AI 被指示"先读这部分"。

**观察**: `CLAUDE.md:2` `"check Codebase Patterns section first"`。
**为何重要**: 与直接读取完整 progress.txt 相比，优先读摘要防止了有效信息被近期条目淹没。
**可迁移性**: Direct — 任何 append-only 日志系统都可加类似 summary section。

---

## 9. 宏观设计亮点

### 9.1 Zero-Framework 哲学

框架的全部逻辑是 113 行 bash，无任何外部依赖（除 `jq`）。这意味着：调试路径完全透明，没有框架版本锁定问题，可以复制到任何项目的 `scripts/` 目录直接使用。

**设计取舍**: 选择了可理解性和可移植性，放弃了复杂功能（并行、多 backend 路由、异常诊断）。

### 9.2 Disk-as-Memory 原则

所有跨迭代状态都在磁盘上：`prd.json`（任务状态）、`progress.txt`（学习积累）、`git history`（实现记录）。AI 进程是无状态的，磁盘是系统状态。

**设计取舍**: 极简化了编排逻辑（bash 不需要管状态），但依赖 AI 诚实地更新磁盘文件（soft-enforced）。

### 9.3 PRD-as-Contract 模式

`prd.json` 既是任务清单又是验收标准（`acceptanceCriteria[]`）。这将"做什么"和"怎么验证"绑定在同一个可机读的数据结构里，使 AI 自主实现成为可能。

---

## 10. 迁移候选评估

### 10.1 候选列表

| 机制 | 可迁移性 | 工作量 | 前置条件 | 风险 |
|------|---------|--------|---------|------|
| bash fork 作 context 隔离 | Direct | S | 无 | 低 |
| prd.json passes 状态机 | Direct | S | 无 | 低 |
| Codebase Patterns section | Direct | S | append-only log 存在 | 低 |
| `<promise>COMPLETE</promise>` 完成协议 | Direct | S | 无 | 中（误触发） |
| 分支切换自动存档 | Direct | S | git repo | 低 |

### 10.2 建议采纳顺序

1. **prd.json passes 状态机** — 最核心模式，其他所有机制围绕它构建
2. **bash fork context 隔离** — Ralph 模式不变量，简单可靠
3. **Codebase Patterns section** — 低成本高收益的知识积累机制
4. **分支切换存档** — 防意外数据覆盖

### 10.3 必须修复再迁移

- 移除 `|| true`，改为捕获退出码并停止 loop
- 在 COMPLETE 退出前校验 prd.json 全部 passes=true

---

## 11. 交叉引用矩阵

### 11.1 实体 → 生命周期阶段

| 实体 | 创建 | 更新 | 读取 | 清除 |
|------|------|------|------|------|
| prd.json | `/ralph` skill | AI iteration (passes=true) | AI iteration 开始 | 分支切换时存档 |
| progress.txt | `ralph.sh:76` | AI iteration 结束 (append) | AI iteration 开始 | 分支切换时重置 |
| git commits | AI iteration 提交 | 永不 | AI iteration (git log) | 永不 |
| archive/ | `ralph.sh:55-58` | 永不 | 手动 | 手动 |

### 11.2 Hard vs Soft Enforcement 比率

| 层面 | Hard | Soft | Unenforced |
|------|------|------|------------|
| 循环控制 | 3 (fork/grep/limit) | 0 | 0 |
| 质量保证 | 0 | 4 | 3 |
| 状态一致性 | 1 (存档) | 2 | 1 |
| **总计** | **4** | **6** | **4** |

**结论**: Hard enforcement 集中在循环控制层，质量保证层几乎全是 soft — 这是框架最大的 reliability gap。

### 11.3 关键路径风险热图

```
HIGH RISK:  质量检查绕过 (|| true)  ← 框架级缺陷
HIGH RISK:  Story 大小无约束         ← 用户责任
MED RISK:   COMPLETE 信号误触发      ← 边缘场景
LOW RISK:   progress.txt 膨胀        ← 渐进降级
LOW RISK:   分支检测失败             ← 边缘场景
```
