# Agent Onboarding

EvoRig should be understandable to an agent that has only the repository and the user's target task. The first step is not to write a validator or assume a test command exists. The first step is to collect enough context to create a baseline attempt.

For a human-friendly guided setup, run:

```powershell
evorig setup
```

For an agent-readable checklist, run:

```powershell
evorig onboard
```

or, before editable install:

```powershell
python -m evorig onboard
```

For machine-readable output:

```powershell
evorig onboard --format json
```

## Minimal User Questions

Ask these before creating the first harness unit:

1. What should this harness help an agent get better at?
2. Where will the harness be used, such as a coding-agent workflow, an app agent, research, or internal automation?
3. How should success criteria be handled?
4. How should results be validated?
5. Does a testing environment already exist, partly exist, need to be built, or is that not clear yet?

Do not turn onboarding into a long intake form. Success criteria and artifact choices are guided options, not required expertise from the user. If an answer is missing but not blocking, record an assumption and create the first baseline attempt.

EvoRig records the environment mapping. It does not discover test endpoints, MCP tools, run commands, screenshot locations, render outputs, or artifact paths by itself. The onboarding agent must inspect the actual project/environment, determine how artifacts are produced, and write that mapping into the harness.

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

## How Answers Map Into EvoRig

- Goal, success strategy, validation preference, and suggested artifacts become a target brief: `evorig target set`.
- Existing commands, MCP servers, manual steps, or custom tools become an environment contract: `evorig environment connect`.
- The first real workflow becomes an attempt plan: `evorig attempt plan`.
- Produced outputs become run artifacts: `evorig run start`, `evorig artifact add`, `evorig run finish`.
- Harness changes become candidates and require evidence before promotion.
- User defaults can be managed with `evorig settings`.
- Local harness units can be listed or registered with `evorig units`.

## Important Behavior

EvoRig does not require every task to have a direct test command. For a tool-driven setup, such as a Blender MCP server or an agent-controlled SVG rendering workflow, declare the tools and artifacts in the environment contract. The agent then writes an attempt plan for how it will use those tools, produce artifacts, inspect them, and turn observations into evidence.

If a required artifact or human judgment is delayed, use `evorig state wait`. If the unit appears to hit a capability limit, use `evorig state stop` with a concrete reason and next action.
