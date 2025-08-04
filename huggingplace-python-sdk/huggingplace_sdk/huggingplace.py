"""
Main HuggingPlace SDK class
"""

import json
import time
import uuid
from typing import Dict, Any, Optional, Callable, Union
import requests
from .validation import validate_config, validate_log_options
from .errors import AuthenticationError, NetworkError, create_error_from_response
from .session import Session


class HuggingPlace:
    """
    Main HuggingPlace SDK class
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Create a new HuggingPlace instance.
        
        Args:
            config: Configuration object
                - api_key: API key for authentication
                - org_id: Organization ID
                - base_url: Base URL for API (optional)
                - mode: Environment mode (prod/dev) (optional)
                - timeout: Request timeout in milliseconds (optional)
                - silent: Silent mode (no console logs) (optional)
        """
        validate_config(config)

        self.config = {
            "mode": "prod",
            "timeout": 10000,
            "silent": False,
            **config,
        }

        self.base_url = config.get("base_url") or "https://anvsj57nul.execute-api.ap-south-1.amazonaws.com"

        # Create session with default headers
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config['api_key']}",
        })
        self.session.timeout = self.config["timeout"] / 1000  # Convert to seconds

    async def log(self, options: Dict[str, Any]) -> None:
        """
        Log a complete interaction with HuggingPlace.
        
        Args:
            options: Log options
                - user_prompt: User prompt (required)
                - response: AI response (required)
                - session_id: Session ID (optional)
                - llm_model: LLM model used (optional)
                - token_count: Token count (optional)
                - response_time: Response time in seconds (optional)
                - metadata: Additional metadata (optional)
                - user_metadata: User metadata (optional)
                - step_data: Array of processing steps (optional)
        """
        try:
            validate_log_options(options)

            # Add org_id and mode from config
            payload = {
                **options,
                "org_id": self.config["org_id"],
                "mode": self.config["mode"],
            }

            if not self.config["silent"]:
                print("📤 Sending payload to backend:", json.dumps(payload, indent=2))

            response = self.session.post(
                f"{self.base_url}/v2/chatgpt/store_generated_response",
                json=payload
            )
            
            if not self.config["silent"]:
                print("📥 Response status:", response.status_code)
                print("📥 Response data:", response.json())

            if response.status_code != 200:
                error_data = response.json() if response.content else {}
                message = error_data.get("message") or error_data.get("error") or "Unknown error"
                raise create_error_from_response(response.status_code, message)

            success_message = response.json().get("message", "Successfully logged interaction")
            if not self.config["silent"]:
                print(f"✅ Logged interaction to HuggingPlace: {success_message}")
                
        except requests.exceptions.RequestException as e:
            if not self.config["silent"]:
                print("❌ Failed to log interaction to HuggingPlace:", str(e))
            raise NetworkError(f"Network error: {str(e)}")
        except Exception as e:
            if not self.config["silent"]:
                print("❌ Failed to log interaction to HuggingPlace:", str(e))
            raise

    async def log_step(self, options: Dict[str, Any]) -> None:
        """
        Log individual processing steps.
        
        Args:
            options: Step options
                - type: Step type (required)
                - user_question: User question for this step (required)
                - prompt_response: Response for this step (required)
                - llm_model: LLM model used (optional)
                - token: Token count (optional)
                - response_time: Response time (optional)
                - input_tokens: Input token count (optional)
                - output_tokens: Output token count (optional)
        """
        # For individual steps, we create a minimal log entry
        await self.log({
            "user_prompt": options["user_question"],
            "response": options["prompt_response"],
            "llm_model": options.get("llm_model"),
            "token_count": options.get("token"),
            "response_time": options.get("response_time"),
            "step_data": [options],
        })

    def start_session(
        self, 
        session_id: Optional[str] = None, 
        options: Optional[Dict[str, Any]] = None
    ) -> Session:
        """
        Start a new session for tracking multiple interactions.
        
        Args:
            session_id: Session ID (auto-generated if not provided)
            options: Session options
                - metadata: Default metadata for the session
                - user_metadata: Default user metadata for the session
                
        Returns:
            Session instance
        """
        session_id = session_id or str(uuid.uuid4())
        return Session(self, session_id, options or {})

    async def log_with_timing(
        self, 
        user_prompt: str, 
        response_generator: Callable, 
        options: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Log with automatic timing.
        
        Args:
            user_prompt: User prompt
            response_generator: Function that generates the response
            options: Additional options
            
        Returns:
            The generated response
        """
        start_time = time.time()
        options = options or {}

        try:
            response = await response_generator()
            response_time = time.time() - start_time

            await self.log({
                "user_prompt": user_prompt,
                "response": response,
                "response_time": response_time,
                **options,
            })

            return response
        except Exception as error:
            # Log the error as well
            await self.log({
                "user_prompt": user_prompt,
                "response": f"Error: {str(error)}",
                "response_time": time.time() - start_time,
                "metadata": {
                    **options.get("metadata", {}),
                    "error": True,
                    "error_message": str(error),
                },
                **options,
            })

            raise

    def get_config(self) -> Dict[str, Any]:
        """
        Get current configuration (without sensitive data).
        
        Returns:
            Safe configuration object
        """
        safe_config = self.config.copy()
        safe_config.pop("api_key", None)
        return safe_config

    def update_config(self, new_config: Dict[str, Any]) -> None:
        """
        Update configuration.
        
        Args:
            new_config: New configuration options
        """
        updated_config = {**self.config, **new_config}
        validate_config(updated_config)

        self.config = updated_config

        # Update session with new config
        self.session.headers["Authorization"] = f"Bearer {self.config['api_key']}"
        self.session.timeout = self.config["timeout"] / 1000

    async def test_connection(self) -> bool:
        """
        Test connection to HuggingPlace API.
        
        Returns:
            True if connection successful
        """
        try:
            # Try to make a minimal request to test the connection
            test_payload = {
                "user_prompt": "connection_test",
                "response": "test_response",
                "org_id": self.config["org_id"],
                "mode": self.config["mode"]
            }
            
            response = self.session.post(
                f"{self.base_url}/v2/chatgpt/store_generated_response",
                json=test_payload
            )
            return response.status_code == 200
        except Exception as e:
            if not self.config["silent"]:
                print("Connection test failed:", str(e))
            return False 