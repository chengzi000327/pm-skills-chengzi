# Superpower Execution Plan Template

Use this template when turning a spec-kit plan into an executable agent plan.

## 写作姿态

写 plan 时假设执行者是：**熟练的开发者，但对本代码库零上下文，且品味存疑**。

- 写清楚每个任务碰哪些文件、参考哪些文档、怎么测试。
- 不要假设执行者知道项目惯例、工具链或领域知识——写出来。
- 不要假设执行者会做好的测试设计——把测试代码直接写进任务。

## 前置决策（写任务之前完成）

### 1. Constitution Check（GATE，research 之前做第一次）

对照项目 constitution（`.specify/memory/constitution.md` 或 `references/constitution-template.md` 生成的文件）逐条检查方案：

- 通过：在 plan 里记录 "Constitution Check (pre-research): PASS"。
- 违反任意一条：必须在 Complexity Tracking 表登记，否则不得继续。

### 2. File Structure（分解决策先锁定）

在拆任务之前，先列出会新建或修改的所有文件及各自职责。分解决策在这里锁定，不在写任务时临时发挥：

- 每个文件一个清晰职责，边界和接口明确。
- 一起变化的代码放在一起；按职责拆分，不按技术层拆分。
- 已有代码库遵循既有模式；不要顺手做无关重构。

### 3. Constitution Check（GATE，设计完成后做第二次）

data-model、contracts、File Structure 定稿后再查一次 constitution。设计阶段引入的新违规同样进 Complexity Tracking。

## 任务粒度规则

- **一个 step = 一个动作 = 2-5 分钟**。"写失败测试"是一个 step，"运行确认失败"是另一个 step。
- 一个 task 由 5-8 个 step 组成（RED/GREEN/验证/evidence/commit）。
- 超过 5 分钟的 step 必须再拆。
- 每个 step 都有明确的命令和预期输出，执行者不需要做任何决策。

## 模板

```markdown
# <Feature> Implementation Plan

> Agentic workers must execute this plan task-by-task. Use checkbox status and do not skip verification. Evidence before claims.

**REQUIRED EXECUTION RULE:** Before marking any task complete, run the fresh verification command in that task during the current execution session, read the output, and record the result.

## Goal

State the user-visible outcome in one paragraph.

## Constitution Check

| Gate | Result | Date | Notes |
|---|---|---|---|
| Pre-research | PASS / VIOLATIONS | YYYY-MM-DD | |
| Post-design | PASS / VIOLATIONS | YYYY-MM-DD | |

## Complexity Tracking

> 只在 Constitution Check 发现违规时填写。没有书面辩护的违规 = analyze CRITICAL。

| Violation | Constitution Rule | Why Needed for This Feature | Simpler Alternative Rejected Because |
|---|---|---|---|
| 引入第二个 ORM | "one persistence layer" | 旧模块迁移期间共存 | 一次性迁移风险超出本期范围 |

## Architecture

Explain where the feature fits:

- Product control impact:
- Platform core impact:
- Client adapter impact:
- Provider adapter impact:
- Governance impact:

## File Structure

| Path | New/Modify | Responsibility |
|---|---|---|
| `src/feature/handler.py` | new | request handling only |

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

Write evidence to `specs/<feature>/evidence/tc-001.json` and ensure it proves TC-001 with positive assertions.

- [ ] **Step 7: Commit**

```bash
git add path/to/file path/to/test specs/<feature>/evidence/tc-001.json
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
- Each step is one action of 2-5 minutes; split anything bigger.
- Verification commands must be run fresh before any completion claim.
- A passing test that was not observed failing first does not count as a regression test.
- Keep unrelated refactors out of task execution.
- Update checkbox status as work completes; mirror progress into `run-state.json`（见 `execution-state-and-resume.md`）。
- Store evidence under `specs/<feature>/evidence/` when the task affects release confidence.
- Constitution Check 两个 gate 都未记录结果的 plan 不允许进入 tasks。
