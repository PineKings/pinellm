from pinellm import ChatRequest, Message, ConfigManager
from dotenv import load_dotenv
import os

config = ConfigManager()
load_dotenv()
config.load_config(
    suppliers=[
            {
            "name": "qwen",
            "description": "阿里云",
            "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
            "api_key": os.getenv("QWEN_API_KEY"),  # 请自己替换一个阿里云api_key的替换逻辑
            "models":['multimodal-embedding-v1', 'qvq-max-latest', 'qwen-coder-plus-latest', 'qwen-coder-turbo-latest', 'qwen-long-latest', 'qwen-max', 'qwen-omni-turbo-latest', 'qwen-plus', 'qwen-plus-character', 'qwen-turbo-latest', 'qwen-vl-max-latest', 'qwen-vl-ocr-latest', 'qwen-vl-plus-latest', 'qwq-plus-latest', 'text-embedding-async-v1', 'text-embedding-async-v2', 'text-embedding-v1', 'text-embedding-v2', 'text-embedding-v3', 'tongyi-intent-detect-v3', 'wanx2.0-t2i-turbo', 'wanx2.1-i2v-plus', 'wanx2.1-i2v-turbo', 'wanx2.1-t2i-plus', 'wanx2.1-t2i-turbo', 'wanx2.1-t2v-plus', 'wanx2.1-t2v-turbo', 'wanx-v1']
            }
        ]
)


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

print(response)
# 处理响应
print(f"回答：{response.choices.message.content}") # 回答：你好！我是通义千问，阿里巴巴集团旗下的超大规模语言模型。我能够回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。我熟练掌握多种语言，包括但不限于中文、英文、德语、法语、西班牙语等。如果你有任何问题或需要帮助，随时可以问我！
print(f"费用：{response.price.total_price} 元") # 费用：0.0001848 元