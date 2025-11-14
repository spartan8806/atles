# ATLES Scratchpad System - Internal Thinking Workspace

## Overview

The Scratchpad System gives ATLES an internal "thinking space" where it can draft, critique, and revise responses **before** sending them to the user. This significantly improves response quality without the user seeing the messy draft stages.

**Key Features:**
- Internal thinking (invisible to user)
- Multi-stage response generation: Draft → Critique → Revise → Send
- Self-critique capability
- Automatic archival for analysis and debugging
- Configurable thinking depth

**Note:** Unlike ATLAS (which has its own trainable model), ATLES uses external models like Qwen. The scratchpad here is purely for improving response quality, not for training data generation.

## How It Works

```
User: "What is the capital of France?"
    ↓
┌─────────────────────────────────────┐
│  INTERNAL THINKING (user can't see) │
├─────────────────────────────────────┤
│  Stage 1: Draft                     │
│  "Paris is the capital."            │
│                                     │
│  Stage 2: Self-Critique             │
│  "Too brief, add context"           │
│                                     │
│  Stage 3: Revision                  │
│  "Paris is the capital and largest  │
│   city of France, located on the    │
│   Seine River..."                   │
│                                     │
│  Stage 4: Final Check               │
│  ✓ Complete ✓ Accurate ✓ Clear     │
└─────────────────────────────────────┘
    ↓
User sees: "Paris is the capital and largest city of France..."
```

## Quick Start

### Using the Thinking Client

```python
from atles import create_thinking_constitutional_client

# Create client with thinking enabled
client = create_thinking_constitutional_client()

# Generate response (with internal thinking)
response = client.generate("llama3.2", "Explain quantum computing")

# User only sees the polished final response
print(response)

# Check thinking stats
stats = client.get_thinking_stats()
print(f"Thoughts recorded: {stats['num_thoughts']}")
```

### Configuration

Edit `config/scratchpad_config.yaml`:

```yaml
scratchpad:
  enabled: true  # Enable/disable thinking
  mode: "every_response"  # always think, or "complex_only"
  
  thinking:
    max_revisions: 2  # How many times to revise
    critique_enabled: true  # Enable self-critique
    self_check_enabled: true  # Final check before sending
```

## Storage Structure

```
atles_memory/scratchpad/
├── active/
│   └── session_20251107_143000.jsonl  # Current session thoughts
├── archive/
│   └── 2025-11-07/
│       ├── session_001.jsonl  # Archived sessions
│       ├── key_thoughts.jsonl  # Important patterns
│       └── summary.txt  # Human-readable summary
└── scratchpad.log  # System logs
```

## Thought Format

Each thought is stored as structured JSON:

```json
{
  "timestamp": "2025-11-07T14:30:00",
  "user_input": "What is quantum computing?",
  "thought_stages": {
    "initial": {
      "timestamp": "2025-11-07T14:30:01",
      "data": {
        "text": "Quantum computing uses quantum bits...",
        "confidence": 0.7
      }
    },
    "critique": {
      "timestamp": "2025-11-07T14:30:02",
      "data": {
        "text": "Too technical, needs simpler explanation",
        "needs_revision": true,
        "issues": ["too technical", "no examples"]
      }
    },
    "revision_1": {
      "timestamp": "2025-11-07T14:30:03",
      "data": {
        "text": "Quantum computing is a new type of computing...",
        "improvements": ["simpler language", "added examples"]
      }
    },
    "final": {
      "timestamp": "2025-11-07T14:30:04",
      "data": {
        "text": "Quantum computing...",
        "ready": true
      }
    }
  },
  "is_key_thought": false,
  "metadata": {
    "response_time": 4.2,
    "num_stages": 4
  }
}
```

## Key Thoughts

Not all thoughts are equally important. The system identifies "key thoughts":

### Types of Key Thoughts

1. **Multiple Revisions** - Response needed 2+ revisions (indicates complexity)
2. **User Correction** - User corrected ATLES (important learning opportunity)
3. **Novel Solution** - Creative/unexpected approach
4. **Error Recovery** - ATLES caught and fixed its own error

### Marking Key Thoughts

```python
# Manually mark when user corrects ATLES
client.mark_user_correction("user_correction")
```

## Daily Archival

The system automatically archives thoughts for analysis:

```python
from atles import ScratchpadArchiver

archiver = ScratchpadArchiver()

# Archive yesterday's sessions
stats = archiver.archive_daily()
print(f"Archived {stats['sessions_archived']} sessions")
print(f"Found {stats['key_thoughts']} key thoughts")

# Get overall stats
stats = archiver.get_archive_stats()
print(f"Total dates: {stats['total_dates']}")
print(f"Total key thoughts: {stats['total_key_thoughts']}")
```

## Performance Impact

### Response Time
- Without thinking: ~1-2 seconds
- With thinking: ~3-6 seconds
- Trade-off: Slower but higher quality responses

### Storage
- Per thought: ~1-5 KB
- Per session: ~100-500 KB (100-1000 thoughts)
- 30-day archive: ~30-150 MB

## Configuration Options

### Thinking Modes

1. **every_response** (recommended) - Always think before responding
2. **complex_only** - Only for complex queries (faster for simple questions)
3. **manual** - Only when explicitly triggered

### Thinking Depth

```yaml
thinking:
  max_revisions: 2  # 0 = no revision, 1-3 = increasing quality
  critique_enabled: true  # Self-critique stage
  self_check_enabled: true  # Final check stage
  min_confidence: 0.8  # Skip revision if confidence > 0.8
```

### Archival Settings

```yaml
archival:
  frequency: "daily"  # Archive old sessions
  keep_days: 30  # Keep last 30 days
  extract_key_thoughts: true  # Extract important patterns
  create_summaries: true  # Human-readable summaries
```

## Use Cases

### 1. Improved Response Quality
ATLES can catch and fix errors before the user sees them.

### 2. Debugging
Review archived thoughts to understand why ATLES responded a certain way.

### 3. System Improvement
Analyze key thoughts to identify patterns and improvement areas.

### 4. User Feedback Analysis
Track user corrections to understand where ATLES needs improvement.

## API Reference

### ThinkingConstitutionalClient

```python
class ThinkingConstitutionalClient(LightweightConstitutionalClient):
    def generate(model: str, prompt: str, **kwargs) -> str
        """Generate response with internal thinking"""
    
    def mark_user_correction(reason: str = "user_correction")
        """Mark last thought as key due to user correction"""
    
    def get_thinking_stats() -> Dict
        """Get statistics about thinking process"""
```

### Scratchpad

```python
class Scratchpad:
    def __init__(session_dir, archive_dir)
    def start_thought(user_input: str)
    def write_thought(stage: str, data: Dict)
    def mark_key_thought(reason: str)
    def finalize_thought()
    def read_thoughts() -> List[Dict]
    def get_key_thoughts() -> List[Dict]
    def get_session_stats() -> Dict
```

### ScratchpadArchiver

```python
class ScratchpadArchiver:
    def __init__(session_dir, archive_dir, keep_days)
    def archive_daily(date: str = None) -> Dict
    def extract_key_thoughts(date_dir: Path) -> List[Dict]
    def get_archive_stats() -> Dict
```

## Troubleshooting

### Issue: Thinking is too slow

**Solution:** 
- Set `mode: "complex_only"` to skip thinking for simple requests
- Reduce `max_revisions` from 2 to 1
- Disable `critique_enabled` for faster responses

### Issue: Not seeing improvement in responses

**Solution:**
- Increase `max_revisions` to 2 or 3
- Ensure `critique_enabled: true`
- Check logs to verify thinking is actually happening

### Issue: Storage growing too large

**Solution:**
- Reduce `keep_days` from 30 to 7 or 14
- Enable `compress_archives: true` (future feature)
- Manually delete old archives

## Examples

### Example 1: Simple Question
```
User: "Hi"
Thinking: SKIPPED (too simple)
Response: "Hello! How can I help you today?"
```

### Example 2: Complex Question
```
User: "Explain how neural networks learn"

Internal Thinking:
1. Draft: "Neural networks learn using backpropagation..."
2. Critique: "Too technical, needs simpler explanation"
3. Revision: "Neural networks learn by adjusting connections..."
4. Final: "Neural networks learn similar to how humans do..."

User Sees: "Neural networks learn similar to how humans do..."
```

### Example 3: User Correction
```
User: "What's 2+2?"
ATLES: "5"
User: "No, it's 4"

# Mark as key thought
client.mark_user_correction("user_correction")
# This helps identify calculation errors for future improvements
```

## Future Enhancements

1. **Adaptive Thinking** - Automatically adjust thinking depth based on question complexity
2. **Learning from Corrections** - Use user corrections to improve future responses
3. **Parallel Thinking** - Generate multiple draft responses and choose the best
4. **Confidence Scoring** - Better estimate of response quality

## Summary

The Scratchpad System gives ATLES the ability to "think before it speaks", resulting in:
- ✅ Higher quality responses
- ✅ Fewer errors
- ✅ Better user experience
- ✅ Improved debugging capabilities
- ✅ Data for system improvements

**Trade-off:** Slightly slower responses for significantly better quality.

