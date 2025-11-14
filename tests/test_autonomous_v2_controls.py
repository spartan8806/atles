#!/usr/bin/env python3
"""
Test ATLES Autonomous System V2 Start/Stop Controls

Simple test to verify the start/stop controls and asyncio integration work correctly.
"""

import asyncio
import sys
import os
import time
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from atles.document_generation_system import create_document_generation_system, DocumentType, Priority
    from atles.ollama_client_enhanced import OllamaFunctionCaller
except ImportError as e:
    print(f"❌ Failed to import ATLES components: {e}")
    sys.exit(1)


async def test_async_integration():
    """Test async integration without GUI"""
    
    print("🧪 Testing ATLES Autonomous V2 Async Integration")
    print("=" * 50)
    
    try:
        # Test 1: Create Ollama client
        print("📡 Testing Ollama client creation...")
        ollama_client = OllamaFunctionCaller()
        print("✅ Ollama client created successfully")
        
        # Test 2: Create document system
        print("📄 Testing document system creation...")
        doc_system = create_document_generation_system("test_autonomous", ollama_client)
        print("✅ Document system created successfully")
        
        # Test 3: Start document system
        print("🚀 Testing document system start...")
        await doc_system.start()
        print("✅ Document system started successfully")
        
        # Test 4: Check system status
        print("📊 Testing system status...")
        status = doc_system.get_system_status()
        print(f"   System ID: {status['system_id']}")
        print(f"   Running: {status['is_running']}")
        print(f"   Active Requests: {status['active_requests']}")
        print("✅ System status retrieved successfully")
        
        # Test 5: Create a test document request
        print("📝 Testing document request creation...")
        request_id = await doc_system.create_document_request(
            requester_system="test_client",
            document_type=DocumentType.TECHNICAL_REPORT,
            title="ATLES V2 System Test Report",
            description="A test document to verify the autonomous system functionality",
            requirements={"style": "technical", "length": "short"},
            priority=Priority.HIGH
        )
        print(f"✅ Document request created: {request_id}")
        
        # Test 6: Wait a moment for processing
        print("⏳ Waiting for document processing...")
        await asyncio.sleep(3)
        
        # Test 7: Check status again
        status = doc_system.get_system_status()
        print(f"📊 Updated status - Active Requests: {status['active_requests']}")
        
        # Test 8: Stop document system
        print("⏹ Testing document system stop...")
        await doc_system.stop()
        print("✅ Document system stopped successfully")
        
        # Test 9: Final status check
        status = doc_system.get_system_status()
        print(f"📊 Final status - Running: {status['is_running']}")
        
        print("\n🎉 All async integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Async integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_event_loop_management():
    """Test event loop management"""
    
    print("\n🔄 Testing Event Loop Management")
    print("=" * 50)
    
    try:
        # Test creating and managing event loops
        print("🔧 Testing event loop creation...")
        
        # Test 1: Check if we can create a new event loop
        try:
            loop = asyncio.get_event_loop()
            print("✅ Got existing event loop")
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            print("✅ Created new event loop")
        
        # Test 2: Run async function
        print("🚀 Testing async function execution...")
        result = loop.run_until_complete(test_async_integration())
        
        if result:
            print("✅ Event loop management test passed!")
            return True
        else:
            print("❌ Event loop management test failed!")
            return False
            
    except Exception as e:
        print(f"❌ Event loop management test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test entry point"""
    
    print("🧪 ATLES Autonomous System V2 - Control System Test")
    print("=" * 60)
    print("Testing start/stop controls and asyncio integration...")
    print()
    
    # Test event loop management
    success = test_event_loop_management()
    
    if success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Start/Stop controls should work correctly")
        print("✅ Asyncio integration is functional")
        print("✅ Document system can start/stop properly")
        print("✅ Event loop management is working")
        return 0
    else:
        print("\n❌ TESTS FAILED!")
        print("❌ There may be issues with the control system")
        return 1


if __name__ == "__main__":
    sys.exit(main())
