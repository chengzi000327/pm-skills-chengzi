# Execution State / Resume / Sync Workflow

跨 session 续跑、agent 上下文同步和任务外部导出的机制。

## run-state.json

每个 feature 维护一份轻量执行状态文件：`specs/###-slug/run-state.json`。它是 `tasks.md` checkbox 之外的机器可读锚点，让中断后的新 session 不需要重读全部 artifact 就能定位进度。

Schema：

```json
{
  "feature": "001-feature-name",
  "version": "V0.1",
  "phase": "implement",
  "phaseHistory": ["ingest", "specify", "clarify", "plan", "tasks", "analyze", "implement"],
  "lastCompletedTask": "T004",
  "inProgressTask": "T005",
  "blocked": false,
  "blockedReason": null,
  "lastVerification": {
    "command": "pytest tests/feature -v",
    "result": "PASS",
    "passed": 12,
    "failed": 0,
    "at": "2026-06-11T10:00:00Z"
  },
  "constitutionCheck": {
    "preResearch": "PASS",
    "postDesign": "PASS"
  },
  "clarify": {
    "openBlocking": 0,
    "openNonBlocking": 2
  },
  "worktree": null,
  "updatedAt": "2026-06-11T10:00:00Z"
}
```

`phase` 取值：`ingest` / `specify` / `clarify` / `plan` / `tasks` / `analyze` / `implement` / `review` / `gate` / `done`。

更新规则：

- 每完成一个阶段或一个 task，更新 `run-state.json` 并和对应 checkbox 一起 commit。
- `lastVerification` 只记录**当前 session 真实运行过**的命令结果；不得手填。
- 发现状态和 `tasks.md` checkbox 不一致时，以 checkbox + git log 为准，并修正 run-state。

## Resume 协议

新 session 接手一个进行中的 feature 时，按顺序做：

1. 读 `run-state.json`，确定 `phase`、`lastCompletedTask`、`blocked`。
2. 只读当前 phase 需要的 artifact（implement 阶段读 `tasks.md` + `plan.md`；clarify 阶段读 `spec.md` + `review.md` 的 Clarifications 区），不要全量重读。
3. 运行 `lastVerification.command` 做 fresh baseline——上一个 session 的结果不算数。
4. baseline 和 run-state 记录不一致（如出现新失败）时，先走 systematic debugging，不要直接继续任务。
5. 从 `inProgressTask`（或 `lastCompletedTask` 的下一个）继续。

## Agent Context 同步

plan 定稿后（post-design Constitution Check 通过时），把**新的长期技术决策**增量同步到 agent 上下文文件（`CLAUDE.md`、`AGENTS.md` 或项目所用 agent 的等价文件）：

- 同步内容：新引入的技术栈、目录约定、命令、契约位置——后续 session 不读 plan 也应知道的事。
- 不同步：feature 细节、任务列表、临时决定。
- 方式：在标记区块内增量更新，保留人工手写内容：

```markdown
<!-- vibe-coding-spec:begin auto-managed -->
- 2026-06-11 (001-feature-name): 引入 SQLite 持久化，schema 见 specs/001-feature-name/plan.md
<!-- vibe-coding-spec:end auto-managed -->
```

## Tasks → Issues 导出

团队协作场景下，可把 `tasks.md` 导出为 GitHub issues（对应 spec-kit 的 `taskstoissues`）：

- 一个 task（或一个 user story phase）= 一个 issue；title 用 `[T004] <task name>`，body 含 requirement ID、test case ID、owned files、验证命令。
- 用 `gh issue create` 批量创建；issue 编号回写到 `tasks.md` 对应 task 行和 `spec.md` traceability 区。
- 导出后 `tasks.md` 仍是 single source of truth；issue 状态变化不自动回流，关闭 issue 前必须确认对应 task 的 fresh verification。

只在用户明确要求或项目已有 issue 驱动惯例时导出；不要默认创建外部资源。
