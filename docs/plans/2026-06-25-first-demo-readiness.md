# First Demo Readiness Implementation Plan

Status: implemented, not yet committed.

> **For Agent:** Use executing-plans skill to implement this plan task-by-task.

**Goal:** Make EvoRig ready for first local demo testing without requiring Blender or a custom project.

**Architecture:** Add a generic artifact-aware unit template and agent-readable status output. Keep template content as framework-neutral seed material, not domain-specific automation.

**Tech Stack:** Python, PyYAML, standard-library `argparse`, and `unittest`.

---

## Task 1: Artifact Review Template

**Files:**
- Create: `src/evorig/templates.py`
- Modify: `src/evorig/unit.py`
- Modify: `src/evorig/cli.py`
- Modify: `tests/test_core_lifecycle.py`

**Steps:**

1. Write failing tests for `init_unit(..., template="artifact-review")`.
2. Implement template application.
3. Add `init-unit --template`.
4. Add `template list`.
5. Run tests.

## Task 2: Agent-Readable Status

**Files:**
- Modify: `src/evorig/cli.py`
- Modify: `src/evorig/state.py`
- Modify: `tests/test_core_lifecycle.py`

**Steps:**

1. Write failing tests for Markdown status rendering.
2. Implement `status --format markdown`.
3. Run tests.

## Task 3: Demo Docs

**Files:**
- Create: `docs/demo-first-test.md`
- Modify: `README.md`

**Steps:**

1. Document the first demo flow.
2. Include the exact commands.
3. Run full verification.
