# Spec-kit + Superpower Workflow

## Lifecycle

Use this mapping when combining spec-kit style development with superpower execution plans.

```text
0. Constitution
   Project rules, architecture principles, quality requirements.

1. Ingest
   Preserve idea or PRD source, normalize scope, create traceability.

2. Specify
   What users need and why. Avoid implementation details.

3. Clarify
   Resolve ambiguous requirements, scope, data, constraints, and non-goals.

4. Plan
   Decide architecture, research, data model, contracts, quickstart validation, test strategy, migration, and risks.

5. Tasks
   Break plan into ordered, dependency-aware, parallel-safe executable steps.

6. Implement
   Execute tasks with superpower discipline: worktree, subagents, checkbox tracking, tests, evidence.

7. Analyze
   Check spec/plan/tasks/checklist/code/tests consistency.

8. Gate
   Evaluate quality evidence and release readiness.
```

## Artifact Map

| Stage | Artifact | Suggested Path |
|---|---|---|
| Constitution | engineering rules | `.specify/memory/constitution.md`, `docs/specs/vibe-coding-directory-and-platform-spec.md`, or `AGENTS.md` |
| Ingest | PRD or idea source | `specs/###-<slug>/prd-source.md` |
| Trace | source mapping | `specs/###-<slug>/traceability.md` |
| Specify | feature spec | `specs/###-<slug>/spec.md` |
| Clarify | clarifications | `specs/###-<slug>/clarify.md` |
| Research | technical findings | `specs/###-<slug>/research.md` |
| Model | data model | `specs/###-<slug>/data-model.md` |
| Contracts | external interfaces | `specs/###-<slug>/contracts/` |
| Quickstart | validation scenario | `specs/###-<slug>/quickstart.md` |
| Plan | technical plan | `specs/###-<slug>/plan.md` |
| Tasks | execution plan | `specs/###-<slug>/tasks.md` or `docs/superpowers/plans/<date>-<slug>.md` |
| Checklist | requirement quality checks | `specs/###-<slug>/CHECKLIST.md` |
| Quality | test matrix | `quality/<version>/TEST_MATRIX.md` |
| Report | test report | `quality/<version>/TEST_REPORT.md` |
| Evidence | reports and artifacts | `quality/<version>/evidence/` |
| Gate | release decision | `quality/<version>/RELEASE_GATE.md` |

## Handoff Rules

- `spec.md` should answer what and why, not how.
- `prd-source.md` should preserve the original idea/PRD input or source path.
- `traceability.md` should map `PRD-S###` rows to FR, SC, user stories, TC, tasks, evidence, or explicit out-of-scope/deferred rationale.
- `clarify.md` should preserve open questions and resolved answers that changed the spec, plan, or tasks.
- `research.md`, `data-model.md`, `contracts/`, and `quickstart.md` should be created before finalizing `plan.md`.
- `plan.md` should explain architecture, file ownership, research decisions, data model, contracts, and validation path.
- `tasks.md` should be executable by an agent without rediscovering the plan.
- Superpower plans should use phases, dependency order, `[P]` parallel markers, ownership tables, checkbox steps, file paths, requirement IDs, test case IDs, test commands, expected RED/GREEN results, evidence refs, and commit points.
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
