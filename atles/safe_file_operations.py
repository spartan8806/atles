"""
Safe File Operations with Atomic Writes and File Locking

This module provides thread-safe and crash-safe file operations for ATLES.
Prevents corruption from concurrent writes and system crashes.
"""

import json
import os
import tempfile
import threading
import time
import platform

# Platform-specific imports
if platform.system() == "Windows":
    import msvcrt  # Windows file locking
else:
    import fcntl  # Unix file locking
from pathlib import Path
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class SafeFileOperations:
    """Thread-safe and crash-safe file operations."""
    
    def __init__(self):
        self._locks = {}  # Per-file locks
        self._global_lock = threading.RLock()
    
    def _get_file_lock(self, filepath: str) -> threading.RLock:
        """Get or create a lock for a specific file."""
        with self._global_lock:
            if filepath not in self._locks:
                self._locks[filepath] = threading.RLock()
            return self._locks[filepath]
    
    def _lock_file(self, file_handle, exclusive: bool = True):
        """Cross-platform file locking."""
        try:
            if platform.system() == "Windows":
                # Windows file locking
                if exclusive:
                    msvcrt.locking(file_handle.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    msvcrt.locking(file_handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                # Unix file locking
                lock_type = fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH
                fcntl.flock(file_handle.fileno(), lock_type | fcntl.LOCK_NB)
        except (OSError, IOError) as e:
            logger.warning(f"Could not acquire file lock: {e}")
            # Continue without file lock - thread lock still protects us
    
    def _unlock_file(self, file_handle):
        """Cross-platform file unlocking."""
        try:
            if platform.system() == "Windows":
                msvcrt.locking(file_handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(file_handle.fileno(), fcntl.LOCK_UN)
        except (OSError, IOError):
            pass  # Ignore unlock errors
    
    def safe_read_json(self, filepath: str, default: Any = None, encoding: str = 'utf-8') -> Any:
        """Safely read JSON file with locking and error handling."""
        filepath = str(Path(filepath).resolve())
        file_lock = self._get_file_lock(filepath)
        
        with file_lock:
            try:
                if not os.path.exists(filepath):
                    logger.info(f"File {filepath} does not exist, returning default")
                    return default
                
                with open(filepath, 'r', encoding=encoding) as f:
                    self._lock_file(f, exclusive=False)  # Shared lock for reading
                    try:
                        data = json.load(f)
                        logger.debug(f"Successfully read JSON from {filepath}")
                        return data
                    finally:
                        self._unlock_file(f)
                        
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error in {filepath}: {e}")
                # Try to recover from backup
                backup_path = f"{filepath}.backup"
                if os.path.exists(backup_path):
                    logger.info(f"Attempting to recover from backup: {backup_path}")
                    try:
                        with open(backup_path, 'r', encoding=encoding) as f:
                            return json.load(f)
                    except Exception:
                        pass
                return default
            except Exception as e:
                logger.error(f"Error reading {filepath}: {e}")
                return default
    
    def safe_write_json(self, filepath: str, data: Any, encoding: str = 'utf-8', 
                       create_backup: bool = True) -> bool:
        """Safely write JSON file with atomic operations and locking."""
        filepath = str(Path(filepath).resolve())
        file_lock = self._get_file_lock(filepath)
        
        with file_lock:
            try:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                
                # Create backup if file exists and backup is requested
                if create_backup and os.path.exists(filepath):
                    backup_path = f"{filepath}.backup"
                    try:
                        import shutil
                        shutil.copy2(filepath, backup_path)
                    except Exception as e:
                        logger.warning(f"Could not create backup: {e}")
                
                # Write to temporary file first (atomic operation)
                temp_path = f"{filepath}.tmp.{int(time.time())}.{os.getpid()}"
                
                with open(temp_path, 'w', encoding=encoding) as f:
                    self._lock_file(f, exclusive=True)  # Exclusive lock for writing
                    try:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                        f.flush()
                        os.fsync(f.fileno())  # Force write to disk
                    finally:
                        self._unlock_file(f)
                
                # Atomic move (rename) - this is atomic on most filesystems
                if platform.system() == "Windows":
                    # Windows requires removing target first
                    if os.path.exists(filepath):
                        os.remove(filepath)
                
                os.rename(temp_path, filepath)
                logger.debug(f"Successfully wrote JSON to {filepath}")
                return True
                
            except Exception as e:
                logger.error(f"Error writing {filepath}: {e}")
                # Clean up temp file if it exists
                if 'temp_path' in locals() and os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except Exception:
                        pass
                return False
    
    def safe_read_text(self, filepath: str, default: str = "", encoding: str = 'utf-8') -> str:
        """Safely read text file with locking."""
        filepath = str(Path(filepath).resolve())
        file_lock = self._get_file_lock(filepath)
        
        with file_lock:
            try:
                if not os.path.exists(filepath):
                    return default
                
                with open(filepath, 'r', encoding=encoding) as f:
                    self._lock_file(f, exclusive=False)
                    try:
                        return f.read()
                    finally:
                        self._unlock_file(f)
                        
            except Exception as e:
                logger.error(f"Error reading {filepath}: {e}")
                return default
    
    def safe_write_text(self, filepath: str, content: str, encoding: str = 'utf-8') -> bool:
        """Safely write text file with atomic operations."""
        filepath = str(Path(filepath).resolve())
        file_lock = self._get_file_lock(filepath)
        
        with file_lock:
            try:
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                
                temp_path = f"{filepath}.tmp.{int(time.time())}.{os.getpid()}"
                
                with open(temp_path, 'w', encoding=encoding) as f:
                    self._lock_file(f, exclusive=True)
                    try:
                        f.write(content)
                        f.flush()
                        os.fsync(f.fileno())
                    finally:
                        self._unlock_file(f)
                
                if platform.system() == "Windows" and os.path.exists(filepath):
                    os.remove(filepath)
                
                os.rename(temp_path, filepath)
                return True
                
            except Exception as e:
                logger.error(f"Error writing {filepath}: {e}")
                if 'temp_path' in locals() and os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except Exception:
                        pass
                return False

# Global instance for easy access
safe_file_ops = SafeFileOperations()

# Convenience functions
def safe_read_json(filepath: str, default: Any = None, encoding: str = 'utf-8') -> Any:
    """Safely read JSON file."""
    return safe_file_ops.safe_read_json(filepath, default, encoding)

def safe_write_json(filepath: str, data: Any, encoding: str = 'utf-8', create_backup: bool = True) -> bool:
    """Safely write JSON file."""
    return safe_file_ops.safe_write_json(filepath, data, encoding, create_backup)

def safe_read_text(filepath: str, default: str = "", encoding: str = 'utf-8') -> str:
    """Safely read text file."""
    return safe_file_ops.safe_read_text(filepath, default, encoding)

def safe_write_text(filepath: str, content: str, encoding: str = 'utf-8') -> bool:
    """Safely write text file."""
    return safe_file_ops.safe_write_text(filepath, content, encoding)
