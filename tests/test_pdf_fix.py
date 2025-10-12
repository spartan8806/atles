#!/usr/bin/env python3
"""
Test PDF Function Fix

Test if ATLES can now actually read PDFs after installing dependencies.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_pdf_function():
    """Test the PDF reading function"""
    
    print("🧪 TESTING PDF FUNCTION")
    print("=" * 40)
    
    try:
        from atles.ollama_client_enhanced import OllamaFunctionCaller
        
        client = OllamaFunctionCaller()
        
        # Check if function is registered
        if 'read_pdf' not in client.available_functions:
            print("❌ read_pdf function not registered")
            return False
        
        print("✅ read_pdf function is registered")
        
        # Test with the arXiv URL
        test_url = "https://arxiv.org/pdf/2112.09332"
        print(f"Testing URL: {test_url}")
        
        result = client.execute_function('read_pdf', {'url': test_url})
        
        if result['success']:
            pdf_data = result['result']
            print(f"✅ PDF read successfully!")
            print(f"   Pages: {pdf_data.get('num_pages', 'Unknown')}")
            print(f"   Characters: {pdf_data.get('total_chars', 'Unknown')}")
            
            # Show preview
            preview = pdf_data.get('text_preview', 'No preview')
            print(f"   Preview: {preview[:100]}...")
            
            # Check if it contains expected content
            full_text = pdf_data.get('text', '')
            if 'WebGPT' in full_text or 'GPT' in full_text:
                print("✅ PDF contains expected content (WebGPT/GPT)")
            else:
                print("⚠️ PDF content may not be correct")
            
            return True
        else:
            print(f"❌ PDF reading failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_function_call_execution():
    """Test if FUNCTION_CALL format actually executes"""
    
    print(f"\n🎯 TESTING FUNCTION_CALL EXECUTION")
    print("=" * 40)
    
    try:
        from atles.ollama_client_enhanced import OllamaFunctionCaller
        
        client = OllamaFunctionCaller()
        
        # Simulate what happens when ATLES generates a function call
        response_text = 'FUNCTION_CALL:read_pdf:{"url": "https://arxiv.org/pdf/2112.09332"}'
        
        print(f"Testing response: {response_text}")
        
        # This should execute the function call
        result = client.handle_function_call(response_text)
        
        if "Successfully extracted text" in result or "Pages:" in result:
            print("✅ FUNCTION_CALL format executes correctly")
            print(f"   Result preview: {result[:100]}...")
            return True
        else:
            print("❌ FUNCTION_CALL format not executing")
            print(f"   Result: {result[:100]}...")
            return False
            
    except Exception as e:
        print(f"❌ Function call test failed: {e}")
        return False

def test_constitutional_interference():
    """Test if constitutional client interferes with PDF calls"""
    
    print(f"\n🛡️ TESTING CONSTITUTIONAL INTERFERENCE")
    print("=" * 40)
    
    try:
        from atles.constitutional_client import ConstitutionalOllamaClient
        from atles.ollama_client_enhanced import OllamaFunctionCaller
        
        base_client = OllamaFunctionCaller()
        constitutional_client = ConstitutionalOllamaClient(base_client)
        
        # Test if constitutional client blocks PDF function calls
        test_prompt = "User wants to read a PDF from https://arxiv.org/pdf/2112.09332"
        test_response = 'FUNCTION_CALL:read_pdf:{"url": "https://arxiv.org/pdf/2112.09332"}'
        
        should_execute, reason = constitutional_client.validator.should_execute_function_call(
            test_prompt, test_response
        )
        
        if should_execute:
            print("✅ Constitutional client allows PDF function calls")
            return True
        else:
            print(f"❌ Constitutional client blocks PDF calls: {reason}")
            return False
            
    except Exception as e:
        print(f"❌ Constitutional test failed: {e}")
        return False

def main():
    """Main test runner"""
    
    print("🔧 PDF READING FIX TEST")
    print("=" * 50)
    
    print("""
TESTING THE CORE ISSUES:
1. Can ATLES actually read PDFs now?
2. Does FUNCTION_CALL format execute properly?
3. Is constitutional client interfering?
    """)
    
    results = []
    results.append(test_pdf_function())
    results.append(test_function_call_execution())
    results.append(test_constitutional_interference())
    
    # Summary
    print(f"\n📊 TEST RESULTS")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print(f"\n🎉 PDF READING IS FIXED!")
        print("✅ Dependencies installed correctly")
        print("✅ PDF function executes properly")
        print("✅ FUNCTION_CALL format works")
        print("✅ Constitutional client allows PDF calls")
        
        print(f"\n💡 ATLES should now be able to:")
        print("- Actually read PDF content from URLs")
        print("- Execute FUNCTION_CALL:read_pdf commands")
        print("- Provide real content analysis instead of evasive responses")
        
    elif passed >= 1:
        print(f"\n⚠️ PARTIAL SUCCESS")
        print("Some functionality is working, but issues remain.")
        
        if not results[0]:
            print("❌ Core PDF reading still broken")
        if not results[1]:
            print("❌ Function call execution still broken")
        if not results[2]:
            print("❌ Constitutional client still blocking calls")
            
    else:
        print(f"\n❌ PDF READING STILL BROKEN")
        print("All tests failed - more investigation needed.")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print(f"\n✨ PDF reading functionality is now working!")
        else:
            print(f"\n⚠️ PDF reading still has issues.")
    except KeyboardInterrupt:
        print(f"\n⏹️ Test interrupted")
    except Exception as e:
        print(f"\n💥 Test error: {e}")
        import traceback
        traceback.print_exc()
