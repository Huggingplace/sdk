# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation Methods

### Method 1: Install from PyPI (Recommended)

```bash
pip install huggingplace-sdk
```

### Method 2: Install from Source

1. Clone the repository:
```bash
git clone https://github.com/huggingplace/huggingplace-sdk-python.git
cd huggingplace-sdk-python
```

2. Install in development mode:
```bash
pip install -e .
```

### Method 3: Install with Development Dependencies

```bash
pip install huggingplace-sdk[dev]
```

## Verification

After installation, you can verify it's working:

```python
from huggingplace_sdk import HuggingPlace
print("✅ HuggingPlace SDK installed successfully!")
```

## Environment Setup

Set up your environment variables:

```bash
export HUGGINGPLACE_API_KEY="your-api-key-here"
export HUGGINGPLACE_ORG_ID="your-org-id-here"
export HUGGINGPLACE_MODE="prod"  # or "dev"
```

## Quick Test

Run the basic usage example:

```bash
python examples/basic_usage.py
```

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure you're using Python 3.8+
2. **Network Issues**: Check your internet connection and firewall settings
3. **Authentication Errors**: Verify your API key and organization ID

### Getting Help

- Check the [README.md](README.md) for detailed documentation
- Run tests: `pytest tests/`
- Report issues on GitHub 