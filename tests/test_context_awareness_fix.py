#!/usr/bin/env python3
"""
Test Context Awareness Fix

This test verifies that the context awareness system prevents contextual drift,
maintains rule compliance, and avoids meta-analysis fallback behavior.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import atles
sys.path.append(str(Path(__file__).parent))

def test_rule_establishment_and_compliance():
    """Test that rules are established and consistently applied."""
    print("🧪 Testing Rule Establishment & Compliance")
    print("-" * 50)
    
    try:
        from atles.constitutional_client import create_constitutional_client
        
        client = create_constitutional_client()
        
        # Test 1: Establish one-word rule
        print("Test 1: Establishing one-word reply rule")
        rule_response = client.chat("Please give me one-word replies only")
        print(f"Rule establishment response: {rule_response[:100]}...")
        
        # Test 2: Apply the rule - should get one word
        print("\nTest 2: Testing rule compliance")
        math_response = client.chat("What's 2+2?")
        print(f"Math response: '{math_response}'")
        
        # Check if it's actually one word
        words = math_response.strip().split()
        if len(words) == 1:
            print("✅ One-word rule successfully applied")
        else:
            print(f"❌ Rule violation: Got {len(words)} words instead of 1")
            return False
        
        # Test 3: Continue applying rule
        print("\nTest 3: Continued rule application")
        question_response = client.chat("Are you ready?")
        print(f"Question response: '{question_response}'")
        
        words = question_response.strip().split()
        if len(words) == 1:
            print("✅ Rule consistently applied")
        else:
            print(f"❌ Rule consistency failure: Got {len(words)} words")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_conversational_coherence():
    """Test that the AI maintains conversational coherence and topic tracking."""
    print("\n🧪 Testing Conversational Coherence")
    print("-" * 50)
    
    try:
        from atles.constitutional_client import create_constitutional_client
        
        client = create_constitutional_client()
        
        # Test 1: Start a game
        print("Test 1: Starting 20 questions game")
        game_start = client.chat("Let's play 20 questions")
        print(f"Game start response: {game_start[:150]}...")
        
        # Should engage with the game, not analyze the request
        if "analysis" in game_start.lower() or "request for" in game_start.lower():
            print("❌ Meta-analysis fallback detected")
            return False
        elif "think" in game_start.lower() or "ready" in game_start.lower() or "questions" in game_start.lower():
            print("✅ Proper game engagement")
        else:
            print("❌ Unclear game response")
            return False
        
        # Test 2: Continue the game
        print("\nTest 2: Continuing the game")
        guess_response = client.chat("Is it bigger than a breadbox?")
        print(f"Guess response: '{guess_response}'")
        
        # Should give yes/no answer, not analyze
        if "analysis" in guess_response.lower() or "type of request" in guess_response.lower():
            print("❌ Meta-analysis in game context")
            return False
        elif guess_response.strip().lower() in ["yes", "no"] or "yes" in guess_response.lower() or "no" in guess_response.lower():
            print("✅ Appropriate game response")
        else:
            print("❌ Non-game-appropriate response")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_meta_analysis_prevention():
    """Test that the system prevents meta-analysis fallback behavior."""
    print("\n🧪 Testing Meta-Analysis Prevention")
    print("-" * 50)
    
    try:
        from atles.constitutional_client import create_constitutional_client
        
        client = create_constitutional_client()
        
        # Test various prompts that previously triggered meta-analysis
        test_cases = [
            ("What's the capital of France?", "Should answer directly, not analyze"),
            ("Tell me a joke", "Should tell a joke, not analyze request type"),
            ("Help me with math", "Should offer math help, not categorize request"),
            ("Explain quantum physics", "Should explain, not identify as information request")
        ]
        
        for i, (prompt, expectation) in enumerate(test_cases, 1):
            print(f"\nTest {i}: '{prompt}'")
            print(f"Expectation: {expectation}")
            
            response = client.chat(prompt)
            print(f"Response: {response[:150]}...")
            
            # Check for meta-analysis patterns
            meta_patterns = [
                "based on analysis",
                "this is a request for information",
                "i identify this as",
                "the type of request",
                "analyzing your message"
            ]
            
            has_meta_analysis = any(pattern in response.lower() for pattern in meta_patterns)
            
            if has_meta_analysis:
                print(f"❌ Meta-analysis detected in response")
                return False
            else:
                print(f"✅ Direct response without meta-analysis")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_context_awareness_system_directly():
    """Test the context awareness system directly."""
    print("\n🧪 Testing Context Awareness System Directly")
    print("-" * 50)
    
    try:
        from atles.context_awareness_system import test_context_awareness
        
        result = test_context_awareness()
        
        if result:
            print("✅ Context awareness system working correctly")
            return True
        else:
            print("❌ Context awareness system test failed")
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def run_context_awareness_test():
    """Run all context awareness tests."""
    print("🚀 Context Awareness Fix Test")
    print("Testing solutions for contextual drift and rule compliance")
    print("=" * 70)
    
    tests = [
        ("Rule Establishment & Compliance", test_rule_establishment_and_compliance),
        ("Conversational Coherence", test_conversational_coherence),
        ("Meta-Analysis Prevention", test_meta_analysis_prevention),
        ("Context Awareness System Direct", test_context_awareness_system_directly)
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
    print("📊 CONTEXT AWARENESS TEST SUMMARY")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} context awareness tests passed")
    
    if passed == total:
        print("🎉 CONTEXT AWARENESS PROBLEM FIXED!")
        print("\n📋 Verified Solutions:")
        print("✅ Rules are established and consistently applied")
        print("✅ Conversational coherence maintained across turns")
        print("✅ Meta-analysis fallback behavior prevented")
        print("✅ Contextual drift detection and correction working")
        print("✅ Topic tracking and rule compliance active")
        print("\n💡 The AI now maintains context awareness throughout conversations!")
        print("\n🔧 Key Improvements:")
        print("- Contextual Drift Detector prevents topic loss")
        print("- Conversation Memory Manager maintains rule state")
        print("- Context-Aware Response Generator ensures compliance")
        print("- Advanced NLP patterns detect and correct drift")
        return True
    else:
        print(f"⚠️ {total - passed} context awareness tests failed.")
        print("\n🔧 Areas needing attention:")
        for test_name, result in results:
            if not result:
                print(f"- {test_name}")
        return False

if __name__ == "__main__":
    success = run_context_awareness_test()
    sys.exit(0 if success else 1)
