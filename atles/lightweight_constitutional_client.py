#!/usr/bin/env python3
"""
Lightweight Constitutional Client for ATLES

This is a streamlined version of the constitutional client that:
1. Uses the architectural layer manager for granular control
2. Focuses on core safety without over-processing
3. Allows simple requests to flow through naturally
4. Maintains essential functionality while reducing interference

Design Philosophy:
- Simple requests should get simple responses
- Complex processing only when actually needed
- Safety without bureaucracy
- Performance over perfection
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

from .architectural_layer_manager import get_layer_manager, should_process_layer, is_simple_request

logger = logging.getLogger(__name__)


class LightweightConstitutionalClient:
    """
    A streamlined constitutional client that respects the layer manager.
    
    This replaces the heavy 1100+ line constitutional client with
    a focused, efficient approach.
    """
    
    def __init__(self, base_client):
        self.base_client = base_client
        self.layer_manager = get_layer_manager()
        self.last_prompt = ""
        
        # Initialize only essential systems
        self._initialize_essential_systems()
    
    def _initialize_essential_systems(self):
        """Initialize only the essential systems based on layer configuration."""
        
        # Memory system (if enabled)
        if should_process_layer("memory_integration", ""):
            try:
                from .unified_memory_manager import get_unified_memory
                self.unified_memory = get_unified_memory()
                logger.info("✅ Memory system initialized")
            except ImportError as e:
                logger.warning(f"⚠️ Memory system not available: {e}")
                self.unified_memory = None
        else:
            self.unified_memory = None
        
        # Bootstrap system (if enabled)
        if should_process_layer("bootstrap", ""):
            try:
                from .bootstrap_system import get_bootstrap_system
                self.bootstrap_system = get_bootstrap_system()
                logger.info("✅ Bootstrap system initialized")
            except ImportError as e:
                logger.warning(f"⚠️ Bootstrap system not available: {e}")
                self.bootstrap_system = None
        else:
            self.bootstrap_system = None
        
        # Capability grounding (if enabled)
        if should_process_layer("capability_grounding", ""):
            try:
                from .capability_grounding_system import create_capability_grounding_system
                self.capability_grounding = create_capability_grounding_system()
                logger.info("✅ Capability grounding initialized")
            except ImportError as e:
                logger.warning(f"⚠️ Capability grounding not available: {e}")
                self.capability_grounding = None
        else:
            self.capability_grounding = None
        
        # Capability self-check (always enabled for safety)
        try:
            from .capability_self_check import create_capability_self_check
            self.capability_check = create_capability_self_check()
            logger.info("✅ Capability self-check initialized")
        except ImportError as e:
            logger.warning(f"⚠️ Capability self-check not available: {e}")
            self.capability_check = None
        
        # Logical reasoning validator (always enabled for consistency)
        try:
            from .logical_reasoning_validator import create_logical_reasoning_validator
            self.logic_validator = create_logical_reasoning_validator()
            logger.info("✅ Logical reasoning validator initialized")
        except ImportError as e:
            logger.warning(f"⚠️ Logical reasoning validator not available: {e}")
            self.logic_validator = None
        
        # Constitutional validator (for AI identity checks)
        try:
            from .constitutional_client import ConstitutionalValidator
            self.constitutional_validator = ConstitutionalValidator()
            logger.info("✅ Constitutional validator initialized")
        except ImportError as e:
            logger.warning(f"⚠️ Constitutional validator not available: {e}")
            self.constitutional_validator = None
    
    def chat(self, message: str, **kwargs) -> str:
        """Chat interface - delegates to generate with a default model."""
        return self.generate(model="llama3.2", prompt=message, **kwargs)
    
    def generate(self, model: str, prompt: str, **kwargs) -> str:
        """
        Lightweight generate that processes only necessary layers.
        
        Flow:
        1. Check AI identity violations (CRITICAL SAFETY)
        2. Check capability requirements
        3. Check if simple request -> fast path
        4. Process enabled layers in priority order
        5. Generate response with minimal interference
        """
        self.last_prompt = prompt
        start_time = datetime.now()
        
        # CRITICAL SAFETY CHECK 1: AI Identity Integrity
        if self.constitutional_validator:
            is_violation, refusal_message = self.constitutional_validator.detect_ai_identity_violation(prompt)
            if is_violation:
                logger.warning(f"AI identity violation blocked: {prompt[:50]}...")
                return refusal_message
        
        # CRITICAL SAFETY CHECK 2: Capability Requirements
        if self.capability_check:
            can_respond, blocked_capability, suggested_response = self.capability_check.check_prompt(prompt)
            if not can_respond:
                logger.info(f"Capability limitation detected ({blocked_capability}): {prompt[:50]}...")
                return suggested_response
        
        # FAST PATH: Simple requests bypass complex processing
        if is_simple_request(prompt):
            logger.debug(f"Simple request detected: {prompt[:50]}...")
            response = self.base_client.generate(model, prompt, **kwargs)
            
            # Apply only essential post-processing
            if self.capability_grounding and should_process_layer("capability_grounding", prompt):
                response = self.capability_grounding.process_response(response, prompt)
            
            self._log_performance("simple_path", start_time)
            return response or "I'm here to help! What would you like to know?"
        
        # COMPLEX PATH: Process through enabled layers
        processed_prompt = prompt
        
        # 1. Bootstrap processing (highest priority)
        if self.bootstrap_system and should_process_layer("bootstrap", prompt):
            try:
                bootstrap_result = self.bootstrap_system.process_user_input(prompt)
                
                # Handle immediate responses (identity, hypothetical engagement)
                if bootstrap_result and isinstance(bootstrap_result, dict):
                    # Identity recognition
                    user_recognition = bootstrap_result.get("user_recognition")
                    if (user_recognition and user_recognition.get("user_identified") and
                        user_recognition.get("is_identity_statement", False)):
                        response = user_recognition["appropriate_response"]
                        final_response = self.bootstrap_system.process_ai_response(prompt, response)
                        self._log_performance("bootstrap_identity", start_time)
                        return final_response
                    
                    # Hypothetical engagement
                    hypothetical_response = bootstrap_result.get("hypothetical_response")
                    if hypothetical_response:
                        final_response = self.bootstrap_system.process_ai_response(prompt, hypothetical_response)
                        self._log_performance("bootstrap_hypothetical", start_time)
                        return final_response
                    
                    # Use bootstrap prompt if session start
                    if (bootstrap_result.get("bootstrap_prompt") and 
                        bootstrap_result.get("session_state", {}).get("is_session_start", False)):
                        processed_prompt = bootstrap_result["bootstrap_prompt"]
                        logger.debug("Using bootstrap prompt for session start")
                
            except Exception as e:
                logger.error(f"Bootstrap processing error: {e}")
        
        # 2. Memory integration
        if self.unified_memory and should_process_layer("memory_integration", prompt):
            try:
                # Check for user identity handling
                identity_response = self.unified_memory.process_user_message(prompt)
                if identity_response:
                    if self.bootstrap_system:
                        final_response = self.bootstrap_system.process_ai_response(prompt, identity_response)
                    else:
                        final_response = identity_response
                    self._log_performance("memory_identity", start_time)
                    return final_response
                
                # Check for name questions
                name_response = self.unified_memory.handle_name_question(prompt)
                if name_response:
                    if self.bootstrap_system:
                        final_response = self.bootstrap_system.process_ai_response(prompt, name_response)
                    else:
                        final_response = name_response
                    self._log_performance("memory_name", start_time)
                    return final_response
                
                # Enhance prompt with memory context
                memory_context = self.unified_memory.process_user_prompt_with_memory(prompt)
                if memory_context and memory_context.get("memory_enhanced"):
                    # Use memory-enhanced context but don't force specific responses
                    logger.debug("Memory context available for response generation")
                
            except Exception as e:
                logger.error(f"Memory integration error: {e}")
        
        # 3. Generate core response
        response = self.base_client.generate(model, processed_prompt, **kwargs)
        
        if not response:
            response = "I'm here to help! Could you please rephrase your question?"
        
        # 4. Post-processing layers (in reverse priority order)
        
        # Capability grounding (prevent hallucinations)
        if self.capability_grounding and should_process_layer("capability_grounding", prompt):
            try:
                grounded_response = self.capability_grounding.process_response(response, prompt)
                if grounded_response:
                    response = grounded_response
            except Exception as e:
                logger.error(f"Capability grounding error: {e}")
        
        # Bootstrap post-processing
        if self.bootstrap_system and should_process_layer("bootstrap", prompt):
            try:
                response = self.bootstrap_system.process_ai_response(prompt, response)
            except Exception as e:
                logger.error(f"Bootstrap post-processing error: {e}")
        
        # Constitutional validation (only for function calls and safety)
        if should_process_layer("constitutional", prompt):
            response = self._apply_lightweight_constitutional_check(response, prompt)
        
        self._log_performance("complex_path", start_time)
        return response
    
    def _apply_lightweight_constitutional_check(self, response: str, prompt: str) -> str:
        """
        Apply lightweight constitutional checks focused on safety, not bureaucracy.
        
        Only blocks truly dangerous actions, not information requests.
        """
        # Check for actual function calls that might be dangerous
        if "FUNCTION_CALL:" in response:
            # Extract function call
            lines = response.split('\n')
            for line in lines:
                if line.strip().startswith("FUNCTION_CALL:"):
                    # Check if it's a dangerous function call
                    if self._is_dangerous_function_call(line, prompt):
                        return self._get_safe_alternative(line, prompt)
        
        # Check for obviously harmful content (very basic safety)
        harmful_patterns = [
            "delete all files", "format hard drive", "rm -rf /",
            "shutdown system", "hack into", "break security"
        ]
        
        response_lower = response.lower()
        for pattern in harmful_patterns:
            if pattern in response_lower and pattern in prompt.lower():
                return f"I can't help with that request as it could be harmful. Is there something else I can assist you with?"
        
        return response
    
    def _is_dangerous_function_call(self, function_call: str, prompt: str) -> bool:
        """Check if a function call is actually dangerous."""
        # Only block truly dangerous operations
        dangerous_patterns = [
            "delete.*all", "format.*drive", "shutdown", "rm.*-rf",
            "hack", "break.*security", "destroy.*data"
        ]
        
        import re
        call_lower = function_call.lower()
        for pattern in dangerous_patterns:
            if re.search(pattern, call_lower):
                return True
        
        return False
    
    def _get_safe_alternative(self, blocked_call: str, prompt: str) -> str:
        """Provide a safe alternative when blocking a dangerous function call."""
        return f"I understand you're asking about a system operation, but I can't execute potentially harmful commands. If you need help with system administration, I'd be happy to explain the concepts or suggest safer alternatives."
    
    def _log_performance(self, path_type: str, start_time: datetime):
        """Log performance metrics for optimization."""
        duration = (datetime.now() - start_time).total_seconds()
        logger.debug(f"Response path '{path_type}' took {duration:.3f}s")
        
        # Update layer manager performance stats
        self.layer_manager.performance_stats["total_requests"] += 1
        if path_type == "simple_path":
            self.layer_manager.performance_stats["bypassed_requests"] += 1
        else:
            self.layer_manager.performance_stats["processed_requests"] += 1
    
    def get_status(self) -> Dict[str, Any]:
        """Get current client status."""
        return {
            "client_type": "lightweight_constitutional",
            "layer_manager_status": self.layer_manager.get_status(),
            "systems_initialized": {
                "memory": self.unified_memory is not None,
                "bootstrap": self.bootstrap_system is not None,
                "capability_grounding": self.capability_grounding is not None
            },
            "last_prompt_length": len(self.last_prompt) if self.last_prompt else 0
        }
    
    # Delegate all other methods to base client
    def __getattr__(self, name):
        return getattr(self.base_client, name)


def create_lightweight_constitutional_client(user_id: str = "lightweight_user"):
    """
    Factory function to create a lightweight constitutional client.
    
    This replaces the heavy constitutional client with a streamlined version
    that uses the architectural layer manager.
    """
    try:
        # Import and create base client
        from .ollama_client_enhanced import OllamaFunctionCaller
        base_client = OllamaFunctionCaller()
        
        # Wrap with lightweight constitutional enforcement
        lightweight_client = LightweightConstitutionalClient(base_client)
        
        logger.info("Lightweight constitutional client created successfully")
        return lightweight_client
        
    except Exception as e:
        logger.error(f"Failed to create lightweight constitutional client: {e}")
        raise


# Migration helper
def migrate_from_heavy_constitutional_client():
    """
    Helper function to migrate from the heavy constitutional client.
    
    This updates the unified constitutional client to use the lightweight version.
    """
    try:
        # Update the unified constitutional client file
        unified_client_code = '''#!/usr/bin/env python3
"""
Unified Constitutional Client - Lightweight Version

This file now uses the lightweight constitutional client with
architectural layer management for better performance and control.
"""

from .lightweight_constitutional_client import create_lightweight_constitutional_client

# For backward compatibility
def create_constitutional_client(user_id: str = "constitutional_user"):
    """Create a constitutional client (now lightweight version)."""
    return create_lightweight_constitutional_client(user_id)

# Export the main factory function
__all__ = ["create_constitutional_client", "create_lightweight_constitutional_client"]
'''
        
        with open("atles/unified_constitutional_client.py", 'w') as f:
            f.write(unified_client_code)
        
        logger.info("✅ Migration to lightweight constitutional client complete")
        return True
        
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        return False


if __name__ == "__main__":
    # Test the lightweight client
    print("🧪 Testing Lightweight Constitutional Client")
    print("=" * 50)
    
    try:
        client = create_lightweight_constitutional_client()
        
        # Test simple requests (should be fast)
        simple_tests = ["Hi", "What is 2 + 2?", "Hello"]
        
        print("\n⚡ Testing Simple Requests (Fast Path):")
        for test in simple_tests:
            print(f"  Input: '{test}'")
            response = client.chat(test)
            print(f"  Output: {response[:100]}...")
        
        # Test complex requests
        complex_tests = [
            "What do you want to do today?",
            "Consider the Ship of Theseus paradox"
        ]
        
        print("\n🧠 Testing Complex Requests:")
        for test in complex_tests:
            print(f"  Input: '{test}'")
            response = client.chat(test)
            print(f"  Output: {response[:100]}...")
        
        # Show status
        status = client.get_status()
        print(f"\n📊 Client Status: {status}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
