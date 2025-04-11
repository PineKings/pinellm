import os

Built_Suppliers = {
    "qwen":
        {
        "name": "qwen",
        "description": "阿里云",
        "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        "api_key":os.getenv("QWEN_API_KEY"), 
        "models":['qwen-vl-max-2025-04-02', 'deepseek-v3', 'deepseek-r1-distill-llama-70b', 'deepseek-r1-distill-qwen-32b', 'deepseek-r1-distill-qwen-14b', 'deepseek-r1-distill-llama-8b', 'deepseek-r1-distill-qwen-1.5b', 'deepseek-r1-distill-qwen-7b', 'deepseek-r1', 'qwen1.5-7b-chat', 'qwen-vl-ocr-latest', 'qwen-vl-ocr', 'qwen-coder-plus-1106', 'qwen-coder-plus', 'qwen-coder-plus-latest', 'qwen2.5-coder-3b-instruct', 'qwen2.5-coder-0.5b-instruct', 'qwen2.5-coder-14b-instruct', 'qwen2.5-coder-32b-instruct', 'qwen-coder-turbo-0919', 'qwen2.5-0.5b-instruct', 'qwen2.5-1.5b-instruct', 'qwen2.5-3b-instruct', 'qwen2.5-7b-instruct', 'qwen2.5-14b-instruct', 'qwen2.5-32b-instruct', 'qwen2.5-72b-instruct', 'qwen2.5-coder-7b-instruct', 'qwen2.5-math-1.5b-instruct', 'qwen2.5-math-7b-instruct', 'qwen2.5-math-72b-instruct', 'qwen-turbo-0919', 'qwen-turbo-latest', 'qwen-plus-0919', 'qwen-plus-latest', 'qwen-max-0919', 'qwen-max-latest', 'qwen-coder-turbo', 'qwen-coder-turbo-latest', 'qwen-math-turbo-0919', 'qwen-math-turbo', 'qwen-math-turbo-latest', 'qwen-math-plus-0919', 'qwen-math-plus', 'qwen-math-plus-latest', 'qwen2-57b-a14b-instruct', 'qwen2-72b-instruct', 'qwen2-7b-instruct', 'qwen2-0.5b-instruct', 'qwen2-1.5b-instruct', 'qwen-long', 'qwen-vl-max', 'qwen-vl-plus', 'qwen-max-0428', 'qwen1.5-110b-chat', 'qwen-72b-chat', 'codeqwen1.5-7b-chat', 'qwen1.5-0.5b-chat', 'qwen-1.8b-chat', 'qwen-1.8b-longcontext-chat', 'qwen-7b-chat', 'qwen-14b-chat', 'qwen1.5-14b-chat', 'qwen1.5-1.8b-chat', 'qwen1.5-32b-chat', 'qwen1.5-72b-chat', 'qwen-max-1201', 'qwen-max-longcontext', 'qwen-max-0403', 'qwen-max-0107', 'qwen-turbo', 'qwen-max', 'qwen-plus']
        },
    "deepseek":
        {
        "name": "deepseek",
        "description": "deepseek",
        "url": "https://api.deepseek.com/chat/completions",
        "api_key": os.getenv("DEEPSEEK_API_KEY"),
        "models":['deepseek-chat', 'deepseek-reasoner']
        },
    "zhipu":
        {
        "name": "zhipu",
        "description": "智谱 AI",
        "url": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        "api_key": os.getenv("ZHIPU_API_KEY"),
        "models":["glm-4-plus"]
        }
}