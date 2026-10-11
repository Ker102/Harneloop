<div align="center">

<h1><img src="../../assets/harneloop-mark.svg" alt="" width="56" height="56" align="absmiddle" /> Harneloop</h1>

<p>AI エージェントのための、成果物を考慮したハーネス進化。</p>

<p><a href="https://harneloop.kaelux.dev/">ウェブサイト</a> · <a href="#agent-quick-start">クイックスタート</a> · <a href="#documentation">ドキュメント</a></p>

</div>

<!-- i18n-switcher:start -->
[English](../../../README.md) | [Español](../es/README.md) | [简体中文](../zh-CN/README.md) | [Français](../fr/README.md) | 日本語 | [Deutsch](../de/README.md) | [Português (Brasil)](../pt-BR/README.md)
<!-- i18n-switcher:end -->

**AI エージェントが失敗から学べるようにします。**

エージェントはタスクを終え、成功したと報告しても、壊れたコード、質の低いレンダリング、動かないワークフローを残すことがあります。Harneloop は既存のエージェントに、結果を調べ、行動を振り返り、原因と思われる誤りを見つけ、よりよい方法を試すための構造を提供します。

エージェントが改善するのは **ハーネス**、つまりモデルを取り巻く指示、ツール、コンテキスト、チェックです。モデル自体の再学習は不要です。提案された変更は、テストで裏付けられて初めて作業用の版になります。

<a id="what-can-you-use-it-for"></a>
## どんな用途に使えるか

エージェントが似た失敗を繰り返し、その出力を確認できるときに Harneloop を使います。コードとテスト、ブラウザ操作、生成文書、視覚タスクなどが対象です。最初の公開事例は ViperMesh による Blender シーン構築で、他のタスク群は今後の検証や貢献の対象です。

<a id="how-it-works"></a>
## 仕組み

1. **タスクを試します。** 出力とエージェントの手順を保存します。
2. **結果を調べます。** 完了報告を信じるのではなく成果物自体を確認します。
3. **振り返ります。** 問題をツール呼び出し、足りないコンテキスト、指示、環境の判断に結び付けます。
4. **改善を試します。** エージェントに変更を提案させ、関連チェックを再実行します。
5. **有効なものを残します。** 裏付けられた改善と復元可能な版を保存します。

<p align="center">
  <a href="https://harneloop.kaelux.dev/media/harneloop-how-it-works.mp4">
    <img src="https://harneloop.kaelux.dev/media/harneloop-video-poster.png" alt="Harneloop の仕組みを見る：目標から再利用可能なハーネスへ" width="900" />
  </a>
</p>

<p align="center"><a href="https://harneloop.kaelux.dev/media/harneloop-how-it-works.mp4"><img src="../../assets/readme-play.svg" alt="" width="18" height="18" align="absmiddle" /> Harneloop の仕組みを見る - 3:40</a></p>

各タスク群には **ハーネスユニット** があります。目標、ツール、試行、証拠、改善をまとめるポータブルなワークスペースです。一時停止して後で再開しても、調査を最初からやり直す必要はありません。

<a id="try-harneloop"></a>
## Harneloop を試す

隔離したツール環境で [PyPI からインストール](https://pypi.org/project/harneloop/)します：

```bash
uv tool install harneloop
harneloop setup
```

Python 環境で `python -m pip install harneloop` を使うこともできます。要件とソースからのインストールは[インストールと開始](#install-and-start)を参照してください。

その後、必要な能力を持つエージェントにリポジトリのリンクと改善対象のタスクを渡します。[エージェント向けクイックスタート](#agent-quick-start)には、そのまま使えるプロンプトがあります。

**状態：**公開アルファ。コアループは動作しており、より幅広いタスクの検証や貢献を歓迎します。[問題の報告や用途の共有](https://github.com/Ker102/Harneloop/issues)。

<a id="evidence-from-a-real-case-study"></a>
## 実際の事例による証拠

Harneloop は、Blender の空間推論とシーン構築用に、カスタムの ViperMesh ハーネスユニットを開発する際に使われました。比較では実行モデルを **GPT-5.5 High** に固定し、進化した ViperMesh ハーネスを **Anthropic x Blender MCP server baseline** と比較しました。主に変更したシステム層をハーネスに限定しています。

- 比較可能な実タスク **7 件中 6 件**で ViperMesh が速く、**平均 2.534x の高速化**でした。
- 中立 LLM による予備的な視覚評価は、7 組の実レンダリングで **8.19 ポイント**改善しました。
- 比較可能な 7 件のベンチマークで、実行エージェントの総トークン使用量は **90.91% 少なく**、合計約 **175K 対 1.9M tokens**でした。

Harneloop 自体がシーンを生成したわけではありません。弱点を明らかにし、ツールとハーネスの開発を導き、ベンチマークが改善したか検証する証拠・成果物のループを構造化しました。方法、制限、全結果は [ViperMesh の事例](https://kristoferjussmann.me/case-studies/vipermesh)を参照してください。

これらは、成果物の多い実際のエージェント環境で Harneloop のプロセスが機能することを示す直接的な実証です。実行モデルは同じまま、進化したハーネスで速度、視覚性能、トークン効率に測定可能な改善が得られました。

<a id="demonstration-vipermesh-mcp"></a>
### デモ：ViperMesh MCP

[ViperMesh MCP を使った Harneloop のデモを見る](https://www.youtube.com/watch?v=bs74QJ6UD5E&t=2s)。

Blender シーン構築は、エージェントの出力を調べて、そのツールと指示を改善する具体例です。フレームワークは [Harneloop の事例](https://kristoferjussmann.me/case-studies/harneloop/#harneloop-demo)、測定結果は [ViperMesh のベンチマーク研究](https://kristoferjussmann.me/case-studies/vipermesh/)を参照してください。[公開 Blender コネクター](https://github.com/Ker102/vipermesh-blender)は、完全なスタジオおよびベンチマーク対象ハーネスとは別に提供されています。

<a id="start-here"></a>
## ここから始める

- **エージェント経由で使う：**[エージェント向けクイックスタート](#agent-quick-start)
- **自分でインストール：**[インストールと開始](#install-and-start)
- **ユニットを理解：**[ハーネスユニットとは](#what-is-a-harness-unit)
- **ループを理解：**[ライフサイクルを簡単に](#the-lifecycle-made-simple)
- **測定による裏付け：**[ViperMesh の事例](https://kristoferjussmann.me/case-studies/vipermesh)
- **実環境を接続：**[環境の設定](#environment-setup)
- **既定値を変更：**[設定](#configuration)
- **技術アーキテクチャ：**[コアライフサイクル](docs/architecture/core-lifecycle.md)、[ランタイム層](docs/architecture/runtime-layers.md)、[並行処理](docs/architecture/concurrency.md)
- **エージェント向け完全な指示：**[エージェントの導入](docs/agent-onboarding.md)
- **プロセス図：**[仕組み](#how-it-works)、[編集可能なコンパクト図](docs/framework-process-compact.md)、[詳細なフレームワーク図](docs/framework-process.md)

<a id="why-harneloop-exists"></a>
## Harneloop が存在する理由

モデルが同じ失敗を繰り返すのは、試行から得た有用な教訓が、検証済みの作業環境の一部にならないことが多いためです。プロンプトを長くしたり評価スコアを集めたりするだけでは、問題全体は解決しません。

モデルはエージェント性能の一部にすぎません。ハーネスが、見るコンテキスト、使えるツール、環境とのやり取り、記憶、結果の確認方法、失敗を持続的な改善にできるかを決めます。多くのタスク固有の問題では、ハーネスが最も効果的な改善対象になります。モデルを再学習せず大きく改善でき、各変更を確認、テスト、復元、移植できます。

Harneloop はこの作業を構造化し、効率化します。一回限りのプロンプト修正を積み重ねるのではなく、複数の独立ユニットを開発し、実際の試行で変更を検証し、証拠と履歴を残して、成功した各ハーネスをまとまったパッケージとして継続・エクスポートできます。

Harneloop は操作エージェントに制御された改善ループを提供します：

- 合成ベンチマークだけでなく実際のタスクに取り組む；
- レンダリング、スクリーンショット、ファイル、トレース、ログ、構造化状態などの成果物を収集する；
- 成果物を視覚、構造、動作の観点で調べる；
- 弱い結果の原因を指示、ツール、コンテキスト、検索、環境、モデルの限界まで追跡する；
- 改善を独立した候補パッチとして開発する；
- 新しい試行と回帰ケースで候補を検証する；
- 有効な証拠に支えられた変更だけを昇格する；
- 復元可能な版を保存し、完成したハーネスを再利用用にパッケージ化する。

エージェントはハーネスのワークスペース内で自由に推論・実験できます。Harneloop は、記録、保護された状態、証拠、昇格、スナップショット、ロールバック、パッケージ化という整合性に関わる境界を管理します。

<details>
<summary>研究背景：なぜ重みより先にハーネスを改善するのか</summary>

<a id="why-improve-the-harness-before-the-weights"></a>
### なぜ重みより先にハーネスを改善するのか

エージェントのインターフェース、検索、ツール、反復フィードバックの研究は、モデルの重みを変えずに周辺システムを変えることで性能を大きく改善できると示しています。コンテキスト、検索、ツール、フィードバック、環境とのやり取りが主なボトルネックのタスクでは、ハーネス層の方法はモデルの汎用能力を維持しつつ、ファインチューニングを上回る場合があり、その差が大きいこともあります。Harneloop はハーネス構築時の実際の問題から生まれました。以下の研究は独立にこの方向性を支持しています：

- [Self-Harness](https://arxiv.org/abs/2606.09498) は、エージェントが実行トレースから弱点を発見し、ハーネス変更を提案して回帰テストで検証し、3 つのモデル群でホールドアウトの合格率を改善できると示しました。
- [SWE-agent](https://arxiv.org/abs/2405.15793) は、専用のエージェント・コンピューターインターフェースにより、言語モデルのリポジトリ探索、コード編集、テスト実行が大きく改善すると示しました。
- [Reflexion](https://arxiv.org/abs/2303.11366) は重み更新ではなく、試行錯誤、言語によるフィードバック、エピソード記憶でエージェントを改善しました。
- [Self-Refine](https://arxiv.org/abs/2303.17651) は、追加学習なしの反復フィードバックと修正により、評価した 7 タスクで平均約 20 パーセントポイントの絶対改善を報告しました。
- [Fine-Tuning or Retrieval?](https://aclanthology.org/2024.emnlp-main.15/) は、評価した既存・新規知識の注入タスクで、RAG が教師なしファインチューニングを一貫して上回ったと示しました。
- [Does Fine-Tuning LLMs on New Knowledge Encourage Hallucinations?](https://arxiv.org/abs/2405.05904) は、教師ありファインチューニングで新しい事実知識を獲得することが難しく、学習に伴って幻覚が増えると示しました。

ViperMesh の事例と合わせ、実用的な方針を支持します。**まずハーネスを最適化して結果を測定し、その有効な限界に達したと証拠が示す場合にだけモデルの重みを変更します。** ハーネス変更は確認、取り消し、再利用、検証が速く、適したタスクではベースモデルを恒久的に変えず、重み変更以上の効果を出せる場合があります。

ハーネスがあらゆるファインチューニング手法を常に上回るという証明ではありません。動作、スタイル、レイテンシー、専門的な表現、推論時には有効に提供できない能力にはファインチューニングが有用な場合があります。強いハーネスと適切なファインチューニングは相互補完もできます。

</details>

<a id="what-is-a-harness-unit"></a>
## ハーネスユニットとは

**ハーネスユニット**は、1 つのタスク群を改善するポータブルなワークスペースです。各ユニットは独立に発展し、独自の対象定義、環境マップ、ハーネス素材、実験、証拠、回帰ケース、昇格済み版を保持します。

新しいユニットは次の構成で始まります：

```text
my-harness-unit/
  unit.yaml                 identity and current version
  UNIT_AGENT.md             instructions for agents entering the unit
  operational-map.md        current understanding of tools, artifacts, and workflow
  target/                   task goal and suggested first tests
  environment/              contract for commands, MCP tools, apps, and artifact paths
  agent-facing/             promoted instructions and context
  tools/                    unit-specific helper tools
  observers/                ways to inspect outputs
  validators/               deterministic or agent-driven checks
  regression-cases/         failures that future candidates should not repeat
  candidates/               isolated proposed harness changes
  runtime/                  local runs and captured artifacts
  versions/                 restorable promoted snapshots
  provenance/               human-readable change history
```

これは制限的なテンプレートではありません。調査、スクリプト、検索データ、インフラ宣言、記憶、独自オブザーバー、新しいフォルダも追加できます。フレームワークはユニットを理解・復元可能に保つためのファイルとライフサイクル規則だけを保護します。

<a id="portable-unit-versus-local-working-data"></a>
### ポータブルユニットとローカル作業データ

再利用可能なハーネス素材はポータブルユニットに含めます。生のトレース、一時的な実験、キャッシュ、秘密情報、未昇格候補、過去のすべてのレンダリングは含めません。

既定の `thin` パッケージには、ハーネスの再構築や統合に必要な昇格済み知識と契約が含まれます。将来のプロファイルが明示的に含める場合を除き、実行時の証拠はローカルに残ります。

<a id="the-lifecycle-made-simple"></a>
## ライフサイクルを簡単に

1. **目標を述べます。** ユーザーがエージェントに何を改善してほしいか説明します。
2. **環境を対応付けます。** 操作エージェントが実際のタスクの実行方法と証拠の取得先を調べます。
3. **前提を整理します。** 初回の実行前に重要なコンテキストを確認、委任、または推論と明示します。
4. **ベースラインを実行します。** ハーネスを変更する前にタスクを試します。
5. **確認して結論を出します。** 成果物を評価し、受け入れ、変更、再実行、入力要求、停止を明示します。
6. **必要なら候補を作成・拡張します。** 関連変更を独立したまとまりに集め、別の問題には並行候補を使えます。
7. **リスクに応じて検証します。** 構造、対象限定、代表的、完全なチェックを使い証拠を添付します。
8. **昇格、修正、待機、停止を選びます。** 裏付けのある改善を版にし、弱い候補は修正または却下します。
9. **エクスポートまたはパッケージ化します。** 昇格済みハーネスをコーディングエージェント、アプリエージェント、互換環境へ適用できます。

終了済み実行は不変です。候補の証拠は添付時と昇格時に再確認されるため、削除済み実行、欠落した成果物や証拠ファイルではリリースを支えられません。

候補はコミットごとの包装ではありません。設定やツールの候補は関連変更を集め、絞ったスモークテストを受けられます。動作変更には実成果物の試行と回帰が必要な場合があります。対象ハーネス、評価、インフラは独立に進められます。1 つが昇格したら旧ベースの並行候補はリベースし、新しい証拠を作ってから昇格します。

README 上部の動画でループを説明しています。[コンパクト版](docs/framework-process-compact.md)には編集可能な Mermaid 図があります。[詳細図](docs/framework-process.md)は能力不足、人の入力、待機、停止、成果物を考慮したループ全体を示します。

<a id="what-makes-it-different"></a>
## 他との違い

<a id="artifact-aware"></a>
### <img src="../../assets/readme-observe.svg" alt="" width="18" height="18" align="absmiddle" /> 成果物を考慮

Harneloop は生成物そのものを証拠とします。自分の文章による報告を信じるのではなく、画像、シーン、UI、文書、生成リポジトリ、実行トレース、DB 状態などの有用な出力を確認できます。

<a id="harness-building-not-only-scoring"></a>
### <img src="../../assets/readme-improve.svg" alt="" width="18" height="18" align="absmiddle" /> 採点だけでなくハーネスを構築

目的は失敗の報告だけではありません。操作エージェントは失敗を診断し、プロンプト、原則、例、検索、ツール、オブザーバー、バリデーター、回帰ケース、環境自動化などを含む具体的な変更を開発します。

<a id="evidence-gated-self-improvement"></a>
### <img src="../../assets/readme-verify.svg" alt="" width="18" height="18" align="absmiddle" /> 証拠を条件とする自己改善

稼働中のエージェントは昇格済みハーネスを自由に書き換えられません。候補を作り、テストして証拠を添付し、フレームワーク経由で昇格します。各昇格版を確認・復元できます。

<a id="environment-agnostic"></a>
### 環境に依存しない

コアは Blender、SVG、Python エージェント、特定のモデル提供元に依存しません。ユニットは端末コマンド、MCP サーバー、ブラウザ自動化、デスクトップアプリ、API、手動手順、独自ツールインターフェースを使えます。

<a id="reasoning-remains-open-ended"></a>
### 推論の自由を維持

Harneloop はライフサイクルを構造化しますが、操作エージェントを固定スクリプトにはしません。適切なテスト、成果物、評価戦略、ツール、停止点は引き続きエージェントが選びます。

<a id="agent-quick-start"></a>
## エージェント向けクイックスタート

Harneloop は主に、ファイルシステムと端末にアクセスできるエージェントと会話して使うことを想定しています。

エージェントにリポジトリと次のようなプロンプトを渡します：

```text
Read this repository's README.md and docs/agent-onboarding.md.
Use Harneloop to create a harness unit that improves an agent at: [describe the task].

Inspect my existing environment before deciding how to test it. Ask only for context
that can materially change the work, and do not silently treat assumptions as confirmed.
Run a baseline, inspect its artifacts, and conclude the attempt before deciding whether
a candidate is needed. Do not promote a candidate without evidence.
```

その後エージェントは次を行います：

1. 必要なら Harneloop をインストールし、`harneloop doctor` を実行する。
2. `harneloop onboard --format json` または[導入ガイド](docs/agent-onboarding.md)を読む。
3. 暫定ユニットを作成または継続し、実環境を調べる。
4. 適応的な情報収集の確認点で、確認済み、委任済み、推論、未知のコンテキストを整理する。
5. 現在の理解で `operational-map.md` を更新する。
6. ベースラインを実行し、得られた成果物を調べる。
7. 現在のハーネスを受け入れるか改善を提案する前に、試行の結論を出す。

<a id="instructions-for-agents-reading-this-repository"></a>
### このリポジトリを読むエージェントへの指示

操作エージェントの場合：

- すべてのタスクにテストコマンドがあると想定しないでください。
- Harneloop がエンドポイント、ツール、スクリーンショット、成果物パスを見つけてくれると想定しないでください。
- ユニットに入るときやコンテキストを失ったときは `harneloop brief <unit>` を実行し、`AGENTS.md`、`UNIT_AGENT.md`、`operational-map.md` を読んでください。
- ユニットのブリーフはそのユニットの作業にだけ適用し、無関係なプロジェクト作業は対象外にしてください。
- `harneloop intake status` で、作業を実質的に変え得る未解決の疑問だけを提示してください。
- `harneloop candidate list <unit>` ですべての未完作業を確認し、アクティブな候補が 1 つだけだと想定しないでください。
- 関連変更をまとまった候補に集め、設定変更ごとに完全なベンチマークをせず、影響に応じて検証してください。
- 証拠の信頼性を保つため、可能なら評価器と対象ハーネスの変更を分けてください。
- 実環境を調べ、`target/` と `environment/` に対応付けてください。
- 決定的なチェックで品質を判断できない場合は、実成果物の確認を優先してください。
- 自分自身の能力と、対象エージェント向けに設計するツールを分けてください。
- 全部を作り直すより最良の検証済み結果を目指してください。適切なツール、スキル、ライブラリ、例、過去の成果を調べて再利用し、来歴を記録し、ライセンス、安全、費用、許可の境界を守ります。
- 提案するハーネス変更は候補ワークスペースに置いてください。
- 実行、成果物、証拠、昇格、ロールバック、待機、停止、再開には Harneloop コマンドを使ってください。
- 認証情報、有料サービス、外部アクセス、セキュリティに影響するツール、高額なインフラの追加前には確認してください。
- 前提、成果物パス、ツール、自動化が変わったら運用マップを更新してください。
- 実行完了だけで止めず、成果物を確認し、`harneloop attempt conclude` で明示的な判断を記録してください。

機械可読の導入情報は次で取得できます：

```bash
harneloop onboard --format json
```

<a id="install-and-start"></a>
## インストールと開始

Harneloop は [PyPI で公開](https://pypi.org/project/harneloop/)されています。[uv](https://docs.astral.sh/uv/getting-started/installation/) で隔離ツールとして入れるか、Python 環境で `python -m pip install harneloop` を使います。`harneloop` コマンドは Windows、macOS、Linux 向けです。

```bash
uv tool install harneloop
harneloop doctor
harneloop setup
```

未リリースのソースビルドには `uv tool install git+https://github.com/Ker102/Harneloop.git` を使います。

`uv` がツールディレクトリが `PATH` にないと報告したら、`uv tool update-shell` を実行して新しい端末を開きます。クローンから作業する貢献者は `uv tool install --editable .` で現行のソースをインストールできます。[開発環境](docs/development.md)を参照してください。

`harneloop setup` は人向けのガイド付き CLI を開きます。`harneloop` をコマンドなしで実行すると、端末でより広い対話メニューが開きます。エージェントは明示的な非対話コマンドを直接使えます。

最初に役立つコマンド：

```bash
harneloop onboard
harneloop template list
harneloop units list
harneloop settings show
```

`harneloop setup` または `harneloop init-unit` で作成したユニットは自動登録されます。既存ユニットは次で一度登録できます：

```bash
harneloop units register /path/to/my-unit
```

登録後は任意のディレクトリから、相対パスではなくユニット ID または名前を使えます：

```bash
harneloop units list
harneloop status my-unit --format markdown
harneloop environment status my-unit
```

<a id="what-the-agent-asks-you"></a>
## エージェントが尋ねること

新ユニットの導入は意図的に短くしています。エージェントは次の 5 点を集めます：

1. このハーネスでエージェントの何を改善するか？
2. ハーネスをどこで使うか？
3. 成功条件は自分で定義するか、エージェントが提案するか、ベースライン後に決めるか？
4. 検証では品質、視覚的証拠、バランス、資源効率のどれを優先するか？
5. テスト環境は存在するか、一部存在するか、構築が必要か？

最適なテストや成果物を事前に知る必要はありません。適切な場合、エージェントがタスクと環境を調べて提案します。制約、保護領域、費用上限、人のレビューは重要な場合にだけ尋ねます。

<a id="environment-setup"></a>
## 環境の設定

Harneloop は環境の対応付けを記録し、操作エージェントがそれを作成します。

CLI は、どの MCP ツールがアプリを制御するか、レンダリング保存先、ブラウザ操作のリセット方法、成功を示す DB 状態を自動で知ることはできません。エージェントが実ワークスペースを調べ、詳細をユニットに対応付けます。

3 つの設定モードがあります：

| モード | 使用する状況 | エージェントの動作 |
|---|---|---|
| `existing` | タスク環境が動作済み | 接続して記録し、理由なく再構築しない |
| `assisted` | 一部が存在 | ベースラインに必要な最小限の不足を特定・追加 |
| `managed` | 環境の作成が必要 | 明示的に構築し、インフラ変更を記録 |

環境はコマンド、MCP、手動、完全な独自方式のいずれでも構いません。例えば Blender ハーネスは単一の実行コマンドなしで既存 MCP サーバーを使えます。ツールを呼び、シーンをレンダリングし、スクリーンショットと構造化シーン状態を収集して Harneloop 実行に添付できます。

詳しい例は[環境の導入](docs/environment-onboarding.md)を参照してください。

<a id="configuration"></a>
## 設定

多くのユーザーは既定値から始めてください。最初に役立つ設定は通常、グローバル設定ではなくユニット内にあります。

<a id="harness-unit-configuration"></a>
### ハーネスユニットの設定

| ファイル・領域 | 変更する状況 |
|---|---|
| `operational-map.md` | ツール、成果物保存先、前提、制約、ワークフローの変更 |
| `target/brief.yaml` | タスク群、成功定義、期待する成果物、既知のリスクの変更 |
| `environment/contract.yaml` | コマンド、MCP ツール、設定・対話モード、出力パスの変更 |
| `agent-facing/` | 検証済み候補が新しい指示や再利用可能なコンテキストを昇格 |
| `observers/` と `validators/` | 成果物確認や決定的なチェックの改善が必要 |
| `regression-cases/` | 発見した失敗を今後の反復でテストする必要 |
| `tools/` と `infrastructure/` | 性能向上にユニット固有の能力やサービスが必要 |

フレームワーク管理の `.evolve/`、`versions/`、`provenance/`、`runtime/`、候補メタデータを手で編集せず、CLI のライフサイクルコマンドを使ってください。

<a id="global-preferences"></a>
### グローバル設定

`harneloop settings show` で設定を確認し、次で変更します：

```bash
harneloop settings set validation.prefer_visual_artifacts true
harneloop settings set agent_behavior.autonomy_level balanced
harneloop settings set runtime.token_efficiency_mode false
```

主な設定グループ：

- `agent_behavior`：自律性、危険な操作の確認、昇格の厳密さ；
- `validation`：エージェントが決める検証、視覚成果物の優先、資源モード；
- `export`：既定の対象アダプターとパッケージプロファイル；
- `runtime`：テレメトリーの詳細度、トークン効率モード、ローカルユニット登録の動作。

アルファ版では、設定は CLI と操作エージェントの永続的な既定値・指針です。すべてのエンジンコマンドが全設定を自動で強制するわけではありません。明示的な開発用オーバーライドを使わない限り、昇格には証拠が必要です。

<a id="example-use-cases"></a>
## 使用例

- Blender や CAD エージェントの空間推論とシーン構築を改善する。
- 描画済み成果物のレビューで SVG、画像、スライド、文書、UI の生成を改善する。
- 実装やデバッグの失敗が繰り返されるリポジトリにコーディングエージェント用ハーネスを作る。
- スクリーンショット、DOM 状態、トレース、タスク結果でブラウザ自動化を改善する。
- MCP ベースのエージェントのツール選択と復旧動作を改善する。
- 研究・データ処理のワークフローで検索、例、バリデーター、コンテキストを進化させる。
- 再利用可能な内部ハーネスを作り、Codex、Cursor、独自アプリエージェントへエクスポートする。

Harneloop はタスクを繰り返し、出力を確認でき、失敗を持続的改善にできる場合に最も役立ちます。学びを再利用しない一回限りのタスクには不要です。

<a id="core-cli-lifecycle"></a>
## CLI のコアライフサイクル

明示的なコマンドはエージェント、自動化、技術ユーザー向けです：

```bash
harneloop init-unit ./my-unit --id my-unit --name "My Harness Unit" --template artifact-review
harneloop target set my-unit --task "..." --success "..."
harneloop environment connect my-unit --name "..." --mode existing --description "..."
harneloop attempt plan my-unit --goal "..." --method "..."
harneloop run start my-unit --task "Baseline attempt"
harneloop artifact add my-unit run-0001 ./output.png --kind image
harneloop run finish my-unit run-0001 --status succeeded --summary "Baseline captured"
harneloop candidate create my-unit --summary "Improve artifact construction" --plane target_harness --validation-tier representative
harneloop run start my-unit --task "Test candidate improvement" --candidate-id cand-0001
harneloop artifact add my-unit run-0002 ./improved-output.png --kind image
harneloop run finish my-unit run-0002 --status succeeded --summary "Candidate result captured"
harneloop candidate evidence add my-unit cand-0001 --kind artifact_review --summary "..." --run-id run-0002 --artifact-id artifact-0001 --validation-tier representative
harneloop candidate stage my-unit cand-0001 ready
harneloop promote my-unit cand-0001 --version 0.1.0
harneloop export my-unit --adapter codex
harneloop package my-unit --output ./my-unit-0.1.0.tar.gz
```

この順序は例示であり固定レシピではありません。ツール駆動のエージェントは `run start` と `run finish` の間に多くの操作を行い、複数成果物や試行を作ったり外部結果を待ったりできます。

<a id="safety-and-integrity"></a>
## 安全性と整合性

- YAML と JSON の制御ファイルはアトミックに書き込まれます。
- 並行 ID 割り当てと読み取り・変更・書き込みはハーネス内のロックを使います。
- 終了済み実行は変更も再終了もできません。
- 候補オーバーレイは保護されたフレームワーク状態を変更できません。
- 証拠の参照先は添付時と昇格時に存在する必要があります。
- 候補証拠は現在のベース版と宣言済み検証レベルに一致する必要があります。
- 並行候補は別候補の昇格後も残りますが、昇格前にリベースと新しい証拠が必要です。
- 昇格済み版は復元可能なスナップショットとして保存されます。
- ロールバックは記録されるフレームワーク操作です。
- thin パッケージは実行データ、候補、キャッシュ、一般的な秘密情報ファイルを除外します。

<a id="documentation"></a>
## ドキュメント

- [Harneloop の仕組み](docs/framework-process.md)
- [エージェントの導入](docs/agent-onboarding.md)
- [環境の導入](docs/environment-onboarding.md)
- [コアライフサイクル](docs/architecture/core-lifecycle.md)
- [ランタイム層と将来の Rust 境界](docs/architecture/runtime-layers.md)
- [並行処理とファイルの安全性](docs/architecture/concurrency.md)
- [製品の原則](docs/product-principles.md)
- [ローカルデモ](docs/demo-first-test.md)
- [開発ノート](docs/development.md)

<a id="contributing"></a>
## 貢献

貢献、問題報告、独立したユニットの事例を歓迎します。特に役立つもの：

- 既存事例以外のタスク群で Harneloop を検証する；
- ライフサイクル、移植性、導入の再現可能な不具合を報告する；
- 対象エージェント用アダプター、バリデーター、パッケージ化、マルチプラットフォーム動作を改善する；
- 範囲を絞った文書、例、回帰テストを追加する。

大きな変更前に [CONTRIBUTING.md](CONTRIBUTING.md) を読み、アーキテクチャ作業は先に issue で範囲と互換性を相談してください。セキュリティ問題は公開 issue ではなく [SECURITY.md](SECURITY.md) に従います。

<a id="development"></a>
## 開発

リポジトリからテストを実行します：

```bash
python -m unittest discover -s tests
```

現在 Python 3.11 以降を使用します。製品の機能面が安定したら、将来の Rust ランタイムが、保護されたライフサイクル、パッケージ化、ファイル監視、デスクトップ配布をより強く担う可能性があります。

Harneloop はアルファ版と公開リリースに選ばれた製品名です。パッケージ、CLI、ユニットのメタデータ、文書、リポジトリで同じ名前を使います。

<a id="license"></a>
## ライセンス

Harneloop は [Apache License 2.0](../../../LICENSE) で利用できます。
