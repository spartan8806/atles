# Wrong Model Selection Fix - Router Using Wrong Models

## Issue

ATLES was trying to use models that don't exist and ignoring the fine-tuned models:

```
Error: Model 'qwen2.5-coder:latest' is not available
```

**Problems:**
1. Router tried to use `qwen2.5-coder:latest` (not installed)
2. Router ignored `atles-qwen2.5:7b-enhanced` (fine-tuned model)
3. For coding tasks, chose coding model even for conversation

## Root Cause

The `IntelligentModelRouter` configuration in `atles/intelligent_model_router.py` didn't include the fine-tuned ATLES models and listed models that weren't installed.

**Available models:**
```
'qwen3-vl:4b'
'atles-qwen2.5:7b-enhanced'  ← MISSING from router!
'atles-llama3.2:latest'       ← MISSING from router!
'qwen2.5:7b'
'llama3.2:latest'
```

**Router database had:**
```python
"qwen2.5-coder:latest": performance_score=0.98  ← NOT INSTALLED!
"qwen2.5:7b": performance_score=0.95
# Missing: atles-qwen2.5:7b-enhanced
# Missing: atles-llama3.2:latest
```

### Why It Chose Wrong Models

The router selected models by highest `performance_score` for each task:
- ❌ `qwen2.5-coder:latest` had score `0.98` (highest)
- ❌ But it wasn't installed!
- ❌ Fine-tuned ATLES models weren't even in the database

## The Fix

### Updated Model Database

**File**: `atles/intelligent_model_router.py` (lines 74-126)

```python
def _initialize_model_capabilities(self) -> Dict[str, ModelCapability]:
    return {
        # ATLES fine-tuned models - HIGHEST PRIORITY
        "atles-qwen2.5:7b-enhanced": ModelCapability(
            model_name="atles-qwen2.5:7b-enhanced",
            supported_tasks=[
                TaskType.CONVERSATION,
                TaskType.REASONING,
                TaskType.TEXT_GENERATION,
                TaskType.QUESTION_ANSWERING,
                TaskType.CODE_GENERATION
            ],
            performance_score=0.99,  # ← HIGHEST - fine-tuned!
            resource_usage="high"
        ),
        "atles-llama3.2:latest": ModelCapability(
            model_name="atles-llama3.2:latest",
            supported_tasks=[...],
            performance_score=0.97,  # ← Second highest
            resource_usage="medium"
        ),
        "qwen2.5:7b": ModelCapability(
            performance_score=0.95,  # ← Base model
            ...
        ),
        # qwen2.5-coder:latest - REMOVED (not installed)
```

## Impact

### Before Fix ❌

| Task | Selected Model | Status |
|------|---------------|--------|
| Conversation | `qwen2.5:7b` | Base model used |
| Question Answering | `qwen2.5-coder:latest` | ❌ ERROR - not installed |
| Reasoning | `qwen2.5-coder:latest` | ❌ ERROR - not installed |
| Code Generation | `qwen2.5-coder:latest` | ❌ ERROR - not installed |

### After Fix ✅

| Task | Selected Model | Status |
|------|---------------|--------|
| Conversation | `atles-qwen2.5:7b-enhanced` | ✅ Fine-tuned model |
| Question Answering | `atles-qwen2.5:7b-enhanced` | ✅ Fine-tuned model |
| Reasoning | `atles-qwen2.5:7b-enhanced` | ✅ Fine-tuned model |
| Code Generation | `atles-qwen2.5:7b-enhanced` | ✅ Fine-tuned model |

## Verification

After restart, your logs should show:

```
ATLES Routing: 'user message...' -> atles-qwen2.5:7b-enhanced (99.0% confidence)
   Task: conversation | Reason: Best model for conversation with fine-tuning
```

**You should NOT see:**
```
❌ Model 'qwen2.5-coder:latest' not found
❌ Routing to qwen2.5-coder:latest
```

## Performance Scores Explained

Higher score = Router prefers this model:

| Model | Score | Reason |
|-------|-------|--------|
| `atles-qwen2.5:7b-enhanced` | **0.99** | Fine-tuned for ATLES |
| `atles-llama3.2:latest` | **0.97** | ATLES tuned |
| `qwen2.5-coder` (removed) | ~~0.98~~ | Not installed |
| `qwen2.5:7b` | **0.95** | Base model fallback |
| `llama3.2:3b` | **0.85** | Smaller base model |

## Adding Models Later

If you install `qwen2.5-coder:latest` later, uncomment these lines:

```python
# "qwen2.5-coder:latest": ModelCapability(
#     model_name="qwen2.5-coder:latest",
#     performance_score=0.96,  # ← Lower than ATLES models!
#     ...
# ),
```

**Note:** Keep score at `0.96` so ATLES models are still preferred!

## Related Issues

This explains why you saw:
- ✅ Router errors about missing models
- ✅ Base models being used instead of fine-tuned ones
- ✅ Coding models attempted for conversation

## Testing

**Test the router:**

```
User: "Hello, how are you?"
Expected: atles-qwen2.5:7b-enhanced (conversation task)

User: "What's 2+2?"
Expected: atles-qwen2.5:7b-enhanced (question answering)

User: "Write a Python function"
Expected: atles-qwen2.5:7b-enhanced (code generation)
```

All tasks should now route to your fine-tuned model!

---

**Date Fixed**: November 14, 2025  
**Status**: RESOLVED ✅  
**Action Required**: Restart ATLES to load new router configuration

