# Reference Map — 各机制 ↔ 参考框架引用索引

## 目的

追溯每个设计决策的来源。当需要深入了解某个机制的细节时，直接查对应的研究报告。

---

## 按 Phase 索引

### Phase 0: TRIAGE

| 机制 | 参考框架 | 研究报告位置 | 关键证据 |
|------|---------|-------------|---------|
| 四维复杂度评分 | FlowSpec | `docs/research/workflow-research-flowspec.md` §4 | `flowspec_workflow.yml:182-260` 状态转换 + 复杂度评分 |
| 三级严格度 (light/medium/heavy) → 5 级 profile | FlowSpec | 同上 §2 | `templates/constitutions/` light.md, medium.md, heavy.md |
| 显式命令跳过 (/quick) | GSD | `docs/research/workflow-research-get-shit-done.md` §4.4 | `/gsd-quick` bypass 完整 lifecycle |
| Durable docs 注入 | Trellis | `docs/research/workflow-research-trellis.md` §1 | JSONL-driven Context Injection |
| Boundary nonce 防注入 | yoyo-evolve | `docs/research/workflow-research-yoyo-evolve.md` §8.3 | `evolve.sh:31-33` 随机 nonce |
| Prompt injection scan | GSD | `workflow-research-get-shit-done.md` §5.1 | `scripts/prompt-injection-scan.sh` |

### Phase 1: DISCOVER

| 机制 | 参考框架 | 研究报告位置 | 关键证据 |
|------|---------|-------------|---------|
| 代码理解摘要 + 人类确认 | **真实场景 (原创)** | `my-workflow/真实场景.md` 优化点 1 | Step 6-8, "先审理解，再审方案" |
| 需求澄清问答 | 半自动流程 | `docs/how-to-explore-a-agent-workflow/semi-automatic-agent-development-workflow.md` | Step 3 |
| 代码入口引导 | 真实场景 | `my-workflow/真实场景.md` Phase B Step 5-6 | 最小实现上下文 |
| Research gate (open questions 阻断) | GSD | `workflow-research-get-shit-done.md` §7.1 M3 | `sdk/src/research-gate.ts:92-93` conservative fail |
| 多源研究路由 | code-context | `docs/mcp-orchestration-skill-design.md` | Context7/Exa/DeepWiki 路由策略 |
| Fresh subagent per phase | GSD + yoyo-evolve | `workflow-research-get-shit-done.md` §3.3 + `workflow-research-yoyo-evolve.md` §8.2 | 独立 200k context |
| Context degradation tiers | GSD | `workflow-research-get-shit-done.md` §3.3 | PEAK/GOOD/DEGRADING/POOR |
| context.jsonl (Complex+) | 11-Claude 建议 + 12-Codex 建议 | 进化意见 | worker 上下文边界声明 |

### Phase 2: SPEC & PLAN

| 机制 | 参考框架 | 研究报告位置 | 关键证据 |
|------|---------|-------------|---------|
| Plan 固定 schema (tasks.json) | **真实场景 (原创)** + 12-Codex | `my-workflow/真实场景.md` 优化点 3 | 7 项必填字段 → machine-checkable protocol |
| SDD→BDD→TDD 漏斗 | SDD 实践指南 + 10-Gemini | `spec-driven-development-practice-guide.md` §3 | 按 profile 递减 |
| Plan-checker + revision loop | GSD | `workflow-research-get-shit-done.md` §7.1 M2 | max 3 + stall detection |
| Wave-based parallel decomposition | GSD | `workflow-research-get-shit-done.md` §4.2 | Wave 1/2/3 并行模型 |
| ADR 条件触发 | FlowSpec | `workflow-research-flowspec.md` §5 E2 | 边界分析触发 |
| Sprint contract | Anthropic harness | `anthropic-orchestrated-design-long-running-apps-translation.md` | "冲刺合同" |
| BDD/Gherkin 场景 | SDD 实践指南 | `spec-driven-development-practice-guide.md` §1 | Given/When/Then |
| tasks.json as agent protocol | ECC-Mobile + 12-Codex | `workflow-research-everything-claude-code-mobile.md` §7.2 | Plan JSON → tasks.json schema |
| 测试显式进入流程 | **真实场景 (原创)** | `my-workflow/真实场景.md` 优化点 5 | Plan 标注 verify_cmd |
| Slice 切分判据 | PAUL 框架 | `docs/research/workflow-research-paul.md` | 独立 AC 集合 / 独立模块 / 独立验证 |

### Phase 3: EXECUTE

| 机制 | 参考框架 | 研究报告位置 | 关键证据 |
|------|---------|-------------|---------|
| Delta 三层模型 (Baseline/DeltaLog/EffectiveView) | **真实场景 (原创)** | `my-workflow/真实场景.md` Delta 处理策略 | event sourcing 模型 |
| Delta 分流重入规则 | **真实场景 (原创)** | `my-workflow/真实场景.md` 优化点 2 | 4 类 delta → 4 个重入点 |
| Build-fix loop + stall detection | GSD + yoyo-evolve | `workflow-research-get-shit-done.md` §7.1 M2 + `workflow-research-yoyo-evolve.md` §4.1 | max 10 + 连续相同错误检测 |
| DAG-ordered agents | ECC-Mobile | `workflow-research-everything-claude-code-mobile.md` §7.1 | architecture→network∥ui→data→wiring |
| Worktree 隔离 | Superpowers + FlowSpec | `workflow-research-superpowers.md` §2 + `workflow-research-flowspec.md` §5 E9 | `using-git-worktrees` skill |
| Thin orchestrator | GSD + Trellis | `workflow-research-get-shit-done.md` §7.2 A1 | 四层架构 |
| Orchestrator/Worker 边界 | 11-Claude 建议 | 进化意见 | 行为约束，非进程模型 |
| Scope Guard (allowed_paths) | 11-Claude + 12-Codex | 进化意见 | PostToolUse hook 比对 |
| Anti-Rationalization | 13-Gemini (泛化) | 进化意见 | 通用 EXECUTE 约束，5 条跳步借口封堵 |
| Completion markers | GSD | `workflow-research-get-shit-done.md` §3.2 | `## PLANNING COMPLETE` 等 |
| Checkpoint-restart | yoyo-evolve | `workflow-research-yoyo-evolve.md` §8.2 | 超时 agent 部分进度保存 |
| 脏原型重构 | CCG | `workflow-research-ccg-workflow.md` §8.3 | "将 Codex/Gemini 的 Unified Diff 视为'脏原型'" |
| Protected files + git diff | yoyo-evolve | `workflow-research-yoyo-evolve.md` §6.1 | `evolve.sh:1296-1339` |
| 多模型编排 | CCG | `workflow-research-ccg-workflow.md` §1 | Claude=orchestrator, Codex/Gemini=worker |
| Slice / Handoff | PAUL 框架 | `docs/research/workflow-research-paul.md` | 执行闭包 + 跨 session 恢复 |

### Phase 4: VERIFY

| 机制 | 参考框架 | 研究报告位置 | 关键证据 |
|------|---------|-------------|---------|
| 轻量质量审查 4 类 | **真实场景 (原创)** | `my-workflow/真实场景.md` 优化点 4 | 架构越层/不必要依赖/漏测试/坏味道 |
| Ralph Loop 防逃逸 | Trellis | `workflow-research-trellis.md` §1 | SubagentStop hook + verify-evidence 硬检查 |
| spec-fit / quality-fit 拆分 | 12-Codex 建议 | 进化意见 | 双维独立审查，避免混淆 |
| verify-evidence.json 硬证据 | ECC-Mobile + 12-Codex | 进化意见 | 结构化证据替代自然语言声称 |
| Verification-over-self-report | ECC-Mobile | `workflow-research-everything-claude-code-mobile.md` §8.2 | 编译→审查→统计测试三层验证 |
| 独立 code-review agent | Superpowers | `workflow-research-superpowers.md` §2 | `agents/code-reviewer.md` |
| 双模型并行审查 | CCG | `workflow-research-ccg-workflow.md` §8.2 | Codex 审后端 + Gemini 审前端 |
| GAN evaluator (生成器-评估器分离) | Anthropic harness | `anthropic-orchestrated-design-long-running-apps-translation.md` | 独立评估器 + Playwright 实测 |
| Rubric evaluator | Anthropic harness | 同上 | 设计质量/原创性/工艺/功能性 |
| Receiving-code-review 纪律 | Superpowers | `workflow-research-superpowers.md` | "不盲目接受审查意见" |
| pass@k | ECC-Mobile | `workflow-research-everything-claude-code-mobile.md` §7.3 | 运行 k 次取通过率 |
| 三层检查点 | ECC-Mobile | `workflow-research-everything-claude-code-mobile.md` §7.4 | quick/standard/full |
| Stall Detection | Gate Taxonomy 统一规范 | — | revision loop 连续 2 次相同错误 → escalation |

### Phase 5: SETTLE

| 机制 | 参考框架 | 研究报告位置 | 关键证据 |
|------|---------|-------------|---------|
| reconcile-settlement.json | PAUL 框架 + 真实场景 | `docs/research/workflow-research-paul.md` + `docs/workflow-design-proposal.md` §4.1 | Planned-vs-actual 强制对账 |
| AC Traceability Matrix | 12-Codex 建议 | 进化意见 | AC → Task → Evidence → Result 追踪链 |
| Minimum Closure Contract | 12-Codex + PAUL | 进化意见 | 按 profile 递减的最低闭环要求 |
| DONE_WITH_CONCERNS 状态 | PAUL 框架 | — | AC FAIL + concerns 为空 → 锁定状态 |
| 9 必答问题 | workflow-design-discussion-notes.md §3 | `docs/workflow-design-discussion-notes.md` | 改了什么/行为/接口/架构/决策/验证/风险/回流/继承 |
| Backflow 增量 patch | workflow-design-proposal.md §4.2 | 同上 | api_contract_changes → interfaces.md |
| Spec 归档销毁 | workflow-design-proposal.md §4.2 | 同上 | "永远不会出现在下一次任务的 Context 中" |
| Conventional Commits hook | GSD | `workflow-research-get-shit-done.md` §5.1 | `gsd-validate-commit.sh` exit 2 |
| Event logging | FlowSpec | `workflow-research-flowspec.md` §2 | `.flowspec/` event logging |
| Lessons append-only | yoyo-evolve | `workflow-research-yoyo-evolve.md` §8.1 | `learnings.jsonl` 仅追加 |
| 后续 context 加载 | Trellis | `workflow-research-trellis.md` §1 | JSONL-driven injection |
| Transient/Decision/Durable 分层 | discussion-notes + proposal | `docs/workflow-design-discussion-notes.md` | 三层文档模型 |

### Cross-Cutting

| 机制 | 参考框架 | 研究报告位置 | 关键证据 |
|------|---------|-------------|---------|
| Gate Taxonomy (4 类统一失败路由) | GSD | `workflow-research-get-shit-done.md` §9 | preflight/revision/escalation/abort |
| State mutation boundary (hook) | GSD (CLI 降级版) | `workflow-research-get-shit-done.md` §7.1 M1 | `gsd-tools.cjs` 确定性操作 |
| Context window monitor | GSD | `workflow-research-get-shit-done.md` §7.1 M4 | `gsd-context-monitor.js` bridge file |
| StatusLine hook | Trellis | `workflow-research-trellis.md` §1 | `statusline.py` |
| Resume-Bootstrap (固定加载顺序) | PAUL + OpenSpec + ECC-Mobile | `docs/research/workflow-research-paul.md` | 不依赖对话历史的确定性恢复 |
| Handoff protocol | PAUL 框架 | `docs/research/workflow-research-paul.md` | 跨 session 恢复载体 |
| Hook 超时 (5s) | yoyo-evolve | `workflow-research-yoyo-evolve.md` §8.4 | `hooks.rs:196` Duration::from_secs(5) |
| Hook 路径安全 | FlowSpec | `workflow-research-flowspec.md` §5 E12 | `config.py` 阻止 `..` 和绝对路径 |
| Deny-first permission | yoyo-evolve | `workflow-research-yoyo-evolve.md` §6.1 | `config.rs:18-33` deny-first |
| Config-driven toggle | GSD | `workflow-research-get-shit-done.md` §7.2 A4 | `absent=enabled` + config.json |
| AC → Task → Evidence → Reconcile 主链 | 12-Codex + PAUL | 进化意见 | 核心 machine-checkable 追踪链 |
| Completion Markers | GSD | `workflow-research-get-shit-done.md` §3.2 | 结构化输出标记 |

---

## 原创机制索引

以下机制来自真实场景、讨论或进化裁决，不源于任何 vendor 框架：

| 机制 | 来源文档 | Phase |
|------|---------|-------|
| 代码理解摘要 + 人类确认理解 | `真实场景.md` 优化点 1 | P1 |
| Delta 三层模型 (Baseline/DeltaLog/EffectiveView) | `真实场景.md` Delta 处理策略 | P3 |
| Delta 分流重入 (4 类 → 4 重入点) | `真实场景.md` 优化点 2 | P3-P4 |
| Plan 固定 schema → tasks.json protocol | `真实场景.md` 优化点 3 + 进化裁决 | P2 |
| 轻量质量审查 4 类 | `真实场景.md` 优化点 4 | P4 |
| 测试显式进入 Plan (verify_cmd) | `真实场景.md` 优化点 5 | P2 |
| Spec=transient, Acceptance=durable | `discussion-notes.md` + `review-brief.md` | P5 |
| 9 必答 settlement 问题 | `discussion-notes.md` §3 | P5 |
| 先冻结骨架，profile 只做减法 | `review-brief.md` §设计前提 | 全局 |
| spec-fit / quality-fit 双维审查 | 12-Codex 建议 (进化裁决) | P4 |
| AC → Task → Evidence → Reconcile 主链 | 12-Codex + PAUL (进化裁决) | 全局 |
| Minimum Closure Contract (按 profile 递减) | 12-Codex + PAUL (进化裁决) | P5 |
| Scope Guard (allowed_paths) | 11-Claude + 12-Codex (进化裁决) | P3 |
| Orchestrator/Worker 边界 | 11-Claude (进化裁决) | P3 |

---

## 研究报告清单（快速跳转）

| 框架 | 报告路径 | 关键贡献 |
|------|---------|---------|
| Superpowers | `docs/research/workflow-research-superpowers.md` | Implicit routing, TDD, worktree, code-review agent |
| GSD | `docs/research/workflow-research-get-shit-done.md` | 四种 gate, gsd-tools, config-driven, context monitor, research gate |
| CCG | `docs/research/workflow-research-ccg-workflow.md` | 多模型编排, 脏原型重构, codeagent-wrapper |
| FlowSpec | `docs/research/workflow-research-flowspec.md` | 复杂度评分, ADR, 状态机 DAG, 三级严格度 |
| Trellis | `docs/research/workflow-research-trellis.md` | JSONL injection, ralph loop, pure dispatcher |
| Specs Generator | `docs/research/workflow-research-claude-code-specs-generator.md` | 6 文档模型 (rejected), CLAUDE.md top-of-file |
| yoyo-evolve | `docs/research/workflow-research-yoyo-evolve.md` | 两层记忆, boundary nonce, protected files, checkpoint-restart |
| ECC-Mobile | `docs/research/workflow-research-everything-claude-code-mobile.md` | DAG agents, plan JSON, pass@k, 三层检查点, instinct |
| PAUL | `docs/research/workflow-research-paul.md` | Planned-vs-actual reconcile, slice/handoff, execution closure |
| Anthropic harness | `docs/how-to-explore-a-agent-workflow/anthropic-orchestrated-design-long-running-apps-translation.md` | GAN evaluator, sprint contract, context reset |
| 半自动流程 | `docs/how-to-explore-a-agent-workflow/semi-automatic-agent-development-workflow.md` | 15 步流程基础 |
| SDD 实践指南 | `docs/how-to-explore-a-agent-workflow/spec-driven-development-practice-guide.md` | BDD/Gherkin, spec-first |
| TDD/BDD/SDD | `docs/how-to-explore-a-agent-workflow/tdd-bdd-sdd-in-agent-era.md` | SDD定边界→BDD定行为→TDD定实现 |
| Harness vs Agent | `docs/how-to-explore-a-agent-workflow/harness-engineering-vs-agent-coding.md` | Harness engineering 定义 |
| 执行 vs 治理对比 | `docs/how-to-explore-a-agent-workflow/execution-vs-governance-workflow-comparison.md` | Superpowers/OpenSpec/OMC 对比 |
