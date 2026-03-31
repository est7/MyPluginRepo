


我现在 mcp 就 context7,exa,google-developer-knowledge,auggie,前三个是不是可以整合成一个 skill 调用 cli 实现啊

可以，而且更合理的做法不是“硬合并成一个 MCP server”，而是做成一个统一入口的 orchestration skill：
Skill 负责意图识别、路由规则、输出格式；CLI 负责执行；底层仍分别调用 Context7、Exa、Google Developer Knowledge。 这更符合这三类源的职责边界。Skills 本身就是给 ChatGPT 复用工作流用的，可以打包指令、示例，甚至代码；创建后也能在合适的时候自动被用到。你也可以在 ChatGPT 的 Skills 页面看到它们，或直接在对话里让 ChatGPT 帮你创建。 ￼

我会直接给结论：
	1.	能整合成一个 skill。
	2.	建议整合的是“调用入口”和“路由策略”，不是把三个服务实现层揉成一个。
	3.	如果你现在已经能在宿主里同时挂多个 MCP，那 skill 未必需要替你“接管调用”，更应该负责“什么时候用谁”。

为什么我建议“统一编排”，不建议“物理合并”

这三个东西天然不是一个层次：
	•	Context7 更偏库/框架文档 grounding，而且它本身就有 CLI，CLI 既能查文档，也能管理 skills，还能配置 Context7 MCP。 ￼
	•	Exa MCP 更偏网页搜索 / code search / 外部信息检索，而且 Exa 提供的是独立 MCP 入口，甚至可以按 URL 参数启用特定工具。 ￼
	•	Google Developer Knowledge 是 Google 官方开发文档的 canonical source，Google 在 2026-02-04 公布了 Developer Knowledge API 和对应 MCP server，目标就是给 AI 助手提供最新的 Google 开发文档。 ￼

所以从第一性原理看，你在做的是检索编排器，不是“单一数据源适配器”。

我推荐的落地形态

做一个 skill，比如 dev-research-router，里面放三类东西：

dev-research-router/
├── SKILL.md
├── scripts/
│   ├── router.py          # 统一入口，做 query classification + source routing
│   ├── context7.sh        # 调 context7 cli / mcp
│   ├── exa.sh             # 调 exa mcp/http
│   └── gdk.sh             # 调 google developer knowledge api/mcp
└── references/
    └── routing-rules.md   # 路由策略、去重策略、失败回退策略

核心路由规则建议这样定：
	•	问库/框架/API 用法，且需要版本敏感 → Context7
	•	问 Google 生态（Android / Firebase / GCP / Chrome / TensorFlow / Gemini 等） → Google Developer Knowledge
	•	问通用外网资料、博客、仓库、对比、最新资料 → Exa
	•	复杂问题 → 先 Google/Context7 拿官方文档，再 Exa 补外围资料和交叉验证

这套路由是低耦合的，因为“策略”和“执行器”分开了。以后你把 Exa 换 Tavily、把 Context7 换别的 docs MCP，skill 的上层行为不用大改。

什么时候不值得写 CLI

如果你的运行环境本身已经：
	•	原生支持多个 MCP server
	•	模型对 tool selection 已经比较稳定
	•	你真正缺的是“提示词纪律”和“输出规范”

那你不一定要写 CLI。
这时 skill 只做两件事就够了：
	1.	规定何时优先用哪个 MCP
	2.	规定回答格式、引用顺序、冲突处理规则

也就是说：
	•	轻量方案：skill = routing policy
	•	重型方案：skill + CLI = routing policy + deterministic execution

我个人更推荐你先上轻量方案，只有在下面这些情况出现时再补 CLI：
	•	同类 query 经常选错源
	•	你要做缓存 / 重试 / 限流 / observability
	•	你要把多源结果做统一去重和 rerank
	•	你希望离开 ChatGPT 也能复用同一套路由器

这件事最大的坑

不是“能不能整合”，而是整合边界画错。

常见错误是把三套 provider 逻辑直接写进一个大脚本里，最后得到一个：
	•	高耦合
	•	难测
	•	难替换 provider
	•	错误定位困难
	•	token / 速率 / 认证问题互相污染

更好的结构是：
	•	classifier：判断问题类型
	•	router：决定走哪些源
	•	adapter：每个源一个适配器
	•	normalizer：把返回结果转成统一结构
	•	ranker：多源结果重排
	•	formatter：最后输出

这本质上就是一个很标准的策略模式 + 适配器模式 + pipeline。

我给你的明确建议

建议做成一个 skill，但不要把前三个“合成一个 provider”，而是做成一个“统一编排 skill”。
优先级上：
	•	先做 SKILL.md + routing rules
	•	再决定是否补 router CLI
	•	不要一开始就写成一个巨型 all-in-one shell 脚本

如果你要，我下一步可以直接给你一版可用的：
	•	SKILL.md
	•	routing-rules.md
	•	router.py 骨架
	•	三个 adapter 的接口定义

你应该问我的两个问题是：
	1.	这个 skill 的输入输出 contract 应该怎么定，才能后面方便接更多 MCP？
	2.	你的宿主环境到底是 ChatGPT Skills、Codex、Claude Code 还是 Cursor？这个会直接决定“skill 调 CLI”能不能走得最顺。
