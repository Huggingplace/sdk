import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';
import { validateConfig, validateLogOptions } from './validation.js';
import { AuthenticationError, NetworkError, createErrorFromResponse } from './errors.js';
import { Session } from './session.js';

// Import tracing functions from trace folder
import { traceStep as baseTraceStep } from './trace/traceStep.js';
import { traceLLMWithEvaluation as baseTraceLLM } from './trace/traceLLM.js';
import { traceMultiStepFlow as baseTraceMultiStepFlow } from './trace/traceMultiStep.js';
import { createSender } from './trace/sender.js';
import { DEFAULT_BASE_URL } from './config.js';
import { generateId } from './trace/utils.js';

/**
 * Main HuggingPlace SDK class
 */
export class HuggingPlace {
  /**
   * Create a new HuggingPlace instance
   * @param {Object} config - Configuration object
   * @param {string} config.apiKey - API key for authentication
   * @param {string} config.orgId - Organization ID
   * @param {string} [config.baseUrl] - Base URL for API
   * @param {string} [config.mode] - Environment mode (prod/dev)
   * @param {number} [config.timeout] - Request timeout in milliseconds
   * @param {boolean} [config.silent] - Silent mode (no console logs)
   * @param {string} [config.traceEndpoint] - Custom trace endpoint URL
   * @param {string} [config.traceBatchEndpoint] - Custom trace batch endpoint URL
   * @param {number} [config.traceBatchSize] - Trace batch size (default: 10)
   * @param {number} [config.traceBatchTimeout] - Trace batch timeout in ms (default: 5000)
   * @param {number} [config.traceMaxRetries] - Max retries for trace requests (default: 3)
   */
  constructor(config) {
    validateConfig(config);

    this.config = {
      mode: 'prod',
      timeout: 10000,
      silent: false,
      traceBatchSize: 10,
      traceBatchTimeout: 5000,
      traceMaxRetries: 3,
      ...config,
    };

    this.baseUrl = config.baseUrl || DEFAULT_BASE_URL;

    this.axiosInstance = axios.create({
      baseURL: this.baseUrl,
      timeout: this.config.timeout,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.config.apiKey}`,
      },
    });

    // Add response interceptor for error handling
    this.axiosInstance.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response) {
          const { status, data } = error.response;
          const message = data?.message || data?.error || error.message;
          throw createErrorFromResponse(status, message);
        } else if (error.request) {
          throw new NetworkError();
        } else {
          throw error;
        }
      }
    );

    // Create a configured sender instance for this HuggingPlace instance
    this.sender = createSender({
      baseUrl: this.baseUrl,
      batchSize: this.config.traceBatchSize,
      batchTimeout: this.config.traceBatchTimeout,
      maxRetries: this.config.traceMaxRetries,
      timeout: this.config.timeout,
      silent: this.config.silent,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.config.apiKey}`,
      }
    });
  }

  /**
   * Custom sendTrace function that enriches trace data with HuggingPlace metadata
   * @param {Object} trace - Trace data to send
   */
  async sendTrace(trace) {
    // Add org and mode from config
    const enrichedTrace = {
      ...trace,
      metadata: {
        ...trace.metadata,
        orgId: this.config.orgId,
        mode: this.config.mode,
      }
    };

    // Use the configured sender
    return await this.sender.sendTrace(enrichedTrace);
  }

  /**
   * Trace a single step with detailed metadata
   * @param {Object} options - Tracing parameters
   * @param {string} options.stepName - Name of the step
   * @param {Function} options.func - Function to trace
   * @param {string} [options.traceId] - Custom trace ID (auto-generated if not provided)
   * @param {string} [options.parentSpanId] - Parent span ID
   * @param {Object} [options.logs] - Additional logs
   * @param {Object} [options.attributes] - Additional attributes
   * @param {string} [options.status] - Step status (default: "OK")
   * @param {string} [options.evaluation] - Evaluation status
   * @param {Object} [options.metadata] - General metadata
   * @param {Object} [options.userMetadata] - User-specific metadata
   * @param {Object} [options.orgData] - Organization data
   * @param {Object} [options.llmData] - LLM-specific data
   * @param {Object} [options.customMetadata] - Custom metadata
   * @param {Object} [options.rest] - Any additional fields
   * @returns {Promise<any>} Result of the step
   */
  async traceStep(options) {
    // Use the base traceStep function but with our custom sendTrace
    return await baseTraceStep({
      ...options,
      traceId: options.traceId || generateId(),
      parentSpanId: options.parentSpanId || generateId(),
      sendTrace: this.sendTrace.bind(this) // Bind our custom sendTrace method
    });
  }

  /**
   * Trace an LLM call with evaluation capabilities
   * @param {Object} options - LLM tracing parameters
   * @param {string} options.prompt - The prompt sent to the LLM
   * @param {Function} options.llmFunction - Function that calls the LLM
   * @param {string} [options.traceId] - Custom trace ID (auto-generated if not provided)
   * @param {string} [options.parentSpanId] - Parent span ID
   * @param {string} [options.evaluationStatus] - Evaluation status (default: "REVIEW")
   * @param {Object} [options.user] - User metadata
   * @param {Object} [options.org] - Organization data
   * @param {Object} [options.llmMetadata] - LLM-specific metadata
   * @param {Array} [options.previousSteps] - Previous steps in the workflow
   * @param {Object} [options.customMetadata] - Custom metadata
   * @param {Object} [options.rest] - Any additional fields
   * @returns {Promise<Object>} LLM response with tracing data
   */
  async traceLLM(options) {
    // Use the base traceLLM function but with our custom sendTrace
    return await baseTraceLLM({
      ...options,
      traceId: options.traceId || generateId(),
      parentSpanId: options.parentSpanId || generateId(),
      sendTrace: this.sendTrace.bind(this) // Bind our custom sendTrace method
    });
  }

  /**
   * Trace a multi-step workflow with sequential execution
   * @param {Object} options - Multi-step tracing parameters
   * @param {string} options.flowName - Name of the workflow
   * @param {Array} options.steps - Array of step objects
   * @param {Object} [options.user] - User metadata
   * @param {Object} [options.org] - Organization data
   * @param {string} [options.traceId] - Custom trace ID (auto-generated if not provided)
   * @param {Object} [options.rest] - Any additional fields
   * @returns {Promise<any>} Result of the last step
   */
  async traceMultiStepFlow(options) {
    // Use the base traceMultiStepFlow function but with our custom sendTrace
    return await baseTraceMultiStepFlow({
      ...options,
      traceId: options.traceId || generateId(),
      sendTrace: this.sendTrace.bind(this) // Bind our custom sendTrace method
    });
  }

  /**
   * Log a complete interaction with HuggingPlace
   * @param {Object} options - Log options
   * @param {string} options.user_prompt - User prompt
   * @param {string} options.ai_response - AI response (preferred over 'response')
   * @param {string} options.response - AI response (alternative to 'ai_response')
   * @param {string} [options.user_uuid] - User UUID
   * @param {string} [options.file_name] - File name
   * @param {string} [options.session_id] - Session ID
   * @param {string} [options.llm_model] - LLM model used
   * @param {string} [options.llm_model2] - Secondary LLM model
   * @param {number} [options.token_count] - Token count
   * @param {Object} [options.metaData] - Additional metadata
   * @param {Array} [options.user_roles] - User roles array
   * @param {string} [options.org_uuid] - Organization UUID
   * @param {string} [options.mapping_table] - Database mapping table
   * @param {Array} [options.step_data] - Array of processing steps
   * @param {number} [options.response_time] - Response time in milliseconds
   * @param {string} [options.message_id] - Message ID
   * @param {Object} [options.user_meta_data] - User metadata (preferred over 'userMetadata')
   * @param {Object} [options.userMetadata] - User metadata (alternative to 'user_meta_data')
   * @param {number} [options.org_id] - Organization ID
   * @param {string} [options.mode] - Environment mode
   * @returns {Promise<void>}
   */
  async log(options) {
    try {
      validateLogOptions(options);

      // Map response to ai_response if not provided (keep both)
      if (options.response && !options.ai_response) {
        options.ai_response = options.response;
      }

      // Map userMetadata to user_meta_data if not provided
      if (options.userMetadata && !options.user_meta_data) {
        options.user_meta_data = options.userMetadata;
      }

      // Send response_time as-is without any formatting

      // Add org_id and mode from config
      const payload = {
        ...options,
        org_id: this.config.orgId,
        mode: this.config.mode,
      };

      if (!this.config.silent) {
        console.log("📤 Sending payload to backend:", JSON.stringify(payload, null, 2));
      }

      const response = await this.axiosInstance.post(
        '/v2/chatgpt/store_generated_response',
        payload
      );

      if (!this.config.silent) {
        console.log("📥 Response status:", response.status);
        console.log("📥 Response data:", response.data);
      }

      if (response.status !== 200) {
        throw createErrorFromResponse(response.status, response.data?.message || 'Unknown error');
      }

      const successMessage = response.data.message || 'Successfully logged interaction';
      if (!this.config.silent) {
        console.log(`✅ Logged interaction to HuggingPlace: ${successMessage}`);
      }
    } catch (error) {
      if (!this.config.silent) {
        console.error('❌ Failed to log interaction to HuggingPlace:', error);
      }
      throw error;
    }
  }

  /**
   * Log individual processing steps
   * @param {Object} options - Step options
   * @param {string} options.step_name - Step name
   * @param {string} options.status - Step status
   * @param {number} options.time_ms - Time in milliseconds
   * @param {string} options.userQuestion - User question for this step
   * @param {string} options.promptResponse - Response for this step
   * @param {string} [options.llmModel] - LLM model used
   * @param {number} [options.token] - Token count
   * @param {number} [options.responseTime] - Response time
   * @param {number} [options.inputTokens] - Input token count
   * @param {number} [options.outputTokens] - Output token count
   * @returns {Promise<void>}
   */
  async logStep(options) {
    // For individual steps, we create a minimal log entry
    await this.log({
      user_prompt: options.userQuestion || '',
      ai_response: options.promptResponse || '',
      llm_model: options.llmModel,
      token_count: options.token,
      response_time: options.responseTime,
      step_data: [options],
    });
  }

  /**
   * Start a new session for tracking multiple interactions
   * @param {string} [sessionId] - Session ID (auto-generated if not provided)
   * @param {Object} [options] - Session options
   * @param {Object} [options.metaData] - Default metadata for the session
   * @param {Object} [options.user_meta_data] - Default user metadata for the session
   * @returns {Session} Session instance
   */
  startSession(sessionId, options = {}) {
    const id = sessionId || uuidv4();
    return new Session(this, id, options);
  }

  /**
   * Log with automatic timing
   * @param {string} userPrompt - User prompt
   * @param {Function} responseGenerator - Function that generates the response
   * @param {Object} [options] - Additional options
   * @returns {Promise<string>} The generated response
   */
  async logWithTiming(userPrompt, responseGenerator, options = {}) {
    const startTime = Date.now();

    try {
      const response = await responseGenerator();
      const responseTime = (Date.now() - startTime) / 1000; // Convert to seconds

      await this.log({
        user_prompt: userPrompt,
        ai_response: response,
        response_time: `0 min ${responseTime.toFixed(2)} sec`, // Send as string format
        ...options,
      });

      return response;
    } catch (error) {
      // Log the error as well
      await this.log({
        user_prompt: userPrompt,
        ai_response: `Error: ${error instanceof Error ? error.message : String(error)}`,
        response_time: `0 min ${((Date.now() - startTime) / 1000).toFixed(2)} sec`, // Send as string format
        metaData: {
          ...options.metaData,
          error: true,
          errorMessage: error instanceof Error ? error.message : String(error),
        },
        ...options,
      });

      throw error;
    }
  }

  /**
   * Get current configuration
   * @returns {Object} Current configuration
   */
  getConfig() {
    return { ...this.config };
  }

  /**
   * Update configuration
   * @param {Object} newConfig - New configuration values
   */
  updateConfig(newConfig) {
    this.config = {
      ...this.config,
      ...newConfig,
    };

    // Update axios instance if baseUrl or timeout changed
    if (newConfig.baseUrl || newConfig.timeout) {
      this.axiosInstance = axios.create({
        baseURL: newConfig.baseUrl || this.baseUrl,
        timeout: newConfig.timeout || this.config.timeout,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.config.apiKey}`,
        },
      });
    }

    // Update sender configuration if tracing config changed
    if (newConfig.traceEndpoint || newConfig.traceBatchEndpoint || 
        newConfig.traceBatchSize || newConfig.traceBatchTimeout || 
        newConfig.traceMaxRetries || newConfig.silent) {
      
      this.sender = createSender({
        traceEndpoint: newConfig.traceEndpoint || this.traceEndpoint,
        batchEndpoint: newConfig.traceBatchEndpoint || this.traceBatchEndpoint,
        batchSize: newConfig.traceBatchSize || this.config.traceBatchSize,
        batchTimeout: newConfig.traceBatchTimeout || this.config.traceBatchTimeout,
        maxRetries: newConfig.traceMaxRetries || this.config.traceMaxRetries,
        timeout: newConfig.timeout || this.config.timeout,
        silent: newConfig.silent !== undefined ? newConfig.silent : this.config.silent,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.config.apiKey}`,
        }
      });
    }
  }

  /**
   * Test connection to HuggingPlace backend
   * @returns {Promise<boolean>} True if connection is successful
   */
  async testConnection() {
    try {
      const response = await this.axiosInstance.get('/health');
      return response.status === 200;
    } catch (error) {
      return false;
    }
  }
} 