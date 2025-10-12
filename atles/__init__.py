"""
ATLES - Advanced Text Language and Execution System

A comprehensive AI system for text processing, machine learning, and automation.

ARCHITECTURAL FIXES INTEGRATED:
- Source verification prevents hallucination
- Data visualization provides real charts/graphs  
- Code security ensures robust, secure code generation
- Functional computer vision replaces non-working examples
"""

__version__ = "0.5.1"  # Updated for architectural fixes
__author__ = "ATLES Team"
__description__ = "Advanced Text Language and Execution System with Architectural Fixes"

# Import lazy loading system first
from .lazy_imports import (
    lazy_import, is_module_available,
    has_source_verification, has_data_visualization, 
    has_code_security, has_computer_vision, 
    has_architectural_integration, has_error_handling
)

# Core components - import immediately as they're always needed
from .machine_learning import ATLESMachineLearning
from .tools import (
    AdvancedToolRegistry, 
    ToolChain, 
    ToolCategory, 
    SafetyLevel,
    AdvancedTool
)

# Check availability of architectural fixes (without importing)
SOURCE_VERIFICATION_AVAILABLE = has_source_verification()
DATA_VISUALIZATION_AVAILABLE = has_data_visualization()
CODE_SECURITY_AVAILABLE = has_code_security()
COMPUTER_VISION_AVAILABLE = has_computer_vision()
ARCHITECTURAL_INTEGRATION_AVAILABLE = has_architectural_integration()
ERROR_HANDLING_AVAILABLE = has_error_handling()

# Export all available components
__all__ = [
    # Core components
    "ATLESMachineLearning",
    
    # Tools
    "AdvancedToolRegistry",
    "ToolChain",
    "ToolCategory", 
    "SafetyLevel",
    "AdvancedTool",
    
    # Architectural fix availability flags
    "SOURCE_VERIFICATION_AVAILABLE",
    "DATA_VISUALIZATION_AVAILABLE", 
    "CODE_SECURITY_AVAILABLE",
    "COMPUTER_VISION_AVAILABLE",
    "ARCHITECTURAL_INTEGRATION_AVAILABLE"
]

# Add architectural components if available
if SOURCE_VERIFICATION_AVAILABLE:
    __all__.extend([
        "SourceVerificationAPI",
        "verify_sources_before_response"
    ])

if DATA_VISUALIZATION_AVAILABLE:
    __all__.extend([
        "DataVisualizationAPI",
        "create_chart_for_response"
    ])

if CODE_SECURITY_AVAILABLE:
    __all__.extend([
        "CodeValidationAPI", 
        "validate_generated_code"
    ])

if COMPUTER_VISION_AVAILABLE:
    __all__.extend([
        "ComputerVisionAPI",
        "extract_text_from_image",
        "analyze_image_comprehensively", 
        "create_functional_cv_example"
    ])

if ARCHITECTURAL_INTEGRATION_AVAILABLE:
    __all__.extend([
        "ATLESArchitecturalSystem",
        "get_architectural_system",
        "process_response_with_all_fixes",
        "generate_secure_functional_code",
        "create_working_visualization",
        "process_image_functionally"
    ])


# Lazy getter functions for architectural components
def get_source_verification_api():
    """Lazy load SourceVerificationAPI."""
    if not SOURCE_VERIFICATION_AVAILABLE:
        return None
    return lazy_import('atles.source_verification', 'SourceVerificationAPI')


def get_data_visualization_api():
    """Lazy load DataVisualizationAPI."""
    if not DATA_VISUALIZATION_AVAILABLE:
        return None
    return lazy_import('atles.data_visualization', 'DataVisualizationAPI')


def get_code_validation_api():
    """Lazy load CodeValidationAPI."""
    if not CODE_SECURITY_AVAILABLE:
        return None
    return lazy_import('atles.code_security', 'CodeValidationAPI')


def get_computer_vision_api():
    """Lazy load ComputerVisionAPI."""
    if not COMPUTER_VISION_AVAILABLE:
        return None
    return lazy_import('atles.computer_vision', 'ComputerVisionAPI')


def get_architectural_system():
    """Lazy load ATLESArchitecturalSystem."""
    if not ARCHITECTURAL_INTEGRATION_AVAILABLE:
        return None
    return lazy_import('atles.architectural_integration', 'ATLESArchitecturalSystem')


def get_error_handler():
    """Lazy load ErrorHandler."""
    if not ERROR_HANDLING_AVAILABLE:
        return None
    return lazy_import('atles.error_handling_standards', 'ErrorHandler')


def get_architectural_status():
    """Get status of all architectural fixes"""
    return {
        "source_verification": SOURCE_VERIFICATION_AVAILABLE,
        "data_visualization": DATA_VISUALIZATION_AVAILABLE,
        "code_security": CODE_SECURITY_AVAILABLE,
        "computer_vision": COMPUTER_VISION_AVAILABLE,
        "architectural_integration": ARCHITECTURAL_INTEGRATION_AVAILABLE,
        "error_handling": ERROR_HANDLING_AVAILABLE,
        "total_fixes_available": sum([
            SOURCE_VERIFICATION_AVAILABLE,
            DATA_VISUALIZATION_AVAILABLE,
            CODE_SECURITY_AVAILABLE,
            COMPUTER_VISION_AVAILABLE,
            ARCHITECTURAL_INTEGRATION_AVAILABLE,
            ERROR_HANDLING_AVAILABLE
        ])
    }


# Lightweight architectural layer management (always available)
from .architectural_layer_manager import get_layer_manager
from .lightweight_constitutional_client import create_lightweight_constitutional_client

# Add lazy getter functions to exports
__all__.extend([
    "get_source_verification_api",
    "get_data_visualization_api", 
    "get_code_validation_api",
    "get_computer_vision_api",
    "get_architectural_system",
    "get_error_handler",
    "get_architectural_status",
    "get_layer_manager",
    "create_lightweight_constitutional_client"
])
