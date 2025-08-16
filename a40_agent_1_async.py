# a40_agent_1_async.md.py
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
import asyncio

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You only speak Spanish.",
    model="o3-mini",
)

english_agent = Agent(
    name="English agent",
    instructions="You only speak English",
    model="o3-mini",
    # model=OpenAIChatCompletionsModel( # (2)!
    #     model="gpt-4o",
    #     openai_client=AsyncOpenAI()
    # ),
)

# triage=選別
triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[spanish_agent, english_agent],
    model="gpt-3.5-turbo",
)

async def main():
    result = await Runner.run(triage_agent, input="Hola, ¿cómo estás?")
    print(result.final_output)
    print('-----------------')
    result = await Runner.run(triage_agent, input="Hi, How's your day?")
    print(result.final_output)

# ---- エントリーポイント（asyncio 実行）----------------------------
if __name__ == "__main__":
    asyncio.run(main())
