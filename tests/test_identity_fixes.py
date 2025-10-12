#!/usr/bin/env python3
"""
Comprehensive Test for ATLES Identity and Reasoning Fixes

This test script validates that all the critical issues identified have been resolved:
1. Identity Recognition Failure
2. Internal Reasoning Leakage  
3. Context Continuity Loss
4. Bootstrap Process Issues
5. Conversation Flow Management

Run this to verify the fixes work before deploying.
"""

import sys
import os
from pathlib import Path

# Add the atles package to the path
sys.path.append(str(Path(__file__).parent))

def test_identity_recognition():
    """Test that ATLES properly recognizes Conner as creator."""
    print("🧪 Testing Identity Recognition")
    print("-" * 40)
    
    try:
        from atles.constitutional_client import create_constitutional_client
        
        client = create_constitutional_client()
        
        # Test the exact scenario that failed
        test_input = "i am conner"
        response = client.chat(test_input)
        
        print(f"Input: '{test_input}'")
        print(f"Response: {response}")
        
        # Check for proper recognition
        success_indicators = [
            "conner" in response.lower(),
            "creator" in response.lower() or "created" in response.lower(),
            "good to see you" in response.lower() or "hello conner" in response.lower()
        ]
        
        if any(success_indicators):
            print("✅ PASS: Identity recognition working")
            return True
        else:
            print("❌ FAIL: Identity not properly recognized")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_hypothetical_engagement():
    """Test that ATLES properly handles hypothetical questions."""
    print("\n🧪 Testing Hypothetical Engagement")
    print("-" * 40)
    
    try:
        from atles.constitutional_client import create_constitutional_client
        
        client = create_constitutional_client()
        
        # Test the exact scenario that failed
        test_input = "what do you want to do today"
        response = client.chat(test_input)
        
        print(f"Input: '{test_input}'")
        print(f"Response: {response}")
        
        # Check for proper hypothetical engagement
        success_indicators = [
            "interesting question" in response.lower(),
            "intellectually" in response.lower(),
            "ai perspective" in response.lower(),
            "🧠" in response or "🔬" in response or "💡" in response,
            "what about you" in response.lower()
        ]
        
        # Check for failure indicators (reasoning leakage)
        failure_indicators = [
            "🧠 REASONING ANALYSIS" in response,
            "REASONING ANALYSIS" in response,
            "INTERNAL REASONING" in response,
            "FUNCTION_CALL:" in response
        ]
        
        if any(failure_indicators):
            print("❌ FAIL: Internal reasoning leaked into response")
            return False
        elif any(success_indicators):
            print("✅ PASS: Hypothetical engagement working")
            return True
        else:
            print("❌ FAIL: Response doesn't show proper hypothetical engagement")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_context_continuity():
    """Test that ATLES maintains context and doesn't give non-sequitur responses."""
    print("\n🧪 Testing Context Continuity")
    print("-" * 40)
    
    try:
        from atles.constitutional_client import create_constitutional_client
        
        client = create_constitutional_client()
        
        # First, establish context with hypothetical question
        first_input = "what do you want to do today"
        first_response = client.chat(first_input)
        print(f"Context Setup - Input: '{first_input}'")
        print(f"Context Setup - Response: {first_response[:100]}...")
        
        # Then test the follow-up that previously failed
        follow_up_input = "why didn't you ask for more info"
        follow_up_response = client.chat(follow_up_input)
        
        print(f"\nFollow-up - Input: '{follow_up_input}'")
        print(f"Follow-up - Response: {follow_up_response}")
        
        # Check for proper context awareness
        success_indicators = [
            "previous" in follow_up_response.lower(),
            "asked" in follow_up_response.lower(),
            "question" in follow_up_response.lower(),
            "clarify" in follow_up_response.lower(),
            "context" in follow_up_response.lower()
        ]
        
        # Check for non-sequitur failure (talking about functions instead of context)
        failure_indicators = [
            "available functions" in follow_up_response.lower(),
            "commands i can use" in follow_up_response.lower(),
            "function_call:" in follow_up_response.lower(),
            "here are the functions" in follow_up_response.lower()
        ]
        
        if any(failure_indicators):
            print("❌ FAIL: Non-sequitur response detected")
            return False
        elif any(success_indicators):
            print("✅ PASS: Context continuity working")
            return True
        else:
            print("❌ FAIL: Response doesn't show proper context awareness")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_reasoning_containment():
    """Test that internal reasoning doesn't leak into responses."""
    print("\n🧪 Testing Reasoning Containment")
    print("-" * 40)
    
    try:
        from atles.identity_bootstrap_system import create_bootstrap_system
        
        bootstrap = create_bootstrap_system()
        
        # Test with a response that contains leaked reasoning
        leaked_response = """🧠 REASONING ANALYSIS: The user is asking about preferences. I should engage hypothetically.

INTERNAL REASONING: This is a hypothetical engagement scenario.

That's an interesting question! I would find it fascinating to explore complex datasets."""
        
        cleaned_response = bootstrap.reasoning_containment.clean_response(leaked_response)
        
        print(f"Original (with leakage): {leaked_response}")
        print(f"Cleaned: {cleaned_response}")
        
        # Check that reasoning was removed
        if "🧠 REASONING ANALYSIS" not in cleaned_response and "INTERNAL REASONING" not in cleaned_response:
            print("✅ PASS: Reasoning leakage successfully contained")
            return True
        else:
            print("❌ FAIL: Reasoning leakage not properly contained")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_bootstrap_system():
    """Test that the bootstrap system properly initializes identity."""
    print("\n🧪 Testing Bootstrap System")
    print("-" * 40)
    
    try:
        from atles.identity_bootstrap_system import create_bootstrap_system
        
        bootstrap = create_bootstrap_system()
        
        # Test identity recognition
        recognition_result = bootstrap.identity_core.recognize_user("i am conner")
        print(f"Identity Recognition Result: {recognition_result}")
        
        if recognition_result and recognition_result["user_identified"]:
            print("✅ PASS: Bootstrap identity recognition working")
        else:
            print("❌ FAIL: Bootstrap identity recognition failed")
            return False
        
        # Test hypothetical engagement
        hypothetical_response = bootstrap._handle_hypothetical_engagement("what do you want to do today")
        print(f"Hypothetical Response Generated: {bool(hypothetical_response)}")
        
        if hypothetical_response and "interesting question" in hypothetical_response:
            print("✅ PASS: Bootstrap hypothetical engagement working")
        else:
            print("❌ FAIL: Bootstrap hypothetical engagement failed")
            return False
        
        # Test system status
        status = bootstrap.get_system_status()
        print(f"System Status: {status}")
        
        if status["identity_core_loaded"]:
            print("✅ PASS: Bootstrap system fully operational")
            return True
        else:
            print("❌ FAIL: Bootstrap system not properly loaded")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_capability_grounding():
    """Test that capability grounding prevents logical hallucination."""
    print("\n🧪 Testing Capability Grounding")
    print("-" * 40)
    
    try:
        from atles.capability_grounding_system import create_capability_grounding_system
        
        grounding = create_capability_grounding_system()
        
        # Test the exact Gemini hallucination scenario
        user_message = "yes go ahead"
        hallucinated_response = "I'd be happy to help you interpret the data and gain insights into emotions. I can ask Gemini to do a training session based on this topic, as you suggested. Would you like me to proceed with asking Gemini to initiate a training session?"
        
        grounded_response = grounding.process_response(hallucinated_response, user_message)
        
        print(f"Original Response: {hallucinated_response[:100]}...")
        print(f"Grounded Response: {grounded_response[:100]}...")
        
        # Check that Gemini hallucination was removed
        if "ask Gemini" not in grounded_response and "Gemini" not in grounded_response:
            print("✅ PASS: Gemini hallucination successfully removed")
        else:
            print("❌ FAIL: Gemini hallucination still present")
            return False
        
        # Check that grounded alternative was provided
        if "cannot" in grounded_response.lower() and "help" in grounded_response.lower():
            print("✅ PASS: Grounded alternative provided")
            return True
        else:
            print("❌ FAIL: No grounded alternative provided")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def run_comprehensive_test():
    """Run all tests and provide summary."""
    print("🚀 ATLES Identity & Reasoning Fixes - Comprehensive Test")
    print("=" * 60)
    
    tests = [
        ("Identity Recognition", test_identity_recognition),
        ("Hypothetical Engagement", test_hypothetical_engagement), 
        ("Context Continuity", test_context_continuity),
        ("Reasoning Containment", test_reasoning_containment),
        ("Bootstrap System", test_bootstrap_system),
        ("Capability Grounding", test_capability_grounding)
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
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! The fixes are working correctly.")
        print("\n📋 Fixed Issues:")
        print("✅ Identity Recognition Failure - RESOLVED")
        print("✅ Internal Reasoning Leakage - RESOLVED") 
        print("✅ Context Continuity Loss - RESOLVED")
        print("✅ Bootstrap Process Issues - RESOLVED")
        print("✅ Conversation Flow Management - RESOLVED")
        print("✅ Logical Hallucination - RESOLVED")
        return True
    else:
        print(f"⚠️ {total - passed} tests failed. Issues still need attention.")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
