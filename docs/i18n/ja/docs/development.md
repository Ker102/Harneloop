<a id="development"></a>
# 開発

<a id="repository-layout"></a>
## リポジトリ構成

```text
src/harneloop/      Python reference implementation
tests/           Unit and behavior tests
docs/            Architecture and development notes
schemas/         Language-neutral data contracts
.github/         CI and repository automation
```

<a id="local-verification"></a>
## ローカル検証

チェックアウトをユーザーレベルの編集可能なツールとして一度インストールします：

```powershell
uv tool install --editable .
```

これにより `harneloop` コマンドはリポジトリ外でも利用でき、ソースの変更も反映されます。検証は次で実行します：

```powershell
uv run python -m compileall src tests
uv run python -m unittest discover -s tests
harneloop doctor
```

<a id="devops-baseline"></a>
## DevOps の基盤

リポジトリでは次を維持してください：

- `src/` を使ったソース構成；
- 再現可能なローカルテスト；
- 対応する Python バージョンの CI；
- 仮想環境や実行成果物をバージョン管理しないこと；
- 明確なセキュリティ文書と貢献ガイド；
- コア記録の言語に依存しないスキーマ。

<a id="runtime-data"></a>
## 実行時データ

実行トレース、コピーされた成果物、実行記録、試行計画、実験はローカルの作業データです。後のパッケージプロファイルが明示的に含める場合を除き、thin ポータブルパッケージに取り込んではいけません。

<a id="pr-review-note"></a>
## PR レビューについて

初期プロトタイプでは CodeRabbit のレビューは不要です。PR を作成した場合は、設定済みの CodeRabbit-ignore タグまたはラベルを付けてください。
