# ATLES Proactive Messaging System

## Overview
ATLES now includes an intelligent proactive messaging system that can detect when you're idle and offer assistance, including overnight messaging capabilities.

## Features

### 🕐 Overnight Messaging
- **4+ hour inactivity trigger**: Sends messages if you've been inactive for 4+ hours
- **Overnight hours**: Only triggers between 10 PM and 8 AM
- **Morning check-in**: Special message if you were inactive for 6+ hours overnight

### ⏰ Regular Idle Detection
- **1+ hour inactivity**: Sends check-in messages during normal hours
- **Smart timing**: Respects minimum intervals between messages
- **Constitutional safeguards**: Won't spam or be intrusive

### 🧠 Intelligent Context
- **Screen monitoring**: Knows what applications you're using
- **Focus respect**: Won't disturb you in development/creative apps
- **Pattern learning**: Adapts to your usage patterns

### 🤖 Self-Review & Learning
- **Downtime analysis**: Reviews conversation logs during idle periods
- **Pattern recognition**: Identifies conversation themes and topics
- **Continuous improvement**: Learns from interaction patterns
- **Insights sharing**: Provides actionable recommendations

## Configuration

### Quick Setup
1. **Enable proactive messaging**: Set `"enabled": true` in `atles_config.json`
2. **Adjust thresholds**: Modify timing values as needed
3. **Restart ATLES**: Changes take effect immediately

### Configuration Options (`atles_config.json`)

```json
{
  "proactive_messaging": {
    "enabled": true,                    // Enable/disable system
    "overnight_messaging": true,        // Allow overnight messages
    "idle_threshold_minutes": 60,       // Minutes before idle check-in
    "overnight_threshold_hours": 4,     // Hours before overnight message
    "morning_checkin_hours": 6,         // Hours for morning check-in
    "max_messages_per_hour": 4,         // Maximum messages per hour
    "min_time_between_messages_hours": 1, // Minimum time between messages
    "self_review_enabled": true,        // Enable self-review during downtime
    "self_review_threshold_minutes": 120, // Minutes before self-review starts
    "self_review_interval_hours": 4     // Hours between self-reviews
  }
}
```

## Testing

### Manual Testing
1. **Click "Test Proactive" button** in the ATLES interface
2. **Choose message type** from the dropdown menu:
   - Idle Check-in
   - Overnight Check-in
   - Morning Check-in
   - Self-Review
   - Interesting Window
   - Clipboard Error

### Viewing Insights
1. **Click "View Insights" button** to see conversation analysis
2. **Review patterns** identified during downtime
3. **Check recommendations** for improving interactions

### Overnight Testing
1. **Leave ATLES running** overnight
2. **Don't interact** with your computer for 4+ hours
3. **Check for messages** in the morning
4. **Verify timing** - should only trigger during overnight hours (10 PM - 8 AM)

## Message Types

### 🤖 Idle Check-in
- **Trigger**: 1+ hour of inactivity
- **Message**: "You've been quiet for a while. Just checking in - is there anything I can help you with?"

### 🌙 Overnight Check-in
- **Trigger**: 4+ hours of inactivity during overnight hours
- **Message**: "I notice you've been inactive for several hours. If you're working late or need assistance, I'm here to help!"

### 🌅 Morning Check-in
- **Trigger**: 6+ hours of inactivity, between 8-10 AM
- **Message**: "Good morning! I noticed you were inactive overnight. If you have any questions or need help getting started, I'm here to assist you!"

### 🤖 Self-Review
- **Trigger**: 2+ hours of inactivity (configurable)
- **Action**: Analyzes conversation logs, identifies patterns, and generates insights
- **Message**: "I've completed a self-review of our conversation history and identified some insights. Would you like me to share what I've learned about our interaction patterns?"

## Troubleshooting

### Proactive Messages Not Working?
1. **Check configuration**: Verify `atles_config.json` exists and is valid
2. **Enable proactive**: Ensure `"enabled": true`
3. **Check timing**: Verify thresholds are reasonable
4. **Restart ATLES**: Configuration changes require restart

### Too Many Messages?
1. **Increase intervals**: Set higher values for `min_time_between_messages_hours`
2. **Reduce frequency**: Lower `max_messages_per_hour`
3. **Adjust thresholds**: Increase `idle_threshold_minutes`

### Not Working Overnight?
1. **Check overnight settings**: Ensure `"overnight_messaging": true`
2. **Verify thresholds**: Check `overnight_threshold_hours` value
3. **Time window**: Messages only send between 10 PM - 8 AM
4. **Activity detection**: Ensure screen monitoring is working

## Advanced Configuration

### Constitutional Safeguards
```json
{
  "constitutional_safeguards": {
    "min_pattern_observations": 1,      // Minimum observations before acting
    "min_confidence_threshold": 0.80    // Confidence level required
  }
}
```

### Debug Settings
```json
{
  "debug_settings": {
    "proactive_debug": true,            // Enable debug logging
    "function_call_debug": false        // Function call debugging
  }
}
```

## Best Practices

1. **Start conservative**: Begin with higher thresholds and reduce gradually
2. **Monitor behavior**: Watch how the system behaves in your environment
3. **Adjust timing**: Fine-tune based on your work patterns
4. **Test thoroughly**: Use the test button to verify functionality
5. **Respect focus**: The system automatically avoids disturbing you in development apps

## Technical Details

- **Check frequency**: Proactive triggers checked every minute
- **Memory persistence**: Settings and patterns saved between sessions
- **Error handling**: Graceful fallback if configuration fails to load
- **Performance**: Minimal impact on system resources
- **Integration**: Works with existing ATLES screen monitoring and memory systems
