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
   * @param {Object} [options.metaData] - Default metadata for the session
   * @param {Object} [options.user_meta_data] - Default user metadata for the session
   */
  constructor(huggingplace, sessionId, options = {}) {
    this.huggingplace = huggingplace;
    this.sessionId = sessionId;
    this.defaultMetadata = options.metaData || {};
    this.defaultUserMetaData = options.user_meta_data || {};
  }

  /**
   * Log an interaction with session defaults
   * @param {Object} options - Log options
   * @param {string} options.user_prompt - User prompt
   * @param {string} options.ai_response - AI response
   * @param {string} [options.session_id] - Session ID (uses session default if not provided)
   * @param {Object} [options.metaData] - Additional metadata
   * @param {Object} [options.user_meta_data] - Additional user metadata
   * @returns {Promise<void>}
   */
  async log(options) {
    // Merge session defaults with provided options
    const mergedOptions = {
      ...options,
      // Only set session_id if not provided by user
      session_id: options.session_id || this.sessionId,
      metaData: {
        ...this.defaultMetadata,
        ...options.metaData,
      },
      user_meta_data: {
        ...this.defaultUserMetaData,
        ...options.user_meta_data,
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
   * @param {Object} [userMetaData] - New default user metadata
   */
  updateDefaults(metadata, userMetaData) {
    if (metadata) {
      this.defaultMetadata = { ...this.defaultMetadata, ...metadata };
    }
    if (userMetaData) {
      this.defaultUserMetaData = { ...this.defaultUserMetaData, ...userMetaData };
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
      defaultUserMetaData: this.defaultUserMetaData,
    };
  }
} 