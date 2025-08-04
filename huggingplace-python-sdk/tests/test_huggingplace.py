"""
Tests for HuggingPlace SDK
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from huggingplace_sdk import (
    HuggingPlace,
    Session,
    HuggingPlaceSDKError,
    AuthenticationError,
    ValidationError,
    NetworkError,
    RateLimitError,
    ServerError,
    create_error_from_response,
)


class TestHuggingPlace:
    """Test cases for HuggingPlace class."""

    def test_init_valid_config(self):
        """Test initialization with valid configuration."""
        config = {
            "api_key": "test-api-key",
            "org_id": "test-org-id",
            "mode": "prod",
            "timeout": 5000,
            "silent": True,
        }
        
        huggingplace = HuggingPlace(config)
        assert huggingplace.config["api_key"] == "test-api-key"
        assert huggingplace.config["org_id"] == "test-org-id"
        assert huggingplace.config["mode"] == "prod"
        assert huggingplace.config["timeout"] == 5000
        assert huggingplace.config["silent"] is True

    def test_init_invalid_config_missing_api_key(self):
        """Test initialization with missing API key."""
        config = {"org_id": "test-org-id"}
        
        with pytest.raises(ValidationError, match="API key is required"):
            HuggingPlace(config)

    def test_init_invalid_config_missing_org_id(self):
        """Test initialization with missing organization ID."""
        config = {"api_key": "test-api-key"}
        
        with pytest.raises(ValidationError, match="Organization ID is required"):
            HuggingPlace(config)

    def test_init_invalid_config_invalid_timeout(self):
        """Test initialization with invalid timeout."""
        config = {
            "api_key": "test-api-key",
            "org_id": "test-org-id",
            "timeout": -1,
        }
        
        with pytest.raises(ValidationError, match="Timeout must be a positive number"):
            HuggingPlace(config)

    def test_init_invalid_config_invalid_mode(self):
        """Test initialization with invalid mode."""
        config = {
            "api_key": "test-api-key",
            "org_id": "test-org-id",
            "mode": "invalid",
        }
        
        with pytest.raises(ValidationError, match='Mode must be either "prod" or "dev"'):
            HuggingPlace(config)

    @pytest.mark.asyncio
    async def test_log_valid_options(self):
        """Test logging with valid options."""
        config = {
            "api_key": "test-api-key",
            "org_id": "test-org-id",
            "silent": True,
        }
        
        huggingplace = HuggingPlace(config)
        
        # Mock the session
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Success"}
        mock_response.content = b'{"message": "Success"}'
        
        with patch.object(huggingplace.session, 'post', return_value=mock_response):
            await huggingplace.log({
                "user_prompt": "Test prompt",
                "response": "Test response",
            })

    @pytest.mark.asyncio
    async def test_log_invalid_options_missing_user_prompt(self):
        """Test logging with missing user prompt."""
        config = {
            "api_key": "test-api-key",
            "org_id": "test-org-id",
        }
        
        huggingplace = HuggingPlace(config)
        
        with pytest.raises(ValidationError, match="User prompt is required"):
            await huggingplace.log({
                "response": "Test response",
            })

    @pytest.mark.asyncio
    async def test_log_invalid_options_missing_response(self):
        """Test logging with missing response."""
        config = {
            "api_key": "test-api-key",
            "org_id": "test-org-id",
        }
        
        huggingplace = HuggingPlace(config)
        
        with pytest.raises(ValidationError, match="Response is required"):
            await huggingplace.log({
                "user_prompt": "Test prompt",
            })

    @pytest.mark.asyncio
    async def test_log_network_error(self):
        """Test logging with network error."""
        config = {
            "api_key": "test-api-key",
            "org_id": "test-org-id",
            "silent": True,
        }
        
        huggingplace = HuggingPlace(config)
        
        with patch.object(huggingplace.session, 'post', side_effect=Exception("Network error")):
            with pytest.raises(NetworkError):
                await huggingplace.log({
                    "user_prompt": "Test prompt",
                    "response": "Test response",
                })

    def test_start_session(self):
        """Test starting a session."""
        config = {
            "api_key": "test-api-key",
            "org_id": "test-org-id",
        }
        
        huggingplace = HuggingPlace(config)
        session = huggingplace.start_session("test-session-id")
        
        assert isinstance(session, Session)
        assert session.session_id == "test-session-id"
        assert session.huggingplace == huggingplace

    def test_get_config(self):
        """Test getting configuration without sensitive data."""
        config = {
            "api_key": "test-api-key",
            "org_id": "test-org-id",
            "mode": "prod",
            "timeout": 10000,
        }
        
        huggingplace = HuggingPlace(config)
        safe_config = huggingplace.get_config()
        
        assert "api_key" not in safe_config
        assert safe_config["org_id"] == "test-org-id"
        assert safe_config["mode"] == "prod"
        assert safe_config["timeout"] == 10000

    def test_update_config(self):
        """Test updating configuration."""
        config = {
            "api_key": "test-api-key",
            "org_id": "test-org-id",
            "mode": "prod",
            "timeout": 10000,
        }
        
        huggingplace = HuggingPlace(config)
        huggingplace.update_config({
            "timeout": 15000,
            "mode": "dev",
        })
        
        assert huggingplace.config["timeout"] == 15000
        assert huggingplace.config["mode"] == "dev"

    @pytest.mark.asyncio
    async def test_test_connection_success(self):
        """Test connection test with success."""
        config = {
            "api_key": "test-api-key",
            "org_id": "test-org-id",
            "silent": True,
        }
        
        huggingplace = HuggingPlace(config)
        
        mock_response = Mock()
        mock_response.status_code = 200
        
        with patch.object(huggingplace.session, 'post', return_value=mock_response):
            result = await huggingplace.test_connection()
            assert result is True

    @pytest.mark.asyncio
    async def test_test_connection_failure(self):
        """Test connection test with failure."""
        config = {
            "api_key": "test-api-key",
            "org_id": "test-org-id",
            "silent": True,
        }
        
        huggingplace = HuggingPlace(config)
        
        with patch.object(huggingplace.session, 'post', side_effect=Exception("Connection failed")):
            result = await huggingplace.test_connection()
            assert result is False


class TestSession:
    """Test cases for Session class."""

    def test_init(self):
        """Test session initialization."""
        huggingplace = HuggingPlace({
            "api_key": "test-api-key",
            "org_id": "test-org-id",
        })
        
        session = Session(huggingplace, "test-session-id", {
            "metadata": {"test": "value"},
            "user_metadata": {"user": "data"},
        })
        
        assert session.session_id == "test-session-id"
        assert session.huggingplace == huggingplace
        assert session.default_metadata == {"test": "value"}
        assert session.default_user_metadata == {"user": "data"}

    @pytest.mark.asyncio
    async def test_log(self):
        """Test session logging."""
        huggingplace = HuggingPlace({
            "api_key": "test-api-key",
            "org_id": "test-org-id",
        })
        
        session = Session(huggingplace, "test-session-id", {
            "metadata": {"default": "value"},
            "user_metadata": {"default_user": "data"},
        })
        
        with patch.object(huggingplace, 'log') as mock_log:
            await session.log({
                "user_prompt": "Test prompt",
                "response": "Test response",
                "metadata": {"custom": "value"},
            })
            
            # Verify that the log was called with merged options
            mock_log.assert_called_once()
            call_args = mock_log.call_args[0][0]
            assert call_args["session_id"] == "test-session-id"
            assert call_args["metadata"]["default"] == "value"
            assert call_args["metadata"]["custom"] == "value"
            assert call_args["user_metadata"]["default_user"] == "data"

    def test_update_defaults(self):
        """Test updating session defaults."""
        huggingplace = HuggingPlace({
            "api_key": "test-api-key",
            "org_id": "test-org-id",
        })
        
        session = Session(huggingplace, "test-session-id")
        session.update_defaults(
            metadata={"new": "metadata"},
            user_metadata={"new_user": "data"}
        )
        
        assert session.default_metadata == {"new": "metadata"}
        assert session.default_user_metadata == {"new_user": "data"}

    def test_get_session_info(self):
        """Test getting session information."""
        huggingplace = HuggingPlace({
            "api_key": "test-api-key",
            "org_id": "test-org-id",
        })
        
        session = Session(huggingplace, "test-session-id", {
            "metadata": {"test": "value"},
            "user_metadata": {"user": "data"},
        })
        
        info = session.get_session_info()
        assert info["session_id"] == "test-session-id"
        assert info["default_metadata"] == {"test": "value"}
        assert info["default_user_metadata"] == {"user": "data"}


class TestErrors:
    """Test cases for error classes."""

    def test_huggingplace_sdk_error(self):
        """Test HuggingPlaceSDKError."""
        error = HuggingPlaceSDKError("Test error")
        assert str(error) == "Test error"
        assert error.name == "HuggingPlaceSDKError"

    def test_authentication_error(self):
        """Test AuthenticationError."""
        error = AuthenticationError("Auth failed")
        assert str(error) == "Auth failed"
        assert error.name == "AuthenticationError"

    def test_validation_error(self):
        """Test ValidationError."""
        error = ValidationError("Validation failed")
        assert str(error) == "Validation failed"
        assert error.name == "ValidationError"

    def test_network_error(self):
        """Test NetworkError."""
        error = NetworkError("Network failed")
        assert str(error) == "Network failed"
        assert error.name == "NetworkError"

    def test_rate_limit_error(self):
        """Test RateLimitError."""
        error = RateLimitError("Rate limit exceeded")
        assert str(error) == "Rate limit exceeded"
        assert error.name == "RateLimitError"

    def test_server_error(self):
        """Test ServerError."""
        error = ServerError("Server error")
        assert str(error) == "Server error"
        assert error.name == "ServerError"

    def test_create_error_from_response(self):
        """Test create_error_from_response function."""
        # Test authentication error
        error = create_error_from_response(401, "Unauthorized")
        assert isinstance(error, AuthenticationError)
        assert str(error) == "Unauthorized"

        # Test validation error
        error = create_error_from_response(400, "Bad request")
        assert isinstance(error, ValidationError)
        assert str(error) == "Bad request"

        # Test rate limit error
        error = create_error_from_response(429, "Too many requests")
        assert isinstance(error, RateLimitError)
        assert str(error) == "Too many requests"

        # Test server error
        error = create_error_from_response(500, "Internal server error")
        assert isinstance(error, ServerError)
        assert str(error) == "Internal server error"

        # Test unknown error
        error = create_error_from_response(418, "I'm a teapot")
        assert isinstance(error, HuggingPlaceSDKError)
        assert str(error) == "I'm a teapot" 