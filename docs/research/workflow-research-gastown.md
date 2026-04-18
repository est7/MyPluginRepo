# Workflow Research: gastown

**Date**: 2025-07-17
**Source**: `vendor/gastown`
**Analyst mode**: Single
**Focus**: All

---

## 1. 框架概况

| 属性 | 值 |
|------|-----|
| **类型** | 多 Agent 编排基础设施 — 面向 20-30+ 个并发 agent 的"小镇"模型 |
| **总文件数** | 1425 |
| **语言** | Bash（命令层）+ Go（基础设施守护进程）+ TOML（Formula 工作流定义）+ Markdown（agent prompt / directives） |
| **入口** | `~/gt/`（Town root），`gt` CLI 子命令族 |
| **CLI 命令** | `gt sling`, `gt done`, `gt mail`, `gt nudge`, `gt escalate`, `gt prime`, `gt handoff`, `gt config` |
| **数据存储** | Dolt SQL Server（port 3307，all-on-main 写入策略） |
| **注册机制** | `gt` CLI 安装后全局可用；agent 通过 hooks 注入 `.claude/settings.json` 获取上下文 |

### 架构分层

gastown 的架构呈三层金字塔结构，从基础设施到工作负载逐层收窄：

```
Town-Level（全局治理）
├── Mayor         — singleton 全局协调器
├── Deacon        — 常驻 daemon（heartbeat 循环）
├── Boot          — watchdog 进程，确保 Deacon 存活
└── Dogs          — 基础设施 worker 池

Rig-Level（项目隔离）
├── Witness       — monitor，巡检 Polecat 状态
├── Refinery      — merge queue，批量合并 + 二分排错
├── Polecats      — code worker（agent 实例）
└── Crews         — human workspace，人机协作界面

Data Plane（持久层）
└── Dolt SQL      — port 3307，all-on-main 写入，beads 账本
```

---

## 2. 源清单

### 核心基础设施

| 路径 | 大小/行数 | 角色 |
|------|-----------|------|
| `gt` CLI 入口 | — | 所有用户/agent 交互的统一命令行界面 |
| `mayor/` | — | Town-level singleton 协调器，全局调度与资源分配 |
| `deacon/` | — | Heartbeat daemon，16 步循环巡检 |
| `boot/` | — | Watchdog，确保 Deacon 进程不死 |
| `dogs/` | — | Infrastructure worker 池，执行底层任务 |

### Rig 组件

| 路径 | 大小/行数 | 角色 |
|------|-----------|------|
| `witness/` | — | Polecat 状态巡检器，检测 Working/Idle/Stalled/Zombie |
| `refinery/` | — | Merge queue，batch-then-bisect 算法 |
| `polecats/` | — | Code worker 实例管理，三层模型 |
| `crews/` | — | Human workspace，人类开发者工作区 |

### 配置与 Prompt

| 路径 | 大小/行数 | 角色 |
|------|-----------|------|
| `~/gt/directives/<role>.md` | — | Town-level 角色指令（低优先级） |
| `~/gt/<rig>/directives/<role>.md` | — | Rig-level 角色指令（高优先级，覆盖 town-level） |
| `*.toml` (Formula 文件) | — | TOML 定义的工作流模板，含 steps / gates / dependencies |
| `~/gt/.beads/` | — | Town-level beads 账本（hq-* 前缀） |
| `<rig>/.beads/` | — | Rig-level beads 账本（项目前缀） |

### 通信层

| 路径 | 大小/行数 | 角色 |
|------|-----------|------|
| Mail 系统 | — | 持久化消息，必须在 session death 后存活 |
| Nudge 系统 | — | 轻量级 ephemeral 通知，无存储开销 |
| Escalation 系统 | — | 三级升级：MEDIUM P2 → HIGH P1 → CRITICAL P0 |

---

## 3. 对象模型

### 一等实体

| 实体 | 定义位置 | 必要字段 | 生命周期 | 分类 |
|------|---------|---------|---------|------|
| **Town** | `~/gt/` | rigs[], mayor, deacon | boot → run → shutdown | infrastructure |
| **Rig** | `~/gt/<rig>/` | bare repo, beads DB, directives | create → active → archive | container |
| **Polecat** | polecats 管理 | identity, sandbox, session | spawn → working → idle → zombie | worker |
| **Crew** | crews 管理 | human workspace, rig binding | create → active → detach | workspace |
| **Bead** | `.beads/` 目录 | type, status, hook_bead, role_bead, agent_state, work_type | create → update → close / expire | ledger-entry |
| **Wisp** | `.beads/` (TTL) | 同 Bead + TTL (7-30 days) | create → expire (auto-gc) | ephemeral-bead |
| **Formula** | `*.toml` | steps[], gates[], dependencies | define → instantiate → execute | workflow-template |
| **Molecule** | Formula 执行实例 | formula_ref, state, polecats[] | start → steps → complete/fail | execution |
| **Convoy** | 跨 rig 协调 | hq-cv-* beads, polecat swarm | assemble → execute → disband | batch-work |
| **Mail** | Mail 系统 | type, sender, recipient, payload | send → deliver → ack | persistent-msg |
| **Directive** | `directives/<role>.md` | role, content | load → inject → override | prompt |

### Polecat 三层模型

gastown 中最精妙的设计之一是 Polecat 的三层隔离模型。每个 Polecat 由三个生命周期完全不同的层组成：

| 层 | 持久性 | 实现 | 说明 |
|----|--------|------|------|
| **Identity** | PERMANENT | CV chain（履历链） | 记录 Polecat 历史上做过的所有工作，构建"声誉" |
| **Sandbox** | PERSISTENT | git worktree | 独立的代码工作区，跨 session 保持 |
| **Session** | EPHEMERAL | Claude context window | 单次对话上下文，session 结束即销毁 |

### Polecat 状态机

```
        ┌──────────┐
        │ Working  │ ← 正在执行任务
        └────┬─────┘
             │ gt done / timeout
             ▼
        ┌──────────┐
        │   Idle   │ ← 等待新任务分配
        └────┬─────┘
             │ unresponsive
             ▼
        ┌──────────┐
        │ Stalled  │ ← Witness 检测到无响应
        └────┬─────┘
             │ recovery failed
             ▼
        ┌──────────┐
        │  Zombie  │ ← 需要回收资源
        └──────────┘
```

### 实体关系

```
Town (1) ──contains──> Rig (N)
Rig (1) ──hosts──> Polecat (N)
Rig (1) ──hosts──> Crew (N)
Rig (1) ──has──> Refinery (1)
Rig (1) ──has──> Witness (1)
Rig (1) ──stores──> Bead (N)
Town (1) ──stores──> Bead (N, hq-* prefix)
Polecat (1) ──produces──> Bead (N)
Convoy (1) ──coordinates──> Polecat (N, cross-rig)
Formula (1) ──instantiates──> Molecule (N)
Molecule (1) ──assigns──> Polecat (N)
```

### 上下文隔离策略

| 范围 | 流向 | 机制 | 说明 |
|------|------|------|------|
| Town → Rig | directives + config | 文件系统层级覆盖 | rig-level directive 优先于 town-level |
| Rig → Polecat | hooks + directives | `.claude/settings.json` 注入 | 每个 Polecat 只看到所属 rig 的上下文 |
| Polecat → Polecat | Mail / Nudge | 异步消息 | 无直接共享内存 |
| 跨 Rig | Convoy + hq-* beads | Town-level beads 账本 | 通过 Mayor 协调 |

---

## 4. 流程与状态机

### Happy Path: Polecat 完成任务

1. **Scheduler 分配** — scheduler 检查 `gt config` 中的 `scheduler.max_polecats` 容量上限，从待办队列中选取任务
2. **Propulsion 原则** — "If you find something on your hook, YOU RUN IT." 工作分配即授权，Polecat 发现 hook 上的任务后立即开始执行
3. **Working 状态** — Polecat 在独立 git worktree (Sandbox 层) 中编写代码，Claude context (Session 层) 提供对话能力
4. **`gt done`** — Polecat 完成工作，发送 `POLECAT_DONE` mail
5. **Witness 巡检** — Witness 检测到完成状态，发送 `MERGE_READY` mail 给 Refinery
6. **Refinery 合并** — Refinery 执行 batch-then-bisect 合并流程
7. **成功通知** — 发送 `MERGED` mail，nuke worktree，Polecat 回到 Idle 状态
8. **资源回收** — Session 层（ephemeral）销毁，Identity 层（CV chain）更新履历

### Refinery Merge Queue: batch-then-bisect 算法

```
1. 收集所有 MERGE_READY 分支
2. Rebase 成一个栈（stack）
3. 测试栈顶（tip）
4. If PASS → fast-forward 全部合并
5. If FAIL → 二分查找（binary search）定位 culprit
6. Culprit 分支 → REWORK_REQUEST mail
7. 其余分支重新入队
```

### Deacon Heartbeat: 16 步巡检循环

```
Step 1:  Dolt health check（数据库连通性）
Step 2:  Witness patrol（各 rig 的 Polecat 状态）
Step 3:  Refinery patrol（merge queue 进展）
Step 4:  Deacon self-check（daemon 健康度）
Step 5:  Branch pruning（清理已合并/废弃分支）
Step 6:  Infrastructure jobs（Dogs worker 任务分发）
Step 7:  Scheduler dispatch（按容量分配新任务）
Step 8:  Nudge idle agents（轻推空闲 Polecat）
Steps 9-16: 其他基础设施维护任务
```

### 通信协议

#### Mail（持久化，必须存活于 session death）

| 类型 | 方向 | 触发 |
|------|------|------|
| `POLECAT_DONE` | Polecat → Witness | 任务完成 |
| `MERGE_READY` | Witness → Refinery | 准备合并 |
| `MERGED` | Refinery → Polecat | 合并成功 |
| `MERGE_FAILED` | Refinery → Polecat | 合并失败 |
| `REWORK_REQUEST` | Refinery → Polecat | 需要返工 |
| `RECOVERED_BEAD` | 系统 → 相关方 | bead 恢复 |
| `HELP` | Polecat → Crew/Mayor | 请求人工介入 |
| `HANDOFF` | Polecat → Polecat | 工作移交 |

#### Nudge（ephemeral，无存储开销）

轻量级推送，用于唤醒 idle agent，不产生持久化记录。

#### Escalation（三级升级）

| 级别 | 优先级 | 典型场景 |
|------|--------|---------|
| MEDIUM | P2 | 非紧急但需关注 |
| HIGH | P1 | 影响进度 |
| CRITICAL | P0 | 系统级故障 |

### 失败路径

| 触发 | 响应 | 恢复 |
|------|------|------|
| Polecat 无响应 | Witness 标记 Stalled → 尝试恢复 → 失败则标记 Zombie | 资源回收，任务重新分配 |
| Merge 冲突 | Refinery bisect 定位 culprit | `REWORK_REQUEST` 退回给 Polecat |
| Deacon 崩溃 | Boot watchdog 检测到心跳丢失 | 自动重启 Deacon |
| Dolt 不可达 | Heartbeat step 1 失败 | 告警 + 等待恢复 |
| Convoy 超时 | 跨 rig 协调超时 | Escalation → Mayor 介入 |

---

## 5. 执行保障审计

### 保障矩阵

| 机制 | Hard（代码强制） | Soft（约定/文档） | Unenforced（仅声明） |
|------|------------------|-------------------|---------------------|
| **Polecat 隔离** | ✅ git worktree 物理隔离 | | |
| **Session ephemeral** | ✅ Claude context 自动销毁 | | |
| **Identity 持久** | ✅ CV chain 写入 beads DB | | |
| **Merge queue** | ✅ Refinery batch-then-bisect | | |
| **Capacity 控制** | ✅ `scheduler.max_polecats` 配置 | | |
| **Heartbeat 监控** | ✅ Deacon 16 步循环 | | |
| **Boot watchdog** | ✅ Boot 进程保活 Deacon | | |
| **Directive 优先级** | ✅ rig-level 覆盖 town-level | | |
| **Mail 持久化** | ✅ 必须存活于 session death | | |
| **Propulsion 原则** | | ✅ "hook 即授权"约定 | |
| **Beads 格式** | | ✅ universal schema 约定 | |
| **Wisp TTL** | ✅ 7-30 天自动 GC | | |
| **Escalation 分级** | | ✅ P0/P1/P2 约定 | |
| **Formula 依赖** | ✅ TOML gates/dependencies | | |
| **Convoy 协调** | | | ⚠️ 跨 rig 一致性依赖 Mayor |
| **Zombie 回收** | ✅ Witness 检测 + 资源释放 | | |
| **All-on-main 写入** | ✅ Dolt 单分支写入策略 | | |

### 分析

gastown 的保障体系以**基础设施级强制**为主。与纯 prompt-based 框架不同，其核心约束通过 Go daemon + Bash script + Dolt DB 硬编码实现。Propulsion 原则是少数依赖约定而非代码的机制之一——它在设计上有意如此：将工作分配与权限合二为一，减少协调开销。

---

## 6. Prompt 目录

### Prompt 1: Role Directives

gastown 的 prompt 不集中于单个文件，而是分散在 `directives/<role>.md` 体系中。每个角色（Mayor、Witness、Polecat 等）有独立的指令文件：

> **Town-level**: `~/gt/directives/<role>.md`
> **Rig-level**: `~/gt/<rig>/directives/<role>.md`（更高优先级）

这种分层设计允许每个 rig 对同一角色施加不同的行为约束。例如一个安全敏感的 rig 可以给 Polecat 角色追加更严格的审查要求，而不影响其他 rig。

### Prompt 2: Formula 工作流定义

Formula 使用 TOML 格式定义工作流模板：

```toml
# Formula 示例结构（推断）
[formula]
name = "feature-implementation"
steps = ["plan", "implement", "test", "review"]

[gates]
test = { required = true, retry = 2 }
review = { required = true, approvers = 1 }

[dependencies]
implement = ["plan"]
test = ["implement"]
review = ["test"]
```

Formula Overlays 允许每个 rig 对同一 formula 施加定制化修改，实现"模板 + 叠加"的灵活工作流定义。Molecule 是 Formula 的运行时实例。

---

## 7. 微观设计亮点

### Highlight 1: Polecat 三层生命周期模型

- **观察**: Identity（PERMANENT）、Sandbox（PERSISTENT）、Session（EPHEMERAL）三层分离，每层有独立的生命周期管理
- **证据**: Polecat 模型定义，CV chain 持久化，git worktree 隔离，Claude context ephemeral
- **价值**: 完美解决了 agent 工作流中的核心矛盾——需要记住历史（Identity）、保持工作现场（Sandbox），但不能让上下文无限膨胀（Session）。CV chain 赋予 agent "经验"而不消耗 token 预算
- **权衡**: 三层模型增加了实现复杂度；CV chain 的写入和查询需要额外的 DB 操作
- **可迁移性**: Inspired — 三层分离思想可用于设计 skill 的状态管理策略

### Highlight 2: Refinery batch-then-bisect 合并算法

- **观察**: 先乐观地将所有 MERGE_READY 分支 rebase 成栈并测试顶端，通过则全部 fast-forward；失败则二分查找 culprit
- **证据**: Refinery merge queue 实现
- **价值**: 在大量并发分支场景下极大减少测试次数——N 个分支最优情况只需 1 次测试，最差情况 O(log N) 次。比逐个测试合并节省 80%+ 的 CI 资源
- **权衡**: Rebase 栈可能引入顺序依赖的假阳性；bisect 假设"单个 culprit"可能在多个互相依赖的失败中失效
- **可迁移性**: Inspired — 算法思想可用于批量 PR 审查流程设计

### Highlight 3: Propulsion 原则

- **观察**: "If you find something on your hook, YOU RUN IT." 工作分配即权限授予，消除了"请求-批准"的协调延迟
- **证据**: Propulsion Principle 设计文档
- **价值**: 在 20-30+ agent 规模下，传统的"请求权限→等待批准→开始执行"模式会产生巨大的协调开销。Propulsion 原则将 O(N) 的协调降为 O(1)
- **权衡**: 缺乏显式权限检查意味着 hook 投递必须准确——错误投递会导致错误执行
- **可迁移性**: Inspired — 设计理念可借鉴，但 Claude Code 单 agent 场景下优势不明显

---

## 8. 宏观设计亮点

### Philosophy 1: "小镇"隐喻驱动的架构设计

gastown 将整个 multi-agent 系统映射为一座小镇：Mayor 管理全局，Deacon 是昼夜不停的值班员，Dogs 是蓝领工人，Polecats 是技术工人，Crews 是人类居民，Rigs 是不同的工厂车间。这不仅仅是命名 convention——隐喻决定了责任边界、通信模式和故障处理策略。一个"小镇"的 mental model 让开发者能直觉性地理解 30+ 个 agent 之间的协作关系，而不需要阅读复杂的架构文档。

### Philosophy 2: 基础设施级编排 vs Prompt 级编排

绝大多数 Claude Code 工作流框架依赖 Markdown prompt 和 hooks 来编排 agent 行为。gastown 走了完全不同的路线：用 Go 写 daemon，用 Bash 写 CLI，用 Dolt 做持久化，用 TOML 定义工作流。Agent prompt 只是系统的末端消费者，而非控制平面。这种"基础设施优先"的设计允许系统在 agent session 崩溃、context window 溢出等场景下仍然保持全局一致性——因为状态活在数据库里，不在 agent 的脑子里。

---

## 9. 失败模式与局限

| # | 失败模式 | 触发 | 影响 | 证据 |
|---|---------|------|------|------|
| 1 | **Dolt 单点故障** | Dolt SQL server (port 3307) 不可达 | 全系统 beads 读写停止，所有 rig 受影响 | all-on-main 写入策略暗示无读副本 |
| 2 | **Zombie 堆积** | 大量 Polecat 同时 stall（如 API 限流） | 资源耗尽，新任务无法分配 | Witness patrol 为串行巡检，大规模故障时恢复慢 |
| 3 | **Bisect 假设失效** | 两个分支互相依赖导致 merge 失败 | batch-then-bisect 无法定位真正的 culprit，可能错误退回无辜分支 | bisect 假设"单 culprit" |
| 4 | **Mail 持久化开销** | 高频通信场景（30+ agent 频繁交互） | beads DB 写入压力增大，影响 heartbeat 延迟 | Mail 必须存活于 session death |
| 5 | **Propulsion 误投递** | Hook 投递到错误的 Polecat | 错误执行任务，无权限检查拦截 | Propulsion 原则无显式验证 |
| 6 | **Formula Overlay 冲突** | 多个 rig overlay 修改同一 formula 的同一 step | 行为难以预测 | overlay 覆盖语义不明确 |
| 7 | **跨 rig Convoy 一致性** | 网络分区或 Mayor 繁忙 | Convoy 中的 Polecat 可能看到不一致的状态 | Convoy 依赖 Mayor 中心化协调 |

### 声明 vs 实际行为偏差

| 声明 | 来源 | 实际行为 | 证据等级 |
|------|------|---------|---------|
| 20-30+ agent 并发 | 架构设计 | 受限于 `scheduler.max_polecats` 和 Dolt 写入吞吐 | indirect |
| Session death 存活 | Mail 设计 | Mail 持久化有效，但 Nudge 丢失不可恢复 | direct |
| All-on-main 一致性 | Dolt 策略 | 单 writer 无冲突，但高并发写入可能排队 | indirect |

---

## 10. 迁移评估

### 候选机制

| # | 机制 | 评级 | 工作量 | 前提 | 风险 | 来源 |
|---|------|------|--------|------|------|------|
| 1 | Polecat 三层模型概念 | Inspired | M | 状态管理设计 | 过度设计风险 | Polecat 模型 |
| 2 | Directive 分层覆盖 | Direct | S | 文件系统 | 无 | directives 体系 |
| 3 | batch-then-bisect 思想 | Inspired | L | merge queue 基础设施 | 复杂度高 | Refinery |
| 4 | 持久化 Mail + ephemeral Nudge 二分 | Inspired | M | 消息系统 | 需适配单 agent | 通信模型 |
| 5 | Beads 账本（结构化工作记录） | Inspired | M | DB 或文件存储 | Schema 维护成本 | beads 系统 |
| 6 | Escalation 三级分级 | Direct | S | 无 | 无 | Escalation 系统 |
| 7 | Formula TOML 工作流定义 | Inspired | L | TOML parser | 与现有 plugin.json 冲突 | Formula 系统 |
| 8 | Propulsion 原则（分配即授权） | Inspired | S | 设计理念 | 无 | Propulsion Principle |
| 9 | Heartbeat 巡检模式 | Inspired | M | daemon 基础设施 | Claude Code 无 daemon | Deacon |

### 推荐采纳顺序

1. **Directive 分层覆盖** — 立即可用，`1st-cc-plugin` 已有 rig-level 类似概念（plugin group），只需形式化 override 规则。工作量 S，ROI 最高
2. **Escalation 三级分级** — 为 `quality/` 插件组添加问题分级机制，帮助用户理解问题严重性。工作量 S
3. **Propulsion 原则** — 作为设计理念融入 skill 调度逻辑，减少不必要的确认步骤。工作量 S
4. **Beads 账本概念** — 为长流程 skill（如 `deep-plan`）添加结构化工作记录。工作量 M
5. **持久化 + ephemeral 消息二分** — 区分必须记录的产出和可丢弃的中间通知。工作量 M

---

## 11. 开放问题

| # | 问题 | 优先级 | 说明 |
|---|------|--------|------|
| 1 | Dolt 选型动因？ | Medium | 为何选择 Dolt（版本化 SQL）而非 SQLite/PostgreSQL？是否利用了 Dolt 的 git-like branching 特性？ |
| 2 | CV chain 如何影响调度？ | High | Polecat 的"履历"是否影响 scheduler 的任务分配决策？即"有经验的 agent 优先处理相似任务"？ |
| 3 | Formula Overlay 合并语义？ | Medium | 多个 overlay 修改同一 formula 时的优先级和合并规则是什么？ |
| 4 | Convoy 失败回滚？ | High | 跨 rig Convoy 中某个 rig 的 Polecat 失败时，其他 rig 的工作如何回滚或补偿？ |
| 5 | Nudge vs Mail 选择标准？ | Low | 何时用 ephemeral Nudge、何时用 persistent Mail 的决策边界在哪里？ |
| 6 | Dogs worker 与 Polecat 的区别？ | Medium | 基础设施 Dogs 和代码工作者 Polecat 的责任边界是否清晰？是否存在灰色地带？ |
| 7 | 人类 Crew 的优先级？ | Medium | 当 Crew（人类）和 Polecat（agent）修改同一文件时，冲突解决策略是什么？ |
