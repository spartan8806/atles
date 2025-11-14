# ConversationMemoryManager AttributeError Fix

## Issue

```
Error saving session: 'ConversationMemoryManager' object has no attribute 'user_preferences'
SAVE: Session 94a5fc0c saved with 14 messages
SUCCESS: Memory saved
```

Despite the error message, the session was actually saved successfully, but the error indicated a code path issue.

## Root Cause

In `atles_app/atles_desktop_pyqt.py`, the `ConversationMemoryManager.__init__()` method had a conditional initialization bug:

```python
if self.use_new_system:
    # Start conversation with unified system
    self.session_id = self.unified_memory.start_conversation_session(...)
    # ❌ PROBLEM: load_memory() was NOT called here
else:
    self.load_memory()  # ✅ Only called in else branch
```

**The Problem:**
- When `use_new_system=True`, `load_memory()` was **never called**
- This meant `self.user_preferences` and `self.session_summaries` were **never initialized**
- Later, `save_current_session()` tried to access `self.user_preferences` → **AttributeError**

## Solution

Fixed by ensuring attributes are ALWAYS initialized, regardless of which memory system is used:

```python
# CRITICAL FIX: Always initialize these attributes first
self.user_preferences = {}
self.session_summaries = []

# Session tracking
self.current_session = {...}

# Load existing preferences and summaries from files
self.load_memory()  # ✅ Always called now

if self.use_new_system:
    # Start conversation session
    self.session_id = self.unified_memory.start_conversation_session(...)
```

**Additional Fix:**
Added the missing `_get_default_preferences()` helper method that was being called but didn't exist.

## Changes Made

### File: `atles_app/atles_desktop_pyqt.py`

1. **Always initialize attributes** (lines 224-227):
   ```python
   self.user_preferences = {}
   self.session_summaries = []
   ```

2. **Always call load_memory()** (line 239):
   ```python
   self.load_memory()  # Now unconditional
   ```

3. **Added missing helper** (lines 250-257):
   ```python
   def _get_default_preferences(self):
       """Get default user preferences structure"""
       return {...}
   ```

4. **Updated load_memory()** to use the helper consistently

## Testing

The fix ensures:
- ✅ No more AttributeError when saving sessions
- ✅ User preferences load from file if they exist
- ✅ Default preferences used if file doesn't exist
- ✅ Works with both unified memory system and legacy fallback

## Impact

- **Severity**: Medium (error message but functionality worked)
- **Users Affected**: All users with unified memory system enabled
- **Fix Status**: ✅ RESOLVED
- **Backward Compatible**: Yes
- **Breaking Changes**: None

## Related Issues

This was discovered alongside the Context Bleeding fix for Ollama. Both issues were manifestations of improper state initialization.

---

**Date Fixed**: November 12, 2025  
**Status**: RESOLVED ✅

