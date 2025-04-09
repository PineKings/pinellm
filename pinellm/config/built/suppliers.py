import os

Built_Suppliers = [
    {
    "name": "qwen",
    "description": "阿里云",
    "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    "api_key": os.getenv("QWEN_API_KEY"),  # 请自己替换一个阿里云api_key的替换逻辑
    "models":['multimodal-embedding-v1', 'qvq-max-latest', 'qwen-coder-plus-latest', 'qwen-coder-turbo-latest', 'qwen-long-latest', 'qwen-max', 'qwen-omni-turbo-latest', 'qwen-plus', 'qwen-plus-character', 'qwen-turbo-latest', 'qwen-vl-max-latest', 'qwen-vl-ocr-latest', 'qwen-vl-plus-latest', 'qwq-plus-latest', 'text-embedding-async-v1', 'text-embedding-async-v2', 'text-embedding-v1', 'text-embedding-v2', 'text-embedding-v3', 'tongyi-intent-detect-v3', 'wanx2.0-t2i-turbo', 'wanx2.1-i2v-plus', 'wanx2.1-i2v-turbo', 'wanx2.1-t2i-plus', 'wanx2.1-t2i-turbo', 'wanx2.1-t2v-plus', 'wanx2.1-t2v-turbo', 'wanx-v1']
    }
]