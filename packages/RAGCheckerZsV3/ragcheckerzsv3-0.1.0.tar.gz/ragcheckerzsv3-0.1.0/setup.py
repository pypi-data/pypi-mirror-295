from setuptools import setup, find_packages

setup(
    name='RAGCheckerZsV3',                      # 包名
    version='0.1.0',                        # 版本号
    packages=find_packages(include=['package_demo','package_demo.*']),  # 包含的包
    install_requires=[                      # 依赖的库
        'requests',                         # 示例依赖
        'pandas',
        'openai',
        'agchecker',
        'spacy',
    ],
    author='john_doe.2024',                     # 作者信息
    author_email='2043389890@qq.com',  # 作者邮箱
    description='A RAG Checker Python package',  # 包的简短描述
    long_description=open('README.md').read(),   # 读取长描述
    long_description_content_type='text/markdown',  # 长描述的格式
    url='https://github.com/amazon-science/RAGChecker',  # 项目主页
    classifiers=[                           # 分类信息
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',                # Python 版本要求
    package_data={                          # 包内需要包含的非代码文件
        '': ['data/*.json', 'imgs/*.png', 'examples/*.txt'],
    },
)
