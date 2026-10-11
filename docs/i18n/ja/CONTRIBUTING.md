<a id="contributing"></a>
# 貢献

Harneloop は現在、公開アルファ段階です。公開 API とハーネスユニットの形式が安定するまで、対象を絞った issue や貢献を歓迎します。

<a id="development-setup"></a>
## 開発環境

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e .
.\.venv\Scripts\python -m unittest discover -s tests
```

macOS または Linux の場合：

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -e .
./.venv/bin/python -m unittest discover -s tests
```

<a id="pull-requests"></a>
## プルリクエスト

各プルリクエストは、1 つの動作またはアーキテクチャの一部分に範囲を絞ってください。

大きなアーキテクチャ変更の前に issue を作成し、問題と互換性への影響について合意してください。ライフサイクル変更にはテストを含め、動作が変わる場合はエージェント向け文書も更新してください。

現時点では CodeRabbit の自動レビューを依頼しないでください。CodeRabbit が設定されている状態で PR を作成した場合、レビュー依頼の前にリポジトリの CodeRabbit-ignore ラベルまたはタグを付けてください。

<a id="standards"></a>
## 基準

- フレームワークのコアはタスクの種類に依存しないようにしてください。
- `src/harneloop` に Blender 固有の前提を追加しないでください。
- ライフサイクル動作のテストを追加または更新してください。
- エージェント向けファイルは読みやすい Markdown、YAML、JSON にしてください。
- 秘密情報、ローカル実行成果物、仮想環境、生成済みパッケージをコミットしないでください。

貢献することで、その貢献がリポジトリの [Apache License 2.0](../../../LICENSE) に基づいてライセンスされることに同意します。
