"""
Validation functions for HuggingPlace SDK
"""

from typing import Dict, Any, Union, Tuple
from .errors import ValidationError





def validate_config(config: Dict[str, Any]) -> None:
    """
    Validate SDK configuration.
    
    Args:
        config: Configuration object
        
    Raises:
        ValidationError: If configuration is invalid
    """
    if not config:
        raise ValidationError("Configuration is required")

    if not config.get("api_key"):
        raise ValidationError("API key is required")

    if not config.get("org_id"):
        raise ValidationError("Organization ID is required")

    timeout = config.get("timeout")
    if timeout is not None and (not isinstance(timeout, (int, float)) or timeout <= 0):
        raise ValidationError("Timeout must be a positive number")

    mode = config.get("mode")
    if mode and mode not in ["prod", "dev"]:
        raise ValidationError('Mode must be either "prod" or "dev"')


def validate_log_options(options: Dict[str, Any]) -> None:
    """
    Validate log options.
    
    Args:
        options: Log options
        
    Raises:
        ValidationError: If options are invalid
    """
    if not options:
        raise ValidationError("Log options are required")

    # Only validate data types, not presence
    token_count = options.get("token_count")
    if token_count is not None and (not isinstance(token_count, (int, float)) or token_count < 0):
        raise ValidationError("Token count must be a non-negative number")

    # No validation for response_time - accept any format
    pass


def validate_step_data(step_data: Dict[str, Any]) -> None:
    """
    Validate step data.
    
    Args:
        step_data: Step data object
        
    Raises:
        ValidationError: If step data is invalid
    """
    if not step_data:
        raise ValidationError("Step data is required")

    if not step_data.get("type"):
        raise ValidationError("Step type is required")

    if not step_data.get("user_question"):
        raise ValidationError("User question is required for step")

    if not step_data.get("prompt_response"):
        raise ValidationError("Prompt response is required for step")

    token = step_data.get("token")
    if token is not None and (not isinstance(token, (int, float)) or token < 0):
        raise ValidationError("Step token count must be a non-negative number")

    # No validation for step response_time - accept any format
    pass 