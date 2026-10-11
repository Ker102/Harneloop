<a id="first-local-demo-test"></a>
# Primeiro teste de demonstração local

Esta demonstração usa o template genérico de revisão de artefatos. Não exige Blender.

<a id="setup"></a>
## Configuração

```powershell
uv tool install --editable .
harneloop doctor
```

<a id="run-the-demo"></a>
## Executar a demonstração

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

- a unidade contém princípios e contratos iniciais de revisão de artefatos;
- `operational-map.md` orienta o agente dentro da unidade sobre fluxo de trabalho, artefatos, evidências, caminhos de reinicialização, lacunas de capacidade, premissas e questões em aberto;
- `target/brief.yaml` descreve a finalidade do harness;
- `environment/contract.yaml` declara como o ambiente de teste é conectado;
- `attempts/attempt-0001/attempt.yaml` registra o fluxo de trabalho criado pelo agente;
- `runtime/runs/run-0001/run.yaml` registra a execução;
- `runtime/artifacts/run-0001/` armazena o artefato copiado;
- a promoção só tem sucesso após adicionar evidências;
- `exports/codex/AGENTS.md` contém as instruções promovidas do harness.

<a id="tool-driven-environment-example"></a>
## Exemplo de ambiente orientado por ferramentas

Alguns ambientes não têm um único comando de execução. Por exemplo, um agente Blender pode interagir com o Blender por meio de um servidor MCP e ferramentas de addon.

Use `--interaction-mode mcp` e declare as ferramentas:

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

Isso gera `environment/GETTING_STARTED.md`, que orienta o agente a executar uma linha de base pela interface de ferramentas e capturar artefatos no Harneloop.

Para uma tentativa com Blender MCP, crie um plano de tentativa em vez de procurar um único comando de teste:

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
## Limpeza

```powershell
Remove-Item -Recurse -Force .\demo-artifact-unit
Remove-Item -Force .\demo-artifact.txt
```
