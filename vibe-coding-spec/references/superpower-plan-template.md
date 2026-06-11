# Superpower Execution Plan Template

Use this template when turning a spec-kit plan into an executable agent plan.

```markdown
# <Feature> Implementation Plan

> Agentic workers must execute this plan task-by-task. Use checkbox status and do not skip verification. Evidence before claims.

**REQUIRED EXECUTION RULE:** Before marking any task complete, run the fresh verification command in that task during the current execution session, read the output, and record the result.

## Goal

State the user-visible outcome in one paragraph.

## Architecture

Explain where the feature fits:

- Product control impact:
- Platform core impact:
- Client adapter impact:
- Provider adapter impact:
- Governance impact:

## Directory Impact

| Path | Layer | Action | Reason |
|---|---|---|---|
| `platform/domain.*` | core | modify | add neutral type |

## Spec Traceability

| Requirement | Plan Section | Task | Test Case | Evidence |
|---|---|---|---|---|
| R1 | Architecture | Task 1 | TC-001 | capture |

## Test Matrix

| Case | Stage | Evidence Type | Priority | Acceptance |
|---|---|---|---|---|
| TC-001 | contract | capture | P0 | outbound field is correct |

## Tasks

## Dependencies

- Setup before foundation.
- Foundation before user stories.
- User stories may run in parallel only when they write disjoint files and do not share interface/model ownership.
- Polish after selected user stories pass independently.

## Parallel Ownership

| Parallel Group | Agent Role | Task IDs | Owned Files | Blocked By |
|---|---|---|---|---|
| PG-001 | worker | T003 | `tests/path/test_file.py` | T001 |

## Phase 1: Setup

- [ ] T001 Create or confirm isolated worktree/branch
- [ ] T002 Confirm baseline verification command and record current result

## Phase 2: Foundation

- [ ] T003 [P] Establish shared test fixture in `tests/path/test_file.py`

## Phase 3: User Story 1 - <title> (Priority: P1)

**Goal:** Describe the user-visible slice.
**Independent Test:** Describe how to validate this story by itself.

### Task T004: <name>

**Requirement:** FR-001
**Test Case:** TC-001

**Files:**
- Modify: `path/to/file`
- Test: `path/to/test`

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function_under_test("input")
    assert result == "expected"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest path/to/test.py::test_specific_behavior -v`
Expected: FAIL because `function_under_test` does not implement FR-001 yet.

- [ ] **Step 3: Write minimal implementation**

```python
def function_under_test(value: str) -> str:
    return "expected"
```

- [ ] **Step 4: Run focused verification**

Run: `pytest path/to/test.py::test_specific_behavior -v`
Expected: PASS with 1 passed and 0 failed.

- [ ] **Step 5: Run required broader verification**

Run: `pytest path/to/test.py -v`
Expected: PASS with 0 failed.

- [ ] **Step 6: Update quality evidence**

Write evidence to `quality/<version>/evidence/tc-001.json` and ensure it proves TC-001 with positive assertions.

- [ ] **Step 7: Commit**

```bash
git add path/to/file path/to/test quality/<version>/evidence/tc-001.json
git commit -m "feat: implement <specific behavior>"
```

## Release Gate

- P0 cases:
- Evidence refs:
- Secret scan:
- Platform constraints:
- Untested scope:
```

## Execution Rules

- Each task must name exact files, requirement IDs, test case IDs, commands, and expected output.
- Each code-changing task must include RED, GREEN, evidence, and commit steps.
- Verification commands must be run fresh before any completion claim.
- A passing test that was not observed failing first does not count as a regression test.
- Keep unrelated refactors out of task execution.
- Update checkbox status as work completes.
- Store evidence under `quality/<version>/evidence/` when the task affects release confidence.
