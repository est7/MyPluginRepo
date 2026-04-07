# Workflow Research: everything-claude-code-mobile

> 逆向工程研究报告 — 移动端全栈 Agent 编排框架
> 仓库: `ahmed3elshaer/everything-claude-code-mobile`
> 版本: 1.1.5 | 日期: 2026-04-07

---

## §1 Framework Profile

| 维度 | 值 |
|------|-----|
| 框架类型 | 移动端 Agent 编排系统 + 技能库混合体 |
| 规模 | 179 文件, 27 agents, 48 skills, 35 commands, 7 contexts, 3 MCP servers |
| 目标平台 | Android (Kotlin/Compose), iOS (Swift/SwiftUI), KMP |
| 核心机制 | 7-phase feature builder pipeline + DAG-ordered layer agents |
| 状态持久化 | `.omc/state/` JSON 文件 + `.omc/plans/` JSON 文件 + `.claude/instincts/` |
| 执行模型 | 命令驱动 → agent 编排 → hook 辅助 → MCP 记忆 |
| 上游关系 | `everything-claude-code` 的移动端伴侣项目 |

### 框架类型判定

这不是纯粹的 skill pack，而是一个以 feature builder pipeline 为核心的 agent 编排系统。27 个 agent 中有 5 个是 DAG 编排的 layer agent（`architecture-impl`, `network-impl`, `data-impl`, `ui-impl`, `wiring-impl`），3 个是并行 reviewer，其余为专项顾问。skill 层提供领域知识参考，command 层提供用户入口，hook 层提供自动化辅助。

---

## §2 Source Inventory

### Overview

| 文件 | 用途 |
|------|------|
| `README.md` | 项目总览、安装、命令列表、agent 目录 |
| `docs/architecture.md` | MVI + Clean Architecture 设计指南 |
| `docs/tdd-workflow.md` | TDD 流程与 Kotlin 示例 |
| `docs/continuous-learning.md` | 持续学习机制说明 |
| `docs/installation.md` | 安装与配置指南 |
| `docs/android-setup.md` | Android 环境配置 |
| `examples/CLAUDE.md` | 推荐的项目 CLAUDE.md 模板 |

### Execution

| 类别 | 数量 | 路径 |
|------|------|------|
| Agents | 27 | `agents/*.md` |
| Commands | 35 | `commands/*.md` |
| Skills | 48 | `skills/*/SKILL.md` |
| Contexts | 7 | `contexts/*.md` |

### Prompts

所有 agent 和 skill 均为 Markdown prompt 文件，无代码逻辑。prompt 即执行定义。

### Enforcement

| 文件 | 类型 | 执行级别 |
|------|------|----------|
| `hooks/hooks.json` | Android hook 配置 | 混合（Hard + Soft） |
| `hooks/hooks-ios.json` | iOS hook 配置 | 混合（Hard + Soft） |
| `hooks/checkpoint-hooks.json` | 检查点 hook 配置 | Hard（脚本执行） |
| `hooks/extended/instinct-hooks.json` | 学习 hook 配置 | Soft |
| `scripts/hooks/evaluate-session.js` | 会话评估脚本 | Hard（`process.exit(1)`） |
| `scripts/hooks/pre-compact.js` | 压缩前保存脚本 | Hard |
| `scripts/hooks/auto-checkpoint.js` | 自动检查点脚本 | Hard |
| `scripts/lint-json.js` | JSON 校验脚本 | Hard（`process.exit(1)`） |
| `rules/mobile-testing.md` | 测试规则 | Soft（prompt 指令） |
| `rules/android-style.md` | Android 代码风格 | Soft |
| `rules/ios-style.md` | iOS 代码风格 | Soft |
| `rules/mobile-security.md` | 安全规则 | Soft |
| `rules/agents.md` | Agent 委派规则 | Soft |

### Evolution

| 文件 | 用途 |
|------|------|
| `tests/verify.js` | 结构完整性验证 |
| `tests/unit/*.test.js` | 6 个单元测试文件 |
| `tests/integration/*.test.js` | 2 个集成测试文件 |
| `package.json` | 版本 1.1.5，无 changelog |

---

## §3 Object Model & Context Strategy

### First-Class Entities

| 实体 | 定义位置 | 生命周期 | 分类 |
|------|----------|----------|------|
| **Feature Plan** | `.omc/plans/feature-{name}.json` | 创建 → 架构审查 → 用户批准 → 执行 → 归档 | Fact Object |
| **Feature State** | `.omc/state/feature-{name}.json` | 创建 → 逐 phase 更新 → 完成/失败 | Evidence Object |
| **Instinct** | `.claude/instincts/` | 提取 → 存储 → 置信度衰减 → 进化为 skill | Judgment Object |
| **Checkpoint** | `.claude/checkpoints/` | 自动创建 → 保留(max 20) → 30天清理 | Evidence Object |
| **Learning Summary** | `.omc/state/feature-{name}-learning.json` | Phase 7 生成 → 反馈到 instinct 系统 | Judgment Object |

### Feature Plan Schema（核心实体）

定义于 `skills/feature-builder/SKILL.md`，结构：

```
{
  featureName, description, platform, createdAt, updatedAt,
  architecture: { pattern, diFramework, networkClient, localStorage, navigationLib },
  moduleLocation,
  modules: { domain: {path, files[]}, data: {...}, presentation: {...}, di: {...} },
  wiring: { navigationChanges[], diRegistration[], manifestChanges[] },
  tests: { unit[], ui[], e2e[] },
  dependencies: { new[], existing[] },
  tasks: [{ id, phase, agent, description, dependsOn[] }]
}
```

### Feature State Schema

```
{
  featureName, platform, startedAt, currentPhase,
  phases: {
    1_planning: { status, startedAt, completedAt, planPath },
    2_implementation: { status, agents: { [name]: { status, filesCreated[] } } },
    3_testing: { status, agents: { [name]: { status, testsCreated } } },
    4_build_fix: { status, iterations, maxIterations, lastError, lastFix },
    5_quality_gate: { status, findings: { critical, high, medium, low } },
    6_verification: { status, passAtK, coverage }
  }
}
```

### Context Flow

```
用户描述
    ↓
feature-planner (读项目结构) → Plan JSON
    ↓
mobile-architect (审查 Plan) → 修订后的 Plan
    ↓
用户批准
    ↓
layer agents (各读 Plan 中自己的 section) → 源文件
    ↓
test agents (读 Plan 的 test section) → 测试文件
    ↓
build-fix loop (读编译输出) → 修复
    ↓
reviewer agents (读源文件) → findings
    ↓
mobile-verifier (运行测试 k 次) → pass@k 报告
    ↓
learning (扫描生成文件) → instincts
```

**Context 隔离策略**: 每个 agent 通过 Plan JSON 获取自己的文件列表，只写自己负责的文件。跨 agent 通信通过 `.omc/state/` 文件实现，不依赖对话上下文传递。MCP memory server 提供跨会话持久化。

**Token 预算**: 无显式 token 预算管理。skill 文件大小不受约束（部分 skill 如 `feature-builder/SKILL.md` 超过 800 行）。

---

## §4 Flow & State Machine Analysis

### 主流程: Feature Builder Pipeline

```
[用户输入描述]
       │
       ▼
Phase 1: PLANNING ──────────────────────────────────────────┐
  feature-planner → Plan JSON                                │
  mobile-architect → 审查 + 修订                              │
  用户 → 批准/修改/取消                                        │
       │                                                     │
       ▼                                                     │
Phase 2: IMPLEMENTATION                                      │
  architecture-impl (Phase 2a)                               │
       │                                                     │
  ┌────┴────┐                                                │
  network-impl  ui-impl (Phase 2b, 并行)                     │
       │                                                     │
  data-impl (Phase 2c, 等待 network)                         │
       │                                                     │
  wiring-impl (Phase 2d, 等待全部)                            │
       │                                                     │
       ▼                                                     │
Phase 3: TESTING (3 agents 并行)                              │
  unit-test-writer + ui-test-writer + mobile-e2e-runner      │
       │                                                     │
       ▼                                                     │
Phase 4: BUILD & FIX (循环, max 5 次)                         │
  编译 → 分析错误 → 修复 → 运行测试                             │
  ├─ 全绿 → Phase 5                                          │
  ├─ 失败 → iteration++ (max 5)                              │
  └─ 超限 → 上报用户                                          │
       │                                                     │
       ▼                                                     │
Phase 5: QUALITY GATE (3 reviewers 并行)                      │
  code-reviewer + security-reviewer + performance-reviewer   │
  ├─ 0 critical + 0 high → Phase 6                           │
  └─ critical found → 修复 → 回到 Phase 4                     │
       │                                                     │
       ▼                                                     │
Phase 6: VERIFICATION                                        │
  mobile-verifier: pass@k=3 测试                              │
  ├─ unit pass@3 >= 0.95 + coverage >= 80% → Phase 7         │
  └─ coverage < 80% → 回到 Phase 3                            │
       │                                                     │
       ▼                                                     │
Phase 7: LEARNING (自动)                                      │
  扫描生成文件 → 提取 patterns → 存储 instincts                 │
  计算 completeness score → 保存 learning summary              │
       │                                                     │
       ▼                                                     │
[完成]                                                        │
                                                             │
恢复路径: --from-phase=N 从任意 phase 恢复 ◄──────────────────┘
跳过路径: --skip-phase=N 跳过指定 phase
```

### 状态转换

每个 phase 的 status 值: `pending` → `in_progress` → `completed` | `failed` | `skipped`

### 失败路径

1. **Phase 4 超限**: 5 次迭代后上报用户，提供错误日志 + 已尝试修复 + 手动干预建议
2. **Phase 5 critical finding**: 修复后回退到 Phase 4 重新编译验证
3. **Phase 6 coverage 不足**: 回退到 Phase 3 补充测试

### 并行执行点

- Phase 2b: `network-impl` + `ui-impl` 并行
- Phase 3: 3 个 test agent 并行
- Phase 5: 3 个 reviewer 并行

---

## §5 Enforcement Audit

### Enforcement Matrix

| 约束 | 声明位置 | 执行级别 | 证据 |
|------|----------|----------|------|
| **80% 测试覆盖率** | `rules/mobile-testing.md`, `skills/feature-builder/SKILL.md` | Soft | prompt 指令要求 coverage >= 80%，Phase 6 验证阈值写在 skill 文本中，但无脚本或 hook 阻止低覆盖率代码提交 |
| **TDD 强制** | `rules/mobile-testing.md:5-9` | Soft | "MANDATORY" 标记，但仅通过 `mobile-tdd-guide` agent prompt 指导，无 hook 阻止非 TDD 流程 |
| **Kotlin 反模式检测** | `hooks/hooks.json:25-32` | Hard | `PostToolUse` hook 对 `.kt` 文件执行 `grep -n 'GlobalScope\|!!\|runBlocking'`，编辑后自动触发 |
| **Swift 反模式检测** | `hooks/hooks-ios.json:23-31` | Hard | `PostToolUse` hook 对 `.swift` 文件执行 `grep -n 'force unwrap\|!\|DispatchQueue.main.async'` |
| **ViewModel 测试提醒** | `hooks/hooks.json:36-43` | Soft | 创建 `*ViewModel.kt` 时发送 message 提醒，不阻止操作 |
| **SwiftUI Preview 提醒** | `hooks/hooks-ios.json:48-55` | Soft | 编辑 `ContentView.swift` 时发送 message 提醒 |
| **Gradle 更新前检查点** | `hooks/checkpoint-hooks.json:19-33` | Hard | `PreToolUse` hook 在 Gradle upgrade 前执行 `auto-checkpoint.js` |
| **Manifest 修改前检查点** | `hooks/checkpoint-hooks.json:34-44` | Hard | `PreToolUse` hook 在 AndroidManifest.xml 编辑前执行 `auto-checkpoint.js` |
| **会话结束学习提取** | `hooks/hooks.json:5-12` | Hard | `Stop` event 触发 `evaluate-session.js` 脚本 |
| **压缩前上下文保存** | `hooks/hooks.json:13-20` | Hard | `PreCompact` event 触发 `pre-compact.js` 脚本 |
| **无硬编码密钥** | `rules/mobile-security.md`, `README.md` | Soft | 仅在 `mobile-security-reviewer` agent prompt 中检查，无 hook 或脚本扫描 |
| **HTTPS only + 证书固定** | `README.md:298` | Soft | 仅文档声明，无执行机制 |
| **文件 < 400 行** | `README.md:300` | Unenforced | 仅 README 声明，未出现在任何 prompt、hook 或脚本中 |
| **函数 < 50 行** | `README.md:300` | Unenforced | 同上 |
| **嵌套 < 4 层** | `README.md:300` | Unenforced | 同上 |
| **结构化并发** | `README.md:299` | Soft | Kotlin 反模式 hook 检测 `GlobalScope`/`runBlocking`，但 Swift 侧的 `DispatchQueue.main.async` 检测 grep 模式过于宽泛 |
| **不可变优先** | `README.md:297` | Soft | `architecture-impl` agent prompt 中强调 immutable data class，但无验证 |
| **Plan 文件完整性** | `skills/feature-builder/SKILL.md` | Soft | 声明 "State file is written atomically"，但无代码实现原子写入 |
| **Phase 依赖顺序** | `commands/feature-implement.md`, `skills/feature-builder/SKILL.md` | Soft | DAG 顺序写在 prompt 中，由 Claude 遵守，无代码强制 |

### 关键发现

1. **Hard enforcement 集中在 hook 层**: 反模式 grep、检查点创建、会话学习提取有实际脚本执行
2. **所有架构约束均为 Soft**: MVI 模式、Clean Architecture 分层、80% 覆盖率等核心约束完全依赖 prompt 指令
3. **README 声明的 3 条代码度量规则完全 Unenforced**: 文件行数、函数行数、嵌套深度仅出现在 README，未进入任何 prompt 或 hook
4. **checkpoint-hooks.json 包含硬编码绝对路径**: `/Users/ah3sh/Developer/everything-claude-code-mobile/scripts/hooks/...`，在其他用户环境下会失败

---

## §6 Prompt Catalog

### 核心 Agent Prompts

| Role | repo_path | quote_excerpt | stage | design_intent | hidden_assumption | likely_failure_mode |
|------|-----------|---------------|-------|---------------|-------------------|---------------------|
| Feature Planner | `agents/feature-planner.md` | "You are a senior mobile feature planning specialist. You analyze codebases, detect platforms, and produce structured implementation plans that can be delegated to specialized agents." | Phase 1 | 自动检测平台、分析项目结构、生成可委派的结构化计划 | 项目遵循标准 Android/iOS/KMP 目录结构 | 非标准项目结构导致平台检测失败或模块发现不完整 |
| Mobile Architect | `agents/mobile-architect.md` | "You are a senior mobile architect specializing in MVI architecture, Clean Architecture principles, and modular Android applications." | Phase 1 (审查) | 审查计划的架构合理性 | 项目使用 MVI + Clean Architecture | 对 MVVM 或其他架构模式的项目给出不适用的建议 |
| Architecture Impl | `agents/architecture-impl.md` | "You are a senior mobile architect focused on domain layer and dependency injection. You create use cases, domain models, repository interfaces, and DI modules following Clean Architecture principles." | Phase 2a | 创建 domain 层代码 | Koin (Android), protocol-based DI (iOS), Koin Multiplatform (KMP) | 项目使用 Hilt/Dagger 时模板不匹配 |
| Mobile Verifier | `agents/mobile-verifier.md` | "Executes automated verification loops with pass@k metrics for Android testing. Detects flaky tests and measures code reliability." | Phase 6 | 通过多次运行检测 flaky test | 有可用的 Android emulator 或设备 | 无设备环境下 UI/E2E 测试无法执行 |
| Feature Builder (Skill) | `skills/feature-builder/SKILL.md` | "Zero-to-feature orchestration pipeline for mobile development. Transforms a feature description into production-ready code through six structured phases with automated agent coordination, build verification, and quality enforcement." | 全流程 | 端到端编排所有 phase 和 agent | 所有 agent 可用且项目结构标准 | 任一 agent 失败导致 pipeline 中断 |

### 辅助 Agent Prompts

| Role | repo_path | stage | design_intent |
|------|-----------|-------|---------------|
| `android-reviewer` | `agents/android-reviewer.md` | Phase 5 | Kotlin/Compose 代码审查 |
| `ios-reviewer` | `agents/ios-reviewer.md` | Phase 5 | Swift/SwiftUI 代码审查 |
| `mobile-security-reviewer` | `agents/mobile-security-reviewer.md` | Phase 5 | 安全审计（密钥、加密、网络） |
| `mobile-performance-reviewer` | `agents/mobile-performance-reviewer.md` | Phase 5 | 性能审查（内存、重组、启动） |
| `unit-test-writer` | `agents/unit-test-writer.md` | Phase 3 | ViewModel/UseCase/Repository 测试 |
| `ui-test-writer` | `agents/ui-test-writer.md` | Phase 3 | Compose/SwiftUI UI 测试 |
| `mobile-e2e-runner` | `agents/mobile-e2e-runner.md` | Phase 3 | E2E 流程测试 |
| `android-build-resolver` | `agents/android-build-resolver.md` | Phase 4 | Gradle/AGP/R8 错误修复 |
| `xcode-build-resolver` | `agents/xcode-build-resolver.md` | Phase 4 | Xcode/SPM/CocoaPods 错误修复 |
| `compose-guide` | `agents/compose-guide.md` | 按需 | Compose 状态、重组、主题 |
| `swiftui-guide` | `agents/swiftui-guide.md` | 按需 | SwiftUI 状态、视图优化 |
| `m3-expressive-guide` | `agents/m3-expressive-guide.md` | 按需 | Material 3 Expressive 设计系统 |
| `liquid-glass-guide` | `agents/liquid-glass-guide.md` | 按需 | Apple Liquid Glass (iOS 26+) |
| `mobile-pattern-extractor` | `agents/mobile-pattern-extractor.md` | Phase 7 | 代码模式提取 |
| `mobile-compactor` | `agents/mobile-compactor.md` | 按需 | 上下文压缩优化 |

---

## §7 Design Highlights — Micro

### 7.1 DAG-Ordered Layer Agent 编排

**观察**: Implementation phase 使用 5 个 layer agent 按依赖图执行，而非线性顺序。

**证据**: `skills/feature-builder/SKILL.md:120-168`, `commands/feature-implement.md:22-40`

```
architecture-impl → [network-impl ∥ ui-impl] → data-impl → wiring-impl
```

**意义**: 这是该框架最独特的设计。将 Clean Architecture 的分层直接映射为 agent 分工，每个 agent 只负责一层，通过 Plan JSON 中的 `dependsOn` 字段控制执行顺序。`network-impl` 和 `ui-impl` 可并行是因为它们都只依赖 `architecture-impl` 的 domain 接口。

**可迁移性**: Direct — 任何支持 agent 编排的系统都可以复用这种 DAG 模式。关键是 Plan JSON 中的 task dependency 声明。

### 7.2 Plan JSON 作为 Agent 间通信协议

**观察**: Feature Plan 不仅是计划文档，更是 agent 间的通信协议。每个 agent 从 Plan 中读取自己的 file list 和 module path。

**证据**: `skills/feature-builder/SKILL.md:510-627` (Plan Document Schema), `commands/feature-implement.md:41`

**意义**: 避免了 agent 间直接通信的复杂性。Plan JSON 充当了 shared contract，类似于微服务架构中的 API schema。

**可迁移性**: Direct — 这种 "plan as protocol" 模式可以直接应用于任何多 agent 编排场景。

### 7.3 pass@k 可靠性度量

**观察**: Phase 6 使用 pass@k 指标（运行测试 k 次，计算通过率）来检测 flaky test。

**证据**: `agents/mobile-verifier.md:47-79`, `skills/feature-builder/SKILL.md:357-371`

**意义**: 超越了简单的 pass/fail 二元判断。不同测试类型有不同阈值（unit >= 0.95, UI >= 0.80, E2E >= 0.60），反映了各类测试的固有不稳定性差异。

**可迁移性**: Inspired — 概念可迁移，但需要实际的测试执行环境（emulator/device）。

### 7.4 三层检查点系统

**观察**: 检查点分为 quick/standard/full 三个级别，根据操作风险自动选择。

**证据**: `hooks/checkpoint-hooks.json:4-17`

```json
"quick":    ["git-status", "git-branch", "recent-files"]
"standard": ["git-status", "git-branch", "build-config", "test-results", "recent-files"]
"full":     ["git-state", "build-config", "dependencies", "manifest", "test-results", "instincts", "compose-state"]
```

**意义**: Gradle 更新触发 standard，大规模重构触发 full，成功构建触发 quick。风险分级的检查点策略比统一检查点更高效。

**可迁移性**: Direct — 检查点分级策略可直接应用于任何 hook 系统。

### 7.5 Instinct 置信度衰减机制

**观察**: 学习到的 pattern 有置信度分数，初始 0.5，每次检测 +0.1（上限 1.0），30 天不活跃 -0.05。

**证据**: `skills/feature-builder/SKILL.md:452-455`

**意义**: 防止过时 pattern 永久影响决策。置信度 >= 0.7 的 instinct 被视为项目惯例，低于阈值的逐渐淡出。

**可迁移性**: Inspired — 衰减机制的概念可迁移，但需要持久化存储和定期评估逻辑。

---

## §8 Design Highlights — Macro

### 8.1 Architecture-as-Agent-Topology

**观察**: 框架将 Clean Architecture 的分层（Domain → Data → Presentation → Wiring）直接映射为 agent 拓扑。架构不是文档中的建议，而是 agent 编排的物理结构。

**证据**: `agents/architecture-impl.md`, `agents/network-impl.md`, `agents/data-impl.md`, `agents/ui-impl.md`, `agents/wiring-impl.md` — 每个 agent 的 prompt 严格限定在一个架构层。

**意义**: 这是一种 "process-as-architecture" 的设计哲学。通过将架构层映射为独立 agent，强制实现了关注点分离 — 不是通过代码审查发现违规，而是通过 agent 边界物理隔离。

**可迁移性**: 这种思路对任何领域特定的 agent 编排都有启发。关键洞察是：如果你的目标架构有明确的层次，可以让每个 agent 只负责一层。

### 8.2 Verification-Over-Self-Report

**观察**: 框架不信任 agent 的自我报告。Phase 4 通过实际编译验证代码正确性，Phase 6 通过多次运行测试验证可靠性，Phase 5 通过独立 reviewer 验证质量。

**证据**: `skills/feature-builder/SKILL.md:229-282` (build-fix loop), `skills/feature-builder/SKILL.md:351-371` (pass@k verification), `commands/feature-quality-gate.md` (parallel reviewers)

**意义**: 三层验证（编译 → 审查 → 统计测试）形成了递进的信任建立过程。这比单纯依赖 agent 声称 "代码已完成" 可靠得多。

### 8.3 Continuous Learning 闭环

**观察**: 框架设计了从执行到学习的完整闭环：执行 → 提取 pattern → 存储 instinct → 影响未来执行。

**证据**: `skills/continuous-learning/SKILL.md`, `skills/feature-builder/SKILL.md:402-499` (Phase 7), `hooks/hooks.json:5-12` (Stop event learning)

**意义**: 这不是简单的 "记住上次做了什么"，而是一个有置信度评分、衰减机制和进化路径（instinct → skill）的学习系统。但实际执行完全依赖 prompt 指令和 Node.js 脚本，学习质量取决于 pattern matcher 的准确性。

### 8.4 Platform-Agnostic Pipeline, Platform-Specific Agents

**观察**: Pipeline 的 7 个 phase 对所有平台相同，但每个 phase 内部根据平台选择不同的 agent 或行为。

**证据**: `skills/feature-builder/SKILL.md:170-176` (platform-specific behavior table), `commands/feature-build.md:18-20` (--platform flag)

**意义**: 这是一种 "策略模式" 的宏观应用。Pipeline 是稳定的骨架，平台差异被封装在 agent 选择和 build command 选择中。

---

## §9 Failure Modes

### 9.1 硬编码绝对路径导致 hook 失败

**证据**: `hooks/checkpoint-hooks.json:27` — `"command": "node /Users/ah3sh/Developer/everything-claude-code-mobile/scripts/hooks/auto-checkpoint.js standard before-gradle-update"`

**影响**: 所有 checkpoint hook 在非作者机器上会因路径不存在而静默失败（`|| true` 模式）或报错。这意味着检查点系统 — 框架的核心安全网 — 在大多数用户环境下不工作。

**严重性**: Critical — 安全机制名存实亡。

### 9.2 iOS hook 的 Swift 反模式 grep 过于宽泛

**证据**: `hooks/hooks-ios.json:28` — `grep -n 'force unwrap\|!\|DispatchQueue.main.async'`

**影响**: `!` 会匹配所有 Swift 中的逻辑非运算符（`if !isEmpty`）、optional chaining 后的强制解包、以及字符串中的感叹号。误报率极高，用户很快会忽略所有警告。

**严重性**: Medium — 降低 hook 系统的可信度。

### 9.3 DAG 执行顺序无代码强制

**证据**: `commands/feature-implement.md`, `skills/feature-builder/SKILL.md:162-168` — DAG 顺序完全写在 prompt 中。

**影响**: Claude 可能在上下文压缩后忘记依赖顺序，导致 `data-impl` 在 `network-impl` 完成前启动，生成引用不存在 DTO 的代码。

**严重性**: High — 核心编排逻辑无硬执行保障。

### 9.4 Plan JSON 无 schema 校验

**证据**: Plan JSON schema 定义在 `skills/feature-builder/SKILL.md:514-627`，但无 JSON Schema 文件或校验脚本。

**影响**: `feature-planner` agent 生成的 Plan 可能缺少必要字段（如 `dependsOn`），下游 agent 读取时静默跳过或产生错误输出。

**严重性**: Medium — 错误在 pipeline 后期才暴露，调试成本高。

### 9.5 MCP Memory Server 无实现代码

**证据**: `mcp-servers/mobile-memory/`, `mcp-servers/ios-memory/`, `mcp-servers/kmp-context/` — 目录存在但未验证是否包含可运行的 server 实现。`mcp-configs/` 中的 JSON 仅为配置声明。

**影响**: 如果 MCP server 未正确实现或未启动，所有依赖跨会话记忆的功能（instinct 读取、项目模式记忆）将静默降级。

**严重性**: Medium — 功能降级但不阻塞核心 pipeline。

### 9.6 Phase 4 build-fix 循环可能陷入死循环模式

**证据**: `skills/feature-builder/SKILL.md:229-282` — max 5 iterations，但无去重逻辑。

**影响**: 如果修复 A 引入错误 B，修复 B 恢复错误 A，循环会在 A↔B 之间振荡直到耗尽 5 次迭代，浪费时间且最终仍需人工介入。

**严重性**: Low — 有 max iteration 兜底，但用户体验差。

### 9.7 Instinct 学习质量依赖 pattern matcher 准确性

**证据**: `skills/feature-builder/SKILL.md:428-448` — 17 个 pattern matcher 基于文件内容 grep。

**影响**: 简单的文本匹配无法区分 "正确使用 sealed interface" 和 "错误使用 sealed interface"。低质量 instinct 会以 0.5 置信度进入系统，需要多次正确使用才能提升，但错误 instinct 也会缓慢衰减而非被主动纠正。

**严重性**: Low — 衰减机制提供了安全网，但学习效率受限。

---

## §10 Migration Assessment

### 迁移候选机制

| 机制 | 可迁移性 | 工作量 | 前置条件 | 风险 | 优先级 |
|------|----------|--------|----------|------|--------|
| DAG-ordered layer agent 编排 | Direct | M | 多 agent 编排能力 | 需要硬执行 DAG 顺序而非仅靠 prompt | 1 |
| Plan JSON 作为 agent 间协议 | Direct | S | JSON schema 定义 | 需添加 schema 校验 | 2 |
| 三层检查点系统 (quick/standard/full) | Direct | S | hook 系统 | 需使用相对路径 | 3 |
| pass@k 可靠性度量 | Inspired | L | 测试执行环境 | 需要 emulator/device | 4 |
| 7-phase pipeline 结构 | Inspired | L | 完整的 agent 生态 | 过度工程化风险 | 5 |
| Instinct 置信度衰减 | Inspired | M | 持久化存储 | 学习质量依赖 pattern matcher | 6 |
| Platform-specific agent routing | Direct | S | 平台检测逻辑 | 非标准项目结构检测失败 | 7 |
| Parallel reviewer pattern | Direct | S | 多 agent 并行能力 | 需要 finding 去重逻辑 | 3 |

### 推荐采纳顺序

1. **Plan JSON 协议 + Schema 校验** — 最小投入、最大收益。为多 agent 协作建立通信基础。
2. **DAG layer agent 编排** — 核心创新，但必须添加硬执行（脚本检查 dependency 完成状态）而非仅靠 prompt。
3. **三层检查点 + Parallel reviewer** — 低成本的安全网和质量保障。
4. **pass@k 度量** — 有价值但依赖测试环境，适合后期引入。

### Must-Build Enforcement List

如果迁移上述机制，以下执行保障必须从头构建（原框架中缺失）：

1. **Plan JSON schema validator** — 在 Phase 2 开始前校验 Plan 完整性
2. **DAG dependency checker** — 脚本级别检查前置 agent 是否已完成，而非依赖 prompt
3. **Hook 路径解析** — 使用 `${CLAUDE_PLUGIN_ROOT}` 或相对路径替代绝对路径
4. **Instinct quality gate** — 新 instinct 入库前的最低质量检查

---

## §11 Open Questions

1. **MCP server 实现质量**: `mcp-servers/` 下的三个 server 是否有完整实现？README 声称 3 个 MCP server，但未验证其功能完整性。
2. **跨平台 Plan 一致性**: KMP 项目的 Plan JSON 需要同时描述 shared/android/ios 三个 source set，当前 schema 是否足够？
3. **Instinct 冲突解决**: 当两个 instinct 给出矛盾建议时（如 "使用 Room" vs "使用 DataStore"），系统如何选择？当前无冲突解决机制。
4. **Phase 7 学习的实际效果**: 17 个 pattern matcher 的准确率和召回率未知。是否有用户反馈表明学习系统确实改善了后续 feature build？
5. **iOS 平台覆盖深度**: 大部分 agent prompt 和代码示例偏向 Android/Kotlin。iOS 侧的 `DependencyContainer` 实现（`agents/architecture-impl.md:280-321`）使用了 `fatalError` 的 service locator 模式，与 Swift 社区主流的 protocol-based DI 有差距。
6. **与 `everything-claude-code` 的关系**: 两个项目共享多少基础设施？instinct 系统、checkpoint 系统是否可以跨项目共享？

---

## Pre-Submit Checklist

| # | Gate | Pass? |
|---|------|-------|
| A | Source Inventory: 分类为 overview / execution / prompt / enforcement / evolution | ✅ §2 |
| B | Prompt Traceability: 每个主要角色有 catalog entry + `repo_path` + `quote_excerpt` | ✅ §6 |
| C | Object Model: 至少 3 个 first-class entity 有生命周期 | ✅ §3 (Plan, State, Instinct, Checkpoint, Learning Summary) |
| D | State Machine: Phase 有转换，非扁平步骤列表 | ✅ §4 (含失败路径和回退) |
| E | Enforcement Audit: 每个关键约束分类为 Hard / Soft / Unenforced | ✅ §5 (19 条约束) |
| F | Micro + Macro Split: 两个层级的设计亮点均存在 | ✅ §7 (5 micro) + §8 (4 macro) |
| G | Failure Modes: 至少 3 个有证据的失败模式 | ✅ §9 (7 个失败模式) |
| H | Migration Output: 候选机制有评级、采纳顺序、must-build enforcement | ✅ §10 |
