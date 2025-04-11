# pinellm/config/config_manager.py
from .built.models import Built_Models
from .built.tools import Built_Tools
from .built.suppliers import Built_Suppliers
from ..schemas.safedot import SafeDotDict,WritableSafeDotDict, ModelTemplate,ToolTemplate,SupplierTemplate

class ConfigManager:
    """安全配置管理器
    
    方法：
     - load_config(tools:dict = {}, models:dict = {}, suppliers:list = []): 加载配置
     - get_supplier(model): 根据模型名称获取供应商信息
    
    属性：
     - Model_Map: 模型字典映射
     - Tools_Map: 工具字典映射
     - Supplier_Map: 供应商列表
    """
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            # 为每个映射指定模板
            cls._instance.Model_Map = WritableSafeDotDict(
                Built_Models,
                template=ModelTemplate
            )
            cls._instance.Tools_Map = WritableSafeDotDict(
                Built_Tools,
                template=None
            )
            cls._instance.Supplier_Map = WritableSafeDotDict(
                Built_Suppliers,
                template=SupplierTemplate
            )
        return cls._instance

    def load_config(self,tools:dict = {}, models:dict = {}, suppliers:dict = {}):
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
        
        suppliers = {
                "qwen":{
                "name": "qwen",
                "description": "阿里云",
                "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
                "api_key": os.getenv("QWEN_API_KEY"),  # 请自己替换一个阿里云api_key的替换逻辑
                "models":['multimodal-embedding-v1', 'qvq-max-latest', 'qwen-coder-plus-latest', 'qwen-coder-turbo-latest', 'qwen-long-latest', 'qwen-max', 'qwen-omni-turbo-latest', 'qwen-plus', 'qwen-plus-character', 'qwen-turbo-latest', 'qwen-vl-max-latest', 'qwen-vl-ocr-latest', 'qwen-vl-plus-latest', 'qwq-plus-latest', 'text-embedding-async-v1', 'text-embedding-async-v2', 'text-embedding-v1', 'text-embedding-v2', 'text-embedding-v3', 'tongyi-intent-detect-v3', 'wanx2.0-t2i-turbo', 'wanx2.1-i2v-plus', 'wanx2.1-i2v-turbo', 'wanx2.1-t2i-plus', 'wanx2.1-t2i-turbo', 'wanx2.1-t2v-plus', 'wanx2.1-t2v-turbo', 'wanx-v1']
                }
            }
        ```
        """
        # 检查是否存在重复的模型名称,如果存在，则新的模型（models）和旧的模型（Built_Models）合并，重复的参数被新的模型参数覆盖
    
        model_map = Built_Models.copy()
    
        # 遍历新字典中的每个模型
        for model_name, model_details in models.items():
            if model_name in Built_Models.keys():
                # 如果模型存在
                sub_dictionary = Built_Models.get(model_name).copy()
                for key, value in model_details.items():
                    sub_dictionary[key] = value
                model_map[model_name] = sub_dictionary
            else:
                # 如果模型不存在，则添加到字典中
                model_map[model_name] = model_details

        self.Model_Map = SafeDotDict(model_map)

        supplier_map = Built_Suppliers.copy()
    
        # 遍历新字典中的每个模型
        for supplier_name, supplier_details in suppliers.items():
            if supplier_name in Built_Suppliers.keys():
                # 如果模型存在
                sub_dictionary = Built_Suppliers.get(supplier_name).copy()
                for key, value in supplier_details.items():
                    if key == "models":
                        sub_dictionary[key] = list(set(sub_dictionary[key] + value))
                    sub_dictionary[key] = value
                supplier_map[supplier_name] = sub_dictionary
            else:
                # 如果模型不存在，则添加到字典中
                supplier_map[supplier_name] = supplier_details

        self.Supplier_Map = SafeDotDict(supplier_map)
    
        # 合并字典
        self.Tools_Map = SafeDotDict({
            **tools,  # 先复制第一个字典的所有键值
            **{k: v for k, v in Built_Tools.items() if k not in tools}
        })
        
        

    def get_supplier(self, model) -> dict:
        if self.Supplier_Map is None:
            for supplier,supplier_info in Built_Suppliers.items():
                if model in supplier_info.get("models", []):
                    return SafeDotDict(supplier_info)
        else:
            
            for supplier,supplier_info in self.Supplier_Map.to_dict().items():
               if model in supplier_info.get("models", []):
                    return SafeDotDict(supplier_info)
        return None
    
    