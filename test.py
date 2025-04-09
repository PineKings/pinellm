from pinellm import ChatRequest, Message, ResponseFormat, Tool, Propertie
from pinellm import Supplier,config
from pinellm import chat,SafeDotDict,Content
from pinellm import tools as pinetools
import os


SupplierList = [
    {
    "name": "qwen",
    "description": "阿里云",
    "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    "api_key": os.getenv("QWEN_API_KEY"),  # 请自己替换一个阿里云api_key的替换逻辑
    "models":['multimodal-embedding-v1', 'qvq-max-latest', 'qwen-coder-plus-latest', 'qwen-coder-turbo-latest', 'qwen-long-latest', 'qwen-max', 'qwen-omni-turbo-latest', 'qwen-plus', 'qwen-plus-character', 'qwen-turbo-latest', 'qwen-vl-max-latest', 'qwen-vl-ocr-latest', 'qwen-vl-plus-latest', 'qwq-plus-latest', 'text-embedding-async-v1', 'text-embedding-async-v2', 'text-embedding-v1', 'text-embedding-v2', 'text-embedding-v3', 'tongyi-intent-detect-v3', 'wanx2.0-t2i-turbo', 'wanx2.1-i2v-plus', 'wanx2.1-i2v-turbo', 'wanx2.1-t2i-plus', 'wanx2.1-t2i-turbo', 'wanx2.1-t2v-plus', 'wanx2.1-t2v-turbo', 'wanx-v1']
    }
]

# 创建消息对象
messages = [
    Message("system", Content(text="你是一个智能助手，请根据用户的问题回答。"))
]

tools = [
    Tool("get_weather","查询天气",[Propertie("location", "城市或县区，比如北京市、杭州市、余杭区等。", "string")]),
    pinetools.get_tools_info(1)
]
while True:
    user_input = input("\n**************************\n**************************\n用户说：(exit:退出)\n")
    if user_input == "exit":
        break
    messages.append(Message("user", Content(text=user_input)))
    # 创建完整请求对象
    request = ChatRequest(
        model="qwen-plus",
        messages=messages,
        tools=tools,  # 假设 config.llm_tools 是一个列表
        tool_choice="auto",
        enable_search=False
    )

    aaa = chat(request)
    tool_calls=aaa.choices.message.tool_calls
    if tool_calls:
        while tool_calls:
            aaa2 = pinetools.toolsutilize(aaa)
            messages += aaa2
            request = ChatRequest(
                model="qwen-plus",
                messages=messages,
                tools=tools,  # 假设 config.llm_tools 是一个列表
                tool_choice="auto",
                enable_search=False
            )
            aaa = chat(request)
            if aaa.choices.message.content:
                print("\n**************************\n**************************\n大模型说：\n")
                print(aaa.choices.message.content)
            tool_calls=aaa.choices.message.tool_calls
    else:
        print("\n**************************\n**************************\n大模型说：\n")
        print(aaa.choices.message.content)
        messages.append(Message("assistant", Content(text=aaa.choices.message.content)))