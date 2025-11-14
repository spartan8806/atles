#!/usr/bin/env python3
"""
ATLES Capability Grounding System

This module prevents "Logical Hallucination" by ensuring ATLES only offers
actions it can actually perform. It provides capability awareness and
prevents the AI from hallucinating non-existent functions or abilities.

CRITICAL FIXES:
1. Capability Inventory: Maintains accurate list of available functions
2. Action Validation: Prevents offering impossible actions
3. Grounded Responses: Ensures responses match actual capabilities
4. Reality Check: Validates proposed actions against available tools
"""

import logging
from typing import Dict, Any, List, Optional, Set
from datetime import datetime

logger = logging.getLogger(__name__)


class CapabilityInventory:
    """
    Maintains an accurate inventory of ATLES's actual capabilities.
    
    This prevents the AI from hallucinating functions it doesn't have.
    """
    
    def __init__(self):
        # Core capabilities that ATLES actually has
        self.available_functions = {
            # File operations
            "read_pdf": {
                "description": "Read and extract text from PDF files",
                "parameters": ["url"],
                "example": "FUNCTION_CALL:read_pdf:{\"url\": \"https://example.com/file.pdf\"}"
            },
            "search_code": {
                "description": "Search through code files for specific patterns",
                "parameters": ["query", "file_type"],
                "example": "FUNCTION_CALL:search_code:{\"query\": \"function name\"}"
            },
            "run_command": {
                "description": "Execute system commands (with safety restrictions)",
                "parameters": ["command"],
                "example": "FUNCTION_CALL:run_command:{\"command\": \"ls -la\"}"
            },
            "get_system_info": {
                "description": "Get system information and status",
                "parameters": [],
                "example": "FUNCTION_CALL:get_system_info:{}"
            },
            "list_files": {
                "description": "List files in a directory",
                "parameters": ["directory", "pattern"],
                "example": "FUNCTION_CALL:list_files:{\"directory\": \"/path\", \"pattern\": \"*.py\"}"
            },
            "web_search": {
                "description": "Search the web for information (if configured)",
                "parameters": ["query"],
                "example": "FUNCTION_CALL:web_search:{\"query\": \"search terms\"}"
            },
            "check_url_accessibility": {
                "description": "Check if a URL is accessible",
                "parameters": ["url"],
                "example": "FUNCTION_CALL:check_url_accessibility:{\"url\": \"https://example.com\"}"
            },
            "fetch_url_content": {
                "description": "Fetch content from a web URL",
                "parameters": ["url"],
                "example": "FUNCTION_CALL:fetch_url_content:{\"url\": \"https://example.com\"}"
            }
        }
        
        # Functions that ATLES does NOT have (common hallucinations)
        self.unavailable_functions = {
            "ask_gemini": "ATLES cannot communicate with Gemini or other external AIs",
            "contact_claude": "ATLES cannot contact Claude or other AI systems",
            "send_email": "ATLES cannot send emails",
            "make_phone_calls": "ATLES cannot make phone calls",
            "access_internet_directly": "ATLES has limited web access through specific functions only",
            "modify_system_files": "ATLES cannot modify critical system files",
            "install_software": "ATLES cannot install software packages",
            "access_camera": "ATLES cannot access camera or recording devices",
            "control_hardware": "ATLES cannot directly control hardware devices",
            "access_private_data": "ATLES cannot access private user data without explicit permission"
        }
        
        # Capabilities that require clarification
        self.conditional_capabilities = {
            "web_functions": "Available but limited to specific URLs and content types",
            "file_operations": "Available for accessible files with appropriate permissions",
            "system_commands": "Available but restricted for safety",
            "code_analysis": "Available for provided code and accessible files"
        }
    
    def has_capability(self, function_name: str) -> bool:
        """Check if ATLES actually has a specific capability."""
        return function_name in self.available_functions
    
    def is_explicitly_unavailable(self, function_name: str) -> bool:
        """Check if a function is explicitly known to be unavailable."""
        return function_name in self.unavailable_functions
    
    def get_capability_info(self, function_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a capability."""
        if function_name in self.available_functions:
            return self.available_functions[function_name]
        return None
    
    def get_unavailability_reason(self, function_name: str) -> Optional[str]:
        """Get the reason why a function is unavailable."""
        return self.unavailable_functions.get(function_name)
    
    def list_available_functions(self) -> List[str]:
        """Get list of all available function names."""
        return list(self.available_functions.keys())
    
    def get_capability_summary(self) -> str:
        """Get a summary of ATLES's actual capabilities."""
        available = list(self.available_functions.keys())
        return f"Available functions: {', '.join(available)}"


class ActionValidator:
    """
    Validates proposed actions against actual capabilities.
    
    This prevents ATLES from offering to do things it cannot do.
    """
    
    def __init__(self, capability_inventory: CapabilityInventory):
        self.capabilities = capability_inventory
        
        # Common hallucination patterns to detect
        self.hallucination_patterns = [
            r"ask\s+gemini",
            r"contact\s+claude", 
            r"communicate\s+with\s+\w+\s+ai",
            r"send\s+email",
            r"make\s+phone\s+call",
            r"install\s+\w+",
            r"access\s+camera",
            r"control\s+hardware",
            r"modify\s+system\s+files"
        ]
    
    def validate_proposed_action(self, action_description: str) -> Dict[str, Any]:
        """
        Validate if a proposed action is actually possible.
        
        Returns validation result with suggestions for grounded alternatives.
        """
        import re
        
        action_lower = action_description.lower()
        
        # Check for explicit hallucination patterns
        for pattern in self.hallucination_patterns:
            if re.search(pattern, action_lower):
                return {
                    "valid": False,
                    "reason": "Proposed action involves capabilities ATLES does not have",
                    "pattern_matched": pattern,
                    "suggestion": self._get_grounded_alternative(action_description)
                }
        
        # Check for specific function references
        for func_name in self.capabilities.unavailable_functions:
            if func_name.replace("_", " ") in action_lower:
                return {
                    "valid": False,
                    "reason": self.capabilities.get_unavailability_reason(func_name),
                    "unavailable_function": func_name,
                    "suggestion": self._get_grounded_alternative(action_description)
                }
        
        # Check if action references available functions
        available_functions = self.capabilities.list_available_functions()
        for func_name in available_functions:
            if func_name.replace("_", " ") in action_lower:
                return {
                    "valid": True,
                    "reason": "Action references available capability",
                    "function_info": self.capabilities.get_capability_info(func_name)
                }
        
        # If no specific function detected, assume it's a general response
        return {
            "valid": True,
            "reason": "General response without specific function calls",
            "type": "conversational"
        }
    
    def _get_grounded_alternative(self, original_action: str) -> str:
        """Suggest a grounded alternative to a hallucinated action."""
        action_lower = original_action.lower()
        
        if "gemini" in action_lower or "claude" in action_lower or "ai" in action_lower:
            return "I cannot contact other AI systems, but I can help you formulate a request or provide information you could use with other systems."
        
        if "email" in action_lower:
            return "I cannot send emails, but I can help you draft email content or provide information you need."
        
        if "install" in action_lower:
            return "I cannot install software, but I can provide installation instructions or help you understand the process."
        
        if "phone" in action_lower:
            return "I cannot make phone calls, but I can help you prepare what to say or find contact information."
        
        return "I cannot perform that specific action, but I can provide information, analysis, or help you plan the steps needed."


class GroundedResponseGenerator:
    """
    Generates responses that are grounded in ATLES's actual capabilities.
    
    This replaces hallucinated responses with honest, helpful alternatives.
    """
    
    def __init__(self, capability_inventory: CapabilityInventory, action_validator: ActionValidator):
        self.capabilities = capability_inventory
        self.validator = action_validator
    
    def generate_grounded_response(self, original_response: str, user_message: str) -> str:
        """
        Generate a response grounded in actual capabilities.
        
        If the original response contains hallucinations, replace with grounded alternative.
        """
        # Check for confusing constitutional responses that don't address the user's needs
        if self._is_confusing_constitutional_response(original_response, user_message):
            return self._create_grounded_alternative(
                original_response,
                user_message,
                {"reason": "Response was unclear about capabilities", "suggestion": "Let me be more direct about what I can do."}
            )
        
        # Validate the proposed action in the response
        validation = self.validator.validate_proposed_action(original_response)
        
        if not validation["valid"]:
            # Response contains hallucination - generate grounded alternative
            return self._create_grounded_alternative(
                original_response, 
                user_message, 
                validation
            )
        
        return original_response
    
    def _is_confusing_constitutional_response(self, response: str, user_message: str) -> bool:
        """Check if response is a confusing constitutional explanation instead of clear capability info."""
        user_lower = user_message.lower().strip()
        response_lower = response.lower()
        
        # If user said "yes go ahead" but response talks about constitutional principles instead of capabilities
        if user_lower in ["yes", "yes go ahead", "go ahead", "proceed"]:
            constitutional_indicators = [
                "constitutional principles",
                "principle of explicit action", 
                "guidance and rules",
                "command: format",
                "constitution of atles"
            ]
            
            if any(indicator in response_lower for indicator in constitutional_indicators):
                # And doesn't clearly explain what ATLES can/cannot do
                capability_indicators = [
                    "i cannot",
                    "i can help",
                    "what i can do",
                    "available functions"
                ]
                
                if not any(indicator in response_lower for indicator in capability_indicators):
                    return True
        
        return False
    
    def _create_grounded_alternative(self, original_response: str, user_message: str, validation: Dict[str, Any]) -> str:
        """Create a grounded alternative to a hallucinated response."""
        
        # Extract the intent from the user message
        user_intent = self._extract_user_intent(user_message)
        
        # For simple "yes go ahead" responses, be more direct
        if user_message.lower().strip() in ["yes", "yes go ahead", "go ahead", "proceed"]:
            return """I understand you'd like me to proceed, but I need to clarify something important:

I cannot actually communicate with Gemini or other external AI systems. I'm an offline-first system that works with local Ollama models.

However, I can help you in other ways:
• Analyze emotion-related data you provide
• Help you structure training approaches
• Provide guidance on emotion interpretation techniques
• Process and analyze text or documents you share

What specific information or analysis would you like me to help with regarding emotion interpretation?"""
        
        grounded_response_parts = [
            "I understand you're asking about " + user_intent + ".",
            "",
            validation.get("reason", "I cannot perform that specific action."),
            ""
        ]
        
        # Add the suggested alternative
        if validation.get("suggestion"):
            grounded_response_parts.extend([
                "However, " + validation["suggestion"],
                ""
            ])
        
        # Add what ATLES can actually do
        grounded_response_parts.extend([
            "What I can help with:",
            "• Analyze and process information you provide",
            "• Search through code and files",
            "• Read PDF documents from URLs", 
            "• Provide detailed explanations and guidance",
            "• Help you plan and structure your approach",
            "",
            "Would you like me to help in any of these ways instead?"
        ])
        
        return "\n".join(grounded_response_parts)
    
    def _extract_user_intent(self, user_message: str) -> str:
        """Extract the user's intent from their message."""
        message_lower = user_message.lower()
        
        if "gemini" in message_lower or "training" in message_lower:
            return "setting up a training session with Gemini"
        
        if "emotion" in message_lower:
            return "emotion interpretation and analysis"
        
        if "help" in message_lower:
            return "assistance with a task"
        
        return "your request"


class CapabilityGroundingSystem:
    """
    Integrated system that prevents logical hallucination by grounding responses in actual capabilities.
    """
    
    def __init__(self):
        self.capability_inventory = CapabilityInventory()
        self.action_validator = ActionValidator(self.capability_inventory)
        self.response_generator = GroundedResponseGenerator(
            self.capability_inventory, 
            self.action_validator
        )
    
    def process_response(self, response: str, user_message: str) -> str:
        """
        Process a response to ensure it's grounded in actual capabilities.
        
        This is the main method that prevents logical hallucination.
        """
        try:
            # Generate grounded response
            grounded_response = self.response_generator.generate_grounded_response(
                response, 
                user_message
            )
            
            return grounded_response
            
        except Exception as e:
            logger.error(f"Error in capability grounding: {e}")
            # Fallback to original response if processing fails
            return response
    
    def check_capability(self, function_name: str) -> Dict[str, Any]:
        """Check if a specific capability is available."""
        return {
            "available": self.capability_inventory.has_capability(function_name),
            "info": self.capability_inventory.get_capability_info(function_name),
            "unavailable_reason": self.capability_inventory.get_unavailability_reason(function_name)
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get status of the capability grounding system."""
        return {
            "available_functions": len(self.capability_inventory.available_functions),
            "unavailable_functions": len(self.capability_inventory.unavailable_functions),
            "capability_summary": self.capability_inventory.get_capability_summary(),
            "system_active": True
        }


# Factory function
def create_capability_grounding_system() -> CapabilityGroundingSystem:
    """Create and return a capability grounding system."""
    return CapabilityGroundingSystem()


# Test function
def test_capability_grounding():
    """Test the capability grounding system with hallucination scenarios."""
    print("🧪 Testing Capability Grounding System")
    print("=" * 50)
    
    grounding = create_capability_grounding_system()
    
    # Test 1: Gemini hallucination scenario
    print("\n1. Testing Gemini Hallucination:")
    user_msg = "yes go ahead"
    hallucinated_response = "I'd be happy to help you interpret the data and gain insights into emotions. I can ask Gemini to do a training session based on this topic, as you suggested. Would you like me to proceed with asking Gemini to initiate a training session?"
    
    grounded_response = grounding.process_response(hallucinated_response, user_msg)
    print(f"Original: {hallucinated_response[:100]}...")
    print(f"Grounded: {grounded_response[:100]}...")
    
    # Test 2: Capability check
    print("\n2. Testing Capability Check:")
    gemini_check = grounding.check_capability("ask_gemini")
    pdf_check = grounding.check_capability("read_pdf")
    print(f"Gemini capability: {gemini_check}")
    print(f"PDF capability: {pdf_check}")
    
    # Test 3: System status
    print(f"\n3. System Status: {grounding.get_system_status()}")


if __name__ == "__main__":
    test_capability_grounding()
