"""
Setup script for HuggingPlace SDK
"""

from setuptools import setup, find_packages

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="huggingplace-sdk",
    version="1.0.1",
    author="HuggingPlace Team",
    author_email="team@huggingplace.com",
    description="Official SDK for HuggingPlace - Log and trace LLM interactions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/huggingplace/huggingplace-sdk-python",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "uuid>=1.30",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "huggingplace=huggingplace_sdk.cli:main",
        ],
    },
    keywords=[
        "huggingplace",
        "llm",
        "logging",
        "tracing",
        "prompt-engineering",
        "ai",
        "machine-learning"
    ],
    project_urls={
        "Homepage": "https://github.com/huggingplace/huggingplace-sdk-python",
        "Documentation": "https://github.com/huggingplace/huggingplace-sdk-python#readme",
        "Repository": "https://github.com/huggingplace/huggingplace-sdk-python",
        "Issues": "https://github.com/huggingplace/huggingplace-sdk-python/issues",
    },
) 