"""
Command-line interface for HuggingPlace SDK
"""

import asyncio
import json
import os
import sys
from typing import Dict, Any
from .huggingplace import HuggingPlace


def load_config() -> Dict[str, Any]:
    """Load configuration from environment variables."""
    return {
        "api_key": os.getenv("HUGGINGPLACE_API_KEY"),
        "org_id": os.getenv("HUGGINGPLACE_ORG_ID"),
        "mode": os.getenv("HUGGINGPLACE_MODE", "prod"),
        "base_url": os.getenv("HUGGINGPLACE_BASE_URL"),
        "timeout": int(os.getenv("HUGGINGPLACE_TIMEOUT", "10000")),
        "silent": os.getenv("HUGGINGPLACE_SILENT", "false").lower() == "true",
    }


async def log_interaction(config: Dict[str, Any], data: Dict[str, Any]) -> None:
    """Log an interaction using the SDK."""
    huggingplace = HuggingPlace(config)
    await huggingplace.log(data)
    print("✅ Interaction logged successfully")


async def test_connection(config: Dict[str, Any]) -> None:
    """Test connection to HuggingPlace API."""
    huggingplace = HuggingPlace(config)
    is_connected = await huggingplace.test_connection()
    if is_connected:
        print("✅ Connection successful")
    else:
        print("❌ Connection failed")
        sys.exit(1)


def print_help():
    """Print help information."""
    print("""
HuggingPlace SDK CLI

Usage:
    huggingplace log <json_data>     # Log an interaction
    huggingplace test                # Test connection
    huggingplace --help              # Show this help

Environment Variables:
    HUGGINGPLACE_API_KEY            # Your API key
    HUGGINGPLACE_ORG_ID             # Your organization ID
    HUGGINGPLACE_MODE               # Environment mode (prod/dev)
    HUGGINGPLACE_BASE_URL           # Custom base URL
    HUGGINGPLACE_TIMEOUT            # Request timeout in ms
    HUGGINGPLACE_SILENT             # Silent mode (true/false)

Examples:
    # Log an interaction
    echo '{"user_prompt": "Hello", "response": "Hi there!"}' | huggingplace log

    # Test connection
    huggingplace test
    """)


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2 or sys.argv[1] in ["--help", "-h"]:
        print_help()
        return

    command = sys.argv[1]
    config = load_config()

    # Validate required configuration
    if not config["api_key"]:
        print("❌ HUGGINGPLACE_API_KEY environment variable is required")
        sys.exit(1)
    
    if not config["org_id"]:
        print("❌ HUGGINGPLACE_ORG_ID environment variable is required")
        sys.exit(1)

    try:
        if command == "log":
            if len(sys.argv) < 3:
                print("❌ JSON data is required for log command")
                sys.exit(1)
            
            # Read JSON data from command line or stdin
            if sys.argv[2] == "-":
                data_str = sys.stdin.read()
            else:
                data_str = sys.argv[2]
            
            try:
                data = json.loads(data_str)
            except json.JSONDecodeError as e:
                print(f"❌ Invalid JSON: {e}")
                sys.exit(1)
            
            asyncio.run(log_interaction(config, data))
            
        elif command == "test":
            asyncio.run(test_connection(config))
            
        else:
            print(f"❌ Unknown command: {command}")
            print_help()
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 