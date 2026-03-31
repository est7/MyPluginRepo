五个主流 Agent 规范与工作流仓库的深度研究报告：compound-engineering-plugin、Everything Claude Code、Get Shit Done、OpenSpec、Superpowers

执行摘要

这五个项目解决的是同一类问题：让“会写代码的智能体”从“聊天式输出”进化到“可重复、可审计、可扩展”的工程化交付。但它们的切入点不同：OpenSpec把“需求与设计”固化成仓库内的可追踪产物（artifacts）并提供严谨 CLI 与 OPSX 指令体系；**Get Shit Done（GSD）**把“规划→执行→验证→里程碑归档”封装成面向单人与小团队的高自动化命令流程；Superpowers强调“技能（skills）驱动的方法论”，用一组可组合技能强制执行 TDD、代码审核、worktree 分支与并行子代理；**Everything Claude Code（ECC）**更像“全量 agent harness 性能优化系统”，覆盖多平台（Claude Code、Cursor、OpenCode 等）并提供大量命令、技能、hooks、规则与持续学习/安全扫描能力；EveryInc/compound-engineering-plugin则偏“生态转换与同步”，用一个 TypeScript/Bun CLI 把 Claude Code 插件/配置转换并安装到多种 AI 编程工具、并把 ~/.claude 的命令/技能/MCP 同步到其他工具配置中。citeturn20view0turn34view0turn26view1turn42view0turn12view0

选型结论（面向典型需求的强建议）：

如果你要“团队级、可复用、跨工具一致”的规范化变更流程，优先 OpenSpec（CLI + OPSX + schema/模板/依赖图）。citeturn27view0turn28view0turn31view3

如果你更看重“一个人/小团队快速做成、并保持质量底线”，优先 GSD（里程碑/阶段/验证架构/并行执行）。citeturn37view0turn34view0turn41view4

如果你需要“强制 TDD + 细粒度任务拆分 + 严格两轮审查 + worktree 并行”，优先 Superpowers（技能体系）；它对 OpenCode/Codex 的手工集成也给了非常工程化的指南与测试方案。citeturn42view0turn46view1turn46view2

如果你已经深度使用 Claude Code（或多种 harness）且想要“命令/技能/规则/钩子/持续学习/安全扫描”的一揽子系统，并愿意承担更高的复杂度与维护成本，选 ECC。citeturn20view0turn21view0turn18view0

如果你的核心痛点是“插件/配置生态迁移（Claude → OpenCode/Codex/Cursor/…）与多工具对齐”，选 compound-engineering-plugin（安装/转换/同步）。citeturn3view0turn13view2turn13view4

（趋势度量，来自各仓库页面在 2026 年 3 月前后的快照）：Superpowers（约 84.7k⭐/6.6k fork）、ECC（约 76.4k⭐/9.5k fork）、OpenSpec（约 30.7k⭐/2k fork）、GSD（约 30.3k⭐/2.5k fork）、compound-engineering-plugin（约 10.4k⭐/827 fork）。citeturn42view0turn20view0turn26view1turn34view0turn12view0

研究范围与方法

本报告优先使用各项目的 GitHub 官方仓库与仓库内文档；对 OpenSpec 额外引用其官方文档站点中的安装要求（Node 版本等），并以仓库内 docs/cli.md、docs/commands.md 等作为命令与参数的“事实来源”。citeturn26view2turn27view0turn28view0turn34view0turn42view0

“库/框架/插件”在这里更准确的统一称呼是：agent harness 工作流包（prompts/commands/skills/hooks/rules）与配套 CLI 工具。其中：OpenSpec 与 compound-engineering-plugin 明确提供 CLI；GSD 提供 npx get-shit-done-cc 安装器 CLI；ECC 提供 install.sh（Node 安装器入口）与大量命令文件；Superpowers侧重 skills，但也提供插件安装命令与部分 command 文件。citeturn27view0turn15view0turn41view4turn21view0turn45view0

项目逐个深挖

EveryInc/compound-engineering-plugin

简要定位：一个“Claude Code 插件 + 转换/安装/同步 CLI”。仓库既包含可直接用作 Claude 插件的一组 agents/skills/commands，也提供 compound-plugin CLI：把 Claude 插件转换并写入多种目标工具的配置目录，并支持把 ~/.claude/ 的 skills/commands/MCP servers 同步到其他工具。citeturn3view0turn15view0turn13view4

安装与基础用法（官方示例）：其 README 给出通过 Bun 在任意目录运行的方式（典型是 bunx @every-env/compound-plugin ...），并在输出路径上按目标工具分别落盘（例如 OpenCode 写 opencode.json、技能写入 .opencode/skills/，Codex 写 ~/.codex/AGENTS.md 或 ~/.codex/agents/ 等）。citeturn5view0turn3view0

CLI 命令总览（可执行入口）：包名 @every-env/compound-plugin，bin 为 compound-plugin。脚本提供 dev / convert / list / cli:install，测试用 bun test。citeturn15view0

Exhaustive：CLI 子命令、参数、flag、变体与用例

compound-plugin 的子命令由 src/index.ts 注册：convert / install / list / sync。citeturn7view0

convert：转换一个 Claude 插件目录为目标格式（核心场景：本地已有插件目录、想输出到某工具）

命令结构（来自 convert.ts）：
- 位置参数：source（必填，Claude 插件目录路径）citeturn13view2
- 关键参数：
    - --to（默认 opencode）：opencode | codex | droid | cursor | pi | copilot | gemini | kiro | windsurf | openclaw | qwen | allciteturn13view2
    - -o, --output：输出目录（项目根）citeturn13view2
    - --codex-home：Codex 的 .codex 根目录（示例：~/.codex）citeturn13view2
    - --pi-home：Pi 根目录（示例：~/.pi/agent 或 ./.pi）citeturn13view2
    - --openclaw-home：OpenClaw extensions 根citeturn13view2
    - --qwen-home：Qwen extensions 根citeturn13view2
    - --scope：global | workspace（默认随 target 变化）citeturn13view2
    - --also：额外生成 target（逗号分隔，如 codex）citeturn13view2
    - --permissions（默认 broad）：none | broad | from-commands（注意：代码接受值为 none|broad|from-commands）citeturn13view2
    - --agent-mode（默认 subagent）：primary | subagentciteturn13view2
    - --infer-temperature（默认 true）：是否从 name/description 推断温度citeturn13view2

关键变体：
- --to all：会检测已安装工具并对“检测到且已实现”的 target 执行转换（否则会提示未检测到工具或跳过未实现）。citeturn13view0

示例模板（按官方参数集合组织，便于复制）：
# 1) 直接转换到 OpenCode（默认）
compound-plugin convert ./path/to/plugin --to opencode -o .

# 2) 转换到 Codex，并把输出写到自定义 codex home
compound-plugin convert ./path/to/plugin --to codex --codex-home ~/.codex

# 3) 一次生成多个目标（主目标 + also）
compound-plugin convert ./path/to/plugin --to opencode --also codex,cursor

# 4) 控制权限映射与 agent 默认模式
compound-plugin convert ./path/to/plugin --permissions broad --agent-mode subagent


install：安装并转换 Claude 插件（核心场景：从 marketplace/repo 名称或路径安装）

命令结构（来自 install.ts）：
- 位置参数：plugin（必填：插件名或路径）citeturn11view1
- 参数与 convert 高度一致：
    - --to（默认 opencode）：同 convert；也支持 all 做多工具落盘citeturn11view1
    - -o, --output、--codex-home、--pi-home、--openclaw-home、--qwen-home、--scope、--also、--agent-mode、--infer-temperatureciteturn11view1
    - --permissions：默认 none（注释解释默认不写全局权限以免污染用户 opencode.json）且允许值在代码层为 none|broad|from-commands；描述文字里出现 from-command（单数）但代码校验集合为 from-commands，以代码为准。citeturn11view1

示例模板：
# 1) 安装并输出到 OpenCode（默认）
bunx @every-env/compound-plugin install compound-engineering-plugin --to opencode

# 2) 安装并输出到 Codex（全局）
bunx @every-env/compound-plugin install compound-engineering-plugin --to codex --codex-home ~/.codex

# 3) 安装并对“已检测到的所有工具”生成/写入
bunx @every-env/compound-plugin install compound-engineering-plugin --to all


list：列出当前项目 plugins/ 下的 Claude 插件
- 无参数；扫描 plugins/<name>/.claude-plugin/plugin.json 存在的目录并输出。citeturn14view0

- 示例：
compound-plugin list


sync：把 Claude Code 配置同步到其他工具

命令结构（来自 sync.ts & README）：
- 参数：
    - --target（默认 all）：同步目标（支持若干预定义 target + all）citeturn13view4turn5view0
    - --claude-home：Claude home 路径（默认 ~/.claude）citeturn13view4
- 行为：读取 Claude home 并同步 skills、commands、MCP servers；如果 MCP server env vars 可能含 secret，会提示“复制前检查”。citeturn13view4turn5view0

示例模板：
# 同步到所有已检测到的目标工具
compound-plugin sync --target all

# 指定 Claude home
compound-plugin sync --claude-home ~/.claude --target all


开发、测试、调试与完整修复流程（step-by-step）

本地开发与测试入口：
- bun run src/index.ts（dev）
- bun test（测试）citeturn15view0

- 测试覆盖了 Claude home 解析、CLI、converter/writer、detect-tools，以及多个目标（copilot、droid、gemini、kiro、openclaw、opencode、pi、qwen、windsurf）与 sync 的专用测试文件。citeturn17view0

建议的 bug-fix 工作流（可复制到团队规范）：
1. 复现与最小化输入：在 tests/fixtures 或新建最小插件样例复现；优先把复现变成单测（例如某 target writer 的输出差异）。citeturn17view0
2. 判定层级：是解析层（Claude plugin loader）、转换层（converter）、落盘层（writer/resolve-output）、还是同步层（sync target）——测试文件命名基本对应这些模块。citeturn17view0turn13view4
3. 写回归测试：在对应 *.test.ts 增加断言（重点：输出路径、scope 推导、权限映射值、--to all 的 detect 行为）。citeturn13view0turn17view0
4. 实现修复：修 converter/writer；对 permissions 字段务必与允许值集合一致（none|broad|from-commands）。citeturn11view1turn13view2
5. 跑全量测试：bun test；特别关注 sync 会复制 MCP env vars 的安全提示不应被破坏。citeturn13view4turn15view0
6. 手工验收：用 compound-plugin convert/install 在临时目录落盘对比；再用 sync 在本机测试（建议在干净用户目录/容器内）。citeturn13view4turn11view1

安全、性能与扩展最佳实践

安全：sync 会复制 MCP server 的环境变量；仓库代码明确提示 env vars 可能包含 secrets，复制前必须审阅、避免提交/分享配置文件。citeturn13view4

性能/可扩展：当你要同时维护多个工具（Claude、OpenCode、Codex、Cursor 等）的“同一套技能/命令”，compound-plugin 的 --to all + sync --target all 可以把“碎片化配置管理”收敛成单一来源（Claude home 或插件目录），降低配置漂移（这是从功能推导的工程收益）。citeturn13view0turn13view4

优势/局限/与其他差异：

优势是“转换+同步”这一独特定位，适合多工具用户；局限是它本身不定义完整的 spec-driven 生命周期（那属于 OpenSpec/GSD/Superpowers/ECC 的范畴）。citeturn7view0turn27view0turn37view0

适用场景：
- 你想把某 Claude 插件/命令体系迁移到 OpenCode/Codex/Cursor/Gemini 等，并保持持续同步；
- 你需要“安装目标检测 + 一键生成多种格式”的工具链。citeturn13view0turn13view2
⸻
affaan-m/everything-claude-code

简要定位：ECC 自称“AI agent harness 性能优化系统”，提供 agents、skills、commands、hooks、rules、MCP configs，并跨 Claude Code、OpenCode、Cursor、Codex 等多个 harness 适配；同时提供安装器与包管理器自动检测、hook 运行时控制等。citeturn18view0turn20view0

安装、setup 与运行方式

最短路径（Quick Start）：
- Claude Code 中：/plugin marketplace add affaan-m/everything-claude-code → /plugin install everything-claude-code@everything-claude-codeciteturn18view0
- 因 Claude 插件不能自动分发 rules，需要手工安装：clone 仓库后运行 ./install.sh typescript（或 python/golang/swift/php），也可多语言混装，并支持 --target cursor 或 --target antigravity。citeturn18view0turn24view0
- 使用命令：
    - 插件方式（带命名空间）：/everything-claude-code:plan "..."citeturn18view0
    - 手工方式（短命令）：/plan "..."citeturn18view0
    - 查看命令：/plugin list everything-claude-code@everything-claude-codeciteturn18view0

Exhaustive：命令、脚本入口、flags、配置项与惯用法

命令文件（仓库内可枚举的“命令面”）：commands/ 目录给出了 ECC 的命令清单（以 .md 表示命令定义/提示）。该目录包含（按文件名）至少以下命令：

aside, build-fix, checkpoint, claw, code-review, e2e, eval, evolve, go-build, go-review, go-test, gradle-build, harness-audit, instinct-export, instinct-import, instinct-status, kotlin-build, kotlin-review, kotlin-test, learn-eval, learn, loop-start, loop-status, model-route, multi-backend, multi-execute, multi-frontend, multi-plan, multi-workflow, orchestrate, plan, pm2, projects, promote, prompt-optimize, python-review, quality-gate, refactor-clean, resume-session, save-session, sessions, setup-pm, skill-create, tdd, test-coverage, update-codemaps, update-docs, verify。citeturn21view0

这些命令在不同 harness 中的呈现形式不同：Claude Code 往往是 /everything-claude-code:<cmd> 或手工安装后的 /<cmd>；OpenCode 则以其自身命令系统呈现。仓库 README 明确给出了 OpenCode 的可用命令子集列表。citeturn18view0turn19view2

OpenCode 侧（README 明确列出的 31+ 命令）：包括 /plan /tdd /code-review /build-fix /e2e /refactor-clean /orchestrate /learn /checkpoint /verify /eval /update-docs /update-codemaps /test-coverage /go-review /go-test /go-build /python-review /multi-plan /multi-execute /multi-backend /multi-frontend /multi-workflow /pm2 /sessions /skill-create /instinct-status /instinct-import /instinct-export /evolve /promote /projects /learn-eval /setup-pm。citeturn19view2

安装器入口与 flags（install.sh → Node 安装器）：install.sh 是 legacy shell wrapper，最终执行 node scripts/install-apply.js。citeturn22view0

安装器帮助文本给出完整用法与选项，核心结构是：
- --target <claude|cursor|antigravity>（默认 claude），并解释每个 target 的落盘内容：claude（rules → ~/.claude/rules/）、cursor（rules/hooks/配置 → ./.cursor/）、antigravity（rules/workflows/skills/agents → ./.agent/）。citeturn24view0
- 控制安装集合的三种模式：
    - --profile <id>：安装某 profile；
    - --modules <id,...>：显式选择模块；
    - --config <path>：从 ecc-install.json 读取 intent。citeturn24view0
- 组件选择：--with <component> / --without <component>；
- 计划/输出：--dry-run（只显示计划）、--json（输出机器可读 JSON）、--help。citeturn24view0

示例模板（与其帮助文本一致，便于工程化脚本化）：
# Claude 默认安装（legacy 语言入口）
./install.sh typescript
./install.sh typescript python golang

# 指定 target
./install.sh --target cursor typescript

# 仅输出安装计划（不落盘）
./install.sh --target claude --dry-run --json --profile <PROFILE_ID>

# 用显式模块安装
./install.sh --target claude --modules <MODULE_ID_1>,<MODULE_ID_2> --dry-run


包管理器自动检测与配置（关键配置项与优先级）：ECC README 明确了包管理器选择的优先级：CLAUDE_PACKAGE_MANAGER 环境变量 → .claude/package-manager.json → package.json.packageManager → lock 文件 → ~/.claude/package-manager.json → fallback；并给出设置方式（环境变量或 node scripts/setup-package-manager.js --global/--project/--detect）以及 Claude 内的 /setup-pm 命令。citeturn18view0turn19view2

Hook 运行时控制（关键环境变量）：
- ECC_HOOK_PROFILE：严格性 profile（示例：minimal|standard|strict，README 示例为 standard）
- ECC_DISABLED_HOOKS：逗号分隔的 hook id 禁用列表（示例：pre:bash:tmux-reminder,post:edit:typecheck）citeturn18view0turn20view0

开发、测试、调试与完整修复流程（step-by-step）

ECC README 公开宣称在 v1.8.0 版本阶段“997 internal tests passing”，并强调 hooks/scripts 迁移到 Node.js 以保证跨平台一致性。citeturn20view0turn18view0

在缺少完整 package.json 脚本细节的前提下（本次检索未全量展开），推荐你把 ECC 的修复流程按“产物类型”拆分（这和它多组件结构一致）：
1. 判定问题归属：命令（commands/*.md）、技能（skills/）、hooks（hooks/）、rules（rules/）、安装器（install.sh/Node runtime）。citeturn18view0turn21view0turn24view0
2. 复现优先策略：尽量把问题变成“可落盘产物”的 diff（比如某命令 prompt、某 hook 触发条件、某 rule 的覆盖范围），以便 code review 与回归。citeturn18view0turn20view0
3. 本地安装验证：对 Claude/Cursor/antigravity 分别用安装器做 --dry-run（必要时 --json）验证“会装什么”；再落盘到一个临时项目目录里跑最小会话（例如 /plan、/tdd 或 /setup-pm）。citeturn24view0turn18view0
4. 跨 harness 回归：ECC 强调跨 Claude Code、Cursor、OpenCode 等一致性与 feature parity；修复要至少在目标 harness 的对应命令上跑一遍（尤其是与包管理器检测、hooks profile 有关的改动）。citeturn18view0turn19view2

安全、性能与扩展最佳实践

ECC 的定位就是“性能优化系统”，它在指南中把 token 优化、记忆持久化、验证循环、并行化、子代理编排列为核心主题（README 导览）。citeturn20view0

对生产实践的关键建议是把“风险控制”前置为可执行机制：
- 用 hook profile 与 disabled hooks 做临时降级/隔离，而不是直接删改规则文件；这能把调试与日常使用隔离开。citeturn18view0turn20view0
- 把包管理器选择固定下来（CLAUDE_PACKAGE_MANAGER 或脚本写入 config），避免不同开发机上 hook 执行结果不一致。citeturn18view0

优势/局限/与其他差异：

ECC覆盖面极大：命令（40）、agents（16）、skills（65）、hooks、rules、MCP servers 等，并在 README 提供 Claude vs OpenCode 的 feature parity 对照。citeturn18view0turn19view1

代价也明显：组件多意味着升级/调试成本上升；如果你只需要“规范化变更流程”或“TDD 方法论”，OpenSpec/Superpowers 可能更轻。citeturn27view0turn42view0

适用场景：
- 需要“一套跨 harness 的工程化 Super Prompt 系统”，且团队愿意维护更复杂的工具链；
- 希望把包管理器、hooks、命令、安全/学习等能力统一治理。citeturn18view0turn20view0
⸻
gsd-build/get-shit-done

简要定位：面向 Claude Code/OpenCode/Gemini CLI/Codex 的“轻量但强力”的 meta-prompting + context engineering + spec-driven 流程系统。它用命令编排完整生命周期：新项目→按 phase 讨论/规划→并行执行→验证→里程碑审计/归档。citeturn34view0turn37view0

安装与 setup

交互式安装：
npx get-shit-done-cc@latest

安装器会提示选择 runtime（Claude Code/OpenCode/Gemini/Codex/All）与安装位置（Global/Local）。citeturn34view0

验证安装：Claude/Gemini 用 /gsd:help；OpenCode 用 /gsd-help；Codex 用 $gsd-help。citeturn34view0turn33view2

非交互安装（CI/Docker/脚本）：支持 --claude/--opencode/--gemini/--codex/--copilot/--all 与 --global(-g)/--local(-l)；并支持 --uninstall(-u) 完整卸载。citeturn41view4turn33view3

此外，安装器支持 --config-dir <path> 指定自定义配置目录，并声明它优先于 CLAUDE_CONFIG_DIR / GEMINI_CONFIG_DIR / CODEX_HOME / COPILOT_CONFIG_DIR 等环境变量。citeturn41view4

安装器 help 的“完整选项”（Exhaustive）：
- 位置：npx get-shit-done-cc [options]
- 选项：-g/--global、-l/--local、--claude、--opencode、--gemini、--codex、--copilot、--all、-u/--uninstall、-c/--config-dir <path>、-h/--help、--force-statusline；并展示了大量示例（Claude/Gemini/Codex/Copilot/All/自定义目录/卸载等）。citeturn41view4

Exhaustive：GSD 命令清单、参数变体、配置项与惯用法

GSD 的“命令面”建议以 User Guide 的 Command Reference 为准（它比 README 更全）。其核心命令分组如下：

Core Workflow（全生命周期）：
- /gsd:new-project：完整初始化（问题→研究→需求→路线图）citeturn37view0
- /gsd:new-project --auto @idea.md：从文档自动化 init（PRD/idea doc 场景）citeturn37view0
- /gsd:discuss-phase [N]：在规划前锁定实现偏好（参数 N 为 phase 序号）citeturn37view0
- /gsd:ui-phase [N]：UI 设计契约（前端 phase）citeturn37view0
- /gsd:plan-phase [N]：研究 + 计划 + 校验citeturn37view0
- /gsd:execute-phase <N>：按依赖分 wave 并行执行citeturn37view0turn37view0
- /gsd:verify-work [N]：人工 UAT + 自动诊断citeturn37view0
- /gsd:ui-review [N]：retroactive 视觉审计（前端）citeturn37view0turn37view0
- /gsd:audit-milestone：验证里程碑 DoD（definition of done）citeturn37view0
- /gsd:complete-milestone：归档里程碑、打 tagciteturn37view0turn33view1
- /gsd:new-milestone [name]：启动下一里程碑周期citeturn37view0turn33view1

Navigation：/gsd:progress /gsd:resume-work /gsd:pause-work /gsd:help /gsd:update /gsd:join-discord。citeturn37view0

Phase Management：/gsd:add-phase /gsd:insert-phase [N] /gsd:remove-phase [N] /gsd:list-phase-assumptions [N] /gsd:plan-milestone-gaps /gsd:research-phase [N]。citeturn37view0

Brownfield & Utilities：/gsd:map-codebase /gsd:quick /gsd:debug [desc] /gsd:add-todo /gsd:check-todos /gsd:settings /gsd:set-profile <profile> /gsd:reapply-patches。citeturn37view0turn36view2

配置文件（核心）：GSD 在项目根写入 .planning/config.json，并在 User Guide 给出 schema 与字段说明：
- mode：interactive|yolo
- granularity：coarse|standard|fine
- model_profile：quality|balanced|budget
- planning.commit_docs、planning.search_gitignored
- workflow.research / plan_check / verifier / nyquist_validation / ui_phase / ui_safety_gate（其中 nyquist_validation 是“验证架构层”，把需求映射到自动化测试命令，用作 plan-check 的额外维度）citeturn37view2turn35view0
- git.branching_strategy：none|phase|milestone，以及 branch template。citeturn37view2turn33view1

安全、权限与敏感信息防护

GSD 推荐在 Claude Code 用 claude --dangerously-skip-permissions 以减少频繁授权打断；同时也提供“细粒度 allow 列表”的替代方案（对 date/ls/mkdir/git add/commit/status/log/diff/tag 等 Bash 命令进行 allow）。citeturn34view0

此外它强调对敏感文件做 deny list（例如 .env、**/secrets/*、**/*.pem 等），以阻止 Claude 读取。citeturn33view0

开发、测试、调试与完整修复流程（step-by-step）

开发安装（用于贡献/调试）：README 给出 clone 后运行本地 installer：node bin/install.js --claude --local，用于把修改安装到 ./.claude/ 做验证。citeturn34view0turn41view4

仓库脚本与测试：get-shit-done-cc 的 package.json 指定 bin 为 bin/install.js，并提供 npm run test（node scripts/run-tests.cjs）与覆盖率门槛（c8 --check-coverage --lines 70 ...）。citeturn38view0

推荐的 bug-fix 工作流（强一致、可审计）：
1. 复现定位：优先用 /gsd:debug "描述" 生成“持久化调试状态”，或用 /gsd:quick 做目标性修复；对流程级问题（phase/milestone）先用 /gsd:progress 看状态。citeturn37view0turn36view2
2. 把问题转成可验证的契约：如果是功能 bug，把验证步骤固化到对应 phase 的验证产物中；GSD 的 nyquist_validation 机制强调“在写代码前建立反馈机制”。citeturn35view0turn37view2
3. 隔离变更：按配置选择 git.branching_strategy=phase|milestone；对已错误执行的 phase，User Guide 的恢复条目建议 git revert phase commits 后再 re-plan。citeturn37view2turn36view2
4. 执行修复与验证：重跑 planning/execution/verify；前端问题补 /gsd:ui-review，并注意它会把截图落到 .planning/ui-reviews/ 并自动写 .gitignore。citeturn37view0
5. 回归与归档：通过 /gsd:audit-milestone 与 /gsd:complete-milestone 确保 DoD 达成并归档。citeturn37view0turn35view0

优势/局限/与其他差异：
- 优势：把并行执行（wave）、验证架构（Nyquist layer）、里程碑审计/归档集成为“命令级工作流”，非常适合“要快但不要烂”的个人/小团队。citeturn37view0turn35view0
- 局限：更偏“流程系统”而非“通用 schema 引擎”；相比 OpenSpec 的可自定义 schema/模板/CLI 体系，GSD 的扩展更依赖其既定命令与 .planning 结构。citeturn31view3turn37view2

适用场景：
- 从 0 到 1 构建产品或对既有代码做连续迭代，想要强规划/强执行/强验证但不想引入“企业流程戏剧”；
- 你需要“按阶段拆解 + 并行执行 + 验证闭环 + 里程碑归档”的一套默认工程方法。citeturn34view0turn37view0
⸻
Fission-AI/OpenSpec

简要定位：OpenSpec 是“spec-driven development（SDD）”框架：把变更从聊天意图变成仓库内明确的 change/spec/design/tasks 产物，并提供强 CLI（openspec）+ 强 AI 指令（OPSX）+ 可自定义 schema/模板/依赖图引擎。citeturn27view0turn29view1turn31view3

安装与初始化

官方安装要求：Node.js >= 20.19.0，全局安装 @fission-ai/openspec 后使用 openspec init 初始化项目（创建目录结构、生成 AGENTS.md 指南并引导配置各 AI 工具）。citeturn26view2turn43view0turn32view3

Exhaustive：OpenSpec CLI（命令、子命令、参数、flags、环境变量）

OpenSpec 在 docs/cli.md 给出完整 CLI Reference；以下为按“可执行面”整理的 完整命令树（含关键 flags），并标注哪些适合脚本/agent（--json）。

全局通用选项（所有命令可用）：--version/-V、--no-color、--help/-h。citeturn32view3

初始化与更新：
- openspec init [path] [options]
    - --tools <list>：all/none/逗号分隔工具ID；工具 ID 列表包含 amazon-q, antigravity, auggie, claude, cline, codex, ... , windsurf 等citeturn32view3
    - --force：自动清理 legacy 文件，跳过提示citeturn32view3
    - --profile <core|custom>：覆盖全局 profileciteturn32view3
- openspec update [path] [options]：升级 CLI 后重生成工具配置文件；--force 强制更新。citeturn32view4

浏览与查看：
- openspec list [options]：--specs / --changes / --sort <recent|name> / --jsonciteturn30view1
- openspec view：交互式 dashboardciteturn32view0
- openspec show [item-name] [options]：
    - 通用：--type <change|spec>、--json、--no-interactiveciteturn30view2
    - change 特化（JSON）：--deltas-onlyciteturn30view2
    - spec 特化（JSON）：--requirements、--no-scenarios、-r/--requirement <id>citeturn30view2

验证与归档：
- openspec validate [item-name] [options]：--all/--changes/--specs、--type <change|spec>、--strict、--json、--concurrency <n>、--no-interactive；并支持环境变量 OPENSPEC_CONCURRENCY（默认 6）。citeturn30view0turn30view4
- openspec archive [change-name] [options]：-y/--yes、--skip-specs、--no-validate；并明确归档步骤（验证→确认→合并 delta specs→移动到按日期归档目录）。citeturn30view3turn30view3

工作流支撑（给 agent/脚本的结构化接口）：
- openspec status [options]：--change <id>、--schema <name>、--jsonciteturn31view0
- openspec instructions [artifact] [options]：artifact 可为 proposal/specs/design/tasks/apply；--change、--schema、--json；输出包含 template、project context、依赖产物内容与 per-artifact rules。citeturn31view1turn32view2
- openspec templates [options]：--schema <name>、--jsonciteturn31view2
- openspec schemas [options]：--json，并展示 schema flow。citeturn31view3

Schema 管理（可扩展性核心）：
- openspec schema init <name> [options]：--description、--artifacts <list>、--default/--no-default、--force、--jsonciteturn31view3
- openspec schema fork <source> [name] [options]：--force、--jsonciteturn31view3
- openspec schema validate [name] [options]：--verbose、--jsonciteturn31view3
- openspec schema which [name] [options]：--all、--json，并定义 schema precedence（Project → User → Package）。citeturn31view3

全局配置（非项目内 config.yaml，而是 global config）：
- openspec config <subcommand>：path/list/get/set/unset/reset/edit/profile；并给出 set ... --string、reset --all --yes 等示例与 profile 交互式向导语义。citeturn30view4

实用命令：
- openspec feedback <message> [--body <text>]（需要已认证的 GitHub CLI gh）citeturn30view4
- openspec completion <generate|install|uninstall> [bash|zsh|fish|powershell]citeturn30view4

环境变量（Exhaustive，文档明确列出）：OPENSPEC_CONCURRENCY、EDITOR/ VISUAL（用于 config edit）、NO_COLOR。citeturn30view4

Telemetry（隐私/合规相关）：OpenSpec README 声明收集匿名使用统计，仅包含“命令名与版本号”，不收集参数、路径、内容或 PII，并在 CI 自动禁用；可通过 OPENSPEC_TELEMETRY=0 或 DO_NOT_TRACK=1 退出。citeturn26view0

Exhaustive：OPSX/AI 指令（slash commands）、语法差异与 legacy 命令

OpenSpec docs/commands.md 与 docs/opsx.md 给出 OPSX 的命令集、用途与语法差异：

默认 quick path（core profile）：/opsx:propose /opsx:explore /opsx:apply /opsx:archive。citeturn28view0turn29view0

扩展工作流（可选）：/opsx:new /opsx:continue /opsx:ff /opsx:verify /opsx:sync /opsx:bulk-archive /opsx:onboard。citeturn28view0turn29view0

语法差异（不同工具）示例：Claude Code 用 /opsx:propose，Cursor/Windsurf/Copilot(IDE) 用 /opsx-propose；Trae 采用 skill-based invocations（如 /openspec-propose）。citeturn28view0

Legacy commands 仍可用但官方推荐 OPSX：/openspec:proposal /openspec:apply /openspec:archive。citeturn28view0

配置与模板（项目内 openspec/config.yaml）与可扩展 Schema

OpenSpec 允许在 openspec/config.yaml 注入：
- schema（默认 schema）、
- context（注入到所有 artifact 指令，且限制 50KB）、
- rules（按 artifact id 定向注入规则）。citeturn29view0turn29view0

Schema precedence（用于解释“为什么我的 schema 没生效”）为：CLI --schema → change 目录的 .openspec.yaml → project config → 默认。citeturn29view0

自定义 schema 提供完整生命周期：schema init/fork/validate/which，并规定 schema 存储位置为项目本地 openspec/schemas/ 或用户全局目录。citeturn29view2turn31view3

开发、测试、调试与完整修复流程（step-by-step）

OpenSpec README 的开发指南：pnpm install、pnpm run build、pnpm test、本地开发 CLI pnpm run dev 或 pnpm run dev:cli。citeturn26view0turn43view0

package.json 显示测试基于 Vitest（含 test:watch/test:ui/test:coverage），并有 postinstall、changeset 发布流程；引擎要求 Node >=20.19.0。citeturn43view0

推荐的 bug-fix 工作流（与 OpenSpec 架构一致）：
1. 复现并定位命令面：是 CLI（openspec ...）、还是 OPSX 生成的 skill/command 文件、还是 schema/模板解析；优先用 openspec validate --all --json 定位结构性问题并可在 CI 复现。citeturn30view0turn29view1
2. 并行验证调优：大仓库可用 --concurrency 或 OPENSPEC_CONCURRENCY 加速批量验证，但要避免过高并发压垮 CI。citeturn30view0turn30view4
3. 对产物做差分回归：修复后跑 openspec templates/openspec schemas/openspec instructions ... --json，确保模板解析与依赖图输出稳定。citeturn31view1turn31view2turn31view3
4. 归档路径回归：对 archive 的路径移动与 delta specs merge 必须回归（CLI 明确了归档步骤与目录结构）。citeturn30view3

安全、性能与扩展最佳实践

- 安全/合规：注意 telemetry 默认开启（除 CI），团队环境若合规要求严格需显式设 OPENSPEC_TELEMETRY=0 或 DO_NOT_TRACK=1。citeturn26view0
- 性能：OpenSpec 的 validate --concurrency 是显式性能旋钮；建议在本地/CI 分别设不同 concurrency，并把 --json 输出作为机器可解析接口。citeturn30view0turn27view0
- 扩展：真正的规模化来自 schema/模板自定义（schema init/fork），把你团队的“规范产物”编码进流程，而不是靠更长 prompt。citeturn31view3turn29view1

优势/局限/与其他差异：
- 优势：CLI 与工作流抽象最“框架化”，且通过 schemas 把流程与模板分离，适配 20+ 工具（init 的 tools 列表体现了其生态目标）。citeturn32view3turn31view3
- 局限：对“只想立刻开始写代码”的用户来说，前期产物生成会增加步骤；但这正是它追求可重复性的代价（工程权衡）。citeturn28view0turn30view3

适用场景：
- 团队需要“变更提案/规格/设计/任务”可审计、可 code review、可复用，并能跨不同 coding agent/harness 保持一致；
- 想把 agent 使用从“聊天记录依赖”升级到“仓库内 source-of-truth”。citeturn28view0turn29view1turn27view0
⸻
obra/superpowers

简要定位：Superpowers 是“技能框架 + 软件开发方法论”，核心是让 agent 在写代码前先提炼 spec、输出可读设计、生成粒度极细的计划，并强制执行 TDD、两阶段 review、worktree 分支与收尾流程；技能自动触发，用户不必记命令。citeturn42view0turn44view0

安装与多平台集成（Exhaustive）

Claude Code（官方 marketplace）：/plugin install superpowers@claude-plugins-official。citeturn42view0

Claude Code（自建 marketplace）：/plugin marketplace add obra/superpowers-marketplace → /plugin install superpowers@superpowers-marketplace。citeturn42view0

Cursor：/add-plugin superpowers 或在 marketplace 搜索安装。citeturn42view0

Gemini CLI：gemini extensions install https://github.com/obra/superpowers；更新：gemini extensions update superpowers。citeturn42view0

Codex（手工/半自动，skills discovery）：官方文档给出两条路径：
- 让 Codex 自己抓取并执行安装说明（指向 .codex/INSTALL.md）；citeturn42view0turn46view0
- 手工安装：clone 到 ~/.codex/superpowers，并把 skills 通过 symlink 暴露到 ~/.agents/skills/superpowers，再重启 Codex；可选开启 Codex 的 collab=true 以使用需要协作/子代理的技能。citeturn46view0

OpenCode（手工安装 + plugin + skills symlink，工程化最强）：文档给出 Quick Install 与 macOS/Linux/Windows 全套脚本化步骤：
- clone 到 ~/.config/opencode/superpowers；
- 创建 ~/.config/opencode/plugins 与 ~/.config/opencode/skills；
- 插件入口 ~/.config/opencode/superpowers/.opencode/plugins/superpowers.js symlink 到 ~/.config/opencode/plugins/superpowers.js；
- skills 目录 symlink/junction 到 ~/.config/opencode/skills/superpowers；并重启 OpenCode。citeturn46view1

- 文档还给出 OpenCode 调试方式：opencode run "test" --print-logs --log-level DEBUG。citeturn46view1

Exhaustive：技能（skills）与命令（commands）清单

skills（仓库目录枚举）：brainstorming, dispatching-parallel-agents, executing-plans, finishing-a-development-branch, receiving-code-review, requesting-code-review, subagent-driven-development, systematic-debugging, test-driven-development, using-git-worktrees, using-superpowers, verification-before-completion, writing-plans, writing-skills。citeturn44view0

commands（仓库目录枚举）：brainstorm.md, execute-plan.md, write-plan.md。citeturn45view0

基本工作流（方法论层）

README 明确列出 7 步“基础工作流”：brainstorming → using-git-worktrees → writing-plans → subagent-driven-development/executing-plans → test-driven-development（红绿重构）→ requesting-code-review → finishing-a-development-branch；并强调“在任何任务前检查相关 skills，属于强制流程”。citeturn42view0

开发、测试、调试与完整修复流程（step-by-step）

Superpowers 给出了显式测试指南，尤其是复杂技能（如 subagent-driven-development）的集成测试：
- 测试思想：通过 headless Claude Code 会话运行真实技能，并基于 session transcript 验证行为。citeturn46view2
- 目录结构示例：tests/claude-code/test-subagent-driven-development-integration.sh、analyze-token-usage.py 等。citeturn46view2
- 运行条件：必须从“superpowers plugin 目录”运行；需要 claude 命令可用；并要求在 ~/.claude/settings.json 开启本地 dev marketplace（示例键："superpowers@superpowers-dev": true）。citeturn46view2

建议的 bug-fix 工作流：
1. 复现：先在具体 harness（Claude/OpenCode/Codex）复现，记录触发的 skill（例如 systematic-debugging 或 executing-plans）。citeturn42view0turn46view1
2. 建测试：对关键行为优先写集成测试（文档强调复杂技能需要真实会话验证）。citeturn46view2
3. 修复：修改对应 skill 的 SKILL.md 或插件注入逻辑（OpenCode 侧通过 experimental.chat.system.transform 注入 using-superpowers 内容）。citeturn46view1
4. 回归：
    - Claude：运行集成测试脚本；
    - OpenCode：用 opencode run --print-logs 验证 plugin 加载、skills 可发现与 bootstrap 注入。citeturn46view1turn46view2

安全、性能与扩展最佳实践

- 扩展（个人/项目 skills）：Codex 与 OpenCode 指南都示范了自定义 skill 的 frontmatter 写法，并强调 description 是自动触发的关键条件表达。citeturn46view0turn46view1
- 性能与可控性：Superpowers 的“计划拆分为 2–5 分钟任务 + 每任务给出验证步骤 + 两阶段 review”本质上是在降低单次上下文负担并提高错误发现率（这是从其设计目标推导的工程效果）。citeturn42view0turn46view2
- OpenCode 可观测性：文档给出日志级别 DEBUG 的运行方式，适合作为插件加载/注入问题的第一排查点。citeturn46view1

优势/局限/与其他差异：
- 优势：方法论非常强，尤其对 TDD/代码审查/分支工作流的强制执行；并且对 OpenCode/Codex 的“skill discovery + symlink/junction”集成讲得很工程化。citeturn46view1turn46view0turn42view0
- 局限：它不提供像 OpenSpec 那样的“schema 驱动产物依赖图与 CLI 管理层”；更适合把“开发行为”规范化，而不是把“变更规格产物”框架化。citeturn31view3turn42view0

适用场景：
- 你信奉或希望强制落地 TDD 与严格 review，并愿意用“技能即流程”来约束 agent；
- 你在 OpenCode/Codex 上需要可靠的技能自动发现与注入机制，并希望有可操作的安装/调试/测试手册。citeturn46view1turn46view0turn46view2
⸻
横向对比、差异点与决策矩阵

命令与 CLI 面对比（摘要表）
项目	可执行 CLI 入口	CLI 子命令/功能面	主要“会话内命令/触发面”	配置落盘核心位置
compound-engineering-plugin	compound-plugin（Bun/TS）citeturn15view0	convert/install/list/sync，并有 --to/--scope/--permissions/... 等citeturn13view2turn11view1turn13view4turn14view0	既是 Claude 插件（agents/skills/commands），又提供跨工具转换/同步citeturn3view0	Claude home ~/.claude 与各 target 配置目录（sync/convert 决定）citeturn13view4turn13view2
ECC	install.sh（Node 安装器入口）citeturn22view0turn24view0	--target/--profile/--modules/--with/--without/--dry-run/--jsonciteturn24view0	commands/ 目录列出大量命令（约 40）citeturn21view0；OpenCode 侧 README 列出 31+ 命令citeturn19view2	rules/skills/hooks/commands 等分散于 .claude/.cursor/.opencode/... 与仓库目录citeturn18view0turn20view0
GSD	npx get-shit-done-cc（安装器 CLI）citeturn41view4	安装/卸载/目录选择：--claude/--opencode/... --global/--local --config-dir --uninstall ...citeturn41view4	/gsd:* 完整生命周期命令集（含 --auto @idea.md 变体）citeturn37view0	项目 .planning/config.json + 各 harness 命令/skills 落盘目录citeturn37view2turn33view0
OpenSpec	openspec（Node/TS CLI）citeturn43view0turn27view0	init/update/list/view/show/validate/archive/status/instructions/templates/schemas/schema*/config*/feedback/completionciteturn27view0turn31view3turn30view4	OPSX：/opsx:* + legacy /openspec:*，跨工具语法差异citeturn28view0turn29view0	openspec/ 目录（specs/changes/config.yaml/schemas/…）+ 生成的工具配置文件citeturn32view3turn29view0
Superpowers	无统一 CLI；靠 marketplace/插件/手工脚本安装citeturn42view0	OpenCode/Codex 给出脚本化安装与验证命令（如 opencode run --print-logs ...）citeturn46view1turn46view0	skills 自动触发为主；另有 3 个 command 文件（brainstorm/write-plan/execute-plan）citeturn44view0turn45view0	各 harness 的 skills 发现目录（如 OpenCode ~/.config/opencode/skills/、Codex ~/.agents/skills/）citeturn46view1turn46view0

运行时/生态支持对比（从官方说明归纳）
项目	明确支持的 harness/IDE（官方文本出现者）	跨平台（Win/macOS/Linux）	生态扩展方式
compound-engineering-plugin	目标格式包含 opencode/codex/cursor/pi/copilot/gemini/kiro/windsurf/openclaw/qwen 等citeturn13view2turn11view1；sync 支持若干工具citeturn5view0turn13view4	未在本次摘录中显式写“跨平台”，但基于 Node/Bun CLI 推断可跨平台（推断）citeturn15view0	新 target 通过 targets/writer/converter 扩展（从代码结构推断）；sync targets 通过 registry 扩展（推断）citeturn7view0turn13view4
ECC	Claude Code、Cursor、OpenCode、Codex 等（README 多处）citeturn18view0turn20view0	明确写“Windows/macOS/Linux fully supports”citeturn18view0	通过新增 commands/skills/hooks/rules/MCP configs 等扩展citeturn18view0turn21view0
GSD	Claude Code、OpenCode、Gemini CLI、Codex（README）citeturn34view0turn33view2；安装器还包含 Copilot 选项citeturn41view4	明确写“Works on Mac, Windows, and Linux”citeturn34view0	配置通过 .planning/config.json 与 workflow toggles；命令体系扩展通常由项目新增citeturn37view2turn37view0
OpenSpec	init --tools 列表显示覆盖面极广（含 claude/cursor/codex/opencode/gemini/...）citeturn32view3	CLI 面向 Node 20.19+（跨平台常规可用）citeturn26view2turn43view0	Schema/模板是第一扩展点（schema init/fork/...）citeturn31view3turn29view2
Superpowers	Claude Code、Cursor、Codex、OpenCode、Gemini CLI（README + guides）citeturn42view0turn46view1turn46view0	OpenCode/Codex guide 明确给 Windows 步骤；整体可跨平台citeturn46view1turn46view0	以 skills 为单元扩展；用户可在个人/项目目录新增 skill（frontmatter 触发）citeturn46view0turn46view1

License 与成熟度对比（可量化 / 可审计指标）
项目	License	版本/发布线索	测试与质量线索	热度（⭐/fork，约）
compound-engineering-plugin	MITciteturn47view0	@every-env/compound-plugin version 2.37.0citeturn15view0	bun test + 大量 target/sync 测试文件citeturn15view0turn17view0	~10.4k / 827citeturn12view0
ECC	仓库标注 MIT licenseciteturn20view0	README“v1.8.0（Mar 2026）”citeturn20view0	README 提到 “997 internal tests passing”citeturn20view0	~76.4k / 9.5kciteturn20view0
GSD	package.json 指定 MITciteturn38view0	get-shit-done-cc version 1.22.4citeturn38view0	node scripts/run-tests.cjs + 覆盖率门槛行覆盖率 70%citeturn38view0	~30.3k / 2.5kciteturn34view0
OpenSpec	MITciteturn26view0turn43view0	@fission-ai/openspec version 1.2.0citeturn43view0turn26view4	Vitest（含 coverage/UI）+ dev:cli 本地运行citeturn43view0turn26view0	~30.7k / 2kciteturn26view1
Superpowers	README 标注 MITciteturn42view0	tags 存在（仓库页面）citeturn42view0	有真实会话集成测试指南（10–30 分钟级）citeturn46view2	~84.7k / 6.6kciteturn42view0

典型需求 → 推荐库的决策矩阵
需求/约束	最推荐	次推荐	不优先/原因
快速原型，但希望质量底线（规划/验证闭环）	GSDciteturn37view0turn35view0	Superpowersciteturn42view0turn44view0	OpenSpec：前期产物生成增加步骤（权衡）；compound-plugin：不是流程系统citeturn28view0turn7view0
生产级“变更规范/可审计产物/可复用模板”	OpenSpecciteturn27view0turn31view3turn30view3	OpenSpec + Superpowers（规格 + 执行方法论组合，推断）citeturn31view3turn42view0	仅用 Superpowers/GSD：规格层的 schema/模板/依赖图能力较弱citeturn31view3turn37view0
多工具/多 IDE 迁移与配置对齐（Claude ↔ OpenCode/Codex/…）	compound-engineering-pluginciteturn13view2turn13view4	OpenSpec（init --tools all + 生成配置，偏规则/指令）citeturn32view3	GSD/Superpowers/ECC：主要是工作流/技能，不是“通用转换器”citeturn7view0turn37view0turn42view0
强多代理并行与任务分解（降低上下文腐化）	GSD（wave 并行执行）citeturn37view0turn37view0	Superpowers（parallel agents/subagent-driven-development）citeturn44view0turn46view2；ECC（/orchestrate、多模型协作命令）citeturn19view2turn21view0	OpenSpec：偏规格与产物编排，不直接提供并行执行引擎citeturn29view2turn30view3
自定义工作流（按团队流程定制 artifacts 与依赖）	OpenSpec（schema/模板）citeturn31view3turn29view2	ECC（profile/modules/with/without 按组件安装，但更像“装什么”而不是“流程schema”）citeturn24view0	GSD/Superpowers：自定义更多靠新增命令/skill，而非可声明式 schemaciteturn37view2turn46view0
离线/低成本模型（依赖 OpenCode 之类 free/local 模型）	Superpowers（OpenCode guide 很完善）citeturn46view1	OpenSpec（工具无关，且强调不需 API key 的定位在其外部站点；本次以仓库 CLI 为主）citeturn27view0turn32view3	ECC/GSD：更偏 Claude 生态与特定工作流，虽可在 OpenCode 使用但需要适配成本citeturn19view2turn33view2

工作流结构对照图（Mermaid）

OpenSpec（OPSX：artifact 依赖图驱动）
flowchart LR
  A["/opsx:propose 或 /opsx:new"] --> B["proposal/specs/design/tasks 产物生成"]
  B --> C["/opsx:apply 按 tasks 实现"]
  C --> D["/opsx:verify 校验实现与产物一致"]
  D --> E["/opsx:archive 合并 delta specs 并归档 change"]
  B -.-> X["openspec status/instructions/validate --json 作为结构化接口"]

（CLI 对 status/instructions/templates/schemas/schema* 的描述与示例体现了“结构化接口 + 依赖图引擎 + 可自定义 schema”。citeturn31view1turn31view3turn29view1）

GSD（里程碑/阶段流水线 + 并行 wave 执行）
flowchart TD
  NP["/gsd:new-project"] --> DP["/gsd:discuss-phase N"]
  DP --> UIP["/gsd:ui-phase N（前端可选）"]
  UIP --> PP["/gsd:plan-phase N"]
  PP --> EP["/gsd:execute-phase N（按依赖分 wave 并行）"]
  EP --> VW["/gsd:verify-work N"]
  VW --> AM["/gsd:audit-milestone"]
  AM --> CM["/gsd:complete-milestone"]

（User Guide 的“Full Project Lifecycle / Execution Wave Coordination”与命令清单对应此结构。citeturn35view0turn37view0）

Superpowers（skills 自动触发的强制工程方法论）
flowchart LR
  U["用户提出需求/问题"] --> S["using-superpowers（引导选择技能）"]
  S --> B["brainstorming（澄清设计/产出设计文档）"]
  B --> W["using-git-worktrees（隔离分支）"]
  W --> P["writing-plans（2-5分钟任务+验证步骤）"]
  P --> E["subagent-driven-development / executing-plans（两阶段审查）"]
  E --> T["test-driven-development（红绿重构）"]
  T --> R["requesting-code-review / receiving-code-review"]
  R --> F["finishing-a-development-branch（收尾合并/清理）"]

（技能清单与 README 的基础工作流逐项对应。citeturn42view0turn44view0）

通用最佳实践：安全、性能与规模化

这些最佳实践不是“泛泛建议”，而是从五个项目的共同结构中抽出来的可执行原则（并尽量映射到项目提供的机制）：

把“意图”变成仓库内产物，而不是聊天记录：OpenSpec 通过 openspec/ 目录、change/spec 结构与 archive 流程把意图固化；GSD 把关键状态与计划固化到 .planning/；Superpowers 强制输出设计与计划文档。citeturn32view3turn37view2turn42view0

把验证前置为“反馈合约”：GSD 的 nyquist_validation 明确要求在计划阶段建立测试映射；Superpowers 强制 TDD；OpenSpec 的 validate 与 archive 默认把结构校验纳入生命周期。citeturn37view2turn46view2turn30view3

并行化要“分波次、控依赖、可回滚”：GSD 把并行执行组织为 wave；Superpowers 有并行子代理技能；OpenSpec 的 validate --concurrency 给出显式控制旋钮。citeturn37view0turn44view0turn30view0

敏感信息默认拒读/避免复制扩散：GSD 提供 deny list 示例用于阻止读取敏感文件；compound-plugin sync 会复制 MCP env vars 并明确警告可能含 secrets；因此团队实践应将“配置文件分享/提交”与“secret 扫描”纳入流程。citeturn33view0turn13view4

把“环境差异”变成可配置项，而不是隐式行为：ECC 的包管理器优先级与 hook profile 是典型做法；GSD 的 --config-dir 与多环境变量优先级让容器/多配置更可控；OpenSpec 的 --tools/--profile 与 config profile 让生成内容可重复。citeturn18view0turn41view4turn32view3turn30view4

升级与配置漂移治理：OpenSpec update 专门用于升级后刷新生成文件，并在 releases 中提到“config drift warning”；GSD 提供 /gsd:update 和 /gsd:reapply-patches；ECC 安装器支持 --dry-run/--json 先看计划再落盘。citeturn32view4turn26view4turn37view0turn24view0
⸻
附录：官方链接与仓库入口

EveryInc/compound-engineering-plugin
- https://github.com/EveryInc/compound-engineering-plugin

affaan-m/everything-claude-code
- https://github.com/affaan-m/everything-claude-code

gsd-build/get-shit-done
- https://github.com/gsd-build/get-shit-done

Fission-AI/OpenSpec
- https://github.com/Fission-AI/OpenSpec
- OpenSpec Docs（安装要求等）：https://thedocs.io/openspec/installation/

obra/superpowers
- https://github.com/obra/superpowers
- Superpowers OpenCode Guide（raw）：https://raw.githubusercontent.com/obra/superpowers/main/docs/README.opencode.md
- Superpowers Codex Guide（raw）：https://raw.githubusercontent.com/obra/superpowers/main/docs/README.codex.md


附录：本次检索关键词的中文翻译

下面给出“实际检索意图”的中文表述（方便你复用/扩展搜索）；括号内对应本次检索的英文/原始关键词表达：

- 查找 compound-engineering-plugin 的官方仓库与说明（“EveryInc compound-engineering-plugin GitHub”）
- 查找 everything-claude-code 的官方仓库与命令/安装说明（“affaan-m everything-claude-code GitHub”）
- 查找 get-shit-done 的官方仓库、命令清单与安装器参数（“get-shit-done agent spec GitHub” / “npx get-shit-done-cc flags”）
- 确认 OpenSpec 的官方上游仓库、CLI reference、OPSX 指令与安装要求（“openspec.dev github repository” / “Fission-AI OpenSpec docs cli commands” / “OpenSpec CLI init update validate archive”）
- 查找 superpowers 的官方仓库，以及其在 OpenCode/Codex 的安装/调试/测试文档（“obra/superpowers GitHub” / “Superpowers OpenCode INSTALL.md skills” / “Superpowers Codex skills symlink”）
