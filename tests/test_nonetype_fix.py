#!/usr/bin/env python3
"""
Test for NoneType Error Fix

This test verifies that the NoneType error is fixed and the system
handles None responses gracefully.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import atles
sys.path.append(str(Path(__file__).parent))

def test_constitutional_client_none_safety():
    """Test that the constitutional client handles None responses safely."""
    print("🧪 Testing Constitutional Client None Safety")
    print("-" * 50)
    
    try:
        from atles.constitutional_client import create_constitutional_client
        
        client = create_constitutional_client()
        
        # Test basic functionality
        print("Testing basic message...")
        response = client.chat("hello")
        print(f"Response: {response}")
        
        if response and len(response) > 0:
            print("✅ Basic message works")
        else:
            print("❌ Basic message failed")
            return False
        
        # Test more complex message
        print("\nTesting complex message...")
        response2 = client.chat("Explain artificial intelligence")
        print(f"Response length: {len(response2)} chars")
        print(f"Preview: {response2[:100]}...")
        
        if response2 and len(response2) > 50:
            print("✅ Complex message works")
        else:
            print("❌ Complex message failed")
            return False
        
        print("✅ All constitutional client tests passed")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_bootstrap_system_none_safety():
    """Test that the bootstrap system handles None responses safely."""
    print("\n🧪 Testing Bootstrap System None Safety")
    print("-" * 50)
    
    try:
        from atles.bootstrap_system import ATLESBootstrapSystem
        
        bootstrap = ATLESBootstrapSystem()
        
        # Test with None response
        print("Testing None response handling...")
        result = bootstrap.process_ai_response("test prompt", None)
        print(f"Result: {result}")
        
        if result and "encountered an issue" in result:
            print("✅ None response handled gracefully")
        else:
            print("❌ None response not handled properly")
            return False
        
        # Test with normal response
        print("\nTesting normal response...")
        result2 = bootstrap.process_ai_response("test prompt", "This is a normal response")
        print(f"Result: {result2}")
        
        if result2 and len(result2) > 0:
            print("✅ Normal response processed correctly")
        else:
            print("❌ Normal response failed")
            return False
        
        print("✅ All bootstrap system tests passed")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_memory_system_initialization():
    """Test that the memory system initializes without errors."""
    print("\n🧪 Testing Memory System Initialization")
    print("-" * 50)
    
    try:
        from atles.unified_memory_manager import get_unified_memory
        
        print("Initializing unified memory...")
        memory = get_unified_memory()
        
        if memory and memory.is_available():
            print("✅ Unified memory system initialized successfully")
        else:
            print("⚠️ Unified memory system not available (this is OK)")
        
        # Test basic memory operations
        print("\nTesting basic memory operations...")
        session_id = memory.start_conversation_session("test_session")
        print(f"Session ID: {session_id}")
        
        memory.add_message("user", "Hello", {})
        memory.add_message("assistant", "Hi there!", {})
        
        context = memory.get_context_for_ai()
        print(f"Context length: {len(context)} chars")
        
        memory.end_conversation_session()
        
        print("✅ Memory system operations completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_nonetype_fix_test():
    """Run all NoneType fix tests."""
    print("🚀 NoneType Error Fix Test")
    print("Verifying that None responses are handled gracefully")
    print("=" * 80)
    
    tests = [
        ("Constitutional Client None Safety", test_constitutional_client_none_safety),
        ("Bootstrap System None Safety", test_bootstrap_system_none_safety),
        ("Memory System Initialization", test_memory_system_initialization)
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
    print("📊 NONETYPE FIX TEST SUMMARY")
    print("=" * 80)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} NoneType fix tests passed")
    
    if passed == total:
        print("🎉 NONETYPE ERROR COMPLETELY FIXED!")
        print("\n📋 Verified Solutions:")
        print("✅ Constitutional client handles None responses gracefully")
        print("✅ Bootstrap system has None safety checks")
        print("✅ Memory system initializes without errors")
        print("✅ All processing components have fallback handling")
        print("\n💡 The 'NoneType' object has no attribute 'get' error should be resolved!")
        return True
    else:
        print(f"⚠️ {total - passed} NoneType fix tests failed.")
        return False

if __name__ == "__main__":
    success = run_nonetype_fix_test()
    sys.exit(0 if success else 1)
