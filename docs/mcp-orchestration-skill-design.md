# dev-research-router：MCP 统一编排 Skill 设计

Context7、Exa、Google Developer Knowledge 这三个 MCP 服务可以整合成一个统一入口的 orchestration skill，但整合的对象是"调用入口和路由策略"，而不是把三个服务的实现层物理合并成一个新的 MCP server。底层仍分别调用各自的服务，skill 负责意图识别、路由规则和输出格式，CLI 在需要时负责执行。

## 为什么是编排器，不是适配器

这三个服务天然处于不同的层次。Context7 偏向库和框架文档的 grounding，本身提供 CLI，既能查文档、管理 skills，也能配置 Context7 MCP。Exa 偏向网页搜索、code search 和外部信息检索，提供独立 MCP 入口，还可通过 URL 参数启用特定工具。Google Developer Knowledge 是 Google 官方开发文档的 canonical source，于 2026-02-04 公布了 Developer Knowledge API 和对应 MCP server，目标就是给 AI 助手提供最新的 Google 开发文档。

从第一性原理看，这件事的本质是检索编排，不是单一数据源适配。把它们揉成一个 provider 实现，只会引入高耦合、难以替换 provider、错误定位困难以及 token / 速率 / 认证问题互相污染等代价。

## 落地形态

推荐的 skill 命名为 `dev-research-router`，目录结构如下：

```
dev-research-router/
├── SKILL.md
├── scripts/
│   ├── router.py          # 统一入口，做 query classification + source routing
│   ├── context7.sh        # 调 context7 cli / mcp
│   ├── exa.sh             # 调 exa mcp/http
│   └── gdk.sh             # 调 google developer knowledge api/mcp
└── references/
    └── routing-rules.md   # 路由策略、去重策略、失败回退策略
```

核心路由规则按问题类型划分：问库 / 框架 / API 用法且需要版本敏感的，走 Context7；问 Google 生态（Android / Firebase / GCP / Chrome / TensorFlow / Gemini 等）的，走 Google Developer Knowledge；问通用外网资料、博客、仓库、对比、最新资料的，走 Exa；复杂问题则先用 Google Developer Knowledge 或 Context7 取官方文档，再用 Exa 补外围资料和交叉验证。

这套路由是低耦合的，因为策略和执行器分开了。以后把 Exa 换成 Tavily、把 Context7 换成其他 docs MCP，skill 的上层行为不需要大改。

## 轻量方案与重型方案

运行环境本身已经原生支持多个 MCP server、模型对 tool selection 已经比较稳定的情况下，skill 未必需要接管调用，更应该负责"什么时候用谁"。此时 skill 只做两件事：规定何时优先用哪个 MCP，以及规定回答格式、引用顺序和冲突处理规则。这是轻量方案，skill 即 routing policy。

重型方案在轻量方案基础上补 CLI，形成 routing policy + deterministic execution 的组合。只有在以下情况出现时才值得补 CLI：同类 query 经常选错源；需要做缓存 / 重试 / 限流 / observability；需要对多源结果做统一去重和 rerank；或者希望离开 Claude Code 也能复用同一套路由器。建议先上轻量方案，在实际使用中观察是否触发这些条件。

## 正确的内部结构

无论最终选择哪种方案，一旦引入 router 脚本，内部都应该遵循标准的策略模式 + 适配器模式 + pipeline：

- **classifier**：判断问题类型
- **router**：决定走哪些源
- **adapter**：每个源一个适配器，互相隔离
- **normalizer**：把返回结果转成统一结构
- **ranker**：多源结果重排
- **formatter**：最终输出

常见的错误是把三套 provider 逻辑直接写进一个大脚本，最终得到一个高耦合、难测试、难替换、错误定位困难的实现。正确的边界是：整合编排逻辑，不整合 provider 实现。

## 实施顺序

先写 `SKILL.md` 和 `references/routing-rules.md`，明确路由策略和输出规范。再根据实际使用中暴露的问题决定是否补 `router.py` 和各 adapter shell 脚本。不要一开始就写成一个巨型 all-in-one shell 脚本。
