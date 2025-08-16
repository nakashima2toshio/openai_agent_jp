from agents import Agent, ModelSettings, function_tool

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"

agent = Agent(
    name="Haiku agent",
    instructions="Always respond in haiku form",
    model="o3-mini",
    tools=[get_weather],
)

def main():
    # Agentクラスの情報を確認
    print("Agent class:", Agent)
    print("Agent type:", type(Agent))
    print("Agent __init__ method:", hasattr(Agent, '__init__'))

    # 初期化パラメータを確認
    import inspect
    import pprint
    try:
        pprint.pprint(("Agent signature:", inspect.signature(Agent)))
    except Exception as e:
        print("Error getting signature:", e)

if __name__ == "__main__":
    main()
