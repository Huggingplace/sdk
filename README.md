# Huggingplace SDK

This repository contains the official SDKs for Huggingplace.

## SDKs

- **JavaScript/Node.js SDK**: `huggingplace-sdk/` - Official JavaScript SDK for Huggingplace
- **Python SDK**: `huggingplace-python-sdk/` - Official Python SDK for Huggingplace

## Quick Start

### JavaScript/Node.js SDK

```bash
cd huggingplace-sdk
npm install
```

### Python SDK

```bash
cd huggingplace-python-sdk
pip install -e .
```

## API Compatibility

Both SDKs support the following key features:

- **Flexible Field Mapping**: Automatically maps `response` to `ai_response` and `user_metadata` to `user_meta_data` for API compatibility
- **Response Time Handling**: Accepts response time in any format and sends it as-is to the backend
- **Minimal Validation**: Accepts data even when fields are empty, with only basic type validation
- **Session Management**: Built-in session support for tracking multiple interactions
- **Error Handling**: Comprehensive error handling with detailed error messages

## Documentation

Each SDK has its own documentation and examples in their respective directories.

## Contributing

Please refer to the individual SDK directories for contribution guidelines. 