"""
Test PDF Reading Capability

This script tests the new PDF reading functionality in ATLES.
"""

import sys
import logging
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

def test_pdf_reading():
    """Test the PDF reading functionality"""
    
    try:
        from atles.ollama_client_enhanced import OllamaFunctionCaller
        
        # Initialize client
        client = OllamaFunctionCaller(debug_mode=True)
        
        print("\n===== PDF Reading Capability Test =====\n")
        
        # Check if PDF reading is available
        print("Checking if PDF reading capability is available...")
        
        # Try to access the read_pdf method
        if hasattr(client, 'read_pdf'):
            print("✅ PDF reading capability is registered")
            
            # Test PDF reading with sample URL
            sample_url = "https://arxiv.org/pdf/2212.08073.pdf"  # WebGPT research paper
            print(f"\nTesting PDF reading with URL: {sample_url}")
            
            # Call the function directly
            result = client.read_pdf(sample_url)
            
            print("\nFunction Result:")
            print(json.dumps(result, indent=2)[:1000] + "...")  # Truncate output for readability
            
            # Test via function call handling
            print("\nTesting function call handling:")
            function_call_text = f'FUNCTION_CALL:read_pdf:{{"url": "{sample_url}"}}'
            
            response = client.handle_function_call(function_call_text)
            print(f"Response: {response[:500]}...")  # Truncate output
            
            return True
        else:
            print("❌ PDF reading capability is not available")
            print("Required dependencies may be missing. Install with: pip install pdfplumber requests")
            return False
            
    except ImportError as e:
        print(f"❌ Error importing modules: {e}")
        print("Make sure you have the required packages installed:")
        print("pip install pdfplumber requests")
        return False
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

if __name__ == "__main__":
    print("Starting PDF reading capability test...")
    success = test_pdf_reading()
    print(f"\nTest {'passed' if success else 'failed'}")
    sys.exit(0 if success else 1)
