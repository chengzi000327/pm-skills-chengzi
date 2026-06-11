# Review / Finish / Debug Workflow

## Brainstorming 分段确认

**HARD-GATE：设计未呈现并获用户批准前，禁止写任何代码、scaffold 任何项目、调用任何实现流程。对每个项目都适用，无论看起来多简单。**

反模式："这个太简单了，不需要设计。"——简单项目恰恰是未审视的假设浪费最多工作量的地方。设计可以只有几句话，但必须呈现并获批准。

流程：

1. 先探索项目上下文（文件、文档、最近 commit），再开始提问。
2. 澄清问题**一次只问一个**，搞清目标、约束、成功标准。
3. **提出 2-3 个方案**，每个带 trade-offs，给出你的推荐和理由——不要只呈现一个方案。
4. 方案选定后，按顺序分段确认设计：
   - 用户目标和非目标。
   - P0 user stories。
   - 数据和权限边界。
   - 外部 contracts 和 adapter 影响。
   - 测试矩阵和 release gate。
5. 每段确认后再写入 artifact。
6. **Spec self-review**：spec 写完后、请用户审阅前，先自查一遍：占位符残留、自相矛盾、歧义、范围蔓延——发现就地修。
7. 请用户审阅写好的 spec 文件，批准后才进入 plan。

用户明确要求直接生成时，可以先生成 draft，但必须标记假设（写入 spec 的 Assumptions），歧义处打 `[NEEDS CLARIFICATION]` 内联标记，且 draft 仍需用户批准后才能进入实现。

## Code Review 关卡

每个任务或并行任务组完成后做两阶段 review（prompt 模板见 `prompts/`）：

1. Spec compliance review
   - 是否满足对应 FR。
   - 是否满足 TC acceptance。
   - evidence ref 是否存在且可读。
   - 是否遗漏 P0 或 blocking clarification。

2. Code quality review
   - 是否破坏 constitution 规则和目录边界。
   - 是否把 provider-specific logic 放进 core。
   - 是否有未必要的抽象或 speculative feature。
   - 测试是否验证行为而不是实现细节。

CRITICAL/HIGH review findings 必须修复后才能继续后续任务。

全部任务完成后还有一次 **final overall review**：审整个 feature 的 diff，重点是跨任务一致性、整体架构和遗漏的集成点（见 `subagent-execution-workflow.md`）。

## Receiving Review 纪律（收到 review 意见时）

reviewer（无论人类还是 agent）也会出错。收到 review 意见后：

- **不要性能化地附和**。"You're absolutely right!" 然后照改，不是 review 流程，是噪音。
- **逐条分类处理**：
  - 意见正确且理解了 → 实施，说明改了什么。
  - 技术上存疑 → 先验证（读代码、跑测试、查文档）再决定；验证结果和意见冲突时，带证据反馈，而不是盲改。
  - 意见和 spec 冲突 → 升级给主 agent / 用户裁决，spec 是 source of truth。
  - 不清楚 → 提问澄清，不要猜着改。
- **修改后必须重新跑原验证**；为响应 review 而做的改动同样遵循 RED/GREEN 纪律。
- 不得为了让 reviewer 满意而弱化断言、删除测试或扩大任务范围。

## Finishing Branch

完成实现和 final review 后，按顺序收尾：

### 1. 最终验证

1. 运行 analyzer（`check_vibe_structure.py`）。
2. 运行完整测试、lint、typecheck、build 中适用的命令。
3. 检查 `git status --short` 和 `git diff`，确认没有未提交或不属于本 feature 的改动。
4. 更新 `review.md` 的 Test Report、Release Gate、evidence refs，以及 `run-state.json`（phase 置为 `review` 或 `gate`）。

### 2. 报告

- fresh verification commands 和真实输出
- passing/failing counts
- changed files
- untested scope
- residual risks

不要在未运行 fresh verification 的情况下说完成、通过、修复、可发布。

### 3. 结构化收尾选项（必须明确问用户选哪个）

验证通过后，向用户呈现四个选项，不要自作主张：

| 选项 | 动作 | 适用 |
|---|---|---|
| A. Merge 回主分支 | checkout 主分支 → merge → 跑一次主分支验证 | 本地工作流、用户授权直接合 |
| B. 开 Pull Request | push branch → `gh pr create`（含 summary 和 test plan） | 团队协作、需要 CI/人工审 |
| C. 保留分支 | 保持现状，记录分支名和未完成事项到 run-state | 还要继续迭代 |
| D. 丢弃 | 确认后删除分支/worktree | 实验失败、spike 结束 |

### 4. Worktree 清理

- 选 A/B/D：merge 或 PR 创建（或确认丢弃）后清理 worktree：

```bash
git worktree remove <path>
git branch -d <branch>   # 仅 A/D；B 留给 PR 合并后
```

- 选 C：保留 worktree，把路径和分支名写入 `run-state.json`。
- 丢弃（D）前必须检查未提交改动并向用户列出，确认后才删除。

`phase` 最终置为 `done`（A/B/D）或停在 `review`（C）。

## Systematic Debugging

失败时按顺序处理：

1. 复现：记录失败命令、输入、输出、环境。
2. 收窄：找到最小失败范围，避免大范围重写。
3. 根因：解释为什么失败，而不是只描述现象。
4. 修复：做最小改动。
5. 验证：原失败命令必须 fresh pass。
6. 回归：如有必要，加入会先 fail 后 pass 的测试。

禁止：

- 没有复现就猜测式修改。
- 为了过测试删除断言。
- 把失败测试标记 skip 当成修复。
- 修改无关模块来"顺手清理"。

### Bug-fix 请求的轻量路径

用户带着一个 bug 来（而不是新功能）时，不需要完整 lifecycle：

1. 按上面 1-3 步定位根因。
2. 若修复只碰 1-2 个文件：直接用单任务模板（RED：先写复现 bug 的失败测试 → GREEN → 验证 → commit），不需要 spec/plan。
3. 若根因揭示需求或架构问题（修复会改变行为契约、跨多模块）：升级为 feature，走 `specify -> plan` 流程，bug 报告写入 `spec.md` Source 区。
4. 修复完成后检查既有 `review.md` Test Matrix 是否要补一行回归 case。
