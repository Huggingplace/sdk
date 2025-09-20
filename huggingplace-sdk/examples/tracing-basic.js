// Basic tracing example for HuggingPlace SDK
import { HuggingPlace, generateId } from '../src/index.js';


console.log("Asdfasjkdf")
// Initialize the SDK with tracing configuration
const hp = new HuggingPlace({
  apiKey: 'your-api-key',
  orgId: 'your-org-id',
  mode: 'dev', // or 'prod'
  silent: false, // Set to true to disable console logs
  // Optional tracing configuration
  traceBatchSize: 10,
  traceBatchTimeout: 5000,
  traceMaxRetries: 3
});

// Example 1: Trace a simple function
async function basicTracingExample() {
  console.log('=== Basic Tracing Example ===');
  
  const result = await hp.traceStep({
    stepName: 'Data Processing',
    func: async () => {
      // Simulate some work
      await new Promise(resolve => setTimeout(resolve, 100));
      return { processed: true, data: 'sample data' };
    },
    userMetadata: { userId: 'user-123', email: 'user@example.com' },
    orgData: { orgId: 'org-456', orgName: 'ExampleOrg' },
    customMetadata: { appVersion: '1.0.0', environment: 'development' },
    tags: ['data-processing', 'example'],
    priority: 'high'
  });
  
  console.log('Tracing result:', result);
}

// Example 2: Trace with logging
async function tracingWithLoggingExample() {
  console.log('\n=== Tracing with Logging Example ===');
  
  // First, trace the function
  const result = await hp.traceStep({
    stepName: 'User Analysis',
    func: async () => {
      // Simulate user analysis
      await new Promise(resolve => setTimeout(resolve, 200));
      return { 
        sentiment: 'positive',
        confidence: 0.85,
        keywords: ['happy', 'satisfied']
      };
    },
    userMetadata: { userId: 'user-123' },
    orgData: { orgId: 'org-456' },
    customMetadata: { analysisType: 'sentiment' }
  });

  
  console.log('Analysis completed and logged');
}

// Example 3: Error handling in tracing
async function tracingErrorExample() {
  console.log('\n=== Tracing Error Example ===');
  
  try {
    const result = await hp.traceStep({
      stepName: 'Risky Operation',
      func: async () => {
        // Simulate an error
        throw new Error('Something went wrong!');
      },
      userMetadata: { userId: 'user-123' },
      orgData: { orgId: 'org-456' }
    });
  } catch (error) {
    console.log('Error was caught and traced:', error.message);
  }
}

// Run all examples
async function runExamples() {
  try {
    await basicTracingExample();
    await tracingWithLoggingExample();
    await tracingErrorExample();
    
    console.log('\n=== All examples completed ===');
    console.log('Check your HuggingPlace backend for trace data!');
  } catch (error) {
    console.error('Example failed:', error);
  }
}

// Run if this file is executed directly
// if (import.meta.url === `file://${process.argv[1]}`) {
  runExamples();
// }

export { basicTracingExample, tracingWithLoggingExample, tracingErrorExample };
