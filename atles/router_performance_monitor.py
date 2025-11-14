#!/usr/bin/env python3
"""
ATLES Router Performance Monitor

Tracks routing decisions, analyzes performance, and identifies optimization opportunities
for the Intelligent Model Router system.
"""

import logging
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from collections import defaultdict, Counter
import statistics

logger = logging.getLogger(__name__)


@dataclass
class RoutingDecisionRecord:
    """Records a single routing decision for analysis"""
    timestamp: str
    request: str
    selected_model: str
    task_type: str
    confidence: float
    reasoning: str
    response_quality: Optional[float] = None  # User feedback or measured quality
    response_time: Optional[float] = None
    success: Optional[bool] = None
    user_satisfaction: Optional[float] = None


@dataclass
class ModelPerformanceMetrics:
    """Performance metrics for a specific model"""
    model_name: str
    total_requests: int = 0
    successful_requests: int = 0
    average_confidence: float = 0.0
    average_response_time: float = 0.0
    average_quality: float = 0.0
    task_distribution: Dict[str, int] = field(default_factory=dict)
    recent_performance: List[float] = field(default_factory=list)


@dataclass
class RouterOptimizationSuggestion:
    """Suggestion for improving router performance"""
    suggestion_id: str
    category: str  # "confidence_threshold", "pattern_update", "model_preference", etc.
    priority: str  # "high", "medium", "low"
    description: str
    current_value: Any
    suggested_value: Any
    expected_improvement: str
    confidence: float
    supporting_data: Dict[str, Any]


class RouterPerformanceMonitor:
    """
    Monitors router performance and suggests optimizations
    """
    
    def __init__(self, data_dir: str = "router_performance_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Data storage
        self.routing_history: List[RoutingDecisionRecord] = []
        self.model_metrics: Dict[str, ModelPerformanceMetrics] = {}
        self.optimization_suggestions: List[RouterOptimizationSuggestion] = []
        
        # Analysis settings
        self.analysis_window_days = 7
        self.min_decisions_for_analysis = 10
        self.confidence_threshold_low = 0.7
        self.confidence_threshold_high = 0.95
        
        # Load existing data
        self._load_historical_data()
        
        logger.info("Router Performance Monitor initialized")
    
    def record_routing_decision(self, request: str, selected_model: str, task_type: str, 
                              confidence: float, reasoning: str, response_time: float = None):
        """Record a routing decision for analysis"""
        record = RoutingDecisionRecord(
            timestamp=datetime.now().isoformat(),
            request=request[:100],  # Truncate for privacy
            selected_model=selected_model,
            task_type=task_type,
            confidence=confidence,
            reasoning=reasoning,
            response_time=response_time
        )
        
        self.routing_history.append(record)
        self._update_model_metrics(record)
        
        # Save periodically
        if len(self.routing_history) % 10 == 0:
            self._save_data()
        
        logger.debug(f"Recorded routing decision: {selected_model} for {task_type} (confidence: {confidence:.2f})")
    
    def record_user_feedback(self, request: str, satisfaction: float, quality: float = None):
        """Record user feedback for the most recent matching request"""
        # Find the most recent matching request
        for record in reversed(self.routing_history):
            if record.request.startswith(request[:50]):
                record.user_satisfaction = satisfaction
                if quality is not None:
                    record.response_quality = quality
                record.success = satisfaction > 0.5
                break
        
        logger.debug(f"Recorded user feedback: satisfaction={satisfaction}")
    
    def _update_model_metrics(self, record: RoutingDecisionRecord):
        """Update performance metrics for a model"""
        model = record.selected_model
        
        if model not in self.model_metrics:
            self.model_metrics[model] = ModelPerformanceMetrics(model_name=model)
        
        metrics = self.model_metrics[model]
        metrics.total_requests += 1
        
        # Update averages
        metrics.average_confidence = self._update_average(
            metrics.average_confidence, record.confidence, metrics.total_requests
        )
        
        if record.response_time:
            metrics.average_response_time = self._update_average(
                metrics.average_response_time, record.response_time, metrics.total_requests
            )
        
        # Update task distribution
        if record.task_type not in metrics.task_distribution:
            metrics.task_distribution[record.task_type] = 0
        metrics.task_distribution[record.task_type] += 1
        
        # Track recent performance
        if record.user_satisfaction is not None:
            metrics.recent_performance.append(record.user_satisfaction)
            if len(metrics.recent_performance) > 20:  # Keep last 20 ratings
                metrics.recent_performance.pop(0)
    
    def _update_average(self, current_avg: float, new_value: float, count: int) -> float:
        """Update running average"""
        if count == 1:
            return new_value
        return ((current_avg * (count - 1)) + new_value) / count
    
    def analyze_performance(self) -> Dict[str, Any]:
        """Analyze router performance and identify issues"""
        if len(self.routing_history) < self.min_decisions_for_analysis:
            return {"status": "insufficient_data", "decisions": len(self.routing_history)}
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "total_decisions": len(self.routing_history),
            "analysis_period": f"Last {self.analysis_window_days} days",
            "model_performance": {},
            "task_distribution": {},
            "confidence_analysis": {},
            "issues_identified": [],
            "optimization_opportunities": []
        }
        
        # Recent decisions only
        cutoff_date = datetime.now() - timedelta(days=self.analysis_window_days)
        recent_decisions = [
            r for r in self.routing_history 
            if datetime.fromisoformat(r.timestamp) > cutoff_date
        ]
        
        if not recent_decisions:
            return analysis
        
        # Model performance analysis
        for model_name, metrics in self.model_metrics.items():
            model_recent = [r for r in recent_decisions if r.selected_model == model_name]
            if not model_recent:
                continue
            
            success_rate = len([r for r in model_recent if r.success]) / len(model_recent) if model_recent else 0
            avg_confidence = statistics.mean([r.confidence for r in model_recent])
            
            analysis["model_performance"][model_name] = {
                "recent_requests": len(model_recent),
                "success_rate": success_rate,
                "average_confidence": avg_confidence,
                "task_types": Counter([r.task_type for r in model_recent])
            }
        
        # Task distribution analysis
        task_counter = Counter([r.task_type for r in recent_decisions])
        analysis["task_distribution"] = dict(task_counter)
        
        # Confidence analysis
        confidences = [r.confidence for r in recent_decisions]
        analysis["confidence_analysis"] = {
            "average": statistics.mean(confidences),
            "median": statistics.median(confidences),
            "low_confidence_count": len([c for c in confidences if c < self.confidence_threshold_low]),
            "high_confidence_count": len([c for c in confidences if c > self.confidence_threshold_high])
        }
        
        # Identify issues
        analysis["issues_identified"] = self._identify_issues(recent_decisions)
        analysis["optimization_opportunities"] = self._identify_optimizations(recent_decisions)
        
        return analysis
    
    def _identify_issues(self, recent_decisions: List[RoutingDecisionRecord]) -> List[Dict[str, Any]]:
        """Identify performance issues"""
        issues = []
        
        # Low confidence decisions
        low_confidence = [r for r in recent_decisions if r.confidence < self.confidence_threshold_low]
        if len(low_confidence) > len(recent_decisions) * 0.2:  # More than 20%
            issues.append({
                "type": "high_low_confidence_rate",
                "severity": "medium",
                "description": f"{len(low_confidence)} decisions had low confidence (<{self.confidence_threshold_low})",
                "affected_tasks": Counter([r.task_type for r in low_confidence])
            })
        
        # Model performance issues
        for model_name, metrics in self.model_metrics.items():
            if len(metrics.recent_performance) >= 5:
                avg_satisfaction = statistics.mean(metrics.recent_performance)
                if avg_satisfaction < 0.6:
                    issues.append({
                        "type": "low_model_satisfaction",
                        "severity": "high",
                        "description": f"Model {model_name} has low user satisfaction ({avg_satisfaction:.2f})",
                        "model": model_name,
                        "satisfaction": avg_satisfaction
                    })
        
        # Task routing consistency
        task_models = defaultdict(list)
        for r in recent_decisions:
            task_models[r.task_type].append(r.selected_model)
        
        for task, models in task_models.items():
            model_distribution = Counter(models)
            if len(model_distribution) > 2 and max(model_distribution.values()) < len(models) * 0.7:
                issues.append({
                    "type": "inconsistent_task_routing",
                    "severity": "low",
                    "description": f"Task '{task}' routed to multiple models inconsistently",
                    "task": task,
                    "model_distribution": dict(model_distribution)
                })
        
        return issues
    
    def _identify_optimizations(self, recent_decisions: List[RoutingDecisionRecord]) -> List[Dict[str, Any]]:
        """Identify optimization opportunities"""
        optimizations = []
        
        # Pattern learning opportunities
        request_patterns = defaultdict(list)
        for r in recent_decisions:
            # Simple pattern extraction (first 3 words)
            pattern = ' '.join(r.request.lower().split()[:3])
            request_patterns[pattern].append(r)
        
        for pattern, decisions in request_patterns.items():
            if len(decisions) >= 3:
                models = [r.selected_model for r in decisions]
                confidences = [r.confidence for r in decisions]
                
                if len(set(models)) == 1 and statistics.mean(confidences) > 0.9:
                    optimizations.append({
                        "type": "pattern_confidence_boost",
                        "description": f"Pattern '{pattern}' consistently routes to {models[0]} with high confidence",
                        "pattern": pattern,
                        "model": models[0],
                        "confidence": statistics.mean(confidences),
                        "occurrences": len(decisions)
                    })
        
        # Model preference optimizations
        successful_decisions = [r for r in recent_decisions if r.success]
        if successful_decisions:
            model_success = defaultdict(list)
            for r in successful_decisions:
                model_success[r.selected_model].append(r.user_satisfaction or 0.8)
            
            best_models = sorted(
                [(model, statistics.mean(satisfactions)) for model, satisfactions in model_success.items()],
                key=lambda x: x[1], reverse=True
            )
            
            if len(best_models) > 1 and best_models[0][1] > best_models[1][1] + 0.1:
                optimizations.append({
                    "type": "model_preference_adjustment",
                    "description": f"Model {best_models[0][0]} shows significantly better performance",
                    "best_model": best_models[0][0],
                    "satisfaction": best_models[0][1],
                    "improvement_over_second": best_models[0][1] - best_models[1][1]
                })
        
        return optimizations
    
    def generate_optimization_suggestions(self) -> List[RouterOptimizationSuggestion]:
        """Generate specific optimization suggestions for the autonomous system"""
        analysis = self.analyze_performance()
        suggestions = []
        
        # Low confidence threshold adjustment
        if analysis.get("confidence_analysis", {}).get("low_confidence_count", 0) > 5:
            suggestions.append(RouterOptimizationSuggestion(
                suggestion_id=f"confidence_threshold_{int(time.time())}",
                category="confidence_threshold",
                priority="medium",
                description="Lower confidence threshold to reduce low-confidence decisions",
                current_value=self.confidence_threshold_low,
                suggested_value=self.confidence_threshold_low - 0.05,
                expected_improvement="Reduce low-confidence routing decisions by 15-20%",
                confidence=0.75,
                supporting_data={
                    "low_confidence_count": analysis["confidence_analysis"]["low_confidence_count"],
                    "total_decisions": analysis["total_decisions"]
                }
            ))
        
        # Model performance adjustments
        for issue in analysis.get("issues_identified", []):
            if issue["type"] == "low_model_satisfaction":
                suggestions.append(RouterOptimizationSuggestion(
                    suggestion_id=f"model_performance_{issue['model']}_{int(time.time())}",
                    category="model_preference",
                    priority="high",
                    description=f"Reduce preference for {issue['model']} due to low satisfaction",
                    current_value=f"Current model preference: normal",
                    suggested_value=f"Reduce {issue['model']} preference by 0.1",
                    expected_improvement="Improve overall user satisfaction by routing away from underperforming model",
                    confidence=0.85,
                    supporting_data=issue
                ))
        
        # Pattern optimization
        for opt in analysis.get("optimization_opportunities", []):
            if opt["type"] == "pattern_confidence_boost":
                suggestions.append(RouterOptimizationSuggestion(
                    suggestion_id=f"pattern_boost_{opt['pattern'].replace(' ', '_')}_{int(time.time())}",
                    category="pattern_update",
                    priority="low",
                    description=f"Add high-confidence pattern for '{opt['pattern']}' → {opt['model']}",
                    current_value="No specific pattern",
                    suggested_value=f"Direct route pattern '{opt['pattern']}' to {opt['model']}",
                    expected_improvement="Faster routing and higher confidence for this pattern",
                    confidence=0.9,
                    supporting_data=opt
                ))
        
        self.optimization_suggestions.extend(suggestions)
        return suggestions
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get a summary of router performance"""
        if not self.routing_history:
            return {"status": "no_data"}
        
        recent_decisions = self.routing_history[-50:]  # Last 50 decisions
        
        return {
            "total_decisions": len(self.routing_history),
            "recent_decisions": len(recent_decisions),
            "models_used": len(set(r.selected_model for r in recent_decisions)),
            "task_types": len(set(r.task_type for r in recent_decisions)),
            "average_confidence": statistics.mean([r.confidence for r in recent_decisions]),
            "success_rate": len([r for r in recent_decisions if r.success]) / len(recent_decisions) if recent_decisions else 0,
            "optimization_suggestions": len(self.optimization_suggestions),
            "last_analysis": datetime.now().isoformat()
        }
    
    def _save_data(self):
        """Save performance data to disk"""
        try:
            # Save routing history
            history_file = self.data_dir / "routing_history.json"
            with open(history_file, 'w') as f:
                json.dump([
                    {
                        "timestamp": r.timestamp,
                        "request": r.request,
                        "selected_model": r.selected_model,
                        "task_type": r.task_type,
                        "confidence": r.confidence,
                        "reasoning": r.reasoning,
                        "response_quality": r.response_quality,
                        "response_time": r.response_time,
                        "success": r.success,
                        "user_satisfaction": r.user_satisfaction
                    } for r in self.routing_history
                ], f, indent=2)
            
            # Save model metrics
            metrics_file = self.data_dir / "model_metrics.json"
            with open(metrics_file, 'w') as f:
                json.dump({
                    model: {
                        "model_name": metrics.model_name,
                        "total_requests": metrics.total_requests,
                        "successful_requests": metrics.successful_requests,
                        "average_confidence": metrics.average_confidence,
                        "average_response_time": metrics.average_response_time,
                        "average_quality": metrics.average_quality,
                        "task_distribution": metrics.task_distribution,
                        "recent_performance": metrics.recent_performance
                    } for model, metrics in self.model_metrics.items()
                }, f, indent=2)
            
            logger.debug("Router performance data saved")
            
        except Exception as e:
            logger.error(f"Failed to save router performance data: {e}")
    
    def _load_historical_data(self):
        """Load historical performance data"""
        try:
            # Load routing history
            history_file = self.data_dir / "routing_history.json"
            if history_file.exists():
                with open(history_file, 'r') as f:
                    data = json.load(f)
                    self.routing_history = [
                        RoutingDecisionRecord(
                            timestamp=r["timestamp"],
                            request=r["request"],
                            selected_model=r["selected_model"],
                            task_type=r["task_type"],
                            confidence=r["confidence"],
                            reasoning=r["reasoning"],
                            response_quality=r.get("response_quality"),
                            response_time=r.get("response_time"),
                            success=r.get("success"),
                            user_satisfaction=r.get("user_satisfaction")
                        ) for r in data
                    ]
            
            # Load model metrics
            metrics_file = self.data_dir / "model_metrics.json"
            if metrics_file.exists():
                with open(metrics_file, 'r') as f:
                    data = json.load(f)
                    for model, metrics_data in data.items():
                        self.model_metrics[model] = ModelPerformanceMetrics(
                            model_name=metrics_data["model_name"],
                            total_requests=metrics_data["total_requests"],
                            successful_requests=metrics_data["successful_requests"],
                            average_confidence=metrics_data["average_confidence"],
                            average_response_time=metrics_data["average_response_time"],
                            average_quality=metrics_data["average_quality"],
                            task_distribution=metrics_data["task_distribution"],
                            recent_performance=metrics_data["recent_performance"]
                        )
            
            logger.info(f"Loaded {len(self.routing_history)} historical routing decisions")
            
        except Exception as e:
            logger.error(f"Failed to load historical data: {e}")


# Convenience functions
def create_router_monitor() -> RouterPerformanceMonitor:
    """Create a router performance monitor"""
    return RouterPerformanceMonitor()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Example usage
    monitor = create_router_monitor()
    
    # Simulate some routing decisions
    monitor.record_routing_decision(
        "Find similar documents", "embeddinggemma:300m", "similarity", 0.95, "Best for similarity tasks"
    )
    monitor.record_routing_decision(
        "Write Python function", "qwen2.5-coder:latest", "code_generation", 0.98, "Best for coding tasks"
    )
    
    # Analyze performance
    analysis = monitor.analyze_performance()
    print("Performance Analysis:")
    print(json.dumps(analysis, indent=2))
    
    # Generate suggestions
    suggestions = monitor.generate_optimization_suggestions()
    print(f"\nGenerated {len(suggestions)} optimization suggestions")
    for suggestion in suggestions:
        print(f"- {suggestion.description} (Priority: {suggestion.priority})")
