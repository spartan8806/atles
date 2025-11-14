"""
ATLES v0.5: Advanced Tool System

This module implements a comprehensive tool system for:
- Function calling and task execution
- Tool discovery and registration
- Safety and validation
- Tool chaining and composition
"""

import asyncio
import logging
import json
import inspect
import hashlib
from typing import Any, Dict, List, Optional, Union, Callable, Type, get_type_hints
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
from enum import Enum
import uuid
import traceback
import re

logger = logging.getLogger(__name__)


class ToolCategory(Enum):
    """Categories for organizing tools."""
    UTILITY = "utility"
    COMMUNICATION = "communication"
    DATA_PROCESSING = "data_processing"
    FILE_OPERATIONS = "file_operations"
    NETWORK = "network"
    SYSTEM = "system"
    AI_MODELS = "ai_models"
    CUSTOM = "custom"


class SafetyLevel(Enum):
    """Safety levels for tools."""
    SAFE = "safe"           # No side effects, read-only
    MODERATE = "moderate"   # Some side effects, controlled
    DANGEROUS = "dangerous" # High risk, requires confirmation


@dataclass
class ToolParameter:
    """Definition of a tool parameter."""
    name: str
    type: Type
    description: str
    required: bool = True
    default: Any = None
    constraints: Optional[Dict[str, Any]] = None
    examples: List[Any] = field(default_factory=list)


@dataclass
class ToolResult:
    """Result of a tool execution."""
    success: bool
    result: Any
    execution_time: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    tool_name: str = ""
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ToolExecution:
    """Record of a tool execution."""
    execution_id: str
    tool_name: str
    parameters: Dict[str, Any]
    result: ToolResult
    user_id: str
    session_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    context: Dict[str, Any] = field(default_factory=dict)


class ToolValidator:
    """Validates tool parameters and execution safety."""
    
    def __init__(self):
        self.safety_rules: Dict[str, Callable] = {}
        self.parameter_validators: Dict[str, Callable] = {}
    
    def add_safety_rule(self, rule_name: str, rule_function: Callable):
        """Add a custom safety rule."""
        self.safety_rules[rule_name] = rule_function
        logger.info(f"Added safety rule: {rule_name}")
    
    def add_parameter_validator(self, type_name: str, validator: Callable):
        """Add a custom parameter validator."""
        self.parameter_validators[type_name] = validator
        logger.info(f"Added parameter validator for: {type_name}")
    
    def validate_parameters(self, tool_name: str, parameters: Dict[str, Any], parameter_defs: List[ToolParameter]) -> Dict[str, Any]:
        """Validate tool parameters."""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "validated_parameters": {}
        }
        
        for param_def in parameter_defs:
            param_name = param_def.name
            param_value = parameters.get(param_name)
            
            # Check if required parameter is missing
            if param_def.required and param_name not in parameters:
                validation_result["valid"] = False
                validation_result["errors"].append(f"Required parameter '{param_name}' is missing")
                continue
            
            # Use default value if parameter is missing
            if param_name not in parameters and param_def.default is not None:
                param_value = param_def.default
            
            # Type validation
            if param_value is not None:
                try:
                    if param_def.type == str:
                        param_value = str(param_value)
                    elif param_def.type == int:
                        param_value = int(param_value)
                    elif param_def.type == float:
                        param_value = float(param_value)
                    elif param_def.type == bool:
                        if isinstance(param_value, str):
                            param_value = param_value.lower() in ('true', '1', 'yes', 'on')
                        else:
                            param_value = bool(param_value)
                    elif param_def.type == list:
                        if not isinstance(param_value, list):
                            param_value = [param_value]
                    elif param_def.type == dict:
                        if not isinstance(param_value, dict):
                            param_value = {}
                    
                    # Custom validation if available
                    if param_def.constraints:
                        validation_result = self._apply_constraints(
                            param_name, param_value, param_def.constraints, validation_result
                        )
                    
                    validation_result["validated_parameters"][param_name] = param_value
                    
                except (ValueError, TypeError) as e:
                    validation_result["valid"] = False
                    validation_result["errors"].append(f"Parameter '{param_name}' type conversion failed: {e}")
        
        return validation_result
    
    def _apply_constraints(self, param_name: str, value: Any, constraints: Dict[str, Any], validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Apply parameter constraints."""
        if "min" in constraints and hasattr(value, '__lt__'):
            if value < constraints["min"]:
                validation_result["valid"] = False
                validation_result["errors"].append(f"Parameter '{param_name}' value {value} is below minimum {constraints['min']}")
        
        if "max" in constraints and hasattr(value, '__gt__'):
            if value > constraints["max"]:
                validation_result["valid"] = False
                validation_result["errors"].append(f"Parameter '{param_name}' value {value} is above maximum {constraints['max']}")
        
        if "min_length" in constraints and hasattr(value, '__len__'):
            if len(value) < constraints["min_length"]:
                validation_result["valid"] = False
                validation_result["errors"].append(f"Parameter '{param_name}' length {len(value)} is below minimum {constraints['min_length']}")
        
        if "max_length" in constraints and hasattr(value, '__len__'):
            if len(value) > constraints["max_length"]:
                validation_result["valid"] = False
                validation_result["errors"].append(f"Parameter '{param_name}' length {len(value)} is above maximum {constraints['max_length']}")
        
        if "pattern" in constraints and isinstance(value, str):
            import re
            if not re.match(constraints["pattern"], value):
                validation_result["valid"] = False
                validation_result["errors"].append(f"Parameter '{param_name}' value '{value}' doesn't match pattern {constraints['pattern']}")
        
        if "choices" in constraints:
            if value not in constraints["choices"]:
                validation_result["valid"] = False
                validation_result["errors"].append(f"Parameter '{param_name}' value '{value}' is not in allowed choices {constraints['choices']}")
        
        return validation_result
    
    def check_safety(self, tool_name: str, parameters: Dict[str, Any], safety_level: SafetyLevel) -> Dict[str, Any]:
        """Check tool execution safety."""
        safety_result = {
            "safe_to_execute": True,
            "warnings": [],
            "blocked": False,
            "reason": ""
        }
        
        # Basic safety checks based on safety level
        if safety_level == SafetyLevel.DANGEROUS:
            safety_result["warnings"].append(f"Tool '{tool_name}' has DANGEROUS safety level")
            safety_result["safe_to_execute"] = False
            safety_result["blocked"] = True
            safety_result["reason"] = "Tool marked as dangerous"
        
        elif safety_level == SafetyLevel.MODERATE:
            safety_result["warnings"].append(f"Tool '{tool_name}' has MODERATE safety level - proceed with caution")
        
        # Apply custom safety rules
        for rule_name, rule_func in self.safety_rules.items():
            try:
                rule_result = rule_func(tool_name, parameters)
                if not rule_result.get("safe", True):
                    safety_result["safe_to_execute"] = False
                    safety_result["warnings"].append(f"Safety rule '{rule_name}' failed: {rule_result.get('reason', 'Unknown')}")
            except Exception as e:
                logger.warning(f"Safety rule '{rule_name}' failed: {e}")
                safety_result["warnings"].append(f"Safety rule '{rule_name}' evaluation failed")
        
        return safety_result


class AdvancedTool:
    """Advanced tool with comprehensive capabilities."""
    
    def __init__(
        self,
        name: str,
        description: str,
        function: Callable,
        category: ToolCategory = ToolCategory.UTILITY,
        safety_level: SafetyLevel = SafetyLevel.SAFE,
        parameters: Optional[List[ToolParameter]] = None,
        examples: List[Dict[str, Any]] = None,
        tags: List[str] = None,
        version: str = "1.0.0"
    ):
        self.name = name
        self.description = description
        self.function = function
        self.category = category
        self.safety_level = safety_level
        self.parameters = parameters or self._extract_parameters(function)
        self.examples = examples or []
        self.tags = tags or []
        self.version = version
        self.usage_count = 0
        self.success_count = 0
        self.last_used: Optional[datetime] = None
        
        # Generate tool ID
        self.tool_id = self._generate_tool_id()
        
        logger.info(f"Created advanced tool: {name} (ID: {self.tool_id})")
    
    def _extract_parameters(self, func: Callable) -> List[ToolParameter]:
        """Extract parameter information from function signature."""
        parameters = []
        sig = inspect.signature(func)
        
        for param_name, param in sig.parameters.items():
            if param_name in ['self', 'cls']:
                continue
            
            # Get type hint
            param_type = param.annotation
            if param_type == inspect.Parameter.empty:
                param_type = str  # Default to string
            
            # Determine if required
            required = param.default == inspect.Parameter.empty
            
            # Get default value
            default = param.default if param.default != inspect.Parameter.empty else None
            
            # Create parameter definition
            param_def = ToolParameter(
                name=param_name,
                type=param_type,
                description=f"Parameter {param_name}",
                required=required,
                default=default
            )
            parameters.append(param_def)
        
        return parameters
    
    def _generate_tool_id(self) -> str:
        """Generate unique tool ID."""
        content = f"{self.name}:{self.description}:{self.version}"
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    async def execute(
        self, 
        parameters: Dict[str, Any], 
        user_id: str, 
        session_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> ToolResult:
        """Execute the tool with given parameters."""
        start_time = datetime.now()
        
        try:
            # Update usage statistics
            self.usage_count += 1
            self.last_used = datetime.now()
            
            # Validate parameters
            validator = ToolValidator()
            validation = validator.validate_parameters(self.name, parameters, self.parameters)
            
            if not validation["valid"]:
                return ToolResult(
                    success=False,
                    result=None,
                    execution_time=0.0,
                    error_message=f"Parameter validation failed: {'; '.join(validation['errors'])}",
                    tool_name=self.name
                )
            
            # Check safety
            safety_check = validator.check_safety(self.name, validation["validated_parameters"], self.safety_level)
            if not safety_check["safe_to_execute"]:
                return ToolResult(
                    success=False,
                    result=None,
                    execution_time=0.0,
                    error_message=f"Safety check failed: {safety_check['reason']}",
                    tool_name=self.name
                )
            
            # Execute function
            if asyncio.iscoroutinefunction(self.function):
                result = await self.function(**validation["validated_parameters"])
            else:
                result = self.function(**validation["validated_parameters"])
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Update success statistics
            self.success_count += 1
            
            return ToolResult(
                success=True,
                result=result,
                execution_time=execution_time,
                metadata={
                    "tool_id": self.tool_id,
                    "category": self.category.value,
                    "safety_level": self.safety_level.value,
                    "parameters_used": validation["validated_parameters"],
                    "warnings": safety_check["warnings"]
                },
                tool_name=self.name
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"Tool execution failed for {self.name}: {e}")
            
            return ToolResult(
                success=False,
                result=None,
                execution_time=execution_time,
                error_message=str(e),
                tool_name=self.name,
                metadata={
                    "tool_id": self.tool_id,
                    "category": self.category.value,
                    "safety_level": self.safety_level.value,
                    "traceback": traceback.format_exc()
                }
            )
    
    def get_info(self) -> Dict[str, Any]:
        """Get comprehensive tool information."""
        return {
            "tool_id": self.tool_id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "safety_level": self.safety_level.value,
            "version": self.version,
            "parameters": [
                {
                    "name": p.name,
                    "type": p.type.__name__,
                    "description": p.description,
                    "required": p.required,
                    "default": p.default,
                    "constraints": p.constraints
                }
                for p in self.parameters
            ],
            "examples": self.examples,
            "tags": self.tags,
            "usage_stats": {
                "total_usage": self.usage_count,
                "successful_executions": self.success_count,
                "success_rate": self.success_count / max(self.usage_count, 1),
                "last_used": self.last_used.isoformat() if self.last_used else None
            }
        }


class ToolChain:
    """Chain multiple tools together for complex operations."""
    
    def __init__(self, chain_id: str, name: str, description: str):
        self.chain_id = chain_id
        self.name = name
        self.description = description
        self.steps: List[Dict[str, Any]] = []
        self.conditional_logic: Dict[str, Any] = {}
        self.error_handling: Dict[str, Any] = {}
        
    def add_step(self, tool_name: str, parameters: Dict[str, Any], step_name: str = None) -> str:
        """Add a step to the tool chain."""
        step_id = str(uuid.uuid4())
        step = {
            "step_id": step_id,
            "step_name": step_name or f"Step {len(self.steps) + 1}",
            "tool_name": tool_name,
            "parameters": parameters,
            "order": len(self.steps),
            "conditional": None,
            "error_handling": None
        }
        
        self.steps.append(step)
        return step_id
    
    def add_conditional_step(self, tool_name: str, parameters: Dict[str, Any], condition: str, step_name: str = None) -> str:
        """Add a conditional step to the tool chain."""
        step_id = self.add_step(tool_name, parameters, step_name)
        
        # Find the step and add conditional logic
        for step in self.steps:
            if step["step_id"] == step_id:
                step["conditional"] = condition
                break
        
        return step_id
    
    def add_error_handling(self, step_id: str, error_condition: str, fallback_tool: str, fallback_parameters: Dict[str, Any]):
        """Add error handling for a specific step."""
        for step in self.steps:
            if step["step_id"] == step_id:
                step["error_handling"] = {
                    "error_condition": error_condition,
                    "fallback_tool": fallback_tool,
                    "fallback_parameters": fallback_parameters
                }
                break
    
    async def execute(
        self, 
        tool_registry: 'AdvancedToolRegistry',
        initial_context: Dict[str, Any],
        user_id: str,
        session_id: str
    ) -> Dict[str, Any]:
        """Execute the tool chain."""
        chain_result = {
            "chain_id": self.chain_id,
            "success": True,
            "steps_executed": [],
            "final_result": None,
            "execution_time": 0.0,
            "errors": []
        }
        
        start_time = datetime.now()
        current_context = initial_context.copy()
        
        for step in self.steps:
            try:
                # Check conditional execution
                if step["conditional"] and not self._evaluate_condition(step["conditional"], current_context):
                    chain_result["steps_executed"].append({
                        "step_id": step["step_id"],
                        "step_name": step["step_name"],
                        "status": "skipped",
                        "reason": "Condition not met"
                    })
                    continue
                
                # Execute the step
                tool = tool_registry.get_tool(step["tool_name"])
                if not tool:
                    error_msg = f"Tool '{step['tool_name']}' not found"
                    chain_result["errors"].append(error_msg)
                    
                    # Try error handling
                    if step["error_handling"]:
                        fallback_result = await self._execute_fallback(
                            step["error_handling"], tool_registry, current_context, user_id, session_id
                        )
                        if fallback_result["success"]:
                            current_context.update(fallback_result["result"])
                            chain_result["steps_executed"].append({
                                "step_id": step["step_id"],
                                "step_name": step["step_name"],
                                "status": "fallback_executed",
                                "fallback_result": fallback_result
                            })
                            continue
                    
                    chain_result["success"] = False
                    break
                
                # Execute tool
                tool_result = await tool.execute(step["parameters"], user_id, session_id, current_context)
                
                if tool_result.success:
                    # Update context with result
                    current_context[f"step_{step['step_id']}_result"] = tool_result.result
                    current_context[f"step_{step['step_id']}_metadata"] = tool_result.metadata
                    
                    chain_result["steps_executed"].append({
                        "step_id": step["step_id"],
                        "step_name": step["step_name"],
                        "status": "success",
                        "result": tool_result.result,
                        "execution_time": tool_result.execution_time
                    })
                else:
                    # Handle tool execution failure
                    error_msg = f"Step '{step['step_name']}' failed: {tool_result.error_message}"
                    chain_result["errors"].append(error_msg)
                    
                    # Try error handling
                    if step["error_handling"]:
                        fallback_result = await self._execute_fallback(
                            step["error_handling"], tool_registry, current_context, user_id, session_id
                        )
                        if fallback_result["success"]:
                            current_context.update(fallback_result["result"])
                            chain_result["steps_executed"].append({
                                "step_id": step["step_id"],
                                "step_name": step["step_name"],
                                "status": "fallback_executed",
                                "fallback_result": fallback_result
                            })
                            continue
                    
                    chain_result["success"] = False
                    break
                
            except Exception as e:
                error_msg = f"Unexpected error in step '{step['step_name']}': {e}"
                chain_result["errors"].append(error_msg)
                chain_result["success"] = False
                break
        
        # Calculate total execution time
        chain_result["execution_time"] = (datetime.now() - start_time).total_seconds()
        chain_result["final_result"] = current_context
        
        return chain_result
    
    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """Evaluate a conditional expression."""
        try:
            # Simple condition evaluation - in production, use a proper expression parser
            if "==" in condition:
                key, value = condition.split("==", 1)
                return str(context.get(key.strip(), "")).strip() == value.strip()
            elif "!=" in condition:
                key, value = condition.split("!=", 1)
                return str(context.get(key.strip(), "")).strip() != value.strip()
            elif "in" in condition:
                key, value = condition.split(" in ", 1)
                return str(value.strip()) in str(context.get(key.strip(), ""))
            else:
                # Default to checking if value exists and is truthy
                return bool(context.get(condition.strip(), False))
        except Exception:
            logger.warning(f"Failed to evaluate condition: {condition}")
            return False
    
    async def _execute_fallback(
        self, 
        error_handling: Dict[str, Any], 
        tool_registry: 'AdvancedToolRegistry',
        context: Dict[str, Any],
        user_id: str,
        session_id: str
    ) -> Dict[str, Any]:
        """Execute fallback tool for error handling."""
        try:
            fallback_tool = tool_registry.get_tool(error_handling["fallback_tool"])
            if fallback_tool:
                result = await fallback_tool.execute(
                    error_handling["fallback_parameters"], 
                    user_id, 
                    session_id, 
                    context
                )
                return {
                    "success": result.success,
                    "result": result.result if result.success else {},
                    "error": result.error_message if not result.success else None
                }
        except Exception as e:
            logger.error(f"Fallback execution failed: {e}")
        
        return {"success": False, "result": {}, "error": "Fallback execution failed"}


class AdvancedToolRegistry:
    """Advanced registry for managing tools and tool chains."""
    
    def __init__(self):
        self.tools: Dict[str, AdvancedTool] = {}
        self.tool_chains: Dict[str, ToolChain] = {}
        self.categories: Dict[str, List[str]] = {}
        self.execution_history: List[ToolExecution] = []
        self.validator = ToolValidator()
        
        # Register built-in tools
        self._register_builtin_tools()
    
    def _register_builtin_tools(self):
        """Register built-in utility tools."""
        # Text processing tools
        text_tools = [
            AdvancedTool(
                name="text_analyzer",
                description="Analyze text for sentiment, topics, and key information",
                function=self._text_analyzer,
                category=ToolCategory.DATA_PROCESSING,
                safety_level=SafetyLevel.SAFE,
                examples=[
                    {"text": "I love this product!", "analysis_type": "sentiment"},
                    {"text": "Python programming language", "analysis_type": "topics"}
                ]
            ),
            AdvancedTool(
                name="text_summarizer",
                description="Generate concise summaries of text content",
                function=self._text_summarizer,
                category=ToolCategory.DATA_PROCESSING,
                safety_level=SafetyLevel.SAFE,
                parameters=[
                    ToolParameter("text", str, "Text to summarize", True),
                    ToolParameter("max_length", int, "Maximum summary length", False, 100),
                    ToolParameter("style", str, "Summary style", False, "concise")
                ]
            )
        ]
        
        for tool in text_tools:
            self.register_tool(tool)
    
    def register_tool(self, tool: AdvancedTool):
        """Register a new tool."""
        self.tools[tool.name] = tool
        
        # Add to categories
        category = tool.category.value
        if category not in self.categories:
            self.categories[category] = []
        if tool.name not in self.categories[category]:
            self.categories[category].append(tool.name)
        
        logger.info(f"Registered tool: {tool.name} in category {category}")
    
    def register_tool_chain(self, tool_chain: ToolChain):
        """Register a new tool chain."""
        self.tool_chains[tool_chain.chain_id] = tool_chain
        logger.info(f"Registered tool chain: {tool_chain.name} (ID: {tool_chain.chain_id})")
    
    def get_tool(self, name: str) -> Optional[AdvancedTool]:
        """Get a tool by name."""
        return self.tools.get(name)
    
    def get_tool_chain(self, chain_id: str) -> Optional[ToolChain]:
        """Get a tool chain by ID."""
        return self.tool_chains.get(chain_id)
    
    def get_tools_by_category(self, category: str) -> List[AdvancedTool]:
        """Get all tools in a category."""
        tool_names = self.categories.get(category, [])
        return [self.tools[name] for name in tool_names if name in self.tools]
    
    def search_tools(self, query: str, category: Optional[str] = None) -> List[AdvancedTool]:
        """Search for tools by query."""
        results = []
        search_query = query.lower()
        
        for tool in self.tools.values():
            if category and tool.category.value != category:
                continue
            
            # Search in name, description, and tags
            if (search_query in tool.name.lower() or 
                search_query in tool.description.lower() or
                any(search_query in tag.lower() for tag in tool.tags)):
                results.append(tool)
        
        return results
    
    def list_available_tools(self) -> Dict[str, List[Dict[str, Any]]]:
        """List all available tools organized by category."""
        result = {}
        for category, tool_names in self.categories.items():
            result[category] = [
                {
                    "name": self.tools[tool_name].name,
                    "description": self.tools[tool_name].description,
                    "safety_level": self.tools[tool_name].safety_level.value,
                    "version": self.tools[tool_name].version,
                    "usage_stats": self.tools[tool_name].get_info()["usage_stats"]
                }
                for tool_name in tool_names
                if tool_name in self.tools
            ]
        return result
    
    def get_execution_history(self, limit: int = 100) -> List[ToolExecution]:
        """Get recent tool execution history."""
        return self.execution_history[-limit:]
    
    def record_execution(self, execution: ToolExecution):
        """Record a tool execution."""
        self.execution_history.append(execution)
        
        # Keep history manageable
        if len(self.execution_history) > 1000:
            self.execution_history = self.execution_history[-500:]
    
    # Built-in tool implementations
    def _text_analyzer(self, text: str, analysis_type: str = "general") -> Dict[str, Any]:
        """Analyze text for various characteristics."""
        result = {
            "text_length": len(text),
            "word_count": len(text.split()),
            "analysis_type": analysis_type
        }
        
        if analysis_type == "sentiment":
            # Simple sentiment analysis
            positive_words = ["good", "great", "excellent", "love", "like", "happy", "wonderful"]
            negative_words = ["bad", "terrible", "hate", "dislike", "awful", "horrible"]
            
            text_lower = text.lower()
            positive_count = sum(1 for word in positive_words if word in text_lower)
            negative_count = sum(1 for word in word in negative_words if word in text_lower)
            
            if positive_count > negative_count:
                result["sentiment"] = "positive"
                result["sentiment_score"] = positive_count - negative_count
            elif negative_count > positive_count:
                result["sentiment"] = "negative"
                result["sentiment_score"] = negative_count - positive_count
            else:
                result["sentiment"] = "neutral"
                result["sentiment_score"] = 0
        
        elif analysis_type == "topics":
            # Simple topic extraction
            common_topics = ["python", "programming", "ai", "machine learning", "data", "analysis"]
            text_lower = text.lower()
            found_topics = [topic for topic in common_topics if topic in text_lower]
            result["topics"] = found_topics
        
        return result
    
    def _text_summarizer(self, text: str, max_length: int = 100, style: str = "concise") -> Dict[str, Any]:
        """Generate text summary."""
        words = text.split()
        
        if len(words) <= max_length:
            summary = text
        else:
            # Simple truncation - in production, use proper summarization
            summary = " ".join(words[:max_length]) + "..."
        
        return {
            "original_length": len(text),
            "summary_length": len(summary),
            "summary": summary,
            "style": style,
            "compression_ratio": len(summary) / len(text) if text else 0
        }

    def _math_calculator(self, expression: str) -> Dict[str, Any]:
        """
        Calculate mathematical expressions safely.
        
        Args:
            expression: Mathematical expression as string (e.g., "2+2", "10/2")
            
        Returns:
            Calculation result with safety validation
        """
        try:
            # Clean the expression - only allow safe math operations
            import re
            
            # Remove any non-math characters except numbers, operators, parentheses, and spaces
            clean_expr = re.sub(r'[^0-9+\-*/().\s]', '', expression)
            
            # Validate the expression contains only safe operations
            if not re.match(r'^[\d+\-*/().\s]+$', clean_expr):
                return {
                    "success": False,
                    "error": "Expression contains unsafe characters",
                    "safe_expression": clean_expr
                }
            
            # Check for potentially dangerous operations
            dangerous_patterns = [
                r'__',  # Double underscore (potential code injection)
                r'eval',  # eval function
                r'exec',  # exec function
                r'import',  # import statements
                r'open',  # file operations
                r'file',  # file operations
            ]
            
            for pattern in dangerous_patterns:
                if re.search(pattern, expression, re.IGNORECASE):
                    return {
                        "success": False,
                        "error": f"Operation '{pattern}' is not allowed for security reasons",
                        "safe_expression": clean_expr
                    }
            
            # Evaluate the expression safely
            result = eval(clean_expr)
            
            # Format the result
            if isinstance(result, (int, float)):
                if result == int(result):
                    formatted_result = str(int(result))
                else:
                    formatted_result = f"{result:.6f}".rstrip('0').rstrip('.')
            else:
                formatted_result = str(result)
            
            return {
                "success": True,
                "expression": clean_expr,
                "result": formatted_result,
                "result_type": type(result).__name__,
                "calculation": f"{clean_expr} = {formatted_result}"
            }
            
        except ZeroDivisionError:
            return {
                "success": False,
                "error": "Division by zero is not allowed",
                "expression": expression
            }
        except SyntaxError:
            return {
                "success": False,
                "error": "Invalid mathematical expression",
                "expression": expression
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Calculation failed: {str(e)}",
                "expression": expression
            }


class CodeGenerationTools:
    """Specialized tools for code generation tasks."""
    
    def __init__(self):
        self.language_templates = {}
        self.framework_patterns = {}
        self._initialize_templates()
    
    def _initialize_templates(self):
        """Initialize code templates for different languages and frameworks."""
        self.language_templates = {
            "python": {
                "function": "def {function_name}({parameters}):\n    \"\"\"{docstring}\"\"\"\n    {body}\n    return {return_value}",
                "class": "class {class_name}:\n    \"\"\"{docstring}\"\"\"\n    \n    def __init__(self, {init_params}):\n        {init_body}\n    \n    {methods}",
                "api_endpoint": "@app.{method}(\"{endpoint}\")\nasync def {function_name}({parameters}):\n    \"\"\"{docstring}\"\"\"\n    {body}\n    return {return_value}"
            },
            "javascript": {
                "function": "function {function_name}({parameters}) {{\n    // {docstring}\n    {body}\n    return {return_value};\n}}",
                "class": "class {class_name} {{\n    constructor({init_params}) {{\n        {init_body}\n    }}\n    \n    {methods}\n}}",
                "api_endpoint": "app.{method}('{endpoint}', async ({parameters}) => {{\n    // {docstring}\n    {body}\n    return {return_value};\n}});"
            }
        }
    
    def generate_code_template(self, language: str, template_type: str, **kwargs) -> str:
        """Generate code using predefined templates."""
        if language not in self.language_templates:
            return f"// Unsupported language: {language}"
        
        if template_type not in self.language_templates[language]:
            return f"// Unsupported template type: {template_type}"
        
        template = self.language_templates[language][template_type]
        return template.format(**kwargs)


class CodeAnalysisTools:
    """Specialized tools for code analysis tasks."""
    
    def __init__(self):
        self.analysis_patterns = {}
        self.metric_calculators = {}
    
    def analyze_code_complexity(self, code: str) -> Dict[str, Any]:
        """Analyze code complexity metrics."""
        lines = code.split('\n')
        
        metrics = {
            "total_lines": len(lines),
            "code_lines": 0,
            "comment_lines": 0,
            "blank_lines": 0,
            "function_count": 0,
            "class_count": 0,
            "complexity_score": 0
        }
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                metrics["blank_lines"] += 1
            elif stripped.startswith('#') or stripped.startswith('//'):
                metrics["comment_lines"] += 1
            else:
                metrics["code_lines"] += 1
                if stripped.startswith('def ') or stripped.startswith('function '):
                    metrics["function_count"] += 1
                elif stripped.startswith('class '):
                    metrics["class_count"] += 1
        
        # Calculate complexity score (simplified)
        metrics["complexity_score"] = min(100, max(0, 
            metrics["function_count"] * 5 + 
            metrics["class_count"] * 3 + 
            metrics["code_lines"] // 10
        ))
        
        return metrics
    
    def detect_code_smells(self, code: str) -> List[Dict[str, Any]]:
        """Detect common code smells and anti-patterns."""
        smells = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Long lines
            if len(line) > 120:
                smells.append({
                    "line": i,
                    "type": "long_line",
                    "severity": "medium",
                    "description": f"Line {i} is too long ({len(line)} characters)",
                    "suggestion": "Break into multiple lines or extract variables"
                })
            
            # Magic numbers
            if re.search(r'\b\d{3,}\b', stripped):
                smells.append({
                    "line": i,
                    "type": "magic_number",
                    "severity": "low",
                    "description": f"Line {i} contains magic number",
                    "suggestion": "Define as named constant"
                })
            
            # TODO/FIXME comments
            if re.search(r'\b(TODO|FIXME|HACK|XXX)\b', stripped, re.IGNORECASE):
                smells.append({
                    "line": i,
                    "type": "todo_comment",
                    "severity": "medium",
                    "description": f"Line {i} contains {stripped}",
                    "suggestion": "Address the technical debt"
                })
        
        return smells


class DebuggingTools:
    """Specialized tools for debugging tasks."""
    
    def __init__(self):
        self.error_patterns = {}
        self.solution_database = {}
        self._initialize_error_patterns()
    
    def _initialize_error_patterns(self):
        """Initialize common error patterns and solutions."""
        self.error_patterns = {
            "nameerror": {
                "pattern": r"NameError: name '(\w+)' is not defined",
                "solutions": [
                    "Check if the variable is defined before use",
                    "Verify spelling and case sensitivity",
                    "Check import statements if it's from another module",
                    "Ensure the variable is in the correct scope"
                ]
            },
            "typeerror": {
                "pattern": r"TypeError: (.*)",
                "solutions": [
                    "Check the types of variables involved",
                    "Verify function parameter types",
                    "Use type() function to inspect types",
                    "Add explicit type conversions when needed"
                ]
            },
            "attributeerror": {
                "pattern": r"AttributeError: (.*)",
                "solutions": [
                    "Check if the object is of the expected type",
                    "Verify the attribute/method name",
                    "Use dir() to see available attributes",
                    "Check if the attribute exists with hasattr()"
                ]
            }
        }
    
    def analyze_error_message(self, error_message: str) -> Dict[str, Any]:
        """Analyze an error message and provide debugging guidance."""
        error_lower = error_message.lower()
        
        analysis = {
            "error_type": "unknown",
            "confidence": 0.0,
            "solutions": [],
            "debugging_steps": [],
            "prevention_tips": []
        }
        
        for error_type, info in self.error_patterns.items():
            if re.search(info["pattern"], error_message, re.IGNORECASE):
                analysis.update({
                    "error_type": error_type,
                    "confidence": 0.9,
                    "solutions": info["solutions"],
                    "debugging_steps": [
                        "Read the error message carefully",
                        "Identify the line number where the error occurred",
                        "Check the variables and their values at that point",
                        "Use print() or logging to debug variable states"
                    ],
                    "prevention_tips": [
                        "Use type hints to catch errors early",
                        "Write unit tests for edge cases",
                        "Use an IDE with real-time error checking",
                        "Follow consistent naming conventions"
                    ]
                })
                break
        
        return analysis


class OptimizationTools:
    """Specialized tools for code optimization tasks."""
    
    def __init__(self):
        self.optimization_patterns = {}
        self.performance_metrics = {}
    
    def analyze_performance_patterns(self, code: str) -> Dict[str, Any]:
        """Analyze code for performance optimization opportunities."""
        analysis = {
            "bottlenecks": [],
            "optimization_opportunities": [],
            "estimated_improvement": 0,
            "complexity_analysis": {},
            "recommendations": []
        }
        
        lines = code.split('\n')
        
        # Analyze each line for performance issues
        for i, line in enumerate(lines, 1):
            self._analyze_line_for_bottlenecks(line.strip(), i, analysis)
            self._analyze_line_for_optimizations(line.strip(), i, analysis)
        
        # Generate overall recommendations
        self._generate_performance_recommendations(analysis)
        
        return analysis
    
    def _analyze_line_for_bottlenecks(self, stripped_line: str, line_num: int, analysis: Dict[str, Any]):
        """Analyze a single line for performance bottlenecks."""
        # Check for nested loops
        if "for " in stripped_line and " in " in stripped_line:
            if "range(" in stripped_line:
                analysis["bottlenecks"].append({
                    "line": line_num,
                    "type": "nested_loop",
                    "severity": "high",
                    "description": "Potential O(n²) complexity",
                    "suggestion": "Consider vectorization or algorithm optimization"
                })
    
    def _analyze_line_for_optimizations(self, stripped_line: str, line_num: int, analysis: Dict[str, Any]):
        """Analyze a single line for optimization opportunities."""
        # Check for inefficient list operations
        if "list(" in stripped_line and "map(" in stripped_line:
            analysis["optimization_opportunities"].append({
                "line": line_num,
                "type": "list_map",
                "severity": "medium",
                "description": "map() with list() is less efficient",
                "suggestion": "Use list comprehension instead"
            })
        
        # Check for wildcard imports
        if "import *" in stripped_line:
            analysis["bottlenecks"].append({
                "line": line_num,
                "type": "wildcard_import",
                "severity": "low",
                "description": "Wildcard import can slow down startup",
                "suggestion": "Import specific functions/classes instead"
            })
    
    def _generate_performance_recommendations(self, analysis: Dict[str, Any]):
        """Generate overall performance recommendations based on analysis."""
        total_issues = len(analysis["bottlenecks"]) + len(analysis["optimization_opportunities"])
        
        if total_issues == 0:
            analysis["recommendations"].append("Code looks well-optimized!")
            analysis["estimated_improvement"] = 0
        else:
            # Calculate estimated improvement based on issue severity
            high_severity = sum(1 for issue in analysis["bottlenecks"] if issue.get("severity") == "high")
            medium_severity = sum(1 for issue in analysis["optimization_opportunities"] if issue.get("severity") == "medium")
            
            analysis["estimated_improvement"] = (high_severity * 30) + (medium_severity * 15)  # Percentage
            
            if high_severity > 0:
                analysis["recommendations"].append("Address high-severity bottlenecks first")
            if medium_severity > 2:
                analysis["recommendations"].append("Consider refactoring for better performance")
            
            analysis["recommendations"].append(f"Potential {analysis['estimated_improvement']}% performance improvement")
    
    def suggest_optimizations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate specific optimization suggestions."""
        suggestions = []
        
        for bottleneck in analysis.get("bottlenecks", []):
            if bottleneck["type"] == "nested_loop":
                suggestions.append({
                    "type": "algorithm",
                    "priority": "high",
                    "description": "Optimize nested loop structure",
                    "before_example": "for i in range(n):\n    for j in range(m):\n        result[i][j] = process(i, j)",
                    "after_example": "# Use vectorized operations\nresult = np.array([[process(i, j) for j in range(m)] for i in range(n)])\n# or\nresult = np.fromfunction(lambda i, j: process(i, j), (n, m))",
                    "improvement": "10-100x faster for large datasets",
                    "complexity": "O(n²) → O(n) for vectorized operations"
                })
            
            elif bottleneck["type"] == "wildcard_import":
                suggestions.append({
                    "type": "import",
                    "priority": "low",
                    "description": "Optimize import statements",
                    "before_example": "from numpy import *",
                    "after_example": "from numpy import array, zeros, ones, linspace",
                    "improvement": "Faster startup, clearer dependencies",
                    "complexity": "No runtime change"
                })
        
        for opportunity in analysis.get("optimization_opportunities", []):
            if opportunity["type"] == "list_map":
                suggestions.append({
                    "type": "syntax",
                    "priority": "medium",
                    "description": "Use list comprehension instead of map()",
                    "before_example": "result = list(map(lambda x: x * 2, data))",
                    "after_example": "result = [x * 2 for x in data]",
                    "improvement": "More readable, slightly faster",
                    "complexity": "No change in runtime"
                })
        
        return suggestions


# Add the new tools to the AdvancedToolRegistry
def register_ai_tools(tool_registry: AdvancedToolRegistry):
    """Register AI-specific tools with the tool registry."""
    
    # Code Generation Tools
    code_gen_tools = CodeGenerationTools()
    generate_code_tool = AdvancedTool(
        name="generate_code_template",
        description="Generate code using predefined templates",
        function=code_gen_tools.generate_code_template,
        category=ToolCategory.AI_MODELS,
        safety_level=SafetyLevel.SAFE
    )
    tool_registry.register_tool(generate_code_tool)
    
    # Code Analysis Tools
    code_analysis_tools = CodeAnalysisTools()
    analyze_complexity_tool = AdvancedTool(
        name="analyze_code_complexity",
        description="Analyze code complexity metrics",
        function=code_analysis_tools.analyze_code_complexity,
        category=ToolCategory.AI_MODELS,
        safety_level=SafetyLevel.SAFE
    )
    tool_registry.register_tool(analyze_complexity_tool)
    
    detect_smells_tool = AdvancedTool(
        name="detect_code_smells",
        description="Detect common code smells and anti-patterns",
        function=code_analysis_tools.detect_code_smells,
        category=ToolCategory.AI_MODELS,
        safety_level=SafetyLevel.SAFE
    )
    tool_registry.register_tool(detect_smells_tool)
    
    # Debugging Tools
    debugging_tools = DebuggingTools()
    analyze_error_tool = AdvancedTool(
        name="analyze_error_message",
        description="Analyze error messages and provide debugging guidance",
        function=debugging_tools.analyze_error_message,
        category=ToolCategory.AI_MODELS,
        safety_level=SafetyLevel.SAFE
    )
    tool_registry.register_tool(analyze_error_tool)
    
    # Optimization Tools
    optimization_tools = OptimizationTools()
    analyze_performance_tool = AdvancedTool(
        name="analyze_performance_patterns",
        description="Analyze code for performance optimization opportunities",
        function=optimization_tools.analyze_performance_patterns,
        category=ToolCategory.AI_MODELS,
        safety_level=SafetyLevel.SAFE
    )
    tool_registry.register_tool(analyze_performance_tool)
    
    suggest_optimizations_tool = AdvancedTool(
        name="suggest_optimizations",
        description="Generate specific optimization suggestions",
        function=optimization_tools.suggest_optimizations,
        category=ToolCategory.AI_MODELS,
        safety_level=SafetyLevel.SAFE
    )
    tool_registry.register_tool(suggest_optimizations_tool)
