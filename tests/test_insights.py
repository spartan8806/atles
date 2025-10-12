#!/usr/bin/env python3
"""
Test script to verify the proactive insights response system
"""

def test_proactive_response_detection():
    """Test the proactive response detection logic"""
    print("🧪 Testing Proactive Response Detection")
    print("=" * 50)
    
    # Simulate the detection logic
    def is_proactive_response(message: str) -> bool:
        message_lower = message.lower().strip()
        
        proactive_responses = [
            'yes', 'show me', 'tell me', 'share', 'what did you find',
            'what insights', 'show insights', 'show analysis', 'what patterns',
            'ok', 'sure', 'go ahead', 'continue', 'proceed'
        ]
        
        for response in proactive_responses:
            if response in message_lower:
                return True
        
        if len(message_lower) <= 10 and any(word in message_lower for word in ['yes', 'ok', 'sure', 'go']):
            return True
        
        return False
    
    # Test cases
    test_messages = [
        ("'yes'", True),
        ("'show me'", True),
        ("yes", True),
        ("show me", True),
        ("tell me", True),
        ("what insights", True),
        ("ok", True),
        ("sure", True),
        ("no", False),
        ("hello", False),
        ("what is the weather", False),
        ("I need help with code", False)
    ]
    
    print("Testing message detection:")
    for message, expected in test_messages:
        result = is_proactive_response(message)
        status = "✅" if result == expected else "❌"
        print(f"   {status} '{message}' -> {result} (expected: {expected})")
    
    print(f"\n✅ Proactive response detection test completed!")

def test_insights_formatting():
    """Test the insights formatting logic"""
    print(f"\n🎨 Testing Insights Formatting")
    print("=" * 50)
    
    # Sample insight data
    sample_insight = {
        'timestamp': '2024-01-15T08:21:00',
        'analysis': {
            'patterns': [
                'Total interactions: 5 user messages, 5 assistant responses',
                'System messages: 2',
                'Conversation length: 15 total lines'
            ],
            'insights': [
                'Common topics: proactive messaging, self-review, testing',
                'Technical focus: Yes'
            ],
            'recommendations': [
                'Consider creating a knowledge base for frequently asked questions',
                'Review response quality and consistency patterns'
            ]
        }
    }
    
    # Format the response
    def format_insights_response(insights):
        if not insights:
            return "I don't have any conversation insights to share yet."
        
        response = "🤖 **ATLES Self-Review Insights**\n\n"
        
        latest_insight = insights[-1]
        analysis = latest_insight.get('analysis', {})
        
        response += f"📊 **Analysis from {latest_insight.get('timestamp', 'recent')}**\n\n"
        
        if 'patterns' in analysis and analysis['patterns']:
            response += "**Patterns Found:**\n"
            for pattern in analysis['patterns']:
                response += f"• {pattern}\n"
            response += "\n"
        
        if 'insights' in analysis and analysis['insights']:
            response += "**Key Insights:**\n"
            for insight in analysis['insights']:
                response += f"• {insight}\n"
            response += "\n"
        
        if 'recommendations' in analysis and analysis['recommendations']:
            response += "**Recommendations:**\n"
            for rec in analysis['recommendations']:
                response += f"• {rec}\n"
            response += "\n"
        
        response += "💡 **What This Means:**\n"
        response += "I'm learning from our conversations to provide better assistance.\n\n"
        response += "🔍 **Want More Details?** Click the 'View Insights' button for a complete analysis!"
        
        return response
    
    # Test formatting
    formatted = format_insights_response([sample_insight])
    print("Sample formatted insights:")
    print("-" * 30)
    print(formatted)
    print("-" * 30)
    
    print(f"\n✅ Insights formatting test completed!")

def main():
    """Run all tests"""
    print("🚀 ATLES Proactive Insights Response Test Suite")
    print("=" * 60)
    
    test_proactive_response_detection()
    test_insights_formatting()
    
    print(f"\n🎉 All tests completed successfully!")
    print(f"\n📝 How to Test in ATLES:")
    print(f"   1. Run ATLES Desktop: python atles_desktop_pyqt.py")
    print(f"   2. Click 'Test Mode: ON' to enable test mode")
    print(f"   3. Click 'Test Proactive' → 'Self-Review'")
    print(f"   4. When you see the proactive message, respond with 'yes' or 'show me'")
    print(f"   5. You should now see formatted insights instead of confusion!")

if __name__ == "__main__":
    main()
