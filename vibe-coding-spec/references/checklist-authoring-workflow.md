# Checklist Authoring Workflow

Checklist 是**需求的单元测试**：spec 是用英语写的代码，checklist 就是它的测试套件。它检验需求写得好不好，**不**检验实现跑得对不对。

## 两层 checklist

| 层 | 文件 | 来源 | 检验对象 |
|---|---|---|---|
| 结构层 | `specs/###-slug/CHECKLIST.md` | `check_vibe_structure.py --write-checklist` 生成 | artifact 结构完整性、覆盖关系 |
| 需求质量层 | `specs/###-slug/checklists/<domain>.md` | 按本工作流人工/agent 生成 | 需求本身的质量 |

需求质量层按领域拆文件：`checklists/ux.md`、`checklists/api.md`、`checklists/security.md`、`checklists/performance.md` 等。每个文件 15-40 条；候选条目超过 ~40 时合并重复项、把低影响 edge case 归并成单条。

## 生成前：最多 3 个校准问题

不要用预制问题列表。从用户输入和 spec/plan 中提取信号（领域关键词、风险暗示、利益相关方、明确交付物），聚成 2-4 个焦点领域，然后最多问 3 个问题校准：

1. **深度**：轻量自查 sanity check，还是正式 release gate？
2. **受众**：作者自查、peer review，还是 stakeholder 门禁？
3. **焦点**：最重要的 2-3 个质量维度是哪些？

用户已经说清楚的不要再问。只从 spec/plan/tasks 推断上下文，不得编造需求或场景。

## 条目句式规则

**每条必须是关于需求质量的问题句**，并带质量维度标签和 traceability 引用。

✅ 正确（检验需求）：

```markdown
- [ ] CHK001 Are error handling requirements defined for failed payment submissions? [Completeness, Spec §FR-003]
- [ ] CHK002 Is "fast response" quantified with a specific latency target? [Clarity, Spec §SC-001]
- [ ] CHK003 Do the retry requirements in §FR-005 align with the idempotency assumption in §FR-002? [Consistency]
- [ ] CHK004 Are requirements defined for concurrent edits to the same record? [Gap]
- [ ] CHK005 Is the assumption that all users have verified emails recorded and validated? [Assumption, Spec §Assumptions]
```

❌ 禁止（检验实现——这是测试计划该干的事，不是 checklist）：

```markdown
- [ ] Verify the button clicks correctly
- [ ] Test error handling works
- [ ] Confirm the API returns 200
```

规则：

- 条目编号 `CHK001` 起；追加到已有文件时从最后一个 CHK ID 继续，**不得删除或改写已有条目**。
- 质量维度标签：`[Completeness]` `[Clarity]` `[Consistency]` `[Measurability]` `[Coverage]`；问题类标签：`[Gap]` `[Ambiguity]` `[Conflict]` `[Assumption]`。
- ≥80% 的条目必须带 traceability 引用：`[Spec §X]`、`[Gap]`、`[Ambiguity]` 等。
- 场景覆盖维度按四类检查：Primary / Alternate / Exception / Recovery flows。

## 质量维度清单

生成条目时按这些维度扫描：

- **Requirement Completeness**：必要的需求都写了吗？
- **Requirement Clarity**：具体、无歧义吗？模糊词量化了吗？
- **Requirement Consistency**：条目之间有冲突吗？
- **Acceptance Criteria Quality**：可客观验证吗？
- **Scenario Coverage**：主流程/备选/异常/恢复四类场景都覆盖了吗？
- **Edge Case Coverage**：边界条件写了吗？
- **Non-Functional**：性能、安全、可达性需求定义了吗？
- **Dependencies & Assumptions**：依赖和假设记录并验证了吗？
- **Ambiguities & Conflicts**：已知歧义都被显式标记了吗？

## 完成报告

生成后报告：文件路径、条目数、焦点领域、深度级别、用户指定的必查项。

## 与 implement 的关系

implement 开工前必须扫描 `checklists/` 统计完成度；有未完成项时暂停并要用户明确确认才继续（见 `subagent-execution-workflow.md` 的 Pre-flight 门禁）。
