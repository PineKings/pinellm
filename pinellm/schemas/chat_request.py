import json
from typing import Dict, Union
import requests

from ..tools.basic.base_image import encode_image
from ..schemas.safedot import SafeDotDict


class Propertie:
    """表示调用的工具参数的结构
    
    参数：
    - name(str): 参数名称
    - description(str): 参数描述
    - type(str): 参数类型，可选值：`"string"` `"integer"` `"float"` `"boolean"`
    
    方法：
    - as_dict(): 将参数结构体转换为字典，用于发送到API
    """
    def __init__(self, name: str, description: str, type: str):
        self.name = name
        self.description = description
        self.type = type

    def as_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "type": self.type
        }
    
    def __repr__(self):
        return f"Propertie(name={self.name!r}, description={self.description!r}, type={self.type!r})"

class Tool:
    """表示工具定义的结构
    
    参数：
    - name(str): 工具的函数或者接口名称
    - description(str): 工具描述
    - properties(list[Propertie]): 工具参数列表，需要通过`Propertie`类创建
    
    方法：
    - as_dict(): 将工具结构体转换为字典，用于发送到API
    """
    def __init__(self, name: str, description: str, properties:list[Propertie] = None):
        from ..config.config_manager import ConfigManager
        ToolsMap = ConfigManager().Tools_Map
        toolsname = [key for key in ToolsMap.to_dict().keys()]
        if name not in toolsname:
            raise ValueError(f"工具{name}未定义！")
        self.name = name
        self.description = description
        if properties is None:
            self.properties = None
            self.required = []
        else:
            self.required = [prop.name for prop in properties]
            self.properties = {prop.name: {"type":prop.type, "description":prop.description} for prop in properties}

    def as_dict(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {  
                    "type": "object",
                    "properties": self.properties
                },
                "required": self.required
            }
        }

    def __repr__(self):
        return f"Tool(name={self.name!r}, description={self.description!r}, properties={self.properties!r})"

class Content:
    """表示图片消息的结构
    
    参数：
    - role(str): 角色，可选值：`"system"` `"user"` `"assistant"` `tool`
    - content(str): 内容
    
    方法：
    - as_dict(): 将消息结构体转换为字典，用于发送到API
    """
    def __init__(self,image_urls: list[str] = None, text: str = None):
        self.text = text
        self.image_urls = image_urls
        if image_urls is None:
            self.content = text
        else:
            self.text = text
            self.image_urls = image_urls
            content = []
            for url in image_urls:
                # 如果url是httptp:// 或者 https://开头
                if url.startswith("http://") or url.startswith("https://"):
                    content.append({
                        "type": "image_url",
                        "image_url": {
                            "url": url
                        }
                    })
                else:
                    content.append({
                        "type": "image_url",
                        "image_url": {
                            "url": encode_image(url)
                        }
                    })
            if text is not None:
                content.append({
                    "type": "text",
                    "text": text
                })
                
            self.content = content

    def as_dict(self):
        return self.content
    
    def __repr__(self):
        if self.image_urls is None:
            return f"Content(text={self.text!r})"
        else:
            return f"Content(image_urls={self.image_urls!r}, text={self.text!r})"
    
class Message:
    """表示对话消息的结构
    
    参数：
    - role(str): 角色，可选值：`"system"` `"user"` `"assistant"` `tool`
    - content(str): 内容
    
    方法：
    - as_dict(): 将消息结构体转换为字典，用于发送到API
    """
    def __init__(self, role: str, content: Union[Content,str], tool_call_id: str = None,tool_calls:list = None,*args, **kwargs):
        self.role = role
        if isinstance(content, Content):
            self.content = content.as_dict()
        else:
            self.content = Content(text=content).as_dict()
            
        if role == "tool":
            self.tool_call_id = tool_call_id
        else:
            self.tool_call_id = None
        if tool_calls is not None:
            if type(tool_calls) != list:
                self.tool_calls = [tool_calls]
            self.tool_calls = tool_calls
        else:
            self.tool_calls = None

    def as_dict(self):
        if self.role == "tool":
            return {
                "role": self.role,
                "content": self.content,
                "tool_call_id": self.tool_call_id
            }
        elif self.tool_calls is not None and self.role == "assistant":
            return {
                "role": self.role,
                "content": self.content,
                "tool_calls": self.tool_calls
            }
        else:
            return {
                "role": self.role,
                "content": self.content
            }

    def __repr__(self):
        if self.role == "tool":
            return f"Message(role={self.role}, content={self.content!r}, tool_call_id={self.tool_call_id!r})"
        elif self.tool_calls is not None and self.role == "assistant":
            return f"Message(role={self.role}, content={self.content!r}, tool_calls={self.tool_calls!r})"
        else:
            return f"Message(role={self.role}, content={self.content!r})"

class ResponseFormat:
    """表示响应格式的结构"""
    def __init__(self, type: str):
        self.type = type

    def as_dict(self):
        return {"type": self.type}

    def __repr__(self):
        return f"ResponseFormat(type={self.type!r})"

class ChatRequest:
    """完整的llm请求结构体,其中`model`和`messages`为必须参数，其他参数可选，为空则调用`config`模块中定义的默认值
    
    参数：
    - model(str): 【必要】模型名称
    - messages(list[Message]): 【必要】对话消息列表，需要通过`Message`类创建
    - modalities(list[str]): 输出的模态类型，只支持Qwen-Omni模型，可选值：`["text"]`，默认为`["text"]`
    - temperature(float): 采样温度，控制模型生成文本的多样性，越高越多样。取值范围 `[0, 2)`，默认为0.7
    - top_p(float): 采样Top-p，控制模型生成文本的确定性，越低越确定。取值范围`[0, 1)`，默认为`0.8`
    - presence_penalty(float): 阻止模型生成重复文本的惩罚系数，取值范围 `[-2, 2)`，默认为`0`，正数会减少重复度（专业性），负数会增加重复度（创造性）
    - response_format(ResponseFormat): 返回内容的格式。可选值：`{"type": "text"}`或`{"type": "json_object"}`，当为`json_object`时，必须在提示词中指定返回格式，需通过`ResponseFormat`类创建
    - max_tokens(int): 返回内容的最大Token数
    - n(int): 返回内容的数量，默认为1
    - seed(int): 内容的随机种子，取值范围：0到2^31−1，默认为1234
    - tools(list[Tool]): 可供模型调用的工具数组，可以包含一个或多个工具对象。一次Function Calling流程模型会从中选择一个工具，需要通过`Tool`类创建
    - tool_choice(any): 工具选择策略，可选值：`"auto"`/`"none"`/`{"type": "function", "function": {"name": "the_function_to_call"}}`。默认为`"auto"`，表示模型会根据上下文自动选择工具；`"none"`表示不调用工具；`"function"`表示调用指定的工具。
    - enable_search(bool): 是否启用搜索，若模型不支持，则忽略该参数。默认为`False`
    - model_version(int): 模型版本，默认为1,可选值：1/2/3,1/2为稳定版，最新版，3为自定义版本
    - model_name(str): 模型名称，默认为None，当`model_version`为3时，该参数必填，请确保该模型存在
    
    方法：
    - as_dict(): 将请求结构体转换为字典，用于使用外部函数发送到API
    - send(): 直接发送请求到API，并返回响应
    
    """
    def __init__(
        self,
        model: str,
        messages: list[Message],
        modalities: list[str] = None,
        temperature: float = None,
        top_p: float = None,
        presence_penalty: float = None,
        response_format: ResponseFormat = None,
        max_tokens: int = None,
        n: int = None,
        seed: int = None,
        tools: list[Tool] = None,
        tool_choice: str = None,
        enable_search: bool = None,
        model_version: int  = 1,
        model_name: str = None,
        stream = False
    ):
        from ..config.config_manager import ConfigManager
        
        self.messages = messages
        model_info = ConfigManager().Model_Map.get(model)
        if model_info is None:
            from ..errors import ModelError
            raise ModelError(f"模型: {model} 不存在,请确保配置文件中包含该模型")
        if model_version == 2:
            self.model = model_info.newname if model_info.newname is not None else model
        elif model_version == 3:
            if model_name is None:
                raise ParamError("当model_version为3时，model_name不能为空")
            self.model = model_name
        else:  # model_version 默认为1
            self.model = model
        self.modalities = ["text"] if modalities is None else modalities
        
        self.temperature = model_info.temperature if temperature is None else temperature
        self.top_p = model_info.top_p if top_p is None else top_p
        self.presence_penalty = model_info.presence_penalty if presence_penalty is None else presence_penalty
        self.response_format = ResponseFormat("text") if response_format is None else response_format
        self.max_tokens = model_info.max_tokens_out if max_tokens is None else max_tokens
        self.n = model_info.n if n is None else n
        self.seed = model_info.seed if seed is None else seed
        self.tools = tools if model_info.tools else None
        self.tool_choice = None if self.tools is None else tool_choice
        self.enable_search = None if model_info.enable_search is False else enable_search
        self.stream = stream if model_info.thought_chain is False else True
        self.thought_chain = model_info.thought_chain if model_info.thought_chain else False

    def as_dict(self):
        data = {}
        if self.model is not None:
            data["model"] = self.model
        if self.messages is not None:
            data["messages"] = [msg.as_dict() for msg in self.messages]
        if self.modalities is not None:
            data["modalities"] = self.modalities
        if self.temperature is not None:
            data["temperature"] = self.temperature
        if self.top_p is not None:
            data["top_p"] = self.top_p
        if self.presence_penalty is not None:
            data["presence_penalty"] = self.presence_penalty
        if self.response_format is not None:
            data["response_format"] = self.response_format.as_dict()
        if self.max_tokens is not None:
            data["max_tokens"] = self.max_tokens
        if self.n is not None:
            data["n"] = self.n
        if self.seed is not None:
            data["seed"] = self.seed
        if self.tools is not None:
            data["tools"] = [tool.as_dict() for tool in self.tools]
        if self.tool_choice is not None:
            data["tool_choice"] = self.tool_choice
        if self.enable_search is not None:
            data["enable_search"] = self.enable_search
        if self.stream is not None:
            data["stream"] = self.stream
        for key, value in data.items():
            if value is None:
                del data[key]
        return data

    def __repr__(self):
        return (f"ChatRequest("
                f"model={self.model!r}, "
                f"messages={self.messages!r}, "
                f"modalities={self.modalities!r}, "
                f"temperature={self.temperature}, "
                f"top_p={self.top_p}, "
                f"presence_penalty={self.presence_penalty}, "
                f"response_format={self.response_format!r}, "
                f"max_tokens={self.max_tokens}, "
                f"n={self.n}, "
                f"seed={self.seed}, "
                f"tools={self.tools!r}, "
                f"tool_choice={self.tool_choice!r}, "
                f"enable_search={self.enable_search})"
        )
    
    def send(self):
        """直接请求请求"""
        from ..llm_chat.request import chat
        if self.thought_chain:
            return chat(payload=self, stream=True)
        else:
            self.stream = False
            return chat(payload=self)

    def send_stream(self):
        """流式请求，返回流"""
        from ..llm_chat.request import chat_stream
        self.stream = True
        return chat_stream(payload=self)

# 使用示例
if __name__ == "__main__":
    # 创建消息对象
    messages = [
        Message("system", "You are a helpful assistant."),
        Message("user", "你是谁？现在是几点了")
    ]
    
    tools = [
        Tool("get_weather","查询天气",[Propertie("location", "城市或县区，比如北京市、杭州市、余杭区等。", "string")]),
        Tool("get_news","查询新闻",[Propertie("topic", "新闻主题，比如体育、娱乐等。", "string")])
    ]
    

    # 创建完整请求对象
    request = ChatRequest(
        model="qwen-plus",
        messages=messages,
        modalities=["text"],
        temperature=0.7,
        top_p=0.8,
        presence_penalty=0,
        response_format=ResponseFormat("text"),
        n=1,
        seed=1234,
        tools=tools,  # 假设 config.llm_tools 是一个列表
        tool_choice="auto",
        enable_search=False
    )

    print(request.as_dict())