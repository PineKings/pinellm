from setuptools import setup, find_packages

setup(
    name='pinellm',  # 包名（需与PyPI唯一）
    version='1.0.2',  # 版本号（后续发布需递增）
    packages=find_packages(),  # 自动发现所有包
    install_requires=[
        'requests',  # 你代码中用到的依赖（如requests）
        'python-dotenv',  # 如果有环境变量处理
        # 其他依赖项...
    ],
    author='PineKing',
    author_email='work.wss@icloud.com',
    description='A Python library for managing LLM chat models',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/PineKings/pinellm',  # 项目主页
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # 你的许可证
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',  # 你的Python版本要求
    include_package_data=True,  # 包含非Python文件（如配置）
)