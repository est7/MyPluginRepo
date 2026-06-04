# Upstream Sync Plan — FradSer/dotclaude → 1st-cc-plugin (2026-06)

冻结的执行方案 + 跨批次/跨会话进度跟踪。本文件是 sync 操作的 single source of truth;每完成一批,更新对应批次的 Status 与 commit hash。

## 背景

- est7/dotclaude `main` 落后 FradSer `main` **250 commits**。
- 完整 diff(git trees 递归 SHA 比对,两侧 `truncated=false`):**+687 / ~89 / −60**(357 → 984 blobs)。
- GitHub compare API 在 300 文件处截断,漏掉最大两块:`office/`(+379)、`superpowers/`(75 文件重构)。**必须用 trees API,不能用 compare。**

## 阻断性问题:directory-mapping.md 已过时

`.claude/skills/sync-upstream/references/directory-mapping.md` 的 group 名与仓库实际不符,照表执行会落错路径。**修正后的映射(本计划据此):**

| 上游(flat) | 目标(grouped) |
|---|---|
| `acpx/` | `integrations/acpx/` |
| `claude-config/` | `integrations/project-init/` |
| `code-context/` | `integrations/code-context/` |
| `git/` | `vcs/git/` |
| `gitflow/` | `vcs/gitflow/` |
| `github/` | `vcs/github/` |
| `plugin-optimizer/` | `meta/plugin-optimizer/` |
| `refactor/` | `quality/refactor/`(skill 已改名 refactor-file/refactor-module) |
| `superpowers/` | `workflows/superpower/`(已 diverge,skills 为空) |
| `swiftui/` | `platforms/swiftui/` |
| `utils/` | `integrations/utils/` |
| `office/` | `integrations/doc-gen/` |
| `frontend/`(新) | 新建插件 |

validate 脚本实际路径:`meta/plugin-optimizer/scripts/validate-plugin.py`(**非** mapping 表写的 authoring)。

## 已冻结的决策

- **frontend**:作为新插件引入(~183 文件)。
- **shadcn / next-devtools**:由 frontend 内含 skill 完全接管,删除独立的 `platforms/shadcn`、`platforms/next-devtools`。
- **office/lark**:本轮**跳过**(+364 vendored 巨型),doc-gen 只 port agent-browser/create-prd/tropes。
- **office/create-feishu-doc**:删除(与上游对齐)。
- **git**:采纳上游重构,同步父/子 CLAUDE.md。
- **"上游删除→我们跟删"** 口径:仅指"FradSer 曾有、双方都有、后被 FradSer 删除"的项 = shadcn / next-devtools(meeseeks-vetted 已删)。**不删** est7 自有的 27 个插件(android/testing/clarify/loaf 等)。

## 共性适配规则(每批套用)

- `author` → `{"name":"est7","email":"t4here@gmail.com"}`;`version` 保留目标现值,不照搬上游。
- 安装命令 `@frad-dotclaude` → `@1st-cc-plugin`;URL `FradSer/dotclaude/...` → `est7/1st-cc-plugin/<group>/...`。
- 校验:`python3 1st-cc-plugin/meta/plugin-optimizer/scripts/validate-plugin.py <plugin-path>`(0=过,1=MUST违规,2=token超限)。
- 永不动 est7-only 插件;gitflow/github 等需逐 skill 核对本地是否 diverge,不盲目覆盖。
- 每批 = 一个独立 commit / 可 review 单元;删除项同步清理 marketplace.json / CLAUDE.md / README 引用。

## 批次清单与进度

| 批次 | 内容 | 文件量 | 风险 | Status | Commit |
|---|---|---|---|---|---|
| 1 | acpx / project-init / gitflow / github / swiftui / utils→doc-tools | ~40 | 低 | DONE(未提交):acpx 0.1.2 / gitflow 1.0.2 / github 0.2.2(+5 refs) / swiftui 0.2.1 / project-init 1.4.1(全盘,保留 name)/ **utils→doc-tools 0.1.0**(+update-changelog,保留 dialogue-rewriter);**code-context 跳过**(est7 改过且上游零增益) | 未提交(攒批次) |
| 2 | git 重构 + 同步 CLAUDE.md/marketplace + code-context bug 修复 | ~15 | 中 | DONE(未提交):git 0.5.0(config-git/update-gitignore→references 保留,删 hooks/scripts/examples,+cli.md+setup);CLAUDE.md hook 引用同步;code-context frontmatter bug 修复(跳过上游) | 未提交(攒批次) |
| 3 | plugin-optimizer 全盘 0.12.0 + graft 回 check_descriptions | ~35 | 中 | DONE(未提交):全盘上游(+5 新组件 monitors/themes/output-styles,777 行校验器重构),**check_descriptions graft 回新校验器**(est7 独有 CSO 门槛保留);9 插件全用新校验器复跑 PASSED | 未提交(攒批次) |
| 4 | frontend 引入 + 删 platforms/shadcn、next-devtools + 清引用 | +183 −16 | 高 | DONE(未提交):frontend 0.3.1(platforms/frontend,183 文件,sparse-clone 拷入)校验 PASSED;删 shadcn+next-devtools;marketplace×2/CLAUDE.md(子+父)/README×2 同步;插件数 38→37 | 未提交(攒批次) |
| 5 | office→doc-tools:agent-browser/create-prd/patent-architect 升级 + 新增 tropes,**不含 lark**;feishu 已删 | ~25 | 高 | DONE(未提交):doc-tools 0.3.0(7 skills);agent-browser/create-prd/patent-architect 全盘升级 + tropes 新增(9 文件);scripts 更新(跳过 sync-lark);agent-browser 路径修复保留 | 未提交(攒批次) |
| 6 | superpowers 全新引入(目标从未存在,非重写) | +50 | 高 | DONE(未提交):workflows/superpowers 3.1.1(name 保复数避免 40 处交叉引用断裂)校验 PASSED;marketplace/CLAUDE.md(子+父)/README×2 同步;插件数 37→38 | 未提交(攒批次) |

## 结构变更记录(批次 1 衍生)

- **utils → doc-tools**(0.2.0):重命名 + 吸收上游 update-changelog + **并入原 doc-gen 的 3 个 skill**(agent-browser / create-prd / patent-architect)及 scripts;保留 est7 自有 dialogue-rewriter / update-readme。
- **doc-gen 插件解散删除**:create-feishu-doc 删除;其余 skill 迁入 doc-tools;清理 marketplace×2 / CLAUDE.md(分组+scope)/ README×2。
- **插件总数 39 → 38**(doc-gen 解散)。
- 修正历史 bug:agent-browser 的 SYNC.md + sync 脚本里 stale 的 `office/scripts/` 路径(原 office→doc-gen 移植时漏改)→ 现指向 `integrations/doc-tools/`。

## 待定 / 残余风险

- batch 4 frontend 自带 `SYNC.md` + `scripts/sync-*.sh`(二级 vendored 内容),维护成本高,引入后需决定是否保留同步脚本。
- batch 6 superpower:目标 skills 为空且已 diverge,需单独立项判断"重写 vs 放弃"。
- office/lark 巨型 vendored 库,后续单独评估是否引入。
- directory-mapping.md 需修订(Boy Scout flag,见下)。

## 附带修复(批次 6 收尾)

- **modern-android 补全**(est7 自有半成品,非 sync):原缺 `.claude-plugin/plugin.json`、8 个 skill 平铺在插件根而非 `skills/`、混入 .DS_Store。已补 plugin.json(0.0.2,8 skill 注册为内部 skill)、skill 移入 `skills/`、删 .DS_Store、marketplace 描述同步。校验 PASSED。**磁盘 plugin.json 数现 = marketplace = 38,off-by-one 消除。**

## Boy Scout(本任务发现、未在范围)

- `.claude/skills/sync-upstream/references/directory-mapping.md` — group 名(version-control/authoring)与仓库实际(vcs/meta/integrations)全面不符,validate 路径也错 — 建议单独修订。
