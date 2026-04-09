# 18. 实施参考指南：博取百家之长，但不整套照搬

> **定位**：这篇文档专门回答“当我们真的开始实现这套 workflow 时，每个部分最值得参考哪个成熟框架的什么实现”。

> **目标**：把研究材料从“理念来源”推进到“实施参考来源”。

---

## 0. 先给结论

不要试图找一个“最好的框架”整套搬。

更好的实现策略是：

- **路由层**参考一类
- **状态机/协议层**参考一类
- **agents / commands / skills** 参考一类
- **hooks / hard guard**参考一类
- **validators / scripts / wrappers** 参考一类
- **长任务恢复**参考一类
- **验证 / 审查 / 质量门**参考一类
- **多模型 / 多 worker**只在需要时参考

也就是说：

> 我们要抄的是“子系统最佳实践”，不是“框架人格”。

---

## 1. 最高层判断：哪些框架最值得借

先给一个总图：

| 实施部位 | 第一参考 | 第二参考 | 第三参考（新增） | 不建议照搬 |
|---------|---------|---------|-----------------|-----------|
| 路由层 | GSD | FlowSpec | **Compound Engineering**（scope-aware ceremony + Phase 0 triage）| 只靠单一评分器 |
| 状态机 / phase / artifacts | FlowSpec | Harness engineering 文档 | **Claude-Code-Workflow**（Completion Status Protocol + 3-Strike）| 纯 markdown 约定无状态机 |
| 协议链（Task→Evidence→Reconcile） | PAUL 思路 + 现有 `14` | ECC-Mobile | — | 只写 summary 不做对账 |
| agents 角色设计 | Superpowers | GSD / ECC-Mobile | **Compound Engineering**（28+ tiered persona reviewers）| 一个大 prompt 包打天下 |
| commands 组织 | GSD | FlowSpec / CCG | — | command 内塞业务逻辑 |
| skills 拆分 | Superpowers | GSD / ECC-Mobile | — | skill 承担状态机职责 |
| hooks / gate enforcement | FlowSpec | ECC-Mobile / yoyo-evolve | **ECC**（Hook Profile Gating）+ **claude-reflect**（never-crash）+ **OMC**（Stop block）| Superpowers 式纯 prompt 纪律 |
| validators / scripts | FlowSpec | GSD / ECC-Mobile | — | 把硬规则留在 prompt 里 |
| wrappers / 外部代理 | CCG | ECC-Mobile | — | 早期就上重代理层 |
| fresh context / handoff / resume | PAUL | GSD / yoyo-evolve | — | 依赖对话历史恢复 |
| context isolation | GSD | Superpowers | **Ouroboros**（FilteredContext 隔离模式）| orchestrator 持有全部上下文 |
| 轻量半自动日常迭代 | GSD | 真实场景输入文档 | **Compound Engineering**（ce:work Phase 0 triage）| 直接上 complex/harness ceremony |
| mobile / 分层 DAG 编排 | ECC-Mobile | CCG | — | 默认引入重多模型编排 |
| 进程代理 / 外部模型桥接 | CCG | ECC-Mobile | — | 早期就上复杂多后端代理 |
| 可观测 / event log / checkpoints | FlowSpec | ECC-Mobile / GSD | **ECC**（Strategic Compact pattern）| 无状态、无日志 |
| docs/backflow/knowledge system | Harness engineering 文档 | FlowSpec / Trellis | **claude-reflect**（9 层 memory routing）+ **CE**（compound learning）| 把知识留在聊天里 |
| anti-rationalization / prompt discipline | **PAUL** | — | — | 靠主观自觉、不做结构化检查 |
| ambiguity / stall detection | **Ouroboros** | — | — | 无量化退出条件的无限循环 |
| review pipeline / quality gate | **Compound Engineering** | Superpowers | **ECC**（Santa Method 双盲审查）| 单 agent 自审 |
| self-learning / knowledge compounding | **claude-reflect** | **Compound Engineering** | — | 不记录经验 |

---

## 2. 总体实施原则：先搭 harness，不先堆 prompt

从 [harness-engineering-vs-agent-coding.md](/Users/est8/MyPluginRepo/docs/how-to-explore-a-agent-workflow/harness-engineering-vs-agent-coding.md) 能抽出一个总原则：

1. 先把状态外部化
2. 先把验证外部化
3. 先把约束做成环境机制
4. 再去写 command / prompt / skill

这意味着我们在实施时应优先做：

- 状态文件
- 协议 schema
- gate hooks
- verify / reconcile
- resume / handoff

而不是先做：

- 漂亮的 slash commands
- 大量 skill prompt
- 多模型编排炫技

---

## 3. 路由层怎么实现，参考谁

### 第一参考：GSD

原因：

- 它最强的不是“复杂状态机”，而是**日常开发节奏中的路由与压缩**
- 有 quick path
- 有 context budget
- 有 fresh subagent pattern
- 更接近你半自动真实场景

应该借什么：

- thin orchestrator
- route 之后尽量把执行丢给 fresh worker
- 对小任务压 ceremony
- 明确 anti-pattern 和 context budget

不该照搬什么：

- 大量 markdown workflow 层级
- 过多 agent 种类
- 过强的 solo-developer 风格假设

### 第二参考：FlowSpec

原因：

- 它的评分器、状态机、transition 规则更完整
- 适合做“硬边界”

应该借什么：

- triage 的结构化 scoring
- workflow state DAG
- transition validation

不该照搬什么：

- 把所有事情都拉进完整 workflow ceremony

---

## 4. 状态机和 artifact-gated transition 怎么实现，参考谁

### 第一参考：FlowSpec

这是最适合直接借结构的部分。

应该借：

- 显式 state 列表
- transition 列表
- 输入/输出 artifact 约束
- config/schema 校验

适合我们的实现部位：

- `.workflow/state.json`
- transition table
- gate 校验器
- phase 进入/退出条件

### 第二参考：harness engineering 文档

原因：

- 它给了为什么必须把状态外部化、持久化、版本化的理论支撑

应该借：

- “状态是 repo-local 资产”
- “验证由环境证明，不由 agent 自报”
- “长期运行靠持久资产，不靠上下文记忆”

---

## 5. 微观实现层：agents / commands / skills 应该参考谁

### 5.1 agents 怎么写，参考谁

#### 第一参考：Superpowers

Superpowers 最值得借的不是硬门禁，而是 **agent 职责拆分的清晰度**。

适合借：

- implementer / reviewer / planner 分离
- reviewer 不信任 implementer 自报
- 每类 agent 只承担一种核心责任

这特别适合我们定义：

- orchestrator
- implementer
- spec-reviewer
- quality-reviewer
- verifier

不建议照搬：

- 它大量依赖 prompt discipline
- 不适合把状态推进职责也交给 agent prompt

#### 第二参考：GSD

GSD 适合借：

- completion markers
- agent contract
- agent 输出结构化完成信号

这对我们未来的：

- `## TASK COMPLETE`
- `## VERIFICATION PASSED`
- `## BLOCKED`

这些协议非常有帮助。

#### 第三参考：ECC-Mobile

ECC-Mobile 适合借：

- layer ownership
- 分层 agent 负责不同模块的写入边界

尤其适用于：

- Android / mobile feature builder
- DAG 分层实现

### 5.2 commands 怎么写，参考谁

#### 第一参考：GSD

GSD 最值得借的是：

- command 只是入口
- workflow 才是过程
- agent 才是执行者

这意味着 command 文件应当：

- 轻
- 只负责收集输入、选择 workflow、触发后续步骤
- 不承担真正业务逻辑

#### 第二参考：FlowSpec

FlowSpec 适合借：

- command -> workflow 映射
- command 和状态机转换之间的关系

#### 第三参考：CCG

CCG 适合借：

- 模板化 command
- command 中对多后端调用的桥接姿势

但不建议早期照搬：

- command 里嵌太多模型编排细节

### 5.3 skills 怎么写，参考谁

#### 第一参考：Superpowers

Superpowers 适合借：

- skill discovery
- skill invocation discipline
- skill 作为“知识与方法包”而不是流程状态包

#### 第二参考：GSD

GSD 适合借：

- references / templates / workflows 分层
- skill 不直接承担全部上下文

#### 第三参考：ECC-Mobile

ECC-Mobile 适合借：

- 领域型 skill 组织方式
- 平台技能与流程技能分离

### 5.4 这一层的实施原则

这三类文件最容易写歪，所以要明确：

- **agent** 负责角色职责
- **command** 负责入口
- **skill** 负责知识和纪律

它们都**不应成为状态机真相源**。

---

## 6. Hook 系统与 Hard Guard 怎么实现，参考谁

### 第一参考：FlowSpec

FlowSpec 最适合借的是：

- hooks 的配置结构
- hook runner
- hook timeout
- hook config 安全
- artifact-gated transition 的落点

适合我们的实现部位：

- `SessionStart`
- `PreToolUse`
- `PostToolUse`
- `SubagentStop`
- `Stop`

尤其值得借：

- hook runner 的 fail-safe 模型
- 路径安全
- 配置层 schema

### 第二参考：ECC-Mobile

ECC-Mobile 适合借的是：

- checkpoint hooks
- pre-compact / auto-checkpoint
- session evaluation

这对我们未来的：

- checkpoint
- resume-pack / handoff
- mobile-specific workflow

很有用。

### 第三参考：yoyo-evolve

适合借：

- deny-first permission
- boundary nonce
- hook 超时语义
- checkpoint-restart 思维

不适合整套照搬：

- 它的 shell / hook 体系过于宿主绑定

### 补充：Everything Claude Code (ECC)

[来源: workflow-research-everything-claude-code.md §10]

ECC 最值得借的 hook 机制：

- **Hook Profile Gating**（`run-with-flags.js`）— 通过 `ECC_HOOK_PROFILE` 环境变量实现运行时 hook 开关，无需修改 hooks.json。profile 控制哪些 hook 激活、哪些跳过。
- **Config Protection Hook** — 阻止 agent 修改 linter/formatter 配置（`.eslintrc`, `tsconfig.json` 等）绕过检查。

适合我们的实现部位：Profile 决定 hook 集合，而不是每次都跑全量 hooks。

### 补充：claude-reflect

[来源: workflow-research-claude-reflect.md §10]

- **never-crash hook pattern** — 所有 hook 用 `try/except: sys.exit(0)` 包裹。任何 hook 内部错误都不会阻断主 Claude 进程。这应该成为我们 hook 实现的**基线标准**。
- **hybrid detection engine** — regex 实时检测 + semantic AI 异步验证的双层架构。regex 快但不精确，AI 精确但慢。组合后可同时保证响应速度和准确性。

### 补充：oh-my-claudecode (OMC)

[来源: workflow-research-oh-my-claudecode.md §10]

- **Stop hook 硬阻断** — `persistent-mode.cjs`（1144 行）通过 `{decision: "block"}` 阻止 Claude 结束。这是真正的 hard enforcement：不是提醒，是阻断。
- 但 OMC 的 Stop hook 是单点故障（1144 行 all-in-one），我们应该拆成更小的专责 hooks。

### 明确不建议照搬：Superpowers

原因很简单：

- 它强在 skill discipline
- 不强在 hard enforcement

可以借它的：

- session-start context 注入
- task/reviewer 隔离思路

但不能拿它当 hard gate 的主要参考。

---

## 7. validators / scripts / wrappers 怎么实现，参考谁

### 7.1 validators，第一参考：FlowSpec

FlowSpec 在这块最值得借的是：

- schema validation
- DAG validation
- transition validation
- config validation

这非常适合我们未来实现：

- `tasks.json` validator
- `verify-evidence.json` validator
- `reconcile-settlement.json` validator
- transition legality checker

### 7.2 状态/文件变更脚本，第二参考：GSD

GSD 最值得借的是：

- 不直接随便改状态文件
- 用统一工具做 mutation

虽然我们不一定照搬 `gsd-tools.cjs`，但这个思路应保留：

> 关键状态变更应通过统一 mutator，而不是让任意 prompt 自由写文件。

### 7.3 JSON / checkpoint / session 脚本，第三参考：ECC-Mobile

ECC-Mobile 适合借：

- JSON state lint
- checkpoint scripts
- session evaluation scripts

这对我们将来的：

- `state.json`
- `resume-pack.md` / `handoff.md`
- checkpoint save

非常实用。

### 7.4 wrappers / 外部代理，第四参考：CCG

CCG 的价值不在日常流程，而在：

- backend wrapper
- process proxy
- 多 CLI 后端统一调用

因此它更适合后期参考：

- 当我们真的需要 Codex / Gemini / Claude 多后端隔离执行时

不适合早期就上。

---

## 8. Continuation / Delta / 小需求补丁路由，参考谁

### 第一参考：真实场景输入文档

这部分其实 vendor 框架里没有哪个比你的真实场景更贴合。

直接来源是：
[input-01-real-world-scenario.md](/Users/est8/MyPluginRepo/my-workflow/evolution-archive/input-01-real-world-scenario.md)

应该直接借：

- Baseline / Delta / Effective View 三层模型
- delta 分流重入点
- “补小需求不重跑整套”的判断

### 第二参考：GSD

借它的：

- quick path / compressed ceremony
- context rot 对抗
- continuation 视角下的轻编排

### 第三参考：FlowSpec

借它的：

- state transition 规则

但不要把小补丁也硬塞进完整 workflow 状态图里。

---

## 9. pre-spec 背景对齐怎么实现，参考谁

### 第一参考：真实场景输入文档

因为你的需求最具体。

适合实现成：

- `background-alignment.md`
- Discover 里的显式产物

它应承载：

- 设计稿
- 对照行为
- API 文档
- 团队约定
- 已知坑点

### 第二参考：Harness engineering 文档

借它的：

- repo-local knowledge system
- progressive disclosure
- 让 agent 看到可索引、可消费的前提资料

### 第三参考：Trellis

借它的：

- JSONL-driven context injection 思路

即便我们不直接用 Trellis 的形式，也可以借它“背景资料要可选择性注入”的思想。

---

## 10. fresh context / handoff / resume 怎么实现，参考谁

### 第一参考：PAUL 思路

虽然仓库里目前没有完整的 `workflow-research-paul.md` 研究报告，但从现有 `14`、`15`、`16` 已经确认了我们借 PAUL 的核心点：

- planned-vs-actual reconcile
- handoff
- resume-bootstrap
- slice closure

所以实施时，PAUL 适合作为：

- handoff 结构
- resume 顺序
- closure artifact 设计

### 第二参考：GSD

借它的：

- fresh subagent
- context degradation
- 长任务通过新的 worker 继续

### 第三参考：ECC-Mobile

借它的：

- checkpoint hooks
- phase resume

### 第四参考：yoyo-evolve

借它的：

- checkpoint-restart
- 明确在上下文恶化时中断并恢复

---

## 11. Verification / Review / Quality Gate 怎么实现，参考谁

### 第一参考：ECC-Mobile

在“阶段化验证”和“分层实现之后的检查点”上，它很值得借。

适合借：

- 3-layer checkpoints
- DAG 之后的验证编排
- mobile 场景中的 pass@k

### 第二参考：Trellis

适合借：

- Ralph Loop
- verify-before-success
- SubagentStop 上做 hard evidence 检查

### 第三参考：Superpowers

适合借：

- reviewer 独立性
- implementer / spec reviewer / code reviewer 分离

不适合直接照搬：

- soft discipline 替代 hard evidence

### 第四参考：真实场景输入文档

适合借：

- 轻量质量 gate 的四项检查

这对 `moderate/semi-auto` 比完整 reviewer pipeline 更适合。

---

## 11.5 补充：Review Pipeline / Multi-Agent 审查怎么实现，参考谁

### 第一参考：Compound Engineering

[来源: workflow-research-compound-engineering-plugin.md §6-7]

CE 在 review 上的实现最成熟：

- **28+ tiered persona reviewers**（security-sentinel, architecture-strategist, correctness-reviewer...）
- **confidence gating**：每个 finding 带 confidence score，低于阈值的不进入报告
- **4 级 severity**（P0-P3）+ 4 级 autofix_class（safe_auto, gated_auto, manual, human）
- **headless mode**：skill-to-skill 调用时不交互，返回结构化 JSON

适合我们的实现部位：Phase 4 VERIFY 的 quality-fit 审查。

### 第二参考：ECC (Santa Method)

[来源: workflow-research-everything-claude-code.md §7]

- **Santa Method 双盲独立审查** — 两个 fresh agent 各自独立审查，相同 rubric，互不可见对方结果
- 打破单 agent 自审偏差
- 代价：2-3x token 成本

适合 Complex+ 的高风险审查。

---

## 11.6 补充：Anti-Rationalization / Prompt Discipline 怎么实现，参考谁

### 第一参考：PAUL

[来源: workflow-research-paul.md §5A, §7]

PAUL 是所有 vendor 中 anti-rationalization 做得最深的：

- **evidence-before-claims 表**：每个断言必须先列证据，再给结论
- **Execute/Qualify 三阶段**：`EXECUTE_TASK` → `QUALIFY_RESULT` → `VERIFY_CLAIM`
- **Diagnostic failure routing**：失败分三路——intent（需求理解错了）/ spec（设计有问题）/ code（实现有 bug）
- **"confidence without evidence is the #1 cause of false completion"** — 直接命名 LLM 的核心失败模式

适合注入 Phase 3 EXECUTE 和 Phase 4 VERIFY 的 prompt 中。

---

## 11.7 补充：Ambiguity Gate / Stall Detection 怎么实现，参考谁

### 第一参考：Ouroboros

[来源: workflow-research-ouroboros.md §3, §7]

- **Ambiguity Gate 公式** — 量化需求模糊度（0-1），≤ 0.2 才允许进入执行。可直接移植为 Phase 1 → Phase 2 的前置条件。
- **Stateless Stagnation Detection** — 4 种停滞模式：
  1. 循环重复（相同输出）
  2. 无进展（指标不变）
  3. 漂移过大（偏离目标）
  4. 收敛假阳性（看似收敛但质量不够）

适合所有 revision loop 的退出判断（G5 Build-Fix、G8 Ralph Loop）。

---

## 12. 多模型 / 多 worker / DAG 编排怎么实现，参考谁

### 第一参考：ECC-Mobile

如果你未来要做：

- 分层 DAG
- mobile-specific 多模块 feature builder
- 计划驱动的 agent 分配

ECC-Mobile 是最佳参考。

最值得借：

- plan JSON 驱动 layer agents
- architecture -> network/ui -> data -> wiring 的 DAG 思路
- feature state JSON

### 第二参考：CCG

CCG 适合借的是：

- 外部模型桥接
- process proxy
- 多 backend 隔离执行

但只建议在后期引入。  
原因是：

- 它的过程代理很强
- 但对当前阶段过重
- 会让我们过早掉进“多后端编排工程”

### 建议

当前阶段：

- 借 ECC-Mobile 的 DAG 思路
- 不急着上 CCG 的进程级多后端代理

---

## 13. 可观测 / Event Log / Checkpoint 怎么实现，参考谁

### 第一参考：FlowSpec

借：

- event log
- transition logging
- workflow-level observability

### 第二参考：ECC-Mobile

借：

- checkpoint
- learning summary
- feature state 文件

### 第三参考：GSD

借：

- context monitor
- degradation tier

建议我们实现时采用：

- FlowSpec 式 event log
- GSD 式 context health
- ECC-Mobile 式 checkpoint

---

## 14. Docs / Backflow / Knowledge System 怎么实现，参考谁

### 第一参考：Harness engineering 文档

借：

- repo-local knowledge system
- doc gardening
- 结构化长期资产

### 第二参考：FlowSpec

借：

- memory / decisions / learnings 分层
- research / plan / validate 产物分层

### 第三参考：Trellis

借：

- JSONL 驱动的注入思维

### 第四参考：真实场景 + `14`

借：

- reconcile-settlement 驱动 backflow
- spec transient / settlement durable

---

## 15. 实施顺序建议：先借谁，后借谁

### 第一阶段：核心内核

先参考：

1. FlowSpec
2. Harness engineering 文档
3. 真实场景输入文档

新增：
4. **claude-reflect**（never-crash hook pattern 作为 hook 容错基线）
5. **ECC**（Hook Profile Gating 作为 hook 分层运行基线）

目标：

- 路由层
- 状态机
- schema
- hooks（含容错基线）
- event log

### 第二阶段：贴近日常使用

再参考：

4. GSD
5. Trellis
6. 真实场景输入文档

新增：
7. **Compound Engineering**（scope-aware ceremony + continuation resume）

目标：

- moderate/semi-auto
- continuation
- context monitor
- verify-before-success

### 第三阶段：长任务与复杂任务

再参考：

7. PAUL 思路
8. yoyo-evolve
9. ECC-Mobile

新增：
10. **Ouroboros**（Ambiguity Gate + Stagnation Detection）
11. **PAUL**（anti-rationalization prompt patterns — 此处从"思路"升级为"直接移植"）

目标：

- handoff / resume
- checkpoint
- slice / wave
- DAG 编排
- ambiguity gate（Phase 1→2 前置条件）
- anti-rationalization injection（Phase 3-4）

### 第四阶段：重编排与外部模型

最后才参考：

10. CCG

目标：

- 多后端
- 进程代理
- 真正的多模型 worker runtime

---

## 16. 一个更实用的实施参考矩阵

| 我们要做的部位 | 最先看谁 | 次看谁 | 新增参考（第三看） | 原因 |
|---------------|---------|--------|-------------------|------|
| triage/router | GSD | FlowSpec | **CE**（scope-aware ceremony）| 一个贴日常，一个给硬规则，CE 给三级路由 |
| agents | Superpowers | GSD / ECC-Mobile | **CE**（28+ persona reviewers）| 一个擅长角色拆分，一个擅长完成协议，CE 给 review 角色库 |
| commands | GSD | FlowSpec / CCG | — | 一个擅长入口分层，一个擅长状态映射，一个擅长模板桥接 |
| skills | Superpowers | GSD / ECC-Mobile | — | 一个擅长 skill discipline，一个擅长 references 分层 |
| lane 模板 | 真实场景输入文档 | GSD | **CE**（brainstorm→plan→work 渐进路径）| 你的场景最具体，GSD 最像日常节奏，CE 给渐进 ceremony |
| state.json | FlowSpec | ECC-Mobile | **CCW**（Completion Status Protocol）| 一个强状态机，一个强 JSON state，CCW 给完成状态协议 |
| transition validator | FlowSpec | Harness engineering 文档 | — | 最成熟 |
| hooks runner | FlowSpec | yoyo-evolve | **claude-reflect**（never-crash）+ **ECC**（profile gating）| 一个完整，一个安全性好，两个新增给容错+分层 |
| schema / config validator | FlowSpec | ECC-Mobile | — | 一个最完整，一个对 JSON state 最有经验 |
| mutation scripts | GSD | FlowSpec | — | 一个强调统一 mutator，一个强调 transition legality |
| continuation | 真实场景输入文档 | GSD | **CE**（resume existing work Phase 0.1）| 你的场景是最真实的源头，CE 有成熟实现 |
| background alignment | 真实场景输入文档 | Harness engineering 文档 | — | 属于 repo-local knowledge |
| verify-evidence / reconcile | `14` + PAUL 思路 | Trellis | — | 一个定协议，一个定 hard verify |
| completion markers | GSD | Superpowers | **CCW**（4 状态 + 3-Strike escalation）| 一个定义得最清楚，CCW 给最完整的终止协议 |
| handoff/resume | PAUL 思路 | GSD / yoyo-evolve | — | 一个强调 closure，一个强调 fresh worker |
| quality gate | 真实场景输入文档 | Superpowers / ECC-Mobile | **CE**（tiered persona + confidence gating）| 轻量 gate + reviewer 分离 + CE 给 confidence-based filter |
| mobile DAG | ECC-Mobile | CCG | — | 先 DAG，后重编排 |
| backend wrapper | CCG | ECC-Mobile | — | 一个强代理，一个强 stateful pipeline |
| observability | FlowSpec | ECC-Mobile / GSD | **ECC**（Strategic Compact pattern）| event log + checkpoint + context health + compact |
| anti-rationalization | **PAUL** | — | — | evidence-before-claims + diagnostic failure routing |
| ambiguity / stall | **Ouroboros** | — | — | Ambiguity Gate + Stagnation Detection（4 模式）|
| review pipeline | **CE** | Superpowers | **ECC**（Santa Method）| persona tiering + confidence gating + 双盲审查 |
| self-learning | **claude-reflect** | **CE** | — | hybrid detection + memory routing + compound learning |

---

## 16.5 补充：自学习 / 知识复利怎么实现，参考谁

这是原版 `18` 没有覆盖的全新子系统。新 research 中有两个 vendor 提供了可移植机制：

### 第一参考：claude-reflect

[来源: workflow-research-claude-reflect.md §3-5]

- **Two-Stage Capture + Review**：hooks 自动捕获 correction patterns → queue → 人工 `/reflect` 审查批准 → 写入 durable memory
- **Hybrid Detection Engine**：regex 快速检测 + semantic AI 验证
- **9 层 Memory Routing**：`find_claude_files()` + `suggest_claude_file()` 自动将知识路由到正确的 CLAUDE.md 层级
- **decay_days 声明但未实现** — 提醒我们如果要做知识衰减，必须真正实现消费逻辑

适合我们的 Phase 5 SETTLE backflow：自动检测哪些经验值得沉淀、沉淀到哪里。

### 第二参考：Compound Engineering

[来源: workflow-research-compound-engineering-plugin.md §7-8]

- **ce:compound skill**：专门的知识复利工作流——并行 subagent 收集信息 → orchestrator 整合成 `docs/solutions/` 文档
- **YAML frontmatter searchability**：每个 solution doc 带 `problem_type`、`category`、`tags` 字段，支持后续检索
- **Discoverability Check**：写完 solution doc 后检查 AGENTS.md/CLAUDE.md 是否有指针指向 docs/solutions/，没有就补

适合我们的 lessons.jsonl → durable docs backflow 流程。

### 建议

当前阶段：
- 先借 claude-reflect 的 hook-based capture 思路（Phase 5 自动提取 backflow 候选）
- 再借 CE 的 structured solution doc 模式（backflow 目标格式）
- 不急着上完整的 self-learning loop

---

## 17. 最终裁决

实施时最危险的事，不是“少看几个框架”，而是：

- 看太多，但每个都抄一层表皮

真正正确的做法是：

1. **先按子系统拆实施部位**
2. **每个子系统只选 1 个第一参考、1 个第二参考**
3. **明确哪些值得借，哪些不能照搬**

一句话收束：

> 我们不是要选一个”冠军框架”，而是要组装一套自己的 harness stack：路由借 GSD + CE，状态机借 FlowSpec + CCW，恢复借 PAUL 思路，验证借 Trellis + CE，复杂编排借 ECC-Mobile，hook 容错借 claude-reflect + ECC，anti-rationalization 借 PAUL，ambiguity/stall 借 Ouroboros，知识复利借 claude-reflect + CE，重代理能力最后才看 CCG。  
