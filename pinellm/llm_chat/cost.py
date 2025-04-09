from decimal import Decimal, getcontext
from ..schemas import SafeDotDict
from ..config import ConfigManager

def cost(request_response: SafeDotDict) -> dict:
    """自动计算成本
    
    参数：
    - request_response: 请求响应对象
    
    返回：
    - cost: 成本字典，包含输入成本、提示成本和总成本（以浮点数形式返回，避免科学计数法显示）
    """
    try:
        model = request_response.model
        prompt_tokens = request_response.usage.prompt_tokens
        completion_tokens = request_response.usage.completion_tokens
        total_tokens = request_response.usage.total_tokens
        model_info = ConfigManager().Model_Map[model]

        # 设置 Decimal 的精度（根据需求调整，例如 28 位有效数字）
        getcontext().prec = 28

        # 将数值转换为 Decimal 类型进行高精度计算
        input_price = (
            Decimal(str(completion_tokens))
            * Decimal(str(model_info.price_in))
            / Decimal("1000")
        )
        prompt_price = (
            Decimal(str(prompt_tokens))
            * Decimal(str(model_info.price_out))
            / Decimal("1000")
        )
        total_price = input_price + prompt_price
        #print(f"输入成本: {input_price}, 提示成本: {prompt_price}, 总成本: {total_price}")
        # 将 Decimal 转换为 float 返回（保留精度）
        return {
            "input_price": float(input_price),
            "prompt_price": float(prompt_price),
            "total_price": float(total_price),
        }
    except Exception as e:
        print(f"计算成本时出错: {e}")
        return {
            "input_price": 0,
            "prompt_price": 0,
            "total_price": 0,
        }