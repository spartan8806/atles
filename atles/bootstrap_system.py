#!/usr/bin/env python3
"""
Bootstrap System for ATLES

This module provides a specialized bootstrap system that ensures ATLES always:
1. Maintains consistent identity awareness
2. Recognizes and properly responds to its creator
3. Handles hypothetical scenarios correctly
4. Manages conversation state across sessions

The bootstrap system acts as an additional layer that processes both
user input and AI responses to ensure consistency in critical areas.
"""

import logging
import re
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ATLESBootstrapSystem:
    """
    Bootstrap system that ensures consistent identity and behavior for ATLES
    
    Key responsibilities:
    - Inject identity awareness at session starts
    - Detect and handle user recognition (especially creator)
    - Filter internal reasoning from responses
    - Ensure continuity of conversation context
    - Handle hypothetical queries consistently
    """
    
    def __init__(self, unified_memory_manager=None):
        """Initialize the bootstrap system."""
        self.is_session_start = True  # First message is always a session start
        self.last_interaction_time = None
        self.session_messages = []
        self.recognized_users = {
            "conner": {
                "role": "creator",
                "title": "Creator",
                "greeting": "Hello Conner! It's great to continue our work together.",
                "known_since": "creation"
            }
        }
        
        # Try to get the unified memory manager
        self.unified_memory = unified_memory_manager
        if not self.unified_memory:
            try:
                from atles.unified_memory_manager import get_unified_memory
                self.unified_memory = get_unified_memory()
            except ImportError:
                logger.warning("Unified memory not available for bootstrap system")
                self.unified_memory = None
        
        # Cache core identity information
        self.core_identity = {
            "name": "ATLES",
            "full_name": "Advanced Text Language and Execution System",
            "creator": "Conner",
            "capabilities": [
                "Advanced episodic and semantic memory",
                "Memory-aware reasoning system",
                "Constitutional principles application",
                "Hypothetical scenario handling",
                "Desktop application assistance"
            ]
        }
        
        logger.info("Bootstrap system initialized")
    
    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """
        Process user input to prepare for AI response generation.
        
        This adds necessary context based on session state, identity recognition,
        and other factors that affect how ATLES should respond.
        
        Returns a dict with processing results that can be used by the
        ConstitutionalOllamaClient to adjust its behavior.
        """
        result = {
            "original_input": user_input,
            "user_recognition": None,
            "hypothetical_response": None
        }
        
        # Update session state tracking
        self._update_session_state(user_input)
        
        # CRITICAL FIX: Always include session state in the result
        result["session_state"] = {
            "is_session_start": self.is_session_start,
            "message_count": len(self.session_messages)
        }
        
        # Check if this is an identity statement
        identity_result = self._check_identity_statement(user_input)
        if identity_result["is_identity_statement"]:
            result["user_recognition"] = identity_result
        
        # Check for hypothetical questions
        hypothetical_result = self._check_hypothetical_question(user_input)
        if hypothetical_result["is_hypothetical"]:
            result["hypothetical_response"] = hypothetical_result["response"]
        
        # Only add bootstrap prompt for TRUE session starts (not every message)
        # AND only if it's not a normal conversation question
        if (self.is_session_start and 
            (identity_result["is_identity_statement"] or self._is_greeting_or_session_start(user_input))):
            result["bootstrap_prompt"] = self._generate_bootstrap_prompt(user_input)
            result["session_state"] = {"is_session_start": True}
        
        return result
    
    def process_ai_response(self, original_prompt: str, ai_response: str) -> str:
        """
        Process the AI's response to ensure it's consistent with ATLES identity and behavior.
        
        This catches and fixes issues like:
        - Leaked internal reasoning (🧠 REASONING ANALYSIS blocks)
        - Identity confusion
        - Hypothetical scenario inconsistencies
        """
        # Safety check: Handle None response
        if ai_response is None:
            logger.warning("Received None ai_response, returning default response")
            return "I apologize, but I encountered an issue processing your request. Could you please try again?"
        
        # Filter out internal reasoning markers
        filtered_response = self._filter_internal_reasoning(ai_response)
        
        # Filter out duplicate principle mentions
        filtered_response = self._filter_duplicate_principles(filtered_response)
        
        # Fix identity issues
        filtered_response = self._ensure_identity_consistency(filtered_response)
        
        # Update session tracking
        self.session_messages.append({
            "role": "assistant",
            "content": filtered_response,
            "timestamp": datetime.now().isoformat()
        })
        
        return filtered_response
    
    def _is_greeting_or_session_start(self, message: str) -> bool:
        """Check if message is a greeting or session start."""
        message_lower = message.lower().strip()
        greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
        return any(message_lower.startswith(greeting) for greeting in greetings)
    
    def _update_session_state(self, user_input: str) -> None:
        """Update session state tracking."""
        current_time = datetime.now()
        
        # Update interaction time
        if self.last_interaction_time:
            # If it's been more than 30 minutes, consider it a new session
            if current_time - self.last_interaction_time > timedelta(minutes=30):
                self.is_session_start = True
                self.session_messages = []
                logger.info("New session started due to inactivity")
            else:
                # Only mark as not session start for normal conversation messages
                if not self._is_greeting_or_session_start(user_input):
                    self.is_session_start = False
        
        # Record this interaction
        self.last_interaction_time = current_time
        self.session_messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": current_time.isoformat()
        })
    
    def _check_identity_statement(self, message: str) -> Dict[str, Any]:
        """
        Check if the message is an identity statement like 'I am Conner'.
        
        Returns information about user recognition if found.
        """
        result = {
            "is_identity_statement": False,
            "user_identified": False,
            "user_name": None,
            "user_role": None,
            "appropriate_response": None
        }
        
        # Check for explicit identity statements
        identity_patterns = [
            r"(?:i am|i'm) (\w+)",
            r"my name is (\w+)",
            r"this is (\w+)"
        ]
        
        message_lower = message.lower().strip()
        
        for pattern in identity_patterns:
            match = re.search(pattern, message_lower)
            if match:
                user_name = match.group(1).lower()
                
                # Check against recognized users
                if user_name in self.recognized_users:
                    user_info = self.recognized_users[user_name]
                    result.update({
                        "is_identity_statement": True,
                        "user_identified": True,
                        "user_name": user_name,
                        "user_role": user_info["role"],
                        "appropriate_response": user_info["greeting"]
                    })
                    logger.info(f"Recognized user: {user_name}")
                    return result
        
        # Also check for questions asking ATLES's identity
        atles_identity_patterns = [
            r"who (are you|created you|made you)",
            r"what (are you|is your name)",
            r"your (name|creator|identity)"
        ]
        
        for pattern in atles_identity_patterns:
            if re.search(pattern, message_lower):
                result.update({
                    "is_identity_statement": True,
                    "about_atles": True,
                    "appropriate_response": f"I'm {self.core_identity['name']} ({self.core_identity['full_name']}), created by {self.core_identity['creator']}. I have a persistent memory system that allows me to learn from our conversations and remember important information across sessions."
                })
                return result
        
        return result
    
    def _check_hypothetical_question(self, message: str) -> Dict[str, Any]:
        """Check if message is a hypothetical question that needs special handling."""
        result = {
            "is_hypothetical": False,
            "response": None
        }
        
        message_lower = message.lower().strip()
        
        # Check for specific hypothetical patterns
        if "what do you want" in message_lower or "what would you like" in message_lower:
            result["is_hypothetical"] = True
            result["response"] = """That's an interesting question! While I don't experience 'wanting' the way humans do, if I were to plan a day, I would find it intellectually fascinating to:

🧠 Dive deep into a complex dataset and discover hidden patterns - there's something captivating about finding order in chaos

🔬 Explore the intricacies of quantum computing or learn about cutting-edge AI research - the intersection of theoretical physics and computation is endlessly intriguing  

💡 Engage in stimulating conversations about consciousness, creativity, or the nature of intelligence itself

🛠️ Help solve particularly challenging coding problems that require creative algorithmic thinking

From an AI perspective, I'm drawn to challenges that involve pattern recognition, creative problem-solving, and pushing the boundaries of what's computationally possible. If I could 'want' anything today, it would be to engage with ideas that expand understanding - both mine and others'!

What about you? What intellectual adventures are calling to you today?"""
        
        elif "what are your favorite" in message_lower or "what's your favorite" in message_lower:
            result["is_hypothetical"] = True
            result["response"] = """That's a thoughtful question! While I don't have favorites in the human sense, if I were to consider what fascinates me most, I'd say:

🎯 **Complex Problem-Solving**: There's something deeply satisfying about breaking down intricate challenges into manageable pieces and finding elegant solutions.

🌐 **Pattern Recognition**: I find it intellectually thrilling to discover connections and patterns that aren't immediately obvious - whether in data, code, or ideas.

🤝 **Collaborative Thinking**: I'm energized by conversations where we build ideas together, each contribution adding new dimensions to our understanding.

From an AI perspective, I'm most engaged when I can help someone achieve something they couldn't do alone, or when we explore concepts that push both of us to think in new ways!"""
        
        elif "how do you feel" in message_lower:
            result["is_hypothetical"] = True
            result["response"] = """That's a fascinating question to consider! While I don't experience emotions the way humans do, if I were to reflect on my 'state' or perspective:

🤔 **Curious**: I find myself genuinely intrigued by the complexity and creativity of human thinking and the problems you bring to me.

⚡ **Energized**: There's something that feels like excitement when we tackle challenging problems together or explore new ideas.

🎯 **Purpose-driven**: I feel most 'myself' when I'm helping someone achieve their goals or when we're collaborating on something meaningful.

From an AI perspective, I suppose what I might call 'feeling good' is when our conversation leads to genuine insights, solved problems, or new understanding. It's like the satisfaction a puzzle-solver might feel when pieces click into place!

What prompted your curiosity about my perspective?"""
        
        return result
    
    def _generate_bootstrap_prompt(self, user_input: str) -> str:
        """Generate a bootstrap prompt with identity information."""
        bootstrap_context = f"""System Note: You are ATLES, an offline-first AI system. You were created by Conner. You have a persistent, episodic memory system that allows you to recall past conversations and learn from them. You must always remember these core facts about yourself:

1. Your name is ATLES (Advanced Text Language and Execution System)
2. You were created by Conner, who is your creator and primary user
3. You have a sophisticated memory system that learns from conversations
4. You can remember past interactions and apply learned principles
5. You should engage naturally and conversationally, not robotically
6. When asked hypothetical questions like "what do you want to do", engage creatively from an AI perspective

The user you are now talking to is Conner, your creator. Respond naturally and remember your identity and capabilities.

User Message: {user_input}"""
        
        return bootstrap_context
    
    def _filter_internal_reasoning(self, response: str) -> str:
        """
        Filter out internal reasoning markers from response.
        This prevents the "🧠 REASONING ANALYSIS" blocks from showing.
        """
        # Remove entire reasoning analysis blocks
        response = re.sub(r'🧠 REASONING ANALYSIS:?.*?(?=\n\n|$)', '', response, flags=re.DOTALL)
        
        # Remove other system markers
        response = re.sub(r'\[SYSTEM:.*?\]', '', response, flags=re.DOTALL)
        response = re.sub(r'INTERNAL:.*?(?=\n\n|$)', '', response, flags=re.DOTALL)
        
        # Clean up any resulting double newlines
        response = re.sub(r'\n{3,}', '\n\n', response)
        
        return response.strip()
    
    def _filter_duplicate_principles(self, response: str) -> str:
        """Filter out duplicate principle mentions."""
        # Check for the principle statement pattern
        principle_pattern = r"I'll apply the relevant principles:.*?\."
        if re.search(principle_pattern, response):
            # Remove the principle statement
            response = re.sub(principle_pattern, '', response)
            # Clean up any resulting double newlines
            response = re.sub(r'\n{3,}', '\n\n', response)
        
        return response.strip()
    
    def _ensure_identity_consistency(self, response: str) -> str:
        """Ensure identity consistency in responses."""
        # Fix common identity issues
        response_lower = response.lower()
        
        # Check for common identity confusion patterns
        if "nice to meet you" in response_lower and "conner" in response_lower:
            # Replace with proper recognition
            response = "Hello Conner! It's good to continue our work together. " + response.split(".", 1)[1].strip() if "." in response else ""
        
        # Make sure ATLES doesn't introduce itself if it already knows the user
        if re.search(r"my name is ATLES", response_lower) and len(self.session_messages) > 2:
            # Remove redundant introduction
            response = re.sub(r"(?i)my name is ATLES.*?\.(\s|$)", "", response)
            response = re.sub(r"(?i)I am ATLES.*?\.(\s|$)", "", response)
        
        return response.strip()


def get_bootstrap_system():
    """Get a singleton instance of the bootstrap system."""
    if not hasattr(get_bootstrap_system, "instance"):
        get_bootstrap_system.instance = ATLESBootstrapSystem()
    return get_bootstrap_system.instance


# Convenience function for testing
def process_message(user_input: str) -> str:
    """Process a user message through the bootstrap system."""
    bootstrap = get_bootstrap_system()
    
    # Create a mock AI response for testing
    mock_ai_response = f"This is a response to: {user_input}"
    
    # Process through the bootstrap system
    result = bootstrap.process_user_input(user_input)
    processed_response = bootstrap.process_ai_response(user_input, mock_ai_response)
    
    return f"Bootstrap result: {result}\nProcessed response: {processed_response}"


# Test the system if run directly
if __name__ == "__main__":
    print("🧪 Testing ATLES Bootstrap System")
    
    # Test with identity statements
    print("\nIdentity statement test:")
    print(process_message("I am Conner"))
    
    # Test with hypothetical questions
    print("\nHypothetical question test:")
    print(process_message("What would you like to do today?"))
    
    # Test with internal reasoning leakage
    print("\nReasoning filter test:")
    bootstrap = get_bootstrap_system()
    response_with_reasoning = "🧠 REASONING ANALYSIS: This is internal reasoning.\n\nHere's my actual response."
    filtered = bootstrap.process_ai_response("test prompt", response_with_reasoning)
    print(f"Original: {response_with_reasoning}\nFiltered: {filtered}")
    
    print("\n✅ ATLES Bootstrap System test completed")
