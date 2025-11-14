"""
ATLES Machine Learning System - Phase 2

Implements advanced learning capabilities:
- Conversation Pattern Learning
- Response Quality Improvement  
- Adaptive Response Generation
"""

import asyncio
import logging
import json
import numpy as np
from typing import Dict, List, Optional, Any, Tuple, Union
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import sqlite3
from dataclasses import dataclass, asdict
import pickle
import hashlib

logger = logging.getLogger(__name__)


@dataclass
class LearningPattern:
    """Represents a learned conversation pattern."""
    
    pattern_id: str
    user_intent: str
    context_conditions: Dict[str, Any]
    successful_responses: List[str]
    success_rate: float
    usage_count: int
    last_used: float
    metadata: Dict[str, Any]


@dataclass
class QualityMetric:
    """Represents response quality metrics."""
    
    response_id: str
    session_id: str
    user_message: str
    ai_response: str
    user_feedback: Optional[float]  # 0.0 to 1.0
    implicit_feedback: float  # Calculated from conversation flow
    quality_score: float
    improvement_suggestions: List[str]
    timestamp: float
    metadata: Dict[str, Any]


@dataclass
class AdaptiveContext:
    """Context for adaptive response generation."""
    
    user_id: str
    conversation_history: List[Dict[str, Any]]
    learned_patterns: List[LearningPattern]
    quality_history: List[QualityMetric]
    user_preferences: Dict[str, Any]
    context_embeddings: Dict[str, List[float]]


class ConversationPatternLearner:
    """
    Learns and tracks successful conversation patterns.
    
    Identifies what works best in different contexts and user interactions.
    """
    
    def __init__(self, learning_dir: Optional[Path] = None):
        """Initialize the pattern learner."""
        if learning_dir is None:
            learning_dir = Path.home() / ".atles" / "learning"
        
        self.learning_dir = Path(learning_dir)
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        
        self.patterns_file = self.learning_dir / "learned_patterns.pkl"
        self.patterns: Dict[str, LearningPattern] = self._load_patterns()
        
        # Pattern matching thresholds
        self.similarity_threshold = 0.7
        self.min_success_rate = 0.6
        self.min_usage_count = 3
        
        logger.info(f"Conversation Pattern Learner initialized at {self.learning_dir}")
    
    def _load_patterns(self) -> Dict[str, LearningPattern]:
        """Load learned patterns from disk."""
        try:
            if self.patterns_file.exists():
                with open(self.patterns_file, 'rb') as f:
                    return pickle.load(f)
        except Exception as e:
            logger.error(f"Failed to load patterns: {e}")
        
        return {}
    
    def _save_patterns(self):
        """Save learned patterns to disk."""
        try:
            with open(self.patterns_file, 'wb') as f:
                pickle.dump(self.patterns, f)
            logger.debug("Patterns saved successfully")
        except Exception as e:
            logger.error(f"Failed to save patterns: {e}")
    
    def _generate_pattern_id(self, user_intent: str, context: Dict[str, Any]) -> str:
        """Generate unique pattern ID."""
        context_str = json.dumps(context, sort_keys=True)
        combined = f"{user_intent}:{context_str}"
        return hashlib.md5(combined.encode()).hexdigest()[:12]
    
    async def learn_from_interaction(
        self,
        user_message: str,
        ai_response: str,
        user_feedback: Optional[float],
        context: Dict[str, Any],
        success_indicator: bool = True
    ) -> str:
        """
        Learn from a user-AI interaction.
        
        Args:
            user_message: User's input message
            ai_response: AI's response
            user_feedback: Explicit user feedback (0.0 to 1.0)
            context: Conversation context
            success_indicator: Whether the interaction was successful
            
        Returns:
            Pattern ID if learned, empty string otherwise
        """
        try:
            # Extract user intent
            user_intent = await self._extract_user_intent(user_message)
            
            # Check if pattern already exists
            pattern_id = self._generate_pattern_id(user_intent, context)
            
            if pattern_id in self.patterns:
                # Update existing pattern
                pattern = self.patterns[pattern_id]
                pattern.successful_responses.append(ai_response)
                pattern.usage_count += 1
                pattern.last_used = asyncio.get_event_loop().time()
                
                # Update success rate
                if user_feedback is not None:
                    pattern.success_rate = (pattern.success_rate * (pattern.usage_count - 1) + user_feedback) / pattern.usage_count
                elif success_indicator:
                    pattern.success_rate = (pattern.success_rate * (pattern.usage_count - 1) + 1.0) / pattern.usage_count
                else:
                    pattern.success_rate = (pattern.success_rate * (pattern.usage_count - 1) + 0.0) / pattern.usage_count
                
            else:
                # Create new pattern
                success_rate = user_feedback if user_feedback is not None else (1.0 if success_indicator else 0.0)
                
                pattern = LearningPattern(
                    pattern_id=pattern_id,
                    user_intent=user_intent,
                    context_conditions=context,
                    successful_responses=[ai_response],
                    success_rate=success_rate,
                    usage_count=1,
                    last_used=asyncio.get_event_loop().time(),
                    metadata={
                        "created": datetime.now().isoformat(),
                        "last_updated": datetime.now().isoformat()
                    }
                )
                
                self.patterns[pattern_id] = pattern
            
            # Save patterns
            self._save_patterns()
            
            logger.info(f"Learned pattern {pattern_id} with success rate {pattern.success_rate:.2f}")
            return pattern_id
            
        except Exception as e:
            logger.error(f"Failed to learn from interaction: {e}")
            return ""
    
    async def _extract_user_intent(self, message: str) -> str:
        """Extract user intent from message."""
        message_lower = message.lower()
        
        # Intent classification based on keywords and patterns
        if any(word in message_lower for word in ["help", "how", "what", "explain", "tell me"]):
            return "information_request"
        elif any(word in message_lower for word in ["create", "make", "build", "generate"]):
            return "creation_request"
        elif any(word in message_lower for word in ["fix", "solve", "error", "problem"]):
            return "problem_solving"
        elif any(word in message_lower for word in ["compare", "difference", "vs", "versus"]):
            return "comparison_request"
        elif any(word in message_lower for word in ["thank", "thanks", "appreciate"]):
            return "gratitude"
        elif any(word in message_lower for word in ["bye", "goodbye", "end", "stop"]):
            return "conversation_end"
        else:
            return "general_inquiry"
    
    async def find_best_pattern(
        self,
        user_intent: str,
        context: Dict[str, Any],
        limit: int = 5
    ) -> List[LearningPattern]:
        """
        Find the best patterns for a given intent and context.
        
        Args:
            user_intent: User's intent
            context: Current context
            limit: Maximum number of patterns to return
            
        Returns:
            List of best matching patterns
        """
        try:
            matching_patterns = []
            
            for pattern in self.patterns.values():
                if pattern.user_intent == user_intent:
                    # Calculate context similarity
                    similarity = await self._calculate_context_similarity(
                        pattern.context_conditions, context
                    )
                    
                    if similarity >= self.similarity_threshold:
                        # Calculate pattern score based on success rate and usage
                        pattern_score = pattern.success_rate * np.log(pattern.usage_count + 1)
                        
                        matching_patterns.append((pattern, pattern_score, similarity))
            
            # Sort by pattern score and similarity
            matching_patterns.sort(key=lambda x: (x[1], x[2]), reverse=True)
            
            # Return top patterns
            return [pattern for pattern, _, _ in matching_patterns[:limit]]
            
        except Exception as e:
            logger.error(f"Failed to find best patterns: {e}")
            return []
    
    async def _calculate_context_similarity(
        self,
        pattern_context: Dict[str, Any],
        current_context: Dict[str, Any]
    ) -> float:
        """Calculate similarity between pattern context and current context."""
        try:
            if not pattern_context or not current_context:
                return 0.0
            
            # Simple similarity calculation based on key overlap
            pattern_keys = set(pattern_context.keys())
            current_keys = set(current_context.keys())
            
            if not pattern_keys or not current_keys:
                return 0.0
            
            # Key overlap
            key_overlap = len(pattern_keys & current_keys) / len(pattern_keys | current_keys)
            
            # Value similarity for common keys
            value_similarity = 0.0
            common_keys = pattern_keys & current_keys
            
            for key in common_keys:
                if isinstance(pattern_context[key], (str, int, float)) and isinstance(current_context[key], (str, int, float)):
                    if pattern_context[key] == current_context[key]:
                        value_similarity += 1.0
            
            if common_keys:
                value_similarity /= len(common_keys)
            
            # Combined similarity score
            similarity = (key_overlap * 0.4) + (value_similarity * 0.6)
            
            return min(similarity, 1.0)
            
        except Exception as e:
            logger.error(f"Context similarity calculation failed: {e}")
            return 0.0
    
    async def get_pattern_statistics(self) -> Dict[str, Any]:
        """Get statistics about learned patterns."""
        try:
            if not self.patterns:
                return {"total_patterns": 0}
            
            total_patterns = len(self.patterns)
            total_usage = sum(pattern.usage_count for pattern in self.patterns.values())
            avg_success_rate = np.mean([pattern.success_rate for pattern in self.patterns.values()])
            
            # Intent distribution
            intent_counts = Counter(pattern.user_intent for pattern in self.patterns.values())
            
            # Top performing patterns
            top_patterns = sorted(
                self.patterns.values(),
                key=lambda x: x.success_rate * x.usage_count,
                reverse=True
            )[:5]
            
            return {
                "total_patterns": total_patterns,
                "total_usage": total_usage,
                "average_success_rate": avg_success_rate,
                "intent_distribution": dict(intent_counts),
                "top_patterns": [
                    {
                        "pattern_id": p.pattern_id,
                        "intent": p.user_intent,
                        "success_rate": p.success_rate,
                        "usage_count": p.usage_count
                    }
                    for p in top_patterns
                ]
            }
            
        except Exception as e:
            logger.error(f"Failed to get pattern statistics: {e}")
            return {"error": str(e)}


class ResponseQualityImprover:
    """
    Improves response quality through learning and feedback analysis.
    
    Learns from user feedback and conversation flow to enhance future responses.
    """
    
    def __init__(self, quality_dir: Optional[Path] = None):
        """Initialize the quality improver."""
        if quality_dir is None:
            quality_dir = Path.home() / ".atles" / "quality"
        
        self.quality_dir = Path(quality_dir)
        self.quality_dir.mkdir(parents=True, exist_ok=True)
        
        self.quality_file = self.quality_dir / "quality_metrics.pkl"
        self.quality_metrics: List[QualityMetric] = self._load_quality_metrics()
        
        # Quality thresholds
        self.high_quality_threshold = 0.8
        self.low_quality_threshold = 0.4
        
        logger.info(f"Response Quality Improver initialized at {quality_dir}")
    
    def _load_quality_metrics(self) -> List[QualityMetric]:
        """Load quality metrics from disk."""
        try:
            if self.quality_file.exists():
                with open(self.quality_file, 'rb') as f:
                    return pickle.load(f)
        except Exception as e:
            logger.error(f"Failed to load quality metrics: {e}")
        
        return []
    
    def _save_quality_metrics(self):
        """Save quality metrics to disk."""
        try:
            with open(self.quality_file, 'wb') as f:
                pickle.dump(self.quality_metrics, f)
            logger.debug("Quality metrics saved successfully")
        except Exception as e:
            logger.error(f"Failed to save quality metrics: {e}")
    
    async def record_quality_metric(
        self,
        session_id: str,
        user_message: str,
        ai_response: str,
        user_feedback: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Record a quality metric for response analysis.
        
        Args:
            session_id: Session identifier
            user_message: User's input message
            ai_response: AI's response
            user_feedback: Explicit user feedback (0.0 to 1.0)
            metadata: Additional metadata
            
        Returns:
            Quality metric ID
        """
        try:
            # Calculate implicit feedback from conversation flow
            implicit_feedback = await self._calculate_implicit_feedback(
                user_message, ai_response, metadata or {}
            )
            
            # Calculate overall quality score
            if user_feedback is not None:
                quality_score = (user_feedback * 0.7) + (implicit_feedback * 0.3)
            else:
                quality_score = implicit_feedback
            
            # Generate improvement suggestions
            improvement_suggestions = await self._generate_improvement_suggestions(
                user_message, ai_response, quality_score, metadata or {}
            )
            
            # Create quality metric
            metric_id = hashlib.md5(f"{session_id}:{user_message}:{ai_response}".encode()).hexdigest()[:12]
            
            metric = QualityMetric(
                response_id=metric_id,
                session_id=session_id,
                user_message=user_message,
                ai_response=ai_response,
                user_feedback=user_feedback,
                implicit_feedback=implicit_feedback,
                quality_score=quality_score,
                improvement_suggestions=improvement_suggestions,
                timestamp=asyncio.get_event_loop().time(),
                metadata=metadata or {}
            )
            
            self.quality_metrics.append(metric)
            self._save_quality_metrics()
            
            logger.info(f"Recorded quality metric {metric_id} with score {quality_score:.2f}")
            return metric_id
            
        except Exception as e:
            logger.error(f"Failed to record quality metric: {e}")
            return ""
    
    async def _calculate_implicit_feedback(
        self,
        user_message: str,
        ai_response: str,
        metadata: Dict[str, Any]
    ) -> float:
        """Calculate implicit feedback from conversation flow and metadata."""
        try:
            feedback_score = 0.5  # Base neutral score
            
            # Check response length appropriateness
            user_words = len(user_message.split())
            ai_words = len(ai_response.split())
            
            if user_words > 0:
                length_ratio = ai_words / user_words
                if 0.5 <= length_ratio <= 3.0:
                    feedback_score += 0.2
                elif length_ratio < 0.5:
                    feedback_score -= 0.1
                elif length_ratio > 5.0:
                    feedback_score -= 0.1
            
            # Check for follow-up questions (indicates user engagement)
            if any(word in user_message.lower() for word in ["why", "how", "what", "when", "where"]):
                if len(ai_response) > 50:  # Substantial response
                    feedback_score += 0.1
            
            # Check for user acknowledgment patterns
            if metadata.get("user_acknowledgment", False):
                feedback_score += 0.2
            
            # Check for conversation continuation
            if metadata.get("conversation_continued", True):
                feedback_score += 0.1
            
            # Normalize to 0.0-1.0 range
            return max(0.0, min(1.0, feedback_score))
            
        except Exception as e:
            logger.error(f"Implicit feedback calculation failed: {e}")
            return 0.5
    
    async def _generate_improvement_suggestions(
        self,
        user_message: str,
        ai_response: str,
        quality_score: float,
        metadata: Dict[str, Any]
    ) -> List[str]:
        """Generate suggestions for improving response quality."""
        suggestions = []
        
        try:
            if quality_score < self.low_quality_threshold:
                suggestions.append("Response quality is below acceptable threshold")
                
                # Check response length
                if len(ai_response.split()) < 10:
                    suggestions.append("Consider providing more detailed responses")
                elif len(ai_response.split()) > 100:
                    suggestions.append("Consider making responses more concise")
                
                # Check for specific issues
                if "I don't know" in ai_response or "I can't" in ai_response:
                    suggestions.append("Provide alternative solutions or suggestions")
                
                if not any(word in ai_response.lower() for word in ["because", "reason", "example", "specifically"]):
                    suggestions.append("Include explanations or examples")
            
            elif quality_score < self.high_quality_threshold:
                suggestions.append("Response quality could be improved")
                
                # Suggest enhancements
                if metadata.get("user_topics"):
                    suggestions.append("Consider addressing specific user topics more directly")
                
                if metadata.get("conversation_context"):
                    suggestions.append("Leverage conversation context for more relevant responses")
            
            # Add general improvement suggestions
            if not suggestions:
                suggestions.append("Maintain current response quality")
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Improvement suggestion generation failed: {e}")
            return ["Error generating suggestions"]
    
    async def get_quality_insights(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Get insights about response quality."""
        try:
            if not self.quality_metrics:
                return {"total_metrics": 0}
            
            # Filter by session if specified
            metrics = [m for m in self.quality_metrics if not session_id or m.session_id == session_id]
            
            if not metrics:
                return {"total_metrics": 0, "session_id": session_id}
            
            total_metrics = len(metrics)
            avg_quality = np.mean([m.quality_score for m in metrics])
            
            # Quality distribution
            high_quality = len([m for m in metrics if m.quality_score >= self.high_quality_threshold])
            medium_quality = len([m for m in metrics if self.low_quality_threshold <= m.quality_score < self.high_quality_threshold])
            low_quality = len([m for m in metrics if m.quality_score < self.low_quality_threshold])
            
            # Common improvement suggestions
            all_suggestions = []
            for metric in metrics:
                all_suggestions.extend(metric.improvement_suggestions)
            
            suggestion_counts = Counter(all_suggestions)
            top_suggestions = suggestion_counts.most_common(5)
            
            return {
                "total_metrics": total_metrics,
                "average_quality": avg_quality,
                "quality_distribution": {
                    "high": high_quality,
                    "medium": medium_quality,
                    "low": low_quality
                },
                "top_improvement_suggestions": top_suggestions,
                "session_id": session_id
            }
            
        except Exception as e:
            logger.error(f"Failed to get quality insights: {e}")
            return {"error": str(e)}


class AdaptiveResponseGenerator:
    """
    Generates adaptive responses based on learned patterns and context.
    
    Adjusts response style, content, and approach based on user preferences and conversation history.
    """
    
    def __init__(self, pattern_learner: ConversationPatternLearner, quality_improver: ResponseQualityImprover):
        """Initialize the adaptive response generator."""
        self.pattern_learner = pattern_learner
        self.quality_improver = quality_improver
        
        # Adaptation parameters
        self.context_window_size = 5  # Number of recent messages to consider
        self.adaptation_threshold = 0.6  # Minimum confidence for adaptation
        
        logger.info("Adaptive Response Generator initialized")
    
    async def generate_adaptive_response(
        self,
        user_message: str,
        base_response: str,
        context: AdaptiveContext,
        model_id: str
    ) -> Dict[str, Any]:
        """
        Generate an adaptive response based on context and learning.
        
        Args:
            user_message: User's input message
            base_response: Base AI response
            context: Adaptive context with user preferences and history
            model_id: Model being used
            
        Returns:
            Adaptive response with adaptation metadata
        """
        try:
            # Extract user intent
            user_intent = await self.pattern_learner._extract_user_intent(user_message)
            
            # Find relevant patterns
            relevant_patterns = await self.pattern_learner.find_best_pattern(
                user_intent, context.user_preferences, limit=3
            )
            
            # Analyze conversation context
            context_analysis = await self._analyze_conversation_context(context)
            
            # Generate adaptation strategy
            adaptation_strategy = await self._generate_adaptation_strategy(
                user_intent, relevant_patterns, context_analysis, context.user_preferences
            )
            
            # Apply adaptations
            adapted_response = await self._apply_adaptations(
                base_response, adaptation_strategy, context
            )
            
            # Record quality metric for learning
            await self.quality_improver.record_quality_metric(
                session_id=context.conversation_history[-1].get("session_id", "unknown"),
                user_message=user_message,
                ai_response=adapted_response["response"],
                metadata={
                    "adaptation_applied": True,
                    "adaptation_strategy": adaptation_strategy,
                    "user_intent": user_intent,
                    "context_analysis": context_analysis
                }
            )
            
            return {
                "response": adapted_response["response"],
                "adaptation_applied": True,
                "adaptation_strategy": adaptation_strategy,
                "context_analysis": context_analysis,
                "pattern_confidence": adapted_response["pattern_confidence"],
                "metadata": {
                    "user_intent": user_intent,
                    "relevant_patterns": len(relevant_patterns),
                    "adaptation_confidence": adapted_response["adaptation_confidence"]
                }
            }
            
        except Exception as e:
            logger.error(f"Adaptive response generation failed: {e}")
            return {
                "response": base_response,
                "adaptation_applied": False,
                "error": str(e)
            }
    
    async def _analyze_conversation_context(self, context: AdaptiveContext) -> Dict[str, Any]:
        """Analyze conversation context for adaptation."""
        try:
            if not context.conversation_history:
                return {"conversation_length": 0, "topic_consistency": 0.0}
            
            recent_messages = context.conversation_history[-self.context_window_size:]
            
            # Topic consistency
            topics = []
            for msg in recent_messages:
                if "metadata" in msg and "user_topics" in msg["metadata"]:
                    topics.extend(msg["metadata"]["user_topics"].get("topics", []))
            
            topic_consistency = 0.0
            if topics:
                topic_counts = Counter(topics)
                most_common = topic_counts.most_common(1)[0]
                topic_consistency = most_common[1] / len(recent_messages)
            
            # User engagement level
            engagement_indicators = []
            for msg in recent_messages:
                if msg.get("role") == "user":
                    # Check for engagement indicators
                    content = msg.get("content", "").lower()
                    if any(word in content for word in ["why", "how", "what", "tell me more"]):
                        engagement_indicators.append(1.0)
                    elif len(content.split()) > 5:
                        engagement_indicators.append(0.7)
                    else:
                        engagement_indicators.append(0.3)
            
            avg_engagement = np.mean(engagement_indicators) if engagement_indicators else 0.5
            
            return {
                "conversation_length": len(context.conversation_history),
                "topic_consistency": topic_consistency,
                "user_engagement": avg_engagement,
                "recent_message_count": len(recent_messages)
            }
            
        except Exception as e:
            logger.error(f"Context analysis failed: {e}")
            return {"error": str(e)}
    
    async def _generate_adaptation_strategy(
        self,
        user_intent: str,
        relevant_patterns: List[LearningPattern],
        context_analysis: Dict[str, Any],
        user_preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate adaptation strategy based on patterns and context."""
        try:
            strategy = {
                "style_adaptation": "neutral",
                "detail_level": "medium",
                "formality": "neutral",
                "engagement_boost": False,
                "context_integration": False
            }
            
            # Style adaptation based on user preferences
            if user_preferences.get("conversation_style") == "casual":
                strategy["style_adaptation"] = "casual"
            elif user_preferences.get("conversation_style") == "formal":
                strategy["formality"] = "formal"
            
            # Detail level based on user engagement
            if context_analysis.get("user_engagement", 0.5) > 0.7:
                strategy["detail_level"] = "high"
                strategy["engagement_boost"] = True
            elif context_analysis.get("user_engagement", 0.5) < 0.3:
                strategy["detail_level"] = "low"
            
            # Context integration for topic consistency
            if context_analysis.get("topic_consistency", 0.0) > 0.5:
                strategy["context_integration"] = True
            
            # Pattern-based adaptations
            if relevant_patterns:
                best_pattern = relevant_patterns[0]
                if best_pattern.success_rate > 0.8:
                    strategy["pattern_confidence"] = "high"
                elif best_pattern.success_rate > 0.6:
                    strategy["pattern_confidence"] = "medium"
                else:
                    strategy["pattern_confidence"] = "low"
            
            return strategy
            
        except Exception as e:
            logger.error(f"Adaptation strategy generation failed: {e}")
            return {"error": str(e)}
    
    async def _apply_adaptations(
        self,
        base_response: str,
        adaptation_strategy: Dict[str, Any],
        context: AdaptiveContext
    ) -> Dict[str, Any]:
        """Apply adaptations to the base response."""
        try:
            adapted_response = base_response
            adaptation_confidence = 0.5
            
            # Apply style adaptations
            if adaptation_strategy.get("style_adaptation") == "casual":
                adapted_response = await self._make_response_casual(adapted_response)
                adaptation_confidence += 0.1
            
            if adaptation_strategy.get("formality") == "formal":
                adapted_response = await self._make_response_formal(adapted_response)
                adaptation_confidence += 0.1
            
            # Apply detail level adaptations
            if adaptation_strategy.get("detail_level") == "high":
                adapted_response = await self._increase_response_detail(adapted_response, context)
                adaptation_confidence += 0.15
            elif adaptation_strategy.get("detail_level") == "low":
                adapted_response = await self._decrease_response_detail(adapted_response)
                adaptation_confidence += 0.1
            
            # Apply engagement boost
            if adaptation_strategy.get("engagement_boost"):
                adapted_response = await self._boost_engagement(adapted_response)
                adaptation_confidence += 0.1
            
            # Apply context integration
            if adaptation_strategy.get("context_integration"):
                adapted_response = await self._integrate_context(adapted_response, context)
                adaptation_confidence += 0.15
            
            # Normalize confidence
            adaptation_confidence = min(adaptation_confidence, 1.0)
            
            return {
                "response": adapted_response,
                "adaptation_confidence": adaptation_confidence,
                "pattern_confidence": adaptation_strategy.get("pattern_confidence", "unknown")
            }
            
        except Exception as e:
            logger.error(f"Adaptation application failed: {e}")
            return {
                "response": base_response,
                "adaptation_confidence": 0.0,
                "pattern_confidence": "unknown"
            }
    
    async def _make_response_casual(self, response: str) -> str:
        """Make response more casual and friendly."""
        # Simple casual adaptations
        casual_replacements = {
            "I will": "I'll",
            "I am": "I'm",
            "you are": "you're",
            "it is": "it's",
            "that is": "that's"
        }
        
        for formal, casual in casual_replacements.items():
            response = response.replace(formal, casual)
        
        return response
    
    async def _make_response_formal(self, response: str) -> str:
        """Make response more formal and professional."""
        # Simple formal adaptations
        formal_replacements = {
            "I'll": "I will",
            "I'm": "I am",
            "you're": "you are",
            "it's": "it is",
            "that's": "that is"
        }
        
        for casual, formal in formal_replacements.items():
            response = response.replace(casual, formal)
        
        return response
    
    async def _increase_response_detail(self, response: str, context: AdaptiveContext) -> str:
        """Increase response detail level."""
        # Add context-aware details
        if context.conversation_history:
            recent_topics = []
            for msg in context.conversation_history[-3:]:
                if "metadata" in msg and "user_topics" in msg["metadata"]:
                    topics = msg["metadata"]["user_topics"].get("topics", [])
                    recent_topics.extend(topics)
            
            if recent_topics:
                unique_topics = list(set(recent_topics))
                if len(unique_topics) > 0:
                    response += f"\n\nThis relates to our discussion about {', '.join(unique_topics[:2])}."
        
        return response
    
    async def _decrease_response_detail(self, response: str) -> str:
        """Decrease response detail level."""
        # Keep only essential information
        sentences = response.split('.')
        if len(sentences) > 2:
            response = '. '.join(sentences[:2]) + '.'
        
        return response
    
    async def _boost_engagement(self, response: str) -> str:
        """Boost user engagement in response."""
        # Add engagement elements
        if not response.endswith('?'):
            response += "\n\nWhat are your thoughts on this?"
        
        return response
    
    async def _integrate_context(self, response: str, context: AdaptiveContext) -> str:
        """Integrate conversation context into response."""
        # Reference previous conversation elements
        if context.conversation_history:
            recent_user_messages = [
                msg for msg in context.conversation_history[-3:] 
                if msg.get("role") == "user"
            ]
            
            if recent_user_messages:
                last_user_msg = recent_user_messages[-1].get("content", "")
                if len(last_user_msg) > 10:
                    response += f"\n\nBuilding on your question about '{last_user_msg[:50]}...', "
        
        return response


class ATLESMachineLearning:
    """
    Main machine learning coordinator for ATLES.
    
    Integrates all learning capabilities and provides a unified interface.
    """
    
    def __init__(self, learning_dir: Optional[Path] = None):
        """Initialize the machine learning system."""
        self.pattern_learner = ConversationPatternLearner(learning_dir)
        self.quality_improver = ResponseQualityImprover(learning_dir)
        self.adaptive_generator = AdaptiveResponseGenerator(
            self.pattern_learner, self.quality_improver
        )
        
        logger.info("ATLES Machine Learning System initialized")
    
    async def learn_from_interaction(
        self,
        user_message: str,
        ai_response: str,
        user_feedback: Optional[float],
        context: Dict[str, Any],
        session_id: str,
        success_indicator: bool = True
    ) -> Dict[str, Any]:
        """
        Learn from a complete user-AI interaction.
        
        Args:
            user_message: User's input message
            ai_response: AI's response
            user_feedback: Explicit user feedback (0.0 to 1.0)
            context: Conversation context
            session_id: Session identifier
            success_indicator: Whether the interaction was successful
            
        Returns:
            Learning results summary
        """
        try:
            # Learn conversation patterns
            pattern_id = await self.pattern_learner.learn_from_interaction(
                user_message, ai_response, user_feedback, context, success_indicator
            )
            
            # Record quality metrics
            quality_id = await self.quality_improver.record_quality_metric(
                session_id, user_message, ai_response, user_feedback, context
            )
            
            return {
                "success": True,
                "pattern_learned": pattern_id,
                "quality_recorded": quality_id,
                "learning_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Learning from interaction failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def generate_adaptive_response(
        self,
        user_message: str,
        base_response: str,
        context: AdaptiveContext,
        model_id: str
    ) -> Dict[str, Any]:
        """Generate an adaptive response using learned patterns."""
        return await self.adaptive_generator.generate_adaptive_response(
            user_message, base_response, context, model_id
        )
    
    async def get_learning_insights(self) -> Dict[str, Any]:
        """Get comprehensive insights about the learning system."""
        try:
            pattern_stats = await self.pattern_learner.get_pattern_statistics()
            quality_insights = await self.quality_improver.get_quality_insights()
            
            return {
                "pattern_learning": pattern_stats,
                "quality_improvement": quality_insights,
                "system_status": "operational",
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get learning insights: {e}")
            return {"error": str(e)}
    
    async def export_learning_data(self, export_path: Path) -> bool:
        """Export learning data for analysis or backup."""
        try:
            export_data = {
                "patterns": self.pattern_learner.patterns,
                "quality_metrics": self.quality_improver.quality_metrics,
                "export_timestamp": datetime.now().isoformat(),
                "version": "2.0"
            }
            
            with open(export_path, 'wb') as f:
                pickle.dump(export_data, f)
            
            logger.info(f"Learning data exported to {export_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export learning data: {e}")
            return False
    
    async def import_learning_data(self, import_path: Path) -> bool:
        """Import learning data from backup or analysis."""
        try:
            with open(import_path, 'rb') as f:
                import_data = pickle.load(f)
            
            # Validate import data
            if "patterns" in import_data and "quality_metrics" in import_data:
                self.pattern_learner.patterns = import_data["patterns"]
                self.quality_improver.quality_metrics = import_data["quality_metrics"]
                
                # Save imported data
                self.pattern_learner._save_patterns()
                self.quality_improver._save_quality_metrics()
                
                logger.info(f"Learning data imported from {import_path}")
                return True
            else:
                logger.error("Invalid import data format")
                return False
                
        except Exception as e:
            logger.error(f"Failed to import learning data: {e}")
            return False


# Example usage and testing
async def test_machine_learning():
    """Test the machine learning system."""
    ml_system = ATLESMachineLearning()
    
    # Test pattern learning
    context = {"user_preference": "technical", "topic": "programming"}
    learning_result = await ml_system.learn_from_interaction(
        "How do I implement a binary search?",
        "Binary search is an efficient algorithm for finding elements in sorted arrays...",
        0.9,  # High user feedback
        context,
        "test_session_1"
    )
    print(f"Learning Result: {learning_result}")
    
    # Test quality improvement
    insights = await ml_system.get_learning_insights()
    print(f"Learning Insights: {json.dumps(insights, indent=2)}")


if __name__ == "__main__":
    asyncio.run(test_machine_learning())
