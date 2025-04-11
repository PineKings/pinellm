from typing import Union,Callable

class SupplierTemplate:
    allowed_fields = {
        "name": (str, None),          # 必须是字符串，无默认值
        "description": (str, ""),     # 字符串，默认空字符串
        "url": (str, None),
        "api_key": (str,None),  # 字符串或函数
        "models": (list, []),         # 列表，默认空列表
        "type": (str, "default_type") # 字符串，默认值
    }

class ModelTemplate:
    allowed_fields = {
        "newname": (str, None),
        "name": (str, None),
        "type": (str, "text"),
        "description": (str, ""),
        "price_in": (float, None),
        "price_out": (float, None),
        "max_tokens_in": (int, None),
        "max_tokens_out": (int, None),
        "max_thought": (int, None),
        "max_context": (int, None),
        "enable_search": (bool, False),
        "response_format": (bool, False),
        "tools": (bool, False),
        "text_input": (bool, False),
        "text_output": (bool, False),
        "audio_input": (bool, False),
        "audio_output": (bool, False),
        "image_input": (bool, False),
        "image_output": (bool, False),
        "video_input": (bool, False),
        "video_output": (bool, False),
        "thought_chain": (bool, False),
        "modalities": (list, ["text"]),
        "temperature": (float, None),
        "top_p": (float, None),
        "presence_penalty": (float, None),
        "n": (int, None),
        "seed": (int, None)
    }

class ToolTemplate:
    allowed_fields = {
        "name": (str, None),
        "description": (str, ""),
        "function": (object, None),
        "parameters": (dict, {})
    }

class NoneProxy:
    """代理对象，用于返回 None 并支持嵌套访问"""
    def __getattr__(self, name):
        return NoneProxy()

    def __bool__(self):
        return False

    def __repr__(self):
        return 'None'

class ListProxy:
    """包装列表，访问属性时默认返回第一个元素的属性"""
    def __init__(self, lst):
        self.lst = lst

    def __getattr__(self, name):
        if self.lst:
            first_element = self.lst[0]
            if isinstance(first_element, dict):
                return getattr(SafeDotDict(first_element), name)
            else:
                return getattr(first_element, name, NoneProxy())
        else:
            return NoneProxy()

    def __getitem__(self, index):
        item = self.lst[index]
        if isinstance(item, dict):
            return SafeDotDict(item)
        else:
            return item

    def __len__(self):
        return len(self.lst)

    def __repr__(self):
        return f"ListProxy({self.lst!r})"

class SafeDotDict:
    """安全访问字典，支持点号访问和嵌套字典的访问
    
    参数：
    - data: 字典数据
    
    方法：
    - to_dict: 还原为字典
    - __getattr__: 支持点号访问
    - __getitem__: 支持索引访问
    - get: 支持获取默认值
    """
    def __init__(self, data: dict):
        self._data = data

    def __getattr__(self, name):
        if name in self._data:
            value = self._data[name]
            if isinstance(value, dict):
                return SafeDotDict(value)
            elif isinstance(value, list):
                return ListProxy(value)
            else:
                return value
        else:
            return NoneProxy()

    def __getitem__(self, key):
        return self.__getattr__(key)

    def get(self, key, default=None):
        value = self.__getattr__(key)
        if isinstance(value, NoneProxy):
            return default
        return value

    def to_dict(self):
        def _to_dict(obj):
            if isinstance(obj, SafeDotDict):
                return {k: _to_dict(v) for k, v in obj._data.items()}
            elif isinstance(obj, list):
                return [_to_dict(item) for item in obj]
            else:
                return obj
        return _to_dict(self)

    def __repr__(self):
        return f"SafeDotDict({self._data!r})"

    def __setattr__(self, name, value):
        """支持通过点号设置属性"""
        if name == "_data":
            super().__setattr__(name, value)
        else:
            # 将属性赋值转换为字典键的赋值
            self._data[name] = value

    def __setitem__(self, key, value):
        """支持通过索引设置值"""
        self._data[key] = value
        
class WritableSafeDotDict(SafeDotDict):
    def __init__(self, data, template=None):
        super().__init__(data)
        self._template = template  # 模板对象，如 SupplierTemplate

    def __setattr__(self, name, value):
        if name in ("_data", "_template"):
            super().__setattr__(name, value)
            return
        
        if self._template:
            field_type, default = self._template.allowed_fields[name]
            
            # 验证属性是否在模板允许的字段中
            if self._template and name not in self._template.allowed_fields:
                raise AttributeError(
                    f"'{name}'参数不存在，无法设置！\n请选择以下参数：{list(self._template.allowed_fields.keys())}"
                )
            
            
            if not isinstance(value, field_type):
                raise TypeError(
                    f"参数 '{name}' 必须是类型 {field_type.__name__}，但传入了类型 {type(value).__name__}"
                )
            
            # 如果是嵌套字典，递归验证
            if isinstance(value, dict):
                self._data[name] = WritableSafeDotDict(value, template=self._template)
            else:
                self._data[name] = value
        else:
            if isinstance(value, dict):
                raise AttributeError(
                    f"工具映射不允许嵌套字典，但传入了字典 {value}"
                )
            if not isinstance(value, Callable):
                raise AttributeError(
                    f"工具映射必须是一个函数，但传入了 {type(value)}"
                )
            self._data[name] = value

    def __getattr__(self, name):
        # 保持原有功能，但新增自动创建符合模板的嵌套结构
        if name not in self._data and self._template:
            # 自动创建空字典并应用模板
            self._data[name] = WritableSafeDotDict({}, template=self._template)
        return super().__getattr__(name)