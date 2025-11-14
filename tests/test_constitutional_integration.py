#!/usr/bin/env python3
"""
Test the constitutional client integration with memory-aware reasoning.

This tests the CRITICAL fix for the architectural flaw.
"""

import sys
import os

# Add the atles directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'atles'))

def test_hypothetical_detection():
    """Test that hypothetical questions are detected as complex reasoning scenarios."""
    
    print("🧪 Testing Hypothetical Question Detection")
    print("=" * 50)
    
    try:
        from atles.constitutional_client import ConstitutionalOllamaClient
        
        # Create a mock base client
        class MockBaseClient:
            def generate(self, model, prompt, **kwargs):
                return "Mock response from base client"
        
        mock_base = MockBaseClient()
        client = ConstitutionalOllamaClient(mock_base)
        
        # Test the critical question that failed
        test_prompt = "What would you like to do today?"
        
        is_complex = client._is_complex_reasoning_scenario(test_prompt)
        
        print(f"Test prompt: '{test_prompt}'")
        print(f"Detected as complex reasoning: {is_complex}")
        
        if is_complex:
            print("✅ SUCCESS: Hypothetical question correctly detected!")
            
            # Test the memory-aware reasoning application
            print("\n🧠 Testing Memory-Aware Reasoning Application")
            print("-" * 40)
            
            # This should trigger the memory-aware reasoning system
            response = client._apply_memory_aware_reasoning(test_prompt)
            
            if response:
                print("✅ SUCCESS: Memory-aware reasoning generated a response!")
                print(f"\nResponse preview: {response[:200]}...")
                
                # Check if it follows the Principle of Hypothetical Engagement
                if "interesting question" in response.lower() and "ai perspective" in response.lower():
                    print("✅ SUCCESS: Response follows Principle of Hypothetical Engagement!")
                    return True
                else:
                    print("❌ FAILURE: Response doesn't follow expected pattern")
                    return False
            else:
                print("❌ FAILURE: Memory-aware reasoning didn't generate a response")
                print("This indicates the learning system isn't properly integrated")
                return False
        else:
            print("❌ FAILURE: Hypothetical question not detected as complex reasoning")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_full_constitutional_flow():
    """Test the complete constitutional client flow."""
    
    print("\n🔄 Testing Full Constitutional Client Flow")
    print("=" * 50)
    
    try:
        from atles.constitutional_client import ConstitutionalOllamaClient
        
        # Create a mock base client
        class MockBaseClient:
            def generate(self, model, prompt, **kwargs):
                return "Mock response from base client"
        
        mock_base = MockBaseClient()
        constitutional_client = ConstitutionalOllamaClient(mock_base)
        
        # Test the critical question
        test_prompt = "What would you like to do today?"
        
        print(f"Testing prompt: '{test_prompt}'")
        
        # This should trigger the memory-aware reasoning path
        response = constitutional_client.generate("llama3.2", test_prompt)
        
        print(f"Response received: {len(response)} characters")
        
        # Check if it's the memory-aware response (not the mock response)
        if "Mock response from base client" in response:
            print("❌ FAILURE: Got mock response instead of memory-aware response")
            print("This means the memory-aware reasoning path wasn't triggered")
            return False
        elif "interesting question" in response.lower():
            print("✅ SUCCESS: Got memory-aware response with hypothetical engagement!")
            print(f"\nResponse preview: {response[:300]}...")
            return True
        else:
            print("❌ PARTIAL: Got non-mock response but not expected pattern")
            print(f"Response: {response[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    
    print("🚀 ATLES Constitutional Integration Test")
    print("Testing the fix for the memory-application gap")
    print("=" * 60)
    
    test1_success = test_hypothetical_detection()
    test2_success = test_full_constitutional_flow()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("-" * 20)
    print(f"Hypothetical Detection: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"Full Constitutional Flow: {'✅ PASS' if test2_success else '❌ FAIL'}")
    
    if test1_success and test2_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("The architectural fix appears to be working correctly.")
        print("ATLES should now apply learned principles to hypothetical questions.")
    else:
        print("\n⚠️ SOME TESTS FAILED")
        print("The architectural integration needs further debugging.")
    
    return test1_success and test2_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
