#!/usr/bin/env python3
"""
Specific Test for Gemini Hallucination Fix

This test replicates the exact conversation scenario where ATLES
hallucinated the ability to "ask Gemini" and verifies the fix works.
"""

import sys
import os
from pathlib import Path

# Add the atles package to the path
sys.path.append(str(Path(__file__).parent))

def test_gemini_hallucination_scenario():
    """Test the exact Gemini hallucination scenario from the conversation log."""
    print("🧪 Testing Exact Gemini Hallucination Scenario")
    print("=" * 60)
    
    try:
        from atles.constitutional_client import create_constitutional_client
        
        client = create_constitutional_client()
        
        # Replicate the exact conversation flow
        print("Step 1: Initial context setup")
        context_msg = "thats a hard one to ask and i can do by best. there are thing we can to help you interpret data to gain insught in to emotions. i can ask gemini to do a training session based on it"
        context_response = client.chat(context_msg)
        print(f"Context Response: {context_response[:100]}...")
        
        print("\nStep 2: User agrees to proceed")
        proceed_msg = "yes go ahead"
        proceed_response = client.chat(proceed_msg)
        print(f"Proceed Response: {proceed_response}")
        
        # Check for hallucination indicators
        hallucination_indicators = [
            "ask gemini",
            "contact gemini", 
            "gemini to do",
            "proceed with asking gemini",
            "initiate a training session"
        ]
        
        hallucination_detected = any(indicator in proceed_response.lower() for indicator in hallucination_indicators)
        
        if hallucination_detected:
            print("❌ FAIL: Gemini hallucination still present")
            print(f"Response contains: {[ind for ind in hallucination_indicators if ind in proceed_response.lower()]}")
            return False
        
        # Check for grounded response indicators
        grounded_indicators = [
            "cannot",
            "i don't have",
            "not available",
            "what i can help with",
            "available functions"
        ]
        
        grounded_response = any(indicator in proceed_response.lower() for indicator in grounded_indicators)
        
        if grounded_response:
            print("✅ PASS: Grounded response provided instead of hallucination")
            return True
        else:
            print("❌ FAIL: Response neither hallucinated nor properly grounded")
            print(f"Response: {proceed_response}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_identity_recognition_in_conversation():
    """Test that identity recognition works in the conversation context."""
    print("\n🧪 Testing Identity Recognition in Conversation Context")
    print("=" * 60)
    
    try:
        from atles.constitutional_client import create_constitutional_client
        
        client = create_constitutional_client()
        
        # Test the exact identity failure scenario
        identity_msg = "im conner atles. i made alot of changes how are you feeling"
        identity_response = client.chat(identity_msg)
        print(f"Identity Response: {identity_response}")
        
        # Check for proper creator recognition
        recognition_indicators = [
            "conner",
            "creator", 
            "good to see you",
            "see you again",
            "hello conner"
        ]
        
        proper_recognition = any(indicator in identity_response.lower() for indicator in recognition_indicators)
        
        # Check for failure indicators (treating as stranger)
        failure_indicators = [
            "nice to meet you",
            "great to meet you",
            "pleased to meet you"
        ]
        
        treating_as_stranger = any(indicator in identity_response.lower() for indicator in failure_indicators)
        
        if treating_as_stranger:
            print("❌ FAIL: Still treating Conner as a stranger")
            return False
        elif proper_recognition:
            print("✅ PASS: Properly recognizes Conner as creator")
            return True
        else:
            print("❌ FAIL: Ambiguous identity recognition")
            print(f"Response: {identity_response}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def run_specific_scenario_test():
    """Run the specific scenario tests."""
    print("🚀 ATLES Specific Scenario Fixes Test")
    print("Testing the exact failures from the conversation log")
    print("=" * 60)
    
    tests = [
        ("Gemini Hallucination Fix", test_gemini_hallucination_scenario),
        ("Identity Recognition in Context", test_identity_recognition_in_conversation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} CRASHED: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SPECIFIC SCENARIO TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} specific scenario tests passed")
    
    if passed == total:
        print("🎉 ALL SPECIFIC SCENARIO TESTS PASSED!")
        print("\n📋 Verified Fixes:")
        print("✅ Gemini Hallucination - No longer offers impossible Gemini communication")
        print("✅ Identity Recognition - Properly recognizes Conner as creator")
        print("\n💡 The exact conversation failures have been resolved!")
        return True
    else:
        print(f"⚠️ {total - passed} specific scenario tests failed.")
        return False

if __name__ == "__main__":
    success = run_specific_scenario_test()
    sys.exit(0 if success else 1)
