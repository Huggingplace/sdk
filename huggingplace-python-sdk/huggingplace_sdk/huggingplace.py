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

# Import tracing functions
from .trace.trace_step import trace_step as base_trace_step
from .trace.trace_llm import trace_llm_with_evaluation as base_trace_llm
from .trace.trace_multi_step import trace_multi_step_flow as base_trace_multi_step_flow
from .trace.sender import create_sender
from .trace.config import DEFAULT_BASE_URL
from .trace.utils import generate_id


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
                - trace_batch_size: Trace batch size (default: 10)
                - trace_batch_timeout: Trace batch timeout in ms (default: 5000)
                - trace_max_retries: Max retries for trace requests (default: 3)
        """
        validate_config(config)

        self.config = {
            "mode": "prod",
            "timeout": 10000,
            "silent": False,
            "trace_batch_size": 10,
            "trace_batch_timeout": 5000,
            "trace_max_retries": 3,
            **config,
        }

        self.base_url = config.get("base_url") or DEFAULT_BASE_URL

        # Create session with default headers
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config['api_key']}",
        })
        self.session.timeout = self.config["timeout"] / 1000  # Convert to seconds

        # Create a configured sender instance for this HuggingPlace instance
        self.sender = create_sender({
            "base_url": self.base_url,
            "batch_size": self.config["trace_batch_size"],
            "batch_timeout": self.config["trace_batch_timeout"],
            "max_retries": self.config["trace_max_retries"],
            "timeout": self.config["timeout"],
            "silent": self.config["silent"],
            "headers": {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config['api_key']}",
            }
        })

    async def send_trace(self, trace: Dict[str, Any]) -> None:
        """
        Custom send_trace function that enriches trace data with HuggingPlace metadata
        
        Args:
            trace: Trace data to send
        """
        # Add org and mode from config
        enriched_trace = {
            **trace,
            "metadata": {
                **(trace.get("metadata", {})),
                "orgId": self.config["org_id"],
                "mode": self.config["mode"],
            }
        }

        # Use the configured sender
        return await self.sender["send_trace"](enriched_trace)

    async def trace_step(self, **kwargs) -> Any:
        """
        Trace a single step with detailed metadata
        
        Args:
            **kwargs: Tracing parameters (same as base_trace_step)
            
        Returns:
            Result of the function execution
        """
        return await base_trace_step(
            trace_id=kwargs.get("trace_id") or generate_id(),
            parent_span_id=kwargs.get("parent_span_id") or generate_id(),
            send_trace_func=self.send_trace,
            **kwargs
        )

    async def trace_llm(self, **kwargs) -> Any:
        """
        Trace an LLM call with evaluation data
        
        Args:
            **kwargs: Tracing parameters (same as base_trace_llm_with_evaluation)
            
        Returns:
            Result of the LLM function execution
        """
        return await base_trace_llm(
            trace_id=kwargs.get("trace_id") or generate_id(),
            parent_span_id=kwargs.get("parent_span_id") or generate_id(),
            send_trace_func=self.send_trace,
            **kwargs
        )

    async def trace_multi_step_flow(self, **kwargs) -> list:
        """
        Trace a multi-step workflow
        
        Args:
            **kwargs: Tracing parameters (same as base_trace_multi_step_flow)
            
        Returns:
            List of results from each step
        """
        return await base_trace_multi_step_flow(
            trace_id=kwargs.get("trace_id") or generate_id(),
            send_trace_func=self.send_trace,
            **kwargs
        )

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
                print(f"❌ Network error: {e}")
            raise NetworkError()
        except Exception as e:
            if not self.config["silent"]:
                print(f"❌ Error logging interaction: {e}")
            raise e

    async def log_step(self, options: Dict[str, Any]) -> None:
        """
        Log a single processing step.
        
        Args:
            options: Step log options
                - step_name: Name of the step (required)
                - step_data: Step data (required)
                - session_id: Session ID (optional)
                - metadata: Additional metadata (optional)
        """
        try:
            # Add org_id and mode from config
            payload = {
                **options,
                "org_id": self.config["org_id"],
                "mode": self.config["mode"],
            }

            if not self.config["silent"]:
                print("📤 Sending step payload to backend:", json.dumps(payload, indent=2))

            response = self.session.post(
                f"{self.base_url}/v2/chatgpt/store_step",
                json=payload
            )

            if response.status_code != 200:
                error_data = response.json() if response.content else {}
                message = error_data.get("message") or error_data.get("error") or "Unknown error"
                raise create_error_from_response(response.status_code, message)

            if not self.config["silent"]:
                print("✅ Step logged successfully")
                
        except requests.exceptions.RequestException as e:
            if not self.config["silent"]:
                print(f"❌ Network error: {e}")
            raise NetworkError()
        except Exception as e:
            if not self.config["silent"]:
                print(f"❌ Error logging step: {e}")
            raise e

    def start_session(
        self, 
        session_id: Optional[str] = None, 
        options: Optional[Dict[str, Any]] = None
    ) -> Session:
        """
        Start a new session for tracking conversations.
        
        Args:
            session_id: Custom session ID (auto-generated if not provided)
            options: Session options
            
        Returns:
            Session object
        """
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        if options is None:
            options = {}
        
        return Session(
            session_id=session_id,
            huggingplace=self,
            options=options
        )

    async def log_with_timing(
        self, 
        user_prompt: str, 
        response_generator: Callable, 
        options: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Log an interaction with automatic timing.
        
        Args:
            user_prompt: User prompt
            response_generator: Function that generates the response
            options: Additional options
            
        Returns:
            Generated response
        """
        if options is None:
            options = {}
        
        start_time = time.time()
        
        try:
            response = response_generator()
            response_time = time.time() - start_time
            
            await self.log({
                "user_prompt": user_prompt,
                "response": response,
                "response_time": f"0 min {response_time:.2f} sec",
                **options,
            })
            return response
            
        except Exception as error:
            if not self.config["silent"]:
                print(f"❌ Failed to log with timing: {error}")
            
            await self.log({
                "user_prompt": user_prompt,
                "response": f"Error: {str(error)}",
                "response_time": f"0 min {(time.time() - start_time):.2f} sec",
                "metadata": {
                    **(options.get("metadata", {})),
                    "error": True,
                    "error_message": str(error),
                },
                **options,
            })
            raise error

    def get_config(self) -> Dict[str, Any]:
        """
        Get current configuration.
        
        Returns:
            Current configuration
        """
        return self.config.copy()

    def update_config(self, new_config: Dict[str, Any]) -> None:
        """
        Update configuration.
        
        Args:
            new_config: New configuration values
        """
        self.config.update(new_config)
        
        # Update session headers if API key changed
        if "api_key" in new_config:
            self.session.headers.update({
                "Authorization": f"Bearer {self.config['api_key']}",
            })
        
        # Update session timeout if timeout changed
        if "timeout" in new_config:
            self.session.timeout = self.config["timeout"] / 1000
        
        # Re-create sender if tracing config changed
        if any(key in new_config for key in ["trace_batch_size", "trace_batch_timeout", "trace_max_retries", "silent"]):
            self.sender = create_sender({
                "base_url": self.base_url,
                "batch_size": self.config["trace_batch_size"],
                "batch_timeout": self.config["trace_batch_timeout"],
                "max_retries": self.config["trace_max_retries"],
                "timeout": self.config["timeout"],
                "silent": self.config["silent"],
                "headers": {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.config['api_key']}",
                }
            })

    async def test_connection(self) -> bool:
        """
        Test connection to HuggingPlace backend.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.status_code == 200
        except Exception:
            return False 