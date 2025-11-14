#!/usr/bin/env python3
"""
ATLES Intelligent Model Router

Automatically routes requests to the appropriate model type:
- EmbeddingGemma for embedding, similarity, and analysis tasks
- Qwen models for conversation, reasoning, and generation tasks

This enables hybrid AI systems that use the best model for each task.
"""

import logging
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class TaskType(Enum):
    """Types of tasks that can be routed to different models"""
    EMBEDDING = "embedding"
    SIMILARITY = "similarity"
    CLUSTERING = "clustering"
    DOCUMENT_ANALYSIS = "document_analysis"
    SEARCH = "search"
    CONVERSATION = "conversation"
    REASONING = "reasoning"
    CODE_GENERATION = "code_generation"
    TEXT_GENERATION = "text_generation"
    QUESTION_ANSWERING = "question_answering"


class ModelType(Enum):
    """Available model types"""
    EMBEDDING = "embedding"
    GENERATIVE = "generative"


@dataclass
class ModelCapability:
    """Defines what a model is capable of"""
    model_name: str
    model_type: ModelType
    supported_tasks: List[TaskType]
    performance_score: float  # 0.0 to 1.0
    resource_usage: str  # "low", "medium", "high"


@dataclass
class RoutingDecision:
    """Result of routing decision"""
    selected_model: str
    model_type: ModelType
    task_type: TaskType
    confidence: float
    reasoning: str


class IntelligentModelRouter:
    """
    Routes requests to the most appropriate model based on task analysis.
    """
    
    def __init__(self):
        self.models = self._initialize_model_capabilities()
        self.task_patterns = self._initialize_task_patterns()
        self.routing_history = []
        
    def _initialize_model_capabilities(self) -> Dict[str, ModelCapability]:
        """Initialize model capabilities database"""
        return {
            # ATLES fine-tuned models - HIGHEST PRIORITY
            "atles-qwen2.5:7b-enhanced": ModelCapability(
                model_name="atles-qwen2.5:7b-enhanced",
                model_type=ModelType.GENERATIVE,
                supported_tasks=[
                    TaskType.CONVERSATION,
                    TaskType.REASONING,
                    TaskType.TEXT_GENERATION,
                    TaskType.QUESTION_ANSWERING,
                    TaskType.CODE_GENERATION
                ],
                performance_score=0.99,  # Highest score - fine-tuned for ATLES
                resource_usage="high"
            ),
            "atles-llama3.2:latest": ModelCapability(
                model_name="atles-llama3.2:latest",
                model_type=ModelType.GENERATIVE,
                supported_tasks=[
                    TaskType.CONVERSATION,
                    TaskType.REASONING,
                    TaskType.TEXT_GENERATION,
                    TaskType.QUESTION_ANSWERING
                ],
                performance_score=0.97,  # High score - ATLES tuned
                resource_usage="medium"
            ),
            "atles-qwen2.5-coder:latest": ModelCapability(
                model_name="atles-qwen2.5-coder:latest",
                model_type=ModelType.CODE,
                supported_tasks=[
                    TaskType.CODE_GENERATION,
                    TaskType.CODE_ANALYSIS,
                    TaskType.REASONING,
                    TaskType.QUESTION_ANSWERING,
                    TaskType.TEXT_GENERATION
                ],
                performance_score=0.98,  # Coding specialist
                resource_usage="high"
            ),
            "atles-llava:latest": ModelCapability(
                model_name="atles-llava:latest",
                model_type=ModelType.MULTIMODAL,
                supported_tasks=[
                    TaskType.VISION,
                    TaskType.DOCUMENT_ANALYSIS,
                    TaskType.CONVERSATION,
                    TaskType.QUESTION_ANSWERING
                ],
                performance_score=0.96,  # Vision specialist
                resource_usage="high"
            ),
            # Base models
            "qwen2.5:7b": ModelCapability(
                model_name="qwen2.5:7b",
                model_type=ModelType.GENERATIVE,
                supported_tasks=[
                    TaskType.CONVERSATION,
                    TaskType.REASONING,
                    TaskType.CODE_GENERATION,
                    TaskType.TEXT_GENERATION,
                    TaskType.QUESTION_ANSWERING
                ],
                performance_score=0.95,
                resource_usage="high"
            ),
            # NOTE: qwen2.5-coder:latest removed - not installed
            # If you install it later, uncomment this:
            # "qwen2.5-coder:latest": ModelCapability(
            #     model_name="qwen2.5-coder:latest",
            #     model_type=ModelType.GENERATIVE,
            #     supported_tasks=[
            #         TaskType.CODE_GENERATION,
            #         TaskType.REASONING,
            #         TaskType.QUESTION_ANSWERING
            #     ],
            #     performance_score=0.96,  # Lower than ATLES models
            #     resource_usage="high"
            # ),
            # Base models below - only used as fallbacks if ATLES models unavailable
            "llama3.2:3b": ModelCapability(
                model_name="llama3.2:3b",
                model_type=ModelType.GENERATIVE,
                supported_tasks=[
                    TaskType.CONVERSATION,
                    TaskType.REASONING,
                    TaskType.TEXT_GENERATION,
                    TaskType.QUESTION_ANSWERING
                ],
                performance_score=0.85,
                resource_usage="medium"
            )
        }
    
    def _initialize_task_patterns(self) -> Dict[TaskType, List[str]]:
        """Initialize patterns that identify different task types"""
        return {
            TaskType.EMBEDDING: [
                r"embed(?:ding)?",
                r"vector(?:ize)?",
                r"encode",
                r"represent(?:ation)?",
                r"feature extraction"
            ],
            TaskType.SIMILARITY: [
                r"similar(?:ity)?",
                r"compare",
                r"match(?:ing)?",
                r"relate(?:d)?",
                r"distance",
                r"closest",
                r"nearest",
                r"find.*like"
            ],
            TaskType.CLUSTERING: [
                r"cluster(?:ing)?",
                r"group(?:ing)?",
                r"categor(?:ize|y)",
                r"classify",
                r"organize",
                r"sort.*by.*type"
            ],
            TaskType.DOCUMENT_ANALYSIS: [
                r"analyz(?:e|ing).*document",
                r"summariz(?:e|ing)",
                r"extract.*information",
                r"parse.*document",
                r"understand.*content",
                r"review.*document"
            ],
            TaskType.SEARCH: [
                r"search",
                r"find",
                r"lookup",
                r"retrieve",
                r"query",
                r"locate"
            ],
            TaskType.CONVERSATION: [
                r"chat",
                r"talk",
                r"discuss",
                r"conversation",
                r"tell me about",
                r"what do you think",
                r"how are you",
                r"hello",
                r"hi",
                r"respond as",
                r"be a",
                r"act like",
                r"pretend to be",
                r"fable",
                r"poem",
                r"poetry"
            ],
            TaskType.REASONING: [
                r"reason(?:ing)?",
                r"logic(?:al)?",
                r"think(?:ing)?",
                r"solve",
                r"problem",
                r"deduce",
                r"infer",
                r"conclude",
                r"because",
                r"therefore",
                r"why"
            ],
            TaskType.CODE_GENERATION: [
                r"code",
                r"program(?:ming)?",
                r"function",
                r"class",
                r"script",
                r"implement",
                r"write.*python",
                r"create.*function",
                r"debug",
                r"fix.*bug",
                r"algorithm",
                r"variable",
                r"loop",
                r"if.*statement",
                r"def ",
                r"import ",
                r"return ",
                r"console\.log",
                r"print\(",
                r"\.py$",
                r"\.js$",
                r"\.java$",
                r"\.cpp$",
                r"\.c$",
                r"\.html$",
                r"\.css$",
                r"\.sql$",
                r"command",
                r"terminal",
                r"shell",
                r"bash",
                r"powershell"
            ],
            TaskType.TEXT_GENERATION: [
                r"write",
                r"generat(?:e|ing)",
                r"creat(?:e|ing)",
                r"compose",
                r"draft",
                r"story",
                r"article",
                r"essay"
            ],
            TaskType.QUESTION_ANSWERING: [
                r"what",
                r"how",
                r"when",
                r"where",
                r"who",
                r"which",
                r"explain",
                r"describe",
                r"define"
            ]
        }
    
    def analyze_request(self, request: str) -> TaskType:
        """
        Analyze a request to determine the most likely task type.
        """
        request_lower = request.lower()
        task_scores = {}
        
        # Score each task type based on pattern matches
        for task_type, patterns in self.task_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, request_lower))
                score += matches
            
            if score > 0:
                task_scores[task_type] = score
        
        # Return the highest scoring task type
        if task_scores:
            best_task = max(task_scores.items(), key=lambda x: x[1])
            logger.debug(f"Task analysis: '{request[:50]}...' -> {best_task[0]} (score: {best_task[1]})")
            return best_task[0]
        
        # Default to conversation if no patterns match
        logger.debug(f"No specific patterns matched, defaulting to CONVERSATION")
        return TaskType.CONVERSATION
    
    def route_request(self, request: str, available_models: List[str] = None) -> RoutingDecision:
        """
        Route a request to the most appropriate model.
        """
        # Analyze the request to determine task type
        task_type = self.analyze_request(request)
        
        # Filter available models
        if available_models is None:
            available_models = list(self.models.keys())
        
        # Find models that can handle this task type
        suitable_models = []
        for model_name in available_models:
            if model_name in self.models:
                model = self.models[model_name]
                if task_type in model.supported_tasks:
                    suitable_models.append((model_name, model))
        
        if not suitable_models:
            # Fallback to best generative model for unknown tasks
            generative_models = [(name, model) for name, model in self.models.items() 
                               if model.model_type == ModelType.GENERATIVE and name in available_models]
            if generative_models:
                best_model = max(generative_models, key=lambda x: x[1].performance_score)
                return RoutingDecision(
                    selected_model=best_model[0],
                    model_type=best_model[1].model_type,
                    task_type=task_type,
                    confidence=0.5,
                    reasoning=f"No specialized model found for {task_type}, using best generative model"
                )
            else:
                # Ultimate fallback
                fallback_model = available_models[0] if available_models else "qwen2.5:7b"
                return RoutingDecision(
                    selected_model=fallback_model,
                    model_type=ModelType.GENERATIVE,
                    task_type=task_type,
                    confidence=0.3,
                    reasoning="Fallback to first available model"
                )
        
        # Select the best suitable model based on performance score
        best_model = max(suitable_models, key=lambda x: x[1].performance_score)
        
        # Calculate confidence based on task-model match and performance
        confidence = min(0.95, best_model[1].performance_score + 0.1)
        
        decision = RoutingDecision(
            selected_model=best_model[0],
            model_type=best_model[1].model_type,
            task_type=task_type,
            confidence=confidence,
            reasoning=f"Best model for {task_type} tasks with {best_model[1].performance_score:.1%} performance"
        )
        
        # Store routing history
        self.routing_history.append({
            "request": request[:100],
            "decision": decision,
            "timestamp": logger.handlers[0].formatter.formatTime(logger.makeRecord("", 0, "", 0, "", (), None)) if logger.handlers else "unknown"
        })
        
        logger.info(f"Routing decision: {request[:30]}... -> {decision.selected_model} ({decision.confidence:.1%} confidence)")
        return decision
    
    def get_embedding_model(self, available_models: List[str] = None) -> Optional[str]:
        """Get the best available embedding model"""
        if available_models is None:
            available_models = list(self.models.keys())
        
        embedding_models = [
            (name, model) for name, model in self.models.items()
            if model.model_type == ModelType.EMBEDDING and name in available_models
        ]
        
        if embedding_models:
            best = max(embedding_models, key=lambda x: x[1].performance_score)
            return best[0]
        return None
    
    def get_generative_model(self, available_models: List[str] = None, task_type: TaskType = None) -> Optional[str]:
        """Get the best available generative model for a specific task"""
        if available_models is None:
            available_models = list(self.models.keys())
        
        generative_models = [
            (name, model) for name, model in self.models.items()
            if model.model_type == ModelType.GENERATIVE and name in available_models
        ]
        
        if task_type:
            # Filter by task support
            generative_models = [
                (name, model) for name, model in generative_models
                if task_type in model.supported_tasks
            ]
        
        if generative_models:
            best = max(generative_models, key=lambda x: x[1].performance_score)
            return best[0]
        return None
    
    def should_use_embedding_model(self, request: str) -> bool:
        """Quick check if request should use embedding model"""
        task_type = self.analyze_request(request)
        return task_type in [TaskType.EMBEDDING, TaskType.SIMILARITY, TaskType.CLUSTERING, 
                           TaskType.DOCUMENT_ANALYSIS, TaskType.SEARCH]
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """Get statistics about routing decisions"""
        if not self.routing_history:
            return {"total_requests": 0}
        
        model_usage = {}
        task_distribution = {}
        
        for entry in self.routing_history:
            decision = entry["decision"]
            
            # Count model usage
            model_usage[decision.selected_model] = model_usage.get(decision.selected_model, 0) + 1
            
            # Count task distribution
            task_distribution[decision.task_type.value] = task_distribution.get(decision.task_type.value, 0) + 1
        
        return {
            "total_requests": len(self.routing_history),
            "model_usage": model_usage,
            "task_distribution": task_distribution,
            "average_confidence": sum(entry["decision"].confidence for entry in self.routing_history) / len(self.routing_history)
        }


# Convenience functions for easy integration
def create_router() -> IntelligentModelRouter:
    """Create a new intelligent model router"""
    return IntelligentModelRouter()

def route_to_best_model(request: str, available_models: List[str] = None) -> RoutingDecision:
    """Quick routing function"""
    router = create_router()
    return router.route_request(request, available_models)


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Create router
    router = create_router()
    
    # Test requests
    test_requests = [
        "Find documents similar to this one",
        "What is the capital of France?",
        "Write a Python function to sort a list",
        "Analyze this document for key themes",
        "How are you doing today?",
        "Create embeddings for these text samples",
        "Cluster these documents by topic",
        "Explain quantum computing",
        "Generate a story about space travel",
        "Search for information about AI"
    ]
    
    print("🧠 Testing Intelligent Model Router\n")
    
    for request in test_requests:
        decision = router.route_request(request)
        print(f"Request: {request}")
        print(f"  -> Model: {decision.selected_model}")
        print(f"  -> Type: {decision.model_type.value}")
        print(f"  -> Task: {decision.task_type.value}")
        print(f"  -> Confidence: {decision.confidence:.1%}")
        print(f"  -> Reasoning: {decision.reasoning}")
        print()
    
    # Show routing statistics
    stats = router.get_routing_stats()
    print("📊 Routing Statistics:")
    print(f"  Total requests: {stats['total_requests']}")
    print(f"  Average confidence: {stats['average_confidence']:.1%}")
    print(f"  Model usage: {stats['model_usage']}")
    print(f"  Task distribution: {stats['task_distribution']}")
