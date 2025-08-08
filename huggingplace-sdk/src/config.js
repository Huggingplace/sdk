// config.js - Default configuration for tracing

// Default base URL - declared once
export const DEFAULT_BASE_URL = 'https://anvsj57nul.execute-api.ap-south-1.amazonaws.com';

/**
 * Default configuration for tracing
 */
export const DEFAULT_TRACE_CONFIG = {
  // Default base URL (will be overridden by HuggingPlace baseUrl)
  baseUrl: DEFAULT_BASE_URL,

  // Batching configuration
  batchSize: 10,
  batchTimeout: 5000, // 5 seconds

  // Retry configuration
  maxRetries: 3,
  retryDelay: 1000, // 1 second

  // HTTP timeouts
  timeout: 10000, // 10 seconds for single requests
  batchTimeoutMs: 30000, // 30 seconds for batch requests

  // Logging
  silent: false,

  // Default headers
  headers: {
    'Content-Type': 'application/json'
  }
};

/**
 * Get trace configuration with optional overrides
 * @param {Object} overrides - Configuration overrides
 * @returns {Object} Merged configuration
 */
export function getTraceConfig(overrides = {}) {
  return {
    ...DEFAULT_TRACE_CONFIG,
    ...overrides
  };
}

/**
 * Build trace endpoints from base URL
 * @param {string} baseUrl - Base URL for the API
 * @returns {Object} Trace endpoints
 */
export function buildTraceEndpoints(baseUrl) {
  return {
    traceEndpoint: `${baseUrl}/api/traces`,
    batchEndpoint: `${baseUrl}/api/traces/batch`
  };
}
