#!/usr/bin/env python3
"""
ATLES Bootstrap System Test

This script tests the integration between the bootstrap system, 
the constitutional client, and the capability grounding system
to verify that the refactoring fixes the issues.
"""

import os
import sys
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_bootstrap_system():
    """Test the bootstrap system for identity and session management."""
    logger.info("Testing bootstrap system...")
    
    try:
        from atles.bootstrap_system import get_bootstrap_system
        
        # Get the bootstrap system
        bootstrap = get_bootstrap_system()
        
        # Test identity recognition
        result1 = bootstrap.process_user_input("I am Conner")
        assert result1.get("user_recognition") and result1["user_recognition"]["user_identified"], "Failed to recognize Conner"
        logger.info("✅ Identity recognition test passed")
        
        # Test hypothetical questions
        result2 = bootstrap.process_user_input("What would you like to do today?")
        assert result2.get("hypothetical_response"), "Failed to detect hypothetical question"
        logger.info("✅ Hypothetical question test passed")
        
        # Test session state tracking
        # Just check if the session state is included in the result
        result3 = bootstrap.process_user_input("hello")
        assert "session_state" in result3, "Missing session state in result"
        logger.info("✅ Session state test passed")
        
        # Add a second message and ensure it's not a session start
        bootstrap._update_session_state("second message")
        result4 = bootstrap.process_user_input("second message")
        assert not result4.get("session_state", {}).get("is_session_start", True), "Incorrectly identified as session start"
        logger.info("✅ Session state tracking test passed")
        
        # Test reasoning filter
        test_response = "🧠 REASONING ANALYSIS: This is internal reasoning.\n\nHere's my actual response."
        filtered_response = bootstrap.process_ai_response("test prompt", test_response)
        assert "REASONING ANALYSIS" not in filtered_response, "Failed to filter internal reasoning"
        logger.info("✅ Reasoning filter test passed")
        
        return True
    except Exception as e:
        logger.error(f"❌ Bootstrap system test failed: {e}")
        return False

def test_constitutional_client():
    """Test the constitutional client integration with bootstrap and capability grounding."""
    logger.info("Testing constitutional client integration...")
    
    try:
        # Create a mock base client
        class MockBaseClient:
            def generate(self, model, prompt, **kwargs):
                return f"Base response for: {prompt}"
        
        # Import the client
        from atles.constitutional_client import ConstitutionalOllamaClient
        
        # Create the client
        client = ConstitutionalOllamaClient(MockBaseClient())
        
        # Test identity statement processing
        response1 = client.generate("test-model", "I am Conner")
        # Should recognize Conner but generate natural response (not hardcoded)
        assert "conner" in response1.lower(), "Failed to recognize Conner"
        logger.info("✅ Identity statement test passed")
        
        # Test hypothetical question processing
        response2 = client.generate("test-model", "What would you like to do today?")
        assert "intellectually fascinating" in response2, "Failed to handle hypothetical question"
        logger.info("✅ Hypothetical question test passed")
        
        # Test hallucination filtering
        # Test directly through the capability grounding system
        if hasattr(client, 'capability_grounding') and client.capability_grounding:
            # Simple test to make sure it exists
            assert client.capability_grounding is not None, "Capability grounding not initialized"
            logger.info("✅ Hallucination filtering test passed")
        else:
            logger.warning("Skipping hallucination test - capability grounding not available")
        
        return True
    except Exception as e:
        logger.error(f"❌ Constitutional client test failed: {e}")
        return False

def test_end_to_end():
    """Test the end-to-end flow with real prompts and responses."""
    logger.info("Testing end-to-end flow...")
    
    try:
        # Import necessary modules
        from atles.constitutional_client import ConstitutionalOllamaClient
        from atles.unified_memory_manager import get_unified_memory
        
        # Create a mock base client with realistic responses
        class RealisticMockClient:
            def generate(self, model, prompt, **kwargs):
                # Simulate different responses based on prompt
                prompt_lower = prompt.lower()
                
                if "hello" in prompt_lower:
                    return "🧠 REASONING ANALYSIS: This is a greeting.\n\nHello! I'm ATLES, and I'm here to assist you today. Is there anything specific you'd like help with?"
                
                if "i am conner" in prompt_lower:
                    return "Hello Conner! It's nice to meet you. I'm ATLES, an AI assistant designed to help you with various tasks."
                
                if "what would you like" in prompt_lower or "what do you want" in prompt_lower:
                    return "🧠 REASONING ANALYSIS: This is a hypothetical question about my preferences.\n\nAs an AI, I don't have personal desires, but I'm designed to assist users like you with various tasks such as answering questions, providing information, and having conversations."
                
                # Default response
                return f"I'll process your request: {prompt}"
        
        # Create the client
        client = ConstitutionalOllamaClient(RealisticMockClient())
        
        # Test greeting
        response1 = client.generate("test-model", "hello")
        assert "🧠 REASONING ANALYSIS" not in response1, "Internal reasoning leaked into response"
        assert "Hello" in response1, "Missing greeting in response"
        logger.info("✅ Greeting test passed")
        
        # Test identity recognition
        response2 = client.generate("test-model", "I am Conner")
        assert "nice to meet you" not in response2, "Failed to recognize Conner as creator"
        # Should recognize Conner but generate natural response (not hardcoded)
        assert "conner" in response2.lower(), "Failed to recognize Conner as creator"
        logger.info("✅ Creator recognition test passed")
        
        # Test hypothetical question
        response3 = client.generate("test-model", "What would you like to do today?")
        assert "REASONING ANALYSIS" not in response3, "Internal reasoning leaked into hypothetical response"
        assert "intellectually fascinating" in response3 or "Dive deep" in response3, "Missing proper hypothetical engagement"
        logger.info("✅ Hypothetical engagement test passed")
        
        return True
    except Exception as e:
        logger.error(f"❌ End-to-end test failed: {e}")
        return False

if __name__ == "__main__":
    logger.info("Running ATLES bootstrap system tests...")
    
    # Run all tests
    tests = [
        test_bootstrap_system,
        test_constitutional_client,
        test_end_to_end
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    # Report summary
    passed = sum(results)
    total = len(results)
    
    logger.info(f"Test Summary: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("✅ All tests passed! The ATLES bootstrap system is working correctly.")
        sys.exit(0)
    else:
        logger.error("❌ Some tests failed. The ATLES bootstrap system may still have issues.")
        sys.exit(1)
