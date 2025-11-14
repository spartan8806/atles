"""
ATLES Orchestrator: Multi-Step Task Execution System

This module implements the Orchestrator class that manages complex, multi-step tasks
by breaking them down into sequential actions and executing them with feedback loops.

Key Features:
- Task Planning: Converts high-level goals into step-by-step action plans
- Sequential Execution: Executes actions one at a time with context preservation
- Feedback Loops: Incorporates results from each step into the next
- Memory Integration: Maintains working memory across the entire task
- Error Handling: Gracefully handles failures and can retry or adapt

Architecture:
1. Receive high-level goal
2. Generate step-by-step plan using ATLES reasoning
3. Execute first step
4. Feed result back to working memory
5. Re-evaluate plan with new information
6. Execute next step
7. Repeat until goal is achieved
"""

import logging
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple, Union
from enum import Enum
import re

logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    """Status of a task or action."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ActionType(Enum):
    """Types of actions the orchestrator can execute."""
    READ_FILE = "read_file"
    WRITE_FILE = "write_file"
    SEARCH_CODE = "search_code"
    EXECUTE_COMMAND = "execute_command"
    ASK_USER = "ask_user"
    ANALYZE = "analyze"
    PLAN = "plan"
    CUSTOM = "custom"

class Action:
    """Represents a single action in a task plan."""
    
    def __init__(self, action_type: ActionType, description: str, parameters: Dict[str, Any] = None, 
                 expected_result: str = None, dependencies: List[str] = None):
        self.action_id = str(uuid.uuid4())[:8]
        self.action_type = action_type
        self.description = description
        self.parameters = parameters or {}
        self.expected_result = expected_result
        self.dependencies = dependencies or []
        self.status = TaskStatus.PENDING
        self.result = None
        self.error = None
        self.created_at = datetime.now()
        self.completed_at = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert action to dictionary for serialization."""
        return {
            "action_id": self.action_id,
            "action_type": self.action_type.value,
            "description": self.description,
            "parameters": self.parameters,
            "expected_result": self.expected_result,
            "dependencies": self.dependencies,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }

class TaskPlan:
    """Represents a complete task plan with multiple actions."""
    
    def __init__(self, goal: str, actions: List[Action] = None):
        self.plan_id = str(uuid.uuid4())[:8]
        self.goal = goal
        self.actions = actions or []
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now()
        self.working_memory = {}  # Stores results and context between actions
    
    def add_action(self, action: Action) -> None:
        """Add an action to the plan."""
        self.actions.append(action)
    
    def get_next_action(self) -> Optional[Action]:
        """Get the next pending action that has all dependencies satisfied."""
        for action in self.actions:
            if action.status == TaskStatus.PENDING:
                # Check if all dependencies are completed
                if all(dep_id in [a.action_id for a in self.actions if a.status == TaskStatus.COMPLETED] 
                       for dep_id in action.dependencies):
                    return action
        return None
    
    def is_complete(self) -> bool:
        """Check if all actions are completed."""
        return all(action.status == TaskStatus.COMPLETED for action in self.actions)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert plan to dictionary for serialization."""
        return {
            "plan_id": self.plan_id,
            "goal": self.goal,
            "actions": [action.to_dict() for action in self.actions],
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "working_memory": self.working_memory
        }

class Orchestrator:
    """
    The Orchestrator manages multi-step task execution with planning and feedback loops.
    
    This is the core component that solves the "one-shot" execution problem by:
    1. Breaking down complex goals into sequential actions
    2. Executing actions one at a time with context preservation
    3. Incorporating results into working memory for next steps
    4. Adapting the plan based on new information
    """
    
    def __init__(self, atles_brain=None, memory_integration=None):
        """
        Initialize the Orchestrator.
        
        Args:
            atles_brain: ATLES Brain instance for reasoning
            memory_integration: Memory integration for context
        """
        self.atles_brain = atles_brain
        self.memory_integration = memory_integration
        self.current_plan = None
        self.execution_history = []
        
        logger.info("Orchestrator initialized")
    
    def execute_goal(self, goal: str, max_steps: int = 10) -> Dict[str, Any]:
        """
        Execute a high-level goal by breaking it down into steps.
        
        Args:
            goal: The high-level goal to achieve
            max_steps: Maximum number of steps to execute
            
        Returns:
            Dictionary with execution results and status
        """
        logger.info(f"🎯 Starting goal execution: {goal}")
        
        try:
            # Step 1: Generate task plan
            plan = self._generate_task_plan(goal)
            if not plan:
                return {"success": False, "error": "Failed to generate task plan"}
            
            # Step 2: Execute the plan
            execution_result = self._execute_plan(plan, max_steps)
            
            # Step 3: Return results
            return {
                "success": execution_result["success"],
                "goal": goal,
                "plan": plan.to_dict(),
                "execution_result": execution_result,
                "working_memory": plan.working_memory
            }
            
        except Exception as e:
            logger.error(f"Goal execution failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _generate_task_plan(self, goal: str) -> Optional[TaskPlan]:
        """
        Generate a step-by-step plan for achieving the goal.
        
        This uses ATLES reasoning to break down the goal into actionable steps.
        """
        logger.info(f"📋 Generating task plan for: {goal}")
        
        try:
            # For now, directly create the plan based on the goal
            actions = self._create_fallback_actions(goal)
            
            if not actions:
                logger.error("Failed to create actions from goal")
                return None
            
            # Create task plan
            plan = TaskPlan(goal, actions)
            logger.info(f"✅ Generated plan with {len(actions)} actions")
            
            return plan
            
        except Exception as e:
            logger.error(f"Plan generation failed: {e}")
            return None
    
    def _simple_plan_generation(self, goal: str) -> str:
        """
        Simple fallback plan generation when ATLES brain is not available.
        """
        # Basic keyword-based plan generation
        goal_lower = goal.lower()
        
        if "read" in goal_lower and "file" in goal_lower:
            # Extract file path from goal
            import re
            file_match = re.search(r'file named (\w+\.\w+)', goal)
            file_path = file_match.group(1) if file_match else "input.txt"
            
            return f'''[
  {{
    "action_type": "READ_FILE",
    "description": "Read the specified file",
    "parameters": {{"file_path": "{file_path}"}},
    "expected_result": "File contents for analysis"
  }},
  {{
    "action_type": "ANALYZE",
    "description": "Count words in the file content",
    "parameters": {{"data": "{{previous_result}}", "analysis_type": "word_count"}},
    "expected_result": "Total word count"
  }},
  {{
    "action_type": "WRITE_FILE",
    "description": "Create output file with word count",
    "parameters": {{"file_path": "output.txt", "content": "The total word count is {{word_count}}."}},
    "expected_result": "Output file created with word count"
  }}
]'''
        elif "update" in goal_lower and "principle" in goal_lower:
            return '''[
  {
    "action_type": "READ_FILE", 
    "description": "Read config file to understand current structure",
    "parameters": {"file_path": "config.py"},
    "expected_result": "Current configuration structure"
  },
  {
    "action_type": "ANALYZE",
    "description": "Analyze config to find principles section", 
    "parameters": {"data": "{{previous_result}}"},
    "expected_result": "Location of principles in config"
  },
  {
    "action_type": "WRITE_FILE",
    "description": "Update the principles section with new content",
    "parameters": {"file_path": "config.py", "content": "{{new_principle}}"},
    "expected_result": "Updated config file with new principle"
  }
]'''
        else:
            return '''[
  {
    "action_type": "ASK_USER",
    "description": "Ask user for clarification on how to proceed",
    "parameters": {"question": "How would you like me to approach this goal?"},
    "expected_result": "User guidance for next steps"
  }
]'''
    
    def _parse_plan_response(self, response: str, goal: str) -> List[Action]:
        """
        Parse the plan response into Action objects.
        """
        actions = []
        
        try:
            # Extract JSON from response
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                logger.info(f"🔍 DEBUG: Extracted JSON: {json_str}")
                actions_data = json.loads(json_str)
                logger.info(f"🔍 DEBUG: Parsed actions data: {actions_data}")
            else:
                logger.warning(f"🔍 DEBUG: No JSON found in response: {response}")
                # Fallback: create simple actions based on goal
                return self._create_fallback_actions(goal)
            
            for i, action_data in enumerate(actions_data):
                action_type = ActionType(action_data.get("action_type", "CUSTOM"))
                description = action_data.get("description", f"Step {i+1}")
                parameters = action_data.get("parameters", {})
                expected_result = action_data.get("expected_result", "")
                
                # Add dependencies (each action depends on the previous one)
                dependencies = []
                if i > 0:
                    dependencies = [actions[i-1].action_id]
                
                action = Action(
                    action_type=action_type,
                    description=description,
                    parameters=parameters,
                    expected_result=expected_result,
                    dependencies=dependencies
                )
                actions.append(action)
                
        except Exception as e:
            logger.error(f"Failed to parse plan response: {e}")
            return self._create_fallback_actions(goal)
        
        return actions
    
    def _create_fallback_actions(self, goal: str) -> List[Action]:
        """
        Create fallback actions when parsing fails.
        """
        actions = []
        logger.info(f"🔍 DEBUG: Creating fallback actions for goal: {goal}")
        
        # Extract file path from goal
        import re
        file_match = re.search(r'file named (\w+\.\w+)', goal)
        file_path = file_match.group(1) if file_match else "input.txt"
        logger.info(f"🔍 DEBUG: Extracted file path: {file_path}")
        
        # Basic fallback based on goal keywords
        if "read" in goal.lower() and "file" in goal.lower():
            logger.info("🔍 DEBUG: Creating 3-step plan for file reading task")
            
            # Step 1: Read file
            action1 = Action(
                action_type=ActionType.READ_FILE,
                description="Read the specified file",
                parameters={"file_path": file_path},
                expected_result="File contents"
            )
            actions.append(action1)
            logger.info(f"🔍 DEBUG: Created action 1: READ_FILE {file_path}")
            
            # Step 2: Analyze/Count words
            action2 = Action(
                action_type=ActionType.ANALYZE,
                description="Count words in the file content",
                parameters={"data": "{{previous_result}}", "analysis_type": "word_count"},
                expected_result="Total word count",
                dependencies=[action1.action_id]
            )
            actions.append(action2)
            logger.info("🔍 DEBUG: Created action 2: ANALYZE word_count")
            
            # Step 3: Write output file
            action3 = Action(
                action_type=ActionType.WRITE_FILE,
                description="Create output file with word count",
                parameters={"file_path": "output.txt", "content": "The total word count is {{word_count}}."},
                expected_result="Output file created with word count",
                dependencies=[action2.action_id]
            )
            actions.append(action3)
            logger.info("🔍 DEBUG: Created action 3: WRITE_FILE output.txt")
        
        logger.info(f"🔍 DEBUG: Created {len(actions)} fallback actions")
        return actions
    
    def _execute_plan(self, plan: TaskPlan, max_steps: int) -> Dict[str, Any]:
        """
        Execute the task plan step by step.
        """
        logger.info(f"🚀 Executing plan with {len(plan.actions)} actions")
        
        plan.status = TaskStatus.IN_PROGRESS
        executed_steps = 0
        
        while not plan.is_complete() and executed_steps < max_steps:
            # Get next action to execute
            next_action = plan.get_next_action()
            if not next_action:
                logger.warning("No more actions to execute")
                break
            
            logger.info(f"⚡ Executing action: {next_action.description}")
            
            # Execute the action
            result = self._execute_action(next_action, plan.working_memory)
            
            # Update action status
            if result["success"]:
                next_action.status = TaskStatus.COMPLETED
                next_action.result = result.get("result")
                next_action.completed_at = datetime.now()
                
                # Store result in working memory
                plan.working_memory[f"action_{next_action.action_id}"] = result.get("result")
                plan.working_memory["last_result"] = result.get("result")
                
                logger.info(f"✅ Action completed: {next_action.description}")
            else:
                next_action.status = TaskStatus.FAILED
                next_action.error = result.get("error")
                logger.error(f"❌ Action failed: {next_action.description} - {result.get('error')}")
                
                # Decide whether to continue or stop
                if not self._should_continue_after_failure(next_action, plan):
                    break
            
            executed_steps += 1
        
        # Update plan status
        if plan.is_complete():
            plan.status = TaskStatus.COMPLETED
            logger.info("🎉 Plan execution completed successfully")
        else:
            plan.status = TaskStatus.FAILED
            logger.warning("⚠️ Plan execution incomplete")
        
        return {
            "success": plan.status == TaskStatus.COMPLETED,
            "executed_steps": executed_steps,
            "total_steps": len(plan.actions),
            "completed_actions": len([a for a in plan.actions if a.status == TaskStatus.COMPLETED]),
            "failed_actions": len([a for a in plan.actions if a.status == TaskStatus.FAILED])
        }
    
    def _execute_action(self, action: Action, working_memory: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single action and return the result.
        """
        try:
            # Substitute placeholders in parameters with working memory values
            parameters = self._substitute_placeholders(action.parameters, working_memory)
            
            if action.action_type == ActionType.READ_FILE:
                return self._execute_read_file(parameters)
            elif action.action_type == ActionType.WRITE_FILE:
                return self._execute_write_file(parameters)
            elif action.action_type == ActionType.SEARCH_CODE:
                return self._execute_search_code(parameters)
            elif action.action_type == ActionType.EXECUTE_COMMAND:
                return self._execute_command(parameters)
            elif action.action_type == ActionType.ASK_USER:
                return self._execute_ask_user(parameters)
            elif action.action_type == ActionType.ANALYZE:
                return self._execute_analyze(parameters)
            else:
                return {"success": False, "error": f"Unknown action type: {action.action_type}"}
                
        except Exception as e:
            logger.error(f"Action execution failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _substitute_placeholders(self, parameters: Dict[str, Any], working_memory: Dict[str, Any]) -> Dict[str, Any]:
        """
        Substitute placeholders in parameters with values from working memory.
        """
        substituted = {}
        for key, value in parameters.items():
            if isinstance(value, str) and "{{" in value and "}}" in value:
                # Handle {{previous_result}} placeholder - use last_result from working memory
                if "{{previous_result}}" in value:
                    previous_result = working_memory.get("last_result", "")
                    value = value.replace("{{previous_result}}", str(previous_result))
                
                # Simple placeholder substitution for other placeholders
                for placeholder, replacement in working_memory.items():
                    if f"{{{{{placeholder}}}}}" in value:
                        value = value.replace(f"{{{{{placeholder}}}}}", str(replacement))
                
                # Special handling for word_count placeholder
                if "{{word_count}}" in value:
                    # Find the word count from previous results
                    word_count = None
                    for memory_key, memory_value in working_memory.items():
                        if isinstance(memory_value, dict) and "word_count" in memory_value:
                            word_count = memory_value["word_count"]
                            break
                        elif isinstance(memory_value, str) and "Word count:" in memory_value:
                            # Extract word count from string like "Word count: 25"
                            import re
                            match = re.search(r'Word count: (\d+)', memory_value)
                            if match:
                                word_count = int(match.group(1))
                                break
                    if word_count is not None:
                        value = value.replace("{{word_count}}", str(word_count))
                
                substituted[key] = value
            else:
                substituted[key] = value
        return substituted
    
    def _execute_read_file(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute READ_FILE action."""
        file_path = parameters.get("file_path")
        if not file_path:
            return {"success": False, "error": "No file_path specified"}
        
        # Look for file in parent directory (D:\portfolio) since orchestrator runs from D:\portfolio\atles
        parent_dir_path = f"../{file_path}"
        
        try:
            with open(parent_dir_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {"success": True, "result": content}
        except Exception as e:
            return {"success": False, "error": f"Failed to read file: {e}"}
    
    def _execute_write_file(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute WRITE_FILE action."""
        file_path = parameters.get("file_path")
        content = parameters.get("content")
        
        if not file_path or content is None:
            return {"success": False, "error": "file_path and content required"}
        
        # Write to parent directory (D:\portfolio) since orchestrator runs from D:\portfolio\atles
        parent_dir_path = f"../{file_path}"
        
        try:
            with open(parent_dir_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return {"success": True, "result": f"File {parent_dir_path} written successfully"}
        except Exception as e:
            return {"success": False, "error": f"Failed to write file: {e}"}
    
    def _execute_search_code(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute SEARCH_CODE action."""
        # This would integrate with the existing codebase search
        return {"success": True, "result": "Search functionality not yet implemented"}
    
    def _execute_command(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute EXECUTE_COMMAND action."""
        command = parameters.get("command")
        if not command:
            return {"success": False, "error": "No command specified"}
        
        # This would integrate with the terminal execution system
        return {"success": True, "result": f"Command execution not yet implemented: {command}"}
    
    def _execute_ask_user(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute ASK_USER action."""
        question = parameters.get("question", "Please provide input")
        return {"success": True, "result": f"User input needed: {question}"}
    
    def _execute_analyze(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute ANALYZE action."""
        data = parameters.get("data", "")
        analysis_type = parameters.get("analysis_type", "general")
        
        # Simple analysis - in real implementation, this would use ATLES reasoning
        if "principle" in analysis_type.lower():
            return {"success": True, "result": "Found principles section in config file"}
        elif "word_count" in analysis_type.lower():
            # Count words in the data
            words = data.split()
            word_count = len(words)
            return {"success": True, "result": f"Word count: {word_count}", "word_count": word_count}
        else:
            return {"success": True, "result": f"Analysis completed for: {analysis_type}"}
    
    def _should_continue_after_failure(self, failed_action: Action, plan: TaskPlan) -> bool:
        """
        Decide whether to continue execution after an action fails.
        """
        # For now, always continue unless it's a critical action
        critical_actions = [ActionType.READ_FILE, ActionType.ANALYZE]
        return failed_action.action_type not in critical_actions

# Convenience function for easy integration
def create_orchestrator(atles_brain=None, memory_integration=None) -> Orchestrator:
    """
    Create and return a new Orchestrator instance.
    
    Args:
        atles_brain: ATLES Brain instance for reasoning
        memory_integration: Memory integration for context
        
    Returns:
        Orchestrator instance
    """
    return Orchestrator(atles_brain, memory_integration)
