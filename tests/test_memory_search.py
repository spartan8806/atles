#!/usr/bin/env python3
"""
Test Memory Search Functionality

This script tests if the semantic index is working and episodes can be found.
"""

import sys
from pathlib import Path

# Add the atles directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_memory_search():
    """Test if memory search is working."""
    print("🧪 TESTING MEMORY SEARCH FUNCTIONALITY")
    print("=" * 50)
    
    try:
        from atles.episodic_semantic_memory import EpisodicSemanticMemory
        
        # Initialize memory system
        memory_path = Path("atles_memory")
        memory_system = EpisodicSemanticMemory(memory_path)
        
        print(f"📁 Memory system initialized")
        print(f"📊 Episodes path: {memory_system.episodes_path}")
        print(f"📊 Semantic index file: {memory_system.semantic_index_file}")
        
        # Check if semantic index file exists and has content
        if memory_system.semantic_index_file.exists():
            with open(memory_system.semantic_index_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.strip() == '{}':
                    print("❌ Semantic index is empty")
                    return False
                else:
                    print(f"✅ Semantic index has content ({len(content)} characters)")
        else:
            print("❌ Semantic index file doesn't exist")
            return False
        
        # Test search queries
        test_queries = [
            "remember",
            "memory", 
            "conversation",
            "What kinds of things",
            "math problem",
            "2+2"
        ]
        
        print("\n🔍 Testing search queries:")
        for query in test_queries:
            try:
                # Try to call the search method - need to find the right method name
                if hasattr(memory_system, 'search_episodes'):
                    results = memory_system.search_episodes(query, limit=3)
                elif hasattr(memory_system, 'query_episodes'):
                    results = memory_system.query_episodes(query, limit=3)
                elif hasattr(memory_system, 'search_memory'):
                    results = memory_system.search_memory(query, limit=3)
                else:
                    # Try to find the search method
                    methods = [method for method in dir(memory_system) if 'search' in method.lower() or 'query' in method.lower()]
                    print(f"  Available search methods: {methods}")
                    results = []
                
                print(f"  '{query}': {len(results)} results")
                
                if results:
                    for i, result in enumerate(results[:2]):
                        if hasattr(result, 'episode_id'):
                            print(f"    {i+1}. {result.episode_id}")
                        elif isinstance(result, dict):
                            print(f"    {i+1}. {result.get('episode_id', 'Unknown')}")
                        else:
                            print(f"    {i+1}. {type(result)}")
                            
            except Exception as e:
                print(f"  '{query}': Error - {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing memory system: {e}")
        return False

def check_semantic_index_content():
    """Check what's actually in the semantic index."""
    print("\n📋 CHECKING SEMANTIC INDEX CONTENT")
    print("-" * 40)
    
    try:
        import json
        
        index_file = Path("atles_memory/semantic_index.json")
        if not index_file.exists():
            print("❌ Semantic index file not found")
            return
        
        with open(index_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 Total episodes indexed: {len(data)}")
        
        if data:
            # Show first few episodes
            for i, (episode_id, episode_data) in enumerate(list(data.items())[:3]):
                print(f"\n📄 Episode {i+1}: {episode_id}")
                print(f"  Title: {episode_data.get('title', 'No title')}")
                print(f"  Summary: {episode_data.get('summary', 'No summary')[:100]}...")
                print(f"  Invoke keys: {episode_data.get('invoke_keys', [])[:5]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading semantic index: {e}")
        return False

if __name__ == "__main__":
    success = test_memory_search()
    check_semantic_index_content()
    
    if success:
        print("\n🎯 NEXT STEPS:")
        print("  1. Memory system appears to be working")
        print("  2. Check if ATLES is actually calling the search methods")
        print("  3. Verify memory integration in constitutional client")
    else:
        print("\n⚠️ Memory system has issues that need fixing")
