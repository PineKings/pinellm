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
### 基础聊天请求  
```python
from pinellm import ChatRequest, Message, ResponseFormat, Tool, Propertie,chat

# 创建消息
messages = [
    Message("system", "You are a helpful assistant."),
    Message("user", "现在几点了？")
]

# 定义工具（获取当前时间）
tools = [
    Tool(
        "get_current_time",
        "获取当前时间",
        properties=None
    )
]

# 发送请求
response = ChatRequest(
    model="qwen-plus",
    messages=messages,
    tools=tools,
    tool_choice="auto"
).send()

# 处理响应
print(f"回答：{response.choices.message.content.text}")
print(f"费用：{response.price.total_price} 元")
```

### 工具调用示例  
```python
# 包含工具调用的请求
messages_with_tool = [
    Message("user", "请告诉我当前时间和天气"),
    Message(
        "assistant",
        tool_calls=[{
            "id": "tool1",
            "function": {
                "name": "get_current_time",
                "arguments": {}
            }
        }]
    )
]

# 自动处理工具调用
response = ChatRequest(
    model="qwen-plus",
    messages=messages_with_tool
).send()

# 输出工具返回结果
print(response.messages[1].content.text)  # 输出当前时间
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