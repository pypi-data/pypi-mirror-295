from setuptools import setup, find_packages

setup(
    name='XHS-DOWNLOADER',  # 替换为你的包名
    version='0.1.0',  # 包的版本
    packages=find_packages(),  # 自动查找包
    install_requires=[
        'textual<=0.63.0',  
        'pyperclip>=1.9.0',
        'lxml>=5.3.0',
        'PyYAML>=6.0.2',
        'aiosqlite>=0.20.0',
        'click>=8.1.7',
        'rookiepy>=0.5.2',
        'httpx>=0.27.0',
        'fastapi>=0.112.1',
        'uvicorn>=0.30.6',
        'aiofiles>=24.1.0',
        'emoji>=2.12.1'
        # 列出依赖包，例如 'requests', 'numpy'
    ],
    author='cby',  # 作者姓名
    author_email='your.email@example.com',  # 作者邮箱
    description='A brief description of your package',  # 包的描述
    long_description=open('README.md').read(),  # 从 README 文件读取详细描述
    long_description_content_type='text/markdown',  # 描述内容类型
    url='https://github.com/yourusername/your_package',  # 项目主页
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # 根据你的许可证选择
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',  # Python 版本要求
)