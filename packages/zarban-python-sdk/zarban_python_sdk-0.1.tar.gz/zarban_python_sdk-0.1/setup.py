from setuptools import setup, find_packages
import os

setup(
    name="zarban-python-sdk",
    version="0.1",
    packages=find_packages(where="src") + ['cmd'],
    package_dir={"": "src", "cmd": "cmd"},
    install_requires=[
        "openapi-generator-cli"
    ],
    entry_points={
        "console_scripts": [
            "zarban-sdk=main:main",
            "code-gen=cmd.code_gen:generate_code" 
        ],
    },
    author="Zarban",
    author_email="info@zarban.io",
    description="Python SDK for Zarban",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zarbanio/zarban-py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
