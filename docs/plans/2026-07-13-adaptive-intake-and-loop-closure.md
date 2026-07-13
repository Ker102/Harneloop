# Adaptive Intake And Loop Closure Implementation Plan

> **For Agent:** Use executing-plans skill to implement this plan task-by-task.

**Goal:** Add adaptive intake state, explicit attempt conclusions, and unit-scoped context recovery.

**Architecture:** Store intake and session context under framework-owned `.evolve/`; keep execution status in run records and evaluation decisions in attempt records. Generate a scoped `AGENTS.md` and `SESSION_BRIEF.md`, and expose machine-usable CLI commands for intake, conclusion, and recovery.

**Tech Stack:** Python 3.11+, argparse, PyYAML, unittest.

---

### Task 1: Adaptive Intake Record

**Files:**
- Create: `src/harneloop/intake.py`
- Modify: `src/harneloop/unit.py`
- Modify: `src/harneloop/cli.py`
- Test: `tests/test_core_lifecycle.py`

1. Write tests for provisional intake creation, status rendering, field resolution, and first-run readiness.
2. Run the focused tests and confirm they fail.
3. Implement intake YAML, `intake status`, and `intake resolve`.
4. Require explicit confirmation or user delegation before the first run while allowing unit scaffolding and inspection.
5. Run focused tests and commit.

### Task 2: Explicit Attempt Conclusion

**Files:**
- Modify: `src/harneloop/attempts.py`
- Modify: `src/harneloop/runs.py`
- Modify: `src/harneloop/cli.py`
- Modify: `schemas/attempt-plan.schema.json`
- Modify: `schemas/run-record.schema.json`
- Test: `tests/test_core_lifecycle.py`

1. Write tests showing that run completion enters `awaiting_evaluation` and does not imply artifact success.
2. Write tests for `accept`, `create_candidate`, `rerun`, `request_input`, and `stop` conclusions.
3. Implement expected-artifact coverage checks and conclusion records.
4. Make missing evidence incompatible with an unqualified passing conclusion.
5. Run focused tests and commit.

### Task 3: Unit-Scoped Context Recovery

**Files:**
- Modify: `src/harneloop/state.py`
- Modify: `src/harneloop/unit.py`
- Modify: `src/harneloop/cli.py`
- Test: `tests/test_core_lifecycle.py`

1. Write tests for generated unit-local `AGENTS.md` and `.evolve/SESSION_BRIEF.md`.
2. Ensure language is scoped to work involving the unit, not the entire agent session.
3. Aggregate target, intake, lifecycle state, latest conclusion, and next action into the brief.
4. Add `harneloop brief <unit>` with Markdown and JSON formats.
5. Run focused tests and commit.

### Task 4: Agent Protocol And Skill

**Files:**
- Create: `skills/harneloop/SKILL.md`
- Modify: `src/harneloop/onboarding.py`
- Modify: `docs/agent-onboarding.md`
- Modify: `README.md`
- Test: `tests/test_core_lifecycle.py`

1. Add tests that machine-readable onboarding requires intake reconciliation and attempt conclusion.
2. Add a bundled skill that teaches context recovery and loop closure without acting as persistent state.
3. Update agent documentation and starter prompts.
4. Run focused tests and commit.

### Task 5: Integration Verification

**Files:**
- Modify as required by failures.

1. Run the full unittest suite.
2. Run `compileall`, `harneloop doctor`, `harneloop onboard --format json`, and a temporary CLI lifecycle.
3. Verify `git diff --check` and inspect the final diff.
4. Push the completed commits to `main`.
