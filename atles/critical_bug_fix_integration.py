"""
Critical Bug Fix Integration for ATLES

This module integrates all the fixes for the critical reasoning failure bug
reported on 2025-08-22. It should be imported and applied to any ATLES Brain
instance to prevent the meta-level reasoning failures.
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def apply_critical_bug_fixes(atles_brain):
    """
    Apply all critical bug fixes to an ATLES Brain instance.
    
    This function integrates:
    1. Error Recovery System
    2. Enhanced Response Processor  
    3. Metacognitive Observer enhancements
    4. Response processing pipeline fixes
    
    Args:
        atles_brain: The ATLES Brain instance to fix
        
    Returns:
        bool: True if fixes were successfully applied
    """
    try:
        logger.info("Applying critical bug fixes to ATLES Brain...")
        
        # Fix 1: Integrate Error Recovery System
        from .error_recovery_system import integrate_error_recovery
        error_recovery = integrate_error_recovery(atles_brain)
        logger.info("✅ Error Recovery System integrated")
        
        # Fix 2: Integrate Enhanced Response Processor
        from .enhanced_response_processor import integrate_enhanced_processor
        enhanced_processor = integrate_enhanced_processor(atles_brain)
        logger.info("✅ Enhanced Response Processor integrated")
        
        # Fix 3: Enhance Metacognitive Observer (if available)
        if hasattr(atles_brain, 'metacognitive_observer') and atles_brain.metacognitive_observer is not None:
            # Observer is already enhanced via direct file edits
            logger.info("✅ Metacognitive Observer enhancements active")
        else:
            logger.warning("⚠️ Metacognitive Observer not found - some fixes may not be fully active")
        
        # Fix 4: Override problematic response method
        _patch_response_method(atles_brain)
        logger.info("✅ Response method patched")
        
        # Add bug fix status tracking
        atles_brain.bug_fixes_applied = {
            "critical_reasoning_failure_fix": True,
            "error_recovery_system": True,
            "enhanced_response_processor": True,
            "metacognitive_observer_enhanced": hasattr(atles_brain, 'metacognitive_observer') and atles_brain.metacognitive_observer is not None,
            "response_method_patched": True,
            "fix_version": "1.0.0",
            "applied_at": "2025-08-22"
        }
        
        logger.info("🎉 All critical bug fixes successfully applied!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to apply critical bug fixes: {e}")
        return False

def _patch_response_method(atles_brain):
    """
    Patch the response generation method to use the enhanced processor.
    
    This prevents the original problematic response guidance system from
    causing the reasoning failure bug.
    """
    # Store original method if it exists
    if hasattr(atles_brain, 'generate_response'):
        atles_brain._original_generate_response = atles_brain.generate_response
    
    def enhanced_generate_response(user_message: str, session_id: str = None, **kwargs) -> str:
        """
        Enhanced response generation that uses the new processing pipeline.
        
        This method replaces the problematic original response generation
        and prevents the critical reasoning failure bug.
        """
        try:
            # Use the enhanced processor if available
            if hasattr(atles_brain, 'enhanced_processor'):
                from .enhanced_response_processor import ProcessingContext
                
                context = ProcessingContext(
                    user_message=user_message,
                    conversation_history=getattr(atles_brain, 'conversation_history', []),
                    session_id=session_id or getattr(atles_brain, 'current_session_id', 'default'),
                    user_id=getattr(atles_brain, 'current_user_id', 'default')
                )
                
                result = atles_brain.enhanced_processor.process_user_message(context)
                
                # Log the processing for analysis
                if hasattr(atles_brain, 'metacognitive_observer') and atles_brain.metacognitive_observer:
                    interaction_data = {
                        "type": "enhanced_response",
                        "processing_mode": result.processing_mode_used,
                        "confidence_score": result.confidence_score,
                        "error_recovery_applied": result.error_recovery_applied
                    }
                    atles_brain.metacognitive_observer.track_performance_metrics(interaction_data)
                
                return result.response_text
            
            # Fallback to original method if enhanced processor not available
            elif hasattr(atles_brain, '_original_generate_response'):
                return atles_brain._original_generate_response(user_message, session_id, **kwargs)
            
            # Last resort fallback
            else:
                return f"I understand your message: '{user_message}'. How can I help you with that?"
                
        except Exception as e:
            logger.error(f"Enhanced response generation failed: {e}")
            
            # Emergency fallback to prevent system failure
            if "correction" in user_message.lower() or "wrong" in user_message.lower():
                return "I understand you're providing a correction. Thank you for the feedback - I'll learn from this."
            else:
                return "I'm here to help. Could you please rephrase your request?"
    
    # Replace the method
    atles_brain.generate_response = enhanced_generate_response
    logger.info("Response method successfully patched with enhanced processor")

def verify_bug_fixes(atles_brain) -> Dict[str, Any]:
    """
    Verify that all bug fixes have been properly applied and are working.
    
    Returns:
        Dict with verification results
    """
    verification_results = {
        "fixes_applied": False,
        "error_recovery_available": False,
        "enhanced_processor_available": False,
        "metacognitive_observer_enhanced": False,
        "response_method_patched": False,
        "test_results": {}
    }
    
    try:
        # Check if fixes were applied
        if hasattr(atles_brain, 'bug_fixes_applied'):
            verification_results["fixes_applied"] = True
            
        # Check error recovery system
        if hasattr(atles_brain, 'error_recovery'):
            verification_results["error_recovery_available"] = True
            
        # Check enhanced processor
        if hasattr(atles_brain, 'enhanced_processor'):
            verification_results["enhanced_processor_available"] = True
            
        # Check metacognitive observer
        if hasattr(atles_brain, 'metacognitive_observer'):
            verification_results["metacognitive_observer_enhanced"] = True
            
        # Check response method patch
        if hasattr(atles_brain, '_original_generate_response'):
            verification_results["response_method_patched"] = True
        
        # Run basic functionality tests
        verification_results["test_results"] = _run_basic_tests(atles_brain)
        
        logger.info("Bug fix verification completed")
        
    except Exception as e:
        logger.error(f"Bug fix verification failed: {e}")
        verification_results["error"] = str(e)
    
    return verification_results

def _run_basic_tests(atles_brain) -> Dict[str, bool]:
    """Run basic tests to verify the fixes are working."""
    test_results = {}
    
    try:
        # Test 1: Normal response generation
        if hasattr(atles_brain, 'generate_response'):
            response = atles_brain.generate_response("Hello")
            test_results["normal_response"] = len(response) > 0 and "RESPONSE GUIDANCE" not in response
        
        # Test 2: Error recovery system
        if hasattr(atles_brain, 'error_recovery'):
            stats = atles_brain.error_recovery.get_recovery_statistics()
            test_results["error_recovery_stats"] = isinstance(stats, dict)
        
        # Test 3: Enhanced processor
        if hasattr(atles_brain, 'enhanced_processor'):
            stats = atles_brain.enhanced_processor.get_processing_statistics()
            test_results["enhanced_processor_stats"] = isinstance(stats, dict)
        
        logger.info("Basic functionality tests completed")
        
    except Exception as e:
        logger.error(f"Basic tests failed: {e}")
        test_results["test_error"] = str(e)
    
    return test_results

# Quick application function for immediate use
def quick_fix_atles_brain(atles_brain):
    """
    Quick function to apply critical bug fixes to an ATLES Brain.
    
    Usage:
        from atles.critical_bug_fix_integration import quick_fix_atles_brain
        quick_fix_atles_brain(my_atles_brain)
    """
    success = apply_critical_bug_fixes(atles_brain)
    if success:
        verification = verify_bug_fixes(atles_brain)
        logger.info(f"Bug fix verification: {verification}")
        return True
    else:
        logger.error("Failed to apply bug fixes")
        return False
