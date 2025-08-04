import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';
import { validateConfig, validateLogOptions } from './validation.js';
import { AuthenticationError, NetworkError, createErrorFromResponse } from './errors.js';
import { Session } from './session.js';

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
   */
  constructor(config) {
    validateConfig(config);

    this.config = {
      mode: 'prod',
      timeout: 10000,
      silent: false,
      ...config,
    };

    this.baseUrl = config.baseUrl || 'https://anvsj57nul.execute-api.ap-south-1.amazonaws.com';

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
  }

  /**
   * Log a complete interaction with HuggingPlace
   * @param {Object} options - Log options
   * @param {string} options.userPrompt - User prompt
   * @param {string} options.response - AI response
   * @param {string} [options.sessionId] - Session ID
   * @param {string} [options.llmModel] - LLM model used
   * @param {number} [options.tokenCount] - Token count
   * @param {number} [options.responseTime] - Response time in seconds
   * @param {Object} [options.metadata] - Additional metadata
   * @param {Object} [options.userMetadata] - User metadata
   * @param {Array} [options.stepData] - Array of processing steps
   * @returns {Promise<void>}
   */
  async log(options) {
    try {
      validateLogOptions(options);

      // Add orgId and mode from config
      const payload = {
        ...options,
        orgId: this.config.orgId,
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
   * @param {string} options.type - Step type
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
      userPrompt: options.userQuestion,
      response: options.promptResponse,
      llmModel: options.llmModel,
      tokenCount: options.token,
      responseTime: options.responseTime,
      stepData: [options],
    });
  }

  /**
   * Start a new session for tracking multiple interactions
   * @param {string} [sessionId] - Session ID (auto-generated if not provided)
   * @param {Object} [options] - Session options
   * @param {Object} [options.metadata] - Default metadata for the session
   * @param {Object} [options.userMetadata] - Default user metadata for the session
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
        userPrompt,
        response,
        responseTime,
        ...options,
      });

      return response;
    } catch (error) {
      // Log the error as well
      await this.log({
        userPrompt,
        response: `Error: ${error instanceof Error ? error.message : String(error)}`,
        responseTime: (Date.now() - startTime) / 1000,
        metadata: {
          ...options.metadata,
          error: true,
          errorMessage: error instanceof Error ? error.message : String(error),
        },
        ...options,
      });

      throw error;
    }
  }

  /**
   * Get current configuration (without sensitive data)
   * @returns {Object} Safe configuration object
   */
  getConfig() {
    const { apiKey, ...safeConfig } = this.config;
    return safeConfig;
  }

  /**
   * Update configuration
   * @param {Object} newConfig - New configuration options
   */
  updateConfig(newConfig) {
    const updatedConfig = { ...this.config, ...newConfig };
    validateConfig(updatedConfig);

    this.config = updatedConfig;

    // Update axios instance with new config
    this.axiosInstance.defaults.headers['Authorization'] = `Bearer ${this.config.apiKey}`;
    this.axiosInstance.defaults.timeout = this.config.timeout;
  }

  /**
   * Test connection to HuggingPlace API
   * @returns {Promise<boolean>} True if connection successful
   */
  async testConnection() {
    try {
      // Try to make a minimal request to test the connection
      // Since /health doesn't exist, we'll test with a minimal log request
      const testPayload = {
        userPrompt: 'connection_test',
        response: 'test_response',
        orgId: this.config.orgId,
        mode: this.config.mode
      };
      
      const response = await this.axiosInstance.post(
        '/v2/chatgpt/store_generated_response',
        testPayload
      );
      return response.status === 200;
    } catch (error) {
      if (!this.config.silent) {
        console.error('Connection test failed:', error);
      }
      return false;
    }
  }
} 