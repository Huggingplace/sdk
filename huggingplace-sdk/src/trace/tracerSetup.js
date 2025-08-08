// tracerSetup.js - OpenTelemetry setup for HuggingPlace SDK
import { NodeSDK } from '@opentelemetry/sdk-node';
import { SimpleSpanProcessor } from '@opentelemetry/sdk-trace-base';
import { trace } from '@opentelemetry/api';
import { ConsoleSpanExporter } from '@opentelemetry/sdk-trace-base';

const serviceName = process.env.SERVICE_NAME || "huggingplace-sdk";

// Use ConsoleSpanExporter for SDK (traces will be sent via HTTP)
const sdk = new NodeSDK({
    serviceName,
    spanProcessor: new SimpleSpanProcessor(new ConsoleSpanExporter()),
});

sdk.start();
const tracer = trace.getTracer("huggingplace-sdk");

export { tracer };
