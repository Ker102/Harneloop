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
- `runtime/runs/run-0001/run.yaml` records the run;
- `runtime/artifacts/run-0001/` stores the copied artifact;
- promotion succeeds only after evidence is added;
- `exports/codex/AGENTS.md` contains the promoted harness instructions.

## Clean Up

```powershell
Remove-Item -Recurse -Force .\demo-artifact-unit
Remove-Item -Force .\demo-artifact.txt
```
