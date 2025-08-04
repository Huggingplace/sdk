# HuggingPlace SDK (Python)

A comprehensive Python SDK for logging and tracing LLM interactions with HuggingPlace, similar to PromptLayer but specifically designed for the HuggingPlace ecosystem.

## Features

- 🔐 **API Key Authentication**: Secure authentication using API keys
- 📊 **Comprehensive Logging**: Log prompts, responses, metadata, and step-by-step traces
- 🚀 **Multi-LLM Support**: Works with any LLM provider (OpenAI, Claude, Mistral, etc.)
- ⚡ **Async Support**: Non-blocking logging operations
- 🏷️ **Rich Metadata**: Support for custom tags, user context, and organization data
- 📈 **Performance Tracking**: Automatic latency and token counting
- 🔄 **Session Management**: Track conversations across multiple interactions

## Installation

```bash
pip install huggingplace-sdk
```

## Production Ready

This SDK is **production-ready** and has been tested with:
- ✅ Real backend integration
- ✅ Comprehensive error handling
- ✅ Session management
- ✅ Performance tracking
- ✅ Rich metadata support

## Quick Start

```python
from huggingplace_sdk import HuggingPlace

# Initialize the SDK
huggingplace = HuggingPlace(
    api_key="your-api-key",
    org_id="your-org-id",
    mode="prod"  # or "dev"
)

# Log a simple interaction
await huggingplace.log({
    "user_prompt": "What's the weather like?",
    "response": "The weather is sunny today.",
    "metadata": {
        "session_id": "session-123",
        "user_id": "user-456"
    }
})
```

## API Reference

### Configuration

```python
from huggingplace_sdk import HuggingPlace

huggingplace = HuggingPlace(
    api_key="your-api-key-here",           # Required: Your HuggingPlace API key
    org_id="your-org-id-here",           # Required: Your organization ID
    mode="prod",   # Optional: Environment mode (default: "prod")
    base_url="https://anvsj57nul.execute-api.ap-south-1.amazonaws.com",        # Optional: Custom base URL (default: production)
    timeout=10000         # Optional: Request timeout in ms (default: 10000)
)
```

### Core Methods

#### `log(options)`

Log a complete interaction with HuggingPlace.

```python
await huggingplace.log({
    # Required fields
    "user_prompt": "What's the weather like?",
    "response": "The weather is sunny today.",
    
    # Optional fields
    "user_id": "user-123",
    "session_id": "session-456",
    "file_name": "weather_data.csv",
    "llm_model": "gpt-4o",
    "llm_model2": "gpt-4o",
    "token_count": 150,
    "response_time": 2.5,
    "message_id": "msg-789",
    
    # Metadata
    "metadata": {
        "session_id": "session-456",
        "likes": 1,
        "dislikes": 0,
        "message_id": "msg-789",
        "recommendation_id": "rec-123"
    },
    
    # User metadata
    "user_metadata": {
        "email": "user@example.com",
        "username": "john_doe",
        "org_name": "Example Corp"
    },
    
    # Step-by-step data
    "step_data": [
        {
            "id": 1,
            "type": "data_processing",
            "user_question": "Process weather data",
            "prompt_response": "Data processed successfully",
            "token": 120,
            "response_time": 1.8,
            "input_tokens": 40,
            "output_tokens": 80,
            "llm_model": "gpt-4o"
        }
    ],
    
    # User context
    "user_roles": "admin",
    "org_uuid": "org-202",
    "mapping_table": "mappings_org_202"
})
```

**Note**: The SDK expects data in the exact format shown above. No automatic transformation is performed.

#### `log_step(step_data)`

Log individual processing steps.

```python
await huggingplace.log_step({
    "type": "sql_generation",
    "user_question": "Generate SQL for sales data",
    "prompt_response": "SELECT * FROM sales WHERE...",
    "token": 150,
    "response_time": 1.5,
    "input_tokens": 50,
    "output_tokens": 100,
    "llm_model": "gpt-4o"
})
```

#### `start_session(session_id=None)`

Start a new session for tracking multiple interactions.

```python
session = huggingplace.start_session("my-session-id")
await session.log({"user_prompt": "Hello", "response": "Hi there!"})
```

### Advanced Usage

#### Manual Logging

```python
from huggingplace_sdk import HuggingPlace
import os

huggingplace = HuggingPlace(
    api_key=os.getenv("HUGGINGPLACE_API_KEY"),
    org_id=os.getenv("HUGGINGPLACE_ORG_ID")
)

# Log a complete interaction
await huggingplace.log({
    "user_prompt": "How many sales were there last month?",
    "response": "There were 1,245 sales last month.",
    "user_id": "user-123",
    "session_id": "session-456",
    "file_name": "sales_data.csv",
    "llm_model": "gpt-4o",
    "token_count": 350,
    "response_time": 2.3,
    "metadata": {
        "session_id": "session-456",
        "likes": 0,
        "dislikes": 0,
        "recommendation_id": "rec-789"
    },
    "user_metadata": {
        "email": "user@example.com",
        "username": "john_doe",
        "org_name": "Example Corp"
    },
    "step_data": [
        {
            "id": 1,
            "type": "sql_generation",
            "user_question": "Generate SQL to find last month's sales",
            "prompt_response": "SELECT COUNT(*) FROM sales WHERE...",
            "token": 150,
            "response_time": 1.5,
            "input_tokens": 50,
            "output_tokens": 100,
            "llm_model": "gpt-4o"
        }
    ],
    "user_roles": "admin",
    "org_uuid": "org-202",
    "mapping_table": "mappings_org_202"
})
```

#### Session-based Logging

```python
session = huggingplace.start_session("conversation-123")

# Log multiple interactions in the same session
await session.log({
    "user_prompt": "What's the weather like?",
    "response": "The weather is sunny today.",
    "metadata": {"step": 1}
})

await session.log({
    "user_prompt": "What about tomorrow?",
    "response": "Tomorrow will be cloudy with a chance of rain.",
    "metadata": {"step": 2}
})
```

#### Error Handling

```python
try:
    await huggingplace.log({
        "user_prompt": "Test prompt",
        "response": "Test response"
    })
except AuthenticationError:
    print("Authentication failed. Check your API key.")
except ValidationError as e:
    print(f"Invalid data provided: {e}")
except NetworkError:
    print("Network connectivity issues.")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Environment Variables

Set these environment variables for automatic configuration:

```bash
HUGGINGPLACE_API_KEY=your-api-key
HUGGINGPLACE_ORG_ID=your-org-id
HUGGINGPLACE_MODE=prod  # or dev
```

## Error Codes

- `AuthenticationError`: Invalid or missing API key
- `ValidationError`: Invalid payload structure
- `NetworkError`: Network connectivity issues
- `RateLimitError`: Too many requests
- `ServerError`: HuggingPlace server error

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details. 