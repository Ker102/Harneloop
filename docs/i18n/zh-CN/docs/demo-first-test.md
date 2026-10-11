<a id="first-local-demo-test"></a>
# 首次本地演示测试

此演示使用通用产物审查模板，不需要 Blender。

<a id="setup"></a>
## 设置

```powershell
uv tool install --editable .
harneloop doctor
```

<a id="run-the-demo"></a>
## 运行演示

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

预期结果：

- harness 单元包含预置的产物审查原则和契约；
- `operational-map.md` 为代理提供单元内的工作流、产物、证据、重置路径、能力缺口、假设和未决问题导航；
- `target/brief.yaml` 描述 harness 的用途；
- `environment/contract.yaml` 声明测试环境的连接方式；
- `attempts/attempt-0001/attempt.yaml` 记录代理编写的工作流；
- `runtime/runs/run-0001/run.yaml` 记录运行；
- `runtime/artifacts/run-0001/` 保存复制的产物；
- 添加证据后才能成功提升；
- `exports/codex/AGENTS.md` 包含已提升的 harness 指令。

<a id="tool-driven-environment-example"></a>
## 工具驱动环境示例

有些环境没有单一运行命令。例如，Blender 代理可通过 MCP 服务器和插件工具与 Blender 交互。

使用 `--interaction-mode mcp` 并声明工具：

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

这会生成 `environment/GETTING_STARTED.md`，指示代理通过工具接口执行基线，并将产物捕获到 Harneloop 中。

对于 Blender MCP 尝试，应创建尝试计划，而不是寻找单一测试命令：

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
## 清理

```powershell
Remove-Item -Recurse -Force .\demo-artifact-unit
Remove-Item -Force .\demo-artifact.txt
```
