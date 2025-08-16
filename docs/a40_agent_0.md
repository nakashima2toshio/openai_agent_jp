Agents SDK の特徴
Agent＝(モデル＋指示＋ツール群) をオブジェクトで表現し、Runner が「考える→ツール実行→考える…→完了」ループを自動化。
openai.github.io

@function_tool で Python 関数を登録するだけで JSON スキーマ生成・入力検証まで完結。

Tracing UI、Guardrails、Handoffs など運用・拡張機能を同梱。

| 観点 | Responses API | Agent（Agents SDK） |
| ---- | -------------- | -------------------- |
| **位置づけ** | モデル＋ツールを直接呼ぶ **API 基盤** | Responses/Chat API 上に構築された **Python ライブラリ** |
| **抽象度** | 低：1 リクエスト＝LLM 1 ターン | 高：内部で複数リクエストを自動ループ |
| **ツール呼び出し** | Web 検索・ファイル検索・画像生成・Code Interpreter など **組込みツールを標準装備**。自作ツールは JSON-schema を自分で用意し、結果メッセージを手動で注入 | `@function_tool` で **普通の Python 関数 ⇒ ツール**。JSON スキーマ生成・呼び出し・結果挿入を SDK が自動処理 [[1]] |
| **ループ＆プランニング** | なし（自分で while ループを書く） | **Agent loop** が内蔵：モデル→ツール→モデル…を Runner が完走するまで自動実行 [[1]] |
| **メモリ / コンテキスト圧縮** | 直接は提供しない（開発者が token 上限を管理） | コンテキスト管理ユーティリティ、ガードレール、トレース UI などを同梱 |
| **マルチエージェント連携** | なし | **Handoffs** でエージェント間タスク委譲をサポート |
| **対象モデル** | GPT-4o / o-series など *Responses 対応* モデル | `model="o3-mini"` 等で **ResponsesModel が推奨**（Chat 形も可） [[2]] |
| **典型ユースケース** | 単発チャット、RAG の最終回答生成、独自オーケストレーションを自前で作りたいとき | TODO リスト実行、データ抽出→変換→保存など **複数手順・ツールを伴う自律タスク** |
| **コード量** | HTTP リクエスト＋手動でツール応答メッセージを構築 | エージェントとツールを宣言 → `Runner.run_sync()` 1 行で実行 |

[1]: https://openai.github.io/openai-agents-python/ "OpenAI Agents SDK"
[2]: https://openai.github.io/openai-agents-python/models/ "Models - OpenAI Agents SDK"
