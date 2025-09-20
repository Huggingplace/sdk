// traceLLM.js - LLM-specific tracing wrapper
import { traceStep } from './traceStep.js';

/**
 * Trace an LLM call with evaluation capabilities
 * @param {Object} params - LLM tracing parameters
 * @param {string} params.traceId - Unique trace ID
 * @param {string} params.parentSpanId - Parent span ID
 * @param {string} params.prompt - The prompt sent to the LLM
 * @param {Function} params.llmFunction - Function that calls the LLM
 * @param {string} [params.evaluationStatus="REVIEW"] - Evaluation status
 * @param {Object} [params.user={}] - User metadata
 * @param {Object} [params.org={}] - Organization data
 * @param {Object} [params.llmMetadata={}] - LLM-specific metadata
 * @param {Array} [params.previousSteps=null] - Previous steps in the workflow
 * @param {Object} [params.customMetadata={}] - Custom metadata
 * @param {Function} [params.sendTrace] - Custom sendTrace function
 * @param {Object} [params.rest] - Any additional fields
 * @returns {Promise<Object>} LLM response with tracing data
 */
export async function traceLLMWithEvaluation({
    traceId,
    parentSpanId,
    prompt,
    llmFunction,
    evaluationStatus = "REVIEW",
    user = {},
    org = {},
    llmMetadata = {},
    previousSteps = null,
    customMetadata = {},
    sendTrace,
    ...rest
}) {
    const wrappedFunc = async () => {
        let llmResult;
        try {
            llmResult = await llmFunction();
            return llmResult;
        } catch (err) {
            throw err;
        }
    };

    return await traceStep({
        traceId,
        parentSpanId,
        stepName: "LLM Call",
        func: wrappedFunc,
        logs: {
            prompt,
            previousSteps,
            evaluation: evaluationStatus,
        },
        attributes: {
            "prompt.text": prompt,
        },
        evaluation: evaluationStatus,
        userMetadata: user,
        orgData: org,
        llmData: llmMetadata,
        customMetadata,
        sendTrace,
        ...rest,
    });
}
