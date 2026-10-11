<a id="target-and-environment-onboarding"></a>
# 対象と環境の導入

Harneloop がユーザーのテスト環境を所有すると想定してはいけません。

CLI が自動で環境を発見するとも示してはいけません。Harneloop は対応を保存します。導入エージェントは実環境、ツール、MCP、スクリプト、アプリのエンドポイント、出力フォルダ、成果物パスを調べ、ユニットに記録します。

現在の理解をまず `operational-map.md` に記録します。改善目標、通常の実行・リセット、有用な成果物、不安定な前提、調査が必要な点を更新してください。マップは案内であり、評価のレシピを固定するものではありません。

能力不足も記録します。操作エージェントのツールとユニット・対象環境に設計したツールは別です。制限されたエージェントには端末、ブラウザ、ファイル、MCP、パッケージ管理、視覚確認、DB、ネットワークがない場合があります。構築が阻害・弱体化するなら、不足、重要な理由、役立つツール・依存関係、代替を記録します。

フレームワークはまず次の理解を助けます：

- ハーネスを構築する対象タスク；
- 成功とみなす条件；
- 収集すべき成果物；
- 重要な失敗パターン；
- テスト環境の有無。

次に試行計画を作成します。これは決定的なテストコマンドではなく、対象タスクに関連するものを生成・確認するエージェント作成のワークフローです。

<a id="setup-modes"></a>
## 設定モード

<a id="existing"></a>
### 既存環境

動作する環境がすでにある場合に使います。

例：Blender プロジェクトにシーン実行、画面取得、ログ出力のスクリプトがすでにある。

次を記録して接続します：

- 実行コマンド；
- 成果物出力パス；
- 収集する画面、レンダリング、ログ、構造化要約；
- 環境固有の注意。

チェック失敗やユーザー要求がない限り環境を再構築しません。

反復する手作業を減らします。サービス再起動、アプリリセット、成果物収集、環境準備が安全に自動化できれば実装・記録します。危険、不明、高額な場合は確認します。

能力追加は証拠で支えます。低リスクのローカルツールは環境が許せば導入・有効化・構築できます。大きな依存、認証情報、有料 API、外部アクセス、ユーザー所有アカウント、ネット拡張、安全変更は先に提案します。

管理・支援設定は全要素をゼロから作る要求ではありません。プロジェクト内や、有用なら外部文書、OSS ツール、スキル、ライブラリ、バリデーター、データ、例、過去のハーネスを調べます。期待結果を改善したり不要な実装を省けるなら維持された解決策を優先します。出典、関連版、目的、ライセンス・帰属、互換性、測定した貢献を記録します。第三者実行物を確認し、リスク、費用、認証、外部アクセス、安全の通常の許可境界を守ります。

既存環境はコマンド駆動またはツール駆動にできます。

コマンド駆動は直接実行するコマンドがあること、ツール駆動は MCP、ブラウザ自動化、デザインプラグイン、Blender アドオン API などで作業することです。

<a id="assisted"></a>
### 支援付き

一部があり、不足を特定する必要がある場合に使います。

ベースラインテストと成果物収集に必要な最小の不足設定を提案します。

<a id="managed"></a>
### 管理型

Harneloop やエージェントが環境のより多くを新規構築する場合に使います。

インフラ変更は明示し、証拠で支えます。管理型設定は後で有用ですが、すでに動くプロジェクトの既定にしないでください。

<a id="attempt-plans"></a>
## 試行計画

多くのタスクは `run this command` には還元できません。

対象エージェントは次を必要とする場合があります：

- MCP ツールを使う；
- ファイルを編集する；
- シーンを作る；
- UI を構築する；
- ブラウザを実行する；
- モデルに成果物生成を依頼する；
- 出力を視覚的に確認する；
- 構造化要約を出力する；
- 重要な追加証拠を判断する。

Harneloop は試行計画として記録します：

```powershell
harneloop attempt plan .\unit `
  --goal "Build a Blender scene with a cube on a table." `
  --method "Use Blender MCP tools to create objects, render, and export scene summary." `
  --action "Create table, cube, camera, and light." `
  --action "Render and capture screenshot." `
  --expected-artifact render `
  --expected-artifact scene_summary `
  --success-check "Cube rests on table." `
  --success-check "Objects are visible to camera."
```

次に実行でその試行を参照できます：

```powershell
harneloop run start .\unit --task "Baseline Blender spatial scene" --attempt-id attempt-0001
```

成果物を集めた後、観察を追加します：

```powershell
harneloop attempt observe .\unit attempt-0001 `
  --run-id run-0001 `
  --outcome failed `
  --summary "Render exists but cube floats above the table." `
  --finding "Likely z-coordinate placement issue."
```

観察は候補証拠や回帰ケースにできます。

<a id="agent-questions"></a>
## エージェントの質問

実際のハーネス開始時は不足情報だけ尋ねます：

- 対象タスク群は何か？
- 重要な出力成果物は何か？
- 動作するテスト環境はあるか？
- コマンド、ツール、手動、独自方式のどれか？
- コマンド駆動なら、何でテスト・タスクを実行するか？
- ツール駆動なら、どのツールを使うか？
- 画面、レンダリング、ログ、構造化要約の保存先は？
- 回帰ケースにする一般的な失敗は？

<a id="blender-case"></a>
## Blender の例

既存 Blender プロジェクトのモードはおそらく `existing` です。

対話モードは `mcp` で、`command` ではない場合があります。

直接テストコマンドがない場合があります。対象エージェントは Blender MCP とアドオンで、シーン変更、画像レンダリング、画面取得、オブジェクト確認、シーン要約出力を行います。

最初は Blender の導入や新しいランナー作成ではなく、次への接続です：

- 既存 MCP・ツールインターフェース；
- エージェントが使うべきツール；
- レンダリング、画面、ログ、シーン要約のパス；
- シーン作成・成果物取得のベースライン手順。

例：

```powershell
harneloop environment connect .\blender-unit `
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

以後 Harneloop は実行記録、成果物収集、証拠保存、ハーネス変更の昇格を担います。実行インターフェースは引き続き Blender MCP です。
