"""
LLM-specific tracing functionality
"""

import asyncio
from typing import Dict, Any, Callable, Optional, Union
from .trace_step import trace_step


async def trace_llm_with_evaluation(
    step_name: str,
    llm_func: Callable,
    trace_id: Optional[str] = None,
    parent_span_id: Optional[str] = None,
    user_metadata: Optional[Dict[str, Any]] = None,
    org_data: Optional[Dict[str, Any]] = None,
    llm_metadata: Optional[Dict[str, Any]] = None,
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
    Trace an LLM call with evaluation data
    
    Args:
        step_name: Name of the LLM step
        llm_func: LLM function to trace (should return rich response object)
        trace_id: Custom trace ID (auto-generated if not provided)
        parent_span_id: Parent span ID
        user_metadata: User metadata
        org_data: Organization data
        llm_metadata: LLM-specific metadata (model, provider, etc.)
        custom_metadata: Custom metadata
        logs: Additional logs
        attributes: Additional attributes
        tags: Array of tags
        priority: Step priority
        status: Step status (default: "OK")
        send_trace_func: Custom send trace function
        **kwargs: Additional arguments to pass to llm_func
        
    Returns:
        Result of the LLM function execution
    """
    # Generate IDs if not provided
    if trace_id is None:
        from .utils import generate_id
        trace_id = generate_id()
    if parent_span_id is None:
        from .utils import generate_id
        parent_span_id = generate_id()
    
    # Prepare LLM-specific metadata
    llm_metadata = llm_metadata or {}
    
    # Prepare metadata with LLM info
    metadata = {
        "userMetadata": user_metadata or {},
        "orgData": org_data or {},
        "llmData": llm_metadata,
        "customMetadata": custom_metadata or {},
        "tags": tags or [],
        "priority": priority,
        "stepName": step_name,
        "traceId": trace_id,
        "parentSpanId": parent_span_id
    }
    
    # Prepare LLM-specific attributes
    llm_attributes = {
        "llm.provider": llm_metadata.get("provider"),
        "llm.model": llm_metadata.get("model"),
        "llm.temperature": llm_metadata.get("temperature"),
        "llm.max_tokens": llm_metadata.get("maxTokens"),
        "llm.top_p": llm_metadata.get("topP"),
        "llm.frequency_penalty": llm_metadata.get("frequencyPenalty"),
        "llm.presence_penalty": llm_metadata.get("presencePenalty"),
        **(attributes or {})
    }
    
    # Prepare LLM-specific logs
    llm_logs = {
        "llm.prompt": kwargs.get("prompt"),
        "llm.messages": kwargs.get("messages"),
        "llm.parameters": {
            "temperature": llm_metadata.get("temperature"),
            "max_tokens": llm_metadata.get("maxTokens"),
            "top_p": llm_metadata.get("topP"),
            "frequency_penalty": llm_metadata.get("frequencyPenalty"),
            "presence_penalty": llm_metadata.get("presencePenalty")
        },
        **(logs or {})
    }
    
    # Call the base trace_step function
    result = await trace_step(
        step_name=step_name,
        func=llm_func,
        trace_id=trace_id,
        parent_span_id=parent_span_id,
        user_metadata=user_metadata,
        org_data=org_data,
        custom_metadata=custom_metadata,
        logs=llm_logs,
        attributes=llm_attributes,
        tags=tags,
        priority=priority,
        status=status,
        send_trace_func=send_trace_func,
        **kwargs
    )
    
    # If result is a rich LLM response object, extract additional data
    if isinstance(result, dict):
        # Update trace with LLM response details
        if send_trace_func:
            # This would require modifying the trace data after execution
            # For now, we'll rely on the function returning rich data
            pass
    
    return result
