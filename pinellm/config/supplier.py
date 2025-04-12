from ..config.config_manager import ConfigManager

class Supplier:
    """检查模型是否支持并返回供应商信息
    
    参数：
    - model: 模型名称
    
    返回：
    - Supplier: 包含供应商名称、模型名称、api_key、api_url的Supplier对象
    
    使用：
    - 属性：
        - model: 模型名称
        - supplier: 供应商名称
        - api_key: api key
        - api_url: api url

    - 方法：
        - as_dict: 返回包含供应商名称、模型名称、api_key、api_url的字典
    
    """
    def __init__(self, model: str):
        config_manager = ConfigManager()
        supplier_info = config_manager.get_supplier(model)
        if not supplier_info:
            from ..errors import SupplierError
            raise SupplierError(f"未找到支持「{model}」模型的供应商，请检查模型名称是否正确或检查供应商配置")
        self.supplier = supplier_info.get("name")
        self.api_key = supplier_info.get("api_key")
        self.api_url = supplier_info.get("url")
        self.emb_url = supplier_info.get("emb_url",None)
        self.model = model
                    
        
    def as_dict(self):
        return {
            "supplier": self.supplier,
            "model": self.model,
            "api_key": self.api_key,
            "api_url": self.api_url
        }

    def __repr__(self):
        return f"ResponseFormat(supplier={self.supplier}, model={self.model}, api_key=***, api_url={self.api_url})"