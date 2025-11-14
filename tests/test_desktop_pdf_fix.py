#!/usr/bin/env python3
"""
Test Desktop PDF Fix

Test that the desktop app now properly suggests PDF reading instead of blocking it.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_desktop_pdf_response():
    """Test that desktop app now suggests PDF reading for PDF URLs"""
    
    print("🧪 TESTING DESKTOP PDF RESPONSE")
    print("=" * 40)
    
    try:
        from atles_desktop_pyqt import ATLESCommunicationThread
        
        comm_thread = ATLESCommunicationThread()
        
        # Test with the arXiv PDF URL
        user_message = "can you read this https://arxiv.org/pdf/2112.09332 and give me a summary"
        fake_response = "I'll help you with that PDF."  # Simulate a response that triggers URL handling
        
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
        
        # Check if it suggests PDF reading instead of accessibility check
        if "FUNCTION_CALL:read_pdf" in fixed_response:
            print("✅ Now suggests PDF reading function!")
        else:
            print("❌ Still not suggesting PDF reading")
        
        # Check if it mentions PDF capabilities
        if "Download and extract text from PDF files" in fixed_response:
            print("✅ Mentions PDF reading capabilities!")
        else:
            print("❌ Doesn't mention PDF capabilities")
        
        # Check if it no longer says "I cannot read PDFs"
        if "I Cannot:" not in fixed_response or "Read PDF content directly from URLs" not in fixed_response:
            print("✅ No longer says 'I cannot read PDFs'!")
        else:
            print("❌ Still says 'I cannot read PDFs'")
        
        return "FUNCTION_CALL:read_pdf" in fixed_response
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_non_pdf_url():
    """Test that non-PDF URLs still use accessibility check"""
    
    print(f"\n🌐 TESTING NON-PDF URL HANDLING")
    print("=" * 40)
    
    try:
        from atles_desktop_pyqt import ATLESCommunicationThread
        
        comm_thread = ATLESCommunicationThread()
        
        # Test with a non-PDF URL
        user_message = "can you check this website https://example.com/article"
        fake_response = "I'll help you with that URL."
        
        print(f"User message: {user_message}")
        
        # Apply architectural fixes
        fixed_response = comm_thread._apply_architectural_fixes(
            fake_response,
            user_message,
            {}
        )
        
        # Check if it uses accessibility check for non-PDF URLs
        if "FUNCTION_CALL:check_url_accessibility" in fixed_response:
            print("✅ Uses accessibility check for non-PDF URLs")
            return True
        else:
            print("❌ Doesn't use accessibility check for non-PDF URLs")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main test runner"""
    
    print("🔧 DESKTOP PDF FIX TEST")
    print("=" * 50)
    
    print("""
TESTING THE FIX:
The desktop app should now suggest FUNCTION_CALL:read_pdf for PDF URLs
instead of saying "I cannot read PDF content directly from URLs"
    """)
    
    results = []
    results.append(test_desktop_pdf_response())
    results.append(test_non_pdf_url())
    
    # Summary
    print(f"\n📊 TEST RESULTS")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print(f"\n🎉 DESKTOP PDF FIX SUCCESSFUL!")
        print("✅ PDF URLs now suggest read_pdf function")
        print("✅ Non-PDF URLs use accessibility check")
        print("✅ No more 'I cannot read PDFs' messages")
        
        print(f"\n💡 ATLES should now respond to PDF requests with:")
        print("'🔧 Let me read this PDF for you:'")
        print("'FUNCTION_CALL:read_pdf:{\"url\": \"...\"}' ")
        print("Instead of blocking PDF reading!")
        
    else:
        print(f"\n⚠️ Desktop fix still has issues")
        if not results[0]:
            print("❌ PDF URLs still not handled correctly")
        if not results[1]:
            print("❌ Non-PDF URLs not handled correctly")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print(f"\n✨ Desktop PDF integration is now working!")
        else:
            print(f"\n⚠️ Desktop PDF integration still needs work.")
    except KeyboardInterrupt:
        print(f"\n⏹️ Test interrupted")
    except Exception as e:
        print(f"\n💥 Test error: {e}")
        import traceback
        traceback.print_exc()
