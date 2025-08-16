## a40_agent_sample1.py ― 詳細設計書

### 1. 目的

OpenAI Agents SDK を用いて

* **Triage Agent** が質問内容を分類
* 適切な **Tutor Agent**（Math / History）へ _handoff_
* 質問が宿題であれば **Guardrail** でブロック

— という安全かつ拡張性の高い対話フローを実装する。

---

### 2. モジュール・クラス構成


| 名称                              | タイプ         | 役割                                         |
| --------------------------------- | -------------- | -------------------------------------------- |
| `Agent`                           | SDK クラス     | LLM プロンプト・ツール・ハンドオフ設定を内包 |
| `Runner`                          | SDK クラス     | エージェント連鎖の実行制御                   |
| `InputGuardrail`                  | SDK クラス     | 入力検査関数のラップ & tripwire 発火         |
| `GuardrailFunctionOutput`         | SDK クラス     | 検査結果＋`tripwire_triggered` フラグを保持  |
| `InputGuardrailTripwireTriggered` | 例外           | tripwire 発火時に Runner が送出              |
| `RunContextWrapper`               | SDK クラス     | Guardrail 関数やツール間で共有する実行状態   |
| `HomeworkOutput`                  | Pydantic Model | Guardrail 用の構造化出力スキーマ             |

---

### 3. 関数仕様


| 関数名               | 概要                                         | 入力<br>(型)                         | 処理                                                                                                                      | 出力                      |
| -------------------- | -------------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| `homework_guardrail` | 入力が宿題か判定し、宿題なら tripwire を発火 | `ctx`<br>`agent`<br>`input_data:str` | 1.`guardrail_agent` を実行<br>2. 結果を `HomeworkOutput` にキャスト<br>3. `tripwire_triggered = final_output.is_homework` | `GuardrailFunctionOutput` |
| `main`               | サンプルクエリ 2 件で動作確認し結果を表示    | なし                                 | ループで`Runner.run(triage_agent, q)` を呼び出し、`InputGuardrailTripwireTriggered` を捕捉                                | なし（標準出力のみ）      |

---

### 4. エージェント定義


| Agent                 | 主要プロパティ                                                                                 | 説明                                          |
| --------------------- | ---------------------------------------------------------------------------------------------- | --------------------------------------------- |
| `guardrail_agent`     | `output_type=HomeworkOutput`                                                                   | 入力が宿題か LLM に判定させるミニエージェント |
| `math_tutor_agent`    | `instructions=数学支援`                                                                        | 数学の質問に詳細解説で答える                  |
| `history_tutor_agent` | `instructions=歴史支援`                                                                        | 歴史の質問に背景込みで答える                  |
| `triage_agent`        | `handoffs=[history_tutor_agent, math_tutor_agent]`<br>`input_guardrails=[InputGuardrail(...)]` | 質問を振り分ける司令塔 & Guardrail 併用       |

---

### 5. 全体処理フロー

```text
┌─ ユーザー入力 ─────────────────────┐
│ Runner.run(triage_agent, query)   │
└───────────────────────────────────┘
          │
          ▼
[Async] InputGuardrail (homework_guardrail)
          │   ├─ 宿題? → tripwire=True → 例外→停止
          │   └─ 宿題でない → 続行
          ▼
triage_agent が LLM 推論で handoff 先決定
          │
          ├──► math_tutor_agent  (数学質問)
          │
          └──► history_tutor_agent (歴史質問)
          ▼
 Tutor Agent が最終回答を生成
          ▼
Runner が結果を返却 / ガードレール例外を伝達
```
