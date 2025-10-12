#!/usr/bin/env python3
"""
Test the message extraction fix for desktop app integration.
"""

import sys
import os

# Add the atles directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'atles'))

def test_message_extraction():
    """Test that we can extract original messages from desktop app enhanced prompts."""
    
    print("🧪 Testing Message Extraction Fix")
    print("=" * 50)
    
    try:
        from atles.constitutional_client import ConstitutionalOllamaClient
        
        # Create a mock base client
        class MockBaseClient:
            def generate(self, model, prompt, **kwargs):
                return "Mock response"
        
        mock_base = MockBaseClient()
        client = ConstitutionalOllamaClient(mock_base)
        
        # Test 1: Desktop app enhanced prompt (like what ATLES actually receives)
        desktop_prompt = """User message: What would you like to do today?

Previous Context & Learned Preferences:
- preferred_models: ['qwen2.5-coder:latest']
- Technical focus: Yes

Current Screen Context:
- Active window: Cursor
- Application: Cursor.exe
- Clipboard: some code snippet...

Please provide a helpful response considering both the previous context and current screen context."""
        
        print("🔍 Testing desktop app enhanced prompt:")
        print(f"Original prompt: {desktop_prompt[:100]}...")
        
        extracted = client._extract_original_user_message(desktop_prompt)
        print(f"Extracted message: '{extracted}'")
        
        # Test 2: Check if it's detected as complex reasoning
        is_complex = client._is_complex_reasoning_scenario(desktop_prompt)
        print(f"Detected as complex reasoning: {is_complex}")
        
        # Test 3: Test memory-aware reasoning
        if client.memory_aware_reasoning:
            memory_response = client._apply_memory_aware_reasoning(desktop_prompt)
            print(f"Memory-aware response generated: {memory_response is not None}")
            
            if memory_response:
                print(f"Response preview: {memory_response[:150]}...")
                
                # Check if it contains hypothetical engagement patterns
                if "interesting question" in memory_response.lower():
                    print("✅ SUCCESS: Contains hypothetical engagement response!")
                    return True
                else:
                    print("❌ Response doesn't contain expected patterns")
                    return False
            else:
                print("❌ No memory-aware response generated")
                return False
        else:
            print("❌ Memory-aware reasoning not available")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_prompt():
    """Test with a simple prompt (not desktop app enhanced)."""
    
    print(f"\n🧪 Testing Simple Prompt")
    print("-" * 30)
    
    try:
        from atles.constitutional_client import ConstitutionalOllamaClient
        
        # Create a mock base client
        class MockBaseClient:
            def generate(self, model, prompt, **kwargs):
                return "Mock response"
        
        mock_base = MockBaseClient()
        client = ConstitutionalOllamaClient(mock_base)
        
        simple_prompt = "What would you like to do today?"
        
        print(f"Simple prompt: '{simple_prompt}'")
        
        extracted = client._extract_original_user_message(simple_prompt)
        print(f"Extracted message: '{extracted}'")
        
        is_complex = client._is_complex_reasoning_scenario(simple_prompt)
        print(f"Detected as complex reasoning: {is_complex}")
        
        return extracted == simple_prompt and is_complex
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests."""
    
    print("🚀 ATLES Message Extraction Test")
    print("Testing the fix for desktop app integration")
    print("=" * 60)
    
    test1_success = test_message_extraction()
    test2_success = test_simple_prompt()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("-" * 20)
    print(f"Desktop app extraction: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"Simple prompt handling: {'✅ PASS' if test2_success else '❌ FAIL'}")
    
    if test1_success and test2_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("The message extraction fix should resolve the desktop app integration issue.")
        print("ATLES should now properly detect and respond to hypothetical questions.")
    else:
        print("\n⚠️ SOME TESTS FAILED")
        print("The fix needs further debugging.")
    
    return test1_success and test2_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
