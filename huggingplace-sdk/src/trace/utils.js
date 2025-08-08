// utils.js - Utility functions for tracing
import { v4 as uuidv4 } from 'uuid';

/**
 * Generate a unique ID for traces and spans
 * @returns {string} Unique ID
 */
export function generateId() {
    return uuidv4();
}

/**
 * Get current timestamp in ISO format
 * @returns {string} ISO timestamp
 */
export function getCurrentTimestamp() {
    return new Date().toISOString();
}

/**
 * Calculate duration between two timestamps
 * @param {number} startTime - Start time in milliseconds
 * @param {number} endTime - End time in milliseconds
 * @returns {number} Duration in milliseconds
 */
export function calculateDuration(startTime, endTime) {
    return endTime - startTime;
}
