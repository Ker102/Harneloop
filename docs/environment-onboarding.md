# Target And Environment Onboarding

EvoRig should not assume it owns the user's test environment.

The framework should first help the agent understand:

- what task the harness is being built for;
- what counts as success;
- what artifacts should be collected;
- what failure patterns matter;
- whether a testing environment already exists.

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

Existing environments can be command-driven or tool-driven.

Command-driven means there is a direct command to run. Tool-driven means the agent performs the task through tools such as an MCP server, browser automation, a design tool plugin, or a Blender addon API.

### Assisted

Use this when part of the environment exists but missing pieces need to be identified.

The agent should propose the smallest missing setup required to run a baseline test and capture artifacts.

### Managed

Use this when EvoRig or the agent should create more of the environment from scratch.

Every infrastructure change should be explicit and evidence-backed. Managed setup is useful later, but it should not be the default for user projects that already work.

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

The first integration step is not to install Blender or create a new runner. It is to connect EvoRig to:

- the existing MCP/tool surface;
- the tools the agent should use;
- the render, screenshot, log, and scene-summary artifact paths;
- the baseline workflow for creating a scene and capturing artifacts.

Example:

```powershell
evorig environment connect .\blender-unit `
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

After this, EvoRig's role is to record runs, capture artifacts, store evidence, and promote harness changes. The Blender MCP server remains the execution interface.
