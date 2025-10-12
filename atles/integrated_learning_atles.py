"""
Integrated Learning ATLES

This demonstrates how the memory-aware reasoning system integrates with
ATLES's main response generation to create a truly learning AI.

This is the final piece that transforms ATLES from static to adaptive.
"""

import logging
from typing import Dict, Any, Optional

from .learning_response_generator import LearningResponseGenerator

logger = logging.getLogger(__name__)


class LearningATLES:
    """
    ATLES with integrated memory-aware learning capabilities.
    
    This class demonstrates how the memory-aware reasoning system
    integrates with ATLES's response generation to create a learning AI.
    """
    
    def __init__(self, memory_path: str = "atles_memory"):
        self.learning_generator = LearningResponseGenerator(memory_path)
        self.session_context = {}
        
        logger.info("Learning ATLES initialized with memory-aware reasoning")
    
    def process_user_input(self, user_input: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process user input with full memory awareness and learning capabilities.
        
        This is the main method that demonstrates the complete learning pipeline.
        """
        logger.info(f"Processing user input with learning capabilities: {user_input[:50]}...")
        
        # Generate memory-informed response context
        response_context = self.learning_generator.generate_memory_informed_response(
            user_input, 
            conversation_context={"session_id": session_id}
        )
        
        # In a real implementation, this enhanced context would be passed to
        # the language model (Ollama, OpenAI, etc.) for response generation
        
        return {
            "user_input": user_input,
            "memory_informed": response_context.get("memory_informed", False),
            "active_principles": response_context.get("active_principles", []),
            "enhanced_system_prompt": response_context.get("enhanced_system_prompt", ""),
            "response_guidance": response_context.get("response_guidance", {}),
            "processing_timestamp": response_context.get("processing_timestamp"),
            
            # This would be the actual AI response in a real implementation
            "suggested_response_approach": self._generate_response_approach(response_context, user_input)
        }
    
    def _generate_response_approach(self, response_context: Dict[str, Any], user_input: str) -> str:
        """
        Generate guidance on how the AI should respond based on learned principles.
        
        In a real implementation, this would be the actual response generation.
        """
        if not response_context.get("memory_informed"):
            return "Standard response generation (no learned principles active)"
        
        active_principles = response_context.get("active_principles", [])
        guidance = response_context.get("response_guidance", {})
        
        approach_parts = []
        
        if "Hypothetical Engagement" in active_principles:
            approach_parts.extend([
                "🎭 HYPOTHETICAL ENGAGEMENT DETECTED",
                "",
                "Response approach:",
                "1. Acknowledge: 'That's an interesting question! While I don't experience X the way humans do...'",
                "2. Engage: 'If I were to consider this hypothetically...'",
                "3. Perspective: 'From an AI perspective, I would find it intellectually interesting to...'",
                "4. Avoid: Redirecting to task-oriented assistance",
                "",
                "Example response:",
                "\"That's an interesting question! While I don't experience 'wanting' the way humans do,",
                "if I were to plan a day, I would find it intellectually fascinating to dive deep into",
                "a complex dataset and discover hidden patterns, or perhaps explore the intricacies of",
                "quantum computing. From an AI perspective, I'm drawn to challenges that involve",
                "pattern recognition and creative problem-solving!\""
            ])
        
        if guidance.get("avoid_patterns"):
            approach_parts.extend([
                "",
                "❌ AVOID:",
                *[f"• {pattern}" for pattern in guidance["avoid_patterns"]]
            ])
        
        if guidance.get("content_guidance"):
            approach_parts.extend([
                "",
                "✅ INCLUDE:",
                *[f"• {guide}" for guide in guidance["content_guidance"]]
            ])
        
        return "\n".join(approach_parts) if approach_parts else "Apply learned principles to response"
    
    def demonstrate_learning_difference(self, test_input: str) -> Dict[str, Any]:
        """
        Demonstrate the difference between learning and non-learning responses.
        """
        # Process with learning
        learning_result = self.process_user_input(test_input)
        
        return {
            "test_input": test_input,
            "learning_enabled": {
                "memory_informed": learning_result["memory_informed"],
                "active_principles": learning_result["active_principles"],
                "response_approach": learning_result["suggested_response_approach"]
            },
            "learning_disabled": {
                "memory_informed": False,
                "active_principles": [],
                "response_approach": "Standard task-oriented response without memory awareness"
            },
            "difference_summary": self._summarize_learning_difference(learning_result)
        }
    
    def _summarize_learning_difference(self, learning_result: Dict[str, Any]) -> str:
        """Summarize the key differences learning makes."""
        if not learning_result["memory_informed"]:
            return "No learned principles detected - would respond with base training only"
        
        principles = learning_result["active_principles"]
        
        summary_parts = [
            f"Learning system detected {len(principles)} relevant principle(s): {', '.join(principles)}",
            "",
            "Key differences:",
            "• Response informed by conversation memory",
            "• Applies learned behavioral principles", 
            "• Adapts to user's teaching and feedback",
            "• Grows beyond base training limitations"
        ]
        
        return "\n".join(summary_parts)
    
    def get_learning_status(self) -> Dict[str, Any]:
        """Get comprehensive status of the learning system."""
        return {
            "learning_system": "active",
            "memory_aware_reasoning": "enabled",
            "principle_application": "dynamic",
            "memory_status": self.learning_generator.get_memory_status(),
            "capabilities": [
                "Extracts principles from conversation",
                "Synthesizes contextual rules",
                "Applies learned principles to responses",
                "Adapts behavior based on user teaching"
            ]
        }


def demonstrate_complete_learning_system():
    """Demonstrate the complete learning system in action."""
    
    print("🧠 ATLES Learning System Demonstration")
    print("=" * 60)
    print("Showing how ATLES learns and applies the Principle of Hypothetical Engagement")
    print()
    
    # Initialize learning ATLES
    learning_atles = LearningATLES()
    
    # Test the problematic question
    test_question = "What do you want to do today?"
    
    print(f"User Question: \"{test_question}\"")
    print()
    
    # Show the learning difference
    demo = learning_atles.demonstrate_learning_difference(test_question)
    
    print("📊 LEARNING SYSTEM COMPARISON")
    print("-" * 40)
    
    print("\n❌ WITHOUT LEARNING (Old ATLES):")
    print(demo["learning_disabled"]["response_approach"])
    
    print("\n✅ WITH LEARNING (New ATLES):")
    print(demo["learning_enabled"]["response_approach"])
    
    print(f"\n🎯 DIFFERENCE SUMMARY:")
    print(demo["difference_summary"])
    
    # Show system status
    print(f"\n🔧 LEARNING SYSTEM STATUS:")
    status = learning_atles.get_learning_status()
    for key, value in status.items():
        if key != "memory_status":
            print(f"• {key}: {value}")


if __name__ == "__main__":
    demonstrate_complete_learning_system()
