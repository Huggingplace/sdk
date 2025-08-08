"""
Send trace data to HuggingPlace backend
"""

import asyncio
import time
from typing import Dict, Any, List, Optional, Callable
import requests
from .config import DEFAULT_TRACE_CONFIG


def create_sender(config: Dict[str, Any] = None) -> Dict[str, Callable]:
    """
    Create a configured sender instance
    
    Args:
        config: Configuration object
        
    Returns:
        Sender instance with methods
    """
    if config is None:
        config = {}
    
    sender_config = {**DEFAULT_TRACE_CONFIG, **config}
    
    # Build endpoints from base_url
    base_url = sender_config.get("base_url", DEFAULT_TRACE_CONFIG["base_url"])
    trace_endpoint = f"{base_url}/api/traces"
    batch_endpoint = f"{base_url}/api/traces/batch"
    
    # Instance state
    trace_batch = []
    batch_timeout = None

    async def send_trace_with_retry(trace_data: Dict[str, Any], retries: int = 0) -> Optional[Dict[str, Any]]:
        """
        Send a single trace with retry logic
        
        Args:
            trace_data: Trace data to send
            retries: Current retry attempt
            
        Returns:
            Response data or None if failed
        """
        try:
            response = requests.post(
                trace_endpoint,
                json=trace_data,
                timeout=sender_config["timeout"] / 1000,  # Convert to seconds
                headers=sender_config["headers"]
            )
            
            if response.status_code == 201:
                if not sender_config["silent"]:
                    print(f"✅ Trace sent successfully: {response.json().get('traceId')}")
                return response.json()
            else:
                raise Exception(f"Unexpected status: {response.status_code}")
        except Exception as error:
            if not sender_config["silent"]:
                print(f"❌ Failed to send trace (attempt {retries + 1}): {str(error)}")
            
            if retries < sender_config["max_retries"]:
                # Exponential backoff
                delay = sender_config["retry_delay"] * (2 ** retries)
                if not sender_config["silent"]:
                    print(f"🔄 Retrying in {delay}ms...")
                
                await asyncio.sleep(delay / 1000)  # Convert to seconds
                return await send_trace_with_retry(trace_data, retries + 1)
            else:
                if not sender_config["silent"]:
                    print("❌ Max retries reached, dropping trace")
                return None

    async def send_batch_with_retry(traces: List[Dict[str, Any]], retries: int = 0) -> Optional[Dict[str, Any]]:
        """
        Send a batch of traces with retry logic
        
        Args:
            traces: Array of trace data
            retries: Current retry attempt
            
        Returns:
            Response data or None if failed
        """
        try:
            response = requests.post(
                batch_endpoint,
                json=traces,
                timeout=sender_config["batch_timeout_ms"] / 1000,  # Convert to seconds
                headers=sender_config["headers"]
            )
            
            if response.status_code == 201:
                if not sender_config["silent"]:
                    print(f"✅ Batch sent successfully: {response.json().get('count')} traces")
                return response.json()
            else:
                raise Exception(f"Unexpected status: {response.status_code}")
        except Exception as error:
            if not sender_config["silent"]:
                print(f"❌ Failed to send batch (attempt {retries + 1}): {str(error)}")
            
            if retries < sender_config["max_retries"]:
                delay = sender_config["retry_delay"] * (2 ** retries)
                if not sender_config["silent"]:
                    print(f"🔄 Retrying batch in {delay}ms...")
                
                await asyncio.sleep(delay / 1000)  # Convert to seconds
                return await send_batch_with_retry(traces, retries + 1)
            else:
                if not sender_config["silent"]:
                    print("❌ Max retries reached, dropping batch")
                return None

    def flush_batch():
        """Flush the current batch of traces"""
        nonlocal trace_batch
        if trace_batch:
            batch = trace_batch.copy()
            trace_batch.clear()
            
            asyncio.create_task(send_batch_with_retry(batch)).add_done_callback(
                lambda task: print(f"❌ Failed to flush batch: {task.exception()}") if task.exception() else None
            )

    async def send_trace(trace: Dict[str, Any]) -> None:
        """
        Send a trace (single or batched)
        
        Args:
            trace: Trace data to send
        """
        try:
            # Validate required fields
            if not all(key in trace for key in ["traceId", "spanId", "operation"]):
                if not sender_config["silent"]:
                    print("❌ Invalid trace data: missing required fields")
                return

            # Add to batch if batching is enabled
            if sender_config["batch_size"] > 1:
                trace_batch.append(trace)
                
                # Clear existing timeout
                nonlocal batch_timeout
                if batch_timeout:
                    batch_timeout.cancel()
                
                # Flush if batch is full
                if len(trace_batch) >= sender_config["batch_size"]:
                    flush_batch()
                else:
                    # Set timeout to flush remaining traces
                    batch_timeout = asyncio.create_task(
                        asyncio.sleep(sender_config["batch_timeout"] / 1000)
                    )
                    batch_timeout.add_done_callback(lambda _: flush_batch())
            else:
                # Send immediately if batching is disabled
                await send_trace_with_retry(trace)
        except Exception as error:
            if not sender_config["silent"]:
                print(f"❌ Error in send_trace: {str(error)}")

    return {
        "send_trace": send_trace,
        "send_trace_with_retry": send_trace_with_retry,
        "send_batch_with_retry": send_batch_with_retry,
        "flush_batch": flush_batch
    }


# Create default sender instance for backward compatibility
_default_sender = create_sender()


async def send_trace(trace: Dict[str, Any]) -> None:
    """
    Send a trace using the default sender (backward compatibility)
    
    Args:
        trace: Trace data to send
    """
    return await _default_sender["send_trace"](trace)
