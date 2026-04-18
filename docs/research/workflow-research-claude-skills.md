# claude-skills (tdd) 工作流逆向工程分析报告

> **仓库**: `vendor/claude-skills` (Multi-agent TDD orchestration)
> **规模**: 299 files, Bash scripts + Markdown skill files
> **框架类型**: 多 Agent TDD 编排器 — 严格 Red-Green-Refactor 循环 + DDD/Onion 层级强制
> **分析日期**: 2025-07-22

---

## 目录

1. [框架概况](#1-框架概况)
2. [源清单](#2-源清单)
3. [对象模型](#3-对象模型)
4. [流程与状态机](#4-流程与状态机)
5. [执行保障审计](#5-执行保障审计)
6. [Prompt 目录](#6-prompt-目录)
7. [微观设计亮点](#7-微观设计亮点)
8. [宏观设计亮点](#8-宏观设计亮点)
9. [失败模式与局限](#9-失败模式与局限)
10. [迁移评估](#10-迁移评估)
11. [开放问题](#11-开放问题)

---

## 1. 框架概况

**类型**: 多 Agent TDD 编排框架，通过严格的 Red-Green-Refactor 循环和 DDD/Onion 架构层级约束驱动 AI 生成高质量代码。

这是目前所见的**最重量级** AI 编码工作流框架。不同于大多数框架的"提示词 + 祈祷"模式，claude-skills 在 TDD 的每个阶段都部署了独立的 Agent（Test Writer、Implementer、Refactorer），通过**信息隔离**（每个 agent 只能看到特定上下文切片）和**机械化门禁**（RED 必须失败、GREEN 必须通过、层级边界必须纯净）来对抗 LLM 的固有倾向——跳过测试、绕过约束、写出看起来正确但架构腐烂的代码。

**文件规模**: 299 个文件，核心逻辑由 Bash 脚本实现（`run_tests.sh` 317 行、`extract_api.sh` 249 行、`discover_docs.sh` 10K+ 行），指令层为 Markdown（`tdd/SKILL.md` 744 行主编排器），参考资料层包含 `agent_prompts.md`、`anti_patterns.md`、`framework_configs.md`、`layer_guide.md`。

**入口点**: `tdd/SKILL.md`（744 行），这是 Claude Code 加载的主 skill 文件，包含完整的 6 阶段编排逻辑和所有 agent 的 prompt 模板。

**语言**: Bash（运行时工具脚本）、Markdown（skill 指令与 agent prompts）、Python（测试套件：`test_prompts.py`、`test_run_tests.py`、`test_extract_api.py`）。

**运行模式**:
- `/tdd` — 交互模式，每个阶段暂停等待用户确认
- `/tdd --auto` — 自主模式，自动推进直到完成或触发熔断（5 次实现失败或 3 次回归）
- `/tdd --resume` — 从 `.tdd-state.json` 恢复中断的会话
- `/tdd --dry-run` — 仅执行分析和分解，不写入任何代码

**研究支撑**: 框架的设计决策有明确的实证依据——AI 无约束编码 80% 违反架构规则，静态工具仅检测 77%，test-driven prompting 提升准确率 38-45%，TDD 减少缺陷 40-90%。

---

## 2. 源清单

### 2.1 核心编排

| 路径 | 大小/行数 | 角色 |
|------|-----------|------|
| `tdd/SKILL.md` | 744 行 | 主编排器：6 阶段流程定义、agent prompt 模板、状态管理逻辑 |
| `.tdd-state.json` | 运行时生成 | 状态持久化文件：phase、current_slice、test 结果、文件追踪 |

### 2.2 运行时工具脚本

| 路径 | 大小/行数 | 角色 |
|------|-----------|------|
| `scripts/run_tests.sh` | 317 行 | 万能测试运行器，自动检测并适配 7 种框架：jest, vitest, pytest, go test, cargo test, rspec, phpunit |
| `scripts/extract_api.sh` | 249 行 | 公共 API 表面提取器，解析源文件生成接口签名清单 |
| `scripts/discover_docs.sh` | 10K+ 行 | 文档发现器，递归扫描项目文档并生成结构化摘要 |

### 2.3 参考资料层

| 路径 | 角色 |
|------|------|
| `references/agent_prompts.md` | 三个 Agent（Test Writer、Implementer、Refactorer）的完整 prompt 模板 |
| `references/anti_patterns.md` | 反模式目录：domain importing infrastructure、tautological tests 等 |
| `references/framework_configs.md` | 7 种测试框架的配置指南与最佳实践 |
| `references/layer_guide.md` | DDD/Onion 层级完整指南：依赖规则、Port Interface Rule、违规示例 |

### 2.4 测试套件

| 路径 | 角色 |
|------|------|
| `tests/test_prompts.py` | Prompt snapshot 测试——确保 agent prompt 模板的变更被有意识地审查 |
| `tests/test_run_tests.py` | `run_tests.sh` 的功能测试 |
| `tests/test_extract_api.py` | `extract_api.sh` 的功能测试 |
| `tests/fixtures/` | 测试 fixture 文件 |

---

## 3. 对象模型

### 3.1 一等实体

#### Entity: TDD State (`.tdd-state.json`)

**定义位置**: 运行时由 SKILL.md 编排器创建和维护

TDD State 是整个框架的**中央状态机**。它是一个 JSON 文件，记录了当前 TDD 会话的完整执行状态：

```json
{
  "feature": "user-authentication",
  "framework": "jest",
  "language": "typescript",
  "test_command": "npm test",
  "source_dir": "src/",
  "slices": [
    {
      "id": "slice-1",
      "name": "login-endpoint",
      "layer": "application",
      "status": "green",
      "test_file": "src/__tests__/login.test.ts",
      "impl_files": ["src/application/login.ts"]
    }
  ],
  "current_slice": 1,
  "phase": "GREEN",
  "layer_map": {
    "domain": ["src/domain/"],
    "domain-service": ["src/domain-service/"],
    "application": ["src/application/"],
    "infrastructure": ["src/infrastructure/"]
  },
  "files_modified": [],
  "test_files_created": []
}
```

**关键属性**:
- `feature` — 当前开发的特性名称
- `framework` / `language` / `test_command` — Phase 0 自动检测的环境信息
- `slices` — Phase 1 分解的垂直切片列表，每个切片有独立的 layer、status、和文件追踪
- `current_slice` — 当前正在处理的切片索引
- `phase` — 当前所处的 TDD 阶段（SETUP/DECOMPOSITION/RED/GREEN/REFACTOR/COMPLETE）
- `layer_map` — DDD/Onion 层级到目录的映射
- `files_modified` / `test_files_created` — 文件变更追踪，用于回滚和审计

#### Entity: Slice

**定义位置**: Phase 1 DECOMPOSITION 阶段生成

Slice（垂直切片）是 TDD 循环的原子工作单元。每个 slice 对应一个可独立测试的功能片段，遵循 inside-out by layer 的排序策略：先 domain 层、后 domain-service 层、再 application 层、最后 infrastructure 层。

每个 slice 在生命周期中经历以下状态转换：

```
pending → red → green → refactored
```

#### Entity: Agent (Test Writer / Implementer / Refactorer)

**定义位置**: `tdd/SKILL.md` 内的 prompt 模板 + `references/agent_prompts.md`

三个 Agent 是框架的核心执行者。它们不是持久化的实体，而是**带有严格上下文隔离的 Task subagent 调用**。每次调用时，编排器构造特定的 prompt（包含允许看到的信息），通过 Claude Code 的 Task 工具发起子 agent 会话。

**上下文隔离矩阵** — 这是框架最关键的设计：

| 信息 | Test Writer | Implementer | Refactorer |
|------|-------------|-------------|------------|
| Slice spec（切片规格） | ✅ 可见 | ❌ 不可见 | ❌ 不可见 |
| Public API surface | ✅ 可见 | ❌ 不可见 | ❌ 不可见 |
| Framework skeleton | ✅ 可见 | ❌ 不可见 | ❌ 不可见 |
| Layer constraints | ✅ 可见 | ❌ 不可见 | ❌ 不可见 |
| Documentation | ✅ 可见 | ❌ 不可见 | ❌ 不可见 |
| Implementation code | ❌ **不可见** | ✅ 可见 | ✅ 可见 |
| Failing test | ❌ 不可见 | ✅ 可见 | ❌ 不可见 |
| Test error output | ❌ 不可见 | ✅ 可见 | ❌ 不可见 |
| File tree | ❌ 不可见 | ✅ 可见 | ✅ 可见 |
| Existing source | ❌ 不可见 | ✅ 可见 | ✅ 可见 |
| All tests + impl | ❌ 不可见 | ❌ 不可见 | ✅ 可见 |
| Green test results | ❌ 不可见 | ❌ 不可见 | ✅ 可见 |
| Original spec | ❌ 不可见 | ❌ **不可见** | ❌ **不可见** |

**关键隔离洞察**:
- **Test Writer 看不到实现代码**：防止测试被实现细节污染，强制测试只依赖公共 API 契约。
- **Implementer 看不到原始 spec**：防止 Implementer 绕过测试直接从 spec 实现，强制其唯一目标是让失败的测试通过。
- **Refactorer 看不到原始 spec**：防止 Refactorer 引入新功能，强制其只做结构改善。

这种"故意致盲"（intentional blinding）是对 AI agent 的**制度性不信任**的工程化表达。

#### Entity: Layer (DDD/Onion Architecture)

**定义位置**: `references/layer_guide.md`

四层 DDD/Onion 架构是 TDD 流程的架构脊柱：

```
domain (无外部依赖)
  → domain-service (仅依赖 domain)
    → application (依赖 domain + domain-service)
      → infrastructure (可依赖所有层)
```

**Port Interface Rule**: 接口由消费者定义，而非提供者。Application 层定义 Repository 接口，Infrastructure 层实现它。这确保了依赖方向始终向内。

每个 slice 被分配到一个 layer，layer 分配决定了：
- 允许导入的模块范围
- 测试中允许使用的 mock 对象
- 文件放置的目录位置

### 3.2 实体关系

```
TDD State (.tdd-state.json)
  ├── Feature (当前开发特性)
  ├── Environment (framework, language, test_command)
  ├── Layer Map (DDD/Onion 目录映射)
  └── Slices[] (垂直切片列表)
        ├── Slice → Test Writer Agent (RED phase)
        ├── Slice → Implementer Agent (GREEN phase)
        └── Slice → Refactorer Agent (REFACTOR phase)

Scripts (运行时工具)
  ├── run_tests.sh (通用测试执行)
  ├── extract_api.sh (API 表面提取)
  └── discover_docs.sh (文档发现)
```

**上下文隔离**: 每个 Agent 通过 Task subagent 调用获得独立的上下文窗口。编排器（SKILL.md）是唯一拥有全局视图的实体——它看到所有 slice 的状态、所有 agent 的输出、和完整的 layer map。Agent 之间**无法直接通信**，所有信息传递必须经过编排器的过滤。

---

## 4. 流程与状态机

### 4.1 主状态机：6 阶段 TDD 循环

```
Phase 0: SETUP
  │  ← 检测框架 (jest/vitest/pytest/go/cargo/rspec/phpunit)
  │  ← 验证 green baseline (现有测试必须全部通过)
  │  ← extract_api.sh → 提取公共 API 表面
  │  ← discover_docs.sh → 发现项目文档
  │  ← 创建 .tdd-state.json
  ▼
Phase 1: DECOMPOSITION
  │  ← 垂直切片分解 (vertical slicing)
  │  ← inside-out by layer 排序 (domain → domain-service → application → infrastructure)
  │  ← 用户审批 (交互模式) 或自动继续 (--auto 模式)
  ▼
Phase 2: RED (per slice)
  │  ← 刷新 API surface (extract_api.sh)
  │  ← 构造 Test Writer prompt (注入: slice spec, API, framework, layer constraints, docs)
  │  ← 调用 Task subagent (Test Writer)
  │  ← 写入测试文件
  │  ← Lint 检查 (assertion roulette, tautologies, domain mock 检测)
  │  ← 运行测试 → **必须 FAIL** (且失败原因必须是 assertion error，非 import error)
  │  ← 若通过 → 回退，重新生成测试
  ▼
Phase 3: GREEN (per slice)
  │  ← 构建 file tree
  │  ← 构造 Implementer prompt (注入: failing test, error output, file tree, existing source)
  │  ← 调用 Task subagent (Implementer)
  │  ← 验证 layer boundary (禁止跨层导入)
  │  ← 应用变更
  │  ← 运行特定测试 → **必须 PASS**
  │  ← 若失败 → 重试 (最多 5 次)
  │  ← 运行完整测试套件 → **全部 PASS** (无回归)
  │  ← Layer purity check (全仓库 import 扫描)
  │  ← 若回归 → 回滚本次变更，重新开始 GREEN
  ▼
Phase 4: REFACTOR (全局)
  │  ← 收集所有实现代码和测试
  │  ← 构造 Refactorer prompt (注入: all impl + tests, green results, layers)
  │  ← 调用 Task subagent (Refactorer)
  │  ← 逐个应用重构建议，每个建议后执行: lint + test gate
  │  ← 任何建议导致测试失败 → 立即 revert 该建议
  │  ← Refactorer 检查直接 + 传递依赖
  ▼
Phase 5: COMPLETE
     ← 汇总所有变更
     ← 输出最终报告
```

### 4.2 Slice 级状态机

```
pending ──→ red ──→ green ──→ refactored
   │          │        │
   │          │        └── GREEN 失败 (5次重试耗尽) → BLOCKED
   │          │
   │          └── RED 测试意外通过 → 回退重写
   │
   └── DECOMPOSITION 阶段分配
```

### 4.3 自动模式 (--auto) 的熔断机制

```
自主推进循环
  → 5 次 implementation 失败 → 熔断，停止执行
  → 3 次 regression (全套件回归) → 熔断，停止执行
  → 正常完成所有 slices → Phase 5 COMPLETE
```

### 4.4 失败路径与恢复

| 失败场景 | 系统行为 | 恢复策略 |
|----------|----------|----------|
| Phase 0: green baseline 失败 | 中止，要求先修复现有测试 | 修复后 `/tdd --resume` |
| Phase 2: RED 测试意外通过 | 丢弃测试，重新生成 | 自动重试 |
| Phase 2: RED 失败原因是 import error | 拒绝，要求 assertion-based failure | 自动重试 |
| Phase 2: Lint 检测到 tautological test | 拒绝测试，重新生成 | 自动重试 |
| Phase 3: GREEN 实现不通过 | 重试最多 5 次 | 5 次耗尽 → slice blocked |
| Phase 3: 全套件回归 | 回滚本次变更 | 重新开始该 slice 的 GREEN |
| Phase 3: Layer boundary violation | 拒绝变更 | 重新生成（提示层级约束） |
| Phase 4: 重构导致测试失败 | 立即 revert 该重构建议 | 继续尝试下一个建议 |
| --auto 模式: 5 impl failures | 熔断，输出诊断信息 | `/tdd --resume` |
| --auto 模式: 3 regressions | 熔断，输出诊断信息 | `/tdd --resume` |
| 会话中断（崩溃/超时） | `.tdd-state.json` 保留进度 | `/tdd --resume` |

---

## 5. 执行保障审计

### 5.1 强制矩阵

| 声明/约束 | Hard (代码强制) | Soft (Prompt 指令) | Unenforced (仅文档) |
|-----------|----------------|-------------------|---------------------|
| RED 阶段测试必须失败 | ✅ run_tests.sh 验证 exit code ≠ 0 | | |
| RED 失败必须是 assertion error | ✅ 检查错误输出模式匹配 | | |
| GREEN 阶段特定测试必须通过 | ✅ run_tests.sh 验证 exit code = 0 | | |
| GREEN 阶段全套件无回归 | ✅ 完整 test suite 运行验证 | | |
| Layer boundary（层级边界） | ✅ 全仓库 import 扫描 | | |
| Domain purity（domain 无外层导入） | ✅ import 静态分析 | | |
| Post-RED lint（assertion roulette 等） | ✅ lint 规则自动检测 | | |
| Test Writer 看不到实现代码 | ✅ prompt 构造时物理排除 | | |
| Implementer 看不到原始 spec | ✅ prompt 构造时物理排除 | | |
| Refactorer 看不到原始 spec | ✅ prompt 构造时物理排除 | | |
| 最多 5 次 GREEN 重试 | ✅ 计数器强制 | | |
| --auto 熔断 (5 failures / 3 regressions) | ✅ 计数器强制 | | |
| Inside-out slice 排序 | | ⚠️ Prompt 建议 | |
| Port Interface Rule | | ⚠️ layer_guide.md 文档 | |
| 禁止 Active Record 模式 | | | ❌ anti_patterns.md 仅列出 |
| 禁止 domain 层 mocking | | ⚠️ Post-RED lint 部分检测 | |
| 单 slice 原子性 | | ⚠️ 编排逻辑暗示 | |
| Refactorer 检查传递依赖 | | ⚠️ Prompt 指令 | |

### 5.2 审计总结

**Hard enforcement 覆盖**: 极为全面。TDD 循环的每个关键门禁都有代码级强制：RED 必须失败（且是正确类型的失败）、GREEN 必须通过（包括全套件回归检查）、layer boundary 有全仓库 import 扫描、agent 上下文隔离通过 prompt 构造物理实现。

**Soft enforcement（Prompt 驱动）**: Inside-out slice 排序和 Port Interface Rule 依赖 prompt 指令而非代码验证。Agent 可能不遵循建议的排序策略——但由于 slice 分解在 Phase 1 由用户审批（交互模式），这是可接受的。

**关键发现**: 这是所有已分析框架中 **hard enforcement 比例最高的一个**。核心原因是 TDD 循环本身就是一个可机械验证的协议——"测试通过/失败"是二元判断，不需要 LLM 的主观解释。框架巧妙地将所有关键约束都转化为了可自动验证的二元条件。

**与 1st-cc-plugin 对比**: 我们的 `quality/testing` 插件实现了 Red-Green-Refactor gates，但缺少 claude-skills 的三大关键能力：(1) agent 上下文隔离、(2) layer boundary 自动验证、(3) 全仓库 import 扫描。

---

## 6. Prompt 目录

### 6.1 Test Writer Agent Prompt（核心片段）

Test Writer 是 RED 阶段的执行者。其 prompt 的关键设计在于**只注入契约信息，排除实现信息**：

```markdown
## Your Role
You are a Test Writer. You write tests for a feature slice based ONLY on:
- The slice specification (what this slice should do)
- The public API surface (extracted by extract_api.sh)
- The testing framework skeleton
- Layer constraints (which layer this slice belongs to)
- Project documentation

## CRITICAL CONSTRAINTS
- You MUST NOT see or reference any implementation code
- Your tests must fail with ASSERTION ERRORS, not import errors
- Do not write tautological tests (tests that always pass)
- Do not mock domain objects
- Do not test implementation details — test behavior through public API
- Each test must have exactly ONE assertion (no assertion roulette)
```

**设计洞察**: "MUST NOT see implementation code" 不是靠 LLM 自律实现的——编排器在构造 prompt 时就物理排除了实现文件的内容。这是**architectural enforcement**，不是 prompt engineering。

### 6.2 Implementer Agent Prompt（核心片段）

Implementer 是 GREEN 阶段的执行者。其 prompt 的关键设计在于**只注入失败测试和项目结构，排除规格说明**：

```markdown
## Your Role
You are an Implementer. Your ONLY goal is to make the failing test pass.
You receive:
- The failing test file and its error output
- The project file tree
- Existing source code in relevant directories

## CRITICAL CONSTRAINTS
- You do NOT have access to the original feature specification
- Write the MINIMUM code to make the failing test pass
- Respect layer boundaries:
  - domain: NO external dependencies
  - domain-service: may import domain only
  - application: may import domain + domain-service
  - infrastructure: may import all layers
- Do not add functionality beyond what the test requires
```

**设计洞察**: "Your ONLY goal is to make the failing test pass" 是对经典 TDD GREEN 阶段的精确翻译。排除原始 spec 防止了 Implementer 偷看答案——它必须纯粹从测试反推实现，这正是 TDD 的核心价值。

### 6.3 反模式检测 Prompt（Post-RED Lint）

```markdown
## Post-RED Quality Gates
After Test Writer produces tests, verify:
1. NO assertion roulette — each test has exactly ONE expect/assert
2. NO tautological assertions — e.g., expect(true).toBe(true)
3. NO mocking in domain layer tests — domain is pure, no mocks needed
4. Failure MUST be assertion-based — import errors mean the test is broken, not failing correctly
5. Tests must be independent — no shared mutable state between tests
```

---

## 7. 微观设计亮点

### 7.1 "故意致盲" (Intentional Blinding) 的上下文隔离

这是框架最具创新性的设计。三个 Agent 的上下文隔离不是安全措施——它是**认知约束工程**。

- **Test Writer 看不到实现** → 测试成为独立于实现的契约文档
- **Implementer 看不到 spec** → 实现成为测试的最小满足，避免过度工程
- **Refactorer 看不到 spec** → 重构仅限于结构改善，不会引入新功能

这种设计的深层逻辑是：LLM 在看到所有信息时会走捷径。如果 Test Writer 看到了实现代码，它会写出"验证现有代码"的测试而非"定义期望行为"的测试。如果 Implementer 看到了 spec，它会直接从 spec 实现而非让测试驱动实现。

框架用物理信息隔离替代了提示词层面的"请不要看这个"——这是对 LLM 不可靠性的正确工程回应。

### 7.2 万能测试运行器 (run_tests.sh)

`run_tests.sh`（317 行）是一个精心设计的**框架无关测试执行层**。它自动检测项目使用的测试框架（jest、vitest、pytest、go test、cargo test、rspec、phpunit），然后用统一的接口执行测试并返回标准化的结果。

这个设计的价值在于：编排器（SKILL.md）不需要关心具体的测试框架——它只需要 "运行测试，告诉我通过还是失败"。这是一个经典的 **Adapter Pattern** 应用，将 7 种异构的测试框架统一为一个二元输出接口。

### 7.3 Post-RED Lint 质量门禁

RED 阶段不是"测试写完就行"——框架在测试文件生成后执行了一套静态分析：

- **Assertion roulette 检测**: 每个测试用例是否只有一个断言
- **Tautological assertion 检测**: 是否存在 `expect(true).toBe(true)` 这样的无意义断言
- **Domain mock 检测**: domain 层测试是否错误地使用了 mock（domain 层应该是纯净的，无需 mock）

这些检查针对的都是 LLM 生成测试时的**典型病理行为**——生成看起来像测试但实际上不验证任何东西的代码。

---

## 8. 宏观设计亮点

### 8.1 制度性不信任 (Institutional Distrust)

claude-skills 的设计哲学可以用一句话概括：**不信任 AI agent 的自律性，用机械化约束替代提示词承诺**。

这与大多数 AI 工作流框架形成鲜明对比。典型框架的做法是：在 prompt 中写 "请遵循 TDD" "请不要跳过测试" "请保持层级纯净"，然后希望 LLM 遵守。claude-skills 的做法是：

1. 让 agent 物理上看不到它不应该看到的信息（上下文隔离）
2. 在每个关键节点用代码验证输出（RED 必须失败、GREEN 必须通过）
3. 用全仓库 import 扫描替代"请不要跨层导入"的提示（layer boundary enforcement）
4. 用计数器和熔断器替代"请在失败时停止"的请求（--auto 模式）

这种哲学的实证依据是：AI 无约束编码 80% 违反架构规则。框架的每一个 hard enforcement 都是对一个已知 AI 失败模式的工程化对策。

### 8.2 TDD 作为可验证协议

TDD 之所以特别适合 AI 编码的约束框架，是因为它的每个步骤都可以**机械化验证**：

- "测试必须失败" → exit code ≠ 0
- "测试必须通过" → exit code = 0
- "层级边界纯净" → import 语句的正则匹配
- "没有回归" → 全套件 exit code = 0

相比之下，"代码质量好" "架构合理" "命名清晰" 这些约束是不可机械验证的。claude-skills 的智慧在于：选择了一个**自带验证机制的开发方法论**（TDD），然后将其每个步骤的验证条件编码为自动化门禁。

这使得框架的 hard enforcement 比例远超其他已分析的框架——因为 TDD 给了它一个可以自动验证的"锚点"。

---

## 9. 失败模式与局限

### 9.1 744 行单文件编排器的可维护性

**严重程度**: 高

`tdd/SKILL.md` 包含 744 行内容，融合了 6 阶段流程逻辑、3 个 agent 的 prompt 模板、状态管理规则、和错误处理策略。这是一个**God Object**——所有编排逻辑集中在一个文件中。

修改任何一个阶段的行为都需要编辑这个文件。Prompt 模板的变更可能意外影响流程逻辑（因为它们用 Markdown 标题分隔，而非文件边界）。测试套件中的 `test_prompts.py`（prompt snapshot 测试）部分缓解了这个风险，但无法防止逻辑层面的回归。

### 9.2 Bash 脚本的脆弱性

**严重程度**: 中

核心工具（`run_tests.sh` 317 行、`extract_api.sh` 249 行、`discover_docs.sh` 10K+ 行）全部用 Bash 实现。Bash 在错误处理、字符串操作和跨平台兼容性方面存在固有弱点：

- `run_tests.sh` 的 7 框架检测依赖文件存在性检查（如 `package.json` 中是否有 `jest`），误判风险存在
- `discover_docs.sh` 10K+ 行的 Bash 脚本是维护噩梦
- 路径中的空格、特殊字符、非 ASCII 文件名可能导致意外行为

### 9.3 Layer Boundary 检测的有限性

**严重程度**: 中

Layer boundary 验证通过 import 语句的模式匹配实现（检查 domain 层文件是否导入了 infrastructure 层模块）。但这种静态分析有盲区：

- 动态导入（`require()` with variable、`importlib.import_module()`）无法检测
- 间接依赖通过中间层的"合法"导入传递违规（transitive dependency 部分依赖 prompt 而非代码检测）
- 反射和依赖注入框架可以绕过 import 层面的检查

### 9.4 Inside-Out 排序的 Prompt 依赖

**严重程度**: 低-中

Slice 的 inside-out by layer 排序（domain → domain-service → application → infrastructure）仅由 prompt 建议，非代码强制。如果 LLM 在 DECOMPOSITION 阶段将 infrastructure slice 排在 domain slice 之前，框架不会阻止——后续的 layer boundary check 可能发现问题，但错误的排序已经浪费了 RED-GREEN 循环的资源。

### 9.5 --auto 模式的熔断阈值固定

**严重程度**: 低

5 次 implementation 失败和 3 次 regression 的熔断阈值是硬编码的。对于简单特性，这个阈值可能过于宽松（浪费了 4 次重试）；对于复杂特性，可能过于严格（一个困难的 slice 可能需要 7+ 次尝试）。缺少自适应阈值机制。

### 9.6 无并行 Slice 执行

**严重程度**: 中

所有 slice 严格串行执行（Phase 2-3 per slice）。对于不存在依赖关系的 slice（如两个独立的 domain 层 slice），理论上可以并行执行 RED-GREEN 循环。当前设计未利用这一优化机会。

### 9.7 Framework 检测的边界情况

**严重程度**: 低

`run_tests.sh` 的框架自动检测覆盖 7 种主流框架，但不覆盖：
- Monorepo 中的多框架项目（如前端 jest + 后端 pytest）
- 自定义测试框架或 wrapper
- 编译型语言的测试依赖构建步骤（如 cargo test 需要先 cargo build）

---

## 10. 迁移评估

### 10.1 迁移候选

| 候选 | 来源 | 价值 | 迁移复杂度 | 优先级 |
|------|------|------|------------|--------|
| Agent 上下文隔离模式 | 三 Agent 隔离矩阵 | 为 1st-cc-plugin 的 TDD skill 增加"故意致盲"能力，大幅提升测试质量 | 中（需重构 prompt 构造逻辑） | **P0** |
| Layer Boundary Enforcement | import 扫描脚本 | 为 quality/testing 增加自动化架构约束验证 | 中（需适配多语言 import 模式） | **P1** |
| Post-RED Lint 门禁 | assertion roulette / tautology 检测 | 直接提升 AI 生成测试的质量 | 低（规则明确，可快速实现） | **P1** |
| run_tests.sh 万能测试运行器 | scripts/run_tests.sh | 为 quality/testing 提供框架无关的测试执行层 | 低（直接适配或重写） | **P2** |
| Anti-pattern 目录 | references/anti_patterns.md | 丰富 quality/ai-hygiene 的检测规则库 | 极低（内容级迁移） | **P2** |
| .tdd-state.json 状态持久化 | 状态机设计 | 为 workflows/deep-plan 增加中断恢复能力 | 中（需定义通用状态 schema） | **P3** |
| --auto 熔断机制 | 计数器 + 阈值 | 为所有自主模式 skill 提供安全网 | 低 | **P2** |
| DDD/Onion Layer Guide | references/layer_guide.md | 作为 quality/testing 或 quality/refactor 的参考资源 | 极低（文档级迁移） | **P3** |

### 10.2 推荐采纳顺序

**第一优先级：Agent 上下文隔离 + Post-RED Lint**

这两个能力的组合可以直接升级 `quality/testing` 插件。当前的 testing skill 执行 Red-Green-Refactor 循环，但 agent 可以看到所有信息——这意味着 Test Writer 可能写出基于实现的测试、Implementer 可能绕过测试直接从 spec 实现。引入上下文隔离后，TDD 循环的纪律性将质的飞跃。

Post-RED Lint 是低成本高收益的补充：assertion roulette 和 tautological test 检测可以在现有 testing skill 中快速实现，直接拦截 LLM 最常见的测试生成病理。

**实现路径**: 在 `quality/testing/SKILL.md` 中重构 agent 调用逻辑，为 Test Writer 和 Implementer 构造隔离的 prompt。新增 `quality/testing/references/test-lint-rules.md` 定义 lint 规则。

**第二优先级：Layer Boundary + 万能测试运行器**

Layer boundary enforcement 需要与现有的 `quality/refactor` 插件协同——refactor skill 在重构时需要验证不引入层级违规。万能测试运行器可以作为 `quality/testing` 的底层工具，替代当前可能存在的框架特定逻辑。

**第三优先级：状态持久化 + 反模式目录**

`.tdd-state.json` 的状态持久化模式可以泛化为通用的 "workflow state" 机制，服务于 `workflows/deep-plan` 和 `workflows/superpower` 等需要中断恢复的工作流。Anti-pattern 目录可以直接融入 `quality/ai-hygiene` 的检测规则库。

### 10.3 不建议迁移

- **discover_docs.sh (10K+ 行 Bash)**: 过于庞大且与特定项目结构耦合。1st-cc-plugin 的 `integrations/code-context` 已有更优雅的文档发现方案。
- **完整的 6 阶段流程**: 直接搬运 744 行 SKILL.md 是 God Object 的复制。应提取核心模式（上下文隔离、门禁验证）而非完整流程。
- **DDD/Onion 强制为默认架构**: 不是所有项目都使用 Onion 架构。应将 layer guide 作为可选参考资源，而非强制约束。

---

## 11. 开放问题

1. **上下文隔离的泄露风险？** Test Writer 的 prompt 排除了实现代码，但如果测试框架的配置文件（如 `jest.config.js`）中包含了实现路径或 alias，Test Writer 是否会间接获得实现信息？prompt 构造逻辑是否足够严密？

2. **Layer boundary 检测的语言覆盖范围？** 当前的 import 扫描逻辑是否覆盖了所有 7 种支持框架的语言？Python 的 `from ... import`、Go 的 `import (...)`、Rust 的 `use` 和 TypeScript 的 `import` 语法都需要不同的 pattern matching 规则。

3. **Prompt snapshot 测试的维护成本？** `test_prompts.py` 对 agent prompt 做快照测试，这意味着任何 prompt 微调都需要更新快照。这是否会导致 prompt 优化的摩擦？快照测试是否区分"结构性变更"（需要审查）和"措辞优化"（可自动接受）？

4. **extract_api.sh 的准确性？** 公共 API 表面提取依赖静态分析（正则匹配导出的函数/类签名）。对于动态语言（Python、Ruby），exported API 不一定通过 `export` 关键字声明。错误的 API surface 会导致 Test Writer 写出无法编译的测试。

5. **多语言项目的 layer map 配置？** `.tdd-state.json` 的 `layer_map` 将 DDD 层级映射到目录路径。对于混合语言项目（如 TypeScript 前端 + Go 后端），是否支持多套 layer map？还是假设项目为单语言？

6. **Refactorer 的传递依赖检查如何实现？** Refactorer 声称检查直接和传递依赖，但这是 prompt 指令还是代码强制？传递依赖分析在 Bash 脚本中实现的可靠性如何？

7. **与 IDE 测试工具的集成？** 框架完全通过 CLI（`run_tests.sh`）执行测试。是否有与 IDE 的 test runner（如 VS Code Test Explorer、IntelliJ test runner）集成的路径？IDE 集成可以提供更好的调试体验。
