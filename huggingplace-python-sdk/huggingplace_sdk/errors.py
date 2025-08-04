"""
Custom error classes for HuggingPlace SDK
"""


class HuggingPlaceSDKError(Exception):
    """Base exception class for HuggingPlace SDK errors."""
    
    def __init__(self, message: str = "HuggingPlace SDK error occurred"):
        super().__init__(message)
        self.name = "HuggingPlaceSDKError"


class AuthenticationError(HuggingPlaceSDKError):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message)
        self.name = "AuthenticationError"


class ValidationError(HuggingPlaceSDKError):
    """Raised when validation fails."""
    
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message)
        self.name = "ValidationError"


class NetworkError(HuggingPlaceSDKError):
    """Raised when network errors occur."""
    
    def __init__(self, message: str = "Network error occurred"):
        super().__init__(message)
        self.name = "NetworkError"


class RateLimitError(HuggingPlaceSDKError):
    """Raised when rate limits are exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message)
        self.name = "RateLimitError"


class ServerError(HuggingPlaceSDKError):
    """Raised when server errors occur."""
    
    def __init__(self, message: str = "Server error occurred"):
        super().__init__(message)
        self.name = "ServerError"


def create_error_from_response(status: int, message: str) -> HuggingPlaceSDKError:
    """
    Create appropriate error from HTTP response.
    
    Args:
        status: HTTP status code
        message: Error message
        
    Returns:
        Appropriate error instance
    """
    if status == 401:
        return AuthenticationError(message)
    elif status == 400:
        return ValidationError(message)
    elif status == 429:
        return RateLimitError(message)
    elif status in [500, 502, 503, 504]:
        return ServerError(message)
    else:
        return HuggingPlaceSDKError(message) 