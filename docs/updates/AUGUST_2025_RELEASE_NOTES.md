# ATLES August 2025 Update Release Notes

## New Features

### 1. PDF Reading Capability

ATLES can now extract and analyze text from PDF documents via URLs:

- **Web PDF Extraction**: Download and read PDFs from the internet
- **Text Analysis**: Extract full text content from PDFs
- **Function Call Integration**: Simple `read_pdf` function for direct access
- **Detailed Metadata**: Page count, character count, and content preview

Example usage:
```
FUNCTION_CALL:read_pdf:{"url": "https://example.com/document.pdf"}
```

Installation:
```bash
pip install pdfplumber requests
# or use the provided script
install_pdf_support.bat
```

### 2. Smart Dependency Management

ATLES now gracefully handles optional dependencies:

- **Elegant Degradation**: Clean fallbacks when packages are missing
- **Clear Instructions**: Helpful installation guidance
- **Dependency Groups**: Logical organization of related packages
- **Decorator System**: Simple API for marking dependency requirements

Benefits:
- No more cryptic import errors
- Optional modules don't break core functionality
- Clear guidance for users on what to install
- Better developer experience with clean decorators

### 3. Enhanced Debug Mode

Comprehensive debug mode for function calling:

- **Toggle Commands**: Easy debug mode activation via command line
- **Function Call Analysis**: Detailed logging of function call processing
- **JSON Parsing Improvements**: Better handling of malformed inputs
- **Constitutional Enforcement Testing**: Tools to verify safety protections

Usage:
```bash
# Show current status
toggle_debug.bat status

# Enable function call debugging
toggle_debug.bat function

# Run tests with debug enabled
python test_function_call_debug.py
python test_pdf_reading.py
```

## Bug Fixes

- Fixed warning messages about missing optional dependencies
- Improved error handling in function call processing
- Enhanced robustness of JSON parsing in function calls
- Better handling of non-standard function call formats

## Documentation Updates

- **`DEPENDENCY_PDF_FEATURES.md`**: Complete guide to new dependency and PDF features
- **`DEBUG_MODE_README.md`**: Comprehensive debug mode documentation
- **`DEBUG_QUICK_REFERENCE.md`**: Quick reference for debugging tools
- **`PDF_READING_README.md`**: Detailed guide to PDF reading functionality
- **`CONSTITUTIONAL_TESTING_README.md`**: Guide to constitutional enforcement testing
- **Updated main `README.md`**: Added new features to feature list

## Installation

For PDF reading support:
```bash
pip install -r pdf_requirements.txt
```

## Testing

Test the new features:
```bash
python test_function_call_debug.py  # Test dependency handling and debug mode
python test_pdf_reading.py          # Test PDF reading capability
```

## Coming Soon

- Advanced document processing capabilities
- Additional file format support (DOCX, PPTX)
- Enhanced PDF analysis with table and image extraction
- Automatic dependency management with installation prompts
