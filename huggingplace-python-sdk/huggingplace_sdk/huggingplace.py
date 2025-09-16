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
                - user_prompt: User prompt
                - ai_response: AI response (preferred over 'response')
                - response: AI response (alternative to 'ai_response')
                - user_uuid: User UUID
                - file_name: File name
                - session_id: Session ID
                - llm_model: LLM model used
                - llm_model2: Secondary LLM model
                - token_count: Token count
                - metaData: Additional metadata
                - user_roles: User roles array
                - org_uuid: Organization UUID
                - mapping_table: Database mapping table
                - step_data: Array of processing steps
                - response_time: Response time in milliseconds
                - message_id: Message ID
                - user_meta_data: User metadata (preferred over 'user_metadata')
                - user_metadata: User metadata (alternative to 'user_meta_data')
                - org_id: Organization ID
                - mode: Environment mode
        """
        try:
            validate_log_options(options)

            # Map response to ai_response if not provided (keep both)
            if "response" in options and "ai_response" not in options:
                options["ai_response"] = options["response"]

            # Map user_metadata to user_meta_data if not provided
            if "user_metadata" in options and "user_meta_data" not in options:
                options["user_meta_data"] = options.pop("user_metadata")

            # Send response_time as-is without any formatting

            # Add org_id and mode from config
            payload = {
                **options,
                "org_id": self.config["org_id"],
                "mode": self.config["mode"],
            }

            # if not self.config["silent"]:
            #     print("📤 Sending payload to backend:", json.dumps(payload, indent=2))

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
                - step_name: Step name
                - status: Step status
                - time_ms: Time in milliseconds
                - user_question: User question for this step
                - prompt_response: Response for this step
                - llm_model: LLM model used
                - token: Token count
                - response_time: Response time
                - input_tokens: Input token count
                - output_tokens: Output token count
        """
        # For individual steps, we create a minimal log entry
        await self.log({
            "user_prompt": options.get("user_question", ""),
            "ai_response": options.get("prompt_response", ""),
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
                "ai_response": response,
                "response_time": f"0 min {response_time:.2f} sec",  # Send as string format
                **options,
            })

            return response
        except Exception as error:
            # Log the error as well
            await self.log({
                "user_prompt": user_prompt,
                "ai_response": f"Error: {str(error)}",
                "response_time": f"0 min {(time.time() - start_time):.2f} sec",  # Send as string format
                "metaData": {
                    **options.get("metaData", {}),
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
                "ai_response": "test_response",
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