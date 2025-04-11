import logging
from logging import StreamHandler, FileHandler
from datetime import datetime

class StructuredLogger:
    def __init__(self, name='StructuredLogger', log_file='app.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # 创建控制台处理器
        console_handler = StreamHandler()
        # 创建文件处理器
        file_handler = FileHandler(log_file, mode='a', encoding='utf-8')
        
        # 统一格式设置
        console_formatter = logging.Formatter(
            '%(asctime)s - [%(role)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        file_handler.setFormatter(console_formatter)
        
        # 添加两个处理器
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
    def log(self, role, message):
        self.logger.info(message, extra={'role': role})

# 使用示例：
logger = StructuredLogger(log_file='my_app.log')

logger.log('System', '初始化完成')
logger.log('User', '用户登录成功')
logger.log('Error', '发生未知错误')