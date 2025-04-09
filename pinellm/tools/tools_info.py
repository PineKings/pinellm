from ..schemas.chat_request import Tool

def get_tools_info(option:int):
    """内置的一些基础工具
    
    选项：
    - 1. 获取当前时间
    
    """
    if option == 1:
        return Tool(name="get_current_time", description="获取当前时间", properties=None)
    else:
        return None