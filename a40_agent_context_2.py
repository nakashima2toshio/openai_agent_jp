"""
Async version of the Business-assistant agent.

✅ そのまま python ファイルに保存 → 実行すると
   - BusinessContext を渡した状態でエージェントを起動
   - 1 ターン質問して最終応答を表示
"""

import asyncio
from dataclasses import dataclass

from agents import Agent, Runner, RunContextWrapper

# ---------- 1) 共有コンテキスト ----------------------------------
@dataclass
class BusinessContext:
    company_name: str
    department: str
    user_role: str


# ---------- 2) 動的 instructions 関数 ----------------------------
def business_instructions(
    wrapper: RunContextWrapper[BusinessContext],
    agent: Agent,
) -> str:
    ctx = wrapper.context
    return f"""
You are an AI assistant for {ctx.company_name}'s {ctx.department} department.
You are helping a {ctx.user_role}.
""".strip()


# ---------- 3) 非同期 main ---------------------------------------
async def main() -> None:
    # コンテキストを用意
    business_ctx = BusinessContext(
        company_name="TechCorp",
        department="Engineering",
        user_role="Senior Developer",
    )

    # エージェント生成
    agent = Agent[BusinessContext](
        name="Business Assistant",
        instructions=business_instructions,
        model="gpt-4",
    )

    input_text = """
        マイクロサービスアーキテクチャを実装するためのベストプラクティスは何ですか？
    私たちのチームのコードレビュープロセスにどのようにアプローチすべきですか？
    技術的負債管理の戦略を提案できますか？
    私たちのソフトウェア開発プロセスで追跡すべきメトリクスは何ですか？"""

    # 1 ターン実行（await Runner.run なので非同期）
    result = await Runner.run(
        starting_agent=agent,
        input=input_text,
        context=business_ctx,
    )

    # 最終アウトプット表示
    print(result.final_output)


# ---------- 4) エントリーポイント --------------------------------
if __name__ == "__main__":
    asyncio.run(main())
