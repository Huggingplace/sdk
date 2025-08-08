"""
Multi-step workflow tracing example for HuggingPlace Python SDK
"""

import asyncio
from huggingplace_sdk import HuggingPlace


async def multi_step_workflow_example():
    """Example: Trace a multi-step workflow"""
    print('=== Multi-Step Workflow Example ===')
    
    # Initialize the SDK
    hp = HuggingPlace({
        'api_key': 'your-api-key',
        'org_id': 'your-org-id',
        'mode': 'dev',
        'silent': False
    })
    
    # Step 1: Data preprocessing
    async def preprocess_data(previous_results=None, **kwargs):
        print("Step 1: Preprocessing data...")
        await asyncio.sleep(0.1)
        return {
            'raw_data': 'sample data',
            'processed': True,
            'step': 'preprocessing'
        }
    
    # Step 2: Feature extraction
    async def extract_features(previous_results=None, **kwargs):
        print("Step 2: Extracting features...")
        await asyncio.sleep(0.2)
        
        # Use data from previous step
        preprocess_result = previous_results[0] if previous_results else {}
        
        return {
            'features': ['feature1', 'feature2', 'feature3'],
            'feature_count': 3,
            'input_data': preprocess_result,
            'step': 'feature_extraction'
        }
    
    # Step 3: LLM call
    async def llm_analysis(previous_results=None, **kwargs):
        print("Step 3: Running LLM analysis...")
        await asyncio.sleep(0.3)
        
        # Use features from previous step
        feature_result = previous_results[1] if len(previous_results) > 1 else {}
        
        return {
            'responseText': f'Analysis of {feature_result.get("feature_count", 0)} features',
            'rawResponse': {
                'choices': [{'message': {'content': 'Analysis complete'}}],
                'usage': {'total_tokens': 15}
            },
            'tokens': {'total': 15},
            'model': 'gpt-4',
            'provider': 'openai',
            'step': 'llm_analysis'
        }
    
    # Step 4: Post-processing
    async def post_process(previous_results=None, **kwargs):
        print("Step 4: Post-processing results...")
        await asyncio.sleep(0.1)
        
        # Use LLM result from previous step
        llm_result = previous_results[2] if len(previous_results) > 2 else {}
        
        return {
            'final_result': 'Analysis completed successfully',
            'llm_response': llm_result.get('responseText', ''),
            'step': 'post_processing'
        }
    
    # Step 5: Validation
    async def validate_results(previous_results=None, **kwargs):
        print("Step 5: Validating results...")
        await asyncio.sleep(0.1)
        
        return {
            'validation_passed': True,
            'confidence_score': 0.95,
            'step': 'validation'
        }
    
    # Step 6: Final output
    async def generate_final_output(previous_results=None, **kwargs):
        print("Step 6: Generating final output...")
        await asyncio.sleep(0.1)
        
        # Use all previous results
        validation_result = previous_results[4] if len(previous_results) > 4 else {}
        
        return {
            'final_output': 'Workflow completed successfully!',
            'validation': validation_result,
            'step': 'final_output'
        }
    
    # Define the workflow steps
    steps = [
        {
            'stepName': 'Data Preprocessing',
            'func': preprocess_data,
            'tags': ['preprocessing', 'data'],
            'priority': 'high'
        },
        {
            'stepName': 'Feature Extraction',
            'func': extract_features,
            'tags': ['features', 'ml'],
            'priority': 'high'
        },
        {
            'stepName': 'LLM Analysis',
            'func': llm_analysis,
            'tags': ['llm', 'analysis'],
            'priority': 'high',
            'llm_metadata': {
                'provider': 'openai',
                'model': 'gpt-4',
                'temperature': 0.7
            }
        },
        {
            'stepName': 'Post Processing',
            'func': post_process,
            'tags': ['post-processing'],
            'priority': 'medium'
        },
        {
            'stepName': 'Validation',
            'func': validate_results,
            'tags': ['validation', 'quality'],
            'priority': 'high'
        },
        {
            'stepName': 'Final Output',
            'func': generate_final_output,
            'tags': ['output', 'final'],
            'priority': 'medium'
        }
    ]
    
    # Execute the multi-step workflow
    results = await hp.trace_multi_step_flow(
        flow_name='Complete Analysis Workflow',
        steps=steps,
        user_metadata={'user_id': 'user-123'},
        org_data={'org_id': 'org-456'},
        custom_metadata={'workflow_type': 'analysis', 'version': '1.0'},
        tags=['workflow', 'analysis', 'complete'],
        priority='high'
    )
    
    print('\nWorkflow results:')
    for i, result in enumerate(results):
        print(f'Step {i+1}: {result}')


async def error_handling_workflow_example():
    """Example: Multi-step workflow with error handling"""
    print('\n=== Error Handling Workflow Example ===')
    
    hp = HuggingPlace({
        'api_key': 'your-api-key',
        'org_id': 'your-org-id',
        'mode': 'dev'
    })
    
    # Step 1: Normal step
    async def step1(previous_results=None, **kwargs):
        await asyncio.sleep(0.1)
        return {'step': 1, 'status': 'success'}
    
    # Step 2: Step that might fail
    async def step2(previous_results=None, **kwargs):
        await asyncio.sleep(0.1)
        # Simulate a failure
        raise Exception('Step 2 failed!')
    
    # Step 3: Recovery step
    async def step3(previous_results=None, **kwargs):
        await asyncio.sleep(0.1)
        return {'step': 3, 'status': 'recovery', 'error_handled': True}
    
    steps = [
        {
            'stepName': 'Step 1',
            'func': step1,
            'tags': ['normal']
        },
        {
            'stepName': 'Step 2 (Fails)',
            'func': step2,
            'tags': ['error'],
            'continue_on_error': True  # Continue even if this step fails
        },
        {
            'stepName': 'Step 3 (Recovery)',
            'func': step3,
            'tags': ['recovery']
        }
    ]
    
    try:
        results = await hp.trace_multi_step_flow(
            flow_name='Error Handling Workflow',
            steps=steps,
            user_metadata={'user_id': 'user-123'},
            org_data={'org_id': 'org-456'}
        )
        
        print('Workflow completed with error handling:')
        for i, result in enumerate(results):
            print(f'Step {i+1}: {result}')
            
    except Exception as error:
        print(f'Workflow failed: {error}')


async def run_examples():
    """Run all multi-step examples"""
    try:
        await multi_step_workflow_example()
        await error_handling_workflow_example()
        
        print('\n=== All multi-step examples completed ===')
        print('Check your HuggingPlace backend for workflow trace data!')
    except Exception as error:
        print('Multi-step example failed:', error)


if __name__ == "__main__":
    asyncio.run(run_examples())
