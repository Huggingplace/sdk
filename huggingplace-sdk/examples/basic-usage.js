import { HuggingPlace } from '../src/index.js';

// Initialize the SDK
const huggingplace = new HuggingPlace({
  apiKey: 'your-api-key-here',
  orgId: 'your-org-id-here',
  mode: 'prod' // or 'dev'
});

// Example 1: Basic logging
async function basicLogging() {
  try {
    await huggingplace.log({
      user_prompt: 'What is the weather today?',
      ai_response: 'The weather is sunny with a temperature of 25°C.',
      session_id: 'session-123',
      llm_model: 'gpt-4o',
      token_count: 150,
      response_time: '0 min 2.50 sec',
      metaData: {
        likes: 1,
        dislikes: 0,
        customField: 'value'
      },
      user_meta_data: {
        email: 'user@example.com',
        username: 'john_doe',
        org_name: 'Example Corp'
      }
    });
    
    console.log('✅ Basic logging completed');
  } catch (error) {
    console.error('❌ Basic logging failed:', error.message);
  }
}

// Example 2: Session-based logging
async function sessionLogging() {
  try {
    // Create a session for related interactions
    const session = huggingplace.startSession('user-123', {
      metaData: {
        userId: 'user-123',
        conversationType: 'support'
      },
      user_meta_data: {
        email: 'user@example.com',
        org_name: 'Example Corp'
      }
    });

    // Log multiple interactions in the same session
    // session_id will automatically be set to 'user-123' from the session
    await session.log({
      user_prompt: 'I need help with my account',
      ai_response: 'I can help you with your account. What specific issue are you facing?',
      llm_model: 'gpt-4o'
    });

    await session.log({
      user_prompt: 'I can\'t log in',
      ai_response: 'Let me help you troubleshoot your login issue. Have you tried resetting your password?',
      llm_model: 'gpt-4o'
    });

    // You can also override the session_id if needed
    await session.log({
      user_prompt: 'What about my other account?',
      ai_response: 'I can help with your other account as well.',
      session_id: 'different-session-id', // This will override the session default
      llm_model: 'gpt-4o'
    });

    console.log('✅ Session logging completed');
  } catch (error) {
    console.error('❌ Session logging failed:', error.message);
  }
}

// Example 3: Step-by-step logging
async function stepLogging() {
  try {
    // Log individual processing steps
    await huggingplace.logStep({
      step_name: 'data_processing',
      status: 'completed',
      time_ms: 1800,
      userQuestion: 'Process the sales data',
      promptResponse: 'Data processed successfully. Found 1,245 sales records.',
      llmModel: 'gpt-4o',
      token: 120,
      responseTime: '0 min 1.80 sec',
      inputTokens: 40,
      outputTokens: 80
    });

    await huggingplace.logStep({
      step_name: 'sql_generation',
      status: 'completed',
      time_ms: 2100,
      userQuestion: 'Generate SQL query for monthly sales',
      promptResponse: 'SELECT DATE_TRUNC(\'month\', sale_date) as month, COUNT(*) as sales_count FROM sales GROUP BY month ORDER BY month;',
      llmModel: 'gpt-4o',
      token: 200,
      responseTime: '0 min 2.10 sec',
      inputTokens: 60,
      outputTokens: 140
    });

    console.log('✅ Step logging completed');
  } catch (error) {
    console.error('❌ Step logging failed:', error.message);
  }
}

// Example 4: Automatic timing
async function automaticTiming() {
  try {
    // Simulate an LLM call
    const mockLLMCall = async () => {
      // Simulate processing time
      await new Promise(resolve => setTimeout(resolve, 1000));
      return 'The weather is sunny with a temperature of 25°C.';
    };

    // Log with automatic timing
    const response = await huggingplace.logWithTiming(
      'What is the weather today?',
      mockLLMCall,
      {
        session_id: 'session-456',
        llm_model: 'gpt-4o',
        metaData: {
          source: 'weather_api',
          location: 'New York'
        }
      }
    );

    console.log('✅ Automatic timing completed. Response:', response);
  } catch (error) {
    console.error('❌ Automatic timing failed:', error.message);
  }
}

// Example 5: Error handling
async function errorHandling() {
  try {
    // Test with invalid configuration
    const invalidHuggingplace = new HuggingPlace({
      // Missing required fields
    });
  } catch (error) {
    console.log('✅ Validation error caught:', error.message);
  }

  try {
    // Test with invalid log options
    await huggingplace.log({
      // Missing required fields
    });
  } catch (error) {
    console.log('✅ Validation error caught:', error.message);
  }
}

// Example 6: Configuration management
async function configurationManagement() {
  try {
    // Get current configuration (without sensitive data)
    const config = huggingplace.getConfig();
    console.log('Current config:', config);

    // Update configuration
    huggingplace.updateConfig({
      timeout: 15000,
      mode: 'dev'
    });

    console.log('✅ Configuration updated');
  } catch (error) {
    console.error('❌ Configuration management failed:', error.message);
  }
}

// Example 7: Connection testing
async function testConnection() {
  try {
    const isConnected = await huggingplace.testConnection();
    console.log('Connection test result:', isConnected ? '✅ Connected' : '❌ Not connected');
  } catch (error) {
    console.error('❌ Connection test failed:', error.message);
  }
}

// Run all examples
async function runExamples() {
  console.log('🚀 Running HuggingPlace SDK Examples\n');

  console.log('1. Basic Logging:');
  await basicLogging();

  console.log('\n2. Session Logging:');
  await sessionLogging();

  console.log('\n3. Step Logging:');
  await stepLogging();

  console.log('\n4. Automatic Timing:');
  await automaticTiming();

  console.log('\n5. Error Handling:');
  await errorHandling();

  console.log('\n6. Configuration Management:');
  await configurationManagement();

  console.log('\n7. Connection Testing:');
  await testConnection();

  console.log('\n✅ All examples completed!');
}

// Run examples if this file is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  runExamples().catch(console.error);
}

export {
  basicLogging,
  sessionLogging,
  stepLogging,
  automaticTiming,
  errorHandling,
  configurationManagement,
  testConnection
}; 