from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="git-autocommit",
    version="0.1.0",
    author="Emilio",
    author_email="andere.emi@gmail.com",
    description="A tool to automatically generate Git commit messages using local LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/technoabsurdist/autocommit",
    packages=find_packages(),
    install_requires=[
        "ollama",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "git-autocommit=autocommit.main:main", 
        ],
    },
)