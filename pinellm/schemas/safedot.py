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
