#!/usr/bin/env python3
"""Scaffold a vibe-coding feature spec pack."""
from __future__ import annotations

import argparse
import datetime
import json
import re
from pathlib import Path


MAX_SOURCE_PREVIEW_CHARS = 12000


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "feature"


def title_from_prd(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            title = stripped.lstrip("#").strip()
            if title:
                return title
    return path.stem.replace("-", " ").replace("_", " ").strip().title() or "PRD Feature"


def extract_prd_sections(text: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        heading = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading:
            title = heading.group(2).strip()
            if title:
                sections.append((f"PRD-S{len(sections) + 1:03d}", title))
        if len(sections) >= 30:
            break
    if not sections:
        sections.append(("PRD-S001", "Whole PRD"))
    return sections


def write_if_missing(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(text, encoding="utf-8")


def next_feature_number(root: Path) -> int:
    specs_dir = root / "specs"
    highest = 0
    if specs_dir.exists():
        for child in specs_dir.iterdir():
            if not child.is_dir():
                continue
            match = re.match(r"^(\d+)-", child.name)
            if match:
                highest = max(highest, int(match.group(1)))
    return highest + 1


def render_template(root: Path, template_name: str, context: dict[str, str], fallback: str) -> str:
    template_roots = [
        root / ".specify" / "templates" / "overrides",
        root / ".specify" / "presets" / "templates",
        root / ".specify" / "extensions" / "templates",
    ]
    text = fallback
    for template_root in template_roots:
        candidate = template_root / template_name
        if candidate.exists():
            text = candidate.read_text(encoding="utf-8")
            break
    for key, value in context.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument("--name", help="Feature name")
    parser.add_argument("--prd", help="Path to an existing PRD markdown/text file")
    parser.add_argument("--version", default="V0.1", help="Quality version folder")
    parser.add_argument("--number", type=int, help="Feature number override")
    parser.add_argument("--full", action="store_true", help="Create the full governance pack instead of the lightweight default")
    parser.add_argument("--audit", action="store_true", help="Create compact SDD plus a release audit pack")
    args = parser.parse_args()
    full = args.full or args.audit

    root = Path(args.root).resolve()
    prd_path = Path(args.prd).resolve() if args.prd else None
    if prd_path and not prd_path.exists():
        parser.error(f"PRD file not found: {prd_path}")
    feature_name = args.name or (title_from_prd(prd_path) if prd_path else None)
    if not feature_name:
        parser.error("--name is required when --prd is not provided")

    prd_text = prd_path.read_text(encoding="utf-8") if prd_path else ""
    prd_sections = extract_prd_sections(prd_text) if prd_text else []
    prd_source_rel = str(prd_path.relative_to(root)) if prd_path and prd_path.is_relative_to(root) else str(prd_path) if prd_path else "N/A"

    slug = slugify(feature_name)
    number = args.number if args.number is not None else next_feature_number(root)
    branch = f"{number:03d}-{slug}"
    feature_dir = root / "specs" / branch
    evidence_dir = feature_dir / "evidence"
    audit_dir = feature_dir / "audit"
    context = {
        "FEATURE_NAME": feature_name,
        "FEATURE_SLUG": slug,
        "FEATURE_NUMBER": f"{number:03d}",
        "FEATURE_BRANCH": branch,
        "QUALITY_VERSION": args.version,
        "PRD_SOURCE": prd_source_rel,
    }

    prd_section_rows = "\n".join(
        f"| {section_id} | {title} | TODO | TODO | TODO | TODO | open |"
        for section_id, title in prd_sections
    ) or "| PRD-S001 | Idea input | FR-001 | US1 | TC-001 | T004 | draft |"

    prd_index_rows = "\n".join(
        f"| {section_id} | {title} | TODO | TODO |"
        for section_id, title in prd_sections
    ) or "| PRD-S001 | Idea input | TODO | TODO |"

    source_preview = prd_text[:MAX_SOURCE_PREVIEW_CHARS]
    truncated = "\n\n> Source truncated in this artifact. Keep the original PRD file as source of truth." if len(prd_text) > MAX_SOURCE_PREVIEW_CHARS else ""
    source_section = ""
    if prd_path:
        source_section = f"""
## Source

**Original PRD**: `{prd_source_rel}`

### Source Index

| Source ID | Section | Normalized Into | Notes |
|---|---|---|---|
{prd_index_rows}

### Traceability

| Source ID | PRD Section | Requirement | User Story | Test Case | Task | Status |
|---|---|---|---|---|---|---|
{prd_section_rows}

### Coverage Rules

- Every PRD-S row must map to one or more FR, SC, non-goal, assumption, or explicit out-of-scope note.
- P0 PRD sections must map to at least one TC and evidence ref.
- Any unmapped PRD section must be marked `out-of-scope`, `duplicate`, or `deferred` with rationale.

### Original PRD Snapshot

```markdown
{source_preview}
```
{truncated}
"""

    write_if_missing(feature_dir / "spec.md", render_template(root, "spec.md", context, f"""# Feature Specification: {feature_name}

**Feature Branch**: `{branch}`
**Status**: Draft
**Input**: {"PRD source: `" + prd_source_rel + "`" if prd_path else "User description: \"" + feature_name + "\""}
{source_section}

## Scope

- In scope: TODO
- Out of scope: TODO
- Assumptions: TODO
- Conflicts: TODO

## User Scenarios & Testing

### User Story 1 - TODO (Priority: P1)

TODO: Describe the independently testable user journey.

**Why this priority**: TODO

**Independent Test**: TODO

**Acceptance Scenarios**:

1. **Given** TODO, **When** TODO, **Then** TODO

### Edge Cases

- What happens when TODO?
- What happens when TODO fails midway?

## Requirements

### Functional Requirements

- **FR-001**: TODO [NEEDS CLARIFICATION: replace with the real requirement; keep this marker on any FR written with unresolved ambiguity]

### Key Entities

- TODO

## Success Criteria

- **SC-001**: TODO

## Assumptions

- TODO (record reasonable defaults adopted where the source description lacked specificity)
"""))

    if full:
        plan_body = f"""# Implementation Plan: {feature_name}

**Branch**: `{branch}` | **Spec**: `specs/{branch}/spec.md`

## Summary

TODO

## Technical Context

- Language/Version: TODO
- Primary Dependencies: TODO
- Storage: TODO
- Testing: TODO
- Target Platform: TODO

## Research

- Decisions: TODO
- Open risks: TODO

## Data Model

- Entities: TODO
- State transitions: TODO

## Contracts

- External interfaces: TODO

## Quickstart

- Validation path: TODO

## Constitution Check

| Gate | Result | Date | Notes |
|---|---|---|---|
| Pre-research | TODO | TODO | |
| Post-design | TODO | TODO | |

- [ ] Project constitution rules are respected (boundaries, testing, dependency policy)
- [ ] P0 behavior has test matrix coverage
- [ ] Evidence type is identified for each P0 case

## Complexity Tracking

> Fill only when a Constitution Check gate reports violations. Unjustified violations block analyze.

| Violation | Constitution Rule | Why Needed for This Feature | Simpler Alternative Rejected Because |
|---|---|---|---|

## Architecture Impact

- Product control impact:
- Platform core impact:
- Client adapter impact:
- Provider adapter impact:
- Governance impact:

## Directory Impact

| Path | Layer | Action | Reason |
|---|---|---|---|

## Test Strategy

- Unit:
- Contract/capture:
- True integration:

## Risks

- TODO
"""
    else:
        plan_body = f"""# Implementation Plan: {feature_name}

**Branch**: `{branch}` | **Spec**: `specs/{branch}/spec.md`

## Summary

TODO

## Technical Context

- Language/Version: TODO
- Primary Dependencies: TODO
- Testing: TODO

## Scope Decisions

- In scope: TODO
- Out of scope: TODO
- Assumptions: TODO

## Implementation Approach

- Files affected: TODO
- Data or contract impact: TODO
- Rollback plan: TODO

## Verification

- Baseline command: TODO
- Focused command: TODO
- Final command: TODO

## Risks

- TODO
"""
    write_if_missing(feature_dir / "plan.md", render_template(root, "plan.md", context, plan_body))

    write_if_missing(feature_dir / "tasks.md", render_template(root, "tasks.md", context, f"""# {feature_name} Implementation Plan

> Agentic workers must execute this plan task-by-task. Do not skip verification. Evidence before claims.

**Goal:** TODO

**Architecture:** TODO

**Tech Stack:** TODO

---

## Dependencies

- Setup before foundation.
- Foundation before any user story.
- User stories may run in parallel only when they write disjoint files and do not share interface/model ownership.
- Polish after selected user stories pass independently.

## Parallel Ownership

| Parallel Group | Agent Role | Task IDs | Owned Files | Blocked By |
|---|---|---|---|---|
| PG-001 | worker | T003 | `test/path/to/test_file.py` | T001 |

## Phase 1: Setup

- [ ] T001 Create or confirm isolated worktree/branch for `{branch}`
- [ ] T002 Confirm baseline verification command and record current result

## Phase 2: Foundation

- [ ] T003 [P] Establish shared test fixture in `test/path/to/test_file.py`

## Phase 3: User Story 1 - TODO (Priority: P1)

**Goal:** TODO
**Independent Test:** TODO

### Task T004: TODO

**Requirement:** FR-001
**Test Case:** TC-001

**Files:**
- Modify: `src/path/to/file.py`
- Test: `test/path/to/test_file.py`

- [ ] **Step 1: Write the failing test**

```text
TODO: Include exact test code or command input.
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest test/path/to/test_file.py::test_specific_behavior -v`
Expected: FAIL because TODO

- [ ] **Step 3: Write minimal implementation**

```text
TODO: Include exact implementation change or precise edit instructions.
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest test/path/to/test_file.py::test_specific_behavior -v`
Expected: PASS

- [ ] **Step 5: Run broader verification**

Run: `pytest test/path/to/test_file.py -v`
Expected: PASS with 0 failed.

- [ ] **Step 6: Commit**

```bash
git add TODO
git commit -m "feat: TODO"
```

## Phase N: Final Verification

- [ ] T999 Run `python3 vibe-coding-spec/scripts/check_vibe_structure.py --root . --feature {branch} --version {args.version}`
"""))

    if full:
        write_if_missing(feature_dir / "review.md", render_template(root, "review.md", context, f"""# Review and Release Gate: {feature_name}

**Feature Branch**: `{branch}`

## Clarifications

Ask at most five questions per clarify pass. Block planning only when the answer changes data model, security/privacy, irreversible UX behavior, external contracts, release gate criteria, or P0 acceptance.

### Open Questions

- [ ] Q1: TODO

### Resolved Clarifications

| Date | Question | Answer | Impacted Artifact |
|---|---|---|---|

## Checklist

### Spec Quality

- [ ] No unresolved `TODO`, `TBD`, or `NEEDS CLARIFICATION`
- [ ] User stories are independently testable
- [ ] Acceptance scenarios use Given/When/Then
- [ ] Success criteria are measurable
- [ ] Assumptions and edge cases are explicitly recorded

### Plan Quality

- [ ] Constitution Check passed at both gates when required
- [ ] All constitution violations are justified in Complexity Tracking
- [ ] Research, data model, contracts, and quickstart decisions are captured in `plan.md`
- [ ] Directory impact names exact paths

### Task Quality

- [ ] Tasks are grouped by setup, foundation, user story, and polish phases
- [ ] Parallel tasks are marked `[P]`
- [ ] Each code-changing task includes RED/GREEN verification
- [ ] Each P0 requirement maps to a test case and evidence ref

## Test Matrix

| Case | Requirement | Capability | Stage | Evidence Type | Priority | Acceptance | Evidence Ref |
|---|---|---|---|---|---|---|---|
| TC-001 | FR-001 | TODO | contract | capture | P0 | TODO | specs/{branch}/evidence/tc-001.json |

## Summary

- Commit:
- Branch:
- Platform:
- Result:

## Cases

| Case | Status | Evidence |
|---|---|---|

## Release Gate

- [ ] Worktree clean
- [ ] Required platform reports present
- [ ] P0 cases pass
- [ ] PASS cases have positive assertions
- [ ] Evidence refs are readable
- [ ] Fresh verification commands were run before completion claims
- [ ] Secret scan passed
- [ ] Untested scope documented
"""))

    if args.audit:
        write_if_missing(audit_dir / "traceability.md", render_template(root, "audit/traceability.md", context, f"""# Audit Traceability: {feature_name}

**Feature Branch**: `{branch}`

## Requirement to Evidence Map

| Source | Requirement | Success Criteria | Task | Test Case | Evidence | Status |
|---|---|---|---|---|---|---|
| PRD-S001 | FR-001 | SC-001 | T004 | TC-001 | specs/{branch}/evidence/tc-001.json | open |

## Coverage Rules

- Every P0/P1 requirement must map to a task, test case, and evidence ref.
- Any unmapped requirement must be explicitly marked `deferred`, `duplicate`, or `out-of-scope` with rationale.
"""))

        write_if_missing(audit_dir / "test-matrix.md", render_template(root, "audit/test-matrix.md", context, f"""# Audit Test Matrix: {feature_name}

**Feature Branch**: `{branch}`

| Case | Requirement | Stage | Evidence Type | Priority | Acceptance | Evidence Ref | Status |
|---|---|---|---|---|---|---|---|
| TC-001 | FR-001 | contract | capture | P0 | TODO | specs/{branch}/evidence/tc-001.json | open |
"""))

        write_if_missing(audit_dir / "release-gate.md", render_template(root, "audit/release-gate.md", context, f"""# Audit Release Gate: {feature_name}

**Feature Branch**: `{branch}`

## Decision

- Status: BLOCKED
- Decider:
- Date:

## Gate Checks

- [ ] P0 cases pass with readable evidence
- [ ] PASS cases include positive assertions
- [ ] Security/privacy risks reviewed
- [ ] Rollback or mitigation path documented
- [ ] Untested scope documented
- [ ] Waivers have owner, expiry, and rationale
"""))

        write_if_missing(audit_dir / "decision-log.md", render_template(root, "audit/decision-log.md", context, f"""# Audit Decision Log: {feature_name}

**Feature Branch**: `{branch}`

| Date | Decision | Context | Alternatives Rejected | Owner | Evidence |
|---|---|---|---|---|---|
| TODO | TODO | TODO | TODO | TODO | TODO |

## Waivers

| Waiver | Reason | Owner | Expiry | Compensating Control |
|---|---|---|---|---|
"""))

    run_state_path = feature_dir / "run-state.json"
    if not run_state_path.exists():
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        run_state = {
            "feature": branch,
            "version": args.version,
            "phase": "ingest" if prd_path else "specify",
            "phaseHistory": ["ingest"] if prd_path else [],
            "lastCompletedTask": None,
            "inProgressTask": None,
            "blocked": False,
            "blockedReason": None,
            "lastVerification": None,
            "constitutionCheck": {"preResearch": None, "postDesign": None},
            "clarify": {"openBlocking": 0, "openNonBlocking": 0},
            "worktree": None,
            "updatedAt": now,
        }
        run_state_path.parent.mkdir(parents=True, exist_ok=True)
        run_state_path.write_text(json.dumps(run_state, indent=2) + "\n", encoding="utf-8")

    if full:
        evidence_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created {'audit' if args.audit else 'full' if args.full else 'lightweight'} feature spec pack: {feature_dir}")
    print(f"Feature branch name: {branch}")
    if full:
        print(f"Created review file: {feature_dir / 'review.md'}")
        print(f"Created evidence directory: {evidence_dir}")
    if args.audit:
        print(f"Created audit pack: {audit_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
