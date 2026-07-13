# Agent Instructions For Harneloop

Harneloop is a framework for agent-built, artifact-aware harness units.

## Current Stage

This repository is in the first core prototype stage. Keep changes small, tested, and generic. Do not let Blender-specific assumptions leak into the framework core.

## First Onboarding Step

When starting a new harness unit, run:

```powershell
harneloop onboard
```

If Harneloop is not installed yet, use:

```powershell
uv run harneloop onboard
```

Use the five onboarding questions to collect only the minimum context needed for the first baseline attempt: harness goal, usage context, success strategy, validation preference, and environment status. Treat success criteria and artifact choices as guided options. The user does not need to know validation design up front.

Harneloop records environment mappings; it does not magically discover test endpoints, MCP tools, run commands, screenshot locations, render outputs, or artifact paths. The onboarding agent must inspect the actual project/environment, determine how artifacts are produced, and write that mapping into the harness via `environment connect`, `attempt plan`, run records, and artifact records.

Every new harness unit includes `operational-map.md`. Treat it as the current orientation for this specific unit: what it is trying to improve, which systems and tools it touches, what artifacts or evidence are useful, how the environment can usually be run or reset, fragile spots, assumptions, open questions, and where prior evidence lives. It is context and navigation, not a rigid procedure. Update it when the workflow, evidence needs, artifact paths, environment assumptions, or automation strategy change.

Track capability gaps in `operational-map.md`. Operating-agent capabilities are what the current agent can actually use while building the unit, such as terminal, filesystem, browser, MCPs, package managers, visual inspection, database access, or custom tools. Unit/target-agent tools are the tools designed into the harness unit or provided to the target agent. Keep those layers separate.

If the operating agent is missing a useful capability, state what is missing, why it matters, what tool or dependency would help, and what risk, cost, auth, or security change it introduces. Low-risk local capabilities can be installed, enabled, or built when the environment allows it. Larger dependencies, credentials, external access, paid services, or security-impacting changes should be proposed first. Capability additions should be justified by observed bottlenecks, failed attempts, missing artifacts, or clear expected improvement.

Optimize for the best verified result, not a from-scratch implementation. Inspect and reuse suitable project-native or external tools, open-source libraries, agent skills, MCP servers, validators, datasets, examples, documentation, research, and prior harness work. Record source, relevant version, purpose, licensing or attribution obligations, compatibility assumptions, and evidence of value. Review executable third-party material before trusting it, and ask first when reuse changes security posture, requires credentials or paid services, expands external access, introduces a restrictive license, or materially changes the environment.

Agents should aim to run repeated testing and improvement loops without requiring the user to manually restart apps, reinstall addons, reset services, or collect files. If automating the environment is reasonable, implement or document it. If automation is risky, unclear, or too expensive/time-consuming, ask the user before proceeding.

For human-guided setup, use:

```powershell
harneloop setup
```

For manual harness unit and preference management, use `harneloop units` and `harneloop settings`. CLI-created units are registered automatically; a registered unit ID or name can be used from any directory.

## Product Principles

- The framework process is protected. Harness unit evolution is sandboxed.
- Agents can explore freely inside candidates. The engine controls promotion.
- A candidate is a coherent change batch with rationale, changes, validation, and evidence; it is not required for every individual edit or commit.
- Multiple independent candidates may remain open. Keep target-harness, evaluation, and infrastructure work separate when their evidence or risks differ.
- Scale validation to impact: structural, targeted, representative, or full. Use full regressions for broad changes and meaningful checkpoints, not every setup edit.
- Promoting one parallel candidate makes siblings on the old base require rebase and fresh evidence.
- Promotion requires a restorable version snapshot.
- Stop, wait, and resume are normal lifecycle states, not error cases.
- Portable harness units should exclude raw traces, caches, secrets, and unpromoted experiments by default.
- Commands that allocate IDs or update shared control files must use Harneloop locks and atomic writes.

## Engineering Defaults

- Use Python for the first reference implementation.
- Prefer standard-library code unless a dependency removes real complexity.
- Use tests for lifecycle behavior before changing implementation.
- Use Harneloop consistently across the package, CLI, harness-unit metadata, documentation, and public materials.
- Never commit secrets.
