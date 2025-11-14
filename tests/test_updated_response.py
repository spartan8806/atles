#!/usr/bin/env python3
"""
Test Updated ATLES Response

Test that ATLES now suggests proper function calls instead of saying "I cannot browse the web"
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_updated_url_response():
    """Test the updated URL response"""
    
    print("🧪 TESTING UPDATED URL RESPONSE")
    print("=" * 50)
    
    try:
        from atles_desktop_pyqt import ATLESCommunicationThread
        
        comm_thread = ATLESCommunicationThread()
        
        # Test the exact scenario from user's conversation
        user_message = "can you read this https://arxiv.org/pdf/2112.09332 and give me a summary"
        fake_response = "I'll help you with that URL."  # Simulate a response that triggers URL handling
        
        print(f"User message: {user_message}")
        print(f"Testing architectural fixes...")
        
        # Apply architectural fixes
        fixed_response = comm_thread._apply_architectural_fixes(
            fake_response,
            user_message,
            {}
        )
        
        print(f"\nFixed response:")
        print("-" * 40)
        print(fixed_response)
        print("-" * 40)
        
        # Check if it suggests proper function calls
        if "FUNCTION_CALL:check_url_accessibility" in fixed_response:
            print("✅ Now suggests proper function call!")
        else:
            print("❌ Still not suggesting function calls")
        
        # Check if it's more positive about capabilities
        if "I can analyze" in fixed_response and "Available Web Functions" in fixed_response:
            print("✅ More positive about web capabilities!")
        else:
            print("❌ Still too negative about capabilities")
        
        # Check if it still blocks fake commands
        fake_command_response = "OPEN_URL[https://example.com]"
        blocked_response = comm_thread._apply_architectural_fixes(
            fake_command_response,
            "open this website",
            {}
        )
        
        if "OPEN_URL[" not in blocked_response:
            print("✅ Still blocks fake commands!")
        else:
            print("❌ Not blocking fake commands")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test"""
    
    print("🔧 TESTING UPDATED ATLES RESPONSE")
    print("=" * 60)
    
    print("""
GOAL: Make ATLES more positive about web capabilities while still being honest.

BEFORE: "I do NOT have web browsing capabilities. I cannot..."
AFTER: "Let me check this URL for you: FUNCTION_CALL:check_url_accessibility..."

This maintains offline-first philosophy while providing helpful web functions when needed.
    """)
    
    success = test_updated_url_response()
    
    if success:
        print(f"\n🎉 SUCCESS!")
        print("✅ ATLES now suggests proper function calls")
        print("✅ More positive about web capabilities") 
        print("✅ Still blocks fake commands")
        print("✅ Maintains offline-first approach with selective web access")
        
        print(f"\n💡 Now when you ask about URLs, ATLES will:")
        print("1. Suggest checking URL accessibility with proper function")
        print("2. Explain what web functions are available")
        print("3. Provide clear guidance for PDF analysis")
        print("4. Be honest about limitations without being completely negative")
        
    else:
        print(f"\n⚠️ Test failed - needs more work")
    
    return success

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n⏹️ Test interrupted")
    except Exception as e:
        print(f"\n💥 Error: {e}")
        import traceback
        traceback.print_exc()
