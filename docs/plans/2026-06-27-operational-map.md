# Operational Map For Harness Units

Status: implemented.

## Goal

Every new harness unit should include a unit-local `operational-map.md` that helps an agent preserve and update its current working understanding of the unit.

The map should capture:

- what the harness unit is trying to improve;
- what systems, tools, and environments it interacts with;
- what artifacts and evidence are useful right now;
- how the environment can usually be run or reset;
- known constraints, fragile spots, and open questions;
- assumptions that need re-checking;
- where prior runs, artifacts, observations, and evidence live.

## Architecture

`operational-map.md` is generated during `harneloop init-unit` and lives at the root of the harness unit beside `UNIT_AGENT.md`.

The file is required for validation, packageable through promoted snapshots, and editable by the operating agent. It is not protected like `unit.yaml`, `.evolve/`, `versions/`, `provenance/`, `candidates/`, or `runtime/`.

The map is context and navigation, not a rigid procedure. Agents should still reason from the current task, inspect available evidence, and choose the most appropriate attempt and evaluation strategy.

## Autonomy Guidance

The operating agent should aim to run repeated testing/improvement loops without requiring the user to manually restart apps, reinstall addons, reset services, or collect files.

If automating the environment is reasonable, the agent should implement or document that automation.

If automation is risky, unclear, or too expensive/time-consuming, the agent should ask the user before proceeding.

## Validation

- Add tests that `init_unit` creates `operational-map.md`.
- Assert the generated map contains orientation sections and avoids rigid evaluation wording.
- Assert onboarding output mentions the operational map and autonomy guidance.
- Assert promoted packages include the operational map through normal snapshot packaging.
