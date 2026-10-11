<a id="first-local-demo-test"></a>
# Premier test de démonstration locale

Cette démonstration utilise le modèle générique de revue d’artefacts. Elle ne nécessite pas Blender.

<a id="setup"></a>
## Installation

```powershell
uv tool install --editable .
harneloop doctor
```

<a id="run-the-demo"></a>
## Exécuter la démonstration

```powershell
$unit = Join-Path $PWD "demo-artifact-unit"
$artifact = Join-Path $PWD "demo-artifact.txt"

harneloop init-unit $unit --id demo-artifact --name "Demo Artifact Unit" --template artifact-review
harneloop target set demo-artifact --task "Create and capture a simple text artifact" --success "The artifact exists, is copied into runtime artifacts, and can be used as promotion evidence." --artifact-kind text --risk "artifact is not captured"
harneloop environment connect demo-artifact --name "Local text artifact smoke environment" --mode existing --description "Uses local PowerShell commands to create a text artifact." --run-command "Set-Content demo-artifact.txt artifact output" --artifact-path "demo-artifact.txt" --note "This demo uses an existing local shell environment."
harneloop attempt plan demo-artifact --goal "Create and capture a simple text artifact" --method "Use local shell commands to create an artifact, then capture it into Harneloop." --action "Write a text file." --action "Add it as a run artifact." --expected-artifact text --success-check "The artifact is present in runtime artifacts."
harneloop run start demo-artifact --task "Create and capture a simple text artifact" --attempt-id attempt-0001
Set-Content -Path $artifact -Value "artifact output"
harneloop artifact add demo-artifact run-0001 $artifact --kind text --description "Demo text artifact"
harneloop run finish demo-artifact run-0001 --status succeeded --summary "Artifact captured"
harneloop attempt observe demo-artifact attempt-0001 --run-id run-0001 --outcome succeeded --summary "The expected text artifact was captured." --finding "Artifact capture path is working."

harneloop candidate create demo-artifact --summary "Add artifact inspection principle" --plane target_harness --validation-tier targeted
New-Item -ItemType Directory -Force (Join-Path $unit "candidates\cand-0001\changes\agent-facing") | Out-Null
Set-Content -Path (Join-Path $unit "candidates\cand-0001\changes\agent-facing\demo-principle.md") -Value "Always inspect captured artifacts before deciding success."
harneloop candidate evidence add demo-artifact cand-0001 --kind artifact_review --summary "The run captured the expected text artifact." --run-id run-0001 --artifact-id artifact-0001
harneloop candidate stage demo-artifact cand-0001 ready
harneloop promote demo-artifact cand-0001 --version 0.1.0

harneloop export demo-artifact --adapter codex
harneloop status demo-artifact --format markdown
```

Résultat attendu :

- l’unité contient les principes et contrats initiaux de revue d’artefacts ;
- `operational-map.md` oriente l’agent dans l’unité sur le workflow, les artefacts, les preuves, les réinitialisations, les capacités manquantes, les hypothèses et les questions ouvertes ;
- `target/brief.yaml` décrit la finalité du harness ;
- `environment/contract.yaml` déclare la connexion de l’environnement de test ;
- `attempts/attempt-0001/attempt.yaml` consigne le workflow rédigé par l’agent ;
- `runtime/runs/run-0001/run.yaml` consigne l’exécution ;
- `runtime/artifacts/run-0001/` stocke l’artefact copié ;
- la promotion ne réussit qu’après l’ajout de preuves ;
- `exports/codex/AGENTS.md` contient les instructions promues du harness.

<a id="tool-driven-environment-example"></a>
## Exemple d’environnement piloté par outils

Certains environnements n’ont pas de commande d’exécution unique. Par exemple, un agent Blender peut interagir avec Blender via un serveur MCP et les outils d’un addon.

Utilisez `--interaction-mode mcp` et déclarez les outils :

```powershell
harneloop environment connect demo-artifact `
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

Cela génère `environment/GETTING_STARTED.md`, qui indique à l’agent d’exécuter une référence via les outils et de capturer les artefacts dans Harneloop.

Pour une tentative Blender MCP, créez un plan de tentative plutôt que de chercher une commande de test unique :

```powershell
harneloop attempt plan demo-artifact `
  --goal "Build a Blender scene with a cube on a table and a visible camera view." `
  --method "Use Blender MCP tools to create objects, render, and export scene summary." `
  --action "Create table, cube, camera, and light with MCP tools." `
  --action "Render the scene and capture a screenshot." `
  --action "Export object transforms and camera visibility summary." `
  --expected-artifact render `
  --expected-artifact screenshot `
  --expected-artifact scene_summary `
  --success-check "Cube rests on table." `
  --success-check "All required objects are visible to camera."
```

<a id="clean-up"></a>
## Nettoyage

```powershell
Remove-Item -Recurse -Force .\demo-artifact-unit
Remove-Item -Force .\demo-artifact.txt
```
