# 🚀 Learning Daemon - Quick Start

## 30-Second Start

```bash
# Windows
start_atles_daemon.bat

# Linux/Mac
python start_atles_with_daemon.py
```

**That's it!** The daemon will:
1. ✅ Start in background
2. ✅ Launch ATLES chat
3. ✅ Learn from your conversations automatically
4. ✅ Create detailed logs

---

## What You Get

### Automatic Learning
- **🧠 Memory Processing**: Extracts topics and patterns
- **🎓 Model Fine-Tuning**: Improves with each session
- **📝 Detailed Logs**: Complete learning history
- **📊 Statistics**: Track improvement over time

### Zero Effort Required
- Starts automatically
- Runs in background
- Processes on session end
- Creates logs automatically

---

## Usage Patterns

### Pattern 1: Auto-Start (Recommended)

```bash
# Just run this every time you start ATLES
start_atles_daemon.bat
```

Daemon starts → You chat → Session ends → Learning happens automatically

### Pattern 2: Always-On Daemon

```bash
# Start daemon once (runs 24/7)
python -m atles.autonomous_learning_daemon

# Then use ATLES normally
streamlit run streamlit_chat.py
```

Daemon always running → Multiple sessions → Continuous learning

### Pattern 3: Programmatic Control

```python
from atles.daemon_integration import SessionTracker

tracker = SessionTracker()
tracker.start_session()
tracker.log_message("user", "Hello")
tracker.log_message("assistant", "Hi!")
tracker.end_session()  # Triggers learning
```

---

## Check Status

### Quick Status

```bash
python -c "from atles.autonomous_learning_daemon import get_daemon; print(get_daemon().get_status())"
```

### View Logs

```bash
# Daemon activity
cat atles_memory/learning_daemon/daemon.log

# Session logs
ls atles_memory/learning_daemon/logs/

# Statistics
cat atles_memory/learning_daemon/logs/daemon_stats.json
```

---

## Integration Examples

### Streamlit App

```python
import streamlit as st
from atles.daemon_integration import SessionTracker

# Initialize tracker
if 'tracker' not in st.session_state:
    st.session_state.tracker = SessionTracker()
    st.session_state.session_id = st.session_state.tracker.start_session()

# Chat logic
user_input = st.chat_input("Your message")
if user_input:
    # Log user message
    st.session_state.tracker.log_message("user", user_input)
    
    # Get AI response
    response = get_ai_response(user_input)
    
    # Log assistant message
    st.session_state.tracker.log_message("assistant", response)

# On app close (in sidebar or button)
if st.button("End Session"):
    st.session_state.tracker.end_session()
    st.success("Session saved for learning!")
```

### Console App

```python
from atles.daemon_integration import SessionTracker

tracker = SessionTracker()
tracker.start_session()

print("Chat with ATLES (type 'exit' to quit)")

while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    
    tracker.log_message("user", user_input)
    response = get_ai_response(user_input)
    tracker.log_message("assistant", response)
    
    print(f"ATLES: {response}")

tracker.end_session()
print("Learning from this session...")
```

### API Integration

```python
from flask import Flask, request, jsonify
from atles.daemon_integration import get_tracker

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    session_id = request.json.get('session_id')
    
    tracker = get_tracker()
    if not tracker.current_session or tracker.current_session['session_id'] != session_id:
        tracker.start_session(session_id)
    
    tracker.log_message("user", user_message)
    response = get_ai_response(user_message)
    tracker.log_message("assistant", response)
    
    return jsonify({"response": response})

@app.route('/end-session', methods=['POST'])
def end_session():
    tracker = get_tracker()
    tracker.end_session()
    return jsonify({"status": "Learning initiated"})
```

---

## Troubleshooting

### Daemon Not Starting?

```bash
# Check if running
ps aux | grep daemon

# Start manually
python -m atles.autonomous_learning_daemon
```

### Sessions Not Processing?

```bash
# Check session directory
ls atles_memory/learning_daemon/sessions/

# Check daemon log for errors
tail -f atles_memory/learning_daemon/daemon.log
```

### Want to Stop Daemon?

```python
from atles.autonomous_learning_daemon import stop_daemon
stop_daemon()
```

Or just Ctrl+C the daemon process.

---

## Key Files

| File/Directory | Purpose |
|---------------|---------|
| `atles/autonomous_learning_daemon.py` | Main daemon code |
| `atles/daemon_integration.py` | Easy integration helpers |
| `start_atles_with_daemon.py` | Startup script |
| `start_atles_daemon.bat` | Windows batch file |
| `atles_memory/learning_daemon/` | All daemon data |
| `atles_memory/learning_daemon/daemon.log` | Main log |
| `atles_memory/learning_daemon/logs/` | Session logs |
| `atles_memory/learning_daemon/sessions/` | Session data |

---

## What Gets Logged

### Session Log Example

```json
{
  "session_id": "session_20240115_103000",
  "start_time": "2024-01-15T10:30:00",
  "end_time": "2024-01-15T10:35:00",
  "messages_count": 8,
  "tokens_processed": 0,
  "memory_items_created": 3,
  "fine_tune_applied": true,
  "fine_tune_loss": 0.15,
  "model_version": "atles-qwen2.5:7b-enhanced",
  "improvements": [
    "Extracted topics: programming, debugging",
    "Identified patterns: prefers_code_examples",
    "Prepared training data: training_session_20240115_103000_103500.jsonl",
    "Fine-tuned with 4 examples"
  ],
  "errors": []
}
```

---

## Best Practices

### ✅ DO
- Let daemon run 24/7 for best results
- Review logs weekly
- Monitor daemon status
- Backup learning data

### ❌ DON'T
- Stop daemon unnecessarily
- Delete logs (unless space constrained)
- Manually edit session files
- Run multiple daemon instances

---

## Quick Commands

```bash
# Start everything
start_atles_daemon.bat

# Check status
python -c "from atles.autonomous_learning_daemon import get_daemon; print(get_daemon().get_status())"

# View recent logs
tail -20 atles_memory/learning_daemon/daemon.log

# View session count
ls atles_memory/learning_daemon/logs/ | wc -l

# Check disk usage
du -sh atles_memory/learning_daemon/
```

---

## Support

- **Full Documentation**: `docs/AUTONOMOUS_LEARNING_DAEMON.md`
- **Code**: `atles/autonomous_learning_daemon.py`
- **Logs**: `atles_memory/learning_daemon/`

---

**You're ready to go!** 🚀

Just run `start_atles_daemon.bat` and let ATLES learn from every conversation!

