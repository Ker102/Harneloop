# Target And Environment Onboarding

Harneloop should not assume it owns the user's test environment.

It also should not imply that the CLI can discover the environment automatically. Harneloop stores the mapping. The onboarding agent must inspect the real workspace, tools, MCP servers, scripts, app endpoints, output folders, and artifact paths, then write that mapping into the harness unit.

The first place for that working understanding is `operational-map.md`. Keep it current with what the harness unit is trying to improve, how the environment is usually run or reset, what artifacts are useful, which assumptions are fragile, and what still needs investigation. The map should orient the agent, not lock it into one evaluation recipe.

Also keep capability gaps in the map. The tools available to the operating agent are separate from the tools designed into the harness unit or target-agent environment. A restricted agent may not have terminal, browser, filesystem, MCP, package-manager, visual-inspection, database, or network capabilities. If a missing operating capability blocks or weakens the harness-building loop, record what is missing, why it matters, which tool or dependency would help, and what fallback exists.

The framework should first help the agent understand:

- what task the harness is being built for;
- what counts as success;
- what artifacts should be collected;
- what failure patterns matter;
- whether a testing environment already exists.

After that, the agent creates an attempt plan. An attempt plan is not a deterministic test command. It is an agent-authored workflow for producing and inspecting something relevant to the target task.

## Setup Modes

### Existing

Use this when the user already has a working environment.

Example: a Blender project already has scripts for running scenes, taking screenshots, and exporting logs.

The agent should connect to it by documenting:

- the run command;
- artifact output paths;
- screenshots, renders, logs, or structured summaries to collect;
- any environment-specific notes.

The agent should not rebuild the environment unless checks fail or the user asks.

The agent should try to remove repeated manual work from the loop. If restarting services, resetting apps, collecting artifacts, or preparing the environment can be automated safely, implement or document that automation. If the automation path is risky, unclear, or expensive, ask the user.

Capability additions should be evidence-backed. Low-risk local tooling can be installed, enabled, or built when the environment allows it. Larger dependencies, credentials, paid APIs, external access, user-owned accounts, network expansion, or security-impacting changes should be proposed first.

Existing environments can be command-driven or tool-driven.

Command-driven means there is a direct command to run. Tool-driven means the agent performs the task through tools such as an MCP server, browser automation, a design tool plugin, or a Blender addon API.

### Assisted

Use this when part of the environment exists but missing pieces need to be identified.

The agent should propose the smallest missing setup required to run a baseline test and capture artifacts.

### Managed

Use this when Harneloop or the agent should create more of the environment from scratch.

Every infrastructure change should be explicit and evidence-backed. Managed setup is useful later, but it should not be the default for user projects that already work.

## Attempt Plans

Many harness tasks cannot be reduced to `run this command`.

The target agent may need to:

- use MCP tools;
- edit files;
- create scenes;
- build UI;
- run a browser;
- ask a model to generate an artifact;
- visually inspect output;
- export structured summaries;
- decide what follow-up evidence matters.

Harneloop records this as an attempt plan:

```powershell
harneloop attempt plan .\unit `
  --goal "Build a Blender scene with a cube on a table." `
  --method "Use Blender MCP tools to create objects, render, and export scene summary." `
  --action "Create table, cube, camera, and light." `
  --action "Render and capture screenshot." `
  --expected-artifact render `
  --expected-artifact scene_summary `
  --success-check "Cube rests on table." `
  --success-check "Objects are visible to camera."
```

Then a run can reference that attempt:

```powershell
harneloop run start .\unit --task "Baseline Blender spatial scene" --attempt-id attempt-0001
```

After artifacts are captured, observations are added:

```powershell
harneloop attempt observe .\unit attempt-0001 `
  --run-id run-0001 `
  --outcome failed `
  --summary "Render exists but cube floats above the table." `
  --finding "Likely z-coordinate placement issue."
```

Those observations can then become candidate evidence or regression cases.

## Agent Questions

When starting a real harness, the agent should ask only for missing information:

- What is the target task family?
- What output artifacts matter?
- Do you already have a working test environment?
- Is the environment command-driven, tool-driven, manual, or custom?
- If command-driven: what command runs the test or task?
- If tool-driven: what tools does the agent use?
- Where are screenshots, renders, logs, or structured summaries written?
- Which common failures should become regression cases?

## Blender Case

For the existing Blender project, the likely mode is `existing`.

The interaction mode may be `mcp`, not `command`.

In that case there may be no direct test command. The target agent uses the Blender MCP server and addon tools to change the scene, render images, take screenshots, inspect objects, or export scene summaries.

The first integration step is not to install Blender or create a new runner. It is to connect Harneloop to:

- the existing MCP/tool surface;
- the tools the agent should use;
- the render, screenshot, log, and scene-summary artifact paths;
- the baseline workflow for creating a scene and capturing artifacts.

Example:

```powershell
harneloop environment connect .\blender-unit `
  --name "Existing Blender MCP environment" `
  --mode existing `
  --interaction-mode mcp `
  --description "Agent interacts with Blender through an MCP server and addon tools." `
  --tool create_object `
  --tool render_scene `
  --tool capture_screenshot `
  --tool export_scene_summary `
  --artifact-path "outputs/renders/*.png" `
  --note "Use MCP tools instead of looking for a single run command."
```

After this, Harneloop's role is to record runs, capture artifacts, store evidence, and promote harness changes. The Blender MCP server remains the execution interface.
