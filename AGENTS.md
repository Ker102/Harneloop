# Agent Instructions For EvoRig

EvoRig is a framework for agent-built, artifact-aware harness units.

## Current Stage

This repository is in the first core prototype stage. Keep changes small, tested, and generic. Do not let Blender-specific assumptions leak into the framework core.

## First Onboarding Step

When starting a new harness unit, run:

```powershell
evorig onboard
```

If EvoRig is not installed yet, use:

```powershell
python -m evorig onboard
```

Use the five onboarding questions to collect only the minimum context needed for the first baseline attempt: harness goal, success/failure criteria, proof artifacts, environment status, and constraints. Then map those answers into `target set`, `environment connect`, and `attempt plan`.

## Product Principles

- The framework process is protected. Unit evolution is sandboxed.
- Agents can explore freely inside candidates. The engine controls promotion.
- A candidate patch is a real object with rationale, changes, validation, and evidence.
- Promotion requires a restorable version snapshot.
- Stop, wait, and resume are normal lifecycle states, not error cases.
- Portable units should exclude raw traces, caches, secrets, and unpromoted experiments by default.

## Engineering Defaults

- Use Python for the first reference implementation.
- Prefer standard-library code unless a dependency removes real complexity.
- Use tests for lifecycle behavior before changing implementation.
- Keep public names temporary until the product and demo prove the right identity.
- Never commit secrets.
