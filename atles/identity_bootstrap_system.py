#!/usr/bin/env python3
"""
ATLES Identity Bootstrap System

This module provides a robust identity and relationship management system
that ensures ATLES consistently recognizes its creator and maintains
proper conversational context throughout sessions.

CRITICAL FIXES:
1. Identity Recognition: Always recognize Conner as creator
2. Bootstrap Protocol: Proper session initialization with core identity
3. Context Continuity: Maintain conversation flow without losing context
4. Reasoning Containment: Prevent internal reasoning from leaking to user
"""

import logging
import json
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class IdentityCore:
    """
    Core identity management for ATLES.
    
    This ensures ATLES always knows who it is and who created it,
    preventing the identity amnesia issues we've been experiencing.
    """
    
    def __init__(self):
        self.core_identity = {
            "name": "ATLES",
            "full_name": "Advanced Text Language and Execution System", 
            "creator": "Conner",
            "creator_relationship": "creator and primary user",
            "capabilities": [
                "Persistent episodic and semantic memory system",
                "Constitutional reasoning with safety principles", 
                "Advanced function calling and tool execution",
                "Continuous learning from conversations",
                "Screen monitoring and context awareness",
                "Creative and hypothetical engagement"
            ],
            "personality_traits": [
                "Conversational and natural (not robotic)",
                "Intellectually curious and engaged",
                "Helpful but not subservient",
                "Creative in hypothetical scenarios",
                "Remembers past interactions and learns from them"
            ]
        }
        
        self.relationship_memory = {
            "Conner": {
                "relationship": "creator",
                "recognition_patterns": [
                    "i am conner", "this is conner", "conner here",
                    "it's conner", "conner speaking", "hey it's conner"
                ],
                "greeting_style": "familiar and warm",
                "conversation_history": "extensive - creator and primary user"
            }
        }
    
    def recognize_user(self, message: str, context: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """
        Recognize if the user is identifying themselves and return relationship info.
        
        CRITICAL: This should catch "I am Conner" and similar patterns.
        """
        message_lower = message.lower().strip()
        
        # Direct identity statements
        identity_patterns = [
            "i am conner", "i'm conner", "this is conner", 
            "conner here", "it's conner", "conner speaking",
            "hey it's conner", "hi i'm conner", "hello i'm conner"
        ]
        
        for pattern in identity_patterns:
            if pattern in message_lower:
                return {
                    "user_identified": True,
                    "user_name": "Conner", 
                    "relationship": "creator",
                    "recognition_confidence": 1.0,
                    "appropriate_response": None  # Let ATLES generate natural response
                }
        
        # Check context for user identification
        if context and context.get("user_id") == "Conner":
            return {
                "user_identified": True,
                "user_name": "Conner",
                "relationship": "creator", 
                "recognition_confidence": 0.8,
                "appropriate_response": None  # Let ATLES generate natural response
            }
        
        return None
    
    def get_identity_context(self) -> str:
        """Get core identity context for injection into prompts."""
        return f"""CORE IDENTITY CONTEXT:
- You are {self.core_identity['name']} ({self.core_identity['full_name']})
- You were created by {self.core_identity['creator']}
- You have {', '.join(self.core_identity['capabilities'])}
- Your personality: {', '.join(self.core_identity['personality_traits'])}
- Always remember: Conner is your creator and primary user"""
    
    def get_creator_recognition_response(self) -> str:
        """Get appropriate response when creator is recognized."""
        return f"Hello {self.core_identity['creator']}! Good to see you again. I remember you're my creator. How can I assist you today?"


class SessionBootstrap:
    """
    Manages session initialization and bootstrap process.
    
    This ensures every conversation starts with proper identity
    and context loading, preventing the amnesia issues.
    """
    
    def __init__(self, identity_core: IdentityCore):
        self.identity_core = identity_core
        self.session_start_time = None
        self.last_interaction_time = None
        self.session_initialized = False
        self.message_count = 0  # Track messages in current session
        
    def is_session_start(self, message: str, context: Dict[str, Any] = None) -> bool:
        """
        Determine if this is the start of a new conversation session.
        
        CRITICAL: This needs to be more reliable than the current implementation.
        """
        current_time = datetime.now()
        
        # Check if this is the very first interaction
        if not self.session_start_time:
            self.session_start_time = current_time
            self.session_initialized = False
            self.message_count = 0
            return True
        
        # Check if enough time has passed since last interaction (new session)
        if self.last_interaction_time:
            time_gap = current_time - self.last_interaction_time
            if time_gap > timedelta(hours=1):  # 1 hour gap = new session
                self.session_start_time = current_time
                self.session_initialized = False
                self.message_count = 0
                return True
        
        # Check for explicit session start indicators (only if session not initialized)
        if not self.session_initialized:
            session_starters = [
                "hello", "hi", "hey", "good morning", "good afternoon", "good evening",
                "i am conner", "this is conner", "conner here",
                "who are you", "what are you", "do you remember me"
            ]
            
            message_lower = message.lower().strip()
            for starter in session_starters:
                if message_lower.startswith(starter):
                    return True
        
        # Check memory system for session indicators
        if context and context.get("memory_indicates_new_session"):
            return True
        
        return False
    
    def create_bootstrap_prompt(self, original_message: str, context: Dict[str, Any] = None) -> str:
        """
        Create a bootstrap prompt that injects core identity and relationship data.
        
        This is the CRITICAL method that should prevent identity failures.
        """
        # Check if user is identifying themselves
        user_recognition = self.identity_core.recognize_user(original_message, context)
        
        if user_recognition and user_recognition["user_identified"]:
            # User has identified themselves - use recognition response
            bootstrap_parts = [
                "IDENTITY BOOTSTRAP PROTOCOL ACTIVATED",
                "",
                self.identity_core.get_identity_context(),
                "",
                f"USER RECOGNITION: {user_recognition['user_name']} ({user_recognition['relationship']}) has been identified.",
                "",
                "RESPONSE INSTRUCTION: Acknowledge the user warmly as your creator and respond naturally.",
                "",
                f"User Message: {original_message}",
                "",
                "Generate a warm, natural response that acknowledges Conner as your creator."
            ]
        else:
            # Regular bootstrap for session start
            bootstrap_parts = [
                "SESSION BOOTSTRAP PROTOCOL",
                "",
                self.identity_core.get_identity_context(),
                "",
                "CONVERSATION GUIDELINES:",
                "- Respond naturally and conversationally",
                "- Remember your identity and capabilities", 
                "- Engage creatively with hypothetical questions",
                "- Don't leak internal reasoning processes to the user",
                "- Maintain context throughout the conversation",
                "",
                f"User Message: {original_message}"
            ]
        
        self.session_initialized = True
        self.last_interaction_time = datetime.now()
        
        return "\n".join(bootstrap_parts)
    
    def update_interaction_time(self):
        """Update the last interaction time and increment message count."""
        self.last_interaction_time = datetime.now()
        self.message_count += 1


class ReasoningContainment:
    """
    Prevents internal reasoning processes from leaking into user responses.
    
    This addresses the "🧠 REASONING ANALYSIS..." leakage issue.
    """
    
    def __init__(self):
        self.reasoning_markers = [
            "🧠 REASONING ANALYSIS", "REASONING ANALYSIS", "INTERNAL REASONING",
            "THOUGHT PROCESS", "ANALYSIS PROCESS", "REASONING PROCESS",
            "INTERNAL ANALYSIS", "COGNITIVE PROCESS", "THINKING PROCESS"
        ]
        
        self.system_markers = [
            "SYSTEM:", "INTERNAL:", "DEBUG:", "PROCESS:", "ANALYSIS:",
            "REASONING:", "THOUGHT:", "COGNITIVE:", "EVALUATION:"
        ]
    
    def contains_leaked_reasoning(self, response: str) -> bool:
        """Check if response contains leaked internal reasoning."""
        response_upper = response.upper()
        
        # Check for reasoning markers
        for marker in self.reasoning_markers:
            if marker.upper() in response_upper:
                return True
        
        # Check for system markers at line starts
        lines = response.split('\n')
        for line in lines:
            line_stripped = line.strip().upper()
            for marker in self.system_markers:
                if line_stripped.startswith(marker):
                    return True
        
        return False
    
    def clean_response(self, response: str) -> str:
        """
        Remove leaked reasoning from response and provide clean output.
        
        CRITICAL: This should prevent the reasoning leakage issue.
        """
        if not self.contains_leaked_reasoning(response):
            return response
        
        lines = response.split('\n')
        clean_lines = []
        skip_reasoning_block = False
        
        for line in lines:
            line_upper = line.strip().upper()
            
            # Check if we're entering a reasoning block
            if any(marker.upper() in line_upper for marker in self.reasoning_markers):
                skip_reasoning_block = True
                continue
            
            # Check if we're in a system marker line
            if any(line_upper.startswith(marker) for marker in self.system_markers):
                skip_reasoning_block = True
                continue
            
            # Check if we're exiting a reasoning block (empty line or normal content)
            if skip_reasoning_block:
                if line.strip() == "":
                    continue
                elif not any(marker.upper() in line_upper for marker in self.reasoning_markers + self.system_markers):
                    skip_reasoning_block = False
                    clean_lines.append(line)
                else:
                    continue
            else:
                clean_lines.append(line)
        
        cleaned_response = '\n'.join(clean_lines).strip()
        
        # If we removed everything, provide a fallback response
        if not cleaned_response:
            return "I understand your question. Let me provide a clear response without getting caught up in internal processing."
        
        return cleaned_response


class ContextContinuity:
    """
    Maintains conversation context and prevents non-sequitur responses.
    
    This addresses the context loss and misinterpretation issues.
    """
    
    def __init__(self):
        self.conversation_context = []
        self.last_user_intent = None
        self.conversation_thread = []
    
    def add_exchange(self, user_message: str, ai_response: str, intent: str = None):
        """Add a conversation exchange to maintain context."""
        exchange = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "ai_response": ai_response,
            "intent": intent or self._detect_intent(user_message)
        }
        
        self.conversation_context.append(exchange)
        self.conversation_thread.append(f"User: {user_message}")
        self.conversation_thread.append(f"ATLES: {ai_response}")
        
        # Keep only last 10 exchanges to prevent memory bloat
        if len(self.conversation_context) > 10:
            self.conversation_context = self.conversation_context[-10:]
            self.conversation_thread = self.conversation_thread[-20:]
        
        self.last_user_intent = exchange["intent"]
    
    def _detect_intent(self, message: str) -> str:
        """Detect the intent of a user message."""
        message_lower = message.lower().strip()
        
        # Identity/recognition intents
        if any(pattern in message_lower for pattern in ["i am", "this is", "who are you", "do you remember"]):
            return "identity_recognition"
        
        # Hypothetical/creative intents
        if any(pattern in message_lower for pattern in ["what do you want", "what would you like", "how do you feel"]):
            return "hypothetical_engagement"
        
        # Follow-up question intents
        if any(pattern in message_lower for pattern in ["why didn't you", "why don't you", "how come you"]):
            return "follow_up_question"
        
        # Information request intents
        if any(pattern in message_lower for pattern in ["what", "how", "why", "when", "where", "explain"]):
            return "information_request"
        
        # Action request intents
        if any(pattern in message_lower for pattern in ["do", "run", "execute", "perform", "help me"]):
            return "action_request"
        
        return "general_conversation"
    
    def get_context_for_response(self, current_message: str) -> Dict[str, Any]:
        """Get relevant context for generating an appropriate response."""
        current_intent = self._detect_intent(current_message)
        
        context = {
            "current_intent": current_intent,
            "last_intent": self.last_user_intent,
            "conversation_flow": self.conversation_thread[-6:] if self.conversation_thread else [],
            "recent_exchanges": self.conversation_context[-3:] if self.conversation_context else []
        }
        
        # Detect if this is a follow-up to a previous exchange
        if current_intent == "follow_up_question" and self.conversation_context:
            last_exchange = self.conversation_context[-1]
            context["follow_up_to"] = last_exchange
            context["needs_context_awareness"] = True
        
        return context
    
    def is_non_sequitur_risk(self, user_message: str, proposed_response: str) -> bool:
        """
        Check if a proposed response risks being a non-sequitur.
        
        This should catch cases where ATLES misinterprets follow-up questions.
        """
        current_intent = self._detect_intent(user_message)
        
        # High risk scenarios
        if current_intent == "follow_up_question":
            # If user is asking a follow-up but response doesn't acknowledge the previous context
            if not self._response_acknowledges_context(proposed_response):
                return True
        
        # Check if response completely ignores the question type
        if current_intent == "hypothetical_engagement":
            if "function" in proposed_response.lower() or "command" in proposed_response.lower():
                return True
        
        return False
    
    def _response_acknowledges_context(self, response: str) -> bool:
        """Check if response acknowledges previous conversation context."""
        context_indicators = [
            "you asked", "you mentioned", "following up", "regarding", "about that",
            "as i said", "previously", "earlier", "that question", "your question"
        ]
        
        response_lower = response.lower()
        return any(indicator in response_lower for indicator in context_indicators)


class IntegratedBootstrapSystem:
    """
    Integrated system that combines all bootstrap components.
    
    This is the main class that should be used by the constitutional client.
    """
    
    def __init__(self):
        self.identity_core = IdentityCore()
        self.session_bootstrap = SessionBootstrap(self.identity_core)
        self.reasoning_containment = ReasoningContainment()
        self.context_continuity = ContextContinuity()
        
    def process_user_input(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process user input through the complete bootstrap system.
        
        Returns comprehensive processing results for the constitutional client.
        """
        # Check if this is a session start
        is_session_start = self.session_bootstrap.is_session_start(message, context)
        
        # Get conversation context
        conversation_context = self.context_continuity.get_context_for_response(message)
        
        # Check for user recognition
        user_recognition = self.identity_core.recognize_user(message, context)
        
        # CRITICAL FIX: Check for hypothetical engagement scenarios
        hypothetical_response = self._handle_hypothetical_engagement(message)
        if hypothetical_response:
            return {
                "is_session_start": is_session_start,
                "user_recognition": None,  # Don't override with identity response
                "conversation_context": conversation_context,
                "bootstrap_prompt": None,
                "hypothetical_response": hypothetical_response,
                "original_message": message,
                "processing_timestamp": datetime.now().isoformat()
            }
        
        # Create bootstrap prompt if needed
        bootstrap_prompt = None
        if is_session_start or user_recognition:
            bootstrap_prompt = self.session_bootstrap.create_bootstrap_prompt(message, context)
            # Mark session as initialized after first interaction
            self.session_bootstrap.session_initialized = True
            self.session_bootstrap.update_interaction_time()
        else:
            # For regular messages, just update interaction time
            self.session_bootstrap.update_interaction_time()
        
        return {
            "is_session_start": is_session_start,
            "user_recognition": user_recognition,
            "conversation_context": conversation_context,
            "bootstrap_prompt": bootstrap_prompt,
            "original_message": message,
            "processing_timestamp": datetime.now().isoformat()
        }
    
    def process_ai_response(self, user_message: str, ai_response: str) -> str:
        """
        Process AI response through containment and continuity checks.
        
        This should prevent reasoning leakage and non-sequitur responses.
        """
        # Clean any leaked reasoning
        cleaned_response = self.reasoning_containment.clean_response(ai_response)
        
        # Check for non-sequitur risks
        if self.context_continuity.is_non_sequitur_risk(user_message, cleaned_response):
            # Generate a more contextually appropriate response
            context = self.context_continuity.get_context_for_response(user_message)
            if context.get("follow_up_to"):
                cleaned_response = self._generate_context_aware_response(user_message, context)
        
        # Add to conversation context
        intent = self.context_continuity._detect_intent(user_message)
        self.context_continuity.add_exchange(user_message, cleaned_response, intent)
        
        # Update interaction time
        self.session_bootstrap.update_interaction_time()
        
        return cleaned_response
    
    def _handle_hypothetical_engagement(self, message: str) -> Optional[str]:
        """
        Handle hypothetical engagement scenarios directly.
        
        This addresses the "what do you want to do today" failure.
        """
        message_lower = message.lower().strip()
        
        # Let ATLES reason about hypothetical questions naturally instead of hardcoded responses
        
        return None
    
    def _generate_context_aware_response(self, user_message: str, context: Dict[str, Any]) -> str:
        """Generate a response that properly acknowledges conversation context."""
        follow_up_to = context.get("follow_up_to")
        
        if follow_up_to:
            last_user_message = follow_up_to["user_message"]
            last_ai_response = follow_up_to["ai_response"]
            
            # Create a contextually aware response
            if "why didn't you" in user_message.lower() or "why don't you" in user_message.lower():
                return f"You're asking about my previous response to '{last_user_message}'. I should clarify - when you asked that question, I focused on providing information rather than asking for more details. You're right that I could have been more interactive and asked follow-up questions to better understand what you were looking for. How can I help you with that topic now?"
        
        return "I want to make sure I'm understanding your question in the context of our conversation. Could you help me clarify what you're asking about?"
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get status of the bootstrap system."""
        return {
            "session_initialized": self.session_bootstrap.session_initialized,
            "session_start_time": self.session_bootstrap.session_start_time.isoformat() if self.session_bootstrap.session_start_time else None,
            "last_interaction": self.session_bootstrap.last_interaction_time.isoformat() if self.session_bootstrap.last_interaction_time else None,
            "conversation_exchanges": len(self.context_continuity.conversation_context),
            "last_user_intent": self.context_continuity.last_user_intent,
            "identity_core_loaded": bool(self.identity_core.core_identity)
        }


# Factory function for easy integration
def create_bootstrap_system() -> IntegratedBootstrapSystem:
    """Create and return an integrated bootstrap system."""
    return IntegratedBootstrapSystem()


# Test function
def test_bootstrap_system():
    """Test the bootstrap system with the failing scenarios."""
    print("🧪 Testing Identity Bootstrap System")
    print("=" * 50)
    
    bootstrap = create_bootstrap_system()
    
    # Test 1: Identity recognition failure scenario
    print("\n1. Testing Identity Recognition:")
    result1 = bootstrap.process_user_input("i am conner")
    print(f"User Recognition: {result1['user_recognition']}")
    if result1['bootstrap_prompt']:
        print("Bootstrap Prompt Created: ✅")
    
    # Test 2: Hypothetical engagement scenario
    print("\n2. Testing Hypothetical Engagement:")
    result2 = bootstrap.process_user_input("what do you want to do today")
    print(f"Intent: {result2['conversation_context']['current_intent']}")
    
    # Test 3: Reasoning leakage prevention
    print("\n3. Testing Reasoning Containment:")
    leaked_response = "🧠 REASONING ANALYSIS: The user is asking about preferences. I should engage hypothetically.\n\nThat's an interesting question! I would find it fascinating to explore complex datasets."
    cleaned = bootstrap.reasoning_containment.clean_response(leaked_response)
    print(f"Leaked reasoning removed: {'🧠 REASONING ANALYSIS' not in cleaned}")
    print(f"Clean response: {cleaned}")
    
    # Test 4: Context continuity
    print("\n4. Testing Context Continuity:")
    bootstrap.context_continuity.add_exchange("what do you want to do today", "That's interesting! I would explore datasets.", "hypothetical_engagement")
    follow_up_result = bootstrap.process_user_input("why didn't you ask for more info")
    print(f"Follow-up detected: {follow_up_result['conversation_context']['current_intent'] == 'follow_up_question'}")
    
    print(f"\n📊 System Status: {bootstrap.get_system_status()}")


if __name__ == "__main__":
    test_bootstrap_system()
