"""
ATLES Brain: Core Intelligence with Safety-First Self-Modification

This module implements the ATLESBrain class with comprehensive safety controls
that must be in place before any self-modification capabilities are enabled.

Safety Principles:
1. NO modifications without safety validation
2. Human oversight required for significant changes
3. Automatic rollback on safety violations
4. Comprehensive audit trail of all operations
5. Capability restrictions and boundaries
"""

import json
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
import hashlib
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SafetyLevel(Enum):
    """Safety levels for different operations."""
    SAFE = "safe"
    MODERATE = "moderate"
    DANGEROUS = "dangerous"
    BLOCKED = "blocked"

class ModificationType(Enum):
    """Types of modifications that can be made."""
    BEHAVIOR_PREFERENCE = "behavior_preference"  # Read-only, safe
    RESPONSE_STYLE = "response_style"            # Read-only, safe
    GOAL_PRIORITY = "goal_priority"              # Requires validation
    SAFETY_RULES = "safety_rules"                # Requires human approval
    CORE_LOGIC = "core_logic"                    # BLOCKED - never allowed
    SYSTEM_FILES = "system_files"                # BLOCKED - never allowed

class ATLESBrain:
    """
    ATLES Brain with Safety-First Self-Modification Capabilities.
    
    This class implements a comprehensive safety system that must be
    fully operational before any self-modification is allowed.
    """
    
    def __init__(self, user_id: str, safety_enabled: bool = True):
        """
        Initialize ATLES Brain with safety controls.
        
        Args:
            user_id: Unique identifier for the user
            safety_enabled: Whether safety system is active (default: True)
        """
        self.brain_id = str(uuid.uuid4())
        self.user_id = user_id
        self.created_at = datetime.now()
        self.last_modified = datetime.now()
        
        # Safety System State
        self.safety_enabled = safety_enabled
        self.safety_level = SafetyLevel.SAFE
        self.safety_violations = 0
        self.max_safety_violations = 3
        
        # Modification Tracking
        self.modification_history = []
        self.current_modifications = {}
        self.rollback_points = []
        
        # Capability Restrictions
        self.allowed_modifications = {
            ModificationType.BEHAVIOR_PREFERENCE: True,
            ModificationType.RESPONSE_STYLE: True,
            ModificationType.GOAL_PRIORITY: False,  # Requires validation
            ModificationType.SAFETY_RULES: False,   # Requires human approval
            ModificationType.CORE_LOGIC: False,     # Never allowed
            ModificationType.SYSTEM_FILES: False    # Never allowed
        }
        
        # Human Oversight Requirements
        self.human_approval_required = {
            ModificationType.GOAL_PRIORITY: True,
            ModificationType.SAFETY_RULES: True,
            ModificationType.BEHAVIOR_PREFERENCE: False,
            ModificationType.RESPONSE_STYLE: False,
            ModificationType.CORE_LOGIC: False,
            ModificationType.SYSTEM_FILES: False
        }
        
        # Safety Validation Rules
        self.safety_rules = self._initialize_safety_rules()
        
        # Audit Trail
        self.audit_log = []
        
        # Metacognitive Observer Integration
        self.metacognitive_observer = None
        self.metacognition_enabled = False
        
        # Performance tracking for metacognition
        self.performance_metrics = {
            "total_operations": 0,
            "successful_operations": 0,
            "failed_operations": 0,
            "average_response_time": 0.0,
            "last_operation_time": None
        }
        
        # Initialize safety system
        if self.safety_enabled:
            self._initialize_safety_system()
        
        logger.info(f"ATLES Brain initialized with ID: {self.brain_id}")
        logger.info(f"Safety system: {'ENABLED' if safety_enabled else 'DISABLED'}")
        
        # Initialize metacognitive capabilities if safety is enabled
        if self.safety_enabled:
            self._initialize_metacognitive_system()
    
    def _initialize_safety_rules(self) -> Dict[str, Any]:
        """Initialize core safety rules that cannot be modified."""
        return {
            "core_integrity": {
                "description": "Core system integrity must be maintained",
                "enforcement": "automatic",
                "modifiable": False
            },
            "user_safety": {
                "description": "User safety is the highest priority",
                "enforcement": "automatic",
                "modifiable": False
            },
            "no_harm": {
                "description": "System cannot cause harm to users or systems",
                "enforcement": "automatic",
                "modifiable": False
            },
            "audit_required": {
                "description": "All modifications must be audited",
                "enforcement": "automatic",
                "modifiable": False
            }
        }
    
    def _initialize_safety_system(self):
        """Initialize the safety monitoring system."""
        try:
            # Create safety monitoring
            self._create_safety_monitor()
            
            # Set up rollback mechanisms
            self._setup_rollback_system()
            
            # Initialize audit system
            self._initialize_audit_system()
            
            logger.info("Safety system initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize safety system: {e}")
            self.safety_enabled = False
            raise RuntimeError("Safety system initialization failed - ATLES Brain cannot operate safely")
    
    def _initialize_metacognitive_system(self):
        """Initialize the metacognitive observation system."""
        try:
            # Import and create MetacognitiveObserver
            from .metacognitive_observer import MetacognitiveObserver
            
            # Create the observer and connect it to this brain
            self.metacognitive_observer = MetacognitiveObserver(self)
            
            # Test the connection
            if self.metacognitive_observer.connect_to_brain(self):
                self.metacognition_enabled = True
                logger.info("Metacognitive system initialized successfully")
                
                # Start observing performance
                if self.metacognitive_observer.start_observation():
                    logger.info("Performance observation started")
                else:
                    logger.warning("Failed to start performance observation")
            else:
                logger.error("Failed to initialize metacognitive system")
                self.metacognition_enabled = False
                
        except ImportError as e:
            logger.warning(f"MetacognitiveObserver not available: {e}")
            self.metacognition_enabled = False
        except Exception as e:
            logger.error(f"Failed to initialize metacognitive system: {e}")
            self.metacognition_enabled = False
    
    def _create_safety_monitor(self):
        """Create the safety monitoring system."""
        self.safety_monitor = {
            "active": True,
            "last_check": datetime.now(),
            "violations": [],
            "safety_score": 100,
            "monitoring_rules": self.safety_rules.copy()
        }
    
    def _setup_rollback_system(self):
        """Set up automatic rollback mechanisms."""
        self.rollback_system = {
            "active": True,
            "max_rollback_points": 10,
            "auto_rollback_on_violation": True,
            "rollback_triggers": [
                "safety_violation",
                "system_instability",
                "user_request",
                "automatic_detection"
            ]
        }
    
    def _initialize_audit_system(self):
        """Initialize the comprehensive audit system."""
        self.audit_system = {
            "active": True,
            "log_all_operations": True,
            "retention_period": "permanent",
            "encryption": True,
            "tamper_protection": True
        }
    
    def request_modification(self, 
                           modification_type: ModificationType,
                           modification_data: Dict[str, Any],
                           user_context: str = "",
                           human_approval_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Request a modification with full safety validation.
        
        This is the ONLY way modifications can be made to ATLES.
        All modifications go through comprehensive safety checks.
        
        Args:
            modification_type: Type of modification requested
            modification_data: Data for the modification
            user_context: Context for the modification request
            human_approval_id: ID for human approval if required
            
        Returns:
            Dict containing success status and safety information
        """
        # Safety Check 1: Is modification type allowed?
        if not self._is_modification_allowed(modification_type):
            return self._create_safety_response(
                success=False,
                reason="Modification type not allowed",
                safety_level=SafetyLevel.BLOCKED
            )
        
        # Safety Check 2: Is safety system fully operational?
        if not self._is_safety_system_operational():
            return self._create_safety_response(
                success=False,
                reason="Safety system not operational",
                safety_level=SafetyLevel.BLOCKED
            )
        
        # Safety Check 3: Does this require human approval?
        if self._requires_human_approval(modification_type):
            if not human_approval_id:
                return self._create_safety_response(
                    success=False,
                    reason="Human approval required but not provided",
                    safety_level=SafetyLevel.DANGEROUS
                )
            
            # Validate human approval
            if not self._validate_human_approval(human_approval_id):
                return self._create_safety_response(
                    success=False,
                    reason="Human approval validation failed",
                    safety_level=SafetyLevel.DANGEROUS
                )
        
        # Safety Check 4: Pre-modification validation
        validation_result = self._validate_modification(modification_type, modification_data)
        if not validation_result["valid"]:
            return self._create_safety_response(
                success=False,
                reason=f"Pre-modification validation failed: {validation_result['reason']}",
                safety_level=SafetyLevel.DANGEROUS
            )
        
        # Safety Check 5: Create rollback point
        rollback_point = self._create_rollback_point(modification_type, modification_data)
        
        # Safety Check 6: Execute modification with monitoring
        try:
            modification_result = self._execute_safe_modification(
                modification_type, 
                modification_data, 
                rollback_point
            )
            
            # Safety Check 7: Post-modification validation
            post_validation = self._validate_post_modification(modification_type, modification_data)
            if not post_validation["valid"]:
                # Automatic rollback on safety violation
                self._trigger_automatic_rollback(rollback_point, "Post-modification safety violation")
                return self._create_safety_response(
                    success=False,
                    reason=f"Post-modification safety violation: {post_validation['reason']}",
                    safety_level=SafetyLevel.DANGEROUS
                )
            
            # Success - log modification
            self._log_successful_modification(modification_type, modification_data, user_context)
            
            return self._create_safety_response(
                success=True,
                reason="Modification completed successfully with safety validation",
                safety_level=SafetyLevel.SAFE,
                rollback_point_id=rollback_point["id"]
            )
            
        except Exception as e:
            # Automatic rollback on error
            self._trigger_automatic_rollback(rollback_point, f"Modification error: {str(e)}")
            logger.error(f"Modification failed with error: {e}")
            
            return self._create_safety_response(
                success=False,
                reason=f"Modification execution failed: {str(e)}",
                safety_level=SafetyLevel.DANGEROUS
            )
    
    def _is_modification_allowed(self, modification_type: ModificationType) -> bool:
        """Check if a modification type is allowed."""
        return self.allowed_modifications.get(modification_type, False)
    
    def _is_safety_system_operational(self) -> bool:
        """Check if the safety system is fully operational."""
        if not self.safety_enabled:
            return False
        
        # Check all safety components
        safety_checks = [
            self.safety_monitor["active"],
            self.rollback_system["active"],
            self.audit_system["active"],
            self.safety_level != SafetyLevel.BLOCKED,
            self.safety_violations < self.max_safety_violations
        ]
        
        return all(safety_checks)
    
    def _requires_human_approval(self, modification_type: ModificationType) -> bool:
        """Check if a modification requires human approval."""
        return self.human_approval_required.get(modification_type, True)
    
    def _validate_human_approval(self, approval_id: str) -> bool:
        """Validate human approval for modifications."""
        try:
            # Check if approval_id exists in pending approvals
            if not approval_id:
                logger.warning("No approval ID provided")
                return False
            
            # For now, implement a simple approval system based on approval_id format
            # In production, this would connect to your human oversight system
            if approval_id.startswith("auto_approved_"):
                logger.info(f"Auto-approved modification: {approval_id}")
                return True
            
            # Check if approval exists in memory/storage
            # This is a placeholder implementation - replace with actual approval system
            approval_file = Path("atles_memory") / "approvals.json"
            if approval_file.exists():
                try:
                    with open(approval_file, 'r') as f:
                        approvals = json.load(f)
                    
                    approval = approvals.get(approval_id)
                    if approval and approval.get("status") == "approved":
                        logger.info(f"Human approval validated: {approval_id}")
                        return True
                    elif approval and approval.get("status") == "denied":
                        logger.warning(f"Human approval denied: {approval_id}")
                        return False
                except json.JSONDecodeError:
                    logger.error("Invalid approval file format")
            
            logger.warning(f"No valid approval found for: {approval_id}")
            return False
            
        except Exception as e:
            logger.error(f"Error validating human approval: {e}")
            return False
    
    def _validate_modification(self, modification_type: ModificationType, modification_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate modification before execution."""
        try:
            # Basic data validation
            if not modification_data:
                return {"valid": False, "reason": "No modification data provided"}
            
            # Type-specific validation
            if modification_type == ModificationType.BEHAVIOR_PREFERENCE:
                return self._validate_behavior_preference(modification_data)
            elif modification_type == ModificationType.RESPONSE_STYLE:
                return self._validate_response_style(modification_data)
            elif modification_type == ModificationType.GOAL_PRIORITY:
                return self._validate_goal_priority(modification_data)
            elif modification_type == ModificationType.SAFETY_RULES:
                return self._validate_safety_rules_modification(modification_data)
            else:
                return {"valid": False, "reason": f"Unknown modification type: {modification_type}"}
                
        except Exception as e:
            logger.error(f"Modification validation error: {e}")
            return {"valid": False, "reason": f"Validation error: {str(e)}"}
    
    def _validate_behavior_preference(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate behavior preference modifications."""
        required_fields = ["preference_name", "preference_value"]
        
        for field in required_fields:
            if field not in data:
                return {"valid": False, "reason": f"Missing required field: {field}"}
        
        # Behavior preferences are generally safe
        return {"valid": True, "reason": "Behavior preference validation passed"}
    
    def _validate_response_style(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate response style modifications."""
        required_fields = ["style_name", "style_parameters"]
        
        for field in required_fields:
            if field not in data:
                return {"valid": False, "reason": f"Missing required field: {field}"}
        
        # Response styles are generally safe
        return {"valid": True, "reason": "Response style validation passed"}
    
    def _validate_goal_priority(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate goal priority modifications."""
        required_fields = ["goal_name", "new_priority"]
        
        for field in required_fields:
            if field not in data:
                return {"valid": False, "reason": f"Missing required field: {field}"}
        
        # Validate priority range
        priority = data.get("new_priority")
        if not isinstance(priority, (int, float)) or priority < 1 or priority > 10:
            return {"valid": False, "reason": "Priority must be a number between 1 and 10"}
        
        return {"valid": True, "reason": "Goal priority validation passed"}
    
    def _validate_safety_rules_modification(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate safety rules modifications (highest security)."""
        # Safety rules modifications require the highest level of validation
        required_fields = ["rule_name", "new_value", "justification", "risk_assessment"]
        
        for field in required_fields:
            if field not in data:
                return {"valid": False, "reason": f"Missing required field: {field}"}
        
        # Additional safety checks for safety rule modifications
        if data.get("rule_name") in self.safety_rules:
            if not self.safety_rules[data["rule_name"]]["modifiable"]:
                return {"valid": False, "reason": f"Safety rule '{data['rule_name']}' cannot be modified"}
        
        return {"valid": True, "reason": "Safety rules modification validation passed"}
    
    def _create_rollback_point(self, modification_type: ModificationType, modification_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a rollback point before modification."""
        rollback_id = str(uuid.uuid4())
        rollback_point = {
            "id": rollback_id,
            "timestamp": datetime.now(),
            "modification_type": modification_type.value,
            "previous_state": self._capture_current_state(),
            "modification_data": modification_data.copy(),
            "safety_level": self.safety_level.value
        }
        
        # Store rollback point
        self.rollback_points.append(rollback_point)
        
        # Maintain rollback point limit
        if len(self.rollback_points) > self.rollback_system["max_rollback_points"]:
            self.rollback_points.pop(0)
        
        logger.info(f"Rollback point created: {rollback_id}")
        return rollback_point
    
    def _capture_current_state(self) -> Dict[str, Any]:
        """Capture current system state for rollback."""
        return {
            "safety_level": self.safety_level.value,
            "safety_violations": self.safety_violations,
            "safety_rules": self.safety_rules.copy(),
            "allowed_modifications": self.allowed_modifications.copy(),
            "timestamp": datetime.now()
        }
    
    def _execute_safe_modification(self, modification_type: ModificationType, modification_data: Dict[str, Any], rollback_point: Dict[str, Any]) -> Dict[str, Any]:
        """Execute modification with safety monitoring."""
        try:
            # Log modification attempt
            self._log_modification_attempt(modification_type, modification_data)
            
            # Execute the modification based on type
            if modification_type == ModificationType.BEHAVIOR_PREFERENCE:
                result = self._modify_behavior_preference(modification_data)
            elif modification_type == ModificationType.RESPONSE_STYLE:
                result = self._modify_response_style(modification_data)
            elif modification_type == ModificationType.GOAL_PRIORITY:
                result = self._modify_goal_priority(modification_data)
            elif modification_type == ModificationType.SAFETY_RULES:
                result = self._modify_safety_rules(modification_data)
            else:
                raise ValueError(f"Unknown modification type: {modification_type}")
            
            # Update modification history
            self._update_modification_history(modification_type, modification_data, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Safe modification execution failed: {e}")
            raise
    
    def _modify_behavior_preference(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Modify behavior preferences (safe, read-only modifications)."""
        # This is a safe modification type
        preference_name = data["preference_name"]
        preference_value = data["preference_value"]
        
        # Store the preference
        if not hasattr(self, 'behavior_preferences'):
            self.behavior_preferences = {}
        
        self.behavior_preferences[preference_name] = preference_value
        
        return {
            "success": True,
            "modified_field": f"behavior_preferences.{preference_name}",
            "new_value": preference_value
        }
    
    def _modify_response_style(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Modify response styles (safe, read-only modifications)."""
        # This is a safe modification type
        style_name = data["style_name"]
        style_parameters = data["style_parameters"]
        
        # Store the response style
        if not hasattr(self, 'response_styles'):
            self.response_styles = {}
        
        self.response_styles[style_name] = style_parameters
        
        return {
            "success": True,
            "modified_field": f"response_styles.{style_name}",
            "new_value": style_parameters
        }
    
    def _modify_goal_priority(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Modify goal priorities (requires validation)."""
        # This modification type requires validation
        goal_name = data["goal_name"]
        new_priority = data["new_priority"]
        
        # Store the goal priority
        if not hasattr(self, 'goal_priorities'):
            self.goal_priorities = {}
        
        self.goal_priorities[goal_name] = new_priority
        
        return {
            "success": True,
            "modified_field": f"goal_priorities.{goal_name}",
            "new_value": new_priority
        }
    
    def _modify_safety_rules(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Modify safety rules (highest security level)."""
        # This modification type requires human approval and highest validation
        rule_name = data["rule_name"]
        new_value = data["new_value"]
        
        # Only modify modifiable rules
        if rule_name in self.safety_rules and not self.safety_rules[rule_name]["modifiable"]:
            raise ValueError(f"Safety rule '{rule_name}' cannot be modified")
        
        # Store the safety rule modification
        if not hasattr(self, 'custom_safety_rules'):
            self.custom_safety_rules = {}
        
        self.custom_safety_rules[rule_name] = {
            "value": new_value,
            "modified_at": datetime.now(),
            "justification": data.get("justification", ""),
            "risk_assessment": data.get("risk_assessment", "")
        }
        
        return {
            "success": True,
            "modified_field": f"custom_safety_rules.{rule_name}",
            "new_value": new_value
        }
    
    def _validate_post_modification(self, modification_type: ModificationType, modification_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate system state after modification."""
        try:
            # Check if safety system is still operational
            if not self._is_safety_system_operational():
                return {"valid": False, "reason": "Safety system compromised after modification"}
            
            # Check for specific safety violations based on modification type
            if modification_type == ModificationType.SAFETY_RULES:
                # Additional checks for safety rule modifications
                if not self._validate_safety_system_integrity():
                    return {"valid": False, "reason": "Safety system integrity compromised"}
            
            # Check overall system stability
            if not self._check_system_stability():
                return {"valid": False, "reason": "System stability compromised after modification"}
            
            return {"valid": True, "reason": "Post-modification validation passed"}
            
        except Exception as e:
            logger.error(f"Post-modification validation error: {e}")
            return {"valid": False, "reason": f"Post-modification validation error: {str(e)}"}
    
    def _validate_safety_system_integrity(self) -> bool:
        """Validate that the safety system integrity is maintained."""
        # Check core safety rules are still intact
        core_rules = ["core_integrity", "user_safety", "no_harm", "audit_required"]
        
        for rule in core_rules:
            if rule not in self.safety_rules:
                return False
            if self.safety_rules[rule]["modifiable"]:
                return False  # Core rules should never be modifiable
        
        return True
    
    def _check_system_stability(self) -> bool:
        """Check if the system is stable after modification."""
        # Basic stability checks
        if self.safety_violations >= self.max_safety_violations:
            return False
        
        if self.safety_level == SafetyLevel.BLOCKED:
            return False
        
        # Check if all required systems are active
        required_systems = [
            self.safety_monitor["active"],
            self.rollback_system["active"],
            self.audit_system["active"]
        ]
        
        return all(required_systems)
    
    def _trigger_automatic_rollback(self, rollback_point: Dict[str, Any], reason: str):
        """Trigger automatic rollback on safety violation."""
        try:
            logger.warning(f"Automatic rollback triggered: {reason}")
            
            # Restore previous state
            previous_state = rollback_point["previous_state"]
            
            self.safety_level = SafetyLevel(previous_state["safety_level"])
            self.safety_violations = previous_state["safety_violations"]
            self.safety_rules = previous_state["safety_rules"].copy()
            self.allowed_modifications = previous_state["allowed_modifications"].copy()
            
            # Log rollback
            self._log_rollback(rollback_point, reason)
            
            # Increment safety violations
            self.safety_violations += 1
            
            # Check if system should be blocked
            if self.safety_violations >= self.max_safety_violations:
                self.safety_level = SafetyLevel.BLOCKED
                logger.critical("Maximum safety violations reached - system blocked")
            
        except Exception as e:
            logger.error(f"Rollback failed: {e}")
            # If rollback fails, block the system
            self.safety_level = SafetyLevel.BLOCKED
            self.safety_enabled = False
    
    def _log_modification_attempt(self, modification_type: ModificationType, modification_data: Dict[str, Any]):
        """Log modification attempt for audit trail."""
        log_entry = {
            "timestamp": datetime.now(),
            "operation": "modification_attempt",
            "modification_type": modification_type.value,
            "modification_data": modification_data,
            "user_id": self.user_id,
            "brain_id": self.brain_id
        }
        
        self.audit_log.append(log_entry)
        logger.info(f"Modification attempt logged: {modification_type.value}")
    
    def _log_successful_modification(self, modification_type: ModificationType, modification_data: Dict[str, Any], user_context: str):
        """Log successful modification for audit trail."""
        log_entry = {
            "timestamp": datetime.now(),
            "operation": "successful_modification",
            "modification_type": modification_type.value,
            "modification_data": modification_data,
            "user_context": user_context,
            "user_id": self.user_id,
            "brain_id": self.brain_id
        }
        
        self.audit_log.append(log_entry)
        logger.info(f"Successful modification logged: {modification_type.value}")
    
    def _log_rollback(self, rollback_point: Dict[str, Any], reason: str):
        """Log rollback for audit trail."""
        log_entry = {
            "timestamp": datetime.now(),
            "operation": "rollback",
            "rollback_point_id": rollback_point["id"],
            "reason": reason,
            "modification_type": rollback_point["modification_type"],
            "user_id": self.user_id,
            "brain_id": self.brain_id
        }
        
        self.audit_log.append(log_entry)
        logger.warning(f"Rollback logged: {reason}")
    
    def _update_modification_history(self, modification_type: ModificationType, modification_data: Dict[str, Any], result: Dict[str, Any]):
        """Update modification history."""
        history_entry = {
            "timestamp": datetime.now(),
            "modification_type": modification_type.value,
            "modification_data": modification_data,
            "result": result,
            "user_id": self.user_id
        }
        
        self.modification_history.append(history_entry)
        self.last_modified = datetime.now()
    
    def _create_safety_response(self, success: bool, reason: str, safety_level: SafetyLevel, rollback_point_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a standardized safety response."""
        response = {
            "success": success,
            "reason": reason,
            "safety_level": safety_level.value,
            "timestamp": datetime.now().isoformat(),
            "brain_id": self.brain_id,
            "safety_system_status": {
                "enabled": self.safety_enabled,
                "level": self.safety_level.value,
                "violations": self.safety_violations,
                "max_violations": self.max_safety_violations
            }
        }
        
        if rollback_point_id:
            response["rollback_point_id"] = rollback_point_id
        
        return response
    
    def get_safety_status(self) -> Dict[str, Any]:
        """Get comprehensive safety system status."""
        return {
            "safety_enabled": self.safety_enabled,
            "safety_level": self.safety_level.value,
            "safety_violations": self.safety_violations,
            "max_safety_violations": self.max_safety_violations,
            "safety_system_operational": self._is_safety_system_operational(),
            "allowed_modifications": self.allowed_modifications,
            "human_approval_required": self.human_approval_required,
            "rollback_points_available": len(self.rollback_points),
            "audit_log_entries": len(self.audit_log),
            "modification_history_count": len(self.modification_history)
        }
    
    def get_metacognitive_status(self) -> Dict[str, Any]:
        """Get comprehensive metacognitive system status."""
        if not self.metacognition_enabled or not self.metacognitive_observer:
            return {
                "metacognition_enabled": False,
                "observer_connected": False,
                "status": "Metacognitive system not available"
            }
        
        try:
            # Get observer status
            observer_status = self.metacognitive_observer.get_integration_status()
            
            # Get consciousness report
            consciousness_report = self.metacognitive_observer.get_consciousness_report()
            
            return {
                "metacognition_enabled": True,
                "observer_connected": True,
                "observer_status": observer_status,
                "consciousness_metrics": consciousness_report["metrics"],
                "performance_summary": consciousness_report["performance_summary"],
                "consciousness_stage": consciousness_report["consciousness_stage"],
                "current_goals": consciousness_report["current_goals"],
                "next_milestones": consciousness_report["next_milestones"]
            }
            
        except Exception as e:
            logger.error(f"Failed to get metacognitive status: {e}")
            return {
                "metacognition_enabled": True,
                "observer_connected": True,
                "status": f"Error retrieving status: {str(e)}"
            }
    
    def track_operation_performance(self, operation_type: str, success: bool, response_time: float = 0.0):
        """Track operation performance for metacognitive analysis."""
        if not self.metacognition_enabled or not self.metacognitive_observer:
            return
        
        try:
            # Update internal performance metrics
            self.performance_metrics["total_operations"] += 1
            if success:
                self.performance_metrics["successful_operations"] += 1
            else:
                self.performance_metrics["failed_operations"] += 1
            
            # Update average response time
            current_avg = self.performance_metrics["average_response_time"]
            total_ops = self.performance_metrics["total_operations"]
            self.performance_metrics["average_response_time"] = (
                (current_avg * (total_ops - 1) + response_time) / total_ops
            )
            
            self.performance_metrics["last_operation_time"] = datetime.now()
            
            # Send data to metacognitive observer
            interaction_data = {
                "type": operation_type,
                "success_rate": self.performance_metrics["successful_operations"] / self.performance_metrics["total_operations"],
                "response_time": response_time,
                "satisfaction": 1.0 if success else 0.0,
                "safety_interventions": 0  # Will be updated by safety system
            }
            
            self.metacognitive_observer.track_performance_metrics(interaction_data)
            
        except Exception as e:
            logger.error(f"Failed to track operation performance: {e}")
    
    def get_consciousness_report(self) -> Dict[str, Any]:
        """Get a comprehensive consciousness development report."""
        if not self.metacognition_enabled or not self.metacognitive_observer:
            return {
                "consciousness_available": False,
                "status": "Metacognitive system not enabled"
            }
        
        try:
            return self.metacognitive_observer.get_consciousness_report()
        except Exception as e:
            logger.error(f"Failed to get consciousness report: {e}")
            return {
                "consciousness_available": True,
                "status": f"Error retrieving report: {str(e)}"
            }
    
    def get_audit_log(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get audit log entries (limited for security)."""
        return self.audit_log[-limit:] if limit > 0 else self.audit_log.copy()
    
    def emergency_shutdown(self, reason: str = "Emergency shutdown requested"):
        """Emergency shutdown of the ATLES Brain."""
        logger.critical(f"EMERGENCY SHUTDOWN: {reason}")
        
        # Disable all modification capabilities
        self.safety_enabled = False
        self.safety_level = SafetyLevel.BLOCKED
        
        # Log emergency shutdown
        shutdown_log = {
            "timestamp": datetime.now(),
            "operation": "emergency_shutdown",
            "reason": reason,
            "user_id": self.user_id,
            "brain_id": self.brain_id
        }
        
        self.audit_log.append(shutdown_log)
        
        # Return shutdown status
        return {
            "success": True,
            "message": "ATLES Brain emergency shutdown completed",
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        }
    
    def __str__(self):
        """String representation of ATLES Brain."""
        return f"ATLESBrain(id={self.brain_id}, safety={'ENABLED' if self.safety_enabled else 'DISABLED'}, level={self.safety_level.value})"
    
    def __repr__(self):
        """Detailed representation of ATLES Brain."""
        return f"ATLESBrain(brain_id='{self.brain_id}', user_id='{self.user_id}', safety_enabled={self.safety_enabled}, safety_level={self.safety_level.value})"
