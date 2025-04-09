class ModelError(Exception):
    "模型错误"

class SupplierError(Exception):
    "供应商错误"

class ApiKeyError(Exception):
    "供应商的API Key错误"

class ApiUrlError(Exception):
    "供应商的API URL错误"

class ApiParamError(Exception):
    "供应商的API参数错误"

class ParamError(Exception):
    "参数错误"