# a40_agent_2_dataclass.py
# -----------------------------------------------------------------------
# ローカルコンテキストは [RunContextWrapper][agents.run_context.RunContextWrapper] クラスと、
# その中の [context][agents.run_context.RunContextWrapper.context] プロパティで表現されます。
# 仕組みは次のとおりです。
#
# 任意の Python オブジェクトを作成します。
# 一般的なパターンとして dataclass や Pydantic オブジェクトを使用します。
# そのオブジェクトを各種 run メソッド（例: Runner.run(..., **context=whatever** )）に渡します。
# すべてのツール呼び出しやライフサイクルフックには、
# ラッパーオブジェクト RunContextWrapper[T] が渡されます。
# ここで T はコンテキストオブジェクトの型で、wrapper.context からアクセスできます。
# -----------------------------------------------------------------------
import asyncio
from dataclasses import dataclass
from agents import Agent, RunContextWrapper, Runner, function_tool

# メッセージリストを使用したい場合の正しい形式
messages = [
    {
        "role": "system",
        "content": "You are a helpful agent."
    },
    {
        "role": "user",
        "content": "What is the age of the user?"
    },
    {
        "role": "assistant",
        "content": "応答は日本語で。"
    },
]

# ---------------------------------------------------------
# 重要なポイント：
#  [コード内で完結 ⇒ instructions] instructions は基本的な行動指針を、
#  [UI で更新・バージョン管理 ⇒ prompt] prompt はより高度なテンプレート制御
# ---------------------------------------------------------
# instructionsは3つのパターン（str, Callable, None）があること
# promptも3つのパターン（Prompt, DynamicPromptFunction, None）があること
# 動的生成の場合の引数と戻り値の詳細
# instructionsとpromptの違いと使い分け
# [code例：]
# agent = Agent(
#     name="Advanced Assistant",
#     instructions="You are a professional assistant.",  # 基本指示
#     prompt={                                          # 詳細制御
#         "id": "professional_template",
#         "version": "1.0"
#     },
#     model="gpt-4"
# )
# ---------------------------------------------------------
@dataclass
class UserInfo:
    name: str
    uid: int

@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:  # (2)!
    return f"User {wrapper.context.name} is 47 years old"

async def main():
    user_info = UserInfo(name="John", uid=123)

    agent = Agent(  # [UserInfo](
        name="Assistant",
        tools=[fetch_user_age],
        model="o3-mini",
    )

    # ---------
    # input: str | list[TResponseInputItem],
    # class EasyInputMessageParam(TypedDict, total=False):
    # ---------
    result = await Runner.run(
        starting_agent=agent,
        input=messages,
        context=user_info,
    )

    print(result.final_output)  # (5)!
    # The user John is 47 years old.

if __name__ == "__main__":
    asyncio.run(main())
