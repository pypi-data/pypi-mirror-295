from setuptools import setup, find_packages

setup(
    name="seekbaseapi",
    version="0.6.1",
    packages=find_packages(),
    install_requires=[
        "elasticsearch",
        "regex",
        "urllib3",
        "tenacity",
        "pydantic",
        "pydantic[email]",
    ],
    description="A Python package for interacting with SeekBaseApi and extracting specific information.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="E2H",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
