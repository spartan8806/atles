# 🚀 Learning Daemon - Cheat Sheet

## Quick Commands

```bash
# Start Everything
start_atles_daemon.bat

# Run Test
python test_learning_daemon.py

# Check Status
python -c "from atles.autonomous_learning_daemon import get_daemon; print(get_daemon().get_status())"

# View Logs
tail -f atles_memory/learning_daemon/daemon.log

# View Stats
cat atles_memory/learning_daemon/logs/daemon_stats.json
```

## 3-Line Integration

```python
from atles.daemon_integration import SessionTracker
tracker = SessionTracker()
tracker.start_session()
# ... chat happens ...
tracker.end_session()  # Triggers learning
```

## One-Liner Tracking

```python
from atles.daemon_integration import track_user_message, track_assistant_message, end_tracked_session

track_user_message("Hello")
track_assistant_message("Hi!")
end_tracked_session()
```

## Key Files

| File | Purpose |
|------|---------|
| `start_atles_daemon.bat` | One-click start |
| `test_learning_daemon.py` | Test everything |
| `atles/autonomous_learning_daemon.py` | Main daemon |
| `atles/daemon_integration.py` | Easy integration |
| `atles_memory/learning_daemon/` | All data |

## What Gets Learned

- **Topics**: programming, debugging, api_development
- **Preferences**: explanation style, code examples
- **Patterns**: user communication style
- **Context**: conversation history

## Session Log Location

```
atles_memory/learning_daemon/logs/session_log_*.json
```

## Statistics Location

```
atles_memory/learning_daemon/logs/daemon_stats.json
```

## Stop Daemon

```python
from atles.autonomous_learning_daemon import stop_daemon
stop_daemon()
```

## Documentation

| Doc | Use When |
|-----|----------|
| `NEW_FEATURE_AUTONOMOUS_LEARNING.md` | Quick overview |
| `LEARNING_DAEMON_README.md` | Getting started |
| `docs/DAEMON_QUICK_START.md` | Fast reference |
| `docs/AUTONOMOUS_LEARNING_DAEMON.md` | Complete guide |
| `docs/LEARNING_DAEMON_ARCHITECTURE.md` | Architecture details |

## Common Patterns

### Streamlit
```python
if 'tracker' not in st.session_state:
    st.session_state.tracker = SessionTracker()
    st.session_state.tracker.start_session()
```

### Console
```python
tracker = SessionTracker()
tracker.start_session()
while chatting:
    tracker.log_message("user", input())
    tracker.log_message("assistant", response())
tracker.end_session()
```

### API
```python
@app.route('/chat', methods=['POST'])
def chat():
    track_user_message(request.json['message'])
    track_assistant_message(response)
    return {"response": response}
```

## Troubleshooting

```bash
# Not working?
tail -f atles_memory/learning_daemon/daemon.log

# Sessions stuck?
ls atles_memory/learning_daemon/sessions/

# High CPU?
ps aux | grep daemon
```

## Quick Test

```bash
python test_learning_daemon.py
```

Expected: ✅ All tests pass, 3 sessions processed

---

**Get Started**: `start_atles_daemon.bat` 🚀

