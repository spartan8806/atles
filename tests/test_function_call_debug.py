"""
Test enhanced function calling with debug mode.

This script tests the improved function calling with debug mode enabled
to verify that the enhancements work correctly.
"""

import logging
import sys
import json
import importlib.util

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Check for optional dependencies without warnings
def check_module_quietly(module_name):
    """Check if a module is available without printing warnings"""
    is_available = importlib.util.find_spec(module_name) is not None
    if not is_available:
        print(f"{module_name} not available: No module named '{module_name}'")
    return is_available

# Silently check for optional modules before importing OllamaFunctionCaller
check_module_quietly('bandit')
check_module_quietly('torchvision')

# Now import our actual module
from atles.ollama_client_enhanced import OllamaFunctionCaller

def test_function_call_handling():
    """Test the enhanced function call handling with various formats."""
    
    print("\n=== Testing Enhanced Function Call Handling ===\n")
    
    # Create client with debug mode enabled
    client = OllamaFunctionCaller(debug_mode=True)
    print(f"Debug mode enabled: {client.get_debug_mode()}")
    
    # Test loading config
    print("Attempting to load debug settings from config...")
    client.load_debug_settings_from_config()
    print(f"Debug mode after loading config: {client.get_debug_mode()}")
    
    # Force debug mode on for testing
    client.set_debug_mode(True)
    print(f"Debug mode after manual setting: {client.get_debug_mode()}")
    
    # Test cases with different function call formats
    test_cases = [
        # Standard format
        "FUNCTION_CALL:web_search:{\"query\": \"ATLES framework capabilities\", \"count\": 3}",
        
        # With extra whitespace
        "FUNCTION_CALL: web_search : {\"query\": \"ATLES framework capabilities\", \"count\": 3}",
        
        # With different capitalization
        "Function_Call:web_search:{\"query\": \"ATLES framework capabilities\", \"count\": 3}",
        
        # With text before and after
        "I think you should search the web. FUNCTION_CALL:web_search:{\"query\": \"ATLES framework capabilities\"} Let me know the results.",
        
        # With single quotes instead of double quotes
        "FUNCTION_CALL:web_search:{'query': 'ATLES framework capabilities', 'count': 3}",
        
        # With line breaks
        """Here's a function call:
        FUNCTION_CALL:web_search:{
            "query": "ATLES framework capabilities",
            "count": 3
        }
        Let's see what it returns.""",
        
        # Alternative format without FUNCTION_CALL prefix
        "web_search:{\"query\": \"ATLES framework capabilities\", \"count\": 3}",
        
        # Invalid function name
        "FUNCTION_CALL:nonexistent_function:{\"query\": \"test\"}",
        
        # Invalid JSON
        "FUNCTION_CALL:web_search:{query: \"Missing quotes\", count: 3}",
    ]
    
    # Run tests
    for i, test_case in enumerate(test_cases):
        print(f"\n--- Test Case {i+1} ---")
        print(f"INPUT: {test_case[:50]}{'...' if len(test_case) > 50 else ''}")
        
        result = client.handle_function_call(test_case)
        
        print(f"OUTPUT: {result[:100]}{'...' if len(result) > 100 else ''}")
        print("-" * 50)
    
    print("\nTesting complete!")

def test_web_functions_execution():
    """Test the execution of web functions."""
    
    print("\n=== Testing Web Functions Execution ===\n")
    
    client = OllamaFunctionCaller(debug_mode=True)
    
    # Test web_search function directly
    print("Testing web_search function:")
    result = client.execute_function("web_search", {"query": "ATLES framework capabilities"})
    print(json.dumps(result, indent=2))
    print("-" * 50)
    
    # Test check_url_accessibility function
    print("\nTesting check_url_accessibility function:")
    result = client.execute_function("check_url_accessibility", {"url": "https://www.example.com"})
    print(json.dumps(result, indent=2))
    print("-" * 50)

if __name__ == "__main__":
    print("Starting function call debug tests...")
    test_function_call_handling()
    test_web_functions_execution()
