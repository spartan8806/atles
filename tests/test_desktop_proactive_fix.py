#!/usr/bin/env python3
"""
Test the desktop app proactive messaging fix.
"""

import sys
import os

# Add the atles directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'atles'))

def test_integrated_proactive_messaging():
    """Test that the integrated proactive messaging works."""
    
    print("🧪 Testing Integrated Proactive Messaging")
    print("=" * 50)
    
    try:
        from atles.integrated_proactive_messaging import IntegratedProactiveMessaging
        
        # Initialize the integrated system
        integrated_pm = IntegratedProactiveMessaging()
        
        print("✅ IntegratedProactiveMessaging initialized")
        
        # Generate self-review insights
        insights = integrated_pm.generate_self_review_insights()
        
        print("✅ Self-review insights generated")
        print(f"   Keys: {list(insights.keys())}")
        
        # Check conversation stats
        conv_stats = insights.get('conversation_stats', {})
        print(f"   Total messages: {conv_stats.get('total_messages', 0)}")
        print(f"   User messages: {conv_stats.get('user_messages', 0)}")
        print(f"   ATLES messages: {conv_stats.get('atles_messages', 0)}")
        
        # Check learning summary
        learning = insights.get('learning_summary', {})
        print(f"   Learned principles: {learning.get('total_principles', 0)}")
        
        return conv_stats.get('total_messages', 0) > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_desktop_conversion():
    """Test the desktop app conversion method."""
    
    print(f"\n🧪 Testing Desktop App Conversion")
    print("-" * 40)
    
    try:
        # Mock the desktop app conversion method
        def _convert_integrated_analysis(integrated_result):
            """Convert integrated proactive messaging analysis to desktop app format."""
            try:
                insights = integrated_result.get('insights', {})
                conversation_stats = integrated_result.get('conversation_stats', {})
                learning_summary = integrated_result.get('learning_summary', {})
                
                # Convert to desktop app format
                formatted = {
                    'summary': f"Memory-aware analysis completed with {learning_summary.get('total_principles', 0)} learned principles",
                    'patterns': [
                        f"Total interactions: {conversation_stats.get('user_messages', 0)} user messages, {conversation_stats.get('atles_messages', 0)} assistant responses",
                        f"System messages: 0",
                        f"Conversation length: {conversation_stats.get('total_messages', 0)} total lines"
                    ],
                    'insights': [
                        f"Learning Status: {insights.get('learning_status', 'Unknown')}",
                        f"Primary Focus: {insights.get('conversation_themes', {}).get('primary_focus', 'Unknown')}",
                        f"Interaction Style: {insights.get('interaction_patterns', {}).get('interaction_style', 'Unknown')}",
                        f"Engagement Level: {insights.get('user_engagement_level', 'Unknown')}"
                    ],
                    'recommendations': insights.get('proactive_suggestions', [])
                }
                
                return formatted
                
            except Exception as e:
                print(f"Error converting integrated analysis: {e}")
                return {
                    'summary': 'Memory-aware analysis completed',
                    'patterns': ['Analysis conversion failed'],
                    'insights': [],
                    'recommendations': []
                }
        
        # Get integrated analysis
        from atles.integrated_proactive_messaging import IntegratedProactiveMessaging
        integrated_pm = IntegratedProactiveMessaging()
        integrated_result = integrated_pm.generate_self_review_insights()
        
        # Convert to desktop format
        desktop_format = _convert_integrated_analysis(integrated_result)
        
        print("✅ Conversion successful")
        print(f"   Summary: {desktop_format['summary']}")
        print(f"   Patterns: {desktop_format['patterns']}")
        print(f"   Insights: {len(desktop_format['insights'])} items")
        print(f"   Recommendations: {len(desktop_format['recommendations'])} items")
        
        # Check if we have real data (not zeros)
        patterns_text = ' '.join(desktop_format['patterns'])
        has_real_data = "0 user messages, 0 assistant responses" not in patterns_text
        
        if has_real_data:
            print("✅ SUCCESS: Real conversation data detected!")
            return True
        else:
            print("❌ Still showing zero interactions")
            return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    
    print("🚀 Desktop App Proactive Messaging Fix Test")
    print("Testing integration with memory-aware reasoning")
    print("=" * 60)
    
    test1_success = test_integrated_proactive_messaging()
    test2_success = test_desktop_conversion()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("-" * 20)
    print(f"Integrated proactive messaging: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"Desktop app conversion: {'✅ PASS' if test2_success else '❌ FAIL'}")
    
    if test1_success and test2_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("The desktop app should now show correct conversation statistics.")
        print("Proactive messaging will use memory-aware reasoning.")
    else:
        print("\n⚠️ SOME TESTS FAILED")
        print("The proactive messaging integration needs further debugging.")
    
    return test1_success and test2_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
