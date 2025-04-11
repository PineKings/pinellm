# 工具调用示例

# 引入相关模块
from pinellm import ChatRequest,Message,Tool
from pinellm.tools.tools_utilize import toolsutilize
from pinellm import ConfigManager

from totools import StructuredLogger
logger = StructuredLogger()
messages = [Message(role="system", content="你是一个导演，和你对话的是一个创意设计师，请根据创意设计师的需求，创作一个短视频文案，在创作过程中，不断与创意设计师沟通，设计完善的脚本。"),
            Message(role="user", content="我准备好了，开始对话吧！"),
            Message(role="assistant", content="视频的主题是：云南松子的电商短视频")]

def dialogue_director(message):
    global messages
    messages.append(Message(role="user", content=message))
    
    response = ChatRequest(
        model="qwen-plus",
        messages=messages
    ).send()
    logger.log("导演", response.choices.message.content)
    messages.append(Message(role="assistant", content=response.choices.message.content))
    return response.choices.message.content
    