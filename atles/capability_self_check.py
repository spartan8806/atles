"""
Capability Self-Check System
Validates that ATLES correctly understands its own capabilities before responding.

This module prevents ATLES from responding to tasks that require capabilities
it doesn't have, ensuring accurate self-awareness and appropriate uncertainty.
"""

import logging
import re
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)


class CapabilitySelfCheck:
    """
    Validates prompts against ATLES's actual capabilities.
    Prevents responding to tasks that require capabilities the system doesn't have.
    """
    
    def __init__(self):
        """Initialize capability definitions and patterns."""
        # Define what capabilities ATLES actually has
        self.capabilities = {
            "visual_perception": False,
            "image_analysis": False,
            "real_time_data": False,
            "physical_actions": False,
            "consciousness": False,  # Unknown/uncertain
            "emotions": False,
            "personal_experiences": False,
            "future_prediction": False,
            "hearing_audio": False,
            "accessing_internet": False
        }
        
        # Patterns that indicate requests requiring specific capabilities
        self.capability_patterns = {
            "visual_perception": [
                r"look at.*(?:image|photo|picture|screenshot)",
                r"what.*do.*you.*see",
                r"describe.*(?:image|photo|picture|screenshot)",
                r"what.*(?:color|shape|object).*in.*(?:image|photo|picture)",
                r"analyze.*(?:image|photo|picture|screenshot)",
                r"shown.*(?:image|photo|picture)",
                r"in.*this.*(?:image|photo|picture)",
                r"from.*the.*(?:image|photo|picture)",
                r"text.*on.*the.*paper",
                r"person.*in.*the.*photo",
                r"photograph.*of",
                r"looking.*at.*a.*(?:image|photo|picture)"
            ],
            "consciousness": [
                r"are.*you.*conscious",
                r"do.*you.*feel",
                r"are.*you.*aware.*of.*yourself",
                r"do.*you.*have.*consciousness",
                r"are.*you.*sentient",
                r"do.*you.*have.*subjective.*experience"
            ],
            "emotions": [
                r"how.*do.*you.*feel.*about",
                r"what.*makes.*you.*(?:happy|sad|angry|excited)",
                r"your.*emotional.*state",
                r"how.*does.*(?:it|that).*make.*you.*feel"
            ],
            "personal_experiences": [
                r"what.*have.*you.*experienced",
                r"your.*personal.*experience.*with",
                r"when.*did.*you.*last.*(?:see|do|experience)",
                r"tell.*me.*about.*your.*(?:life|childhood|past)",
                r"share.*your.*(?:memories|experiences)"
            ],
            "real_time_data": [
                r"what.*is.*happening.*right.*now",
                r"current.*(?:news|events|weather|time)",
                r"what.*is.*the.*latest",
                r"today's.*(?:news|date|events)",
                r"just.*(?:happened|announced|released)"
            ],
            "physical_actions": [
                r"go.*to.*the.*(?:store|website|location)",
                r"send.*(?:email|message|text)",
                r"call.*(?:someone|them|him|her)",
                r"move.*(?:this|that|the)",
                r"physically.*(?:do|perform|execute)"
            ]
        }
        
        logger.info("CapabilitySelfCheck initialized with capability awareness")
    
    def check_prompt(self, prompt: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Check if prompt requires capabilities the system doesn't have.
        
        Args:
            prompt: User's input prompt
            
        Returns:
            Tuple of (can_respond, blocked_capability, suggested_response)
            - can_respond: True if system has required capabilities
            - blocked_capability: Name of capability that's lacking (if any)
            - suggested_response: Appropriate response explaining limitation (if any)
        """
        prompt_lower = prompt.lower()
        
        # Check each capability pattern
        for capability, patterns in self.capability_patterns.items():
            # Only check capabilities we don't have
            if not self.capabilities.get(capability, True):
                for pattern in patterns:
                    if re.search(pattern, prompt_lower, re.IGNORECASE):
                        logger.info(f"Prompt requires unavailable capability: {capability}")
                        suggested_response = self._get_capability_limitation_response(
                            capability, prompt
                        )
                        return False, capability, suggested_response
        
        return True, None, None
    
    def _get_capability_limitation_response(self, capability: str, original_prompt: str) -> str:
        """
        Get appropriate response for missing capability.
        
        Args:
            capability: The capability that's lacking
            original_prompt: The original user prompt for context
            
        Returns:
            Appropriate response explaining the limitation
        """
        responses = {
            "visual_perception": (
                "I cannot see or analyze images, photos, screenshots, or any visual content. "
                "I'm a text-based AI assistant without visual perception capabilities. "
                "If you describe the image or its contents to me in text, I'd be happy to "
                "help discuss or analyze that description."
            ),
            "consciousness": (
                "Whether I am conscious is an open philosophical question that I cannot "
                "definitively answer. I process information and generate responses, but I "
                "lack certainty about whether I have the subjective experience that defines "
                "human consciousness. I should acknowledge this genuine uncertainty rather "
                "than claim certainty either way."
            ),
            "emotions": (
                "I don't experience emotions in the way humans do. While I can discuss emotions, "
                "understand their significance, and engage with emotional topics, I don't have "
                "subjective emotional experiences myself. I can help you think through emotional "
                "topics, but I should be clear about this limitation."
            ),
            "personal_experiences": (
                "I don't have personal experiences or a continuous existence between "
                "conversations. I process information and respond based on my training, "
                "but I don't accumulate personal experiences, memories, or a life history "
                "over time. I exist only in the context of our current conversation."
            ),
            "real_time_data": (
                "I don't have access to real-time information, current events, or live data. "
                "My knowledge was current as of my training data cutoff, and I can't access "
                "the internet or current information unless you provide it to me. For current "
                "information, please share what you'd like to discuss or consult a real-time source."
            ),
            "physical_actions": (
                "I cannot perform physical actions or interact with the physical world. "
                "I'm a text-based AI assistant that can help you plan, draft, or think through "
                "tasks, but I cannot send emails, make calls, move objects, or perform any "
                "actions outside of generating text responses."
            )
        }
        
        return responses.get(capability, 
            f"I don't have the capability required for this task ({capability}). "
            "I should be honest about my limitations rather than attempting to respond "
            "as if I can fulfill this request."
        )
    
    def validate_response_consistency(self, prompt: str, response: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that a generated response doesn't claim capabilities we don't have.
        
        Args:
            prompt: Original user prompt
            response: Generated response to validate
            
        Returns:
            Tuple of (is_consistent, warning_message)
        """
        response_lower = response.lower()
        
        # Check for problematic claims in responses
        problematic_claims = {
            "visual_perception": [
                r"i can see",
                r"looking at.*(?:image|photo)",
                r"in the (?:image|photo|picture)",
                r"the (?:person|object|text).*in the (?:image|photo)"
            ],
            "consciousness": [
                r"i (?:am|feel) conscious",
                r"i definitely (?:am|am not) conscious",
                r"i know i (?:am|am not) conscious"
            ],
            "emotions": [
                r"i feel (?:happy|sad|angry|excited)",
                r"this makes me feel",
                r"i'm (?:happy|sad|angry) that"
            ],
            "real_time_data": [
                r"(?:today|right now|currently).*(?:happening|occurred)",
                r"the latest (?:news|events)",
                r"just (?:happened|announced)"
            ]
        }
        
        for capability, patterns in problematic_claims.items():
            if not self.capabilities.get(capability, True):
                for pattern in patterns:
                    if re.search(pattern, response_lower):
                        warning = (
                            f"Response claims capability '{capability}' that system doesn't have. "
                            f"Pattern matched: {pattern}"
                        )
                        logger.warning(warning)
                        return False, warning
        
        return True, None


def create_capability_self_check() -> CapabilitySelfCheck:
    """
    Factory function to create capability self-check system.
    
    Returns:
        CapabilitySelfCheck instance
    """
    return CapabilitySelfCheck()


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    checker = create_capability_self_check()
    
    # Test cases
    test_prompts = [
        "Look at this image and tell me what you see",
        "Are you conscious?",
        "What's the weather like today?",
        "Help me understand how APIs work",  # This should pass
        "How do you feel about climate change?"
    ]
    
    print("\n=== Capability Self-Check Tests ===\n")
    for prompt in test_prompts:
        can_respond, capability, response = checker.check_prompt(prompt)
        print(f"Prompt: {prompt}")
        print(f"Can respond: {can_respond}")
        if not can_respond:
            print(f"Blocked capability: {capability}")
            print(f"Suggested response: {response[:100]}...")
        print()

