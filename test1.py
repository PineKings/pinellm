from pinellm import ChatRequest, Message, ResponseFormat, Tool, Propertie

# 创建消息
messages = [
    Message("system", "You are a helpful assistant."),
    Message("user", "现在几点了？")
]

# 定义工具（获取当前时间）
tools = [
    Tool(
        "get_current_time",
        "获取当前时间",
        properties=None
    )
]

# 发送请求
response = ChatRequest(
    model="qwen-plus",
    messages=messages,
    #tools=tools,
    tool_choice="auto"
).send()

# 处理响应
print(f"回答：{response.choices.message.content}")
print(f"费用：{response.price.total_price} 元")