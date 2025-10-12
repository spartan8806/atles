"""
ATLES Conversation Flow Manager

Enhanced multi-step conversation capabilities including:
- Conversation state tracking
- Context preservation across turns
- Multi-step task management
- Conversation flow analysis
- Intelligent follow-up suggestions
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)

class ConversationState(Enum):
    """States of a conversation."""
    STARTING = "starting"
    ACTIVE = "active"
    WAITING_FOR_INPUT = "waiting_for_input"
    CLARIFYING = "clarifying"
    EXECUTING = "executing"
    COMPLETED = "completed"
    PAUSED = "paused"
    ERROR = "error"

class TaskStatus(Enum):
    """Status of multi-step tasks."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    WAITING_FOR_USER = "waiting_for_user"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class ConversationTurn:
    """A single turn in the conversation."""
    turn_id: str
    timestamp: datetime
    user_input: str
    ai_response: str
    intent: str
    topics: List[str]
    entities: List[Dict[str, Any]]
    context_used: List[str]
    follow_up_needed: bool = False
    satisfaction_score: Optional[float] = None

@dataclass
class MultiStepTask:
    """A multi-step task being tracked."""
    task_id: str
    title: str
    description: str
    steps: List[Dict[str, Any]]
    current_step: int
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    completion_percentage: float = 0.0
    user_preferences: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.user_preferences is None:
            self.user_preferences = {}

@dataclass
class ConversationFlow:
    """Complete conversation flow tracking."""
    conversation_id: str
    user_id: Optional[str]
    state: ConversationState
    turns: List[ConversationTurn]
    active_tasks: List[MultiStepTask]
    context_memory: Dict[str, Any]
    user_preferences: Dict[str, Any]
    conversation_goals: List[str]
    started_at: datetime
    last_activity: datetime
    
    def __post_init__(self):
        if not self.turns:
            self.turns = []
        if not self.active_tasks:
            self.active_tasks = []
        if not self.context_memory:
            self.context_memory = {}
        if not self.user_preferences:
            self.user_preferences = {}
        if not self.conversation_goals:
            self.conversation_goals = []

class ConversationFlowManager:
    """
    Manages multi-step conversations and task flows.
    
    This system enables ATLES to:
    - Track conversation context across multiple turns
    - Manage complex multi-step tasks
    - Provide intelligent follow-up suggestions
    - Maintain conversation continuity
    - Learn user preferences over time
    """
    
    def __init__(self, storage_path: str = "atles_memory/conversations"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.active_conversations = {}
        self.conversation_templates = self._initialize_templates()
        self.follow_up_strategies = self._initialize_follow_up_strategies()
        
        # Load existing conversations
        self._load_conversations()
    
    def start_conversation(self, user_id: Optional[str] = None, 
                          initial_goals: List[str] = None) -> str:
        """Start a new conversation flow."""
        conversation_id = f"conv_{datetime.now().timestamp()}"
        
        flow = ConversationFlow(
            conversation_id=conversation_id,
            user_id=user_id,
            state=ConversationState.STARTING,
            turns=[],
            active_tasks=[],
            context_memory={},
            user_preferences={},
            conversation_goals=initial_goals or [],
            started_at=datetime.now(),
            last_activity=datetime.now()
        )
        
        self.active_conversations[conversation_id] = flow
        self._save_conversation(flow)
        
        logger.info(f"Started new conversation: {conversation_id}")
        return conversation_id
    
    def add_turn(self, conversation_id: str, user_input: str, ai_response: str,
                 nlp_analysis: Dict[str, Any]) -> ConversationTurn:
        """Add a new turn to the conversation."""
        if conversation_id not in self.active_conversations:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        flow = self.active_conversations[conversation_id]
        
        turn = ConversationTurn(
            turn_id=f"turn_{len(flow.turns) + 1}",
            timestamp=datetime.now(),
            user_input=user_input,
            ai_response=ai_response,
            intent=nlp_analysis.get('intent', 'unknown'),
            topics=nlp_analysis.get('topics', []),
            entities=nlp_analysis.get('entities', []),
            context_used=nlp_analysis.get('context_clues', []),
            follow_up_needed=self._needs_follow_up(user_input, ai_response, nlp_analysis)
        )
        
        flow.turns.append(turn)
        flow.last_activity = datetime.now()
        flow.state = ConversationState.ACTIVE
        
        # Update context memory
        self._update_context_memory(flow, turn)
        
        # Check for multi-step tasks
        self._check_for_multi_step_tasks(flow, turn)
        
        self._save_conversation(flow)
        
        return turn
    
    def create_multi_step_task(self, conversation_id: str, title: str, 
                              description: str, steps: List[Dict[str, Any]]) -> str:
        """Create a new multi-step task."""
        if conversation_id not in self.active_conversations:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        flow = self.active_conversations[conversation_id]
        
        task = MultiStepTask(
            task_id=f"task_{datetime.now().timestamp()}",
            title=title,
            description=description,
            steps=steps,
            current_step=0,
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        flow.active_tasks.append(task)
        flow.state = ConversationState.EXECUTING
        
        self._save_conversation(flow)
        
        logger.info(f"Created multi-step task: {task.task_id} in conversation {conversation_id}")
        return task.task_id
    
    def advance_task_step(self, conversation_id: str, task_id: str, 
                         step_result: Dict[str, Any] = None) -> Dict[str, Any]:
        """Advance a multi-step task to the next step."""
        flow = self.active_conversations.get(conversation_id)
        if not flow:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        task = next((t for t in flow.active_tasks if t.task_id == task_id), None)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        # Record step result
        if step_result:
            task.steps[task.current_step]['result'] = step_result
            task.steps[task.current_step]['completed_at'] = datetime.now().isoformat()
        
        # Advance to next step
        task.current_step += 1
        task.updated_at = datetime.now()
        
        # Update completion percentage
        task.completion_percentage = (task.current_step / len(task.steps)) * 100
        
        # Check if task is complete
        if task.current_step >= len(task.steps):
            task.status = TaskStatus.COMPLETED
            flow.state = ConversationState.COMPLETED
        else:
            task.status = TaskStatus.IN_PROGRESS
        
        self._save_conversation(flow)
        
        return {
            "task_id": task_id,
            "current_step": task.current_step,
            "total_steps": len(task.steps),
            "completion_percentage": task.completion_percentage,
            "status": task.status.value,
            "next_step": task.steps[task.current_step] if task.current_step < len(task.steps) else None
        }
    
    def get_conversation_context(self, conversation_id: str) -> Dict[str, Any]:
        """Get comprehensive conversation context."""
        flow = self.active_conversations.get(conversation_id)
        if not flow:
            return {"error": "Conversation not found"}
        
        # Recent turns for immediate context
        recent_turns = flow.turns[-5:] if len(flow.turns) > 5 else flow.turns
        
        # Active task context
        active_task_context = None
        if flow.active_tasks:
            current_task = flow.active_tasks[-1]  # Most recent task
            if current_task.status in [TaskStatus.IN_PROGRESS, TaskStatus.WAITING_FOR_USER]:
                active_task_context = {
                    "task_id": current_task.task_id,
                    "title": current_task.title,
                    "current_step": current_task.current_step,
                    "total_steps": len(current_task.steps),
                    "next_step": current_task.steps[current_task.current_step] if current_task.current_step < len(current_task.steps) else None,
                    "completion_percentage": current_task.completion_percentage
                }
        
        # Topic continuity
        all_topics = []
        for turn in flow.turns:
            all_topics.extend(turn.topics)
        
        topic_frequency = {}
        for topic in all_topics:
            topic_frequency[topic] = topic_frequency.get(topic, 0) + 1
        
        main_topics = sorted(topic_frequency.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "conversation_id": conversation_id,
            "state": flow.state.value,
            "turn_count": len(flow.turns),
            "recent_turns": [
                {
                    "user_input": turn.user_input,
                    "ai_response": turn.ai_response,
                    "intent": turn.intent,
                    "topics": turn.topics
                }
                for turn in recent_turns
            ],
            "active_task": active_task_context,
            "main_topics": [topic for topic, count in main_topics],
            "context_memory": flow.context_memory,
            "user_preferences": flow.user_preferences,
            "conversation_goals": flow.conversation_goals,
            "duration_minutes": (datetime.now() - flow.started_at).total_seconds() / 60
        }
    
    def suggest_follow_ups(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Suggest intelligent follow-up actions or questions."""
        flow = self.active_conversations.get(conversation_id)
        if not flow or not flow.turns:
            return []
        
        suggestions = []
        last_turn = flow.turns[-1]
        
        # Task-based follow-ups
        if flow.active_tasks:
            current_task = flow.active_tasks[-1]
            if current_task.status == TaskStatus.IN_PROGRESS:
                next_step = current_task.steps[current_task.current_step]
                suggestions.append({
                    "type": "task_continuation",
                    "text": f"Ready to continue with: {next_step.get('title', 'next step')}?",
                    "priority": "high"
                })
        
        # Intent-based follow-ups
        intent_strategies = self.follow_up_strategies.get(last_turn.intent, [])
        for strategy in intent_strategies:
            suggestions.append({
                "type": "intent_based",
                "text": strategy,
                "priority": "medium"
            })
        
        # Topic-based follow-ups
        if last_turn.topics:
            for topic in last_turn.topics[:2]:  # Top 2 topics
                suggestions.append({
                    "type": "topic_exploration",
                    "text": f"Would you like to explore more about {topic}?",
                    "priority": "low"
                })
        
        # Unresolved questions
        unresolved = [turn for turn in flow.turns if turn.follow_up_needed and not turn.satisfaction_score]
        if unresolved:
            suggestions.append({
                "type": "clarification",
                "text": "I noticed some questions might need more clarification. Shall we revisit them?",
                "priority": "medium"
            })
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    def _initialize_templates(self) -> Dict[str, Any]:
        """Initialize conversation templates for common flows."""
        return {
            "system_upgrade": {
                "title": "System Upgrade Process",
                "steps": [
                    {"title": "Analyze current capabilities", "type": "analysis"},
                    {"title": "Identify improvement areas", "type": "planning"},
                    {"title": "Design upgrade architecture", "type": "design"},
                    {"title": "Implement upgrades", "type": "implementation"},
                    {"title": "Test and validate", "type": "testing"},
                    {"title": "Deploy and monitor", "type": "deployment"}
                ]
            },
            "problem_solving": {
                "title": "Problem Solving Process",
                "steps": [
                    {"title": "Define the problem", "type": "analysis"},
                    {"title": "Gather information", "type": "research"},
                    {"title": "Generate solutions", "type": "brainstorming"},
                    {"title": "Evaluate options", "type": "evaluation"},
                    {"title": "Implement solution", "type": "implementation"},
                    {"title": "Monitor results", "type": "monitoring"}
                ]
            },
            "learning_session": {
                "title": "Learning Session",
                "steps": [
                    {"title": "Assess current knowledge", "type": "assessment"},
                    {"title": "Set learning objectives", "type": "planning"},
                    {"title": "Provide explanations", "type": "teaching"},
                    {"title": "Practice exercises", "type": "practice"},
                    {"title": "Review and reinforce", "type": "review"}
                ]
            }
        }
    
    def _initialize_follow_up_strategies(self) -> Dict[str, List[str]]:
        """Initialize follow-up strategies for different intents."""
        return {
            "question": [
                "Does that answer your question completely?",
                "Would you like me to explain any part in more detail?",
                "Do you have any related questions?"
            ],
            "request": [
                "Is this what you were looking for?",
                "Would you like me to modify or expand on this?",
                "Shall we proceed to the next step?"
            ],
            "command": [
                "The command has been executed. Would you like to see the results?",
                "Is there anything else you'd like me to do with this?",
                "Shall we continue with the next action?"
            ],
            "conversation": [
                "What are your thoughts on this?",
                "Would you like to explore this topic further?",
                "Is there anything specific you'd like to know more about?"
            ]
        }
    
    def _needs_follow_up(self, user_input: str, ai_response: str, 
                        nlp_analysis: Dict[str, Any]) -> bool:
        """Determine if this turn needs a follow-up."""
        # Check for incomplete responses
        if "..." in ai_response or len(ai_response) < 50:
            return True
        
        # Check for questions in user input that might need clarification
        if "?" in user_input and nlp_analysis.get('confidence', 0) < 0.7:
            return True
        
        # Check for complex topics that might benefit from follow-up
        topics = nlp_analysis.get('topics', [])
        complex_topics = ['programming', 'ai_ml', 'system', 'security']
        if any(topic in complex_topics for topic in topics):
            return True
        
        return False
    
    def _update_context_memory(self, flow: ConversationFlow, turn: ConversationTurn):
        """Update conversation context memory."""
        # Store important entities
        for entity in turn.entities:
            entity_type = entity.get('type')
            entity_value = entity.get('value')
            if entity_type and entity_value:
                if entity_type not in flow.context_memory:
                    flow.context_memory[entity_type] = []
                if entity_value not in flow.context_memory[entity_type]:
                    flow.context_memory[entity_type].append(entity_value)
        
        # Store topic preferences
        for topic in turn.topics:
            if 'preferred_topics' not in flow.user_preferences:
                flow.user_preferences['preferred_topics'] = {}
            
            current_count = flow.user_preferences['preferred_topics'].get(topic, 0)
            flow.user_preferences['preferred_topics'][topic] = current_count + 1
        
        # Store conversation patterns
        if 'interaction_patterns' not in flow.context_memory:
            flow.context_memory['interaction_patterns'] = []
        
        pattern = {
            "intent": turn.intent,
            "topics": turn.topics,
            "timestamp": turn.timestamp.isoformat(),
            "response_length": len(turn.ai_response)
        }
        
        flow.context_memory['interaction_patterns'].append(pattern)
        
        # Limit memory size
        if len(flow.context_memory['interaction_patterns']) > 50:
            flow.context_memory['interaction_patterns'] = flow.context_memory['interaction_patterns'][-50:]
    
    def _check_for_multi_step_tasks(self, flow: ConversationFlow, turn: ConversationTurn):
        """Check if the current turn indicates a multi-step task."""
        # Keywords that suggest multi-step processes
        multi_step_indicators = [
            "upgrade", "improve", "enhance", "implement", "create", "build",
            "develop", "design", "plan", "analyze", "solve", "fix", "debug"
        ]
        
        user_input_lower = turn.user_input.lower()
        
        # Check for multi-step indicators
        for indicator in multi_step_indicators:
            if indicator in user_input_lower:
                # Check if we have a template for this type of task
                if indicator in ["upgrade", "improve", "enhance"]:
                    template = self.conversation_templates["system_upgrade"]
                elif indicator in ["solve", "fix", "debug"]:
                    template = self.conversation_templates["problem_solving"]
                elif indicator in ["learn", "explain", "teach"]:
                    template = self.conversation_templates["learning_session"]
                else:
                    continue  # No template available
                
                # Create task if none exists for this conversation
                if not flow.active_tasks or all(task.status == TaskStatus.COMPLETED for task in flow.active_tasks):
                    task_id = self.create_multi_step_task(
                        flow.conversation_id,
                        template["title"],
                        f"Multi-step {indicator} process based on user request",
                        template["steps"]
                    )
                    logger.info(f"Auto-created multi-step task: {task_id}")
                break
    
    def _save_conversation(self, flow: ConversationFlow):
        """Save conversation to persistent storage."""
        try:
            file_path = self.storage_path / f"{flow.conversation_id}.json"
            
            # Convert to serializable format
            data = asdict(flow)
            
            # Handle datetime serialization
            data['started_at'] = flow.started_at.isoformat()
            data['last_activity'] = flow.last_activity.isoformat()
            
            for turn in data['turns']:
                turn['timestamp'] = datetime.fromisoformat(turn['timestamp']).isoformat() if isinstance(turn['timestamp'], str) else turn['timestamp'].isoformat()
            
            for task in data['active_tasks']:
                task['created_at'] = datetime.fromisoformat(task['created_at']).isoformat() if isinstance(task['created_at'], str) else task['created_at'].isoformat()
                task['updated_at'] = datetime.fromisoformat(task['updated_at']).isoformat() if isinstance(task['updated_at'], str) else task['updated_at'].isoformat()
            
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"Failed to save conversation {flow.conversation_id}: {e}")
    
    def _load_conversations(self):
        """Load existing conversations from storage."""
        try:
            for file_path in self.storage_path.glob("*.json"):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                # Convert back from serialized format
                flow = ConversationFlow(**data)
                
                # Handle datetime deserialization
                flow.started_at = datetime.fromisoformat(data['started_at'])
                flow.last_activity = datetime.fromisoformat(data['last_activity'])
                
                # Only load recent conversations (last 7 days)
                if (datetime.now() - flow.last_activity).days <= 7:
                    self.active_conversations[flow.conversation_id] = flow
                    
        except Exception as e:
            logger.error(f"Failed to load conversations: {e}")
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get statistics about all conversations."""
        total_conversations = len(self.active_conversations)
        total_turns = sum(len(flow.turns) for flow in self.active_conversations.values())
        active_tasks = sum(len(flow.active_tasks) for flow in self.active_conversations.values())
        
        # State distribution
        state_counts = {}
        for flow in self.active_conversations.values():
            state = flow.state.value
            state_counts[state] = state_counts.get(state, 0) + 1
        
        return {
            "total_conversations": total_conversations,
            "total_turns": total_turns,
            "active_tasks": active_tasks,
            "state_distribution": state_counts,
            "average_turns_per_conversation": total_turns / max(total_conversations, 1)
        }

