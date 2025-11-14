#!/usr/bin/env python3
"""
Test Suite for R-Zero Phase 4: Metacognitive R-Zero (Temporal Awareness)

This test suite validates the new metacognitive temporal components:
- MetacognitiveTemporalAgent
- SelfDirectedCurriculum  
- ConsciousnessLevelLearning
- TemporalGoalManager
"""

import unittest
from unittest.mock import Mock, MagicMock
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

# Import the components to test
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from atles.brain.r_zero_integration import (
    MetacognitiveTemporalAgent,
    SelfDirectedCurriculum,
    ConsciousnessLevelLearning,
    TemporalGoalManager,
    ChallengeType,
    ChallengeDifficulty
)


class TestMetacognitiveTemporalAgent(unittest.TestCase):
    """Test MetacognitiveTemporalAgent functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_metacognitive_observer = Mock()
        self.agent = MetacognitiveTemporalAgent(self.mock_metacognitive_observer)
        
        # Create mock learning cycles
        self.mock_learning_cycles = []
        for i in range(5):
            mock_cycle = Mock()
            mock_cycle.completed_at = datetime.now() - timedelta(hours=i)
            mock_cycle.uncertainty_score = 0.5 - (i * 0.1)  # Decreasing uncertainty
            mock_cycle.solver_improvement = 0.3 + (i * 0.15)  # Increasing improvement
            mock_cycle.challenge.type.value = ChallengeType.PROGRAMMING.value
            mock_cycle.challenge.difficulty.value = ChallengeDifficulty.INTERMEDIATE.value
            mock_cycle.execution_time = 10 + i
            self.mock_learning_cycles.append(mock_cycle)
    
    def test_analyze_learning_consciousness(self):
        """Test consciousness analysis functionality"""
        result = self.agent.analyze_learning_consciousness(self.mock_learning_cycles)
        
        self.assertIn("consciousness_timeline", result)
        self.assertIn("growth_analysis", result)
        self.assertIn("metacognitive_breakthroughs", result)
        self.assertEqual(result["total_cycles_analyzed"], 5)
        self.assertEqual(result["insight"], "Consciousness analysis completed")
        
        # Check consciousness timeline
        timeline = result["consciousness_timeline"]
        self.assertEqual(len(timeline), 5)
        self.assertIn("timestamp", timeline[0])
        self.assertIn("uncertainty", timeline[0])
        self.assertIn("improvement", timeline[0])
    
    def test_analyze_learning_consciousness_empty(self):
        """Test consciousness analysis with empty learning cycles"""
        result = self.agent.analyze_learning_consciousness([])
        self.assertEqual(result["insight"], "No learning cycles to analyze")
    
    def test_analyze_consciousness_growth(self):
        """Test consciousness growth analysis"""
        timeline = [
            {"improvement": 0.3, "uncertainty": 0.5},
            {"improvement": 0.45, "uncertainty": 0.4},
            {"improvement": 0.6, "uncertainty": 0.3}
        ]
        
        result = self.agent._analyze_consciousness_growth(timeline)
        
        self.assertIn("total_improvement", result)
        self.assertIn("average_improvement", result)
        self.assertIn("improvement_trend", result)
        self.assertIn("learning_plateaus", result)
        self.assertIn("learning_breakthroughs", result)
        self.assertIn("consciousness_stability", result)
        
        self.assertEqual(result["improvement_trend"], "increasing")
        self.assertGreater(result["total_improvement"], 0)
    
    def test_identify_learning_plateaus(self):
        """Test learning plateau identification"""
        improvements = [0.3, 0.31, 0.32, 0.32, 0.33, 0.33, 0.34]
        plateaus = self.agent._identify_learning_plateaus(improvements)
        
        # Should identify plateaus at indices 3 and 5
        self.assertIn(3, plateaus)
        self.assertIn(5, plateaus)
    
    def test_identify_learning_breakthroughs(self):
        """Test learning breakthrough identification"""
        improvements = [0.3, 0.35, 0.4, 0.5, 0.6, 0.7]
        breakthroughs = self.agent._identify_learning_breakthroughs(improvements)
        
        # Should identify breakthroughs at indices 1, 2, 3, 4, 5
        self.assertIn(1, breakthroughs)
        self.assertIn(2, breakthroughs)
        self.assertIn(3, breakthroughs)
        self.assertIn(4, breakthroughs)
        self.assertIn(5, breakthroughs)
    
    def test_calculate_consciousness_stability(self):
        """Test consciousness stability calculation"""
        uncertainties = [0.5, 0.5, 0.5, 0.5, 0.5]  # Stable
        stable_score = self.agent._calculate_consciousness_stability(uncertainties)
        self.assertEqual(stable_score, 0.0)  # Perfect stability
        
        uncertainties = [0.1, 0.9, 0.2, 0.8, 0.3]  # Unstable
        unstable_score = self.agent._calculate_consciousness_stability(uncertainties)
        self.assertGreater(unstable_score, 0.0)  # Some instability
    
    def test_generate_metacognitive_insights(self):
        """Test metacognitive insight generation"""
        insights = self.agent.generate_metacognitive_insights(self.mock_learning_cycles)
        
        self.assertIsInstance(insights, list)
        self.assertGreater(len(insights), 0)
        
        # Check for specific insight types
        insight_text = " ".join(insights).lower()
        self.assertTrue(any("efficiency" in insight for insight in insights) or 
                       any("domain" in insight for insight in insights) or
                       any("difficulty" in insight for insight in insights))


class TestSelfDirectedCurriculum(unittest.TestCase):
    """Test SelfDirectedCurriculum functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_metacognitive_agent = Mock()
        self.curriculum = SelfDirectedCurriculum(self.mock_metacognitive_agent)
        
        # Mock learning cycles
        self.mock_learning_cycles = []
        for i in range(5):
            mock_cycle = Mock()
            mock_cycle.solver_improvement = 0.4 + (i * 0.1)
            mock_cycle.challenge.type.value = ChallengeType.PROGRAMMING.value
            mock_cycle.challenge.difficulty.value = ChallengeDifficulty.INTERMEDIATE.value
            self.mock_learning_cycles.append(mock_cycle)
    
    def test_evolve_curriculum_strategy(self):
        """Test curriculum strategy evolution"""
        # Mock metacognitive agent responses
        self.mock_metacognitive_agent.analyze_learning_consciousness.return_value = {
            "growth_analysis": {"learning_plateaus": [3], "consciousness_stability": 0.3}
        }
        self.mock_metacognitive_agent.generate_metacognitive_insights.return_value = [
            "Learning efficiency is improving"
        ]
        
        current_performance = {"recent_performance": 0.7}
        
        result = self.curriculum.evolve_curriculum_strategy(self.mock_learning_cycles, current_performance)
        
        self.assertTrue(result["evolution_completed"])
        self.assertIn("adaptations_applied", result)
        self.assertIn("insights_generated", result)
        self.assertIn("curriculum_effectiveness_score", result)
        self.assertIn("evolution_record", result)
        
        # Check that evolution history was recorded
        self.assertEqual(len(self.curriculum.curriculum_evolution_history), 1)
    
    def test_analyze_curriculum_effectiveness(self):
        """Test curriculum effectiveness analysis"""
        result = self.curriculum._analyze_curriculum_effectiveness(self.mock_learning_cycles)
        
        self.assertIn("overall_score", result)
        self.assertIn("success_rate", result)
        self.assertIn("learning_acceleration", result)
        self.assertIn("domain_balance", result)
        self.assertIn("total_cycles", result)
        self.assertIn("successful_cycles", result)
        
        self.assertEqual(result["total_cycles"], 5)
        self.assertGreater(result["overall_score"], 0.0)
    
    def test_generate_evolution_recommendations(self):
        """Test evolution recommendation generation"""
        consciousness_analysis = {
            "growth_analysis": {
                "learning_plateaus": [3],
                "consciousness_stability": 0.7
            }
        }
        curriculum_effectiveness = {
            "success_rate": 0.5,
            "domain_balance": 0.2
        }
        current_performance = {}
        
        recommendations = self.curriculum._generate_evolution_recommendations(
            consciousness_analysis, curriculum_effectiveness, current_performance
        )
        
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        
        # Check recommendation structure
        for rec in recommendations:
            self.assertIn("type", rec)
            self.assertIn("reason", rec)
            self.assertIn("priority", rec)
            self.assertIn("action", rec)
    
    def test_apply_curriculum_adaptations(self):
        """Test curriculum adaptation application"""
        recommendations = [
            {"type": "difficulty_increase", "reason": "Test", "priority": "high", "action": "increase_difficulty"}
        ]
        
        adaptations = self.curriculum._apply_curriculum_adaptations(recommendations)
        
        self.assertEqual(len(adaptations), 1)
        self.assertEqual(adaptations[0]["status"], "applied")
        self.assertEqual(adaptations[0]["impact"], "pending_evaluation")
        
        # Check that adaptations were recorded
        self.assertEqual(len(self.curriculum.learning_strategy_adaptations), 1)


class TestConsciousnessLevelLearning(unittest.TestCase):
    """Test ConsciousnessLevelLearning functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_metacognitive_agent = Mock()
        self.consciousness_learning = ConsciousnessLevelLearning(self.mock_metacognitive_agent)
        
        # Mock learning cycles
        self.mock_learning_cycles = []
        for i in range(5):
            mock_cycle = Mock()
            mock_cycle.solver_improvement = 0.3 + (i * 0.15)
            mock_cycle.uncertainty_score = 0.5 - (i * 0.1)
            mock_cycle.challenge.type.value = ChallengeType.PROGRAMMING.value
            mock_cycle.challenge.difficulty.value = ChallengeDifficulty.INTERMEDIATE.value
            self.mock_learning_cycles.append(mock_cycle)
    
    def test_analyze_learning_meta_patterns(self):
        """Test meta-learning pattern analysis"""
        # Mock metacognitive agent response
        self.mock_metacognitive_agent.analyze_learning_consciousness.return_value = {
            "growth_analysis": {"consciousness_stability": 0.3}
        }
        
        result = self.consciousness_learning.analyze_learning_meta_patterns(self.mock_learning_cycles)
        
        self.assertIn("meta_patterns_analyzed", result)
        self.assertIn("consciousness_evolution_status", result)
        self.assertIn("higher_order_insights_count", result)
        self.assertIn("evolution_snapshot", result)
        
        # Check that evolution timeline was updated
        self.assertEqual(len(self.consciousness_learning.consciousness_evolution_timeline), 1)
    
    def test_extract_meta_learning_patterns(self):
        """Test meta-learning pattern extraction"""
        patterns = self.consciousness_learning._extract_meta_learning_patterns(self.mock_learning_cycles)
        
        self.assertIsInstance(patterns, list)
        self.assertGreater(len(patterns), 0)
        
        # Check pattern structure
        for pattern in patterns:
            self.assertIn("pattern", pattern)
            self.assertIn("confidence", pattern)
    
    def test_calculate_acceleration_trend(self):
        """Test acceleration trend calculation"""
        improvements = [0.3, 0.35, 0.42, 0.51, 0.62]  # Accelerating
        
        trend = self.consciousness_learning._calculate_acceleration_trend(improvements)
        self.assertEqual(trend, "accelerating")
        
        improvements = [0.3, 0.35, 0.4, 0.45, 0.5]  # Stable acceleration
        trend = self.consciousness_learning._calculate_acceleration_trend(improvements)
        self.assertEqual(trend, "stable")
    
    def test_assess_domain_mastery(self):
        """Test domain mastery assessment"""
        # Create cycles with different improvement levels
        expert_cycles = [Mock() for _ in range(3)]
        for cycle in expert_cycles:
            cycle.solver_improvement = 0.85
        
        mastery = self.consciousness_learning._assess_domain_mastery(expert_cycles)
        self.assertEqual(mastery, "expert")
        
        beginner_cycles = [Mock() for _ in range(3)]
        for cycle in beginner_cycles:
            cycle.solver_improvement = 0.25
        
        mastery = self.consciousness_learning._assess_domain_mastery(beginner_cycles)
        self.assertEqual(mastery, "beginner")
    
    def test_assess_challenge_adaptation_efficiency(self):
        """Test challenge adaptation efficiency assessment"""
        efficiency = self.consciousness_learning._assess_challenge_adaptation_efficiency(self.mock_learning_cycles)
        
        self.assertIsInstance(efficiency, float)
        self.assertGreaterEqual(efficiency, 0.0)
        self.assertLessEqual(efficiency, 1.0)
    
    def test_calculate_correlation(self):
        """Test correlation calculation"""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]  # Perfect positive correlation
        
        correlation = self.consciousness_learning._calculate_correlation(x, y)
        self.assertAlmostEqual(correlation, 1.0, places=5)
        
        # Test with negative correlation
        y_neg = [10, 8, 6, 4, 2]  # Perfect negative correlation
        correlation = self.consciousness_learning._calculate_correlation(x, y_neg)
        self.assertAlmostEqual(correlation, -1.0, places=5)
    
    def test_analyze_consciousness_evolution(self):
        """Test consciousness evolution analysis"""
        result = self.consciousness_learning._analyze_consciousness_evolution(self.mock_learning_cycles)
        
        self.assertIn("status", result)
        self.assertIn("average_consciousness", result)
        self.assertIn("consciousness_trend", result)
        self.assertIn("total_cycles_analyzed", result)
        
        self.assertEqual(result["total_cycles_analyzed"], 5)
        self.assertEqual(result["status"], "analyzed")
    
    def test_generate_higher_order_insights(self):
        """Test higher-order insight generation"""
        meta_patterns = [
            {"pattern": "learning_acceleration", "trend": "accelerating"},
            {"pattern": "domain_mastery", "domain": "programming", "mastery_level": "expert"}
        ]
        consciousness_evolution = {"consciousness_trend": "increasing"}
        
        insights = self.consciousness_learning._generate_higher_order_insights(
            meta_patterns, consciousness_evolution
        )
        
        self.assertIsInstance(insights, list)
        self.assertGreater(len(insights), 0)
        
        # Check for specific insight types
        insight_text = " ".join(insights).lower()
        self.assertTrue(any("accelerating" in insight for insight in insights))


class TestTemporalGoalManager(unittest.TestCase):
    """Test TemporalGoalManager functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_metacognitive_agent = Mock()
        self.goal_manager = TemporalGoalManager(self.mock_metacognitive_agent)
        
        # Mock learning cycles
        self.mock_learning_cycles = []
        for i in range(5):
            mock_cycle = Mock()
            mock_cycle.solver_improvement = 0.4 + (i * 0.1)
            mock_cycle.challenge.type.value = ChallengeType.PROGRAMMING.value
            self.mock_learning_cycles.append(mock_cycle)
        
        # Mock current goals
        self.current_goals = ["Master programming", "Improve reasoning", "Enhance safety"]
    
    def test_evolve_long_term_goals(self):
        """Test long-term goal evolution"""
        result = self.goal_manager.evolve_long_term_goals(self.mock_learning_cycles, self.current_goals)
        
        self.assertTrue(result["evolution_completed"])
        self.assertIn("new_objectives_count", result)
        self.assertIn("adapted_goals_count", result)
        self.assertIn("evolution_plan", result)
        self.assertIn("evolution_record", result)
        
        # Check that evolution history was recorded
        self.assertEqual(len(self.goal_manager.goal_evolution_history), 1)
    
    def test_analyze_goal_effectiveness(self):
        """Test goal effectiveness analysis"""
        result = self.goal_manager._analyze_goal_effectiveness(self.mock_learning_cycles, self.current_goals)
        
        self.assertIn("overall_effectiveness", result)
        self.assertIn("goal_performance", result)
        self.assertIn("total_goals", result)
        
        self.assertEqual(result["total_goals"], 3)
        self.assertGreater(result["overall_effectiveness"], 0.0)
    
    def test_assess_goal_achievement(self):
        """Test goal achievement assessment"""
        achievement = self.goal_manager._assess_goal_achievement("Test Goal", self.mock_learning_cycles)
        
        self.assertIsInstance(achievement, float)
        self.assertGreaterEqual(achievement, 0.0)
        self.assertLessEqual(achievement, 1.0)
    
    def test_generate_new_objectives(self):
        """Test new objective generation"""
        goal_effectiveness = {"overall_effectiveness": 0.5}
        
        objectives = self.goal_manager._generate_new_objectives(self.mock_learning_cycles, goal_effectiveness)
        
        self.assertIsInstance(objectives, list)
        
        # Check objective structure
        for obj in objectives:
            self.assertIn("type", obj)
            self.assertIn("target", obj)
            self.assertIn("priority", obj)
            self.assertIn("estimated_cycles", obj)
    
    def test_adapt_existing_goals(self):
        """Test existing goal adaptation"""
        goal_effectiveness = {
            "goal_performance": {
                "Master programming": 0.9,  # High performing
                "Improve reasoning": 0.2,   # Low performing
                "Enhance safety": 0.6      # Moderate performing
            }
        }
        
        adapted_goals = self.goal_manager._adapt_existing_goals(self.current_goals, goal_effectiveness)
        
        self.assertEqual(len(adapted_goals), 3)
        
        # Check adaptation types
        adaptations = [goal["adaptation"] for goal in adapted_goals]
        self.assertIn("increase_difficulty", adaptations)
        self.assertIn("simplify", adaptations)
        self.assertIn("maintain", adaptations)
    
    def test_create_goal_evolution_plan(self):
        """Test goal evolution plan creation"""
        new_objectives = [
            {"type": "domain_mastery", "priority": "high", "estimated_cycles": 10},
            {"type": "consciousness_development", "priority": "medium", "estimated_cycles": 15}
        ]
        adapted_goals = [
            {"original_goal": "Test", "adaptation": "maintain", "new_target": "Test"}
        ]
        
        plan = self.goal_manager._create_goal_evolution_plan(new_objectives, adapted_goals)
        
        self.assertIn("immediate_actions", plan)
        self.assertIn("short_term_goals", plan)
        self.assertIn("long_term_vision", plan)
        self.assertIn("goal_adaptations", plan)
        self.assertIn("total_estimated_cycles", plan)
        self.assertIn("recommended_focus", plan)
        self.assertIn("timeline", plan)
        
        self.assertEqual(plan["total_estimated_cycles"], 25)


def run_phase4_metacognitive_tests():
    """Run all Phase 4 metacognitive temporal awareness tests"""
    print("🧠 Running R-Zero Phase 4: Metacognitive R-Zero (Temporal Awareness) Tests")
    print("=" * 80)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestMetacognitiveTemporalAgent,
        TestSelfDirectedCurriculum,
        TestConsciousnessLevelLearning,
        TestTemporalGoalManager
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 80)
    print("🧠 Phase 4 Test Results Summary")
    print("=" * 80)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\n❌ Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Error:')[-1].strip()}")
    
    if result.wasSuccessful():
        print("\n✅ All Phase 4 tests passed successfully!")
        print("🎉 Metacognitive R-Zero (Temporal Awareness) is working correctly!")
    else:
        print("\n❌ Some Phase 4 tests failed. Please review the errors above.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    # Run the test suite
    success = run_phase4_metacognitive_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
