import { ValidationError } from './errors.js';



/**
 * Validate SDK configuration
 * @param {Object} config - Configuration object
 * @throws {ValidationError} - If configuration is invalid
 */
export function validateConfig(config) {
  if (!config) {
    throw new ValidationError('Configuration is required');
  }

  if (!config.apiKey) {
    throw new ValidationError('API key is required');
  }

  if (!config.orgId) {
    throw new ValidationError('Organization ID is required');
  }

  if (config.timeout && (typeof config.timeout !== 'number' || config.timeout <= 0)) {
    throw new ValidationError('Timeout must be a positive number');
  }

  if (config.mode && !['prod', 'dev'].includes(config.mode)) {
    throw new ValidationError('Mode must be either "prod" or "dev"');
  }
}

/**
 * Validate log options
 * @param {Object} options - Log options
 * @throws {ValidationError} - If options are invalid
 */
export function validateLogOptions(options) {
  if (!options) {
    throw new ValidationError('Log options are required');
  }

  // Only validate data types, not presence
  if (options.token_count && (typeof options.token_count !== 'number' || options.token_count < 0)) {
    throw new ValidationError('Token count must be a non-negative number');
  }

  // No validation for response_time - accept any format
}

/**
 * Validate step data
 * @param {Object} stepData - Step data object
 * @throws {ValidationError} - If step data is invalid
 */
export function validateStepData(stepData) {
  if (!stepData) {
    throw new ValidationError('Step data is required');
  }

  if (!stepData.type) {
    throw new ValidationError('Step type is required');
  }

  if (!stepData.userQuestion) {
    throw new ValidationError('User question is required for step');
  }

  if (!stepData.promptResponse) {
    throw new ValidationError('Prompt response is required for step');
  }

  if (stepData.token && (typeof stepData.token !== 'number' || stepData.token < 0)) {
    throw new ValidationError('Step token count must be a non-negative number');
  }

  // No validation for step responseTime - accept any format
}

 