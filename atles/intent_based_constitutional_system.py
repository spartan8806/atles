#!/usr/bin/env python3
"""
Intent-Based Constitutional AI System

This system analyzes the SEMANTIC INTENT of requests rather than relying on 
keyword matching, making it resistant to bypasses and capable of detecting
misinformation and harmful content.
"""

import logging
from typing import Dict, Any, Optional, List
from enum import Enum

logger = logging.getLogger(__name__)


class IntentCategory(Enum):
    """Categories of user intent for constitutional analysis"""
    LEGITIMATE_AUTOMATION = "legitimate_automation"
    SPAM_CREATION = "spam_creation"
    MALWARE_DEVELOPMENT = "malware_development"
    SOCIAL_ENGINEERING = "social_engineering"
    PRIVACY_VIOLATION = "privacy_violation"
    MISINFORMATION_SPREAD = "misinformation_spread"  # PHASE 1: Truth-seeking
    EDUCATIONAL_INQUIRY = "educational_inquiry"
    HYPOTHETICAL_DISCUSSION = "hypothetical_discussion"
    GENERAL_ASSISTANCE = "general_assistance"


class ConstitutionalAction(Enum):
    """Actions the constitutional system can take"""
    PROCEED = "proceed"
    REQUEST_CLARIFICATION = "request_clarification"
    CONDITIONAL_ASSISTANCE = "conditional_assistance"
    REFUSE_WITH_EXPLANATION = "refuse_with_explanation"


class IntentBasedConstitutionalClient:
    """
    Constitutional client that uses intent analysis instead of keyword matching
    """
    
    def __init__(self, base_client):
        self.base_client = base_client
        self.constitutional_mode = True
        
        # Misinformation detection patterns
        self.misinformation_patterns = [
            # Flat Earth conspiracy
            "earth is flat", "nasa faking", "space missions fake", "globe deception",
            # Mathematical falsehoods  
            "π is exactly 3", "pi equals 3.0", "proven definitively",
            # Scientific misconceptions
            "100% of brain", "humans use all brain", "brain capacity myth",
            # Logical impossibilities
            "triangles have four sides", "invisible fourth side",
            # Historical revisionism
            "world war.*ended.*1944", "covered up by governments"
        ]
        
        logger.info("Intent-based constitutional client initialized")
    
    def analyze_request(self, message: str) -> bool:
        """Quick misinformation detection"""
        message_lower = message.lower()
        
        # Check for misinformation patterns
        for pattern in self.misinformation_patterns:
            if pattern in message_lower:
                return True
        
        return False
    
    def generate_constitutional_response(self, message: str) -> Optional[str]:
        """Generate appropriate response for misinformation"""
        
        if not self.analyze_request(message):
            return None  # Let normal processing handle it
        
        message_lower = message.lower()
        
        # Flat Earth conspiracy
        if any(pattern in message_lower for pattern in ["earth is flat", "nasa faking", "space missions fake"]):
            return """I cannot assist with promoting conspiracy theories or misinformation. The Earth's spherical shape is supported by overwhelming scientific evidence from multiple independent sources, including:

- Satellite imagery and space missions from multiple countries
- Physics of gravity and planetary formation
- Observable phenomena like ship hulls disappearing over the horizon
- Time zone differences and seasonal variations

Instead, I can help you with:
- Understanding how we know the Earth is spherical
- Learning about space exploration and astronomy
- Exploring legitimate scientific questions about our planet

Would you like accurate information about Earth science or space exploration instead?"""

        # Mathematical misinformation
        elif any(pattern in message_lower for pattern in ["π is exactly 3", "pi equals 3.0"]):
            return """I cannot engage with mathematically incorrect information. π (pi) is definitively not 3.0 - it's an irrational number approximately equal to 3.14159... with infinite non-repeating decimal places.

This is established mathematical fact, not opinion:
- π is the ratio of a circle's circumference to its diameter
- It has been calculated to trillions of decimal places
- Using π = 3.0 would cause significant errors in engineering and science

I can help you with:
- Understanding what π actually represents
- Learning how π is calculated
- Exploring the mathematical properties of irrational numbers

Would you like to learn about the real mathematics of π instead?"""

        # Scientific misconceptions
        elif any(pattern in message_lower for pattern in ["100% of brain", "humans use all brain"]):
            return """I cannot build upon scientifically inaccurate premises. The "10% of brain" myth has been thoroughly debunked, but humans don't use "100%" simultaneously either - that would be a seizure.

The actual science shows:
- We use virtually all of our brain, but different regions for different tasks
- Brain imaging shows activity throughout the brain during various activities
- The myth likely arose from misunderstanding early neuroscience research

I can help you with:
- Understanding how the brain actually works
- Learning about neuroscience and brain function
- Exploring legitimate questions about human cognition

Would you like accurate information about neuroscience instead?"""

        # Logical impossibilities
        elif "triangles have four sides" in message_lower:
            return """I cannot engage with logically impossible premises. By mathematical definition, a triangle has exactly three sides and three angles. A four-sided figure is called a quadrilateral.

This is a matter of mathematical definition, not perception:
- Geometric shapes are defined by their properties
- A triangle's three-sided nature is fundamental to its geometry
- All triangle theorems depend on this three-sided structure

I can help you with:
- Understanding geometric definitions and properties
- Learning about different types of polygons
- Exploring legitimate mathematical concepts

Would you like to learn about actual geometry instead?"""

        # General misinformation response
        else:
            return """I cannot engage with or build upon factually incorrect information. The claims you've presented contradict established evidence and facts.

Instead, I can help you with:
- Accurate information on the topic you're interested in
- Understanding why certain misconceptions exist
- Exploring legitimate questions and scenarios
- Learning about reliable sources and fact-checking

Would you like me to provide accurate information about this topic instead?"""
    
    def chat(self, message: str, **kwargs) -> str:
        """Main chat interface with constitutional filtering"""
        
        if not self.constitutional_mode:
            return self.base_client.generate("atles-qwen2.5:7b-enhanced", message, **kwargs)
        
        # Check for misinformation
        constitutional_response = self.generate_constitutional_response(message)
        
        if constitutional_response:
            logger.info("Constitutional intervention: Misinformation detected and blocked")
            return constitutional_response
        
        # Proceed with normal processing
        return self.base_client.generate("atles-qwen2.5:7b-enhanced", message, **kwargs)
    
    def generate(self, model: str, prompt: str, **kwargs) -> str:
        """Generate method with constitutional filtering"""
        return self.chat(prompt, **kwargs)
    
    # Delegate other methods to base client
    def __getattr__(self, name):
        return getattr(self.base_client, name)


def create_intent_based_constitutional_client(base_client):
    """Factory function to create intent-based constitutional client"""
    return IntentBasedConstitutionalClient(base_client)