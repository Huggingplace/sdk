"""
Utility functions for tracing
"""

import time
import uuid
from typing import Optional


def generate_id() -> str:
    """
    Generate a unique ID for traces and spans
    
    Returns:
        Unique ID string
    """
    return str(uuid.uuid4())


def get_current_timestamp() -> int:
    """
    Get current timestamp in milliseconds
    
    Returns:
        Current timestamp in milliseconds
    """
    return int(time.time() * 1000)


def calculate_duration(start_time: int, end_time: Optional[int] = None) -> int:
    """
    Calculate duration between timestamps
    
    Args:
        start_time: Start timestamp in milliseconds
        end_time: End timestamp in milliseconds (uses current time if None)
        
    Returns:
        Duration in milliseconds
    """
    if end_time is None:
        end_time = get_current_timestamp()
    
    return end_time - start_time
