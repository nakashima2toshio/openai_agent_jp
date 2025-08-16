# a40_agent_3_context_1.py
import asyncio
from dataclasses import dataclass
from typing import List

from agents import Agent, RunContextWrapper, Runner


@dataclass
class BusinessContext:
    company_name: str
    department: str
    user_role: str


def business_instructions(wrapper: RunContextWrapper[BusinessContext], agent: Agent[BusinessContext]) -> str:
    ctx = wrapper.context
    return f"""
    You are an AI assistant for {ctx.company_name}'s {ctx.department} department.
    You are helping a {ctx.user_role}.
    """


async def run_business_query(agent: Agent[BusinessContext], context: BusinessContext, query: str) -> str:
    """単一のクエリを実行する関数"""
    result = await Runner.run(
        starting_agent=agent,
        input=query,
        context=context
    )
    return result.final_output


async def main():
    # ビジネスコンテキストの作成
    business_ctx = BusinessContext(
        company_name="TechCorp",
        department="Engineering",
        user_role="Senior Developer"
    )

    # エージェントの作成
    agent = Agent(
        name="Business Assistant",
        instructions=business_instructions,
        model="gpt-4"
    )

    # 複数のビジネス関連質問例
    business_queries = [
        "応答は全て日本語で。"
        "マイクロサービスアーキテクチャを実装するためのベストプラクティスは何ですか？",
        "私たちのチームのコードレビュープロセスにどのようにアプローチすべきですか？",
        "技術的負債管理の戦略を提案できますか？",
        "私たちのソフトウェア開発プロセスで追跡すべきメトリクスは何ですか？"
        # "What are the best practices for implementing microservices architecture?",
        # "How should we approach code review processes for our team?",
        # "Can you suggest strategies for technical debt management?",
        # "What metrics should we track for our software development process?"
    ]

    print(f"=== {business_ctx.company_name} {business_ctx.department} Assistant ===")
    print(f"Assisting: {business_ctx.user_role}")
    print("=" * 60)

    # 各質問を順次実行
    for i, query in enumerate(business_queries, 1):
        print(f"\n🔍 Query {i}: {query}")
        print("-" * 50)

        try:
            response = await run_business_query(agent, business_ctx, query)
            print(f"💡 Response:\n{response}")
        except Exception as e:
            print(f"❌ Error: {e}")

        print("-" * 50)

    print("\n✅ All business queries completed!")


if __name__ == "__main__":
    asyncio.run(main())
