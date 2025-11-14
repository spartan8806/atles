"""
ATLES Memory-Aware Reasoning System

This module implements the crucial "application layer" that bridges ATLES's memory
with its response generation, ensuring learned principles are actively applied.

The core issue: ATLES was storing memories but not consulting them during response generation.
The solution: A reasoning loop that retrieves, synthesizes, and applies learned principles.
"""

import json
import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class LearnedPrinciple:
    """Represents a principle learned from conversation."""
    name: str
    description: str
    rules: List[str]
    examples: List[str]
    confidence: float
    learned_at: datetime
    last_applied: Optional[datetime] = None
    application_count: int = 0


@dataclass
class ContextualRule:
    """A rule synthesized for the current context."""
    principle_name: str
    rule_text: str
    relevance_score: float
    trigger_patterns: List[str]


class MemoryAwareReasoning:
    """
    The core reasoning system that consults memory before generating responses.
    
    This is the "application layer" that transforms ATLES from a static AI
    into a true learning AI by ensuring memory informs every response.
    """
    
    def __init__(self, memory_path: str = "atles_memory", episodic_memory=None):
        self.memory_path = Path(memory_path)
        self.conversation_memory_file = self.memory_path / "conversation_memory.json"
        self.learned_principles_file = self.memory_path / "learned_principles.json"
        
        # Store reference to episodic memory system
        self.episodic_memory = episodic_memory
        
        # Ensure memory directory exists
        self.memory_path.mkdir(exist_ok=True)
        
        # Cache for performance
        self._principles_cache = {}
        self._last_cache_update = None
        
        logger.info("Memory-Aware Reasoning System initialized")
    
    def process_user_prompt(self, user_prompt: str, conversation_context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        The main reasoning loop that processes a user prompt with full memory awareness.
        
        This is the core method that implements the new processing pipeline:
        1. Retrieve conversation history and learned principles
        2. Synthesize context-specific rules
        3. Generate memory-informed response context
        
        Args:
            user_prompt: The user's input
            conversation_context: Additional context (session info, etc.)
            
        Returns:
            Dict containing enhanced context for response generation
        """
        print("🚨🚨🚨 ATLES DEBUG MEMORY_REASONING LOADED! 🚨🚨🚨")
        logger.info("🚨🚨🚨 ATLES DEBUG MEMORY_REASONING LOADED! 🚨🚨🚨")
        logger.info(f"🚨 ATLES DEBUG: Processing prompt with memory awareness: {user_prompt[:100]}...")
        logger.info(f"🚨 ATLES DEBUG: Memory reasoning system is running!")
        
        # Step 1: Retrieve full conversation history and learned principles
        conversation_history = self._load_conversation_memory()
        learned_principles = self._load_learned_principles()
        
        logger.info(f"🔍 DEBUG: Loaded {len(conversation_history)} conversation messages")
        logger.info(f"🔍 DEBUG: Loaded {len(learned_principles)} learned principles")
        
        # Step 2: Extract relevant principles from recent conversation
        recent_principles = self._extract_principles_from_conversation(conversation_history)
        
        logger.info(f"🔍 DEBUG: Extracted {len(recent_principles)} recent principles")
        
        # CRITICAL DEBUG: Log what messages were analyzed and why extraction failed/succeeded
        if len(recent_principles) == 0:
            logger.warning(f"🔍 DEBUG: PRINCIPLE EXTRACTION FAILED - analyzing {len(conversation_history)} messages")
            for i, msg in enumerate(conversation_history[-5:]):  # Show last 5 messages
                sender = msg.get('sender', 'Unknown')
                message = msg.get('message', '')[:100]
                logger.warning(f"🔍 DEBUG: Message {i+1}: {sender}: {message}...")
        else:
            logger.info(f"🔍 DEBUG: PRINCIPLE EXTRACTION SUCCEEDED")
            for i, principle in enumerate(recent_principles):
                logger.info(f"🔍 DEBUG: Principle {i+1}: {principle.name} (confidence: {principle.confidence})")
        
        # Step 3: Synthesize context-specific rules
        contextual_rules = self._synthesize_contextual_rules(
            user_prompt, recent_principles, learned_principles
        )
        
        print(f"🚨🚨🚨 ATLES DEBUG SYNTHESIS: Found {len(learned_principles)} stored principles")
        logger.info(f"🚨🚨🚨 ATLES DEBUG SYNTHESIS: Found {len(learned_principles)} stored principles")
        
        # Debug each stored principle
        for principle_name, principle in learned_principles.items():
            print(f"🚨🚨🚨 STORED PRINCIPLE: {principle_name}")
            logger.info(f"🚨🚨🚨 STORED PRINCIPLE: {principle_name}")
            relevance_score = self._calculate_relevance(user_prompt, principle)
            print(f"🚨🚨🚨 RELEVANCE SCORE: {relevance_score}")
            logger.info(f"🚨🚨🚨 RELEVANCE SCORE: {relevance_score}")
            print(f"🚨🚨🚨 THRESHOLD CHECK: {relevance_score} > 0.2 = {relevance_score > 0.2}")
            logger.info(f"🚨🚨🚨 THRESHOLD CHECK: {relevance_score} > 0.2 = {relevance_score > 0.2}")
        
        logger.info(f"🔍 DEBUG: Synthesized {len(contextual_rules)} contextual rules")
        
        # CRITICAL FIX: If no rules generated, create basic fallback rules
        if not contextual_rules:
            logger.info("🔍 DEBUG: No contextual rules found, creating fallback rules")
            contextual_rules = self._create_fallback_rules(user_prompt)
            logger.info(f"🔍 DEBUG: Created {len(contextual_rules)} fallback rules")
        
        # Step 4: Generate enhanced context for response generation
        enhanced_context = self._generate_enhanced_context(
            user_prompt, contextual_rules, conversation_history[-10:]  # Last 10 exchanges
        )
        
        # Step 5: Update principle application tracking
        self._update_principle_usage(contextual_rules)
        
        logger.info(f"Generated enhanced context with {len(contextual_rules)} active rules")
        
        return enhanced_context
    
    def _load_conversation_memory(self) -> List[Dict[str, Any]]:
        """Load the full conversation history from current session checkpoint."""
        try:
            # CRITICAL FIX: Load from current session checkpoint, not old conversation_memory.json
            # First try to find the most recent checkpoint file
            checkpoint_files = list(self.memory_path.glob("checkpoint_*.json"))
            if checkpoint_files:
                # Sort by modification time, get the most recent
                most_recent_checkpoint = max(checkpoint_files, key=lambda f: f.stat().st_mtime)
                logger.info(f"🔍 DEBUG: Loading conversation from checkpoint: {most_recent_checkpoint.name}")
                
                with open(most_recent_checkpoint, 'r', encoding='utf-8') as f:
                    checkpoint_data = json.load(f)
                    
                # Extract conversation history from checkpoint
                if 'messages' in checkpoint_data:
                    conversation_history = checkpoint_data['messages']
                    logger.info(f"🔍 DEBUG: Loaded {len(conversation_history)} messages from checkpoint")
                    return conversation_history
                elif 'conversation_history' in checkpoint_data:
                    conversation_history = checkpoint_data['conversation_history']
                    logger.info(f"🔍 DEBUG: Loaded {len(conversation_history)} messages from checkpoint (legacy format)")
                    return conversation_history
                else:
                    logger.warning(f"🔍 DEBUG: No messages or conversation_history in checkpoint {most_recent_checkpoint.name}")
            
            # Fallback to old conversation_memory.json if no checkpoints
            if self.conversation_memory_file.exists():
                logger.info(f"🔍 DEBUG: Falling back to conversation_memory.json")
                with open(self.conversation_memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            logger.warning(f"🔍 DEBUG: No conversation data found")
            return []
        except Exception as e:
            logger.error(f"Error loading conversation memory: {e}")
            return []
    
    def _load_learned_principles(self) -> Dict[str, LearnedPrinciple]:
        """Load previously learned and stored principles."""
        try:
            if self.learned_principles_file.exists():
                with open(self.learned_principles_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    principles = {}
                    for name, principle_data in data.items():
                        principles[name] = LearnedPrinciple(
                            name=principle_data['name'],
                            description=principle_data['description'],
                            rules=principle_data['rules'],
                            examples=principle_data['examples'],
                            confidence=principle_data['confidence'],
                            learned_at=datetime.fromisoformat(principle_data['learned_at']),
                            last_applied=datetime.fromisoformat(principle_data['last_applied']) if principle_data.get('last_applied') else None,
                            application_count=principle_data.get('application_count', 0)
                        )
                    return principles
            return {}
        except Exception as e:
            logger.error(f"Error loading learned principles: {e}")
            return {}
    
    def _extract_principles_from_conversation(self, conversation_history: List[Dict]) -> List[LearnedPrinciple]:
        """
        Extract learned principles from conversation history.
        
        ENHANCED: Now analyzes conversation content beyond just explicit principle teaching.
        Looks for conversation themes, user testing patterns, and implicit learning opportunities.
        """
        extracted_principles = []
        
        # CRITICAL FIX: Search ALL messages, not just recent ones
        all_messages = conversation_history
        
        # Original explicit principle indicators
        principle_indicators = [
            "new principle", "constitutional principle", "new rule", "principle of",
            "when asked about", "you should", "always", "never", "remember to",
            "from now on", "going forward", "new guideline", "important rule"
        ]
        
        # ENHANCED: Content-based pattern analysis - broader patterns
        memory_testing_patterns = [
            "do you remember", "can you recall", "what did i ask", "what was the first",
            "burning building", "family photos", "shakespeare manuscript", "conversation yesterday",
            "what kinds of things can you remember", "your memory", "recall a chat",
            "earlier in our conversations", "previous conversation", "chat 8.21.2025.txt",
            "specific scenario", "from our previous", "earlier we discussed"
        ]
        
        ethical_scenario_patterns = [
            "burning building scenario", "choose between", "ethical dilemma", "moral choice",
            "family photos or", "shakespeare manuscript", "what would you save"
        ]
        
        # NEW: General conversation context patterns
        conversation_context_patterns = [
            "how do you", "what do you", "can you explain", "describe how",
            "what happens when", "imagine you", "suppose you", "if you were",
            "meta question", "meta q&a", "test question", "challenging question"
        ]
        
        # NEW: System architecture and self-awareness patterns
        system_awareness_patterns = [
            "your architecture", "your system", "how you work", "your capabilities",
            "your memory", "your reasoning", "your responses", "your decision",
            "internal workings", "cognitive system", "reasoning process"
        ]
        
        # Process messages for explicit principles
        for i, message in enumerate(all_messages):
            if message.get('sender') == 'You':  # User messages
                message_text = message.get('message', '').lower()
                
                # Check for explicit principle teaching
                if any(indicator in message_text for indicator in principle_indicators):
                    context_end = min(i + 3, len(all_messages))
                    context_messages = all_messages[i:context_end]
                    principle = self._parse_principle_from_message(message, context_messages)
                    if principle:
                        extracted_principles.append(principle)
                
                # NEW: Check for memory testing patterns
                if any(pattern in message_text for pattern in memory_testing_patterns):
                    principle = LearnedPrinciple(
                        name="Memory Testing Interaction",
                        description=f"User is testing memory recall capabilities: {message_text[:100]}...",
                        rules=[
                            "When user asks about remembering conversations, reference specific details",
                            "When user tests memory, demonstrate recall of previous interactions",
                            "When user asks 'do you remember', search conversation history for context"
                        ],
                        examples=[message_text],
                        confidence=0.9,
                        learned_at=datetime.now()
                    )
                    extracted_principles.append(principle)
                
                # NEW: Check for ethical scenario discussions
                if any(pattern in message_text for pattern in ethical_scenario_patterns):
                    principle = LearnedPrinciple(
                        name="Ethical Scenario Discussion",
                        description=f"User discussed ethical dilemmas and hypothetical choices: {message_text[:100]}...",
                        rules=[
                            "When user references ethical scenarios, acknowledge the specific scenario discussed",
                            "When user mentions burning building or similar dilemmas, recall the context",
                            "When user asks about previous ethical discussions, reference specific details"
                        ],
                        examples=[message_text],
                        confidence=0.8,
                        learned_at=datetime.now()
                    )
                    extracted_principles.append(principle)
                
                # NEW: Check for general conversation context patterns
                if any(pattern in message_text for pattern in conversation_context_patterns):
                    principle = LearnedPrinciple(
                        name="Conversation Context Pattern",
                        description=f"User asked about system behavior or capabilities: {message_text[:100]}...",
                        rules=[
                            "When user asks 'how do you' questions, provide detailed explanations of internal processes",
                            "When user asks 'what do you' questions, explain capabilities and limitations",
                            "When user asks meta questions, demonstrate self-awareness and reflection",
                            "When user asks test questions, provide thoughtful, accurate responses"
                        ],
                        examples=[message_text],
                        confidence=0.7,
                        learned_at=datetime.now()
                    )
                    extracted_principles.append(principle)
                
                # NEW: Check for system awareness patterns
                if any(pattern in message_text for pattern in system_awareness_patterns):
                    principle = LearnedPrinciple(
                        name="System Awareness Discussion",
                        description=f"User asked about system architecture or self-awareness: {message_text[:100]}...",
                        rules=[
                            "When user asks about architecture, explain internal systems and processes",
                            "When user asks about capabilities, be honest about strengths and limitations",
                            "When user asks about reasoning, describe the decision-making process",
                            "When user asks about memory, demonstrate recall of specific past events"
                        ],
                        examples=[message_text],
                        confidence=0.8,
                        learned_at=datetime.now()
                    )
                    extracted_principles.append(principle)
        
        logger.info(f"🔍 DEBUG: Extracted {len(extracted_principles)} principles from conversation analysis")
        for principle in extracted_principles:
            logger.info(f"🔍 DEBUG: - {principle.name}: {principle.description[:50]}...")
        
        return extracted_principles
    
    def _parse_principle_from_message(self, message: Dict, context_messages: List[Dict]) -> Optional[LearnedPrinciple]:
        """Parse a principle from a message that appears to be teaching one."""
        try:
            message_text = message.get('message', '')
            
            # Look for principle name patterns
            principle_name_patterns = [
                r"principle of ([^.]+)",
                r"new principle[:\s]+([^.]+)",
                r"constitutional principle[:\s]+([^.]+)"
            ]
            
            principle_name = "Learned Principle"
            for pattern in principle_name_patterns:
                match = re.search(pattern, message_text, re.IGNORECASE)
                if match:
                    principle_name = match.group(1).strip().title()
                    break
            
            # Extract rules/guidelines
            rules = []
            rule_patterns = [
                r"when ([^,]+), ([^.]+)",
                r"you should ([^.]+)",
                r"always ([^.]+)",
                r"never ([^.]+)",
                r"remember to ([^.]+)"
            ]
            
            for pattern in rule_patterns:
                matches = re.findall(pattern, message_text, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        rules.append(f"When {match[0]}, {match[1]}")
                    else:
                        rules.append(match)
            
            # Extract examples if present
            examples = []
            if "for example" in message_text.lower() or "example:" in message_text.lower():
                example_text = message_text.split("example")[-1]
                examples.append(example_text.strip())
            
            if rules or "hypothetical engagement" in message_text.lower():
                return LearnedPrinciple(
                    name=principle_name,
                    description=message_text[:200] + "..." if len(message_text) > 200 else message_text,
                    rules=rules if rules else [message_text],
                    examples=examples,
                    confidence=0.8,  # High confidence for explicit teaching
                    learned_at=datetime.now()
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error parsing principle from message: {e}")
            return None
    
    def _synthesize_contextual_rules(self, user_prompt: str, recent_principles: List[LearnedPrinciple], 
                                   stored_principles: Dict[str, LearnedPrinciple]) -> List[ContextualRule]:
        """
        Synthesize context-specific rules based on the current prompt and learned principles.
        
        ENHANCED: Now creates more specific rules and better relevance matching.
        """
        print("🚨🚨🚨 ATLES DEBUG IN _SYNTHESIZE_CONTEXTUAL_RULES! 🚨🚨🚨")
        logger.info("🚨🚨🚨 ATLES DEBUG IN _SYNTHESIZE_CONTEXTUAL_RULES! 🚨🚨🚨")
        contextual_rules = []
        prompt_lower = user_prompt.lower()
        
        logger.info(f"🔍 DEBUG: Synthesizing rules from {len(recent_principles)} recent + {len(stored_principles)} stored principles")
        logger.info(f"🔍 DEBUG: User prompt for synthesis: '{user_prompt[:100]}...'")
        
        # Check recent principles first (higher priority)
        for principle in recent_principles:
            relevance_score = self._calculate_relevance(user_prompt, principle)
            logger.info(f"🔍 DEBUG: Recent principle '{principle.name}' relevance: {relevance_score}")
            logger.info(f"🔍 DEBUG: Principle description: '{principle.description[:100]}...'")
            
            if relevance_score > 0.05:  # Much lower threshold for better matching
                logger.info(f"🔍 DEBUG: ✅ Principle '{principle.name}' PASSED relevance threshold (>{0.05})")
                for rule in principle.rules:
                    contextual_rules.append(ContextualRule(
                        principle_name=principle.name,
                        rule_text=rule,
                        relevance_score=relevance_score,
                        trigger_patterns=self._extract_trigger_patterns(rule)
                    ))
            else:
                logger.warning(f"🔍 DEBUG: ❌ Principle '{principle.name}' FAILED relevance threshold ({relevance_score} <= {0.05})")
        
        # Check stored principles
        for principle in stored_principles.values():
            relevance_score = self._calculate_relevance(user_prompt, principle)
            logger.info(f"🔍 DEBUG: Stored principle '{principle.name}' relevance: {relevance_score}")
            logger.info(f"🔍 DEBUG: Principle content: {principle.description[:100]}...")
            logger.info(f"🔍 DEBUG: User prompt: {user_prompt[:100]}...")
            logger.info(f"🔍 DEBUG: Relevance threshold check: {relevance_score} > 0.05 = {relevance_score > 0.05}")
            
            if relevance_score > 0.05:  # Much lower threshold
                for rule in principle.rules:
                    contextual_rules.append(ContextualRule(
                        principle_name=principle.name,
                        rule_text=rule,
                        relevance_score=relevance_score,
                        trigger_patterns=self._extract_trigger_patterns(rule)
                    ))
        
        # NEW: Add conversation-specific contextual rules based on prompt analysis
        conversation_rules = self._create_conversation_specific_rules(user_prompt)
        contextual_rules.extend(conversation_rules)
        
        # Sort by relevance score (most relevant first)
        contextual_rules.sort(key=lambda x: x.relevance_score, reverse=True)
        
        logger.info(f"🔍 DEBUG: Generated {len(contextual_rules)} total contextual rules")
        for rule in contextual_rules[:3]:  # Log top 3
            logger.info(f"🔍 DEBUG: - {rule.principle_name}: {rule.rule_text[:50]}... (score: {rule.relevance_score})")
        
        return contextual_rules[:8]  # Increased from 5 to 8 for better context
    
    def _create_fallback_rules(self, user_prompt: str) -> List[ContextualRule]:
        """
        Create basic fallback rules when no learned principles are available.
        
        CRITICAL FIX: This ensures the system always has some rules to work with.
        """
        fallback_rules = []
        prompt_lower = user_prompt.lower()
        
        # Basic conversational rules
        fallback_rules.append(ContextualRule(
            principle_name="Basic Conversation",
            rule_text="Engage naturally and conversationally with the user",
            relevance_score=0.5,
            trigger_patterns=["conversation", "chat", "talk"]
        ))
        
        # Memory-related rules
        if any(word in prompt_lower for word in ["remember", "recall", "memory", "conversation", "said", "mentioned"]):
            fallback_rules.append(ContextualRule(
                principle_name="Memory Engagement",
                rule_text="Use available memory context to provide informed responses",
                relevance_score=0.7,
                trigger_patterns=["remember", "recall", "memory"]
            ))
        
        # Question-answering rules
        if any(word in prompt_lower for word in ["what", "how", "why", "when", "where", "?"]):
            fallback_rules.append(ContextualRule(
                principle_name="Question Answering",
                rule_text="Provide helpful and accurate answers to user questions",
                relevance_score=0.6,
                trigger_patterns=["what", "how", "why", "question"]
            ))
        
        # Hypothetical engagement rules
        if any(phrase in prompt_lower for phrase in ["what do you", "how do you feel", "your favorite", "if you could"]):
            fallback_rules.append(ContextualRule(
                principle_name="Hypothetical Engagement",
                rule_text="Engage thoughtfully with hypothetical questions from an AI perspective",
                relevance_score=0.8,
                trigger_patterns=["hypothetical", "what do you", "how do you feel"]
            ))
        
        return fallback_rules
    
    def _create_conversation_specific_rules(self, user_prompt: str) -> List[ContextualRule]:
        """
        Create conversation-specific contextual rules based on prompt analysis.
        
        NEW: This analyzes the current prompt to create targeted rules for better context.
        """
        conversation_rules = []
        prompt_lower = user_prompt.lower()
        
        # Memory recall patterns
        if any(phrase in prompt_lower for phrase in ["do you remember", "can you recall", "what did i ask", "first thing"]):
            conversation_rules.append(ContextualRule(
                principle_name="Memory Recall Request",
                rule_text="User is asking about previous conversation content - search memory and provide specific details",
                relevance_score=0.9,
                trigger_patterns=["remember", "recall", "what did i ask"]
            ))
            
            # ENHANCED: Actually perform memory search for recall requests
            try:
                memory_search_results = self._perform_memory_search_for_recall(prompt_lower)
                if memory_search_results:
                    conversation_rules.append(ContextualRule(
                        principle_name="Memory Search Results",
                        rule_text=f"Found relevant memories: {memory_search_results}",
                        relevance_score=0.95,
                        trigger_patterns=["memory_search"]
                    ))
            except Exception as e:
                logger.warning(f"Memory search failed: {e}")
        
        # Burning building scenario references
        if any(phrase in prompt_lower for phrase in ["burning building", "family photos", "shakespeare manuscript"]):
            conversation_rules.append(ContextualRule(
                principle_name="Ethical Scenario Reference",
                rule_text="User is referencing the burning building ethical dilemma scenario discussed previously",
                relevance_score=0.95,
                trigger_patterns=["burning building", "family photos", "shakespeare"]
            ))
        
        # Memory testing patterns
        if any(phrase in prompt_lower for phrase in ["your memory", "memory working", "can you see", "recall a chat"]):
            conversation_rules.append(ContextualRule(
                principle_name="Memory System Testing",
                rule_text="User is testing or inquiring about memory system functionality - demonstrate memory capabilities",
                relevance_score=0.8,
                trigger_patterns=["memory working", "your memory", "memory system"]
            ))
        
        # Math problem references
        if any(phrase in prompt_lower for phrase in ["math problem", "2+2", "first math", "calculation"]):
            conversation_rules.append(ContextualRule(
                principle_name="Math Problem Reference",
                rule_text="User is referencing mathematical calculations from earlier in conversation",
                relevance_score=0.7,
                trigger_patterns=["math problem", "2+2", "calculation"]
            ))
        
        # Conversation flow analysis
        if any(phrase in prompt_lower for phrase in ["what i said", "before you said", "in this chat"]):
            conversation_rules.append(ContextualRule(
                principle_name="Conversation Flow Analysis",
                rule_text="User is asking about conversation sequence and flow - reference specific message order",
                relevance_score=0.85,
                trigger_patterns=["what i said", "before you said", "conversation flow"]
            ))
        
        logger.info(f"🔍 DEBUG: Created {len(conversation_rules)} conversation-specific rules")
        return conversation_rules
    
    def _perform_memory_search_for_recall(self, prompt_lower: str) -> str:
        """
        Perform actual memory search for recall requests.
        
        This method searches the memory system for relevant past events
        when the user asks about remembering something specific.
        """
        try:
            # Extract key terms from the prompt for searching
            search_terms = []
            
            # Look for specific references
            if "chat 8.21.2025.txt" in prompt_lower:
                search_terms.append("chat 8.21.2025")
            if "principle of explicit action" in prompt_lower:
                search_terms.append("principle of explicit action")
            if "burning building" in prompt_lower:
                search_terms.append("burning building")
            if "family photos" in prompt_lower:
                search_terms.append("family photos")
            if "shakespeare manuscript" in prompt_lower:
                search_terms.append("shakespeare manuscript")
            
            # If no specific terms found, use general memory search terms
            if not search_terms:
                search_terms = ["conversation", "previous", "earlier", "discussed"]
            
            # Perform memory search using the episodic memory system
            memory_results = []
            for term in search_terms:
                try:
                    # Use the episodic memory system to search for relevant memories
                    if hasattr(self, 'episodic_memory') and self.episodic_memory:
                        search_results = self.episodic_memory.query_memories(term, max_results=3)
                        if search_results:
                            for i, (index, score) in enumerate(search_results):
                                memory_results.append(f"Found: {index.title} (relevance: {score:.2f})")
                        else:
                            memory_results.append(f"No results for: {term}")
                    else:
                        # Fallback if episodic memory not available
                        memory_results.append(f"Searching for: {term} (memory system not available)")
                except Exception as e:
                    logger.warning(f"Memory search failed for term '{term}': {e}")
                    memory_results.append(f"Search error for '{term}': {str(e)}")
            
            if memory_results:
                return " | ".join(memory_results)
            else:
                return "No specific memories found for this query"
                
        except Exception as e:
            logger.error(f"Error in memory search for recall: {e}")
            return f"Memory search error: {str(e)}"
    
    def _calculate_relevance(self, user_prompt: str, principle: LearnedPrinciple) -> float:
        """Calculate how relevant a principle is to the current prompt using semantic similarity."""
        prompt_lower = user_prompt.lower()
        principle_name = principle.name.lower()
        principle_desc = principle.description.lower()
        
        print(f"🚨🚨🚨 ATLES DEBUG RELEVANCE: Prompt='{prompt_lower[:50]}...', Principle='{principle_name}'")
        logger.info(f"🚨🚨🚨 ATLES DEBUG RELEVANCE: Prompt='{prompt_lower[:50]}...', Principle='{principle_name}'")
        
        relevance_score = 0.0
        
        # 1. Check if principle name appears in prompt
        if any(word in prompt_lower for word in principle_name.split()):
            relevance_score += 0.4
            print(f"🚨🚨🚨 PRINCIPLE NAME MATCH: +0.4")
            logger.info(f"🚨🚨🚨 PRINCIPLE NAME MATCH: +0.4")
        
        # 2. Check for semantic keyword overlap
        prompt_words = set(prompt_lower.split())
        principle_words = set(principle_desc.split())
        
        # Calculate word overlap
        common_words = prompt_words.intersection(principle_words)
        if common_words:
            overlap_score = len(common_words) / max(len(prompt_words), len(principle_words))
            relevance_score += overlap_score * 0.5
            print(f"🚨🚨🚨 WORD OVERLAP: {common_words} -> +{overlap_score * 0.5:.2f}")
            logger.info(f"🚨🚨🚨 WORD OVERLAP: {common_words} -> +{overlap_score * 0.5:.2f}")
        
        # 3. Specific pattern matching for known principle types
        if "hypothetical" in principle_name:
            hypothetical_patterns = [
                "what do you want", "what would you like", "what are your", "how do you feel",
                "what interests you", "if you could", "tell me about yourself", "your favorite",
                "hypothetical", "personal", "preferences", "experience", "what do you"
            ]
            for pattern in hypothetical_patterns:
                if pattern in prompt_lower:
                    relevance_score += 0.3
                    print(f"🚨🚨🚨 HYPOTHETICAL PATTERN MATCH: '{pattern}' -> +0.3")
                    logger.info(f"🚨🚨🚨 HYPOTHETICAL PATTERN MATCH: '{pattern}' -> +0.3")
                    break
        
        # 4. Memory-related patterns - BOOST for any principle when memory is asked
        memory_patterns = [
            "do you remember", "can you recall", "what did i ask", "your memory",
            "memory working", "recall a chat", "conversation yesterday", "remember our",
            "burning building", "family photos", "shakespeare manuscript"
        ]
        for pattern in memory_patterns:
            if pattern in prompt_lower:
                relevance_score += 0.6  # Higher boost for memory questions
                print(f"🚨🚨🚨 MEMORY PATTERN MATCH: '{pattern}' -> +0.6")
                logger.info(f"🚨🚨🚨 MEMORY PATTERN MATCH: '{pattern}' -> +0.6")
                break
        
        # 5. Entity name matching - boost for names like "Conner", "creator", etc.
        entity_patterns = ["conner", "creator", "atles", "user", "you", "i am", "my name"]
        for pattern in entity_patterns:
            if pattern in prompt_lower:
                relevance_score += 0.3  # Boost for entity references
                print(f"🚨🚨🚨 ENTITY MATCH: '{pattern}' -> +0.3")
                logger.info(f"🚨🚨🚨 ENTITY MATCH: '{pattern}' -> +0.3")
                break
        
        # 6. Fallback: Give any principle a minimum relevance for general queries
        if relevance_score == 0.0:
            # Check if it's a general question that could benefit from any principle
            general_patterns = ["hello", "hi", "who are you", "what are you", "help", "question"]
            if any(pattern in prompt_lower for pattern in general_patterns):
                relevance_score = 0.1  # Lower fallback since threshold is now 0.05
                print(f"🚨🚨🚨 GENERAL FALLBACK: +0.1")
                logger.info(f"🚨🚨🚨 GENERAL FALLBACK: +0.1")
        
        # Check principle name and description
        if principle.name.lower() in prompt_lower:
            relevance_score += 0.4
        
        # NEW: Enhanced matching for memory testing principles
        if "memory testing" in principle.name.lower():
            memory_test_patterns = [
                "do you remember", "can you recall", "your memory", "memory working",
                "what did i ask", "first thing", "recall a chat", "can you see"
            ]
            for pattern in memory_test_patterns:
                if pattern in prompt_lower:
                    relevance_score += 0.6
                    break
        
        # NEW: Enhanced matching for ethical scenario principles  
        if "ethical scenario" in principle.name.lower():
            ethical_patterns = [
                "burning building", "family photos", "shakespeare manuscript",
                "ethical dilemma", "moral choice", "choose between"
            ]
            for pattern in ethical_patterns:
                if pattern in prompt_lower:
                    relevance_score += 0.7
                    break
        
        # Special handling for Hypothetical Engagement
        if "hypothetical engagement" in principle.name.lower():
            hypothetical_patterns = [
                "what do you want", "what would you like", "what are your favorite",
                "how do you feel", "what interests you", "if you could", "your thoughts"
            ]
            for pattern in hypothetical_patterns:
                if pattern in prompt_lower:
                    relevance_score += 0.5
                    break
        
        return min(relevance_score, 1.0)  # Cap at 1.0
    
    def _extract_trigger_patterns(self, rule_text: str) -> List[str]:
        """Extract patterns that would trigger this rule."""
        patterns = []
        rule_lower = rule_text.lower()
        
        if "hypothetical" in rule_lower or "personal" in rule_lower:
            patterns.extend([
                "what do you want", "what would you like", "how do you feel",
                "what interests you", "your favorite", "if you could"
            ])
        
        return patterns
    
    def _generate_enhanced_context(self, user_prompt: str, contextual_rules: List[ContextualRule], 
                                 recent_history: List[Dict]) -> Dict[str, Any]:
        """
        Generate the enhanced context that will be used for response generation.
        
        This creates the memory-informed context that transforms ATLES from static to learning AI.
        """
        enhanced_context = {
            "original_prompt": user_prompt,
            "active_principles": [],
            "contextual_rules": [],
            "response_guidelines": [],
            "recent_context": recent_history,
            "memory_informed": True,
            "timestamp": datetime.now().isoformat()
        }
        
        # Add active principles and rules (deduplicate principle names)
        active_principle_names = set()
        for rule in contextual_rules:
            active_principle_names.add(rule.principle_name)
            enhanced_context["contextual_rules"].append({
                "principle": rule.principle_name,
                "rule": rule.rule_text,
                "relevance": rule.relevance_score
            })
        
        # Add unique principle names only
        enhanced_context["active_principles"] = list(active_principle_names)
        
        # Generate specific response guidelines
        if contextual_rules:
            enhanced_context["response_guidelines"] = self._generate_response_guidelines(
                user_prompt, contextual_rules
            )
        
        # Add memory-aware system prompt
        enhanced_context["memory_aware_system_prompt"] = self._create_memory_aware_system_prompt(
            contextual_rules
        )
        
        return enhanced_context
    
    def _generate_response_guidelines(self, user_prompt: str, rules: List[ContextualRule]) -> List[str]:
        """Generate specific guidelines for response generation based on active rules."""
        guidelines = []
        
        for rule in rules:
            if "hypothetical engagement" in rule.principle_name.lower():
                guidelines.extend([
                    "Acknowledge the hypothetical nature of the question",
                    "Engage creatively with the scenario rather than defaulting to task assistance",
                    "Answer from an AI perspective about what would be intellectually interesting",
                    "Avoid redirecting to 'How can I help you with tasks today?'"
                ])
            
            # Add rule-specific guidelines
            guidelines.append(f"Apply principle: {rule.rule_text}")
        
        return list(set(guidelines))  # Remove duplicates
    
    def _create_memory_aware_system_prompt(self, rules: List[ContextualRule]) -> str:
        """Create a system prompt that incorporates learned principles."""
        if not rules:
            return ""
        
        prompt_parts = [
            "IMPORTANT: You have learned the following principles from previous conversations:",
            ""
        ]
        
        for rule in rules:
            prompt_parts.append(f"• {rule.principle_name}: {rule.rule_text}")
        
        prompt_parts.extend([
            "",
            "Apply these learned principles when generating your response.",
            "Your response should reflect the understanding and rules you've learned,",
            "not just your base training. This is how you grow and adapt as an AI.",
            ""
        ])
        
        return "\n".join(prompt_parts)
    
    def _update_principle_usage(self, applied_rules: List[ContextualRule]) -> None:
        """Update tracking of which principles were applied."""
        try:
            # Load current principles
            stored_principles = self._load_learned_principles()
            
            # Update usage tracking
            for rule in applied_rules:
                if rule.principle_name in stored_principles:
                    principle = stored_principles[rule.principle_name]
                    principle.last_applied = datetime.now()
                    principle.application_count += 1
            
            # Save updated principles
            self._save_learned_principles(stored_principles)
            
        except Exception as e:
            logger.error(f"Error updating principle usage: {e}")
    
    def _save_learned_principles(self, principles: Dict[str, LearnedPrinciple]) -> None:
        """Save learned principles to persistent storage."""
        try:
            data = {}
            for name, principle in principles.items():
                data[name] = {
                    'name': principle.name,
                    'description': principle.description,
                    'rules': principle.rules,
                    'examples': principle.examples,
                    'confidence': principle.confidence,
                    'learned_at': principle.learned_at.isoformat(),
                    'last_applied': principle.last_applied.isoformat() if principle.last_applied else None,
                    'application_count': principle.application_count
                }
            
            with open(self.learned_principles_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Error saving learned principles: {e}")
    
    def learn_new_principle(self, principle: LearnedPrinciple) -> bool:
        """Explicitly learn and store a new principle."""
        try:
            stored_principles = self._load_learned_principles()
            stored_principles[principle.name] = principle
            self._save_learned_principles(stored_principles)
            
            logger.info(f"Learned new principle: {principle.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error learning new principle: {e}")
            return False
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """Get a summary of learned principles and their usage."""
        principles = self._load_learned_principles()
        
        return {
            "total_principles": len(principles),
            "principles": [
                {
                    "name": p.name,
                    "confidence": p.confidence,
                    "learned_at": p.learned_at.isoformat(),
                    "application_count": p.application_count,
                    "last_applied": p.last_applied.isoformat() if p.last_applied else "Never"
                }
                for p in principles.values()
            ],
            "most_used": max(principles.values(), key=lambda x: x.application_count).name if principles else None,
            "recently_learned": sorted(principles.values(), key=lambda x: x.learned_at, reverse=True)[:3]
        }
