"""
ATLES Dependency Checker Module

This module provides utilities for checking and handling optional dependencies
in a graceful manner, with fallback mechanisms and helpful error messages.
"""

import importlib.util
import logging
from typing import Dict, Optional, Callable, List, Tuple

logger = logging.getLogger(__name__)

class DependencyManager:
    """Manages optional dependencies and provides graceful fallbacks"""
    
    def __init__(self):
        self.dependency_status = {}
        self.dependency_groups = {
            "code_security": ["bandit", "pylint"],
            "computer_vision": ["torch", "torchvision", "transformers", "opencv-python"],
            "pdf_processing": ["pdfplumber", "requests"]
        }
    
    def check_dependency(self, module_name: str) -> bool:
        """Check if a dependency is available"""
        if module_name in self.dependency_status:
            return self.dependency_status[module_name]
            
        is_available = importlib.util.find_spec(module_name) is not None
        self.dependency_status[module_name] = is_available
        
        if not is_available:
            logger.warning(f"{module_name} is not available")
        
        return is_available
    
    def check_dependency_group(self, group_name: str) -> Tuple[bool, List[str]]:
        """Check if all dependencies in a group are available"""
        if group_name not in self.dependency_groups:
            return False, []
            
        dependencies = self.dependency_groups[group_name]
        missing = []
        
        for dep in dependencies:
            if not self.check_dependency(dep):
                missing.append(dep)
                
        return len(missing) == 0, missing
    
    def get_installation_instructions(self, group_name: str) -> str:
        """Get pip installation instructions for a dependency group"""
        if group_name not in self.dependency_groups:
            return ""
            
        dependencies = self.dependency_groups[group_name]
        return f"pip install {' '.join(dependencies)}"

# Global instance for use across the application
dependency_manager = DependencyManager()

def dependency_required(dependency_name: str):
    """Decorator to require a specific dependency"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if dependency_manager.check_dependency(dependency_name):
                return func(*args, **kwargs)
            else:
                logger.warning(f"Function {func.__name__} requires {dependency_name}, which is not installed")
                return {
                    "error": f"Required dependency '{dependency_name}' is not installed",
                    "installation": f"pip install {dependency_name}"
                }
        return wrapper
    return decorator

def dependency_group_required(group_name: str):
    """Decorator to require a group of dependencies"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            group_available, missing = dependency_manager.check_dependency_group(group_name)
            if group_available:
                return func(*args, **kwargs)
            else:
                missing_str = ', '.join(missing)
                logger.warning(f"Function {func.__name__} requires {group_name} dependencies: {missing_str}")
                return {
                    "error": f"Required dependencies for {group_name} are not installed: {missing_str}",
                    "installation": dependency_manager.get_installation_instructions(group_name)
                }
        return wrapper
    return decorator
