"""
ATLES Enhanced Conversation System

Integration layer that combines the Advanced NLP Module and Conversation Flow Manager
with the existing ATLES system to provide sophisticated conversation capabilities.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

# Import the new modules
try:
    from .advanced_nlp_module import AdvancedNLPModule, NLPAnalysis
    from .conversation_flow_manager import ConversationFlowManager, ConversationState
    NLP_AVAILABLE = True
except ImportError:
    NLP_AVAILABLE = False

logger = logging.getLogger(__name__)

class EnhancedConversationSystem:
    """
    Enhanced conversation system that integrates advanced NLP and conversation flow management.
    
    This system provides:
    - Sophisticated natural language understanding
    - Multi-step conversation tracking
    - Context-aware responses
    - Intelligent follow-up suggestions
    - Task flow management
    """
    
    def __init__(self, storage_path: str = "atles_memory/conversations"):
        self.nlp_module = AdvancedNLPModule() if NLP_AVAILABLE else None
        self.flow_manager = ConversationFlowManager(storage_path) if NLP_AVAILABLE else None
        self.active_conversation_id = None
        
        if not NLP_AVAILABLE:
            logger.warning("Enhanced conversation modules not available - using basic mode")
    
    def start_conversation(self, user_id: Optional[str] = None, 
                          goals: List[str] = None) -> str:
        """Start a new enhanced conversation."""
        if not self.flow_manager:
            return "basic_conversation"
        
        conversation_id = self.flow_manager.start_conversation(user_id, goals)
        self.active_conversation_id = conversation_id
        
        logger.info(f"Started enhanced conversation: {conversation_id}")
        return conversation_id
    
    def process_user_input(self, user_input: str, conversation_id: str = None) -> Dict[str, Any]:
        """
        Process user input with enhanced NLP and conversation tracking.
        
        Returns comprehensive analysis and conversation context.
        """
        if not self.nlp_module or not self.flow_manager:
            return self._basic_processing(user_input)
        
        # Use active conversation if none specified
        if not conversation_id:
            conversation_id = self.active_conversation_id
        
        if not conversation_id:
            conversation_id = self.start_conversation()
        
        # Perform NLP analysis
        nlp_analysis = self.nlp_module.analyze_input(user_input, conversation_id)
        
        # Get conversation context
        conversation_context = self.flow_manager.get_conversation_context(conversation_id)
        
        # Generate response guidance
        response_guidance = self._generate_response_guidance(nlp_analysis, conversation_context)
        
        return {
            "conversation_id": conversation_id,
            "nlp_analysis": {
                "intent": nlp_analysis.intent.value if hasattr(nlp_analysis.intent, 'value') else str(nlp_analysis.intent),
                "sentiment": nlp_analysis.sentiment.value if hasattr(nlp_analysis.sentiment, 'value') else str(nlp_analysis.sentiment),
                "confidence": nlp_analysis.confidence,
                "topics": nlp_analysis.topics,
                "entities": nlp_analysis.entities,
                "urgency_level": nlp_analysis.urgency_level,
                "complexity_score": nlp_analysis.complexity_score,
                "context_clues": nlp_analysis.context_clues,
                "conversation_markers": nlp_analysis.conversation_markers
            },
            "conversation_context": conversation_context,
            "response_guidance": response_guidance,
            "processing_timestamp": datetime.now().isoformat()
        }
    
    def add_ai_response(self, conversation_id: str, user_input: str, 
                       ai_response: str, nlp_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Add AI response to conversation and get follow-up suggestions."""
        if not self.flow_manager:
            return {"follow_ups": []}
        
        # Add turn to conversation
        turn = self.flow_manager.add_turn(
            conversation_id, 
            user_input, 
            ai_response, 
            nlp_data or {}
        )
        
        # Get follow-up suggestions
        follow_ups = self.flow_manager.suggest_follow_ups(conversation_id)
        
        # Check for task advancement
        task_updates = self._check_task_advancement(conversation_id, ai_response)
        
        return {
            "turn_id": turn.turn_id,
            "follow_ups": follow_ups,
            "task_updates": task_updates,
            "conversation_state": self.flow_manager.active_conversations[conversation_id].state.value
        }
    
    def create_multi_step_task(self, conversation_id: str, task_description: str) -> Dict[str, Any]:
        """Create a multi-step task based on user request."""
        if not self.flow_manager:
            return {"error": "Multi-step tasks not available"}
        
        # Analyze task description to determine type and steps
        task_info = self._analyze_task_description(task_description)
        
        task_id = self.flow_manager.create_multi_step_task(
            conversation_id,
            task_info["title"],
            task_description,
            task_info["steps"]
        )
        
        return {
            "task_id": task_id,
            "title": task_info["title"],
            "total_steps": len(task_info["steps"]),
            "first_step": task_info["steps"][0] if task_info["steps"] else None
        }
    
    def get_enhanced_context_for_response(self, conversation_id: str) -> Dict[str, Any]:
        """Get enhanced context to inform AI response generation."""
        if not self.flow_manager or not self.nlp_module:
            return {}
        
        # Get conversation context
        context = self.flow_manager.get_conversation_context(conversation_id)
        
        # Get conversation summary from NLP module
        nlp_summary = self.nlp_module.get_conversation_summary(conversation_id)
        
        # Combine and enhance
        enhanced_context = {
            "conversation_flow": context,
            "nlp_insights": nlp_summary,
            "response_recommendations": self._generate_response_recommendations(context, nlp_summary)
        }
        
        return enhanced_context
    
    def _basic_processing(self, user_input: str) -> Dict[str, Any]:
        """Basic processing when enhanced modules aren't available."""
        return {
            "conversation_id": "basic",
            "nlp_analysis": {
                "intent": "conversation",
                "sentiment": "neutral",
                "confidence": 0.5,
                "topics": [],
                "entities": [],
                "urgency_level": 3,
                "complexity_score": 0.5,
                "context_clues": [],
                "conversation_markers": []
            },
            "conversation_context": {
                "state": "active",
                "turn_count": 0,
                "main_topics": [],
                "active_task": None
            },
            "response_guidance": {
                "style": "conversational",
                "focus_areas": [],
                "suggested_actions": []
            }
        }
    
    def _generate_response_guidance(self, nlp_analysis: 'NLPAnalysis', 
                                  conversation_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate guidance for AI response based on analysis and context."""
        guidance = {
            "style": "conversational",
            "focus_areas": [],
            "suggested_actions": [],
            "tone": "helpful",
            "urgency": "normal"
        }
        
        # Adjust based on intent
        if nlp_analysis.intent.value == "question":
            guidance["style"] = "informative"
            guidance["suggested_actions"].append("provide_comprehensive_answer")
        elif nlp_analysis.intent.value == "request":
            guidance["style"] = "action_oriented"
            guidance["suggested_actions"].append("confirm_understanding")
        elif nlp_analysis.intent.value == "command":
            guidance["style"] = "direct"
            guidance["suggested_actions"].append("execute_or_explain")
        
        # Adjust based on sentiment
        if nlp_analysis.sentiment.value == "negative":
            guidance["tone"] = "empathetic"
            guidance["suggested_actions"].append("address_concerns")
        elif nlp_analysis.sentiment.value == "positive":
            guidance["tone"] = "enthusiastic"
        
        # Adjust based on urgency
        if nlp_analysis.urgency_level >= 4:
            guidance["urgency"] = "high"
            guidance["suggested_actions"].append("prioritize_response")
        
        # Focus on detected topics
        guidance["focus_areas"] = nlp_analysis.topics[:3]  # Top 3 topics
        
        # Consider conversation context
        if conversation_context.get("active_task"):
            guidance["suggested_actions"].append("reference_active_task")
        
        if conversation_context.get("turn_count", 0) > 5:
            guidance["suggested_actions"].append("maintain_context_continuity")
        
        return guidance
    
    def _check_task_advancement(self, conversation_id: str, ai_response: str) -> List[Dict[str, Any]]:
        """Check if AI response indicates task step completion."""
        if not self.flow_manager:
            return []
        
        flow = self.flow_manager.active_conversations.get(conversation_id)
        if not flow or not flow.active_tasks:
            return []
        
        task_updates = []
        
        # Check for completion indicators in AI response
        completion_indicators = [
            "completed", "finished", "done", "ready for next",
            "step complete", "moving to", "proceeding to"
        ]
        
        ai_response_lower = ai_response.lower()
        
        for task in flow.active_tasks:
            if task.status.value == "in_progress":
                if any(indicator in ai_response_lower for indicator in completion_indicators):
                    # Advance task step
                    update = self.flow_manager.advance_task_step(
                        conversation_id, 
                        task.task_id,
                        {"ai_response": ai_response, "completed_at": datetime.now().isoformat()}
                    )
                    task_updates.append(update)
        
        return task_updates
    
    def _analyze_task_description(self, description: str) -> Dict[str, Any]:
        """Analyze task description to determine appropriate steps."""
        description_lower = description.lower()
        
        # Default task structure
        task_info = {
            "title": "Custom Task",
            "steps": [
                {"title": "Analyze requirements", "type": "analysis"},
                {"title": "Plan approach", "type": "planning"},
                {"title": "Execute task", "type": "execution"},
                {"title": "Review results", "type": "review"}
            ]
        }
        
        # Customize based on keywords
        if any(word in description_lower for word in ["upgrade", "improve", "enhance"]):
            task_info["title"] = "System Enhancement"
            task_info["steps"] = [
                {"title": "Assess current state", "type": "assessment"},
                {"title": "Identify improvements", "type": "analysis"},
                {"title": "Design enhancements", "type": "design"},
                {"title": "Implement changes", "type": "implementation"},
                {"title": "Test and validate", "type": "testing"}
            ]
        
        elif any(word in description_lower for word in ["learn", "understand", "explain"]):
            task_info["title"] = "Learning Session"
            task_info["steps"] = [
                {"title": "Assess knowledge level", "type": "assessment"},
                {"title": "Provide explanation", "type": "teaching"},
                {"title": "Practice examples", "type": "practice"},
                {"title": "Reinforce learning", "type": "reinforcement"}
            ]
        
        elif any(word in description_lower for word in ["create", "build", "develop"]):
            task_info["title"] = "Development Project"
            task_info["steps"] = [
                {"title": "Define requirements", "type": "requirements"},
                {"title": "Design architecture", "type": "design"},
                {"title": "Implement solution", "type": "implementation"},
                {"title": "Test functionality", "type": "testing"},
                {"title": "Deploy and monitor", "type": "deployment"}
            ]
        
        return task_info
    
    def _generate_response_recommendations(self, context: Dict[str, Any], 
                                         nlp_summary: Dict[str, Any]) -> List[str]:
        """Generate specific recommendations for response content."""
        recommendations = []
        
        # Based on conversation state
        state = context.get("state", "active")
        if state == "starting":
            recommendations.append("Provide welcoming introduction and set expectations")
        elif state == "executing":
            recommendations.append("Focus on task progress and next steps")
        elif state == "waiting_for_input":
            recommendations.append("Gently prompt for needed information")
        
        # Based on active tasks
        if context.get("active_task"):
            task = context["active_task"]
            recommendations.append(f"Reference current task progress ({task['completion_percentage']:.0f}% complete)")
            if task.get("next_step"):
                recommendations.append(f"Prepare for next step: {task['next_step']['title']}")
        
        # Based on main topics
        main_topics = context.get("main_topics", [])
        if main_topics:
            recommendations.append(f"Maintain focus on key topics: {', '.join(main_topics[:2])}")
        
        # Based on conversation length
        turn_count = context.get("turn_count", 0)
        if turn_count > 10:
            recommendations.append("Consider summarizing key points covered so far")
        elif turn_count < 3:
            recommendations.append("Build rapport and understand user needs")
        
        return recommendations
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get status of the enhanced conversation system."""
        status = {
            "enhanced_mode": NLP_AVAILABLE,
            "active_conversation": self.active_conversation_id,
            "modules": {
                "nlp_module": self.nlp_module is not None,
                "flow_manager": self.flow_manager is not None
            }
        }
        
        if self.flow_manager:
            status["conversation_stats"] = self.flow_manager.get_conversation_stats()
        
        return status
