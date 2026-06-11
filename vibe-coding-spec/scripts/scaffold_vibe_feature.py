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
    args = parser.parse_args()

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
    quality_dir = root / "quality" / args.version
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

    if prd_path:
        source_preview = prd_text[:MAX_SOURCE_PREVIEW_CHARS]
        truncated = "\n\n> Source truncated in this artifact. Keep the original PRD file as source of truth." if len(prd_text) > MAX_SOURCE_PREVIEW_CHARS else ""
        write_if_missing(feature_dir / "prd-source.md", render_template(root, "prd-source.md", context, f"""# {feature_name} PRD Source

**Feature Branch**: `{branch}`
**Original PRD**: `{prd_source_rel}`

## Source Index

| Source ID | Section | Normalized Into | Notes |
|---|---|---|---|
{prd_index_rows}

## Original PRD Snapshot

```markdown
{source_preview}
```
{truncated}
"""))
    else:
        write_if_missing(feature_dir / "prd-source.md", render_template(root, "prd-source.md", context, f"""# {feature_name} PRD Source

**Feature Branch**: `{branch}`
**Original PRD**: Idea input only

## Source Index

| Source ID | Section | Normalized Into | Notes |
|---|---|---|---|
| PRD-S001 | Idea input | spec.md | Expand through clarify before planning |
"""))

    write_if_missing(feature_dir / "traceability.md", render_template(root, "traceability.md", context, f"""# {feature_name} Traceability

**Feature Branch**: `{branch}`
**Source**: `specs/{branch}/prd-source.md`

## PRD to Delivery Map

| Source ID | PRD Section | Requirement | User Story | Test Case | Task | Status |
|---|---|---|---|---|---|---|
{prd_section_rows}

## Coverage Rules

- Every PRD-S row must map to one or more FR, SC, non-goal, assumption, or explicit out-of-scope note.
- P0 PRD sections must map to at least one TC and evidence ref.
- Any unmapped PRD section must be marked `out-of-scope`, `duplicate`, or `deferred` with rationale.
"""))

    write_if_missing(feature_dir / "spec.md", render_template(root, "spec.md", context, f"""# Feature Specification: {feature_name}

**Feature Branch**: `{branch}`
**Status**: Draft
**Input**: {"PRD source: `" + prd_source_rel + "`" if prd_path else "User description: \"" + feature_name + "\""}

## Source Normalization

| Source | Traceability |
|---|---|
| `specs/{branch}/prd-source.md` | `specs/{branch}/traceability.md` |

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

    write_if_missing(feature_dir / "clarify.md", render_template(root, "clarify.md", context, f"""# {feature_name} Clarifications

**Feature Branch**: `{branch}`

## Open Questions

Ask at most five questions per clarify pass. Block planning only when the answer changes data model, security/privacy, irreversible UX behavior, external contracts, release gate criteria, or P0 acceptance.

- [ ] Q1: TODO

## Blocking Questions

- TODO

## PRD-Derived Ambiguities

| Source ID | Ambiguity | Blocking? | Proposed Handling |
|---|---|---|---|
| PRD-S001 | TODO | yes | Ask before plan |

## Resolved Clarifications

| Date | Question | Answer | Impacted Artifact |
|---|---|---|---|
"""))

    write_if_missing(feature_dir / "research.md", render_template(root, "research.md", context, f"""# {feature_name} Research

**Feature Branch**: `{branch}`

## Research Questions

| ID | Question | Owner | Status | Decision Impact |
|---|---|---|---|---|
| RQ-001 | TODO | explorer | open | plan.md |

## Decisions

| Topic | Decision | Rationale | Alternatives Rejected |
|---|---|---|---|
| TODO | TODO | TODO | TODO |

## External References

- TODO
"""))

    write_if_missing(feature_dir / "data-model.md", render_template(root, "data-model.md", context, f"""# {feature_name} Data Model

**Feature Branch**: `{branch}`

## Entities

### TODO

- Purpose: TODO
- Fields:
  - `id`: TODO
- Relationships: TODO
- Validation: TODO

## State Transitions

| Entity | From | To | Trigger | Guard |
|---|---|---|---|---|
| TODO | TODO | TODO | TODO | TODO |
"""))

    write_if_missing(feature_dir / "contracts" / "README.md", render_template(root, "contracts/README.md", context, f"""# {feature_name} Contracts

**Feature Branch**: `{branch}`

Define external API, event, CLI, file, or adapter contracts before implementation.

## Contract Inventory

| Contract | Requirement | Producer | Consumer | Evidence |
|---|---|---|---|---|
| TODO | FR-001 | TODO | TODO | TC-001 |

## Compatibility Notes

- TODO
"""))

    write_if_missing(feature_dir / "quickstart.md", render_template(root, "quickstart.md", context, f"""# {feature_name} Quickstart

**Feature Branch**: `{branch}`

## Prerequisites

- TODO

## Run

```bash
TODO
```

## Validate

| Step | Command | Expected |
|---|---|---|
| 1 | `TODO` | TODO |
"""))

    write_if_missing(feature_dir / "CHECKLIST.md", render_template(root, "CHECKLIST.md", context, f"""# {feature_name} Requirement Checklist

**Feature Branch**: `{branch}`

## Spec Quality

- [ ] PRD source is preserved in `prd-source.md`
- [ ] PRD sections are mapped in `traceability.md`
- [ ] No unresolved `TODO`, `TBD`, or `NEEDS CLARIFICATION`
- [ ] User stories are independently testable
- [ ] Acceptance scenarios use Given/When/Then
- [ ] Success criteria are measurable

- [ ] Remaining `[NEEDS CLARIFICATION]` markers are zero before plan
- [ ] Assumptions and edge cases are explicitly recorded

## Plan Quality

- [ ] Constitution Check passed at both gates (pre-research, post-design)
- [ ] All constitution violations are justified in Complexity Tracking

- [ ] Architecture impact covers product control, platform core, client adapters, provider adapters, and governance
- [ ] Directory impact names exact paths
- [ ] Research decisions are captured in `research.md`
- [ ] Data model entities are captured in `data-model.md`
- [ ] Contracts are captured in `contracts/`

## Task Quality

- [ ] Tasks are grouped by setup, foundation, user story, and polish phases
- [ ] Parallel tasks are marked `[P]`
- [ ] Each code-changing task includes RED/GREEN verification
- [ ] Each P0 requirement maps to a test case and evidence ref
"""))

    write_if_missing(feature_dir / "plan.md", render_template(root, "plan.md", context, f"""# Implementation Plan: {feature_name}

**Branch**: `{branch}` | **Spec**: `specs/{branch}/spec.md`

## Summary

TODO

## PRD Traceability

Source: `specs/{branch}/prd-source.md`
Map: `specs/{branch}/traceability.md`

- P0 source sections: TODO
- Deferred source sections: TODO

## Technical Context

- Language/Version: TODO
- Primary Dependencies: TODO
- Storage: TODO
- Testing: TODO
- Target Platform: TODO

## Research

Source: `specs/{branch}/research.md`

- Decisions: TODO
- Open risks: TODO

## Data Model

Source: `specs/{branch}/data-model.md`

- Entities: TODO
- State transitions: TODO

## Contracts

Source: `specs/{branch}/contracts/`

- External interfaces: TODO

## Quickstart

Source: `specs/{branch}/quickstart.md`

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
"""))

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

- [ ] **Step 5: Update quality evidence**

Evidence: `quality/{args.version}/evidence/TODO`

- [ ] **Step 6: Run broader verification**

Run: `pytest test/path/to/test_file.py -v`
Expected: PASS with 0 failed.

- [ ] **Step 7: Commit**

```bash
git add TODO
git commit -m "feat: TODO"
```

## Phase N: Polish and Release Evidence

- [ ] T999 Run `python3 vibe-coding-spec/scripts/check_vibe_structure.py --root . --feature {branch} --version {args.version}`
- [ ] T998 Update `quality/{args.version}/RELEASE_GATE.md` with fresh verification evidence
"""))

    write_if_missing(quality_dir / "TEST_MATRIX.md", render_template(root, "TEST_MATRIX.md", context, f"""# {args.version} Test Matrix

| Case | Requirement | Capability | Stage | Evidence Type | Priority | Acceptance | Evidence Ref |
|---|---|---|---|---|---|---|---|
| TC-001 | FR-001 | TODO | contract | capture | P0 | TODO | quality/{args.version}/evidence/tc-001.json |
"""))

    write_if_missing(quality_dir / "TEST_REPORT.md", render_template(root, "TEST_REPORT.md", context, f"""# {args.version} Test Report

## Summary

- Commit:
- Branch:
- Platform:
- Result:

## Cases

| Case | Status | Evidence |
|---|---|---|
"""))

    write_if_missing(quality_dir / "RELEASE_GATE.md", render_template(root, "RELEASE_GATE.md", context, f"""# {args.version} Release Gate

- [ ] Worktree clean
- [ ] Required platform reports present
- [ ] P0 cases pass
- [ ] PASS cases have positive assertions
- [ ] Evidence refs are readable
- [ ] Fresh verification commands were run before completion claims
- [ ] Secret scan passed
- [ ] Untested scope documented
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

    write_if_missing(root / ".specify" / "extensions.yml", render_template(root, "extensions.yml", context, """# Optional extension hooks.
# Hooks are advisory unless optional is false.
hooks:
  before_analyze: []
  after_analyze: []
  before_implement: []
  after_implement: []
"""))

    write_if_missing(feature_dir / "checklists" / "README.md", render_template(root, "checklists/README.md", context, f"""# {feature_name} Requirement Quality Checklists

Domain checklists generated per `checklist-authoring-workflow.md`.
Items are questions about requirement quality (CHK-numbered, dimension-tagged, traceable),
never implementation tests.

| File | Focus | Depth | Items |
|---|---|---|---|
| (none yet) | | | |
"""))

    (quality_dir / "evidence").mkdir(parents=True, exist_ok=True)
    (root / ".specify" / "templates" / "overrides").mkdir(parents=True, exist_ok=True)
    (root / ".specify" / "presets" / "templates").mkdir(parents=True, exist_ok=True)
    (root / ".specify" / "extensions" / "templates").mkdir(parents=True, exist_ok=True)
    print(f"Created feature spec pack: {feature_dir}")
    print(f"Feature branch name: {branch}")
    print(f"Created quality pack: {quality_dir}")
    print("Template priority: .specify/templates/overrides/ > .specify/presets/templates/ > .specify/extensions/templates/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
