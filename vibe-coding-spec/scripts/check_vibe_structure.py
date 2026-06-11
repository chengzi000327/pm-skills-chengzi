#!/usr/bin/env python3
"""Check vibe-coding structure and analyze spec/plan/tasks/test coverage."""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path


RECOMMENDED_DIRS = [
    "src",
    "platform",
    "platform/clients",
    "platform/providers",
    "scripts/certification",
    "test",
    "specs",
]

PLACEHOLDER_RE = re.compile(r"\b(TODO|TBD|TKTK|FIXME|NEEDS CLARIFICATION)\b|<[^>]+>|\?\?\?", re.I)
REQ_RE = re.compile(r"\b(?:FR|R|SC)-?\d{3}\b", re.I)
CASE_RE = re.compile(r"\bTC-\d{3}\b", re.I)
TASK_RE = re.compile(r"^\s*-\s+\[[ xX]\]\s+(?:\*\*)?(T\d{3}(?!\d)|Step\s+\d+|Task\s+\d+)", re.M)
FILE_REF_RE = re.compile(r"`([^`]+\.[A-Za-z0-9]+(?::\d+(?:-\d+)?)?)`")
AMBIGUOUS_RE = re.compile(
    r"\b(fast|scalable|secure|intuitive|robust|simple|easy|performant|reliable|seamless)\b"
    r"|高效|稳定|易用|安全|灵活|完善|尽快|快速|智能|自动|优化|提升体验|体验好|可扩展|高质量|丝滑|简单",
    re.I,
)
MUST_RE = re.compile(r"\b(MUST|SHALL|REQUIRED|必须|不得|禁止)\b")
PRD_SOURCE_RE = re.compile(r"\bPRD-S\d{3}\b")


@dataclass
class Finding:
    id: str
    category: str
    severity: str
    location: str
    summary: str
    recommendation: str


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def first_existing(canonical: Path, *legacy: Path) -> Path:
    if canonical.exists():
        return canonical
    for path in legacy:
        if path.exists():
            return path
    return canonical


def extract_ids(pattern: re.Pattern[str], text: str) -> set[str]:
    return {match.group(0).upper().replace("R-", "R-") for match in pattern.finditer(text)}


def line_for(text: str, needle: str) -> int:
    for idx, line in enumerate(text.splitlines(), start=1):
        if needle in line:
            return idx
    return 1


def normalized_requirement_lines(text: str) -> dict[str, list[tuple[int, str]]]:
    results: dict[str, list[tuple[int, str]]] = {}
    for idx, line in enumerate(text.splitlines(), start=1):
        req_match = REQ_RE.search(line)
        if not req_match:
            continue
        req_prefix = req_match.group(0).split("-")[0].upper()
        normalized = REQ_RE.sub("", line.lower())
        normalized = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", normalized).strip()
        if normalized:
            results.setdefault(f"{req_prefix}:{normalized}", []).append((idx, line.strip()))
    return results


def discover_constitution(root: Path) -> Path | None:
    candidates = [
        root / ".specify" / "memory" / "constitution.md",
        root / "docs" / "specs" / "vibe-coding-directory-and-platform-spec.md",
        root / "AGENTS.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def summarize_hooks(root: Path) -> dict[str, object]:
    path = root / ".specify" / "extensions.yml"
    if not path.exists():
        return {"path": None, "before_analyze": 0, "after_analyze": 0}
    text = read(path)
    return {
        "path": str(path.relative_to(root)),
        "before_analyze": len(re.findall(r"before_analyze:|hooks\.before_analyze", text)),
        "after_analyze": len(re.findall(r"after_analyze:|hooks\.after_analyze", text)),
        "disabled": len(re.findall(r"enabled:\s*false", text, re.I)),
    }


def template_layer_summary(root: Path) -> dict[str, int]:
    layers = {
        "overrides": root / ".specify" / "templates" / "overrides",
        "presets": root / ".specify" / "presets" / "templates",
        "extensions": root / ".specify" / "extensions" / "templates",
    }
    return {
        name: len([p for p in path.rglob("*") if p.is_file()]) if path.exists() else 0
        for name, path in layers.items()
    }


def find_latest_feature(root: Path) -> Path | None:
    specs = root / "specs"
    if not specs.exists():
        return None
    candidates = [p for p in specs.iterdir() if p.is_dir() and re.match(r"^\d+-", p.name)]
    if not candidates:
        return None
    return sorted(candidates, key=lambda p: p.name)[-1]


def resolve_feature(root: Path, feature: str | None) -> Path | None:
    if feature:
        path = Path(feature)
        if not path.is_absolute():
            path = root / feature
        if path.exists():
            return path
        specs_path = root / "specs" / feature
        if specs_path.exists():
            return specs_path
        matches = sorted((root / "specs").glob(f"*-{feature}")) if (root / "specs").exists() else []
        return matches[-1] if matches else None
    return find_latest_feature(root)


def add_finding(findings: list[Finding], category: str, severity: str, location: str, summary: str, recommendation: str) -> None:
    prefixes = {
        "ambiguity": "A",
        "constitution": "CN",
        "coverage": "CV",
        "duplication": "D",
        "evidence": "E",
        "lifecycle": "L",
        "missing": "M",
        "parallel": "PA",
        "placeholder": "PH",
        "prd": "PRD",
        "structure": "S",
        "task": "T",
        "tdd": "TD",
        "verification": "V",
    }
    prefix = prefixes.get(category, category[:3].upper())
    count = sum(1 for finding in findings if finding.category == category) + 1
    findings.append(Finding(f"{prefix}{count}", category, severity, location, summary, recommendation))


def analyze_artifacts(root: Path, feature_dir: Path | None, quality_version: str, profile: str = "auto") -> tuple[list[Finding], dict[str, object]]:
    findings: list[Finding] = []
    if feature_dir is None:
        add_finding(
            findings,
            "missing",
            "CRITICAL",
            "specs/",
            "No numbered feature directory found.",
            "Run scaffold_vibe_feature.py to create specs/###-feature artifacts.",
        )
        return findings, {}

    review_dir = feature_dir / "review"
    legacy_quality_dir = root / "quality" / quality_version
    audit_dir = feature_dir / "audit"
    artifacts = {
        "prd_source": first_existing(feature_dir / "source" / "prd.md", feature_dir / "prd-source.md"),
        "traceability": first_existing(feature_dir / "source" / "traceability.md", feature_dir / "traceability.md"),
        "spec": feature_dir / "spec.md",
        "review": feature_dir / "review.md",
        "clarify": first_existing(feature_dir / "review.md", review_dir / "clarify.md", feature_dir / "clarify.md"),
        "research": first_existing(feature_dir / "plan.md", feature_dir / "design" / "research.md", feature_dir / "research.md"),
        "data_model": first_existing(feature_dir / "plan.md", feature_dir / "design" / "data-model.md", feature_dir / "data-model.md"),
        "contracts": first_existing(feature_dir / "plan.md", feature_dir / "design" / "contracts.md", feature_dir / "contracts" / "README.md"),
        "quickstart": first_existing(feature_dir / "plan.md", feature_dir / "design" / "quickstart.md", feature_dir / "quickstart.md"),
        "checklist": first_existing(feature_dir / "review.md", review_dir / "checklist.md", feature_dir / "CHECKLIST.md"),
        "plan": feature_dir / "plan.md",
        "tasks": feature_dir / "tasks.md",
        "matrix": first_existing(feature_dir / "review.md", review_dir / "test-matrix.md", legacy_quality_dir / "TEST_MATRIX.md"),
        "gate": first_existing(feature_dir / "review.md", review_dir / "release-gate.md", legacy_quality_dir / "RELEASE_GATE.md"),
        "audit_traceability": audit_dir / "traceability.md",
        "audit_matrix": audit_dir / "test-matrix.md",
        "audit_gate": audit_dir / "release-gate.md",
        "audit_decisions": audit_dir / "decision-log.md",
    }

    if profile == "auto":
        audit_markers = [
            audit_dir / "traceability.md",
            audit_dir / "test-matrix.md",
            audit_dir / "release-gate.md",
            audit_dir / "decision-log.md",
        ]
        full_markers = [
            feature_dir / "review.md",
            review_dir / "clarify.md",
            review_dir / "checklist.md",
            review_dir / "test-matrix.md",
            review_dir / "release-gate.md",
            feature_dir / "design" / "research.md",
            feature_dir / "design" / "data-model.md",
            feature_dir / "design" / "contracts.md",
            feature_dir / "design" / "quickstart.md",
            legacy_quality_dir / "TEST_MATRIX.md",
            legacy_quality_dir / "RELEASE_GATE.md",
        ]
        if any(path.exists() for path in audit_markers):
            active_profile = "audit"
        elif any(path.exists() for path in full_markers):
            active_profile = "full"
        else:
            active_profile = "lite"
    else:
        active_profile = profile

    required_artifacts = {"spec", "plan", "tasks"}
    if active_profile in {"full", "audit"}:
        required_artifacts.update({"review"})
    if active_profile == "audit":
        required_artifacts.update({"audit_traceability", "audit_matrix", "audit_gate", "audit_decisions"})

    for name, path in artifacts.items():
        if name in required_artifacts and not path.exists():
            add_finding(
                findings,
                "missing",
                "CRITICAL" if name in {"spec", "plan", "tasks", "matrix"} else "HIGH",
                str(path.relative_to(root)),
                f"Required {name} artifact is missing.",
                "Create the missing artifact before implementation or release gate review.",
            )

    texts = {name: read(path) for name, path in artifacts.items()}
    spec_reqs = extract_ids(REQ_RE, texts["spec"])
    plan_reqs = extract_ids(REQ_RE, texts["plan"])
    task_reqs = extract_ids(REQ_RE, texts["tasks"])
    matrix_reqs = extract_ids(REQ_RE, texts["matrix"])
    matrix_cases = extract_ids(CASE_RE, texts["matrix"])
    task_cases = extract_ids(CASE_RE, texts["tasks"])
    task_ids = {match.group(1) for match in TASK_RE.finditer(texts["tasks"])}
    prd_source_ids = extract_ids(PRD_SOURCE_RE, texts["prd_source"])
    trace_source_ids = extract_ids(PRD_SOURCE_RE, texts["traceability"])

    for req in sorted(spec_reqs):
        if req.startswith("SC-"):
            continue
        covered_by_plan = req in plan_reqs or req in task_reqs or req in matrix_reqs
        covered_by_task = req in task_reqs
        covered_by_matrix = req in matrix_reqs if active_profile in {"full", "audit"} else True
        if not covered_by_plan:
            add_finding(
                findings,
                "coverage",
                "HIGH",
                f"{artifacts['spec'].relative_to(root)}:L{line_for(texts['spec'], req)}",
                f"{req} appears in the spec but not in plan, tasks, or test matrix.",
                "Map the requirement to a plan section, implementation task, and test case.",
            )
        elif not covered_by_task or not covered_by_matrix:
            missing = []
            if not covered_by_task:
                missing.append("tasks.md")
            if not covered_by_matrix:
                missing.append("review/test-matrix.md")
            add_finding(
                findings,
                "coverage",
                "MEDIUM",
                f"{artifacts['spec'].relative_to(root)}:L{line_for(texts['spec'], req)}",
                f"{req} is not covered by {', '.join(missing)}.",
                "Add explicit requirement IDs to the missing artifact rows or task steps.",
            )

    for case in sorted(matrix_cases):
        if active_profile in {"full", "audit"} and case not in task_cases and case.lower() not in texts["tasks"].lower():
            add_finding(
                findings,
                "coverage",
                "MEDIUM",
                f"{artifacts['matrix'].relative_to(root)}:L{line_for(texts['matrix'], case)}",
                f"{case} is in review/test-matrix.md but no task references it.",
                "Reference the test case in the task that creates or verifies its evidence.",
            )

    for source_id in sorted(prd_source_ids):
        if source_id not in trace_source_ids:
            add_finding(
                findings,
                "prd",
                "HIGH",
                f"{artifacts['prd_source'].relative_to(root)}:L{line_for(texts['prd_source'], source_id)}",
                f"{source_id} appears in source/prd.md but not source/traceability.md.",
                "Add a traceability row mapping the PRD section to FR, user story, test case, task, or out-of-scope rationale.",
            )

    for source_id in sorted(trace_source_ids):
        line_no = line_for(texts["traceability"], source_id)
        trace_line = texts["traceability"].splitlines()[line_no - 1] if texts["traceability"].splitlines() else ""
        if "TODO" in trace_line or re.search(r"\|\s*(open|draft)\s*\|?$", trace_line, re.I):
            add_finding(
                findings,
                "prd",
                "HIGH",
                f"{artifacts['traceability'].relative_to(root)}:L{line_no}",
                f"{source_id} traceability row is not resolved.",
                "Map the source row to concrete FR/US/TC/task IDs or mark it out-of-scope/deferred with rationale.",
            )

    names_to_scan = ["spec", "plan", "tasks"]
    if active_profile in {"full", "audit"}:
        names_to_scan.append("review")
    if active_profile == "audit":
        names_to_scan.extend(["audit_traceability", "audit_matrix", "audit_gate", "audit_decisions"])
    else:
        names_to_scan.extend(name for name, path in artifacts.items() if name not in names_to_scan and path.exists())
    for name in names_to_scan:
        text = texts[name]
        match = PLACEHOLDER_RE.search(text)
        if match:
            add_finding(
                findings,
                "placeholder",
                "HIGH" if name in {"spec", "tasks", "matrix"} else "MEDIUM",
                f"{artifacts[name].relative_to(root)}:L{line_for(text, match.group(0))}",
                f"{name} contains unresolved placeholder text: {match.group(0)}.",
                "Resolve placeholders before using this pack for implementation or release readiness.",
            )

    for match in AMBIGUOUS_RE.finditer(texts["spec"]):
        add_finding(
            findings,
            "ambiguity",
            "MEDIUM",
            f"{artifacts['spec'].relative_to(root)}:L{line_for(texts['spec'], match.group(0))}",
            f"Spec uses ambiguous quality word: {match.group(0)}.",
            "Replace with measurable success criteria or acceptance behavior.",
        )

    duplicates = normalized_requirement_lines(texts["spec"])
    for lines in duplicates.values():
        if len(lines) > 1:
            add_finding(
                findings,
                "duplication",
                "MEDIUM",
                f"{artifacts['spec'].relative_to(root)}:L{lines[0][0]}",
                "Multiple requirements appear to have near-identical wording.",
                "Merge duplicates or clarify the behavioral difference.",
            )
            break

    constitution_path = discover_constitution(root)
    constitution_text = read(constitution_path) if constitution_path else ""
    if active_profile in {"full", "audit"} and constitution_path and MUST_RE.search(constitution_text):
        for phrase in ("provider-specific", "provider id", "secret", "release gate", "evidence"):
            if phrase in constitution_text.lower() and phrase not in (texts["plan"] + texts["tasks"] + texts["matrix"]).lower():
                add_finding(
                    findings,
                    "constitution",
                    "HIGH",
                    str(constitution_path.relative_to(root)),
                    f"Constitution mentions `{phrase}` but related artifacts do not.",
                    "Map constitution MUST rules into plan, tasks, or release gate evidence.",
                )
                break
    elif active_profile in {"full", "audit"} and not constitution_path:
        add_finding(
            findings,
            "constitution",
            "MEDIUM",
            ".specify/memory/constitution.md",
            "No project constitution artifact found.",
            "Create a constitution or document why this feature does not need one.",
        )

    if active_profile in {"full", "audit"} and not re.search(r"^#{2,3}\s+Constitution Check", texts["plan"], re.M):
        add_finding(
            findings,
            "constitution",
            "HIGH",
            str(artifacts["plan"].relative_to(root)),
            "plan.md has no Constitution Check gate section.",
            "Add Constitution Check results for both gates (pre-research, post-design).",
        )
    elif re.search(r"VIOLATIONS?", texts["plan"]) and "Complexity Tracking" not in texts["plan"]:
        add_finding(
            findings,
            "constitution",
            "HIGH",
            str(artifacts["plan"].relative_to(root)),
            "plan.md reports constitution violations without a Complexity Tracking justification table.",
            "Justify each violation: rule violated, why needed, why the simpler alternative was rejected.",
        )

    run_state_path = feature_dir / "run-state.json"
    run_state: dict[str, object] | None = None
    if not run_state_path.exists():
        add_finding(
            findings,
            "lifecycle",
            "MEDIUM",
            f"{feature_dir.relative_to(root)}/run-state.json",
            "run-state.json is missing; cross-session resume has no anchor.",
            "Create run-state.json (see execution-state-and-resume.md) and update it with phase/task progress.",
        )
    else:
        try:
            run_state = json.loads(read(run_state_path))
        except json.JSONDecodeError:
            add_finding(
                findings,
                "lifecycle",
                "HIGH",
                f"{feature_dir.relative_to(root)}/run-state.json",
                "run-state.json is not valid JSON.",
                "Repair the file; resume protocol depends on it being machine-readable.",
            )
        if isinstance(run_state, dict):
            done_tasks = {m.group(1) for m in re.finditer(r"^\s*-\s+\[[xX]\]\s+(?:\*\*)?(T\d{3})", texts["tasks"], re.M)}
            last_done = run_state.get("lastCompletedTask")
            if isinstance(last_done, str) and last_done and last_done not in done_tasks:
                add_finding(
                    findings,
                    "lifecycle",
                    "MEDIUM",
                    f"{feature_dir.relative_to(root)}/run-state.json",
                    f"run-state.json says {last_done} is complete but tasks.md checkbox does not confirm it.",
                    "Reconcile run-state.json with tasks.md checkboxes; checkboxes plus git log are the source of truth.",
                )

    for expected in ("## Research", "## Data Model", "## Contracts", "## Quickstart"):
        if active_profile in {"full", "audit"} and expected not in texts["plan"]:
            add_finding(
                findings,
                "lifecycle",
                "MEDIUM",
                str(artifacts["plan"].relative_to(root)),
                f"plan.md does not contain `{expected}`.",
                "Summarize research, data model, contracts, and quickstart decisions in the compact plan.",
            )

    if "Evidence before claims" not in texts["tasks"] and "Fresh verification" not in texts["tasks"]:
        add_finding(
            findings,
            "verification",
            "HIGH",
            str(artifacts["tasks"].relative_to(root)),
            "tasks.md does not state the fresh verification rule.",
            "Add an explicit Evidence before claims rule and exact verification commands to each task.",
        )

    if "Expected: FAIL" not in texts["tasks"] or "Expected: PASS" not in texts["tasks"]:
        add_finding(
            findings,
            "tdd",
            "HIGH",
            str(artifacts["tasks"].relative_to(root)),
            "tasks.md does not include both expected failing and passing verification steps.",
            "Use the strong task template with RED, GREEN, evidence, and commit steps.",
        )

    if "## Dependencies" not in texts["tasks"] or "## Parallel Ownership" not in texts["tasks"]:
        add_finding(
            findings,
            "task",
            "HIGH",
            str(artifacts["tasks"].relative_to(root)),
            "tasks.md does not define dependency and parallel ownership sections.",
            "Add dependency order, parallel groups, agent roles, owned files, and blockers.",
        )

    if "[P]" not in texts["tasks"]:
        add_finding(
            findings,
            "parallel",
            "MEDIUM",
            str(artifacts["tasks"].relative_to(root)),
            "tasks.md has no `[P]` parallel task markers.",
            "Mark safe parallel tasks `[P]` only when they write disjoint files.",
        )

    if not FILE_REF_RE.search(texts["tasks"]):
        add_finding(
            findings,
            "task",
            "MEDIUM",
            str(artifacts["tasks"].relative_to(root)),
            "tasks.md does not contain backticked file references.",
            "Name exact files for each task.",
        )

    p0_rows = [line for line in texts["matrix"].splitlines() if active_profile in {"full", "audit"} and ("| P0 " in line or "|P0" in line)]
    for idx, row in enumerate(p0_rows, start=1):
        if "true-integration" not in row and "capture" not in row and "artifact" not in row:
            add_finding(
                findings,
                "evidence",
                "MEDIUM",
                f"{artifacts['matrix'].relative_to(root)}:P0 row {idx}",
                "P0 matrix row lacks a recognized evidence type.",
                "Set Evidence Type to artifact, capture, or true-integration.",
            )

    checklist_open = len(re.findall(r"- \[ \]", texts["checklist"]))
    checklist_done = len(re.findall(r"- \[[xX]\]", texts["checklist"]))
    domain_checklists: dict[str, dict[str, int]] = {}
    checklists_dir = feature_dir / "checklists"
    if checklists_dir.exists():
        for chk_file in sorted(checklists_dir.glob("*.md")):
            if chk_file.name == "README.md":
                continue
            chk_text = read(chk_file)
            domain_checklists[chk_file.name] = {
                "open": len(re.findall(r"- \[ \]", chk_text)),
                "done": len(re.findall(r"- \[[xX]\]", chk_text)),
            }
            for line in chk_text.splitlines():
                if re.match(r"^\s*-\s+\[[ xX]\]", line) and re.search(r"\b(verify|test|confirm)\b.*\b(works|correctly|returns)\b", line, re.I):
                    add_finding(
                        findings,
                        "placeholder",
                        "MEDIUM",
                        f"{chk_file.relative_to(root)}:L{line_for(chk_text, line.strip())}",
                        "Domain checklist item is implementation-focused, not a requirement quality question.",
                        "Rephrase as a question about requirement quality (see checklist-authoring-workflow.md).",
                    )
                    break
    hooks = summarize_hooks(root)
    templates = template_layer_summary(root)
    summary = {
        "feature_dir": str(feature_dir.relative_to(root)),
        "profile": active_profile,
        "review_file": str(artifacts["review"].relative_to(root)) if artifacts["review"].exists() else None,
        "review_dir": str(review_dir.relative_to(root)) if review_dir.exists() else None,
        "audit_dir": str(audit_dir.relative_to(root)) if audit_dir.exists() else None,
        "legacy_quality_dir": str(legacy_quality_dir.relative_to(root)) if legacy_quality_dir.exists() else None,
        "prd_source_ids": sorted(prd_source_ids),
        "trace_source_ids": sorted(trace_source_ids),
        "constitution": str(constitution_path.relative_to(root)) if constitution_path else None,
        "hooks": hooks,
        "template_layers": templates,
        "checklist": {"open": checklist_open, "done": checklist_done},
        "domain_checklists": domain_checklists,
        "run_state": {
            "present": run_state_path.exists(),
            "phase": run_state.get("phase") if isinstance(run_state, dict) else None,
            "lastCompletedTask": run_state.get("lastCompletedTask") if isinstance(run_state, dict) else None,
        },
        "requirements": sorted(spec_reqs),
        "test_cases": sorted(matrix_cases),
        "task_markers": sorted(task_ids),
        "coverage": {
            "requirements_total": len([req for req in spec_reqs if not req.startswith("SC-")]),
            "requirements_with_tasks": len([req for req in spec_reqs if req in task_reqs and not req.startswith("SC-")]),
            "requirements_with_matrix": len([req for req in spec_reqs if req in matrix_reqs and not req.startswith("SC-")]),
        },
    }
    return findings, summary


def write_checklist(feature_dir: Path, findings: list[Finding]) -> None:
    counts: dict[str, int] = {}
    for finding in findings:
        counts[finding.severity] = counts.get(finding.severity, 0) + 1
    lines = [
        "# Generated Analysis Checklist",
        "",
        "## Blocking Quality",
        "",
        f"- [ ] Critical findings resolved: {counts.get('CRITICAL', 0)} current",
        f"- [ ] High findings resolved: {counts.get('HIGH', 0)} current",
        "- [ ] No unresolved placeholders in spec, plan, tasks, or matrix",
        "- [ ] Every PRD-S source row maps to FR/US/TC/task or explicit out-of-scope rationale",
        "- [ ] Clarifications that block planning are resolved and backfilled",
        "",
        "## Traceability",
        "",
        "- [ ] Each FR maps to a task",
        "- [ ] Each FR maps to a TC row",
        "- [ ] Each P0 TC has readable evidence ref",
        "",
        "## Execution Readiness",
        "",
        "- [ ] Tasks include dependency order",
        "- [ ] Parallel tasks use `[P]` and disjoint owned files",
        "- [ ] Fresh verification commands are listed before completion claims",
    ]
    path = feature_dir / "review.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def render_markdown(findings: list[Finding], summary: dict[str, object]) -> str:
    lines = ["# Vibe Structure and Artifact Analysis", ""]
    if summary:
        lines.append(f"- Feature: `{summary['feature_dir']}`")
        lines.append(f"- Profile: `{summary['profile']}`")
        lines.append(f"- Review: `{summary.get('review_file') or summary.get('review_dir')}`")
        if summary.get("legacy_quality_dir"):
            lines.append(f"- Legacy quality: `{summary['legacy_quality_dir']}`")
        if isinstance(summary.get("prd_source_ids"), list):
            lines.append(f"- PRD source rows: {len(summary['prd_source_ids'])}")
        if isinstance(summary.get("trace_source_ids"), list):
            lines.append(f"- Traceability rows: {len(summary['trace_source_ids'])}")
        lines.append(f"- Constitution: `{summary['constitution']}`")
        if isinstance(summary.get("hooks"), dict):
            hooks = summary["hooks"]
            lines.append(f"- Hooks: `{hooks.get('path')}`")
        if isinstance(summary.get("template_layers"), dict):
            layers = summary["template_layers"]
            lines.append(
                f"- Template layers: overrides={layers.get('overrides', 0)}, "
                f"presets={layers.get('presets', 0)}, extensions={layers.get('extensions', 0)}"
            )
        if isinstance(summary.get("checklist"), dict):
            checklist = summary["checklist"]
            lines.append(f"- Checklist: open={checklist.get('open', 0)}, done={checklist.get('done', 0)}")
        coverage = summary["coverage"]
        if isinstance(coverage, dict):
            lines.append(f"- Requirements: {coverage['requirements_total']}")
            lines.append(f"- Requirements with task coverage: {coverage['requirements_with_tasks']}")
            lines.append(f"- Requirements with matrix coverage: {coverage['requirements_with_matrix']}")
        lines.append("")

    if findings:
        lines.extend([
            "| ID | Category | Severity | Location | Summary | Recommendation |",
            "|---|---|---|---|---|---|",
        ])
        for finding in findings:
            lines.append(
                f"| {finding.id} | {finding.category} | {finding.severity} | `{finding.location}` | "
                f"{finding.summary} | {finding.recommendation} |"
            )
    else:
        lines.append("No structure or artifact coverage issues found.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument("--feature", help="Feature directory, branch name, or slug")
    parser.add_argument("--version", default="V0.1", help="Quality version folder")
    parser.add_argument("--profile", choices=("auto", "lite", "full", "audit"), default="auto", help="Validation strictness")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--write-checklist", action="store_true", help="Write specs/<feature>/review.md from analyzer findings")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    findings: list[Finding] = []
    missing = [d for d in RECOMMENDED_DIRS if not (root / d).exists()]
    for directory in missing:
        add_finding(
            findings,
            "structure",
            "LOW",
            directory,
            "Recommended directory is missing.",
            "Create it when this project uses the corresponding layer or evidence type.",
        )

    feature_dir = resolve_feature(root, args.feature)
    artifact_findings, summary = analyze_artifacts(root, feature_dir, args.version, args.profile)
    findings.extend(artifact_findings)

    if args.write_checklist and feature_dir is not None:
        write_checklist(feature_dir, findings)

    if args.json:
        print(json.dumps({"summary": summary, "findings": [asdict(f) for f in findings]}, indent=2))
    else:
        print(render_markdown(findings, summary))

    severe = {"CRITICAL", "HIGH"}
    return 1 if any(finding.severity in severe for finding in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
