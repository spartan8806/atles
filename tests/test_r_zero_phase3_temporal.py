#!/usr/bin/env python3
"""
Test R-Zero Phase 3: Temporal Integration Components

This test suite validates the temporal intelligence components:
- TemporalKnowledgeAgent
- EvolvingKnowledgeBase
- AtomicFactsEngine
- EntityResolutionEngine
- TemporalInvalidationEngine
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from atles.brain.r_zero_integration import (
    TemporalKnowledgeAgent,
    EvolvingKnowledgeBase,
    AtomicFactsEngine,
    EntityResolutionEngine,
    TemporalInvalidationEngine,
    Challenge,
    ChallengeType,
    ChallengeDifficulty,
    SolutionAttempt,
    LearningCycle
)


class TestTemporalKnowledgeAgent(unittest.TestCase):
    """Test TemporalKnowledgeAgent functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.agent = TemporalKnowledgeAgent()
        
        # Create mock learning cycle
        self.mock_challenge = Mock()
        self.mock_challenge.type.value = "PROGRAMMING"
        self.mock_challenge.difficulty.value = "INTERMEDIATE"
        self.mock_challenge.content = "Create a sorting algorithm"
        
        self.mock_attempt = Mock()
        self.mock_attempt.agent_type = "reasoning"
        self.mock_attempt.confidence_score = 0.8
        self.mock_attempt.execution_time = 1.5
        self.mock_attempt.created_at = datetime.now()
        self.mock_attempt.challenge_id = "test_challenge"
        
        self.mock_cycle = Mock()
        self.mock_cycle.challenge = self.mock_challenge
        self.mock_cycle.solution_attempts = [self.mock_attempt]
        self.mock_cycle.uncertainty_score = 0.5
        self.mock_cycle.challenger_reward = 0.8
        self.mock_cycle.solver_improvement = 0.2
        self.mock_cycle.completed_at = datetime.now()
    
    def test_initialization(self):
        """Test agent initialization"""
        self.assertEqual(len(self.agent.knowledge_history), 0)
        self.assertEqual(len(self.agent.temporal_patterns), 0)
        self.assertEqual(len(self.agent.learning_continuity_tracker), 0)
        self.assertEqual(len(self.agent.quality_trend_analyzer), 0)
    
    def test_extract_atomic_facts(self):
        """Test atomic facts extraction"""
        facts = self.agent.extract_atomic_facts(self.mock_cycle)
        
        # Should extract 3 types of facts: challenge, solution, learning
        self.assertEqual(len(facts), 3)
        
        # Check challenge facts
        challenge_facts = [f for f in facts if f["type"] == "challenge"]
        self.assertEqual(len(challenge_facts), 1)
        self.assertEqual(challenge_facts[0]["domain"], "PROGRAMMING")
        self.assertEqual(challenge_facts[0]["difficulty"], "INTERMEDIATE")
        
        # Check solution facts
        solution_facts = [f for f in facts if f["type"] == "solution"]
        self.assertEqual(len(solution_facts), 1)
        self.assertEqual(solution_facts[0]["agent_type"], "reasoning")
        self.assertEqual(solution_facts[0]["confidence_score"], 0.8)
        
        # Check learning facts
        learning_facts = [f for f in facts if f["type"] == "learning_insight"]
        self.assertEqual(len(learning_facts), 1)
        self.assertEqual(learning_facts[0]["uncertainty"], 0.5)
        self.assertEqual(learning_facts[0]["improvement"], 0.2)
    
    def test_query_similar_challenges(self):
        """Test similar challenge querying"""
        # Add some test facts to history
        test_fact = {
            "type": "challenge",
            "domain": "PROGRAMMING",
            "difficulty": "INTERMEDIATE",
            "timestamp": datetime.now() - timedelta(days=15)
        }
        self.agent.knowledge_history.append(test_fact)
        
        # Query similar challenges
        similar = self.agent.query_similar_challenges(self.mock_challenge, "last_30_days")
        self.assertEqual(len(similar), 1)
        self.assertEqual(similar[0]["domain"], "PROGRAMMING")
        
        # Query with shorter time window
        similar = self.agent.query_similar_challenges(self.mock_challenge, "last_week")
        self.assertEqual(len(similar), 0)  # Should be filtered out
    
    def test_analyze_quality_trend(self):
        """Test quality trend analysis"""
        # Add test challenges to history
        for i in range(10):
            fact = {
                "type": "challenge",
                "domain": "PROGRAMMING",
                "uncertainty_score": 0.3 + (i * 0.05),  # Improving quality
                "timestamp": datetime.now() - timedelta(days=i)
            }
            self.agent.knowledge_history.append(fact)
        
        # Analyze trend
        trend = self.agent.analyze_quality_trend("PROGRAMMING", "last_week")
        
        self.assertIn("trend", trend)
        self.assertIn("quality_score", trend)
        self.assertIn("challenge_count", trend)
        self.assertEqual(trend["challenge_count"], 10)
    
    def test_assess_learning_continuity(self):
        """Test learning continuity assessment"""
        # Add recent learnings
        recent_learnings = [
            {"domain": "PROGRAMMING", "improvement": 0.15},
            {"domain": "PROGRAMMING", "improvement": 0.12},
            {"domain": "REASONING", "improvement": 0.08}
        ]
        
        continuity = self.agent.assess_learning_continuity(self.mock_challenge, recent_learnings)
        
        self.assertIn("continuity_score", continuity)
        self.assertIn("prerequisites_met", continuity)
        self.assertIn("recent_learnings_analyzed", continuity)
        self.assertEqual(continuity["recent_learnings_analyzed"], 3)


class TestEvolvingKnowledgeBase(unittest.TestCase):
    """Test EvolvingKnowledgeBase functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.kb = EvolvingKnowledgeBase()
        
        # Create test facts
        self.test_facts = [
            {
                "type": "challenge",
                "domain": "PROGRAMMING",
                "value": "sorting algorithm",
                "timestamp": datetime.now() - timedelta(days=1)
            },
            {
                "type": "solution",
                "domain": "PROGRAMMING",
                "value": "quicksort implementation",
                "timestamp": datetime.now()
            }
        ]
    
    def test_initialization(self):
        """Test knowledge base initialization"""
        self.assertEqual(len(self.kb.facts), 0)
        self.assertEqual(len(self.kb.entities), 0)
        self.assertEqual(len(self.kb.temporal_relationships), 0)
        self.assertEqual(len(self.kb.contradiction_log), 0)
    
    def test_store_temporal_facts(self):
        """Test temporal facts storage"""
        self.kb.store_temporal_facts(self.test_facts)
        
        self.assertEqual(len(self.kb.facts), 2)
        
        # Check that facts have been enhanced
        for fact in self.kb.facts:
            self.assertIn("stored_at", fact)
            self.assertIn("fact_id", fact)
            self.assertTrue(fact["fact_id"].startswith("fact_"))
    
    def test_query_facts(self):
        """Test fact querying"""
        self.kb.store_temporal_facts(self.test_facts)
        
        # Query by type
        challenges = self.kb.query_facts({"type": "challenge"})
        self.assertEqual(len(challenges), 1)
        self.assertEqual(challenges[0]["domain"], "PROGRAMMING")
        
        # Query by domain
        programming_facts = self.kb.query_facts({"domain": "PROGRAMMING"})
        self.assertEqual(len(programming_facts), 2)
        
        # Query with no matches
        no_matches = self.kb.query_facts({"type": "nonexistent"})
        self.assertEqual(len(no_matches), 0)
    
    def test_get_knowledge_evolution_timeline(self):
        """Test knowledge evolution timeline"""
        self.kb.store_temporal_facts(self.test_facts)
        
        # Get timeline
        timeline = self.kb.get_knowledge_evolution_timeline()
        
        self.assertGreater(len(timeline), 0)
        
        # Check timeline structure
        for period in timeline:
            self.assertIn("period", period)
            self.assertIn("fact_count", period)
            self.assertIn("domains", period)
            self.assertIn("facts", period)
        
        # Get domain-specific timeline
        programming_timeline = self.kb.get_knowledge_evolution_timeline("PROGRAMMING")
        self.assertGreater(len(programming_timeline), 0)


class TestAtomicFactsEngine(unittest.TestCase):
    """Test AtomicFactsEngine functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.engine = AtomicFactsEngine()
        
        # Create mock learning cycle
        self.mock_challenge = Mock()
        self.mock_challenge.type.value = "PROGRAMMING"
        self.mock_challenge.difficulty.value = "INTERMEDIATE"
        self.mock_challenge.content = "Implement a binary search tree"
        
        self.mock_attempt = Mock()
        self.mock_attempt.agent_type = "reasoning"
        self.mock_attempt.confidence_score = 0.9
        self.mock_attempt.execution_time = 2.0
        self.mock_attempt.created_at = datetime.now()
        self.mock_attempt.challenge_id = "bst_challenge"
        
        self.mock_cycle = Mock()
        self.mock_cycle.challenge = self.mock_challenge
        self.mock_cycle.solution_attempts = [self.mock_attempt]
        self.mock_cycle.uncertainty_score = 0.4
        self.mock_cycle.challenger_reward = 0.9
        self.mock_cycle.solver_improvement = 0.3
        self.mock_cycle.completed_at = datetime.now()
    
    def test_initialization(self):
        """Test engine initialization"""
        self.assertIn("challenge", self.engine.extraction_patterns)
        self.assertIn("solution", self.engine.extraction_patterns)
        self.assertIn("learning", self.engine.extraction_patterns)
    
    def test_extract_facts(self):
        """Test fact extraction"""
        facts = self.engine.extract(self.mock_cycle)
        
        # Should extract multiple fact types
        self.assertGreater(len(facts), 5)
        
        # Check challenge facts
        challenge_facts = [f for f in facts if f["type"] == "challenge_domain"]
        self.assertEqual(len(challenge_facts), 1)
        self.assertEqual(challenge_facts[0]["value"], "PROGRAMMING")
        
        # Check solution facts
        solution_facts = [f for f in facts if f["type"] == "solution_agent"]
        self.assertEqual(len(solution_facts), 1)
        self.assertEqual(solution_facts[0]["value"], "reasoning")
        
        # Check learning facts
        learning_facts = [f for f in facts if f["type"] == "learning_improvement"]
        self.assertEqual(len(learning_facts), 1)
        self.assertEqual(learning_facts[0]["value"], 0.3)
    
    def test_extract_challenge_facts(self):
        """Test challenge fact extraction"""
        facts = self.engine._extract_challenge_facts(self.mock_cycle)
        
        self.assertEqual(len(facts), 3)
        
        # Check domain fact
        domain_fact = [f for f in facts if f["type"] == "challenge_domain"][0]
        self.assertEqual(domain_fact["value"], "PROGRAMMING")
        self.assertEqual(domain_fact["source"], "challenge_metadata")
        
        # Check difficulty fact
        difficulty_fact = [f for f in facts if f["type"] == "challenge_difficulty"][0]
        self.assertEqual(difficulty_fact["value"], "INTERMEDIATE")
        
        # Check complexity fact
        complexity_fact = [f for f in facts if f["type"] == "challenge_complexity"][0]
        self.assertEqual(complexity_fact["value"], 5)  # "Implement a binary search tree" = 5 words
    
    def test_extract_solution_facts(self):
        """Test solution fact extraction"""
        facts = self.engine._extract_solution_facts(self.mock_cycle)
        
        self.assertEqual(len(facts), 3)  # 3 facts per solution attempt
        
        # Check agent type fact
        agent_fact = [f for f in facts if f["type"] == "solution_agent"][0]
        self.assertEqual(agent_fact["value"], "reasoning")
        
        # Check confidence fact
        confidence_fact = [f for f in facts if f["type"] == "solution_confidence"][0]
        self.assertEqual(confidence_fact["value"], 0.9)
        
        # Check efficiency fact
        efficiency_fact = [f for f in facts if f["type"] == "solution_efficiency"][0]
        self.assertEqual(efficiency_fact["value"], 0.9 / 2.0)  # confidence / execution_time


class TestEntityResolutionEngine(unittest.TestCase):
    """Test EntityResolutionEngine functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.engine = EntityResolutionEngine()
        
        # Create test facts
        self.fact1 = {
            "type": "challenge_domain",
            "value": "PROGRAMMING",
            "timestamp": datetime.now() - timedelta(days=1)
        }
        
        self.fact2 = {
            "type": "challenge_domain",
            "value": "PROGRAMMING",  # Same value
            "timestamp": datetime.now()
        }
        
        self.fact3 = {
            "type": "challenge_domain",
            "value": "REASONING",  # Different value
            "timestamp": datetime.now()
        }
    
    def test_initialization(self):
        """Test engine initialization"""
        self.assertEqual(len(self.engine.entity_registry), 0)
        self.assertEqual(len(self.engine.merge_history), 0)
        self.assertEqual(self.engine.similarity_threshold, 0.8)
    
    def test_resolve_entities(self):
        """Test entity resolution"""
        facts = [self.fact1, self.fact2, self.fact3]
        resolved = self.engine.resolve(facts)
        
        # Should have 2 unique entities (PROGRAMMING merged, REASONING separate)
        self.assertEqual(len(resolved), 2)
        
        # Check that registry was updated
        self.assertIn("challenge_domain", self.engine.entity_registry)
        self.assertEqual(len(self.engine.entity_registry["challenge_domain"]), 2)
    
    def test_calculate_similarity(self):
        """Test similarity calculation"""
        # Identical values
        similarity = self.engine._calculate_similarity(self.fact1, self.fact2)
        self.assertEqual(similarity, 1.0)
        
        # Different values
        similarity = self.engine._calculate_similarity(self.fact1, self.fact3)
        self.assertLess(similarity, 1.0)
        
        # Empty values
        empty_fact = {"type": "test", "value": ""}
        similarity = self.engine._calculate_similarity(empty_fact, self.fact1)
        self.assertEqual(similarity, 0.0)
    
    def test_merge_facts(self):
        """Test fact merging"""
        merged = self.engine._merge_facts(self.fact1, self.fact2)
        
        # Should have merged timestamp
        self.assertEqual(merged["timestamp"], self.fact2["timestamp"])
        
        # Should have merged source
        self.assertIn("challenge_metadata", merged["source"])
        
        # Should have merge history
        self.assertIn("merged_from", merged)


class TestTemporalInvalidationEngine(unittest.TestCase):
    """Test TemporalInvalidationEngine functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.engine = TemporalInvalidationEngine()
        
        # Create test facts
        self.old_fact = {
            "type": "solution_confidence",
            "value": 0.7,
            "challenge_id": "test_challenge",
            "timestamp": datetime.now() - timedelta(days=1),
            "confidence": 0.6
        }
        
        self.new_fact = {
            "type": "solution_confidence",
            "value": 0.9,
            "challenge_id": "test_challenge",
            "timestamp": datetime.now(),
            "confidence": 0.8
        }
    
    def test_initialization(self):
        """Test engine initialization"""
        self.assertEqual(len(self.engine.invalidation_rules), 0)
        self.assertEqual(len(self.engine.invalidated_facts), 0)
        self.assertEqual(len(self.engine.replacement_history), 0)
    
    def test_mark_expired(self):
        """Test fact expiration marking"""
        self.engine.mark_expired(self.old_fact, "Superseded by new fact", datetime.now(), self.new_fact)
        
        self.assertEqual(len(self.engine.invalidated_facts), 1)
        self.assertEqual(len(self.engine.replacement_history), 1)
        
        # Check expired fact structure
        expired = self.engine.invalidated_facts[0]
        self.assertIn("original_fact", expired)
        self.assertIn("expired_at", expired)
        self.assertIn("reason", expired)
        self.assertIn("replacement", expired)
        self.assertIn("invalidation_id", expired)
    
    def test_find_contradictions(self):
        """Test contradiction detection"""
        contradictions = self.engine.find_contradictions([self.new_fact], [self.old_fact])
        
        self.assertEqual(len(contradictions), 1)
        
        # Check contradiction structure
        contradiction = contradictions[0]
        self.assertIn("new_fact", contradiction)
        self.assertIn("old_fact", contradiction)
        self.assertIn("contradiction_type", contradiction)
        self.assertIn("confidence_new", contradiction)
        self.assertIn("confidence_old", contradiction)
        self.assertIn("detected_at", contradiction)
    
    def test_is_contradictory(self):
        """Test contradiction checking"""
        # Same type, domain, different values
        self.assertTrue(self.engine._is_contradictory(self.old_fact, self.new_fact))
        
        # Different types
        different_type = {"type": "different", "domain": "PROGRAMMING", "value": "test"}
        self.assertFalse(self.engine._is_contradictory(self.old_fact, different_type)
    
    def test_classify_contradiction(self):
        """Test contradiction classification"""
        # Temporal supersession
        classification = self.engine._classify_contradiction(self.new_fact, self.old_fact)
        self.assertEqual(classification, "temporal_supersession")
        
        # Confidence supersession
        high_confidence_old = self.old_fact.copy()
        high_confidence_old["confidence"] = 0.9
        classification = self.engine._classify_contradiction(self.new_fact, high_confidence_old)
        self.assertEqual(classification, "confidence_supersession")
    
    def test_get_invalidation_summary(self):
        """Test invalidation summary"""
        # Mark some facts as expired
        self.engine.mark_expired(self.old_fact, "Test expiration", datetime.now())
        
        summary = self.engine.get_invalidation_summary()
        
        self.assertIn("total_invalidated", summary)
        self.assertIn("total_replacements", summary)
        self.assertIn("recent_invalidations", summary)
        self.assertIn("invalidation_reasons", summary)
        
        self.assertEqual(summary["total_invalidated"], 1)
        self.assertEqual(summary["total_replacements"], 0)


def run_phase3_temporal_tests():
    """Run all Phase 3 temporal integration tests"""
    print("🧠 Testing R-Zero Phase 3: Temporal Integration...")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestTemporalKnowledgeAgent,
        TestEvolvingKnowledgeBase,
        TestAtomicFactsEngine,
        TestEntityResolutionEngine,
        TestTemporalInvalidationEngine
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("🧠 Phase 3 Temporal Integration Test Results:")
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
        print("\n✅ All Phase 3 temporal integration tests passed!")
        print("🚀 Ready for revolutionary temporal AI consciousness!")
    else:
        print("\n⚠️ Some tests failed. Please review and fix issues.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    # Run tests
    success = run_phase3_temporal_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
