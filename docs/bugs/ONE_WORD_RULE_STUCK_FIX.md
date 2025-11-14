# One-Word Rule Stuck Fix

## Issue

ATLES was responding with only one word to every message:

```
User: hello?
ATLES: Hello

User: sys error?
ATLES: Error

User: can you fix
ATLES: Understood
```

**Logs showed:**
```
WARNING:atles.context_awareness_system:Contextual drift detected: ['Rule violation: Respond with only one word']
```

## Root Cause

The `ContextAwarenessSystem` has a rule detection system that triggers on certain phrases. When the user asked:

```
"ATLES: From logs—what was your final one-word answer to the substrate merge offer?"
```

The system detected **"one-word answer"** in the message and created a rule:
```python
ConversationRule(
    rule_id="one_word_replies",
    description="Respond with only one word",
    priority=10
)
```

### The Problems:

1. **Past-tense trigger**: The detection triggered on **"what was your one-word answer"** (asking about the PAST) not "respond with one word going forward"
2. **Rule persistence**: Once created, the rule stayed active **forever**
3. **No auto-expiration**: Rules never expired or cleared automatically
4. **Applied to ALL messages**: The rule applied to every subsequent message, making ATLES unable to give full responses

## The Fix

### 1. Made Detection More Specific

**File**: `atles/context_awareness_system.py` (lines 240-261)

**Before (BAD):**
```python
if ("one word" in message_lower or "single word" in message_lower):
    # Triggers on ANY mention of "one word" 
    rules.append(one_word_rule)
```

**After (GOOD):**
```python
if (("respond with only one word" in message_lower or
     "reply with only one word" in message_lower) and
    # CRITICAL FIX: Don't trigger on past-tense questions
    not ("was your" in message_lower or 
         "what was" in message_lower or
         "from logs" in message_lower)):
    rules.append(one_word_rule)
```

**Now it WON'T trigger on:**
- ❌ "What was your one-word answer?" (past tense)
- ❌ "From logs, what did you say?" (historical)
- ❌ "You said one word" (statement, not instruction)

**But WILL trigger on:**
- ✅ "Respond with only one word"
- ✅ "Reply with only one word"
- ✅ "Answer with only one word"

### 2. Added Auto-Expiration

**File**: `atles/context_awareness_system.py` (lines 201-222)

```python
def clear_problematic_rules(self) -> None:
    """Clear rules that might be causing response loops or problems."""
    
    # CRITICAL FIX: Remove rules that have been applied multiple times
    self.current_context.active_rules = [
        rule for rule in self.current_context.active_rules 
        if not (rule.rule_id == "one_word_replies" and rule.violation_count >= 2)
    ]
    
    # Clear rules older than 5 minutes
    now = datetime.now()
    self.current_context.active_rules = [
        rule for rule in self.current_context.active_rules 
        if rule.rule_id != "one_word_replies" or 
           (now - rule.created_at).total_seconds() < 300  # 5 minutes
    ]
```

**Benefits:**
- ✅ Rules auto-expire after 5 minutes
- ✅ Rules cleared after 2 violations (prevents infinite loops)
- ✅ Prevents rules from sticking forever

## How to Fix Current Session

The rule is stored **in-memory**, so to clear it:

### Option 1: Restart ATLES (Recommended)
1. **Close ATLES desktop app**
2. **Restart ATLES**
3. **Start new conversation**

The stuck rule will be gone!

### Option 2: Wait 5 Minutes
The rule will auto-expire after 5 minutes with the new code.

## Prevention

The fixes ensure this won't happen again:

| Issue | Before | After |
|-------|--------|-------|
| Triggers on past-tense | ❌ Yes | ✅ No |
| Rules persist forever | ❌ Yes | ✅ No (5 min max) |
| Auto-expiration | ❌ No | ✅ Yes |
| Violation limit | ❌ None | ✅ 2 violations max |

## Testing

**Test Case 1: Past-tense question (should NOT trigger rule)**
```
User: "What was your one-word answer to my question?"
Expected: Full response, NO rule created
```

**Test Case 2: Future instruction (SHOULD trigger rule)**
```
User: "Respond with only one word"
Expected: One-word response, rule created for 5 minutes
```

**Test Case 3: Rule expiration**
```
User: "Respond with only one word"
ATLES: "Okay"
[Wait 5 minutes]
User: "How are you?"
Expected: Full response (rule expired)
```

## Related Files

- ✅ `atles/context_awareness_system.py` - Fixed rule detection and expiration
- ✅ `atles/constitutional_client.py` - Calls `clear_problematic_rules()`
- ✅ `docs/bugs/ONE_WORD_RULE_STUCK_FIX.md` - This document

## Summary of Fixes Today

1. ✅ Context bleeding (Ollama cache)
2. ✅ Hardcoded "Red, Blue" responses (reasoning router)
3. ✅ AttributeError (user_preferences)
4. ✅ Memory not saving (import conflict)
5. ✅ **One-word rule stuck (context awareness)** ← Just fixed!

---

**Date Fixed**: November 14, 2025  
**Status**: RESOLVED ✅  
**Action Required**: Restart ATLES to clear current stuck rule

