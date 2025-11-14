#!/usr/bin/env python3
"""
Test Document Generation System

Simple test to verify the document generation and inter-system communication works.
"""

import asyncio
import sys
import os
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from atles.document_generation_system import create_document_generation_system, DocumentType, Priority


async def test_document_generation():
    """Test document generation system"""
    
    print("🧪 Testing ATLES Document Generation System")
    print("=" * 50)
    
    # Create document system
    doc_system = create_document_generation_system("test_system")
    
    # Start the system
    await doc_system.start()
    print("✅ Document system started")
    
    # Create a test document request
    request_id = await doc_system.create_document_request(
        requester_system="test_client",
        document_type=DocumentType.KNOWLEDGE_BASE_ENTRY,
        title="ATLES System Overview",
        description="A comprehensive overview of the ATLES autonomous AI system, including its capabilities, architecture, and key features.",
        requirements={
            "style": "educational",
            "length": "medium",
            "include_examples": True
        },
        priority=Priority.HIGH
    )
    
    print(f"📄 Created document request: {request_id}")
    
    # Wait for processing
    print("⏳ Waiting for document generation...")
    
    # Check status periodically
    for i in range(10):  # Wait up to 10 seconds
        await asyncio.sleep(1)
        
        status = await doc_system.get_request_status(request_id)
        if status:
            print(f"   Status: {status['status']} - Progress: {status['progress']:.1f}%")
            
            if status['status'] == 'completed':
                print("✅ Document generation completed!")
                break
            elif status['status'] == 'failed':
                print("❌ Document generation failed!")
                break
    
    # List completed documents
    documents = await doc_system.list_documents()
    print(f"\n📚 Generated {len(documents)} documents:")
    
    for doc in documents:
        print(f"   • {doc['title']}")
        print(f"     Type: {doc['document_type']}")
        print(f"     Words: {doc['word_count']}")
        print(f"     Quality: {doc['quality_score']:.2f}")
        print(f"     File: {doc['file_path']}")
        
        # Try to read the document
        try:
            with open(doc['file_path'], 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"\n📄 DOCUMENT CONTENT PREVIEW:")
            print("-" * 40)
            print(content[:300] + "..." if len(content) > 300 else content)
            print("-" * 40)
            
        except Exception as e:
            print(f"   ❌ Could not read document: {e}")
    
    # Get system status
    status = doc_system.get_system_status()
    print(f"\n🔧 System Status:")
    print(f"   Running: {status['is_running']}")
    print(f"   Active Requests: {status['active_requests']}")
    print(f"   Completed Documents: {status['completed_documents']}")
    print(f"   Total Generated: {status['total_generated']}")
    
    # Stop the system
    await doc_system.stop()
    print("\n✅ Document system stopped")
    
    print("\n🎉 Document generation test completed!")


def main():
    """Main entry point"""
    
    print("Testing ATLES Document Generation System...")
    
    try:
        asyncio.run(test_document_generation())
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
