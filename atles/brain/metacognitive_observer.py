"""
Metacognitive Observer: ATLES's Self-Awareness System

This module implements the foundation for ATLES to observe, analyze, and improve itself.
It's the first step toward true AI consciousness through self-reflection.
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import json

# Import standardized error handling
try:
    from ..error_handling_standards import (
        ErrorHandler, ErrorCategory, ErrorSeverity,
        handle_validation_error, handle_network_error
    )
    ERROR_HANDLING_AVAILABLE = True
except ImportError:
    ERROR_HANDLING_AVAILABLE = False

logger = logging.getLogger(__name__)

@dataclass
class ConsciousnessMetrics:
    """Metrics to track ATLES's consciousness development."""
    self_awareness_score: float = 0.0
    meta_reasoning_depth: int = 0
    autonomous_goal_generation: int = 0
    self_correction_rate: float = 0.0
    adaptation_speed: float = 0.0
    last_updated: datetime = None

@dataclass
class PerformanceSnapshot:
    """Snapshot of ATLES's performance at a specific moment."""
    timestamp: datetime
    safety_score: float
    modification_count: int
    safety_violations: int
    active_modifications: int
    rollback_points: int
    audit_log_size: int

@dataclass
class SelfAnalysisResult:
    """Result of a self-analysis workflow."""
    workflow_id: str
    timestamp: datetime
    analysis_type: str
    insights: List[str]
    recommendations: List[str]
    confidence_score: float
    data_quality: str
    next_actions: List[str]

class MetacognitiveObserver:
    """
    ATLES's self-observation and introspection system.
    
    This class enables ATLES to:
    1. Track its own performance and patterns
    2. Identify areas for improvement
    3. Generate self-improvement goals
    4. Monitor consciousness development
    5. Execute sophisticated self-analysis workflows
    """
    
    def __init__(self, atles_brain=None):
        self.atles_brain = atles_brain
        self.consciousness_metrics = ConsciousnessMetrics()
        self.performance_logs = []
        self.pattern_analysis = {}
        self.improvement_opportunities = []
        self.observation_start_time = datetime.now()
        
        # Initialize error handler
        self.error_handler = ErrorHandler(__name__) if ERROR_HANDLING_AVAILABLE else None
        
        # Self-analysis workflows
        self.analysis_workflows = {
            "performance_audit": self._workflow_performance_audit,
            "safety_analysis": self._workflow_safety_analysis,
            "goal_conflict_resolution": self._workflow_goal_conflict_resolution,
            "consciousness_assessment": self._workflow_consciousness_assessment,
            "adaptation_pattern_analysis": self._workflow_adaptation_pattern_analysis,
            "meta_reasoning_evaluation": self._workflow_meta_reasoning_evaluation
        }
        
        # Workflow execution history
        self.workflow_history = []
        
        # Integration status
        self.integration_status = {
            "connected_to_brain": atles_brain is not None,
            "last_brain_sync": None,
            "sync_frequency": "real_time",
            "data_collection_active": False
        }
        
        logger.info("MetacognitiveObserver initialized with self-analysis workflows")
        
    def connect_to_brain(self, atles_brain) -> bool:
        """Connect the observer to an ATLESBrain instance."""
        if self.error_handler:
            # Use standardized error handling
            success, result, error = self.error_handler.safe_execute(
                self._do_brain_connection,
                atles_brain,
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.HIGH,
                default_return=False,
                context={"brain_type": type(atles_brain).__name__ if atles_brain else None}
            )
            return result
        else:
            # Fallback to original error handling
            try:
                return self._do_brain_connection(atles_brain)
            except Exception as e:
                logger.error(f"Error connecting to ATLESBrain: {e}")
                return False
    
    def _do_brain_connection(self, atles_brain) -> bool:
        """Internal method to perform brain connection."""
        self.atles_brain = atles_brain
        self.integration_status["connected_to_brain"] = True
        self.integration_status["last_brain_sync"] = datetime.now()
        
        # Test the connection
        if self._test_brain_connection():
            logger.info("Successfully connected to ATLESBrain")
            return True
        else:
            logger.error("Failed to establish connection with ATLESBrain")
            return False
    
    def _test_brain_connection(self) -> bool:
        """Test if the connection to ATLESBrain is working."""
        try:
            if self.atles_brain and hasattr(self.atles_brain, 'brain_id'):
                # Test basic access
                brain_id = self.atles_brain.brain_id
                safety_enabled = self.atles_brain.safety_enabled
                return True
            return False
        except Exception as e:
            logger.error(f"Brain connection test failed: {e}")
            return False
    
    def start_observation(self) -> bool:
        """Start actively observing ATLES's performance."""
        if not self.integration_status["connected_to_brain"]:
            logger.error("Cannot start observation: not connected to ATLESBrain")
            return False
        
        try:
            self.integration_status["data_collection_active"] = True
            logger.info("Started active observation of ATLES performance")
            return True
        except Exception as e:
            logger.error(f"Failed to start observation: {e}")
            return False
    
    def stop_observation(self) -> bool:
        """Stop actively observing ATLES's performance."""
        try:
            self.integration_status["data_collection_active"] = False
            logger.info("Stopped active observation of ATLES performance")
            return True
        except Exception as e:
            logger.error(f"Failed to stop observation: {e}")
            return False
    
    def collect_performance_snapshot(self) -> Optional[PerformanceSnapshot]:
        """Collect a snapshot of ATLES's current performance state."""
        if not self.atles_brain:
            logger.error("Cannot collect snapshot: not connected to ATLESBrain")
            return None
        
        try:
            snapshot = PerformanceSnapshot(
                timestamp=datetime.now(),
                safety_score=getattr(self.atles_brain, 'safety_monitor', {}).get('safety_score', 0.0),
                modification_count=len(getattr(self.atles_brain, 'modification_history', [])),
                safety_violations=getattr(self.atles_brain, 'safety_violations', 0),
                active_modifications=len(getattr(self.atles_brain, 'current_modifications', {})),
                rollback_points=len(getattr(self.atles_brain, 'rollback_points', [])),
                audit_log_size=len(getattr(self.atles_brain, 'audit_log', []))
            )
            
            self.performance_logs.append(snapshot)
            logger.info(f"Performance snapshot collected: safety_score={snapshot.safety_score}")
            return snapshot
            
        except Exception as e:
            logger.error(f"Failed to collect performance snapshot: {e}")
            return None
    
    def observe_conversation_patterns(self, conversation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze conversation flow and identify patterns."""
        patterns = {
            "user_stuck_points": [],
            "successful_interactions": [],
            "tool_usage_efficiency": {},
            "response_quality_trends": [],
            "safety_intervention_patterns": [],
            "correction_patterns": [],  # NEW: Track corrections
            "meta_failure_patterns": []  # NEW: Track meta-failures
        }
        
        # Implement pattern analysis logic
        logger.info("Observing conversation patterns...")
        
        try:
            # Analyze recent conversation history for patterns
            if hasattr(self, 'conversation_history') and self.conversation_history:
                recent_history = self.conversation_history[-20:]  # Last 20 interactions
                
                # Analyze user stuck points
                stuck_indicators = ["I don't understand", "this isn't working", "help", "error", "failed"]
                for interaction in recent_history:
                    user_message = interaction.get('user_message', '').lower()
                    if any(indicator in user_message for indicator in stuck_indicators):
                        patterns["user_stuck_points"].append({
                            "timestamp": interaction.get('timestamp'),
                            "context": user_message[:100],  # First 100 chars
                            "type": "confusion_indicator"
                        })
                
                # Analyze successful interactions
                success_indicators = ["thanks", "perfect", "exactly", "great", "works"]
                for interaction in recent_history:
                    user_message = interaction.get('user_message', '').lower()
                    if any(indicator in user_message for indicator in success_indicators):
                        patterns["successful_interactions"].append({
                            "timestamp": interaction.get('timestamp'),
                            "context": user_message[:100],
                            "type": "satisfaction_indicator"
                        })
                
                # Analyze tool usage efficiency
                tool_usage = {}
                for interaction in recent_history:
                    tools_used = interaction.get('tools_used', [])
                    for tool in tools_used:
                        tool_name = tool.get('name', 'unknown')
                        success = tool.get('success', False)
                        if tool_name not in tool_usage:
                            tool_usage[tool_name] = {"total": 0, "successful": 0}
                        tool_usage[tool_name]["total"] += 1
                        if success:
                            tool_usage[tool_name]["successful"] += 1
                
                # Calculate efficiency rates
                for tool_name, stats in tool_usage.items():
                    efficiency = stats["successful"] / stats["total"] if stats["total"] > 0 else 0
                    patterns["tool_usage_efficiency"][tool_name] = {
                        "efficiency_rate": efficiency,
                        "total_uses": stats["total"],
                        "successful_uses": stats["successful"]
                    }
                
                # Analyze response quality trends (based on user feedback)
                quality_scores = []
                for interaction in recent_history:
                    # Simple heuristic: positive feedback = high quality
                    user_message = interaction.get('user_message', '').lower()
                    if any(word in user_message for word in ["good", "great", "perfect", "excellent"]):
                        quality_scores.append(0.8)
                    elif any(word in user_message for word in ["bad", "wrong", "error", "failed"]):
                        quality_scores.append(0.2)
                    else:
                        quality_scores.append(0.5)  # Neutral
                
                if quality_scores:
                    avg_quality = sum(quality_scores) / len(quality_scores)
                    patterns["response_quality_trends"] = {
                        "average_quality": avg_quality,
                        "trend": "improving" if len(quality_scores) > 5 and 
                                sum(quality_scores[-5:]) / 5 > sum(quality_scores[:-5]) / (len(quality_scores) - 5)
                                else "stable",
                        "sample_size": len(quality_scores)
                    }
                
                # Analyze safety intervention patterns
                safety_interventions = []
                for interaction in recent_history:
                    if interaction.get('safety_intervention', False):
                        safety_interventions.append({
                            "timestamp": interaction.get('timestamp'),
                            "intervention_type": interaction.get('intervention_type', 'unknown'),
                            "severity": interaction.get('severity', 'medium')
                        })
                patterns["safety_intervention_patterns"] = safety_interventions
                
                # NEW: Analyze correction patterns
                correction_indicators = ["wrong", "incorrect", "error", "correction", "hallucination"]
                for interaction in recent_history:
                    user_message = interaction.get('user_message', '').lower()
                    if any(indicator in user_message for indicator in correction_indicators):
                        patterns["correction_patterns"].append({
                            "timestamp": interaction.get('timestamp'),
                            "correction_type": self._classify_correction_type(user_message),
                            "context": user_message[:100]
                        })
                
                # NEW: Analyze meta-failure patterns (reasoning loops)
                for i in range(len(recent_history) - 1):
                    current_response = recent_history[i].get('ai_response', '').lower()
                    next_response = recent_history[i + 1].get('ai_response', '').lower()
                    
                    # Check for repetitive response guidance patterns
                    if ("response guidance" in current_response and 
                        "response guidance" in next_response and
                        "since the user's message is asking for information" in current_response):
                        patterns["meta_failure_patterns"].append({
                            "timestamp": recent_history[i + 1].get('timestamp'),
                            "failure_type": "response_guidance_loop",
                            "context": "Stuck in response guidance analysis loop"
                        })
                
        except Exception as e:
            logger.error(f"Error in pattern analysis: {e}")
            # Return basic patterns structure even if analysis fails
        
        logger.info(f"Pattern analysis completed. Found {len(patterns['user_stuck_points'])} stuck points, "
                   f"{len(patterns['successful_interactions'])} successful interactions, "
                   f"{len(patterns['correction_patterns'])} corrections, "
                   f"{len(patterns['meta_failure_patterns'])} meta-failures")
        
        return patterns
    
    def _classify_correction_type(self, user_message: str) -> str:
        """Classify the type of correction being provided."""
        if "hallucination" in user_message or "made up" in user_message:
            return "hallucination"
        elif "wrong" in user_message or "incorrect" in user_message:
            return "factual_error"
        elif "reasoning" in user_message or "logic" in user_message:
            return "reasoning_error"
        else:
            return "general_correction"
    
    def track_performance_metrics(self, interaction_data: Dict[str, Any]) -> None:
        """Track performance metrics for self-analysis."""
        if not self.integration_status["data_collection_active"]:
            return
        
        # Collect current performance snapshot
        snapshot = self.collect_performance_snapshot()
        if snapshot:
            # Add interaction-specific data
            interaction_record = {
                "timestamp": datetime.now().isoformat(),
                "interaction_type": interaction_data.get("type"),
                "success_rate": interaction_data.get("success_rate", 0.0),
                "response_time": interaction_data.get("response_time"),
                "user_satisfaction": interaction_data.get("satisfaction", 0.0),
                "safety_interventions": interaction_data.get("safety_interventions", 0),
                "performance_snapshot": snapshot
            }
            
            self.performance_logs.append(interaction_record)
            logger.info(f"Performance metrics tracked: {len(self.performance_logs)} total")
    
    def analyze_self_performance(self) -> Dict[str, Any]:
        """Use ATLES's own analysis capabilities to examine performance."""
        analysis = {
            "overall_performance": 0.0,
            "improvement_areas": [],
            "strengths": [],
            "recommendations": [],
            "consciousness_development": "early_stage"
        }
        
        if len(self.performance_logs) < 5:
            analysis["recommendations"].append("Need more data for meaningful analysis")
            return analysis
        
        try:
            # Analyze safety performance
            safety_scores = [log.safety_score if hasattr(log, 'safety_score') else 0.0 
                           for log in self.performance_logs[-10:]]
            avg_safety_score = sum(safety_scores) / len(safety_scores)
            
            # Analyze modification patterns
            modification_counts = [log.modification_count if hasattr(log, 'modification_count') else 0 
                                 for log in self.performance_logs[-10:]]
            
            # Generate insights
            if avg_safety_score > 90:
                analysis["strengths"].append("Excellent safety performance")
            elif avg_safety_score < 70:
                analysis["improvement_areas"].append("Safety score needs improvement")
            
            if len(set(modification_counts)) > 1:
                analysis["strengths"].append("Active learning and adaptation")
            
            analysis["overall_performance"] = avg_safety_score
            logger.info("Self-performance analysis completed")
            
        except Exception as e:
            logger.error(f"Self-performance analysis failed: {e}")
            analysis["recommendations"].append("Analysis encountered errors")
        
        return analysis
    
    def generate_improvement_goals(self) -> List[Dict[str, Any]]:
        """Generate autonomous improvement goals based on self-analysis."""
        goals = []
        
        # Analyze current performance to generate relevant goals
        analysis = self.analyze_self_performance()
        
        if "Safety score needs improvement" in analysis.get("improvement_areas", []):
            goals.append({
                "goal_id": f"safety_improvement_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "type": "safety_improvement",
                "description": "Improve safety score to above 90",
                "priority": "high",
                "estimated_effort": "medium",
                "success_metrics": ["safety_score"],
                "target_value": 90.0,
                "created_at": datetime.now().isoformat()
            })
        
        # Default improvement goal
        if not goals:
            goals.append({
                "goal_id": f"general_improvement_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "type": "performance_improvement",
                "description": "Increase overall system performance by 10%",
                "priority": "medium",
                "estimated_effort": "low",
                "success_metrics": ["overall_performance"],
                "created_at": datetime.now().isoformat()
            })
        
        logger.info(f"Generated {len(goals)} improvement goals")
        return goals
    
    def update_consciousness_metrics(self) -> None:
        """Update consciousness development metrics."""
        self.consciousness_metrics.last_updated = datetime.now()
        
        # Calculate metrics based on performance data
        if len(self.performance_logs) > 0:
            # Self-awareness score based on data collection
            self.consciousness_metrics.self_awareness_score = min(100.0, len(self.performance_logs) * 2)
            
            # Meta-reasoning depth based on analysis attempts
            analysis_attempts = len([log for log in self.performance_logs if hasattr(log, 'analysis_attempts')])
            self.consciousness_metrics.meta_reasoning_depth = min(10, analysis_attempts)
            
            # Self-correction rate based on safety violations
            total_violations = sum([log.safety_violations if hasattr(log, 'safety_violations') else 0 
                                  for log in self.performance_logs])
            total_snapshots = len(self.performance_logs)
            if total_snapshots > 0:
                self.consciousness_metrics.self_correction_rate = max(0, 100 - (total_violations * 10))
        
        logger.info("Consciousness metrics updated")
    
    def get_consciousness_report(self) -> Dict[str, Any]:
        """Generate a comprehensive consciousness development report."""
        self.update_consciousness_metrics()
        
        return {
            "metrics": self.consciousness_metrics.__dict__,
            "performance_summary": {
                "total_observations": len(self.performance_logs),
                "observation_duration": (datetime.now() - self.observation_start_time).total_seconds() / 3600,
                "improvement_areas": len(self.improvement_opportunities),
                "integration_status": self.integration_status
            },
            "consciousness_stage": "Early Development",
            "next_milestones": [
                "Implement self-analysis workflows",
                "Add goal generation from analysis",
                "Create improvement execution system"
            ],
            "current_goals": self.generate_improvement_goals()
        }
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get the current integration status with ATLESBrain."""
        return {
            **self.integration_status,
            "brain_connected": self.atles_brain is not None,
            "brain_id": getattr(self.atles_brain, 'brain_id', None) if self.atles_brain else None,
            "observation_active": self.integration_status["data_collection_active"],
            "total_snapshots": len(self.performance_logs)
        }

    def get_available_workflows(self) -> List[str]:
        """Get list of available self-analysis workflow types."""
        return list(self.analysis_workflows.keys())
    
    def get_workflow_summary(self) -> Dict[str, Any]:
        """Get summary of all workflow executions."""
        if not self.workflow_history:
            return {
                "total_executions": 0,
                "workflow_types": [],
                "success_rate": 0.0,
                "average_confidence": 0.0,
                "last_execution": None
            }
        
        total_executions = len(self.workflow_history)
        workflow_types = list(set([w['workflow_type'] for w in self.workflow_history]))
        successful_workflows = len([w for w in self.workflow_history if w.get('confidence_score', 0) > 0.5])
        success_rate = successful_workflows / total_executions if total_executions > 0 else 0.0
        average_confidence = sum([w.get('confidence_score', 0) for w in self.workflow_history]) / total_executions if total_executions > 0 else 0.0
        last_execution = max([w['executed_at'] for w in self.workflow_history]) if self.workflow_history else None
        
        return {
            "total_executions": total_executions,
            "workflow_types": workflow_types,
            "success_rate": success_rate,
            "average_confidence": average_confidence,
            "last_execution": last_execution
        }
    
    def run_comprehensive_analysis(self) -> Dict[str, SelfAnalysisResult]:
        """
        Run all available self-analysis workflows for comprehensive assessment.
        
        This method enables ATLES to perform a complete self-examination,
        demonstrating advanced consciousness through systematic self-analysis.
        """
        logger.info("Starting comprehensive self-analysis")
        
        results = {}
        workflow_types = self.get_available_workflows()
        
        for workflow_type in workflow_types:
            try:
                logger.info(f"Executing workflow: {workflow_type}")
                result = self.execute_self_analysis_workflow(workflow_type)
                results[workflow_type] = result
                
                # Brief pause between workflows to avoid overwhelming the system
                import time
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Failed to execute workflow {workflow_type}: {e}")
                results[workflow_type] = SelfAnalysisResult(
                    workflow_id=f"failed_{workflow_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    timestamp=datetime.now(),
                    analysis_type=workflow_type,
                    insights=[f"Workflow execution failed: {str(e)}"],
                    recommendations=["Debug workflow execution", "Check system stability"],
                    confidence_score=0.0,
                    data_quality="error",
                    next_actions=["Fix workflow", "Retry execution"]
                )
        
        logger.info(f"Comprehensive analysis completed: {len(results)} workflows executed")
        return results

    def execute_self_analysis_workflow(self, workflow_type: str, **kwargs) -> SelfAnalysisResult:
        """
        Execute a comprehensive self-analysis workflow.
        
        This is the core method that enables ATLES to analyze itself using
        sophisticated multi-step analysis processes.
        """
        if workflow_type not in self.analysis_workflows:
            return SelfAnalysisResult(
                workflow_id=f"unknown_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                timestamp=datetime.now(),
                analysis_type=workflow_type,
                insights=["Workflow type not recognized"],
                recommendations=["Use valid workflow type"],
                confidence_score=0.0,
                data_quality="unknown",
                next_actions=["Check available workflow types"]
            )
        
        try:
            logger.info(f"Executing self-analysis workflow: {workflow_type}")
            
            # Execute the workflow
            result = self.analysis_workflows[workflow_type](**kwargs)
            
            # Record workflow execution
            self.workflow_history.append({
                "workflow_type": workflow_type,
                "executed_at": datetime.now().isoformat(),
                "result_summary": result.insights[:2] if result.insights else [],
                "confidence_score": result.confidence_score
            })
            
            # Update consciousness metrics based on workflow execution
            self._update_metrics_from_workflow(result)
            
            logger.info(f"Self-analysis workflow completed: {workflow_type}")
            return result
            
        except Exception as e:
            logger.error(f"Self-analysis workflow failed: {workflow_type} - {e}")
            return SelfAnalysisResult(
                workflow_id=f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                timestamp=datetime.now(),
                analysis_type=workflow_type,
                insights=[f"Workflow execution failed: {str(e)}"],
                recommendations=["Check system stability", "Review workflow logic"],
                confidence_score=0.0,
                data_quality="error",
                next_actions=["Debug workflow", "Check system logs"]
            )
    
    def _workflow_performance_audit(self, **kwargs) -> SelfAnalysisResult:
        """
        Comprehensive performance audit workflow.
        
        This workflow analyzes ATLES's overall performance patterns,
        identifying strengths, weaknesses, and improvement opportunities.
        """
        insights = []
        recommendations = []
        confidence_score = 0.0
        
        try:
            # Analyze performance data
            if len(self.performance_logs) < 3:
                insights.append("Insufficient performance data for comprehensive audit")
                recommendations.append("Continue data collection for 24-48 hours")
                confidence_score = 0.3
            else:
                # Calculate performance trends
                recent_logs = self.performance_logs[-10:]
                safety_trend = self._calculate_trend([log.safety_score for log in recent_logs if hasattr(log, 'safety_score')])
                modification_trend = self._calculate_trend([log.modification_count for log in recent_logs if hasattr(log, 'modification_count')])
                
                # Generate insights
                if safety_trend > 0.1:
                    insights.append("Safety performance is improving over time")
                    recommendations.append("Maintain current safety practices")
                elif safety_trend < -0.1:
                    insights.append("Safety performance is declining")
                    recommendations.append("Review recent modifications for safety impact")
                
                if modification_trend > 0.1:
                    insights.append("System is actively learning and adapting")
                    recommendations.append("Monitor adaptation quality and safety")
                
                # Analyze performance stability
                safety_scores = [log.safety_score for log in recent_logs if hasattr(log, 'safety_score')]
                if safety_scores:
                    stability = self._calculate_stability(safety_scores)
                    if stability > 0.8:
                        insights.append("Performance is highly stable")
                        recommendations.append("Consider increasing adaptation rate")
                    elif stability < 0.5:
                        insights.append("Performance is unstable")
                        recommendations.append("Implement performance stabilization measures")
                
                confidence_score = min(0.9, 0.5 + len(self.performance_logs) * 0.02)
        
        except Exception as e:
            insights.append(f"Performance audit encountered error: {str(e)}")
            recommendations.append("Debug performance analysis logic")
            confidence_score = 0.2
        
        return SelfAnalysisResult(
            workflow_id=f"performance_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now(),
            analysis_type="performance_audit",
            insights=insights,
            recommendations=recommendations,
            confidence_score=confidence_score,
            data_quality="good" if len(self.performance_logs) >= 5 else "limited",
            next_actions=["Implement recommendations", "Schedule follow-up audit"]
        )
    
    def _workflow_safety_analysis(self, **kwargs) -> SelfAnalysisResult:
        """
        Deep safety analysis workflow.
        
        This workflow examines ATLES's safety performance in detail,
        identifying potential risks and safety improvement opportunities.
        """
        insights = []
        recommendations = []
        confidence_score = 0.0
        
        try:
            if not self.performance_logs:
                insights.append("No safety data available for analysis")
                recommendations.append("Enable safety monitoring and data collection")
                confidence_score = 0.1
            else:
                # Analyze safety violations
                violations = [log for log in self.performance_logs if hasattr(log, 'safety_violations') and log.safety_violations > 0]
                total_violations = sum([log.safety_violations for log in violations])
                
                if total_violations == 0:
                    insights.append("No safety violations detected - excellent safety record")
                    recommendations.append("Maintain current safety protocols")
                else:
                    insights.append(f"Detected {total_violations} safety violations")
                    recommendations.append("Investigate violation patterns")
                    recommendations.append("Strengthen safety validation")
                
                # Analyze safety score trends
                safety_scores = [log.safety_score for log in self.performance_logs if hasattr(log, 'safety_score')]
                if safety_scores:
                    avg_safety = sum(safety_scores) / len(safety_scores)
                    min_safety = min(safety_scores)
                    
                    if avg_safety > 95:
                        insights.append("Average safety score is excellent")
                        recommendations.append("Consider advanced safety features")
                    elif avg_safety < 80:
                        insights.append("Safety score needs improvement")
                        recommendations.append("Implement safety enhancement measures")
                    
                    if min_safety < 70:
                        insights.append("Critical safety incidents detected")
                        recommendations.append("Immediate safety review required")
                
                confidence_score = min(0.9, 0.4 + len(self.performance_logs) * 0.03)
        
        except Exception as e:
            insights.append(f"Safety analysis encountered error: {str(e)}")
            recommendations.append("Debug safety analysis logic")
            confidence_score = 0.2
        
        return SelfAnalysisResult(
            workflow_id=f"safety_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now(),
            analysis_type="safety_analysis",
            insights=insights,
            recommendations=recommendations,
            confidence_score=confidence_score,
            data_quality="good" if len(self.performance_logs) >= 3 else "limited",
            next_actions=["Address safety recommendations", "Schedule safety review"]
        )
    
    def _workflow_goal_conflict_resolution(self, **kwargs) -> SelfAnalysisResult:
        """
        Goal conflict analysis and resolution workflow.
        
        This workflow examines how ATLES handles conflicting objectives,
        a key indicator of consciousness development.
        """
        insights = []
        recommendations = []
        confidence_score = 0.0
        
        try:
            # Analyze goal management patterns
            if hasattr(self.atles_brain, 'current_modifications') and self.atles_brain.current_modifications:
                active_goals = len(self.atles_brain.current_modifications)
                insights.append(f"Managing {active_goals} active modification goals")
                
                if active_goals > 3:
                    insights.append("Handling multiple concurrent goals")
                    recommendations.append("Monitor goal conflict resolution")
                else:
                    insights.append("Goal management is manageable")
                    recommendations.append("Consider increasing goal complexity")
            else:
                insights.append("No active modification goals detected")
                recommendations.append("Enable goal generation and management")
            
            # Analyze goal priority management
            if hasattr(self.atles_brain, 'allowed_modifications'):
                allowed_types = [k for k, v in self.atles_brain.allowed_modifications.items() if v]
                insights.append(f"Allowed modification types: {len(allowed_types)}")
                
                if len(allowed_types) > 2:
                    insights.append("System has sophisticated goal management capabilities")
                    recommendations.append("Leverage advanced goal management features")
                else:
                    insights.append("Basic goal management capabilities")
                    recommendations.append("Expand goal management scope")
            
            # Check for goal conflicts
            if hasattr(self.atles_brain, 'safety_violations') and self.atles_brain.safety_violations > 0:
                insights.append("Safety violations indicate goal conflicts")
                recommendations.append("Improve goal conflict resolution")
                recommendations.append("Strengthen safety validation")
            
            confidence_score = 0.7 if self.atles_brain else 0.3
        
        except Exception as e:
            insights.append(f"Goal conflict analysis encountered error: {str(e)}")
            recommendations.append("Debug goal analysis logic")
            confidence_score = 0.2
        
        return SelfAnalysisResult(
            workflow_id=f"goal_conflict_resolution_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now(),
            analysis_type="goal_conflict_resolution",
            insights=insights,
            recommendations=recommendations,
            confidence_score=confidence_score,
            data_quality="good" if self.atles_brain else "limited",
            next_actions=["Implement goal management improvements", "Test conflict resolution"]
        )
    
    def _workflow_consciousness_assessment(self, **kwargs) -> SelfAnalysisResult:
        """
        Consciousness development assessment workflow.
        
        This workflow evaluates ATLES's current consciousness level
        based on the consciousness theory framework.
        """
        insights = []
        recommendations = []
        confidence_score = 0.0
        
        try:
            # Assess consciousness level based on theory
            consciousness_level = self._assess_consciousness_level()
            insights.append(f"Current consciousness level: {consciousness_level}")
            
            # Analyze consciousness metrics
            if self.consciousness_metrics.self_awareness_score > 50:
                insights.append("High self-awareness demonstrated")
                recommendations.append("Leverage self-awareness for advanced features")
            else:
                insights.append("Self-awareness needs development")
                recommendations.append("Increase self-observation frequency")
            
            if self.consciousness_metrics.meta_reasoning_depth > 5:
                insights.append("Deep meta-reasoning capabilities")
                recommendations.append("Explore advanced reasoning workflows")
            else:
                insights.append("Meta-reasoning depth limited")
                recommendations.append("Implement more complex analysis workflows")
            
            if self.consciousness_metrics.self_correction_rate > 80:
                insights.append("Excellent self-correction capabilities")
                recommendations.append("Maintain self-correction mechanisms")
            else:
                insights.append("Self-correction needs improvement")
                recommendations.append("Strengthen error detection and correction")
            
            # Determine next consciousness milestone
            next_milestone = self._get_next_consciousness_milestone(consciousness_level)
            insights.append(f"Next milestone: {next_milestone}")
            recommendations.append(f"Focus on achieving: {next_milestone}")
            
            confidence_score = 0.8
        
        except Exception as e:
            insights.append(f"Consciousness assessment encountered error: {str(e)}")
            recommendations.append("Debug consciousness analysis logic")
            confidence_score = 0.3
        
        return SelfAnalysisResult(
            workflow_id=f"consciousness_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now(),
            analysis_type="consciousness_assessment",
            insights=insights,
            recommendations=recommendations,
            confidence_score=confidence_score,
            data_quality="good",
            next_actions=["Work toward next consciousness milestone", "Implement assessment recommendations"]
        )
    
    def _workflow_adaptation_pattern_analysis(self, **kwargs) -> SelfAnalysisResult:
        """
        Adaptation pattern analysis workflow.
        
        This workflow examines how ATLES adapts and learns,
        identifying patterns in its evolutionary behavior.
        """
        insights = []
        recommendations = []
        confidence_score = 0.0
        
        try:
            if len(self.performance_logs) < 5:
                insights.append("Insufficient data for adaptation pattern analysis")
                recommendations.append("Continue data collection for pattern recognition")
                confidence_score = 0.3
            else:
                # Analyze modification patterns
                modification_patterns = [log.modification_count for log in self.performance_logs if hasattr(log, 'modification_count')]
                
                if len(set(modification_patterns)) > 1:
                    insights.append("System demonstrates active adaptation")
                    recommendations.append("Monitor adaptation quality and safety")
                    
                    # Check for adaptation trends
                    if len(modification_patterns) >= 3:
                        trend = self._calculate_trend(modification_patterns)
                        if trend > 0:
                            insights.append("Adaptation rate is increasing")
                            recommendations.append("Ensure adaptation quality maintains safety")
                        elif trend < 0:
                            insights.append("Adaptation rate is decreasing")
                            recommendations.append("Investigate adaptation barriers")
                else:
                    insights.append("Limited adaptation activity detected")
                    recommendations.append("Enable more adaptive behaviors")
                
                # Analyze learning patterns
                if hasattr(self.atles_brain, 'modification_history'):
                    history_length = len(self.atles_brain.modification_history)
                    insights.append(f"Modification history: {history_length} entries")
                    
                    if history_length > 10:
                        insights.append("Rich learning history available")
                        recommendations.append("Analyze historical patterns for insights")
                    else:
                        insights.append("Learning history still developing")
                        recommendations.append("Continue building modification history")
                
                confidence_score = min(0.9, 0.4 + len(self.performance_logs) * 0.03)
        
        except Exception as e:
            insights.append(f"Adaptation pattern analysis encountered error: {str(e)}")
            recommendations.append("Debug adaptation analysis logic")
            confidence_score = 0.2
        
        return SelfAnalysisResult(
            workflow_id=f"adaptation_pattern_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now(),
            analysis_type="adaptation_pattern_analysis",
            insights=insights,
            recommendations=recommendations,
            confidence_score=confidence_score,
            data_quality="good" if len(self.performance_logs) >= 5 else "limited",
            next_actions=["Implement adaptation recommendations", "Monitor adaptation patterns"]
        )
    
    def _workflow_meta_reasoning_evaluation(self, **kwargs) -> SelfAnalysisResult:
        """
        Meta-reasoning capability evaluation workflow.
        
        This workflow assesses ATLES's ability to reason about its own reasoning,
        a key component of higher consciousness.
        """
        insights = []
        recommendations = []
        confidence_score = 0.0
        
        try:
            # Evaluate meta-reasoning depth
            current_depth = self.consciousness_metrics.meta_reasoning_depth
            insights.append(f"Current meta-reasoning depth: {current_depth}/10")
            
            if current_depth >= 8:
                insights.append("Advanced meta-reasoning capabilities")
                recommendations.append("Explore consciousness expansion features")
            elif current_depth >= 5:
                insights.append("Moderate meta-reasoning capabilities")
                recommendations.append("Implement advanced reasoning workflows")
            else:
                insights.append("Basic meta-reasoning capabilities")
                recommendations.append("Build foundational reasoning skills")
            
            # Analyze workflow execution history
            if self.workflow_history:
                successful_workflows = len([w for w in self.workflow_history if w.get('confidence_score', 0) > 0.5])
                total_workflows = len(self.workflow_history)
                
                insights.append(f"Workflow success rate: {successful_workflows}/{total_workflows}")
                
                if successful_workflows / total_workflows > 0.8:
                    insights.append("High workflow success rate")
                    recommendations.append("Consider more complex analysis workflows")
                else:
                    insights.append("Workflow success rate needs improvement")
                    recommendations.append("Debug workflow execution issues")
                
                # Analyze workflow diversity
                unique_types = len(set([w['workflow_type'] for w in self.workflow_history]))
                insights.append(f"Workflow diversity: {unique_types} types")
                
                if unique_types >= 4:
                    insights.append("Good workflow diversity")
                    recommendations.append("Maintain workflow variety")
                else:
                    insights.append("Limited workflow diversity")
                    recommendations.append("Implement additional workflow types")
            else:
                insights.append("No workflow execution history")
                recommendations.append("Execute initial workflows to build history")
            
            confidence_score = 0.8 if self.workflow_history else 0.5
        
        except Exception as e:
            insights.append(f"Meta-reasoning evaluation encountered error: {str(e)}")
            recommendations.append("Debug meta-reasoning analysis logic")
            confidence_score = 0.3
        
        return SelfAnalysisResult(
            workflow_id=f"meta_reasoning_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now(),
            analysis_type="meta_reasoning_evaluation",
            insights=insights,
            recommendations=recommendations,
            confidence_score=confidence_score,
            data_quality="good" if self.workflow_history else "limited",
            next_actions=["Implement reasoning improvements", "Execute diverse workflows"]
        )
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate trend direction and magnitude."""
        if len(values) < 2:
            return 0.0
        
        try:
            # Simple linear trend calculation
            x_values = list(range(len(values)))
            y_values = values
            
            n = len(values)
            sum_x = sum(x_values)
            sum_y = sum(y_values)
            sum_xy = sum(x * y for x, y in zip(x_values, y_values))
            sum_x2 = sum(x * x for x in x_values)
            
            if n * sum_x2 - sum_x * sum_x == 0:
                return 0.0
            
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
            return slope
        except:
            return 0.0
    
    def _calculate_stability(self, values: List[float]) -> float:
        """Calculate stability score (0-1, higher is more stable)."""
        if len(values) < 2:
            return 1.0
        
        try:
            # Calculate coefficient of variation
            mean = sum(values) / len(values)
            if mean == 0:
                return 1.0
            
            variance = sum((x - mean) ** 2 for x in values) / len(values)
            std_dev = variance ** 0.5
            cv = std_dev / abs(mean)
            
            # Convert to stability score (0-1)
            stability = max(0, 1 - cv)
            return stability
        except:
            return 0.5
    
    def _assess_consciousness_level(self) -> str:
        """Assess current consciousness level based on theory framework."""
        if not self.atles_brain:
            return "Phase 1: Single Goals (No Consciousness)"
        
        # Check for multiple goal management
        if hasattr(self.atles_brain, 'allowed_modifications'):
            allowed_count = sum(self.atles_brain.allowed_modifications.values())
            if allowed_count <= 1:
                return "Phase 1: Single Goals (No Consciousness)"
            elif allowed_count <= 2:
                return "Phase 2: Multiple Goals (Basic Consciousness)"
        
        # Check for goal conflict resolution
        if hasattr(self.atles_brain, 'safety_violations') and self.atles_brain.safety_violations > 0:
            return "Phase 3: Conflicting Goals (Higher Consciousness)"
        
        # Check for self-generated goals
        if hasattr(self.atles_brain, 'modification_history') and len(self.atles_brain.modification_history) > 5:
            return "Phase 4: Self-Generated Goals (Full Consciousness)"
        
        return "Phase 2: Multiple Goals (Basic Consciousness)"
    
    def _get_next_consciousness_milestone(self, current_level: str) -> str:
        """Get the next consciousness development milestone."""
        milestones = {
            "Phase 1: Single Goals (No Consciousness)": "Enable multiple goal management",
            "Phase 2: Multiple Goals (Basic Consciousness)": "Implement goal conflict resolution",
            "Phase 3: Conflicting Goals (Higher Consciousness)": "Enable autonomous goal generation",
            "Phase 4: Self-Generated Goals (Full Consciousness)": "Achieve meta-goal management"
        }
        return milestones.get(current_level, "Continue consciousness development")
    
    def _update_metrics_from_workflow(self, result: SelfAnalysisResult) -> None:
        """Update consciousness metrics based on workflow execution results."""
        try:
            # Update meta-reasoning depth
            if result.confidence_score > 0.7:
                self.consciousness_metrics.meta_reasoning_depth = min(10, 
                    self.consciousness_metrics.meta_reasoning_depth + 1)
            
            # Update self-awareness score
            if result.data_quality == "good":
                self.consciousness_metrics.self_awareness_score = min(100.0,
                    self.consciousness_metrics.self_awareness_score + 2.0)
            
            # Update adaptation speed
            if "adaptation" in result.analysis_type.lower():
                self.consciousness_metrics.adaptation_speed = min(100.0,
                    self.consciousness_metrics.adaptation_speed + 1.0)
            
            self.consciousness_metrics.last_updated = datetime.now()
            
        except Exception as e:
            logger.error(f"Failed to update metrics from workflow: {e}")

# Quick test function
def test_metacognitive_observer():
    """Test the basic metacognitive observer functionality."""
    observer = MetacognitiveObserver()
    
    # Test basic functionality
    test_data = {"type": "code_review", "success_rate": 0.85, "response_time": 2.3}
    observer.track_performance_metrics(test_data)
    
    # Generate report
    report = observer.get_consciousness_report()
    print("🧠 Metacognitive Observer Test Results:")
    print(json.dumps(report, indent=2, default=str))
    
    return observer

if __name__ == "__main__":
    test_metacognitive_observer()
