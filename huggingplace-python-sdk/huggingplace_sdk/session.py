"""
Session class for managing related interactions
"""

from typing import Dict, Any, Optional
from .huggingplace import HuggingPlace


class Session:
    """
    Session class for managing related interactions.
    """
    
    def __init__(
        self, 
        huggingplace: HuggingPlace, 
        session_id: str, 
        options: Optional[Dict[str, Any]] = None
    ):
        """
        Create a new session.
        
        Args:
            huggingplace: HuggingPlace instance
            session_id: Session ID
            options: Session options
        """
        self.huggingplace = huggingplace
        self.session_id = session_id
        self.default_metadata = options.get("metadata", {}) if options else {}
        self.default_user_metadata = options.get("user_metadata", {}) if options else {}

    async def log(self, options: Dict[str, Any]) -> None:
        """
        Log an interaction with session defaults.
        
        Args:
            options: Log options
                - user_prompt: User prompt
                - response: AI response
                - session_id: Session ID (uses session default if not provided)
                - metadata: Additional metadata
                - user_metadata: Additional user metadata
        """
        # Merge session defaults with provided options
        merged_options = {
            **options,
            # Only set session_id if not provided by user
            "session_id": options.get("session_id") or self.session_id,
            "metadata": {
                **self.default_metadata,
                **options.get("metadata", {}),
            },
            "user_metadata": {
                **self.default_user_metadata,
                **options.get("user_metadata", {}),
            },
        }

        await self.huggingplace.log(merged_options)

    async def log_step(self, options: Dict[str, Any]) -> None:
        """
        Log an individual processing step.
        
        Args:
            options: Step options
                - type: Step type
                - user_question: User question for this step
                - prompt_response: Response for this step
                - llm_model: LLM model used
                - token: Token count
                - response_time: Response time
                - input_tokens: Input token count
                - output_tokens: Output token count
        """
        await self.huggingplace.log_step(options)

    def update_defaults(
        self, 
        metadata: Optional[Dict[str, Any]] = None, 
        user_metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Update session defaults.
        
        Args:
            metadata: New default metadata
            user_metadata: New default user metadata
        """
        if metadata:
            self.default_metadata = {**self.default_metadata, **metadata}
        if user_metadata:
            self.default_user_metadata = {**self.default_user_metadata, **user_metadata}

    def get_session_info(self) -> Dict[str, Any]:
        """
        Get current session information.
        
        Returns:
            Session information
        """
        return {
            "session_id": self.session_id,
            "default_metadata": self.default_metadata,
            "default_user_metadata": self.default_user_metadata,
        } 