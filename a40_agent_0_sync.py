# 同期版：
# -----------------------------------------------
# def main:        同期なら Runner.run_sync()、
# async def main: 非同期なら Runner.run()／Runner.run_streamed()
# -----------------------------------------------
# pip install git+https://github.com/openai/openai-python.git@main
# pip install git+https://github.com/openai/openai-agents-python.git
from agents import Agent, function_tool, Runner   # ← Runner を追加

def main():
    @function_tool
    def get_weather(city: str) -> str:
        return f"The weather in {city} is sunny"

    agent = Agent(
        name="Haiku agent",
        instructions="Always respond in haiku form",
        model="o3-mini",
        tools=[get_weather],
    )

    # Runner.run_sync はブロッキング実行
    result = Runner.run_sync(agent, "東京の天気は？")
    print(result.final_output)      # 俳句で返る最終アウトプット

if __name__ == "__main__":
    main()
