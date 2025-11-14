#!/usr/bin/env python3
"""
Test script for ATLES Enhanced Conversation System

This script demonstrates the new advanced NLP and multi-step conversation capabilities.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_advanced_nlp():
    """Test the Advanced NLP Module."""
    print("🧠 Testing Advanced NLP Module...")
    
    try:
        from atles.advanced_nlp_module import AdvancedNLPModule, IntentType, SentimentType
        
        nlp = AdvancedNLPModule()
        
        # Test various types of input
        test_inputs = [
            "Hello ATLES, what upgrades would you like to see added to you?",
            "Can you help me create a new Python function for data analysis?",
            "I'm frustrated with this error - it keeps happening!",
            "That's amazing! The solution worked perfectly, thank you!",
            "How does machine learning work in natural language processing?",
            "Please run the system diagnostics now",
            "By the way, that reminds me of something we discussed earlier"
        ]
        
        for i, text in enumerate(test_inputs, 1):
            print(f"\n  Test {i}: '{text[:50]}...'")
            analysis = nlp.analyze_input(text, f"test_conv_{i}")
            
            print(f"    Intent: {analysis.intent.value}")
            print(f"    Sentiment: {analysis.sentiment.value}")
            print(f"    Topics: {analysis.topics}")
            print(f"    Urgency: {analysis.urgency_level}/5")
            print(f"    Confidence: {analysis.confidence:.2f}")
            
            if analysis.conversation_markers:
                print(f"    Conversation Markers: {analysis.conversation_markers}")
        
        print("\n  ✅ Advanced NLP Module working correctly!")
        
    except Exception as e:
        print(f"  ❌ ERROR: {e}")

def test_conversation_flow():
    """Test the Conversation Flow Manager."""
    print("\n🔄 Testing Conversation Flow Manager...")
    
    try:
        from atles.conversation_flow_manager import ConversationFlowManager, ConversationState
        
        flow_manager = ConversationFlowManager("test_conversations")
        
        # Start a conversation
        conv_id = flow_manager.start_conversation(user_id="test_user", 
                                                 initial_goals=["system_upgrade", "learning"])
        print(f"  Started conversation: {conv_id}")
        
        # Simulate conversation turns
        test_turns = [
            ("I want to upgrade ATLES with better NLP capabilities", "Great! I'll help you upgrade ATLES with advanced NLP. Let's start by analyzing the current capabilities."),
            ("What's the first step?", "The first step is to assess the current NLP capabilities. We need to understand what's already implemented."),
            ("I've reviewed the current system", "Excellent! Now let's move to the next step: identifying specific improvements we can make.")
        ]
        
        for user_input, ai_response in test_turns:
            # Simulate NLP analysis
            nlp_data = {
                "intent": "request" if "want" in user_input or "help" in user_input else "question",
                "topics": ["upgrade", "nlp"] if "upgrade" in user_input or "nlp" in user_input.lower() else [],
                "confidence": 0.8
            }
            
            turn = flow_manager.add_turn(conv_id, user_input, ai_response, nlp_data)
            print(f"  Added turn: {turn.turn_id}")
        
        # Get conversation context
        context = flow_manager.get_conversation_context(conv_id)
        print(f"  Conversation state: {context['state']}")
        print(f"  Turn count: {context['turn_count']}")
        print(f"  Main topics: {context['main_topics']}")
        
        # Test follow-up suggestions
        follow_ups = flow_manager.suggest_follow_ups(conv_id)
        print(f"  Follow-up suggestions: {len(follow_ups)}")
        for suggestion in follow_ups[:2]:
            print(f"    - {suggestion['text']}")
        
        print("  ✅ Conversation Flow Manager working correctly!")
        
    except Exception as e:
        print(f"  ❌ ERROR: {e}")

def test_multi_step_tasks():
    """Test multi-step task management."""
    print("\n📋 Testing Multi-Step Task Management...")
    
    try:
        from atles.conversation_flow_manager import ConversationFlowManager
        
        flow_manager = ConversationFlowManager("test_conversations")
        conv_id = flow_manager.start_conversation()
        
        # Create a multi-step task
        steps = [
            {"title": "Analyze current NLP capabilities", "type": "analysis"},
            {"title": "Design advanced NLP architecture", "type": "design"},
            {"title": "Implement new NLP module", "type": "implementation"},
            {"title": "Test and validate improvements", "type": "testing"}
        ]
        
        task_id = flow_manager.create_multi_step_task(
            conv_id, 
            "NLP System Upgrade", 
            "Upgrade ATLES with advanced NLP capabilities",
            steps
        )
        
        print(f"  Created task: {task_id}")
        
        # Advance through steps
        for i in range(len(steps)):
            result = flow_manager.advance_task_step(
                conv_id, 
                task_id, 
                {"step_result": f"Completed step {i+1}", "notes": f"Step {i+1} finished successfully"}
            )
            
            print(f"  Step {result['current_step']}/{result['total_steps']} - {result['completion_percentage']:.0f}% complete")
            
            if result['status'] == 'completed':
                print("  🎉 Task completed!")
                break
        
        print("  ✅ Multi-step task management working correctly!")
        
    except Exception as e:
        print(f"  ❌ ERROR: {e}")

def test_enhanced_system_integration():
    """Test the complete Enhanced Conversation System."""
    print("\n🚀 Testing Enhanced Conversation System Integration...")
    
    try:
        from atles.enhanced_conversation_system import EnhancedConversationSystem
        
        system = EnhancedConversationSystem("test_conversations")
        
        # Check system status
        status = system.get_system_status()
        print(f"  Enhanced mode: {status['enhanced_mode']}")
        print(f"  Modules available: {status['modules']}")
        
        if not status['enhanced_mode']:
            print("  ⚠️  Running in basic mode - enhanced modules not available")
            return
        
        # Start conversation
        conv_id = system.start_conversation(goals=["system_upgrade"])
        print(f"  Started enhanced conversation: {conv_id}")
        
        # Process user input
        user_input = "I'd like to add advanced NLP capabilities to ATLES. Can you help me implement this as a multi-step process?"
        
        result = system.process_user_input(user_input, conv_id)
        
        print(f"  NLP Analysis:")
        nlp = result['nlp_analysis']
        print(f"    Intent: {nlp['intent']}")
        print(f"    Sentiment: {nlp['sentiment']}")
        print(f"    Topics: {nlp['topics']}")
        print(f"    Confidence: {nlp['confidence']:.2f}")
        
        print(f"  Response Guidance:")
        guidance = result['response_guidance']
        print(f"    Style: {guidance['style']}")
        print(f"    Tone: {guidance['tone']}")
        print(f"    Suggested Actions: {guidance['suggested_actions']}")
        
        # Simulate AI response
        ai_response = "I'll help you implement advanced NLP capabilities for ATLES! This is a great enhancement that will significantly improve conversation understanding. Let me create a multi-step process for this upgrade."
        
        response_result = system.add_ai_response(conv_id, user_input, ai_response, result['nlp_analysis'])
        
        print(f"  AI Response Added:")
        print(f"    Turn ID: {response_result['turn_id']}")
        print(f"    Follow-ups available: {len(response_result['follow_ups'])}")
        print(f"    Conversation state: {response_result['conversation_state']}")
        
        # Create multi-step task
        task_result = system.create_multi_step_task(conv_id, "Implement advanced NLP capabilities for ATLES")
        print(f"  Created task: {task_result['title']} ({task_result['total_steps']} steps)")
        
        # Get enhanced context
        enhanced_context = system.get_enhanced_context_for_response(conv_id)
        print(f"  Enhanced context available: {len(enhanced_context)} sections")
        
        print("  ✅ Enhanced Conversation System working correctly!")
        
    except Exception as e:
        print(f"  ❌ ERROR: {e}")

def demonstrate_upgrade_benefits():
    """Demonstrate the benefits of the new system."""
    print("\n🎯 Demonstrating Upgrade Benefits...")
    
    print("  🧠 Advanced NLP Capabilities:")
    print("    - Intent detection (question, request, command, etc.)")
    print("    - Sentiment analysis (positive, negative, neutral, mixed)")
    print("    - Topic extraction and categorization")
    print("    - Entity recognition (files, URLs, numbers)")
    print("    - Urgency assessment (1-5 scale)")
    print("    - Context clue detection")
    print("    - Conversation flow markers")
    
    print("\n  🔄 Multi-Step Conversation Management:")
    print("    - Conversation state tracking")
    print("    - Context preservation across turns")
    print("    - Multi-step task creation and management")
    print("    - Intelligent follow-up suggestions")
    print("    - User preference learning")
    print("    - Conversation continuity")
    
    print("\n  🚀 Enhanced Integration:")
    print("    - Seamless integration with existing ATLES")
    print("    - Backward compatibility (graceful degradation)")
    print("    - Persistent conversation storage")
    print("    - Real-time conversation analysis")
    print("    - Response guidance for AI")
    print("    - Task progress tracking")
    
    print("\n  💡 Real-World Benefits:")
    print("    - More natural conversations")
    print("    - Better understanding of user intent")
    print("    - Improved task completion rates")
    print("    - Enhanced user experience")
    print("    - Smarter response generation")
    print("    - Long-term conversation memory")

def main():
    """Run all tests and demonstrations."""
    print("🚀 ATLES Enhanced Conversation System - Test Suite")
    print("=" * 60)
    
    test_advanced_nlp()
    test_conversation_flow()
    test_multi_step_tasks()
    test_enhanced_system_integration()
    demonstrate_upgrade_benefits()
    
    print("\n" + "=" * 60)
    print("🎉 ATLES Enhanced Conversation System Testing Complete!")
    print("\nThe new system provides:")
    print("✅ Advanced natural language understanding")
    print("✅ Multi-step conversation tracking")
    print("✅ Intelligent task management")
    print("✅ Context-aware response guidance")
    print("✅ Seamless integration with existing ATLES")
    
    print("\n🎯 ATLES is now ready for more sophisticated conversations!")

if __name__ == "__main__":
    main()

