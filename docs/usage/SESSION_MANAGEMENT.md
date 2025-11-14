# ATLES Session Management Guide

## Overview

ATLES now includes robust session management to prevent context bleeding and ensure clean conversation boundaries.

## Quick Start

### Basic Usage (Automatic)

The fixes are **automatic** - no code changes needed:

```python
from atles.ollama_client_sync import OllamaClientSync

client = OllamaClientSync()

# Just use it normally - cache-busting is automatic
response = client.generate("qwen2.5:7b", "Hello, ATLES!")
```

### Explicit Session Management (Recommended)

For cleaner conversation boundaries:

```python
from atles.ollama_client_sync import OllamaClientSync

client = OllamaClientSync()

# Start a new conversation
conversation_id = client.start_conversation()

# Have your conversation
response1 = client.generate("qwen2.5:7b", "What is quantum physics?")
response2 = client.generate("qwen2.5:7b", "Can you explain wave-particle duality?")

# End the conversation (clears context)
client.end_conversation()

# Start a new, isolated conversation
client.start_conversation()
response3 = client.generate("qwen2.5:7b", "What are the best pizza toppings?")
# This won't reference quantum physics
```

## API Reference

### `start_conversation(conversation_id=None)`

Start a new conversation session.

**Parameters:**
- `conversation_id` (str, optional): Custom conversation ID. If not provided, a UUID is generated.

**Returns:**
- `str`: The conversation ID

**Example:**
```python
conv_id = client.start_conversation("user_session_123")
print(f"Started conversation: {conv_id}")
```

### `end_conversation()`

End the current conversation and reset context tracking.

**Example:**
```python
client.end_conversation()
# Context is now cleared
```

### `generate(model, prompt, **kwargs)`

Generate a response with automatic cache-busting.

**Automatic Features:**
- Random seed for each request
- Response relevance validation
- Automatic retry on context bleeding detection

**Example:**
```python
response = client.generate(
    model="qwen2.5:7b",
    prompt="Explain neural networks"
)
```

## Best Practices

### 1. Use Explicit Session Management for Multi-Turn Conversations

```python
client.start_conversation("support_ticket_456")

# All related messages
response1 = client.generate("qwen2.5:7b", "I need help with login")
response2 = client.generate("qwen2.5:7b", "The password reset didn't work")
response3 = client.generate("qwen2.5:7b", "Can you check my account?")

client.end_conversation()
```

### 2. Reset Between Unrelated Topics

```python
# Topic 1: Science
client.start_conversation()
response = client.generate("qwen2.5:7b", "Explain photosynthesis")
client.end_conversation()

# Topic 2: Sports (completely unrelated)
client.start_conversation()
response = client.generate("qwen2.5:7b", "Who won the World Cup in 2022?")
client.end_conversation()
```

### 3. Monitor Context Bleeding Warnings

Enable debug logging to see warnings:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now you'll see warnings like:
# "⚠️ CONTEXT BLEEDING DETECTED: Response appears unrelated to prompt"
```

## Context Bleeding Detection

The system automatically detects when responses don't match prompts:

```python
# Example: If this prompt...
prompt = "Tell me about ancient Hittite civilization"

# ...gets a response like:
response = "There are 7 valid configurations: (Red, Red, Blue)..."

# The system will:
# 1. Detect the mismatch
# 2. Log a warning
# 3. Automatically retry with fresh context
# 4. Return the corrected response
```

## Advanced Usage

### Custom Cache-Busting Parameters

Override default cache-busting if needed:

```python
response = client.generate(
    model="qwen2.5:7b",
    prompt="Your prompt here",
    options={
        "seed": 42,  # Fixed seed for reproducibility
        "temperature": 0.9,  # Custom temperature
        "num_ctx": 8192,  # Larger context window
    }
)
```

### Checking Session State

```python
# Check if a conversation is active
if client.conversation_id:
    print(f"Active conversation: {client.conversation_id}")
    print(f"Messages sent: {client.message_count}")
else:
    print("No active conversation")
```

## Troubleshooting

### Issue: Getting Irrelevant Responses

**Solution**: The system should auto-detect and retry. If it persists:

```python
# Force a fresh conversation
client.end_conversation()
client.start_conversation()

# Try again
response = client.generate(model, prompt)
```

### Issue: Responses Reference Previous Conversation

**Solution**: Always call `end_conversation()` between topics:

```python
# BAD: No explicit boundary
response1 = client.generate("qwen2.5:7b", "Talk about physics")
response2 = client.generate("qwen2.5:7b", "Talk about cooking")
# May reference physics

# GOOD: Clear boundary
response1 = client.generate("qwen2.5:7b", "Talk about physics")
client.end_conversation()
client.start_conversation()
response2 = client.generate("qwen2.5:7b", "Talk about cooking")
# Won't reference physics
```

### Issue: Context Bleeding Still Occurring

1. **Check Ollama Version**: Ensure you're running latest Ollama
2. **Restart Ollama Server**: `ollama serve` (restart the service)
3. **Clear Server Cache**: Restart completely clears any server-side cache
4. **Check Logs**: Look for warnings in the logs

```bash
# Restart Ollama (Windows)
# Stop any running Ollama processes, then:
ollama serve

# Or restart via Task Manager
```

## Performance Considerations

### Cache-Busting Overhead

The cache-busting parameters add **minimal overhead** (< 1ms) but prevent catastrophic context bleeding.

### When to Use Session Management

- ✅ **Use explicit sessions** for: Multi-turn conversations, support tickets, tutorials
- ✅ **Use automatic only** for: Single-shot queries, one-off questions
- ❌ **Don't over-use**: Starting/ending sessions for every single message (unnecessary)

## Migration Guide

### From Old Code

**Before (no session management):**
```python
client = OllamaClientSync()
response = client.generate("qwen2.5:7b", prompt)
```

**After (same code works, but enhanced):**
```python
client = OllamaClientSync()
response = client.generate("qwen2.5:7b", prompt)
# Now includes automatic cache-busting and validation!
```

**After (with explicit sessions - recommended):**
```python
client = OllamaClientSync()
client.start_conversation()
response = client.generate("qwen2.5:7b", prompt)
client.end_conversation()
```

## Summary

| Feature | Status | Action Required |
|---------|--------|-----------------|
| Cache-busting | ✅ Automatic | None |
| Response validation | ✅ Automatic | None |
| Automatic retry | ✅ Automatic | None |
| Session tracking | ⚠️ Optional | Recommended for multi-turn |

**Bottom Line**: The fixes work automatically, but explicit session management gives you better control and cleaner conversation boundaries.

---

*For more details, see: [CONTEXT_BLEEDING_FIX.md](../bugs/CONTEXT_BLEEDING_FIX.md)*

