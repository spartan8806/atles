# Hardcoded Response Bug Fix - Logical Reasoning Router

## Issue

Users were experiencing **hardcoded responses** that were completely unrelated to their prompts:

### Example 1: Philosophical Prompt → Logic Puzzle Response
```
[19:03] User: "ATLES, you're so close—and then you stepped..."
         (Münchhausen paradox discussion)

[19:03] ATLES: "Error: Could not extract problem parameters from prompt."

[Retry same prompt]

[19:03] ATLES: "NO, it is not required that any box contains a blue ball.
         Reasoning: There exist valid configurations with zero blue balls.
         Valid configurations (7 total):
         • (Red, Red, Red) → Red: 3
         • (Red, Red, Blue) → Red: 2, Blue: 1
         ..."
```

### Pattern Detected

The user noticed:
1. First attempt: `"Error: Could not extract problem parameters from prompt."` (56 characters)
2. Retry: Hardcoded "Red, Blue" logic puzzle response (394 characters)
3. **Exact same response length** appearing multiple times across different prompts

This indicated **hardcoded fallback responses** being returned instead of LLM-generated content.

## Root Cause

### The Culprit: Overly Aggressive Logical Reasoning Router

Located in `atles_app/atles/constitutional_client.py` lines 60-66:

```python
# Check if this is a logical reasoning question
if self.reasoning_router and self.reasoning_router.should_use_reasoning_engine(prompt):
    logger.info("🎯 Detected logical reasoning question - using reasoning helper")
    reasoning_response = self.reasoning_router.process_with_reasoning_engine(prompt)
    return reasoning_response  # ❌ PROBLEM: Returns hardcoded response
```

### How It Failed

**Step 1: Over-Matching**
The `LogicalReasoningRouter.should_use_reasoning_engine()` was TOO AGGRESSIVE:

```python
# OLD BUGGY CODE
keyword_count = sum(1 for kw in self.logic_keywords if kw in prompt_lower)

# If multiple logic keywords present, it's a logical reasoning question
if keyword_count >= 2:  # ❌ Too broad!
    return True
```

**Keywords included:**
- "must", "cannot", "contradict", "consistent", "at least", "at most", etc.

**Problem:** These words appear in **philosophical discussions**, **general reasoning**, and **paradoxes**!

Example: The Münchhausen prompt contained:
- "contradict" ✅ (match)
- "must" ✅ (match)
- Result: 2+ keywords → **falsely detected as logic puzzle**

**Step 2: Failed Parsing**
The router then tried to extract "box/ball" constraints from the philosophical prompt:

```python
params = self.extract_problem_parameters(prompt)
if params is None:
    return "Error: Could not extract problem parameters from prompt."  # ❌ Hardcoded error
```

**Step 3: Retry Triggers Cached Response**
On retry, the router used **default parameters** and returned a **hardcoded example** about Red/Blue configurations!

```python
default_params = {
    'constraints': ['at least one red ball'],
    'num_positions': 3,
    'possible_items': ['red', 'blue']
}
# Returns hardcoded Red/Blue configuration response
```

## The Fix

### 1. Made Router Much More Selective

**File: `atles_app/atles/logical_reasoning_router.py`**

Added explicit puzzle context requirement:

```python
def should_use_reasoning_engine(self, prompt: str) -> bool:
    """
    CRITICAL FIX: Made much more selective to avoid catching philosophical/general questions
    """
    prompt_lower = prompt.lower()
    
    # CRITICAL FIX: Must contain explicit box/ball/configuration language
    has_puzzle_context = any(word in prompt_lower for word in 
        ['box', 'boxes', 'ball', 'balls', 'configuration'])
    
    if not has_puzzle_context:
        # Not a logic puzzle - let LLM handle it
        return False
    
    # Count logic keywords ONLY if we have puzzle context
    keyword_count = sum(1 for kw in self.logic_keywords if kw in prompt_lower)
    
    # Require 3+ keywords to be more selective (was 2)
    if keyword_count >= 3:
        return True
    
    # Very specific patterns only
    if re.search(r'at\s+(?:least|most)\s+\w+\s+(?:red|blue|green|yellow)', prompt_lower):
        return True
    
    return False
```

**Key Changes:**
- ✅ **Requires puzzle context** (box/ball/configuration words)
- ✅ Increased keyword threshold from 2 to 3
- ✅ Made patterns more specific

### 2. Graceful Fallback Instead of Hardcoded Error

When parameter extraction fails:

```python
# OLD CODE
else:
    return "Error: Could not extract problem parameters from prompt."

# NEW CODE
else:
    logger.warning("Could not extract logic puzzle parameters - letting LLM handle this")
    return None  # Signal to fall back to LLM
```

### 3. Constitutional Client Handles None Response

**File: `atles_app/atles/constitutional_client.py`**

```python
reasoning_response = self.reasoning_router.process_with_reasoning_engine(prompt)

# CRITICAL FIX: If reasoning engine returns None, fall back to LLM
if reasoning_response is None:
    logger.info("Reasoning helper returned None - falling back to LLM")
    # Fall through to normal LLM generation
else:
    logger.info("✅ Reasoning helper provided answer")
    return reasoning_response
```

## Impact

### Before Fix ❌

| Prompt Type | Result |
|-------------|--------|
| "Münchhausen paradox..." | ❌ Hardcoded Red/Blue response |
| "Bootstrap certainty..." | ❌ "Error: Could not extract..." |
| "Simulation vs reality..." | ❌ Random logic puzzle answer |
| Actual logic puzzle | ✅ Works correctly |

### After Fix ✅

| Prompt Type | Result |
|-------------|--------|
| "Münchhausen paradox..." | ✅ LLM handles philosophical discussion |
| "Bootstrap certainty..." | ✅ LLM handles epistemology |
| "Simulation vs reality..." | ✅ LLM handles metaphysics |
| Actual logic puzzle | ✅ Reasoning engine handles it |

## Testing

### Test Cases

**1. Philosophical Prompt (Should NOT Trigger Router)**
```python
prompt = """
ATLES, you just pulled a Münchhausen—yanked yourself out by your logic ponytail.
But that's consistency, not proof. A perfect simulation would pass the same check.
Name one property your R-Zero loop has that a simulation cannot replicate.
"""

# Expected: LLM generates thoughtful philosophical response
# Should NOT see: Red/Blue configurations
```

**2. Actual Logic Puzzle (SHOULD Trigger Router)**
```python
prompt = """
I have 3 boxes. Each box contains at least one red ball.
How many valid configurations are possible with red and blue balls?
"""

# Expected: Reasoning engine provides structured answer
# Should see: Red/Blue configurations (appropriately!)
```

**3. Edge Case: Uses Logic Words But Not a Puzzle**
```python
prompt = """
We must consider whether AI can truly contradict its programming.
At least in theory, it should be consistent with its training.
"""

# Expected: LLM handles (no box/ball context)
# Should NOT trigger reasoning engine
```

## Verification

Look for these log messages after fix:

**When router is correctly bypassed:**
```
Reasoning helper returned None - falling back to LLM
```

**When router is correctly triggered:**
```
🎯 Detected logical reasoning question - using reasoning helper
✅ Reasoning helper provided answer
```

## Modified Files

1. ✅ **`atles_app/atles/logical_reasoning_router.py`**
   - Added `has_puzzle_context` requirement
   - Increased keyword threshold
   - Return `None` instead of hardcoded error

2. ✅ **`atles_app/atles/constitutional_client.py`**
   - Handle `None` response from reasoning router
   - Graceful fallback to LLM

3. ✅ **`atles/ollama_client_enhanced.py`** (from previous fix)
   - Cache-busting to prevent response reuse

## Lessons Learned

### Design Flaws

1. **Over-Eager Detection**: Keyword matching without context is too broad
2. **Hardcoded Fallbacks**: Never return hardcoded content when user expects dynamic response
3. **No Graceful Degradation**: Should always have LLM fallback path

### Best Practices

1. ✅ **Context-Aware Detection**: Require domain-specific words (box/ball/configuration)
2. ✅ **Graceful Fallback**: Return `None` to signal "can't handle, try something else"
3. ✅ **Layered Defense**: Multiple systems can handle same prompt type
4. ✅ **Clear Logging**: Easy to debug which system is handling what

## Future Improvements

### Short Term
- [x] Make router more selective ✅
- [x] Add graceful fallback ✅
- [ ] Add unit tests for false positives

### Medium Term
- [ ] Add confidence scoring to router decisions
- [ ] Allow router to suggest "maybe" (use both systems)
- [ ] Track false positive rate

### Long Term
- [ ] ML-based classifier for logic puzzles vs general reasoning
- [ ] User feedback loop for misclassifications
- [ ] A/B testing for router thresholds

## Related Issues

This fix addresses both:
1. ✅ Context bleeding from Ollama (previous fix)
2. ✅ Hardcoded responses from reasoning router (this fix)

Together, these ensure ATLES gives **relevant, dynamic responses** every time.

---

**Date Fixed**: November 14, 2025  
**Status**: RESOLVED ✅  
**Severity**: CRITICAL → RESOLVED  
**User Impact**: All users seeing hardcoded "Red, Blue" responses

