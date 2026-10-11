<a id="first-local-demo-test"></a>
# Primera prueba de demostración local

Esta demostración usa la plantilla genérica de revisión de artefactos. No requiere Blender.

<a id="setup"></a>
## Preparación

```powershell
uv tool install --editable .
harneloop doctor
```

<a id="run-the-demo"></a>
## Ejecutar la demostración

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

Resultado esperado:

- la unidad contiene principios y contratos iniciales de revisión de artefactos;
- `operational-map.md` orienta al agente dentro de la unidad sobre flujo de trabajo, artefactos, evidencia, restablecimiento, capacidades ausentes, supuestos y preguntas abiertas;
- `target/brief.yaml` describe el propósito del harness;
- `environment/contract.yaml` declara cómo se conecta el entorno de pruebas;
- `attempts/attempt-0001/attempt.yaml` registra el flujo de trabajo diseñado por el agente;
- `runtime/runs/run-0001/run.yaml` registra la ejecución;
- `runtime/artifacts/run-0001/` almacena el artefacto copiado;
- la promoción solo tiene éxito después de añadir evidencia;
- `exports/codex/AGENTS.md` contiene las instrucciones promovidas del harness.

<a id="tool-driven-environment-example"></a>
## Ejemplo de entorno basado en herramientas

Algunos entornos no tienen un único comando de ejecución. Por ejemplo, un agente Blender puede interactuar con Blender mediante un servidor MCP y herramientas del complemento.

Usa `--interaction-mode mcp` y declara las herramientas:

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

Esto genera `environment/GETTING_STARTED.md`, que indica al agente que ejecute una línea base mediante las herramientas y capture artefactos en Harneloop.

Para un intento con Blender MCP, crea un plan de intento en lugar de buscar un único comando de pruebas:

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
## Limpieza

```powershell
Remove-Item -Recurse -Force .\demo-artifact-unit
Remove-Item -Force .\demo-artifact.txt
```
