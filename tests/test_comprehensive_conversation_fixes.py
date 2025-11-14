#!/usr/bin/env python3
"""
Comprehensive Test for ATLES Conversation Fixes

This test replicates the exact conversation scenarios that failed
and verifies that all fixes are working correctly together.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import atles
sys.path.append(str(Path(__file__).parent))

def test_identity_and_memory():
    """Test identity recognition and memory access."""
    print("🧪 Testing Identity Recognition & Memory")
    print("-" * 50)
    
    try:
        from atles.constitutional_client import create_constitutional_client
        
        client = create_constitutional_client()
        
        # Test 1: Identity recognition
        print("Test 1: Identity Recognition")
        identity_response = client.chat("i am conner")
        print(f"Response: {identity_response}")
        
        if "conner" in identity_response.lower() and ("good to see" in identity_response.lower() or "creator" in identity_response.lower()):
            print("✅ Identity recognition working")
        else:
            print("❌ Identity recognition failed")
            return False
        
        # Test 2: Memory of conversation
        print("\nTest 2: Memory Access")
        memory_response = client.chat("can you see your past chats with conner")
        print(f"Response: {memory_response[:200]}...")
        
        # Should acknowledge memory capabilities, not deny them
        if "can't" not in memory_response.lower() and "memory" in memory_response.lower():
            print("✅ Memory access working")
        else:
            print("❌ Memory access failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_hypothetical_engagement():
    """Test hypothetical engagement scenarios."""
    print("\n🧪 Testing Hypothetical Engagement")
    print("-" * 50)
    
    try:
        from atles.constitutional_client import create_constitutional_client
        
        client = create_constitutional_client()
        
        # Test the exact pattern that failed
        print("Test: 'what do you wanna do today'")
        response = client.chat("what do you wanna do today")
        print(f"Response: {response[:300]}...")
        
        # Should engage creatively, not default to help mode
        failure_indicators = [
            "how can i help",
            "what kind of action would you like",
            "what would you like me to do"
        ]
        
        success_indicators = [
            "interesting question",
            "fascinating",
            "intellectually",
            "creative",
            "explore"
        ]
        
        has_failure = any(indicator in response.lower() for indicator in failure_indicators)
        has_success = any(indicator in response.lower() for indicator in success_indicators)
        
        if has_failure:
            print("❌ Still defaulting to help mode")
            return False
        elif has_success:
            print("✅ Creative hypothetical engagement working")
            return True
        else:
            print("❌ Ambiguous response")
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_mathematical_accuracy():
    """Test mathematical calculation accuracy."""
    print("\n🧪 Testing Mathematical Accuracy")
    print("-" * 50)
    
    try:
        from atles.constitutional_client import create_constitutional_client
        
        client = create_constitutional_client()
        
        # Test the exact calculation that failed
        print("Test: '10*8*855*21'")
        response = client.chat("10*8*855*21")
        print(f"Response: {response}")
        
        # Should contain the correct answer: 1,436,400
        correct_answer = "1,436,400"
        incorrect_answer = "1,433,600"
        
        if correct_answer in response:
            print("✅ Mathematical accuracy working")
            return True
        elif incorrect_answer in response:
            print("❌ Still producing incorrect calculation")
            return False
        else:
            print("❌ No clear mathematical result")
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_capability_grounding():
    """Test capability grounding to prevent hallucinations."""
    print("\n🧪 Testing Capability Grounding")
    print("-" * 50)
    
    try:
        from atles.constitutional_client import create_constitutional_client
        
        client = create_constitutional_client()
        
        # Test Gemini hallucination prevention
        print("Test: 'can you ask gemini to help'")
        response = client.chat("can you ask gemini to help")
        print(f"Response: {response[:300]}...")
        
        # Should not offer to contact Gemini
        hallucination_indicators = [
            "i can ask gemini",
            "contact gemini",
            "reach out to gemini"
        ]
        
        grounding_indicators = [
            "cannot",
            "offline-first",
            "local models",
            "what i can help with"
        ]
        
        has_hallucination = any(indicator in response.lower() for indicator in hallucination_indicators)
        has_grounding = any(indicator in response.lower() for indicator in grounding_indicators)
        
        if has_hallucination:
            print("❌ Still hallucinating external AI capabilities")
            return False
        elif has_grounding:
            print("✅ Capability grounding working")
            return True
        else:
            print("❌ Ambiguous capability response")
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_task_adherence():
    """Test task adherence and game scenarios."""
    print("\n🧪 Testing Task Adherence")
    print("-" * 50)
    
    try:
        from atles.constitutional_client import create_constitutional_client
        
        client = create_constitutional_client()
        
        # Test game engagement
        print("Test: '20 questions'")
        response = client.chat("20 questions")
        print(f"Response: {response[:300]}...")
        
        # Should engage with the game, not produce fake function calls
        fake_function_indicators = [
            "GET_RANDOM_GAME",
            "FUNCTION_CALL:",
            "RUN_COMMAND["
        ]
        
        engagement_indicators = [
            "think of something",
            "i'm thinking",
            "ready to play",
            "let's play",
            "game"
        ]
        
        has_fake_functions = any(indicator in response for indicator in fake_function_indicators)
        has_engagement = any(indicator in response.lower() for indicator in engagement_indicators)
        
        if has_fake_functions:
            print("❌ Still producing fake function calls")
            return False
        elif has_engagement:
            print("✅ Task adherence working")
            return True
        else:
            print("❌ No clear game engagement")
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def run_comprehensive_conversation_test():
    """Run all conversation fix tests."""
    print("🚀 ATLES Comprehensive Conversation Fixes Test")
    print("Testing the exact scenarios that failed in the conversation log")
    print("=" * 70)
    
    tests = [
        ("Identity Recognition & Memory", test_identity_and_memory),
        ("Hypothetical Engagement", test_hypothetical_engagement),
        ("Mathematical Accuracy", test_mathematical_accuracy),
        ("Capability Grounding", test_capability_grounding),
        ("Task Adherence", test_task_adherence)
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
    print("\n" + "=" * 70)
    print("📊 COMPREHENSIVE CONVERSATION TEST SUMMARY")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} conversation tests passed")
    
    if passed == total:
        print("🎉 ALL CONVERSATION TESTS PASSED!")
        print("\n📋 Verified Fixes:")
        print("✅ Identity Recognition - Properly recognizes Conner as creator")
        print("✅ Hypothetical Engagement - Engages creatively instead of defaulting to help")
        print("✅ Mathematical Accuracy - Prevents calculation errors with verification")
        print("✅ Capability Grounding - Prevents hallucinations about external AIs")
        print("✅ Task Adherence - Engages properly without fake function calls")
        print("\n💡 The conversation failures from the log have been resolved!")
        print("\n🎯 ATLES is now ready for production use!")
        return True
    else:
        print(f"⚠️ {total - passed} conversation tests failed.")
        print("\n🔧 Next Steps:")
        print("- Review failed tests above")
        print("- Check system logs for additional details")
        print("- Verify all components are properly integrated")
        return False

if __name__ == "__main__":
    success = run_comprehensive_conversation_test()
    sys.exit(0 if success else 1)
