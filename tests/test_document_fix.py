#!/usr/bin/env python3
"""
Quick test to verify document generation with new model name
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'atles'))

from document_generation_system import DocumentGenerationSystem, DocumentRequest, DocumentType, Priority

def test_document_generation():
    print("Testing document generation with atles-qwen2.5:7b-enhanced...")
    
    # Initialize document system
    doc_system = DocumentGenerationSystem()
    
    # Create a simple test request
    request = DocumentRequest(
        title="System Status Test",
        document_type=DocumentType.REPORT,
        priority=Priority.MEDIUM,
        description="Test document to verify model integration"
    )
    
    print(f"Creating document request: {request.title}")
    
    # Submit request
    request_id = doc_system.submit_request(request)
    print(f"Request submitted with ID: {request_id}")
    
    # Check status
    status = doc_system.get_request_status(request_id)
    print(f"Request status: {status}")
    
    print("Test completed - check atles_generated_documents/ for output")

if __name__ == "__main__":
    test_document_generation()
