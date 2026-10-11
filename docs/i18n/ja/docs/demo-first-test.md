<a id="first-local-demo-test"></a>
# 最初のローカルデモテスト

このデモは汎用の成果物レビュー用テンプレートを使います。Blender は不要です。

<a id="setup"></a>
## セットアップ

```powershell
uv tool install --editable .
harneloop doctor
```

<a id="run-the-demo"></a>
## デモの実行

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

期待される結果：

- ユニットに成果物レビューの初期原則と契約が含まれる；
- `operational-map.md` がワークフロー、成果物、証拠、リセット手順、能力不足、前提、未解決の疑問についてユニット内の状況を示す；
- `target/brief.yaml` がハーネスの目的を記述する；
- `environment/contract.yaml` がテスト環境との接続方法を宣言する；
- `attempts/attempt-0001/attempt.yaml` がエージェント作成のワークフローを記録する；
- `runtime/runs/run-0001/run.yaml` が実行を記録する；
- `runtime/artifacts/run-0001/` がコピー済み成果物を保存する；
- 証拠を追加した後でのみ昇格が成功する；
- `exports/codex/AGENTS.md` に昇格済みのハーネス指示が含まれる。

<a id="tool-driven-environment-example"></a>
## ツール駆動環境の例

単一の実行コマンドがない環境もあります。例えば Blender エージェントは MCP サーバーやアドオンツールを通じて Blender とやり取りできます。

`--interaction-mode mcp` を使い、ツールを宣言します：

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

これで `environment/GETTING_STARTED.md` が生成され、ツールを使ってベースラインを実行し、成果物を Harneloop に収集するようエージェントに指示します。

Blender MCP の試行では、単一のテストコマンドを探すのではなく試行計画を作成します：

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
## クリーンアップ

```powershell
Remove-Item -Recurse -Force .\demo-artifact-unit
Remove-Item -Force .\demo-artifact.txt
```
