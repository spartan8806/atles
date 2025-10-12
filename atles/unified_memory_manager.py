#!/usr/bin/env python3
"""
Unified Memory Manager for ATLES

This module provides a single, shared memory integration instance that all
components of ATLES can use. This prevents the multiple memory integration
conflicts that were causing session conflicts and incomplete memory tracking.

Key Features:
- Singleton pattern ensures only one memory integration instance
- Thread-safe access for desktop app communication
- Shared context generation for all components
- Unified session management
"""

import logging
import threading
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)


class UnifiedMemoryManager:
    """
    Singleton memory manager that provides a single memory integration instance
    for all ATLES components to share.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, memory_dir: str = "atles_memory"):
        """Ensure only one instance exists (singleton pattern)."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, memory_dir: str = "atles_memory"):
        """Initialize the unified memory manager (only once)."""
        if self._initialized:
            return
        
        self.memory_dir = memory_dir
        self._memory_integration = None
        self._current_session_id = None
        self._lock = threading.Lock()
        self._session_start_time = None
        self._last_interaction_time = None
        
        # Initialize the memory integration system
        self._initialize_memory_integration()
        self._initialized = True
        
        logger.info("Unified Memory Manager initialized")
    
    def _initialize_memory_integration(self):
        """Initialize the memory integration system."""
        try:
            from .memory_integration import MemoryIntegration
            self._memory_integration = MemoryIntegration(self.memory_dir, auto_migrate=True)
            logger.info("✅ Memory integration system initialized")
        except ImportError as e:
            logger.error(f"Failed to initialize memory integration: {e}")
            self._memory_integration = None
    
    @property
    def memory_integration(self):
        """Get the shared memory integration instance."""
        return self._memory_integration
    
    def is_available(self) -> bool:
        """Check if memory integration is available."""
        return self._memory_integration is not None
    
    def start_conversation_session(self, session_id: str = None) -> Optional[str]:
        """Start a new conversation session."""
        if not self.is_available():
            return None
        
        with self._lock:
            try:
                self._current_session_id = self._memory_integration.start_conversation_session(session_id)
                logger.info(f"Started conversation session: {self._current_session_id}")
                return self._current_session_id
            except Exception as e:
                logger.error(f"Error starting conversation session: {e}")
                return None
    
    def add_message(self, sender: str, message: str, context: Dict[str, Any] = None) -> bool:
        """Add a message to the current session."""
        if not self.is_available():
            return False
        
        try:
            # Update interaction tracking
            from datetime import datetime
            self._last_interaction_time = datetime.now()
            
            self._memory_integration.add_message(sender, message, context or {})
            return True
        except Exception as e:
            logger.error(f"Error adding message: {e}")
            return False
    
    def end_conversation_session(self) -> Optional[str]:
        """End the current conversation session."""
        if not self.is_available():
            return None
        
        with self._lock:
            try:
                episode_id = self._memory_integration.end_conversation_session()
                if episode_id:
                    logger.info(f"Ended conversation session: {episode_id}")
                self._current_session_id = None
                return episode_id
            except Exception as e:
                logger.error(f"Error ending conversation session: {e}")
                return None
    
    def process_user_prompt_with_memory(self, user_message: str) -> Dict[str, Any]:
        """Process user prompt with memory-aware reasoning."""
        if not self.is_available():
            return {"memory_enhanced": False}
        
        try:
            return self._memory_integration.process_user_prompt_with_memory(user_message)
        except Exception as e:
            logger.error(f"Error processing user prompt with memory: {e}")
            return {"memory_enhanced": False}
    
    def get_conversation_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent conversation history."""
        if not self.is_available():
            return []
        
        try:
            return self._memory_integration.get_conversation_history(limit)
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            return []
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory system statistics."""
        if not self.is_available():
            return {}
        
        try:
            return self._memory_integration.get_memory_stats()
        except Exception as e:
            logger.error(f"Error getting memory stats: {e}")
            return {}
    
    def get_context_for_ai(self) -> str:
        """Generate unified context string for AI from memory."""
        if not self.is_available():
            return ""
        
        try:
            # Get recent conversation history
            recent_history = self.get_conversation_history(limit=20)
            
            context_parts = []
            
            if recent_history:
                context_parts.append("# Recent Conversation Context:")
                for entry in recent_history[-10:]:  # Last 10 messages
                    timestamp = entry.get("timestamp", "")
                    sender = entry.get("sender", "Unknown")
                    message = entry.get("message", "")
                    if timestamp and sender and message:
                        # Format timestamp for readability
                        time_str = timestamp.split('T')[1][:8] if 'T' in timestamp else timestamp
                        context_parts.append(f"[{time_str}] {sender}: {message}")
            
            # Get memory stats
            stats = self.get_memory_stats()
            learned_principles = stats.get("learned_principles", {})
            
            if learned_principles.get("total_principles", 0) > 0:
                context_parts.append(f"\n# Memory System Status:")
                context_parts.append(f"- Episodes: {stats.get('episodes', 0)}")
                context_parts.append(f"- Learned Principles: {learned_principles.get('total_principles', 0)}")
                context_parts.append(f"- Core Memory Items: {stats.get('core_memory_items', 0)}")
            
            return "\n".join(context_parts)
            
        except Exception as e:
            logger.error(f"Error generating AI context: {e}")
            return ""
    
    def get_current_session_id(self) -> Optional[str]:
        """Get the current session ID."""
        return self._current_session_id
    
    def is_new_session(self) -> bool:
        """Check if this is a new session (for bootstrap protocol)."""
        from datetime import datetime, timedelta
        
        # If no session is active, it's definitely new
        if not self._current_session_id:
            return True
        
        # If no previous interaction, it's new
        if not self._last_interaction_time:
            return True
        
        # If it's been more than 30 minutes since last interaction, consider it new
        time_since_last = datetime.now() - self._last_interaction_time
        if time_since_last > timedelta(minutes=30):
            return True
        
        return False
    
    @classmethod
    def get_instance(cls, memory_dir: str = "atles_memory") -> 'UnifiedMemoryManager':
        """Get the singleton instance."""
        return cls(memory_dir)
    
    @classmethod
    def reset_instance(cls):
        """Reset the singleton instance (for testing)."""
        with cls._lock:
            if cls._instance:
                # End any active session
                if cls._instance._current_session_id:
                    cls._instance.end_conversation_session()
            cls._instance = None


# Convenience functions for easy access
def get_unified_memory() -> UnifiedMemoryManager:
    """Get the unified memory manager instance."""
    return UnifiedMemoryManager.get_instance()


def is_memory_available() -> bool:
    """Check if memory integration is available."""
    return get_unified_memory().is_available()


def process_with_memory(user_message: str) -> Dict[str, Any]:
    """Process user message with memory-aware reasoning."""
    return get_unified_memory().process_user_prompt_with_memory(user_message)


def add_conversation_message(sender: str, message: str, context: Dict[str, Any] = None) -> bool:
    """Add a message to the current conversation."""
    return get_unified_memory().add_message(sender, message, context)


def get_memory_context_for_ai() -> str:
    """Get memory context for AI responses."""
    return get_unified_memory().get_context_for_ai()


if __name__ == "__main__":
    # Test the unified memory manager
    print("🧪 Testing Unified Memory Manager")
    
    # Test singleton behavior
    manager1 = UnifiedMemoryManager()
    manager2 = UnifiedMemoryManager()
    print(f"Singleton test: {manager1 is manager2}")  # Should be True
    
    # Test memory availability
    print(f"Memory available: {manager1.is_available()}")
    
    # Test session management
    session_id = manager1.start_conversation_session()
    print(f"Started session: {session_id}")
    
    # Test message adding
    success = manager1.add_message("User", "Hello, this is a test message")
    print(f"Added message: {success}")
    
    # Test context generation
    context = manager1.get_context_for_ai()
    print(f"Generated context length: {len(context)}")
    
    # End session
    episode_id = manager1.end_conversation_session()
    print(f"Ended session, created episode: {episode_id}")
    
    print("✅ Unified Memory Manager test completed")
