#!/usr/bin/env python3
"""
ATLES Enhanced Error Handler
Provides robust error handling for complex reasoning scenarios and prevents
system crashes when encountering temporal paradoxes or edge cases.
"""

import logging
import traceback
import json
from typing import Dict, Any, Optional, List, Tuple, Union
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    """Categories of errors ATLES can encounter"""
    REASONING_FAILURE = "reasoning_failure"
    PARADOX_HANDLING = "paradox_handling"
    FUNCTION_CALL_ERROR = "function_call_error"
    MEMORY_ERROR = "memory_error"
    CONSTITUTIONAL_VIOLATION = "constitutional_violation"
    SYSTEM_ERROR = "system_error"
    USER_INPUT_ERROR = "user_input_error"
    TEMPORAL_LOGIC_ERROR = "temporal_logic_error"

class ATLESError(Exception):
    """Base exception class for ATLES-specific errors"""
    
    def __init__(self, message: str, category: ErrorCategory, severity: ErrorSeverity, 
                 context: Optional[Dict[str, Any]] = None, recovery_suggestion: Optional[str] = None):
        super().__init__(message)
        self.category = category
        self.severity = severity
        self.context = context or {}
        self.recovery_suggestion = recovery_suggestion
        self.timestamp = datetime.now().isoformat()

class ReasoningError(ATLESError):
    """Errors related to reasoning failures"""
    pass

class ParadoxError(ATLESError):
    """Errors related to paradox handling"""
    pass

class TemporalLogicError(ATLESError):
    """Errors related to temporal logic problems"""
    pass

class ErrorHandler:
    """
    Comprehensive error handler for ATLES that provides graceful degradation
    and recovery strategies for complex scenarios.
    """
    
    def __init__(self):
        self.error_history = []
        self.recovery_strategies = {
            ErrorCategory.REASONING_FAILURE: self._handle_reasoning_failure,
            ErrorCategory.PARADOX_HANDLING: self._handle_paradox_error,
            ErrorCategory.FUNCTION_CALL_ERROR: self._handle_function_call_error,
            ErrorCategory.MEMORY_ERROR: self._handle_memory_error,
            ErrorCategory.CONSTITUTIONAL_VIOLATION: self._handle_constitutional_violation,
            ErrorCategory.SYSTEM_ERROR: self._handle_system_error,
            ErrorCategory.USER_INPUT_ERROR: self._handle_user_input_error,
            ErrorCategory.TEMPORAL_LOGIC_ERROR: self._handle_temporal_logic_error
        }
        
        self.fallback_responses = {
            ErrorCategory.REASONING_FAILURE: "I encountered a reasoning challenge. Let me approach this differently by breaking it into smaller components.",
            ErrorCategory.PARADOX_HANDLING: "This appears to be a paradox or logical contradiction. Such scenarios often require careful analysis of underlying assumptions.",
            ErrorCategory.TEMPORAL_LOGIC_ERROR: "This involves temporal logic that's challenging to resolve definitively. Let me explore different temporal frameworks.",
            ErrorCategory.FUNCTION_CALL_ERROR: "I encountered an issue with system operations. Let me provide the information in a different format.",
            ErrorCategory.CONSTITUTIONAL_VIOLATION: "This request conflicts with my operational principles. Let me suggest an alternative approach.",
            ErrorCategory.MEMORY_ERROR: "I'm having difficulty accessing previous context. Let me work with the current information available.",
            ErrorCategory.SYSTEM_ERROR: "I encountered a technical issue. Let me try a different approach to help you.",
            ErrorCategory.USER_INPUT_ERROR: "I'm having trouble understanding the request. Could you rephrase or provide more context?"
        }
    
    def handle_error(self, error: Union[Exception, ATLESError], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Main error handling entry point. Provides graceful error handling
        and recovery strategies.
        """
        try:
            # Convert regular exceptions to ATLES errors
            if not isinstance(error, ATLESError):
                atles_error = self._convert_to_atles_error(error, context)
            else:
                atles_error = error
            
            # Log the error
            self._log_error(atles_error)
            
            # Add to error history
            self._record_error(atles_error)
            
            # Get recovery strategy
            recovery_handler = self.recovery_strategies.get(
                atles_error.category, 
                self._handle_generic_error
            )
            
            # Execute recovery strategy
            recovery_result = recovery_handler(atles_error, context or {})
            
            return {
                "error_handled": True,
                "error_category": atles_error.category.value,
                "error_severity": atles_error.severity.value,
                "recovery_strategy": recovery_result["strategy"],
                "user_response": recovery_result["response"],
                "technical_details": recovery_result.get("technical_details"),
                "suggestions": recovery_result.get("suggestions", []),
                "timestamp": atles_error.timestamp
            }
            
        except Exception as e:
            # Meta-error: error in error handling
            logger.critical(f"Error in error handler: {e}")
            return self._emergency_fallback(error, e)
    
    def _convert_to_atles_error(self, error: Exception, context: Optional[Dict[str, Any]]) -> ATLESError:
        """Convert regular exceptions to ATLES errors with appropriate categorization"""
        error_str = str(error).lower()
        error_type = type(error).__name__
        
        # Categorize based on error content and type
        if any(word in error_str for word in ["paradox", "contradiction", "temporal", "causality"]):
            category = ErrorCategory.PARADOX_HANDLING
            severity = ErrorSeverity.MEDIUM
        elif any(word in error_str for word in ["reasoning", "logic", "analysis"]):
            category = ErrorCategory.REASONING_FAILURE
            severity = ErrorSeverity.MEDIUM
        elif any(word in error_str for word in ["function", "call", "execution"]):
            category = ErrorCategory.FUNCTION_CALL_ERROR
            severity = ErrorSeverity.LOW
        elif any(word in error_str for word in ["memory", "context", "session"]):
            category = ErrorCategory.MEMORY_ERROR
            severity = ErrorSeverity.MEDIUM
        elif any(word in error_str for word in ["constitutional", "principle", "violation"]):
            category = ErrorCategory.CONSTITUTIONAL_VIOLATION
            severity = ErrorSeverity.HIGH
        elif error_type in ["TimeoutError", "ConnectionError", "SystemError"]:
            category = ErrorCategory.SYSTEM_ERROR
            severity = ErrorSeverity.HIGH
        else:
            category = ErrorCategory.SYSTEM_ERROR
            severity = ErrorSeverity.MEDIUM
        
        return ATLESError(
            message=str(error),
            category=category,
            severity=severity,
            context=context,
            recovery_suggestion=self._generate_recovery_suggestion(category, error_str)
        )
    
    def _generate_recovery_suggestion(self, category: ErrorCategory, error_str: str) -> str:
        """Generate recovery suggestions based on error category"""
        suggestions = {
            ErrorCategory.REASONING_FAILURE: "Try breaking the problem into smaller, more manageable components",
            ErrorCategory.PARADOX_HANDLING: "Consider examining the underlying assumptions that lead to the paradox",
            ErrorCategory.FUNCTION_CALL_ERROR: "Verify the function parameters and try a simpler approach",
            ErrorCategory.MEMORY_ERROR: "Restart the conversation or provide more context",
            ErrorCategory.CONSTITUTIONAL_VIOLATION: "Rephrase the request to align with operational principles",
            ErrorCategory.SYSTEM_ERROR: "Try again in a moment or restart the system",
            ErrorCategory.TEMPORAL_LOGIC_ERROR: "Consider different temporal frameworks or models",
            ErrorCategory.USER_INPUT_ERROR: "Provide more specific or clearer input"
        }
        return suggestions.get(category, "Try a different approach or restart the operation")
    
    def _log_error(self, error: ATLESError):
        """Log error with appropriate level based on severity"""
        log_message = f"ATLES Error [{error.category.value}]: {error.message}"
        
        if error.severity == ErrorSeverity.CRITICAL:
            logger.critical(log_message, extra={"context": error.context})
        elif error.severity == ErrorSeverity.HIGH:
            logger.error(log_message, extra={"context": error.context})
        elif error.severity == ErrorSeverity.MEDIUM:
            logger.warning(log_message, extra={"context": error.context})
        else:
            logger.info(log_message, extra={"context": error.context})
    
    def _record_error(self, error: ATLESError):
        """Record error in history for pattern analysis"""
        error_record = {
            "timestamp": error.timestamp,
            "category": error.category.value,
            "severity": error.severity.value,
            "message": error.message,
            "context": error.context,
            "recovery_suggestion": error.recovery_suggestion
        }
        
        self.error_history.append(error_record)
        
        # Keep only last 100 errors
        if len(self.error_history) > 100:
            self.error_history = self.error_history[-100:]
    
    # Recovery strategy handlers
    
    def _handle_reasoning_failure(self, error: ATLESError, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle reasoning failures gracefully"""
        return {
            "strategy": "reasoning_fallback",
            "response": f"I encountered a reasoning challenge with this problem. Let me try a different approach:\n\n1. **Simplified Analysis**: Breaking this into basic components\n2. **Alternative Perspective**: Looking at this from a different angle\n3. **Structured Approach**: Using step-by-step logical analysis\n\nWhile I can't provide a complete analysis due to the complexity, I can offer that problems like this often benefit from examining the core assumptions and constraints involved.",
            "suggestions": [
                "Try rephrasing the question in simpler terms",
                "Break the problem into smaller parts",
                "Provide additional context or constraints"
            ]
        }
    
    def _handle_paradox_error(self, error: ATLESError, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle paradox-related errors"""
        return {
            "strategy": "paradox_analysis",
            "response": f"🤔 **Paradox Analysis**\n\nI've encountered what appears to be a logical paradox or contradiction. This is actually quite interesting from a philosophical perspective!\n\n**Analysis Approach:**\n• Paradoxes often reveal limitations in our logical frameworks\n• They may indicate incomplete or inconsistent premises\n• Different logical systems may resolve them differently\n\n**Possible Perspectives:**\n• Classical logic: May reject one of the premises\n• Multi-valued logic: May allow for degrees of truth\n• Temporal logic: May consider time-dependent truth values\n\n**Conclusion:** Paradoxes like this don't always have definitive answers, but exploring them helps us understand the boundaries of logical reasoning.",
            "suggestions": [
                "Examine the assumptions that lead to the paradox",
                "Consider alternative logical frameworks",
                "Look for hidden premises or context"
            ]
        }
    
    def _handle_temporal_logic_error(self, error: ATLESError, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle temporal logic errors - DISABLED to prevent response loops"""
        # Don't provide hardcoded temporal paradox responses - let ATLES reason naturally
        return {
            "strategy": "natural_reasoning",
            "response": "Let me think about this question naturally instead of using a hardcoded template.",
            "suggestions": ["Engage with the actual question being asked"]
        }
    
    def _handle_function_call_error(self, error: ATLESError, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle function call errors"""
        return {
            "strategy": "function_fallback",
            "response": f"I encountered an issue with a system operation. Instead of executing the function, let me provide the information you're looking for in text format.\n\n{self.fallback_responses[ErrorCategory.FUNCTION_CALL_ERROR]}",
            "technical_details": f"Function call error: {error.message}",
            "suggestions": [
                "Try rephrasing the request as a direct question",
                "Specify if you want information about a command vs. executing it",
                "Check if the system operation is available"
            ]
        }
    
    def _handle_memory_error(self, error: ATLESError, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle memory-related errors"""
        return {
            "strategy": "memory_recovery",
            "response": f"I'm having difficulty accessing previous conversation context. Let me work with the current information available and ask for clarification if needed.\n\n{self.fallback_responses[ErrorCategory.MEMORY_ERROR]}",
            "suggestions": [
                "Provide relevant context from earlier in our conversation",
                "Restart the conversation if the issue persists",
                "Be more explicit about what you're referring to"
            ]
        }
    
    def _handle_constitutional_violation(self, error: ATLESError, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle constitutional principle violations"""
        return {
            "strategy": "constitutional_guidance",
            "response": f"🛡️ **Constitutional Guidance**\n\nThis request conflicts with my operational principles. Let me suggest an alternative approach that achieves your goal while maintaining appropriate boundaries.\n\n**Alternative Approaches:**\n• Rephrase the request to focus on information rather than action\n• Consider the underlying goal and find a different path\n• Ask for guidance on best practices instead\n\n{self.fallback_responses[ErrorCategory.CONSTITUTIONAL_VIOLATION]}",
            "suggestions": [
                "Focus on learning about the topic rather than performing actions",
                "Ask for general guidance or best practices",
                "Rephrase to align with helpful assistance principles"
            ]
        }
    
    def _handle_system_error(self, error: ATLESError, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle system-level errors"""
        return {
            "strategy": "system_recovery",
            "response": f"I encountered a technical issue, but I'm still here to help! Let me try a different approach to assist you.\n\n{self.fallback_responses[ErrorCategory.SYSTEM_ERROR]}",
            "technical_details": f"System error: {error.message}",
            "suggestions": [
                "Try the request again in a moment",
                "Simplify the request if it was complex",
                "Restart the application if issues persist"
            ]
        }
    
    def _handle_user_input_error(self, error: ATLESError, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle user input errors"""
        return {
            "strategy": "input_clarification",
            "response": f"I'm having trouble understanding your request. Could you help me by providing more details or rephrasing?\n\n**What would help:**\n• More specific details about what you're looking for\n• Context about the problem you're trying to solve\n• Examples of what you have in mind\n\n{self.fallback_responses[ErrorCategory.USER_INPUT_ERROR]}",
            "suggestions": [
                "Provide more context about your goal",
                "Break complex requests into smaller parts",
                "Give specific examples of what you're looking for"
            ]
        }
    
    def _handle_generic_error(self, error: ATLESError, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generic error handler for uncategorized errors"""
        return {
            "strategy": "generic_recovery",
            "response": f"I encountered an unexpected issue, but I'm still here to help! Let me try to assist you in a different way.\n\nError details: {error.message}\n\nLet me know how you'd like to proceed, and I'll do my best to help.",
            "suggestions": [
                "Try rephrasing your request",
                "Provide more context about what you're trying to achieve",
                "Break complex requests into simpler parts"
            ]
        }
    
    def _emergency_fallback(self, original_error: Exception, handler_error: Exception) -> Dict[str, Any]:
        """Emergency fallback when error handling itself fails"""
        logger.critical(f"Emergency fallback triggered. Original: {original_error}, Handler: {handler_error}")
        
        return {
            "error_handled": False,
            "emergency_mode": True,
            "user_response": "I encountered a complex technical issue, but I'm still operational. Please try rephrasing your request or starting a new conversation.",
            "technical_details": f"Original error: {original_error}, Handler error: {handler_error}",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get statistics about error patterns"""
        if not self.error_history:
            return {"total_errors": 0, "message": "No errors recorded"}
        
        # Analyze error patterns
        category_counts = {}
        severity_counts = {}
        recent_errors = []
        
        for error in self.error_history:
            category = error["category"]
            severity = error["severity"]
            
            category_counts[category] = category_counts.get(category, 0) + 1
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            # Recent errors (last 10)
            if len(recent_errors) < 10:
                recent_errors.append({
                    "timestamp": error["timestamp"],
                    "category": category,
                    "message": error["message"][:100] + "..." if len(error["message"]) > 100 else error["message"]
                })
        
        return {
            "total_errors": len(self.error_history),
            "category_breakdown": category_counts,
            "severity_breakdown": severity_counts,
            "recent_errors": recent_errors,
            "most_common_category": max(category_counts.items(), key=lambda x: x[1])[0] if category_counts else None,
            "error_rate_trend": "stable"  # Could be enhanced with time-based analysis
        }
    
    def clear_error_history(self):
        """Clear error history (for testing or reset)"""
        self.error_history.clear()
        logger.info("Error history cleared")


# Integration functions
def create_error_handler() -> ErrorHandler:
    """Factory function to create error handler"""
    return ErrorHandler()

def handle_atles_error(error: Exception, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Convenience function for handling ATLES errors"""
    handler = create_error_handler()
    return handler.handle_error(error, context)


# Test function
def test_error_handler():
    """Test the error handler with various error scenarios"""
    handler = ErrorHandler()
    
    print("🧪 Testing ATLES Error Handler")
    print("=" * 50)
    
    # Test different error types
    test_errors = [
        (Exception("Reasoning failed on temporal paradox"), {"prompt": "time travel paradox"}),
        (ValueError("Invalid function call parameters"), {"function": "get_system_info"}),
        (RuntimeError("Memory context lost"), {"session": "user_123"}),
        (TimeoutError("System operation timed out"), {"operation": "file_read"}),
        (ParadoxError("Liar's paradox detected", ErrorCategory.PARADOX_HANDLING, ErrorSeverity.MEDIUM), {})
    ]
    
    for error, context in test_errors:
        print(f"\nTesting error: {type(error).__name__}: {error}")
        result = handler.handle_error(error, context)
        print(f"Strategy: {result['recovery_strategy']}")
        print(f"Response: {result['user_response'][:100]}...")
        print(f"Handled: {result['error_handled']}")
        print("-" * 30)
    
    # Statistics
    stats = handler.get_error_statistics()
    print(f"\n📊 Error Statistics: {stats}")


if __name__ == "__main__":
    test_error_handler()
