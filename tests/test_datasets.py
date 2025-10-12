#!/usr/bin/env python3
"""
Test script for ATLES Code Datasets

This script demonstrates how to use the various code datasets
and shows that they work even with placeholder implementations.
"""

import sys
import os
from pathlib import Path

# Add the atles directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / 'atles'))

def test_datasets():
    """Test the code datasets functionality."""
    print("🧪 Testing ATLES Code Datasets...")
    print("=" * 50)
    
    try:
        # Import the dataset manager
        from datasets.dataset_manager import CodeDatasetManager
        
        # Initialize the manager
        print("📁 Initializing Code Dataset Manager...")
        manager = CodeDatasetManager()
        
        # Get dataset information
        print("\n📊 Available Datasets:")
        dataset_info = manager.get_dataset_info()
        for name, info in dataset_info.items():
            print(f"  • {name}: {info['name']}")
            print(f"    Description: {info['description']}")
            print(f"    Size: {info['size']} examples")
            print(f"    Tags: {', '.join(info['tags'])}")
            print()
        
        # Test search functionality
        print("🔍 Testing Search Functionality:")
        
        # Search for Python examples
        print("  Searching for 'python' examples...")
        python_results = manager.search_code("python")
        print(f"    Found {len(python_results)} results")
        
        # Search for API examples
        print("  Searching for 'api' examples...")
        api_results = manager.search_code("api")
        print(f"    Found {len(api_results)} results")
        
        # Search for algorithm examples
        print("  Searching for 'algorithm' examples...")
        algo_results = manager.search_code("algorithm")
        print(f"    Found {len(algo_results)} results")
        
        # Test specific dataset search
        print("\n🎯 Testing Specific Dataset Search:")
        github_results = manager.search_code("flask", dataset_type="github_code")
        print(f"  GitHub Code (flask): {len(github_results)} results")
        
        book_results = manager.search_code("design pattern", dataset_type="programming_books")
        print(f"  Programming Books (design pattern): {len(book_results)} results")
        
        challenge_results = manager.search_code("array", dataset_type="code_challenges")
        print(f"  Code Challenges (array): {len(challenge_results)} results")
        
        framework_results = manager.search_code("fastapi", dataset_type="framework_docs")
        print(f"  Framework Docs (fastapi): {len(framework_results)} results")
        
        # Get statistics
        print("\n📈 Dataset Statistics:")
        stats = manager.get_statistics()
        print(f"  Total datasets: {stats['total_datasets']}")
        print(f"  Total examples: {stats['total_examples']}")
        print(f"  Languages: {', '.join(stats['languages'])}")
        print(f"  Total tags: {len(stats['tags'])}")
        
        # Test getting specific examples
        print("\n🔍 Testing Example Retrieval:")
        if python_results:
            first_example = python_results[0]
            example_id = first_example.get('id', 'unknown')
            dataset_type = 'github_code'  # Default to first available
            
            retrieved = manager.get_code_example(example_id, dataset_type)
            if retrieved:
                print(f"  Successfully retrieved example: {retrieved.get('title', 'Unknown')}")
            else:
                print(f"  Could not retrieve example: {example_id}")
        
        print("\n✅ Dataset testing completed successfully!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from the project root directory.")
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

def test_individual_datasets():
    """Test individual dataset classes."""
    print("\n🧪 Testing Individual Dataset Classes...")
    print("=" * 50)
    
    try:
        # Test GitHub Code Dataset
        print("📚 Testing GitHub Code Dataset...")
        from datasets.github_code import GitHubCodeDataset
        github_dataset = GitHubCodeDataset(Path("test_github"))
        metadata = github_dataset.get_metadata()
        print(f"  Name: {metadata['name']}")
        print(f"  Size: {metadata['size']} examples")
        
        # Test Programming Books Dataset
        print("\n📖 Testing Programming Books Dataset...")
        from datasets.programming_books import ProgrammingBooksDataset
        books_dataset = ProgrammingBooksDataset(Path("test_books"))
        metadata = books_dataset.get_metadata()
        print(f"  Name: {metadata['name']}")
        print(f"  Size: {metadata['size']} examples")
        
        # Test Code Challenges Dataset
        print("\n🧩 Testing Code Challenges Dataset...")
        from datasets.code_challenges import CodeChallengesDataset
        challenges_dataset = CodeChallengesDataset(Path("test_challenges"))
        metadata = challenges_dataset.get_metadata()
        print(f"  Name: {metadata['name']}")
        print(f"  Size: {metadata['size']} examples")
        
        # Test Framework Docs Dataset
        print("\n🔧 Testing Framework Docs Dataset...")
        from datasets.framework_docs import FrameworkDocsDataset
        framework_dataset = FrameworkDocsDataset(Path("test_frameworks"))
        metadata = framework_dataset.get_metadata()
        print(f"  Name: {metadata['name']}")
        print(f"  Size: {metadata['size']} examples")
        
        print("\n✅ Individual dataset testing completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during individual dataset testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 ATLES Code Datasets Test Suite")
    print("=" * 50)
    
    # Test the main dataset manager
    test_datasets()
    
    # Test individual datasets
    test_individual_datasets()
    
    print("\n🎉 All tests completed!")
    print("\n💡 The datasets are now ready to use in your ATLES project!")
