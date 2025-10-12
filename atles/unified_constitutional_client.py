#!/usr/bin/env python3
"""
Unified Constitutional Client - Lightweight Version

This file now uses the lightweight constitutional client with
architectural layer management for better performance and control.
"""

from .lightweight_constitutional_client import create_lightweight_constitutional_client

# For backward compatibility
def create_constitutional_client(user_id: str = "constitutional_user"):
    """Create a constitutional client (now lightweight version)."""
    return create_lightweight_constitutional_client(user_id)

# Export the main factory function
__all__ = ["create_constitutional_client", "create_lightweight_constitutional_client"]