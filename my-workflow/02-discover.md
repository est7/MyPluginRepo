# Phase 1: DISCOVER — 需求澄清 + 代码理解 + 人类确认

## 目的

确保 agent 在写任何 spec/plan 之前，**真正理解了问题和代码**。

这是真实场景中验证过的关键洞察：不是所有理解错误都能在 plan review 时发现。如果 agent 对调用链的理解本身就是错的，它产出的 plan 看起来"合理"但基于错误前提。必须在 plan 之前有一个独立的"理解确认" checkpoint。

---

## 内部步骤

```
[来自 Phase 0 的 triage-result + profile]
    │
    ▼
[Step 1.1] 需求澄清
    │   Agent 主动提问不清楚的需求点
    │   输出：clarification Q&A
    │   Gate: 用户确认需求边界
    │
    ▼
[Step 1.2] 最小实现上下文获取
    │   用户提供代码入口 + 验收锚点
    │   可选：相关模块名、设计稿、API 文档、团队约定
    │   → 若入口不明确，主动请求 (C5)
    │
    ▼
[Step 1.3] 代码库探索
    │   Agent 沿入口定向探索（Glob/Grep/Read/LSP）
    │   外部知识检索（Context7/Exa/DeepWiki，按需）
    │   Research gate: 未解决问题必须标记 (C1)
    │
    ▼
[Step 1.3b] context.jsonl 产出 (Complex+ only)
    │   基于探索结果声明 worker 上下文边界
    │   输出：context.jsonl (schema 见 09-schemas.md)
    │
    ▼
[Step 1.4] 代码理解摘要 ← 关键产物
    │   输出结构化摘要（非自由文本）
    │
    ▼
[G1: Understanding Confirm Gate]
    │   人类审查摘要 → 确认/修正/打回
    │   通过 → Phase 2
    │   打回 → 回到 Step 1.3 重新探索
```

---

## 输入产物

| 产物 | 来源 | 必需？ |
|------|------|--------|
| triage-result (profile, score, evidence) | Phase 0 | YES |
| 用户请求文本 | 用户 | YES |
| Durable docs | Phase 0 加载 | 如果存在 |
| 最小实现上下文 (入口+锚点) | 用户提供 | Standard+ |

## 输出产物

| 产物 | 类型 | Schema | Profile |
|------|------|--------|---------|
| `code-understanding.md` | Transient | 见下方模板 | Standard+ |
| `clarification-log` | Transient (内存) | Q&A pairs | Standard+ |
| `open-questions.md` | Transient | 未解决问题列表 | Standard+ |
| `context.jsonl` | Transient | 见 [09-schemas.md](./09-schemas.md) §4 | Complex+ |

### context.jsonl 产出规则（Complex+）

Complex 及以上 profile 在代码探索完成后，产出 `context.jsonl` 声明 worker agent 的上下文边界。

**何时产出**：Step 1.3 代码探索完成后，Step 1.4 理解摘要之前。

**产出方式**：基于探索过程中实际访问的文件列表，过滤为影响范围内的文件，标注 `read-write` 或 `read-only` 模式。

```jsonl
{"file": "src/auth/middleware.ts", "reason": "Main modification target", "mode": "read-write"}
{"file": "src/auth/types.ts", "reason": "Type definitions to update", "mode": "read-write"}
{"file": "docs/interfaces.md", "reason": "API contract reference", "mode": "read-only"}
```

**Standard 以下**不产出 context.jsonl，靠 durable docs + code-understanding.md 做粗粒度上下文注入。

### code-understanding.md 模板

```markdown
## 入口与主调用链
- 入口：[文件:行号]
- 主路径调用链：A → B → C → D
- 关键分支：[条件] → [分支路径]

## 模块与职责
- 模块 A：[职责]
- 模块 B：[职责]

## 数据流 / 状态流
- 谁产生：
- 谁持有：
- 谁消费：
- 谁更新：

## 影响范围初判
- 直接影响：[文件列表]
- 间接影响：[调用方列表]

## 假设 / 不确定点
- 假设 1：[内容] — 已确认/待确认
- 不确定项 1：[内容]
```

---

## Gate 定义

### G1: Understanding Confirm Gate

| 属性 | 值 |
|------|-----|
| 类型 | Hard (Standard+), Skip (Quick/Simple) |
| 触发 | code-understanding.md 产出后 |
| 行为 | 人类审查"理解是否正确"，不是审查"方案是否合理" |
| 通过 | 进入 Phase 2 |
| 打回 | 回到 Step 1.3，Agent 带着修正信息重新探索 |
| 最大重试 | 3 次（超限 → Escalation，暂停等用户提供更多上下文） |

### Research Gate (C1, 内嵌)

| 属性 | 值 |
|------|-----|
| 类型 | Soft (Standard), Hard (Complex+) |
| 触发 | Step 1.3 结束时 |
| 行为 | 检查 open-questions.md 是否有未解决问题 |
| Complex+ | 存在未解决问题 → **阻断**，不允许进入 Phase 2 |
| Standard | 存在未解决问题 → **警告**，用户决定是否继续 |

---

## Profile 行为矩阵

| Step | Quick | Simple | Standard | Complex | Orchestrated |
|------|---------|--------|----------|---------|---------|
| 1.1 需求澄清 | 跳过 | 1句话确认 | 标准 Q&A | 全量 + scope 确认 | 全量 + BDD 场景草案 |
| 1.2 上下文获取 | 跳过 | 跳过 | 用户提供入口 | 用户提供入口+模块 | 全量 |
| 1.3 代码探索 | 跳过 | 快速 grep | 定向探索 | 深度探索 + 外部研究 | 深度 + 多源 (C2) |
| 1.3b context.jsonl | 跳过 | 跳过 | 跳过 | ✅ 产出 | ✅ 产出 |
| 1.4 理解摘要 | 跳过 | 跳过 | 标准模板 | 标准 + 假设清单 | 标准 + 影响图 |
| G1 人类确认 | 跳过 | 跳过 | ✅ 必须 | ✅ 必须 | ✅ 必须 |

---

## 参考框架

| 机制 | 来源 | 如何使用 |
|------|------|---------|
| 代码理解摘要 (Step 7-8) | 真实场景 `真实场景.md` | 直接采用，模板微调 |
| 需求澄清问答 (Step 3) | 真实场景 + 半自动流程 | 直接采用 |
| Research gate (open questions 阻断) | GSD `research-gate.ts` | Conservative fail 模式 |
| 代码库入口引导 (Step 5-6) | 真实场景 | 用户提供最小上下文包 |
| 多源研究路由 | code-context plugin | Context7/Exa/DeepWiki 按问题类型路由 |
| Fresh subagent per phase | GSD/yoyo-evolve | Phase 1 使用独立上下文 agent |
| Context degradation tiers | GSD | 监控 agent 上下文使用率 |

---

## Hooks

| Hook | 事件 | 行为 |
|------|------|------|
| `discover-start` | Phase transition | 创建 code-understanding.md 框架 |
| `context-monitor` | PostToolUse | 监控上下文使用率，DEGRADING 时警告 |
| `research-complete` | 自定义 | 检查 open-questions.md |

---

## 失败路径

| 场景 | Gate Taxonomy | 处理 |
|------|--------------|------|
| Agent 无法找到代码入口 | `escalation` | 请求用户提供入口文件 |
| 理解摘要被打回 3 次 | `escalation` | 暂停，用户提供更详细的上下文包 |
| 外部研究源不可用 (Context7/Exa) | `revision` (降级) | 仅用本地代码探索 |
| 上下文窗口 DEGRADING | `revision` | 将已收集信息写入 code-understanding.md，重启 fresh subagent 继续 |

---

## Open Questions

1. **代码理解摘要是否应该用 subagent 生成？** 如果主 agent 做探索，它的上下文会被代码内容填满。用 subagent 探索 → 返回摘要 → 主 agent 继续，可以保持主 agent 上下文干净。但增加了编排复杂度。
2. **clarification Q&A 是否持久化？** 当前设计：内存中，不写文件。但跨会话恢复时可能需要。
3. **Standard 任务的理解摘要是否过重？** 如果大部分 standard 任务用户已经很清楚入口，理解摘要可能是多余的 ceremony。考虑加 `--skip-understanding` flag？
