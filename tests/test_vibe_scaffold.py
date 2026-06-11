import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD = ROOT / "vibe-coding-spec" / "scripts" / "scaffold_vibe_feature.py"
CHECK = ROOT / "vibe-coding-spec" / "scripts" / "check_vibe_structure.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def files_under(root: Path) -> set[str]:
    return {str(path.relative_to(root)) for path in root.rglob("*") if path.is_file()}


class VibeScaffoldTests(unittest.TestCase):
    def test_default_scaffold_is_lightweight(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = run(str(SCAFFOLD), "--root", str(root), "--name", "Ask AI Extension")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                files_under(root),
                {
                    "specs/001-ask-ai-extension/plan.md",
                    "specs/001-ask-ai-extension/run-state.json",
                    "specs/001-ask-ai-extension/spec.md",
                    "specs/001-ask-ai-extension/tasks.md",
                },
            )
            check = run(
                str(CHECK),
                "--root",
                str(root),
                "--feature",
                "001-ask-ai-extension",
                "--json",
            )
            payload = json.loads(check.stdout)
            self.assertEqual(payload["summary"]["profile"], "lite")

    def test_prd_scaffold_keeps_source_inside_spec(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prd = root / "prd.md"
            prd.write_text("# Ask AI Extension\n\n## Goal\nShip it.\n", encoding="utf-8")
            result = run(str(SCAFFOLD), "--root", str(root), "--prd", str(prd))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                files_under(root),
                {
                    "prd.md",
                    "specs/001-ask-ai-extension/plan.md",
                    "specs/001-ask-ai-extension/run-state.json",
                    "specs/001-ask-ai-extension/spec.md",
                    "specs/001-ask-ai-extension/tasks.md",
                },
            )
            spec = (root / "specs" / "001-ask-ai-extension" / "spec.md").read_text(encoding="utf-8")
            self.assertIn("## Source", spec)
            self.assertIn("Original PRD", spec)
            self.assertIn("PRD-S001", spec)

    def test_full_scaffold_uses_compact_sdd_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = run(str(SCAFFOLD), "--root", str(root), "--name", "Ask AI Extension", "--full")

            self.assertEqual(result.returncode, 0, result.stderr)
            paths = files_under(root)
            self.assertFalse(any(path.startswith(".specify/") for path in paths), paths)
            self.assertFalse(any(path.startswith("quality/") for path in paths), paths)
            self.assertEqual(
                paths,
                {
                    "specs/001-ask-ai-extension/plan.md",
                    "specs/001-ask-ai-extension/review.md",
                    "specs/001-ask-ai-extension/run-state.json",
                    "specs/001-ask-ai-extension/spec.md",
                    "specs/001-ask-ai-extension/tasks.md",
                },
            )
            self.assertTrue((root / "specs" / "001-ask-ai-extension" / "evidence").is_dir())

            check = run(
                str(CHECK),
                "--root",
                str(root),
                "--feature",
                "001-ask-ai-extension",
                "--json",
            )
            payload = json.loads(check.stdout)
            self.assertEqual(payload["summary"]["profile"], "full")

    def test_audit_scaffold_adds_release_audit_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = run(str(SCAFFOLD), "--root", str(root), "--name", "Ask AI Extension", "--audit")

            self.assertEqual(result.returncode, 0, result.stderr)
            paths = files_under(root)
            self.assertFalse(any(path.startswith(".specify/") for path in paths), paths)
            self.assertFalse(any(path.startswith("quality/") for path in paths), paths)
            self.assertEqual(
                paths,
                {
                    "specs/001-ask-ai-extension/audit/decision-log.md",
                    "specs/001-ask-ai-extension/audit/release-gate.md",
                    "specs/001-ask-ai-extension/audit/test-matrix.md",
                    "specs/001-ask-ai-extension/audit/traceability.md",
                    "specs/001-ask-ai-extension/plan.md",
                    "specs/001-ask-ai-extension/review.md",
                    "specs/001-ask-ai-extension/run-state.json",
                    "specs/001-ask-ai-extension/spec.md",
                    "specs/001-ask-ai-extension/tasks.md",
                },
            )
            self.assertTrue((root / "specs" / "001-ask-ai-extension" / "evidence").is_dir())

            check = run(
                str(CHECK),
                "--root",
                str(root),
                "--feature",
                "001-ask-ai-extension",
                "--json",
            )
            payload = json.loads(check.stdout)
            self.assertEqual(payload["summary"]["profile"], "audit")


if __name__ == "__main__":
    unittest.main()
