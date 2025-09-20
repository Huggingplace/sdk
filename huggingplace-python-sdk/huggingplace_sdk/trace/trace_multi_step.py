"""
Multi-step workflow tracing functionality
"""

import asyncio
from typing import Dict, Any, Callable, Optional, List, Union
from .trace_step import trace_step
from .utils import generate_id


async def trace_multi_step_flow(
    flow_name: str,
    steps: List[Dict[str, Any]],
    trace_id: Optional[str] = None,
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
) -> List[Any]:
    """
    Trace a multi-step workflow
    
    Args:
        flow_name: Name of the workflow
        steps: List of step configurations
        trace_id: Custom trace ID (auto-generated if not provided)
        user_metadata: User metadata
        org_data: Organization data
        custom_metadata: Custom metadata
        logs: Additional logs
        attributes: Additional attributes
        tags: Array of tags
        priority: Step priority
        status: Step status (default: "OK")
        send_trace_func: Custom send trace function
        **kwargs: Additional flow-level metadata
        
    Returns:
        List of results from each step
    """
    # Generate trace ID if not provided
    if trace_id is None:
        trace_id = generate_id()
    
    # Prepare flow-level metadata
    flow_metadata = {
        "userMetadata": user_metadata or {},
        "orgData": org_data or {},
        "customMetadata": custom_metadata or {},
        "tags": tags or [],
        "priority": priority,
        "flowName": flow_name,
        "traceId": trace_id,
        **kwargs  # Include any additional flow-level metadata
    }
    
    # Prepare flow-level attributes
    flow_attributes = {
        "workflow.name": flow_name,
        "workflow.step_count": len(steps),
        **(attributes or {})
    }
    
    # Prepare flow-level logs
    flow_logs = {
        "workflow.steps": [step.get("stepName", f"step_{i}") for i, step in enumerate(steps)],
        **(logs or {})
    }
    
    # Execute steps sequentially
    results = []
    previous_results = []
    
    for i, step_config in enumerate(steps):
        step_name = step_config.get("stepName", f"step_{i}")
        step_func = step_config["func"]
        
        # Prepare step-specific metadata
        step_metadata = {
            **flow_metadata,
            "stepOrder": i,
            "stepName": step_name
        }
        
        # Prepare step-specific attributes
        step_attributes = {
            **flow_attributes,
            "workflow.step_order": i,
            "workflow.step_name": step_name,
            **(step_config.get("attributes", {}))
        }
        
        # Prepare step-specific logs
        step_logs = {
            **flow_logs,
            "workflow.previous_results": previous_results,
            **(step_config.get("logs", {}))
        }
        
        # Execute the step
        try:
            # Pass previous results as arguments to the step function
            step_kwargs = {
                **step_config.get("kwargs", {}),
                "previous_results": previous_results
            }
            
            result = await trace_step(
                step_name=step_name,
                func=step_func,
                trace_id=trace_id,
                parent_span_id=trace_id,  # Use trace_id as parent for all steps
                user_metadata=user_metadata,
                org_data=org_data,
                custom_metadata=step_metadata,
                logs=step_logs,
                attributes=step_attributes,
                tags=step_config.get("tags", tags),
                priority=step_config.get("priority", priority),
                status=status,
                send_trace_func=send_trace_func,
                **step_kwargs
            )
            
            results.append(result)
            previous_results.append(result)
            
        except Exception as error:
            # Log the error and continue with next step if possible
            if not step_config.get("continue_on_error", False):
                raise error
            
            results.append(None)
            previous_results.append({"error": str(error)})
    
    return results
