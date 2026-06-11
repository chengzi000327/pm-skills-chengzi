# Spec-kit + Superpower Workflow

## Lifecycle

Use this mapping when combining spec-kit style development with superpower execution plans.

```text
0. Constitution
   Project rules, principles, quality requirements.
   无 constitution 时用 constitution-template.md 引导生成（带 semver 版本治理）。

1. Ingest
   Preserve idea or PRD source, normalize scope, create traceability.
   初始化 run-state.json。

2. Specify
   What users need and why. Avoid implementation details.
   歧义处打 [NEEDS CLARIFICATION: ...] 内联标记；合理默认写入 Assumptions。

3. Clarify
   九类覆盖扫描 -> Impact × Uncertainty 排序 -> 逐题多选呈现 ->
   逐题原子回写 -> coverage summary。

4. Plan
   Constitution Check (pre-research GATE) -> research -> File Structure ->
   data model / contracts / quickstart -> Constitution Check (post-design GATE)
   -> Complexity Tracking（违规辩护）。
   定稿后同步 agent context（CLAUDE.md / AGENTS.md）。

5. Tasks
   Break plan into ordered, dependency-aware, parallel-safe steps.
   一个 step = 一个动作 = 2-5 分钟。可选导出 GitHub issues。

6. Implement
   Execute with superpower discipline: worktree, fresh subagent per task,
   question loop, per-task two-stage review, continuous execution,
   checkbox + run-state tracking, tests, evidence.

7. Analyze
   Check spec/plan/tasks/checklist/code/tests consistency,
   Constitution gates, Complexity Tracking, run-state.

8. Review & Finish
   Final overall review -> fresh verification ->
   structured options (merge / PR / keep / discard) -> worktree cleanup.

9. Gate
   Evaluate quality evidence and release readiness.
```

## Artifact Map

| Stage | Artifact | Suggested Path |
|---|---|---|
| Constitution | engineering rules (versioned) | `.specify/memory/constitution.md`（platform-gateway preset 见 `vibe-engineering-constitution.md`） |
| Ingest | PRD or idea source | `specs/###-<slug>/prd-source.md` |
| Trace | source mapping | `specs/###-<slug>/traceability.md` |
| State | execution state | `specs/###-<slug>/run-state.json` |
| Specify | feature spec | `specs/###-<slug>/spec.md` |
| Clarify | clarifications + coverage summary | `specs/###-<slug>/clarify.md` |
| Research | technical findings | `specs/###-<slug>/research.md` |
| Model | data model | `specs/###-<slug>/data-model.md` |
| Contracts | external interfaces | `specs/###-<slug>/contracts/` |
| Quickstart | validation scenario | `specs/###-<slug>/quickstart.md` |
| Plan | technical plan + Constitution Check + Complexity Tracking | `specs/###-<slug>/plan.md` |
| Tasks | execution plan | `specs/###-<slug>/tasks.md` or `docs/superpowers/plans/<date>-<slug>.md` |
| Checklist | requirement quality checks | `specs/###-<slug>/CHECKLIST.md` |
| Quality | test matrix | `quality/<version>/TEST_MATRIX.md` |
| Report | test report | `quality/<version>/TEST_REPORT.md` |
| Evidence | reports and artifacts | `quality/<version>/evidence/` |
| Gate | release decision | `quality/<version>/RELEASE_GATE.md` |
| Agent context | long-lived tech decisions | `CLAUDE.md` / `AGENTS.md`（auto-managed 区块） |

## Handoff Rules

- `spec.md` should answer what and why, not how. 未解决的歧义必须带 `[NEEDS CLARIFICATION]` 标记；采用的默认值必须进 Assumptions。
- `prd-source.md` should preserve the original idea/PRD input or source path.
- `traceability.md` should map `PRD-S###` rows to FR, SC, user stories, TC, tasks, evidence, or explicit out-of-scope/deferred rationale.
- `clarify.md` should preserve open questions, resolved answers, and a coverage summary; blocking `Outstanding` 项阻塞 plan。
- `research.md`, `data-model.md`, `contracts/`, and `quickstart.md` should be created before finalizing `plan.md`.
- `plan.md` must record both Constitution Check gates; violations require Complexity Tracking justification.
- `tasks.md` should be executable by an agent without rediscovering the plan; steps are single actions of 2-5 minutes.
- Superpower plans should use phases, dependency order, `[P]` parallel markers, ownership tables, checkbox steps, file paths, requirement IDs, test case IDs, test commands, expected RED/GREEN results, evidence refs, and commit points.
- `run-state.json` mirrors phase/task progress and anchors cross-session resume（见 `execution-state-and-resume.md`）。
- `CHECKLIST.md` should act as unit tests for requirement quality.
- Release gate should be independent of test execution; it reads reports and evidence and decides readiness.
- Template priority is `.specify/templates/overrides/` > `.specify/presets/templates/` > `.specify/extensions/templates/` > skill fallback.

## Prompt Pattern

When asked to create a workflow, produce:

```markdown
# <Feature> Spec Pack

## Feature Spec
...

## Technical Plan
...

## Task Plan
- [ ] Task 1 ...

## Test Matrix
...

## Release Gate
...
```

If the user wants files created, use `scripts/scaffold_vibe_feature.py` first and then fill the generated files.
