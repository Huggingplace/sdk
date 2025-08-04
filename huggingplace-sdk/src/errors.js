/**
 * Custom error classes for HuggingPlace SDK
 */

export class HuggingPlaceSDKError extends Error {
  constructor(message) {
    super(message);
    this.name = 'HuggingPlaceSDKError';
  }
}

export class AuthenticationError extends Error {
  constructor(message = 'Authentication failed') {
    super(message);
    this.name = 'AuthenticationError';
  }
}

export class ValidationError extends Error {
  constructor(message = 'Validation failed') {
    super(message);
    this.name = 'ValidationError';
  }
}

export class NetworkError extends Error {
  constructor(message = 'Network error occurred') {
    super(message);
    this.name = 'NetworkError';
  }
}

export class RateLimitError extends Error {
  constructor(message = 'Rate limit exceeded') {
    super(message);
    this.name = 'RateLimitError';
  }
}

export class ServerError extends Error {
  constructor(message = 'Server error occurred') {
    super(message);
    this.name = 'ServerError';
  }
}

/**
 * Create appropriate error from HTTP response
 * @param {number} status - HTTP status code
 * @param {string} message - Error message
 * @returns {Error} - Appropriate error instance
 */
export function createErrorFromResponse(status, message) {
  switch (status) {
    case 401:
      return new AuthenticationError(message);
    case 400:
      return new ValidationError(message);
    case 429:
      return new RateLimitError(message);
    case 500:
    case 502:
    case 503:
    case 504:
      return new ServerError(message);
    default:
      return new HuggingPlaceSDKError(message);
  }
} 