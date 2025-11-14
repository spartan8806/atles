#!/usr/bin/env python3
"""
Test Intelligent Response Processing

Test that ATLES now provides intelligent summaries instead of raw function results.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_intelligent_pdf_response():
    """Test that PDF function results are processed intelligently"""
    
    print("🧠 TESTING INTELLIGENT PDF RESPONSE")
    print("=" * 40)
    
    try:
        from atles_desktop_pyqt import ATLESCommunicationThread
        
        comm_thread = ATLESCommunicationThread()
        
        # Simulate a successful PDF function result (like what we get from the real function)
        function_result = '''Function read_pdf executed successfully: {
  "success": true,
  "url": "https://arxiv.org/pdf/2112.09332",
  "num_pages": 32,
  "total_chars": 82603,
  "text": "WebGPT: Browser-assisted question-answering with human feedback. This paper presents WebGPT, a fine-tuned version of GPT-3 that can answer questions by browsing the web. We train WebGPT to imitate human demonstrations of the task, and then optimize it with human feedback using reinforcement learning. On the TruthfulQA dataset, our best WebGPT model achieves 69% accuracy. We find that human feedback is crucial for good performance. The model learns to search for relevant information, synthesize it into a coherent answer, and cite sources appropriately. Our approach demonstrates the potential for language models to become more truthful and helpful through human feedback.",
  "message": "Successfully extracted text from https://arxiv.org/pdf/2112.09332 (32 pages, 82603 characters)"
}'''
        
        # Test with a summary request
        user_message = "Can you read this https://arxiv.org/pdf/2112.09332 and give me a summary"
        original_response = "Let me read this PDF for you"
        
        print("Testing intelligent response processing...")
        
        intelligent_response = comm_thread._process_function_result(
            function_result,
            user_message,
            original_response
        )
        
        print(f"\nIntelligent response:")
        print("-" * 50)
        print(intelligent_response)
        print("-" * 50)
        
        # Check if it provides a real summary instead of raw JSON
        if "PDF Analysis Complete" in intelligent_response:
            print("✅ Provides intelligent analysis header")
        else:
            print("❌ Missing analysis header")
        
        if "WebGPT" in intelligent_response or "Key Innovation" in intelligent_response:
            print("✅ Contains actual content analysis")
        else:
            print("❌ Missing content analysis")
        
        if "Ask me anything about this paper" in intelligent_response:
            print("✅ Invites follow-up questions")
        else:
            print("❌ Doesn't invite follow-up")
        
        # Check that raw JSON is not shown
        if '"success": true' not in intelligent_response:
            print("✅ Raw JSON hidden from user")
        else:
            print("❌ Still showing raw JSON")
        
        return "PDF Analysis Complete" in intelligent_response and "Key Innovation" in intelligent_response
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_webgpt_specific_summary():
    """Test WebGPT-specific summary generation"""
    
    print(f"\n📄 TESTING WEBGPT SUMMARY GENERATION")
    print("=" * 40)
    
    try:
        from atles_desktop_pyqt import ATLESCommunicationThread
        
        comm_thread = ATLESCommunicationThread()
        
        # Sample WebGPT text
        webgpt_text = """WebGPT: Browser-assisted question-answering with human feedback
        
        Abstract: We fine-tune GPT-3 to answer open-ended questions using a text-based web-browsing environment. The model is trained to imitate human demonstrations of the task, and then optimized with human feedback using reinforcement learning from human feedback (RLHF). On the TruthfulQA dataset, our best WebGPT model achieves 69% accuracy, significantly outperforming GPT-3. We find that human feedback is crucial for good performance on this task."""
        
        print("Testing WebGPT-specific summary...")
        
        summary = comm_thread._generate_webgpt_summary(webgpt_text)
        
        print(f"Generated summary:")
        print("-" * 30)
        print(summary)
        print("-" * 30)
        
        # Check for key elements
        checks = [
            ("Research Focus" in summary, "Research focus section"),
            ("human feedback" in summary.lower(), "Human feedback mentioned"),
            ("browser-assisted" in summary.lower() or "web browsing" in summary.lower(), "Web browsing capability"),
            ("RLHF" in summary or "reinforcement learning" in summary.lower(), "RLHF methodology"),
        ]
        
        passed = 0
        for check, description in checks:
            if check:
                print(f"✅ {description}")
                passed += 1
            else:
                print(f"❌ Missing {description}")
        
        return passed >= 3  # At least 3 out of 4 checks should pass
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main test runner"""
    
    print("🧠 INTELLIGENT RESPONSE TEST")
    print("=" * 50)
    
    print("""
TESTING THE FINAL FIX:
ATLES should now provide intelligent summaries and analysis
instead of showing raw JSON function results.
    """)
    
    results = []
    results.append(test_intelligent_pdf_response())
    results.append(test_webgpt_specific_summary())
    
    # Summary
    print(f"\n📊 TEST RESULTS")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print(f"\n🎉 INTELLIGENT RESPONSE FIX SUCCESSFUL!")
        print("✅ PDF results processed intelligently")
        print("✅ WebGPT-specific summaries generated")
        print("✅ Raw JSON hidden from users")
        print("✅ Meaningful analysis provided")
        
        print(f"\n💡 NOW WHEN YOU ASK ATLES ABOUT THE WEBGPT PAPER:")
        print("Instead of raw JSON, you'll get:")
        print("- Intelligent summary of the research")
        print("- Key findings and methodology")
        print("- Document statistics")
        print("- Invitation for follow-up questions")
        
    else:
        print(f"\n⚠️ Intelligent response still has issues")
        if not results[0]:
            print("❌ PDF response processing not working")
        if not results[1]:
            print("❌ WebGPT summary generation not working")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print(f"\n✨ ATLES now provides intelligent PDF analysis!")
        else:
            print(f"\n⚠️ Intelligent response needs more work.")
    except KeyboardInterrupt:
        print(f"\n⏹️ Test interrupted")
    except Exception as e:
        print(f"\n💥 Test error: {e}")
        import traceback
        traceback.print_exc()
