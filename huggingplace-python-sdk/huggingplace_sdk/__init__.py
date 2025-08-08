"""
HuggingPlace SDK for Python

A comprehensive SDK for logging and tracing LLM interactions with HuggingPlace.
"""

from .huggingplace import HuggingPlace
from .session import Session
from .errors import (
    HuggingPlaceSDKError,
    AuthenticationError,
    ValidationError,
    NetworkError,
    RateLimitError,
    ServerError,
    create_error_from_response,
)
from .validation import (
    validate_config,
    validate_log_options,
)

# Import tracing utilities
from .trace.utils import generate_id, get_current_timestamp, calculate_duration

__version__ = "1.0.1"
__author__ = "HuggingPlace Team"
__email__ = "team@huggingplace.com"

__all__ = [
    "HuggingPlace",
    "Session",
    "HuggingPlaceSDKError",
    "AuthenticationError",
    "ValidationError",
    "NetworkError",
    "RateLimitError",
    "ServerError",
    "create_error_from_response",
    "validate_config",
    "validate_log_options",
    # Tracing utilities
    "generate_id",
    "get_current_timestamp",
    "calculate_duration",
] 