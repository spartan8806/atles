# Circular Import Fix: UnifiedMemoryManager

## Problem

```
WARNING: Intelligent Model Router not available

Could not import real UnifiedMemoryManager: cannot import name 'UnifiedMemoryManager' 
from partially initialized module 'atles.unified_memory_manager' 
(most likely due to a circular import) (D:\.atles\atles_app\atles\unified_memory_manager.py)

Memory system will not function properly!
```

## Root Cause Analysis

The circular import occurs because:

1. **`atles_desktop_pyqt.py`** imports `intelligent_model_router` at module level (line 30)
2. **`ConversationMemoryManager`** (in same file) imports `unified_memory_manager` at module level (line 210)
3. When Python tries to import these modules, it creates a circular dependency chain:
   - `atles_desktop_pyqt.py` → `intelligent_model_router` → (some module) → `unified_memory_manager`
   - `atles_desktop_pyqt.py` → `ConversationMemoryManager` → `unified_memory_manager`
   - `unified_memory_manager` → `memory_integration` → (possibly back to something that imports router)

## Solutions (Multiple Approaches)

### Solution 1: Lazy Import in ConversationMemoryManager (RECOMMENDED)

Move the import of `UnifiedMemoryManager` inside the `__init__` method or use lazy import pattern.

**Current Code:**
```python
# In ConversationMemoryManager.__init__
from atles.unified_memory_manager import UnifiedMemoryManager, get_unified_memory
```

**Fixed Code:**
```python
# Import moved inside try block, already done, but need to ensure it's truly lazy
```

### Solution 2: Defer Router Import (RECOMMENDED)

Move the router import to be lazy/conditional, only importing when actually needed.

**Current Code:**
```python
# At top of atles_desktop_pyqt.py
try:
    from atles.intelligent_model_router import IntelligentModelRouter, ModelType, TaskType
    from atles.router_performance_monitor import RouterPerformanceMonitor
    ROUTER_AVAILABLE = True
except ImportError:
    ROUTER_AVAILABLE = False
    print("WARNING: Intelligent Model Router not available")
```

**Fixed Code:**
```python
# Use lazy import pattern - import only when needed
ROUTER_AVAILABLE = None  # Will be set on first use

def _get_router_imports():
    """Lazy import of router components"""
    global ROUTER_AVAILABLE
    if ROUTER_AVAILABLE is None:
        try:
            from atles.intelligent_model_router import IntelligentModelRouter, ModelType, TaskType
            from atles.router_performance_monitor import RouterPerformanceMonitor
            ROUTER_AVAILABLE = True
            return IntelligentModelRouter, ModelType, TaskType, RouterPerformanceMonitor
        except ImportError as e:
            ROUTER_AVAILABLE = False
            print(f"WARNING: Intelligent Model Router not available: {e}")
            return None, None, None, None
    elif ROUTER_AVAILABLE:
        from atles.intelligent_model_router import IntelligentModelRouter, ModelType, TaskType
        from atles.router_performance_monitor import RouterPerformanceMonitor
        return IntelligentModelRouter, ModelType, TaskType, RouterPerformanceMonitor
    else:
        return None, None, None, None
```

### Solution 3: Use TYPE_CHECKING Guard

Use `TYPE_CHECKING` to avoid runtime imports for type hints.

**Implementation:**
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from atles.intelligent_model_router import IntelligentModelRouter
    from atles.unified_memory_manager import UnifiedMemoryManager
```

### Solution 4: Break Circular Dependency with Import Inside Function

Ensure all imports of `UnifiedMemoryManager` happen inside functions, not at module level.

**Current Issue:**
- `ConversationMemoryManager.__init__` imports at method level (good)
- But if `ConversationMemoryManager` class is defined/imported at module load time, it might trigger issues

**Fix:**
- Ensure the import is truly inside `__init__` and wrapped in try/except
- Add better error handling

### Solution 5: Use sys.modules Check (DEFENSIVE)

Add a check to prevent re-import during circular import:

```python
def safe_import_unified_memory():
    """Safely import UnifiedMemoryManager, handling circular imports"""
    import sys
    
    # Check if module is already being imported
    if 'atles.unified_memory_manager' in sys.modules:
        module = sys.modules['atles.unified_memory_manager']
        if hasattr(module, 'UnifiedMemoryManager'):
            return module.UnifiedMemoryManager, module.get_unified_memory
    
    # Safe import
    try:
        from atles.unified_memory_manager import UnifiedMemoryManager, get_unified_memory
        return UnifiedMemoryManager, get_unified_memory
    except (ImportError, AttributeError) as e:
        # Module might be partially initialized
        import time
        time.sleep(0.01)  # Brief delay
        try:
            from atles.unified_memory_manager import UnifiedMemoryManager, get_unified_memory
            return UnifiedMemoryManager, get_unified_memory
        except (ImportError, AttributeError):
            return None, None
```

## Recommended Implementation Plan

1. **Immediate Fix**: Use Solution 2 (Lazy Router Import) - This breaks the top-level import cycle
2. **Secondary Fix**: Ensure Solution 1 is properly implemented (lazy import in ConversationMemoryManager)
3. **Defensive Fix**: Add Solution 5 as a fallback

## Implementation Status ✅

### Fix 1: Lazy Router Import (IMPLEMENTED)

**File**: `atles_app/atles_desktop_pyqt.py`

- Changed router imports from module-level to lazy function `_get_router_imports()`
- Router classes are only imported when actually needed (in `ATLESCommunicationThread.__init__`)
- This breaks the circular dependency at the top level

**Before:**
```python
# Module-level import (causes circular dependency)
from atles.intelligent_model_router import IntelligentModelRouter, ModelType, TaskType
from atles.router_performance_monitor import RouterPerformanceMonitor
```

**After:**
```python
# Lazy import function
def _get_router_imports():
    """Lazy import of router components to avoid circular dependencies."""
    global ROUTER_AVAILABLE, _router_classes
    if ROUTER_AVAILABLE is None:
        try:
            from atles.intelligent_model_router import IntelligentModelRouter, ModelType, TaskType
            from atles.router_performance_monitor import RouterPerformanceMonitor
            ROUTER_AVAILABLE = True
            _router_classes = (IntelligentModelRouter, ModelType, TaskType, RouterPerformanceMonitor)
            return _router_classes
        except ImportError as e:
            ROUTER_AVAILABLE = False
            print(f"WARNING: Intelligent Model Router not available: {e}")
            return (None, None, None, None)
    # ... rest of function
```

### Fix 2: Retry Logic for Memory Import (IMPLEMENTED)

**File**: `atles_app/atles_desktop_pyqt.py` - `ConversationMemoryManager.__init__`

- Added retry logic with delay to handle partially initialized modules
- Better error messages for circular import detection
- Graceful fallback if import fails

**Key Changes:**
- Retry up to 3 times with 50ms delay between attempts
- Detects circular import errors specifically
- Provides clear warning messages

### Fix 3: Missing Import (FIXED)

- Added `import shutil` to fix linter error

## Testing

After implementing fixes:

1. ✅ Restart the application
2. ✅ Check that router imports successfully (no circular import error)
3. ✅ Check that memory system initializes correctly
4. ✅ Verify no circular import warnings

**Expected Behavior:**
- Router should import successfully when first used
- Memory system should initialize without "partially initialized module" errors
- No warnings about circular imports

## Files Modified

1. ✅ `atles_app/atles_desktop_pyqt.py` 
   - Lines 28-59: Changed router import to lazy function
   - Lines 225-277: Added retry logic for memory import
   - Line 21: Added `import shutil`
   - Lines 588-597: Updated router initialization to use lazy import

## How It Works

1. **At Module Load**: Router imports are deferred (no top-level import)
2. **When Router Needed**: `_get_router_imports()` is called, imports happen then
3. **Memory Import**: Retry logic handles partially initialized modules
4. **Result**: Circular dependency broken, both systems can initialize independently

## Verification

To verify the fix works:

1. Start the desktop app
2. Check console output - should see:
   ```
   ATLES Intelligent Model Router initialized
   INFO: Using Unified Episodic & Semantic Memory System
   ```
3. Should NOT see:
   ```
   WARNING: Circular import detected with UnifiedMemoryManager
   Could not import real UnifiedMemoryManager: cannot import name 'UnifiedMemoryManager' from partially initialized module
   ```

