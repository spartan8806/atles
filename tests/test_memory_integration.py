#!/usr/bin/env python3
"""
Test Memory Integration
This script tests the integration between the unified memory system, 
the constitutional client, and the desktop application to verify that
the fixes work correctly.
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

def test_unified_memory_singleton():
    """Test that the unified memory manager is truly a singleton."""
    logger.info("Testing unified memory singleton pattern...")
    
    try:
        from atles.unified_memory_manager import UnifiedMemoryManager, get_unified_memory
        
        # Get two instances using different methods
        manager1 = UnifiedMemoryManager()
        manager2 = get_unified_memory()
        
        # They should be the same object
        assert manager1 is manager2, "Unified memory manager is not a singleton!"
        logger.info("✅ Unified memory singleton test passed")
        return True
    except Exception as e:
        logger.error(f"❌ Unified memory singleton test failed: {e}")
        return False

def test_memory_principle_response():
    """Test that principle-based responses work correctly for simple greetings."""
    logger.info("Testing principle-based responses...")
    
    try:
        # Import necessary modules
        from atles.constitutional_client import ConstitutionalOllamaClient
        
        # Create a mock base client
        class MockBaseClient:
            def generate(self, model, prompt, **kwargs):
                return f"Base response for: {prompt}"
        
        # Create the constitutional client
        client = ConstitutionalOllamaClient(MockBaseClient())
        
        # Test a simple greeting
        response = client.generate("test-model", "hello")
        
        # Should be a proper greeting, not a principles message
        assert "I'll apply the relevant principles" not in response, "Simple greeting still shows principles message!"
        assert "Hello" in response, "Simple greeting doesn't return a proper greeting!"
        
        logger.info("✅ Principle response test passed")
        return True
    except Exception as e:
        logger.error(f"❌ Principle response test failed: {e}")
        return False

def test_desktop_memory_integration():
    """Test that the desktop app uses the unified memory system correctly."""
    logger.info("Testing desktop memory integration...")
    
    try:
        # Import necessary modules
        from atles.unified_memory_manager import get_unified_memory
        
        # Get the singleton memory manager
        unified_memory = get_unified_memory()
        
        # Import the ConversationMemoryManager
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from atles_desktop_pyqt import ConversationMemoryManager
        
        # Create the conversation memory manager
        memory_manager = ConversationMemoryManager()
        
        # Verify it's using the unified memory system
        assert memory_manager.unified_memory is unified_memory, "Desktop app is not using the unified memory singleton!"
        assert memory_manager.memory_integration is unified_memory.memory_integration, "Desktop app has a separate memory_integration instance!"
        
        logger.info("✅ Desktop memory integration test passed")
        return True
    except Exception as e:
        logger.error(f"❌ Desktop memory integration test failed: {e}")
        return False

def test_full_integration():
    """Test that all components work together correctly."""
    logger.info("Testing full integration...")
    
    try:
        # Get the unified memory singleton
        from atles.unified_memory_manager import get_unified_memory
        unified_memory = get_unified_memory()
        
        # Start a session
        session_id = unified_memory.start_conversation_session()
        logger.info(f"Started session: {session_id}")
        
        # Add test messages
        unified_memory.add_message("User", "hello")
        unified_memory.add_message("ATLES", "Hello! How can I assist you today?")
        
        # Process with memory
        result = unified_memory.process_user_prompt_with_memory("What did I just say?")
        assert result.get("memory_enhanced", False), "Memory enhancement not working!"
        
        # End the session
        episode_id = unified_memory.end_conversation_session()
        logger.info(f"Ended session, created episode: {episode_id}")
        
        logger.info("✅ Full integration test passed")
        return True
    except Exception as e:
        logger.error(f"❌ Full integration test failed: {e}")
        return False

if __name__ == "__main__":
    logger.info("Running memory integration tests...")
    
    # Run all tests
    tests = [
        test_unified_memory_singleton,
        test_memory_principle_response,
        test_desktop_memory_integration,
        test_full_integration
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    # Report summary
    passed = sum(results)
    total = len(results)
    
    logger.info(f"Test Summary: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("✅ All tests passed! The memory integration is working correctly.")
        sys.exit(0)
    else:
        logger.error("❌ Some tests failed. The memory integration may still have issues.")
        sys.exit(1)
