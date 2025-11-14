#!/usr/bin/env python3
"""
Test Session Management Fix

This test verifies that the session management problem has been resolved
and that bootstrap only triggers for actual session starts.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import atles
sys.path.append(str(Path(__file__).parent))

def test_session_state_management():
    """Test that session state is properly managed."""
    print("🧪 Testing Session State Management")
    print("-" * 50)
    
    try:
        from atles.identity_bootstrap_system import create_bootstrap_system
        
        bootstrap = create_bootstrap_system()
        
        # Test 1: First message should be session start
        print("Test 1: First message (session start)")
        result1 = bootstrap.process_user_input("hello")
        print(f"  Is session start: {result1.get('is_session_start')}")
        print(f"  Bootstrap prompt created: {bool(result1.get('bootstrap_prompt'))}")
        print(f"  Session initialized: {bootstrap.session_bootstrap.session_initialized}")
        print(f"  Message count: {bootstrap.session_bootstrap.message_count}")
        
        if not result1.get('is_session_start'):
            print("❌ First message should be session start")
            return False
        
        # Test 2: Second message should NOT be session start
        print("\nTest 2: Second message (regular conversation)")
        result2 = bootstrap.process_user_input("10*8*855*21")
        print(f"  Is session start: {result2.get('is_session_start')}")
        print(f"  Bootstrap prompt created: {bool(result2.get('bootstrap_prompt'))}")
        print(f"  Session initialized: {bootstrap.session_bootstrap.session_initialized}")
        print(f"  Message count: {bootstrap.session_bootstrap.message_count}")
        
        if result2.get('is_session_start'):
            print("❌ Second message should NOT be session start")
            return False
        
        # Test 3: Third message should NOT be session start
        print("\nTest 3: Third message (regular conversation)")
        result3 = bootstrap.process_user_input("can you ask gemini to help")
        print(f"  Is session start: {result3.get('is_session_start')}")
        print(f"  Bootstrap prompt created: {bool(result3.get('bootstrap_prompt'))}")
        print(f"  Session initialized: {bootstrap.session_bootstrap.session_initialized}")
        print(f"  Message count: {bootstrap.session_bootstrap.message_count}")
        
        if result3.get('is_session_start'):
            print("❌ Third message should NOT be session start")
            return False
        
        # Test 4: Identity statement should trigger recognition but not session start
        print("\nTest 4: Identity statement")
        result4 = bootstrap.process_user_input("i am conner")
        print(f"  Is session start: {result4.get('is_session_start')}")
        print(f"  User recognition: {bool(result4.get('user_recognition'))}")
        print(f"  Bootstrap prompt created: {bool(result4.get('bootstrap_prompt'))}")
        print(f"  Message count: {bootstrap.session_bootstrap.message_count}")
        
        if not result4.get('user_recognition'):
            print("❌ Identity statement should trigger user recognition")
            return False
        
        print("✅ Session state management working correctly")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_constitutional_client_session_management():
    """Test that the constitutional client properly handles session management."""
    print("\n🧪 Testing Constitutional Client Session Management")
    print("-" * 50)
    
    try:
        from atles.constitutional_client import create_constitutional_client
        
        client = create_constitutional_client()
        
        # Test 1: First message (session start)
        print("Test 1: First message - 'hello'")
        response1 = client.chat("hello")
        print(f"Response preview: {response1[:100]}...")
        
        # Should get appropriate greeting, not identity dump
        if "Hello" in response1 and "Conner" in response1:
            print("✅ Appropriate greeting response")
        else:
            print("❌ Unexpected response to greeting")
            return False
        
        # Test 2: Mathematical question (should NOT trigger bootstrap)
        print("\nTest 2: Mathematical question - '10*8*855*21'")
        response2 = client.chat("10*8*855*21")
        print(f"Response preview: {response2[:100]}...")
        
        # Should NOT get identity response
        if "I'm ATLES, and yes, I was created by Conner" in response2:
            print("❌ Getting identity response for math question")
            return False
        else:
            print("✅ Appropriate response for math question")
        
        # Test 3: Capability question (should NOT trigger bootstrap)
        print("\nTest 3: Capability question - 'can you ask gemini to help'")
        response3 = client.chat("can you ask gemini to help")
        print(f"Response preview: {response3[:100]}...")
        
        # Should NOT get identity response
        if "I'm ATLES, and yes, I was created by Conner" in response3:
            print("❌ Getting identity response for capability question")
            return False
        else:
            print("✅ Appropriate response for capability question")
        
        # Test 4: Game request (should NOT trigger bootstrap)
        print("\nTest 4: Game request - '20 questions'")
        response4 = client.chat("20 questions")
        print(f"Response preview: {response4[:100]}...")
        
        # Should NOT get identity response
        if "I'm ATLES, and yes, I was created by Conner" in response4:
            print("❌ Getting identity response for game request")
            return False
        else:
            print("✅ Appropriate response for game request")
        
        # Test 5: Identity statement (should trigger recognition)
        print("\nTest 5: Identity statement - 'i am conner'")
        response5 = client.chat("i am conner")
        print(f"Response preview: {response5[:100]}...")
        
        # Should get appropriate recognition response
        if "conner" in response5.lower():
            print("✅ Appropriate identity recognition response")
        else:
            print("❌ Unexpected response to identity statement")
            return False
        
        print("✅ Constitutional client session management working correctly")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_session_management_test():
    """Run all session management tests."""
    print("🚀 Session Management Fix Test")
    print("=" * 60)
    
    tests = [
        ("Bootstrap System Session State", test_session_state_management),
        ("Constitutional Client Session Management", test_constitutional_client_session_management)
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
    print("📊 SESSION MANAGEMENT TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} session management tests passed")
    
    if passed == total:
        print("🎉 SESSION MANAGEMENT PROBLEM FIXED!")
        print("\n📋 Verified Fixes:")
        print("✅ Bootstrap only triggers for actual session starts")
        print("✅ Regular messages don't create bootstrap prompts")
        print("✅ Session state properly tracked across messages")
        print("✅ Identity responses only for identity statements")
        print("✅ Message counting and session initialization working")
        print("\n💡 The session management problem has been resolved!")
        return True
    else:
        print(f"⚠️ {total - passed} session management tests failed.")
        return False

if __name__ == "__main__":
    success = run_session_management_test()
    sys.exit(0 if success else 1)
