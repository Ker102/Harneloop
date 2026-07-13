# Agent Onboarding

Harneloop should be understandable to an agent that has only the repository and the user's target task. The first step is not to write a validator or assume a test command exists. The first step is to collect enough context to create a baseline attempt.

For a human-friendly guided setup, run:

```powershell
harneloop setup
```

For an agent-readable checklist, run:

```powershell
harneloop onboard
```

or, before editable install:

```powershell
python -m harneloop onboard
```

For machine-readable output:

```powershell
harneloop onboard --format json
```

For a harness unit created by an earlier Harneloop version, run `harneloop upgrade-unit <unit>` once. It adds missing framework protocol files without replacing existing harness material.

## Minimal User Questions

Use these as context fields, not as a mandatory questionnaire. The agent may create the provisional unit and inspect the workspace first, then ask only the questions that still matter:

1. What should this harness help an agent get better at?
2. Where will the harness be used, such as a coding-agent workflow, an app agent, research, or internal automation?
3. How should success criteria be handled?
4. How should results be validated?
5. Does a testing environment already exist, partly exist, need to be built, or is that not clear yet?

Do not turn onboarding into a long intake form. Success criteria and artifact choices are guided options, not required expertise from the user. Run `harneloop intake status <unit>` after inspection and classify important context as confirmed, delegated, inferred, unknown, or not applicable. Do not silently convert an inference into confirmed unit truth.

Before the first real run, resolve the relevant fields and record explicit user confirmation or delegation with `harneloop intake acknowledge`. If a missing reference, target project, credential, or judgment can materially change the test, ask for it directly or enter a wait state rather than only mentioning the gap after setup.

Harneloop records the environment mapping. It does not discover test endpoints, MCP tools, run commands, screenshot locations, render outputs, or artifact paths by itself. The onboarding agent must inspect the actual project/environment, determine how artifacts are produced, and write that mapping into the harness.

Every new harness unit has `operational-map.md`. Use it as current orientation: what this unit is trying to improve, what systems and tools it interacts with, which artifacts or evidence are currently useful, how the environment can usually run or reset, known constraints, fragile spots, open questions, assumptions to re-check, and where prior runs or evidence live. Update it when the workflow, evidence needs, environment assumptions, or automation strategy change.

This map is context and navigation, not a rigid procedure. The agent should still reason from the task, inspect available evidence, and choose the appropriate test or evaluation strategy for the current attempt.

## Capability Gaps

Do not assume every operating agent has Codex-level powers. A custom Hermes, OpenClaw, app agent, or restricted automation worker may lack terminal access, filesystem access, browser access, package managers, MCP servers, visual inspection, database access, or other capabilities needed to build the harness unit well.

Separate two layers:

- Operating-agent capabilities: what the current agent can actually use while building the unit.
- Unit/target-agent tools: tools designed into the harness unit or provided to the target agent through the environment contract.

If the operating agent is missing a useful capability, record the gap in `operational-map.md`: what is missing, why it matters, what tool or dependency would help, what risk/cost/auth/security change it introduces, and what fallback exists if the user declines.

Low-risk local capabilities can be installed, enabled, or built when the environment allows it. Larger dependencies, credentials, paid APIs, user-owned accounts, external access, network expansion, or security-impacting changes should be proposed first.

Capability additions should be justified by observed bottlenecks, failed attempts, missing artifacts, or clear expected improvement, not added speculatively.

## Reuse Existing Work

The goal is the best verified harness, not a from-scratch implementation. Before building a missing capability, inspect what already exists: project-native tools, open-source libraries, agent skills, MCP servers, validators, datasets, examples, documentation, research, and reusable harness material. The agent may install, adapt, combine, or learn from suitable existing work when doing so is likely to improve results or reduce unnecessary effort.

Do not reuse blindly. Record the source, version or revision when relevant, purpose, license or attribution obligations, compatibility assumptions, and evidence that the addition helped. Review executable third-party material before trusting it. Ask first when reuse introduces credentials, paid services, external access, material downloads, restrictive licenses, security-sensitive execution, or a meaningful change to the environment. If an existing solution is unsuitable, document why before building a replacement.

Suggested success answers:

- Let the agent propose success criteria.
- I know the exact successful result.
- Decide after the first baseline attempt.

Suggested validation answers:

- Best validation quality.
- Visual or artifact-first validation.
- Balanced validation.
- Resource-efficient validation.
- Let the agent decide per task.

Optional follow-up:

- Are there constraints, protected areas, human review points, or cost/time limits the harness must obey?

## How Answers Map Into Harneloop

- Goal, success strategy, validation preference, and suggested artifacts become a target brief: `harneloop target set`.
- The current working map of the unit is captured and revised in `operational-map.md`.
- Existing commands, MCP servers, manual steps, or custom tools become an environment contract: `harneloop environment connect`.
- The first real workflow becomes an attempt plan: `harneloop attempt plan`.
- Produced outputs become run artifacts: `harneloop run start`, `harneloop artifact add`, `harneloop run finish`.
- Result quality and the next lifecycle decision are recorded with `harneloop attempt conclude`.
- Harness changes become candidates and require evidence before promotion.
- User defaults can be managed with `harneloop settings`.
- Local harness units can be listed or registered with `harneloop units`.

## Important Behavior

Harneloop does not require every task to have a direct test command. For a tool-driven setup, such as a Blender MCP server or an agent-controlled SVG rendering workflow, declare the tools and artifacts in the environment contract. The agent then writes an attempt plan for how it will use those tools, produce artifacts, inspect them, and turn observations into evidence.

The agent should aim to run repeated testing and improvement loops without requiring the user to manually restart apps, reinstall addons, reset services, or collect files. If environment automation is reasonable, implement or document it. If it is risky, unclear, or too expensive/time-consuming, ask the user before proceeding.

If a required artifact or human judgment is delayed, use `harneloop state wait`. If the unit appears to hit a capability limit, use `harneloop state stop` with a concrete reason and next action.

Finishing a run records execution status; it does not prove that the produced result is good. Inspect the artifacts and conclude every attempt with one explicit decision: accept the current harness, create a candidate, rerun with a corrected plan, request missing input, or stop. A good first result may be accepted with no candidate. Missing expected evidence cannot support an unqualified pass.

When entering or resuming work on a unit, run `harneloop brief <unit>`. The generated brief is scoped to that harness unit, so unrelated work in the same agent session remains unaffected.
