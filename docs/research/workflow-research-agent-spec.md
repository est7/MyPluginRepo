# Workflow Research: agent-spec

**Date**: 2026-04-13
**Source**: `/Users/est8/MyPluginRepo/vendor/agent-spec`
**Analyst mode**: Single
**Focus**: All

---

## 1. Framework Profile

| Attribute | Value |
|-----------|-------|
| **Type** | hybrid — spec-driven workflow + verification CLI |
| **Total files** | 107（Phase 0 quick scan: `find vendor/agent-spec -type f | wc -l`） |
| **Prompt files** | 4（`README.md`, `AGENTS.md`, `skills/agent-spec-authoring/SKILL.md`, `skills/agent-spec-estimate/SKILL.md`, `skills/agent-spec-tool-first/SKILL.md`；严格按 workflow surface 计主要 prompt 文件为 5） |
| **Scripts/hooks** | 4（`install-skills.sh`, `.github/workflows/contract-guard.yml`, `.github/workflows/contract-guard-minimal.yml`, `.github/workflows/static.yml`） |
| **Test files** | 0 standalone test files；测试嵌在 Rust source `#[cfg(test)]` blocks 中（如 `src/spec_verify/boundaries.rs:271`, `src/spec_verify/test_verifier.rs:271`, `src/vcs.rs:138`） |
| **Entry points** | `README.md`, `AGENTS.md`, `Cargo.toml`, `src/main.rs`, `skills/*/SKILL.md`, `specs/project.spec.md` |
| **Registration mechanism** | CLI subcommands are registered in `src/main.rs:36-245`; Claude/Codex workflow surfaces are registered by presence of `skills/*/SKILL.md` and `AGENTS.md` (`README.md:103-155`, `AGENTS.md:1-4`) |
| **Language** | Rust + Markdown + GitHub Actions YAML |

### Directory Map

```text
vendor/agent-spec/
├── README.md                              # canonical workflow + CLI claims
├── AGENTS.md                              # Codex/OpenAI-agent mirror of the workflow
├── Cargo.toml                             # Rust package manifest, binary metadata
├── install-skills.sh                      # installs CLI + Claude skills
├── .github/workflows/
│   ├── contract-guard.yml                 # full CI enforcement
│   ├── contract-guard-minimal.yml         # minimal CI enforcement
│   └── static.yml                         # Pages deploy only
├── skills/
│   ├── agent-spec-authoring/              # authoring prompt surface
│   ├── agent-spec-estimate/               # estimation prompt surface
│   └── agent-spec-tool-first/             # implementation/verification prompt surface
├── specs/
│   ├── project.spec.md                    # project-level inherited constraints
│   ├── task-*.spec.md                     # self-hosting active task contracts
│   └── roadmap/README.md                  # staged roadmap contracts excluded from default guard
├── examples/                              # reference contracts, not runtime inputs
├── docs/                                  # user-facing docs, GitHub Pages content
└── src/
    ├── main.rs                            # command dispatcher + operational pipeline
    ├── spec_core/ast.rs                   # core entity schema
    ├── spec_parser/resolver.rs            # inheritance resolution
    ├── spec_gateway/lifecycle.rs          # SpecGateway: lint/verify/decision/report bridge
    ├── spec_gateway/plan.rs               # plan context construction
    ├── spec_lint/pipeline.rs              # lint stack registration
    ├── spec_verify/test_verifier.rs       # selector-bound cargo test execution
    ├── spec_verify/boundaries.rs          # path boundary enforcement
    ├── spec_verify/ai_verifier.rs         # stub/external AI verifier layer
    ├── spec_report/mod.rs                 # explain/status/report formatting
    └── vcs.rs                             # git/jj detection and history context
```

---

## 2. Source Inventory

### Overview Sources
| File | Type | Why It Matters |
|------|------|---------------|
| `vendor/agent-spec/README.md` | README | 定义公开工作流、CLI 语义、AI verifier 范围与当前能力边界（`README.md:8-16`, `README.md:157-234`, `README.md:300-405`） |
| `vendor/agent-spec/AGENTS.md` | agent guidance | 为不加载 Claude skills 的 agent 提供等价流程镜像，暴露 repo 作者希望 agent 遵循的“七步流程”（`AGENTS.md:33-55`） |
| `vendor/agent-spec/Cargo.toml` | manifest | 标识框架本体是 Rust CLI binary，不是 plugin-only prompt pack（`Cargo.toml:0-22`） |
| `vendor/agent-spec/specs/project.spec.md` | inherited project contract | 把 README 里的理念转成项目级硬/软约束，是 self-hosting 的“元规则来源”（`specs/project.spec.md:10-29`） |
| `vendor/agent-spec/specs/roadmap/README.md` | roadmap policy | 说明 roadmap contract 的 staging 策略与默认 guard 范围（`specs/roadmap/README.md:2-13`） |

### Execution Sources
| File | Type | Why It Matters |
|------|------|---------------|
| `vendor/agent-spec/src/main.rs` | CLI dispatcher | 注册所有命令并定义 `lifecycle` / `guard` / `install-hooks` / `explain` / `plan` / `resolve-ai` 的执行路径（`src/main.rs:36-245`, `src/main.rs:491-721`, `src/main.rs:907-985`, `src/main.rs:1267-1353`, `src/main.rs:1633-1684`, `src/main.rs:2286-2361`） |
| `vendor/agent-spec/src/spec_gateway/lifecycle.rs` | gateway | 把 lint、verify、decision、report 封装为统一门面，是真正的 stage bridge（`src/spec_gateway/lifecycle.rs:16-27`, `src/spec_gateway/lifecycle.rs:62-80`, `src/spec_gateway/lifecycle.rs:196-217`, `src/spec_gateway/lifecycle.rs:221-245`） |
| `vendor/agent-spec/src/spec_gateway/plan.rs` | planner | 构造 `Contract + CodebaseContext + TaskSketch` 三块计划上下文，显示框架如何把 spec 变成实现提示（`src/spec_gateway/plan.rs:9-17`, `src/spec_gateway/plan.rs:71-95`） |
| `vendor/agent-spec/install-skills.sh` | installer | 把 CLI 与三个 skills 一起安装，说明作者把 prompt surface 当作一等配套物（`README.md:120-143` 引用该脚本） |
| `vendor/agent-spec/.github/workflows/contract-guard.yml` | CI workflow | 把 `guard` / `lifecycle` / `explain` 接入 PR gate，是 repo 外层强制机制（`.github/workflows/contract-guard.yml:14-27`, `.github/workflows/contract-guard.yml:53-102`, `.github/workflows/contract-guard.yml:104-213`） |
| `vendor/agent-spec/.github/workflows/contract-guard-minimal.yml` | CI workflow | 最小版 gate，证明完整 workflow 不是唯一部署形态（`.github/workflows/contract-guard-minimal.yml:7-54`） |

### Prompt Sources
| File | Type | Why It Matters |
|------|------|---------------|
| `vendor/agent-spec/skills/agent-spec-tool-first/SKILL.md` | prompt / implementation | 定义 tool-first 主路径、七步流程、retry protocol、evidence rule（`skills/agent-spec-tool-first/SKILL.md:74-118`, `...:145-198`, `...:200-241`） |
| `vendor/agent-spec/skills/agent-spec-authoring/SKILL.md` | prompt / authoring | 定义 contract 编写规则、authoring self-check、observable behavior coverage（`skills/agent-spec-authoring/SKILL.md:58-64`, `...:77-90`, `...:91-129`, `...:208-219`） |
| `vendor/agent-spec/skills/agent-spec-estimate/SKILL.md` | prompt / planning | 定义从 Task Contract 估算 rounds 的方法，体现 `plan` 输出的第二用途（`skills/agent-spec-estimate/SKILL.md:41-80`, `...:81-126`, `...:141-176`） |
| `vendor/agent-spec/skills/agent-spec-tool-first/references/commands.md` | command reference | 给 tool-first 提供所有 CLI 旗标与默认值，是 prompt → command 的桥梁（由 prompt-explorer 读取；主 README 同步这些命令于 `README.md:368-386`） |
| `vendor/agent-spec/skills/agent-spec-authoring/references/patterns.md` | authoring reference | 明确 authoring 兼容性边界与 syntax discipline（由 prompt-explorer 读取；SKILL.md 明确要求先读它：`skills/agent-spec-authoring/SKILL.md:67-75`） |
| `vendor/agent-spec/AGENTS.md` | prompt / cross-platform mirror | 在没有 Claude skill runtime 时保留同样的行为模型（`AGENTS.md:1-4`, `AGENTS.md:33-76`, `AGENTS.md:185-207`） |

### Enforcement Sources
| File | Type | Why It Matters |
|------|------|---------------|
| `vendor/agent-spec/src/spec_lint/pipeline.rs` | validator | 注册 21 个内建 linters，说明 spec 质量并不是一句 prompt，而是可计算的 lint stack（`src/spec_lint/pipeline.rs:20-47`） |
| `vendor/agent-spec/src/spec_verify/boundaries.rs` | verifier | 对路径边界做机械检查，是真正的 hard enforcement（`src/spec_verify/boundaries.rs:8-24`, `...:36-104`） |
| `vendor/agent-spec/src/spec_verify/test_verifier.rs` | verifier | 把场景与 `cargo test` 绑定，并以 exit status 决定 verdict（`src/spec_verify/test_verifier.rs:32-74`, `...:96-123`, `...:172-199`） |
| `vendor/agent-spec/src/spec_verify/ai_verifier.rs` | verifier | 明确 AI 层当前只是 stub/external backend 容器，不是自动成功器（`src/spec_verify/ai_verifier.rs:8-16`, `...:18-45`, `...:66-99`） |
| `vendor/agent-spec/src/main.rs` | hook/guard logic | `cmd_lifecycle`, `cmd_guard`, `cmd_install_hooks`, `cmd_resolve_ai` 把 prompt 宣称变成具体错误码和落盘协议（`src/main.rs:491-721`, `...:907-985`, `...:1633-1684`, `...:2286-2361`） |
| `vendor/agent-spec/.github/workflows/contract-guard.yml` | CI | PR 层面的硬门禁和 comment/report 集成（`.github/workflows/contract-guard.yml:87-102`, `...:172-213`） |

### Evolution Evidence
| Source | Type | Why It Matters |
|--------|------|---------------|
| `vendor/agent-spec/specs/task-add-ai-verifier-skeleton.spec.md` | self-hosting spec | 证明 AI verifier 是增量引入的，而不是天然内置完成品（README 也承认 `no real model provider is wired in yet`: `README.md:319-338`） |
| `vendor/agent-spec/specs/task-phase1-contract-review-loop.spec.md` | self-hosting spec | 表明 `explain` / contract acceptance 是 roadmap 中明确建模过的能力，而不是 README 临时包装（README 对 phase sequence 也有呼应：`README.md:218-226`, `README.md:441-449`） |
| `vendor/agent-spec/specs/task-phase2-run-history-and-vcs-context.spec.md` | self-hosting spec | 对应 run log / checkpoint / VCS history 的实现（`src/main.rs:686-715`, `src/main.rs:1408-1629`, `src/vcs.rs:23-31`） |
| `vendor/agent-spec/specs/roadmap/README.md` | staged roadmap policy | 清楚区分 active contracts 与 future contracts（`specs/roadmap/README.md:2-13`） |
| `vendor/agent-spec/examples/README.md` | example curation | 把 examples 定位为 authoring reference，而不是运行时真实输入（`examples/README.md:2-14`） |
| `vendor/agent-spec/.github/workflows/static.yml` | deployment workflow | 说明 `docs/` GitHub Pages 是文档发布层，不是 enforcement 层（`.github/workflows/static.yml:23-42`） |

---

## 3. Object Model

### First-Class Entities

| Entity | Definition Location | Required Fields | Lifecycle | Fact/Judgment/Evidence |
|--------|-------------------|-----------------|-----------|----------------------|
| `SpecDocument` | `src/spec_core/ast.rs:36-43` | `meta`, `sections`, `source_path` | parse from disk/string → resolve inheritance → feed gateway (`src/spec_gateway/lifecycle.rs:23-35`) | fact object |
| `SpecMeta` | `src/spec_core/ast.rs:20-34` | `level`, `name`; optional `inherits`, `lang`, `tags`, `depends`, `estimate` | authored in frontmatter → parsed → used for inheritance/plan/report | fact object |
| `ResolvedSpec` | `src/spec_core/ast.rs:283-290` | `task`, `inherited_constraints`, `inherited_decisions`, `all_scenarios` | `resolve_spec` builds it from inheritance chain (`src/spec_parser/resolver.rs:8-53`) → carried through gateway | fact object |
| `Scenario` | `src/spec_core/ast.rs:145-160` | `name`, `steps`, `tags`, `review`, `mode`, `depends_on`, `span`; optional `test_selector` | authored in Completion Criteria → parsed → verified → summarized (`src/spec_verify/test_verifier.rs:40-123`) | fact object |
| `TestSelector` | `src/spec_core/ast.rs:199-229` | `filter`; optional `package`, `level`, `test_double`, `targets` | authored in spec → resolved into cargo args (`src/spec_verify/test_verifier.rs:191-199`) → evidence label | fact/evidence bridge |
| `TaskContract` | `src/spec_gateway/mod.rs:5-7` and gateway use in `src/spec_gateway/lifecycle.rs:44-50` | derived contract fields (`name`, `intent`, `must`, `must_not`, `decisions`, `allowed_changes`, `forbidden`, `out_of_scope`) | resolved spec → contract render (`contract`) / plan / explain / stamp | judgment object |
| `VerificationContext` | consumed in verifiers (`src/spec_gateway/lifecycle.rs:203-208`) | `code_paths`, `change_paths`, `ai_mode`, `resolved_spec` | created by gateway → passed to verifiers → discarded after report | fact object |
| `VerificationReport` | summary usage in `src/spec_gateway/lifecycle.rs:221-350`, `src/spec_report/mod.rs:30-110` | results + summary counts | produced by `run_verification` (`src/spec_gateway/lifecycle.rs:210-217`) → checked by `is_passing` / `gate_status` / formatting | evidence object |
| `PlanContext` | `src/spec_gateway/plan.rs:9-17` | `contract`, `codebase_context`, `task_sketch`, `warnings` | `plan` command builds it from resolved spec + code scan (`src/spec_gateway/plan.rs:71-95`) → rendered to text/json/prompt (`src/main.rs:2361+`) | fact+judgment object |
| `StatusReport` | `src/spec_report/mod.rs:14-24` | `spec`, `outcome`, `gate_blocked`, `scenarios`, `context_updates`, `timestamp`, `notes` | derived from verification report (`src/spec_report/mod.rs:30-110`) → intended for CI/agent consumption | evidence object |
| `AiRequest` / `AiDecision` | consumed/built in `src/spec_verify/ai_verifier.rs:13-16`, `src/spec_verify/ai_verifier.rs:102-161` | scenario name, contract context, code/change paths / verdict, confidence, reasoning | skipped/uncovered scenario → AI request → stub/external decision → merged into report | judgment/evidence object |
| `RunLogEntry` / `Checkpoint` | `src/main.rs:1408-1504` | spec name, passing, summary, timestamp, optional vcs / scenario verdict map | lifecycle pass/fail → write run log + checkpoint → explain/history / resume consume | evidence object |

### Entity Relationships

```text
SpecDocument
  └─(resolve inheritance)→ ResolvedSpec
       ├─→ TaskContract
       │    ├─→ contract output
       │    ├─→ explain input
       │    └─→ plan context
       ├─→ Scenario[*]
       │    ├─→ TestSelector? ─→ cargo test args
       │    ├─→ dependency graph ─→ TaskSketch / dependency skip
       │    └─→ AiRequest when caller/stub flow needs non-mechanical judgment
       └─→ VerificationContext
             └─→ Verifiers[structural, boundaries, test, ai, complexity]
                    └─→ VerificationReport
                          ├─→ StatusReport
                          ├─→ Explain markdown/text
                          ├─→ Stamp trailers
                          └─→ RunLogEntry / Checkpoint
```

### Context Isolation Strategy

| Scope | What Flows | Mechanism | Evidence |
|-------|-----------|-----------|----------|
| Author → Implementer | `TaskContract` + allowed paths + test selectors + code scan | `contract` / `plan` render contract and codebase context instead of relying on chat memory | `README.md:157-189`, `src/spec_gateway/plan.rs:71-95` |
| Implementer → Verifier | code path, change set, AI mode, resolved spec | `VerificationContext` injected into verifier chain | `src/spec_gateway/lifecycle.rs:196-217` |
| Verifier → Reviewer | summarized report, not raw diff | `explain` builds `ExplainInput` + `VerificationReport` and formats it for human review | `src/main.rs:1267-1305`, `README.md:218-226` |
| Cross-run persistence | pass/fail history, VCS ref, checkpoint verdicts | `.agent-spec/runs/*.json` + `.agent-spec/checkpoint.json` | `src/main.rs:686-715`, `src/main.rs:1418-1504` |
| VCS-aware context | git short hash or jj change/op ids | `vcs.rs` auto-detects Git/JJ and stores refs in run logs | `src/vcs.rs:35-57`, `src/vcs.rs:59-102` |
| Compression/lost context fallback | explicit file-backed contract + run logs + checkpoint | framework writes state to disk instead of assuming conversation continuity | `src/main.rs:1294-1302`, `src/main.rs:1418-1504`, `README.md:183-189` |

这个框架没有 controller / implementer / reviewer 的多 agent 隔离模型。它的 isolation strategy 不是“多上下文并行”，而是“把关键上下文转为文件和 CLI 输出，再让任何 agent 重新加载”。这一点更像 protocol，而不像 orchestrator。

---

## 4. Flow & State Machine

### Happy Path

1. 编写 Task Contract：`init` 生成 `.spec.md`，用户填充 `Intent / Decisions / Boundaries / Completion Criteria` —— `README.md:87-99`, `AGENTS.md:35-41`, `src/main.rs:77-91`, `src/main.rs:1689-1725`
2. 质量门禁：`lint` 对 spec 运行 linter stack，不满足 `min_score` 或有 error 就终止 —— `README.md:191-208`, `AGENTS.md:36-39`, `src/spec_gateway/lifecycle.rs:69-80`, `src/main.rs:544-563`
3. 合约渲染：`contract` 把 `ResolvedSpec` 投影成 `TaskContract`，给 agent 明确实现目标 —— `README.md:169-190`, `src/spec_gateway/lifecycle.rs:42-56`, `src/main.rs:898-902`
4. 计划生成：`plan` 在 Allowed Changes 范围内扫描代码，生成 `Contract + CodebaseContext + TaskSketch` —— `README.md:177-189`, `src/spec_gateway/plan.rs:71-95`
5. 实现后执行 `lifecycle`：先 lint，再 verify，再输出结构化报告；如果启用 run log，还会持久化历史和 checkpoint —— `src/main.rs:491-721`
6. 仓库级 gate：`guard` 扫描 `specs/` 下所有活跃 spec，对当前 change set 做统一 lint + verify 检查 —— `README.md:210-216`, `src/main.rs:907-985`
7. 人类验收：`explain` 生成 reviewer-friendly summary，替代 line-by-line code review —— `README.md:218-226`, `src/main.rs:1267-1305`
8. Traceability：`stamp --dry-run` 生成 `Spec-Name`, `Spec-Passing`, `Spec-Summary`, 可选 `Spec-Change` trailer —— `README.md:228-234`, `src/main.rs:1310-1353`

### Phase Transitions

| From | To | Trigger | Gate? | Evidence |
|------|----|---------|-------|----------|
| `Authoring` | `Linted contract` | `agent-spec lint <spec> --min-score ...` passes | Yes | `AGENTS.md:35-37`, `src/spec_gateway/lifecycle.rs:69-80` |
| `Linted contract` | `Executable contract` | `contract` / `plan` called on resolved spec | No | `src/spec_gateway/lifecycle.rs:44-50`, `src/spec_gateway/plan.rs:71-95` |
| `Executable contract` | `Verified report` | `lifecycle` or `verify` runs verifier chain | Yes | `src/spec_gateway/lifecycle.rs:196-217`, `src/main.rs:569-590` |
| `Verified report` | `Passing` | `failed == 0 && skipped == 0 && uncertain == 0`（strict mode 还要求 `pending_review == 0`） | Yes | `src/spec_gateway/lifecycle.rs:229-245` |
| `Passing/Failing report` | `Persisted history` | `--run-log-dir` set in lifecycle | No, but durable | `src/main.rs:686-715`, `src/main.rs:1418-1504` |
| `Verified report` | `Reviewer summary` | `explain` formats `ExplainInput + report` | No | `src/main.rs:1267-1292`, `src/spec_report/mod.rs:139-152` |
| `Skipped scenarios in caller mode` | `AI pending` | `lifecycle --ai-mode caller` sees skipped results | Yes | `src/main.rs:607-645` |
| `AI decisions file` | `Merged report` | `resolve-ai --decisions` merges external decisions | Yes | `src/main.rs:2286-2361` |
| `Roadmap contract` | `Active contract` | file moved from `specs/roadmap/` to top-level `specs/` | Yes, by inclusion in default guard scope | `specs/roadmap/README.md:2-13` |

### Failure Paths

#### Failure Path 1: Lint gate rejection
当 spec 存在解析错误、lint error 或质量分低于阈值时，`lifecycle` 在 Stage 1 直接输出 failure payload 并返回错误，不进入 verify 阶段（`src/main.rs:544-563`）。这意味着“代码已经写完，但 spec 质量不过关”也会被 pipeline 拒绝。README 也明确写出 lifecycle fails if lint emits error or score below threshold（`README.md:203-208`）。

#### Failure Path 2: `skip` 不是通过
`TestVerifier` 找不到 selector 或不运行测试时不会给 `pass`；`is_passing` 明确要求 `skipped == 0` 且 `uncertain == 0` 才能通过（`src/spec_gateway/lifecycle.rs:234-245`）。`AGENTS.md:45-55` 和 `README.md:238-261` 都把 `skip` 当成需要修复的状态，而不是“先放行”。

#### Failure Path 3: 边界越界
`BoundariesVerifier` 对每个 change path 做 allow/forbid 匹配；命中 forbidden 或没被任何 allowed 覆盖时生成 `Fail` verdict（`src/spec_verify/boundaries.rs:36-84`）。`guard` 与 `lifecycle` 都会把这个 non-pass 算进最终失败（`src/main.rs:717-721`, `src/main.rs:958-983`）。

#### Failure Path 4: AI caller mode unfinished
当 `--ai-mode caller` 且 skipped 场景存在时，`lifecycle` 不会偷偷给出通过，而是把 `AiRequest` 写入 `.agent-spec/pending-ai-requests.json` 并设置 `ai_pending`（`src/main.rs:607-660`）。如果宿主 agent 不继续执行 `resolve-ai`，这个状态就停在“需要外部判断”。

#### Failure Path 5: Hook 安装存在 repo-shape 假设
`install-hooks` 写死 `agent-spec guard --spec-dir specs --code src --min-score 0.6`（`src/main.rs:1647-1649`）。如果目标项目不是 `src/` 目录布局，这个自动安装的 hook 仍然会执行，但代码路径假设可能不合适。这是一个 implementation-coupled default，而不是 repo-agnostic installer。

### Parallelism

| Parallel Unit | What Runs | Synchronization | Evidence |
|--------------|-----------|-----------------|----------|
| None in core runtime | verifier chain is sequential: structural → boundaries → test → ai → complexity | single `run_verification` pipeline | `src/spec_gateway/lifecycle.rs:210-217` |
| CI jobs | `rust-checks` and `contract-guard` run as separate GitHub Actions jobs | GitHub Actions job graph; both run independently inside same workflow | `.github/workflows/contract-guard.yml:36-55` |
| Scenario grouping in planning | `TaskSketch` groups scenarios by topological order for potential sequencing, not actual parallel execution | grouped by dependency order; no executor attached | `src/spec_gateway/plan.rs:40-53`, `README.md:183-189` |

这不是 orchestration framework，所以不存在 controller fan-out、reviewer 并发、worktree wave 等机制。它只在 `plan` 层提供“可以并行实现”的信息，但自己不调度。

---

## 5. Enforcement Audit

### Enforcement Matrix

| # | Constraint | Source | Level | Evidence | Gap? |
|---|-----------|--------|-------|----------|------|
| 1 | Spec lint score must pass before implementation/verification | `README.md:191-208`, `AGENTS.md:36-37` | Hard | `quality_gate` rejects on errors or low score (`src/spec_gateway/lifecycle.rs:69-80`); `cmd_lifecycle` exits early (`src/main.rs:544-563`) | No |
| 2 | Changed files must stay within `Allowed Changes` / `Forbidden` paths | `README.md:263-299`, `skills/agent-spec-authoring/SKILL.md:208-213` | Hard | `BoundariesVerifier` mechanically matches paths and fails on violations (`src/spec_verify/boundaries.rs:36-104`) | No |
| 3 | Bound scenarios should execute real tests via explicit selectors | `README.md:236-261`, `examples/README.md:13-14` | Hard for execution, Soft for authoring completeness | `TestVerifier` converts selectors to `cargo test` and verdicts by exit code (`src/spec_verify/test_verifier.rs:46-74`, `...:191-199`); but missing explicit selector can still fall back to legacy `@spec` comments (`src/spec_verify/test_verifier.rs:172-189`) | Yes — explicit-only policy still has compatibility escape hatch |
| 4 | `skip` != `pass` | `AGENTS.md:65`, `specs/project.spec.md:16,31` | Hard | `is_passing` requires skipped=0 (`src/spec_gateway/lifecycle.rs:234-245`); lifecycle/guard both fail non-passing summary (`src/main.rs:717-721`, `src/main.rs:961-983`) | No |
| 5 | `uncertain` must block success | `README.md:203-208`, `specs/project.spec.md:16,22` | Hard | `is_passing` requires uncertain=0 (`src/spec_gateway/lifecycle.rs:234-245`) | No |
| 6 | AI verifier should not silently claim success when no real backend exists | `README.md:319-338` | Hard | `StubAiBackend` always returns `Verdict::Uncertain` with manual-review-required reasoning (`src/spec_verify/ai_verifier.rs:18-35`) | No |
| 7 | `guard` should verify all active specs against current change set | `README.md:210-216`, `specs/roadmap/README.md:2-13` | Hard | `cmd_guard` scans only top-level `specs/` files and checks each (`src/main.rs:914-983`); roadmap specs excluded unless promoted | No |
| 8 | Pre-commit should block bad specs/changes | `README.md:435`, `contract-guard.yml:87-102` | Hard when hook/CI installed | `cmd_install_hooks` writes pre-commit hook invoking guard (`src/main.rs:1633-1684`); GitHub Actions exits non-zero on failed guard (`.github/workflows/contract-guard.yml:87-102`, `...:208-213`) | Yes — local enforcement only exists after explicit install |
| 9 | Humans should review Contract Acceptance instead of diffs | `README.md:218-226`, `skills/agent-spec-tool-first/SKILL.md:212-241` | Soft | `cmd_explain` only formats current report; nothing prevents a team from skipping it (`src/main.rs:1267-1305`) | Yes |
| 10 | After 3 consecutive failures on same scenario, escalate to human | `AGENTS.md:54`, `skills/agent-spec-tool-first/SKILL.md:173-186` | Soft | Prompt instruction only; no retry counter or auto-stop in code | Yes |
| 11 | Do not modify spec to make code pass | `AGENTS.md:52`, `skills/agent-spec-tool-first/SKILL.md:182-186` | Soft | No code-level diff provenance check between failing lifecycle runs and spec edits | Yes |
| 12 | Public CLI / gateway behavior must have regression tests | `specs/project.spec.md:14-15` | Soft-to-Hard inside self-hosting, not universal | Self-hosting spec encodes this as project rule, but enforcement depends on tests existing and being bound; no generic public-API coverage checker beyond selected tests | Yes |
| 13 | Roadmap specs must stay out of default guard until promoted | `specs/project.spec.md:26`, `specs/roadmap/README.md:2-13` | Hard by directory convention | `cmd_guard` only scans direct children of `specs/` (`src/main.rs:919-923`) | No |
| 14 | `checkpoint create` should support VCS-aware checkpointing | `README.md:382`, command table | Unenforced / partially implemented | `cmd_checkpoint create` prints “not yet implemented” (`src/main.rs:1381-1389`) | Yes |
| 15 | `measure-determinism` is part of command surface | `README.md:383-385` | Unenforced / experimental | command exists but returns explicit “not yet fully implemented” error (`src/main.rs:1395-1403`) | Yes |

### Enforcement Statistics

| Level | Count | Percentage |
|-------|-------|------------|
| Hard-enforced | 8 | 53% |
| Soft-enforced | 5 | 33% |
| Unenforced | 2 | 14% |

### Critical Gaps

1. **Review/approval discipline mostly lives in prompts, not gates.** `Contract Acceptance` 被广泛宣传，但 `explain` 只是 formatter，没有 approval state、no-merge gate、也没有“review completed”标记（`src/main.rs:1267-1305`）。
2. **Retry escalation is narrative-only.** 文档要求 3 次失败升级给人，但 runtime 不记录 per-scenario retry budget，也不会自动中断（`AGENTS.md:54`, `skills/agent-spec-tool-first/SKILL.md:184`, code absent）。
3. **Spec tampering between failing and passing runs is not prevented.** lifecycle 会重新 lint spec，但不会比较 spec 是否被为了过门而改弱。框架假设“如果 spec 要改，应显式 authoring”，但没有 diff-level provenance guard。
4. **Hook installer has opinionated defaults.** 自动写入 `--code src`，对非 Rust / 非 `src/` layout 仓库可能不合适（`src/main.rs:1647-1649`）。
5. **部分命令是“surface exists, implementation partial”。** `checkpoint create` 和 `measure-determinism` 都已暴露在 CLI/README，但核心行为未完成（`src/main.rs:1381-1389`, `src/main.rs:1395-1403`）。

---

## 6. Prompt Catalog

### Prompt: Tool-First Implementer

| Field | Value |
|-------|-------|
| **repo_path** | `skills/agent-spec-tool-first/SKILL.md` |
| **quote_excerpt** | "NO CODE IS \"DONE\" WITHOUT A PASSING LIFECYCLE" |
| **stage** | implementation / verification / review handoff |
| **design_intent** | 强迫 agent 把 `lifecycle` 当成唯一完成条件，而不是主观自报完成 |
| **hidden_assumption** | 假设 repo 可通过 `cargo test` 和 selected tests 机械验证，且 agent 会真的读取 JSON evidence |
| **likely_failure_mode** | agent 知道规则但跳过执行；或 selector 不准导致大量 `skip`，又没有真正修复 spec/test binding |
| **evidence_level** | direct |

Evidence: `skills/agent-spec-tool-first/SKILL.md:145-186`

### Prompt: Contract Author

| Field | Value |
|-------|-------|
| **repo_path** | `skills/agent-spec-authoring/SKILL.md` |
| **quote_excerpt** | "After drafting or editing a spec, always run `agent-spec parse <spec>` and then `agent-spec lint <spec> --min-score 0.7`." |
| **stage** | authoring / pre-implementation |
| **design_intent** | 把自然语言 contract 变成可检查 artifact，防止“写完 spec 就直接交给 agent” |
| **hidden_assumption** | 假设任务能被提前规格化，且重要行为都能转成 deterministic scenarios |
| **likely_failure_mode** | rewrite/parity 任务只覆盖 happy path，漏掉 stdout/stderr/output mode/cache/fallback surfaces |
| **evidence_level** | direct |

Evidence: `skills/agent-spec-authoring/SKILL.md:58-64`, `...:77-90`, `...:91-129`

### Prompt: Estimator

| Field | Value |
|-------|-------|
| **repo_path** | `skills/agent-spec-estimate/SKILL.md` |
| **quote_excerpt** | "Every number in the estimate table MUST trace back to a specific Contract element" |
| **stage** | planning / sprint sizing |
| **design_intent** | 把 contract 当作 estimation substrate，而不是拍脑袋估时 |
| **hidden_assumption** | 假设 scenario count、boundary breadth 和 decisions specificity 与真实工作量有稳定相关性 |
| **likely_failure_mode** | spec 本身写得差时，估算会变成“有格式的猜测”；另一个风险是把 rounds 当 wallclock certainty |
| **evidence_level** | direct |

Evidence: `skills/agent-spec-estimate/SKILL.md:41-80`, `...:141-176`

### Prompt: Cross-Platform Agent Mirror

| Field | Value |
|-------|-------|
| **repo_path** | `AGENTS.md` |
| **quote_excerpt** | "Two workflows: Tool-First (using the CLI) and Authoring (writing .spec/.spec.md files)." |
| **stage** | onboarding / agent adaptation |
| **design_intent** | 把 Claude-local skill protocol 翻译成任何其他 agent 都能遵守的 textual contract |
| **hidden_assumption** | 假设外部 agent 能自行执行 CLI，并且会接受相同的 review-point displacement |
| **likely_failure_mode** | 把 AGENTS.md 当成全部真相，忽略 skill reference files 和 runtime defaults |
| **evidence_level** | direct |

Evidence: `AGENTS.md:1-4`, `AGENTS.md:33-76`

### Prompt: Human Review Reframing

| Field | Value |
|-------|-------|
| **repo_path** | `README.md` |
| **quote_excerpt** | "The reviewer judges two questions: (1) Is the Contract definition correct? (2) Did all verifications pass?" |
| **stage** | review / acceptance |
| **design_intent** | 用“合约定义是否正确 + 验证是否全绿”替代传统代码 diff review |
| **hidden_assumption** | 假设 reviewer 愿意把关注点从代码质量直读转移到 contract adequacy |
| **likely_failure_mode** | 复杂架构或非功能性问题在 contract 中没有被建模时，review summary 可能掩盖 deeper design flaws |
| **evidence_level** | direct |

Evidence: `README.md:218-226`, `README.md:453-457`

---

## 7. Design Highlights — Micro

### Highlight: `plan` 把 Allowed Changes 直接转成 code scan scope

- **Observation**: `plan` 不是全仓库索引，而是先抽取 `Boundaries` 里的 allowed path patterns，再只扫描这些路径下的代码与测试函数。 
- **Evidence**: `src/spec_gateway/plan.rs:80-85`, `src/spec_gateway/plan.rs:97-110`, `src/spec_gateway/plan.rs:133-209`
- **Why it matters**: 这让 spec 不只是验收条件，还是上下文过滤器，减少 prompt 噪音。
- **Trade-off**: 如果 Allowed Changes 写错或路径不存在，`plan` 只给 warning，不会 hard fail（`src/spec_gateway/plan.rs:156-161`）。
- **Transferability**: Direct

### Highlight: verifier chain 固定顺序，报告统一汇总

- **Observation**: `SpecGateway::run_verify` 把 verifier 固定为 `structural → boundaries → test → ai → complexity`，再统一汇总成一个 report。 
- **Evidence**: `src/spec_gateway/lifecycle.rs:196-217`
- **Why it matters**: 顺序固定意味着框架的“什么算验证”是 process-as-code，而不是 agent 自己判断。
- **Trade-off**: 没有 per-project verifier registry，扩展性受限；用户必须改源码。
- **Transferability**: Inspired

### Highlight: verdict taxonomy 是一等对象，不被压扁成 pass/fail

- **Observation**: 报告、状态文件、explain、is_passing 都保留 `pass/fail/skip/uncertain/pending_review` 五类状态。 
- **Evidence**: `specs/project.spec.md:16`, `src/spec_gateway/lifecycle.rs:229-245`, `src/spec_report/mod.rs:55-61`, `src/spec_report/mod.rs:171-178`
- **Why it matters**: 这是把“未验证”和“验证失败”从语义上剥离开，防止假阳性。
- **Trade-off**: 使用者必须真的理解这些状态，不然会觉得流程“太严格”。
- **Transferability**: Direct

### Highlight: `resolve-ai` 不是内嵌 provider，而是宿主注入点

- **Observation**: AI verifier 只定义 `AiBackend` trait；stub 返回 `uncertain`，external backend 由 host 注入。caller mode 则通过 JSON file handoff。 
- **Evidence**: `src/spec_verify/ai_verifier.rs:13-16`, `src/spec_verify/ai_verifier.rs:18-45`, `src/main.rs:607-645`, `README.md:334-338`
- **Why it matters**: 避免把 provider/model/auth policy 烧进框架核心，降低供应商耦合。
- **Trade-off**: out-of-the-box 体验较弱；用户必须补 host-side glue。
- **Transferability**: Direct

### Highlight: run log + checkpoint 是 file-backed retry memory

- **Observation**: lifecycle 可选把 run result 落盘为 `.agent-spec/runs/*.json` 和 `.agent-spec/checkpoint.json`，`explain --history` 再把这些 history 读回。 
- **Evidence**: `src/main.rs:686-715`, `src/main.rs:1418-1629`
- **Why it matters**: 这是极轻量的 durable execution memory，不需要数据库或 orchestrator。
- **Trade-off**: 只适合单 repo / file-based workflow；没有多任务并发调度能力。
- **Transferability**: Direct

### Highlight: Hook 安装采取 append-not-overwrite 策略

- **Observation**: `install-hooks` 如果发现已有 pre-commit，会检测其中是否已有 `agent-spec`；没有就 append，而不是覆盖。 
- **Evidence**: `src/main.rs:1656-1674`
- **Why it matters**: 对已有 repo 的侵入性更低，减少破坏已有 hook 的概率。
- **Trade-off**: 追加式安装也更容易让 hook 累积历史垃圾，且默认参数未必适配目标项目。
- **Transferability**: Direct

---

## 8. Design Highlights — Macro

### Philosophy: Contract-first, code-second

- **Observation**: 仓库把 Task Contract 视为 primary planning surface，代码只是 contract 的实现物。 
- **Where it appears**: `README.md:16`, `README.md:20-27`, `AGENTS.md:35-41`, `skills/agent-spec-authoring/SKILL.md:37-45`
- **How it shapes the workflow**: 所有阶段都围绕 spec artifact 展开：authoring → contract render → plan → lifecycle → explain。
- **Strengths**: 明确 done definition；更容易把 edge cases 提前显式化。
- **Limitations**: 对 exploratory tasks、无法写 deterministic tests 的问题不友好（authoring skill 自己也承认这一点：`skills/agent-spec-authoring/SKILL.md:133-142`）。
- **Adopt?**: Yes — 但要保留“探索性 spike 不强制合同化”的逃生口。

### Philosophy: Verification over self-report

- **Observation**: “done” 的定义不是 agent 说完了，而是 lifecycle 通过。 
- **Where it appears**: `skills/agent-spec-tool-first/SKILL.md:165-171`, `src/spec_gateway/lifecycle.rs:229-245`, `src/main.rs:717-721`
- **How it shapes the workflow**: 完成标准被收敛到 verifier chain 和 summary counts，而不是 conversational confidence。
- **Strengths**: 明显降低“说自己修好了但没验证”的假完成。
- **Limitations**: 任何没进 verifier 的质量维度都会被忽略，尤其 architecture fitness 和长期 maintainability。
- **Adopt?**: Yes — 但要搭配额外 reviewer 或 architecture checks。

### Philosophy: Prompts declare behavior, code enforces only the critical subset

- **Observation**: repo 同时有大量 prompt discipline 和一组较小但真实的 hard gates。 
- **Where it appears**: skills/AGENTS 里大量 MUST/STOP/DO NOT（如 `AGENTS.md:45-54`, `skills/agent-spec-tool-first/SKILL.md:175-198`），而真正 code enforcement 集中在 lint/boundary/test/pass-state（`src/spec_gateway/lifecycle.rs:69-80`, `src/spec_verify/boundaries.rs:36-104`, `src/spec_verify/test_verifier.rs:46-74`）
- **How it shapes the workflow**: 框架并不试图把所有 process rhetoric 编译成 gate，而是只把最关键的 correctness checks 编译进去。
- **Strengths**: 实现成本低、协议清晰、可渐进升级。
- **Limitations**: 人类 review discipline、retry budget、spec tampering 等高层规则仍然靠 agent 自觉。
- **Adopt?**: Modify — 迁移时应挑出最容易作弊的软规则补成硬 gate。

### Philosophy: File-backed portability over runtime orchestration

- **Observation**: 框架的主要交互面是 CLI + files，而不是 runtime orchestrator。 
- **Where it appears**: `Cargo.toml:0-7`, `src/main.rs:36-245`, `README.md:157-234`, `AGENTS.md:18-31`
- **How it shapes the workflow**: Claude、Codex、Cursor 甚至 CI 都能围绕同一个 contract/report protocol 工作。
- **Strengths**: 高可移植性，host-agnostic。
- **Limitations**: 没有原生任务并发、队列调度、review arbitration、多 agent state machine。
- **Adopt?**: Yes — 适合作为 protocol layer，但别期待它替代 orchestrator。

### Philosophy: Human review moves up one abstraction level

- **Observation**: 它不是取消 human review，而是把 review 从 diff-level 移到 contract/evidence-level。 
- **Where it appears**: `README.md:218-226`, `README.md:453-457`, `AGENTS.md:11-16`
- **How it shapes the workflow**: reviewer 看 `explain` 和 passed verifications，而不是逐行读 patch。
- **Strengths**: 在需求明确、可测边界清晰的任务上，review 成本显著下降。
- **Limitations**: 当 contract 本身遗漏重要非功能需求时，人类会被“绿色 summary”误导。
- **Adopt?**: Modify — 可用于大量 task-level work，但要保留对架构/安全/性能改动的 deeper review path。

---

## 9. Failure Modes & Limitations

| # | Failure Mode | Trigger | Impact | Evidence |
|---|-------------|---------|--------|----------|
| 1 | Selector drift causes `skip` avalanche | spec 里的 `Test:` 与真实 test name 不匹配 | lifecycle/guard 全线不通过，agent 可能错误地修代码而不是修 selector | `AGENTS.md:47-51`, `src/spec_verify/test_verifier.rs:41-47`, `src/spec_gateway/lifecycle.rs:234-245` |
| 2 | Allowed Changes under-specification weakens planning | `Boundaries` 路径缺失或写错 | `plan` 扫不到关键代码，只产生 warnings，agent 可能在上下文不足下实现 | `src/spec_gateway/plan.rs:145-161` |
| 3 | Soft review discipline is easy to bypass | 团队只跑 lifecycle，不看 explain/Contract Acceptance | 通过了功能 gate，但审查环节缺失 | `README.md:218-226`, `src/main.rs:1267-1305` |
| 4 | Retry budget exists only in prose | 连续失败 3 次后没有 runtime stop | agent 可能无限重试或在错误方向上浪费轮次 | `AGENTS.md:54`, code has no retry budget enforcement |
| 5 | Hook installer assumes `src/` code root | 非 Rust / 非 `src/` layout 项目执行 `install-hooks` | pre-commit guard 范围偏差，可能漏检或错检 | `src/main.rs:1647-1649` |
| 6 | Experimental commands inflate perceived capability | README/CLI 暴露 `checkpoint create` / `measure-determinism` | 用户误以为 feature 完整，实际只能拿到 placeholder/错误 | `README.md:382-385`, `src/main.rs:1381-1389`, `src/main.rs:1395-1403` |
| 7 | Legacy comment fallback dilutes “explicit selector required” rule | scenario missing explicit selector but source has `// @spec:` mapping | 框架继续工作，但 authorship discipline 被弱化 | `README.md:261`, `src/spec_verify/test_verifier.rs:172-189` |

### Observed vs Claimed Behavior Divergences

| Claim | Source | Actual Behavior | Evidence | Evidence Level |
|-------|--------|----------------|----------|---------------|
| `checkpoint` is a checkpoint mechanism | `README.md:382`, command table | `status` only reports VCS type; `create` is not implemented | `src/main.rs:1357-1389` | direct |
| `measure-determinism` is available | `README.md:384-385` | command exists but immediately errors as experimental/unimplemented | `src/main.rs:1395-1403` | direct |
| Explicit `Test:` selector is the default quality rule | `README.md:236-261`, `examples/README.md:13-14` | runtime still supports legacy `// @spec:` comment fallback | `src/spec_verify/test_verifier.rs:148-189` | direct |
| Contract Acceptance replaces code review | `README.md:218-226`, `README.md:453-457` | framework provides formatter (`explain`) but no approval state machine or blocking reviewer signoff | `src/main.rs:1267-1305` | direct |
| AI verification expansion exists | `README.md:300-338` | shipped implementation is stub/external backend scaffold, not model-backed verifier | `src/spec_verify/ai_verifier.rs:18-45`, `README.md:319-338` | direct |

---

## 10. Migration Assessment

### Candidates

| # | Mechanism | Rating | Effort | Prerequisite | Risk | Source |
|---|----------|--------|--------|-------------|------|--------|
| 1 | Distinct verdict taxonomy (`pass/fail/skip/uncertain/pending_review`) | Direct | S | unified report schema | 如果只复制文案不复制 pass rule，很容易把 `skip` 当绿灯 | `src/spec_gateway/lifecycle.rs:229-245`, `src/spec_report/mod.rs:55-61` |
| 2 | Boundaries-driven code scan for planning | Direct | M | task spec with allowed paths | path quality不足会导致 false confidence | `src/spec_gateway/plan.rs:80-109`, `src/spec_gateway/plan.rs:133-209` |
| 3 | Unified verifier chain behind a gateway | Inspired | M | pluggable verification API | naive port 可能把 repo-specific verifier 顺序硬编码死 | `src/spec_gateway/lifecycle.rs:196-217` |
| 4 | File-backed run log + checkpoint memory | Direct | S | writable workspace state dir | 并发任务会互相污染单目录 run logs | `src/main.rs:686-715`, `src/main.rs:1418-1504` |
| 5 | Caller-mode AI request/decision handoff | Direct | M | external agent that can read/write JSON | 如果没有严格 merge protocol，AI layer 会变成 unverifiable black box | `src/main.rs:607-645`, `src/main.rs:2286-2361`, `src/spec_verify/ai_verifier.rs:102-161` |
| 6 | Contract Acceptance summary (`explain`) | Inspired | M | report formatter + contract schema | 如果合同覆盖不足，会给 reviewer 过强安全感 | `src/main.rs:1267-1305`, `README.md:218-226` |
| 7 | Self-hosting roadmap via staged contracts | Direct | S | docs/spec directory discipline | roadmap 和 active specs 边界不清会造成 gate 漏洞 | `specs/roadmap/README.md:2-13` |
| 8 | Hook installer that appends local guard | Inspired | S | pre-commit hook convention | 默认参数过于 opinionated 可能误伤多语言项目 | `src/main.rs:1633-1684` |
| 9 | Prompt trio split (`authoring` / `tool-first` / `estimate`) | Direct | S | clear workflow stages | prompt proliferation without enforcement 会变成文档噪音 | `README.md:103-109`, `skills/*/SKILL.md` |
| 10 | Full contract-first review-point displacement | Inspired | L | strong test culture + spec discipline + reviewer buy-in | 迁移过猛会让团队把“少看代码”误解为“不看架构” | `AGENTS.md:11-16`, `README.md:218-226` |

### Recommended Adoption Order

1. **Verdict taxonomy + hard pass rule** — 最低成本、最高收益。先把 `skip`/`uncertain` 从“模糊状态”变成正式非通过态。
2. **File-backed run log + checkpoint** — 这能立刻提升 retry evidence 和 session continuity，而且实现简单。
3. **Boundaries-driven planning scope** — 让 spec 同时控制上下文和改动范围，减少 agent 漫游。
4. **Caller-mode AI handoff protocol** — 在已有 verifier/report schema 后再接入，避免先上模型再补证据链。
5. **Contract Acceptance formatter** — 先有强 report，再让人类 review 上移到 contract/evidence 层。
6. **Prompt trio split** — 在 stage 边界明确后再拆 authoring/tool-first/estimate，否则只是文档分裂。
7. **Gateway verifier chain** — 等验证维度稳定后再抽象成统一 pipeline。
8. **完整 review-point displacement** — 这是文化级迁移，最后做。

### Non-Transferable (with reasons)

| Mechanism | Why Not | Alternative |
|----------|---------|-------------|
| `cargo test`-centric `TestVerifier` | 强耦合 Rust/Cargo；其他栈无法直接复用 | 抽象成 `TestRunnerBackend`，把 selector → command mapping 放到 host project 层 |
| `install-hooks` 默认 `--code src` | 假设 Rust repo shape | 让 installer 读取 project config 或在安装时询问 code root |
| `checkpoint create` current design | 功能未完成，本体都还没闭环 | 先只迁移 `status` / run-log resume，不迁移 create |

### Must-Build Enforcement

| Mechanism | Original Level | Recommended Level | How to Enforce |
|----------|---------------|-------------------|---------------|
| Retry budget / human escalation | Soft (prompt) | Hard | 在 run log 中按 scenario 计失败次数，超过阈值时 lifecycle 返回专门的 `escalation_required` 状态 |
| Do-not-weaken-spec-on-failure | Soft (prompt) | Hard | 对比 failing run 与 passing run 间的 spec diff；若只放宽 criteria 而无相应 review flag，则阻断 |
| Contract Acceptance actually happened | Soft | Hard | 在 CI 中要求 reviewer-approved artifact/comment marker，或要求 `explain` output attached to PR |
| Public interface regression coverage | Soft/self-hosted only | Hard | 建立 public-surface inventory，要求每项 interface change 绑定至少一个 explicit scenario/test selector |
| Hook install defaults | Soft/implicit | Hard-configured | 安装时生成 project-local config，不允许硬编码 `src` |

---

## 11. Open Questions

1. `resolve-ai` 的完整 merge logic 在多 scenario、多 backend、partial decisions 下如何处理冲突？—— 这关系到 AI verifier protocol 是否适合迁移。
2. `StructuralVerifier` 与 `ComplexityVerifier` 的具体规则强度有多大？—— 当前报告已看到 pipeline 接入点，但未逐条展开其内部规则。
3. `plan` 的 `TaskSketch` 如何精确构建依赖组？—— 已确认有 grouping schema，但未完整展开其 topo/grouping heuristics。
4. `contract-guard.yml` 在外部仓库落地时的 comment/update UX 是否足够稳定？—— 这影响 contract acceptance 的团队采用成本。
5. self-hosting specs 与真实外部项目使用之间是否存在隐性偏差？—— agent-spec 在自己仓库里用得很好，不代表对其他语言/测试生态同样平滑。

---

## Appendix: Source Trace Table

| # | Source Type | Repo Path | Role | Excerpt | Evidence Level | Referenced In |
|---|-----------|-----------|------|---------|---------------|--------------|
| 1 | README | `README.md` | canonical workflow claims | "The primary planning surface is the Task Contract" | direct | §1, §4, §8 |
| 2 | agent guidance | `AGENTS.md` | cross-platform agent mirror | "Two workflows: Tool-First ... and Authoring ..." | direct | §2, §6, §8 |
| 3 | manifest | `Cargo.toml` | CLI package identity | `name = "agent-spec"` | direct | §1, §2 |
| 4 | schema | `src/spec_core/ast.rs` | entity definitions | `pub struct SpecDocument`, `pub struct Scenario`, `pub struct TestSelector` | direct | §3 |
| 5 | resolver | `src/spec_parser/resolver.rs` | inheritance chain | `resolve_spec` merges inherited constraints/decisions | direct | §3 |
| 6 | gateway | `src/spec_gateway/lifecycle.rs` | verifier orchestration + pass rule | `vec![&structural, &boundaries, &test, &ai, &complexity]` | direct | §3, §4, §5, §7 |
| 7 | planner | `src/spec_gateway/plan.rs` | scoped code scan | `collect_allowed_patterns`, `scan_codebase` | direct | §3, §4, §7 |
| 8 | verifier | `src/spec_verify/boundaries.rs` | path enforcement | `not covered by any allowed boundary` | direct | §2, §5 |
| 9 | verifier | `src/spec_verify/test_verifier.rs` | test execution binding | `Command::new("cargo")` | direct | §2, §5, §9 |
| 10 | verifier | `src/spec_verify/ai_verifier.rs` | AI scaffold | `manual review required` | direct | §2, §5, §7, §9 |
| 11 | command impl | `src/main.rs` | lifecycle gate | `quality gate failed`, `ai_pending`, `write_run_log` | direct | §4, §5, §7 |
| 12 | command impl | `src/main.rs` | explain/history/stamp/checkpoint | `No run history found`, `not yet implemented` | direct | §4, §5, §9 |
| 13 | CI workflow | `.github/workflows/contract-guard.yml` | repo-level hard gate | `exit $GUARD_EXIT` | direct | §2, §5 |
| 14 | project contract | `specs/project.spec.md` | self-hosting meta-rules | `不要把 skip 记为 pass` | direct | §2, §5 |
| 15 | roadmap policy | `specs/roadmap/README.md` | staged contract inclusion rule | `not part of the default ... guard run until promoted` | direct | §2, §4, §10 |
| 16 | prompt | `skills/agent-spec-tool-first/SKILL.md` | implementer discipline | `NO CODE IS "DONE" WITHOUT A PASSING LIFECYCLE` | direct | §2, §6, §8 |
| 17 | prompt | `skills/agent-spec-authoring/SKILL.md` | authoring discipline | `always run parse ... lint ...` | direct | §2, §6, §8 |
| 18 | prompt | `skills/agent-spec-estimate/SKILL.md` | estimation discipline | `Every number ... MUST trace back` | direct | §2, §6 |
