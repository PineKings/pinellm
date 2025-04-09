import requests
from typing import Dict, Union, Generator
import json

from ..schemas.safedot import SafeDotDict
from ..schemas.chat_request import ChatRequest
from ..config.supplier import Supplier
from .cost import cost



def stream_response(response):
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8').strip()
            if line.startswith("data: "):
                json_str = line[len("data: "):].strip()
                if json_str == "[DONE]":  # 可选：处理结束标记
                    break
                try:
                    data = json.loads(json_str)
                    yield data
                except json.JSONDecodeError as e:
                    print(f"解析JSON失败: {json_str}\n错误: {str(e)}")


def chat(payload: ChatRequest, headers:dict = None, stream:bool = False) -> SafeDotDict:
    """适合于非流式的对话，即使是思维模型（速度会比较慢），也会将所有内容一次性返回"""

    # 创建供应商实例
    supplier = Supplier(payload.model)
    
    # 设置请求头
    headers = {
        "Authorization": f"Bearer {supplier.api_key}",  # 设置授权信息
        "Content-Type": "application/json",  # 设置内容类型为JSON
        "Accept": "*/*",  # 接受所有类型的响应
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "PostmanRuntime-ApipostRuntime/1.1.0",
        "Connection": "keep-alive"
    }
    if supplier.api_key is None:
        from ..errors import SupplierError
        raise SupplierError(f"模型{payload.model}对应的供应商{supplier.supplier}没有配置API_KEY")
    
    if stream:
        responses = chat_stream(payload)
        if isinstance(responses, SafeDotDict):
            return responses
        else:
            reasoning_content = ''
            chat_content = ''
            tool_calls = None
            re_data = {}
            message = {}
            choice = {}
            first = True
            for response in responses:
                if first:
                    object = response.object
                    created = response.created
                    system_fingerprint = response.system_fingerprint
                    model = response.model
                    id = response.id
                    first = False
                if response.choices.message.content:
                    chat_content += response.choices.message.content
                else:
                    pass
                if response.choices.message.reasoning:
                    if "</think>" in response.choices.message.reasoning:
                        pass
                    else:
                        reasoning_content += response.choices.message.reasoning
                if response.choices.message.tool_calls.function.name:
                    tool_calls = [{
                        'function': {
                            'name': response.choices.message.tool_calls.function.name if response.choices.message.tool_calls.function.name else None, 
                            'arguments': response.choices.message.tool_calls.function.arguments if response.choices.message.tool_calls.function.arguments else "{}"
                        }, 
                        'index': response.choices.message.tool_calls.index, 
                        'id': response.choices.message.tool_calls.id, 
                        'type': response.choices.message.tool_calls.type
                    }]

            message["role"] = "assistant"
            message["content"] = chat_content
            message["reasoning_content"] = reasoning_content
            message["tool_calls"] = tool_calls if tool_calls else None
            re_data["object"] = object
            re_data["created"] = created
            re_data["system_fingerprint"] = system_fingerprint
            re_data["model"] = model
            re_data["id"] = id
            choice["message"] = message
            choice["finish_reason"] = "stop"
            re_data["choices"] = [choice]
            return SafeDotDict(re_data)
    response = requests.request("POST", url=supplier.api_url, json=payload.as_dict(), headers=headers) 
    
    if response.status_code == 200:    
        data = response.json()
        data["price"] = cost(SafeDotDict(data))
        data["error"] = False
        return SafeDotDict(data)
    elif response.status_code == 404:
            return SafeDotDict({
                "error": True,
                "status_code": response.status_code,
                "message": "404错误，请排查：供应商服务器错误/供应商配置的Api_Url错误/网络错误"
            })
    else:
        return SafeDotDict({
            "error": True,
            "status_code": response.status_code,
            "message": response.json().get("error",{}).get("message","请求失败"),
        })

def chat_stream(payload:ChatRequest, headers:dict = None) -> Union[SafeDotDict, Generator[SafeDotDict, None, None]]:
    """适合于流式的对话"""
    # 创建供应商实例
    supplier = Supplier(payload.model)
    
    # 设置请求头
    headers = {
        "Authorization": f"Bearer {supplier.api_key}",  # 设置授权信息
        "Content-Type": "application/json",  # 设置内容类型为JSON
        "Accept": "*/*",  # 接受所有类型的响应
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "PostmanRuntime-ApipostRuntime/1.1.0",
        "Connection": "keep-alive"
    }
    if supplier.api_key is None:
        from ..errors import SupplierError
        raise SupplierError(f"模型{payload.model}对应的供应商{supplier.supplier}没有配置API_KEY")
    
    payload = payload.as_dict()
    payload["stream"] = True
    response = requests.request("POST", url=supplier.api_url, json=payload, headers=headers) 
    if response.status_code == 200:
        for data in stream_response(response):
            data = SafeDotDict(data)
            reasoning_content = data.choices.delta.reasoning_content
            chat_content = data.choices.delta.content
            if data.choices.delta.tool_calls:
                tool_calls = SafeDotDict(data.choices.delta.tool_calls.to_dict())
            else:
                tool_calls = SafeDotDict({
                    'function': {'name': None, 'arguments': None}, 
                    'index': None, 'id': None, 'type': None
                })
            finish_reason = data.choices.finish_reason
            re_data = {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": chat_content,
                            "reasoning":reasoning_content,
                            "tool_calls":[{
                                'function': {
                                    'name': tool_calls.function.name if tool_calls.function else None, 
                                    'arguments': tool_calls.function.arguments if tool_calls.function else "{}"
                                }, 
                                'index': tool_calls.index, 
                                'id': tool_calls.id, 
                                'type': tool_calls.type
                            }]
                        },
                        "finish_reason": finish_reason,
                    }
                ],
                "object": data.object,
                "created": data.created,
                "system_fingerprint": data.system_fingerprint,
                "model": data.model,
                "id": data.id
            }
            yield SafeDotDict(re_data)
    elif response.status_code == 404:
            return SafeDotDict({
                "error": True,
                "status_code": response.status_code,
                "message": "404错误，请排查：供应商服务器错误/供应商配置的Api_Url错误/网络错误"
            })
    else:
        return SafeDotDict({
            "error": True,
            "status_code": response.status_code,
            "message": response.json().get("error",{}).get("message","请求失败"),
        })
