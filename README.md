# PineLLM  
**一个轻量级的多供应商LLM交互框架**  
[![GitHub](https://img.shields.io/badge/GitHub-PineKings/pingllm-blue)](https://github.com/PineKings/pingllm)  
[![Email](https://img.shields.io/badge/Email-work.wss%40icloud.com-red)](mailto:work.wss@icloud.com)

---

## 项目概述  
PineLLM 是一个用于与多个大语言模型（LLM）供应商进行交互的Python框架，支持灵活的模型配置、成本计算、工具调用等功能。当前支持阿里云Qwen系列模型，未来计划扩展更多供应商。

---

## 依赖项  
```python
requests       # HTTP请求处理
typing         # 类型提示
os             # 环境变量处理
datetime       # 时间处理
base64         # 图像编码
decimal        # 高精度计算
```

---

## 核心功能  
### 1. 多供应商支持  
- 内置对阿里云Qwen系列模型的支持（如`qwen-plus`、`qwen-max`等）
- 可通过配置扩展其他供应商

### 2. 模型配置管理  
- 模型参数自动填充（如温度、上下文长度等）
- 供应商API密钥动态加载
- 模型元数据管理（价格、性能指标等）

### 3. 成本计算  
- 根据模型配置计算输入/输出/总费用
- 支持实时费用统计

### 4. 工具调用  
- 内置基础工具（如获取当前时间）
- 支持自定义工具扩展

### 5. 结构化响应  
- 自动处理JSON/YAML格式响应
- 提供安全的嵌套数据访问（通过`SafeDotDict`）

---

## 目录结构说明  
```plaintext
pinellm/  
├── __init__.py          # 入口文件
├── config/              # 配置模块
│   ├── config_manager.py # 配置管理器
│   ├── supplier.py      # 供应商信息处理
│   └── built/           # 内置配置
│       ├── models.py    # 模型元数据
│       ├── suppliers.py # 供应商列表
│       └── tools.py     # 工具定义
├── llm_chat/            # 聊天核心模块
│   ├── request.py       # 请求处理
│   ├── cost.py          # 成本计算
│   └── tools_utilize.py # 工具调用处理
├── schemas/             # 数据结构定义
│   ├── chat_request.py  # 聊天请求模型
│   └── safedot.py       # 安全字典实现
├── tools/               # 工具模块
│   ├── basic/           # 基础工具
│   │   ├── base_image.py # 图像处理
│   │   └── get_basic_info.py # 基础信息工具
│   └── tools_info.py    # 工具元数据
└── prompts/             # 提示词模板
```

---

## 使用示例  
### 增加模型和供应商配置
```python
from pinellm.config import ConfigManager

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

```

### 基础聊天请求  
```python
from pinellm import ChatRequest, Message

# 创建消息
messages = [
    Message("system", "You are a helpful assistant."),
    Message("user", "介绍一下你自己")
]

# 发送请求
response = ChatRequest(
    model="qwen-plus",
    messages=messages
).send()

# 处理响应
print(f"回答：{response.choices.message.content}") # 回答：你好！我是通义千问，阿里巴巴集团旗下的超大规模语言模型。我能够回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。我熟练掌握多种语言，包括但不限于中文、英文、德语、法语、西班牙语等。如果你有任何问题或需要帮助，随时可以问我！
print(f"费用：{response.price.total_price} 元") # 费用：0.0001848 元
```

### 工具调用示例  
```python
# 工具调用示例

# 引入相关模块
from pinellm.schemas import ChatRequest,Message,Tool
from pinellm.tools import toolsutilize
from pinellm.config import ConfigManager

# 配置文件
config = ConfigManager()
# 增加自定义工具
def get_neme():
    return "PineKing"

mytools = {
    "get_neme": get_neme
}
config.load_config(tools=mytools)

# 调用工具
## 构建消息列表
messages = [Message(role="system", content="你是一位用户对话助理，请根据用户需求提供帮助"),
            Message(role="user", content="请告诉我你的名字")]

## 构建请求体并直接发送请求
response = ChatRequest(
    model="qwen-plus",
    messages=messages,
    tools=[Tool(name="get_neme",description="获取助理名字",properties=None)]
).send()

# 判断是否调用工具
if response.choices.message.tool_calls:
    ## 调用工具
    tool_messages = toolsutilize(response)
    ## 如果结果不需要返回大模型处理，则直接返回工具返回的消息
    print(tool_messages[-1].content) # 返回：PineKing
    
    ## 如果结果需要返回大模型处理，则将工具返回的消息添加到消息列表中，再次发送请求
    messages += tool_messages
    response = ChatRequest(
        model="qwen-plus",
        messages=messages,
        tools=[Tool(name="get_neme", description="获取助理名字", properties=None)]
    ).send()
    ## 大模型返回结果
    print(response.choices.message.content) # 返回：我的名字是PineKing。很高兴为您服务！
```

---

## 配置管理  
### 供应商配置  
```python
# 自定义供应商配置示例
from pinellm.config import ConfigManager

config = ConfigManager()
config.load_config(
    suppliers=[{
        "name": "custom_supplier",
        "url": "https://api.example.com/v1/chat",
        "api_key": "YOUR_API_KEY",
        "models": ["custom_model"]
    }]
)
```

### 模型覆盖配置  
```python
# 覆盖默认模型配置
config.load_config(
    models={
        "qwen-plus": {
            "temperature": 0.8,
            "max_tokens": 2048
        }
    }
)
```

---

## 开发计划  
### 短期目标（1-3个月）  
| 功能模块       | 进度 | 说明 |
|----------------|------|------|
| 支持更多供应商 | 20%  | 计划集成Anthropic、OpenAI等 |
| 图像处理增强   | 10%  | 支持图片输入/输出 |
| 文档自动化     | 5%   | 使用mkdocs生成文档 |
| 性能优化       | 30%  | 异步请求支持 |

### 中期目标（3-6个月）  
| 功能模块       | 说明 |
|----------------|------|
| 工具市场       | 用户可上传/下载工具插件 |
| 模型比较工具   | 自动对比不同模型输出 |
| 成本监控系统   | 实时API调用费用统计 |

### 长期目标  
| 功能模块       | 说明 |
|----------------|------|
| 多语言支持     | 完善非中文环境支持 |
| 企业级部署     | Kubernetes部署方案 |
| 安全审计       | API密钥加密存储 |

---

## 测试用例  
### 基础测试  
```python
def test_chat_request():
    req = ChatRequest(
        model="qwen-plus",
        messages=[Message("user", "你好")],
    )
    assert req.model == "qwen-plus"
    assert req.messages[0].role == "user"
```

### 异常测试  
```python
def test_invalid_model():
    with pytest.raises(ValueError):
        ChatRequest(model="nonexistent_model", messages=[])
```

### 性能测试  
```python
def test_cost_calculation():
    mock_response = SafeDotDict({
        "model": "qwen-plus",
        "usage": {
            "prompt_tokens": 100,
            "completion_tokens": 50
        }
    })
    cost = pinellm.cost(mock_response)
    assert cost["total_price"] == 0.00024  # 100*0.0008 + 50*0.002
```

---

## 模块详解  
### 1. 配置模块 (`pinellm.config`)  
- **ConfigManager**  
  - 单例模式管理配置
  - 自动合并内置配置和用户自定义配置
  - 提供模型/供应商/工具的快速查找接口

- **Supplier**  
  - 根据模型名称自动匹配供应商
  - 动态获取API密钥和URL
  - 提供安全的API参数获取接口

### 2. 聊天模块 (`pinellm.llm_chat`)  
- **chat()**  
  - 处理完整的请求-响应流程
  - 自动计算费用并附加到响应
  - 支持工具调用的链式处理

- **cost()**  
  - 使用Decimal进行高精度费用计算
  - 根据模型价格参数动态计算

### 3. 工具模块 (`pinellm.tools`)  
- **内置工具**  
  - `get_current_time()`：获取当前时间（含星期）
  - `get_weather()`：基础天气查询（待扩展）

- **工具扩展规范**  
  ```python
  def new_tool(latitude: float, longitude: float):
      # 自定义工具实现
      return f"Location {latitude},{longitude} info"
  ```

---

## 贡献指南  
1. Fork仓库  
2. 创建新分支 `git checkout -b feature/tool-extension`  
3. 提交PR至 `main` 分支  
4. 遵循PEP8编码规范  

---

## 联系我们  
- 项目地址：https://github.com/PineKings/pingllm  
- 开发者邮件：work.wss@icloud.com  
- 技术交流群：QQ群 1234567（群名称：PineLLM开发者社区）

---

> 特别说明：本框架使用Apache-2.0协议开源，商用需遵守协议条款。