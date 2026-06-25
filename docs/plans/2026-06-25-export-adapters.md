# Export Adapters Implementation Plan

Status: implemented, not yet committed.

> **For Agent:** Use executing-plans skill to implement this plan task-by-task.

**Goal:** Let a promoted harness unit export agent-facing instructions for common target agent environments.

**Architecture:** Export adapters are file generators over the promoted unit state. They do not change the harness unit lifecycle and they do not own runtime state.

**Tech Stack:** Python, standard-library file operations, and `unittest`.

---

## Task 1: Generic And Codex Exports

**Files:**
- Create: `src/evorig/adapters.py`
- Modify: `src/evorig/cli.py`
- Modify: `tests/test_core_lifecycle.py`

**Steps:**

1. Write failing tests for generic and Codex exports.
2. Implement `export_unit` for `generic`, `codex`, and `cursor`.
3. Add `evorig export`.
4. Run tests and CLI smoke flow.
