# Workflow Research: aegisFlow (williamnie/aegisFlow)

**Date**: 2026-04-18
**Source**: `vendor/aegisFlow` (https://github.com/williamnie/aegisFlow)
**Analyst mode**: Single
**Focus**: All

---

## 1. 框架概况

| 属性 | 值 |
|------|-----|
| **类型** | 多 Agent CLI 编排器 — 从 idea 到交付的 8 阶段流水线 |
| **总文件数** | 29 |
| **Prompt 文件** | 0（prompt 内嵌于 TypeScript 代码中） |
| **脚本/钩子** | 0 |
| **测试文件** | 0 |
| **入口** | `src/index.ts` → `src/orchestrator.ts` |
| **注册机制** | npm 全局安装 → `aegis` CLI 命令 |
| **语言** | TypeScript (Node.js 18+) |

### 目录结构

```
aegisFlow/
├── src/
│   ├── index.ts                # CLI 入口
│   ├── orchestrator.ts         # 核心编排器（~2000+ 行）
│   ├── schemas.ts              # JSON Schema 定义（结构化输出）
│   ├── types.ts                # TypeScript 类型定义
│   ├── config.ts               # 配置加载
│   ├── engine-discovery.ts     # 引擎检测 (claude/codex/gemini)
│   ├── engine/consensus.ts     # 共识引擎
│   ├── store/index.ts          # 会话持久化
│   ├── adapters/               # CLI 适配器
│   │   ├── base.ts
│   │   ├── cli-strategies.ts
│   │   └── acp-wrapper.ts
│   ├── ui/chat-cli.ts          # 交互式 UI
│   └── i18n.ts, defaults.ts, utils.ts, paths.ts
├── package.json                # v1.0.4, esbuild 打包
├── CHANGELOG.md
└── README.md / README_zh.md
```

---

## 2. 源清单

### Overview Sources
| 文件 | 类型 | 价值 |
|------|------|------|
| `README.md` | 用户文档 | 8 阶段工作流、CLI 用法、引擎支持 |
| `README_zh.md` | 中文文档 | 同上 |
| `CHANGELOG.md` | 变更日志 | 版本演进记录 |

### Execution Sources
| 文件 | 类型 | 价值 |
|------|------|------|
| `src/orchestrator.ts` | 核心编排器 | 全部阶段逻辑：idea → review → roundtable → execution |
| `src/engine-discovery.ts` | 引擎检测 | 运行时发现 claude/codex/gemini CLI |
| `src/adapters/` | CLI 适配器 | 统一 API 调用不同 agent CLI |
| `src/store/index.ts` | 会话存储 | 持久化阶段状态用于恢复 |

### Prompt Sources
| 文件 | 类型 | 价值 |
|------|------|------|
| `src/orchestrator.ts` | 内嵌 prompt | prompt 字符串直接写在编排器代码中 |
| `src/schemas.ts` | JSON Schema | 约束 agent 输出为结构化 JSON |

### Enforcement Sources
| 文件 | 类型 | 价值 |
|------|------|------|
| `src/schemas.ts` | Schema 校验 | JSON Schema 强制输出格式 |
| `src/engine/consensus.ts` | 共识引擎 | 多 agent 审查结论汇总 + 分歧触发圆桌 |

---

## 3. 对象模型

### 一等实体

| 实体 | 定义位置 | 必要字段 | 生命周期 | 分类 |
|------|---------|---------|---------|------|
| **Session** | `src/store/` | session-id, stage | create → persist → resume | fact |
| **IdeaBrief** | `src/schemas.ts` | rawIdea, targetUsers, goals, constraints | intake → validate → freeze | fact |
| **RequirementPack** | `src/types.ts` | summary, assessment, validation | generate → review → approve | fact |
| **StructuredReview** | `src/schemas.ts` | verdict, findings[], severity | generate → consensus → roundtable | fact |
| **TaskGraph** | `src/schemas.ts` | nodes[], dependencies | generate → execute → complete | fact |
| **RoundtableMinutes** | `src/schemas.ts` | turns[], final_decision | open → debate → resolve | evidence |

### 实体关系

```
Session (1) ──tracks──> Stage (8)
Stage0: IdeaBrief ──produces──> RequirementPack
Stage1-2: RequirementPack ──produces──> PRD + TechDesign
Stage3: PRD/Design ──reviewed-by──> StructuredReview (N per engine)
Stage4: Reviews ──fed-into──> RoundtableMinutes
Stage5-6: TaskGraph ──contains──> TaskNode (N)
Stage7: IntegrationReview
```

### 上下文隔离策略

| 范围 | 流向 | 机制 | 证据 |
|------|------|------|------|
| 编排器 → Agent | prompt + schema + 前序文档 | CLI spawn + JSON schema | `src/orchestrator.ts` |
| Agent → 编排器 | 结构化 JSON | schema 校验 | `src/schemas.ts` |
| 多引擎审查 | 独立上下文 | 各引擎分别 spawn | ENGINE_LENSES 变量 |
| 跨会话 | 持久化 artifacts | 文件系统 + session store | `src/store/` |

---

## 4. 流程与状态机

### Happy Path

1. `aegis` — 启动新会话 — `src/index.ts`
2. **Stage 0**: Idea intake — 提问 2-4 个 follow-up 问题 — `orchestrator.ts`
3. **Stage 0.5**: Requirement gate — 验证需求完整性
4. **Stage 1**: PRD 生成 — 输出 `prd.md`
5. **Stage 2**: Tech design — 输出 `design.md`
6. **Stage 3**: 独立多引擎审查 — 每个引擎带不同 lens (架构/实现/UX)
7. **Stage 4**: 共识汇总；若分歧则圆桌辩论
8. **Stage 4.5**: 开发策略选择
9. **Stage 5**: Task planning — 输出 task graph DAG
10. **Stage 6**: 逐任务执行 + workspace snapshot diff
11. **Stage 7**: Integration review + 交付报告

### 阶段转换

| From | To | 触发 | Gate? | 证据 |
|------|----|------|-------|------|
| stage0 | stage0.5 | idea brief 完成 | Yes — schema 校验 | `IDEA_BRIEF_SCHEMA` |
| stage0.5 | stage1 | requirement 验证通过 | Yes — assessment 校验 | `REQUIREMENT_ASSESSMENT_SCHEMA` |
| stage3 | stage4 | 所有引擎审查完成 | Yes — consensus engine | `ConsensusEngine` |
| stage5 | stage6 | task graph 生成 | Yes — TASK_GRAPH_SCHEMA | `src/schemas.ts` |

### 失败路径

#### 失败路径 1：引擎不可用
`engine-discovery.ts` 检测可用引擎。若所有引擎都不可用，流程中止。部分引擎缺失时降级为可用引擎。

#### 失败路径 2：审查分歧无法收敛
圆桌辩论有固定轮数限制，最终由 final_decision 字段强制收敛，但决策质量可能受限。

---

## 5. 执行保障审计

| # | 约束 | 来源 | 等级 | 证据 | 缺口? |
|---|------|------|------|------|-------|
| 1 | 输出格式 | `src/schemas.ts` | Hard — JSON Schema 校验 | 11 个 schema 定义 | No |
| 2 | 阶段顺序 | `src/orchestrator.ts` | Hard — 代码流程控制 | 顺序执行 + `--from` 重启 | No |
| 3 | 多引擎独立审查 | `ENGINE_LENSES` | Hard — 分别 spawn | 每引擎独立上下文 | No |
| 4 | 会话可恢复 | `src/store/` | Hard — 文件持久化 | `--sessions` + `<session-id>` | No |
| 5 | 需求充分性 | requirement gate | Soft — LLM 判断 | 无硬性完整性检查 | Yes |
| 6 | 代码质量 | stage6 执行 | Soft — 无测试 gate | 无 TDD 要求 | Yes |

### 执行保障统计

| 等级 | 数量 | 百分比 |
|------|------|--------|
| Hard-enforced | 4 | 67% |
| Soft-enforced | 2 | 33% |
| Unenforced | 0 | 0% |

---

## 6. Prompt 目录

### Prompt: 引擎角色分配

| 字段 | 值 |
|------|-----|
| **repo_path** | `src/orchestrator.ts` (ENGINE_LENSES) |
| **quote_excerpt** | "claude: 'architecture, boundaries, long-range tradeoffs'; codex: 'backend implementation, data flow, testing'; gemini: 'frontend UX, interaction design'" |
| **stage** | Stage 3 (审查) |
| **design_intent** | 三引擎分工审查，避免同质化意见 |
| **hidden_assumption** | 三引擎的能力确实符合声称的分工 |
| **likely_failure_mode** | 引擎能力趋同时分工失去意义；单引擎时退化为自审 |
| **evidence_level** | direct |

---

## 7. 微观设计亮点

### Highlight: 结构化 Schema 约束输出

- **观察**: 11 个 JSON Schema 强制每个阶段的 agent 输出格式
- **证据**: `src/schemas.ts` 全文
- **价值**: 消除自由文本解析的不确定性，确保下游阶段可消费上游输出
- **权衡**: Schema 刚性可能限制 agent 表达，边界 case 可能被 schema 拒绝
- **可迁移性**: Direct — schema-constrained output 模式直接可用

### Highlight: 圆桌辩论机制

- **观察**: 当审查者之间存在分歧时，自动启动多轮圆桌辩论
- **证据**: `src/engine/consensus.ts`, `ROUNDTABLE_MINUTES_SCHEMA`
- **价值**: 将分歧显性化并通过辩论收敛，而非简单多数投票
- **权衡**: 辩论质量依赖引擎能力，固定轮数可能过早截断
- **可迁移性**: Inspired — 辩论机制值得借鉴，但实现需适配

### Highlight: Workspace Snapshot Diff

- **观察**: 执行阶段前后对比 workspace 文件变化
- **证据**: `src/utils.ts` (captureWorkspaceSnapshot, diffSnapshots)
- **价值**: 精确追踪 agent 每个任务的实际文件变更
- **权衡**: 大型项目 snapshot 可能很慢
- **可迁移性**: Direct — snapshot + diff 模式通用

---

## 8. 宏观设计亮点

### Philosophy: 多引擎共识

- **观察**: 不信任单一 LLM 的判断，通过多引擎交叉审查产生共识
- **出现位置**: `src/orchestrator.ts` ENGINE_LENSES, `src/engine/consensus.ts`
- **塑造方式**: 每个引擎带预设 lens 审查，分歧时触发圆桌，最终产生有据可查的共识
- **优势**: 减少单点偏见，审查更全面
- **局限**: 依赖多个 CLI 可用性；成本 3x+；引擎退化时共识无意义
- **采纳?**: Inspired — 多引擎概念好但实际部署门槛高

---

## 9. 失败模式与局限

| # | 失败模式 | 触发 | 影响 | 证据 |
|---|---------|------|------|------|
| 1 | 无测试保障 | 仓库 0 测试文件 | 回归风险高 | `find . -name "test_*"` 为空 |
| 2 | Prompt 与代码耦合 | prompt 内嵌 orchestrator.ts | 修改 prompt 需改代码重新打包 | `src/orchestrator.ts` |
| 3 | 单引擎降级 | 仅 claude 可用 | 独立审查退化为自审 | `src/engine-discovery.ts` |
| 4 | 无实现质量 gate | stage6 无 TDD | 交付代码可能有 bug | 无测试 schema |

### 声明 vs 实际行为偏差

| 声明 | 来源 | 实际行为 | 证据 | 证据等级 |
|------|------|---------|------|---------|
| "Multi-agent reviews" | README.md | 单引擎时退化为单 agent | engine-discovery 逻辑 | direct |

---

## 10. 迁移评估

### 候选机制

| # | 机制 | 评级 | 工作量 | 前提 | 风险 | 来源 |
|---|------|------|--------|------|------|------|
| 1 | JSON Schema 约束输出 | Direct | S | schema 定义 | 无 | `src/schemas.ts` |
| 2 | 多引擎共识 + 圆桌 | Inspired | L | 多 LLM 接入 | 成本高 | `src/engine/consensus.ts` |
| 3 | 8 阶段流水线 | Inspired | M | 编排框架 | 过重 | `src/orchestrator.ts` |
| 4 | 会话持久化 + 恢复 | Direct | S | 文件存储 | 无 | `src/store/` |
| 5 | Workspace snapshot diff | Direct | S | fs 工具 | 无 | `src/utils.ts` |

### 推荐采纳顺序

1. **JSON Schema 约束输出** — 立即可用，最高 ROI
2. **Workspace snapshot diff** — 低成本实现变更追踪
3. **会话持久化** — 长流程必需
4. **圆桌辩论概念** — 用于关键决策点

---

## 11. 开放问题

1. 圆桌辩论在实际使用中的收敛率？多少轮通常足够？
2. `--from` 重启阶段时，artifact 清理是否完整？
3. 是否计划支持更多引擎（如 Qwen、Deepseek）？
