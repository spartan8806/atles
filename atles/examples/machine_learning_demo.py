#!/usr/bin/env python3
"""
ATLES Machine Learning Demo - Phase 2

Demonstrates the three key machine learning capabilities:
1. Conversation Pattern Learning
2. Response Quality Improvement  
3. Adaptive Response Generation
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import ATLES components
from atles.brain import ATLESBrain
from atles.machine_learning import ATLESMachineLearning, AdaptiveContext


async def demo_conversation_pattern_learning():
    """Demonstrate conversation pattern learning capabilities."""
    print("\n" + "="*60)
    print("DEMO 1: Conversation Pattern Learning")
    print("="*60)
    
    # Initialize machine learning system
    ml_system = ATLESMachineLearning()
    
    # Simulate different types of interactions
    interactions = [
        {
            "user_message": "How do I implement a binary search algorithm?",
            "ai_response": "Binary search is an efficient algorithm for finding elements in sorted arrays. Here's how to implement it in Python...",
            "context": {"user_preference": "technical", "topic": "programming", "complexity": "intermediate"},
            "feedback": 0.9
        },
        {
            "user_message": "What's the difference between REST and GraphQL?",
            "ai_response": "REST and GraphQL are both API design approaches. REST uses multiple endpoints while GraphQL uses a single endpoint...",
            "context": {"user_preference": "technical", "topic": "web_development", "complexity": "intermediate"},
            "feedback": 0.8
        },
        {
            "user_message": "Can you help me debug this Python error?",
            "ai_response": "I'd be happy to help debug your Python error. Please share the error message and the relevant code...",
            "context": {"user_preference": "helpful", "topic": "programming", "complexity": "beginner"},
            "feedback": 0.7
        }
    ]
    
    print("Learning from interactions...")
    for i, interaction in enumerate(interactions, 1):
        result = await ml_system.learn_from_interaction(
            interaction["user_message"],
            interaction["ai_response"],
            interaction["feedback"],
            interaction["context"],
            f"demo_session_{i}",
            True
        )
        print(f"  Interaction {i}: {result}")
    
    # Get pattern statistics
    pattern_stats = await ml_system.pattern_learner.get_pattern_statistics()
    print(f"\nPattern Learning Results:")
    print(f"  Total patterns learned: {pattern_stats['total_patterns']}")
    print(f"  Average success rate: {pattern_stats['average_success_rate']:.2f}")
    print(f"  Intent distribution: {pattern_stats['intent_distribution']}")
    
    # Show top patterns
    if pattern_stats['top_patterns']:
        print(f"\nTop performing patterns:")
        for pattern in pattern_stats['top_patterns'][:3]:
            print(f"  - {pattern['intent']}: {pattern['success_rate']:.2f} success rate, {pattern['usage_count']} uses")


async def demo_response_quality_improvement():
    """Demonstrate response quality improvement capabilities."""
    print("\n" + "="*60)
    print("DEMO 2: Response Quality Improvement")
    print("="*60)
    
    # Initialize machine learning system
    ml_system = ATLESMachineLearning()
    
    # Simulate quality metrics for different response types
    quality_scenarios = [
        {
            "session_id": "quality_demo_1",
            "user_message": "Explain machine learning in simple terms",
            "ai_response": "Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed.",
            "feedback": 0.9,
            "metadata": {"user_acknowledgment": True, "conversation_continued": True}
        },
        {
            "session_id": "quality_demo_2",
            "user_message": "What is the capital of France?",
            "ai_response": "Paris.",
            "feedback": 0.3,
            "metadata": {"user_acknowledgment": False, "conversation_continued": False}
        },
        {
            "session_id": "quality_demo_3",
            "user_message": "How do neural networks work?",
            "ai_response": "Neural networks are inspired by biological neurons. They consist of layers of interconnected nodes that process information and learn patterns through training data.",
            "feedback": 0.7,
            "metadata": {"user_acknowledgment": True, "conversation_continued": True}
        }
    ]
    
    print("Recording quality metrics...")
    for scenario in quality_scenarios:
        metric_id = await ml_system.quality_improver.record_quality_metric(
            scenario["session_id"],
            scenario["user_message"],
            scenario["ai_response"],
            scenario["feedback"],
            scenario["metadata"]
        )
        print(f"  Recorded metric: {metric_id}")
    
    # Get quality insights
    quality_insights = await ml_system.quality_improver.get_quality_insights()
    print(f"\nQuality Improvement Results:")
    print(f"  Total metrics recorded: {quality_insights['total_metrics']}")
    print(f"  Average quality score: {quality_insights['average_quality']:.2f}")
    print(f"  Quality distribution: {quality_insights['quality_distribution']}")
    
    # Show improvement suggestions
    if quality_insights['top_improvement_suggestions']:
        print(f"\nTop improvement suggestions:")
        for suggestion, count in quality_insights['top_improvement_suggestions'][:3]:
            print(f"  - {suggestion} (mentioned {count} times)")


async def demo_adaptive_response_generation():
    """Demonstrate adaptive response generation capabilities."""
    print("\n" + "="*60)
    print("DEMO 3: Adaptive Response Generation")
    print("="*60)
    
    # Initialize machine learning system
    ml_system = ATLESMachineLearning()
    
    # Create adaptive context
    adaptive_context = AdaptiveContext(
        user_id="demo_user",
        conversation_history=[
            {
                "role": "user",
                "content": "I'm working on a machine learning project",
                "metadata": {"user_topics": {"topics": ["machine_learning", "project"]}}
            },
            {
                "role": "assistant", 
                "content": "That sounds interesting! What kind of machine learning project are you working on?",
                "metadata": {"ai_topics": {"topics": ["machine_learning", "project"]}}
            },
            {
                "role": "user",
                "content": "I want to build a recommendation system",
                "metadata": {"user_topics": {"topics": ["recommendation_system", "machine_learning"]}}
            }
        ],
        learned_patterns=[],
        quality_history=[],
        user_preferences={
            "conversation_style": "casual",
            "detail_level": "high",
            "topics_of_interest": ["machine_learning", "programming", "data_science"]
        },
        context_embeddings={}
    )
    
    # Test different user messages
    test_messages = [
        "Can you help me choose the right algorithm?",
        "What are the best practices for data preprocessing?",
        "How do I evaluate my model's performance?"
    ]
    
    base_response = "I can help you with that. Let me provide some guidance based on your project needs."
    
    print("Generating adaptive responses...")
    for i, message in enumerate(test_messages, 1):
        adaptive_response = await ml_system.generate_adaptive_response(
            message,
            base_response,
            adaptive_context,
            "demo_model"
        )
        
        print(f"\n  Test {i}: {message}")
        print(f"    Base response: {base_response}")
        print(f"    Adaptive response: {adaptive_response['response']}")
        print(f"    Adaptation applied: {adaptive_response['adaptation_applied']}")
        print(f"    Adaptation strategy: {adaptive_response['adaptation_strategy']}")


async def demo_integrated_brain():
    """Demonstrate the integrated brain with all machine learning capabilities."""
    print("\n" + "="*60)
    print("DEMO 4: Integrated ATLES Brain with Machine Learning")
    print("="*60)
    
    # Initialize the full ATLES brain
    brain = ATLESBrain()
    
    # Start a conversation
    session_id = await brain.start_conversation("demo_user", "demo_model")
    print(f"Started conversation: {session_id}")
    
    # Simulate a chat interaction
    print("\nSimulating chat interaction...")
    chat_response = await brain.chat(
        "I need help understanding deep learning concepts",
        session_id
    )
    
    print(f"Chat response: {chat_response['response']}")
    print(f"Machine learning insights: {json.dumps(chat_response['machine_learning'], indent=2)}")
    
    # Record user feedback
    print("\nRecording user feedback...")
    feedback_result = await brain.record_user_feedback(session_id, 0.8)
    print(f"Feedback result: {feedback_result}")
    
    # Get learning insights
    print("\nGetting learning insights...")
    insights = await brain.get_learning_insights()
    print(f"Learning insights: {json.dumps(insights, indent=2)}")
    
    # Get conversation patterns
    print("\nGetting conversation patterns...")
    patterns = await brain.get_conversation_patterns("demo_user")
    print(f"User patterns: {json.dumps(patterns, indent=2)}")
    
    # End conversation
    await brain.end_conversation(session_id)
    print(f"\nEnded conversation: {session_id}")


async def demo_advanced_features():
    """Demonstrate advanced machine learning features."""
    print("\n" + "="*60)
    print("DEMO 5: Advanced Machine Learning Features")
    print("="*60)
    
    ml_system = ATLESMachineLearning()
    
    # Export learning data
    print("Exporting learning data...")
    export_path = Path.home() / ".atles" / "learning" / "demo_export.pkl"
    export_success = await ml_system.export_learning_data(export_path)
    print(f"  Export successful: {export_success}")
    print(f"  Export path: {export_path}")
    
    # Import learning data
    print("\nImporting learning data...")
    import_success = await ml_system.import_learning_data(export_path)
    print(f"  Import successful: {import_success}")
    
    # Test pattern finding with different contexts
    print("\nTesting pattern finding...")
    test_contexts = [
        {"user_preference": "technical", "topic": "programming"},
        {"user_preference": "casual", "topic": "general"},
        {"user_preference": "detailed", "topic": "machine_learning"}
    ]
    
    for context in test_contexts:
        patterns = await ml_system.pattern_learner.find_best_pattern(
            "information_request", context, limit=2
        )
        print(f"  Context {context}: Found {len(patterns)} patterns")


async def main():
    """Run all machine learning demonstrations."""
    print("ATLES Machine Learning System - Phase 2 Demo")
    print("="*60)
    
    try:
        # Run all demos
        await demo_conversation_pattern_learning()
        await demo_response_quality_improvement()
        await demo_adaptive_response_generation()
        await demo_integrated_brain()
        await demo_advanced_features()
        
        print("\n" + "="*60)
        print("All demonstrations completed successfully!")
        print("="*60)
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print(f"\nDemo failed with error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
