# Phase 4: VERIFY — 双维审查 + 质量门禁 + 人类验收

## 目的

回答一个问题：**代码真的对吗？**

不信任 agent 的自我声称。用编译、测试、独立审查 agent、人类验收四层递进验证。

核心创新点：
1. **spec-fit vs quality-fit 双维审查**：拆开"是否做对"和"是否做好"，避免混为一体
2. **verify-evidence.json 硬证据**：Ralph Loop 要求结构化证据文件，不接受自然语言声称
3. **Stall Detection**：所有 revision loop 增加连续相同错误检测

---

## 内部步骤

```
[来自 Phase 3 的代码变更 + G7 checkpoint 结果]
    │
    ▼
[Step 4.1] 自动化验证
    │   G7 checkpoint 结果已在 Phase 3 末尾运行
    │   此处做补充验证：
    │   - 运行完整测试套件（不只是增量）
    │   - 检查覆盖率变化
    │   - lint/format 最终确认
    │   → 产出 verify-evidence.json (每个 task 一条)
    │
    ▼
[Step 4.2] 双维质量审查 (spec-fit + quality-fit)
    │   a. spec-fit: AC 覆盖、边界遵守、spec 要求满足
    │   b. quality-fit: 架构违规、不必要依赖、缺失测试、坏味道
    │
    │   Standard: Agent 自检 → 仅 spec-fit (soft)
    │   Complex: 独立 code-review agent → spec-fit + quality-fit
    │   Orchestrated: 双模型并行审查 + Rubric evaluator
    │   → 产出 verify-review.json (schema 见 09-schemas.md §8)
    │
    ▼
[G8: Ralph Loop — verify-evidence 硬检查]
    │   Agent 不能仅说 "Looks good / Done"
    │   必须存在 verify-evidence.json:
    │   - exit_code = 0
    │   - stdout_excerpt 非空
    │   - timestamp 有效
    │
    │   缺少 evidence → 打回重跑验证
    │   Stall detection: 连续 2 次同样的 evidence 缺失 → escalation
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
    │   - 对照验收条件逐项确认（AC Traceability Matrix）
    │
    │   通过 → Phase 5
    │   发现问题 → 按 delta 类型分流重入（真实场景优化点 2）
    │     ├─ 实现 bug → 回 Phase 3 直接修复
    │     ├─ 方案偏差 → 回 Phase 2 Plan Gate
    │     └─ 需求变化 → 回 Phase 1 需求澄清
```

---

## spec-fit vs quality-fit 双维审查

拆分审查为两个独立维度（来自 12-Codex 建议），避免"功能正确但架构糟糕"或"代码漂亮但不满足需求"的混淆。

### spec-fit（规格符合度）

- AC 覆盖率：每个 covers_ac 是否有对应 verify-evidence
- 边界遵守：修改是否超出 allowed_paths 声明
- spec 要求满足：BDD 场景是否全部通过
- 结果：`PASS | FAIL | PASS_WITH_NOTES`

### quality-fit（工程质量）

四类问题检查（来自真实场景）：
- 是否违反既有架构边界
- 是否引入不必要依赖或新模式
- 核心改动是否带必要测试
- 是否出现明显坏味道

结果：`PASS | FAIL | PASS_WITH_NOTES`

### Profile 裁剪

| Profile | spec-fit | quality-fit |
|---------|----------|-------------|
| quick | 跳过 | 跳过 |
| simple | 隐含（verify_cmd 通过即可） | 跳过 |
| standard | ✅ Agent 自检 | 跳过 |
| complex | ✅ 独立 review agent | ✅ 独立 review agent |
| orchestrated | ✅ 双模型审查 | ✅ 双模型审查 + Rubric |

---

## 输入产物

| 产物 | 来源 | 必需？ |
|------|------|--------|
| 源代码变更 | Phase 3 | YES |
| `tasks.json` (Baseline + Delta) | Phase 2-3 | Simple+ |
| G7 checkpoint 结果 | Phase 3 | YES |
| `spec.md` (验收条件) | Phase 2 | Standard+ |
| `delta-log.jsonl` | Phase 3 | 如果存在 |
| Execution contract | Phase 2 (Orchestrated) | Orchestrated |

## 输出产物

| 产物 | 类型 | Schema | 说明 |
|------|------|--------|------|
| `verify-evidence.json` | Transient | [09-schemas.md §2](./09-schemas.md) | 每个 task 的验证证据 |
| `verify-review.json` | Transient | [09-schemas.md §8](./09-schemas.md) | spec-fit + quality-fit 双维审查 |
| Human acceptance decision | 触发 Phase 5 | — | pass / fail + delta type |
| Completion Markers | 内嵌于 agent 输出 | [09-schemas.md §10](./09-schemas.md) | VERIFICATION PASSED / ESCALATION NEEDED |

---

## Gate 定义

### G8: Ralph Loop (防逃逸)

| 属性 | 值 |
|------|-----|
| 类型 | Hard (Standard+) |
| 来源 | Trellis `ralph-loop.py` (SubagentStop hook) |
| 触发 | Agent 声称验证完成时 |
| 检测 | 扫描 `verify-evidence.json`，必须包含 `exit_code` + `stdout_excerpt` + `timestamp` |
| evidence 缺失 | → 打回，附带"请实际运行测试并提供 verify-evidence" |
| exit_code != 0 | → task 标记 `failed`，触发 build-fix loop (G5) |
| Stall detection | 连续 2 次相同缺失模式 → 自动升级为 `escalation` |
| 最大重试 | 3 次 → Escalation |

### G9: Human Acceptance Gate

| 属性 | 值 |
|------|-----|
| 类型 | Skip (Quick/Simple), Soft (Standard), Hard (Complex+) |
| 触发 | 自动化验证 + 审查全部通过后 |
| Quick/Simple | 自动通过（代码改动小，checkpoint 已覆盖） |
| Standard | 用户可选确认（默认通过，但可打回） |
| Complex+ | **强制人工验收**，不可跳过 |
| 验收依据 | AC Traceability Matrix（见 [09-schemas.md §9](./09-schemas.md)） |

### 审查层级

| Profile | 审查方式 |
|---------|---------|
| Quick | 无审查 |
| Simple | Agent 自检（soft） |
| Standard | Agent 自检 → spec-fit only |
| Complex | 独立 code-review agent → spec-fit + quality-fit |
| Orchestrated | 双模型并行审查 + Rubric evaluator |

---

## Profile 行为矩阵

| Step | Quick | Simple | Standard | Complex | Orchestrated |
|------|---------|--------|----------|---------|---------|
| 4.1 自动验证 | Quick (lint) | Standard (unit) | Full (integration) | Full + coverage | Full + pass@k (可选) |
| 4.2 spec-fit | 无 | 隐含 | ✅ Agent 自检 | ✅ Review agent | ✅ 双模型 |
| 4.2 quality-fit | 无 | 无 | 无 | ✅ Review agent | ✅ 双模型 + Rubric |
| verify-evidence | 无 | 无 | ✅ 每 task 产出 | ✅ 每 task 产出 | ✅ 每 task 产出 |
| verify-review | 无 | 无 | ✅ spec-fit only | ✅ 完整双维 | ✅ 完整双维 |
| G8 Ralph loop | 跳过 | 跳过 | ✅ | ✅ | ✅ |
| Stall Detection | 无 | 无 | ✅ G8 | ✅ G8 | ✅ G8 |
| 4.3 Delta check | 无 | 无 | ✅ | ✅ | ✅ |
| G9 人类验收 | 自动通过 | 自动通过 | 可选 | **强制** | **强制 + UAT** |

---

## 参考框架

| 机制 | 来源 | 如何使用 |
|------|------|---------|
| 轻量质量审查 4 类 | 真实场景 优化点 4 | quality-fit 的审查清单 |
| Ralph Loop | Trellis `ralph-loop.py` | G8 防逃逸，升级为 verify-evidence 硬检查 |
| Verification-over-self-report | ECC-Mobile | verify-evidence.json 结构化证据 |
| spec-fit / quality-fit 拆分 | 12-Codex 建议 | 双维独立审查，避免混淆 |
| 独立 code-review agent | Superpowers `code-reviewer.md` | Complex 层 |
| 双模型并行审查 | CCG Codex∥Gemini | Orchestrated 层 |
| Receiving-code-review 纪律 | Superpowers | 收到审查不盲目接受 |
| GAN evaluator | Anthropic harness | 独立评估器 |
| Rubric evaluator | Anthropic harness | Orchestrated 层结构化打分 |
| Delta 分流重入 | 真实场景 优化点 2 | G9 失败后按 delta 类型回到正确层级 |
| pass@k | ECC-Mobile | Core Optional, Orchestrated 可启用 |
| 三层检查点 | ECC-Mobile | Quick/Standard/Full |
| Stall Detection | Gate Taxonomy 统一规范 | revision loop 连续 2 次相同错误 → escalation |

---

## Hooks

| Hook | 事件 | 行为 |
|------|------|------|
| `ralph-check` | SubagentStop | 检测 verify-evidence.json 存在且 exit_code=0 |
| `review-dispatch` | Phase 4 进入 | 按 profile 启动对应审查 agent |
| `evidence-validate` | verify-evidence 写入 | 校验 schema 完整性（字段、类型） |
| `acceptance-prompt` | 审查完成 | 提示用户做最终验收 |

---

## 失败路径

| 场景 | Gate Taxonomy | 处理 |
|------|--------------|------|
| 测试套件有 flaky test | `revision` | 如启用 pass@k → 运行 3 次取通过率；否则 → 标记 flaky，不阻断 |
| Review agent 给出误报 | `revision` | Receiving-code-review 纪律：技术论证后可拒绝审查意见 |
| 人类验收发现 UI 问题 | `revision` | Delta type=实现 bug → 回 Phase 3 直接修复 |
| 人类验收发现需求偏差 | `revision` | Delta type=需求变化 → 回 Phase 1 重新澄清 |
| Ralph loop 3 次仍无证据 | `escalation` | Agent 可能无法运行测试环境，需人工介入 |
| Ralph loop stall (连续相同缺失) | `escalation` | 连续 2 次同样 evidence 缺失 → 自动升级，不等 3 次 |
| spec-fit FAIL + quality-fit PASS | `revision` | 功能不对 → 回 Phase 3 修复实现 |
| spec-fit PASS + quality-fit FAIL | `revision` | 功能对但质量差 → 决定是否追加重构 task |
| 双维都 FAIL | `escalation` | 暂停，可能需要回 Phase 2 重新 plan |
| verify-evidence schema 校验失败 | `preflight` | 阻断 Ralph Loop 通过，修正后重试 |

---

## Open Questions

1. **Review agent 和 verify agent 是同一个还是分开？** 当前设计：verify = 跑测试 (自动化，产出 verify-evidence)，review = 看代码 (agent，产出 verify-review)。分开更清晰，但增加了 agent 数量。
2. **Rubric evaluator 的评分维度**：Anthropic harness 用了设计质量/原创性/工艺/功能性。代码审查可能需要不同维度：正确性/可维护性/性能/安全性。需要定义 code-specific rubric。
3. **spec-fit 的自动化程度**：AC 覆盖检查可以自动比对 tasks.json 的 covers_ac 和 verify-evidence，但 BDD 场景的通过判定仍需人工或 agent 解读。
