# Claude CodeドキュメントURLの抽出

## 目的
Claude CodeのドキュメントのURLリストが欲しい

## 要望
`https://code.claude.com/llms.txt` をfetchして `## Docs`配下のURLをパースする関数を書いてください。

## プラン
`src/handlers/fetcher/main.py` に以下を実装:
- `main()`: llms.txt をfetchしてURLをパース
- `_parse_docs_urls()`: Markdown形式からURL抽出

## 完了サマリー

**完了日時**: 2026-05-06T03:20:00+09:00

**成果物**:
- `src/handlers/fetcher/main.py`: llms.txt フェッチとURLパース処理を実装
  - 124個のドキュメントURLを正しく抽出
  - 構造化ログで抽出結果を出力

**実装の詳細はログを参照**: `kanban/0001_fetch_docs_urls/log.md`
