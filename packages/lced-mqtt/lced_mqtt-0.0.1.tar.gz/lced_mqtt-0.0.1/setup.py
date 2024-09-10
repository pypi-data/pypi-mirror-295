from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description_content = f.read()
setup(
    name="lced_mqtt",
    version="0.0.1",
    description="lced_mqtt",
    long_description=long_description_content,
    long_description_content_type="text/markdown",
    author="linwanlong",
    author_email="linwanlong88@gmail.com",
    url="",
    packages=find_packages(),  # 自动找到所有子包
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
