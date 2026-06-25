# Live Testing Slice Implementation Plan

Status: implemented, not yet committed.

> **For Agent:** Use executing-plans skill to implement this plan task-by-task.

**Goal:** Make the current EvoRig prototype easier for a user or coding agent to test live on a local machine.

**Architecture:** Keep the protocol-first Python core. Add agent-readable edit boundaries, local environment diagnostics, and clearer install/test instructions without adding Blender-specific behavior.

**Tech Stack:** Python, PyYAML, standard-library `subprocess`, `argparse`, and `unittest`.

---

## Task 1: Allowed Edit Contract

**Files:**
- Modify: `src/evorig/state.py`
- Modify: `src/evorig/validation.py`
- Modify: `tests/test_core_lifecycle.py`

**Steps:**

1. Write failing tests for `.evolve/allowed-edits.yaml` after unit init and candidate creation.
2. Generate `allowed-edits.yaml` whenever lifecycle state is written.
3. Include protected paths, sandbox roots, active candidate path, and guidance notes.
4. Validate that the allowed-edits file exists.
5. Run `python -m unittest discover -s tests`.

## Task 2: Doctor Command

**Files:**
- Create: `src/evorig/diagnostics.py`
- Modify: `src/evorig/cli.py`
- Modify: `tests/test_core_lifecycle.py`

**Steps:**

1. Write a failing test for diagnostic checks.
2. Implement core checks for Python version, PyYAML import, git availability, and writable working directory.
3. Add `evorig doctor` with normal text output and `--json`.
4. Run `python -m unittest discover -s tests`.

## Task 3: Local Testing Docs

**Files:**
- Modify: `README.md`

**Steps:**

1. Add editable-install commands.
2. Add a complete lifecycle smoke test a user can run.
3. Explain that `EvoRig` is temporary.
4. Run `python -m unittest discover -s tests`.

## Task 4: DevOps And Repo Structure

**Files:**
- Create: `.github/workflows/ci.yml`
- Create: `.github/pull_request_template.md`
- Create: `CONTRIBUTING.md`
- Create: `SECURITY.md`
- Create: `docs/development.md`
- Modify: `pyproject.toml`

**Implemented:**

1. Added CI for supported Python versions.
2. Added contribution, security, and development docs.
3. Added a PR template with CodeRabbit-ignore guidance.
4. Added package metadata and coverage configuration.

## Task 5: Run Records And Artifact Manifests

**Files:**
- Create: `src/evorig/runs.py`
- Create: `schemas/run-record.schema.json`
- Create: `schemas/artifact-manifest.schema.json`
- Modify: `src/evorig/cli.py`
- Modify: `tests/test_core_lifecycle.py`

**Implemented:**

1. Added `evorig run start`.
2. Added `evorig artifact add`.
3. Added `evorig run finish`.
4. Stored runtime records under `runtime/`.
5. Added tests for run records and artifact metadata.
