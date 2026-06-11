# Quality Gate Template

## Test Levels

```text
L0 Static checks: lint, typecheck, schema, dependency checks
L1 Unit tests: pure logic, boundaries, errors
L2 Component tests: module composition, config, state changes
L3 Contract tests: outgoing requests, incoming response shape, protocol compatibility
L4 E2E tests: real client/service/key/account where needed
L5 Release gate: report trust, evidence, platform matrix, secret scan
```

## Test Case Schema

```json
{
  "id": "TC-001",
  "capability": "capability_name",
  "stage": "contract",
  "priority": "P0",
  "name": "human-readable behavior",
  "evidenceType": "capture",
  "failureClass": "gateway",
  "requiredPlatforms": ["darwin", "linux"],
  "requiresSecret": false,
  "owner": "platform",
  "acceptance": [
    "statusCode == 200",
    "response field exists"
  ]
}
```

## Evidence Types

| Type | Meaning |
|---|---|
| `artifact` | local file, config, snapshot, function output |
| `capture` | captured request/event proving actual emitted behavior |
| `true-integration` | real account, real key, real client, or real external service |

Rules:

- P0 core paths need at least one true-integration case unless explicitly impossible.
- Protocol translation needs capture tests.
- Config/restore/security checks may use artifact evidence.
- Release reports cannot be artifact-only.

## Release Gate Rules

```text
1. Release branch is allowed.
2. Worktree is clean.
3. Required platform reports exist.
4. Reports come from the same commit.
5. All P0 cases pass.
6. SKIPPED/BLOCKED are not counted as PASS.
7. PASS cases have positiveAssertions > 0.
8. PASS cases have readable evidenceRefs.
9. true-integration required cases are not replaced by artifact/capture.
10. Reports and evidence contain no secrets.
11. runnerId/platform/os provenance is consistent.
12. Copied or relabeled platform reports are rejected.
13. Completion, fixed, pass, and release-ready claims cite fresh verification from the current execution session.
```

## Report Shape

```json
{
  "runId": "2026-06-10T10-00-00Z-linux-ci-001",
  "project": "your-project",
  "commit": "abc123",
  "branch": "main",
  "platform": "linux",
  "runnerId": "ci-linux-001",
  "dirty": false,
  "passed": false,
  "counts": {"PASS": 10, "FAIL": 1, "BLOCKED": 0, "SKIPPED": 0},
  "cases": [
    {
      "id": "TC-001",
      "status": "PASS",
      "positiveAssertions": 3,
      "evidenceType": "capture",
      "evidenceRefs": ["quality/V1.0/evidence/tc-001.json"],
      "verifiedAt": "2026-06-11T10:00:00Z",
      "verificationCommand": "pytest tests/path/test_file.py -v"
    }
  ]
}
```
