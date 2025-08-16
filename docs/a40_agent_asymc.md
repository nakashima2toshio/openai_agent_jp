# マルチエージェントシステム設計書

## 1. プログラム概要

本プログラムは、OpenAIのAPIを使用したマルチエージェントシステムの実装サンプルです。ユーザーからの入力言語を自動判定し、適切な言語専用エージェントに処理を振り分けるトリアージ機能を持つシステムです。

### 主要機能
- 言語自動判定によるエージェント振り分け
- 複数エージェントの連携処理
- 非同期処理による効率的な実行

## 2. システム構成

### 2.1 エージェント構成
```
triage_agent (振り分け役)
├── spanish_agent (スペイン語専用)
└── english_agent (英語専用)
```

### 2.2 使用技術
- **言語**: Python 3.7+
- **OpenAI API**: GPT-3.5-turbo, GPT-4o, o3-mini
- **非同期処理**: asyncio
- **エージェントフレームワーク**: agents ライブラリ

## 3. 処理フロー

### 3.1 全体処理フロー
```
1. ユーザー入力受付
2. トリアージエージェントによる言語判定
3. 適切な言語エージェントへのハンドオフ
4. 言語専用エージェントによる応答生成
5. 結果返却
```

### 3.2 詳細処理ステップ

#### ステップ1: 初期化
- 各エージェントの初期化
- OpenAIクライアントの設定

#### ステップ2: 入力処理
- ユーザー入力の受付
- トリアージエージェントへの処理依頼

#### ステップ3: 言語判定・振り分け
- 入力テキストの言語分析
- 適切なエージェントの選択
- ハンドオフ実行

#### ステップ4: 応答生成
- 専用エージェントによる処理
- 指定言語での応答生成

## 4. 詳細設計

### 4.1 エージェント設計

#### トリアージエージェント (triage_agent)
```python
Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[spanish_agent, english_agent],
    model="gpt-3.5-turbo"
)
```

**役割**: 入力言語の判定と適切なエージェントへの振り分け
**モデル**: GPT-3.5-turbo（コスト効率重視）
**機能**: 言語判定とハンドオフ制御

#### スペイン語エージェント (spanish_agent)
```python
Agent(
    name="Spanish agent",
    instructions="You only speak Spanish.",
    model="o3-mini"
)
```

**役割**: スペイン語専用応答
**モデル**: o3-mini
**制約**: スペイン語のみでの応答

#### 英語エージェント (english_agent)
```python
Agent(
    name="English agent",
    instructions="You only speak English",
    model=OpenAIChatCompletionsModel(
        model="gpt-4o",
        openai_client=AsyncOpenAI()
    )
)
```

**役割**: 英語専用応答
**モデル**: GPT-4o（高性能重視）
**制約**: 英語のみでの応答

### 4.2 実行制御

#### 非同期実行 (main関数)
```python
async def main():
    result = await Runner.run(triage_agent, input="Hola, ¿cómo estás?")
    print(result.final_output)
```

**処理内容**:
- 非同期でのエージェント実行
- 結果取得と出力

#### エントリーポイント
```python
if __name__ == "__main__":
    asyncio.run(main())
```

**機能**: asyncioによる非同期実行の開始

## 5. 設計上の特徴

### 5.1 モデル選択戦略
- **トリアージ**: GPT-3.5-turbo（コスト効率重視）
- **スペイン語**: o3-mini（最新モデル）
- **英語**: GPT-4o（高性能重視）

### 5.2 非同期処理の採用
- 複数エージェント間の効率的な連携
- APIレスポンス時間の最適化

### 5.3 エージェント間連携
- ハンドオフ機能による柔軟な処理分散
- 専門化による応答品質の向上

## 6. 実行例

### 入力
```
"Hola, ¿cómo estás?"
```

### 処理過程
1. トリアージエージェントが入力を受付
2. スペイン語と判定
3. spanish_agentにハンドオフ
4. スペイン語で応答生成

### 期待される出力
```
スペイン語での応答（例: "¡Hola! Estoy bien, gracias. ¿Cómo puedo ayudarte hoy?"）
```

## 7. 拡張可能性

### 7.1 エージェント追加
- 新しい言語エージェントの追加
- 専門分野エージェントの実装

### 7.2 処理能力拡張
- 複数言語混在入力への対応
- より複雑な振り分けロジックの実装

### 7.3 統合可能性
- Streamlitとの連携
- Webアプリケーションへの組み込み

## 8. 注意事項

### 8.1 依存関係
- `agents` ライブラリの適切なインストール
- OpenAI APIキーの設定

### 8.2 エラーハンドリング
- API呼び出し失敗時の対処
- エージェント間通信エラーの処理

### 8.3 パフォーマンス
- 非同期処理による効率化
- API呼び出し回数の最適化
