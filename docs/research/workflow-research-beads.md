# Workflow Research: beads (steveyegge/beads)

**Date**: 2026-04-18
**Source**: `vendor/beads` (https://github.com/steveyegge/beads)
**Analyst mode**: Single
**Focus**: All

---

## 1. 框架概况

| 属性 | 值 |
|------|-----|
| **类型** | Agent 任务跟踪工具 — Dolt-powered 分布式图状 issue tracker |
| **总文件数** | 1546 |
| **Prompt 文件** | `claude-plugin/` 下 agents, commands, skills |
| **脚本/钩子** | `.githooks/`, `hooks` 包, git hook 集成 |
| **测试文件** | `tests/integration/`, `tests/regression/`, `*_test.go` |
| **入口** | `cmd/bd/main.go` (cobra CLI), `claude-plugin/.claude-plugin/` |
| **注册机制** | Go CLI 通过 cobra 子命令注册；Claude Code 通过 plugin.json 发现 |
| **语言** | Go (核心), Markdown (prompts), Bash (安装脚本) |

### 目录结构

```
beads/
├── cmd/bd/main.go              # CLI 入口 (cobra)
├── internal/
│   ├── beads/                   # 核心业务逻辑
│   ├── storage/dolt/            # Dolt 存储层
│   ├── hooks/                   # Git hook 集成
│   ├── compact/                 # 语义压缩
│   ├── molecules/               # 复合操作
│   ├── idgen/                   # Hash-based ID 生成
│   └── config/                  # 配置管理
├── claude-plugin/               # Claude Code 插件
│   ├── agents/*.md
│   ├── commands/*.md
│   └── skills/*/SKILL.md
├── tests/                       # 集成 + 回归测试
├── website/                     # Docusaurus 文档站
├── CLAUDE.md                    # Agent 工作指南
└── AGENTS.md → AGENT_INSTRUCTIONS.md
```

---

## 2. 源清单

### Overview Sources
| 文件 | 类型 | 价值 |
|------|------|------|
| `README.md` | 用户文档 | 安装、命令参考、存储模式、工作流 |
| `CLAUDE.md` | Agent 指南 | 项目概述、bd 命令用法、工作流规范 |
| `AGENT_INSTRUCTIONS.md` | 扩展 Agent 指南 | 开发规范、视觉设计系统、贡献者保护 |

### Execution Sources
| 文件 | 类型 | 价值 |
|------|------|------|
| `cmd/bd/main.go` | CLI 入口 | cobra 命令注册、信号处理、Dolt 连接 |
| `internal/beads/` | 核心逻辑 | Issue CRUD、依赖图、状态机 |
| `internal/storage/dolt/` | 存储层 | Dolt SQL 操作、嵌入/服务器模式 |
| `internal/compact/` | 压缩引擎 | 语义压缩旧任务保护上下文 |

### Enforcement Sources
| 文件 | 类型 | 价值 |
|------|------|------|
| `internal/hooks/` | Hook 运行器 | 可扩展的 hook 系统 |
| `.githooks/` | Git hooks | 预提交检查 |
| `cmd/bd/main.go` | 原子操作 | `--claim` 原子 claim、`readonlyMode` 保护 |

### Evolution Evidence
| 来源 | 类型 | 价值 |
|------|------|------|
| `tests/integration/` | 集成测试 | 端到端行为验证 |
| `tests/regression/` | 回归测试 | Bug 修复验证 |
| `website/versioned_docs/` | 版本文档 | 多版本演进 |

---

## 3. 对象模型

### 一等实体

| 实体 | 定义位置 | 必要字段 | 生命周期 | 分类 |
|------|---------|---------|---------|------|
| **Issue** | `internal/beads/` | id (hash), title, status, priority | create → in_progress → close | fact |
| **Dependency** | `internal/beads/` | child_id, parent_id, type | add → resolve | fact |
| **Epic** | 层级 ID 系统 | parent_id, child issues | create → 子任务全完成 → close | fact |
| **Message** | message 类型 issue | thread, lifecycle: ephemeral | create → read → expire | fact |
| **Molecule** | `internal/molecules/` | 复合操作集 | 组装 → 执行 → 完成 | evidence |

### 实体关系

```
Epic (1) ──parent-of──> Issue (N)     (层级 ID: bd-a3f8.1)
Issue (1) ──blocks──> Issue (N)       (依赖图)
Issue (1) ──relates-to──> Issue (N)   (图链接)
Issue (1) ──discovered-from──> Issue (N)
Message ──replies-to──> Message       (线程)
```

### 上下文隔离策略

| 范围 | 流向 | 机制 | 证据 |
|------|------|------|------|
| Agent → bd CLI | 命令 + JSON 输出 | `--json` flag，结构化输出 | `CLAUDE.md:18-25` |
| 跨分支 | Hash-based ID 无冲突 | Dolt cell-level merge | `README.md:37` |
| 长期记忆 → 上下文 | 语义压缩 | `internal/compact/` | `README.md:38` |
| 贡献者隔离 | 独立仓库 | `--contributor` mode → `~/.beads-planning` | `README.md:72-74` |

---

## 4. 流程与状态机

### Happy Path

1. `bd init` — 初始化 Dolt 数据库 — `cmd/bd/main.go`
2. `bd create "Title" -t feature -p 0` — 创建 issue — `CLAUDE.md:18`
3. `bd dep add <child> <parent>` — 建立依赖 — `CLAUDE.md:22`
4. `bd ready` — 找到无阻塞任务 — `CLAUDE.md:14`
5. `bd update <id> --claim` — 原子认领 — `CLAUDE.md:20`
6. Agent 实现任务
7. `bd close <id> --reason "Done"` — 关闭任务 — `CLAUDE.md:24`
8. `bd compact` — 压缩已关闭旧任务 — `internal/compact/`

### 阶段转换

| From | To | 触发 | Gate? | 证据 |
|------|----|------|-------|------|
| created | in_progress | `--claim` (原子) | Yes — file lock | `cmd/bd/main.go` |
| in_progress | closed | `bd close` | No | `CLAUDE.md:24` |
| any | deferred | `--defer=<date>` | No | `CLAUDE.md:31-32` |
| deferred | ready | defer_until 过期 | Yes — 时间 gate | `CLAUDE.md:35-37` |

### 失败路径

#### 失败路径 1：并发写冲突（嵌入模式）
嵌入模式单写者，file lock 保护。多 agent 并发需使用 server 模式。

#### 失败路径 2：依赖环
依赖图可能形成环，`bd dep tree` 可视化但未见环检测硬保障。

---

## 5. 执行保障审计

| # | 约束 | 来源 | 等级 | 证据 | 缺口? |
|---|------|------|------|------|-------|
| 1 | 原子 claim | `--claim` flag | Hard — file lock + atomic update | `cmd/bd/main.go` storeMutex | No |
| 2 | 只读模式 | `readonlyMode` flag | Hard — block writes | `cmd/bd/main.go` | No |
| 3 | Hash ID 无冲突 | `internal/idgen/` | Hard — 算法保证 | hash-based generation | No |
| 4 | 语义压缩 | `internal/compact/` | Hard — 自动执行 | compact 包 | No |
| 5 | 不使用 `bd edit` | `AGENTS.md:30-32` | Soft — agent 指令 | 仅文档警告 | Yes |
| 6 | Issue 类型规范 | `CLAUDE.md` | Soft — 指南 | 无 schema 强制 | Yes |

### 执行保障统计

| 等级 | 数量 | 百分比 |
|------|------|--------|
| Hard-enforced | 4 | 67% |
| Soft-enforced | 2 | 33% |
| Unenforced | 0 | 0% |

---

## 6. Prompt 目录

### Prompt: CLAUDE.md (Agent 工作指南)

| 字段 | 值 |
|------|-----|
| **repo_path** | `CLAUDE.md` |
| **quote_excerpt** | "We use bd (beads) for issue tracking instead of Markdown TODOs or external tools" |
| **stage** | 全流程 |
| **design_intent** | 强制 agent 使用 bd 而非临时方案跟踪工作 |
| **hidden_assumption** | 假设 bd CLI 已安装且 `bd init` 已执行 |
| **likely_failure_mode** | Agent 忽略 bd 指令，回退到 markdown TODO |
| **evidence_level** | direct |

---

## 7. 微观设计亮点

### Highlight: Dolt 作为 Agent 记忆后端

- **观察**: 使用版本控制数据库（Dolt）而非文件系统存储 issue 状态
- **证据**: `internal/storage/dolt/`, `README.md:89-110`
- **价值**: Cell-level merge、原生分支、SQL 查询能力、远程同步
- **权衡**: 需要安装 Dolt（200MB+），学习曲线陡峭
- **可迁移性**: Inspired — Dolt 后端过重，但 SQL-as-state 思路可借鉴

### Highlight: 语义压缩（Compaction）

- **观察**: 自动汇总已关闭旧任务，释放上下文窗口
- **证据**: `internal/compact/`, `README.md:38`
- **价值**: 解决长期任务跟踪的上下文膨胀问题
- **权衡**: 压缩后细节丢失，可能影响后续回溯
- **可迁移性**: Inspired — 压缩策略可适配到任何记忆系统

### Highlight: 层级 ID + Hash 无冲突

- **观察**: `bd-a3f8.1.1` 风格 ID 支持 epic → task → subtask 层级
- **证据**: `internal/idgen/`, `README.md:59-63`
- **价值**: 多 agent 多分支并发创建任务不冲突
- **权衡**: Hash ID 不可读，需要 `bd show` 查看详情
- **可迁移性**: Direct — ID 生成策略直接可用

---

## 8. 宏观设计亮点

### Philosophy: 数据库即真相源

- **观察**: 全部状态存储在 Dolt SQL 数据库中，非文件系统
- **出现位置**: `internal/storage/dolt/`, `README.md:89`
- **塑造方式**: SQL 查询替代文件遍历，事务保证一致性，分支隔离状态
- **优势**: ACID 保证、多 agent 安全、合并能力强
- **局限**: 依赖 Dolt 运行时，不可 `cat` 直接查看状态
- **采纳?**: Modify — SQL 思路好但 Dolt 太重，可用 SQLite 替代

---

## 9. 失败模式与局限

| # | 失败模式 | 触发 | 影响 | 证据 |
|---|---------|------|------|------|
| 1 | Dolt 安装门槛 | 首次使用 | 阻塞初始化 | `README.md` install 步骤 |
| 2 | 嵌入模式单写者 | 多 agent 并发 | 锁等待或超时 | `cmd/bd/main.go` lockTimeout |
| 3 | Agent 忽略 bd | Agent 不遵守 CLAUDE.md | 状态丢失 | Soft enforcement only |

---

## 10. 迁移评估

### 候选机制

| # | 机制 | 评级 | 工作量 | 前提 | 风险 | 来源 |
|---|------|------|--------|------|------|------|
| 1 | 依赖图任务跟踪 | Inspired | M | 图数据结构 | 环检测 | `internal/beads/` |
| 2 | 语义压缩 | Inspired | M | LLM 汇总 | 信息丢失 | `internal/compact/` |
| 3 | 原子 claim | Direct | S | 锁机制 | 已有 | `cmd/bd/main.go` |
| 4 | Hash ID 无冲突 | Direct | S | ID 生成器 | 无 | `internal/idgen/` |

### 推荐采纳顺序

1. **依赖图任务跟踪** — agent 长期任务管理的核心缺失
2. **语义压缩** — 解决上下文膨胀
3. **原子 claim** — 多 agent 安全

---

## 11. 开放问题

1. Dolt server 模式在多 agent 场景下的性能基准数据？
2. 语义压缩的质量评估 — 压缩后是否丢失关键决策上下文？
3. `bd sync` 的跨仓库同步在网络中断时的恢复机制？

---

## 附录：Gemini Deepdive 补充信息

> 来源：`1st-cc-plugin/workflows/loaf/docs/gemini-roadmap-review/deepdive-beads.md`
> 补充内容：依赖查询优化、cycle 检测算法、层级 ID 解析和 tree 渲染的实现级细节。

### A.1 Dependency 数据结构与 SQL 批量查询

Dependency struct（`internal/models/dependency.go`）的完整字段：
- `IssueID`, `DependsOnID`: 两个 Bead 引用
- `Type` 枚举：`blocks` | `parent-child` | `conditional-blocks` | `tracks` | `related`

批量查询优化（`internal/storage/issueops/dependency_queries.go`）：
- `GetBlockingInfoForIssuesInTx(tx, issueIDs)`：接受 ID 数组，单次 SQL 查询返回所有阻塞关系
- 构建三个内存 map：`blockedByMap`、`blocksMap`、`parentMap`
- 使用 `queryBatchSize` 常量分批 IN 查询，避免 SQLite 参数上限（默认 999）

### A.2 Cycle 检测算法

`DetectCycles` 函数（`internal/dependency/cycle.go`）实现 DFS cycle detection：
- 输入：依赖图的邻接表
- 维护 visited + recursion-stack 双 set
- 检测到 cycle 时返回完整路径（`[]IssueID`），供 CLI 展示给用户

### A.3 层级 ID 解析

`ParseHierarchicalID`（`internal/models/issue.go`）解析 `owner/repo#123` 格式：
- 支持短格式（`#123`，当前仓库隐含）和完整格式（`org/repo#456`）
- 返回 `HierarchicalIssueID{Owner, Repo, Number}`

### A.4 Tree 渲染器

`bd dep tree` 命令（`internal/cli/dep_tree.go`）使用 `treeRenderer` 状态结构体：
- 维护 indent 栈和"是否是最后子节点"标志
- 输出 Unicode box-drawing 字符（`├──`、`└──`、`│`）
- 递归渲染依赖子树，处理已访问节点避免无限循环
