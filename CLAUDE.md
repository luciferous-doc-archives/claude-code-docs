# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 概要

このプロジェクトはClaude Codeのドキュメントをウェブからフェッチし、ファイルハッシュで変更を検出して、更新されたドキュメントをGitHub Releasesとして公開する。GitHub Actionsで毎日03:00 JSTに自動実行される。

## コマンド

```bash
# 依存関係のインストール
uv sync

# フェッチャーをローカル実行
BASE_TIMESTAMP=$(date -u +'%Y%m%d-%H%M') uv run src/handlers/fetcher/fetcher.py

# テスト実行
uv run pytest

# 特定のテストファイルのみ実行
uv run pytest tests/path/to/test_file.py

# コードフォーマット
uv run black src/
uv run isort src/

# フォーマットチェック（変更なし）
uv run black --check src/
uv run isort --check src/
```

## カンバンワークフロー

このプロジェクトは `kanban-kit` プラグイン（`luciferous-plugins` マーケットプレイス）を使ったカンバン方式でタスクを管理する。

**タスクの追加**: `/add-kanban` を実行すると `kanban/` ディレクトリに新規タスクファイル（目的と要望を記述したMarkdown）が作成される。

**タスクの実行**: `/kanban` または `/kanban <タスク番号>` を実行する。プランモードで実装計画を立てて承認を得た後、`kanban/{xxxx}_{title}/log.md` に詳細な作業ログを残しながら実装する。

## アーキテクチャ

**エントリポイント**: `src/handlers/fetcher/fetcher.py` はスクリプトとして直接実行される（Lambdaハンドラーではない）。`src/handlers/fetcher/main.py` の `main()` を呼び出し、そこにフェッチロジックを実装する。

**`src/utils/http/interval_fetcher.py`**: インターバル制限付きHTTPフェッチャー。`make_interval_fetcher(sec=N)` はリクエスト間に最低N秒の間隔を強制し、5xx/429エラー時に指数バックオフでリトライするcallableを返す。`default_fetcher`（1秒間隔、5回リトライ）がデフォルトとして提供される。

**`src/utils/logger/`**: `aws-lambda-powertools.Logger` をラップしたカスタム構造化ロガー。`create_logger(__name__)` でインスタンスを生成する。`@logging_function(logger)` デコレータで関数の開始・終了・エラーを呼び出しIDと実行時間付きで自動デバッグログ記録できる。`@logging_handler(logger)` デコレータはLambdaハンドラー用でLambdaコンテキストを注入する。JSONシリアライザー `custom_default` は `datetime`、`bytes`（gzip+base64）、`Decimal`、Pydanticモデル、dataclassに対応。

**`src/utils/path/converter.py`**: `url_to_file_path(url, all_urls)` はURLをローカルファイルパスに変換する。`.md` URLに対して同じパスプレフィックス配下の子URLが存在する場合、`{stem}.md` ではなく `{stem}/index.md` として保存する。

**CIワークフロー** (`.github/workflows/fetch-docs.yml`): ドキュメントのフェッチ → sha256ハッシュ生成 → リポジトリの `file_hashes.txt` と差分比較 → 変更あればリリースzipを作成して `file_hashes.txt` をコミット更新。失敗時は `SLACK_INCOMING_WEBHOOK_URL` シークレット経由でSlack通知。

## Python バージョン

Python >= 3.14 必須（`.python-version` 参照）。`uuid7` はPython 3.14標準ライブラリを使用。
