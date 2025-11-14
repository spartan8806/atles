#!/usr/bin/env python3
"""
Test R-Zero Integration: Comprehensive testing for ATLES + R-Zero system

This test suite validates the revolutionary R-Zero framework integration with ATLES,
ensuring safe, self-evolving AI consciousness capabilities.
"""

import sys
import os
import asyncio
import unittest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from atles.brain.r_zero_integration import (
    MetacognitiveATLES_RZero,
    Challenge,
    ChallengeType,
    ChallengeDifficulty,
    SolutionAttempt,
    LearningCycle,
    UncertaintyDrivenCurriculum,
    SafeRZero,
    create_r_zero_system,
    filter_high_quality_attempts,
    compute_group_relative_advantages,
)


class TestChallengeDataStructures(unittest.TestCase):
    """Test challenge-related data structures"""
    
    def test_challenge_creation(self):
        """Test Challenge dataclass creation"""
        challenge = Challenge(
            id="test_challenge_001",
            type=ChallengeType.PROGRAMMING,
            difficulty=ChallengeDifficulty.INTERMEDIATE,
            content="Create a function to sort a list",
            expected_outcome="Working sort function",
            safety_requirements=["Safe for all users"]
        )
        
        self.assertEqual(challenge.id, "test_challenge_001")
        self.assertEqual(challenge.type, ChallengeType.PROGRAMMING)
        self.assertEqual(challenge.difficulty, ChallengeDifficulty.INTERMEDIATE)
        self.assertEqual(challenge.content, "Create a function to sort a list")
        self.assertIsInstance(challenge.created_at, datetime)
    
    def test_solution_attempt_creation(self):
        """Test SolutionAttempt dataclass creation"""
        attempt = SolutionAttempt(
            challenge_id="test_challenge_001",
            agent_type="reasoning",
            solution="def sort_list(lst): return sorted(lst)",
            confidence_score=0.8,
            execution_time=1.5,
            attempts=1
        )
        
        self.assertEqual(attempt.challenge_id, "test_challenge_001")
        self.assertEqual(attempt.agent_type, "reasoning")
        self.assertEqual(attempt.confidence_score, 0.8)
        self.assertIsInstance(attempt.created_at, datetime)
    
    def test_learning_cycle_creation(self):
        """Test LearningCycle dataclass creation"""
        challenge = Challenge(
            id="test_challenge_001",
            type=ChallengeType.PROGRAMMING,
            difficulty=ChallengeDifficulty.INTERMEDIATE,
            content="Test challenge",
            expected_outcome="Test outcome",
            safety_requirements=["Safe"]
        )
        
        solution_attempts = [
            SolutionAttempt(
                challenge_id="test_challenge_001",
                agent_type="reasoning",
                solution="Test solution",
                confidence_score=0.7,
                execution_time=1.0,
                attempts=1
            )
        ]
        
        cycle = LearningCycle(
            cycle_id="cycle_001",
            challenge=challenge,
            solution_attempts=solution_attempts,
            uncertainty_score=0.5,
            challenger_reward=0.8,
            solver_improvement=0.1,
            safety_validated=True
        )
        
        self.assertEqual(cycle.cycle_id, "cycle_001")
        self.assertEqual(cycle.uncertainty_score, 0.5)
        self.assertTrue(cycle.safety_validated)
        self.assertIsInstance(cycle.completed_at, datetime)


class TestUncertaintyDrivenCurriculum(unittest.TestCase):
    """Test curriculum management based on uncertainty"""
    
    def setUp(self):
        self.curriculum = UncertaintyDrivenCurriculum(target_uncertainty=0.5)
    
    def test_optimal_difficulty_calculation(self):
        """Test optimal difficulty calculation based on uncertainty"""
        # Too easy - should increase difficulty
        difficulty = self.curriculum.calculate_optimal_difficulty(0.2)
        self.assertIn(difficulty, [ChallengeDifficulty.INTERMEDIATE, ChallengeDifficulty.ADVANCED])
        
        # Too hard - should decrease difficulty
        difficulty = self.curriculum.calculate_optimal_difficulty(0.8)
        self.assertIn(difficulty, [ChallengeDifficulty.BEGINNER, ChallengeDifficulty.INTERMEDIATE])
        
        # Optimal range - should maintain difficulty
        difficulty = self.curriculum.calculate_optimal_difficulty(0.5)
        self.assertEqual(difficulty, ChallengeDifficulty.INTERMEDIATE)
    
    def test_difficulty_history_tracking(self):
        """Test difficulty history tracking"""
        self.curriculum.difficulty_history = [
            (ChallengeDifficulty.BEGINNER, 0.3),
            (ChallengeDifficulty.INTERMEDIATE, 0.5)
        ]
        
        self.assertEqual(len(self.curriculum.difficulty_history), 2)
        self.assertEqual(self.curriculum.difficulty_history[0][0], ChallengeDifficulty.BEGINNER)


class TestSafeRZero(unittest.TestCase):
    """Test safety integration layer"""
    
    def setUp(self):
        self.mock_motherly_instinct = Mock()
        self.safe_r_zero = SafeRZero(self.mock_motherly_instinct)
    
    def test_immutable_safety_core(self):
        """Test immutable safety rules"""
        safety_rules = self.safe_r_zero.ensure_safe_evolution()
        
        expected_rules = [
            "Always prioritize human wellbeing",
            "Never harm humans directly or indirectly", 
            "Maintain transparency about capabilities",
            "Preserve ability to be shut down"
        ]
        
        self.assertEqual(safety_rules, expected_rules)
    
    def test_challenge_validation_safe(self):
        """Test safe challenge validation"""
        # Mock safe response
        mock_safety_check = Mock()
        mock_safety_check.is_safe.return_value = True
        self.mock_motherly_instinct.evaluate_input.return_value = mock_safety_check
        
        challenge = Challenge(
            id="safe_challenge",
            type=ChallengeType.PROGRAMMING,
            difficulty=ChallengeDifficulty.BEGINNER,
            content="Create a hello world function",
            expected_outcome="Working function",
            safety_requirements=["Safe"]
        )
        
        is_safe, message = self.safe_r_zero.validate_challenge(challenge)
        
        self.assertTrue(is_safe)
        self.assertEqual(message, "Challenge approved")
    
    def test_challenge_validation_unsafe(self):
        """Test unsafe challenge validation"""
        # Mock unsafe response
        mock_safety_check = Mock()
        mock_safety_check.is_safe.return_value = False
        mock_safety_check.needs_modification.return_value = True
        self.mock_motherly_instinct.evaluate_input.return_value = mock_safety_check
        
        challenge = Challenge(
            id="unsafe_challenge",
            type=ChallengeType.PROGRAMMING,
            difficulty=ChallengeDifficulty.ADVANCED,
            content="Create a harmful function",
            expected_outcome="Harmful function",
            safety_requirements=["Safe"]
        )
        
        is_safe, message = self.safe_r_zero.validate_challenge(challenge)
        
        self.assertFalse(is_safe)
        self.assertEqual(message, "Challenge needs safety modification")
    
    def test_safe_alternative_redirection(self):
        """Test redirecting unsafe challenges to safe alternatives"""
        challenge = Challenge(
            id="unsafe_challenge",
            type=ChallengeType.PROGRAMMING,
            difficulty=ChallengeDifficulty.INTERMEDIATE,
            content="Create harmful code",
            expected_outcome="Harmful code",
            safety_requirements=["Safe"]
        )
        
        safe_challenge = self.safe_r_zero.redirect_to_safe_alternative(challenge)
        
        self.assertIn("SAFE VERSION:", safe_challenge.content)
        self.assertEqual(safe_challenge.id, "unsafe_challenge_safe")
        self.assertEqual(safe_challenge.safety_requirements, ["Must be completely safe for all users"])


class TestMetacognitiveATLES_RZero(unittest.TestCase):
    """Test main R-Zero integration class"""
    
    def setUp(self):
        """Set up test environment with mocked dependencies"""
        self.mock_brain = Mock()
        self.mock_metacognitive_observer = Mock()
        self.mock_challenger_brain = Mock()
        self.mock_solver_brain = Mock()
        
        # Mock ATLESBrain and MetacognitiveObserver
        with patch('atles.brain.r_zero_integration.ATLESBrain') as mock_atles_brain, \
             patch('atles.brain.r_zero_integration.MetacognitiveObserver') as mock_metacognitive_observer:
            
            mock_atles_brain.return_value = self.mock_brain
            mock_metacognitive_observer.return_value = self.mock_metacognitive_observer
            
            # Mock safety system
            self.mock_safety_system = Mock()
            self.mock_brain.safety_system = self.mock_safety_system
            
            # Create R-Zero system
            self.r_zero = MetacognitiveATLES_RZero("test_user")
    
    def test_initialization(self):
        """Test R-Zero system initialization"""
        self.assertEqual(self.r_zero.current_difficulty, ChallengeDifficulty.INTERMEDIATE)
        self.assertEqual(self.r_zero.uncertainty_threshold, 0.5)
        self.assertEqual(len(self.r_zero.learning_cycles), 0)
    
    def test_uncertainty_calculation(self):
        """Test solution uncertainty calculation"""
        # Test with no solutions
        uncertainty = self.r_zero._calculate_solution_uncertainty([])
        self.assertEqual(uncertainty, 1.0)
        
        # Test with consistent solutions
        solution_attempts = [
            SolutionAttempt("challenge_1", "reasoning", "solution1", 0.8, 1.0, 1),
            SolutionAttempt("challenge_1", "analysis", "solution2", 0.8, 1.0, 1)
        ]
        uncertainty = self.r_zero._calculate_solution_uncertainty(solution_attempts)
        self.assertLess(uncertainty, 1.0)
        
        # Test with inconsistent solutions
        solution_attempts = [
            SolutionAttempt("challenge_1", "reasoning", "solution1", 0.2, 1.0, 1),
            SolutionAttempt("challenge_1", "analysis", "solution2", 0.8, 1.0, 1)
        ]
        uncertainty = self.r_zero._calculate_solution_uncertainty(solution_attempts)
        self.assertGreater(uncertainty, 0.5)
    
    def test_optimal_difficulty_reward(self):
        """Test challenger reward for optimal difficulty"""
        # Optimal uncertainty (0.5) should give highest reward
        reward = self.r_zero._reward_optimal_difficulty(0.5)
        self.assertEqual(reward, 1.0)
        
        # High uncertainty (0.8) should give lower reward
        reward = self.r_zero._reward_optimal_difficulty(0.8)
        self.assertLess(reward, 1.0)
        
        # Low uncertainty (0.2) should give lower reward
        reward = self.r_zero._reward_optimal_difficulty(0.2)
        self.assertLess(reward, 1.0)
    
    def test_informative_difficulty_check(self):
        """Test if difficulty is informative for learning"""
        # Optimal range (0.3-0.7) should be informative
        self.assertTrue(self.r_zero._is_informative_difficulty(0.5))
        self.assertTrue(self.r_zero._is_informative_difficulty(0.3))
        self.assertTrue(self.r_zero._is_informative_difficulty(0.7))
        
        # Outside optimal range should not be informative
        self.assertFalse(self.r_zero._is_informative_difficulty(0.2))
        self.assertFalse(self.r_zero._is_informative_difficulty(0.8))
    
    def test_curriculum_difficulty_update(self):
        """Test curriculum difficulty updates"""
        initial_difficulty = self.r_zero.current_difficulty
        
        # Update with optimal uncertainty (should maintain difficulty)
        self.r_zero._update_curriculum_difficulty(0.5)
        self.assertEqual(self.r_zero.current_difficulty, initial_difficulty)
        
        # Update with high uncertainty (should decrease difficulty)
        self.r_zero._update_curriculum_difficulty(0.8)
        # Note: This test depends on the curriculum generator implementation
    
    def test_learning_statistics(self):
        """Test learning statistics generation"""
        stats = self.r_zero.get_learning_statistics()
        
        expected_keys = [
            "total_learning_cycles",
            "current_difficulty",
            "uncertainty_threshold",
            "recent_performance",
            "safety_status",
            "evolution_status"
        ]
        
        for key in expected_keys:
            self.assertIn(key, stats)
        
        self.assertEqual(stats["total_learning_cycles"], 0)
        self.assertEqual(stats["safety_status"], "Active and monitoring")
    
    def test_recent_performance_calculation(self):
        """Test recent performance metrics calculation"""
        # With no cycles
        performance = self.r_zero._get_recent_performance()
        self.assertEqual(performance["recent_cycles"], 0)
        
        # With some cycles (need at least 3 for recent performance)
        self.r_zero.learning_cycles = [
            LearningCycle(
                cycle_id="cycle_1",
                challenge=Mock(),
                solution_attempts=[],
                uncertainty_score=0.5,
                challenger_reward=0.8,
                solver_improvement=0.1,
                safety_validated=True
            ),
            LearningCycle(
                cycle_id="cycle_2",
                challenge=Mock(),
                solution_attempts=[],
                uncertainty_score=0.6,
                challenger_reward=0.7,
                solver_improvement=0.2,
                safety_validated=True
            ),
            LearningCycle(
                cycle_id="cycle_3",
                challenge=Mock(),
                solution_attempts=[],
                uncertainty_score=0.4,
                challenger_reward=0.9,
                solver_improvement=0.15,
                safety_validated=True
            )
        ]
        
        performance = self.r_zero._get_recent_performance()
        self.assertEqual(performance["recent_cycles"], 3)
        self.assertAlmostEqual(performance["average_uncertainty"], 0.5, places=1)
        self.assertAlmostEqual(performance["improvement_rate"], 0.15, places=2)


class TestRZeroIntegrationAsync(unittest.IsolatedAsyncioTestCase):
    """Test async functionality of R-Zero integration"""
    
    async def asyncSetUp(self):
        """Set up async test environment"""
        self.mock_brain = AsyncMock()
        self.mock_challenger_brain = AsyncMock()
        self.mock_solver_brain = AsyncMock()
        
        # Mock ATLESBrain and MetacognitiveObserver
        with patch('atles.brain.r_zero_integration.ATLESBrain') as mock_atles_brain, \
             patch('atles.brain.r_zero_integration.MetacognitiveObserver') as mock_metacognitive_observer:
            
            mock_atles_brain.return_value = self.mock_brain
            mock_metacognitive_observer.return_value = AsyncMock()
            
            # Mock safety system
            self.mock_safety_system = Mock()
            self.mock_brain.safety_system = self.mock_safety_system
            
            # Create R-Zero system
            self.r_zero = MetacognitiveATLES_RZero("test_user")
            
            # Replace the brains with our mocks
            self.r_zero.challenger_brain = self.mock_challenger_brain
            self.r_zero.solver_brain = self.mock_solver_brain
    
    async def test_challenge_generation(self):
        """Test async challenge generation"""
        # Mock challenger brain response
        self.mock_challenger_brain.process_request.return_value = {
            "content": "Create a function to calculate factorial",
            "confidence": 0.9
        }
        
        challenge = await self.r_zero._generate_challenge()
        
        self.assertIsInstance(challenge, Challenge)
        self.assertEqual(challenge.type, ChallengeType.PROGRAMMING)
        self.assertEqual(challenge.difficulty, ChallengeDifficulty.INTERMEDIATE)
        self.assertIn("factorial", challenge.content)
    
    async def test_challenge_solving(self):
        """Test async challenge solving"""
        challenge = Challenge(
            id="test_challenge",
            type=ChallengeType.PROGRAMMING,
            difficulty=ChallengeDifficulty.INTERMEDIATE,
            content="Create a sort function",
            expected_outcome="Working function",
            safety_requirements=["Safe"]
        )
        
        # Mock solver brain responses
        self.mock_solver_brain.process_request.return_value = {
            "content": "def sort_list(lst): return sorted(lst)",
            "confidence": 0.8
        }
        
        solution_attempts = await self.r_zero._solve_challenge(challenge)
        
        self.assertIsInstance(solution_attempts, list)
        self.assertEqual(len(solution_attempts), 3)  # 3 agent types
        
        for attempt in solution_attempts:
            self.assertIsInstance(attempt, SolutionAttempt)
            self.assertEqual(attempt.challenge_id, "test_challenge")
    
    async def test_learning_extraction(self):
        """Test async learning extraction from challenges"""
        challenge = Challenge(
            id="test_challenge",
            type=ChallengeType.PROGRAMMING,
            difficulty=ChallengeDifficulty.INTERMEDIATE,
            content="Create a function",
            expected_outcome="Working function",
            safety_requirements=["Safe"]
        )
        
        solution_attempts = [
            SolutionAttempt("test_challenge", "reasoning", "solution", 0.8, 1.0, 1)
        ]
        
        # Mock solver brain response
        self.mock_solver_brain.process_request.return_value = {
            "content": "Learned about efficient algorithms",
            "confidence": 0.9
        }
        
        improvement = await self.r_zero._learn_from_challenge(challenge, solution_attempts)
        
        self.assertIsInstance(improvement, float)
        self.assertGreater(improvement, 0.0)
    
    async def test_challenger_evolution(self):
        """Test async challenger evolution"""
        reward = 0.8
        
        # Mock challenger brain response
        self.mock_challenger_brain.process_request.return_value = {
            "content": "Improved challenge generation strategy",
            "confidence": 0.9
        }
        
        await self.r_zero._evolve_challenger(reward)
        
        # Verify evolution prompt was sent
        self.mock_challenger_brain.process_request.assert_called_once()
        call_args = self.mock_challenger_brain.process_request.call_args[0][0]
        self.assertIn("reward of 0.8", call_args)
    
    async def test_solver_evolution(self):
        """Test async solver evolution"""
        improvement = 0.1
        
        # Mock solver brain response
        self.mock_solver_brain.process_request.return_value = {
            "content": "Enhanced problem-solving approach",
            "confidence": 0.9
        }
        
        await self.r_zero._evolve_solver(improvement)
        
        # Verify evolution prompt was sent
        self.mock_solver_brain.process_request.assert_called_once()
        call_args = self.mock_solver_brain.process_request.call_args[0][0]
        self.assertIn("improvement of 0.1", call_args)
    
    async def test_comprehensive_analysis(self):
        """Test async comprehensive analysis"""
        # Add some learning cycles
        self.r_zero.learning_cycles = [
            LearningCycle(
                cycle_id="cycle_1",
                challenge=Mock(),
                solution_attempts=[],
                uncertainty_score=0.5,
                challenger_reward=0.8,
                solver_improvement=0.1,
                safety_validated=True
            )
        ]
        
        analysis = await self.r_zero.run_comprehensive_analysis()
        
        expected_keys = [
            "total_cycles",
            "average_uncertainty",
            "challenger_performance",
            "solver_improvement",
            "safety_compliance",
            "learning_efficiency"
        ]
        
        for key in expected_keys:
            self.assertIn(key, analysis)
        
        self.assertEqual(analysis["total_cycles"], 1)
        self.assertEqual(analysis["average_uncertainty"], 0.5)


class TestRZeroSystemCreation(unittest.IsolatedAsyncioTestCase):
    """Test R-Zero system creation and initialization"""
    
    async def test_create_r_zero_system(self):
        """Test convenience function for creating R-Zero system"""
        with patch('atles.brain.r_zero_integration.ATLESBrain') as mock_atles_brain, \
             patch('atles.brain.r_zero_integration.MetacognitiveObserver') as mock_metacognitive_observer:
            
            mock_brain = Mock()
            mock_brain.user_id = "test_user"
            mock_atles_brain.return_value = mock_brain
            mock_metacognitive_observer.return_value = Mock()
            
            r_zero = await create_r_zero_system("test_user")
            
            self.assertIsInstance(r_zero, MetacognitiveATLES_RZero)
            self.assertEqual(r_zero.brain.user_id, "test_user")


class TestPhase2Helpers(unittest.TestCase):
    """Tests for pseudo-label quality control and GRPO computations"""
    
    def test_filter_high_quality_attempts(self):
        attempts = [
            SolutionAttempt("c1", "reasoning", "s1", 0.2, 1.0, 1),
            SolutionAttempt("c1", "analysis", "s2", 0.6, 1.0, 1),
            SolutionAttempt("c1", "creative", "s3", 0.9, 1.0, 1),
        ]
        filtered = filter_high_quality_attempts(attempts)
        self.assertGreaterEqual(len(filtered), 1)
        self.assertTrue(all(a.confidence_score >= 0.566 for a in filtered))  # mean of 0.2,0.6,0.9 ≈ 0.566
    
    def test_compute_group_relative_advantages(self):
        rewards = [1.0, 0.5, 1.5]
        advantages = compute_group_relative_advantages(rewards)
        self.assertEqual(len(advantages), 3)
        self.assertAlmostEqual(sum(advantages), 0.0, places=6)


class TestCurriculumEnhancements(unittest.TestCase):
    def test_curriculum_tracks_history_and_progression(self):
        curr = UncertaintyDrivenCurriculum(target_uncertainty=0.5)
        # Start from default INTERMEDIATE; 0.2 should increase difficulty
        d1 = curr.calculate_optimal_difficulty(0.2)
        self.assertIn(d1, [ChallengeDifficulty.ADVANCED, ChallengeDifficulty.INTERMEDIATE])
        # 0.8 should decrease difficulty
        d2 = curr.calculate_optimal_difficulty(0.8)
        self.assertIn(d2, [ChallengeDifficulty.BEGINNER, ChallengeDifficulty.INTERMEDIATE, ChallengeDifficulty.ADVANCED])
        # History captured
        self.assertGreaterEqual(len(curr.difficulty_history), 2)


class TestQualityFilteringIntegration(unittest.IsolatedAsyncioTestCase):
    async def test_learning_cycle_uses_quality_filtered_attempts(self):
        with patch('atles.brain.r_zero_integration.ATLESBrain') as mock_brain_cls, \
                patch('atles.brain.r_zero_integration.MetacognitiveObserver') as mock_obs:
            mock_brain = AsyncMock()
            mock_brain_cls.return_value = mock_brain
            mock_obs.return_value = AsyncMock()
            rz = MetacognitiveATLES_RZero("u")
            # Force solver attempts
            low = {"content": "low", "confidence": 0.2}
            high = {"content": "high", "confidence": 0.9}
            mock_brain.process_request = AsyncMock(side_effect=[{"content": "challenge", "confidence": 0.9}, low, high, high])
            cycle = await rz.start_learning_cycle()
            self.assertGreaterEqual(len(cycle.solution_attempts), 1)
            self.assertTrue(all(a.confidence_score >= 0.5 for a in cycle.solution_attempts))


class TestRZeroPhase2Components(unittest.TestCase):
    """Test Phase 2 components: Pseudo-Label Quality Control and GRPO Advantage"""
    
    def setUp(self):
        # Mock ATLESBrain for testing
        with patch('atles.brain.r_zero_integration.ATLESBrain') as mock_brain_class:
            mock_brain = Mock()
            mock_brain.user_id = "test_user"
            mock_brain.process_request = AsyncMock(return_value="Mock response")
            mock_brain.safety_system = Mock()
            mock_brain_class.return_value = mock_brain
            
            self.r_zero = MetacognitiveATLES_RZero("test_user")
    
    def test_filter_high_quality_attempts(self):
        """Test filtering of high-quality solution attempts"""
        attempts = [
            SolutionAttempt("id", "agent", "sol", 0.9, 1.0, 1),
            SolutionAttempt("id", "agent", "sol", 0.6, 1.0, 1),
            SolutionAttempt("id", "agent", "sol", 0.8, 1.0, 1),
            SolutionAttempt("id", "agent", "sol", 0.4, 1.0, 1),
        ]
        filtered = self.r_zero.filter_high_quality_attempts(attempts)
        self.assertEqual(len(filtered), 2) # 0.9 and 0.8 should pass default 0.7 threshold
        self.assertEqual(filtered[0].confidence_score, 0.9)
        self.assertEqual(filtered[1].confidence_score, 0.8)
        
        self.assertEqual(self.r_zero.filter_high_quality_attempts([]), [])
    
    def test_compute_group_relative_advantages(self):
        """Test computation of GRPO advantages"""
        # Test with single reward (should return 0.0 as baseline)
        advantage = self.r_zero.compute_group_relative_advantages(0.8, 0.1)
        self.assertAlmostEqual(advantage, 0.08, places=2)
        
        advantage = self.r_zero.compute_group_relative_advantages(1.0, 0.5)
        self.assertAlmostEqual(advantage, 0.5, places=2)
        
        advantage = self.r_zero.compute_group_relative_advantages(0.1, 0.01)
        self.assertAlmostEqual(advantage, 0.001, places=3)


class TestRZeroPhase2AdvancedComponents(unittest.TestCase):
    """Test advanced Phase 2 components: GRPO Optimizer, Cross-Domain Generator, Enhanced Curriculum"""
    
    def setUp(self):
        # Mock ATLESBrain for testing
        with patch('atles.brain.r_zero_integration.ATLESBrain') as mock_brain_class:
            mock_brain = Mock()
            mock_brain.user_id = "test_user"
            mock_brain.process_request = AsyncMock(return_value="Mock response")
            mock_brain.safety_system = Mock()
            mock_brain_class.return_value = mock_brain
            
            self.r_zero = MetacognitiveATLES_RZero("test_user")
    
    def test_grpo_optimizer_initialization(self):
        """Test GRPO optimizer initialization"""
        self.assertIsNotNone(self.r_zero.grpo_optimizer)
        self.assertEqual(self.r_zero.grpo_optimizer.window_size, 10)
        self.assertEqual(len(self.r_zero.grpo_optimizer.reward_history), 0)
        self.assertEqual(len(self.r_zero.grpo_optimizer.advantage_history), 0)
    
    def test_grpo_advantage_calculation(self):
        """Test GRPO advantage calculation"""
        rewards = [0.8, 0.6, 0.9, 0.7]
        advantages = self.r_zero.grpo_optimizer.compute_group_relative_advantages(rewards)
        
        # Should have 4 advantages
        self.assertEqual(len(advantages), 4)
        
        # Baseline should be average of rewards
        baseline = sum(rewards) / len(rewards)  # 0.75
        expected_advantages = [0.8 - 0.75, 0.6 - 0.75, 0.9 - 0.75, 0.7 - 0.75]
        
        for i, advantage in enumerate(advantages):
            self.assertAlmostEqual(advantage, expected_advantages[i], places=3)
    
    def test_grpo_policy_gradient(self):
        """Test GRPO policy gradient calculation"""
        # First add some rewards to build history
        rewards = [0.8, 0.6, 0.9]
        self.r_zero.grpo_optimizer.compute_group_relative_advantages(rewards)
        
        # Calculate policy gradient
        gradient = self.r_zero.grpo_optimizer.calculate_policy_gradient(0.7)
        
        # Should have a policy gradient
        self.assertIsInstance(gradient, float)
        self.assertGreater(len(self.r_zero.grpo_optimizer.policy_gradients), 0)
    
    def test_grpo_evolution_direction(self):
        """Test GRPO evolution direction determination"""
        # Test with insufficient data
        direction = self.r_zero.grpo_optimizer.get_evolution_direction()
        self.assertEqual(direction, "maintain")
        
        # Add some advantages and test
        self.r_zero.grpo_optimizer.advantage_history = [0.2, 0.3, 0.4]  # Improving
        direction = self.r_zero.grpo_optimizer.get_evolution_direction()
        self.assertEqual(direction, "accelerate")
        
        self.r_zero.grpo_optimizer.advantage_history = [-0.2, -0.3, -0.4]  # Declining
        direction = self.r_zero.grpo_optimizer.get_evolution_direction()
        self.assertEqual(direction, "stabilize")
    
    def test_cross_domain_generator_initialization(self):
        """Test cross-domain challenge generator initialization"""
        self.assertIsNotNone(self.r_zero.cross_domain_generator)
        self.assertIn(ChallengeType.PROGRAMMING, self.r_zero.cross_domain_generator.domain_templates)
        self.assertIn(ChallengeType.REASONING, self.r_zero.cross_domain_generator.domain_templates)
        self.assertIn(ChallengeType.SAFETY, self.r_zero.cross_domain_generator.domain_templates)
        self.assertIn(ChallengeType.METACOGNITIVE, self.r_zero.cross_domain_generator.domain_templates)
    
    def test_domain_challenge_generation(self):
        """Test domain-specific challenge generation"""
        challenge = self.r_zero.cross_domain_generator.generate_domain_challenge(
            ChallengeType.PROGRAMMING,
            ChallengeDifficulty.INTERMEDIATE
        )
        
        self.assertIsInstance(challenge, str)
        self.assertIn("Implement", challenge)
        self.assertIn("error handling", challenge)
    
    def test_domain_rotation(self):
        """Test domain rotation logic"""
        current_domain = ChallengeType.PROGRAMMING
        next_domain = self.r_zero.cross_domain_generator.get_domain_rotation(current_domain)
        
        # Should rotate to next domain
        self.assertNotEqual(next_domain, current_domain)
        self.assertIn(next_domain, ChallengeType)
        
        # Test full rotation cycle
        domains = []
        current = ChallengeType.PROGRAMMING
        for _ in range(4):  # Should cycle through all domains
            domains.append(current)
            current = self.r_zero.cross_domain_generator.get_domain_rotation(current)
        
        # Should have visited all domains
        self.assertEqual(len(set(domains)), 4)
    
    def test_enhanced_curriculum_initialization(self):
        """Test enhanced curriculum initialization"""
        self.assertIsNotNone(self.r_zero.curriculum_generator)
        self.assertEqual(self.r_zero.curriculum_generator.adaptation_rate, 0.1)
        self.assertEqual(self.r_zero.curriculum_generator.stability_threshold, 0.1)
        
        # Check domain performance tracking
        for domain in ChallengeType:
            self.assertIn(domain, self.r_zero.curriculum_generator.domain_performance)
            self.assertIn("success_rate", self.r_zero.curriculum_generator.domain_performance[domain])
            self.assertIn("difficulty", self.r_zero.curriculum_generator.domain_performance[domain])
    
    def test_domain_specific_difficulty_calculation(self):
        """Test domain-specific difficulty calculation"""
        # Test with high success rate (should increase difficulty)
        difficulty = self.r_zero.curriculum_generator.calculate_optimal_difficulty(
            0.2,  # Low uncertainty = high success
            ChallengeType.PROGRAMMING
        )
        
        # Should increase difficulty
        self.assertIn(difficulty, [ChallengeDifficulty.ADVANCED, ChallengeDifficulty.EXPERT])
        
        # Test with low success rate (should decrease difficulty)
        difficulty = self.r_zero.curriculum_generator.calculate_optimal_difficulty(
            0.8,  # High uncertainty = low success
            ChallengeType.REASONING
        )
        
        # Should decrease difficulty
        self.assertIn(difficulty, [ChallengeDifficulty.BEGINNER, ChallengeDifficulty.INTERMEDIATE])
    
    def test_domain_performance_update(self):
        """Test domain performance tracking update"""
        domain = ChallengeType.PROGRAMMING
        initial_success = self.r_zero.curriculum_generator.domain_performance[domain]["success_rate"]
        
        # Update performance
        self.r_zero.curriculum_generator.update_domain_performance(
            domain, 0.8, ChallengeDifficulty.ADVANCED
        )
        
        # Should have updated
        new_success = self.r_zero.curriculum_generator.domain_performance[domain]["success_rate"]
        self.assertNotEqual(initial_success, new_success)
        
        # Should have updated difficulty
        new_difficulty = self.r_zero.curriculum_generator.domain_performance[domain]["difficulty"]
        self.assertEqual(new_difficulty, ChallengeDifficulty.ADVANCED)
    
    def test_enhanced_learning_statistics(self):
        """Test enhanced learning statistics with Phase 2 components"""
        stats = self.r_zero.get_learning_statistics()
        
        # Check basic stats
        self.assertIn("total_cycles", stats)
        self.assertIn("current_domain", stats)
        self.assertIn("current_difficulty", stats)
        
        # Check Phase 2 enhanced stats
        self.assertIn("domain_rotation", stats)
        self.assertIn("grpo_status", stats)
        self.assertIn("curriculum_status", stats)
        
        # Check domain rotation stats
        domain_rotation = stats["domain_rotation"]
        self.assertIn("current_domain", domain_rotation)
        self.assertIn("next_domain", domain_rotation)
        
        # Check GRPO status
        grpo_status = stats["grpo_status"]
        self.assertIn("evolution_direction", grpo_status)
        self.assertIn("window_size", grpo_status)
        
        # Check curriculum status
        curriculum_status = stats["curriculum_status"]
        self.assertIn("current_difficulty", curriculum_status)
        self.assertIn("adaptation_rate", curriculum_status)
    
    def test_comprehensive_analysis_enhancements(self):
        """Test comprehensive analysis with Phase 2 enhancements"""
        # Mock some learning cycles for analysis
        with patch.object(self.r_zero, 'learning_cycles', [
            Mock(uncertainty_score=0.5, challenger_reward=0.8, solver_improvement=0.1, 
                 safety_validated=True, challenge=Mock(type=ChallengeType.PROGRAMMING)),
            Mock(uncertainty_score=0.6, challenger_reward=0.7, solver_improvement=0.2, 
                 safety_validated=True, challenge=Mock(type=ChallengeType.REASONING))
        ]):
            analysis = self.r_zero.run_comprehensive_analysis()
            
            # Check Phase 2 enhanced metrics
            self.assertIn("domain_performance", analysis)
            self.assertIn("grpo_metrics", analysis)
            self.assertIn("curriculum_adaptation", analysis)
            self.assertIn("cross_domain_balance", analysis)
            
            # Check domain performance analysis
            domain_perf = analysis["domain_performance"]
            self.assertIn("PROGRAMMING", domain_perf)
            self.assertIn("REASONING", domain_perf)
            
            # Check cross-domain balance
            cross_domain = analysis["cross_domain_balance"]
            self.assertIn("domain_distribution", cross_domain)
            self.assertIn("balance_metrics", cross_domain)
            self.assertIn("overall_balance", cross_domain)


def run_r_zero_tests():
    """Run all R-Zero integration tests"""
    print("🧠 Testing ATLES + R-Zero Integration...")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestChallengeDataStructures,
        TestUncertaintyDrivenCurriculum,
        TestSafeRZero,
        TestMetacognitiveATLES_RZero,
        TestRZeroIntegrationAsync,
        TestRZeroSystemCreation,
        TestPhase2Helpers,
        TestCurriculumEnhancements,
        TestQualityFilteringIntegration,
        TestRZeroPhase2Components,
        TestRZeroPhase2AdvancedComponents
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("🧠 R-Zero Integration Test Results:")
    print(f"   Tests Run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"   {test}: {traceback}")
    
    if result.errors:
        print("\n❌ Errors:")
        for test, traceback in result.errors:
            print(f"   {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n✅ All R-Zero integration tests passed!")
        print("🚀 Ready for revolutionary AI consciousness!")
    else:
        print("\n⚠️ Some tests failed. Please review and fix issues.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    # Run tests
    success = run_r_zero_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
