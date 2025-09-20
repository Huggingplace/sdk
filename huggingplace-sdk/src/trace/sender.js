// sender.js - Send trace data to HuggingPlace backend
import axios from 'axios';
import { DEFAULT_TRACE_CONFIG } from '../config.js';

/**
 * Create a configured sender instance
 * @param {Object} config - Configuration object
 * @returns {Object} Sender instance with methods
 */
export function createSender(config = {}) {
    const senderConfig = { ...DEFAULT_TRACE_CONFIG, ...config };
    
    // Build endpoints from baseUrl
    const baseUrl = senderConfig.baseUrl || DEFAULT_TRACE_CONFIG.baseUrl;
    const traceEndpoint = `${baseUrl}/api/traces`;
    const batchEndpoint = `${baseUrl}/api/traces/batch`;
    
    // Instance state
    let traceBatch = [];
    let batchTimeout = null;

    /**
     * Send a single trace with retry logic
     * @param {Object} traceData - Trace data to send
     * @param {number} retries - Current retry attempt
     * @returns {Promise<Object|null>} Response data or null if failed
     */
    async function sendTraceWithRetry(traceData, retries = 0) {
        try {
            const response = await axios.post(traceEndpoint, traceData, {
                timeout: senderConfig.timeout,
                headers: senderConfig.headers
            });
            
            if (response.status === 201) {
                if (!senderConfig.silent) {
                    console.log(`✅ Trace sent successfully: ${response.data.traceId}`);
                }
                return response.data;
            } else {
                throw new Error(`Unexpected status: ${response.status}`);
            }
        } catch (error) {
            if (!senderConfig.silent) {
                console.error(`❌ Failed to send trace (attempt ${retries + 1}):`, error.message);
            }
            
            if (retries < senderConfig.maxRetries) {
                // Exponential backoff
                const delay = senderConfig.retryDelay * Math.pow(2, retries);
                if (!senderConfig.silent) {
                    console.log(`🔄 Retrying in ${delay}ms...`);
                }
                
                await new Promise(resolve => setTimeout(resolve, delay));
                return sendTraceWithRetry(traceData, retries + 1);
            } else {
                if (!senderConfig.silent) {
                    console.error('❌ Max retries reached, dropping trace');
                }
                return null;
            }
        }
    }

    /**
     * Send a batch of traces with retry logic
     * @param {Array} traces - Array of trace data
     * @param {number} retries - Current retry attempt
     * @returns {Promise<Object|null>} Response data or null if failed
     */
    async function sendBatchWithRetry(traces, retries = 0) {
        try {
            const response = await axios.post(batchEndpoint, traces, {
                timeout: senderConfig.batchTimeoutMs,
                headers: senderConfig.headers
            });
            
            if (response.status === 201) {
                if (!senderConfig.silent) {
                    console.log(`✅ Batch sent successfully: ${response.data.count} traces`);
                }
                return response.data;
            } else {
                throw new Error(`Unexpected status: ${response.status}`);
            }
        } catch (error) {
            if (!senderConfig.silent) {
                console.error(`❌ Failed to send batch (attempt ${retries + 1}):`, error.message);
            }
            
            if (retries < senderConfig.maxRetries) {
                const delay = senderConfig.retryDelay * Math.pow(2, retries);
                if (!senderConfig.silent) {
                    console.log(`🔄 Retrying batch in ${delay}ms...`);
                }
                
                await new Promise(resolve => setTimeout(resolve, delay));
                return sendBatchWithRetry(traces, retries + 1);
            } else {
                if (!senderConfig.silent) {
                    console.error('❌ Max retries reached, dropping batch');
                }
                return null;
            }
        }
    }

    /**
     * Flush the current batch of traces
     */
    function flushBatch() {
        if (traceBatch.length > 0) {
            const batch = [...traceBatch];
            traceBatch = [];
            
            sendBatchWithRetry(batch).catch(error => {
                if (!senderConfig.silent) {
                    console.error('❌ Failed to flush batch:', error);
                }
            });
        }
    }

    /**
     * Send a trace (single or batched)
     * @param {Object} trace - Trace data to send
     */
    async function sendTrace(trace) {
        try {
            // Validate required fields
            if (!trace.traceId || !trace.spanId || !trace.operation) {
                if (!senderConfig.silent) {
                    console.error('❌ Invalid trace data: missing required fields');
                }
                return;
            }

            // Add to batch if batching is enabled
            if (senderConfig.batchSize > 1) {
                traceBatch.push(trace);
                
                // Clear existing timeout
                if (batchTimeout) {
                    clearTimeout(batchTimeout);
                }
                
                // Flush if batch is full
                if (traceBatch.length >= senderConfig.batchSize) {
                    flushBatch();
                } else {
                    // Set timeout to flush remaining traces
                    batchTimeout = setTimeout(flushBatch, senderConfig.batchTimeout);
                }
            } else {
                // Send immediately if batching is disabled
                await sendTraceWithRetry(trace);
            }
        } catch (error) {
            if (!senderConfig.silent) {
                console.error('❌ Error in sendTrace:', error);
            }
        }
    }

    return {
        sendTrace,
        sendTraceWithRetry,
        sendBatchWithRetry,
        flushBatch
    };
}

// Create default sender instance for backward compatibility
const defaultSender = createSender();

/**
 * Send a trace using the default sender (backward compatibility)
 * @param {Object} trace - Trace data to send
 */
export async function sendTrace(trace) {
    return await defaultSender.sendTrace(trace);
}

// Graceful shutdown - flush any remaining traces
process.on('SIGINT', () => {
    console.log('Flushing remaining traces...');
    defaultSender.flushBatch();
    process.exit(0);
});

process.on('SIGTERM', () => {
    console.log('Flushing remaining traces...');
    defaultSender.flushBatch();
    process.exit(0);
});
