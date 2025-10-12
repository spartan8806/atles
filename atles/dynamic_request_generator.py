#!/usr/bin/env python3
"""
Dynamic Request Generator for Router Intelligence System
Eliminates hardcoded request lists by generating requests based on system state
"""

import random
import json
from typing import List, Dict, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

class TaskType(Enum):
    """Task types for request generation"""
    EMBEDDING = "embedding"
    CONVERSATION = "conversation"
    CODE_GENERATION = "code_generation"
    SIMILARITY = "similarity"
    ANALYSIS = "analysis"
    OPTIMIZATION = "optimization"
    MEMORY = "memory"
    SEARCH = "search"

@dataclass
class RequestTemplate:
    """Template for generating requests"""
    task_type: TaskType
    templates: List[str]
    context_variables: List[str]
    priority: int = 1

class DynamicRequestGenerator:
    """Generates dynamic requests based on system state and context"""
    
    def __init__(self, system_state: Dict[str, Any] = None, 
                 user_context: Dict[str, Any] = None,
                 task_history: List[Dict[str, Any]] = None,
                 config: Dict[str, Any] = None):
        self.system_state = system_state or {}
        self.user_context = user_context or {}
        self.task_history = task_history or []
        self.config = config or {}
        
        # Initialize request templates
        self._initialize_templates()
        
        # Load configuration
        self._load_config()
    
    def _initialize_templates(self):
        """Initialize request templates for different task types"""
        self.templates = {
            TaskType.EMBEDDING: RequestTemplate(
                task_type=TaskType.EMBEDDING,
                templates=[
                    "Generate embeddings for {document_type}",
                    "Create vector representation of {content_type}",
                    "Process {data_type} for similarity analysis",
                    "Convert {text_type} to embedding space",
                    "Analyze semantic similarity of {content_type}"
                ],
                context_variables=["document_type", "content_type", "data_type", "text_type"]
            ),
            
            TaskType.CONVERSATION: RequestTemplate(
                task_type=TaskType.CONVERSATION,
                templates=[
                    "Respond to user query about {topic}",
                    "Explain {concept} in simple terms",
                    "Help with {problem_type}",
                    "Answer question regarding {subject}",
                    "Provide guidance on {task_type}"
                ],
                context_variables=["topic", "concept", "problem_type", "subject", "task_type"]
            ),
            
            TaskType.CODE_GENERATION: RequestTemplate(
                task_type=TaskType.CODE_GENERATION,
                templates=[
                    "Write {language} function for {functionality}",
                    "Generate code to {action}",
                    "Create {component_type} implementation",
                    "Debug {code_type} issue",
                    "Optimize {algorithm_type} performance"
                ],
                context_variables=["language", "functionality", "action", "component_type", "code_type", "algorithm_type"]
            ),
            
            TaskType.SIMILARITY: RequestTemplate(
                task_type=TaskType.SIMILARITY,
                templates=[
                    "Find documents similar to {reference}",
                    "Compare {item1} with {item2}",
                    "Identify related {content_type}",
                    "Cluster {data_type} by similarity",
                    "Match {pattern_type} patterns"
                ],
                context_variables=["reference", "item1", "item2", "content_type", "data_type", "pattern_type"]
            ),
            
            TaskType.ANALYSIS: RequestTemplate(
                task_type=TaskType.ANALYSIS,
                templates=[
                    "Analyze {data_type} for {analysis_type}",
                    "Extract {feature_type} from {content_type}",
                    "Evaluate {metric_type} performance",
                    "Assess {quality_type} of {item_type}",
                    "Review {document_type} for {review_type}"
                ],
                context_variables=["data_type", "analysis_type", "feature_type", "content_type", "metric_type", "quality_type", "item_type", "document_type", "review_type"]
            ),
            
            TaskType.OPTIMIZATION: RequestTemplate(
                task_type=TaskType.OPTIMIZATION,
                templates=[
                    "Optimize {parameter_type} for {goal_type}",
                    "Improve {performance_type} of {system_type}",
                    "Tune {setting_type} for better {outcome_type}",
                    "Adjust {config_type} to enhance {feature_type}",
                    "Refine {algorithm_type} for {target_type}"
                ],
                context_variables=["parameter_type", "goal_type", "performance_type", "system_type", "setting_type", "outcome_type", "config_type", "feature_type", "algorithm_type", "target_type"]
            ),
            
            TaskType.MEMORY: RequestTemplate(
                task_type=TaskType.MEMORY,
                templates=[
                    "Store {memory_type} in {storage_type}",
                    "Retrieve {information_type} from {source_type}",
                    "Update {record_type} with {data_type}",
                    "Consolidate {memory_type} for {purpose_type}",
                    "Archive {content_type} for {retention_type}"
                ],
                context_variables=["memory_type", "storage_type", "information_type", "source_type", "record_type", "data_type", "purpose_type", "content_type", "retention_type"]
            ),
            
            TaskType.SEARCH: RequestTemplate(
                task_type=TaskType.SEARCH,
                templates=[
                    "Search for {query_type} in {source_type}",
                    "Find {item_type} matching {criteria_type}",
                    "Locate {resource_type} with {attribute_type}",
                    "Discover {pattern_type} in {data_type}",
                    "Query {database_type} for {information_type}"
                ],
                context_variables=["query_type", "source_type", "item_type", "criteria_type", "resource_type", "attribute_type", "pattern_type", "data_type", "database_type", "information_type"]
            )
        }
    
    def _load_config(self):
        """Load configuration for request generation"""
        self.context_values = self.config.get('context_values', {
            "document_type": ["PDF", "text", "code", "log", "config"],
            "content_type": ["data", "text", "code", "images", "audio"],
            "data_type": ["user_data", "system_data", "training_data", "test_data"],
            "text_type": ["query", "response", "document", "comment", "description"],
            "topic": ["AI", "programming", "science", "technology", "business"],
            "concept": ["machine learning", "algorithms", "data structures", "AI safety"],
            "problem_type": ["debugging", "optimization", "integration", "configuration"],
            "subject": ["Python", "JavaScript", "databases", "networking", "security"],
            "task_type": ["development", "testing", "deployment", "maintenance"],
            "language": ["Python", "JavaScript", "Java", "C++", "Go"],
            "functionality": ["sorting", "searching", "filtering", "validation", "transformation"],
            "action": ["process data", "validate input", "generate output", "transform format"],
            "component_type": ["API", "service", "module", "class", "function"],
            "code_type": ["bug", "performance", "security", "compatibility"],
            "algorithm_type": ["sorting", "searching", "optimization", "machine learning"],
            "reference": ["document", "code", "data", "pattern"],
            "item1": ["file", "record", "entry", "item"],
            "item2": ["template", "example", "reference", "standard"],
            "pattern_type": ["usage", "error", "performance", "behavior"],
            "analysis_type": ["trends", "patterns", "anomalies", "performance"],
            "feature_type": ["keywords", "entities", "sentiments", "topics"],
            "metric_type": ["accuracy", "speed", "memory", "reliability"],
            "quality_type": ["accuracy", "completeness", "consistency", "relevance"],
            "item_type": ["data", "code", "document", "response"],
            "review_type": ["quality", "accuracy", "completeness", "clarity"],
            "parameter_type": ["learning rate", "batch size", "timeout", "threshold"],
            "goal_type": ["accuracy", "speed", "efficiency", "reliability"],
            "performance_type": ["speed", "memory", "accuracy", "throughput"],
            "system_type": ["database", "API", "service", "algorithm"],
            "setting_type": ["configuration", "parameters", "options", "preferences"],
            "outcome_type": ["performance", "accuracy", "efficiency", "reliability"],
            "config_type": ["settings", "parameters", "options", "preferences"],
            "target_type": ["accuracy", "speed", "efficiency", "scalability"],
            "memory_type": ["episodic", "semantic", "procedural", "working"],
            "storage_type": ["database", "cache", "file", "memory"],
            "information_type": ["facts", "procedures", "concepts", "experiences"],
            "source_type": ["database", "cache", "file", "API"],
            "record_type": ["user", "session", "transaction", "event"],
            "purpose_type": ["learning", "retrieval", "analysis", "optimization"],
            "retention_type": ["short-term", "long-term", "permanent", "temporary"],
            "query_type": ["information", "data", "documents", "patterns"],
            "criteria_type": ["keywords", "filters", "conditions", "patterns"],
            "resource_type": ["file", "document", "data", "service"],
            "attribute_type": ["name", "type", "size", "date"],
            "database_type": ["SQL", "NoSQL", "graph", "vector"],
            "information_type": ["facts", "procedures", "concepts", "experiences"]
        })
    
    def generate_request(self) -> str:
        """Generate a single dynamic request based on system state"""
        # Select task type based on system state and history
        task_type = self._select_task_type()
        
        # Get template for selected task type
        template = self.templates.get(task_type)
        if not template:
            return "Process system request"
        
        # Select random template
        template_text = random.choice(template.templates)
        
        # Fill in context variables
        request = self._fill_template(template_text, template.context_variables)
        
        return request
    
    def generate_test_requests(self, count: int) -> List[str]:
        """Generate multiple test requests for router testing"""
        requests = []
        
        # Ensure we get a good distribution of task types
        task_types = list(TaskType)
        for i in range(count):
            # Cycle through task types for comprehensive testing
            task_type = task_types[i % len(task_types)]
            template = self.templates.get(task_type)
            
            if template:
                template_text = random.choice(template.templates)
                request = self._fill_template(template_text, template.context_variables)
                requests.append(request)
        
        return requests
    
    def _select_task_type(self) -> TaskType:
        """Select task type based on system state and history"""
        # Analyze recent task history
        recent_tasks = self.task_history[-10:] if self.task_history else []
        
        # Count task types in recent history
        task_counts = {}
        for task in recent_tasks:
            task_type = task.get('type', 'conversation')
            task_counts[task_type] = task_counts.get(task_type, 0) + 1
        
        # Prefer task types that haven't been used recently
        available_types = list(TaskType)
        if task_counts:
            # Weight against recently used types
            weights = []
            for task_type in available_types:
                recent_count = task_counts.get(task_type.value, 0)
                weight = max(1, 10 - recent_count)  # Higher weight for less used types
                weights.append(weight)
            
            return random.choices(available_types, weights=weights)[0]
        
        # If no history, use system state to determine task type
        if self.system_state.get('optimization_active'):
            return random.choice([TaskType.OPTIMIZATION, TaskType.ANALYSIS])
        elif self.system_state.get('memory_consolidation_active'):
            return random.choice([TaskType.MEMORY, TaskType.SIMILARITY])
        elif self.system_state.get('code_generation_active'):
            return TaskType.CODE_GENERATION
        else:
            return random.choice([TaskType.CONVERSATION, TaskType.EMBEDDING, TaskType.SEARCH])
    
    def _fill_template(self, template: str, context_variables: List[str]) -> str:
        """Fill template with context values"""
        filled_template = template
        
        for var in context_variables:
            if f"{{{var}}}" in filled_template:
                # Get context value for this variable
                value = self._get_context_value(var)
                filled_template = filled_template.replace(f"{{{var}}}", value)
        
        return filled_template
    
    def _get_context_value(self, variable: str) -> str:
        """Get context value for a variable"""
        # Check if we have specific context values
        if variable in self.context_values:
            return random.choice(self.context_values[variable])
        
        # Check system state
        if variable in self.system_state:
            return str(self.system_state[variable])
        
        # Check user context
        if variable in self.user_context:
            return str(self.user_context[variable])
        
        # Default fallback
        return f"sample_{variable}"
    
    def update_system_state(self, new_state: Dict[str, Any]):
        """Update system state for better request generation"""
        self.system_state.update(new_state)
    
    def update_user_context(self, new_context: Dict[str, Any]):
        """Update user context for better request generation"""
        self.user_context.update(new_context)
    
    def add_task_to_history(self, task: Dict[str, Any]):
        """Add completed task to history"""
        self.task_history.append({
            **task,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only recent history (last 100 tasks)
        if len(self.task_history) > 100:
            self.task_history = self.task_history[-100:]

# Factory function for easy instantiation
def create_request_generator(system_state: Dict[str, Any] = None,
                           user_context: Dict[str, Any] = None,
                           task_history: List[Dict[str, Any]] = None,
                           config: Dict[str, Any] = None) -> DynamicRequestGenerator:
    """Create a new DynamicRequestGenerator instance"""
    return DynamicRequestGenerator(system_state, user_context, task_history, config)
