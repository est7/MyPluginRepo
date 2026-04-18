# Workflow Research Report: lean-spec

> **研究日期**: 2025-07  
> **仓库**: lean-spec  
> **文件数**: ~1559  
> **许可证**: 未明确声明  

---

## 1. 框架概况

LeanSpec 是一个 **tool-agnostic spec framework**，为 Spec-Driven Development (SDD) 提供可插拔的后端适配器架构。核心理念是 "Your workflow, not ours"——不强制特定工作流后端，而是通过 Adapter trait 支持 Markdown 文件、GitHub Issues、Azure DevOps、Jira、Linear 等多种 backend。框架以 **Rust** (core) + **TypeScript** (UI/CLI) 双语言构建，注重 context economy 和 progressive growth。

| 属性 | 值 |
|------|------|
| **类型** | Tool-Agnostic Spec Framework (npm package) |
| **语言** | Rust (core, leanspec-core) + TypeScript (CLI, UI, tooling) |
| **入口** | `npx leanspec` CLI / MCP Server (Axum HTTP) |
| **核心模块** | `rust/leanspec-core/src/` (adapter, validators, relationships) |
| **Backend 支持** | Markdown (完整), GitHub Issues (WIP), Azure DevOps, Jira, Linear (planned) |
| **i18n** | zh-Hans (中文简体) 完整翻译 |
| **文档站** | Docusaurus + live examples |

---

## 2. 源清单

| 文件/目录 | 用途 | 重要度 |
|-----------|------|--------|
| `rust/leanspec-core/src/adapters/mod.rs` | Adapter trait 定义 + SemanticHint | ★★★ |
| `rust/leanspec-core/src/adapters/markdown.rs` | Markdown adapter 完整实现 (1000+ 行) | ★★★ |
| `rust/leanspec-core/src/adapters/registry.rs` | Adapter 配置解析与注册 | ★★★ |
| `rust/leanspec-core/src/types/spec.rs` | Spec 数据模型 (frontmatter, status lifecycle) | ★★★ |
| `rust/leanspec-core/src/validators/` | 全局校验器 (frontmatter, structure, token count) | ★★★ |
| `rust/leanspec-core/src/relationships.rs` | 依赖关系 + 循环检测 | ★★☆ |
| `rust/leanspec-core/src/error.rs` | ErrorCode enum + StructuredError | ★★☆ |
| `packages/cli/src/` | TypeScript CLI 入口 | ★★☆ |
| `.github/workflows/ci.yml` | 双语言 CI (Node.js + Rust) | ★★☆ |
| `docs-site/i18n/zh-Hans/` | 中文本地化文件 | ★☆☆ |

---

## 3. 对象模型

### 核心实体

```
SpecItem (Adapter-Neutral)
  ├── id: string              # adapter-native ID ("123-my-spec", "#42")
  ├── title: string
  ├── body: string            # Markdown content
  ├── url: Option<string>     # backend URL
  ├── metadata: HashMap<String, MetadataValue>  # 动态元数据
  ├── links: ItemLink[]       # 关系链接
  └── raw: Option<JSON>       # adapter-specific 原始数据

MetadataValue (类型安全的动态值)
  ├── Null | String | Bool | Number
  ├── StringList(Vec<String>)
  └── Timestamp(DateTime<Utc>)

Adapter (trait, 核心抽象)
  ├── capabilities() → AdapterCapabilities
  ├── list(filter) → Vec<SpecItem>
  ├── get(id) → SpecItem
  ├── create(req) → SpecItem
  ├── update(id, req) → SpecItem
  ├── delete(id) → ()
  ├── search(query, opts) → Vec<SearchHit>
  └── get_links(id) → Vec<ItemLink>

AdapterCapabilities
  ├── name: string            # "markdown", "github", "ado"
  ├── supports_create/update/delete/search/webhooks: bool
  ├── metadata_fields: MetadataFieldSpec[]  # 动态 schema 声明
  └── link_types: Vec<string> # 支持的关系类型

SemanticHint (跨 adapter 语义映射)
  └── Status | Priority | Tags | Assignee | DueDate ...
```

### Markdown-Specific 模型

```
SpecFrontmatter
  ├── status: SpecStatus (draft → planned → in-progress → complete → archived)
  ├── created: string (YYYY-MM-DD)
  ├── priority: Option<SpecPriority> (low|medium|high|critical)
  ├── tags: Vec<string>
  ├── depends_on: Vec<string>   # spec ID 引用
  ├── parent: Option<string>    # umbrella spec
  ├── assignee, reviewer, issue, pr, epic: Option<string>
  ├── transitions: StatusTransition[]  # 状态变更历史
  └── custom: HashMap<String, JSON>    # 可扩展字段

StatusTransition
  ├── status: SpecStatus
  └── at: DateTime<Utc>
```

### 实体关系

- **SpecItem** 通过 `links` (parent/child/depends_on) 形成 DAG
- **Adapter** 声明 **AdapterCapabilities**，SpecItem 的 metadata 字段由 adapter 动态定义
- **SemanticHint** 跨 adapter 映射（markdown "status" = GitHub "state" = ADO "State"）

### Context 隔离

每个 backend adapter 独立实现 Adapter trait，共享 SpecItem 数据模型。不同 backend 通过 `raw` 字段保留 adapter-specific 数据，互不干扰。

---

## 4. 流程与状态机

### Spec Lifecycle

```
┌──────────┐
│  DRAFT   │  ← 新建 spec 的初始状态
└────┬─────┘
     ↓
┌──────────┐
│ PLANNED  │  ← 设计阶段
└────┬─────┘
     ↓
┌──────────────┐
│ IN-PROGRESS  │  ← 实现阶段
└────┬─────────┘
     ↓
┌──────────┐
│ COMPLETE │  ← 完成 (测试通过, PR merged)
└────┬─────┘
     ↓
┌──────────┐
│ ARCHIVED │  ← 取消 / 已被替代
└──────────┘
```

### SDD Workflow

```
1. DISCOVER  → 查找已有 spec (避免重复)
2. DESIGN    → 编写精简 spec (≤300 行, <2K tokens)
3. IMPLEMENT → AI/开发者根据 spec 编码
4. VALIDATE  → 对照 spec 验证测试
5. PUBLISH   → 标记 complete, merge PR
```

### Happy Path (Markdown Backend)

```
[用户] leanspec create "Auth Module"
   ↓
[系统] 生成 specs/001-auth-module/README.md (frontmatter: status=draft)
   ↓
[用户/AI] 编写 spec 内容 → leanspec update 001 --status planned
   ↓
[系统] 记录 StatusTransition {status: planned, at: now}
   ↓
[开发] 实现 → leanspec update 001 --status in-progress
   ↓
[验证] 测试通过 → leanspec update 001 --status complete
   ↓
[归档] leanspec update 001 --status archived (如需)
```

### Failure Paths

| 失败场景 | 系统响应 |
|----------|----------|
| Circular dependency | `validate_dependency_addition` 拒绝，返回 CircularDependency error |
| Token limit exceeded | TokenCountValidator 拒绝，返回 TokenLimitExceeded error |
| Invalid frontmatter | FrontmatterValidator 返回具体字段错误 |
| Backend 不支持操作 | AdapterCapabilities 声明 `supports_create: false`，CLI 级别拦截 |

---

## 5. 执行保障审计

| 机制 | 级别 | 说明 |
|------|------|------|
| Adapter trait 类型约束 | **Hard** | Rust 编译期强制所有 backend 实现相同接口 |
| Circular Dependency Detection | **Hard** | `validate_dependency_addition` 阻止循环依赖 |
| Token Count Validation | **Hard** | Spec 超过 token 阈值时拒绝创建/更新 |
| Frontmatter Validation | **Hard** | 必填字段 (status, created) 缺失时报错 |
| Structure Validation | **Hard** | 目录结构 + 文件命名格式校验 |
| SemanticHint 跨 backend 映射 | **Soft** | 依赖 adapter 实现的正确性，无编译期保证 |
| Status Transition 自动记录 | **Hard** | 每次 status 变更自动追加 StatusTransition |
| CI TypeScript Binding 校验 | **Hard** | `git diff --exit-code` 确保 Rust→TS 类型同步 |
| Spec 内容质量 | **Unenforced** | 无自动检查 spec 内容是否充分 |

---

## 6. Prompt 目录

### Prompt 1: SDD Workflow Guidance

```
Spec-Driven Development 流程:
1. DISCOVER — 在 specs/ 中搜索已有 spec，避免重复
2. DESIGN — 编写 minimal spec (≤300 行, 5-10 分钟可读完)
3. IMPLEMENT — 根据 spec 实现，保持精简
4. VALIDATE — 对照 spec 验证
5. PUBLISH — 标记 complete

Context Economy 原则:
- Spec ≤ 300 行
- < 2K tokens
- Progressive disclosure: 从简单开始，按需增加结构
```

### Prompt 2: AI Agent Integration (MCP)

```
可用工具:
- leanspec:list — 列出所有 spec
- leanspec:get <id> — 获取 spec 详情
- leanspec:create <title> — 创建新 spec
- leanspec:update <id> --status <status> — 更新状态
- leanspec:search <query> — 全文搜索

开始编码前，先 DISCOVER 是否有相关 spec。
```

---

## 7. 微观设计亮点

### 7.1 SemanticHint 跨 Backend 语义映射

`SemanticHint` enum 将不同 backend 的字段名映射到统一语义——markdown 的 "status"、GitHub Issues 的 "state"、ADO 的 "State" 都映射到 `SemanticHint::Status`。这使上层 CLI/UI 无需关心底层 backend 的字段命名差异。

### 7.2 Adjacently-Tagged JSON Serialization

`MetadataValue` 使用 `{kind: "string", value: "draft"}` 格式序列化，避免了 untagged union 在 JSON round-trip 中的类型歧义问题。这是 Rust serde 生态中的一个重要实践。

### 7.3 Status Transition 自动追踪

每次 spec 状态变更时自动追加 `StatusTransition` 记录到 frontmatter 的 `transitions` 数组。这为 velocity tracking 和 cycle time analysis 提供了零成本的数据基础。

---

## 8. 宏观设计亮点

### 8.1 "Your Workflow, Not Ours" 的 Adapter 哲学

多数 spec 框架强制一种 backend（如 "必须用 GitHub Issues"）。LeanSpec 通过 Adapter trait 实现了真正的 backend 无关性——用户可以从 Markdown 文件开始，随着团队成长迁移到 GitHub Issues 或 Jira，无需重写 spec。

### 8.2 Rust Core + TypeScript Shell 的双语言架构

将不可妥协的核心逻辑（validation、dependency graph、adapter trait）用 Rust 编写确保了类型安全和性能，而用 TypeScript 编写用户界面层（CLI、Web UI）确保了开发效率。通过 ts-rs 自动生成 TypeScript bindings，并在 CI 中验证 binding 是否已提交，消除了双语言架构中常见的类型漂移问题。

---

## 9. 失败模式与局限

| # | 失败模式 | 严重度 | 说明 |
|---|----------|--------|------|
| 1 | **Adapter 实现差异** | 高 | 不同 backend adapter 的功能差异大（markdown 支持所有操作，GitHub Issues 可能不支持 search），用户迁移时可能遇到功能缺失 |
| 2 | **Non-Markdown adapter 成熟度** | 高 | GitHub Issues、Jira、Linear adapter 仍为 WIP 或 planned，当前仅 Markdown 可用 |
| 3 | **Spec 内容质量无检查** | 中 | 结构和格式有 validator，但 spec 内容是否充分、是否有歧义无自动检测 |
| 4 | **Dual-language 构建复杂度** | 中 | Rust + TypeScript + Nix 三层工具链，新贡献者上手成本高 |
| 5 | **Context Economy 依赖纪律** | 低 | "≤300 行" 建议无 hard enforcement（token validator 阈值可配置但默认宽松） |
| 6 | **i18n 覆盖不完整** | 低 | zh-Hans 翻译主要覆盖 Docusaurus UI，CLI 本身未见 i18n |

---

## 10. 迁移评估

### 可迁移候选

| 机制 | 目标插件 | 可行性 | 备注 |
|------|----------|--------|------|
| Adapter Pattern (多 backend) | `integrations/mcp-services` | ★★☆ | 抽象模式可借鉴，但 Rust 实现需重写 |
| Spec Lifecycle (5-status) | `workflows/deep-plan` | ★★★ | 状态机可直接采用 |
| Status Transition Tracking | `vcs/git` 或 `workflows/issue-driven-dev` | ★★☆ | 自动记录变更历史的模式可移植 |
| Circular Dependency Detection | `workflows/deep-plan` | ★★☆ | 依赖图校验逻辑可提取 |
| Context Economy 原则 | `meta/plugin-optimizer` | ★★★ | "≤300 行 / <2K tokens" 规则与 plugin-optimizer 的 token budget 一致 |
| SDD Workflow (5-step) | 新增 skill | ★★☆ | DISCOVER→DESIGN→IMPLEMENT→VALIDATE→PUBLISH 可作为通用 SDD skill |

### 建议采纳顺序

1. **Spec Lifecycle + Status Transition** → 提取为通用 spec 状态管理 skill
2. **Context Economy 原则** → 融入 plugin-optimizer 的最佳实践文档
3. **SDD Workflow** → 作为 deep-plan 的补充 skill

---

## 11. 开放问题

1. **Non-Markdown adapter 时间表**: GitHub Issues adapter 预计何时可用？是否有 alpha 版本可测试？
2. **MCP Server 稳定性**: Axum HTTP MCP Server 是否有 production 使用案例？性能基准数据？
3. **Spec 模板生态**: 是否有计划建立 spec template marketplace？不同项目类型（web app、CLI tool、library）的模板？
4. **团队协作**: 多人同时修改同一 spec 时的冲突解决策略？是否支持 lock/merge？
5. **与 CI/CD 集成深度**: 除了 `lean-spec validate --warnings-only`，是否有计划支持 PR 级别的 spec-diff 报告？
