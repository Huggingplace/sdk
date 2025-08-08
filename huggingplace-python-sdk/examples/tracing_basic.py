"""
Basic tracing example for HuggingPlace Python SDK
"""

import asyncio
from huggingplace_sdk import HuggingPlace, generate_id


async def basic_tracing_example():
    """Example 1: Trace a simple function"""
    print('=== Basic Tracing Example ===')
    
    # Initialize the SDK with tracing configuration
    hp = HuggingPlace({
        'api_key': 'your-api-key',
        'org_id': 'your-org-id',
        'mode': 'dev',  # or 'prod'
        'silent': False,  # Set to True to disable console logs
        # Optional tracing configuration
        'trace_batch_size': 10,
        'trace_batch_timeout': 5000,
        'trace_max_retries': 3
    })
    
    # Example 1: Trace a simple function
    async def data_processing():
        # Simulate some work
        await asyncio.sleep(0.1)
        return {'processed': True, 'data': 'sample data'}
    
    result = await hp.trace_step(
        step_name='Data Processing',
        func=data_processing,
        user_metadata={'user_id': 'user-123', 'email': 'user@example.com'},
        org_data={'org_id': 'org-456', 'org_name': 'ExampleOrg'},
        custom_metadata={'app_version': '1.0.0', 'environment': 'development'},
        tags=['data-processing', 'example'],
        priority='high'
    )
    
    print('Tracing result:', result)


async def tracing_with_logging_example():
    """Example 2: Trace with logging"""
    print('\n=== Tracing with Logging Example ===')
    
    hp = HuggingPlace({
        'api_key': 'your-api-key',
        'org_id': 'your-org-id',
        'mode': 'dev'
    })
    
    # First, trace the function
    async def user_analysis():
        # Simulate user analysis
        await asyncio.sleep(0.2)
        return {
            'sentiment': 'positive',
            'confidence': 0.85,
            'keywords': ['happy', 'satisfied']
        }
    
    result = await hp.trace_step(
        step_name='User Analysis',
        func=user_analysis,
        user_metadata={'user_id': 'user-123'},
        org_data={'org_id': 'org-456'},
        custom_metadata={'analysis_type': 'sentiment'}
    )
    
    print('Analysis completed and logged')


async def tracing_error_example():
    """Example 3: Error handling in tracing"""
    print('\n=== Tracing Error Example ===')
    
    hp = HuggingPlace({
        'api_key': 'your-api-key',
        'org_id': 'your-org-id',
        'mode': 'dev'
    })
    
    try:
        async def risky_operation():
            # Simulate an error
            raise Exception('Something went wrong!')
        
        result = await hp.trace_step(
            step_name='Risky Operation',
            func=risky_operation,
            user_metadata={'user_id': 'user-123'},
            org_data={'org_id': 'org-456'}
        )
    except Exception as error:
        print('Error was caught and traced:', str(error))


async def run_examples():
    """Run all examples"""
    try:
        await basic_tracing_example()
        await tracing_with_logging_example()
        await tracing_error_example()
        
        print('\n=== All examples completed ===')
        print('Check your HuggingPlace backend for trace data!')
    except Exception as error:
        print('Example failed:', error)


if __name__ == "__main__":
    asyncio.run(run_examples())
