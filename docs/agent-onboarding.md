# Agent Onboarding

EvoRig should be understandable to an agent that has only the repository and the user's target task. The first step is not to write a validator or assume a test command exists. The first step is to collect enough context to create a baseline attempt.

Run:

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

1. What is the harness goal, and where will the harness be used?
2. What should a good result look like, and what failure patterns matter most?
3. What artifacts prove success or failure, such as renders, screenshots, files, traces, logs, or summaries?
4. Does a testing environment already exist, should the agent connect to one, or should the harness help build it?
5. What constraints, protected areas, human review points, or cost/time limits must the harness obey?

Do not turn onboarding into a long intake form. If an answer is missing but not blocking, record an assumption and create the first baseline attempt.

## How Answers Map Into EvoRig

- Goal and success criteria become a target brief: `evorig target set`.
- Existing commands, MCP servers, manual steps, or custom tools become an environment contract: `evorig environment connect`.
- The first real workflow becomes an attempt plan: `evorig attempt plan`.
- Produced outputs become run artifacts: `evorig run start`, `evorig artifact add`, `evorig run finish`.
- Harness changes become candidates and require evidence before promotion.

## Important Behavior

EvoRig does not require every task to have a direct test command. For a tool-driven setup, such as a Blender MCP server or an agent-controlled SVG rendering workflow, declare the tools and artifacts in the environment contract. The agent then writes an attempt plan for how it will use those tools, produce artifacts, inspect them, and turn observations into evidence.

If a required artifact or human judgment is delayed, use `evorig state wait`. If the unit appears to hit a capability limit, use `evorig state stop` with a concrete reason and next action.
