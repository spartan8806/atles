#!/usr/bin/env python3
"""
ATLES Autonomous Router Optimizer

A specialized autonomous agent that continuously monitors and optimizes
the Intelligent Model Router system for better performance.
"""

import logging
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import threading

from .router_performance_monitor import RouterPerformanceMonitor, RouterOptimizationSuggestion
from .intelligent_model_router import IntelligentModelRouter, TaskType, ModelType

logger = logging.getLogger(__name__)


@dataclass
class RouterOptimizationGoal:
    """Represents an optimization goal for the router"""
    goal_id: str
    goal_type: str  # "performance", "accuracy", "efficiency", "user_satisfaction"
    priority: str   # "high", "medium", "low"
    description: str
    target_metric: str
    current_value: float
    target_value: float
    optimization_suggestions: List[RouterOptimizationSuggestion]
    status: str = "pending"  # "pending", "in_progress", "completed", "failed"
    created_at: str = ""
    completed_at: Optional[str] = None


class AutonomousRouterOptimizer:
    """
    Autonomous agent that continuously optimizes the router system
    """
    
    def __init__(self, router: IntelligentModelRouter, monitor: RouterPerformanceMonitor):
        self.router = router
        self.monitor = monitor
        self.running = False
        self.optimization_goals: List[RouterOptimizationGoal] = []
        
        # Optimization settings
        self.optimization_interval = 300  # 5 minutes
        self.min_decisions_for_optimization = 20
        self.performance_threshold = 0.8
        self.confidence_threshold = 0.85
        
        # Safety boundaries
        self.max_confidence_adjustment = 0.1
        self.max_performance_adjustment = 0.2
        self.rollback_threshold = 0.6  # Rollback if performance drops below this
        
        # State tracking
        self.last_optimization = None
        self.optimization_history = []
        self.current_baseline = {}
        
        logger.info("Autonomous Router Optimizer initialized")
    
    def start_optimization_loop(self):
        """Start the continuous optimization loop"""
        if self.running:
            return
        
        self.running = True
        self.optimization_thread = threading.Thread(target=self._optimization_loop, daemon=True)
        self.optimization_thread.start()
        logger.info("Autonomous router optimization started")
    
    def stop_optimization_loop(self):
        """Stop the optimization loop"""
        self.running = False
        if hasattr(self, 'optimization_thread'):
            self.optimization_thread.join(timeout=5)
        logger.info("Autonomous router optimization stopped")
    
    def _optimization_loop(self):
        """Main optimization loop"""
        while self.running:
            try:
                # Wait for optimization interval
                time.sleep(self.optimization_interval)
                
                if not self.running:
                    break
                
                # Perform optimization cycle
                self._perform_optimization_cycle()
                
            except Exception as e:
                logger.error(f"Error in optimization loop: {e}")
                time.sleep(60)  # Wait before retrying
    
    def _perform_optimization_cycle(self):
        """Perform a single optimization cycle"""
        logger.info("🔄 Starting router optimization cycle")
        
        # Analyze current performance
        analysis = self.monitor.analyze_performance()
        
        if analysis.get("status") == "insufficient_data":
            logger.info("⏳ Insufficient data for optimization, waiting for more routing decisions")
            return
        
        # Generate optimization goals
        goals = self._generate_optimization_goals(analysis)
        
        if not goals:
            logger.info("✅ No optimization opportunities identified")
            return
        
        # Execute optimizations
        for goal in goals:
            if self._should_execute_goal(goal):
                self._execute_optimization_goal(goal)
        
        # Update baseline metrics
        self._update_baseline_metrics(analysis)
        
        logger.info(f"🎯 Optimization cycle completed, processed {len(goals)} goals")
    
    def _generate_optimization_goals(self, analysis: Dict[str, Any]) -> List[RouterOptimizationGoal]:
        """Generate optimization goals based on performance analysis"""
        goals = []
        
        # Performance-based goals
        if analysis.get("total_decisions", 0) >= self.min_decisions_for_optimization:
            
            # Confidence optimization
            confidence_analysis = analysis.get("confidence_analysis", {})
            avg_confidence = confidence_analysis.get("average", 0)
            
            if avg_confidence < self.confidence_threshold:
                suggestions = self.monitor.generate_optimization_suggestions()
                confidence_suggestions = [s for s in suggestions if s.category == "confidence_threshold"]
                
                if confidence_suggestions:
                    goals.append(RouterOptimizationGoal(
                        goal_id=f"confidence_opt_{int(time.time())}",
                        goal_type="accuracy",
                        priority="medium",
                        description=f"Improve average confidence from {avg_confidence:.2f} to {self.confidence_threshold}",
                        target_metric="average_confidence",
                        current_value=avg_confidence,
                        target_value=self.confidence_threshold,
                        optimization_suggestions=confidence_suggestions,
                        created_at=datetime.now().isoformat()
                    ))
            
            # Model performance optimization
            model_performance = analysis.get("model_performance", {})
            for model, metrics in model_performance.items():
                success_rate = metrics.get("success_rate", 0)
                
                if success_rate < self.performance_threshold and metrics.get("recent_requests", 0) >= 5:
                    suggestions = self.monitor.generate_optimization_suggestions()
                    model_suggestions = [s for s in suggestions if s.category == "model_preference" and model in str(s.supporting_data)]
                    
                    if model_suggestions:
                        goals.append(RouterOptimizationGoal(
                            goal_id=f"model_perf_{model}_{int(time.time())}",
                            goal_type="performance",
                            priority="high",
                            description=f"Improve {model} success rate from {success_rate:.2f} to {self.performance_threshold}",
                            target_metric=f"{model}_success_rate",
                            current_value=success_rate,
                            target_value=self.performance_threshold,
                            optimization_suggestions=model_suggestions,
                            created_at=datetime.now().isoformat()
                        ))
            
            # Pattern optimization
            suggestions = self.monitor.generate_optimization_suggestions()
            pattern_suggestions = [s for s in suggestions if s.category == "pattern_update"]
            
            if pattern_suggestions:
                goals.append(RouterOptimizationGoal(
                    goal_id=f"pattern_opt_{int(time.time())}",
                    goal_type="efficiency",
                    priority="low",
                    description="Optimize routing patterns for better efficiency",
                    target_metric="routing_efficiency",
                    current_value=0.8,  # Estimated current efficiency
                    target_value=0.9,   # Target efficiency
                    optimization_suggestions=pattern_suggestions,
                    created_at=datetime.now().isoformat()
                ))
        
        return goals
    
    def _should_execute_goal(self, goal: RouterOptimizationGoal) -> bool:
        """Determine if a goal should be executed"""
        # Safety checks
        if goal.priority == "high":
            return True
        elif goal.priority == "medium":
            # Execute medium priority goals if no high priority goals are pending
            high_priority_pending = any(g.priority == "high" and g.status == "pending" for g in self.optimization_goals)
            return not high_priority_pending
        else:  # low priority
            # Execute low priority goals only if system is stable
            return self._is_system_stable()
    
    def _is_system_stable(self) -> bool:
        """Check if the router system is stable enough for low-priority optimizations"""
        recent_performance = self.monitor.get_performance_summary()
        
        # Check if recent performance is good
        success_rate = recent_performance.get("success_rate", 0)
        avg_confidence = recent_performance.get("average_confidence", 0)
        
        return success_rate > 0.8 and avg_confidence > 0.8
    
    def _execute_optimization_goal(self, goal: RouterOptimizationGoal):
        """Execute an optimization goal"""
        logger.info(f"🎯 Executing optimization goal: {goal.description}")
        
        goal.status = "in_progress"
        self.optimization_goals.append(goal)
        
        try:
            # Store baseline before optimization
            baseline = self._capture_baseline()
            
            # Apply optimizations
            applied_changes = []
            for suggestion in goal.optimization_suggestions:
                change = self._apply_optimization_suggestion(suggestion)
                if change:
                    applied_changes.append(change)
            
            if applied_changes:
                # Wait for some decisions to evaluate impact
                logger.info(f"⏳ Applied {len(applied_changes)} changes, waiting to evaluate impact...")
                
                # Record the optimization
                self.optimization_history.append({
                    "goal_id": goal.goal_id,
                    "timestamp": datetime.now().isoformat(),
                    "changes_applied": applied_changes,
                    "baseline": baseline,
                    "status": "applied"
                })
                
                goal.status = "completed"
                goal.completed_at = datetime.now().isoformat()
                
                logger.info(f"✅ Optimization goal completed: {goal.description}")
            else:
                goal.status = "failed"
                logger.warning(f"❌ Failed to apply optimizations for goal: {goal.description}")
                
        except Exception as e:
            goal.status = "failed"
            logger.error(f"❌ Error executing optimization goal: {e}")
    
    def _apply_optimization_suggestion(self, suggestion: RouterOptimizationSuggestion) -> Optional[Dict[str, Any]]:
        """Apply a specific optimization suggestion"""
        try:
            if suggestion.category == "confidence_threshold":
                # Adjust confidence thresholds (simulated - would need router API)
                logger.info(f"🔧 Adjusting confidence threshold: {suggestion.current_value} → {suggestion.suggested_value}")
                return {
                    "type": "confidence_threshold",
                    "old_value": suggestion.current_value,
                    "new_value": suggestion.suggested_value,
                    "suggestion_id": suggestion.suggestion_id
                }
            
            elif suggestion.category == "model_preference":
                # Adjust model preferences (simulated - would need router API)
                logger.info(f"🔧 Adjusting model preference: {suggestion.description}")
                return {
                    "type": "model_preference",
                    "description": suggestion.description,
                    "suggestion_id": suggestion.suggestion_id
                }
            
            elif suggestion.category == "pattern_update":
                # Add or update routing patterns (simulated - would need router API)
                logger.info(f"🔧 Updating routing pattern: {suggestion.description}")
                return {
                    "type": "pattern_update",
                    "description": suggestion.description,
                    "suggestion_id": suggestion.suggestion_id
                }
            
            else:
                logger.warning(f"Unknown optimization category: {suggestion.category}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to apply optimization suggestion: {e}")
            return None
    
    def _capture_baseline(self) -> Dict[str, Any]:
        """Capture current performance baseline"""
        return {
            "timestamp": datetime.now().isoformat(),
            "performance_summary": self.monitor.get_performance_summary(),
            "recent_analysis": self.monitor.analyze_performance()
        }
    
    def _update_baseline_metrics(self, analysis: Dict[str, Any]):
        """Update baseline performance metrics"""
        self.current_baseline = {
            "timestamp": datetime.now().isoformat(),
            "total_decisions": analysis.get("total_decisions", 0),
            "average_confidence": analysis.get("confidence_analysis", {}).get("average", 0),
            "model_performance": analysis.get("model_performance", {}),
            "issues_count": len(analysis.get("issues_identified", [])),
            "optimization_opportunities": len(analysis.get("optimization_opportunities", []))
        }
    
    def get_optimization_status(self) -> Dict[str, Any]:
        """Get current optimization status"""
        return {
            "running": self.running,
            "last_optimization": self.last_optimization,
            "total_goals": len(self.optimization_goals),
            "pending_goals": len([g for g in self.optimization_goals if g.status == "pending"]),
            "completed_goals": len([g for g in self.optimization_goals if g.status == "completed"]),
            "failed_goals": len([g for g in self.optimization_goals if g.status == "failed"]),
            "optimization_history_count": len(self.optimization_history),
            "current_baseline": self.current_baseline,
            "system_stable": self._is_system_stable()
        }
    
    def get_recent_optimizations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent optimization activities"""
        return self.optimization_history[-limit:] if self.optimization_history else []
    
    def force_optimization_cycle(self):
        """Force an immediate optimization cycle (for testing/manual trigger)"""
        logger.info("🔄 Manual optimization cycle triggered")
        self._perform_optimization_cycle()


# Integration functions for V5 autonomous system
def create_router_optimizer(router: IntelligentModelRouter, monitor: RouterPerformanceMonitor) -> AutonomousRouterOptimizer:
    """Create a router optimizer for integration with V5"""
    return AutonomousRouterOptimizer(router, monitor)


def integrate_with_v5_autonomous_system(v5_system, router: IntelligentModelRouter, monitor: RouterPerformanceMonitor):
    """Integrate router optimization with V5 autonomous system"""
    optimizer = create_router_optimizer(router, monitor)
    
    # Add router optimization goals to V5 system
    v5_system.router_optimizer = optimizer
    
    # Start optimization loop
    optimizer.start_optimization_loop()
    
    logger.info("Router optimization integrated with V5 autonomous system")
    return optimizer


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Example usage
    from .intelligent_model_router import IntelligentModelRouter
    from .router_performance_monitor import RouterPerformanceMonitor
    
    router = IntelligentModelRouter()
    monitor = RouterPerformanceMonitor()
    optimizer = AutonomousRouterOptimizer(router, monitor)
    
    # Start optimization
    optimizer.start_optimization_loop()
    
    print("Router optimization started. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(10)
            status = optimizer.get_optimization_status()
            print(f"Status: {status['pending_goals']} pending, {status['completed_goals']} completed")
    except KeyboardInterrupt:
        optimizer.stop_optimization_loop()
        print("Router optimization stopped.")
