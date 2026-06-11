# Subagent Execution Workflow

## 何时使用子 agent

可以使用多个子 agent 加速，但必须先切清楚边界。

适合并行：

- spec/plan 阶段的技术调研、风险审查、测试矩阵审查。
- implementation 阶段写入不同文件集合的任务。
- review 阶段的 spec compliance review 和 code quality review。

不适合并行：

- 多个 agent 同时改同一个文件。
- 多个 agent 同时定义同一个接口、数据模型或 contract。
- 下一个关键步骤马上依赖结果的阻塞任务。

## 角色

Explorer agent：

- 只读或以报告为主。
- 用于 research、risk、artifact consistency、test matrix review。
- 输出必须包含来源文件、结论、风险、建议改动。

Worker agent：

- 负责实现任务。
- 必须有明确 ownership：文件、模块、任务 ID、测试命令。
- 只改自己负责的文件。
- 不得回滚其他 agent 或用户的改动。
- final 必须列出改过的文件、运行过的命令、未验证范围。

Reviewer agent：

- 第一阶段 review：spec compliance，检查是否满足 FR、TC、acceptance、evidence。
- 第二阶段 review：code quality，检查边界、可维护性、测试质量、安全风险。

## 分派模板

Worker prompt 应包含：

```text
你不是唯一在代码库里工作的 agent。不要回滚别人或用户的改动。

Task: T004
Requirement: FR-001
Test Case: TC-001
Owned files:
- src/path/to/file.py
- test/path/to/test_file.py

Do not edit:
- contracts/
- data-model.md
- files owned by other agents

Steps:
1. Write failing test and run it.
2. Implement minimal code.
3. Run focused verification.
4. Update evidence ref.
5. Report changed files and commands.
```

## 并行安全规则

- 先在 `tasks.md` 的 Parallel Ownership 表登记任务、owned files、blocked by。
- 只有 `[P]` 任务可并行。
- 共享接口、数据模型、contract 必须由一个 owner 先完成，其他任务依赖它。
- 主 agent 负责整合结果、解决冲突、最终 fresh verification。
- 子 agent 报告成功后，主 agent 仍必须检查 diff 和运行验证；不能直接相信报告。

## Worktree 隔离

推荐每个大任务或并行任务组使用独立 worktree/branch：

```bash
git worktree add ../<repo>-<feature>-pg001 -b <feature>-pg001
```

如果不能使用 worktree，必须用 disjoint write set，并在 `tasks.md` 写清楚 ownership。
