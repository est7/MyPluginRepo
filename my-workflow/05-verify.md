# Phase 4: VERIFY — 检查点 + 质量门禁 + 人类验收

## 目的

回答一个问题：**代码真的对吗？**

不信任 agent 的自我声称。用编译、测试、独立审查 agent、人类验收四层递进验证。

---

## 内部步骤

```
[来自 Phase 3 的代码变更 + checkpoint 结果]
    │
    ▼
[Step 4.1] 自动化验证
    │   G7 checkpoint 结果已在 Phase 3 末尾运行
    │   此处做补充验证：
    │   - 运行完整测试套件（不只是增量）
    │   - 检查覆盖率变化
    │   - lint/format 最终确认
    │
    ▼
[Step 4.2] 轻量工程质量审查
    │   四类问题检查（来自真实场景）：
    │   a. 是否违反既有架构边界
    │   b. 是否引入不必要依赖或新模式
    │   c. 核心改动是否带必要测试
    │   d. 是否出现明显坏味道
    │
    │   Moderate: Agent 自检 (soft)
    │   Complex: 独立 code-review agent (G1 分离原则)
    │   Harness: 双模型并行审查 (Codex∥Gemini)
    │
    ▼
[G8: Ralph Loop — 防逃逸检查]
    │   Agent 不能仅说 "Looks good / Done"
    │   必须提供 verify 证据：
    │   - 测试通过截图/日志
    │   - lint 零 warning 证据
    │   - 覆盖率数值
    │
    │   缺少证据 → 打回重跑验证
    │
    ▼
[Step 4.3] Delta loop 检查
    │   验证通过后，检查是否有 delta 需要处理
    │   → 有未处理 delta → 回 Phase 3 (G6)
    │   → 无 delta → 继续
    │
    ▼
[G9: Human Acceptance Gate]
    │   程序员做最终验收：
    │   - E2E / 真机 / UI 验证
    │   - 对照验收条件逐项确认
    │
    │   通过 → Phase 5
    │   发现问题 → 按 delta 类型分流重入（真实场景优化点 2）
    │     ├─ 实现 bug → 回 Phase 3 直接修复
    │     ├─ 方案偏差 → 回 Phase 2 Plan Gate
    │     └─ 需求变化 → 回 Phase 1 需求澄清
```

---

## 输入产物

| 产物 | 来源 | 必需？ |
|------|------|--------|
| 源代码变更 | Phase 3 | YES |
| Baseline Plan + Delta Log | Phase 2-3 | 参考 |
| G7 checkpoint 结果 | Phase 3 | YES |
| spec.md (验收条件) | Phase 2 | Moderate+ |
| Execution contract | Phase 2 (Harness) | Harness |

## 输出产物

| 产物 | 类型 | 说明 |
|------|------|------|
| `verify-report.md` | Transient | 验证结果汇总 |
| Review feedback | Transient | 审查意见（如有） |
| Human acceptance decision | 触发 Phase 5 | pass / fail + delta type |

---

## Gate 定义

### G8: Ralph Loop (防逃逸)

| 属性 | 值 |
|------|-----|
| 类型 | Hard (Moderate+) |
| 来源 | Trellis `ralph-loop.py` (SubagentStop hook) |
| 触发 | Agent 声称验证完成时 |
| 检测 | 扫描 agent 输出，必须包含实际命令执行的证据 |
| 缺少证据 | → 打回，附带"请实际运行测试并提供输出" |
| 最大重试 | 3 次 → Escalation |

### G9: Human Acceptance Gate

| 属性 | 值 |
|------|-----|
| 类型 | Skip (Trivial/Simple), Soft (Moderate), Hard (Complex+) |
| 触发 | 自动化验证 + 审查全部通过后 |
| Trivial/Simple | 自动通过（代码改动小，checkpoint 已覆盖） |
| Moderate | 用户可选确认（默认通过，但可打回） |
| Complex+ | **强制人工验收**，不可跳过 |

### 审查层级

| Profile | 审查方式 |
|---------|---------|
| Trivial | 无审查 |
| Simple | Agent 自检（soft） |
| Moderate | Verification skill（Superpowers 模式） |
| Complex | 独立 code-review agent（隔离上下文） |
| Harness | Codex∥Gemini 并行审查 + Rubric evaluator (G3) |

---

## Profile 行为矩阵

| Step | Trivial | Simple | Moderate | Complex | Harness |
|------|---------|--------|----------|---------|---------|
| 4.1 自动验证 | Quick (lint) | Standard (unit) | Full (integration) | Full + coverage | Full + pass@k (可选) |
| 4.2 质量审查 | 无 | 自检 | Verification skill | Review agent | Codex∥Gemini + Rubric |
| G8 Ralph loop | 跳过 | 跳过 | ✅ | ✅ | ✅ |
| 4.3 Delta check | 无 | 无 | ✅ | ✅ | ✅ |
| G9 人类验收 | 自动通过 | 自动通过 | 可选 | **强制** | **强制 + UAT** |

---

## 参考框架

| 机制 | 来源 | 如何使用 |
|------|------|---------|
| 轻量质量审查 4 类 | 真实场景 优化点 4 | Step 4.2 的审查清单 |
| Ralph Loop | Trellis `ralph-loop.py` | G8 防逃逸 |
| Verification-over-self-report | ECC-Mobile | 必须有 verify 证据 |
| 独立 code-review agent | Superpowers `code-reviewer.md` | Complex 层 |
| 双模型并行审查 | CCG Codex∥Gemini | Harness 层 |
| Receiving-code-review 纪律 | Superpowers | 收到审查不盲目接受 |
| GAN evaluator | Anthropic harness | 独立评估器 |
| Rubric evaluator | Anthropic harness | Harness 层结构化打分 |
| Delta 分流重入 | 真实场景 优化点 2 | G9 失败后按 delta 类型回到正确层级 |
| pass@k | ECC-Mobile | Core Optional, Harness 可启用 |
| 三层检查点 | ECC-Mobile | Quick/Standard/Full |

---

## Hooks

| Hook | 事件 | 行为 |
|------|------|------|
| `ralph-check` | SubagentStop | 检测 verify 证据存在 |
| `review-dispatch` | Phase 4 进入 | 按 profile 启动对应审查 agent |
| `acceptance-prompt` | 审查完成 | 提示用户做最终验收 |

---

## 失败路径

| 场景 | 处理 |
|------|------|
| 测试套件有 flaky test | 如启用 pass@k → 运行 3 次取通过率；否则 → 标记 flaky，不阻断 |
| Review agent 给出误报 | Receiving-code-review 纪律：技术论证后可拒绝审查意见 |
| 人类验收发现 UI 问题 | → Delta type=实现 bug → 回 Phase 3 直接修复 |
| 人类验收发现需求偏差 | → Delta type=需求变化 → 回 Phase 1 重新澄清 |
| Ralph loop 3 次仍无证据 | → Escalation: Agent 可能无法运行测试环境，需人工介入 |

---

## Open Questions

1. **Review agent 和 verify agent 是同一个还是分开？** 当前设计：verify = 跑测试 (自动化)，review = 看代码 (agent)。分开更清晰，但增加了 agent 数量。
2. **Rubric evaluator 的评分维度**：Anthropic harness 用了设计质量/原创性/工艺/功能性。代码审查可能需要不同维度：正确性/可维护性/性能/安全性。需要定义 code-specific rubric。
3. **人类验收的"验收条件清单"谁来生成？** 当前设计：从 spec.md 的验收条件自动提取 checklist。但 trivial/simple 没有 spec。
