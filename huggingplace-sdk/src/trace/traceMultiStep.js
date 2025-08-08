// traceMultiStep.js - Multi-step workflow tracer
import { generateId } from './utils.js';
import { traceStep } from './traceStep.js';

/**
 * Trace a multi-step workflow with sequential execution
 * @param {Object} params - Multi-step tracing parameters
 * @param {string} params.flowName - Name of the workflow
 * @param {Array} params.steps - Array of step objects
 * @param {Object} [params.user={}] - User metadata
 * @param {Object} [params.org={}] - Organization data
 * @param {Function} [params.sendTrace] - Custom sendTrace function
 * @param {Object} [params.rest] - Any additional fields from user
 * @returns {Promise<any>} Result of the last step
 */
export async function traceMultiStepFlow({
    flowName,
    steps = [],
    user = {},
    org = {},
    sendTrace,
    ...rest // capture any additional fields from user
}) {
    const traceId = generateId();
    const rootSpanId = generateId();
    let previousSteps = [];
    let previousResults = []; // Array to store all previous step results

    let result = null;

    for (const step of steps) {
        const wrappedFunc = async () => {
            // Call the step function with previousResults as argument
            // Check if function expects arguments
            if (step.func.length > 0) {
                return await step.func(previousResults);
            } else {
                return await step.func();
            }
        };

        const stepResult = await traceStep({
            traceId,
            parentSpanId: rootSpanId,
            stepName: step.name,
            func: wrappedFunc,
            logs: {
                previousSteps,
            },
            evaluation: step.evaluation || "REVIEW",
            metadata: {
                user,
                org,
                stepMetadata: step.metadata || {},
                flowName,
            },
            userMetadata: user,
            orgData: org,
            customMetadata: step.metadata || {},
            sendTrace,
            ...rest, // include all additional fields from user (flow-level)
            ...step.rest || {}, // allow step-specific additional fields
        });

        previousSteps.push({
            step: step.name,
            result: stepResult,
        });
        previousResults.push(stepResult);
        result = stepResult;
    }

    return result;
}
