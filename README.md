# EvoRig

Temporary working name.

EvoRig is a protocol-first framework for building self-evolving agent harnesses. The first goal is not to build another eval dashboard. The goal is to give agents a structured way to attempt artifact-producing tasks, inspect what actually happened, trace failures, propose candidate harness changes, test those changes, and promote only evidence-backed improvements.

The name may change before public launch. The architecture should not depend on the name.

## Current Core

This repository starts with the generic lifecycle engine:

- create portable harness units;
- create candidate harness patches;
- keep agents inside candidate sandboxes;
- protect framework-owned control files;
- promote candidates into restorable version snapshots;
- roll back to prior snapshots;
- package thin units;
- record explicit wait, stop, and resume state.

The first demo may use Blender, but the framework core must stay task-family-neutral.

## Development Status

Private prototype. API and file formats are expected to change.

## Quick Start

From this repository:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e .
.\.venv\Scripts\evorig doctor
```

On macOS or Linux:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -e .
./.venv/bin/evorig doctor
```

You can also run without installing by setting `PYTHONPATH=src` or using your agent's equivalent environment setup.

For the guided human-facing CLI:

```powershell
evorig setup
```

For unit and preference management:

```powershell
evorig units list
evorig settings show
```

If you are an agent starting a new harness, run the onboarding checklist first:

```powershell
evorig onboard
```

Before editable install:

```powershell
python -m evorig onboard
```

The onboarding flow asks five setup questions, lists the context being collected, and maps the answers into `target`, `environment`, `attempt`, run/artifact, and evidence records. Success criteria and artifact choices are guided options; the user does not need to design validation up front. See [docs/agent-onboarding.md](docs/agent-onboarding.md).

```powershell
python -m evorig init-unit .\demo-unit --id demo-unit --name "Demo Unit"
python -m evorig candidate create .\demo-unit --summary "Add first task principle"
python -m evorig status .\demo-unit
```

List available templates:

```powershell
evorig template list
```

## Local Lifecycle Smoke Test

```powershell
evorig init-unit .\demo-unit --id demo-unit --name "Demo Unit" --template artifact-review
evorig target set .\demo-unit --task "Create and capture a simple text artifact" --success "The artifact is captured and usable as evidence." --artifact-kind text --risk "artifact is not captured"
evorig environment connect .\demo-unit --name "Local text artifact environment" --mode existing --description "Uses local shell commands for the demo." --run-command "Set-Content artifact.txt artifact output" --artifact-path artifact.txt
evorig attempt plan .\demo-unit --goal "Create and capture a text artifact" --method "Use local tools to generate the artifact and record it." --expected-artifact text --success-check "Artifact is captured in runtime artifacts."
evorig candidate create .\demo-unit --summary "Add first task principle"
New-Item -ItemType Directory -Force .\demo-unit\candidates\cand-0001\changes\agent-facing
Set-Content .\demo-unit\candidates\cand-0001\changes\agent-facing\principles.md "Inspect real artifacts before promotion."
evorig validate .\demo-unit
evorig candidate evidence add .\demo-unit cand-0001 --kind manual_review --summary "Initial smoke evidence supports promotion."
evorig promote .\demo-unit cand-0001 --version 0.1.0
evorig run start .\demo-unit --task "Create and inspect first artifact"
Set-Content .\artifact.txt "artifact output"
evorig artifact add .\demo-unit run-0001 .\artifact.txt --kind text --description "Smoke-test artifact"
evorig run finish .\demo-unit run-0001 --status succeeded --summary "Artifact captured"
evorig export .\demo-unit --adapter codex
evorig state wait .\demo-unit --reason delayed_artifact --next-action inspect_artifact --resume-condition "artifact exists"
evorig package .\demo-unit --output .\demo-unit-0.1.0.tar.gz
evorig status .\demo-unit
```

The generated unit will include `.evolve/allowed-edits.yaml`, `CURRENT_STATE.md`, and `NEXT_ACTION.md` so a coding agent can see the current lifecycle phase and edit boundaries.
Run records and copied artifacts live under `runtime/`, which is intentionally excluded from portable packages by default.

For a fuller first local demo, see [docs/demo-first-test.md](docs/demo-first-test.md).

For existing tool-driven environments such as a Blender MCP server, use `evorig environment connect --interaction-mode mcp` and declare the tools/artifact paths instead of forcing a single run command.
For custom work, use `evorig attempt plan` to record how the agent will use its own capabilities and tools to produce relevant artifacts.

Run tests:

```powershell
python -m unittest discover -s tests
```
