"""
ATLES PDF Processing Module

This module provides functionality to extract text from PDF documents,
supporting both direct file paths and URLs.
"""

import os
import tempfile
import logging
from typing import Dict, Any, Optional
from pathlib import Path

# Import dependency manager
from .dependency_checker import dependency_group_required, dependency_required

logger = logging.getLogger(__name__)

@dependency_required("pdfplumber")
def extract_text_from_pdf(file_path: str) -> Dict[str, Any]:
    """Extract text from a local PDF file"""
    try:
        import pdfplumber
        
        # Validate file exists
        if not os.path.exists(file_path):
            return {
                "success": False,
                "error": f"File not found: {file_path}",
                "text": ""
            }
            
        # Validate it's a PDF by checking extension
        if not file_path.lower().endswith('.pdf'):
            return {
                "success": False,
                "error": f"File is not a PDF: {file_path}",
                "text": ""
            }
            
        # Extract text
        text_content = []
        with pdfplumber.open(file_path) as pdf:
            num_pages = len(pdf.pages)
            
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text() or ""
                text_content.append(page_text)
                
                # Provide progress log for large documents
                if i % 10 == 0 and num_pages > 20:
                    logger.info(f"PDF processing: {i+1}/{num_pages} pages")
            
        full_text = "\n\n".join(text_content)
        
        return {
            "success": True,
            "text": full_text,
            "num_pages": num_pages,
            "file_path": file_path,
            "chars": len(full_text)
        }
        
    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        return {
            "success": False,
            "error": f"Failed to extract text from PDF: {str(e)}",
            "text": ""
        }

@dependency_group_required("pdf_processing")
def fetch_and_read_pdf(url: str, timeout: int = 30) -> Dict[str, Any]:
    """Fetch a PDF from a URL and extract its text content"""
    try:
        import requests
        import pdfplumber
        
        # Create a temp file for the PDF
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            # Download the PDF
            logger.info(f"Downloading PDF from {url}")
            headers = {
                'User-Agent': 'ATLES-Bot/1.0 (Educational Research)'
            }
            
            response = requests.get(url, headers=headers, timeout=timeout, stream=True)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            # Verify it's actually a PDF
            content_type = response.headers.get('content-type', '').lower()
            if 'application/pdf' not in content_type:
                return {
                    "success": False,
                    "error": f"URL does not point to a PDF document. Content-Type: {content_type}",
                    "url": url
                }
            
            # Write to temp file
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Extract text from the downloaded PDF
            extract_result = extract_text_from_pdf(temp_path)
            
            # Add URL info to the result
            extract_result["url"] = url
            
            return extract_result
            
        finally:
            # Clean up temp file
            try:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
            except Exception as e:
                logger.warning(f"Failed to delete temporary PDF file: {e}")
                
    except ImportError as e:
        return {
            "success": False,
            "error": f"Required dependency not available: {e}",
            "installation": "pip install requests pdfplumber"
        }
    except Exception as e:
        logger.error(f"PDF fetching error: {e}")
        return {
            "success": False,
            "error": f"Failed to fetch or process PDF from {url}: {str(e)}",
            "url": url
        }
