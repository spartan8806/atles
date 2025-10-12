#!/usr/bin/env python3
"""
Final Response Length Fix Test

This test verifies that both the original and unified constitutional clients
now provide appropriately detailed responses instead of short ones.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import atles
sys.path.append(str(Path(__file__).parent))

def test_original_constitutional_client():
    """Test that the original constitutional client now gives detailed responses."""
    print("🧪 Testing Original Constitutional Client")
    print("-" * 50)
    
    try:
        from atles.constitutional_client import create_constitutional_client
        
        client = create_constitutional_client()
        
        test_cases = [
            ("Detailed explanation", "Explain machine learning in detail", 200),
            ("General question", "What are the benefits of exercise?", 150),
            ("How-to question", "How do I learn Python programming?", 100),
            ("Complex topic", "What is quantum computing?", 180),
        ]
        
        success_count = 0
        
        for test_name, prompt, min_length in test_cases:
            print(f"\nTesting: {test_name}")
            print(f"Prompt: {prompt}")
            
            response = client.chat(prompt)
            length = len(response)
            words = len(response.split())
            
            print(f"Response length: {length} chars, {words} words")
            print(f"Preview: {response[:100]}...")
            
            if length >= min_length:
                print(f"✅ {test_name} - Appropriate length")
                success_count += 1
            else:
                print(f"❌ {test_name} - Too short ({length} < {min_length})")
        
        print(f"\nOriginal client success rate: {success_count}/{len(test_cases)}")
        return success_count == len(test_cases)
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_unified_constitutional_client():
    """Test that the unified constitutional client gives detailed responses."""
    print("\n🧪 Testing Unified Constitutional Client")
    print("-" * 50)
    
    try:
        from atles.unified_constitutional_client import create_unified_constitutional_client
        
        client = create_unified_constitutional_client()
        
        test_cases = [
            ("Detailed explanation", "Explain artificial intelligence in detail", 200),
            ("General question", "What are the causes of climate change?", 150),
            ("Technical question", "How does blockchain technology work?", 180),
        ]
        
        success_count = 0
        
        for test_name, prompt, min_length in test_cases:
            print(f"\nTesting: {test_name}")
            print(f"Prompt: {prompt}")
            
            response = client.chat(prompt)
            length = len(response)
            words = len(response.split())
            
            print(f"Response length: {length} chars, {words} words")
            print(f"Preview: {response[:100]}...")
            
            if length >= min_length:
                print(f"✅ {test_name} - Appropriate length")
                success_count += 1
            else:
                print(f"❌ {test_name} - Too short ({length} < {min_length})")
        
        print(f"\nUnified client success rate: {success_count}/{len(test_cases)}")
        return success_count == len(test_cases)
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_session_management():
    """Test that session management doesn't interfere with response length."""
    print("\n🧪 Testing Session Management vs Response Length")
    print("-" * 50)
    
    try:
        from atles.constitutional_client import create_constitutional_client
        
        client = create_constitutional_client()
        
        # Test 1: First message (potential session start)
        print("Test 1: First message")
        response1 = client.chat("Tell me about renewable energy")
        length1 = len(response1)
        print(f"First message length: {length1} chars")
        print(f"Preview: {response1[:100]}...")
        
        # Test 2: Follow-up message (not session start)
        print("\nTest 2: Follow-up message")
        response2 = client.chat("What about solar panels specifically?")
        length2 = len(response2)
        print(f"Follow-up length: {length2} chars")
        print(f"Preview: {response2[:100]}...")
        
        # Both should be detailed
        both_detailed = length1 > 100 and length2 > 100
        
        if both_detailed:
            print("✅ Session management doesn't interfere with response length")
            return True
        else:
            print(f"❌ Session management issue: First: {length1}, Follow-up: {length2}")
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_identity_vs_normal_responses():
    """Test that identity responses are short but normal responses are detailed."""
    print("\n🧪 Testing Identity vs Normal Response Lengths")
    print("-" * 50)
    
    try:
        from atles.constitutional_client import create_constitutional_client
        
        client = create_constitutional_client()
        
        # Test 1: Identity statement (should be short and appropriate)
        print("Test 1: Identity statement")
        identity_response = client.chat("I am Conner")
        identity_length = len(identity_response)
        print(f"Identity response length: {identity_length} chars")
        print(f"Identity response: {identity_response}")
        
        # Test 2: Normal question (should be detailed)
        print("\nTest 2: Normal question")
        normal_response = client.chat("Explain photosynthesis")
        normal_length = len(normal_response)
        print(f"Normal response length: {normal_length} chars")
        print(f"Normal preview: {normal_response[:100]}...")
        
        # Identity should be concise, normal should be detailed
        identity_appropriate = 30 <= identity_length <= 200  # Reasonable identity response
        normal_detailed = normal_length > 150  # Should be detailed explanation
        
        if identity_appropriate and normal_detailed:
            print("✅ Both identity and normal responses are appropriately sized")
            return True
        else:
            print(f"❌ Length issue - Identity: {identity_length}, Normal: {normal_length}")
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def run_final_response_length_test():
    """Run all final response length tests."""
    print("🚀 Final Response Length Fix Test")
    print("Verifying that the bootstrap session management fix resolved short responses")
    print("=" * 80)
    
    tests = [
        ("Original Constitutional Client", test_original_constitutional_client),
        ("Unified Constitutional Client", test_unified_constitutional_client),
        ("Session Management", test_session_management),
        ("Identity vs Normal Responses", test_identity_vs_normal_responses)
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
    print("\n" + "=" * 80)
    print("📊 FINAL RESPONSE LENGTH TEST SUMMARY")
    print("=" * 80)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} final response length tests passed")
    
    if passed == total:
        print("🎉 RESPONSE LENGTH ISSUE COMPLETELY FIXED!")
        print("\n📋 Verified Solutions:")
        print("✅ Original constitutional client gives detailed responses")
        print("✅ Unified constitutional client gives detailed responses")
        print("✅ Session management doesn't interfere with response length")
        print("✅ Identity responses are appropriate, normal responses are detailed")
        print("✅ Bootstrap system only triggers for actual session starts")
        print("✅ No more generic short responses for normal questions")
        print("\n💡 Both client architectures now work correctly!")
        print("\n🔧 Root Cause Fixed:")
        print("- Bootstrap system was too aggressive about session detection")
        print("- Identity responses were being triggered for normal questions")
        print("- Session start logic has been refined to be more precise")
        return True
    else:
        print(f"⚠️ {total - passed} final response length tests failed.")
        return False

if __name__ == "__main__":
    success = run_final_response_length_test()
    sys.exit(0 if success else 1)
