// Multi-step workflow tracing example for HuggingPlace SDK
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

// Example 1: Complete AI workflow with multiple steps
async function completeWorkflowExample() {
  console.log('=== Complete AI Workflow Example ===');
  
  const user = { userId: 'user-123', email: 'user@example.com' };
  const org = { orgId: 'org-456', orgName: 'ExampleOrg' };
  
  const result = await hp.traceMultiStepFlow({
    flowName: 'Customer Support Analysis',
    user,
    org,
    steps: [
      {
        name: 'Data Collection',
        func: async () => {
          await new Promise(resolve => setTimeout(resolve, 100));
          return {
            customerId: 'cust-789',
            query: 'I need help with my subscription',
            timestamp: new Date().toISOString()
          };
        },
        evaluation: 'REVIEW',
        metadata: { stepType: 'data-collection' },
        rest: { source: 'web-form', priority: 'medium' }
      },
      {
        name: 'Sentiment Analysis',
        func: async (previousResults) => {
          const data = previousResults[0];
          await new Promise(resolve => setTimeout(resolve, 150));
          
          return {
            sentiment: 'neutral',
            confidence: 0.75,
            keywords: ['help', 'subscription', 'need'],
            urgency: 'medium'
          };
        },
        evaluation: 'APPROVED',
        metadata: { stepType: 'nlp-analysis' },
        rest: { model: 'sentiment-v1', language: 'en' }
      },
      {
        name: 'LLM Response Generation',
        func: async (previousResults) => {
          const data = previousResults[0];
          const sentiment = previousResults[1];
          
          // Simulate LLM call
          await new Promise(resolve => setTimeout(resolve, 300));
          
          return {
            responseText: `Thank you for reaching out about your subscription. I understand you need assistance, and I'm here to help. Let me connect you with our support team who can address your specific concerns.`,
            finishReason: 'stop',
            inputTokens: 45,
            outputTokens: 35,
            totalTokens: 80,
            rawResponse: {
              choices: [{
                message: { content: `Thank you for reaching out about your subscription. I understand you need assistance, and I'm here to help. Let me connect you with our support team who can address your specific concerns.` },
                finish_reason: 'stop'
              }],
              usage: {
                prompt_tokens: 45,
                completion_tokens: 35,
                total_tokens: 80
              }
            }
          };
        },
        evaluation: 'REVIEW',
        metadata: { stepType: 'llm-generation' },
        rest: { model: 'gpt-4', provider: 'openai', temperature: 0.7 }
      },
      {
        name: 'Response Validation',
        func: async (previousResults) => {
          const llmResult = previousResults[2];
          await new Promise(resolve => setTimeout(resolve, 50));
          
          return {
            isValid: true,
            safetyScore: 0.95,
            complianceCheck: 'passed',
            suggestedImprovements: []
          };
        },
        evaluation: 'APPROVED',
        metadata: { stepType: 'validation' },
        rest: { validator: 'safety-v2', threshold: 0.9 }
      },
      {
        name: 'Final Response',
        func: async (previousResults) => {
          const data = previousResults[0];
          const sentiment = previousResults[1];
          const llmResult = previousResults[2];
          const validation = previousResults[3];
          
          await new Promise(resolve => setTimeout(resolve, 75));
          
          return {
            finalResponse: llmResult.responseText,
            customerId: data.customerId,
            sentiment: sentiment.sentiment,
            urgency: sentiment.urgency,
            isValid: validation.isValid,
            totalProcessingTime: 675, // sum of all delays
            traceId: generateId()
          };
        },
        evaluation: 'APPROVED',
        metadata: { stepType: 'final-assembly' },
        rest: { format: 'json', includeMetadata: true }
      }
    ],
    customMetadata: {
      workflowType: 'customer-support',
      version: '1.0.0',
      environment: 'production'
    },
    tags: ['workflow', 'customer-support', 'ai-pipeline']
  });
  
  console.log('Complete workflow result:', result);

}

// Example 2: Simple 3-step workflow
async function simpleWorkflowExample() {
  console.log('\n=== Simple 3-Step Workflow Example ===');
  
  const result = await hp.traceMultiStepFlow({
    flowName: 'Data Processing Pipeline',
    user: { userId: 'user-123' },
    org: { orgId: 'org-456' },
    steps: [
      {
        name: 'Data Input',
        func: async () => {
          await new Promise(resolve => setTimeout(resolve, 50));
          return { data: [1, 2, 3, 4, 5], count: 5 };
        },
        evaluation: 'APPROVED'
      },
      {
        name: 'Data Processing',
        func: async (previousResults) => {
          const input = previousResults[0];
          await new Promise(resolve => setTimeout(resolve, 100));
          
          const processed = input.data.map(x => x * 2);
          return { 
            original: input.data, 
            processed, 
            sum: processed.reduce((a, b) => a + b, 0) 
          };
        },
        evaluation: 'APPROVED'
      },
      {
        name: 'Result Output',
        func: async (previousResults) => {
          const processed = previousResults[1];
          await new Promise(resolve => setTimeout(resolve, 25));
          
          return {
            message: `Processed ${processed.original.length} items. Sum: ${processed.sum}`,
            summary: processed
          };
        },
        evaluation: 'APPROVED'
      }
    ],
    customMetadata: { pipelineType: 'data-processing' },
    tags: ['pipeline', 'data-processing', 'simple']
  });
  
  console.log('Simple workflow result:', result);
}

// Example 3: Error handling in workflow
async function workflowWithErrorExample() {
  console.log('\n=== Workflow with Error Example ===');
  
  try {
    const result = await hp.traceMultiStepFlow({
      flowName: 'Error Handling Test',
      user: { userId: 'user-123' },
      org: { orgId: 'org-456' },
      steps: [
        {
          name: 'Step 1 - Success',
          func: async () => {
            await new Promise(resolve => setTimeout(resolve, 50));
            return { status: 'success', data: 'step1' };
          },
          evaluation: 'APPROVED'
        },
        {
          name: 'Step 2 - Error',
          func: async (previousResults) => {
            await new Promise(resolve => setTimeout(resolve, 50));
            throw new Error('Simulated error in step 2');
          },
          evaluation: 'REVIEW'
        },
        {
          name: 'Step 3 - Never Reached',
          func: async (previousResults) => {
            return { status: 'skipped' };
          },
          evaluation: 'APPROVED'
        }
      ],
      customMetadata: { testType: 'error-handling' }
    });
  } catch (error) {
    console.log('Workflow error caught:', error.message);
  }
}

// Run all examples
async function runExamples() {
  try {
    await completeWorkflowExample();
    await simpleWorkflowExample();
    await workflowWithErrorExample();
    
    console.log('\n=== All multi-step workflow examples completed ===');
    console.log('Check your HuggingPlace backend for trace data!');
  } catch (error) {
    console.error('Example failed:', error);
  }
}

// Run if this file is executed directly
// if (import.meta.url === `file://${process.argv[1]}`) {
  runExamples();
// }

export { completeWorkflowExample, simpleWorkflowExample, workflowWithErrorExample };
