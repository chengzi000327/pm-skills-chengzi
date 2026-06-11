# Review / Finish / Debug Workflow

## Brainstorming 分段确认

不要一口气生成大规格。按顺序分段确认：

1. 用户目标和非目标。
2. P0 user stories。
3. 数据和权限边界。
4. 外部 contracts 和 adapter 影响。
5. 测试矩阵和 release gate。

每段确认后再写入 artifact。用户明确要求直接生成时，可以先生成 draft，但必须标记假设。

## Code Review 关卡

每个任务或并行任务组完成后做两阶段 review：

1. Spec compliance review
   - 是否满足对应 FR。
   - 是否满足 TC acceptance。
   - evidence ref 是否存在且可读。
   - 是否遗漏 P0 或 blocking clarification。

2. Code quality review
   - 是否破坏目录边界。
   - 是否把 provider-specific logic 放进 core。
   - 是否有未必要的抽象或 speculative feature。
   - 测试是否验证行为而不是实现细节。

CRITICAL/HIGH review findings 必须修复后才能继续后续任务。

## Finishing Branch

完成实现后：

1. 运行 analyzer。
2. 运行完整测试、lint、typecheck、build 中适用的命令。
3. 检查 `git status --short` 和 `git diff`。
4. 更新 `TEST_REPORT.md`、`RELEASE_GATE.md`、evidence refs。
5. 报告：
   - fresh verification commands
   - passing/failing counts
   - changed files
   - untested scope
   - residual risks

不要在未运行 fresh verification 的情况下说完成、通过、修复、可发布。

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
- 修改无关模块来“顺手清理”。
