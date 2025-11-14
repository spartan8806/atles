"""
ATLES Learning Response Generator

This module integrates the memory-aware reasoning system with response generation,
ensuring that every response is informed by learned principles and conversation memory.

This is the bridge that transforms ATLES from a static AI into a true learning AI.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from .memory_aware_reasoning import MemoryAwareReasoning, LearnedPrinciple

logger = logging.getLogger(__name__)


class LearningResponseGenerator:
    """
    Response generator that consults memory and applies learned principles.
    
    This implements the new processing pipeline:
    1. User prompt comes in
    2. System retrieves conversation history and learned principles
    3. Pre-processing synthesizes context-specific rules
    4. Enhanced context + original prompt sent to language model
    5. Response generated with memory awareness
    """
    
    def __init__(self, memory_path: str = "atles_memory"):
        self.memory_reasoning = MemoryAwareReasoning(memory_path)
        self.response_history = []
        
        logger.info("Learning Response Generator initialized")
    
    def generate_memory_informed_response(self, user_prompt: str, 
                                        conversation_context: Optional[Dict] = None,
                                        base_system_prompt: str = "") -> Dict[str, Any]:
        """
        Generate a response that is fully informed by conversation memory and learned principles.
        
        This is the main method that implements the memory-aware response generation.
        
        Args:
            user_prompt: The user's input
            conversation_context: Additional context
            base_system_prompt: Base system prompt from the model
            
        Returns:
            Dict containing the enhanced response context and guidance
        """
        logger.info("Generating memory-informed response")
        
        # Step 1: Process the prompt with full memory awareness
        enhanced_context = self.memory_reasoning.process_user_prompt(
            user_prompt, conversation_context
        )
        
        # Step 2: Create the memory-informed system prompt
        memory_informed_prompt = self._create_comprehensive_system_prompt(
            base_system_prompt, enhanced_context
        )
        
        # Step 3: Generate response guidance based on active principles
        response_guidance = self._generate_response_guidance(enhanced_context)
        
        # Step 4: Create the final response context
        response_context = {
            "enhanced_system_prompt": memory_informed_prompt,
            "response_guidance": response_guidance,
            "active_principles": enhanced_context.get("active_principles", []),
            "contextual_rules": enhanced_context.get("contextual_rules", []),
            "memory_informed": True,
            "original_prompt": user_prompt,
            "processing_timestamp": datetime.now().isoformat()
        }
        
        # Step 5: Log the memory-aware processing
        self._log_memory_usage(enhanced_context)
        
        return response_context
    
    def _create_comprehensive_system_prompt(self, base_prompt: str, enhanced_context: Dict[str, Any]) -> str:
        """
        Create a comprehensive system prompt that includes learned principles.
        
        This ensures that the language model receives both its base instructions
        and the dynamically learned principles from conversation memory.
        """
        prompt_parts = []
        
        # Start with base system prompt
        if base_prompt:
            prompt_parts.append(base_prompt)
            prompt_parts.append("")
        
        # Add memory-aware section
        if enhanced_context.get("memory_informed"):
            prompt_parts.append("=" * 60)
            prompt_parts.append("🧠 MEMORY-INFORMED RESPONSE GENERATION")
            prompt_parts.append("=" * 60)
            prompt_parts.append("")
            
            # Add learned principles
            if enhanced_context.get("active_principles"):
                prompt_parts.append("📚 ACTIVE LEARNED PRINCIPLES:")
                prompt_parts.append("You have learned the following principles from previous conversations.")
                prompt_parts.append("Apply these principles when generating your response:")
                prompt_parts.append("")
                
                for rule_info in enhanced_context.get("contextual_rules", []):
                    principle_name = rule_info.get("principle", "Unknown")
                    rule_text = rule_info.get("rule", "")
                    relevance = rule_info.get("relevance", 0)
                    
                    prompt_parts.append(f"• {principle_name}: {rule_text}")
                    prompt_parts.append(f"  (Relevance: {relevance:.2f})")
                    prompt_parts.append("")
            
            # Add response guidelines
            if enhanced_context.get("response_guidelines"):
                prompt_parts.append("🎯 RESPONSE GUIDELINES:")
                prompt_parts.append("Based on your learned principles, follow these guidelines:")
                prompt_parts.append("")
                
                for guideline in enhanced_context.get("response_guidelines", []):
                    prompt_parts.append(f"• {guideline}")
                
                prompt_parts.append("")
            
            # Add memory-aware instructions
            prompt_parts.extend([
                "🔄 MEMORY-AWARE INSTRUCTIONS:",
                "• Your response should reflect the principles you've learned, not just base training",
                "• Apply the active principles to the current context appropriately", 
                "• This is how you grow and adapt as a learning AI",
                "• If principles conflict, prioritize the most recent and relevant ones",
                "",
                "=" * 60,
                ""
            ])
        
        return "\n".join(prompt_parts)
    
    def _generate_response_guidance(self, enhanced_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate specific guidance for response generation based on active principles.
        
        This provides structured guidance that can be used by different response
        generation systems (Ollama, OpenAI, etc.)
        """
        guidance = {
            "should_apply_principles": len(enhanced_context.get("active_principles", [])) > 0,
            "principle_count": len(enhanced_context.get("active_principles", [])),
            "high_relevance_rules": [],
            "response_style_guidance": [],
            "content_guidance": [],
            "avoid_patterns": []
        }
        
        # Analyze contextual rules for specific guidance
        for rule_info in enhanced_context.get("contextual_rules", []):
            rule_text = rule_info.get("rule", "").lower()
            relevance = rule_info.get("relevance", 0)
            
            if relevance > 0.7:  # High relevance
                guidance["high_relevance_rules"].append(rule_info)
            
            # Extract specific guidance patterns
            if "hypothetical" in rule_text:
                guidance["response_style_guidance"].extend([
                    "Acknowledge hypothetical nature of questions",
                    "Engage creatively rather than defaulting to task assistance",
                    "Answer from AI perspective about intellectual interests"
                ])
                guidance["avoid_patterns"].extend([
                    "Redirecting to task management",
                    "Generic helper responses",
                    "Productivity-focused suggestions"
                ])
            
            if "acknowledge" in rule_text:
                guidance["content_guidance"].append("Start response with acknowledgment")
            
            if "engage creatively" in rule_text:
                guidance["content_guidance"].append("Show creativity and personality in response")
        
        # Remove duplicates
        for key in ["response_style_guidance", "content_guidance", "avoid_patterns"]:
            guidance[key] = list(set(guidance[key]))
        
        return guidance
    
    def _log_memory_usage(self, enhanced_context: Dict[str, Any]) -> None:
        """Log how memory was used in response generation."""
        active_principles = enhanced_context.get("active_principles", [])
        contextual_rules = enhanced_context.get("contextual_rules", [])
        
        if active_principles:
            logger.info(f"Applied {len(active_principles)} learned principles: {', '.join(active_principles)}")
        
        if contextual_rules:
            high_relevance = [r for r in contextual_rules if r.get("relevance", 0) > 0.7]
            if high_relevance:
                logger.info(f"High relevance rules applied: {len(high_relevance)}")
    
    def learn_from_feedback(self, user_prompt: str, response: str, 
                          feedback: str, feedback_type: str = "correction") -> bool:
        """
        Learn from user feedback to improve future responses.
        
        This allows ATLES to learn new principles or refine existing ones
        based on user corrections or feedback.
        """
        try:
            if feedback_type == "correction" and "should" in feedback.lower():
                # Extract new principle from correction
                principle = self._extract_principle_from_feedback(feedback, user_prompt, response)
                if principle:
                    success = self.memory_reasoning.learn_new_principle(principle)
                    if success:
                        logger.info(f"Learned new principle from feedback: {principle.name}")
                        return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error learning from feedback: {e}")
            return False
    
    def _extract_principle_from_feedback(self, feedback: str, original_prompt: str, 
                                       response: str) -> Optional[LearnedPrinciple]:
        """Extract a new principle from user feedback."""
        try:
            # Look for correction patterns
            if "should have" in feedback.lower() or "instead" in feedback.lower():
                principle_name = f"Feedback Principle {datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                return LearnedPrinciple(
                    name=principle_name,
                    description=f"Learned from feedback: {feedback}",
                    rules=[feedback],
                    examples=[f"Prompt: {original_prompt}\nFeedback: {feedback}"],
                    confidence=0.7,  # Medium confidence for feedback-based learning
                    learned_at=datetime.now()
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting principle from feedback: {e}")
            return None
    
    def get_memory_status(self) -> Dict[str, Any]:
        """Get status of the memory-aware reasoning system."""
        learning_summary = self.memory_reasoning.get_learning_summary()
        
        return {
            "memory_aware_reasoning": "active",
            "learning_summary": learning_summary,
            "response_generation": "memory_informed",
            "last_processing": getattr(self, '_last_processing_time', None)
        }
    
    def demonstrate_learning_capability(self, test_prompt: str) -> Dict[str, Any]:
        """
        Demonstrate how the learning system would process a specific prompt.
        
        This is useful for testing and validation.
        """
        logger.info(f"Demonstrating learning capability for: {test_prompt}")
        
        # Process the prompt
        enhanced_context = self.memory_reasoning.process_user_prompt(test_prompt)
        response_context = self.generate_memory_informed_response(test_prompt)
        
        return {
            "test_prompt": test_prompt,
            "memory_informed": enhanced_context.get("memory_informed", False),
            "active_principles": enhanced_context.get("active_principles", []),
            "contextual_rules": enhanced_context.get("contextual_rules", []),
            "response_guidance": response_context.get("response_guidance", {}),
            "enhanced_system_prompt": response_context.get("enhanced_system_prompt", ""),
            "demonstration_timestamp": datetime.now().isoformat()
        }
