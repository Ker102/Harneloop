# Evidence-Gated Promotion Implementation Plan

Status: implemented, not yet committed.

> **For Agent:** Use executing-plans skill to implement this plan task-by-task.

**Goal:** Make promotion evidence-backed by default so candidates cannot silently become promoted harness versions without a recorded reason.

**Architecture:** Evidence is stored as YAML records inside candidate workspaces. Promotion checks candidate evidence by default and allows an explicit development override for incomplete early experiments.

**Tech Stack:** Python, PyYAML, standard-library `argparse`, and `unittest`.

---

## Task 1: Candidate Evidence Records

**Files:**
- Create: `src/evorig/evidence.py`
- Create: `schemas/candidate-evidence.schema.json`
- Modify: `src/evorig/cli.py`
- Modify: `tests/test_core_lifecycle.py`

**Steps:**

1. Write failing tests for adding evidence to a candidate.
2. Implement evidence IDs and YAML records under `candidates/<id>/evidence/`.
3. Add `evorig candidate evidence add`.
4. Run tests.

## Task 2: Promotion Gate

**Files:**
- Modify: `src/evorig/versioning.py`
- Modify: `src/evorig/cli.py`
- Modify: `tests/test_core_lifecycle.py`

**Steps:**

1. Write a failing test that promotion without evidence is blocked.
2. Write a passing test that promotion with evidence succeeds.
3. Add explicit `--allow-missing-evidence` override for development only.
4. Run tests and CLI smoke flow.
