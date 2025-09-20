# HuggingPlace SDK

A comprehensive SDK for logging and tracing LLM interactions with HuggingPlace, similar to PromptLayer but specifically designed for the HuggingPlace ecosystem.

## Features

- 🔐 **API Key Authentication**: Secure authentication using API keys
- 📊 **Comprehensive Logging**: Log prompts, responses, metadata, and step-by-step traces
- 🔍 **Advanced Tracing**: OpenTelemetry-based tracing for detailed workflow analysis
- 🚀 **Multi-LLM Support**: Works with any LLM provider (OpenAI, Claude, Mistral, etc.)
- ⚡ **Async Support**: Non-blocking logging and tracing operations
- 🏷️ **Rich Metadata**: Support for custom tags, user context, and organization data
- 📈 **Performance Tracking**: Automatic latency and token counting
- 🔄 **Session Management**: Track conversations across multiple interactions
- 🔗 **Multi-Step Workflows**: Trace complex AI workflows with sequential steps
- 📊 **Batch Processing**: Efficient batch sending of trace data

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
- ✅ OpenTelemetry tracing
- ✅ Multi-step workflow support

## Quick Start

### Basic Logging

```javascript
import { HuggingPlace } from 'huggingplace-sdk';

// Initialize the SDK
const huggingplace = new HuggingPlace({
  apiKey: 'your-api-key',
  orgId: 'your-org-id',
  mode: 'prod' // or 'dev'
});

// Log a simple interaction
await huggingplace.log({
  user_prompt: "What's the weather like?",
  ai_response: "The weather is sunny today.",
  user_uuid: 'user-123',
  org_uuid: 'org-456'
});
```

### Basic Tracing

```javascript
import { HuggingPlace } from 'huggingplace-sdk';

// Initialize the SDK with tracing configuration
const huggingplace = new HuggingPlace({
  apiKey: 'your-api-key',
  orgId: 'your-org-id',
  mode: 'prod',
  // Optional tracing configuration
  traceBatchSize: 10,
  traceBatchTimeout: 5000,
  traceMaxRetries: 3
});

// Trace a simple function
const result = await huggingplace.traceStep({
  stepName: 'Data Processing',
  func: async () => {
    // Your function logic here
    return { processed: true, data: 'sample data' };
  },
  userMetadata: { userId: 'user-123' },
  orgData: { orgId: 'org-456' }
});
```

## API Reference

### Configuration

```javascript
const huggingplace = new HuggingPlace({
  // Required
  apiKey: 'your-api-key-here',           // Your HuggingPlace API key
  orgId: 'your-org-id-here',           // Your organization ID
  
  // Optional (same as logging)
  mode: 'prod',   // Environment mode (default: 'prod')
  baseUrl: 'https://anvsj57nul.execute-api.ap-south-1.amazonaws.com',        // Custom base URL (default: production)
  timeout: 10000,         // Request timeout in ms (default: 10000)
  silent: false,          // Silent mode (default: false)
  
  // Optional (tracing-specific)
  traceEndpoint: 'https://your-backend.com/api/traces',        // Custom trace endpoint
  traceBatchEndpoint: 'https://your-backend.com/api/traces/batch',  // Custom batch endpoint
  traceBatchSize: 10,     // Batch size (default: 10)
  traceBatchTimeout: 5000, // Batch timeout in ms (default: 5000)
  traceMaxRetries: 3      // Max retries (default: 3)
});
```

### Core Methods

#### `log(options)`

Log a complete interaction with HuggingPlace.

```javascript
await huggingplace.log({
  // Required fields
  user_prompt: "What's the weather like?",
  ai_response: "The weather is sunny today.",
  // Alternative: you can also use 'response' instead of 'ai_response'
  response: "The weather is sunny today.",
  
  // Optional fields
  user_uuid: "user-123",
  session_id: "session-456",
  file_name: "weather_data.csv",
  llm_model: "gpt-4o",
  llm_model2: "gpt-4o",
  token_count: 150,
  response_time: "0 min 2.50 sec", // Accepts any format, sent as-is
  message_id: "msg-789",
  
  // Metadata
  metaData: {
    sessionId: "session-456",
    likes: 1,
    dislikes: 0,
    messageId: "msg-789",
    recommendationId: "rec-123"
  },
  
  // User metadata
  user_meta_data: {
    userId: "user-123",
    email: "user@example.com",
    preferences: {
      language: "en",
      theme: "dark"
    }
  },
  
  // Organization data
  org_uuid: "org-456",
  org_id: 456,
  
  // Step data for complex workflows
  step_data: [
    {
      step: "Data Collection",
      result: "Collected user query",
      timestamp: "2024-01-01T00:00:00Z"
    },
    {
      step: "LLM Processing",
      result: "Generated response",
      timestamp: "2024-01-01T00:00:01Z"
    }
  ],
  
  // User roles
  user_roles: ["admin", "developer"],
  
  // Mapping table for database operations
  mapping_table: "user_interactions"
});
```

## Tracing API

The SDK provides comprehensive tracing capabilities using OpenTelemetry standards, integrated directly into the HuggingPlace class.

### Default Configuration

The SDK uses sensible defaults for tracing configuration:

```javascript
// Default tracing configuration
{
  batchSize: 10,           // Number of traces to batch
  batchTimeout: 5000,      // Batch timeout in milliseconds
  maxRetries: 3,           // Maximum retry attempts
  retryDelay: 1000,        // Initial retry delay in milliseconds
  timeout: 10000,          // HTTP timeout for single requests
  batchTimeoutMs: 30000,   // HTTP timeout for batch requests
  silent: false            // Enable/disable console logging
}
```

### `traceStep(options)`

Trace any function with detailed metadata.

```javascript
const result = await huggingplace.traceStep({
  // Required parameters
  stepName: 'My Function',
  func: async () => {
    // Your function logic here
    return { success: true, data: 'result' };
  },
  
  // Optional parameters
  traceId: 'custom-trace-id', // Auto-generated if not provided
  parentSpanId: 'parent-span-id', // Auto-generated if not provided
  logs: { additional: 'log data' },
  attributes: { custom: 'attributes' },
  status: 'OK', // or 'ERROR'
  evaluation: 'REVIEW', // or 'APPROVED', 'REJECTED'
  
  // Metadata
  metadata: { general: 'metadata' },
  userMetadata: { userId: 'user-123' },
  orgData: { orgId: 'org-456' },
  llmData: { model: 'gpt-4', provider: 'openai' },
  customMetadata: { appVersion: '1.0.0' },
  
  // Additional fields (any data you want to include)
  tags: ['important', 'processing'],
  priority: 'high',
  environment: 'production'
});
```

### `traceLLM(options)`

Specialized tracer for LLM calls with evaluation capabilities.

```javascript
const result = await huggingplace.traceLLM({
  // Required parameters
  prompt: 'What is the capital of France?',
  llmFunction: async () => {
    // Your LLM API call here
    const response = await openai.createChatCompletion({
      model: 'gpt-4',
      messages: [{ role: 'user', content: 'What is the capital of France?' }]
    });
    
    return {
      responseText: response.data.choices[0].message.content,
      finishReason: response.data.choices[0].finish_reason,
      inputTokens: response.data.usage.prompt_tokens,
      outputTokens: response.data.usage.completion_tokens,
      totalTokens: response.data.usage.total_tokens,
      rawResponse: response.data
    };
  },
  
  // Optional parameters
  traceId: 'custom-trace-id', // Auto-generated if not provided
  parentSpanId: 'parent-span-id', // Auto-generated if not provided
  evaluationStatus: 'REVIEW', // or 'APPROVED', 'REJECTED'
  user: { userId: 'user-123', email: 'user@example.com' },
  org: { orgId: 'org-456', orgName: 'ExampleOrg' },
  llmMetadata: {
    model: 'gpt-4',
    provider: 'openai',
    temperature: 0.7,
    maxTokens: 100
  },
  previousSteps: [
    { step: 'Data Preparation', result: 'Prepared query' }
  ],
  customMetadata: { appVersion: '1.0.0' },
  
  // Additional fields
  tags: ['llm', 'gpt-4', 'geography'],
  sessionId: 'session-789'
});
```

### `traceMultiStepFlow(options)`

Trace complex workflows with multiple sequential steps.

```javascript
const result = await huggingplace.traceMultiStepFlow({
  flowName: 'Customer Support Analysis',
  user: { userId: 'user-123' },
  org: { orgId: 'org-456' },
  traceId: 'custom-trace-id', // Auto-generated if not provided
  
  steps: [
    {
      name: 'Data Collection',
      func: async () => {
        return { customerId: 'cust-789', query: 'Help with subscription' };
      },
      evaluation: 'REVIEW',
      metadata: { stepType: 'data-collection' },
      rest: { source: 'web-form', priority: 'medium' }
    },
    {
      name: 'Sentiment Analysis',
      func: async (previousResults) => {
        const data = previousResults[0];
        return {
          sentiment: 'neutral',
          confidence: 0.75,
          urgency: 'medium'
        };
      },
      evaluation: 'APPROVED',
      metadata: { stepType: 'nlp-analysis' }
    },
    {
      name: 'LLM Response Generation',
      func: async (previousResults) => {
        const data = previousResults[0];
        const sentiment = previousResults[1];
        
        // Your LLM call here
        const response = await openai.createChatCompletion({
          model: 'gpt-4',
          messages: [{ role: 'user', content: data.query }]
        });
        
        return {
          responseText: response.data.choices[0].message.content,
          finishReason: response.data.choices[0].finish_reason,
          inputTokens: response.data.usage.prompt_tokens,
          outputTokens: response.data.usage.completion_tokens,
          totalTokens: response.data.usage.total_tokens,
          rawResponse: response.data
        };
      },
      evaluation: 'REVIEW',
      metadata: { stepType: 'llm-generation' }
    }
  ],
  
  customMetadata: {
    workflowType: 'customer-support',
    version: '1.0.0'
  },
  tags: ['workflow', 'customer-support', 'ai-pipeline']
});
```

### Utility Functions

```javascript
import { 
  generateId, 
  getCurrentTimestamp, 
  calculateDuration 
} from 'huggingplace-sdk';

// Generate unique IDs
const traceId = generateId();
const spanId = generateId();

// Get current timestamp
const timestamp = getCurrentTimestamp();

// Calculate duration
const duration = calculateDuration(startTime, endTime);
```

## Examples

### Basic Tracing

```javascript
import { HuggingPlace } from 'huggingplace-sdk';

// Initialize with tracing configuration
const huggingplace = new HuggingPlace({
  apiKey: 'your-api-key',
  orgId: 'your-org-id',
  mode: 'prod',
  traceBatchSize: 10
});

// Trace a simple data processing function
const result = await huggingplace.traceStep({
  stepName: 'Data Processing',
  func: async () => {
    // Simulate some work
    await new Promise(resolve => setTimeout(resolve, 100));
    return { processed: true, data: 'sample data' };
  },
  userMetadata: { userId: 'user-123' },
  orgData: { orgId: 'org-456' },
  tags: ['data-processing', 'example']
});
```

### LLM Tracing

```javascript
import { HuggingPlace } from 'huggingplace-sdk';

const huggingplace = new HuggingPlace({
  apiKey: 'your-api-key',
  orgId: 'your-org-id'
});

// Trace an OpenAI API call
const result = await huggingplace.traceLLM({
  prompt: 'How are you feeling today?',
  llmFunction: async () => {
    const response = await openai.createChatCompletion({
      model: 'gpt-4',
      messages: [{ role: 'user', content: 'How are you feeling today?' }]
    });
    
    return {
      responseText: response.data.choices[0].message.content,
      finishReason: response.data.choices[0].finish_reason,
      inputTokens: response.data.usage.prompt_tokens,
      outputTokens: response.data.usage.completion_tokens,
      totalTokens: response.data.usage.total_tokens,
      rawResponse: response.data
    };
  },
  user: { userId: 'user-123' },
  org: { orgId: 'org-456' },
  llmMetadata: { model: 'gpt-4', provider: 'openai' }
});
```

### Multi-Step Workflow

```javascript
import { HuggingPlace } from 'huggingplace-sdk';

const huggingplace = new HuggingPlace({
  apiKey: 'your-api-key',
  orgId: 'your-org-id'
});

// Trace a complete AI workflow
const result = await huggingplace.traceMultiStepFlow({
  flowName: 'Document Analysis',
  user: { userId: 'user-123' },
  org: { orgId: 'org-456' },
  steps: [
    {
      name: 'Document Upload',
      func: async () => ({ documentId: 'doc-123', content: 'Sample content' }),
      evaluation: 'APPROVED'
    },
    {
      name: 'Text Extraction',
      func: async (previousResults) => {
        const doc = previousResults[0];
        return { extractedText: doc.content, wordCount: 100 };
      },
      evaluation: 'APPROVED'
    },
    {
      name: 'AI Analysis',
      func: async (previousResults) => {
        const extracted = previousResults[1];
        // Your LLM call here
        return { analysis: 'Positive sentiment', confidence: 0.85 };
      },
      evaluation: 'REVIEW'
    }
  ],
  tags: ['document-analysis', 'workflow']
});
```

## Error Handling

The SDK provides comprehensive error handling for both logging and tracing operations.

```javascript
try {
  const result = await huggingplace.traceStep({
    stepName: 'Risky Operation',
    func: async () => {
      throw new Error('Something went wrong!');
    },
    userMetadata: { userId: 'user-123' }
  });
} catch (error) {
  console.log('Error was caught and traced:', error.message);
  // The error is automatically traced with status 'ERROR'
}
```

## Best Practices

1. **Use meaningful step names**: Choose descriptive names for your traced steps
2. **Include relevant metadata**: Add user, organization, and custom metadata for better analysis
3. **Handle errors gracefully**: Wrap your functions in try-catch blocks
4. **Use tags for filtering**: Add tags to make traces easier to find and analyze
5. **Batch when possible**: The SDK automatically batches trace data for better performance
6. **Set appropriate evaluation status**: Use 'REVIEW', 'APPROVED', or 'REJECTED' based on your needs
7. **Configure tracing endpoints**: Set custom trace endpoints if needed
8. **Use silent mode in production**: Set `silent: true` to reduce console output

## Architecture

The SDK uses OpenTelemetry for tracing and sends data to your HuggingPlace backend via HTTP. The architecture is designed to be:

- **Non-blocking**: All operations are asynchronous
- **Reliable**: Includes retry logic and error handling
- **Scalable**: Supports batching for high-throughput scenarios
- **Flexible**: Works with any AI model or provider
- **Standards-compliant**: Follows OpenTelemetry standards
- **Secure**: Uses the same authentication as logging operations

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 