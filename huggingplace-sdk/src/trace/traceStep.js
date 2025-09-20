// traceStep.js - Generic step tracer for any AI workflow step
import { tracer } from './tracerSetup.js';
import { sendTrace as defaultSendTrace } from './sender.js';
import { generateId } from './utils.js';

/**
 * Generic step tracer for any AI workflow step (LLM, embedding, custom, etc.)
 * Handles any return type: object, array, string, number, boolean, or void.
 * Users can pass any additional data via ...rest which gets included in the trace.
 * @param {Object} params - Tracing parameters
 * @param {string} params.traceId - Unique trace ID
 * @param {string} params.parentSpanId - Parent span ID
 * @param {string} params.stepName - Name of the step
 * @param {Function} params.func - Function to trace
 * @param {Object} [params.logs={}] - Additional logs
 * @param {Object} [params.attributes={}] - Additional attributes
 * @param {string} [params.status="OK"] - Step status
 * @param {string} [params.evaluation=null] - Evaluation status
 * @param {Object} [params.metadata={}] - General metadata
 * @param {Object} [params.userMetadata={}] - User-specific metadata
 * @param {Object} [params.orgData={}] - Organization data
 * @param {Object} [params.llmData={}] - LLM-specific data
 * @param {Object} [params.customMetadata={}] - Custom metadata
 * @param {Object} [params.parentOtelContext=null] - Parent OpenTelemetry context
 * @param {Function} [params.sendTrace] - Custom sendTrace function (defaults to default sender)
 * @param {Object} [params.rest] - Any additional fields from user
 * @returns {Promise<any>} Result of the step
 */
export async function traceStep({
    traceId,
    parentSpanId,
    stepName,
    func,
    logs = {},
    attributes = {},
    status = "OK",
    evaluation = null,
    metadata = {},
    userMetadata = {},
    orgData = {},
    llmData = {},
    customMetadata = {},
    parentOtelContext = null,
    sendTrace = defaultSendTrace,
    ...rest // capture any additional fields from user
}) {
    const startTime = Date.now();
    let otelSpan;
    
    if (parentOtelContext) {
        otelSpan = tracer.startSpan(stepName, { parent: parentOtelContext });
    } else {
        otelSpan = tracer.startSpan(stepName);
    }
    
    const spanId = generateId();

    let result;
    let error = null;
    try {
        result = await func();
    } catch (err) {
        status = "ERROR";
        error = err;
        result = { error: err.message };
    }

    const duration = Date.now() - startTime;

    // Always include the function result as functionResponse
    const functionResponse = result;

    const traceAttributes = {
        ...attributes,
        evaluation,
        ...llmData, // only include light/filtered values
        ...rest,
    };

    const traceLogs = {
        ...logs,
        ...llmData,
        functionResponse, // good for audit/debug
        ...rest,
        error: error?.message,
    };

    const fullMetadata = {
        ...metadata,
        userMetadata,
        orgData,
        llmData,
        ...customMetadata,
        functionResponse,
        ...rest, // include all additional fields from user
    };

    console.log({
        traceId,
        spanId,
        parentSpanId: parentSpanId || "0000000000000000",
        operation: stepName,
        service: "huggingplace-sdk",
        startTime: new Date(startTime).toISOString(),
        endTime: new Date().toISOString(),
        durationMs: duration,
        status,
        attributes: traceAttributes,
        logs: traceLogs,
        metadata: fullMetadata,
        otelContext: {
            otelTraceId: otelSpan.spanContext().traceId,
            otelSpanId: otelSpan.spanContext().spanId,
        },
    })

    await sendTrace({
        traceId,
        spanId,
        parentSpanId: parentSpanId || "0000000000000000",
        operation: stepName,
        service: "huggingplace-sdk",
        startTime: new Date(startTime).toISOString(),
        endTime: new Date().toISOString(),
        durationMs: duration,
        status,
        attributes: traceAttributes,
        logs: traceLogs,
        metadata: fullMetadata,
        otelContext: {
            otelTraceId: otelSpan.spanContext().traceId,
            otelSpanId: otelSpan.spanContext().spanId,
        },
    });

    otelSpan.end();
    return result;
}
