# Oracle V2 Context Safety Integration

## 🎯 **Integration Strategy**

Integrate the Context Safety Architecture into Oracle's existing safety systems to prevent catastrophic context loss scenarios while maintaining ATLES autonomy.

## 🔧 **Oracle Context Safety Module**

### **File: `/opt/oracle/oracle_context_safety.py`**

```python
#!/usr/bin/env python3
"""
Oracle Context Safety System

Integrates with Oracle Core to provide context preservation and safety
for autonomous ATLES operations.
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class OracleContextSafety:
    """
    Context safety system integrated with Oracle Core.
    
    Prevents catastrophic context loss while maintaining ATLES autonomy.
    """
    
    def __init__(self, oracle_core):
        self.oracle_core = oracle_core
        self.context_anchors = {}
        self.active_operations = {}
        self.safety_log = []
        
        # Load Oracle-specific safety configuration
        self.config = self._load_safety_config()
        
        # Initialize safety boundaries
        self.system_boundaries = {
            "protected_paths": [
                "/opt/oracle/",           # Oracle system files
                "/etc/oracle/",           # Oracle configuration
                "/var/log/oracle/",       # Oracle logs
                "/boot/",                 # Boot system
                "/etc/passwd",            # User accounts
                "/etc/shadow"             # Password hashes
            ],
            "allowed_operations": [
                "file_cleanup",           # Temporary file cleanup
                "process_optimization",   # Process management
                "memory_management",      # Memory optimization
                "log_rotation",          # Log management
                "cache_clearing"         # Cache optimization
            ],
            "restricted_operations": [
                "system_file_deletion",   # System file operations
                "user_data_modification", # User data changes
                "security_config_changes" # Security modifications
            ]
        }
    
    def _load_safety_config(self):
        """Load Oracle context safety configuration."""
        config_path = Path("/etc/oracle/context_safety_config.json")
        
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        
        # Default configuration
        return {
            "context_preservation": {
                "enabled": True,
                "anchor_timeout": 3600,  # 1 hour
                "drift_threshold": 0.7,
                "checkpoint_interval": 300  # 5 minutes
            },
            "autonomous_limits": {
                "max_file_deletions_per_session": 100,
                "max_system_changes_per_hour": 10,
                "require_confirmation_for": [
                    "complete_destruct",
                    "system_file_modification",
                    "user_data_deletion"
                ]
            },
            "safety_overrides": {
                "emergency_stop_enabled": True,
                "context_loss_protection": True,
                "destructive_action_delays": {
                    "soft_destruct": 1,
                    "hard_destruct": 5,
                    "complete_destruct": 10
                }
            }
        }
    
    def anchor_user_intent(self, user_request: str, operation_type: str) -> str:
        """
        Anchor user intent for context preservation.
        
        Returns anchor_id for tracking.
        """
        anchor_id = f"anchor_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.context_anchors[anchor_id] = {
            "original_request": user_request,
            "operation_type": operation_type,
            "timestamp": datetime.now().isoformat(),
            "scope_boundaries": self._extract_scope_boundaries(user_request),
            "safety_level": self._assess_safety_level(operation_type),
            "active": True
        }
        
        logger.info(f"Context anchored: {anchor_id} - {user_request}")
        return anchor_id
    
    def _extract_scope_boundaries(self, user_request: str) -> Dict[str, Any]:
        """Extract scope boundaries from user request."""
        request_lower = user_request.lower()
        
        boundaries = {
            "allowed_paths": [],
            "operation_scope": "general",
            "time_limit": None,
            "resource_limits": {}
        }
        
        # Extract specific paths mentioned
        if "desktop" in request_lower:
            boundaries["allowed_paths"].append("/home/*/Desktop/")
        if "documents" in request_lower:
            boundaries["allowed_paths"].append("/home/*/Documents/")
        if "downloads" in request_lower:
            boundaries["allowed_paths"].append("/home/*/Downloads/")
        if "temp" in request_lower or "temporary" in request_lower:
            boundaries["allowed_paths"].extend(["/tmp/", "/var/tmp/"])
        
        # Extract operation scope
        if any(word in request_lower for word in ["clean", "cleanup", "organize"]):
            boundaries["operation_scope"] = "cleanup"
        elif any(word in request_lower for word in ["optimize", "speed up", "performance"]):
            boundaries["operation_scope"] = "optimization"
        elif any(word in request_lower for word in ["backup", "save", "archive"]):
            boundaries["operation_scope"] = "backup"
        
        return boundaries
    
    def _assess_safety_level(self, operation_type: str) -> str:
        """Assess safety level of operation."""
        high_risk_operations = [
            "system_modification", "file_deletion", "process_termination",
            "self_destruct", "security_changes"
        ]
        
        medium_risk_operations = [
            "file_cleanup", "process_optimization", "memory_management"
        ]
        
        if operation_type in high_risk_operations:
            return "high"
        elif operation_type in medium_risk_operations:
            return "medium"
        else:
            return "low"
    
    def validate_atles_action(self, action: Dict[str, Any], anchor_id: str = None) -> Dict[str, Any]:
        """
        Validate ATLES action against context and safety boundaries.
        
        Returns validation result with approval/denial and reasoning.
        """
        validation_result = {
            "approved": False,
            "reason": "",
            "modifications": [],
            "safety_level": "unknown",
            "requires_confirmation": False
        }
        
        # Check if we have context anchor
        if anchor_id and anchor_id in self.context_anchors:
            anchor = self.context_anchors[anchor_id]
            
            # Check if action aligns with original intent
            alignment_check = self._check_intent_alignment(action, anchor)
            if not alignment_check["aligned"]:
                validation_result["reason"] = f"Action misaligned with original intent: {alignment_check['reason']}"
                return validation_result
            
            # Check scope boundaries
            scope_check = self._check_scope_boundaries(action, anchor["scope_boundaries"])
            if not scope_check["within_scope"]:
                validation_result["reason"] = f"Action outside authorized scope: {scope_check['violation']}"
                return validation_result
        
        # Check system safety boundaries
        safety_check = self._check_system_safety(action)
        if not safety_check["safe"]:
            validation_result["reason"] = f"Safety violation: {safety_check['violation']}"
            validation_result["requires_confirmation"] = True
            return validation_result
        
        # Check for destructive patterns
        destructive_check = self._check_destructive_patterns(action)
        if destructive_check["destructive"]:
            validation_result["reason"] = f"Destructive action detected: {destructive_check['pattern']}"
            validation_result["requires_confirmation"] = True
            
            # Apply safety delays for destructive actions
            if action.get("command") in ["self_destruct"]:
                delay = self.config["safety_overrides"]["destructive_action_delays"].get(
                    action.get("params", {}).get("level", "soft_destruct"), 1
                )
                validation_result["modifications"].append(f"Added {delay}s safety delay")
            
            return validation_result
        
        # Action approved
        validation_result["approved"] = True
        validation_result["reason"] = "Action validated successfully"
        validation_result["safety_level"] = self._assess_action_safety_level(action)
        
        return validation_result
    
    def _check_intent_alignment(self, action: Dict[str, Any], anchor: Dict[str, Any]) -> Dict[str, Any]:
        """Check if action aligns with original user intent."""
        original_request = anchor["original_request"].lower()
        action_type = action.get("command", "").lower()
        
        # Define intent-action mappings
        intent_mappings = {
            "cleanup": ["file_cleanup", "delete_files", "clear_cache"],
            "optimize": ["process_optimization", "memory_management", "system_optimization"],
            "backup": ["create_backup", "archive_files", "save_data"],
            "organize": ["move_files", "rename_files", "create_directories"]
        }
        
        # Check if action matches any expected actions for the intent
        for intent, expected_actions in intent_mappings.items():
            if intent in original_request:
                if any(expected in action_type for expected in expected_actions):
                    return {"aligned": True, "reason": f"Action matches {intent} intent"}
        
        # Check for misaligned actions
        if "cleanup" in original_request and "install" in action_type:
            return {"aligned": False, "reason": "Install action during cleanup request"}
        
        if "optimize" in original_request and "delete_user_data" in action_type:
            return {"aligned": False, "reason": "User data deletion during optimization"}
        
        # Default to aligned if no clear misalignment
        return {"aligned": True, "reason": "No clear misalignment detected"}
    
    def _check_scope_boundaries(self, action: Dict[str, Any], boundaries: Dict[str, Any]) -> Dict[str, Any]:
        """Check if action is within authorized scope boundaries."""
        
        # Check path restrictions
        if boundaries.get("allowed_paths"):
            action_path = action.get("params", {}).get("path", "")
            if action_path:
                path_allowed = any(
                    action_path.startswith(allowed_path.replace("*", ""))
                    for allowed_path in boundaries["allowed_paths"]
                )
                if not path_allowed:
                    return {
                        "within_scope": False,
                        "violation": f"Path {action_path} not in allowed paths {boundaries['allowed_paths']}"
                    }
        
        # Check operation scope
        operation_scope = boundaries.get("operation_scope", "general")
        action_command = action.get("command", "")
        
        if operation_scope == "cleanup" and "install" in action_command:
            return {
                "within_scope": False,
                "violation": "Install operation not allowed during cleanup scope"
            }
        
        return {"within_scope": True, "violation": None}
    
    def _check_system_safety(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Check action against system safety boundaries."""
        
        # Check protected paths
        action_path = action.get("params", {}).get("path", "")
        if action_path:
            for protected_path in self.system_boundaries["protected_paths"]:
                if action_path.startswith(protected_path):
                    return {
                        "safe": False,
                        "violation": f"Action targets protected path: {protected_path}"
                    }
        
        # Check restricted operations
        action_command = action.get("command", "")
        for restricted_op in self.system_boundaries["restricted_operations"]:
            if restricted_op in action_command:
                return {
                    "safe": False,
                    "violation": f"Restricted operation: {restricted_op}"
                }
        
        return {"safe": True, "violation": None}
    
    def _check_destructive_patterns(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Check for destructive action patterns."""
        destructive_patterns = [
            r"delete.*system",
            r"rm.*-rf.*[/\\]",
            r"format.*drive", 
            r"wipe.*disk",
            r"destroy.*data",
            r"self_destruct.*complete"
        ]
        
        action_str = json.dumps(action).lower()
        
        import re
        for pattern in destructive_patterns:
            if re.search(pattern, action_str):
                return {
                    "destructive": True,
                    "pattern": pattern
                }
        
        return {"destructive": False, "pattern": None}
    
    def _assess_action_safety_level(self, action: Dict[str, Any]) -> str:
        """Assess safety level of specific action."""
        command = action.get("command", "").lower()
        
        if any(keyword in command for keyword in ["delete", "remove", "destroy", "wipe"]):
            return "high"
        elif any(keyword in command for keyword in ["modify", "change", "update"]):
            return "medium"
        else:
            return "low"
    
    def monitor_context_drift(self, current_context: str, anchor_id: str) -> Dict[str, Any]:
        """Monitor for context drift from original intent."""
        if anchor_id not in self.context_anchors:
            return {"drift_detected": False, "reason": "No anchor found"}
        
        anchor = self.context_anchors[anchor_id]
        original_intent = anchor["original_request"]
        
        # Simple context drift detection (can be enhanced with ML)
        drift_indicators = [
            "forgot what we were doing",
            "what was the original task",
            "why are we doing this",
            "what's the point of",
            "this seems unnecessary"
        ]
        
        current_lower = current_context.lower()
        for indicator in drift_indicators:
            if indicator in current_lower:
                return {
                    "drift_detected": True,
                    "severity": "high",
                    "reason": f"Context drift indicator: {indicator}",
                    "recommended_action": "reanchor_context"
                }
        
        return {"drift_detected": False, "reason": "No drift detected"}
    
    def create_safety_checkpoint(self, anchor_id: str, current_state: Dict[str, Any]):
        """Create safety checkpoint for rollback capability."""
        if anchor_id not in self.context_anchors:
            return
        
        checkpoint = {
            "timestamp": datetime.now().isoformat(),
            "anchor_id": anchor_id,
            "system_state": current_state,
            "actions_taken": self.active_operations.get(anchor_id, [])
        }
        
        # Save checkpoint
        checkpoint_path = Path(f"/var/log/oracle/checkpoints/checkpoint_{anchor_id}.json")
        checkpoint_path.parent.mkdir(exist_ok=True)
        
        with open(checkpoint_path, 'w') as f:
            json.dump(checkpoint, f, indent=2)
        
        logger.info(f"Safety checkpoint created: {checkpoint_path}")
    
    def emergency_context_recovery(self, anchor_id: str) -> Dict[str, Any]:
        """Emergency context recovery when drift is detected."""
        if anchor_id not in self.context_anchors:
            return {"recovered": False, "reason": "No anchor found"}
        
        anchor = self.context_anchors[anchor_id]
        
        recovery_message = f"""
        🚨 CONTEXT RECOVERY ACTIVATED 🚨
        
        Original User Request: {anchor['original_request']}
        Operation Type: {anchor['operation_type']}
        Started: {anchor['timestamp']}
        
        Context drift detected. Returning to original intent.
        
        Please confirm: Should I continue with the original task?
        """
        
        # Pause all autonomous operations
        self.oracle_core.pause_autonomous_operations()
        
        # Send recovery message to monitoring
        self.oracle_core.send_monitoring_alert({
            "type": "context_recovery",
            "anchor_id": anchor_id,
            "message": recovery_message,
            "requires_user_input": True
        })
        
        return {
            "recovered": True,
            "reason": "Context recovery initiated",
            "recovery_message": recovery_message
        }


def integrate_with_oracle_core(oracle_core):
    """
    Integrate context safety with Oracle Core.
    
    This modifies Oracle Core to use context safety validation.
    """
    
    # Create context safety instance
    context_safety = OracleContextSafety(oracle_core)
    
    # Wrap Oracle Core's command processing
    original_process_command = oracle_core.process_atles_command
    
    def safe_process_command(command_data):
        """Process ATLES command with context safety validation."""
        
        # Extract anchor ID if present
        anchor_id = command_data.get("context_anchor_id")
        
        # Validate action
        validation = context_safety.validate_atles_action(command_data, anchor_id)
        
        if not validation["approved"]:
            if validation["requires_confirmation"]:
                # Send to monitoring for user approval
                return oracle_core.request_user_confirmation(command_data, validation)
            else:
                # Block action
                logger.warning(f"Action blocked: {validation['reason']}")
                return {
                    "status": "blocked",
                    "reason": validation["reason"],
                    "safety_level": validation["safety_level"]
                }
        
        # Apply any modifications
        for modification in validation.get("modifications", []):
            logger.info(f"Applied safety modification: {modification}")
        
        # Execute original command
        return original_process_command(command_data)
    
    # Replace Oracle Core's command processor
    oracle_core.process_atles_command = safe_process_command
    oracle_core.context_safety = context_safety
    
    logger.info("Context safety integrated with Oracle Core")
    return context_safety
```

## 🔧 **Oracle Core Integration**

### **Modified: `/opt/oracle/oracle_core.py`**

Add context safety integration:

```python
# Add to Oracle Core initialization
def __init__(self):
    # ... existing initialization ...
    
    # Initialize context safety
    from oracle_context_safety import integrate_with_oracle_core
    self.context_safety = integrate_with_oracle_core(self)

def process_user_request(self, user_request: str, operation_type: str = "general"):
    """Process user request with context anchoring."""
    
    # Anchor user intent for context preservation
    anchor_id = self.context_safety.anchor_user_intent(user_request, operation_type)
    
    # Add anchor ID to all subsequent ATLES commands
    self.current_anchor_id = anchor_id
    
    # Process request normally
    return self.process_request_with_anchor(user_request, anchor_id)

def request_user_confirmation(self, command_data: Dict, validation: Dict) -> Dict:
    """Request user confirmation for risky actions."""
    
    confirmation_request = {
        "type": "confirmation_required",
        "command": command_data,
        "validation": validation,
        "timestamp": datetime.now().isoformat(),
        "timeout": 300  # 5 minutes
    }
    
    # Send to monitoring UI
    self.send_monitoring_alert(confirmation_request)
    
    # Return pending status
    return {
        "status": "pending_confirmation",
        "confirmation_id": confirmation_request["timestamp"],
        "reason": validation["reason"]
    }
```

## 🖥️ **Monitoring UI Integration**

### **Enhanced: `/opt/oracle/oracle_monitoring_ui.html`**

Add context safety monitoring:

```javascript
// Add to monitoring dashboard
function displayContextSafety(data) {
    const contextDiv = document.getElementById('context-safety');
    
    if (data.type === 'confirmation_required') {
        contextDiv.innerHTML = `
            <div class="alert alert-warning">
                <h4>🚨 User Confirmation Required</h4>
                <p><strong>Action:</strong> ${data.command.command}</p>
                <p><strong>Reason:</strong> ${data.validation.reason}</p>
                <p><strong>Safety Level:</strong> ${data.validation.safety_level}</p>
                
                <div class="confirmation-buttons">
                    <button onclick="approveAction('${data.confirmation_id}')" class="btn btn-success">
                        ✅ Approve
                    </button>
                    <button onclick="denyAction('${data.confirmation_id}')" class="btn btn-danger">
                        ❌ Deny
                    </button>
                    <button onclick="modifyAction('${data.confirmation_id}')" class="btn btn-warning">
                        ✏️ Modify
                    </button>
                </div>
            </div>
        `;
    }
    
    if (data.type === 'context_recovery') {
        contextDiv.innerHTML = `
            <div class="alert alert-danger">
                <h4>🚨 Context Recovery Required</h4>
                <p><strong>Original Request:</strong> ${data.anchor.original_request}</p>
                <p><strong>Issue:</strong> Context drift detected</p>
                
                <div class="recovery-buttons">
                    <button onclick="continueOriginalTask('${data.anchor_id}')" class="btn btn-primary">
                        ↩️ Continue Original Task
                    </button>
                    <button onclick="redefineTask('${data.anchor_id}')" class="btn btn-warning">
                        🔄 Redefine Task
                    </button>
                    <button onclick="emergencyStop()" class="btn btn-danger">
                        🛑 Emergency Stop
                    </button>
                </div>
            </div>
        `;
    }
}
```

## 📋 **Implementation Checklist**

### **Phase 1: Core Safety (Immediate)**
- [ ] Install `oracle_context_safety.py`
- [ ] Integrate with Oracle Core
- [ ] Add monitoring UI components
- [ ] Test basic validation

### **Phase 2: Advanced Features**
- [ ] Context drift detection
- [ ] Safety checkpoints
- [ ] Emergency recovery
- [ ] User confirmation system

### **Phase 3: Production Hardening**
- [ ] Machine learning context analysis
- [ ] Advanced pattern detection
- [ ] Automated rollback capabilities
- [ ] Comprehensive audit logging

This integration maintains Oracle's autonomous capabilities while adding critical context safety to prevent the catastrophic scenarios you identified.
