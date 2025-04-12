# pinellm/config/config_manager.py
from .built.models import Built_Models
from .built.tools import Built_Tools
from .built.suppliers import Built_Suppliers
from .built.emb_models import Built_EmbModels
from ..schemas.safedot import SafeDotDict,WritableSafeDotDict, ModelTemplate,SupplierTemplate,EmbModelTemplate

from typing import Union

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
            cls._instance.Emb_Model_Map = WritableSafeDotDict(
                Built_EmbModels,
                template=EmbModelTemplate
            )
            
        return cls._instance

    def load_config(self,tools:dict = {}, models:dict = {}, suppliers:dict = {}, emb_models:dict = {}):
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
        
        emb_models_map = Built_EmbModels.copy()
    
        # 遍历新字典中的每个模型
        for emb_model_name, emb_model_details in emb_models.items():
            if emb_model_name in Built_EmbModels.keys():
                # 如果模型存在
                sub_dictionary = Built_EmbModels.get(model_name).copy()
                for key, value in model_details.items():
                    sub_dictionary[key] = value
                emb_models_map[model_name] = sub_dictionary
            else:
                # 如果模型不存在，则添加到字典中
                emb_models_map[model_name] = model_details
        
        
        self.Emb_Model_Map = SafeDotDict(emb_models_map)
    
        # 合并字典
        self.Tools_Map = SafeDotDict({
            **tools,  # 先复制第一个字典的所有键值
            **{k: v for k, v in Built_Tools.items() if k not in tools}
        })

    def get_supplier(self, model) -> dict:
        """获取模型对应的供应商信息"""
       
        suppliers = self.Supplier_Map.to_dict()
        
        def _supplier(info:SafeDotDict):
            #print(f"找到模型{model}配置信息: {info}")
            supplier = info.supplier
            modelname = info.name
            #print(f"供应商: {supplier}, 模型名称: {modelname}")
            #print(f"供应商列表：{suppliers.keys()}")
            if supplier in suppliers.keys():
                
                return suppliers[supplier]
            else:
                # 如果不在供应商配置的键中，则去供应商配置的 models 和 emb_models 中查找是否存在
                for supplier_key,supplier_value in suppliers.items():
                    if supplier_key == '_template':
                        continue
                    if modelname in supplier_value.get('models',[]):
                        return suppliers[supplier_key]
                    elif modelname in supplier_value.get('emd_models',[]):
                        return suppliers[supplier_key]
                raise Exception(f"没有找到模型{model}的供应商信息: 供应商的模型配置中无此模型")
        modelinfo = self.get_model(model)
        return _supplier(modelinfo)

    def get_model(self, model) -> Union[SafeDotDict,any]:
        """解决模型命名或者格式不一致下获取模型信息"""
        if self.Supplier_Map is None or self.Model_Map is None or self.Emb_Model_Map is None:
            raise Exception("请先配置模型和供应商信息")
        models = self.Model_Map.to_dict()
        emb_models = self.Emb_Model_Map.to_dict()
        suppliers = self.Supplier_Map.to_dict()
        
        if model in models.keys() or model in emb_models.keys():
            if model in emb_models.keys():
                return SafeDotDict(emb_models.get(model))
            else:
                return SafeDotDict(models.get(model))
        
        for a in models.values():
            if isinstance(a, dict):
                if model == a.get('name') or model == a.get('newname',None):
                    return SafeDotDict(a)
            else:
                continue
        for b in emb_models.values():
            #print(f"在{b}中查找模型{model}")
            if isinstance(b, dict):
                if model == b.get('name') or model == b.get('newname',None):
                    return SafeDotDict(b)
            else:
                continue
        raise Exception(f"没有找到模型{model}的配置信息,模型没有配置")