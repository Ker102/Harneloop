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

Use the five onboarding questions to collect only the minimum context needed for the first baseline attempt: harness goal, usage context, success strategy, validation preference, and environment status. Treat success criteria and artifact choices as guided options. The user does not need to know validation design up front.

EvoRig records environment mappings; it does not magically discover test endpoints, MCP tools, run commands, screenshot locations, render outputs, or artifact paths. The onboarding agent must inspect the actual project/environment, determine how artifacts are produced, and write that mapping into the harness via `environment connect`, `attempt plan`, run records, and artifact records.

Every new harness unit includes `operational-map.md`. Treat it as the current orientation for this specific unit: what it is trying to improve, which systems and tools it touches, what artifacts or evidence are useful, how the environment can usually be run or reset, fragile spots, assumptions, open questions, and where prior evidence lives. It is context and navigation, not a rigid procedure. Update it when the workflow, evidence needs, artifact paths, environment assumptions, or automation strategy change.

Track capability gaps in `operational-map.md`. Operating-agent capabilities are what the current agent can actually use while building the unit, such as terminal, filesystem, browser, MCPs, package managers, visual inspection, database access, or custom tools. Unit/target-agent tools are the tools designed into the harness unit or provided to the target agent. Keep those layers separate.

If the operating agent is missing a useful capability, state what is missing, why it matters, what tool or dependency would help, and what risk, cost, auth, or security change it introduces. Low-risk local capabilities can be installed, enabled, or built when the environment allows it. Larger dependencies, credentials, external access, paid services, or security-impacting changes should be proposed first. Capability additions should be justified by observed bottlenecks, failed attempts, missing artifacts, or clear expected improvement.

Agents should aim to run repeated testing and improvement loops without requiring the user to manually restart apps, reinstall addons, reset services, or collect files. If automating the environment is reasonable, implement or document it. If automation is risky, unclear, or too expensive/time-consuming, ask the user before proceeding.

For human-guided setup, use:

```powershell
evorig setup
```

For manual harness unit and preference management, use `evorig units` and `evorig settings`.

## Product Principles

- The framework process is protected. Harness unit evolution is sandboxed.
- Agents can explore freely inside candidates. The engine controls promotion.
- A candidate patch is a real object with rationale, changes, validation, and evidence.
- Promotion requires a restorable version snapshot.
- Stop, wait, and resume are normal lifecycle states, not error cases.
- Portable harness units should exclude raw traces, caches, secrets, and unpromoted experiments by default.
- Commands that allocate IDs or update shared control files must use EvoRig locks and atomic writes.

## Engineering Defaults

- Use Python for the first reference implementation.
- Prefer standard-library code unless a dependency removes real complexity.
- Use tests for lifecycle behavior before changing implementation.
- Keep public names temporary until the product and demo prove the right identity.
- Never commit secrets.
