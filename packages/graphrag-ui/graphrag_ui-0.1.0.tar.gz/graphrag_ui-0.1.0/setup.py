import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requires_list = open(f'requirements.txt', 'r', encoding='utf8').readlines()
requires_list = [i.strip() for i in requires_list]

setuptools.setup(
    name="graphrag_ui",
    version="0.1.0",
    author="wade1010",
    url='https://github.com/wade1010/graphrag-ui',
    author_email="640297@qq.com",
    description="The latest graphrag interface is used, using the local ollama to provide the LLM interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    packages=['.'],
    entry_points={
        'console_scripts': [
            'graphrag-ui-server=api:main',
            'graphrag-ui=app:main',
            'graphrag-ui-pure=index_app:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 设置依赖包
    install_requires=requires_list
)