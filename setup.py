from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    required_packages = fh.read().splitlines()

setup(
    name="english-learning-app",
    version="0.1.0",
    author="NguyenThiYenNhi",
    author_email="yennhinguyen090605@gmail.com",
    description="A PoC project about English learning app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nhiney/english-app",
    packages=find_packages(),
    install_requires=required_packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)