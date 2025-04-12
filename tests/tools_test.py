# 工具调用示例

# 引入相关模块
from pinellm import ChatRequest,Message,Tool,Propertie
from pinellm.tools.tools_utilize import toolsutilize
from pinellm import ConfigManager
from datetime import datetime

# 获取当前日期
current_date = datetime.now().strftime("%Y-%m-%d")
# 配置文件
config = ConfigManager()

# 增加自定义工具
def get_name():
    return "PineKing"

mytools = {
    "get_name": get_name
}
config.load_config(tools=mytools)

# 调用工具
## 构建消息列表
messages = [Message(role="system", content=f"你是一个具备网络访问能力的智能助手，在适当情况下，优先使用网络信息（参考信息）来回答，以确保用户得到最新、准确的帮助。当前日期是 {current_date}。"),
            Message(role="user", content="2024年美国大选的结果")]

## 构建请求体并直接发送请求
response = ChatRequest(
    model="glm-4-plus",
    messages=messages,
    tools=[Tool(name="get_name",description="获取助理名字")],
    enable_search=True
).send()

if response.error:
    print("\n\n=================错误=================")
    print(response.message)
    exit()
if response.choices.message.reasoning_content:
    print("\n\n=================思考=================")
    print(response.choices.message.reasoning_content)
if  response.choices.message.content:
    print("\n\n=================回复=================")
    print(response.choices.message.content)
if response.choices.message.tool_calls:
    print("\n\n=================工具调用=================")
    function_name = response.choices.message.tool_calls.function.name
    print(f"开始调用：{function_name}")
    ## 调用工具
    tool_messages = toolsutilize(response)
    ## 如果结果不需要返回大模型处理，则直接返回工具返回的消息
    print("\n\n=================工具返回=================")
    print(f"工具返回：{tool_messages[-1].content}")
    
    ## 如果结果需要返回大模型处理，则将工具返回的消息添加到消息列表中，再次发送请求
    messages += tool_messages
    response = ChatRequest(
        model="glm-4-plus",
        messages=messages,
        tools=[Tool(name="get_name",description="获取助理名字")],
        enable_search=True
    ).send()

    if response.choices.message.reasoning_content:
        print("\n\n=================思考=================")
        print(response.choices.message.reasoning_content)
    if  response.choices.message.content:
        print("\n\n=================回复=================")
        print(response.choices.message.content)