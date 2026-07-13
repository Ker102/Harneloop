# Parallel Candidates Implementation Plan

> **For Agent:** Use executing-plans skill to implement this plan task-by-task.

**Goal:** Add concurrent accumulating candidates with impact planes, scaled validation, and safe sequential promotion.

**Architecture:** Candidate metadata owns classification, stage, base version, and required validation. Unit state tracks all open candidates. Promotion remains linear and marks parallel candidates stale when their shared base changes.

**Tech Stack:** Python 3.11+, argparse, YAML, unittest, existing atomic writes and cross-platform file locks.

---

### Task 1: Candidate Metadata And Parallel State Tests

**Files:**
- Modify: `tests/test_core_lifecycle.py`
- Modify: `src/harneloop/candidate.py`
- Modify: `src/harneloop/state.py`

1. Add failing tests that create infrastructure and target-harness candidates and expect both IDs in `active_candidates`.
2. Add candidate constants, metadata fields, listing, stage transitions, and state synchronization.
3. Update allowed-edit and brief rendering to include all open candidates.
4. Run `python -m unittest tests.test_core_lifecycle -v` and confirm the focused tests pass.

### Task 2: Tiered Evidence And Safe Promotion Tests

**Files:**
- Modify: `tests/test_core_lifecycle.py`
- Modify: `src/harneloop/evidence.py`
- Modify: `src/harneloop/versioning.py`

1. Add failing tests for insufficient evidence tier, representative evidence without a run, stale parallel candidate promotion, and rebase invalidating old evidence.
2. Record candidate base and validation tier on evidence.
3. Require new-schema candidates to be ready, current-base, and supported at the required tier.
4. Mark other open candidates `needs_rebase` after promotion and implement explicit rebase.
5. Run the focused lifecycle tests.

### Task 3: CLI Surface

**Files:**
- Modify: `tests/test_user_cli_support.py`
- Modify: `src/harneloop/cli.py`

1. Add failing CLI tests for `candidate list`, classified creation, `candidate stage`, and `candidate rebase`.
2. Add `--plane` and `--validation-tier` to creation, tier to evidence, and the new lifecycle subcommands.
3. Preserve existing candidate command compatibility.
4. Run the CLI support tests.

### Task 4: Contracts And Agent Guidance

**Files:**
- Create: `schemas/candidate-record.schema.json`
- Modify: `README.md`
- Modify: `AGENTS.md`
- Modify: `docs/agent-onboarding.md`
- Modify: `docs/architecture/core-lifecycle.md`
- Modify: `skills/harneloop/SKILL.md`

1. Document planes, validation tiers, batching, parallel candidates, and rebase behavior.
2. Teach agents not to create one candidate per commit or run full benchmarks for infrastructure-only changes.
3. Explain that evaluation and target-harness changes should normally use separate candidates.

### Task 5: Verification And Delivery

**Files:**
- Modify as required by verification findings.

1. Run `python -m compileall src tests`.
2. Run `python -m unittest discover -s tests -v`.
3. Run a temporary CLI lifecycle with two parallel candidates, promotion, stale-base rejection, rebase, and second promotion.
4. Run `git diff --check` and inspect the final diff.
5. Commit and push the verified change.
