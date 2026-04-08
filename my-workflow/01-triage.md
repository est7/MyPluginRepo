# Phase 0: TRIAGE — 复杂度评估与路由

## 目的

解决"这个任务该走多重的流程"问题。是整个工作流的入口分流器。

两条路径并存：
- **默认路径**：模糊请求 → 打分评估 → 推荐 profile → 用户确认
- **快通道**：显式命令（`/simple`, `/moderate`, `/complex`, `/harness`）→ 跳过打分 → 直入

---

## 内部步骤

```
用户输入
    │
    ├── 命中显式命令？ (/trivial, /simple, /moderate, /complex, /harness)
    │       │
    │       └─ YES → 设置 profile → 加载 durable docs → 进入 Phase 1
    │
    └── NO (模糊请求)
            │
            ▼
        [Step 0.1] 加载 durable docs (architecture, invariants, recent lessons)
            │
            ▼
        [Step 0.2] Prompt Injection Scan (G10) — 扫描外部输入
            │
            ▼
        [Step 0.3] Evidence Gathering — 用 Glob/Grep/Read 实际扫描代码库
            │   - 预计涉及的文件/模块列表
            │   - 是否需要新依赖
            │   - 是否触碰敏感区域 (auth, migration, CI)
            │
            ▼
        [Step 0.4] Complexity Scoring — 四维结构化评分
            │
            ▼
        [Step 0.5] Recommendation — 呈现 {score, evidence, recommended profile}
            │
            ▼
        [G0: Triage Gate] — 用户确认或覆盖
            │
            ▼
        设置 profile → 进入 Phase 1
```

---

## 输入产物

| 产物 | 来源 | 必需？ |
|------|------|--------|
| 用户请求文本 | 用户 | YES |
| Durable docs (architecture, invariants) | 上一任务 Phase 5 | 如果存在 |
| Recent lessons | lessons.jsonl 合成 | 如果存在 |

## 输出产物

| 产物 | 类型 | 消费者 |
|------|------|--------|
| `triage-result` | Transient (内存) | Phase 1 |
| — profile: trivial\|simple\|moderate\|complex\|harness | | |
| — score: {scope, novelty, risk, reversibility, total} | | |
| — evidence: [file list, dependency changes, sensitive areas] | | |
| — user_override: boolean | | |

---

## 打分 Rubric

### 四维评分（每维 0-3）

| 维度 | 0 | 1 | 2 | 3 |
|------|---|---|---|---|
| **Scope** | 单文件 | 同模块多文件 | 跨模块 | 跨仓库/跨服务 |
| **Novelty** | 纯修改现有 | 加新函数/组件 | 新模块/新依赖 | 新架构模式 |
| **Risk** | UI/样式/文案 | 业务逻辑 | 数据/安全/迁移 | 核心不可逆变更 |
| **Reversibility** | git revert 即可 | 需回滚+小修 | 需数据迁移/协调 | 不可逆 |

### Profile 映射（总分）

| 总分 | Profile |
|------|---------|
| 0 | trivial |
| 1-2 | simple |
| 3-5 | moderate |
| 6-9 | complex |
| 10-12 | harness |

### 关键约束

- **打分必须基于实际代码扫描**（Glob/Grep/Read），不是凭空猜测
- 打分输出**必须包含证据列表**（涉及的文件、模块、依赖变化）
- 打分不自动推进，**必须呈现给用户确认**
- 用户可以覆盖推荐（例如打分推荐 moderate 但用户说"这个我很熟，走 simple"）

---

## Gate 定义

### G0: Triage Gate

| 属性 | 值 |
|------|-----|
| 类型 | Soft (trivial/simple), Hard (complex/harness) |
| 触发 | 打分完成后 |
| 行为 | 呈现 {score, evidence, recommendation}，等用户确认或覆盖 |
| trivial/simple | 自动定级，用户可覆盖但不强制确认 |
| complex/harness | **强制人工确认**，不允许自动通过 |

### G10: Prompt Injection Scan

| 属性 | 值 |
|------|-----|
| 类型 | Hard |
| 触发 | 读取外部输入（issue, PR comment, 第三方代码）前 |
| 行为 | Boundary nonce 扫描 + 已知 injection pattern grep |
| 失败 | 标记可疑内容，警告用户 |

---

## Profile 行为矩阵

| Step | Trivial | Simple | Moderate | Complex | Harness |
|------|---------|--------|----------|---------|---------|
| Durable docs 加载 | 跳过 | 最小 | 标准 | 全量 | 全量 |
| Prompt injection scan | ✅ | ✅ | ✅ | ✅ | ✅ |
| Evidence gathering | 跳过 | 快速 | 标准 | 深度 | 深度+多源 |
| Complexity scoring | 自动极速 | 自动 | 标准 | 标准 | 标准 |
| User confirmation | 不强制 | 不强制 | 不强制 | **强制** | **强制** |

---

## 参考框架

| 机制 | 来源 | 如何使用 |
|------|------|---------|
| 四维评分 (effort/components/integration/risk) | FlowSpec `/flow:assess` | 改造为 scope/novelty/risk/reversibility |
| 三级 constitution (light/medium/heavy) | FlowSpec | 映射为 5 级 profile |
| Quick mode bypass | GSD `/gsd-quick` | 显式命令跳过打分 |
| Durable docs 注入 | Trellis JSONL-driven injection | Phase 0 加载 architecture+invariants |
| Boundary nonce | yoyo-evolve `evolve.sh:31-33` | Prompt injection 防御 |

---

## Hooks

| Hook | 事件 | 行为 |
|------|------|------|
| `triage-start` | SessionStart | 加载 durable docs + 检测显式命令 |
| `injection-scan` | PreToolUse (Read external) | 扫描外部输入内容 |
| `triage-complete` | 自定义事件 | 记录 triage result 到 event log |

---

## 失败路径

| 场景 | 处理 |
|------|------|
| 打分器无法判断复杂度 | 默认推荐 **moderate**（最安全的中间层） |
| 用户不确认也不覆盖 | 提示一次后按推荐执行（但记录 `user_override: false`） |
| Prompt injection 检出 | 标记内容，**不阻断任务**，但在后续 phase 中高亮警告 |

---

## Open Questions

1. **打分是每次任务都做，还是只在首次？** — 当前设计：每次任务都做（除非显式跳过）。但如果同一个 PR 内的连续小改动都重新打分，会很烦。考虑"同一会话内 profile 锁定"？
2. **Durable docs 的加载粒度**：全量加载 vs 按任务相关性过滤？Trellis 用 JSONL 做精确注入，但早期可以先全量。
3. **打分结果是否持久化？** — 当前设计：只在内存中，不写文件。但如果要支持 `--from-phase=1` 恢复，可能需要持久化到 triage-result.json。
