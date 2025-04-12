import requests
from typing import Dict, Union, Generator
import json

from ..schemas.safedot import SafeDotDict
from ..schemas.chat_request import ChatRequest
from ..config.supplier import Supplier
from .cost import cost


def embedding(payload: ChatRequest, headers:dict = None, stream:bool = False) -> SafeDotDict:
    """适合于非流式的对话，即使是思维模型（速度会比较慢），也会将所有内容一次性返回"""

    # 创建供应商实例
    supplier = Supplier(payload.model)
    payload_data = payload.as_dict()
    
    # 如果厂商是zhipu，如果调用工具，如果工具没有参数，则修改parameters
    if supplier.supplier == "zhipu" and payload_data.get("tools", None) is not None:
        for tool in payload_data.get("tools", None):
            if tool.get("function", {}).get("parameters", {}).get("properties",{}) is None:
                tool["function"] = {
                    "name": tool["function"]["name"],
                    "description": tool["function"]["description"],
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
    if supplier.supplier == "zhipu" and payload.enable_search is True:
        web_search = {
            "type": "web_search",
            "web_search": {
                "enable": True  # 启用网络搜索
            }
        }
        payload_data["tools"].append(web_search)
        
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
    print(f"请求体：{payload_data}")
   
    response = requests.request("POST", url=supplier.api_url, json=payload_data, headers=headers) 
    print(f"状态码：{response.status_code}，响应内容：{response.text}")
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
