#!/usr/bin/env python3
"""
ATLES Demo Manager
=================
Manages demo users, sessions, and logging for the ATLES portfolio demonstration.
"""

import json
import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path

class ATLESDemoManager:
    """Manages demo users, sessions, and logging for ATLES portfolio demo."""
    
    def __init__(self, data_dir: str = "atles_demo_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Demo user codes (you can add more)
        self.demo_users = {
            "DEMO001": {
                "name": "John Smith",
                "company": "TechCorp",
                "email": "john@techcorp.com",
                "active": True,
                "usage_count": 0,
                "max_usage": 50,
                "created": datetime.now().isoformat(),
                "last_activity": None,
                "session_id": None
            },
            "DEMO002": {
                "name": "Sarah Johnson", 
                "company": "StartupXYZ",
                "email": "sarah@startupxyz.com",
                "active": True,
                "usage_count": 0,
                "max_usage": 50,
                "created": datetime.now().isoformat(),
                "last_activity": None,
                "session_id": None
            },
            "DEMO003": {
                "name": "Mike Chen",
                "company": "Enterprise Inc",
                "email": "mike@enterprise.com", 
                "active": True,
                "usage_count": 0,
                "max_usage": 50,
                "created": datetime.now().isoformat(),
                "last_activity": None,
                "session_id": None
            }
        }
        
        # Admin codes
        self.admin_codes = ["ADMIN123", "MASTER456"]
        
        # Interaction logs
        self.interaction_logs = []
        
        # Load existing data
        self._load_data()
    
    def _load_data(self):
        """Load existing data from files."""
        # Load demo users
        users_file = self.data_dir / "demo_users.json"
        if users_file.exists():
            with open(users_file, 'r') as f:
                self.demo_users = json.load(f)
        
        # Load interaction logs
        logs_file = self.data_dir / "interaction_logs.json"
        if logs_file.exists():
            with open(logs_file, 'r') as f:
                self.interaction_logs = json.load(f)
    
    def _save_data(self):
        """Save data to files."""
        # Save demo users
        users_file = self.data_dir / "demo_users.json"
        with open(users_file, 'w') as f:
            json.dump(self.demo_users, f, indent=2)
        
        # Save interaction logs
        logs_file = self.data_dir / "interaction_logs.json"
        with open(logs_file, 'w') as f:
            json.dump(self.interaction_logs, f, indent=2)
    
    def validate_demo_code(self, code: str) -> Dict[str, Any]:
        """Validate demo code and return user info."""
        if code not in self.demo_users:
            return {"valid": False, "error": "Invalid demo code"}
        
        user = self.demo_users[code]
        
        if not user["active"]:
            return {"valid": False, "error": "Demo code has been revoked"}
        
        if user["usage_count"] >= user["max_usage"]:
            return {"valid": False, "error": "Usage limit exceeded"}
        
        # Update last activity
        user["last_activity"] = datetime.now().isoformat()
        self._save_data()
        
        return {
            "valid": True,
            "user": {
                "name": user["name"],
                "company": user["company"],
                "usage_remaining": user["max_usage"] - user["usage_count"]
            }
        }
    
    def create_session(self, user_code: str) -> str:
        """Create a new session for a user."""
        session_id = str(uuid.uuid4())
        self.demo_users[user_code]["session_id"] = session_id
        self._save_data()
        return session_id
    
    def log_interaction(self, user_code: str, action: str, input_data: str, 
                       output_data: str, response_time: float, ip_address: str = None):
        """Log user interaction for quality assurance."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_code": user_code,
            "user_name": self.demo_users[user_code]["name"],
            "action": action,
            "input": input_data,
            "output": output_data,
            "response_time": response_time,
            "ip_address": ip_address,
            "session_id": self.demo_users[user_code]["session_id"]
        }
        
        self.interaction_logs.append(log_entry)
        
        # Increment usage count
        self.demo_users[user_code]["usage_count"] += 1
        self.demo_users[user_code]["last_activity"] = datetime.now().isoformat()
        
        self._save_data()
    
    def check_usage_limits(self, user_code: str) -> bool:
        """Check if user has exceeded usage limits."""
        user = self.demo_users[user_code]
        return user["usage_count"] < user["max_usage"]
    
    def revoke_user(self, user_code: str) -> bool:
        """Revoke user access (admin function)."""
        if user_code in self.demo_users:
            self.demo_users[user_code]["active"] = False
            self._save_data()
            return True
        return False
    
    def activate_user(self, user_code: str) -> bool:
        """Activate user access (admin function)."""
        if user_code in self.demo_users:
            self.demo_users[user_code]["active"] = True
            self._save_data()
            return True
        return False
    
    def reset_usage(self, user_code: str) -> bool:
        """Reset user usage count (admin function)."""
        if user_code in self.demo_users:
            self.demo_users[user_code]["usage_count"] = 0
            self._save_data()
            return True
        return False
    
    def get_user_stats(self) -> Dict[str, Any]:
        """Get user statistics for admin panel."""
        total_users = len(self.demo_users)
        active_users = sum(1 for user in self.demo_users.values() if user["active"])
        total_usage = sum(user["usage_count"] for user in self.demo_users.values())
        
        recent_logs = [log for log in self.interaction_logs 
                      if datetime.fromisoformat(log["timestamp"]) > 
                      datetime.now() - timedelta(hours=24)]
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "total_usage": total_usage,
            "recent_interactions": len(recent_logs),
            "users": self.demo_users
        }
    
    def get_interaction_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent interaction logs."""
        return self.interaction_logs[-limit:]
