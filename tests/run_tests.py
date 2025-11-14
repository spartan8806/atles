#!/usr/bin/env python3
"""
Quick test runner for ATLES tests

Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py ollama            # Run only Ollama tests
    python run_tests.py datasets          # Run only dataset tests
    python run_tests.py --help            # Show help
"""

import sys
import subprocess
from pathlib import Path

def run_test(test_name, description):
    """Run a specific test and show results."""
    print(f"\n🧪 Running {test_name}...")
    print(f"📝 {description}")
    print("-" * 50)
    
    try:
        result = subprocess.run([sys.executable, test_name], 
                              capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✅ Test completed successfully!")
        else:
            print("❌ Test failed!")
            if result.stderr:
                print("Error output:")
                print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Failed to run test: {e}")
        return False

def show_help():
    """Show help information."""
    print("🧪 ATLES Test Runner")
    print("=" * 40)
    print("Usage:")
    print("  python run_tests.py                    # Run all tests")
    print("  python run_tests.py ollama            # Run only Ollama tests")
    print("  python run_tests.py datasets          # Run only dataset tests")
    print("  python run_tests.py --help            # Show this help")
    print("\nAvailable Tests:")
    print("  ollama_integration.py    - Comprehensive Ollama integration tests")
    print("  test_function_calling.py - Function calling specific tests")
    print("  debug_search.py          - Code dataset search debugging")
    print("  test_datasets.py         - Dataset manager tests")

def main():
    """Main test runner."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            show_help()
            return
        
        test_type = sys.argv[1].lower()
        
        if test_type == "ollama":
            success = run_test("test_ollama_integration.py", 
                             "Comprehensive Ollama integration and function calling tests")
        elif test_type == "datasets":
            success = run_test("test_datasets.py", 
                             "Dataset manager and code search tests")
        else:
            print(f"❌ Unknown test type: {test_type}")
            show_help()
            return
        
        if success:
            print("\n🎉 Selected tests completed successfully!")
        else:
            print("\n⚠️ Some tests failed. Check the output above.")
            sys.exit(1)
    
    else:
        # Run all tests
        print("🧪 Running All ATLES Tests...")
        print("=" * 50)
        
        tests = [
            ("test_ollama_integration.py", "Comprehensive Ollama integration tests"),
            ("test_datasets.py", "Dataset manager tests")
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, description in tests:
            if run_test(test_name, description):
                passed += 1
        
        print(f"\n📊 Test Summary: {passed}/{total} test suites passed")
        
        if passed == total:
            print("🎉 All test suites completed successfully!")
        else:
            print("⚠️ Some test suites failed. Check the output above.")
            sys.exit(1)

if __name__ == "__main__":
    main()
