  <context>
  目标工作流路径：
  - `/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf`

  重点参考目录：
  - 设计与版本文档：`/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf/docs`
  - 成熟框架源码：`/Users/est9/MyPluginRepo/vendor`
  - 研究报告：`/Users/est9/MyPluginRepo/docs/research`

  当前已确认事实：
  - `loaf` 当前 shipped baseline 是 `v1.5.0-rc.1`
  - `v1.5` 是 current active package
  - 文档优先级必须参考 `docs/` 内文件修改时间，越近越优先
  - `docs/README.md` 的阅读顺序、`docs/ROADMAP.md`、`docs/v1_5/README.md`、`docs/v1_5/design/implementation-design.md`、`docs/v1_5/implementation/acceptance-test-report.md` 是高优先级入口
  - 这是一个 protocol-driven、phase-based、machine-checkable 的 workflow，不是普通插件功能 review
  </context>

  <task>
  按以下顺序执行，不能跳步：

  第一阶段：建立事实基线
  1. 完整阅读 `loaf/docs`，按修改时间和根入口文档给出的 reading order 建立理解。
  2. 明确回答：
     - `loaf` v1.5 当前已经解决了什么问题
     - 还有哪些结构性短板没有解决
     - 哪些机制是“设计上成立但实现上不够强”
     - 哪些地方存在“文档说得比代码强”或“代码有了但治理语义没闭环”的问题
  3. 输出一个 “Current State Baseline” 小节，必须引用具体文件路径与关键实现位置。

  第二阶段：源码级全面 review
  1. 对 `/Users/est9/MyPluginRepo/1st-cc-plugin/workflows/loaf` 做全面代码 review。
  2. review 必须覆盖：
     - 宏观：phase model、profile model、state machine、artifact model、gate model、agent/skill/hook/script 职责边界
     - 中观：模块拆分是否过浅/过碎、协议层与表现层是否混杂、命令与脚本是否存在重复编排逻辑
     - 微观：命令参数、异常处理、路径处理、schema 严格性、hook 行为、测试组织、性能热点、容易出错的分支
  3. 每个发现必须给出：
     - 严重级别：`critical` / `high` / `medium` / `low`
     - 问题标题
     - 证据：具体文件与函数/脚本位置
     - 为什么重要
     - 推荐修复方向
     - 是否应进入 `1.6` / `1.7` / `1.8` / `1.9` / `2.0`
  4. 不要输出空泛建议，必须源码落点明确。

  第三阶段：成熟框架对照研究
  1. 对照 `vendor/` 中成熟 agent workflow/framework 的源码与 `docs/research/` 中对应研究报告。
  2. 不是做罗列式综述，而是针对 `loaf` 的关键问题去找“成熟解法”。
  3. 至少比较这些维度：
     - spec-first / sdd / tdd support
     - task decomposition / story slicing
     - artifact retention / traceability
     - state transition discipline
     - human gate / approval semantics
     - review / verification / evidence collection
     - extensibility / pluginability / command ergonomics
     - testability / regression protection
  4. 如果 vendor 中存在明显优于当前 `loaf` 的方案，优先采用更好的方案，而不是强行为现状辩护。
  5. 明确区分：
     - 可直接借鉴
     - 需要本土化改造后借鉴
     - 不适合 `loaf` 的方案及原因

  第四阶段：制定 `1.6` → `2.0` 演进路线图
  1. 目标是把 `2.0` 设计成一个“完整大版本”，而不是零散修补。
  2. 为 `1.6`、`1.7`、`1.8`、`1.9`、`2.0` 分别定义 3-5个 major sprint。
  3. 每个版本给出接近 `20-30` 个 story，不要求平均分布，但总量与版本定位必须合理。
  4. 每个版本必须明确：
     - 本版本主题
     - 进入条件
     - 退出条件
     - 核心 stories
     - 必须新增或修订的文档
     - 必须新增或修订的测试
     - 对上一版本的兼容/迁移要求
  5. 路线图必须体现：
     - 小任务保持敏捷
     - 大任务严格 SDD
     - TDD 作为实现路径
     - BDD 作为开发语义与验收表面
  6. `2.0` 需要被定义为“为什么它值得成为 major release”，而不是版本号凑整。

  第五阶段：把方案落到可改代码的 implementation plan
  1. 给出源码级可执行 plan，要求能直接指导后续改造。
  2. 每项改造必须说明：
     - 修改哪些文件
     - 新增哪些文件
     - 哪些脚本要重构
     - 哪些 schema / docs / tests 要同步更新
     - 伪代码或逻辑骨架
  3. TDD 优先：
     - 对每个高风险改造，先写出应先落地的 failing tests
     - 说明这些测试在证明什么行为
     - 再说明实现步骤
  4. 如果你判断当前某些文档或验收标准已经落后于更优 vendor 解法，直接提出需要修改的文档与 acceptance criteria。

  第六阶段：产出文档修订建议
  1. 指出 `loaf/docs` 中哪些文档应该修改。
  2. 指出 `acceptance-test-plan.md`、`acceptance-test-report.md`、`craft-roadmap.md`、`implementation-design.md`、`tasks/prd.md` 中哪些验收口径或设计口径需要调整。
  3. 输出建议时按“文档路径 → 应改内容 → 原因 → 受影响实现”组织。
  </task>

  <constraints>
  - 必须基于本地真实源码与真实文档，不允许闭门造车。
  - 必须优先相信最新文档，但不能迷信文档；如果代码与文档冲突，要明确指出冲突。
  - 必须给出文件路径级证据，不能只讲抽象观点。
  - 不要只给“推荐列表”，要给带版本归属的演进结构。
  - 不要把所有建议都推到 `2.0`；中间版本必须承担清晰的演进职责。
  - 不要输出泛泛的“可以优化性能/增加测试/改善模块化”。
  - 不要为了凑数编造 stories；每个 story 必须能落到具体能力、约束、测试或文档变更。
  - 如果发现 `vendor` 中有更好的成熟方案，允许推翻你最初对 `loaf` 的判断，但必须说明证据链。
  - 不要修改任何代码或文档；本次任务只做调研、review、对照、规划与修订建议。
  - 如需假设，必须明确写出 “Assumption”。
  </constraints>

  <output_format>
  输出必须严格按以下结构：

  # Executive Verdict
  - 用 8-15 条高信息密度结论总结 `loaf` 当前状态、主要短板、2.0 演进方向

  # Current State Baseline
  - 当前设计目标
  - 当前实现强项
  - 当前治理/实现/测试缺口
  - 文档与源码一致性评估

  # Source-Level Findings
  - 按严重级别排序
  - 每条 finding 必须带文件路径与具体证据

  # Vendor Comparison Matrix
  - 用表格或结构化列表对比 `loaf` 与成熟框架
  - 明确 “保留 / 借鉴 / 替换 / 不采纳”

  # Roadmap 1.6 → 2.0
  ## v1.6
  - theme
  - why now
  - 20-30 stories
  - tests first
  - docs to update
  - acceptance gates

  ## v1.7
  - 同上

  ## v1.8
  - 同上

  ## v1.9
  - 同上

  ## v2.0
  - 同上，并补充为什么这是 major release

  # TDD-First Implementation Plan
  - 按工作包拆解
  - 每个工作包先列 failing tests，再列 implementation steps

  # Documentation And Acceptance Rewrites
  - 逐文档给出修改建议
  - 逐验收标准给出收紧或替换建议

  # Appendix
  - 阅读过的关键文档清单
  - 对照过的 vendor 项目清单
  - 仍需进一步验证的问题
  </output_format>

  <quality_bar>
  你的交付物必须满足以下标准：
  - 能直接作为后续代码演进的总计划
  - 能直接指导文档修订
  - 能直接指导测试先行实施
  - 对 `loaf` 现状的理解必须体现你真的读过源码和文档
  - 对 vendor 的借鉴必须体现你真的对照过实现，而不是只看 README
  </quality_bar>
