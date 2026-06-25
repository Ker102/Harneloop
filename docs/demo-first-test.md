# First Local Demo Test

This demo uses the generic artifact-review template. It does not require Blender.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e .
.\.venv\Scripts\evorig doctor
```

## Run The Demo

```powershell
$unit = Join-Path $PWD "demo-artifact-unit"
$artifact = Join-Path $PWD "demo-artifact.txt"

.\.venv\Scripts\evorig init-unit $unit --id demo-artifact --name "Demo Artifact Unit" --template artifact-review
.\.venv\Scripts\evorig target set $unit --task "Create and capture a simple text artifact" --success "The artifact exists, is copied into runtime artifacts, and can be used as promotion evidence." --artifact-kind text --risk "artifact is not captured"
.\.venv\Scripts\evorig environment connect $unit --name "Local text artifact smoke environment" --mode existing --description "Uses local PowerShell commands to create a text artifact." --run-command "Set-Content demo-artifact.txt artifact output" --artifact-path "demo-artifact.txt" --note "This demo uses an existing local shell environment."
.\.venv\Scripts\evorig run start $unit --task "Create and capture a simple text artifact"
Set-Content -Path $artifact -Value "artifact output"
.\.venv\Scripts\evorig artifact add $unit run-0001 $artifact --kind text --description "Demo text artifact"
.\.venv\Scripts\evorig run finish $unit run-0001 --status succeeded --summary "Artifact captured"

.\.venv\Scripts\evorig candidate create $unit --summary "Add artifact inspection principle"
New-Item -ItemType Directory -Force (Join-Path $unit "candidates\cand-0001\changes\agent-facing") | Out-Null
Set-Content -Path (Join-Path $unit "candidates\cand-0001\changes\agent-facing\demo-principle.md") -Value "Always inspect captured artifacts before deciding success."
.\.venv\Scripts\evorig candidate evidence add $unit cand-0001 --kind artifact_review --summary "The run captured the expected text artifact." --run-id run-0001 --artifact-id artifact-0001
.\.venv\Scripts\evorig promote $unit cand-0001 --version 0.1.0

.\.venv\Scripts\evorig export $unit --adapter codex
.\.venv\Scripts\evorig status $unit --format markdown
```

Expected result:

- the unit contains seeded artifact-review principles and contracts;
- `target/brief.yaml` describes what the harness is for;
- `environment/contract.yaml` declares how the test environment is connected;
- `runtime/runs/run-0001/run.yaml` records the run;
- `runtime/artifacts/run-0001/` stores the copied artifact;
- promotion succeeds only after evidence is added;
- `exports/codex/AGENTS.md` contains the promoted harness instructions.

## Tool-Driven Environment Example

Some environments do not have a single run command. For example, a Blender agent may interact with Blender through an MCP server and addon tools.

Use `--interaction-mode mcp` and declare the tools:

```powershell
.\.venv\Scripts\evorig environment connect $unit `
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

This generates `environment/GETTING_STARTED.md`, which tells the agent to run a baseline through the tool surface and capture artifacts into EvoRig.

## Clean Up

```powershell
Remove-Item -Recurse -Force .\demo-artifact-unit
Remove-Item -Force .\demo-artifact.txt
```
