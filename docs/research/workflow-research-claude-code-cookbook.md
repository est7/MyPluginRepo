# Workflow Research Report: claude-code-cookbook

> 生成时间：2025-07  
> 仓库：`vendor/claude-code-cookbook/`  
> 版本：v3.2.0 | 许可证：Apache 2.0 | 作者：wasabeef

---

## 1. 框架概况

| 维度 | 值 |
|------|-----|
| **类型** | 多语言 Claude Code plugin — 命令集 + 角色集 + Hook 自动化 |
| **文件数** | ~748 |
| **语言** | Markdown（commands/roles）+ JSON（配置）+ Shell（hooks） |
| **入口** | `.claude-plugin/marketplace.json` → 8 个语言变体 plugin |
| **平台** | Claude Code（支持 Cursor/Windsurf 共存） |
| **设计哲学** | "Immediate Execution" — 编辑已有文件无需确认，仅大范围变更需确认 |

claude-code-cookbook 是当前调研的 vendor 中**命令数量最多**（39 个）和**语言覆盖最广**（8 种自然语言）的框架。它将工程实践编码为 slash command，覆盖 PR 管理、代码质量、开发工具、规划分析和依赖管理五大领域。

---

## 2. 源清单

| 文件 / 目录 | 作用 |
|-------------|------|
| `.claude-plugin/marketplace.json` | Marketplace manifest，注册 8 个语言变体 plugin |
| `plugins/en/` | English plugin（39 commands + 9 roles） |
| `plugins/ja/` | Japanese plugin（默认语言） |
| `plugins/ko/` | Korean plugin |
| `plugins/zh-cn/` | Simplified Chinese plugin |
| `plugins/zh-tw/` | Traditional Chinese plugin |
| `plugins/es/` | Spanish plugin |
| `plugins/fr/` | French plugin |
| `plugins/pt/` | Portuguese plugin |
| `plugins/en/CLAUDE.md` | AI 执行指南：确认规则、TDD、quality assurance |
| `plugins/en/commands/` | 39 个 slash command 文件 |
| `plugins/en/agents/roles/` | 9 个专家角色定义 |
| `plugins/en/skills/` | Skill 定义目录 |
| `plugins/en/COMMAND_TEMPLATE.md` | Command 编写模板 |
| `settings.json` | 全局配置：权限、hooks、状态栏 |

---

## 3. 对象模型

### 核心实体关系

```
Marketplace
    └── Plugin (per language: cook, cook-en, cook-ko, ...)
            ├── Commands (39 slash commands)
            │   ├── PR Management: pr-list, pr-issue, pr-create, pr-review, pr-fix, pr-auto-update
            │   ├── Code Quality: refactor, smart-review, tech-debt, analyze-*, design-patterns
            │   ├── Development: fix-error, explain-code, commit-message, semantic-commit, ...
            │   ├── Planning: plan, spec, ultrathink, check-fact, sequential-thinking, task
            │   └── Dependencies: update-node-deps, update-flutter-deps, update-rust-deps
            │
            ├── Roles (9 expert personas)
            │   ├── security (opus model)
            │   ├── architect (opus model)
            │   ├── frontend (sonnet model)
            │   ├── backend (sonnet model)
            │   ├── performance (sonnet model)
            │   ├── qa, mobile, reviewer, analyzer
            │   └── Multi-role execution: /multi-role security,performance --agent
            │
            └── Hooks (PreToolUse / PostToolUse)
                └── preserve-file-permissions.sh
```

### 角色的 Model 选择

不同角色指定了不同的 AI model：
- **Security / Architect** → `opus`（需要深度推理）
- **Frontend / Backend / Performance** → `sonnet`（需要执行能力）

这种**按角色选择 model**的策略体现了对 model 能力差异的精细理解。

### Context 隔离

- 每个 command 独立执行，不保留跨 command 状态
- Roles 可通过 `--agent` flag 在独立 subagent context 中执行
- `/multi-role` 支持多角色并行分析（`/multi-role security,performance --agent`）

---

## 4. 流程与状态机

### 典型 PR 生命周期流程

```
/pr-issue (查看 open issues)
    → /plan (制定实现策略)
    → /spec (创建详细规格)
    → [编码实现]
    → /semantic-commit (拆分语义提交)
    → /pr-create (自动创建 PR)
    → /pr-review (系统化 review)
    → /pr-fix (处理 review 意见)
    → /pr-auto-update (更新 PR 描述)
    → /pr-checks (监控 CI 状态)
```

### `/spec` 的 Kiro-inspired 流程

```
Minimal requirements
    → Detailed user stories
    → EARS notation requirements
    → Dialogue refinement
    → 3 independent files:
        requirements.md
        design.md (with Mermaid)
        tasks.md
```

### `/plan` 的 Plan Mode 协议

```
Enter Plan Mode
    → 需求分析
    → 设计文档
    → 实现步骤
    → 风险分析
    → Show plan with "ExitPlanMode"
    → Wait for explicit OK
    → Begin implementation (with TaskCreate tracking)
```

### 没有全局状态机

cookbook 的设计是**命令驱动**而非**流程驱动**——用户按需调用 command，无强制的 phase 流转。这是"cookbook"（食谱书）命名的精确体现：每个 recipe 独立可用。

---

## 5. 执行保障审计

| 机制 | 级别 | 说明 |
|------|------|------|
| `settings.json` deny list | **Hard** | 禁止 `rm -rf`、`git reset --hard`、`git push --force`、`gh repo delete` 等破坏性操作 |
| PreToolUse/PostToolUse hooks | **Hard** | 文件权限保持 hook（`preserve-file-permissions.sh`） |
| Bash timeout 600s | **Hard** | `BASH_DEFAULT_TIMEOUT_MS: 600000` 防止无限执行 |
| `/plan` 的 ExitPlanMode gate | **Soft** | 展示计划后等待用户明确 OK，但 AI 可能跳过 |
| `/pr-review` 的 5 级分类 | **Soft** | `critical.must` → `low.nits`，但分类准确性依赖 AI |
| `/semantic-commit` 的拆分阈值 | **Soft** | 5+ files 或 100+ lines 触发拆分，但不强制 |
| TDD cycle（Red→Green→Refactor） | **Soft** | CLAUDE.md 要求但依赖 AI 自律 |
| "May the Force be with you" 完成密码 | **Soft** | 100% 完成零错误时输出此密语，纯仪式性 |
| Immediate Execution 规则 | **Unenforced** | "编辑已有文件无需确认"是指导原则，无技术强制 |

**总评**：cookbook 在**防御层面**（deny list、timeout、hooks）实现了 Hard enforcement，在**工作流层面**依赖 Soft 约束。`settings.json` 的 deny list 是所有 vendor 中**最全面的破坏性操作黑名单**。

---

## 6. Prompt 目录

### Prompt 1: `/pr-review` — 5 级 Comment 分类体系

```markdown
# Comment Classification System
🔴 critical.must — Security vulnerabilities, data integrity problems, system failure risks
🟡 high.imo — Risk of malfunction, performance issues, maintainability decrease
🟢 medium.imo — Readability enhancement, structure improvement, test quality
🟢 low.nits — Style unification, typos, comments
🔵 info.q — Implementation intent, design decisions, best practices

# Review Perspectives
Code Correctness, Security, Performance
```

**设计意图**：通过 5 级分类将 review 意见的严重性量化，使得 `critical.must` 和 `low.nits` 获得截然不同的处理优先级。`.must` / `.imo` / `.nits` / `.q` 的后缀清晰标识了意见的约束力。

### Prompt 2: Backend Role — "Inevitable Code" Principle

```markdown
# Philosophy: "Inevitable Code" Principle
Natural implementation that's the only way.

# Key Checks
1. API Design: RESTful/GraphQL principles, OpenAPI/Swagger, microservices, event-driven
2. Database Design: Data models, index optimization, query performance, transactions
3. Security: OAuth2/JWT/RBAC, encryption, OWASP Top 10, GDPR/SOC2
4. Cloud/Infrastructure: Cloud-native, serverless, Docker/Kubernetes, IaC
```

**设计意图**："Inevitable Code"（不可避免的代码）原则认为，好的实现应该是"唯一自然的选择"，而非众多可能中的一种。这将代码质量标准从"可接受"提升到"必然"。

---

## 7. 微观设计亮点

### 7.1 Per-Role Model 选择

Security 和 Architect 角色指定 `opus` model，Frontend/Backend/Performance 角色指定 `sonnet` model。这种**按角色精确匹配 model 能力**的做法在同类项目中独一无二——深度分析用高能力 model，执行实操用高效率 model。

### 7.2 Comprehensive Deny List

`settings.json` 中的 deny list 覆盖了 20+ 种破坏性操作，包括 `git reset --hard`、`git push --force`、`rm -rf`、`gh repo delete`、`gh release delete` 等。这是一种**防御性权限设计**，通过黑名单而非白名单保护用户，在允许广泛工具访问的同时防止灾难性操作。

### 7.3 `/semantic-commit` 的智能拆分

当变更涉及 5+ 文件或 100+ 行时，自动将大 diff 拆分为语义独立的小 commit。这解决了 AI 编码中常见的"一次提交所有变更"问题，产出 bisectable 的 git 历史。

---

## 8. 宏观设计亮点

### 8.1 "Cookbook" 即插即用哲学

框架名为 "cookbook"（食谱书），设计上每个 command 都是独立的 "recipe"——用户按需选取，无需理解全局架构。这与 BMAD 的"完整 SDLC 流程"和 cc-sdd 的"spec-driven pipeline"形成鲜明对比。Cookbook 的哲学是：**最好的工具是你今天就能用的工具**。

### 8.2 多语言作为一等公民

8 种语言不是后期翻译，而是从设计之初就作为独立 plugin 管理。每种语言有独立的 plugin name（`cook`, `cook-en`, `cook-ko`...）、独立的 CLAUDE.md、独立的 command 文件。这种**多语言并行维护**的架构支持不同语言社区独立演化。

---

## 9. 失败模式与局限

| # | 失败模式 | 影响 | 可能性 |
|---|----------|------|--------|
| 1 | **39 命令的认知负荷** — 用户难以记住所有命令及其适用场景 | 大部分命令被忽略 | 高 |
| 2 | **8 语言同步维护** — 任何命令更新需同步 8 个语言版本 | 语言版本漂移 | 高 |
| 3 | **无工作流串联** — 命令间无状态传递，用户需手动编排执行顺序 | 工作流碎片化 | 中 |
| 4 | **Role model 依赖** — Security/Architect 指定 opus model，用户可能无权访问该 model | 角色功能退化 | 中 |
| 5 | **Hook 脚本外部依赖** — `preserve-file-permissions.sh` 等脚本存放在 `~/.claude/scripts/`，需要独立安装 | 首次使用时 hook 失效 | 中 |
| 6 | **deny list 维护** — 新的危险命令（如新版 gh CLI 的破坏性操作）需手动添加到 deny list | 保护不完整 | 低 |

---

## 10. 迁移评估

### 可移植候选

| 机制 | 目标位置（1st-cc-plugin） | 优先级 | 改造量 |
|------|--------------------------|--------|--------|
| Deny list 设计 | 全局 settings 规范 | P1 | 直接采纳作为安全基线 |
| `/pr-review` 5 级分类 | `quality/codex-review` | P1 | 移植分类体系 |
| Per-role model 选择 | 全局 agent 设计规范 | P2 | 引入按角色选 model 的 pattern |
| `/semantic-commit` | `vcs/git` | P2 | 移植智能拆分逻辑 |
| `/spec` Kiro-inspired flow | `workflows/deep-plan` | P3 | 参考但 cc-sdd 的版本更完善 |
| `/fix-error` 根因分析 | `quality/testing` | P3 | 提取分析框架 |

### 建议采纳顺序

1. **Deny list** → 立即提升安全防护
2. **PR review 分类** → 增强 code review 质量
3. **Semantic commit** → 改善 git 提交质量

---

## 11. 开放问题

1. **"May the Force be with you" 完成密码**：这是纯仪式性设计还是有下游消费者（如 CI hook）检测此密语？
2. **Hook 脚本的安装路径**：`~/.claude/scripts/` 中的脚本如何随 plugin 安装分发？当前似乎需要用户手动部署。
3. **Multi-role 的 context 管理**：`/multi-role security,performance --agent` 并行执行时，两个角色的输出如何合并？是否存在上下文冲突？
4. **StatusLine 脚本**：`settings.json` 配置了 `statusline.sh`（每 30 秒刷新），其内容和功能不明。
5. **Windsurf/Cursor 共存**：CLAUDE.md 提到"Exclude `.windsurf/` in Cursor, `.cursor/` in Windsurf"——这种互斥排除策略是否足够健壮？
