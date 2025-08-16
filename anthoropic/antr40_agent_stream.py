#
# pip install anthropic
import asyncio
import anthropic
import os
from typing import Optional, AsyncGenerator


class Agent:
    def __init__(self, name: str, instructions: str):
        self.name = name
        self.instructions = instructions


class Runner:
    @staticmethod
    async def run_streamed(agent: Agent, input: str, api_key: Optional[str] = None) -> AsyncGenerator[str, None]:
        """
        Anthropic APIを使用してストリーミングレスポンスを取得
        """
        # API キーの取得順序: 引数 -> 環境変数
        effective_api_key = api_key or os.getenv("ANTHROPIC_API_KEY")

        if not effective_api_key:
            raise ValueError(
                "API キーが設定されていません。以下のいずれかの方法で設定してください:\n"
                "1. 環境変数: export ANTHROPIC_API_KEY='your-api-key'\n"
                "2. 引数で直接指定: Runner.run_streamed(agent, input, api_key='your-api-key')"
            )

        client = anthropic.AsyncAnthropic(api_key=effective_api_key)

        # システムメッセージとユーザーメッセージを構築
        messages = [
            {"role": "user", "content": input}
        ]

        try:
            async with client.messages.stream(
                    model="claude-3-5-sonnet-20241022",  # 最新のSonnetモデル
                    max_tokens=1000,
                    system=agent.instructions,  # システムプロンプト
                    messages=messages
            ) as stream:
                async for text in stream.text_stream:
                    yield text
        except Exception as e:
            raise RuntimeError(f"Anthropic API呼び出しでエラーが発生しました: {e}")


async def main():
    try:

        agent = Agent(
            name="Joker",
            instructions="You are a helpful assistant.",
        )
        input_text = """応答は全て日本語で。
        マイクロサービスアーキテクチャを実装するためのベストプラクティスは何ですか？
        私たちのチームのコードレビュープロセスにどのようにアプローチすべきですか？
        技術的負債管理の戦略を提案できますか？",
        私たちのソフトウェア開発プロセスで追跡すべきメトリクスは何ですか？"""
        print("方式提案：")
        print("-" * 50)

        async for text_chunk in Runner.run_streamed(agent, input=input_text):
            print(text_chunk, end="", flush=True)

        print()  # 最後に改行
        print("-" * 50)
        print("完了！")

    except ValueError as e:
        print(f"設定エラー: {e}")
    except RuntimeError as e:
        print(f"実行エラー: {e}")
    except Exception as e:
        print(f"予期しないエラー: {e}")


if __name__ == "__main__":
    # API キーの確認
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("警告: ANTHROPIC_API_KEY 環境変数が設定されていません。")
        print("以下のコマンドで設定してください:")
        print("export ANTHROPIC_API_KEY='your-anthropic-api-key'")
        print()
        print("または、以下のようにコード内で直接指定することもできます:")
        print("Runner.run_streamed(agent, input, api_key='your-api-key')")
        print()

    asyncio.run(main())
