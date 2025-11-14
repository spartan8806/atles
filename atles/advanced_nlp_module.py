"""
ATLES Advanced NLP Module

Enhanced natural language processing capabilities including:
- Context-aware intent detection
- Sentiment and emotion analysis
- Topic modeling and extraction
- Conversation flow analysis
- Multi-turn dialogue understanding
"""

import re
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class IntentType(Enum):
    """Types of user intents we can detect."""
    QUESTION = "question"
    REQUEST = "request"
    COMMAND = "command"
    CONVERSATION = "conversation"
    CLARIFICATION = "clarification"
    FEEDBACK = "feedback"
    GREETING = "greeting"
    GOODBYE = "goodbye"

class SentimentType(Enum):
    """Sentiment analysis results."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"

@dataclass
class NLPAnalysis:
    """Complete NLP analysis of user input."""
    text: str
    intent: IntentType
    sentiment: SentimentType
    confidence: float
    topics: List[str]
    entities: List[Dict[str, Any]]
    context_clues: List[str]
    conversation_markers: List[str]
    urgency_level: int  # 1-5 scale
    complexity_score: float

@dataclass
class ConversationContext:
    """Context tracking for multi-step conversations."""
    conversation_id: str
    turn_count: int
    topic_history: List[str]
    intent_history: List[IntentType]
    unresolved_questions: List[str]
    context_stack: List[Dict[str, Any]]
    user_preferences: Dict[str, Any]
    last_updated: datetime

class AdvancedNLPModule:
    """
    Enhanced NLP capabilities for ATLES.
    
    This module provides sophisticated natural language understanding
    that goes beyond basic text processing to understand context,
    intent, sentiment, and conversation flow.
    """
    
    def __init__(self):
        self.conversation_contexts = {}
        self.intent_patterns = self._initialize_intent_patterns()
        self.sentiment_indicators = self._initialize_sentiment_indicators()
        self.topic_keywords = self._initialize_topic_keywords()
        
    def analyze_input(self, text: str, conversation_id: str = None) -> NLPAnalysis:
        """
        Perform comprehensive NLP analysis on user input.
        
        Args:
            text: User input text
            conversation_id: Optional conversation identifier for context
            
        Returns:
            Complete NLP analysis results
        """
        try:
            # Get or create conversation context
            context = self._get_conversation_context(conversation_id)
            
            # Perform analysis
            intent = self._detect_intent(text, context)
            sentiment = self._analyze_sentiment(text)
            topics = self._extract_topics(text)
            entities = self._extract_entities(text)
            context_clues = self._find_context_clues(text, context)
            conversation_markers = self._find_conversation_markers(text)
            urgency = self._assess_urgency(text)
            complexity = self._calculate_complexity(text)
            
            # Calculate overall confidence
            confidence = self._calculate_confidence(intent, sentiment, topics, entities)
            
            # Update conversation context
            self._update_context(context, intent, topics, text)
            
            return NLPAnalysis(
                text=text,
                intent=intent,
                sentiment=sentiment,
                confidence=confidence,
                topics=topics,
                entities=entities,
                context_clues=context_clues,
                conversation_markers=conversation_markers,
                urgency_level=urgency,
                complexity_score=complexity
            )
            
        except Exception as e:
            logger.error(f"NLP analysis failed: {e}")
            # Return basic analysis as fallback
            return NLPAnalysis(
                text=text,
                intent=IntentType.CONVERSATION,
                sentiment=SentimentType.NEUTRAL,
                confidence=0.5,
                topics=[],
                entities=[],
                context_clues=[],
                conversation_markers=[],
                urgency_level=3,
                complexity_score=0.5
            )
    
    def _initialize_intent_patterns(self) -> Dict[IntentType, List[str]]:
        """Initialize patterns for intent detection."""
        return {
            IntentType.QUESTION: [
                r"^(what|how|why|when|where|who|which|can|could|would|should|is|are|do|does|did)",
                r"\?$",
                r"(tell me|explain|help me understand)",
                r"(i don't understand|i'm confused|unclear)"
            ],
            IntentType.REQUEST: [
                r"(please|could you|would you|can you|i need|i want|i would like)",
                r"(help me|assist me|show me|give me)",
                r"(create|make|build|generate|write)"
            ],
            IntentType.COMMAND: [
                r"^(run|execute|start|stop|open|close|delete|remove|install)",
                r"(do this|go ahead|proceed|continue)",
                r"(now|immediately|right away)"
            ],
            IntentType.CONVERSATION: [
                r"(i think|i believe|in my opinion|it seems)",
                r"(that's interesting|good point|i see)",
                r"(by the way|speaking of|that reminds me)"
            ],
            IntentType.CLARIFICATION: [
                r"(what do you mean|can you clarify|i don't follow)",
                r"(are you saying|do you mean|so you're telling me)",
                r"(wait|hold on|let me understand)"
            ],
            IntentType.FEEDBACK: [
                r"(that worked|that didn't work|good job|well done)",
                r"(that's wrong|that's not right|incorrect)",
                r"(thank you|thanks|appreciate it|helpful)"
            ],
            IntentType.GREETING: [
                r"^(hello|hi|hey|good morning|good afternoon|good evening)",
                r"(how are you|how's it going|what's up)"
            ],
            IntentType.GOODBYE: [
                r"(goodbye|bye|see you|talk to you later|have a good)",
                r"(that's all|i'm done|finished|end)"
            ]
        }
    
    def _initialize_sentiment_indicators(self) -> Dict[SentimentType, List[str]]:
        """Initialize sentiment analysis indicators."""
        return {
            SentimentType.POSITIVE: [
                "good", "great", "excellent", "amazing", "wonderful", "fantastic",
                "love", "like", "enjoy", "happy", "pleased", "satisfied",
                "thank", "thanks", "appreciate", "helpful", "useful", "perfect"
            ],
            SentimentType.NEGATIVE: [
                "bad", "terrible", "awful", "horrible", "hate", "dislike",
                "frustrated", "annoyed", "angry", "disappointed", "confused",
                "wrong", "error", "problem", "issue", "broken", "failed"
            ],
            SentimentType.NEUTRAL: [
                "okay", "fine", "alright", "normal", "standard", "regular",
                "maybe", "perhaps", "possibly", "might", "could", "would"
            ]
        }
    
    def _initialize_topic_keywords(self) -> Dict[str, List[str]]:
        """Initialize topic detection keywords."""
        return {
            "programming": ["code", "function", "variable", "class", "method", "algorithm", "debug", "syntax"],
            "system": ["computer", "system", "hardware", "software", "performance", "memory", "cpu"],
            "ai_ml": ["ai", "artificial intelligence", "machine learning", "neural network", "model", "training"],
            "web": ["website", "html", "css", "javascript", "browser", "url", "http", "api"],
            "data": ["database", "sql", "data", "analysis", "statistics", "visualization", "chart"],
            "security": ["security", "password", "encryption", "authentication", "vulnerability", "hack"],
            "help": ["help", "assistance", "support", "guide", "tutorial", "documentation", "explain"],
            "upgrade": ["upgrade", "improvement", "enhancement", "feature", "update", "new", "add"]
        }
    
    def _detect_intent(self, text: str, context: ConversationContext) -> IntentType:
        """Detect user intent from text and context."""
        text_lower = text.lower().strip()
        
        # Check each intent type
        for intent_type, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return intent_type
        
        # Context-based intent detection
        if context and context.intent_history:
            last_intent = context.intent_history[-1]
            if last_intent == IntentType.QUESTION and not text.endswith('?'):
                return IntentType.CLARIFICATION
        
        # Default to conversation
        return IntentType.CONVERSATION
    
    def _analyze_sentiment(self, text: str) -> SentimentType:
        """Analyze sentiment of the text."""
        text_lower = text.lower()
        
        positive_score = sum(1 for word in self.sentiment_indicators[SentimentType.POSITIVE] if word in text_lower)
        negative_score = sum(1 for word in self.sentiment_indicators[SentimentType.NEGATIVE] if word in text_lower)
        
        if positive_score > negative_score:
            return SentimentType.POSITIVE
        elif negative_score > positive_score:
            return SentimentType.NEGATIVE
        elif positive_score > 0 and negative_score > 0:
            return SentimentType.MIXED
        else:
            return SentimentType.NEUTRAL
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics from text."""
        text_lower = text.lower()
        detected_topics = []
        
        for topic, keywords in self.topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_topics.append(topic)
        
        return detected_topics
    
    def _extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract entities (simplified implementation)."""
        entities = []
        
        # File paths
        file_matches = re.findall(r'[a-zA-Z0-9_/\\.-]+\.[a-zA-Z]{2,4}', text)
        for match in file_matches:
            entities.append({"type": "file", "value": match})
        
        # URLs
        url_matches = re.findall(r'https?://[^\s]+', text)
        for match in url_matches:
            entities.append({"type": "url", "value": match})
        
        # Numbers
        number_matches = re.findall(r'\b\d+\b', text)
        for match in number_matches:
            entities.append({"type": "number", "value": int(match)})
        
        return entities
    
    def _find_context_clues(self, text: str, context: ConversationContext) -> List[str]:
        """Find context clues that reference previous conversation."""
        clues = []
        text_lower = text.lower()
        
        context_indicators = [
            "that", "this", "it", "they", "them", "those", "these",
            "the one", "the thing", "what you said", "your suggestion",
            "earlier", "before", "previously", "last time", "again"
        ]
        
        for indicator in context_indicators:
            if indicator in text_lower:
                clues.append(indicator)
        
        return clues
    
    def _find_conversation_markers(self, text: str) -> List[str]:
        """Find markers that indicate conversation flow."""
        markers = []
        text_lower = text.lower()
        
        flow_markers = {
            "continuation": ["also", "and", "furthermore", "additionally", "moreover"],
            "contrast": ["but", "however", "although", "nevertheless", "on the other hand"],
            "conclusion": ["so", "therefore", "thus", "in conclusion", "finally"],
            "example": ["for example", "for instance", "such as", "like"],
            "clarification": ["in other words", "that is", "specifically", "namely"]
        }
        
        for marker_type, words in flow_markers.items():
            for word in words:
                if word in text_lower:
                    markers.append(f"{marker_type}:{word}")
        
        return markers
    
    def _assess_urgency(self, text: str) -> int:
        """Assess urgency level (1-5 scale)."""
        text_lower = text.lower()
        
        urgent_indicators = ["urgent", "emergency", "asap", "immediately", "right now", "critical", "important"]
        moderate_indicators = ["soon", "quickly", "fast", "please help", "need"]
        
        if any(indicator in text_lower for indicator in urgent_indicators):
            return 5
        elif any(indicator in text_lower for indicator in moderate_indicators):
            return 4
        elif "?" in text:
            return 3
        else:
            return 2
    
    def _calculate_complexity(self, text: str) -> float:
        """Calculate complexity score based on text characteristics."""
        # Simple complexity metrics
        word_count = len(text.split())
        sentence_count = len(re.split(r'[.!?]+', text))
        avg_word_length = sum(len(word) for word in text.split()) / max(word_count, 1)
        
        # Normalize to 0-1 scale
        complexity = min(1.0, (word_count / 100 + sentence_count / 10 + avg_word_length / 10) / 3)
        return complexity
    
    def _calculate_confidence(self, intent: IntentType, sentiment: SentimentType, 
                           topics: List[str], entities: List[Dict[str, Any]]) -> float:
        """Calculate overall confidence in the analysis."""
        confidence = 0.5  # Base confidence
        
        # Boost confidence based on detected elements
        if topics:
            confidence += 0.2
        if entities:
            confidence += 0.1
        if intent != IntentType.CONVERSATION:
            confidence += 0.1
        if sentiment != SentimentType.NEUTRAL:
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def _get_conversation_context(self, conversation_id: str) -> ConversationContext:
        """Get or create conversation context."""
        if not conversation_id:
            conversation_id = f"conv_{datetime.now().timestamp()}"
        
        if conversation_id not in self.conversation_contexts:
            self.conversation_contexts[conversation_id] = ConversationContext(
                conversation_id=conversation_id,
                turn_count=0,
                topic_history=[],
                intent_history=[],
                unresolved_questions=[],
                context_stack=[],
                user_preferences={},
                last_updated=datetime.now()
            )
        
        return self.conversation_contexts[conversation_id]
    
    def _update_context(self, context: ConversationContext, intent: IntentType, 
                       topics: List[str], text: str):
        """Update conversation context with new information."""
        context.turn_count += 1
        context.intent_history.append(intent)
        context.topic_history.extend(topics)
        context.last_updated = datetime.now()
        
        # Track unresolved questions
        if intent == IntentType.QUESTION and "?" in text:
            context.unresolved_questions.append(text)
        
        # Limit history size
        if len(context.intent_history) > 20:
            context.intent_history = context.intent_history[-20:]
        if len(context.topic_history) > 50:
            context.topic_history = context.topic_history[-50:]
    
    def get_conversation_summary(self, conversation_id: str) -> Dict[str, Any]:
        """Get a summary of the conversation context."""
        if conversation_id not in self.conversation_contexts:
            return {"error": "Conversation not found"}
        
        context = self.conversation_contexts[conversation_id]
        
        # Calculate topic frequency
        topic_counts = {}
        for topic in context.topic_history:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        return {
            "conversation_id": conversation_id,
            "turn_count": context.turn_count,
            "duration": (datetime.now() - context.last_updated).total_seconds(),
            "main_topics": sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            "recent_intents": context.intent_history[-5:],
            "unresolved_questions": len(context.unresolved_questions),
            "last_updated": context.last_updated.isoformat()
        }

