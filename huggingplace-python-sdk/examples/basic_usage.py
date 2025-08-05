"""
Basic usage examples for HuggingPlace SDK
"""

import asyncio
import os
from huggingplace_sdk import HuggingPlace, AuthenticationError, ValidationError, NetworkError


async def basic_logging():
    """Example 1: Basic logging"""
    try:
        # Initialize the SDK
        huggingplace = HuggingPlace({
            "api_key": "your-api-key-here",
            "org_id": "your-org-id-here",
            "mode": "prod"  # or "dev"
        })

        await huggingplace.log({
            "user_prompt": "What is the weather today?",
            "ai_response": "The weather is sunny with a temperature of 25°C.",
            "session_id": "session-123",
            "llm_model": "gpt-4o",
            "token_count": 150,
            "response_time": "0 min 2.50 sec",
            "metaData": {
                "likes": 1,
                "dislikes": 0,
                "custom_field": "value"
            },
            "user_meta_data": {
                "email": "user@example.com",
                "username": "john_doe",
                "org_name": "Example Corp"
            }
        })
        
        print("✅ Basic logging completed")
    except Exception as error:
        print(f"❌ Basic logging failed: {error}")


async def session_logging():
    """Example 2: Session-based logging"""
    try:
        huggingplace = HuggingPlace({
            "api_key": "your-api-key-here",
            "org_id": "your-org-id-here"
        })

        # Create a session for related interactions
        session = huggingplace.start_session("user-123", {
            "metaData": {
                "user_id": "user-123",
                "conversation_type": "support"
            },
            "user_meta_data": {
                "email": "user@example.com",
                "org_name": "Example Corp"
            }
        })

        # Log multiple interactions in the same session
        # session_id will automatically be set to 'user-123' from the session
        await session.log({
            "user_prompt": "I need help with my account",
            "ai_response": "I can help you with your account. What specific issue are you facing?",
            "llm_model": "gpt-4o"
        })

        await session.log({
            "user_prompt": "I can't log in",
            "ai_response": "Let me help you troubleshoot your login issue. Have you tried resetting your password?",
            "llm_model": "gpt-4o"
        })

        # You can also override the session_id if needed
        await session.log({
            "user_prompt": "What about my other account?",
            "ai_response": "I can help with your other account as well.",
            "session_id": "different-session-id",  # This will override the session default
            "llm_model": "gpt-4o"
        })

        print("✅ Session logging completed")
    except Exception as error:
        print(f"❌ Session logging failed: {error}")


async def step_logging():
    """Example 3: Step-by-step logging"""
    try:
        huggingplace = HuggingPlace({
            "api_key": "your-api-key-here",
            "org_id": "your-org-id-here"
        })

        # Log individual processing steps
        await huggingplace.log_step({
            "step_name": "data_processing",
            "status": "completed",
            "time_ms": 1800,
            "user_question": "Process the sales data",
            "prompt_response": "Data processed successfully. Found 1,245 sales records.",
            "llm_model": "gpt-4o",
            "token": 120,
            "response_time": "0 min 1.80 sec",
            "input_tokens": 40,
            "output_tokens": 80
        })

        await huggingplace.log_step({
            "step_name": "sql_generation",
            "status": "completed",
            "time_ms": 2100,
            "user_question": "Generate SQL query for monthly sales",
            "prompt_response": "SELECT DATE_TRUNC('month', sale_date) as month, COUNT(*) as sales_count FROM sales GROUP BY month ORDER BY month;",
            "llm_model": "gpt-4o",
            "token": 200,
            "response_time": "0 min 2.10 sec",
            "input_tokens": 60,
            "output_tokens": 140
        })

        print("✅ Step logging completed")
    except Exception as error:
        print(f"❌ Step logging failed: {error}")


async def automatic_timing():
    """Example 4: Automatic timing"""
    try:
        huggingplace = HuggingPlace({
            "api_key": "your-api-key-here",
            "org_id": "your-org-id-here"
        })

        # Simulate an LLM call
        async def mock_llm_call():
            # Simulate processing time
            await asyncio.sleep(1)
            return "The weather is sunny with a temperature of 25°C."

        # Log with automatic timing
        response = await huggingplace.log_with_timing(
            "What is the weather today?",
            mock_llm_call,
            {
                "session_id": "session-456",
                "llm_model": "gpt-4o",
                "metaData": {
                    "source": "weather_api",
                    "location": "New York"
                }
            }
        )

        print(f"✅ Automatic timing completed. Response: {response}")
    except Exception as error:
        print(f"❌ Automatic timing failed: {error}")


async def error_handling():
    """Example 5: Error handling"""
    try:
        # Test with invalid configuration
        invalid_huggingplace = HuggingPlace({
            # Missing required fields
        })
    except ValidationError as error:
        print(f"✅ Validation error caught: {error}")

    try:
        huggingplace = HuggingPlace({
            "api_key": "your-api-key-here",
            "org_id": "your-org-id-here"
        })
        
        # Test with invalid log options
        await huggingplace.log({
            # Missing required fields
        })
    except ValidationError as error:
        print(f"✅ Validation error caught: {error}")


async def configuration_management():
    """Example 6: Configuration management"""
    try:
        huggingplace = HuggingPlace({
            "api_key": "your-api-key-here",
            "org_id": "your-org-id-here"
        })

        # Get current configuration (without sensitive data)
        config = huggingplace.get_config()
        print("Current config:", config)

        # Update configuration
        huggingplace.update_config({
            "timeout": 15000,
            "mode": "dev"
        })

        print("✅ Configuration updated")
    except Exception as error:
        print(f"❌ Configuration management failed: {error}")


async def test_connection():
    """Example 7: Connection testing"""
    try:
        huggingplace = HuggingPlace({
            "api_key": "your-api-key-here",
            "org_id": "your-org-id-here"
        })

        is_connected = await huggingplace.test_connection()
        print(f"Connection test result: {'✅ Connected' if is_connected else '❌ Not connected'}")
    except Exception as error:
        print(f"❌ Connection test failed: {error}")


async def run_examples():
    """Run all examples"""
    print("🚀 Running HuggingPlace SDK Examples\n")

    print("1. Basic Logging:")
    await basic_logging()

    print("\n2. Session Logging:")
    await session_logging()

    print("\n3. Step Logging:")
    await step_logging()

    print("\n4. Automatic Timing:")
    await automatic_timing()

    print("\n5. Error Handling:")
    await error_handling()

    print("\n6. Configuration Management:")
    await configuration_management()

    print("\n7. Connection Testing:")
    await test_connection()

    print("\n✅ All examples completed!")


if __name__ == "__main__":
    asyncio.run(run_examples()) 