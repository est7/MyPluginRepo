# Workflow Research Report: claude-code-quickstart

> 生成时间：2025-07  
> 仓库：`vendor/claude-code-quickstart/`  
> 版本：无显式语义版本 | 许可证：MIT | 作者：MrNine-666

---

## 1. 框架概况

| 维度 | 值 |
|------|-----|
| **类型** | Windows 平台 Claude Code 开发环境自动化安装器 |
| **文件数** | ~148 |
| **语言** | PowerShell（5.1 + 7.0+）|
| **入口** | `Bootstrap-ClaudeEnv.ps1`（PS 5.1）→ `Install-ClaudeEnv.ps1`（PS 7+）→ `Manage-ClaudeEnv.ps1` |
| **平台** | Windows 10 1903+ / Windows 11 |
| **设计哲学** | 把"装环境"变成"跑脚本"——一次完成从基础依赖到 MCP/workflow 的全部配置 |

这是一个**纯 Windows 平台**的环境安装器，与其他 vendor（workflow 框架或 skill 集合）定位截然不同。它解决的是 Claude Code 在 Windows 上**开发环境搭建**的痛点，通过 13 步自动安装覆盖 Node.js、Git、Claude Code、API 配置、MCP server 等全栈依赖。

---

## 2. 源清单

| 文件 / 目录 | 作用 |
|-------------|------|
| `README.md` | 中文文档：安装方式、13 步内容、feature 列表 |
| `CLAUDE.md` | AI Context Index：架构总览、依赖图、Hard Constraints |
| `installer/Bootstrap-ClaudeEnv.ps1` | PS 5.1 bootstrap：Windows 版本检查、winget、PS 7 安装 |
| `installer/Install-ClaudeEnv.ps1` | PS 7+ 安装入口：分组安装（Basic/Advanced）、交互菜单 |
| `installer/Manage-ClaudeEnv.ps1` | PS 7+ 管理入口：更新、Provider 管理、MCP 管理 |
| `installer/core/Ui.ps1` | TUI 组件：语义色彩系统 |
| `installer/core/Process.ps1` | 外部命令执行 |
| `installer/core/Profile.ps1` | `$PROFILE` 安全编辑（marker 包裹） |
| `installer/core/Admin.ps1` | 权限检查 |
| `installer/core/Net.ps1` | 网络工具 |
| `installer/core/Registry.ps1` | Step 注册表 |
| `installer/core/Bootstrap.ps1` | Step 编排 |
| `installer/core/McpManager.ps1` | MCP CRUD 操作 |
| `installer/core/Provider.ps1` | Vendor Profile 管理 |
| `installer/steps/` | 13 个安装步骤（每步一个 .ps1 文件） |
| `installer/build/Build-SingleFile.ps1` | 单文件打包构建器 |
| `.github/workflows/build-and-release.yml` | CI/CD：构建 + GitHub Release |
| `test-syntax.ps1` | PS7 语法校验 |

---

## 3. 对象模型

### 核心实体关系

```
Bootstrap (PS 5.1)
    └── Install (PS 7+)
            ├── Basic Group (必需)
            │   ├── Step: NodeJS (fnm)
            │   ├── Step: Git
            │   ├── Step: ClaudeCode
            │   └── Step: ApiKey (Vendor Profile)
            │
            ├── Advanced Group (可选)
            │   ├── Step: Ccline
            │   ├── Step: ClaudeConfig
            │   ├── Step: ClaudeMd
            │   ├── Step: Mcp
            │   ├── Step: CcgWorkflow
            │   ├── Step: OpenSpec
            │   ├── Step: CcSwitch (optional)
            │   ├── Step: CodexCli (optional)
            │   └── Step: GeminiCli (optional)
            │
            └── Manage (PS 7+)
                    ├── Update Management
                    ├── Provider Management
                    └── MCP Management
```

### Step 接口规范（HC-2）

每个 step 文件**必须**实现 3 个函数：
- `Test-<StepId>Installed` — 检测是否已安装
- `Install-<StepId>` — 执行安装
- `Verify-<StepId>` — 验证安装（可选）

### 依赖图谱

```
NodeJS ─── ClaudeCode ─── ApiKey / Ccline / ClaudeConfig / Mcp
       ├── CcgWorkflow / OpenSpec / CodexCli / GeminiCli
Git (无依赖)
ClaudeMd (无依赖)
CcSwitch (可选，依赖 ClaudeCode)
```

### 状态检测

框架采用**无状态检测**策略（HC-3）：每次运行重新检测组件状态，不依赖持久化状态文件。已安装组件自动跳过。

---

## 4. 流程与状态机

### 双阶段架构

```
Stage 1: Bootstrap (PS 5.1)
    ├── Assert-StepPrivilege (require admin)
    ├── Test-WindowsVersion (Win 10 1903+)
    ├── Test-WingetAvailability
    ├── Install-WindowsTerminal (soft requirement)
    ├── Install-PowerShell7 (hard requirement)
    └── Show-CompletionMessage → 指引进入 Stage 2

Stage 2: Install (PS 7+)
    ├── Show-AsciiBanner
    └── Loop:
        ├── Select-TopLevelAction
        │   ├── [Basic] → Invoke-GroupedInstall(basic steps)
        │   ├── [Advanced] → Select-AdvancedAction
        │   │   ├── [OneClick] → Invoke-GroupedInstall(all advanced)
        │   │   ├── [Select] → Show-AdvancedSelectMenu → Invoke-GroupedInstall
        │   │   └── [Esc] → return to top menu
        │   └── [Esc] → exit
```

### Update 流程

```
Manage → Update Management
    ├── Mutex lock (Global\CCQ.Update.Lock)
    ├── Snapshot backup (keep 5 most recent)
    ├── Fingerprint pre-check (skip unchanged)
    ├── Interactive multi-select
    └── Execute updates → Rollback on failure
```

### Vendor Profile 切换

```
Manage → Provider Management
    ├── Create: 选择 vendor type → 输入 API key (SecureString) → 保存到 providers/
    ├── Switch: 选择 profile → merge settings.json
    └── Delete: 移除 profile 文件
```

### 支持的 Vendor

| Vendor | ID |
|--------|-----|
| 智谱 GLM | `zhipu` |
| MiniMax | `minimax` |
| Kimi / Moonshot | `moonshot` |
| 阿里云百炼 | `bailian` |
| Custom | `custom` |

---

## 5. 执行保障审计

| 机制 | 级别 | 说明 |
|------|------|------|
| Step 接口规范（3 函数） | **Hard** | HC-2：每个 step 必须实现 Test/Install/Verify |
| 无状态实时检测 | **Hard** | HC-3：每次运行重新检测，不依赖状态文件 |
| `$PROFILE` marker 包裹 | **Hard** | HC-4：使用 `# >>> Claude Code Quickstart >>>` / `# <<<` marker |
| PS 版本约束 | **Hard** | HC-14：Bootstrap 要求 PS 5.1+，Install/Manage 要求 PS 7.0+ |
| `@()` 数组安全 | **Hard** | HC-13：在 `Set-StrictMode -Version Latest` 下防止 null `.Count` 异常 |
| Mutex 更新锁 | **Hard** | `Global\CCQ.Update.Lock` 防止并发更新 |
| Snapshot 备份 + 回滚 | **Hard** | 更新前备份，保留最近 5 个 snapshot |
| Admin 权限检查 | **Hard** | Bootstrap 阶段强制 admin 权限 |
| Fingerprint pre-check | **Soft** | 跳过未变更的模板，但 fingerprint 计算可能不够精确 |
| 语法校验 | **Soft** | `test-syntax.ps1` 使用 PSParser，但非 CI 强制 |

**总评**：作为安装器，CCQ 在**系统安全**（权限检查、mutex、备份回滚、marker 隔离）方面实现了高水平的 Hard enforcement。这反映了 Windows 环境安装器需要处理的**系统级风险**（权限、并发、环境变量污染）远高于普通 workflow 框架。

---

## 6. Prompt 目录

### Prompt 1: CLAUDE.md — Hard Constraints 编码

```markdown
# Hard Constraints (HC)
HC-2: Each step file must implement 3 functions: Test-<StepId>Installed, Install-<StepId>, Verify-<StepId>
HC-3: Real-time detection: Every run checks component status, no persistent state files
HC-4: $PROFILE edit uses markers: # >>> Claude Code Quickstart >>> / # <<< Claude Code Quickstart <<<
HC-12: ApiKey stores in env.ANTHROPIC_AUTH_TOKEN + env.ANTHROPIC_BASE_URL
HC-13: PowerShell array safety: Use @() wrapper in Set-StrictMode -Version Latest
HC-14: PS version: Bootstrap=5.1+, Install/Manage=7.0+ only
```

**设计意图**：将关键约束编码为 **Hard Constraints** 列表，使得 AI 在修改代码时能够精确识别不可违反的规则。HC 编号系统使得约束可以被精确引用和追踪。

### Prompt 2: 依赖拓扑排序

```markdown
# Step Dependency Graph
NodeJS ─── ClaudeCode ─── ApiKey / Ccline / ClaudeConfig / Mcp
       ├── CcgWorkflow / OpenSpec / CodexCli / GeminiCli
Git (no deps)    ClaudeMd (no deps)    CcSwitch (optional, depends on ClaudeCode)

# Execution: Invoke-GroupedInstall computes transitive dependency closure with topological sort
```

**设计意图**：依赖图谱可视化让 AI 理解安装顺序约束，`Invoke-GroupedInstall` 自动计算传递依赖闭包确保正确的安装序列。

---

## 7. 微观设计亮点

### 7.1 双阶段 PS 版本桥接

Bootstrap 脚本在 PS 5.1 环境中运行，其唯一目标是将环境升级到 PS 7.0+。Install 和 Manage 脚本则利用 PS 7 的高级特性。这种**版本桥接**设计优雅地解决了"鸡和蛋"问题——在低版本环境中引导安装高版本运行时。

### 7.2 UTF-8 编码修复

Bootstrap 脚本通过 kernel32 API（`SetConsoleOutputCP(65001)`）修复 Windows 控制台的 UTF-8 编码问题。这解决了 `irm | iex` 管道中中文字符乱码的常见痛点，体现了对 Windows 命令行**编码陷阱**的深入理解。

### 7.3 MCP Credentials Vault

`~/.ccq/mcp-meta.json` 实现了 MCP server 的凭证保险库，支持凭证的加密存储、启用/禁用切换和状态查看（Active/Disabled/Missing）。这种**集中式凭证管理**避免了 MCP 配置散落在多个文件中的混乱。

---

## 8. 宏观设计亮点

### 8.1 "检测即状态" 的无状态架构

CCQ 刻意不使用持久化状态文件记录安装进度。每次运行时重新检测所有组件状态，已安装组件自动跳过。这种**无状态设计**消除了"状态文件与实际环境不同步"的常见问题，牺牲了少量启动性能换来了**始终准确的环境视图**。

### 8.2 中国大陆 Vendor 生态支持

内置支持智谱 GLM、MiniMax、Kimi/Moonshot、阿里云百炼等中国大陆 AI vendor。这使得 Claude Code 可以通过兼容 API 对接国内大模型服务商，解决了**网络访问限制**下的实际使用需求。

---

## 9. 失败模式与局限

| # | 失败模式 | 影响 | 可能性 |
|---|----------|------|--------|
| 1 | **Windows 独占** — 完全基于 PowerShell，macOS/Linux 用户无法使用 | 目标用户群受限 | 确定性 |
| 2 | **winget 依赖** — Bootstrap 依赖 winget 安装 PS 7，部分企业环境禁用 winget | 安装流程中断 | 中 |
| 3 | **13 步安装的网络依赖** — 大量从 GitHub/npm 下载，中国大陆网络环境下可能超时 | 安装不完整 | 高 |
| 4 | **Vendor Profile 安全** — API key 存储在文件系统中（SecureString 仅限本机解密），多用户环境下存在风险 | 凭证泄露 | 低-中 |
| 5 | **Single-file 构建的可维护性** — `Build-SingleFile.ps1` 将多个脚本合并为单文件，调试困难 | 问题定位效率低 | 中 |
| 6 | **非核心组件更新** — Ccline、CcgWorkflow、OpenSpec 等第三方组件的更新依赖上游稳定性 | 更新失败 | 中 |

---

## 10. 迁移评估

### 可移植候选

| 机制 | 目标位置（1st-cc-plugin） | 优先级 | 改造量 |
|------|--------------------------|--------|--------|
| HC 编号约束系统 | `meta/skill-dev` CLAUDE.md 规范 | P2 | 提取 Hard Constraint 编号 pattern |
| MCP Credentials Vault 设计 | `integrations/mcp-services` | P3 | 概念可参考，但实现是 PowerShell 特定 |
| 无状态检测策略 | 全局设计原则 | P3 | 作为"环境检测"类 skill 的设计指南 |

### 建议

CCQ 作为**安装器**而非 **workflow 框架**，其直接可移植到 `1st-cc-plugin` 的内容有限。主要价值在于：
1. **HC 约束编码模式** — 将关键约束编号化的做法可推广到 skill 设计中
2. **防御性系统操作** — deny list、mutex、snapshot 备份等安全实践可作为参考

---

## 11. 开放问题

1. **CI 覆盖**：`build-and-release.yml` 只构建 single-file 脚本并验证文件存在，没有运行 `test-syntax.ps1`——语法校验是否应纳入 CI？
2. **Vendor Profile 格式**：`~/.claude/providers/` 中的 profile 文件格式是什么？是否有 schema 校验？
3. **MCP server 生态**：内置支持的 9 个 MCP server（Context7、DeepWiki、Tavily 等）的配置模板如何维护和更新？
4. **升级安全**：Snapshot 备份保留最近 5 个，但没有提到空间清理策略。在频繁更新场景下 `%TEMP%\ClaudeEnvInstaller\` 是否会膨胀？
