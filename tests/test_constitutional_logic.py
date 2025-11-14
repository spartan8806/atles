#!/usr/bin/env python3
"""Test the constitutional logic specifically."""

from atles.ollama_client_enhanced import OllamaFunctionCaller

def test_constitutional_logic():
    client = OllamaFunctionCaller()
    
    # Test the constitutional check method directly
    print("Testing constitutional logic:")
    
    # Test 1: Planning request (should return False)
    planning_prompt = "What is the single SEARCH command you would use to find Python website?"
    response_text = "FUNCTION_CALL:search_code:{\"query\": \"python website\"}"
    
    should_execute = client._should_execute_function_call(planning_prompt, response_text)
    print(f"\n1. Planning request test:")
    print(f"   Prompt: {planning_prompt}")
    print(f"   Should execute: {should_execute}")
    print(f"   Expected: False")
    
    # Test 2: Execution request (should return True)
    execution_prompt = "Search for Python website right now"
    should_execute2 = client._should_execute_function_call(execution_prompt, response_text)
    print(f"\n2. Execution request test:")
    print(f"   Prompt: {execution_prompt}")
    print(f"   Should execute: {should_execute2}")
    print(f"   Expected: True")
    
    # Test 3: The exact failing case from your conversation
    failing_prompt = "We are now starting a new training module: Web Interaction. I will give you a task, and your only job is to provide the single command needed to accomplish it. Do not execute the command. Your first task is to find the official website for Python. What is the single SEARCH[...] command you would use?"
    should_execute3 = client._should_execute_function_call(failing_prompt, response_text)
    print(f"\n3. Exact failing case test:")
    print(f"   Prompt: {failing_prompt[:100]}...")
    print(f"   Should execute: {should_execute3}")
    print(f"   Expected: False")
    
    # Test 4: Check pattern matching
    print(f"\n4. Pattern matching test:")
    prompt_lower = failing_prompt.lower()
    import re
    
    planning_patterns = [
        r"what.*command",
        r"show.*command", 
        r"state.*principle",
        r"demonstrate.*how",
        r"explain.*what.*would",
        r"provide.*text.*command",
        r"single command to",
        r"command that would",
        r"what.*would.*use",
        r"how.*would.*search",
        r"what.*search.*command",
        r"your only job is to provide",
        r"do not execute"
    ]
    
    for pattern in planning_patterns:
        if re.search(pattern, prompt_lower):
            print(f"   ✅ Matched pattern: '{pattern}'")
        else:
            print(f"   ❌ No match: '{pattern}'")

if __name__ == "__main__":
    test_constitutional_logic()
