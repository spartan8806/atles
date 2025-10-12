#!/usr/bin/env python3
"""
Test script for improved Ollama function calling
"""

import sys
import os
from pathlib import Path

# Add the atles directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / 'atles'))

def test_function_calling():
    """Test the improved function calling capabilities."""
    print("🧪 Testing Improved Ollama Function Calling...")
    print("=" * 60)
    
    try:
        from atles.ollama_client_enhanced import OllamaFunctionCaller
        
        # Create the enhanced client
        print("📱 Creating Enhanced Ollama Client...")
        client = OllamaFunctionCaller()
        
        # Check availability
        print("🔍 Checking Ollama availability...")
        if not client.is_available():
            print("❌ Ollama is not running. Please start Ollama with: ollama serve")
            return
        
        print("✅ Ollama is available!")
        
        # Show available functions
        print("\n🔧 Available Functions:")
        schema = client.get_function_schema()
        for func in schema["functions"]:
            print(f"  • {func['name']}: {func['description']}")
        
        # Test function execution directly
        print("\n🧪 Testing Direct Function Execution...")
        
        # Test search_code function
        print("🔍 Testing search_code function...")
        try:
            result = client.search_code_datasets("python flask", "python", "github_code")
            print(f"  ✅ Found {len(result)} code examples")
            if result:
                first_result = result[0]
                print(f"    - Example: {first_result.get('title', 'No title')}")
        except Exception as e:
            print(f"  ❌ search_code failed: {e}")
        
        # Test system info function
        print("\n💻 Testing get_system_info function...")
        try:
            info = client.get_system_info()
            print(f"  ✅ Platform: {info.get('platform', 'Unknown')}")
            print(f"  ✅ Python: {info.get('python_version', 'Unknown')}")
        except Exception as e:
            print(f"  ❌ get_system_info failed: {e}")
        
        # Test file listing function
        print("\n📁 Testing list_files function...")
        try:
            result = client.list_files(".", "*.py")
            print(f"  ✅ Found {len(result)} Python files")
            for file in result[:3]:  # Show first 3
                print(f"    - {file}")
        except Exception as e:
            print(f"  ❌ list_files failed: {e}")
        
        # Test function call handling with different formats
        print("\n🔄 Testing Function Call Handling...")
        
        # Test 1: Standard FUNCTION_CALL format
        test_response1 = "FUNCTION_CALL:get_system_info:{}"
        print(f"  Testing format 1: {test_response1}")
        result1 = client.handle_function_call(test_response1)
        print(f"    Result: {result1[:100]}...")
        
        # Test 2: Alternative format
        test_response2 = "get_system_info:{}"
        print(f"  Testing format 2: {test_response2}")
        result2 = client.handle_function_call(test_response2)
        print(f"    Result: {result2[:100]}...")
        
        # Test 3: Search code format
        test_response3 = 'search_code:{"query": "python flask", "language": "python"}'
        print(f"  Testing format 3: {test_response3}")
        result3 = client.handle_function_call(test_response3)
        print(f"    Result: {result3[:100]}...")
        
        # Close client
        client.close()
        print("\n✅ Function calling test completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_function_calling()
