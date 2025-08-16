# 非同期版： async_main --- python a40_agent_0_async.py
# -----------------------------------------------
# Agents SDKの特徴
# ・Agent＝(モデル＋指示＋ツール群) をオブジェクトで表現
# ・Runner が「考える→ツール実行→考える…→完了」ループを自動化。
# ・@function_tool で Python 関数を登録するだけで JSON スキーマ生成・入力検証まで完結。
# ・Tracing UI、Guardrails、Handoffs など運用・拡張機能を同梱。
# -----------------------------------------------
# def main:        同期なら Runner.run_sync()、
# async def main: 非同期なら Runner.run()／Runner.run_streamed()
# -----------------------------------------------
# pip install git+https://github.com/openai/openai-python.git@main
# pip install git+https://github.com/openai/openai-agents-python.git
# -----------------------------------------------
import asyncio
from agents import Agent, function_tool, Runner
import logging

# --------------------------------------------------------
# ★ 1. 先に root ロガーを DEBUG で一括設定
#     basicConfig を使うと楽。handlers を渡すとこれだけで済む。
# --------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG,                                   # <- ここを DEBUG に
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),                           # コンソール
        logging.FileHandler("agent_run.log", encoding="utf-8")  # ファイル
    ],
    force=True   # 既存設定を上書き（Py >= 3.8）
)

# --------------------------------------------------------
# ★ 2. openai 系ロガーだけ INFO 以上に絞りたいなら個別に下げる
# --------------------------------------------------------
logging.getLogger("openai").setLevel(logging.INFO)

# --------------------------------
@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"

agent = Agent(
    name="Haiku agent",
    instructions="Always respond in haiku form",
    model="o3-mini",
    tools=[get_weather],
)

async def main():
    result = await Runner.run(agent, "東京の天気は？")
    print(result.final_output)

# ---- エントリーポイント（asyncio 実行）----------------------------
if __name__ == "__main__":
    asyncio.run(main())
