import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# 配置项比较多，有些不是必须，可参考官方文档 https://packaging.python.org/guides/distributing-packages-using-setuptools/
setuptools.setup(
    name="deptest1-zs",  # 项目的名字，将来通过pip install ******安装，不能与其他项目重复，否则上传失败
    version="0.0.1",  # 项目版本号，自己决定吧
    author="zs",  # 作者
    author_email="123456@yeah.net",  # email
    description="python项目的**********工具",  # 项目描述
    long_description=long_description,  # 加载read_me的内容
    long_description_content_type="text/markdown",  # 描述文本类型
    url="",  # 项目的地址，比如github或者gitlib地址
    packages=setuptools.find_packages(),  # 这个函数可以帮你找到包下的所有文件，你可以手动指定
    package_data={'': ['*.yaml', '*.csv', '*.txt', '.toml']},  # 这个很重要,要与 MANIFEST.in也要有
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pyyaml'
    ],
    requires=[

    ]
)