# ATLES Test Suite

This directory contains comprehensive tests for the ATLES project to ensure everything works correctly and to help debug issues when they arise.

## 🧪 Available Tests

### Core Tests
- **`test_ollama_integration.py`** - Comprehensive test suite for Ollama integration and function calling
- **`test_datasets.py`** - Tests for the code dataset manager and search functionality
- **`test_function_calling.py`** - Specific tests for Ollama function calling capabilities
- **`debug_search.py`** - Debugging script for code dataset search issues

### Test Runner
- **`run_tests.py`** - Main test runner that can execute individual tests or all tests

## 🚀 Quick Start

### Run All Tests
```bash
cd tests
python run_tests.py
```

### Run Specific Test Categories
```bash
# Run only Ollama integration tests
python run_tests.py ollama

# Run only dataset tests
python run_tests.py datasets

# Show help
python run_tests.py --help
```

### Run Individual Tests
```bash
# Run comprehensive Ollama tests
python test_ollama_integration.py

# Test dataset functionality
python test_datasets.py

# Debug code search issues
python debug_search.py
```

## 📋 What Gets Tested

### Ollama Integration Tests
- ✅ Ollama server availability
- ✅ Function registration and schema generation
- ✅ File operations (read, write, list)
- ✅ Code dataset search functionality
- ✅ Terminal command execution
- ✅ System information retrieval
- ✅ Function call parsing and execution
- ✅ Error handling and edge cases

### Dataset Tests
- ✅ Dataset manager initialization
- ✅ Available datasets listing
- ✅ Code search functionality
- ✅ Language and dataset type filtering
- ✅ Individual dataset operations

## 🔧 Troubleshooting

### Common Issues

1. **Ollama Not Running**
   ```
   ❌ Ollama is not running. Please start Ollama with: ollama serve
   ```
   **Solution**: Start Ollama in another terminal with `ollama serve`

2. **Import Errors**
   ```
   ❌ Import failed: No module named 'atles'
   ```
   **Solution**: Make sure you're running tests from the `tests/` directory

3. **Function Call Failures**
   ```
   ❌ Function execution failed: Unknown function
   ```
   **Solution**: Check that all functions are properly registered in the Ollama client

### Debug Mode

If you need to debug specific functionality:

1. **Code Search Issues**: Use `debug_search.py` to step through dataset operations
2. **Function Calling**: Use `test_function_calling.py` to test specific function call formats
3. **Integration Issues**: Use `test_ollama_integration.py` for comprehensive testing

## 📁 Test Structure

```
tests/
├── README.md                    # This file
├── run_tests.py                # Main test runner
├── test_ollama_integration.py  # Comprehensive Ollama tests
├── test_function_calling.py    # Function calling tests
├── test_datasets.py            # Dataset manager tests
└── debug_search.py             # Code search debugging
```

## 🎯 When to Run Tests

- **Before deploying** - Ensure all functionality works
- **After code changes** - Verify nothing broke
- **When debugging** - Isolate specific issues
- **Regular maintenance** - Catch issues early

## 🚨 Important Notes

- **Keep these tests!** They're valuable for troubleshooting
- **Run tests regularly** to catch issues early
- **Use specific test categories** when debugging specific functionality
- **Check test output** for detailed error information

## 🔄 Updating Tests

When adding new functionality to ATLES:

1. **Add corresponding tests** to the appropriate test file
2. **Update the test runner** if adding new test categories
3. **Document new test requirements** in this README
4. **Test the tests** to ensure they work correctly

---

**Remember**: A good test suite is like insurance - you hope you never need it, but you're glad it's there when you do! 🛡️
