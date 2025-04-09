"""
pinellm
========

一个用于处理和国内LLM供应商调用模型的 Python 包。

:Author: PineKing <work.wss@icloud.com>
:Version: 1.0.0
:License: MIT License
:Description: 提供高效便捷的国内厂商各类模型调用服务，支持 [功能1]、[功能2] 等核心模块。

Usage:
------
>>> from pinellm import ChatRequest, Message, ResponseFormat, Tool, Propertie
>>> from pinellm import models, Supplier
>>> from pinellm import Setting,chat,SafeDotDict
>>> # 创建消息对象
>>> messages = [
>>>     Message("system", "You are a helpful assistant."),
>>>     Message("user", "你是谁？曲靖现在是什么天气？")
>>> ]
>>> # 创建工具对象
>>> tools = [
>>>     Tool("get_weather","查询天气",[Propertie("location", "城市或县区，比如北京市、杭州市、余杭区等。", "string")]),
>>>     Tool("get_news","查询新闻",[Propertie("topic", "新闻主题，比如体育、娱乐等。", "string")])
>>> ]
>>> # 创建完整请求对象
>>> request = ChatRequest(
>>>     model="qwen-plus",
>>>     messages=messages,
>>>     tools=tools,  # 假设 config.llm_tools 是一个列表
>>>     tool_choice="auto",
>>>     enable_search=False
>>> )
>>> # 调用 chat 函数
>>> aaa = chat(request)
"""
from .config.config_manager import ConfigManager
from .llm_chat.request import chat,chat_stream
from .schemas.chat_request import ChatRequest,Content,Message,Tool,Propertie
from .tools.tools_utilize import toolsutilize

__all__ = [
    "chat",
    "ChatRequest",
    "Message",
    "Tool",
    "Propertie",
    "Content",
    "ConfigManager",
    "toolsutilize",
    "chat_stream"
]
