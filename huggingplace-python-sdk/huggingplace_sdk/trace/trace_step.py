"""
Generic function for tracing any single step in an AI workflow
"""

import asyncio
from typing import Dict, Any, Callable, Optional, Union
from .utils import generate_id, get_current_timestamp, calculate_duration


async def trace_step(
    step_name: str,
    func: Callable,
    trace_id: Optional[str] = None,
    parent_span_id: Optional[str] = None,
    user_metadata: Optional[Dict[str, Any]] = None,
    org_data: Optional[Dict[str, Any]] = None,
    custom_metadata: Optional[Dict[str, Any]] = None,
    logs: Optional[Dict[str, Any]] = None,
    attributes: Optional[Dict[str, Any]] = None,
    tags: Optional[list] = None,
    priority: Optional[str] = None,
    status: str = "OK",
    send_trace_func: Optional[Callable] = None,
    **kwargs
) -> Any:
    """
    Trace a single step in an AI workflow
    
    Args:
        step_name: Name of the step
        func: Function to trace
        trace_id: Custom trace ID (auto-generated if not provided)
        parent_span_id: Parent span ID
        user_metadata: User metadata
        org_data: Organization data
        custom_metadata: Custom metadata
        logs: Additional logs
        attributes: Additional attributes
        tags: Array of tags
        priority: Step priority
        status: Step status (default: "OK")
        send_trace_func: Custom send trace function
        **kwargs: Additional arguments to pass to func
        
    Returns:
        Result of the function execution
    """
    # Generate IDs if not provided
    if trace_id is None:
        trace_id = generate_id()
    if parent_span_id is None:
        parent_span_id = generate_id()
    
    span_id = generate_id()
    start_time = get_current_timestamp()
    
    # Prepare metadata
    metadata = {
        "userMetadata": user_metadata or {},
        "orgData": org_data or {},
        "customMetadata": custom_metadata or {},
        "tags": tags or [],
        "priority": priority,
        "stepName": step_name,
        "traceId": trace_id,
        "parentSpanId": parent_span_id,
        "spanId": span_id
    }
    
    # Prepare trace data
    trace_data = {
        "traceId": trace_id,
        "spanId": span_id,
        "parentSpanId": parent_span_id,
        "operation": step_name,
        "service": "huggingplace-sdk",
        "status": status,
        "startTime": start_time,
        "attributes": attributes or {},
        "logs": logs or {},
        "metadata": metadata,
        "otelContext": {
            "otelTraceId": trace_id,
            "otelSpanId": span_id
        }
    }
    
    try:
        # Execute the function
        if asyncio.iscoroutinefunction(func):
            result = await func(**kwargs)
        else:
            result = func(**kwargs)
        
        # Calculate duration
        end_time = get_current_timestamp()
        duration_ms = calculate_duration(start_time, end_time)
        
        # Update trace data with success info
        trace_data.update({
            "endTime": end_time,
            "durationMs": duration_ms,
            "status": "OK",
            "logs": {
                **(logs or {}),
                "functionResponse": result,
                "success": True
            }
        })
        
        # Send trace if function provided
        if send_trace_func:
            await send_trace_func(trace_data)
        
        return result
        
    except Exception as error:
        # Calculate duration
        end_time = get_current_timestamp()
        duration_ms = calculate_duration(start_time, end_time)
        
        # Update trace data with error info
        trace_data.update({
            "endTime": end_time,
            "durationMs": duration_ms,
            "status": "ERROR",
            "logs": {
                **(logs or {}),
                "error": str(error),
                "errorType": type(error).__name__,
                "success": False
            }
        })
        
        # Send trace if function provided
        if send_trace_func:
            await send_trace_func(trace_data)
        
        # Re-raise the error
        raise error
