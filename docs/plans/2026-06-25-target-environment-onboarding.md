# Target And Environment Onboarding Implementation Plan

Status: implemented and extended with MCP/tool-driven environments.

> **For Agent:** Use executing-plans skill to implement this plan task-by-task.

**Goal:** Let users or agents describe what a harness is for, then connect EvoRig to an existing or managed testing environment without assuming the framework owns setup.

**Architecture:** Store the target task brief and environment contract as unit-local YAML/Markdown. Default to connecting existing environments first. Managed setup is a declared mode, not automatic provisioning.

**Tech Stack:** Python, PyYAML, standard-library `argparse`, and `unittest`.

---

## Task 1: Target Brief

**Files:**
- Create: `src/evorig/target.py`
- Modify: `src/evorig/cli.py`
- Modify: `tests/test_core_lifecycle.py`

**Steps:**

1. Write failing tests for target brief creation.
2. Implement `target set`.
3. Generate starter test suggestions.
4. Run tests.

## Task 2: Environment Contract

**Files:**
- Create: `src/evorig/environment.py`
- Modify: `src/evorig/unit.py`
- Modify: `src/evorig/cli.py`
- Modify: `tests/test_core_lifecycle.py`

**Steps:**

1. Write failing tests for an existing environment contract.
2. Implement `environment connect`.
3. Implement `environment status`.
4. Run tests.

## Task 3: Documentation And Demo Verification

**Files:**
- Create: `docs/environment-onboarding.md`
- Modify: `docs/demo-first-test.md`
- Modify: `README.md`

**Steps:**

1. Document the setup-mode architecture.
2. Update the first demo with target and environment commands.
3. Run the full local verification and smoke demo.
