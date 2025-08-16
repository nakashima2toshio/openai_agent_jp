#### Agent SDK: https://github.com/openai/openai-agents-python

##### (1) コンテキストを用意
```python
business_ctx = BusinessContext(
    company_name="TechCorp",
    department="Engineering",
    user_role="Senior Developer",
)
```
##### (2) エージェント生成
- instructions(responsesのsystemと同等)で動的関数を指定。
```python
agent = Agent[BusinessContext](
    name="Business Assistant",
    instructions=business_instructions,
    model="gpt-4",
)
```
##### (3) 1 ターン実行 (await Runner.run なので非同期)
