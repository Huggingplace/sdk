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
    validate_step_data,
)

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
    "validate_step_data",
] 