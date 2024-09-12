from setuptools import setup, find_packages

setup(
    name="ai_tools_zxw",
    version="2.8.10",
    packages=find_packages(),
    install_requires=[
        'xlwt',
        'psutil',
    ],
    author="xue wei zhang",
    author_email="",
    description="更新了nlp预处理，中文文字识别",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sunshineinwater/",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
