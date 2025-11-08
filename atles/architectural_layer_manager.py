#!/usr/bin/env python3
"""
Architectural Layer Manager for ATLES

Manages which architectural layers (memory, bootstrap, capability grounding, etc.)
are active and should process each request.
"""

import logging
from typing import Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class ArchitecturalLayerManager:
    """Manages architectural processing layers."""
    
    def __init__(self):
        self.layers = {
            "memory_integration": True,
            "bootstrap": True,
            "capability_grounding": True,
            "constitutional": True,
            "scratchpad": True
        }
        
        self.performance_stats = {
            "total_requests": 0,
            "bypassed_requests": 0,
            "processed_requests": 0
        }
    
    def is_layer_enabled(self, layer_name: str) -> bool:
        """Check if a layer is enabled."""
        return self.layers.get(layer_name, False)
    
    def enable_layer(self, layer_name: str):
        """Enable a processing layer."""
        self.layers[layer_name] = True
        logger.info(f"Enabled layer: {layer_name}")
    
    def disable_layer(self, layer_name: str):
        """Disable a processing layer."""
        self.layers[layer_name] = False
        logger.info(f"Disabled layer: {layer_name}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of all layers."""
        return {
            "layers": self.layers.copy(),
            "performance": self.performance_stats.copy()
        }


# Global instance
_layer_manager = None


def get_layer_manager() -> ArchitecturalLayerManager:
    """Get the global layer manager instance."""
    global _layer_manager
    if _layer_manager is None:
        _layer_manager = ArchitecturalLayerManager()
    return _layer_manager


def should_process_layer(layer_name: str, prompt: str) -> bool:
    """
    Check if a layer should process this prompt.
    
    Args:
        layer_name: Name of the layer
        prompt: User prompt
    
    Returns:
        True if layer should process
    """
    manager = get_layer_manager()
    return manager.is_layer_enabled(layer_name)


def is_simple_request(prompt: str) -> bool:
    """
    Check if this is a simple request that doesn't need complex processing.
    
    Args:
        prompt: User prompt
    
    Returns:
        True if simple request
    """
    if not prompt:
        return True
    
    prompt_lower = prompt.lower().strip()
    
    # Very simple greetings/responses
    simple_patterns = [
        "hi", "hello", "hey", "thanks", "thank you",
        "ok", "okay", "yes", "no", "bye", "goodbye"
    ]
    
    # Check if it's just a simple greeting
    if prompt_lower in simple_patterns:
        return True
    
    # Check if it starts with a simple greeting and is short
    if len(prompt_lower) < 20:
        for pattern in simple_patterns:
            if prompt_lower.startswith(pattern + " ") or prompt_lower.startswith(pattern + ","):
                return True
    
    return False


if __name__ == "__main__":
    # Test the layer manager
    manager = get_layer_manager()
    print(f"Layer status: {manager.get_status()}")
    
    # Test simple request detection
    print(f"\nSimple request tests:")
    print(f"  'hi' -> {is_simple_request('hi')}")
    print(f"  'Hello!' -> {is_simple_request('Hello!')}")
    print(f"  'Explain quantum computing' -> {is_simple_request('Explain quantum computing')}")

