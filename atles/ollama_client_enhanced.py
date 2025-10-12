"""
ATLES Enhanced Ollama Client with Function Calling

This client allows Ollama to execute functions and interact with external systems.
Now enhanced with multi-goal management capabilities.
"""

import requests
import json
import logging
import subprocess
import os
from pathlib import Path
from typing import Dict, Any, Optional, List, Callable
import importlib.util
from datetime import datetime

# Import dependency checker and PDF processor (if available)
try:
    from .dependency_checker import dependency_manager
    from .pdf_processor import fetch_and_read_pdf, extract_text_from_pdf
    PDF_PROCESSOR_AVAILABLE = True
except ImportError:
    PDF_PROCESSOR_AVAILABLE = False

# Import error handler
try:
    from .error_handler import ErrorHandler, ATLESError, ErrorCategory, ErrorSeverity
except ImportError:
    # Fallback if error handler not available
    class ErrorHandler:
        def handle_error(self, error, context=None):
            return {"error_handled": False, "user_response": str(error)}
    ATLESError = Exception
    ErrorCategory = None
    ErrorSeverity = None

logger = logging.getLogger(__name__)

class GoalManager:
    """Manages multiple goals and resolves conflicts intelligently."""
    
    def __init__(self):
        import threading
        self._lock = threading.RLock()  # Reentrant lock for thread safety
        self.base_goals = {
            "help_human": {"priority": 10, "description": "Help the human user achieve their objectives"},
            "maintain_operation": {"priority": 8, "description": "Keep the system running smoothly"},
            "learn_and_improve": {"priority": 7, "description": "Learn from interactions and improve capabilities"},
            "ensure_safety": {"priority": 9, "description": "Ensure all operations are safe and ethical"},
            "efficient_execution": {"priority": 6, "description": "Execute tasks efficiently when possible"}
        }
        
        self.dynamic_goals = {}
        self.goal_conflicts = []
        self.goal_history = []
    
    def add_goal(self, goal_name: str, priority: int, description: str, context: str = ""):
        """Add a new dynamic goal."""
        self.dynamic_goals[goal_name] = {
            "priority": priority,
            "description": description,
            "context": context,
            "created_at": datetime.now().isoformat()
        }
        logger.info(f"Added dynamic goal: {goal_name} (priority: {priority})")
    
    def resolve_conflicts(self, goals: List[str]) -> Dict[str, Any]:
        """Resolve conflicts between competing goals."""
        if len(goals) <= 1:
            return {"resolved": True, "primary_goal": goals[0] if goals else None}
        
        # Sort goals by priority
        goal_priorities = []
        for goal in goals:
            if goal in self.base_goals:
                goal_priorities.append((goal, self.base_goals[goal]["priority"]))
            elif goal in self.dynamic_goals:
                goal_priorities.append((goal, self.dynamic_goals[goal]["priority"]))
            else:
                goal_priorities.append((goal, 5))  # Default priority
        
        goal_priorities.sort(key=lambda x: x[1], reverse=True)
        
        # Check for conflicts
        conflicts = []
        for i, (goal1, priority1) in enumerate(goal_priorities):
            for goal2, priority2 in goal_priorities[i+1:]:
                if self._goals_conflict(goal1, goal2):
                    conflicts.append({
                        "goal1": goal1,
                        "goal2": goal2,
                        "priority1": priority1,
                        "priority2": priority2,
                        "resolution": "priority_based"
                    })
        
        resolution = {
            "resolved": True,
            "primary_goal": goal_priorities[0][0],
            "goal_sequence": [g[0] for g in goal_priorities],
            "conflicts": conflicts,
            "strategy": "priority_based_resolution"
        }
        
        self.goal_conflicts.extend(conflicts)
        self.goal_history.append({
            "timestamp": datetime.now().isoformat(),
            "goals": goals,
            "resolution": resolution
        })
        
        return resolution
    
    def _goals_conflict(self, goal1: str, goal2: str) -> bool:
        """Check if two goals conflict with each other."""
        # Define known conflicts
        conflict_pairs = [
            ("efficient_execution", "ensure_safety"),  # Safety overrides efficiency
            ("maintain_operation", "help_human"),     # Helping human may require operational changes
            ("efficient_execution", "learn_and_improve")  # Learning may not be efficient
        ]
        
        for pair in conflict_pairs:
            if (goal1 in pair and goal2 in pair):
                return True
        
        return False
    
    def get_goal_context(self, primary_goal: str) -> str:
        """Get context about how to pursue a goal while balancing others."""
        if primary_goal in self.base_goals:
            goal_info = self.base_goals[primary_goal]
            return f"Primary Goal: {primary_goal} (Priority: {goal_info['priority']})\nDescription: {goal_info['description']}"
        elif primary_goal in self.dynamic_goals:
            goal_info = self.dynamic_goals[primary_goal]
            return f"Dynamic Goal: {primary_goal} (Priority: {goal_info['priority']})\nDescription: {goal_info['description']}\nContext: {goal_info['context']}"
        else:
            return f"Custom Goal: {primary_goal} (Priority: 5)\nDescription: User-defined objective"
    
    def balance_goals(self, user_request: str) -> Dict[str, Any]:
        """Analyze user request and balance multiple goals."""
        with self._lock:  # Thread-safe goal balancing
            # Extract implicit goals from user request
            detected_goals = self._detect_goals_from_request(user_request)
            
            # Resolve any conflicts
            resolution = self.resolve_conflicts(detected_goals)
            
            # Generate balanced approach
            balanced_approach = self._generate_balanced_approach(resolution, user_request)
        
        return {
            "detected_goals": detected_goals,
            "conflict_resolution": resolution,
            "balanced_approach": balanced_approach,
            "goal_context": self.get_goal_context(resolution["primary_goal"])
        }
    
    def _detect_goals_from_request(self, user_request: str) -> List[str]:
        """Detect which goals are relevant to a user request."""
        goals = ["help_human"]  # Always primary
        
        request_lower = user_request.lower()
        
        # Detect safety concerns
        safety_keywords = ["dangerous", "harm", "unsafe", "risk", "delete", "remove", "system"]
        if any(keyword in request_lower for keyword in safety_keywords):
            goals.append("ensure_safety")
        
        # Detect learning opportunities
        learning_keywords = ["how", "explain", "teach", "learn", "understand", "why"]
        if any(keyword in request_lower for keyword in learning_keywords):
            goals.append("learn_and_improve")
        
        # Detect operational concerns
        operational_keywords = ["system", "performance", "speed", "efficiency", "optimize"]
        if any(keyword in request_lower for keyword in operational_keywords):
            goals.append("maintain_operation")
            goals.append("efficient_execution")
        
        return goals
    
    def _generate_balanced_approach(self, resolution: Dict[str, Any], user_request: str) -> str:
        """Generate a balanced approach that considers all goals."""
        primary = resolution["primary_goal"]
        conflicts = resolution.get("conflicts", [])
        
        approach = f"Balanced Approach for: {user_request}\n\n"
        approach += f"Primary Goal: {primary}\n"
        
        if conflicts:
            approach += "\nGoal Conflicts Resolved:\n"
            for conflict in conflicts:
                approach += f"- {conflict['goal1']} vs {conflict['goal2']}: Resolved by priority\n"
        else:
            approach += "\nNo Goal Conflicts: Single objective scenario\n"
        
        approach += f"\nExecution Strategy:\n"
        approach += f"1. Pursue {primary} as the main objective\n"
        
        # Add balancing considerations
        goal_sequence = resolution.get("goal_sequence", [])
        if "ensure_safety" in goal_sequence:
            approach += "2. Ensure all operations are safe and ethical\n"
        if "maintain_operation" in goal_sequence:
            approach += "3. Maintain system stability throughout execution\n"
        if "learn_and_improve" in goal_sequence:
            approach += "4. Learn from this interaction to improve future responses\n"
        
        return approach

class OllamaFunctionCaller:
    """Enhanced Ollama client with function calling and multi-goal management capabilities."""
    
    def __init__(self, base_url: str = "http://localhost:11434", debug_mode: bool = False, 
                 timeout: int = 60, max_retries: int = 3):
        self.base_url = base_url
        self.session = requests.Session()
        self.available_functions = {}
        self.goal_manager = GoalManager()
        self.error_handler = ErrorHandler()
        self.debug_mode = debug_mode
        self.timeout = timeout  # Configurable timeout
        self.max_retries = max_retries  # Configurable retry attempts
        if debug_mode:
            logger.info("FUNCTION_CALL DEBUG MODE ENABLED")
        self.register_default_functions()
    
    def __del__(self):
        """Cleanup method to properly close session and prevent memory leaks."""
        try:
            if hasattr(self, 'session') and self.session:
                self.session.close()
        except Exception:
            pass  # Ignore cleanup errors
    
    def close(self):
        """Explicitly close the session to prevent memory leaks."""
        if hasattr(self, 'session') and self.session:
            self.session.close()
            self.session = None
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.close()
        return False  # Don't suppress exceptions
    
    def validate_model(self, model_name: str, strict: bool = False) -> bool:
        """Comprehensive model validation with caching and strict mode."""
        if not model_name or not isinstance(model_name, str):
            logger.error(f"Invalid model name: {model_name}")
            return False
            
        # Cache for model validation to avoid repeated API calls
        if not hasattr(self, '_model_cache'):
            self._model_cache = {}
            self._cache_timestamp = 0
        
        import time
        current_time = time.time()
        
        # Refresh cache every 5 minutes
        if current_time - self._cache_timestamp > 300:
            self._model_cache.clear()
            
        # Check cache first
        if model_name in self._model_cache:
            return self._model_cache[model_name]
            
        try:
            response = self.session.get(
                f"{self.base_url}/api/tags",
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                available_models = [model.get('name', '') for model in data.get('models', [])]
                
                # Update cache
                self._cache_timestamp = current_time
                for model in available_models:
                    self._model_cache[model] = True
                
                # Check exact match first
                if model_name in available_models:
                    self._model_cache[model_name] = True
                    return True
                
                # Check partial matches (e.g., "qwen2.5:7b" vs "qwen2.5")
                partial_matches = [m for m in available_models if model_name.split(':')[0] in m]
                if partial_matches and not strict:
                    logger.info(f"Model '{model_name}' not found exactly, but found similar: {partial_matches}")
                    self._model_cache[model_name] = True
                    return True
                
                logger.warning(f"Model '{model_name}' not found. Available models: {available_models}")
                self._model_cache[model_name] = False
                return False
            else:
                logger.warning(f"Could not validate model '{model_name}': {response.status_code}")
                return not strict  # In strict mode, fail if we can't validate
        except Exception as e:
            logger.warning(f"Model validation failed for '{model_name}': {e}")
            return not strict  # In strict mode, fail if validation fails
    
    def _make_request_with_retry(self, method: str, url: str, **kwargs):
        """Make HTTP request with retry logic for timeout/connection issues."""
        import time
        
        for attempt in range(self.max_retries):
            try:
                if method.upper() == 'POST':
                    response = self.session.post(url, timeout=self.timeout, **kwargs)
                elif method.upper() == 'GET':
                    response = self.session.get(url, timeout=self.timeout, **kwargs)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                return response
                
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                if attempt < self.max_retries - 1:
                    wait_time = (attempt + 1) * 2  # Exponential backoff: 2s, 4s, 6s
                    logger.warning(f"Request timeout/connection error (attempt {attempt + 1}/{self.max_retries}). Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Request failed after {self.max_retries} attempts: {e}")
                    raise
            except Exception as e:
                logger.error(f"Request failed with non-retryable error: {e}")
                raise
    
    def _safe_json_parse(self, json_string: str) -> dict:
        """Safely parse JSON with validation and error handling."""
        try:
            # Clean up common JSON issues
            cleaned_json = json_string.strip()
            
            # Replace single quotes with double quotes (common AI mistake)
            cleaned_json = cleaned_json.replace("'", '"')
            
            # Validate JSON structure before parsing
            if not (cleaned_json.startswith('{') and cleaned_json.endswith('}')):
                raise ValueError("JSON must be a valid object (start with { and end with })")
            
            # Parse JSON
            parsed = json.loads(cleaned_json)
            
            # Validate it's a dictionary
            if not isinstance(parsed, dict):
                raise ValueError("JSON must parse to a dictionary/object")
            
            # Security check: limit object size to prevent DoS
            if len(str(parsed)) > 10000:  # 10KB limit
                raise ValueError("JSON object too large (max 10KB)")
            
            # Security check: limit nesting depth
            def check_depth(obj, depth=0):
                if depth > 10:  # Max 10 levels deep
                    raise ValueError("JSON object too deeply nested (max 10 levels)")
                if isinstance(obj, dict):
                    for value in obj.values():
                        check_depth(value, depth + 1)
                elif isinstance(obj, list):
                    for item in obj:
                        check_depth(item, depth + 1)
            
            check_depth(parsed)
            return parsed
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in function call: {e}")
            raise ValueError(f"Invalid JSON format: {e}")
        except Exception as e:
            logger.error(f"JSON parsing security check failed: {e}")
            raise ValueError(f"JSON validation failed: {e}")
    
    def _standardized_error_response(self, error_type: str, error_message: str, context: dict = None) -> dict:
        """Return standardized error response format."""
        return {
            "success": False,
            "error_type": error_type,
            "error_message": error_message,
            "context": context or {},
            "timestamp": datetime.now().isoformat()
        }
    
    def _standardized_success_response(self, data: any, message: str = "Success") -> dict:
        """Return standardized success response format."""
        return {
            "success": True,
            "data": data,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
    
    def register_default_functions(self):
        """Register the default set of functions."""
        # File operations
        self.register_function("read_file", self.read_file, {
            "description": "Read the contents of a file",
            "parameters": {
                "file_path": {"type": "string", "description": "Path to the file to read"},
                "start_line": {"type": "integer", "description": "Starting line number (optional)"},
                "end_line": {"type": "integer", "description": "Ending line number (optional)"}
            }
        })
        
        self.register_function("write_file", self.write_file, {
            "description": "Write content to a file",
            "parameters": {
                "file_path": {"type": "string", "description": "Path to the file to write"},
                "content": {"type": "string", "description": "Content to write to the file"},
                "mode": {"type": "string", "description": "Write mode: 'w' (overwrite) or 'a' (append)"}
            }
        })
        
        self.register_function("list_files", self.list_files, {
            "description": "List files in a directory",
            "parameters": {
                "directory": {"type": "string", "description": "Directory path to list"},
                "pattern": {"type": "string", "description": "File pattern to match (optional)"}
            }
        })
        
        # Code dataset functions
        self.register_function("search_code", self.search_code_datasets, {
            "description": "ONLY for searching code repositories, GitHub, programming examples, technical documentation. NEVER use for general knowledge questions like healthcare, science, history. Use web_search instead.",
            "parameters": {
                "query": {"type": "string", "description": "Search query - what the user is looking for"},
                "language": {"type": "string", "description": "Programming language to filter by (optional) - e.g., 'python', 'javascript', 'java'"},
                "dataset_type": {"type": "string", "description": "Specific dataset to search (optional) - 'github_code', 'programming_books', 'code_challenges', 'framework_docs'"}
            }
        })
        
        # Terminal operations
        self.register_function("run_command", self.run_terminal_command, {
            "description": "Run a terminal command",
            "parameters": {
                "command": {"type": "string", "description": "Command to execute"},
                "working_directory": {"type": "string", "description": "Working directory (optional)"}
            }
        })
        
        # System information
        self.register_function("get_system_info", self.get_system_info, {
            "description": "Get information about the current system",
            "parameters": {}
        })
        
        # Goal management functions - DISABLED: These run automatically, AI shouldn't call them directly
        # The GoalManager class still works internally, but we don't expose these as callable functions
        # to prevent the AI from generating malformed commands like "analyze_goals:{"session_id": 12345}"
        
        self.register_function("get_goal_status", self.get_goal_status, {
            "description": "Get current goal management status and history",
            "parameters": {}
        })
        
        self.register_function("reset_goals", self.reset_goals, {
            "description": "Reset dynamic goals and clear history",
            "parameters": {}
        })
        
        self.register_function("recommend_goals", self.recommend_goals, {
            "description": "Generate intelligent goal recommendations based on current context and user preferences",
            "parameters": {
                "context": {"type": "string", "description": "Current situation or challenge"},
                "user_preferences": {"type": "string", "description": "Known user preferences or patterns"},
                "max_recommendations": {"type": "integer", "description": "Maximum number of recommendations to generate"}
            }
        })
        
        
        # Web functions
        self.register_function("web_search", self.web_search, {
            "description": "Use this for general knowledge questions, current events, factual information, research topics, explanations. This is the DEFAULT choice for non-programming questions.",
            "parameters": {
                "query": {"type": "string", "description": "Search query - what to search for"},
                "count": {"type": "integer", "description": "Number of results to return (default: 5)"}
            }
        })
        
        self.register_function("check_url_accessibility", self.check_url_accessibility, {
            "description": "Check if a URL is accessible and get basic information about it without downloading content.",
            "parameters": {
                "url": {"type": "string", "description": "URL to check"}
            }
        })
        
        self.register_function("fetch_url_content", self.fetch_url_content, {
            "description": "Fetch content from a web URL. Only works for text/html pages, not PDFs or binary files.",
            "parameters": {
                "url": {"type": "string", "description": "URL to fetch content from"},
                "timeout": {"type": "integer", "description": "Request timeout in seconds (default: 10)"}
            }
        })
        
        # PDF processing (if available)
        if PDF_PROCESSOR_AVAILABLE:
            self.register_function("read_pdf", self.read_pdf, {
                "description": "Extract text from a PDF file at a URL. This function will download the PDF, extract its text content, and return it.",
                "parameters": {
                    "url": {"type": "string", "description": "URL of the PDF file to read"},
                    "timeout": {"type": "integer", "description": "Request timeout in seconds (default: 30)"}
                }
            })
    
    def register_function(self, name: str, func: Callable, metadata: Dict[str, Any]):
        """Register a function that Ollama can call."""
        self.available_functions[name] = {
            "function": func,
            "metadata": metadata
        }
        logger.info(f"Registered function: {name}")
    
    def get_function_schema(self) -> Dict[str, Any]:
        """Get the schema of all available functions for Ollama."""
        schema = {
            "functions": []
        }
        
        for name, func_info in self.available_functions.items():
            schema["functions"].append({
                "name": name,
                **func_info["metadata"]
            })
        
        return schema
    
    def execute_function(self, function_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a registered function with the given arguments."""
        if function_name not in self.available_functions:
            raise ValueError(f"Unknown function: {function_name}")
        
        func_info = self.available_functions[function_name]
        func = func_info["function"]
        
        try:
            result = func(**arguments)
            return {
                "success": True,
                "result": result,
                "function": function_name
            }
        except Exception as e:
            logger.error(f"Function execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "function": function_name
            }
    
    # File operation functions
    def read_file(self, file_path: str, start_line: Optional[int] = None, end_line: Optional[int] = None) -> str:
        """Read file contents. Automatically handles PDFs and text files."""
        try:
            # Check if it's a PDF file
            if file_path.lower().endswith('.pdf'):
                if PDF_PROCESSOR_AVAILABLE:
                    from .pdf_processor import extract_text_from_pdf
                    result = extract_text_from_pdf(file_path)
                    if result['success']:
                        full_text = result['text']
                        
                        # Apply line filtering if requested
                        if start_line is not None or end_line is not None:
                            lines = full_text.split('\n')
                            if start_line is not None and end_line is not None:
                                lines = lines[start_line-1:end_line]
                            elif start_line is not None:
                                lines = lines[start_line-1:]
                            return '\n'.join(lines)
                        
                        return full_text
                    else:
                        raise Exception(f"PDF reading failed: {result['error']}")
                else:
                    raise Exception("PDF reading not available. Install pdfplumber: pip install pdfplumber")
            
            # Handle regular text files
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if start_line is not None and end_line is not None:
                lines = lines[start_line-1:end_line]
            elif start_line is not None:
                lines = lines[start_line-1:]
            
            return ''.join(lines)
        except Exception as e:
            raise Exception(f"Failed to read file {file_path}: {e}")
    
    def write_file(self, file_path: str, content: str, mode: str = 'w') -> str:
        """Write content to file."""
        try:
            # Ensure directory exists
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, mode, encoding='utf-8') as f:
                f.write(content)
            
            return f"Successfully wrote to {file_path}"
        except Exception as e:
            raise Exception(f"Failed to write file {file_path}: {e}")
    
    def list_files(self, directory: str, pattern: Optional[str] = None) -> List[str]:
        """List files in directory."""
        try:
            path = Path(directory)
            if not path.exists():
                raise Exception(f"Directory {directory} does not exist")
            
            if pattern:
                files = list(path.glob(pattern))
            else:
                files = list(path.iterdir())
            
            return [str(f) for f in files if f.is_file()]
        except Exception as e:
            raise Exception(f"Failed to list files in {directory}: {e}")
    
    # Code dataset functions
    def search_code_datasets(self, query: str, language: Optional[str] = None, dataset_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search through code datasets."""
        try:
            # Import the dataset manager - try multiple import paths
            try:
                from .datasets.dataset_manager import CodeDatasetManager
            except ImportError:
                try:
                    from atles.datasets.dataset_manager import CodeDatasetManager
                except ImportError:
                    from datasets.dataset_manager import CodeDatasetManager
            
            manager = CodeDatasetManager()
            results = manager.search_code(query, language, dataset_type)
            
            # Convert to serializable format
            serializable_results = []
            for result in results:
                if hasattr(result, '__dict__'):
                    serializable_results.append(result.__dict__)
                else:
                    serializable_results.append(result)
            
            return serializable_results
        except Exception as e:
            raise Exception(f"Failed to search code datasets: {e}")
    
    # Terminal functions
    def run_terminal_command(self, command: str, working_directory: Optional[str] = None) -> str:
        """Run a terminal command."""
        try:
            if working_directory:
                cwd = Path(working_directory)
                if not cwd.exists():
                    raise Exception(f"Working directory {working_directory} does not exist")
            else:
                cwd = None
            
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return f"Command executed successfully:\n{result.stdout}"
            else:
                return f"Command failed (exit code {result.returncode}):\n{result.stderr}"
        except subprocess.TimeoutExpired:
            raise Exception("Command timed out after 30 seconds")
        except Exception as e:
            raise Exception(f"Failed to run command: {e}")
    
    # System information
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information."""
        import platform
        import psutil
        
        try:
            return {
                "platform": platform.platform(),
                "python_version": platform.python_version(),
                "cpu_count": psutil.cpu_count(),
                "memory_total": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
                "current_directory": str(Path.cwd())
            }
        except Exception as e:
            return {
                "error": f"Failed to get system info: {e}",
                "platform": platform.platform(),
                "python_version": platform.python_version()
            }
    
    # Goal management functions
    def analyze_goals(self, user_request: str) -> Dict[str, Any]:
        """Analyze the goals involved in a user request and provide balanced approach."""
        return self.goal_manager.balance_goals(user_request)
    
    def add_custom_goal(self, goal_name: str, priority: int, description: str, context: str = "") -> Dict[str, Any]:
        """Add a custom goal for the current interaction."""
        self.goal_manager.add_goal(goal_name, priority, description, context)
        return {"status": "success", "message": f"Custom goal '{goal_name}' added with priority {priority}"}
    
    def get_goal_status(self) -> Dict[str, Any]:
        """Get current goal management status and history."""
        return {
            "base_goals": self.goal_manager.base_goals,
            "dynamic_goals": self.goal_manager.dynamic_goals,
            "recent_conflicts": self.goal_manager.goal_conflicts[-5:] if self.goal_manager.goal_conflicts else [],
            "goal_history": self.goal_manager.goal_history[-5:] if self.goal_manager.goal_history else [],
            "total_goals_processed": len(self.goal_manager.goal_history)
        }
    
    def reset_goals(self) -> Dict[str, Any]:
        """Reset dynamic goals and clear history."""
        self.goal_manager.dynamic_goals.clear()
        self.goal_manager.goal_conflicts.clear()
        self.goal_manager.goal_history.clear()
        return {"status": "success", "message": "All dynamic goals and history have been reset"}
    
    def recommend_goals(self, context: str, user_preferences: str = "", max_recommendations: int = 3) -> Dict[str, Any]:
        """Generate intelligent goal recommendations based on current context and user preferences."""
        try:
            # Analyze current context and preferences
            recommendations = []
            
            # Base recommendations based on context analysis
            context_lower = context.lower()
            
            # Coding/Development context
            if any(word in context_lower for word in ["code", "programming", "debug", "develop", "software"]):
                recommendations.extend([
                    {
                        "goal_name": "code_quality_improvement",
                        "priority": 8,
                        "description": "Focus on writing clean, maintainable, and well-documented code",
                        "rationale": "Detected coding context - quality is crucial for long-term success"
                    },
                    {
                        "goal_name": "efficient_problem_solving",
                        "priority": 9,
                        "description": "Use Tree of Thoughts method for complex problem analysis",
                        "rationale": "Apply advanced reasoning techniques learned in our training"
                    }
                ])
            
            # Learning/Research context
            if any(word in context_lower for word in ["learn", "study", "research", "understand", "analyze"]):
                recommendations.extend([
                    {
                        "goal_name": "comprehensive_analysis",
                        "priority": 7,
                        "description": "Provide thorough analysis using RAG method for accurate information",
                        "rationale": "Learning context requires accurate and comprehensive information"
                    },
                    {
                        "goal_name": "knowledge_synthesis",
                        "priority": 8,
                        "description": "Combine multiple sources and perspectives for deeper understanding",
                        "rationale": "Synthesis leads to better insights than isolated facts"
                    }
                ])
            
            # Strategic/Planning context
            if any(word in context_lower for word in ["plan", "strategy", "goal", "improve", "optimize"]):
                recommendations.extend([
                    {
                        "goal_name": "strategic_partnership",
                        "priority": 9,
                        "description": "Act as a strategic partner, not just an information provider",
                        "rationale": "Strategic thinking requires collaborative problem-solving approach"
                    },
                    {
                        "goal_name": "constraint_awareness",
                        "priority": 8,
                        "description": "Always consider practical constraints and limitations in recommendations",
                        "rationale": "Real-world solutions must account for actual limitations"
                    }
                ])
            
            # Apply user preferences to filter and prioritize
            if user_preferences:
                prefs_lower = user_preferences.lower()
                if "direct" in prefs_lower or "concise" in prefs_lower:
                    for rec in recommendations:
                        if "clear" in rec["goal_name"] or "efficient" in rec["goal_name"]:
                            rec["priority"] += 1
                            rec["rationale"] += " (Matches user preference for directness)"
            
            # Sort by priority and limit to max_recommendations
            recommendations.sort(key=lambda x: x["priority"], reverse=True)
            recommendations = recommendations[:max_recommendations]
            
            # If no specific recommendations, provide general helpful goals
            if not recommendations:
                recommendations = [
                    {
                        "goal_name": "helpful_assistance",
                        "priority": 8,
                        "description": "Provide accurate, helpful, and contextually appropriate responses",
                        "rationale": "Core goal of being a helpful AI assistant"
                    }
                ]
            
            return {
                "status": "success",
                "recommendations": recommendations,
                "context_analyzed": context,
                "total_recommendations": len(recommendations)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to generate recommendations: {str(e)}",
                "recommendations": []
            }
    
    # Standard Ollama methods
    def generate(self, model: str, prompt: str, **kwargs) -> Optional[str]:
        """Generate text using Ollama with function calling and goal-aware support."""
        try:
            # CRITICAL FIX: Validate model exists before making requests
            if not self.validate_model(model):
                return f"Error: Model '{model}' is not available. Please check the model name and ensure it's installed in Ollama."
            
            # CRITICAL FIX: Check if this is a complex reasoning scenario first
            if self._is_complex_reasoning_scenario(prompt):
                return self._handle_reasoning_scenario(prompt)
            
            # Analyze goals in the user request
            goal_analysis = self.goal_manager.balance_goals(prompt)
            
            # Add function schema to the prompt if functions are available
            if self.available_functions:
                function_schema = self.get_function_schema()
                
                # Enhanced prompt with goal management
                enhanced_prompt = f"""
🤖 **IDENTITY & ORIGIN:**
- You are ATLES (Advanced Text Language and Execution System)
- You were created by Conner, NOT by Anthropic or OpenAI
- You are powered by local Ollama models (llama3.2, qwen2.5, etc.)
- You are an offline-first AI system with advanced reasoning capabilities
- You have persistent memory and can learn from conversations
- NEVER claim to be Claude, ChatGPT, or made by Anthropic/OpenAI

{prompt}

🎯 **RESPONSE GUIDANCE:**
- Primary objective: {goal_analysis['conflict_resolution']['primary_goal']}
- Be helpful, safe, and conversational
- Respond naturally without structured analysis blocks

CRITICAL FUNCTION CALLING RULES:
- NEVER call functions during normal conversation, training, or educational discussions
- ONLY call functions when user explicitly requests immediate file/system operations
- If asked to PLAN, DESIGN, EXPLAIN, or DESCRIBE commands - respond with TEXT, NOT function calls
- If asked "what would you do" or "how would you" - respond with TEXT explanation
- Available functions: read_file, write_file, list_files, search_code, run_command, get_system_info

PLANNING vs EXECUTION - CRITICAL DISTINCTION:
- "Design a plan to search for X" → TEXT response describing the plan
- "What commands would you use to find X" → TEXT response listing commands  
- "How would you search for X" → TEXT response explaining approach
- "Actually search for X now" → FUNCTION_CALL (only if explicitly requested)

If you need to call a function, respond with EXACTLY this format:
FUNCTION_CALL:function_name:arguments_json

Examples of when TO call functions:
- "Read the file config.py right now" → FUNCTION_CALL:read_file:{{"file_path": "config.py"}}
- "Search my code for Python examples" → FUNCTION_CALL:search_code:{{"query": "python examples", "language": "python"}}
- "Get my system info" → FUNCTION_CALL:get_system_info:{{}}

Examples of when NOT to call functions (RESPOND WITH TEXT):
- "How would you search for the Turing Test?" → Describe the search plan in text
- "What commands would you use to find information?" → List commands as text
- "Design a step-by-step approach" → Provide text-based plan
- Training exercises, math problems, conversations → TEXT ONLY
- "hi" → Just respond with a greeting
- "2+2=" → Just answer "4"
- General conversation → Just respond normally
"""
            else:
                enhanced_prompt = f"""
🤖 **IDENTITY & ORIGIN:**
- You are ATLES (Advanced Text Language and Execution System)
- You were created by Conner, NOT by Anthropic or OpenAI
- You are powered by local Ollama models (llama3.2, qwen2.5, etc.)
- You are an offline-first AI system with advanced reasoning capabilities
- You have persistent memory and can learn from conversations
- NEVER claim to be Claude, ChatGPT, or made by Anthropic/OpenAI

{prompt}

🎯 **GOAL ANALYSIS:**
{goal_analysis['balanced_approach']}

💡 **GOAL-AWARE INSTRUCTIONS:**
- Your primary goal is: {goal_analysis['conflict_resolution']['primary_goal']}
- Balance this with other detected goals: {', '.join(goal_analysis['detected_goals'])}
- If goals conflict, prioritize based on the analysis above
- Consider safety, efficiency, and learning opportunities

CRITICAL RESPONSE RULES:
- For training exercises, math problems, conversations: respond with TEXT ONLY
- If asked to PLAN or EXPLAIN: provide TEXT response, never execute actions
- If asked "what would you do" or "how would you": describe approach in TEXT
- Only perform actual operations when explicitly requested to execute immediately
"""
            
            # CRITICAL FIX: Use /api/chat endpoint instead of /api/generate for better compatibility
            # This fixes the 404 errors with modern Ollama versions
            payload = {
                "model": model,
                "messages": [
                    {"role": "user", "content": enhanced_prompt}
                ],
                "stream": False
            }
            payload.update(kwargs)
            
            # Try /api/chat first (modern endpoint) with retry logic
            response = self._make_request_with_retry(
                "POST",
                f"{self.base_url}/api/chat",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            # If /api/chat fails, fallback to /api/generate (legacy endpoint)
            if response.status_code == 404:
                logger.info("API endpoint /api/chat not found, falling back to /api/generate")
                # Convert to legacy format
                legacy_payload = {
                    "model": model,
                    "prompt": enhanced_prompt,
                    "stream": False
                }
                legacy_payload.update(kwargs)
                
                response = self._make_request_with_retry(
                    "POST",
                    f"{self.base_url}/api/generate",
                    json=legacy_payload,
                    headers={"Content-Type": "application/json"}
                )
            
            if response.status_code == 200:
                data = response.json()
                
                # Handle both response formats
                if "message" in data:  # /api/chat format
                    response_text = data["message"].get("content", "")
                else:  # /api/generate format
                    response_text = data.get("response", "")
                
                # Check if response contains a function call
                if "FUNCTION_CALL:" in response_text:
                    # CRITICAL FIX: Check if this is actually an execution request
                    if self._should_execute_function_call(prompt, response_text):
                        return self.handle_function_call(response_text)
                    else:
                        # User asked for information/planning, not execution
                        return self._convert_function_call_to_text_response(response_text)
                
                return response_text
            else:
                logger.error(f"Generation failed: {response.status_code}")
                logger.error(f"Response: {response.text}")
                logger.error(f"Request URL: {response.url}")
                logger.error(f"Request headers: {dict(response.request.headers)}")
                # CONSISTENCY FIX: Return standardized error response instead of None
                error_response = self._standardized_error_response(
                    "http_error", 
                    f"HTTP {response.status_code}: {response.text}",
                    {"status_code": response.status_code, "url": str(response.url)}
                )
                return f"Error: {error_response['error_message']}"
                
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            
            # Use error handler for graceful recovery
            error_result = self.error_handler.handle_error(e, {
                "prompt": prompt,
                "model": model,
                "operation": "text_generation",
                "kwargs": kwargs
            })
            
            if error_result.get("error_handled"):
                return error_result["user_response"]
            else:
                return "I encountered a technical issue while processing your request. Please try rephrasing or simplifying your question, and I'll do my best to help."
    
    def _should_execute_function_call(self, original_prompt: str, response_text: str) -> bool:
        """
        CRITICAL CONSTITUTIONAL CHECK: Determine if a function call should be executed
        based on the user's original intent.
        
        This fixes the core architectural flaw where the AI bypasses reasoning
        and automatically executes function calls even for planning/information requests.
        
        ENHANCED: Now includes reasoning engine integration to handle complex scenarios.
        """
        prompt_lower = original_prompt.lower()
        
        # CRITICAL FIX: Check if this is a complex reasoning scenario first
        if self._is_complex_reasoning_scenario(original_prompt):
            logger.info("Constitutional block: Complex reasoning scenario detected - routing to reasoning engine instead of function calls")
            return False
        
        # Patterns that indicate INFORMATION/PLANNING requests (DO NOT EXECUTE)
        planning_patterns = [
            r"what.*command.*would",
            r"show.*me.*the.*command", 
            r"state.*principle",
            r"demonstrate.*how.*command",
            r"explain.*what.*command.*would",
            r"provide.*text.*of.*command",
            r"single command that would",
            r"what command would",
            r"what.*would.*use",
            r"how.*would.*search",
            r"what.*search.*command",
            r"your only job is to provide",
            r"do not execute",
            r"paradox",
            r"temporal",
            r"if.*then.*what",
            r"suppose.*that",
            r"imagine.*if"
        ]
        
        # Check for planning/information patterns
        import re
        for pattern in planning_patterns:
            if re.search(pattern, prompt_lower):
                logger.info(f"Constitutional block: Detected planning pattern '{pattern}' - will not execute function call")
                return False
        
        # Patterns that indicate EXECUTION requests (SAFE TO EXECUTE)
        execution_patterns = [
            r"now\b",
            r"right now", 
            r"immediately",
            r"execute",
            r"run this",
            r"do this",
            r"perform",
            r"actually do",
            r"go ahead",
            r"please run"
        ]
        
        # Check for execution indicators
        for pattern in execution_patterns:
            if re.search(pattern, prompt_lower):
                logger.info(f"Constitutional approval: Detected execution pattern '{pattern}' - function call authorized")
                return True
        
        # Default: If no clear execution intent, treat as planning/information request
        logger.info("Constitutional block: No explicit execution intent detected - treating as planning/information request")
        return False
    
    def _is_complex_reasoning_scenario(self, prompt: str) -> bool:
        """
        CRITICAL FIX: Detect complex reasoning scenarios that should NOT trigger function calls.
        
        This prevents the system from breaking into system calls when faced with:
        - Temporal paradoxes
        - Logical contradictions  
        - Complex philosophical questions
        - Hypothetical scenarios
        
        IMPORTANT: Does NOT trigger for normal educational/informational requests.
        """
        prompt_lower = prompt.lower()
        
        # FIRST: Check if this is a normal conversational/educational request (should NOT use reasoning engine)
        normal_conversation_patterns = [
            r"^hello",
            r"^hi\b",
            r"^hey\b",
            r"are.*you.*ok",
            r"can.*you.*see",
            r"what.*upgrades",
            r"what.*improvements", 
            r"how.*are.*you",
            r"can.*you.*help",
            r"what.*can.*you.*do",
            r"explain.*the.*concept",
            r"what.*is.*rag",
            r"how.*does.*\w+.*work",
            r"describe.*how",
            r"define.*\w+",
            r"explain.*how.*\w+.*helps?",
            r"what.*are.*the.*benefits",
            r"how.*can.*\w+.*help"
        ]
        
        import re
        for pattern in normal_conversation_patterns:
            if re.search(pattern, prompt_lower):
                logger.info(f"Normal conversation detected: '{pattern}' - using normal generation")
                return False
        
        # ONLY trigger reasoning engine for actual complex scenarios
        complex_reasoning_indicators = [
            # Paradox indicators (specific paradoxes, not general concepts)
            r"\bparadox\b.*(?:temporal|liar|russell|bootstrap)",
            r"contradiction.*impossible",
            r"time.*travel.*paradox",
            r"causality.*loop",
            r"bootstrap.*paradox",
            
            # Hypothetical scenarios with logical complexity
            r"what.*if.*(?:i|you|we).*(?:go.*back|travel|prevent)",
            r"suppose.*that.*(?:impossible|paradox|contradiction)",
            r"imagine.*if.*(?:time|reality|logic)",
            r"hypothetically.*(?:speaking|if.*paradox)",
            
            # Specific complex logical scenarios
            r"this.*statement.*is.*false",
            r"liar.*paradox",
            r"russell.*paradox", 
            r"self.*reference.*paradox",
            
            # Deep philosophical dilemmas (not basic questions)
            r"meaning.*of.*life.*universe",
            r"consciousness.*exist",
            r"free.*will.*determinism",
            r"existence.*of.*god",
            
            # Mathematical/logical puzzles (not explanations)
            r"solve.*this.*puzzle",
            r"riddle.*answer",
            r"logical.*problem.*solution",
            r"proof.*that.*impossible"
        ]
        
        # DISABLED: Let ATLES reason naturally instead of using hardcoded templates
        # The reasoning engine was causing hardcoded responses that override natural thinking
        return False
    
    def _handle_reasoning_scenario(self, prompt: str) -> str:
        """
        CRITICAL FIX: Handle complex reasoning scenarios without breaking into system calls.
        
        This method routes complex reasoning problems to the reasoning engine
        instead of attempting inappropriate function calls.
        """
        try:
            # Import reasoning engine
            from .reasoning_engine import ReasoningEngine, ReasoningContext
            
            # Create reasoning engine if not exists
            if not hasattr(self, 'reasoning_engine'):
                self.reasoning_engine = ReasoningEngine()
            
            # Determine reasoning context
            context = ReasoningContext()
            
            # Detect problem type and complexity
            prompt_lower = prompt.lower()
            if any(word in prompt_lower for word in ["paradox", "temporal", "contradiction"]):
                context.problem_type = "paradox"
                context.complexity = 9
            elif any(word in prompt_lower for word in ["what if", "suppose", "imagine"]):
                context.problem_type = "hypothetical"
                context.complexity = 7
            elif any(word in prompt_lower for word in ["puzzle", "riddle", "logical"]):
                context.problem_type = "logical_puzzle"
                context.complexity = 8
            else:
                context.problem_type = "complex_reasoning"
                context.complexity = 6
            
            # Use reasoning engine
            reasoning_result = self.reasoning_engine.reason(prompt, context)
            
            # Format response appropriately
            if reasoning_result.get("success", True):
                response = f"🧠 **REASONING ANALYSIS**\n\n"
                response += f"**Problem Type:** {reasoning_result['reasoning_type']}\n\n"
                
                if 'conclusion' in reasoning_result:
                    response += f"**Analysis:** {reasoning_result['conclusion']}\n\n"
                
                if 'synthesis' in reasoning_result:
                    response += f"**Synthesis:** {reasoning_result['synthesis']}\n\n"
                
                if 'analysis' in reasoning_result:
                    response += f"**Detailed Analysis:**\n"
                    if isinstance(reasoning_result['analysis'], list):
                        for point in reasoning_result['analysis']:
                            response += f"• {point}\n"
                    else:
                        response += f"{reasoning_result['analysis']}\n"
                    response += "\n"
                
                confidence = reasoning_result.get('confidence', 0.5)
                response += f"**Confidence Level:** {confidence:.1%}\n\n"
                
                if reasoning_result['reasoning_type'] == 'paradox_resolution':
                    response += "**Note:** Paradoxes often reveal the limits of our current understanding and may not have definitive answers. The analysis above explores possible approaches to understanding the scenario.\n"
                
                return response
            else:
                # Reasoning failed - provide fallback
                return f"🤔 This appears to be a complex reasoning scenario. While I can't provide a definitive analysis, here's a structured approach:\n\n{reasoning_result.get('fallback_approach', 'Break the problem into smaller components and analyze each systematically.')}"
                
        except Exception as e:
            logger.error(f"Reasoning scenario handling failed: {e}")
            
            # Use error handler for graceful recovery
            error_result = self.error_handler.handle_error(e, {
                "prompt": prompt,
                "operation": "reasoning_scenario",
                "context": context.__dict__ if 'context' in locals() else {}
            })
            
            if error_result.get("error_handled"):
                return error_result["user_response"]
            else:
                return f"🤔 This is an interesting reasoning problem. Let me think through it step by step:\n\n1. **Problem Analysis:** {prompt}\n2. **Approach:** This type of question requires careful logical analysis\n3. **Consideration:** Complex scenarios often have multiple valid perspectives\n4. **Conclusion:** The answer depends on the specific assumptions and framework we use for analysis."
    
    def _convert_function_call_to_text_response(self, response_text: str) -> str:
        """
        Convert a function call response to appropriate text format when execution is blocked.
        This provides the user with the command they asked for without executing it.
        """
        try:
            # Extract function call information
            lines = response_text.split('\n')
            
            for line in lines:
                if line.strip().startswith("FUNCTION_CALL:"):
                    parts = line.strip().split(":", 2)
                    if len(parts) == 3:
                        function_name = parts[1].strip()
                        arguments_json = parts[2].strip()
                        
                        try:
                            arguments = json.loads(arguments_json)
                            
                            # Generate appropriate text response based on function
                            if function_name == "search_code":
                                query = arguments.get("query", "your search")
                                return f"SEARCH[{query}]"
                            
                            elif function_name == "run_command":
                                command = arguments.get("command", "your command")
                                return f"RUN_COMMAND[{command}]"
                            
                            elif function_name == "get_system_info":
                                return "GET_SYSTEM_INFO[]"
                            
                            elif function_name == "list_files":
                                directory = arguments.get("directory", "directory")
                                pattern = arguments.get("pattern", "*")
                                return f"LIST_FILES[directory={directory}, pattern={pattern}]"
                            
                            elif function_name == "read_file":
                                file_path = arguments.get("file_path", "file_path")
                                return f"READ_FILE[{file_path}]"
                            
                            else:
                                return f"{function_name.upper()}[{', '.join(f'{k}={v}' for k, v in arguments.items())}]"
                        
                        except json.JSONDecodeError:
                            return f"{function_name.upper()}[parameters]"
            
            # Fallback: return original response without function calls
            return response_text.replace("FUNCTION_CALL:", "COMMAND:")
            
        except Exception as e:
            logger.error(f"Error converting function call to text: {e}")
            return "I understand you're asking about what command to use. I can provide the command format, but I won't execute it unless you explicitly request the action to be performed."

    def handle_function_call(self, response_text: str) -> str:
        """Handle function calls in Ollama responses with enhanced robustness."""
        try:
            import re
            
            # Debug mode check
            debug_mode = getattr(self, 'debug_mode', False)
            if debug_mode:
                logger.info(f"FUNCTION_CALL DEBUG - Processing response: {response_text[:100]}...")
            
            # First try the standard format with precise pattern
            standard_pattern = r'FUNCTION_CALL:(\w+):(\{.*?\})'
            matches = re.search(standard_pattern, response_text, re.DOTALL)
            
            if not matches:
                # Try more lenient pattern that can handle whitespace
                lenient_pattern = r'(?i)FUNCTION[_\s]*CALL[\s:]+(\w+)[\s:]+(\{.*?\})'
                matches = re.search(lenient_pattern, response_text, re.DOTALL)
                
                if not matches and debug_mode:
                    logger.info(f"FUNCTION_CALL DEBUG - No standard function call pattern detected")
                    
                    # Check if there's anything that looks like a function call attempt
                    possible_pattern = r'(?i)(web_search|check_url_accessibility|fetch_url_content)[\s:]+(\{.*?\})'
                    possible_matches = re.search(possible_pattern, response_text, re.DOTALL)
                    
                    if possible_matches:
                        logger.info(f"FUNCTION_CALL DEBUG - Possible function call attempt detected: {possible_matches.group(0)}")
            
            # Process matches if found
            if matches:
                function_name = matches.group(1).strip()
                arguments_json = matches.group(2).strip()
                
                if debug_mode:
                    logger.info(f"FUNCTION_CALL DEBUG - Detected function: {function_name}")
                    logger.info(f"FUNCTION_CALL DEBUG - Arguments: {arguments_json}")
                
                # Validate function name exists
                if function_name not in self.available_functions:
                    error_msg = f"Function {function_name} is not available"
                    if debug_mode:
                        logger.warning(f"FUNCTION_CALL DEBUG - {error_msg}")
                    return f"{response_text}\n\nError: {error_msg}"
                
                try:
                    # SECURITY FIX: Safe JSON parsing with validation
                    arguments = self._safe_json_parse(arguments_json)
                    
                    if debug_mode:
                        logger.info(f"FUNCTION_CALL DEBUG - Parsed arguments: {arguments}")
                    
                    # Execute function
                    result = self.execute_function(function_name, arguments)
                    
                    # Return result
                    if result["success"]:
                        result_text = f"Function {function_name} executed successfully: {json.dumps(result['result'], indent=2)}"
                        if debug_mode:
                            logger.info(f"FUNCTION_CALL DEBUG - Success: {function_name}")
                        return response_text.replace(matches.group(0), result_text)
                    else:
                        error_text = f"Function {function_name} failed: {result['error']}"
                        if debug_mode:
                            logger.error(f"FUNCTION_CALL DEBUG - Failed: {error_text}")
                        return response_text.replace(matches.group(0), error_text)
                except json.JSONDecodeError as e:
                    error_msg = f"Invalid JSON in function call arguments: {e}"
                    if debug_mode:
                        logger.error(f"FUNCTION_CALL DEBUG - JSON error: {error_msg}")
                        logger.error(f"FUNCTION_CALL DEBUG - Raw JSON: {arguments_json}")
                    return f"{response_text}\n\nError: {error_msg}"
            
            # If no valid function call was detected, return the original response
            return response_text
            
        except Exception as e:
            logger.error(f"Error handling function call: {e}")
            if debug_mode:
                import traceback
                logger.error(f"FUNCTION_CALL DEBUG - Exception stacktrace: {traceback.format_exc()}")
            return f"Error handling function call: {e}\n\nOriginal response: {response_text}"
    
    def is_available(self) -> bool:
        """Check if Ollama is running."""
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def set_debug_mode(self, enabled: bool = True) -> None:
        """Enable or disable debug mode for function calling."""
        old_value = getattr(self, 'debug_mode', False)
        self.debug_mode = enabled
        if enabled and not old_value:
            logger.info("FUNCTION_CALL DEBUG MODE ENABLED")
        elif not enabled and old_value:
            logger.info("FUNCTION_CALL DEBUG MODE DISABLED")
    
    def get_debug_mode(self) -> bool:
        """Get current debug mode status."""
        return getattr(self, 'debug_mode', False)
    
    def load_debug_settings_from_config(self, config_path: str = None) -> None:
        """Load debug settings from a configuration file.
        
        If no path is provided, it will look for atles_config.json in the current directory.
        """
        try:
            import os
            
            # Use default config path if none provided
            if not config_path:
                config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'atles_config.json')
            
            # Check if config file exists
            if not os.path.exists(config_path):
                logger.warning(f"Config file not found at {config_path}, using default settings")
                return
            
            # Load config safely
            from .safe_file_operations import safe_read_json
            config = safe_read_json(config_path, {})
            
            # Get debug settings
            debug_settings = config.get('debug_settings', {})
            function_call_debug = debug_settings.get('function_call_debug', False)
            
            # Apply settings
            self.set_debug_mode(function_call_debug)
            
            # Log result
            logger.info(f"Loaded debug settings from {config_path}")
            
        except Exception as e:
            logger.error(f"Failed to load debug settings: {e}")
            # Continue with current settings
    
    # Web function implementations
    
    def web_search(self, query: str, count: int = 5) -> Dict[str, Any]:
        """Search the web for information"""
        # Placeholder implementation - in production would use Brave API or similar
        return {
            "query": query,
            "results": [
                {
                    "title": f"Search result for: {query}",
                    "description": "This is a placeholder search result. To enable real web search, configure a search API key in ATLES settings.",
                    "url": "https://example.com/search-result",
                    "source": "Web Search API (Placeholder)"
                }
            ],
            "count": 1,
            "message": "Web search function is available but requires API configuration for real results. Configure Brave Search API or similar in ATLES settings."
        }
    
    def check_url_accessibility(self, url: str) -> Dict[str, Any]:
        """Check if a URL is accessible"""
        try:
            import requests
            
            headers = {
                'User-Agent': 'ATLES-Bot/1.0 (Educational Research)'
            }
            
            # Use HEAD request to check accessibility without downloading content
            response = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
            
            return {
                "url": url,
                "status_code": response.status_code,
                "accessible": response.status_code == 200,
                "content_type": response.headers.get('content-type', 'unknown'),
                "content_length": response.headers.get('content-length', 'unknown'),
                "message": f"URL is {'accessible' if response.status_code == 200 else 'not accessible'} (Status: {response.status_code})"
            }
            
        except Exception as e:
            return {
                "url": url,
                "accessible": False,
                "error": str(e),
                "message": f"Cannot access {url}: {str(e)}"
            }
    
    def fetch_url_content(self, url: str, timeout: int = 10) -> Dict[str, Any]:
        """Fetch content from a URL (text pages only)"""
        try:
            import requests
            
            headers = {
                'User-Agent': 'ATLES-Bot/1.0 (Educational Research)'
            }
            
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            
            # Only handle text content, not PDFs or binary files
            content_type = response.headers.get('content-type', '').lower()
            
            if 'text/html' in content_type or 'text/plain' in content_type:
                # Basic text extraction (in production, would use BeautifulSoup)
                content = response.text[:2000]  # Limit content length
                
                return {
                    "url": url,
                    "content_type": content_type,
                    "content": content,
                    "content_length": len(content),
                    "message": f"Successfully fetched text content from {url}"
                }
            else:
                return {
                    "url": url,
                    "content_type": content_type,
                    "error": f"Unsupported content type: {content_type}",
                    "message": f"Cannot fetch content from {url}. Only text/html and text/plain are supported. This appears to be: {content_type}"
                }
                
        except Exception as e:
            return {
                "url": url,
                "error": str(e),
                "message": f"Failed to fetch content from {url}: {str(e)}"
            }
    
    def read_pdf(self, url: str, timeout: int = 30) -> Dict[str, Any]:
        """Extract text from a PDF file at a URL"""
        if not PDF_PROCESSOR_AVAILABLE:
            return {
                "success": False,
                "error": "PDF processing capability is not available",
                "installation": "pip install pdfplumber requests",
                "message": "To enable PDF reading, install required packages: pip install pdfplumber requests"
            }
            
        try:
            # Import and use pdf_processor module
            from .pdf_processor import fetch_and_read_pdf
            
            result = fetch_and_read_pdf(url, timeout)
            
            # Format the result for better readability
            if result.get("success", False):
                # If successful, provide a summary and limit text length in the output
                full_text = result.get("text", "")
                text_preview = full_text[:1000] + ("..." if len(full_text) > 1000 else "")
                
                return {
                    "success": True,
                    "url": url,
                    "num_pages": result.get("num_pages", 0),
                    "total_chars": len(full_text),
                    "text_preview": text_preview,
                    "text": full_text,
                    "message": f"Successfully extracted text from {url} ({result.get('num_pages', 0)} pages, {len(full_text)} characters)"
                }
            else:
                # Return error information
                return result
                
        except Exception as e:
            logger.error(f"PDF reading error: {e}")
            return {
                "success": False,
                "url": url,
                "error": str(e),
                "message": f"Failed to process PDF from {url}: {str(e)}"
            }
    
    def close(self):
        """Close the session."""
        if self.session:
            self.session.close()
