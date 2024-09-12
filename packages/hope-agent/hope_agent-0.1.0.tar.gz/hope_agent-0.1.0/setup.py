from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hope-agent",
    version="0.1.0",
    author="Umutcan Edizaslan",
    author_email="noreply@deuz.ai",
    description="Advanced AI agent orchestration system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/U-C4N/HOPE-Agent",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "langchain",
        "rich",
        "pytest",
        "groq",
        "textblob",
        "fastapi",
        "python-dotenv",
    ],
    extras_require={
        "dev": ["black", "flake8", "mypy"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "hope-agent=interfaces.cli:main",
        ],
    },
)