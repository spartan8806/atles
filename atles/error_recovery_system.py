"""
ATLES Error Recovery System - Fix for Critical Reasoning Failure

This module implements enhanced error recovery specifically for handling
corrections and meta-level reasoning failures.
"""

import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class CorrectionContext:
    """Context for handling user corrections."""
    original_response: str
    correction_text: str
    correction_type: str  # 'hallucination', 'factual_error', 'reasoning_error'
    user_feedback: str
    timestamp: datetime
    session_id: str

@dataclass
class RecoveryAction:
    """Action to take for error recovery."""
    action_type: str  # 'acknowledge', 'learn', 'adjust_behavior'
    description: str
    priority: int
    success_criteria: List[str]

class ErrorRecoverySystem:
    """
    Enhanced error recovery system to handle corrections and meta-failures.
    
    This system specifically addresses the bug where ATLES fails to process
    corrections properly and gets stuck in low-level analysis loops.
    """
    
    def __init__(self, atles_brain=None):
        self.atles_brain = atles_brain
        self.correction_history = []
        self.recovery_patterns = {}
        self.meta_failure_count = 0
        
        # Initialize correction detection patterns
        self.correction_indicators = [
            "that's not correct", "you're wrong", "that's a hallucination",
            "you made an error", "let me correct you", "actually",
            "the correct answer is", "you misunderstood", "correction:"
        ]
        
        # Initialize meta-failure patterns
        self.meta_failure_indicators = [
            "you're not understanding", "you're missing the point",
            "you're stuck in a loop", "you're not processing this correctly",
            "stop analyzing and just", "you failed to learn"
        ]
        
    def detect_correction_context(self, user_message: str, previous_response: str) -> Optional[CorrectionContext]:
        """
        Detect when a user is providing a correction and extract context.
        
        This is the first line of defense against the reported bug.
        """
        user_lower = user_message.lower()
        
        # Check for correction indicators
        is_correction = any(indicator in user_lower for indicator in self.correction_indicators)
        
        if not is_correction:
            return None
        
        # Determine correction type
        correction_type = "general"
        if any(word in user_lower for word in ["hallucination", "made up", "fabricated"]):
            correction_type = "hallucination"
        elif any(word in user_lower for word in ["wrong", "incorrect", "error"]):
            correction_type = "factual_error"
        elif any(word in user_lower for word in ["reasoning", "logic", "thinking"]):
            correction_type = "reasoning_error"
        
        return CorrectionContext(
            original_response=previous_response,
            correction_text=user_message,
            correction_type=correction_type,
            user_feedback=user_message,
            timestamp=datetime.now(),
            session_id=getattr(self.atles_brain, 'current_session_id', 'unknown')
        )
    
    def detect_meta_failure(self, user_message: str, response_history: List[str]) -> bool:
        """
        Detect when ATLES is experiencing a meta-level reasoning failure.
        
        This addresses the specific bug where ATLES gets stuck in analysis loops.
        """
        user_lower = user_message.lower()
        
        # Check for meta-failure indicators
        has_meta_indicators = any(indicator in user_lower for indicator in self.meta_failure_indicators)
        
        # Check for repetitive response patterns (stuck in loop)
        if len(response_history) >= 2:
            last_response = response_history[-1].lower()
            second_last = response_history[-2].lower()
            
            # Check if responses are too similar (indicating a loop)
            similarity = self._calculate_similarity(last_response, second_last)
            if similarity > 0.8:  # High similarity indicates stuck behavior
                return True
        
        # Check for response guidance repetition (the specific bug pattern)
        if len(response_history) >= 1:
            last_response = response_history[-1]
            if "RESPONSE GUIDANCE" in last_response and "Since the user's message is asking for information" in last_response:
                return True
        
        return has_meta_indicators
    
    def generate_recovery_actions(self, correction_context: CorrectionContext, is_meta_failure: bool = False) -> List[RecoveryAction]:
        """
        Generate specific recovery actions based on the correction context.
        
        This provides the roadmap for proper error recovery.
        """
        actions = []
        
        if is_meta_failure:
            # Priority 1: Break out of the analysis loop
            actions.append(RecoveryAction(
                action_type="break_loop",
                description="Stop current analysis pattern and reset reasoning mode",
                priority=1,
                success_criteria=["No repetitive response patterns", "Clear acknowledgment of issue"]
            ))
            
            # Priority 2: Acknowledge the meta-failure
            actions.append(RecoveryAction(
                action_type="acknowledge_meta_failure",
                description="Explicitly acknowledge the reasoning failure and reset",
                priority=2,
                success_criteria=["Direct acknowledgment", "No defensive responses"]
            ))
        
        # Standard correction handling
        if correction_context.correction_type == "hallucination":
            actions.append(RecoveryAction(
                action_type="acknowledge_hallucination",
                description="Acknowledge the hallucination and commit to factual accuracy",
                priority=1,
                success_criteria=["Clear acknowledgment", "Commitment to accuracy"]
            ))
            
            actions.append(RecoveryAction(
                action_type="learn_factual_grounding",
                description="Learn to ground responses in actual memory/facts",
                priority=2,
                success_criteria=["Demonstrate factual grounding", "Reference actual events"]
            ))
        
        # Always include learning action
        actions.append(RecoveryAction(
            action_type="learn_from_correction",
            description="Integrate the correction into future behavior",
            priority=3,
            success_criteria=["Show understanding", "Commit to improvement"]
        ))
        
        return sorted(actions, key=lambda x: x.priority)
    
    def execute_recovery_response(self, correction_context: CorrectionContext, recovery_actions: List[RecoveryAction], is_meta_failure: bool = False) -> str:
        """
        Generate an appropriate recovery response that addresses the correction properly.
        
        This is the core fix for the reported bug.
        """
        if is_meta_failure:
            # Special handling for meta-failures - break the loop immediately
            response = self._generate_meta_failure_response(correction_context)
        else:
            # Standard correction response
            response = self._generate_correction_response(correction_context, recovery_actions)
        
        # Log the recovery attempt
        self._log_recovery_attempt(correction_context, recovery_actions, response)
        
        return response
    
    def _generate_meta_failure_response(self, correction_context: CorrectionContext) -> str:
        """Generate a response specifically for meta-level reasoning failures."""
        return f"""I understand. I was caught in a reasoning loop and failed to process your correction properly. 

You're absolutely right - I need to stop the surface-level analysis and actually engage with what you're teaching me. 

{self._extract_key_lesson(correction_context.correction_text)}

I will apply this lesson going forward and avoid getting stuck in analysis patterns when you're providing important corrections. Thank you for the feedback."""
    
    def _generate_correction_response(self, correction_context: CorrectionContext, recovery_actions: List[RecoveryAction]) -> str:
        """Generate a standard correction response."""
        if correction_context.correction_type == "hallucination":
            return f"""You're absolutely correct, and I apologize for the hallucination. I should not have fabricated details that weren't in my actual memory.

{self._extract_key_lesson(correction_context.correction_text)}

I understand the importance of grounding my responses in factual memory rather than creating plausible-sounding but incorrect information. I will be more careful to distinguish between what I actually know and what I might be inferring or creating."""
        
        else:
            return f"""Thank you for the correction. I understand that I made an error in my previous response.

{self._extract_key_lesson(correction_context.correction_text)}

I will incorporate this feedback and be more accurate in similar situations going forward."""
    
    def _extract_key_lesson(self, correction_text: str) -> str:
        """Extract the key lesson from the correction text."""
        # Simple extraction - in a full implementation, this would be more sophisticated
        if "grounding" in correction_text.lower() or "factual" in correction_text.lower():
            return "The key lesson: I must ground all reasoning in actual factual memory, not fabricated details."
        elif "monologue" in correction_text.lower():
            return "The key lesson: Reflective monologues must be based on specific, factual events from my memory."
        else:
            return "The key lesson: I need to be more accurate and careful in my responses."
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts (simple implementation)."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _log_recovery_attempt(self, correction_context: CorrectionContext, recovery_actions: List[RecoveryAction], response: str):
        """Log the recovery attempt for analysis and improvement."""
        self.correction_history.append({
            "timestamp": datetime.now().isoformat(),
            "correction_context": correction_context,
            "recovery_actions": [action.action_type for action in recovery_actions],
            "response_generated": response[:100] + "..." if len(response) > 100 else response
        })
        
        logger.info(f"Error recovery executed: {correction_context.correction_type} correction processed")
    
    def get_recovery_statistics(self) -> Dict[str, Any]:
        """Get statistics on error recovery performance."""
        if not self.correction_history:
            return {"total_corrections": 0, "correction_types": {}, "success_rate": 0.0}
        
        correction_types = {}
        for entry in self.correction_history:
            correction_type = entry["correction_context"].correction_type
            correction_types[correction_type] = correction_types.get(correction_type, 0) + 1
        
        return {
            "total_corrections": len(self.correction_history),
            "correction_types": correction_types,
            "recent_corrections": self.correction_history[-5:] if len(self.correction_history) >= 5 else self.correction_history,
            "meta_failure_count": self.meta_failure_count
        }

# Integration function for ATLES Brain
def integrate_error_recovery(atles_brain):
    """Integrate the error recovery system with ATLES Brain."""
    if not hasattr(atles_brain, 'error_recovery'):
        atles_brain.error_recovery = ErrorRecoverySystem(atles_brain)
        logger.info("Error Recovery System integrated with ATLES Brain")
    return atles_brain.error_recovery
