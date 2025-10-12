#!/usr/bin/env python3
"""Test if alternative function call formats are being detected."""

from atles.ollama_client_enhanced import OllamaFunctionCaller

def test_alternative_formats():
    client = OllamaFunctionCaller()
    
    print("Testing alternative function call formats:")
    
    # Test 1: Standard format (should not execute due to our fix)
    print("\n1. Standard FUNCTION_CALL format:")
    result1 = client.handle_function_call('FUNCTION_CALL:search_code:{"query": "test"}')
    print(f"   Result: {result1[:100]}...")
    
    # Test 2: Alternative format without FUNCTION_CALL prefix
    print("\n2. Alternative format (search_code:...):")
    result2 = client.handle_function_call('search_code:{"query": "test"}')
    print(f"   Result: {result2[:100]}...")
    
    # Test 3: Check if it's the same
    print(f"\n3. Are results the same? {result1 == result2}")
    
    # Test 4: Check what the method actually detects
    print("\n4. Method detection test:")
    test_text = 'search_code:{"query": "test"}'
    lines = test_text.split('\n')
    detected = False
    for line in lines:
        if line.strip().startswith("FUNCTION_CALL:"):
            detected = True
            break
    print(f"   Does 'search_code:...' start with 'FUNCTION_CALL:'? {detected}")

if __name__ == "__main__":
    test_alternative_formats()
