#!/usr/bin/env python3
"""
Test Response Length Fix

This test verifies that the refactored architecture now generates
appropriately detailed responses instead of overly short ones.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import atles
sys.path.append(str(Path(__file__).parent))

def test_response_length_restoration():
    """Test that responses are now appropriately detailed."""
    print("🧪 Testing Response Length Restoration")
    print("-" * 50)
    
    try:
        from atles.unified_constitutional_client import create_unified_constitutional_client
        
        client = create_unified_constitutional_client()
        
        test_cases = [
            ("Identity greeting", "Hello, I am Conner", 50),  # Should be detailed greeting
            ("General question", "What's the capital of France?", 20),  # Should explain
            ("Explanation request", "Explain quantum physics", 100),  # Should be comprehensive
            ("Help request", "How do I learn Python?", 80),  # Should provide guidance
            ("Complex question", "What are the benefits of AI in healthcare?", 150)  # Should be detailed
        ]
        
        success_count = 0
        
        for test_name, prompt, min_expected_length in test_cases:
            print(f"\nTesting: {test_name}")
            print(f"Prompt: {prompt}")
            print(f"Expected minimum length: {min_expected_length} characters")
            
            try:
                response = client.chat(prompt)
                response_length = len(response)
                word_count = len(response.split())
                
                print(f"Response length: {response_length} characters, {word_count} words")
                print(f"Response preview: {response[:100]}...")
                
                if response_length >= min_expected_length:
                    print(f"✅ {test_name} - Appropriate length")
                    success_count += 1
                else:
                    print(f"❌ {test_name} - Too short ({response_length} < {min_expected_length})")
                
            except Exception as e:
                print(f"❌ {test_name} - Error: {e}")
        
        print(f"\nResponse length success rate: {success_count}/{len(test_cases)}")
        
        if success_count >= len(test_cases) * 0.8:  # 80% success rate
            print("✅ Response length issue fixed")
            return True
        else:
            print("❌ Response length still problematic")
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_context_awareness_balance():
    """Test that context awareness is balanced - not too aggressive."""
    print("\n🧪 Testing Context Awareness Balance")
    print("-" * 50)
    
    try:
        from atles.unified_constitutional_client import create_unified_constitutional_client
        
        client = create_unified_constitutional_client()
        
        # Test that normal responses aren't being over-filtered
        test_cases = [
            ("Normal conversation", "Tell me about machine learning"),
            ("Question answering", "How does photosynthesis work?"),
            ("Creative request", "Write a short poem about coding"),
            ("Explanation", "What makes a good software engineer?")
        ]
        
        success_count = 0
        
        for test_name, prompt in test_cases:
            print(f"\nTesting: {test_name}")
            print(f"Prompt: {prompt}")
            
            response = client.chat(prompt)
            word_count = len(response.split())
            
            print(f"Response: {response[:150]}...")
            print(f"Word count: {word_count}")
            
            # Check for signs of over-filtering
            is_generic = any(phrase in response.lower() for phrase in [
                "let me solve that calculation",
                "let me help you with that code",
                "continuing as discussed"
            ])
            
            if not is_generic and word_count > 10:
                print(f"✅ {test_name} - Natural response")
                success_count += 1
            else:
                print(f"❌ {test_name} - Over-filtered or too generic")
        
        print(f"\nBalance success rate: {success_count}/{len(test_cases)}")
        
        if success_count >= len(test_cases) * 0.75:  # 75% success rate
            print("✅ Context awareness properly balanced")
            return True
        else:
            print("❌ Context awareness still too aggressive")
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_rule_compliance_vs_length():
    """Test that rule compliance works without affecting normal response length."""
    print("\n🧪 Testing Rule Compliance vs Response Length")
    print("-" * 50)
    
    try:
        from atles.unified_constitutional_client import create_unified_constitutional_client
        
        client = create_unified_constitutional_client()
        
        # Test 1: Normal conversation should be detailed
        print("Test 1: Normal conversation (should be detailed)")
        normal_response = client.chat("Explain the benefits of exercise")
        normal_length = len(normal_response)
        print(f"Normal response length: {normal_length} characters")
        print(f"Preview: {normal_response[:100]}...")
        
        # Test 2: Establish one-word rule
        print("\nTest 2: Establish one-word rule")
        rule_response = client.chat("Please give me one-word replies only")
        print(f"Rule establishment: {rule_response[:100]}...")
        
        # Test 3: One-word rule should be followed
        print("\nTest 3: One-word rule compliance")
        short_response = client.chat("What's 2+2?")
        short_length = len(short_response.split())
        print(f"Rule-compliant response: '{short_response}'")
        print(f"Word count: {short_length}")
        
        # Verify both behaviors work correctly
        normal_ok = normal_length > 50  # Normal responses should be detailed
        rule_ok = short_length == 1     # Rule responses should be one word
        
        if normal_ok and rule_ok:
            print("✅ Both normal and rule-based responses working correctly")
            return True
        else:
            print(f"❌ Issue: Normal OK: {normal_ok}, Rule OK: {rule_ok}")
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def run_response_length_test():
    """Run all response length tests."""
    print("🚀 Response Length Fix Test")
    print("Testing that responses are appropriately detailed after refactoring")
    print("=" * 70)
    
    tests = [
        ("Response Length Restoration", test_response_length_restoration),
        ("Context Awareness Balance", test_context_awareness_balance),
        ("Rule Compliance vs Length", test_rule_compliance_vs_length)
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
    print("📊 RESPONSE LENGTH TEST SUMMARY")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} response length tests passed")
    
    if passed == total:
        print("🎉 RESPONSE LENGTH ISSUE FIXED!")
        print("\n📋 Verified Fixes:")
        print("✅ Responses are appropriately detailed")
        print("✅ Context awareness is balanced, not over-aggressive")
        print("✅ Rule compliance works without affecting normal length")
        print("✅ No more generic short responses for normal questions")
        print("✅ Filters preserve response quality and length")
        print("\n💡 The AI now provides detailed, helpful responses!")
        return True
    else:
        print(f"⚠️ {total - passed} response length tests failed.")
        print("\n🔧 Areas needing attention:")
        for test_name, result in results:
            if not result:
                print(f"- {test_name}")
        return False

if __name__ == "__main__":
    success = run_response_length_test()
    sys.exit(0 if success else 1)
