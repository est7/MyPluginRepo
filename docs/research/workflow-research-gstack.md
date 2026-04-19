# Workflow Research: gstack (Garry Tan)

**Date**: 2025-07-17
**Source**: `vendor/gstack`
**Analyst mode**: Single
**Focus**: All

---

## 1. 框架概况

| 属性 | 值 |
|------|-----|
| **类型** | 专家 Specialist 集合 + 基础设施工具链 — CEO 视角的全栈开发工作流 |
| **总文件数** | 755 |
| **语言** | TypeScript / Bun 运行时 + Playwright（headless browser） |
| **作者** | Garry Tan（Y Combinator CEO） |
| **入口** | `SKILL.md.tmpl`（auto-generated 根模板）→ 各 skill 目录 → `bin/`（36+ CLI 工具） |
| **Specialist 数量** | 23 个 slash command specialists |
| **Power Tool 数量** | 8 个 slash command power tools |
| **注册机制** | `SKILL.md.tmpl` + `gen-skill-docs.ts` → 生成 `SKILL.md`；模板占位符系统 |
| **测试框架** | 三层测试 + diff-based 选择性执行 |

### 目录结构概览

```
gstack/
├── SKILL.md.tmpl              # 根模板，占位符驱动
├── gen-skill-docs.ts          # 模板 → SKILL.md 生成器
├── bin/                       # 36+ CLI 工具
├── skills/                    # 23 specialists + 8 power tools
│   ├── office-hours/
│   ├── plan-ceo-review/
│   ├── plan-eng-review/
│   ├── plan-design-review/
│   ├── plan-devex-review/
│   ├── plan-tune/
│   ├── autoplan/
│   ├── review/
│   ├── qa/ & qa-only/
│   ├── design-*/              # consultation, shotgun, review, html
│   ├── ship/
│   ├── land-and-deploy/
│   ├── setup-deploy/
│   ├── document-release/
│   ├── canary/
│   ├── investigate/
│   ├── retro/
│   ├── cso/
│   ├── health/
│   ├── benchmark/
│   ├── browse/
│   ├── codex/
│   ├── pair-agent/
│   ├── learn/
│   ├── checkpoint/
│   ├── freeze/ & unfreeze/
│   ├── guard/
│   └── careful/
├── tests/                     # 三层测试体系
│   ├── touchfiles.ts          # diff-based 依赖声明
│   └── ...
└── ~/.gstack/                 # 运行时状态
    ├── browse.json            # daemon 状态
    └── freeze-dir.txt         # freeze 持久化
```

---

## 2. 源清单

### Specialist Skills（23 个）

| 路径 | 大小/行数 | 角色 |
|------|-----------|------|
| `/office-hours` | — | 办公时间对话模式 |
| `/plan-ceo-review` | — | CEO 视角审查 plan |
| `/plan-eng-review` | — | Engineering 视角审查 plan |
| `/plan-design-review` | — | Design 视角审查 plan |
| `/plan-devex-review` | — | Developer Experience 视角审查 plan |
| `/plan-tune` | — | 调优 plan |
| `/autoplan` | — | 自动审查流水线：CEO → Design → Eng → DX |
| `/review` | — | Pre-landing PR 审查 |
| `/qa` | — | QA 全流程（包含修复） |
| `/qa-only` | — | QA 仅检查（不修复） |
| `/design-consultation` | — | 设计咨询 |
| `/design-shotgun` | — | 快速设计迭代 |
| `/design-review` | — | 设计审查 |
| `/design-html` | — | HTML 设计稿生成 |
| `/ship` | — | 发布流程 |
| `/land-and-deploy` | — | PR 合并 + 部署 |
| `/setup-deploy` | — | 部署环境配置 |
| `/document-release` | — | 发布文档生成 |
| `/canary` | — | Canary 发布 |
| `/investigate` | — | 根因调查（Iron Law: 无根因不修复） |
| `/retro` | — | 事后复盘 |
| `/cso` | — | 安全审查（OWASP + STRIDE） |
| `/health` | — | 项目健康检查 |

### Power Tools（8 个）

| 路径 | 大小/行数 | 角色 |
|------|-----------|------|
| `/benchmark` | — | 性能基准测试 |
| `/browse` | — | Headless browser QA，Chromium daemon |
| `/codex` | — | Codex 集成 |
| `/open-gstack-browser` | — | 打开 gstack 内置浏览器 |
| `/pair-agent` | — | Agent 配对编程 |
| `/learn` | — | 学习/研究模式 |
| `/checkpoint` | — | 检查点保存 |
| `/investigate` | — | 根因分析（同时列为 specialist 和 power tool） |

### 保障机制

| 路径 | 大小/行数 | 角色 |
|------|-----------|------|
| `/freeze` + `/unfreeze` | — | PreToolUse hook 限制 Edit/Write 到特定目录 |
| `/guard` | — | ship/deploy/delete 操作的确认门控 |
| `/careful` | — | 副作用 shell 命令前的审批门控 |
| `~/.gstack/freeze-dir.txt` | — | freeze 状态持久化文件 |

### 基础设施

| 路径 | 大小/行数 | 角色 |
|------|-----------|------|
| `SKILL.md.tmpl` | — | 根模板，`{{COMMAND_REFERENCE}}` 等占位符 |
| `gen-skill-docs.ts` | — | 模板生成器：SKILL.md.tmpl → SKILL.md |
| `bin/` (36+ 文件) | — | CLI 工具集 |
| `tests/touchfiles.ts` | — | diff-based 测试依赖声明 |
| `~/.gstack/browse.json` | — | Browse daemon 状态（pid, port, token, startedAt, binaryVersion） |

---

## 3. 对象模型

### 一等实体

| 实体 | 定义位置 | 必要字段 | 生命周期 | 分类 |
|------|---------|---------|---------|------|
| **Skill** | 各 skill 目录 | SKILL.md, slash command | register → invoke → complete | command |
| **Plan** | autoplan 流水线 | content, review stages | draft → CEO review → design review → eng review → DX review → finalize | document |
| **SkillTestResult** | test runner | toolCalls, browseErrors, exitReason, costEstimate, transcript | spawn → execute → collect → persist | test-artifact |
| **TestDelta** | EvalCollector | status_change (improved/regressed/unchanged) | compare → classify → report | eval-metric |
| **BrowseSession** | browse daemon | pid, port, token, startedAt, binaryVersion | start → serve → version-check → restart | daemon |
| **FreezeState** | `~/.gstack/freeze-dir.txt` | directory path | freeze → persist → unfreeze | constraint |
| **EvalPartial** | `_partial-e2e.json` | incremental results | collect → append → finalize | persistence |
| **TouchfileMapping** | `touchfiles.ts` | test → file glob[] | declare → git diff match → select tests | dependency |

### Skill 模板系统

gstack 的 skill 注册采用独特的模板生成模式：

```
SKILL.md.tmpl（手写模板）
  ├── {{COMMAND_REFERENCE}}    ← 所有 slash command 列表
  ├── {{SNAPSHOT_FLAGS}}       ← 当前功能开关状态
  ├── {{PREAMBLE}}             ← 通用前言
  └── 其他占位符...
        │
        ▼  gen-skill-docs.ts
SKILL.md（自动生成，运行时使用）
```

这种设计确保所有 skill 的文档从单一模板源生成，避免手动维护 N 份 SKILL.md 时的不一致。

### 实体关系

```
SKILL.md.tmpl (1) ──generates──> SKILL.md (1)
Skill (23+8) ──registered-in──> SKILL.md
Plan (1) ──reviewed-by──> autoplan pipeline (4 stages)
SkillTestResult (N) ──collected-by──> EvalCollector
EvalCollector (1) ──produces──> TestDelta (N)
TouchfileMapping (1) ──selects──> Test (N) via git diff
BrowseSession (1) ──serves──> /browse skill
FreezeState (1) ──constrains──> Edit/Write tools
```

### 上下文隔离策略

| 范围 | 流向 | 机制 | 说明 |
|------|------|------|------|
| 用户 → Skill | slash command 调用 | SKILL.md 注册 + Claude 路由 | 每个 skill 有独立的 prompt 上下文 |
| Skill → Browser | HTTP API | Bearer token auth + localhost | BrowseSession 隔离 |
| Freeze → Tool | PreToolUse hook | `~/.gstack/freeze-dir.txt` 持久化 | 跨 session 生效 |
| Test → Code | touchfiles.ts | git diff → glob match | 只运行受影响的测试 |

---

## 4. 流程与状态机

### Happy Path: autoplan 自动审查流水线

1. **用户调用 `/autoplan`** — 提交一份 plan 草案
2. **CEO Review** (`/plan-ceo-review`) — 从商业价值、用户影响、战略对齐角度审查
3. **Design Review** (`/plan-design-review`) — 从用户体验、界面一致性、可用性角度审查
4. **Engineering Review** (`/plan-eng-review`) — 从技术可行性、架构合理性、性能角度审查
5. **DX Review** (`/plan-devex-review`) — 从开发者体验、API 设计、工具链角度审查
6. **Plan Finalize** — 汇总四轮审查意见，生成最终版本

### Happy Path: /investigate (Iron Law)

1. **触发调查** — 用户报告 bug 或异常行为
2. **Root Cause 分析** — **Iron Law: 不确定根因之前不允许修复**
3. **证据收集** — 日志、复现步骤、代码追踪
4. **根因确认** — 明确根本原因
5. **修复方案** — 仅在根因确认后提出修复

### Happy Path: /ship + /land-and-deploy

1. **`/ship`** — 准备发布，运行检查
2. **`/review`** — Pre-landing PR 审查
3. **Guard gate** — `/guard` 确认门控（ship/deploy/delete 需显式确认）
4. **`/land-and-deploy`** — PR merge + 部署
5. **`/canary`** — 可选的 canary 发布阶段
6. **`/document-release`** — 生成发布文档

### Browse Daemon 生命周期

```
首次调用 /browse
    │
    ▼
启动 Chromium + Bun HTTP server（localhost）
    │ ~3s 冷启动
    ▼
运行态（Bearer token auth）
    │ 后续调用 ~100-200ms
    ▼
Ref 系统（@e1, @e2）via accessibility snapshot
    │
    ▼
Version check（每次 CLI 调用时检查 binaryVersion）
    │ 版本不匹配
    ▼
自动重启（杀旧进程 → 启新进程）
```

状态持久化于 `~/.gstack/browse.json`：`{ pid, port, token, startedAt, binaryVersion }`。写入采用 atomic write（tmp + rename）确保一致性。

### Cookie 安全模型

Browse daemon 的 cookie 处理：Keychain 存储 → PBKDF2 + AES 解密 → in-memory only（不落盘）。

### 测试执行流程

```
git diff（获取变更文件列表）
    │
    ▼
touchfiles.ts（声明每个测试依赖的文件 glob）
    │ 匹配
    ▼
选中测试子集 ←── GLOBAL_TOUCHFILE 变更时触发全量
    │
    ▼
三层执行：
  Tier 1: Static（免费, <2s, parse commands）
  Tier 2: E2E（spawn `claude -p`, ~$3.85/run, ~20min）
  Tier 3: LLM Judge（Sonnet 评分, ~$0.15/run）
    │
    ▼
EvalCollector 收集结果
  ├── _partial-e2e.json（增量写入）
  └── 最终 timestamped 文件
    │
    ▼
TestDelta 对比（improved / regressed / unchanged）
```

### Session Runner 细节

E2E 测试通过 session runner 执行：spawn `claude -p` subprocess → stream NDJSON → parse `SkillTestResult`。每个结果包含 `toolCalls`、`browseErrors`、`exitReason`、`costEstimate`、`transcript`。

### 失败路径

| 触发 | 响应 | 恢复 |
|------|------|------|
| `/freeze` 目录外编辑 | PreToolUse hook 拒绝 Edit/Write | 用户 `/unfreeze` 或切换目录 |
| `/guard` 未确认 | 阻止 ship/deploy/delete | 用户显式确认 |
| Browse daemon 崩溃 | 下次 `/browse` 调用检测到 pid 不存在 | 自动重启 |
| Binary version 不匹配 | CLI 调用时检测到 | 自动重启 daemon |
| E2E 测试超时 | session runner timeout | 记录失败，继续下一测试 |
| GATE tier 失败 | 阻止 PR merge | 修复后重跑 |

---

## 5. 执行保障审计

### 保障矩阵

| 机制 | Hard（代码强制） | Soft（约定/文档） | Unenforced（仅声明） |
|------|------------------|-------------------|---------------------|
| **Freeze 目录锁** | ✅ PreToolUse hook 拦截 | | |
| **Freeze 持久化** | ✅ `~/.gstack/freeze-dir.txt` 跨 session | | |
| **Guard 确认门控** | ✅ ship/deploy/delete 前必须确认 | | |
| **Careful 审批** | ✅ 副作用 shell 命令前审批 | | |
| **GATE tier 测试** | ✅ ~50 tests, 阻止 PR merge | | |
| **PERIODIC tier 测试** | | ✅ ~40+ tests, weekly cron | |
| **Iron Law (investigate)** | | ✅ "无根因不修复"约定 | |
| **autoplan 四轮审查** | | ✅ CEO → Design → Eng → DX 顺序约定 | |
| **Browse token auth** | ✅ Bearer token 验证 | | |
| **Cookie 安全** | ✅ Keychain + PBKDF2 + AES, in-memory only | | |
| **Atomic state write** | ✅ tmp + rename 写入 browse.json | | |
| **Version auto-restart** | ✅ 每次 CLI 调用检查 binaryVersion | | |
| **Diff-based test select** | ✅ touchfiles.ts + git diff 自动选择 | | |
| **GLOBAL_TOUCHFILE** | ✅ 全局变更触发全量测试 | | |
| **Skill 模板单源** | ✅ SKILL.md.tmpl → gen-skill-docs.ts | | |
| **Tier 1 静态测试** | ✅ parse-level 校验, 免费 <2s | | |
| **CSO 安全审查** | | ✅ OWASP + STRIDE 框架约定 | |
| **Boil the Lake 哲学** | | | ⚠️ 理念层面，无代码强制 |

### 分析

gstack 的保障体系呈现"双层防线"特征。第一层是**工具级硬强制**：freeze hook、guard gate、careful gate 三道门控在 tool invocation 层拦截危险操作，这是整个框架中最独特的设计。第二层是**测试级硬强制**：GATE tier 阻止未通过测试的 PR merge，diff-based 选择确保测试覆盖精准且经济。

值得注意的是 Iron Law（"无根因不修复"）虽然只是 soft enforcement，但它嵌入在 `/investigate` skill 的 prompt 中，是整个 debug 哲学的核心——这比代码层面的 lint 规则更深刻地影响工程行为。

---

## 6. Prompt 目录

### Prompt 1: /investigate 的 Iron Law

`/investigate` skill 的核心约束是 Iron Law——一条贯穿整个调查流程的不可违反原则：

> **Iron Law**: No fixes without root cause.
> 在确定根本原因之前，禁止提出任何修复方案。先收集证据、追踪调用链、复现问题，确认根因后才能动手修复。

这条规则看似简单，却解决了 AI agent 最常见的 anti-pattern：跳过分析直接猜测修复。大多数 agent 在看到 error 后会立即尝试"可能的修复"，导致掩盖真正的问题。Iron Law 强制 agent 必须经过完整的调查流程。

### Prompt 2: SKILL.md.tmpl 模板系统

根模板使用占位符系统将动态内容注入 skill 文档：

```markdown
{{PREAMBLE}}

# Commands

{{COMMAND_REFERENCE}}

# Current Configuration

{{SNAPSHOT_FLAGS}}
```

`gen-skill-docs.ts` 在构建时扫描所有 skill 目录，收集 command 列表、feature flag 状态等信息，填充占位符后生成最终的 `SKILL.md`。这确保了：
- 所有 command 的帮助文档始终与实现同步
- Feature flag 状态自动反映在 prompt 中
- 新增 skill 只需创建目录，无需手动更新根文档

---

## 7. 微观设计亮点

### Highlight 1: diff-based 测试选择 + 成本感知

- **观察**: `touchfiles.ts` 为每个测试声明文件依赖 glob，`git diff` 匹配后只运行受影响的测试。三层测试分别标注成本：Tier 1 免费 / Tier 2 ~$3.85 / Tier 3 ~$0.15
- **证据**: `touchfiles.ts`, GATE tier (~$0-15, ~50 tests), PERIODIC tier (~$20-40, ~40+ tests)
- **价值**: 在 AI 测试成本非零（每次 E2E 需 spawn Claude session）的场景下，精准的测试选择直接节省真金白银。`GLOBAL_TOUCHFILE` 作为安全网确保关键变更不漏测
- **权衡**: touchfiles 依赖声明需人工维护，遗漏依赖会导致回归
- **可迁移性**: Direct — `1st-cc-plugin` 的 plugin validator 可引入类似的"变更影响分析 → 选择性校验"模式

### Highlight 2: Browse Daemon 的 Ref 系统

- **观察**: Headless Chromium daemon 通过 accessibility snapshot 为页面元素生成 `@e1, @e2, ...` 引用，agent 可在对话中直接引用 `@e3` 指代特定 UI 元素
- **证据**: Browse daemon 实现，Bearer token auth，首次 ~3s / 后续 ~100-200ms
- **价值**: 将视觉内容转化为 agent 可操作的符号引用，弥合了"agent 看不到 UI"的鸿沟。长驻 daemon 避免每次调用的冷启动开销
- **权衡**: Chromium 内存占用大；accessibility snapshot 可能遗漏非标准 UI 元素
- **可迁移性**: Inspired — 理念可借鉴，但需要 Playwright + Bun 基础设施

### Highlight 3: Freeze/Unfreeze 目录锁

- **观察**: `/freeze` 通过 PreToolUse hook 将 Edit/Write 限制到特定目录，状态持久化到 `~/.gstack/freeze-dir.txt`，跨 session 生效
- **证据**: freeze hook 实现，`~/.gstack/freeze-dir.txt` 持久化
- **价值**: 在大型 monorepo 中防止 agent 意外修改非目标目录。持久化设计避免每次 session 重新设置。`/unfreeze` 提供安全的解除路径
- **权衡**: 全局单目录锁粒度较粗；多任务并行时可能互相阻塞
- **可迁移性**: Direct — PreToolUse hook + 文件持久化模式可直接用于 `1st-cc-plugin` 的安全约束

---

## 8. 宏观设计亮点

### Philosophy 1: "Boil the Lake"（煮沸整个湖）

gstack 的核心设计哲学是"Boil the Lake"——在 AI 时代，完成一件事的**边际完整性成本**趋近于零。与其做 80% 然后手动补完剩余 20%，不如让 AI 做完 100%。这一理念直接驱动了 `/autoplan` 的四轮全维度审查设计：CEO、Design、Engineering、DX 四个视角一个不落。在传统开发中，让四位专家逐一审查一份 plan 的成本极高；在 AI specialist 模式下，成本接近零。

这一哲学同样解释了为什么 gstack 有 23 个 specialist 而非 3-5 个通用 skill——**specialization is free**，每多一个 specialist 的维护成本远低于其带来的审查质量提升。

### Philosophy 2: "Search Before Building"（先搜再造）

与 "Boil the Lake" 互补的第二原则。在 AI 能力过剩的环境下，最大的浪费不是写了糟糕的代码，而是重新发明已有的方案。`/investigate` 的 Iron Law、`/learn` 的研究模式都体现了这一原则：先充分理解现状，再决定行动。

---

## 9. 失败模式与局限

| # | 失败模式 | 触发 | 影响 | 证据 |
|---|---------|------|------|------|
| 1 | **touchfiles 依赖遗漏** | 新增代码路径未在 touchfiles.ts 中声明 | diff-based 选择漏掉相关测试，回归无法被 GATE 拦截 | touchfiles 需手工维护 |
| 2 | **E2E 测试成本失控** | 频繁触发 GLOBAL_TOUCHFILE 或大量 Tier 2 测试 | 单次测试运行成本可达 $15+，weekly PERIODIC 达 $40+ | 成本标注 |
| 3 | **Browse daemon 内存泄漏** | 长时间运行 Chromium 不重启 | 系统内存压力增大 | Chromium 已知长时间运行问题 |
| 4 | **Freeze 单目录限制** | 需要同时编辑两个不相关的目录 | 必须频繁 freeze/unfreeze 切换 | 全局单 freeze-dir 设计 |
| 5 | **autoplan 四轮延迟** | 每轮审查需完整 LLM 调用 | 简单 plan 也需经历四轮审查，浪费时间和 token | 流水线固定四阶段 |
| 6 | **Iron Law 过度约束** | 明显的 typo 或 trivial fix | 仍需完整调查流程，效率低下 | 无 severity-based 豁免 |
| 7 | **模板生成时效** | 修改 skill 后忘记重新运行 gen-skill-docs.ts | SKILL.md 与实际实现不同步 | 手动触发生成 |
| 8 | **Session runner 不稳定** | `claude -p` subprocess 异常退出 | NDJSON stream 中断，部分测试结果丢失 | E2E 测试依赖 external process |

### 声明 vs 实际行为偏差

| 声明 | 来源 | 实际行为 | 证据等级 |
|------|------|---------|---------|
| "Boil the Lake" 完整性 | 设计哲学 | 受限于 LLM context window 和 API 成本 | indirect |
| GATE tier 阻止 PR | 测试框架 | 仅 ~50 tests，覆盖率未知 | direct |
| Iron Law 无例外 | /investigate prompt | Soft enforcement，agent 可忽略 | direct |
| Browse Ref 全覆盖 | /browse 设计 | Accessibility snapshot 可能遗漏非标准元素 | indirect |

---

## 10. 迁移评估

### 候选机制

| # | 机制 | 评级 | 工作量 | 前提 | 风险 | 来源 |
|---|------|------|--------|------|------|------|
| 1 | Freeze/Unfreeze 目录锁 | Direct | S | PreToolUse hook | 无 | `/freeze` skill |
| 2 | Iron Law (无根因不修复) | Direct | S | prompt 设计 | 无 | `/investigate` |
| 3 | Guard 确认门控 | Direct | S | PreToolUse hook | 无 | `/guard` |
| 4 | diff-based 测试选择 | Inspired | M | touchfiles 依赖声明 | 维护成本 | `touchfiles.ts` |
| 5 | autoplan 多视角审查流水线 | Inspired | M | 多 specialist 定义 | token 成本 | `/autoplan` |
| 6 | Browse Ref 系统 | Inspired | L | Playwright + daemon | 基础设施重 | `/browse` |
| 7 | Skill 模板生成 (tmpl → md) | Inspired | M | 模板引擎 | 与 plugin.json 体系冲突 | `SKILL.md.tmpl` |
| 8 | Careful 审批门控 | Direct | S | hook 实现 | 无 | `/careful` |
| 9 | EvalCollector 增量持久化 | Inspired | M | JSON 存储 | 额外 IO | `_partial-e2e.json` |
| 10 | 三层测试 + 成本标注 | Inspired | M | 测试框架 | 成本度量 | 测试体系 |

### 推荐采纳顺序

1. **Iron Law (无根因不修复)** — 零成本引入，直接写入 `quality/` 相关 skill 的 prompt 中。对 `1st-cc-plugin` 中 debug 类 skill 质量提升最大
2. **Freeze/Unfreeze 目录锁** — PreToolUse hook + 文件持久化，技术简单，对大型项目场景价值高。可集成到 `quality/ai-hygiene` 或新建独立 skill
3. **Guard + Careful 门控** — 三道门控（freeze / guard / careful）形成完整的安全防线。可集成到 `workflows/` 或 `quality/` 插件组
4. **autoplan 多视角审查概念** — 借鉴四轮审查流水线思想，可用于 `workflows/deep-plan` 的增强
5. **diff-based 测试选择概念** — 为 `quality/testing` 添加变更影响分析能力，但需要构建 touchfile 机制

---

## 11. 开放问题

| # | 问题 | 优先级 | 说明 |
|---|------|--------|------|
| 1 | SKILL.md.tmpl 占位符完整列表？ | Medium | 除 `COMMAND_REFERENCE`、`SNAPSHOT_FLAGS`、`PREAMBLE` 外还有哪些？ |
| 2 | Freeze 多目录支持计划？ | Low | 当前单目录限制是设计选择还是尚未实现？ |
| 3 | GATE vs PERIODIC 测试划分标准？ | High | 哪些测试进 GATE（阻止 PR），哪些进 PERIODIC（weekly），决策依据是什么？ |
| 4 | Browse Ref 持久化？ | Medium | `@e1` 等引用是否跨 session 持久化，还是每次重新生成？ |
| 5 | autoplan 四轮审查的跳过机制？ | High | 简单 plan 是否可以跳过部分审查阶段？ |
| 6 | Garry Tan 本人的使用模式？ | Low | 作为 YC CEO，日常使用哪些 specialist 频率最高？ |
| 7 | touchfiles 自动生成可能性？ | Medium | 是否可以从代码 import graph 自动推断依赖而非手工声明？ |
| 8 | `/cso` 安全审查的覆盖范围？ | Medium | OWASP + STRIDE 框架是完整实现还是部分覆盖？ |

---

## 附录：Gemini Deepdive 补充信息

> 来源：`1st-cc-plugin/workflows/loaf/docs/gemini-roadmap-review/deepdive-gstack.md`
> 补充内容：Hook 脚本的具体实现、permissionDecision JSON 协议、advisory vs hard block 区分。

### A.1 `check-careful.sh` 实现细节

该脚本作为 Claude Code hook 拦截危险操作：

1. **输入**：从 stdin 读取 JSON（包含 `tool_name` 和 `tool_input`）
2. **解析**：使用 `grep`/`sed` 提取 `tool_input`，失败时 fallback 到 `python3 -c 'import json...'`
3. **检测模式**：匹配破坏性命令模式（`rm -rf`、`git reset --hard`、`git push --force`、`drop table` 等）
4. **输出**：
   ```json
   {"permissionDecision": "ask", "message": "⚠️ Detected potentially destructive command: rm -rf"}
   ```
   `"ask"` 将自主执行转为交互确认（advisory warning），不阻止操作。

### A.2 `check-freeze.sh` 实现细节

该脚本实现目录级硬性写保护：

1. 读取 `freeze-dir.txt`（一行一个受保护路径）
2. 从 hook JSON 中提取 `file_path` 参数
3. 逐行比较，匹配则返回：
   ```json
   {"permissionDecision": "deny", "message": "🚫 File is in frozen directory: src/core/"}
   ```
   `"deny"` 是硬性阻止，Claude Code 直接拒绝执行，无法绕过。

### A.3 Permission Decision 协议

两种决策的关键区别：
| Decision | 效果 | 用户体验 |
|----------|------|----------|
| `"ask"` | 自主模式 → 交互模式（需人工确认） | Advisory warning，用户可选择继续 |
| `"deny"` | 硬性拒绝 | 操作被阻止，无法执行 |

### A.4 `.tmpl` 模板注册机制

Hook 脚本通过 `.tmpl` 模板文件注册到 Claude Code 的 `settings.json`：
- 模板包含 hook 触发事件（`PreToolUse`）、脚本路径、匹配条件
- `gstack init` 从模板生成实际配置，确保格式与 Claude Code 期望一致
