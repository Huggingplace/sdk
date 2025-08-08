"""
LLM tracing example for HuggingPlace Python SDK
"""

import asyncio
import os
from huggingplace_sdk import HuggingPlace


async def llm_tracing_example():
    """Example: Trace an LLM call"""
    print('=== LLM Tracing Example ===')
    
    # Initialize the SDK
    hp = HuggingPlace({
        'api_key': 'your-api-key',
        'org_id': 'your-org-id',
        'mode': 'dev',
        'silent': False
    })
    
    # Example LLM function that returns rich response data
    async def mock_openai_call(prompt, **kwargs):
        # Simulate OpenAI API call
        await asyncio.sleep(0.5)  # Simulate API delay
        
        # Return rich response object (like OpenAI would)
        return {
            'responseText': f'This is a response to: {prompt}',
            'rawResponse': {
                'id': 'chatcmpl-123',
                'object': 'chat.completion',
                'created': 1234567890,
                'model': 'gpt-4',
                'choices': [{
                    'index': 0,
                    'message': {
                        'role': 'assistant',
                        'content': f'This is a response to: {prompt}'
                    },
                    'finish_reason': 'stop'
                }],
                'usage': {
                    'prompt_tokens': 10,
                    'completion_tokens': 20,
                    'total_tokens': 30
                }
            },
            'tokens': {
                'input': 10,
                'output': 20,
                'total': 30
            },
            'finishReason': 'stop',
            'model': 'gpt-4',
            'provider': 'openai'
        }
    
    # Trace the LLM call
    result = await hp.trace_llm(
        step_name='OpenAI Chat Completion',
        llm_func=mock_openai_call,
        prompt='What is the weather like today?',
        user_metadata={'user_id': 'user-123'},
        org_data={'org_id': 'org-456'},
        llm_metadata={
            'provider': 'openai',
            'model': 'gpt-4',
            'temperature': 0.7,
            'maxTokens': 100,
            'topP': 1.0,
            'frequencyPenalty': 0.0,
            'presencePenalty': 0.0
        },
        custom_metadata={'session_id': 'session-789'},
        tags=['llm', 'openai', 'chat-completion']
    )
    
    print('LLM tracing result:', result)


async def llm_with_evaluation_example():
    """Example: Trace LLM with evaluation data"""
    print('\n=== LLM with Evaluation Example ===')
    
    hp = HuggingPlace({
        'api_key': 'your-api-key',
        'org_id': 'your-org-id',
        'mode': 'dev'
    })
    
    async def llm_with_evaluation(prompt, **kwargs):
        # Simulate LLM call with evaluation
        await asyncio.sleep(0.3)
        
        response_text = f'Response to: {prompt}'
        
        # Simulate evaluation metrics
        evaluation = {
            'relevance_score': 0.85,
            'fluency_score': 0.92,
            'coherence_score': 0.88,
            'overall_score': 0.88
        }
        
        return {
            'responseText': response_text,
            'rawResponse': {
                'choices': [{'message': {'content': response_text}}],
                'usage': {'total_tokens': 25}
            },
            'tokens': {'total': 25},
            'evaluation': evaluation,
            'model': 'gpt-4',
            'provider': 'openai'
        }
    
    result = await hp.trace_llm(
        step_name='LLM with Evaluation',
        llm_func=llm_with_evaluation,
        prompt='Explain quantum computing in simple terms',
        user_metadata={'user_id': 'user-123'},
        org_data={'org_id': 'org-456'},
        llm_metadata={
            'provider': 'openai',
            'model': 'gpt-4',
            'temperature': 0.5
        },
        custom_metadata={'evaluation_enabled': True},
        tags=['llm', 'evaluation', 'quantum']
    )
    
    print('LLM with evaluation result:', result)


async def run_examples():
    """Run all LLM examples"""
    try:
        await llm_tracing_example()
        await llm_with_evaluation_example()
        
        print('\n=== All LLM examples completed ===')
        print('Check your HuggingPlace backend for LLM trace data!')
    except Exception as error:
        print('LLM example failed:', error)


if __name__ == "__main__":
    asyncio.run(run_examples())
