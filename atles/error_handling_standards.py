"""
ATLES Error Handling Standards

This module provides standardized error handling patterns and utilities
for consistent error management across the ATLES codebase.
"""

import logging
import traceback
from typing import Dict, Any, Optional, Callable, Union
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path


class ErrorSeverity(Enum):
    """Standard error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Standard error categories."""
    VALIDATION = "validation"
    NETWORK = "network"
    FILE_IO = "file_io"
    DATABASE = "database"
    AUTHENTICATION = "authentication"
    CONFIGURATION = "configuration"
    BUSINESS_LOGIC = "business_logic"
    EXTERNAL_API = "external_api"
    SYSTEM = "system"


@dataclass
class StandardError:
    """Standardized error structure."""
    error_id: str
    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = None
    module: str = ""
    function: str = ""
    traceback_info: Optional[str] = None
    user_message: Optional[str] = None  # User-friendly message
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class ErrorHandler:
    """Centralized error handling with consistent patterns."""
    
    def __init__(self, module_name: str):
        self.module_name = module_name
        self.logger = logging.getLogger(module_name)
        self.error_log: list[StandardError] = []
        
    def handle_error(
        self,
        error: Exception,
        category: ErrorCategory,
        severity: ErrorSeverity,
        context: Optional[Dict[str, Any]] = None,
        user_message: Optional[str] = None,
        function_name: str = "",
        should_raise: bool = True
    ) -> StandardError:
        """
        Handle an error with standardized logging and optional re-raising.
        
        Args:
            error: The exception that occurred
            category: Error category for classification
            severity: Error severity level
            context: Additional context information
            user_message: User-friendly error message
            function_name: Name of the function where error occurred
            should_raise: Whether to re-raise the exception
            
        Returns:
            StandardError object with all error details
        """
        import uuid
        
        # Create standardized error
        std_error = StandardError(
            error_id=str(uuid.uuid4())[:8],
            category=category,
            severity=severity,
            message=str(error),
            details=context or {},
            module=self.module_name,
            function=function_name,
            traceback_info=traceback.format_exc(),
            user_message=user_message
        )
        
        # Log based on severity
        log_message = f"[{std_error.error_id}] {std_error.message}"
        if context:
            log_message += f" | Context: {context}"
            
        if severity == ErrorSeverity.CRITICAL:
            self.logger.critical(log_message)
        elif severity == ErrorSeverity.HIGH:
            self.logger.error(log_message)
        elif severity == ErrorSeverity.MEDIUM:
            self.logger.warning(log_message)
        else:
            self.logger.info(log_message)
        
        # Store error for analysis
        self.error_log.append(std_error)
        
        # Optionally re-raise
        if should_raise and severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]:
            raise error
            
        return std_error
    
    def safe_execute(
        self,
        func: Callable,
        *args,
        category: ErrorCategory = ErrorCategory.BUSINESS_LOGIC,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        default_return: Any = None,
        context: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> tuple[bool, Any, Optional[StandardError]]:
        """
        Safely execute a function with standardized error handling.
        
        Returns:
            (success: bool, result: Any, error: Optional[StandardError])
        """
        try:
            result = func(*args, **kwargs)
            return True, result, None
        except Exception as e:
            error = self.handle_error(
                error=e,
                category=category,
                severity=severity,
                context=context,
                function_name=func.__name__,
                should_raise=False
            )
            return False, default_return, error
    
    def validate_and_execute(
        self,
        validation_func: Callable,
        execution_func: Callable,
        *args,
        validation_context: Optional[Dict[str, Any]] = None,
        execution_context: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> tuple[bool, Any, Optional[StandardError]]:
        """
        Validate inputs before executing a function.
        
        Returns:
            (success: bool, result: Any, error: Optional[StandardError])
        """
        # Validate first
        success, validation_result, validation_error = self.safe_execute(
            validation_func,
            *args,
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.MEDIUM,
            context=validation_context,
            **kwargs
        )
        
        if not success or not validation_result:
            return False, None, validation_error
        
        # Execute if validation passes
        return self.safe_execute(
            execution_func,
            *args,
            category=ErrorCategory.BUSINESS_LOGIC,
            severity=ErrorSeverity.HIGH,
            context=execution_context,
            **kwargs
        )
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of errors by category and severity."""
        summary = {
            "total_errors": len(self.error_log),
            "by_category": {},
            "by_severity": {},
            "recent_errors": []
        }
        
        for error in self.error_log:
            # Count by category
            cat_name = error.category.value
            if cat_name not in summary["by_category"]:
                summary["by_category"][cat_name] = 0
            summary["by_category"][cat_name] += 1
            
            # Count by severity
            sev_name = error.severity.value
            if sev_name not in summary["by_severity"]:
                summary["by_severity"][sev_name] = 0
            summary["by_severity"][sev_name] += 1
        
        # Recent errors (last 10)
        summary["recent_errors"] = [
            {
                "id": error.error_id,
                "category": error.category.value,
                "severity": error.severity.value,
                "message": error.message,
                "timestamp": error.timestamp.isoformat()
            }
            for error in self.error_log[-10:]
        ]
        
        return summary


# Convenience functions for common error patterns
def create_error_handler(module_name: str) -> ErrorHandler:
    """Create a standardized error handler for a module."""
    return ErrorHandler(module_name)


def handle_validation_error(
    handler: ErrorHandler,
    error: Exception,
    field_name: str = "",
    expected_type: str = "",
    actual_value: Any = None
) -> StandardError:
    """Handle validation errors with consistent context."""
    context = {
        "field_name": field_name,
        "expected_type": expected_type,
        "actual_value": str(actual_value) if actual_value is not None else None
    }
    
    user_message = f"Invalid {field_name}: expected {expected_type}" if field_name else "Validation failed"
    
    return handler.handle_error(
        error=error,
        category=ErrorCategory.VALIDATION,
        severity=ErrorSeverity.MEDIUM,
        context=context,
        user_message=user_message,
        should_raise=False
    )


def handle_network_error(
    handler: ErrorHandler,
    error: Exception,
    url: str = "",
    timeout: Optional[float] = None,
    retry_count: int = 0
) -> StandardError:
    """Handle network errors with consistent context."""
    context = {
        "url": url,
        "timeout": timeout,
        "retry_count": retry_count
    }
    
    user_message = "Network connection failed. Please check your internet connection."
    
    return handler.handle_error(
        error=error,
        category=ErrorCategory.NETWORK,
        severity=ErrorSeverity.HIGH,
        context=context,
        user_message=user_message,
        should_raise=False
    )


def handle_file_error(
    handler: ErrorHandler,
    error: Exception,
    file_path: str = "",
    operation: str = ""
) -> StandardError:
    """Handle file I/O errors with consistent context."""
    context = {
        "file_path": file_path,
        "operation": operation,
        "file_exists": Path(file_path).exists() if file_path else False
    }
    
    user_message = f"File operation failed: {operation} on {file_path}" if operation else "File operation failed"
    
    return handler.handle_error(
        error=error,
        category=ErrorCategory.FILE_IO,
        severity=ErrorSeverity.MEDIUM,
        context=context,
        user_message=user_message,
        should_raise=False
    )


# Decorator for automatic error handling
def with_error_handling(
    category: ErrorCategory = ErrorCategory.BUSINESS_LOGIC,
    severity: ErrorSeverity = ErrorSeverity.MEDIUM,
    default_return: Any = None,
    should_raise: bool = False
):
    """Decorator to add standardized error handling to functions."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            handler = ErrorHandler(func.__module__)
            
            success, result, error = handler.safe_execute(
                func,
                *args,
                category=category,
                severity=severity,
                default_return=default_return,
                **kwargs
            )
            
            if not success and should_raise:
                raise Exception(f"Function {func.__name__} failed: {error.message if error else 'Unknown error'}")
            
            return result
        return wrapper
    return decorator
