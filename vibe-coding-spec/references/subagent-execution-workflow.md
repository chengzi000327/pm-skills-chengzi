# Subagent Execution Workflow

## 核心原则

**每个任务派发一个全新的 subagent + 每个任务两阶段 review（先 spec 后 quality）= 高质量、快迭代。**

subagent 不继承主 session 的上下文和历史——主 agent 为它精确构造所需的全部上下文（任务全文、owned files、命令、项目约定）。这同时保护主 agent 自己的上下文用于协调工作。

## Continuous Execution 规则

进入 implement 阶段后，**不要在任务之间停下来向用户汇报或请求确认**。"要继续吗？"和逐任务进度总结浪费用户时间——用户要求执行计划，就执行完。

只有三种情况允许停下：

1. BLOCKED 且主 agent 无法解决（环境缺失、权限不足、外部依赖挂了）。
2. 真歧义：任务和 spec/代码冲突，且任何选择都会改变需求语义。
3. 全部任务完成。

停下时更新 `run-state.json` 的 `blocked` / `blockedReason`，让下一个 session 能接手。

## 何时使用子 agent

适合并行：

- spec/plan 阶段的技术调研、风险审查、测试矩阵审查。
- implementation 阶段写入不同文件集合的任务。
- review 阶段的 spec compliance review 和 code quality review。

不适合并行：

- 多个 agent 同时改同一个文件。
- 多个 agent 同时定义同一个接口、数据模型或 contract。
- 下一个关键步骤马上依赖结果的阻塞任务。

任务紧耦合（每个任务都依赖上一个的产出）时，放弃并行，主 agent 顺序执行或派单个 worker 顺序做。

## 每任务执行循环

```text
对每个任务 T：
1. 主 agent 从 tasks.md 提取任务全文 + 上下文，
   用 prompts/implementer-prompt.md 填空派发 implementer。
2. [Question loop] implementer 发现歧义/缺上下文 → 返回问题清单，
   主 agent 答疑（必要时查 spec/plan/代码）→ 重新派发。
   没有问题才开始写代码。
3. implementer 执行：RED → GREEN → self-review → evidence → commit → 报告。
4. 主 agent 派 spec reviewer（prompts/spec-reviewer-prompt.md）。
   FAIL → implementer 修 spec 缺口 → 重新 spec review。
5. spec review PASS 后，派 code quality reviewer
   （prompts/code-quality-reviewer-prompt.md）。
   CHANGES REQUIRED（CRITICAL/HIGH）→ implementer 修 → 重新 quality review。
6. 两阶段都通过 → 勾掉 tasks.md checkbox，更新 run-state.json，进入下一个任务。

全部任务完成后：
7. 派 final reviewer 用 quality reviewer prompt 审整个 feature 的 diff
   （范围 = 整个 branch，重点：跨任务一致性、整体架构、遗漏的集成点）。
8. 主 agent 做最终 fresh verification，然后进入 finish 流程
   （见 review-finish-debug-workflow.md）。
```

关键纪律：

- **逐任务 review 通过才算完成**——不要攒一批任务最后一起 review。
- **最终整体 review 不可省略**——逐任务 review 看不到跨任务的不一致。
- 子 agent 报告成功后，主 agent 仍必须检查 diff 和运行验证；不能直接相信报告。
- reviewer 的意见也可能错；implementer 对存疑意见先验证再改（见 review-finish-debug-workflow.md 的 receiving-review 纪律）。

## 角色

Explorer agent：

- 只读或以报告为主。
- 用于 research、risk、artifact consistency、test matrix review。
- 输出必须包含来源文件、结论、风险、建议改动。

Worker / Implementer agent：

- 用 `prompts/implementer-prompt.md` 派发。
- 必须有明确 ownership：文件、模块、任务 ID、测试命令。
- 只改自己负责的文件；不得回滚其他 agent 或用户的改动。
- 开工前有 question loop 权利；final 必须列出改过的文件、运行过的命令、未验证范围。

Reviewer agent：

- 第一阶段用 `prompts/spec-reviewer-prompt.md`：spec compliance。
- 第二阶段用 `prompts/code-quality-reviewer-prompt.md`：code quality。
- final overall review 复用 quality prompt，范围换成整个 feature。

## 并行安全规则

- 先在 `tasks.md` 的 Parallel Ownership 表登记任务、owned files、blocked by。
- 只有 `[P]` 任务可并行。
- 共享接口、数据模型、contract 必须由一个 owner 先完成，其他任务依赖它。
- 主 agent 负责整合结果、解决冲突、最终 fresh verification。
- 并行任务各自走完两阶段 review 后，合流点再做一次集成验证。

## Worktree 隔离

推荐每个大任务或并行任务组使用独立 worktree/branch：

```bash
git worktree add ../<repo>-<feature>-pg001 -b <feature>-pg001
```

如果不能使用 worktree，必须用 disjoint write set，并在 `tasks.md` 写清楚 ownership。worktree 路径记入 `run-state.json` 的 `worktree` 字段，finish 阶段负责清理（见 review-finish-debug-workflow.md）。
