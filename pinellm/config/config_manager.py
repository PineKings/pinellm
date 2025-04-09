# pinellm/config/config_manager.py
from .built import Built_Models,Built_Suppliers,Built_Tools
from ..schemas import SafeDotDict

class ConfigManager:
    """安全配置管理器
    
    方法：
     - load_config(tools:dict = {}, models:dict = {}, suppliers:list = []): 加载配置
     - get_supplier(model): 根据模型名称获取供应商信息
    
    属性：
     - Model_Map: 模型字典映射
     - Tools_Map: 工具字典映射
     - Supplier_List: 供应商列表
    """
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.Model_Map = SafeDotDict(Built_Models)
            cls._instance.Tools_Map = SafeDotDict(Built_Tools)
            cls._instance.Supplier_List = Built_Suppliers
        return cls._instance

    def load_config(self,tools:dict = {}, models:dict = {}, suppliers:list = []):
        """加载配置

        Args:
            tools (dict, optional): 自定义的工具字典映射. Defaults to {}.
            models (dict, optional): 模型字典. Defaults to {}.
            suppliers (list, optional): 模型厂商列表. Defaults to [].
            
        格式：
        ```
        tools = {
            "get_current_time": get_current_time
        }
        models = {
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
        
        suppliers = [
                {
                "name": "qwen",
                "description": "阿里云",
                "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
                "api_key": os.getenv("QWEN_API_KEY"),  # 请自己替换一个阿里云api_key的替换逻辑
                "models":['multimodal-embedding-v1', 'qvq-max-latest', 'qwen-coder-plus-latest', 'qwen-coder-turbo-latest', 'qwen-long-latest', 'qwen-max', 'qwen-omni-turbo-latest', 'qwen-plus', 'qwen-plus-character', 'qwen-turbo-latest', 'qwen-vl-max-latest', 'qwen-vl-ocr-latest', 'qwen-vl-plus-latest', 'qwq-plus-latest', 'text-embedding-async-v1', 'text-embedding-async-v2', 'text-embedding-v1', 'text-embedding-v2', 'text-embedding-v3', 'tongyi-intent-detect-v3', 'wanx2.0-t2i-turbo', 'wanx2.1-i2v-plus', 'wanx2.1-i2v-turbo', 'wanx2.1-t2i-plus', 'wanx2.1-t2i-turbo', 'wanx2.1-t2v-plus', 'wanx2.1-t2v-turbo', 'wanx-v1']
                }
            ]
        ```
        """
        # 检查是否存在重复的模型名称
        self.Model_Map = SafeDotDict({
            **models,  # 先复制第一个字典的所有键值
            **{k: v for k, v in Built_Models.items() if k not in models}
        })
        
        self.Tools_Map = SafeDotDict({
            **tools,  # 先复制第一个字典的所有键值
            **{k: v for k, v in Built_Tools.items() if k not in tools}
        })
        
        merged = []
        url_set = set()  # 用于快速查找已存在的URL
        
        # 先处理第一个列表，确保所有条目都被保留
        for item in suppliers:
            merged.append(item)
            url_set.add(item['url'])
        
        # 处理第二个列表，仅添加URL未出现过的条目
        for item in Built_Suppliers:
            current_url = item['url']
            if current_url not in url_set:
                merged.append(item)
                url_set.add(current_url)
        
        self.Supplier_List = merged

    def get_supplier(self, model) -> dict:
        if self.Supplier_List is None:
            for supplier in Built_Suppliers:
                if model in supplier.get("models", []):
                    return supplier
        else:
            for supplier in self.Supplier_List:
                if model in supplier.get("models", []):
                    return supplier
        return None
    

    def get_model(self, model):
        return self.Model_Map.get(model, None)
    