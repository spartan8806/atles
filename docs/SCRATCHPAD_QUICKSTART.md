# ATLES Scratchpad - Quick Start Guide

## What is it?

The Scratchpad System gives ATLES an internal "thinking workspace" where it can draft, critique, and revise responses before sending them to you. You only see the final polished response, not the messy drafts.

## Setup (30 seconds)

### 1. Enable Scratchpad

Already done! Scratchpad is enabled by default in ATLES.

### 2. Verify Configuration

Check `config/scratchpad_config.yaml`:

```yaml
scratchpad:
  enabled: true  # ✓ Thinking enabled
  mode: "every_response"  # Always think before responding
```

## Usage

### Basic Usage

```python
from atles import create_thinking_constitutional_client

# Create client
client = create_thinking_constitutional_client()

# Ask a question - ATLES will think internally before responding
response = client.generate("llama3.2", "Explain quantum computing")

# You see only the polished final response
print(response)
```

### What Happens Internally

```
Your Question → Draft → Critique → Revise → Final Response → You
                  ↓        ↓         ↓          ↓
              [All saved in scratchpad for analysis]
```

### Mark User Corrections

When you correct ATLES, mark it so the system can learn:

```python
# ATLES gave wrong answer
response = client.generate("llama3.2", "What's 2+2?")
# User says "No, it's 4"

# Mark the correction
client.mark_user_correction("user_correction")
```

## Configuration

### Thinking Modes

Edit `config/scratchpad_config.yaml`:

```yaml
scratchpad:
  mode: "every_response"  # Options:
    # - "every_response" (always think)
    # - "complex_only" (skip simple questions)
    # - "manual" (only when triggered)
```

### Thinking Depth

```yaml
thinking:
  max_revisions: 2  # How many times to revise (0-3)
  critique_enabled: true  # Self-critique before sending
  self_check_enabled: true  # Final quality check
```

### Speed vs Quality

**For Speed:**
```yaml
mode: "complex_only"  # Skip simple questions
thinking:
  max_revisions: 1  # Less revision
  critique_enabled: false  # Skip critique
```

**For Quality:**
```yaml
mode: "every_response"  # Always think
thinking:
  max_revisions: 2  # More revision
  critique_enabled: true  # Enable critique
```

## Monitoring

### Session Stats

```python
# Get stats about current session
stats = client.get_thinking_stats()

print(f"Thoughts: {stats['num_thoughts']}")
print(f"Key thoughts: {stats['key_thoughts']}")
print(f"Avg response time: {stats['avg_response_time']:.2f}s")
```

### Archive Stats

```python
from atles import ScratchpadArchiver

archiver = ScratchpadArchiver()
stats = archiver.get_archive_stats()

print(f"Total sessions: {stats['total_sessions']}")
print(f"Key thoughts: {stats['total_key_thoughts']}")
```

## File Locations

### Active Session
```
atles_memory/scratchpad/active/session_YYYYMMDD_HHMMSS.jsonl
```
Current session's internal thoughts.

### Archives
```
atles_memory/scratchpad/archive/YYYY-MM-DD/
├── session_001.jsonl     # Archived thoughts
├── key_thoughts.jsonl    # Important patterns
└── summary.txt           # Human-readable summary
```

### Logs
```
atles_memory/scratchpad/scratchpad.log
```

## Common Tasks

### Disable Thinking Temporarily

```python
# In config
scratchpad:
  enabled: false
```

Or use the lightweight client instead:

```python
from atles import create_lightweight_constitutional_client
client = create_lightweight_constitutional_client()
```

### View Today's Key Thoughts

```bash
# On Windows
type atles_memory\scratchpad\archive\2025-11-07\summary.txt

# On Linux/Mac
cat atles_memory/scratchpad/archive/2025-11-07/summary.txt
```

### Archive Yesterday's Sessions

```python
from atles import ScratchpadArchiver

archiver = ScratchpadArchiver()
stats = archiver.archive_daily()  # Archives yesterday

print(f"Archived {stats['sessions_archived']} sessions")
print(f"Found {stats['key_thoughts']} key thoughts")
```

### Clean Up Old Archives

```yaml
# In config
archival:
  keep_days: 30  # Keep last 30 days (or less to save space)
```

## Troubleshooting

### "Too slow!"

**Option 1:** Skip simple questions
```yaml
mode: "complex_only"
```

**Option 2:** Reduce revisions
```yaml
thinking:
  max_revisions: 1  # Down from 2
```

**Option 3:** Disable temporarily
```yaml
enabled: false
```

### "Not seeing improvement"

**Enable full thinking:**
```yaml
mode: "every_response"
thinking:
  max_revisions: 2
  critique_enabled: true
  self_check_enabled: true
```

### "Taking up too much space"

**Reduce retention:**
```yaml
archival:
  keep_days: 7  # Down from 30
```

## Best Practices

### ✅ DO

- Leave thinking enabled for better quality
- Mark user corrections so system can learn
- Review key thoughts periodically for insights
- Adjust `max_revisions` based on your needs

### ❌ DON'T

- Disable thinking for important questions
- Ignore user corrections (mark them!)
- Let archives grow unbounded (set `keep_days`)
- Expect instant responses (thinking takes 2-4 seconds)

## Quick Reference

| Task | Command |
|------|---------|
| Create thinking client | `create_thinking_constitutional_client()` |
| Generate with thinking | `client.generate(model, prompt)` |
| Mark correction | `client.mark_user_correction()` |
| Get stats | `client.get_thinking_stats()` |
| Archive sessions | `ScratchpadArchiver().archive_daily()` |
| Enable thinking | Set `enabled: true` in config |
| Disable thinking | Set `enabled: false` in config |

## Example Session

```python
from atles import create_thinking_constitutional_client

# Initialize
client = create_thinking_constitutional_client()

# Ask questions - ATLES thinks before responding
q1 = client.generate("llama3.2", "What is AI?")
print(f"Answer: {q1}\n")

q2 = client.generate("llama3.2", "Explain neural networks")
print(f"Answer: {q2}\n")

# If user corrects an answer
client.mark_user_correction("user_correction")

# View stats
stats = client.get_thinking_stats()
print(f"\nSession Stats:")
print(f"- Thoughts: {stats['num_thoughts']}")
print(f"- Key thoughts: {stats['key_thoughts']}")
print(f"- Avg time: {stats['avg_response_time']:.2f}s")
```

## Next Steps

- Read full documentation: `docs/SCRATCHPAD_SYSTEM.md`
- Customize configuration: `config/scratchpad_config.yaml`
- Review archived thoughts: `atles_memory/scratchpad/archive/`
- Monitor performance: Check `scratchpad.log`

## Support

For detailed information, see:
- **Full Docs:** `docs/SCRATCHPAD_SYSTEM.md`
- **Config:** `config/scratchpad_config.yaml`
- **Logs:** `atles_memory/scratchpad/scratchpad.log`

