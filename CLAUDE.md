# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 概要

このプロジェクトはClaude Codeのドキュメントをウェブからフェッチし、ファイルハッシュで変更を検出して、更新されたドキュメントをGitHub Releasesとして公開する。GitHub Actionsで毎日03:00 JSTに自動実行される。

## コマンド

Makefile を使用するのが推奨。全ターゲットは `PYTHONPATH=src` を自動設定する。

```bash
make sync         # 依存関係のインストール
make fetch        # フェッチャーをローカル実行
make test-unit    # ユニットテスト実行（-vv付き）
make format       # コードフォーマット（black + isort）
make lint         # フォーマットチェックのみ（変更なし）
```

特定のテストファイルのみ実行する場合:
```bash
PYTHONPATH=src uv run pytest tests/unit/path/to/test_file.py
```

## カンバンワークフロー

このプロジェクトは `kanban-kit` プラグイン（`luciferous-plugins` マーケットプレイス）を使ったカンバン方式でタスクを管理する。

**タスクの追加**: `/add-kanban` を実行すると `kanban/` ディレクトリに新規タスクファイル（目的と要望を記述したMarkdown）が作成される。

**タスクの実行**: `/kanban` または `/kanban <タスク番号>` を実行する。プランモードで実装計画を立てて承認を得た後、`kanban/{xxxx}_{title}/log.md` に詳細な作業ログを残しながら実装する。

## アーキテクチャ

**エントリポイント**: `src/handlers/fetcher/fetcher.py` はスクリプトとして直接実行される（Lambdaハンドラーではない）。`src/handlers/fetcher/main.py` の `main()` を呼び出す。`main()` には `@logging_function` デコレータを付ける。

**llms.txt パース**: `main.py` の `parse_docs_urls(content)` は `https://code.claude.com/llms.txt` の `## Docs` セクションを抽出し、`- [title](url)` 形式またはベアURL形式のリンクを収集する。相対URLは `https://code.claude.com` を自動付与する。

**出力ディレクトリ**: フェッチャーはドキュメントを `docs/claude-code-docs-{BASE_TIMESTAMP}/` に保存する。CIは `file_hashes.txt`（リポジトリルート）と現在のハッシュを比較し、差分があればリリースzipを作成する。

**`src/utils/http/interval_fetcher.py`**: インターバル制限付きHTTPフェッチャー。`make_interval_fetcher(sec=N)` はリクエスト間に最低N秒の間隔を強制し、5xx/429エラー時に指数バックオフでリトライするcallableを返す。`default_fetcher`（1秒間隔、5回リトライ）がデフォルトとして提供される。

**`src/utils/logger/`**: `aws-lambda-powertools.Logger` をラップしたカスタム構造化ロガー。`create_logger(__name__)` でインスタンスを生成する。`@logging_function(logger)` デコレータで関数の開始・終了・エラーを呼び出しIDと実行時間付きで自動デバッグログ記録できる。`@logging_handler(logger)` はLambdaハンドラー用でLambdaコンテキストを注入する。

**`src/utils/path/converter.py`**: `url_to_file_path(url, all_urls)` はURLをローカルファイルパスに変換する。`.md` URLに対して同じパスプレフィックス配下の子URLが存在する場合、`{stem}.md` ではなく `{stem}/index.md` として保存する。

**CIワークフロー** (`.github/workflows/fetch-docs.yml`): ドキュメントのフェッチ → sha256ハッシュ生成 → リポジトリの `file_hashes.txt` と差分比較 → 変更あればリリースzipを作成して `file_hashes.txt` をコミット更新。失敗時は `SLACK_INCOMING_WEBHOOK_URL` シークレット経由でSlack通知。

**テスト構造**: `tests/unit/` は `src/` のディレクトリ構造をミラーリングする（例: `src/utils/path/converter.py` → `tests/unit/utils/path/test_converter.py`）。

## Python バージョン

Python >= 3.14 必須（`.python-version` 参照）。`uuid7` はPython 3.14標準ライブラリを使用。
