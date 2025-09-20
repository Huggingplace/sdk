// LLM tracing example for HuggingPlace SDK
import { HuggingPlace, generateId } from '../src/index.js';

// Initialize the SDK with tracing configuration
const hp = new HuggingPlace({
  apiKey: 'your-api-key',
  orgId: 'your-org-id',
  mode: 'dev',
  silent: false,
  traceBatchSize: 10,
  traceBatchTimeout: 5000,
  traceMaxRetries: 3
});

// Example 1: Trace OpenAI API call
async function openAITracingExample() {
  console.log('=== OpenAI Tracing Example ===');
  
  // Simulate OpenAI API call
  const openAIFunction = async () => {
    // In real usage, this would be an actual OpenAI API call
    await new Promise(resolve => setTimeout(resolve, 500));
    
    return {
      responseText: "I'm doing great! How can I help you today?",
      finishReason: "stop",
      inputTokens: 25,
      outputTokens: 15,
      totalTokens: 40,
      rawResponse: {
        choices: [{
          message: { content: "I'm doing great! How can I help you today?" },
          finish_reason: "stop"
        }],
        usage: {
          prompt_tokens: 25,
          completion_tokens: 15,
          total_tokens: 40
        }
      }
    };
  };
  
  const result = await hp.traceLLM({
    prompt: "How are you feeling today?",
    llmFunction: openAIFunction,
    evaluationStatus: "REVIEW",
    user: { userId: "user-123", email: "user@example.com" },
    org: { orgId: "org-456", orgName: "ExampleOrg" },
    llmMetadata: {
      model: "gpt-4",
      provider: "openai",
      temperature: 0.7,
      maxTokens: 100
    },
    customMetadata: {
      appVersion: "1.0.0",
      environment: "development"
    },
    tags: ["openai", "gpt-4", "conversation"],
    sessionId: "session-789"
  });
  
  console.log('OpenAI tracing result:', result);
  
}

// Example 2: Trace Anthropic API call
async function anthropicTracingExample() {
  console.log('\n=== Anthropic Tracing Example ===');
  
  // Simulate Anthropic API call
  const anthropicFunction = async () => {
    await new Promise(resolve => setTimeout(resolve, 300));
    
    return {
      responseText: "I'm an AI assistant designed to help with various tasks. What would you like to know?",
      finishReason: "end_turn",
      inputTokens: 30,
      outputTokens: 20,
      totalTokens: 50,
      rawResponse: {
        content: [{
          type: "text",
          text: "I'm an AI assistant designed to help with various tasks. What would you like to know?"
        }],
        stop_reason: "end_turn",
        usage: {
          input_tokens: 30,
          output_tokens: 20
        }
      }
    };
  };
  
  const result = await hp.traceLLM({
    prompt: "What can you help me with?",
    llmFunction: anthropicFunction,
    evaluationStatus: "APPROVED",
    user: { userId: "user-123" },
    org: { orgId: "org-456" },
    llmMetadata: {
      model: "claude-3-sonnet",
      provider: "anthropic",
      temperature: 0.5,
      maxTokens: 150
    },
    customMetadata: {
      appVersion: "1.0.0"
    },
    tags: ["anthropic", "claude-3", "assistant"]
  });
  
  console.log('Anthropic tracing result:', result);
}

// Example 3: Trace with previous steps context
async function tracingWithContextExample() {
  console.log('\n=== Tracing with Context Example ===');
  
  // Simulate a conversation with context
  const conversationFunction = async () => {
    await new Promise(resolve => setTimeout(resolve, 400));
    
    return {
      responseText: "Based on our previous conversation about AI, I can help you understand machine learning concepts, implement algorithms, or discuss the latest developments in the field.",
      finishReason: "stop",
      inputTokens: 45,
      outputTokens: 35,
      totalTokens: 80,
      rawResponse: {
        choices: [{
          message: { content: "Based on our previous conversation about AI, I can help you understand machine learning concepts, implement algorithms, or discuss the latest developments in the field." },
          finish_reason: "stop"
        }],
        usage: {
          prompt_tokens: 45,
          completion_tokens: 35,
          total_tokens: 80
        }
      }
    };
  };
  
  const previousSteps = [
    { step: "User Introduction", result: "User asked about AI capabilities" },
    { step: "Context Analysis", result: "Identified user's interest in machine learning" }
  ];
  
  const result = await hp.traceLLM({
    prompt: "What specific areas of AI can you help me with?",
    llmFunction: conversationFunction,
    evaluationStatus: "REVIEW",
    user: { userId: "user-123" },
    org: { orgId: "org-456" },
    llmMetadata: {
      model: "gpt-4",
      provider: "openai",
      temperature: 0.3
    },
    previousSteps,
    customMetadata: {
      conversationId: "conv-123",
      turnNumber: 3
    },
    tags: ["conversation", "context-aware", "gpt-4"]
  });
  
  console.log('Context-aware tracing result:', result);
}

// Run all examples
async function runExamples() {
  try {
    await openAITracingExample();
    await anthropicTracingExample();
    await tracingWithContextExample();
    
    console.log('\n=== All LLM tracing examples completed ===');
    console.log('Check your HuggingPlace backend for trace data!');
  } catch (error) {
    console.error('Example failed:', error);
  }
}

// Run if this file is executed directly
// if (import.meta.url === `file://${process.argv[1]}`) {
  runExamples();
// }

export { openAITracingExample, anthropicTracingExample, tracingWithContextExample };
