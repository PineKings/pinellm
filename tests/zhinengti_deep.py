# 工具调用示例

# 引入相关模块
from pinellm import ChatRequest,Message,Tool
from pinellm.tools.tools_utilize import toolsutilize
from pinellm import ConfigManager,Propertie

from zhinengti_qwen import dialogue_director
from totools import StructuredLogger

logger = StructuredLogger()

# 全局变量
if_while = True

# 配置文件
config = ConfigManager()
# 增加自定义工具
def get_name():
    return "PineKing"


# 调用工具
## 构建消息列表
daoyan_messages = [Message(role="system", content="你是一位创意设计专家，正在和你沟通的是导演，你需要与导演进行对话，设计合适的脚本，并确保脚本的完整，你无法判断任务的完成状态，必须不断进行优化。"),
            Message(role="user", content="视频的主题是：云南松子的电商短视频")]

logger.log("系统", "开始任务")
logger.log("用户", "视频的主题是：云南松子的电商短视频")
while if_while:
    ## 构建请求体并直接发送请求
    response = ChatRequest(
        model="qwen-plus",
        messages=daoyan_messages
    ).send()

    if  response.choices.message.content:
        logger.log("创意设计师", f"{response.choices.message.content}")
        daoyan_messages.append(Message(role="assistant", content=response.choices.message.content))
        new_message = dialogue_director(message=response.choices.message.content)
        if new_message:
            daoyan_messages.append(Message(role="user", content=new_message))
        else:
            continue
    else:
        continue
        