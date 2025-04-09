from pinellm import ConfigManager
config = ConfigManager()


# 设置参数
mymodels = {
    "qwen-plus":{
        "newname": "qwen-plus-latest",
        "name": "qwen-plus",
        "type": "text",
        "description": "能力均衡，推理效果、成本和速度介于通义千问-Max和通义千问-Turbo之间，适合中等复杂任务。",
        "price_in": 0.002,
        "price_out": 0.0008,
        "max_tokens_in": 129024,
        "max_tokens_out": 8192,
        "max_thought": 0,
        "max_context": 131072,
        "enable_search": True,
        "response_format": True,
        "tools": True,
        "text_input": True,
        "text_output": True,
        "audio_input": False,
        "audio_output": False,
        "image_input": False,
        "image_output": False,
        "video_input": False,
        "video_output": False,
        "thought_chain": False,
        "modalities": ["text"],
        "temperature": 0.95,
        "top_p": 0.7,
        "presence_penalty": 0.6,
        "n": 1,
        "seed": 1234
    }
}

config.load_config(models=mymodels)

# 设置供应商
mysuppliers = [
    {
        "name": "custom_supplier",
        "url": "https://api.example.com/v1/chat",
        "api_key": "YOUR_API_KEY", # 避免明文，可以是一个apikey的获取函数，如：os.getenv("API_KEY"),
        "models": ["qwen-plus-latest"]
    }
]

config.load_config(suppliers=mysuppliers)
