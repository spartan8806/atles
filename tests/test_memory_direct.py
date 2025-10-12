#!/usr/bin/env python3
"""
Direct test of memory search to debug the 0 results issue
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_direct_memory():
    print("🔍 Testing Direct Memory Search...")
    
    try:
        # Test the exact same path as the desktop app
        from atles.unified_memory_manager import UnifiedMemoryManager
        
        memory_manager = UnifiedMemoryManager("desktop_user")
        print(f"✅ Memory manager initialized")
        
        # Test the exact query from the logs
        query = "Do you remember our previous conversations"
        print(f"🔍 Testing query: '{query}'")
        
        result = memory_manager.process_user_prompt_with_memory(query)
        print(f"📊 Result: {result}")
        
        # Also test the memory integration directly
        if hasattr(memory_manager, '_memory_integration'):
            print("🔍 Testing memory integration directly...")
            search_results = memory_manager._memory_integration.search_memories(query, max_results=5)
            print(f"📊 Direct search results: {len(search_results)} found")
            
            for i, result in enumerate(search_results[:2]):
                print(f"   [{i+1}] {result}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct_memory()
