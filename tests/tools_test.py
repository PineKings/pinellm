# 工具调用示例

# 引入相关模块
from pinellm import ChatRequest,Message,Tool
from pinellm import toolsutilize
from pinellm import ConfigManager

# 配置文件
config = ConfigManager()
# 增加自定义工具
def get_neme():
    return "PineKing"

mytools = {
    "get_neme": get_neme
}
config.load_config(tools=mytools)

# 调用工具
## 构建消息列表
messages = [Message(role="system", content="你是一位用户对话助理，请根据用户需求提供帮助"),
            Message(role="user", content="请告诉我你的名字")]

## 构建请求体并直接发送请求
response = ChatRequest(
    model="qwen-plus",
    messages=messages,
    tools=[Tool(name="get_neme",description="获取助理名字",properties=None)]
).send()

# 判断是否调用工具
if response.choices.message.tool_calls:
    ## 调用工具
    tool_messages = toolsutilize(response)
    ## 如果结果不需要返回大模型处理，则直接返回工具返回的消息
    print(tool_messages[-1].content) # 返回：PineKing
    
    ## 如果结果需要返回大模型处理，则将工具返回的消息添加到消息列表中，再次发送请求
    messages += tool_messages
    response = ChatRequest(
        model="qwen-plus",
        messages=messages,
        tools=[Tool(name="get_neme", description="获取助理名字", properties=None)]
    ).send()
    ## 大模型返回结果
    print(response.choices.message.content) # 返回：我的名字是PineKing。很高兴为您服务！