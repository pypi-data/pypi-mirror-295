from setuptools import find_packages, setup

setup(
    name="aicli-agent",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "pydantic-settings",
        "generalagent",
        # 添加其他依赖项
    ],
    entry_points={
        "console_scripts": [
            "aicli=aicli:cli",
        ],
    },
)
