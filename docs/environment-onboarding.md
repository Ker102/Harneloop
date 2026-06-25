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
- What command runs the test or task?
- Where are screenshots, renders, logs, or structured summaries written?
- Which common failures should become regression cases?

## Blender Case

For the existing Blender project, the likely mode is `existing`.

The first integration step is not to install Blender or create a new runner. It is to connect EvoRig to the current project commands and artifact paths, then run a baseline attempt through EvoRig run records.
