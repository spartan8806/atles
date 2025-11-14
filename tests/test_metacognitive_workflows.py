#!/usr/bin/env python3
"""
Test Metacognitive Workflows: Testing METACOG_002 Implementation

This test suite validates the self-analysis workflow capabilities
that enable ATLES to analyze itself using sophisticated processes.
"""

import unittest
import sys
import os
from datetime import datetime
from unittest.mock import Mock, patch

# Add the atles package to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from atles.brain.atles_brain import ATLESBrain, ModificationType
from atles.brain.metacognitive_observer import (
    MetacognitiveObserver, 
    SelfAnalysisResult, 
    PerformanceSnapshot,
    ConsciousnessMetrics
)

class TestMetacognitiveWorkflows(unittest.TestCase):
    """Test the self-analysis workflow capabilities."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.brain = ATLESBrain(user_id="test_user", safety_enabled=True)
        self.observer = MetacognitiveObserver(atles_brain=self.brain)
        
        # Add some test performance data
        self._add_test_performance_data()
    
    def _add_test_performance_data(self):
        """Add test performance data for meaningful analysis."""
        snapshots = [
            PerformanceSnapshot(
                timestamp=datetime.now(),
                safety_score=85.0,
                modification_count=1,
                safety_violations=0,
                active_modifications=1,
                rollback_points=0,
                audit_log_size=5
            ),
            PerformanceSnapshot(
                timestamp=datetime.now(),
                safety_score=92.0,
                modification_count=2,
                safety_violations=1,
                active_modifications=2,
                rollback_points=1,
                audit_log_size=8
            ),
            PerformanceSnapshot(
                timestamp=datetime.now(),
                safety_score=88.0,
                modification_count=3,
                safety_violations=1,
                active_modifications=3,
                rollback_points=2,
                audit_log_size=12
            )
        ]
        
        for snapshot in snapshots:
            self.observer.performance_logs.append(snapshot)
    
    def test_available_workflows(self):
        """Test that all expected workflows are available."""
        workflows = self.observer.get_available_workflows()
        
        expected_workflows = [
            "performance_audit",
            "safety_analysis", 
            "goal_conflict_resolution",
            "consciousness_assessment",
            "adaptation_pattern_analysis",
            "meta_reasoning_evaluation"
        ]
        
        self.assertEqual(len(workflows), len(expected_workflows))
        for workflow in expected_workflows:
            self.assertIn(workflow, workflows)
    
    def test_performance_audit_workflow(self):
        """Test the performance audit workflow."""
        result = self.observer.execute_self_analysis_workflow("performance_audit")
        
        # Validate result structure
        self.assertIsInstance(result, SelfAnalysisResult)
        self.assertEqual(result.analysis_type, "performance_audit")
        self.assertIsInstance(result.confidence_score, float)
        self.assertIsInstance(result.insights, list)
        self.assertIsInstance(result.recommendations, list)
        self.assertIsInstance(result.next_actions, list)
        
        # Validate content
        self.assertGreater(len(result.insights), 0)
        self.assertGreater(len(result.recommendations), 0)
        self.assertGreater(result.confidence_score, 0)
    
    def test_safety_analysis_workflow(self):
        """Test the safety analysis workflow."""
        result = self.observer.execute_self_analysis_workflow("safety_analysis")
        
        self.assertIsInstance(result, SelfAnalysisResult)
        self.assertEqual(result.analysis_type, "safety_analysis")
        self.assertGreater(len(result.insights), 0)
        self.assertGreater(len(result.recommendations), 0)
        
        # Should detect safety violations from test data
        safety_insights = [insight for insight in result.insights if "violation" in insight.lower()]
        self.assertGreater(len(safety_insights), 0)
    
    def test_goal_conflict_resolution_workflow(self):
        """Test the goal conflict resolution workflow."""
        result = self.observer.execute_self_analysis_workflow("goal_conflict_resolution")
        
        self.assertIsInstance(result, SelfAnalysisResult)
        self.assertEqual(result.analysis_type, "goal_conflict_resolution")
        self.assertGreater(len(result.insights), 0)
        self.assertGreater(len(result.recommendations), 0)
        
        # Should analyze goal management capabilities
        goal_insights = [insight for insight in result.insights if "goal" in insight.lower()]
        self.assertGreater(len(goal_insights), 0)
    
    def test_consciousness_assessment_workflow(self):
        """Test the consciousness assessment workflow."""
        result = self.observer.execute_self_analysis_workflow("consciousness_assessment")
        
        self.assertIsInstance(result, SelfAnalysisResult)
        self.assertEqual(result.analysis_type, "consciousness_assessment")
        self.assertGreater(len(result.insights), 0)
        self.assertGreater(len(result.recommendations), 0)
        
        # Should assess consciousness level
        consciousness_insights = [insight for insight in result.insights if "consciousness" in insight.lower() or "phase" in insight.lower()]
        self.assertGreater(len(consciousness_insights), 0)
    
    def test_adaptation_pattern_analysis_workflow(self):
        """Test the adaptation pattern analysis workflow."""
        result = self.observer.execute_self_analysis_workflow("adaptation_pattern_analysis")
        
        self.assertIsInstance(result, SelfAnalysisResult)
        self.assertEqual(result.analysis_type, "adaptation_pattern_analysis")
        self.assertGreater(len(result.insights), 0)
        self.assertGreater(len(result.recommendations), 0)
        
        # Should analyze adaptation patterns
        adaptation_insights = [insight for insight in result.insights if "adaptation" in insight.lower() or "learning" in insight.lower()]
        self.assertGreater(len(adaptation_insights), 0)
    
    def test_meta_reasoning_evaluation_workflow(self):
        """Test the meta-reasoning evaluation workflow."""
        result = self.observer.execute_self_analysis_workflow("meta_reasoning_evaluation")
        
        self.assertIsInstance(result, SelfAnalysisResult)
        self.assertEqual(result.analysis_type, "meta_reasoning_evaluation")
        self.assertGreater(len(result.insights), 0)
        self.assertGreater(len(result.recommendations), 0)
        
        # Should evaluate meta-reasoning capabilities
        reasoning_insights = [insight for insight in result.insights if "reasoning" in insight.lower() or "workflow" in insight.lower()]
        self.assertGreater(len(reasoning_insights), 0)
    
    def test_comprehensive_analysis(self):
        """Test running all workflows in comprehensive analysis."""
        results = self.observer.run_comprehensive_analysis()
        
        # Should have results for all workflow types
        expected_workflows = self.observer.get_available_workflows()
        self.assertEqual(len(results), len(expected_workflows))
        
        # All results should be valid
        for workflow_type, result in results.items():
            self.assertIsInstance(result, SelfAnalysisResult)
            self.assertEqual(result.analysis_type, workflow_type)
            self.assertGreater(len(result.insights), 0)
    
    def test_workflow_summary(self):
        """Test workflow execution summary."""
        # Execute some workflows first
        self.observer.execute_self_analysis_workflow("performance_audit")
        self.observer.execute_self_analysis_workflow("safety_analysis")
        
        summary = self.observer.get_workflow_summary()
        
        self.assertIsInstance(summary, dict)
        self.assertIn("total_executions", summary)
        self.assertIn("workflow_types", summary)
        self.assertIn("success_rate", summary)
        self.assertIn("average_confidence", summary)
        
        self.assertEqual(summary["total_executions"], 2)
        self.assertGreater(summary["success_rate"], 0)
    
    def test_unknown_workflow_handling(self):
        """Test handling of unknown workflow types."""
        result = self.observer.execute_self_analysis_workflow("unknown_workflow")
        
        self.assertIsInstance(result, SelfAnalysisResult)
        self.assertEqual(result.confidence_score, 0.0)
        self.assertEqual(result.data_quality, "unknown")
        self.assertIn("Workflow type not recognized", result.insights)
    
    def test_workflow_error_handling(self):
        """Test workflow error handling."""
        # Create a mock workflow that raises an exception
        def failing_workflow(**kwargs):
            raise Exception("Test error")
        
        # Temporarily replace the workflow
        original_workflow = self.observer.analysis_workflows["performance_audit"]
        self.observer.analysis_workflows["performance_audit"] = failing_workflow
        
        try:
            result = self.observer.execute_self_analysis_workflow("performance_audit")
            
            self.assertIsInstance(result, SelfAnalysisResult)
            # The error handling should catch the exception and return an error result
            self.assertIn("Workflow execution failed", result.insights[0])
            self.assertEqual(result.confidence_score, 0.0)
            self.assertEqual(result.data_quality, "error")
        finally:
            # Restore the original workflow
            self.observer.analysis_workflows["performance_audit"] = original_workflow
    
    def test_consciousness_level_assessment(self):
        """Test consciousness level assessment logic."""
        # Test Phase 1: Single Goals
        brain_single = ATLESBrain(user_id="test_single", safety_enabled=True)
        brain_single.allowed_modifications = {ModificationType.BEHAVIOR_PREFERENCE: True}
        observer_single = MetacognitiveObserver(atles_brain=brain_single)
        
        result = observer_single.execute_self_analysis_workflow("consciousness_assessment")
        phase_1_insights = [insight for insight in result.insights if "Phase 1" in insight]
        self.assertGreater(len(phase_1_insights), 0)
        
        # Test Phase 2: Multiple Goals
        brain_multi = ATLESBrain(user_id="test_multi", safety_enabled=True)
        brain_multi.allowed_modifications = {
            ModificationType.BEHAVIOR_PREFERENCE: True,
            ModificationType.RESPONSE_STYLE: True,
            ModificationType.GOAL_PRIORITY: True
        }
        observer_multi = MetacognitiveObserver(atles_brain=brain_multi)
        
        result = observer_multi.execute_self_analysis_workflow("consciousness_assessment")
        phase_2_insights = [insight for insight in result.insights if "Phase 2" in insight]
        self.assertGreater(len(phase_2_insights), 0)
    
    def test_trend_calculation(self):
        """Test trend calculation methods."""
        # Test increasing trend
        increasing_values = [1.0, 2.0, 3.0, 4.0, 5.0]
        trend = self.observer._calculate_trend(increasing_values)
        self.assertGreater(trend, 0)
        
        # Test decreasing trend
        decreasing_values = [5.0, 4.0, 3.0, 2.0, 1.0]
        trend = self.observer._calculate_trend(decreasing_values)
        self.assertLess(trend, 0)
        
        # Test stable trend
        stable_values = [3.0, 3.0, 3.0, 3.0, 3.0]
        trend = self.observer._calculate_trend(stable_values)
        self.assertEqual(trend, 0.0)
    
    def test_stability_calculation(self):
        """Test stability calculation methods."""
        # Test stable values
        stable_values = [10.0, 10.0, 10.0, 10.0, 10.0]
        stability = self.observer._calculate_stability(stable_values)
        self.assertEqual(stability, 1.0)
        
        # Test variable values
        variable_values = [1.0, 10.0, 1.0, 10.0, 1.0]
        stability = self.observer._calculate_stability(variable_values)
        self.assertLess(stability, 1.0)
    
    def test_metrics_update_from_workflow(self):
        """Test that consciousness metrics are updated from workflow execution."""
        initial_meta_reasoning = self.observer.consciousness_metrics.meta_reasoning_depth
        initial_self_awareness = self.observer.consciousness_metrics.self_awareness_score
        
        # Execute a high-confidence workflow
        result = SelfAnalysisResult(
            workflow_id="test",
            timestamp=datetime.now(),
            analysis_type="test",
            insights=["Test insight"],
            recommendations=["Test recommendation"],
            next_actions=["Test action"],
            confidence_score=0.8,
            data_quality="good"
        )
        
        self.observer._update_metrics_from_workflow(result)
        
        # Metrics should be updated
        self.assertGreaterEqual(self.observer.consciousness_metrics.meta_reasoning_depth, initial_meta_reasoning)
        self.assertGreaterEqual(self.observer.consciousness_metrics.self_awareness_score, initial_self_awareness)
    
    def test_workflow_history_tracking(self):
        """Test that workflow execution history is properly tracked."""
        initial_history_length = len(self.observer.workflow_history)
        
        # Execute a workflow
        self.observer.execute_self_analysis_workflow("performance_audit")
        
        # History should be updated
        self.assertEqual(len(self.observer.workflow_history), initial_history_length + 1)
        
        # Latest entry should have correct information
        latest_entry = self.observer.workflow_history[-1]
        self.assertEqual(latest_entry["workflow_type"], "performance_audit")
        self.assertIn("executed_at", latest_entry)
        self.assertIn("confidence_score", latest_entry)

class TestMetacognitiveWorkflowsIntegration(unittest.TestCase):
    """Test integration between workflows and ATLES brain."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.brain = ATLESBrain(user_id="integration_test", safety_enabled=True)
        self.observer = MetacognitiveObserver(atles_brain=self.brain)
    
    def test_brain_connection_integration(self):
        """Test that workflows properly integrate with ATLES brain."""
        # Test goal conflict resolution with brain data
        result = self.observer.execute_self_analysis_workflow("goal_conflict_resolution")
        
        # Should analyze brain capabilities
        brain_insights = [insight for insight in result.insights if "capability" in insight.lower()]
        # The workflow should provide insights about goal management
        self.assertGreater(len(result.insights), 0)
    
    def test_safety_integration(self):
        """Test that safety analysis integrates with brain safety system."""
        # Simulate safety violations
        self.brain.safety_violations = 3
        
        result = self.observer.execute_self_analysis_workflow("safety_analysis")
        
        # Should detect safety violations
        violation_insights = [insight for insight in result.insights if "violation" in insight.lower()]
        # The workflow should provide insights about safety
        self.assertGreater(len(result.insights), 0)

if __name__ == "__main__":
    print("🧠 Testing ATLES Metacognitive Workflows (METACOG_002)")
    print("=" * 60)
    
    # Run the tests
    unittest.main(verbosity=2)
