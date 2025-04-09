from pinellm import ChatRequest, Message

# 创建消息
messages = [
    Message("system", "You are a helpful assistant."),
    Message("user", "介绍一下你自己")
]

# 发送请求
response = ChatRequest(
    model="qwen-plus",
    messages=messages
).send()

# 处理响应
print(f"回答：{response.choices.message.content}") # 回答：你好！我是通义千问，阿里巴巴集团旗下的超大规模语言模型。我能够回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。我熟练掌握多种语言，包括但不限于中文、英文、德语、法语、西班牙语等。如果你有任何问题或需要帮助，随时可以问我！
print(f"费用：{response.price.total_price} 元") # 费用：0.0001848 元