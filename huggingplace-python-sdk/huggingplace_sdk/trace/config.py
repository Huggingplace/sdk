"""
Configuration for tracing functionality
"""

# Default base URL - declared once
DEFAULT_BASE_URL = "https://anvsj57nul.execute-api.ap-south-1.amazonaws.com"

"""
Default configuration for tracing
"""
DEFAULT_TRACE_CONFIG = {
    # Default base URL (will be overridden by HuggingPlace base_url)
    "base_url": DEFAULT_BASE_URL,
    
    # Batching configuration
    "batch_size": 10,
    "batch_timeout": 5000,  # 5 seconds

    # Retry configuration
    "max_retries": 3,
    "retry_delay": 1000,  # 1 second

    # HTTP timeouts
    "timeout": 10000,  # 10 seconds for single requests
    "batch_timeout_ms": 30000,  # 30 seconds for batch requests

    # Logging
    "silent": False,

    # Default headers
    "headers": {
        "Content-Type": "application/json"
    }
}


def get_trace_config(overrides: dict = None) -> dict:
    """
    Get trace configuration with optional overrides
    
    Args:
        overrides: Configuration overrides
        
    Returns:
        Merged configuration
    """
    if overrides is None:
        overrides = {}
    
    return {
        **DEFAULT_TRACE_CONFIG,
        **overrides
    }


def build_trace_endpoints(base_url: str) -> dict:
    """
    Build trace endpoints from base URL
    
    Args:
        base_url: Base URL for the API
        
    Returns:
        Trace endpoints
    """
    return {
        "trace_endpoint": f"{base_url}/api/traces",
        "batch_endpoint": f"{base_url}/api/traces/batch"
    }
