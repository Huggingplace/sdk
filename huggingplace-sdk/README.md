# HuggingPlace SDK

A comprehensive SDK for logging and tracing LLM interactions with HuggingPlace, similar to PromptLayer but specifically designed for the HuggingPlace ecosystem.

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
npm install huggingplace-sdk
```

## Production Ready

This SDK is **production-ready** and has been tested with:
- ✅ Real backend integration
- ✅ Comprehensive error handling
- ✅ Session management
- ✅ Performance tracking
- ✅ Rich metadata support

## Quick Start

```javascript
const { HuggingPlace } = require('huggingplace-sdk');

// Initialize the SDK
const huggingplace = new HuggingPlace({
  apiKey: 'your-api-key',
  orgId: 'your-org-id',
  mode: 'prod' // or 'dev'
});

// Log a simple interaction
await huggingplace.log({
  userPrompt: "What's the weather like?",
  response: "The weather is sunny today.",
  metadata: {
    sessionId: 'session-123',
    userId: 'user-456'
  }
});
```

## API Reference

### Configuration

```javascript
const huggingplace = new HuggingPlace({
  apiKey: 'your-api-key-here',           // Required: Your HuggingPlace API key
  orgId: 'your-org-id-here',           // Required: Your organization ID
  mode: 'prod',   // Optional: Environment mode (default: 'prod')
  baseUrl: 'https://anvsj57nul.execute-api.ap-south-1.amazonaws.com',        // Optional: Custom base URL (default: production)
  timeout: 10000         // Optional: Request timeout in ms (default: 10000)
});
```

### Core Methods

#### `log(options)`

Log a complete interaction with HuggingPlace.

```javascript
await huggingplace.log({
  // Required fields
  userPrompt: "What's the weather like?",
  response: "The weather is sunny today.",
  
  // Optional fields
  userId: "user-123",
  sessionId: "session-456",
  fileName: "weather_data.csv",
  llmModel: "gpt-4o",
  llmModel2: "gpt-4o",
  tokenCount: 150,
  responseTime: 2.5,
  messageId: "msg-789",
  
  // Metadata
  metadata: {
    sessionId: "session-456",
    likes: 1,
    dislikes: 0,
    messageId: "msg-789",
    recommendationId: "rec-123"
  },
  
  // User metadata
  userMetadata: {
    email: "user@example.com",
    username: "john_doe",
    orgName: "Example Corp"
  },
  
  // Step-by-step data
  stepData: [
    {
      id: 1,
      type: "data_processing",
      userQuestion: "Process weather data",
      promptResponse: "Data processed successfully",
      token: 120,
      responseTime: 1.8,
      inputTokens: 40,
      outputTokens: 80,
      llmModel: "gpt-4o"
    }
  ],
  
  // User context
  userRoles: "admin",
  orgUuid: "org-202",
  mappingTable: "mappings_org_202"
});
```

**Note**: The SDK expects data in the exact format shown above. No automatic transformation is performed.

#### `logStep(stepData)`

Log individual processing steps.

```javascript
await huggingplace.logStep({
  type: 'sql_generation',
  userQuestion: 'Generate SQL for sales data',
  promptResponse: 'SELECT * FROM sales WHERE...',
  token: 150,
  responseTime: 1.5,
  inputTokens: 50,
  outputTokens: 100,
  llmModel: 'gpt-4o'
});
```

#### `startSession(sessionId?)`

Start a new session for tracking multiple interactions.

```javascript
const session = huggingplace.startSession('my-session-id');
await session.log({ userPrompt: 'Hello', response: 'Hi there!' });
```

### Advanced Usage

#### Manual Logging

```javascript
const { HuggingPlace } = require('huggingplace-sdk');

const huggingplace = new HuggingPlace({
  apiKey: process.env.HUGGINGPLACE_API_KEY,
  orgId: process.env.HUGGINGPLACE_ORG_ID
});

// Log a complete interaction
await huggingplace.log({
  userPrompt: "How many sales were there last month?",
  response: "There were 1,245 sales last month.",
  userId: "user-123",
  sessionId: "session-456",
  fileName: "sales_data.csv",
  llmModel: "gpt-4o",
  tokenCount: 350,
  responseTime: 2.3,
  metadata: {
    sessionId: "session-456",
    likes: 0,
    dislikes: 0,
    recommendationId: "rec-789"
  },
  userMetadata: {
    email: "user@example.com",
    username: "john_doe",
    orgName: "Example Corp"
  },
  stepData: [
    {
      id: 1,
      type: "sql_generation",
      userQuestion: "Generate SQL to find last month's sales",
      promptResponse: "SELECT COUNT(*) FROM sales WHERE...",
      token: 150,
      responseTime: 1.5,
      inputTokens: 50,
      outputTokens: 100,
      llmModel: "gpt-4o"
    }
  ],
  userRoles: "admin",
  orgUuid: "org-202",
  mappingTable: "mappings_org_202"
});
```

#### Session-based Logging

```javascript
const session = huggingplace.startSession('conversation-123');

// Log multiple interactions in the same session
await session.log({
  userPrompt: "What's the weather like?",
  response: "The weather is sunny today.",
  metadata: { step: 1 }
});

await session.log({
  userPrompt: "What about tomorrow?",
  response: "Tomorrow will be cloudy with a chance of rain.",
  metadata: { step: 2 }
});
```

#### Error Handling

```javascript
try {
  await huggingplace.log({
    userPrompt: "Test prompt",
    response: "Test response"
  });
} catch (error) {
  if (error.code === 'AUTH_ERROR') {
    console.error('Authentication failed. Check your API key.');
  } else if (error.code === 'VALIDATION_ERROR') {
    console.error('Invalid data provided:', error.details);
  } else {
    console.error('Unexpected error:', error.message);
  }
}
```

## Environment Variables

Set these environment variables for automatic configuration:

```bash
HUGGINGPLACE_API_KEY=your-api-key
HUGGINGPLACE_ORG_ID=your-org-id
HUGGINGPLACE_MODE=prod  # or dev
```

## Error Codes

- `AUTH_ERROR`: Invalid or missing API key
- `VALIDATION_ERROR`: Invalid payload structure
- `NETWORK_ERROR`: Network connectivity issues
- `RATE_LIMIT_ERROR`: Too many requests
- `SERVER_ERROR`: HuggingPlace server error

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details. 