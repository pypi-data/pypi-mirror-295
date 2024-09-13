from setuptools import setup, find_packages

setup(
    name='xhs_auto_down',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        # 列出依赖包
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
        'emoji>=2.12.1',
    ],
    author='bauyin',
    author_email='your_email@example.com',
    description='A brief description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your_package_name',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)
