"""
构建数据对象

数据对象：
- ChatRequest: 聊天请求对象
- Propertie: 属性对象
- Tool: 工具对象
- Message: 消息对象
- ResponseFormat: 响应格式对象
- SafeDotDict: 安全点字典对象（将任何字典数据转换为SafeDotDict）

"""

from .safedot import SafeDotDict
from .chat_request import ChatRequest, Propertie, Tool, Message, ResponseFormat,Content


__all__ = [
    "SafeDotDict",
    "ChatRequest",
    "Propertie",
    "Tool",
    "Message",
    "ResponseFormat",
    "Content"
]