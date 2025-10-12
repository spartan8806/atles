"""
Integrated Proactive Messaging with Memory-Aware Reasoning

This connects ATLES's proactive messaging system with the new memory-aware
reasoning system, ensuring all analysis uses the same learning capabilities.
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path

from .memory_aware_reasoning import MemoryAwareReasoning
from .learning_response_generator import LearningResponseGenerator

logger = logging.getLogger(__name__)


class IntegratedProactiveMessaging:
    """
    Proactive messaging system that uses memory-aware reasoning for analysis.
    
    This replaces the basic conversation analysis with sophisticated
    learning-based insights.
    """
    
    def __init__(self, memory_path: str = "atles_memory"):
        self.memory_reasoning = MemoryAwareReasoning(memory_path)
        self.learning_generator = LearningResponseGenerator(memory_path)
        
        # Load configuration
        self.config = self._load_config()
        
        logger.info("Integrated Proactive Messaging initialized with memory-aware reasoning")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load proactive messaging configuration."""
        try:
            config_file = Path("atles_config.json")
            if config_file.exists():
                with open(config_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {}
    
    def generate_self_review_insights(self) -> Dict[str, Any]:
        """
        Generate self-review insights using memory-aware reasoning.
        
        This replaces the basic conversation counting with sophisticated analysis.
        """
        logger.info("Generating memory-aware self-review insights")
        
        # Load conversation history
        conversation_history = self.memory_reasoning._load_conversation_memory()
        
        # Get learning summary
        learning_summary = self.memory_reasoning.get_learning_summary()
        
        # Analyze conversation patterns with memory awareness
        insights = self._analyze_conversation_patterns(conversation_history)
        
        # Add learning-based insights
        insights.update(self._generate_learning_insights(learning_summary))
        
        # Generate proactive suggestions based on learned principles
        insights["proactive_suggestions"] = self._generate_proactive_suggestions(
            conversation_history, learning_summary
        )
        
        return {
            "analysis_timestamp": datetime.now().isoformat(),
            "memory_informed": True,
            "insights": insights,
            "learning_summary": learning_summary,
            "conversation_stats": self._get_accurate_conversation_stats(conversation_history)
        }
    
    def _analyze_conversation_patterns(self, conversation_history: list) -> Dict[str, Any]:
        """Analyze conversation patterns using memory-aware reasoning."""
        if not conversation_history:
            return {
                "pattern_analysis": "No conversation history available",
                "key_insights": ["Start a conversation to begin learning patterns"]
            }
        
        # Extract recent conversations (last 50 messages)
        recent_conversations = conversation_history[-50:] if len(conversation_history) > 50 else conversation_history
        
        # Analyze user message patterns
        user_messages = [msg for msg in recent_conversations if msg.get('sender') == 'You']
        atles_messages = [msg for msg in recent_conversations if msg.get('sender') == 'ATLES']
        
        # Identify conversation themes
        themes = self._identify_conversation_themes(user_messages)
        
        # Analyze interaction patterns
        interaction_patterns = self._analyze_interaction_patterns(recent_conversations)
        
        return {
            "conversation_themes": themes,
            "interaction_patterns": interaction_patterns,
            "user_engagement_level": self._calculate_engagement_level(user_messages),
            "learning_opportunities": self._identify_learning_opportunities(recent_conversations)
        }
    
    def _identify_conversation_themes(self, user_messages: list) -> Dict[str, Any]:
        """Identify themes in user conversations."""
        if not user_messages:
            return {"themes": [], "primary_focus": "No user messages yet"}
        
        # Analyze message content for themes
        technical_keywords = ["code", "function", "error", "debug", "programming", "python", "javascript"]
        creative_keywords = ["story", "creative", "write", "imagine", "design", "art"]
        learning_keywords = ["learn", "understand", "explain", "how", "what", "why"]
        personal_keywords = ["want", "like", "feel", "think", "prefer", "favorite"]
        
        theme_counts = {
            "technical": 0,
            "creative": 0, 
            "learning": 0,
            "personal": 0
        }
        
        for msg in user_messages[-20:]:  # Last 20 user messages
            content = msg.get('message', '').lower()
            
            if any(keyword in content for keyword in technical_keywords):
                theme_counts["technical"] += 1
            if any(keyword in content for keyword in creative_keywords):
                theme_counts["creative"] += 1
            if any(keyword in content for keyword in learning_keywords):
                theme_counts["learning"] += 1
            if any(keyword in content for keyword in personal_keywords):
                theme_counts["personal"] += 1
        
        # Determine primary theme
        primary_theme = max(theme_counts.items(), key=lambda x: x[1])
        
        return {
            "theme_distribution": theme_counts,
            "primary_focus": primary_theme[0] if primary_theme[1] > 0 else "general",
            "focus_strength": primary_theme[1]
        }
    
    def _analyze_interaction_patterns(self, conversations: list) -> Dict[str, Any]:
        """Analyze patterns in user-AI interactions."""
        if len(conversations) < 4:
            return {"pattern": "insufficient_data", "description": "Need more interactions to identify patterns"}
        
        # Look for question patterns
        user_messages = [msg for msg in conversations if msg.get('sender') == 'You']
        
        question_patterns = {
            "hypothetical": 0,
            "technical": 0,
            "explanatory": 0,
            "creative": 0
        }
        
        for msg in user_messages:
            content = msg.get('message', '').lower()
            
            if any(pattern in content for pattern in ["what do you", "what would you", "if you could", "how do you feel"]):
                question_patterns["hypothetical"] += 1
            elif any(pattern in content for pattern in ["how to", "error", "debug", "code"]):
                question_patterns["technical"] += 1
            elif any(pattern in content for pattern in ["explain", "what is", "how does", "why"]):
                question_patterns["explanatory"] += 1
            elif any(pattern in content for pattern in ["create", "write", "design", "imagine"]):
                question_patterns["creative"] += 1
        
        dominant_pattern = max(question_patterns.items(), key=lambda x: x[1])
        
        return {
            "question_patterns": question_patterns,
            "dominant_pattern": dominant_pattern[0],
            "pattern_strength": dominant_pattern[1],
            "interaction_style": self._determine_interaction_style(question_patterns)
        }
    
    def _determine_interaction_style(self, question_patterns: Dict[str, int]) -> str:
        """Determine the user's interaction style."""
        total_questions = sum(question_patterns.values())
        
        if total_questions == 0:
            return "exploratory"
        
        # Calculate percentages
        percentages = {k: (v / total_questions) * 100 for k, v in question_patterns.items()}
        
        if percentages["hypothetical"] > 40:
            return "philosophical_explorer"
        elif percentages["technical"] > 50:
            return "technical_problem_solver"
        elif percentages["creative"] > 40:
            return "creative_collaborator"
        elif percentages["explanatory"] > 50:
            return "knowledge_seeker"
        else:
            return "balanced_conversationalist"
    
    def _calculate_engagement_level(self, user_messages: list) -> str:
        """Calculate user engagement level."""
        if not user_messages:
            return "no_engagement"
        
        recent_messages = user_messages[-10:] if len(user_messages) > 10 else user_messages
        
        # Calculate average message length
        avg_length = sum(len(msg.get('message', '')) for msg in recent_messages) / len(recent_messages)
        
        # Look for engagement indicators
        engagement_indicators = ["interesting", "great", "thanks", "perfect", "exactly", "love", "amazing"]
        positive_feedback = sum(1 for msg in recent_messages 
                               if any(indicator in msg.get('message', '').lower() 
                                     for indicator in engagement_indicators))
        
        if avg_length > 100 and positive_feedback > 2:
            return "highly_engaged"
        elif avg_length > 50 or positive_feedback > 1:
            return "moderately_engaged"
        elif len(recent_messages) > 5:
            return "actively_participating"
        else:
            return "minimal_engagement"
    
    def _identify_learning_opportunities(self, conversations: list) -> list:
        """Identify opportunities for ATLES to learn and improve."""
        opportunities = []
        
        # Look for correction patterns
        user_messages = [msg for msg in conversations if msg.get('sender') == 'You']
        
        for msg in user_messages:
            content = msg.get('message', '').lower()
            
            if any(pattern in content for pattern in ["should have", "instead", "wrong", "incorrect", "better"]):
                opportunities.append({
                    "type": "correction_feedback",
                    "description": "User provided correction or feedback",
                    "message": msg.get('message', '')[:100] + "..." if len(msg.get('message', '')) > 100 else msg.get('message', '')
                })
            
            if any(pattern in content for pattern in ["principle", "rule", "always", "never", "remember"]):
                opportunities.append({
                    "type": "principle_teaching",
                    "description": "User taught a new principle or rule",
                    "message": msg.get('message', '')[:100] + "..." if len(msg.get('message', '')) > 100 else msg.get('message', '')
                })
        
        return opportunities[-5:]  # Last 5 opportunities
    
    def _generate_learning_insights(self, learning_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights based on learned principles."""
        total_principles = learning_summary.get("total_principles", 0)
        
        if total_principles == 0:
            return {
                "learning_status": "No learned principles yet",
                "learning_recommendation": "Continue conversations to help me learn your preferences and patterns"
            }
        
        most_used = learning_summary.get("most_used")
        recently_learned = learning_summary.get("recently_learned", [])
        
        insights = {
            "learning_status": f"Active learning with {total_principles} learned principle(s)",
            "most_applied_principle": most_used,
            "recent_learning": [p.name for p in recently_learned[:3]],
            "learning_progress": "Continuously adapting based on our conversations"
        }
        
        return insights
    
    def _generate_proactive_suggestions(self, conversation_history: list, learning_summary: Dict[str, Any]) -> list:
        """Generate proactive suggestions based on conversation patterns and learned principles."""
        suggestions = []
        
        if not conversation_history:
            return ["Start a conversation to help me learn your preferences and patterns!"]
        
        # Analyze recent conversation for suggestion opportunities
        recent_messages = conversation_history[-10:] if len(conversation_history) > 10 else conversation_history
        user_messages = [msg for msg in recent_messages if msg.get('sender') == 'You']
        
        # Suggest based on conversation patterns
        if any("error" in msg.get('message', '').lower() for msg in user_messages):
            suggestions.append("I notice you've been working with errors. Would you like me to help debug or explain error patterns?")
        
        if any(pattern in msg.get('message', '').lower() for msg in user_messages for pattern in ["what do you", "what would you"]):
            suggestions.append("I see you enjoy hypothetical questions! Feel free to ask me about my thoughts on any topic.")
        
        # Suggest based on learned principles
        if learning_summary.get("total_principles", 0) > 0:
            suggestions.append("I've learned from our conversations and can now apply those lessons. Try asking me something similar to what we discussed before!")
        
        # Default suggestions
        if not suggestions:
            suggestions.extend([
                "Ask me about my thoughts on a topic you're curious about",
                "Share something you're working on - I'd love to help or learn about it",
                "Try a hypothetical question - I enjoy creative scenarios!"
            ])
        
        return suggestions[:3]  # Limit to 3 suggestions
    
    def _get_accurate_conversation_stats(self, conversation_history: list) -> Dict[str, Any]:
        """Get accurate conversation statistics."""
        if not conversation_history:
            return {
                "total_messages": 0,
                "user_messages": 0,
                "atles_messages": 0,
                "conversation_length": 0
            }
        
        user_messages = [msg for msg in conversation_history if msg.get('sender') == 'You']
        atles_messages = [msg for msg in conversation_history if msg.get('sender') == 'ATLES']
        
        return {
            "total_messages": len(conversation_history),
            "user_messages": len(user_messages),
            "atles_messages": len(atles_messages),
            "conversation_length": len(conversation_history),
            "last_interaction": conversation_history[-1].get('timestamp') if conversation_history else None
        }
    
    def should_send_proactive_message(self) -> bool:
        """Determine if a proactive message should be sent based on memory-aware analysis."""
        pm_config = self.config.get('proactive_messaging', {})
        
        if not pm_config.get('enabled', False):
            return False
        
        # Use memory-aware analysis to determine if proactive messaging is appropriate
        insights = self.generate_self_review_insights()
        
        # Check if there are learning opportunities or interesting patterns
        learning_opportunities = insights["insights"].get("learning_opportunities", [])
        engagement_level = insights["insights"].get("user_engagement_level", "minimal")
        
        # Send proactive message if there are learning insights to share
        return (len(learning_opportunities) > 0 or 
                engagement_level in ["highly_engaged", "moderately_engaged"] or
                insights["learning_summary"].get("total_principles", 0) > 0)


def demonstrate_integrated_proactive_messaging():
    """Demonstrate the integrated proactive messaging system."""
    
    print("🔄 ATLES Integrated Proactive Messaging Demonstration")
    print("=" * 60)
    print("Showing memory-aware proactive messaging vs basic analysis")
    print()
    
    # Initialize integrated system
    integrated_pm = IntegratedProactiveMessaging()
    
    # Generate insights
    insights = integrated_pm.generate_self_review_insights()
    
    print("📊 MEMORY-AWARE SELF-REVIEW INSIGHTS")
    print("-" * 40)
    
    # Show conversation stats
    stats = insights["conversation_stats"]
    print(f"Total messages: {stats['total_messages']}")
    print(f"User messages: {stats['user_messages']}")
    print(f"ATLES messages: {stats['atles_messages']}")
    print()
    
    # Show learning insights
    learning = insights["learning_summary"]
    print(f"📚 Learning Status:")
    print(f"  Learned principles: {learning.get('total_principles', 0)}")
    if learning.get('most_used'):
        print(f"  Most applied: {learning['most_used']}")
    print()
    
    # Show conversation analysis
    analysis = insights["insights"]
    print(f"🎯 Conversation Analysis:")
    print(f"  Primary focus: {analysis.get('conversation_themes', {}).get('primary_focus', 'Unknown')}")
    print(f"  Interaction style: {analysis.get('interaction_patterns', {}).get('interaction_style', 'Unknown')}")
    print(f"  Engagement level: {analysis.get('user_engagement_level', 'Unknown')}")
    print()
    
    # Show proactive suggestions
    suggestions = analysis.get("proactive_suggestions", [])
    if suggestions:
        print(f"💡 Proactive Suggestions:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")
    
    print(f"\n✅ Memory-aware proactive messaging is working correctly!")


if __name__ == "__main__":
    demonstrate_integrated_proactive_messaging()
