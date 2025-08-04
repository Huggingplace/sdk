import { HuggingPlace } from './huggingplace.js';

/**
 * Session class for managing related interactions
 */
export class Session {
  /**
   * Create a new session
   * @param {HuggingPlace} huggingplace - HuggingPlace instance
   * @param {string} sessionId - Session ID
   * @param {Object} options - Session options
   * @param {Object} [options.metadata] - Default metadata for the session
   * @param {Object} [options.userMetadata] - Default user metadata for the session
   */
  constructor(huggingplace, sessionId, options = {}) {
    this.huggingplace = huggingplace;
    this.sessionId = sessionId;
    this.defaultMetadata = options.metadata || {};
    this.defaultUserMetadata = options.userMetadata || {};
  }

  /**
   * Log an interaction with session defaults
   * @param {Object} options - Log options
   * @param {string} options.userPrompt - User prompt
   * @param {string} options.response - AI response
   * @param {string} [options.sessionId] - Session ID (uses session default if not provided)
   * @param {Object} [options.metadata] - Additional metadata
   * @param {Object} [options.userMetadata] - Additional user metadata
   * @returns {Promise<void>}
   */
  async log(options) {
    // Merge session defaults with provided options
    const mergedOptions = {
      ...options,
      // Only set sessionId if not provided by user
      sessionId: options.sessionId || this.sessionId,
      metadata: {
        ...this.defaultMetadata,
        ...options.metadata,
      },
      userMetadata: {
        ...this.defaultUserMetadata,
        ...options.userMetadata,
      },
    };

    await this.huggingplace.log(mergedOptions);
  }

  /**
   * Log an individual processing step
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
    await this.huggingplace.logStep(options);
  }

  /**
   * Update session defaults
   * @param {Object} [metadata] - New default metadata
   * @param {Object} [userMetadata] - New default user metadata
   */
  updateDefaults(metadata, userMetadata) {
    if (metadata) {
      this.defaultMetadata = { ...this.defaultMetadata, ...metadata };
    }
    if (userMetadata) {
      this.defaultUserMetadata = { ...this.defaultUserMetadata, ...userMetadata };
    }
  }

  /**
   * Get current session information
   * @returns {Object} Session information
   */
  getSessionInfo() {
    return {
      sessionId: this.sessionId,
      defaultMetadata: this.defaultMetadata,
      defaultUserMetadata: this.defaultUserMetadata,
    };
  }
} 