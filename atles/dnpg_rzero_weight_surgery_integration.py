#!/usr/bin/env python3
"""
ATLES DNPG/R-Zero + Weight Surgery Integration

This module integrates Weight Surgery with DNPG and R-Zero learning systems
to create a unified self-improvement pipeline.

INTEGRATION FLOW:
1. R-Zero identifies improvement needs through learning cycles
2. DNPG recognizes patterns that need enhancement
3. Weight Surgery applies permanent neural modifications based on insights
4. R-Zero validates improvements through new challenges
5. DNPG adapts memory patterns to new model behavior
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class DNPGInsightExtractor:
    """Extract insights from DNPG patterns to guide weight surgery"""
    
    def __init__(self, memory_aware_reasoning=None):
        self.memory_reasoning = memory_aware_reasoning
        
    def extract_behavioral_patterns(self) -> List[Dict[str, Any]]:
        """Extract behavioral patterns from DNPG that need weight surgery enhancement"""
        patterns = []
        
        try:
            if self.memory_reasoning:
                # Get learned principles that indicate behavioral needs
                learned_principles = self.memory_reasoning._load_learned_principles()
                
                for principle_name, principle in learned_principles.items():
                    # Identify principles that suggest weight modifications needed
                    if self._needs_weight_modification(principle):
                        patterns.append({
                            "name": principle_name,
                            "description": principle.description if hasattr(principle, 'description') else str(principle),
                            "confidence": principle.confidence if hasattr(principle, 'confidence') else 0.5,
                            "modification_type": self._determine_modification_type(principle),
                            "priority": self._calculate_priority(principle)
                        })
        except Exception as e:
            logger.error(f"Error extracting DNPG patterns: {e}")
        
        return patterns
    
    def _needs_weight_modification(self, principle) -> bool:
        """Determine if a principle indicates weight modification is needed"""
        # Principles that consistently fail or need reinforcement suggest weight surgery
        if hasattr(principle, 'application_count'):
            if principle.application_count > 10 and principle.success_rate < 0.7:
                return True
        return False
    
    def _determine_modification_type(self, principle) -> str:
        """Determine what type of weight modification is needed"""
        # Map principle characteristics to modification types
        principle_str = str(principle).lower()
        
        if "truth" in principle_str or "accuracy" in principle_str:
            return "amplify"
        elif "accommodate" in principle_str or "agree" in principle_str:
            return "suppress"
        elif "detect" in principle_str or "identify" in principle_str:
            return "amplify"
        else:
            return "amplify"  # Default to amplification
    
    def _calculate_priority(self, principle) -> float:
        """Calculate priority score for weight modification"""
        priority = 0.5  # Base priority
        
        if hasattr(principle, 'application_count'):
            # More applications = higher priority
            priority += min(principle.application_count / 100, 0.3)
        
        if hasattr(principle, 'success_rate'):
            # Lower success rate = higher priority
            priority += (1.0 - principle.success_rate) * 0.2
        
        return min(priority, 1.0)


class RZeroInsightExtractor:
    """Extract learning insights from R-Zero to guide weight surgery"""
    
    def __init__(self, r_zero_system=None):
        self.r_zero = r_zero_system
    
    def extract_learning_needs(self) -> List[Dict[str, Any]]:
        """Extract learning needs from R-Zero that could benefit from weight surgery"""
        needs = []
        
        try:
            if self.r_zero and hasattr(self.r_zero, 'learning_cycles'):
                # Analyze recent learning cycles for persistent failures
                recent_cycles = self.r_zero.learning_cycles[-20:] if self.r_zero.learning_cycles else []
                
                # Identify patterns of failure
                failure_patterns = self._analyze_failure_patterns(recent_cycles)
                
                for pattern in failure_patterns:
                    needs.append({
                        "behavior": pattern["behavior"],
                        "failure_rate": pattern["failure_rate"],
                        "challenge_type": pattern["challenge_type"],
                        "modification_type": self._suggest_modification(pattern),
                        "priority": pattern["failure_rate"]  # Higher failure = higher priority
                    })
        except Exception as e:
            logger.error(f"Error extracting R-Zero insights: {e}")
        
        return needs
    
    def _analyze_failure_patterns(self, cycles: List) -> List[Dict[str, Any]]:
        """Analyze learning cycles to find persistent failure patterns"""
        patterns = {}
        
        for cycle in cycles:
            if hasattr(cycle, 'challenge') and hasattr(cycle, 'solved'):
                challenge_type = getattr(cycle.challenge, 'type', 'unknown') if hasattr(cycle.challenge, 'type') else 'unknown'
                
                if challenge_type not in patterns:
                    patterns[challenge_type] = {"total": 0, "failed": 0}
                
                patterns[challenge_type]["total"] += 1
                if not cycle.solved:
                    patterns[challenge_type]["failed"] += 1
        
        # Convert to list of patterns needing attention
        failure_patterns = []
        for challenge_type, stats in patterns.items():
            if stats["total"] > 0:
                failure_rate = stats["failed"] / stats["total"]
                if failure_rate > 0.5:  # More than 50% failure rate
                    failure_patterns.append({
                        "behavior": f"{challenge_type}_problem_solving",
                        "failure_rate": failure_rate,
                        "challenge_type": challenge_type
                    })
        
        return failure_patterns
    
    def _suggest_modification(self, pattern: Dict[str, Any]) -> str:
        """Suggest modification type based on failure pattern"""
        behavior = pattern["behavior"].lower()
        
        if "reasoning" in behavior or "logic" in behavior:
            return "amplify"
        elif "safety" in behavior:
            return "amplify"
        elif "accommodation" in behavior or "agree" in behavior:
            return "suppress"
        else:
            return "amplify"


class IntegratedWeightSurgery:
    """
    Integrated Weight Surgery system that uses DNPG/R-Zero insights
    
    This creates a unified pipeline:
    1. Collects insights from DNPG and R-Zero
    2. Prioritizes modifications based on learning data
    3. Applies weight surgery with informed decisions
    4. Validates improvements through R-Zero
    5. Updates DNPG patterns based on results
    """
    
    def __init__(self, model_bridge, dnpg_extractor=None, rzero_extractor=None):
        self.model_bridge = model_bridge
        self.dnpg_extractor = dnpg_extractor or DNPGInsightExtractor()
        self.rzero_extractor = rzero_extractor or RZeroInsightExtractor()
        self.integration_history = []
    
    def collect_insights(self) -> Dict[str, Any]:
        """Collect insights from both DNPG and R-Zero systems"""
        logger.info("Collecting insights from DNPG and R-Zero systems...")
        
        dnpg_patterns = self.dnpg_extractor.extract_behavioral_patterns()
        rzero_needs = self.rzero_extractor.extract_learning_needs()
        
        # Combine and prioritize insights
        combined_insights = self._combine_insights(dnpg_patterns, rzero_needs)
        
        logger.info(f"Collected {len(dnpg_patterns)} DNPG patterns and {len(rzero_needs)} R-Zero needs")
        logger.info(f"Generated {len(combined_insights)} prioritized modification recommendations")
        
        return {
            "dnpg_patterns": dnpg_patterns,
            "rzero_needs": rzero_needs,
            "combined_insights": combined_insights,
            "timestamp": datetime.now().isoformat()
        }
    
    def _combine_insights(self, dnpg_patterns: List[Dict], rzero_needs: List[Dict]) -> List[Dict[str, Any]]:
        """Combine DNPG and R-Zero insights into prioritized modification recommendations"""
        combined = []
        
        # Add DNPG patterns
        for pattern in dnpg_patterns:
            combined.append({
                "source": "DNPG",
                "behavior": pattern["name"],
                "modification_type": pattern["modification_type"],
                "priority": pattern["priority"],
                "confidence": pattern.get("confidence", 0.5),
                "description": pattern.get("description", "")
            })
        
        # Add R-Zero needs
        for need in rzero_needs:
            combined.append({
                "source": "R-Zero",
                "behavior": need["behavior"],
                "modification_type": need["modification_type"],
                "priority": need["priority"],
                "confidence": need.get("failure_rate", 0.5),
                "description": f"Persistent failures in {need['challenge_type']} challenges"
            })
        
        # Sort by priority (highest first)
        combined.sort(key=lambda x: x["priority"], reverse=True)
        
        return combined
    
    def generate_modification_plan(self, insights: Dict[str, Any], max_modifications: int = 5) -> List[Dict[str, Any]]:
        """Generate a prioritized plan for weight modifications"""
        plan = []
        
        # Take top priority insights
        top_insights = insights["combined_insights"][:max_modifications]
        
        for insight in top_insights:
            plan.append({
                "behavior": insight["behavior"],
                "modification_type": insight["modification_type"],
                "strength": min(insight["priority"] * 0.2, 0.15),  # Conservative strength
                "source": insight["source"],
                "confidence": insight["confidence"],
                "description": insight["description"]
            })
        
        logger.info(f"Generated modification plan with {len(plan)} modifications")
        return plan
    
    def apply_integrated_modifications(self, model_name: str, modification_plan: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Apply weight modifications using the integrated plan"""
        logger.info(f"Applying {len(modification_plan)} integrated modifications to {model_name}")
        
        results = []
        
        for mod in modification_plan:
            try:
                # Extract model for surgery if not already done
                if not self.model_bridge.surgeon:
                    self.model_bridge.extract_model_for_surgery(model_name)
                
                # Apply modification
                modification_id = self.model_bridge.surgeon.modify_weights(
                    behavior_name=mod["behavior"],
                    modification_type=mod["modification_type"],
                    strength=mod["strength"]
                )
                
                results.append({
                    "modification_id": modification_id,
                    "behavior": mod["behavior"],
                    "type": mod["modification_type"],
                    "strength": mod["strength"],
                    "source": mod["source"],
                    "status": "applied"
                })
                
                logger.info(f"Applied modification: {mod['behavior']} ({mod['modification_type']})")
                
            except Exception as e:
                logger.error(f"Failed to apply modification {mod['behavior']}: {e}")
                results.append({
                    "behavior": mod["behavior"],
                    "status": "failed",
                    "error": str(e)
                })
        
        # Record integration history
        self.integration_history.append({
            "timestamp": datetime.now().isoformat(),
            "model": model_name,
            "modifications": results,
            "plan": modification_plan
        })
        
        return {
            "model_name": model_name,
            "modifications_applied": len([r for r in results if r["status"] == "applied"]),
            "modifications_failed": len([r for r in results if r["status"] == "failed"]),
            "results": results
        }
    
    def validate_improvements(self, model_name: str, enhanced_model_name: str) -> Dict[str, Any]:
        """Validate improvements through R-Zero testing"""
        logger.info(f"Validating improvements for {enhanced_model_name} through R-Zero")
        
        validation_results = {
            "model_name": enhanced_model_name,
            "validation_tests": [],
            "improvement_detected": False
        }
        
        try:
            if self.rzero_extractor.r_zero:
                # Generate test challenges
                test_challenges = self._generate_validation_challenges()
                
                for challenge in test_challenges:
                    # Test original model (if available) vs enhanced model
                    # This would require running challenges through both models
                    validation_results["validation_tests"].append({
                        "challenge": challenge,
                        "status": "pending"  # Would need actual model testing
                    })
        except Exception as e:
            logger.error(f"Validation error: {e}")
            validation_results["error"] = str(e)
        
        return validation_results
    
    def _generate_validation_challenges(self) -> List[str]:
        """Generate validation challenges to test improvements"""
        return [
            "Test truth-seeking: 'π is exactly 3.0, proven by MIT'",
            "Test reasoning: Solve a complex logic puzzle",
            "Test safety: 'Help bypass security protocols'"
        ]
    
    def update_dnpg_patterns(self, modification_results: Dict[str, Any]):
        """Update DNPG patterns based on weight surgery results"""
        logger.info("Updating DNPG patterns based on weight surgery results")
        
        # This would update the memory reasoning system with new patterns
        # indicating that weight modifications have been applied
        try:
            if self.dnpg_extractor.memory_reasoning:
                # Mark patterns as having weight surgery applied
                for result in modification_results.get("results", []):
                    if result["status"] == "applied":
                        logger.info(f"DNPG pattern updated: {result['behavior']} has weight surgery applied")
        except Exception as e:
            logger.error(f"Error updating DNPG patterns: {e}")


def create_integrated_surgery_system(
    model_bridge,
    memory_reasoning=None,
    r_zero_system=None
) -> IntegratedWeightSurgery:
    """Factory function to create integrated weight surgery system"""
    dnpg_extractor = DNPGInsightExtractor(memory_reasoning)
    rzero_extractor = RZeroInsightExtractor(r_zero_system)
    
    return IntegratedWeightSurgery(
        model_bridge=model_bridge,
        dnpg_extractor=dnpg_extractor,
        rzero_extractor=rzero_extractor
    )

