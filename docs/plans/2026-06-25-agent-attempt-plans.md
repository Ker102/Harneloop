# Agent Attempt Plans Implementation Plan

Status: implemented, not yet committed.

> **For Agent:** Use executing-plans skill to implement this plan task-by-task.

**Goal:** Represent complex task-specific validation as agent-authored attempts instead of assuming a single test command.

**Architecture:** Attempt plans live inside harness units under `attempts/`. A run can link to an attempt plan. Observations recorded after the run can later become evidence, candidate changes, or regression cases.

**Tech Stack:** Python, PyYAML, standard-library `argparse`, and `unittest`.

---

## Implemented

- Added `harneloop attempt plan`.
- Added `harneloop attempt observe`.
- Added `attempts/attempt-0001/attempt.yaml`.
- Added `attempts/attempt-0001/OBSERVATIONS.md`.
- Added `run start --attempt-id`.
- Added `schemas/attempt-plan.schema.json`.
- Updated docs to describe agent-authored attempts for tool-driven tasks.
