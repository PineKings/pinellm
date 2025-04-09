import requests
from typing import Dict, Union

from ..schemas import SafeDotDict, ChatRequest
from ..config import Supplier
from .cost import cost

def chat(payload:ChatRequest, headers:dict = None) -> Union[SafeDotDict, dict]:
    # 打印模型信息
    #print(f"模型 {payload.model} ")
    # 创建供应商实例
    supplier = Supplier(payload.model)
    # 打印供应商信息
    #print(f"供应商 {supplier.supplier}")
    
    # 设置请求头
    headers = {
        "Authorization": f"Bearer {supplier.api_key}",  # 设置授权信息
        "Content-Type": "application/json",  # 设置内容类型为JSON
        "Accept": "*/*",  # 接受所有类型的响应
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "PostmanRuntime-ApipostRuntime/1.1.0",
        "Connection": "keep-alive"
    }
    #print(f"请求体：{payload.as_dict()}")
    response = requests.request("POST", url=supplier.api_url, json=payload.as_dict(), headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        data["price"] = cost(SafeDotDict(data))
        return SafeDotDict(data)
    else:
        return SafeDotDict({
            "error": True,
            "status_code": response.status_code,
            "message": response.text,
        })
