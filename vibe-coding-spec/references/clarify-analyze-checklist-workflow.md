# Clarify / Analyze / Checklist Workflow

## Clarify 工作流

在进入 `plan.md` 前先处理澄清问题。Clarify 不是随便问几个问题，而是一次结构化的覆盖扫描。

### Step 1: 九类覆盖扫描

逐类扫描 `spec.md`（以及其中落盘的 PRD source 和 traceability），把每一类标记为 `Clear` / `Partial` / `Missing`：

| # | 分类 | 检查内容 |
|---|---|---|
| C1 | Functional Scope & Behavior | 用户目标、out-of-scope 边界、角色区分 |
| C2 | Domain & Data Model | 实体、属性、唯一性规则、状态转换、规模 |
| C3 | Interaction & UX Flow | 用户旅程、错误/加载状态、可达性、不可逆操作 |
| C4 | Non-Functional Quality | 性能目标、可扩展性、可靠性、可观测性、安全、合规 |
| C5 | Integration & External Dependencies | 外部 API、数据格式、协议假设、adapter contract |
| C6 | Edge Cases & Failure Handling | 负向场景、限流、冲突解决、并发 |
| C7 | Constraints & Tradeoffs | 技术约束、被拒绝的替代方案 |
| C8 | Terminology & Consistency | 术语表、同义词混用 |
| C9 | Completion Signals | 可测试的 acceptance、Definition of Done、evidence type |

同时收集 spec 正文中所有 `[NEEDS CLARIFICATION: ...]` 内联标记——它们是 specify 阶段留下的待澄清点，必须全部进入候选问题或显式 deferred。

### Step 2: 生成并排序问题

- 只对 `Partial` / `Missing` 的分类生成候选问题。
- 按 **Impact × Uncertainty** 排序：答案会改变 spec/plan/tasks/release gate 的问题优先；只是偏好型的问题丢弃。
- 每轮最多问 5 个问题。

阻塞 plan 的问题（blocking）：

- 数据模型或状态转换不清楚。
- 安全、隐私、权限、审计、密钥处理不清楚。
- 不可逆 UX 或破坏性操作不清楚。
- 外部 API、事件、文件格式、adapter contract 不清楚。
- P0 acceptance、evidence type、release gate 不清楚。

非阻塞问题写入 `review.md` 的 Clarifications / Open Questions，可以进入 plan，但必须在风险里标注。

### Step 3: 逐题多选呈现

问题**一次只问一个**。每个问题必须能用以下方式之一回答：

- **多选**：2-5 个离散选项，用 Markdown 表格呈现；推荐选项放最上面并给 1-2 句推荐理由；用户回答字母即可。
- **短答**：5 个词以内能答完。

格式示例：

```markdown
**Q1 (C2 Domain & Data Model): 删除会话时关联消息如何处理？**

推荐 A：级联软删除——保留审计能力且符合 spec 中"可恢复"的描述。

| 选项 | 含义 |
|---|---|
| A | 级联软删除，30 天后物理清除 |
| B | 级联硬删除，立即不可恢复 |
| C | 禁止删除有消息的会话 |
| Short | 5 词以内自定义答案 |
```

### Step 4: 逐题原子回写

每得到一个答案，**立即**做完以下动作再问下一题：

1. 在 `review.md` 的 `## Clarifications` 下追加 `### Session <YYYY-MM-DD>` 记录：`Q: ... → A: ...`。
2. 把答案立即应用到受影响 artifact，替换矛盾的旧表述而不是并存：
   - 需求变更回填 `spec.md`（并移除对应的 `[NEEDS CLARIFICATION]` 标记）
   - 默认假设回填 `spec.md` 的 Assumptions
   - 技术决策回填 `plan.md`
   - 任务顺序回填 `tasks.md`
   - 验证要求回填 `review.md` 的 Test Matrix 或 Release Gate
3. 保存文件后再继续，防止上下文丢失。

### Step 5: Coverage Summary

clarify 结束时在 `review.md` 输出覆盖总结表：

```markdown
## Coverage Summary <YYYY-MM-DD>

| 分类 | 状态 |
|---|---|
| C1 Functional Scope | Resolved |
| C2 Domain & Data Model | Clear |
| C3 Interaction & UX | Deferred |
| ... | ... |

- Questions asked: 4
- Sections modified: spec.md (FR-002, Assumptions), review.md (TC-003)
- Remaining [NEEDS CLARIFICATION] markers: 0
- Next: proceed to plan / re-run clarify
```

状态含义：`Resolved`（本轮解决）、`Clear`（本来就清楚）、`Deferred`（超出问题配额或更适合 plan 阶段处理）、`Outstanding`（仍 Partial/Missing 但影响低）。

`Outstanding` 和 `Deferred` 项必须出现在 `plan.md` 的风险或 `spec.md` 的 Assumptions 里；存在 blocking 级 `Outstanding` 时不得进入 plan。

## Analyze 工作流

实现前运行 analyzer：

```bash
python3 vibe-coding-spec/scripts/check_vibe_structure.py --root . --feature <###-slug> --version <version>
```

需要机器消费时：

```bash
python3 vibe-coding-spec/scripts/check_vibe_structure.py --root . --feature <###-slug> --version <version> --json
```

需要刷新 checklist 时：

```bash
python3 vibe-coding-spec/scripts/check_vibe_structure.py --root . --feature <###-slug> --version <version> --write-checklist
```

处理顺序：

1. 先修 CRITICAL 和 HIGH。
2. MEDIUM 可以带风险进入实现，但必须在 final report 说明。
3. LOW 是结构建议，不应阻塞 spike；release readiness 时需要解释。

analyze 还必须人工检查脚本覆盖不到的语义问题：

- spec 正文是否残留 `[NEEDS CLARIFICATION]` 标记。
- plan 的 Constitution Check 是否通过；Complexity Tracking 表中的违规是否都有辩护。
- coverage summary 中是否有 blocking 级 `Outstanding`。

## Checklist 规则

Checklist 是需求质量的单元测试，不是项目待办，更不是实现测试计划。分两层：

- **结构层** `review.md`（脚本生成）必须覆盖：
  - 规格是否没有占位符和 `[NEEDS CLARIFICATION]` 残留。
  - user stories 是否可独立测试、是否标了 P1/P2/P3。
  - acceptance 是否可验证。
  - Assumptions 和 Edge Cases 是否显式记录。
  - plan 是否包含 Research、Data Model、Contracts、Quickstart 决策。
  - plan 的 Constitution Check 是否完成、违规是否进入 Complexity Tracking。
  - tasks 是否有 dependency、parallel ownership、RED/GREEN、evidence。
  - P0 是否映射到 TC 和 evidence ref。
- **需求质量层** `review.md`：按领域生成的问题句条目（CHK 编号、质量维度标签、traceability 引用）。生成方法论、句式规则、校准问题见 `checklist-authoring-workflow.md`。

implement 开工前必须检查两层的完成度（Pre-flight 门禁，见 `subagent-execution-workflow.md`）。
