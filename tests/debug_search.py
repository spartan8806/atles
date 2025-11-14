#!/usr/bin/env python3
"""
Debug script for search_code function
"""

import sys
import os
from pathlib import Path

# Add the atles directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / 'atles'))

def debug_search():
    """Debug the search_code function step by step."""
    print("🔍 Debugging search_code function...")
    print("=" * 50)
    
    try:
        # Test 1: Direct import
        print("1️⃣ Testing direct import...")
        try:
            from atles.datasets.dataset_manager import CodeDatasetManager
            print("   ✅ Imported from atles.datasets.dataset_manager")
        except ImportError as e:
            print(f"   ❌ Import failed: {e}")
            return
        
        # Test 2: Create manager
        print("2️⃣ Creating CodeDatasetManager...")
        manager = CodeDatasetManager()
        print("   ✅ Manager created successfully")
        
        # Test 3: Check available datasets
        print("3️⃣ Checking available datasets...")
        info = manager.get_dataset_info()
        print(f"   📊 Available datasets: {list(info.keys())}")
        
        # Test 4: Test search with different parameters
        print("4️⃣ Testing search with different parameters...")
        
        # Test 4a: Basic search
        print("   🔍 Test 4a: Basic search for 'python'")
        results = manager.search_code("python")
        print(f"      Found {len(results)} results")
        
        # Test 4b: Search with language
        print("   🔍 Test 4b: Search for 'python' with language='python'")
        results = manager.search_code("python", "python")
        print(f"      Found {len(results)} results")
        
        # Test 4c: Search with dataset type
        print("   🔍 Test 4c: Search for 'python' with dataset_type='github_code'")
        results = manager.search_code("python", dataset_type="github_code")
        print(f"      Found {len(results)} results")
        
        # Test 4d: Search with all parameters
        print("   🔍 Test 4d: Search for 'flask' with language='python' and dataset_type='github_code'")
        results = manager.search_code("flask", "python", "github_code")
        print(f"      Found {len(results)} results")
        
        if results:
            print("      First result:")
            first = results[0]
            print(f"        Title: {first.get('title', 'No title')}")
            print(f"        Language: {first.get('language', 'No language')}")
            print(f"        Tags: {first.get('tags', [])}")
        
        # Test 5: Test specific dataset
        print("5️⃣ Testing specific dataset...")
        try:
            github_dataset = manager.github_code
            print(f"   📁 GitHub dataset: {github_dataset.get_metadata()}")
            github_results = github_dataset.search("flask", "python")
            print(f"   🔍 GitHub search results: {len(github_results)}")
        except Exception as e:
            print(f"   ❌ GitHub dataset test failed: {e}")
        
        print("\n✅ Debug completed!")
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_search()
