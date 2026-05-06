# parse_docs_urls を public 化してログを追加

## 目的
属性を調整し、ログを残すようにする

## 要望
_parse_docs_urls()をpublicな関数にしてlogging_functionでログを出力してください

## 完了サマリー

**実施日時**: 2026-05-06T23:20:22+09:00

**実施内容**:
1. `src/handlers/fetcher/main.py` の `_parse_docs_urls()` 関数を `parse_docs_urls()` に名前変更（private → public）
2. `@logging_function(logger)` デコレータを parse_docs_urls() に追加
3. main() 内の呼び出しを更新
4. black と isort でコードフォーマット完了

**結果**: ✅ 正常に完了。logging_function により以下が自動記録されるようになった:
- CallID、開始・終了時刻（JST）、実行時間
- 関数の引数と戻り値
- エラー時のスタックトレース
