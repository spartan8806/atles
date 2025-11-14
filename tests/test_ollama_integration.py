#!/usr/bin/env python3
"""
Comprehensive test suite for Ollama integration and function calling

This test suite covers:
- Ollama client availability
- Function registration and execution
- File operations
- Code dataset search
- Terminal commands
- System information
- Function call handling
- Error handling
"""

import sys
import os
import json
import tempfile
from pathlib import Path

# Add the atles directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / 'atles'))

def test_ollama_availability():
    """Test if Ollama is available and running."""
    print("🔍 Testing Ollama Availability...")
    
    try:
        from atles.ollama_client_enhanced import OllamaFunctionCaller
        
        client = OllamaFunctionCaller()
        is_available = client.is_available()
        
        if is_available:
            print("  ✅ Ollama is available and running")
            return True, client
        else:
            print("  ❌ Ollama is not running")
            print("     Start Ollama with: ollama serve")
            return False, None
            
    except Exception as e:
        print(f"  ❌ Failed to create Ollama client: {e}")
        return False, None

def test_function_registration(client):
    """Test function registration and schema generation."""
    print("\n🔧 Testing Function Registration...")
    
    try:
        # Get function schema
        schema = client.get_function_schema()
        
        # Check if functions are registered
        if not schema.get("functions"):
            print("  ❌ No functions registered")
            return False
        
        print(f"  ✅ Registered {len(schema['functions'])} functions:")
        
        expected_functions = {
            "read_file", "write_file", "list_files", 
            "search_code", "run_command", "get_system_info"
        }
        
        registered_functions = {func["name"] for func in schema["functions"]}
        
        for func_name in expected_functions:
            if func_name in registered_functions:
                print(f"    ✅ {func_name}")
            else:
                print(f"    ❌ {func_name} (missing)")
                return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Function registration test failed: {e}")
        return False

def test_file_operations(client):
    """Test file reading, writing, and listing operations."""
    print("\n📁 Testing File Operations...")
    
    try:
        # Create a temporary test file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            test_content = "This is a test file for ATLES\nLine 2\nLine 3"
            f.write(test_content)
            test_file_path = f.name
        
        try:
            # Test read_file
            print("  🔍 Testing read_file...")
            content = client.read_file(test_file_path)
            if content == test_content:
                print("    ✅ read_file works correctly")
            else:
                print("    ❌ read_file returned incorrect content")
                return False
            
            # Test read_file with line limits
            content_lines = client.read_file(test_file_path, start_line=2, end_line=2)
            if content_lines.strip() == "Line 2":
                print("    ✅ read_file with line limits works")
            else:
                print("    ❌ read_file with line limits failed")
                return False
            
            # Test list_files
            print("  📋 Testing list_files...")
            files = client.list_files(str(Path(test_file_path).parent), "*.txt")
            if test_file_path in files:
                print("    ✅ list_files works correctly")
            else:
                print("    ❌ list_files failed to find test file")
                return False
            
            # Test write_file
            print("  ✍️ Testing write_file...")
            new_content = "New content for testing"
            result = client.write_file(test_file_path, new_content, 'w')
            if "Successfully wrote" in result:
                print("    ✅ write_file works correctly")
            else:
                print("    ❌ write_file failed")
                return False
            
            # Verify write
            updated_content = client.read_file(test_file_path)
            if updated_content == new_content:
                print("    ✅ write_file content verification passed")
            else:
                print("    ❌ write_file content verification failed")
                return False
            
            return True
            
        finally:
            # Clean up test file
            try:
                os.unlink(test_file_path)
            except:
                pass
                
    except Exception as e:
        print(f"  ❌ File operations test failed: {e}")
        return False

def test_code_dataset_search(client):
    """Test code dataset search functionality."""
    print("\n🔍 Testing Code Dataset Search...")
    
    try:
        # Test basic search
        print("  🔍 Testing basic search...")
        results = client.search_code_datasets("python")
        if isinstance(results, list):
            print(f"    ✅ Basic search returned {len(results)} results")
        else:
            print("    ❌ Basic search failed")
            return False
        
        # Test search with language filter
        print("  🔍 Testing search with language filter...")
        results = client.search_code_datasets("flask", "python")
        if isinstance(results, list):
            print(f"    ✅ Language-filtered search returned {len(results)} results")
        else:
            print("    ❌ Language-filtered search failed")
            return False
        
        # Test search with dataset type
        print("  🔍 Testing search with dataset type...")
        results = client.search_code_datasets("api", dataset_type="framework_docs")
        if isinstance(results, list):
            print(f"    ✅ Dataset-type search returned {len(results)} results")
        else:
            print("    ❌ Dataset-type search failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Code dataset search test failed: {e}")
        return False

def test_terminal_commands(client):
    """Test terminal command execution."""
    print("\n💻 Testing Terminal Commands...")
    
    try:
        # Test simple command
        print("  🔧 Testing simple command...")
        result = client.run_terminal_command("echo 'Hello ATLES'")
        if "Hello ATLES" in result:
            print("    ✅ Simple command execution works")
        else:
            print("    ❌ Simple command execution failed")
            return False
        
        # Test command with working directory
        print("  🔧 Testing command with working directory...")
        result = client.run_terminal_command("pwd", str(Path.cwd()))
        if "Command executed successfully" in result:
            print("    ✅ Command with working directory works")
        else:
            print("    ❌ Command with working directory failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Terminal commands test failed: {e}")
        return False

def test_system_info(client):
    """Test system information retrieval."""
    print("\n💻 Testing System Information...")
    
    try:
        info = client.get_system_info()
        
        required_keys = ["platform", "python_version", "cpu_count", "memory_total", "current_directory"]
        
        for key in required_keys:
            if key in info:
                print(f"    ✅ {key}: {info[key]}")
            else:
                print(f"    ❌ {key} missing from system info")
                return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ System info test failed: {e}")
        return False

def test_function_call_handling(client):
    """Test function call parsing and execution."""
    print("\n🔄 Testing Function Call Handling...")
    
    try:
        # Test standard FUNCTION_CALL format
        print("  🔄 Testing standard FUNCTION_CALL format...")
        test_response = "FUNCTION_CALL:get_system_info:{}"
        result = client.handle_function_call(test_response)
        if "Function get_system_info executed successfully" in result:
            print("    ✅ Standard FUNCTION_CALL format works")
        else:
            print("    ❌ Standard FUNCTION_CALL format failed")
            return False
        
        # Test alternative format
        print("  🔄 Testing alternative format...")
        test_response2 = 'search_code:{"query": "python", "language": "python"}'
        result2 = client.handle_function_call(test_response2)
        if "Function search_code executed successfully" in result2:
            print("    ✅ Alternative format works")
        else:
            print("    ❌ Alternative format failed")
            return False
        
        # Test invalid JSON handling
        print("  🔄 Testing invalid JSON handling...")
        test_response3 = 'search_code:{"query": "python", "language":}'
        result3 = client.handle_function_call(test_response3)
        if "Invalid JSON" in result3 or "Error handling function call" in result3:
            print("    ✅ Invalid JSON handling works")
        else:
            print("    ❌ Invalid JSON handling failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Function call handling test failed: {e}")
        return False

def test_error_handling(client):
    """Test error handling and edge cases."""
    print("\n⚠️ Testing Error Handling...")
    
    try:
        # Test unknown function
        print("  ⚠️ Testing unknown function...")
        try:
            result = client.execute_function("unknown_function", {})
            if not result["success"] and "Unknown function" in result["error"]:
                print("    ✅ Unknown function handling works")
            else:
                print("    ❌ Unknown function handling failed")
                return False
        except Exception as e:
            if "Unknown function" in str(e):
                print("    ✅ Unknown function handling works")
            else:
                print("    ❌ Unknown function handling failed")
                return False
        
        # Test file operations with non-existent file
        print("  ⚠️ Testing non-existent file handling...")
        try:
            result = client.read_file("/non/existent/file.txt")
            print("    ❌ Should have raised an exception")
            return False
        except Exception:
            print("    ✅ Non-existent file handling works")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error handling test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and provide a summary."""
    print("🧪 ATLES Ollama Integration Test Suite")
    print("=" * 60)
    
    # Test Ollama availability first
    is_available, client = test_ollama_availability()
    if not is_available:
        print("\n❌ Cannot run tests - Ollama is not available")
        return False
    
    # Run all tests
    test_results = []
    
    test_results.append(("Function Registration", test_function_registration(client)))
    test_results.append(("File Operations", test_file_operations(client)))
    test_results.append(("Code Dataset Search", test_code_dataset_search(client)))
    test_results.append(("Terminal Commands", test_terminal_commands(client)))
    test_results.append(("System Information", test_system_info(client)))
    test_results.append(("Function Call Handling", test_function_call_handling(client)))
    test_results.append(("Error Handling", test_error_handling(client)))
    
    # Clean up
    client.close()
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ollama integration is working perfectly.")
        return True
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
