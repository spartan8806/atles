"""
ATLES Daemon Integration Helper

Easy integration of the learning daemon with any ATLES interface
"""

import os
import sys
import json
import atexit
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Import daemon functions
from atles.autonomous_learning_daemon import (
    get_daemon,
    mark_session_complete
)


class SessionTracker:
    """
    Track chat sessions for automatic learning
    
    Usage:
        tracker = SessionTracker()
        tracker.start_session()
        tracker.log_message("user", "Hello")
        tracker.log_message("assistant", "Hi there!")
        tracker.end_session()  # Triggers learning
    """
    
    def __init__(self, auto_start_daemon: bool = True):
        self.current_session: Optional[Dict] = None
        self.auto_start_daemon = auto_start_daemon
        
        # Start daemon if requested
        if auto_start_daemon:
            self._ensure_daemon_running()
        
        # Register cleanup
        atexit.register(self._cleanup)
    
    def _ensure_daemon_running(self):
        """Ensure learning daemon is running"""
        try:
            from atles.autonomous_learning_daemon import start_daemon
            daemon = get_daemon()
            if not daemon.is_running:
                start_daemon()
        except Exception as e:
            print(f"Warning: Could not start daemon: {e}")
    
    def start_session(self, session_id: Optional[str] = None) -> str:
        """
        Start a new session
        
        Args:
            session_id: Optional custom session ID
            
        Returns:
            Session ID
        """
        if self.current_session:
            # End previous session
            self.end_session()
        
        if not session_id:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.current_session = {
            "session_id": session_id,
            "start_time": datetime.now().isoformat(),
            "messages": [],
            "metadata": {}
        }
        
        return session_id
    
    def log_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """
        Log a message to current session
        
        Args:
            role: "user" or "assistant"
            content: Message content
            metadata: Optional metadata
        """
        if not self.current_session:
            self.start_session()
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        if metadata:
            message["metadata"] = metadata
        
        self.current_session["messages"].append(message)
    
    def set_metadata(self, key: str, value: any):
        """Set session metadata"""
        if not self.current_session:
            self.start_session()
        
        self.current_session["metadata"][key] = value
    
    def end_session(self):
        """
        End current session and trigger learning
        
        This will:
        1. Mark session as complete
        2. Trigger memory processing
        3. Trigger model fine-tuning
        4. Create detailed logs
        """
        if not self.current_session:
            return
        
        # Add end time
        self.current_session["end_time"] = datetime.now().isoformat()
        
        # Mark for daemon processing
        try:
            mark_session_complete(
                self.current_session["session_id"],
                self.current_session
            )
            print(f"✅ Session {self.current_session['session_id']} marked for learning")
        except Exception as e:
            print(f"Warning: Could not mark session for learning: {e}")
        
        self.current_session = None
    
    def _cleanup(self):
        """Cleanup on exit"""
        if self.current_session:
            self.end_session()
    
    def get_current_session_id(self) -> Optional[str]:
        """Get current session ID"""
        return self.current_session["session_id"] if self.current_session else None
    
    def get_message_count(self) -> int:
        """Get number of messages in current session"""
        return len(self.current_session["messages"]) if self.current_session else 0


# Global tracker instance
_tracker: Optional[SessionTracker] = None


def get_tracker(auto_start: bool = True) -> SessionTracker:
    """Get or create global session tracker"""
    global _tracker
    if _tracker is None:
        _tracker = SessionTracker(auto_start_daemon=auto_start)
    return _tracker


# Convenience functions

def track_user_message(content: str, metadata: Optional[Dict] = None):
    """Track a user message"""
    tracker = get_tracker()
    tracker.log_message("user", content, metadata)


def track_assistant_message(content: str, metadata: Optional[Dict] = None):
    """Track an assistant message"""
    tracker = get_tracker()
    tracker.log_message("assistant", content, metadata)


def start_tracked_session(session_id: Optional[str] = None) -> str:
    """Start a tracked session"""
    tracker = get_tracker()
    return tracker.start_session(session_id)


def end_tracked_session():
    """End current tracked session"""
    tracker = get_tracker()
    tracker.end_session()


def get_daemon_status() -> Dict:
    """Get learning daemon status"""
    daemon = get_daemon()
    return daemon.get_status()


# Example usage
if __name__ == "__main__":
    print("🧪 Testing Session Tracker\n")
    
    # Create tracker
    tracker = SessionTracker()
    
    # Start session
    session_id = tracker.start_session()
    print(f"Started session: {session_id}")
    
    # Log some messages
    tracker.log_message("user", "What is Python?")
    tracker.log_message("assistant", "Python is a high-level programming language...")
    tracker.log_message("user", "Show me an example")
    tracker.log_message("assistant", "Here's a simple example: print('Hello, World!')")
    
    print(f"Logged {tracker.get_message_count()} messages")
    
    # End session (triggers learning)
    print("\nEnding session (will trigger learning)...")
    tracker.end_session()
    
    print("\n✅ Test complete!")
    print("Check: atles_memory/learning_daemon/sessions/")

