"""
ATLES Lazy Import System

This module provides lazy loading functionality to reduce startup overhead
and avoid circular import issues.
"""

import importlib
import logging
from typing import Any, Dict, Optional, Callable
from functools import wraps

logger = logging.getLogger(__name__)


class LazyImporter:
    """Lazy importer that loads modules only when needed."""
    
    def __init__(self):
        self._cached_modules: Dict[str, Any] = {}
        self._import_errors: Dict[str, Exception] = {}
        
    def lazy_import(self, module_name: str, attribute: Optional[str] = None, 
                   fallback: Any = None) -> Any:
        """
        Lazily import a module or attribute.
        
        Args:
            module_name: Name of the module to import
            attribute: Specific attribute to get from the module
            fallback: Value to return if import fails
            
        Returns:
            The imported module/attribute or fallback value
        """
        cache_key = f"{module_name}.{attribute}" if attribute else module_name
        
        # Return cached result if available
        if cache_key in self._cached_modules:
            return self._cached_modules[cache_key]
        
        # Return None if we know this import failed before
        if cache_key in self._import_errors:
            return fallback
        
        try:
            module = importlib.import_module(module_name)
            
            if attribute:
                result = getattr(module, attribute)
            else:
                result = module
                
            self._cached_modules[cache_key] = result
            logger.debug(f"Lazy imported: {cache_key}")
            return result
            
        except (ImportError, AttributeError) as e:
            self._import_errors[cache_key] = e
            logger.debug(f"Failed to lazy import {cache_key}: {e}")
            return fallback
    
    def is_available(self, module_name: str, attribute: Optional[str] = None) -> bool:
        """Check if a module/attribute is available without importing it."""
        cache_key = f"{module_name}.{attribute}" if attribute else module_name
        
        if cache_key in self._cached_modules:
            return True
        if cache_key in self._import_errors:
            return False
            
        # Try to import to check availability
        result = self.lazy_import(module_name, attribute)
        return result is not None
    
    def get_import_status(self) -> Dict[str, Any]:
        """Get status of all attempted imports."""
        return {
            "cached_modules": list(self._cached_modules.keys()),
            "failed_imports": list(self._import_errors.keys()),
            "total_cached": len(self._cached_modules),
            "total_failed": len(self._import_errors)
        }


# Global lazy importer instance
_lazy_importer = LazyImporter()


def lazy_import(module_name: str, attribute: Optional[str] = None, 
               fallback: Any = None) -> Any:
    """Convenience function for lazy importing."""
    return _lazy_importer.lazy_import(module_name, attribute, fallback)


def is_module_available(module_name: str, attribute: Optional[str] = None) -> bool:
    """Check if a module/attribute is available."""
    return _lazy_importer.is_available(module_name, attribute)


def lazy_property(module_name: str, attribute: Optional[str] = None, 
                 fallback: Any = None):
    """Decorator to create lazy-loaded properties."""
    def decorator(func):
        @property
        @wraps(func)
        def wrapper(self):
            return lazy_import(module_name, attribute, fallback)
        return wrapper
    return decorator


class LazyModule:
    """A module-like object that loads attributes lazily."""
    
    def __init__(self, module_name: str):
        self._module_name = module_name
        self._module = None
        self._failed = False
    
    def __getattr__(self, name: str) -> Any:
        if self._failed:
            raise AttributeError(f"Module {self._module_name} is not available")
        
        if self._module is None:
            try:
                self._module = importlib.import_module(self._module_name)
            except ImportError:
                self._failed = True
                raise AttributeError(f"Module {self._module_name} is not available")
        
        return getattr(self._module, name)
    
    def __bool__(self) -> bool:
        """Check if the module is available."""
        if self._failed:
            return False
        if self._module is not None:
            return True
        
        try:
            self._module = importlib.import_module(self._module_name)
            return True
        except ImportError:
            self._failed = True
            return False


def create_lazy_module(module_name: str) -> LazyModule:
    """Create a lazy-loading module proxy."""
    return LazyModule(module_name)


# Convenience functions for ATLES modules
def get_source_verification():
    """Lazy import source verification module."""
    return lazy_import('atles.source_verification')


def get_data_visualization():
    """Lazy import data visualization module."""
    return lazy_import('atles.data_visualization')


def get_code_security():
    """Lazy import code security module."""
    return lazy_import('atles.code_security')


def get_computer_vision():
    """Lazy import computer vision module."""
    return lazy_import('atles.computer_vision')


def get_architectural_integration():
    """Lazy import architectural integration module."""
    return lazy_import('atles.architectural_integration')


def get_error_handling():
    """Lazy import error handling standards."""
    return lazy_import('atles.error_handling_standards')


def get_import_status() -> Dict[str, Any]:
    """Get status of all lazy imports."""
    return _lazy_importer.get_import_status()


# Module availability checkers
def has_source_verification() -> bool:
    """Check if source verification is available."""
    return is_module_available('atles.source_verification')


def has_data_visualization() -> bool:
    """Check if data visualization is available."""
    return is_module_available('atles.data_visualization')


def has_code_security() -> bool:
    """Check if code security is available."""
    return is_module_available('atles.code_security')


def has_computer_vision() -> bool:
    """Check if computer vision is available."""
    return is_module_available('atles.computer_vision')


def has_architectural_integration() -> bool:
    """Check if architectural integration is available."""
    return is_module_available('atles.architectural_integration')


def has_error_handling() -> bool:
    """Check if error handling standards are available."""
    return is_module_available('atles.error_handling_standards')
