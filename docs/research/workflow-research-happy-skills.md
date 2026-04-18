# Workflow Research Report: happy-skills

> **研究日期**: 2025-07  
> **仓库**: notedit/happy-skills  
> **文件数**: ~115  
> **许可证**: 未明确声明  

---

## 1. 框架概况

happy-skills 是一套面向 Claude Code 环境的 **AI-native skill orchestration framework**，通过 `npx @anthropic/skills-cli install happy-skills` 一键安装。框架以中文 README 为主文档，涵盖 8 个开发 skill，覆盖从 idea 到 merged PR 的全生命周期。

| 属性 | 值 |
|------|------|
| **类型** | Claude Code Skill Collection (npm package) |
| **语言** | Markdown (skill 定义) + JavaScript/TypeScript (CLI) |
| **入口** | `npx @anthropic/skills-cli install happy-skills` |
| **核心目录** | `skills/dev/` (开发流), `skills/quality/` (质量流), `skills/arch/` (架构流) |
| **安装方式** | npm registry → skills CLI → `.claude/skills/` |

---

## 2. 源清单

| 文件 | 用途 | 重要度 |
|------|------|--------|
| `README.md` | 中文主文档，skill 概览与安装指南 | ★★★ |
| `package.json` | npm 包定义与 skill metadata | ★★★ |
| `skills/dev/feature-dev/SKILL.md` | Feature 开发全流程 skill | ★★★ |
| `skills/dev/issue-flow/SKILL.md` | Issue-driven 开发流 | ★★★ |
| `skills/dev/hotfix/SKILL.md` | Hotfix 紧急修复流程 | ★★☆ |
| `skills/quality/code-review/SKILL.md` | AI 代码评审 skill | ★★★ |
| `skills/quality/tdd/SKILL.md` | TDD Red-Green-Refactor 流程 | ★★☆ |
| `skills/quality/bug-hunt/SKILL.md` | Bug 定位与修复 skill | ★★☆ |
| `skills/quality/refactor/SKILL.md` | 安全重构 skill | ★★☆ |
| `skills/arch/architecture/SKILL.md` | 架构分析与决策 skill | ★★☆ |

---

## 3. 对象模型

### 核心实体

```
Skill
  ├── name: string           # 如 "feature-dev"
  ├── category: enum         # dev | quality | arch
  ├── trigger: string        # 用户意图匹配关键词
  ├── workflow: Phase[]      # 有序阶段列表
  └── output: Artifact[]     # 交付物类型

Phase
  ├── name: string           # 如 "需求分析", "实现", "测试"
  ├── gate: GateCondition?   # 进入下一阶段的前置条件
  └── actions: Action[]      # 该阶段要执行的动作

Artifact
  ├── type: enum             # branch | commit | pr | test-report
  └── location: string       # 文件路径或 git ref
```

### 实体关系

- 一个 **Skill** 包含多个 **Phase**（顺序执行）
- 每个 **Phase** 可产出多个 **Artifact**
- Skill 之间无显式依赖，但 feature-dev 和 issue-flow 共享 branch 命名规范

### Context 隔离

每个 skill 通过 `SKILL.md` 独立加载，Claude Code 仅在触发时注入对应 skill 的 prompt，不同 skill 之间无共享上下文。

---

## 4. 流程与状态机

### Happy Path (以 feature-dev 为例)

```
[触发] 用户描述 feature
   ↓
[Phase 1: 需求分析]
   分析需求 → 拆解任务 → 确定分支策略
   ↓
[Phase 2: 分支创建]
   git checkout -b feature/<name>
   ↓
[Phase 3: 实现]
   逐文件实现 → commit 分拆 → conventional commit 格式
   ↓
[Phase 4: 测试]
   运行测试 → 验证覆盖率
   ↓
[Phase 5: PR 创建]
   生成 PR description → 创建 PR → 请求 review
   ↓
[完成]
```

### 状态转移

| 当前阶段 | 触发条件 | 下一阶段 |
|----------|----------|----------|
| 需求分析 | 任务拆解完成 | 分支创建 |
| 分支创建 | branch 创建成功 | 实现 |
| 实现 | 所有任务完成 | 测试 |
| 测试 | 测试通过 | PR 创建 |
| 测试 | 测试失败 | 实现（回退修复） |

### Failure Path

- **测试失败**: 回退到实现阶段修复，重新运行测试
- **PR 冲突**: 提示用户手动 rebase
- **需求不明确**: 在 Phase 1 要求用户补充信息

---

## 5. 执行保障审计

| 机制 | 级别 | 说明 |
|------|------|------|
| Conventional Commit 格式 | **Soft** | SKILL.md 中以 prompt 指令要求，无自动校验 |
| Branch 命名规范 | **Soft** | 文本约定 `feature/`、`hotfix/` 前缀 |
| 测试必须通过才能 PR | **Soft** | Prompt 要求但无 hook 阻断 |
| TDD Red-Green-Refactor 顺序 | **Soft** | 仅 prompt 引导，无状态文件记录 |
| Code Review 检查清单 | **Soft** | 内嵌在 SKILL.md 的 prompt 中 |
| Phase 顺序执行 | **Unenforced** | 单次 prompt 注入，无持久化阶段状态 |
| 分支存在性检查 | **Unenforced** | 未见 pre-check 逻辑 |

**总评**: 所有约束均为 **prompt-level enforcement**，无 hook、无状态文件、无 CI gate。依赖 LLM 的 instruction-following 能力。

---

## 6. Prompt 目录

### Prompt 1: feature-dev（核心开发流）

```
你是一个经验丰富的全栈开发工程师。当用户描述一个需要开发的功能时：
1. 分析需求，拆解为可执行的任务列表
2. 创建 feature 分支 (feature/<描述性名称>)
3. 逐步实现每个任务，每完成一个逻辑单元就创建 commit
4. 使用 conventional commit 格式
5. 运行测试确保不破坏现有功能
6. 创建 PR 并生成清晰的描述
```

**特征**: 中文 prompt，步骤式指令，无条件分支，无 error handling 指令。

### Prompt 2: code-review（代码评审）

```
你是一个资深代码审查专家。审查时关注：
- 代码逻辑正确性
- 潜在的性能问题
- 安全漏洞
- 代码可读性和可维护性
- 测试覆盖度
输出结构化的审查报告，按严重程度排序。
```

**特征**: 角色设定 + 关注点列表 + 输出格式要求。

---

## 7. 微观设计亮点

### 7.1 中文优先的 Prompt 设计

所有 skill 的 prompt 均以中文编写，降低中文用户的认知门槛。这在 Claude Code 生态中较为少见——多数框架默认英文 prompt，中文团队需额外翻译。

### 7.2 三域分类法 (dev / quality / arch)

将 8 个 skill 按 **开发流**、**质量流**、**架构流** 三个维度组织，形成清晰的能力矩阵。每个域内的 skill 自包含，降低认知负荷。

### 7.3 npx 一键安装

利用 `@anthropic/skills-cli` 的 npm 分发通道，用户无需手动克隆仓库。`npx skills install happy-skills` 直接将 skill 文件拷贝到 `.claude/skills/` 目录。

---

## 8. 宏观设计亮点

### 8.1 "Skill 即 Prompt" 的极简哲学

happy-skills 将复杂的工程实践（feature 开发、TDD、code review）压缩为纯文本 prompt。无 runtime、无状态管理、无外部依赖。这种极简主义使框架的安装成本趋近于零，但也意味着所有保障均依赖 LLM 的理解能力。

### 8.2 全生命周期覆盖

8 个 skill 构成从 idea → implementation → review → merge 的完整闭环。虽然每个 skill 独立运行，组合使用时可覆盖日常开发的绝大多数场景。

---

## 9. 失败模式与局限

| # | 失败模式 | 严重度 | 说明 |
|---|----------|--------|------|
| 1 | **无阶段持久化** | 高 | 每个 Phase 无状态文件记录，context window 刷新后 LLM 无法恢复进度 |
| 2 | **Prompt-only enforcement** | 高 | 所有规范（commit 格式、branch 命名、测试要求）仅靠 prompt 约束，无 hook 或 CI 验证 |
| 3 | **无 error recovery 指令** | 中 | Skill prompt 中缺少失败重试、回退策略等 error handling 逻辑 |
| 4 | **Skill 间无编排** | 中 | 无法定义 "先 issue-flow 再 feature-dev 再 code-review" 的组合工作流 |
| 5 | **无 token budget 控制** | 低 | SKILL.md 未控制指令 token 数，复杂 prompt 可能超出最优范围 |
| 6 | **中文 prompt 模型依赖** | 低 | 中文指令在非 Claude 模型上的 instruction-following 质量未验证 |

---

## 10. 迁移评估

### 可迁移候选

| Skill | 目标插件 | 可行性 | 备注 |
|-------|----------|--------|------|
| feature-dev | `vcs/git` | ★★★ | 核心流程与 git plugin 高度契合 |
| issue-flow | `workflows/issue-driven-dev` | ★★★ | 直接补充 issue-flow 插件 |
| code-review | `quality/codex-review` | ★★☆ | 需与现有 Codex review 能力合并 |
| tdd | `quality/testing` | ★★☆ | 可补充 Red-Green-Refactor 的中文指令 |
| hotfix | `vcs/gitflow` | ★★☆ | 对齐 GitFlow hotfix 分支策略 |
| bug-hunt | `quality/testing` | ★☆☆ | 与 testing 插件的 bug 定位能力重叠 |
| refactor | `quality/refactor` | ★☆☆ | 现有 refactor 插件已覆盖 |
| architecture | `workflows/deep-plan` | ★☆☆ | 架构分析功能较浅 |

### 建议采纳顺序

1. **feature-dev** → 提取分支创建 + conventional commit + PR 生成流程的中文 prompt
2. **issue-flow** → 补充 issue-driven-dev 的触发逻辑
3. **code-review** → 合并为 codex-review 的中文变体

---

## 11. 开放问题

1. **Skill 版本管理**: npm package 更新后如何同步已安装的 `.claude/skills/` 文件？是否支持增量更新？
2. **多 skill 编排**: 用户是否有组合多个 skill 的实际需求？如有，是否需要引入 workflow orchestrator？
3. **跨模型兼容性**: 中文 prompt 在 GPT-4o、Gemini 等非 Claude 模型上的效果如何？
4. **社区贡献机制**: 115 个文件中是否包含第三方贡献的 skill？是否有审核流程？
