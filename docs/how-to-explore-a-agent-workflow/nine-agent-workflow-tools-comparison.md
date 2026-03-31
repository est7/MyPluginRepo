# Agent 工作流工具全景分析

结论先给：没有一个”全场最佳”，只有”在你当前约束下最合适”。如果你是个人开发者、主力用 Claude Code、想少 ceremony 多产出，我会先看 GSD；如果你做的是长期维护的现有代码库，要规格可审计、变更可回放，我会先看 OpenSpec；如果你要最完整、最“规格驱动正统派”的链路，我会看 Spec Kit；如果你要 TDD/工艺纪律，我会看 Superpowers；如果你要 repo-aware 的计划→执行→审查→沉淀闭环，我会看 Compound Engineering/workflows；如果你要组织级、多角色、多 track 的大流程，才上 BMAD；如果你只是想解决长会话失忆，不想引入大框架，用 planning-with-files；如果你要让 agent 反复 fresh-context 干到 PRD 清零，用 Ralph。

## 1. GSD / get-shit-done

定位：反 bureaucracy 的 spec-driven 工作流，作者明确把它写成“个人开发者高吞吐量系统”，重点是解决 context rot。核心路径是 PROJECT.md、REQUIREMENTS.md、ROADMAP.md、STATE.md、.planning/research/，每个 phase 还会产出 {n}-CONTEXT.md、{n}-RESEARCH.md、{n}-{k}-PLAN.md、{n}-VERIFICATION.md，quick 模式走 .planning/quick/...。核心命令是 /gsd:new-project、/gsd:discuss-phase、/gsd:plan-phase、/gsd:execute-phase、/gsd:verify-work、/gsd:complete-milestone、/gsd:new-milestone、/gsd:quick；安装用 npx get-shit-done-cc@latest，Claude/OpenCode/Codex 的命令前缀还不一样。优点是：阶段清楚、fresh-context 执行强、原生把“研究/计划/执行/验证”串起来；缺点是：它把复杂度藏在系统内部，出了偏差你要理解它的文件协议，而且 repo 还推荐 claude --dangerously-skip-permissions，我不建议在公司仓库或高风险仓库里无脑照做，最好改成 allowlist。适合：单兵开发、从想法到功能落地、你愿意信任系统帮你做大量 orchestration。

## 2. OpenSpec
定位：轻量、brownfield-first 的 spec/change management。它把“当前真相”和“拟议变更”分开：openspec/specs/ 放现状规范，openspec/changes/<change>/ 放 proposal/tasks/design/spec delta，这个结构对老项目非常友好。核心命令是 openspec init、openspec list、openspec show、openspec validate、openspec archive，AI 侧常用 /openspec:proposal、/openspec:apply、/openspec:archive；新版还有更流动的 OPSX：/opsx:new、/opsx:continue、/opsx:ff、/opsx:apply、/opsx:archive。优点是：变更可审计、diff 语义清晰、跨工具兼容好；缺点是：执行自动化本身不算强，更像“规格层”而不是“自动施工队”。适合：现有项目增量迭代、多人协作、需要 reviewable spec delta。

## 3. Spec Kit / speckit
定位：规格驱动的“全套正统流”，强调 constitution → specification → plan → tasks → implement 的完整链路。核心路径是 .specify/memory/constitution.md、.specify/scripts/...、specs/001-foo/spec.md，继续规划后会长出 research.md、plan.md、quickstart.md、data-model.md、contracts/ 等。CLI 是 specify init、specify check；AI 命令在文档里同时出现了两套写法：GitHub README 用 /speckit.constitution、/speckit.specify、/speckit.plan、/speckit.tasks、/speckit.implement，官网 quick start 又展示了短命令 /specify、/plan、/tasks、/implement。这不是你记混了，而是不同文档/集成层存在命名漂移，实际以 specify init 生成到你 agent 里的命令为准。优点是：artifact 完整、治理感强、很适合需要规范化产出的团队；缺点是：ceremony 比 OpenSpec 更重。还有一个重要点：OpenSpec 官方把自己描述成更偏 brownfield，而 Spec Kit 现在也公开给了 brownfield demo，所以它已经不只是 greenfield 工具了。

## 4. planning-with-files / planwithfiles
定位：不是大方法论，而是持久化工作记忆。核心路径非常简单：task_plan.md、findings.md、progress.md。核心命令是 /planning-with-files:plan（autocomplete 输 /plan）、/planning-with-files:status（/plan:status）、/planning-with-files:start（/planning）。它还靠 hooks 做几件事：关键决策前重读 plan、写文件后提醒更新状态、停止前验证完成、/clear 后做 session recovery。优点是：轻、直接、对抗长会话失忆特别有效；缺点是：它本质上只是 memory discipline，不是完整的 spec / architecture / implementation framework，文档如果不持续维护，很快就会变成另一种“过期上下文”。适合：多步任务、研究型任务、跨很多 tool call 的复杂会话；不适合：单文件小修。

## 5. Superpowers / superpowes
定位：工程纪律型 skills framework，核心价值不在“写多少 artifact”，而在强制触发正确的工程习惯。repo 结构里最关键的是 agents/、commands/、hooks/、skills/；工作流技能包括 brainstorming、using-git-worktrees、writing-plans、subagent-driven-development、test-driven-development、requesting-code-review 等。安装上现在有两条路：官方 Claude marketplace 可直接 /plugin install superpowers@claude-plugins-official，社区 marketplace 则是先 /plugin marketplace add obra/superpowers-marketplace 再 /plugin install superpowers@superpowers-marketplace。命令也有两套说法：仓库里展示了 namespaced 版 /superpowers:brainstorm|write-plan|execute-plan，marketplace 页又写成 /brainstorm|/write-plan|/execute-plan，所以最佳实践也是装完先看 /help，别死背 README。优点是：TDD、worktree、并行 subagent、code review 都很强，适合把 agent 拉回工程正轨；缺点是：它非常 opinionated，尤其是 TDD-first 和 mandatory workflow，不喜欢这套的人会觉得“被管太多”。适合：你重视测试、工艺、可维护性，而不是只求快出代码。

## 6. BMAD Method / bmad-method
定位：最重、最组织化、最“角色化”的一套。它不是一个小插件，而是一个模块化框架：安装后会生成 bmad/core、bmad/bmm、bmad/bmb、bmad/cis、bmad/_cfg/agents，其中 _cfg 专门用来放可升级保留的定制。安装命令是 npx bmad-method@alpha install（v6 alpha）或 npx bmad-method install（v4 stable），入门建议是先跑 *workflow-init；你也可以直接用 /bmad:bmm:workflows:workflow-init、/bmad:bmm:workflows:prd、/bmad:bmm:workflows:dev-story 这类命令。优点是：scale-adaptive、角色分工清晰、适合复杂产品与组织级流程；缺点也很明显：学习曲线最高、ceremony 最高，且 v6 文档仍在收敛。如果你是 solo builder，只想把功能做出来，BMAD 往往太重。适合：复杂产品、多人协作、需要 PM/架构/UX/开发多角色工作流的场景。

## 7. workflows / Compound Engineering Plugin
定位：repo-aware 的 plan → work → review → compound 闭环。关键 repo 路径能看到 .claude/commands、.claude-plugin、docs/，并且它还有一个 Bun/TypeScript CLI 可以把 Claude Code 插件转换到 OpenCode、Codex、Droid、Gemini 等。安装是 /plugin marketplace add EveryInc/compound-engineering-plugin + /plugin install compound-engineering，或用 bunx @every-env/compound-plugin install compound-engineering --to opencode|codex|droid|pi|gemini 做跨工具转换。这里有个你一定要知道的坑：公开文档存在命令名漂移。仓库搜索摘要写的是 /workflows:plan|work|review|compound，而 Every Marketplace 页面又写的是 /compound-engineering:plan|work|review|triage|resolve_todo_parallel|generate_command。我的判断是版本/包装层重命名过，所以安装后先信任你本地 /help 里真正注册出来的命令。优点是：worktree、plan file、multi-agent review、知识沉淀闭环很完整；缺点是：命令和包装层还在变化，更偏“工程执行与评审系统”，不是需求发现工具。适合：已有仓库、PR 驱动、评审质量和知识沉淀比“灵感式开发”更重要的团队。

## 8. Everything Claude Code / ECC
定位：这是“大而全 harness”，不是单一 workflow。它同时覆盖插件、hooks、rules、skills、agents、commands、contexts、MCP configs，而且已经扩展到 Claude Code、Codex、Cursor、OpenCode 等。核心 repo 路径非常多：.claude-plugin/、.claude/、.codex/、.cursor/、commands/、contexts/、hooks/、mcp-configs/、rules/、skills/、tests/。安装先走 /plugin marketplace add affaan-m/everything-claude-code 和 /plugin install everything-claude-code@everything-claude-code，但规则文件不能随插件自动分发，README 明确要求你再 git clone 仓库并执行 ./install.sh typescript|python|golang|swift|php 之类的脚本。命令层则有 /everything-claude-code:plan，官网还重点推荐 /tdd、/plan、/code-review、/e2e、/security-review、/build-fix、/continuous-learning-v2，另有 ecc-universal 和 AgentShield。优点是：覆盖面最大、跨 harness 一致性最好、hooks/security/research/continuous learning 都齐；缺点是：复杂度也最大，你不是在装一个 workflow，而是在装一整套 agent harness。适合：你想把 Claude Code 体系彻底武装起来，而不是只引入一个 planning 方法。

## 9. Ralph
定位：它不是 spec 工具，而是autonomous execution loop。现在的 README 已经不只写 Amp，也支持 Claude Code：你可以手动复制 ralph.sh 和对应的 prompt.md/CLAUDE.md，也可以在 Claude Code 里 /plugin marketplace add snarktank/ralph，再 /plugin install ralph-skills@ralph-marketplace，然后获得 /prd 和 /ralph 两个技能。核心运行文件是 ralph.sh、prd.json、progress.txt、AGENTS.md、tasks/prd-*.md；真正执行时是 ./scripts/ralph/ralph.sh [max_iterations]。它的核心思想非常硬核：每轮 fresh context，记忆只靠 git history、progress.txt、prd.json。优点是：极强的长任务推进能力，特别适合拆成小 user stories 后循环干活；缺点是：任务粒度如果太大就会崩，而且它强依赖反馈回路——typecheck、tests、browser verification、AGENTS.md learnings，全都不能省。适合：你已经有 PRD/任务清单，想让 agent 连续跑很多轮直到清零。

如果你问“到底哪个更好”，我的直接建议是这样：
对你这种明显在意结构、测试、长期可维护性的工程师，默认首推 OpenSpec + Superpowers。原因很简单：OpenSpec 负责把变更语义和审计轨迹落到磁盘，Superpowers 负责把实现过程拉回 TDD、worktree、review 的工程轨道；这套组合比 “一个大而全框架包打天下” 更稳，也更符合 production codebase 的低耦合/高内聚诉求。

如果你是个人项目 / side project / 快速试错，我反而更推荐 GSD 单飞。它把研究、分 phase、计划、执行、验证都串好了，吞吐量很高，比 BMAD 和 Spec Kit 少很多 ceremony。

如果你已经有明确 backlog，想让 agent 持续打工，那就上 Ralph；但别把 Ralph 当需求管理工具，它更像执行引擎。前面最好先有 OpenSpec / Spec Kit / PRD 之一，不然就是把模糊需求放进自动循环里放大错误。

如果你想把 Claude Code 彻底武装成一个大型 agent harness，再考虑 ECC；如果你更关心 PR、评审和知识沉淀闭环，再考虑 Compound Engineering；如果你要的是组织级多角色流程，再考虑 BMAD。这三者都不是“先装了再说”的轻量选项。

最后给你几个我认为真正有用的最佳实践。
第一，不要同时把 GSD、BMAD、Spec Kit、OpenSpec 全都当主方法论来跑。它们在 spec/plan/execute 上重叠很大，叠太多只会让 agent 命令空间冲突、artifact 重复、上下文规则互相打架。最稳的组合通常是：1 个规格层（OpenSpec / Spec Kit / GSD / BMAD 四选一）+ 1 个执行纪律层（Superpowers / ECC / Compound 三选一）+ 可选 1 个循环层（Ralph）或记忆层（planning-with-files）。这个不是 README 原话，是我基于它们公开结构做的工程判断。

第二，安装后永远先看本地 /help / /plugin list / 实际生成的命令目录。Spec Kit、Superpowers、Compound 这几套公开文档都能看到命令命名漂移或多套入口；死背 README 很容易踩坑。

第三，任何 autonomous 流程都必须配 feedback loops。Ralph 明说要 typecheck/tests/browser verification；GSD 专门有 verify-work；Compound 也是把 review 作为核心闭环。没有这些，所谓“自动化”只是更快地产生错误。

第四，对权限要保守。GSD README 推荐 --dangerously-skip-permissions 是为了 frictionless automation，但这更适合你完全信任的本地仓库；只要有公司代码、脚本副作用、或联网/凭证风险，我建议用 allowlist。这个结论里，“推荐 skip-permissions”是官方写法；“生产仓库里别这么干”是我的明确意见。

如果你只让我给一个最终落地版建议：
严肃产品开发：OpenSpec + Superpowers。
个人高吞吐量：GSD。
	1.	你的主战场到底是 Claude Code 单一环境，还是 Claude/Codex/Cursor/OpenCode 混用？
	2.	你更看重的是 规格可审计，还是 自动执行吞吐量最大化？

可以，这三项加进来之后，前面的结论要做一次重新分层：

结论先说：
oh-my-claudecode 和 oh-my-opencode 本质上都不是“规格方法”，而是agent harness / orchestration layer；LeanSpec 才是轻量规格层。所以它们不是在同一个赛道上互相替代，而是分别补到你前面那张图里的执行层和规格层。对大多数人来说，最稳的组合不再是“只选一个神器”，而是：一个规格层（LeanSpec / OpenSpec / Spec Kit / GSD 里选一个主的）+ 一个执行层（OMC / OMOC / 其他 harness）+ 可选一个循环层（Ralph）。

1) oh-my-claudecode：Claude Code 里的“一体化自动驾驶执行层”

它的官方定位很明确：面向 Claude Code 的多代理 orchestration，主打 autopilot、ultrapilot、swarm、pipeline、ralph 等执行模式；文档页还给了 omc setup/config/info/update/doctor/install 这一套管理命令，并写明会把 OMC 安装到 ~/.claude/，同步 hooks、agents、skills。换句话说，它解决的是怎么更猛地执行，不是“怎么定义规范”。

你真正该记的核心路径和命令是这组：

# 安装
/plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode
/plugin install oh-my-claudecode

# 初始化
/oh-my-claudecode:omc-setup

# 管理/诊断
omc info
omc config --validate
omc doctor
omc update
omc install

# 执行模式
autopilot: build a todo app
ultrapilot: build a fullstack app
/swarm 5:executor "fix all errors"
ralph: refactor auth system

这些入口来自它的官方主页与文档页；要注意的是，官方主页、文档站和版本页之间存在命名与数量漂移，比如代理/技能数量有 28/30/32 和 37/40+ 的不同写法，初始化命令也同时出现了 /oh-my-claudecode:omc-setup 与 /omc-setup 两种风格。所以安装后不要死背网页，以本地 /help、omc info、实际注册出的命令为准。

优点：
它最大的价值是把 Claude Code 从“会写代码的 agent”拉成“能编队施工的执行系统”。它内建多种执行模式，支持并行 worker、通知、验证、Ralph 式 persistence，还带有跨模型协同叙事（Claude/Gemini/Codex）。如果你不想手工拼 commands、agents、hooks、MCP，这种一体化体验很有吸引力。

缺点：
第一，它非常 opinionated。第二，它的文档/版本页有漂移，说明发布节奏快、接口心智负担不低。第三，它更擅长“执行推进”，不擅长“让需求和变更本身可审计”。所以如果你拿它单独当完整方法论，后面很容易回到“代码跑得很快，但意图沉淀不稳”。

什么时候优先选它：
当你的主战场就是 Claude Code，而且你要的是最少学习成本的多 agent 执行力，它应该直接进第一梯队。尤其是个人项目、快速迭代、需要并行拆活时，它比“自己拼一堆插件和命令”省事得多。

⸻

2) oh-my-opencode：OpenCode 里的“高可定制执行层 + Claude 兼容桥”

oh-my-opencode 的官方描述也很直接：它是构建在 OpenCode 之上的 batteries-included orchestration layer，强调 modular workflows、specialized agents、hooks、MCP、LSP，以及对复杂 build pipeline / multi-repo 结构的理解。更关键的是，它自带 Claude Code compatibility layer，会读取 .claude 的 commands / skills / agents / hooks / MCP 配置。

这套东西真正要记的是这些路径和命令：

# 安装
bunx oh-my-opencode install
# 或
npx oh-my-opencode install

# 运行基础 runtime
opencode

# 常见触发词 / 用法
ultrawork
Ask @oracle to review this design
Ask @librarian how this is implemented
Ask @explore for the policy on this feature

以及这些核心路径：

配置:
~/.config/opencode/oh-my-opencode.json
./.opencode/oh-my-opencode.json

Claude 兼容层会读取:
~/.claude/commands/
./.claude/commands/
~/.claude/skills/
./.claude/skills/
~/.claude/agents/
./.claude/agents/
~/.claude/settings.json
./.claude/settings.json
./.claude/settings.local.json

OpenCode 自己的命令目录:
~/.config/opencode/command/
./.opencode/command/

会话数据:
~/.claude/todos/
~/.claude/transcripts/

这些都直接写在其 README/官网摘要里；它还明确提醒：除非用户明确要求，不要乱改模型设置，也不要默认关掉 agents/hooks/MCPs。这说明它的设计哲学不是“先最小化功能”，而是“先把完整 harness 装起来再裁剪”。

优点：
如果你愿意进入 OpenCode 生态，它比很多 Claude Code 向工具更开放、更 hackable，也更适合多 provider、多模型编排，还保留了对 .claude 资产的兼容桥。这一点很实用：你不必从零抛弃已有 Claude Code 配置。

缺点：
它的复杂度是真复杂度。官方自己就承认 OpenCode 本身可扩展但学习成本高，所以 oh-my-opencode 才试图把这件事“包装好”。这意味着：如果你并不打算切到 OpenCode，或者你根本不需要多 provider / LSP / pipeline-aware runtime，那它就是过度工程。

什么时候优先选它：
当你满足下面任意两条时，我会优先考虑它：
	1.	你准备把主 runtime 迁到 OpenCode；
	2.	你要多模型编排而不是只围着 Claude Code 转；
	3.	你有复杂 repo / build pipeline / monorepo；
	4.	你想复用 .claude 资产，但不想受限于 Claude Code 本身。
这些判断是我基于它的官方定位和兼容层设计推出来的。

⸻

3) LeanSpec：比 OpenSpec / Spec Kit 更轻的规格层

LeanSpec 的定位非常清楚：lightweight, flexible SDD。它反对 heavy spec-first waterfall，强调“write specs as you code”“specs fit in working memory”“begin with just README.md and status tracking”“add structure only when needed”。仓库 README 里又补上了 CLI / MCP / board / stats / ui / search 这些工具能力。它显然不是像 OMC/OMOC 那样的执行编排器，而是一套让规格保持短、小、活、可被 AI 直接吃掉的轻量规格方法。

核心路径和命令记这组就够了：

# 初始化
npx lean-spec init --example dark-theme
# 或
npm install -g lean-spec && lean-spec init

# 查看/运维
lean-spec board
lean-spec stats
lean-spec ui
lean-spec search

{
  "mcpServers": {
    "lean-spec": { "command": "npx", "args": ["@leanspec/mcp"] }
  }
}

以及你真正关心的目录心智：

起步心智:
README.md
status tracking

常见目录/文件:
.lean-spec/
specs/
AGENTS.md

官方文档强调先从 README.md + status tracking 起步，再按需增加结构；仓库自身也能看到 .lean-spec/、specs/、AGENTS.md。它的 CLI 侧重可视化与搜索，不是那种要求你必须跑完“requirements -> design -> tasks -> implement”整套 ceremony 的重型方法。

优点：
它最强的点是上下文经济性。官方说法是 specs 目标保持在人和 AI 都能消化的规模，文档里写到 “under 300 lines / 5–10 分钟可读”，仓库 README 则把目标描述成“小于 2,000 tokens”。这类尺度对于 agent 特别重要，因为它直接降低 context rot。

缺点：
它轻，所以它不会天然给你 OpenSpec 那种变更提案 / delta / archive 的审计感，也不会给你 Spec Kit 那种constitution → specification → plan → tasks → implement 的全流程治理。换句话说，LeanSpec 不是不要纪律，而是把纪律压到最低足够集。你的团队如果需要强 review 轨迹、合规、审批，LeanSpec 单独不够。

什么时候优先选它：
当你觉得 OpenSpec 太“变更管理导向”，Spec Kit 又太“重流程”，但你又不接受纯 vibe coding，那 LeanSpec 很可能正好卡在甜点位：有规格，但不官僚；有方法，但不厚重。

⸻

4) 放回前面的总图：这三项该怎么插进去

如果按我现在重构后的地图来看：
	•	规格层：LeanSpec、OpenSpec、Spec Kit、GSD、BMAD
	•	执行层：oh-my-claudecode、oh-my-opencode、ECC、Compound、Superpowers
	•	循环层 / 长任务推进层：Ralph
	•	轻记忆层：planning-with-files

这是我基于各项目公开说明做的工程分层，不是官方分类；但这个分法比把它们全当“workflow 框架”更接近实际。

新的选型规则我会改成这样：

A. 你还在 Claude Code，且要少学命令、直接猛干
先上 oh-my-claudecode。它是新增项里最值得直接上手的。

B. 你准备转 OpenCode，且看重多 provider / 更强可定制性
先上 oh-my-opencode。但这是 runtime 迁移，不是小修小补。

C. 你缺的是规格纪律，不是执行火力
先上 LeanSpec。它补的是 intent clarity，不是 orchestration horsepower。

D. 你要的是审计、proposal、delta、archive
还是 OpenSpec 更对路；LeanSpec 不替代这个能力。

E. 你要完整、重治理、constitution 驱动的 SDD
还是 Spec Kit 更正统。LeanSpec 更轻，不是更全。

F. 你已经有清晰 PRD，想让 agent 一轮一轮直到清空任务
还是 Ralph 最纯粹；不过 OMC 也把 Ralph 风格 persistence 吸进了执行模式里。

⸻

5) 我给你的实际推荐组合

结合你前面问的那一大串工具，我现在会这样推荐：

方案一：你主战场是 Claude Code，追求产出与结构平衡

LeanSpec + oh-my-claudecode
LeanSpec 负责把需求压成短小、活的 spec；OMC 负责多 agent 执行、并行、验证、持续推进。这套比“只装 OMC 然后把规格全留在聊天里”稳定得多。

方案二：你是 brownfield 项目、多人 review、要变更审计

OpenSpec + oh-my-claudecode
OpenSpec 管 specs/ 与 changes/ 的变更语义，OMC 只负责施工。这个组合比 LeanSpec 更适合老系统持续演进。

方案三：你要切 OpenCode，当成长期主平台

LeanSpec 或 OpenSpec + oh-my-opencode
规格层照样独立，OMOC 做 runtime/harness。这样分层最干净。

方案四：你已经有明确定义好的 PRD/backlog，要持续自动推进

OpenSpec / LeanSpec + Ralph
先把任务边界做清楚，再上 Ralph 循环。不要拿模糊需求直接喂 Ralph。

⸻

6) 最佳实践：真正会踩坑的地方

第一，不要把 OMC 和 OMOC 当成两个同级主 harness 一起长期挂在同一套 .claude 心智上。
原因很直接：OMC 安装/同步目标是 ~/.claude/，而 OMOC 又会主动读取 .claude 里的 commands / skills / agents / hooks，并加上它自己的 .opencode 体系。两者都想接管同一类资产时，命令空间、hook 行为和期望运行时都可能打架。选一个主执行层。 这是我基于它们的路径设计做的工程判断。

第二，不要把 LeanSpec 和 OpenSpec 同时当主规格源。
LeanSpec 的哲学是 living spec、按需加结构；OpenSpec 的哲学是 current truth + proposed changes 的双目录变更管理。两者都做“主规格”，最后通常不是互补，而是双写。更合理的做法是：选一个当 source of truth。

第三，OMC/OMOC 的并行模式只在任务天然可分解时才有收益。
ultrapilot、swarm、ultrawork 这类模式适合多组件、多文件、多子任务的工作；如果任务本身高度串行、共享上下文重、设计还没定，强行并行只会提高冲突和返工。这个结论是从它们的执行模式设计直接推出的。

第四，LeanSpec 的价值不是“生成 spec”，而是“让 spec 一直短且更新得起”。
官方反复强调 start simple、context economy、write specs as you code。你要是把它写成 1,500 行 PRD，它就不再是 LeanSpec 了。

第五，任何带 persistence / autonomous loop 的东西，都必须绑反馈回路。
Ralph 明确要求 typecheck、tests、browser verification、AGENTS.md learnings；OMC 也强调 verified complete、architect verification。没有反馈回路，所谓“自动化”只是自动制造脏代码。

⸻

最后的直接判断

把这三个补进来以后，我的排序会变成：

Claude Code 用户：
先看 oh-my-claudecode；如果你还缺规格层，再补 LeanSpec 或 OpenSpec。

OpenCode 用户：
先看 oh-my-opencode；规格层照样独立选。

嫌 OpenSpec / Spec Kit 太重，但又不想乱写：
先看 LeanSpec。

要最稳，不要神化单一框架：
一个主规格层 + 一个主执行层 + 可选 Ralph，不要把所有框架都装成“主脑”。

