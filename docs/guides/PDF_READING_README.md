# PDF Reading Capability for ATLES

This document explains how to use the new PDF reading functionality added to ATLES.

## Overview

ATLES now has the ability to extract and process text from PDF documents available on the web. This enhancement allows ATLES to:

1. Download PDF files from URLs
2. Extract text content from the documents
3. Process and analyze the information contained in PDFs

## Installation

The PDF reading capability requires additional Python packages. To install them, run:

```bash
pip install pdfplumber requests
```

Or use the provided installation script:

```bash
install_pdf_support.bat
```

## Using the PDF Reading Function

### Function Call Format

To read a PDF, use the `read_pdf` function:

```
FUNCTION_CALL:read_pdf:{"url": "https://example.com/document.pdf"}
```

### Parameters

- `url` (required): The URL of the PDF document to read
- `timeout` (optional): Request timeout in seconds (default: 30)

### Example

```
FUNCTION_CALL:read_pdf:{"url": "https://arxiv.org/pdf/2212.08073.pdf"}
```

### Response

The function returns a JSON object containing:

```json
{
  "success": true,
  "url": "https://example.com/document.pdf",
  "num_pages": 10,
  "total_chars": 12345,
  "text_preview": "The first 1000 characters of the document...",
  "text": "The full text of the document...",
  "message": "Successfully extracted text from URL (10 pages, 12345 characters)"
}
```

## Error Handling

If the PDF reading fails, the function will return an error message:

```json
{
  "success": false,
  "error": "Error message explaining what went wrong",
  "url": "https://example.com/document.pdf"
}
```

Common errors include:
- Missing dependencies
- Invalid URL
- URL does not point to a PDF
- Network connectivity issues
- PDF parsing errors

## Testing

To test the PDF reading capability, run:

```bash
python test_pdf_reading.py
```

This will attempt to read a sample PDF and display the results.

## Implementation Details

The PDF reading functionality is implemented in the `pdf_processor.py` module and integrated into the `OllamaFunctionCaller` class. It uses:

1. `requests` to download the PDF from the URL
2. `pdfplumber` to extract text from the PDF
3. Dependency checking to gracefully handle missing libraries

The implementation handles various edge cases:
- Large PDFs
- PDFs with complex layouts
- Error handling for network issues
- Clean temporary file management
