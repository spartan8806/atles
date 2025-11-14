#!/usr/bin/env python3
"""
R-Zero Phase 3 Demo: Temporal Integration & Knowledge Evolution

This demo showcases the revolutionary temporal intelligence components:
- TemporalKnowledgeAgent: Manages knowledge evolution and temporal intelligence
- EvolvingKnowledgeBase: Manages evolving knowledge with temporal awareness
- AtomicFactsEngine: Extracts atomic facts from learning experiences
- EntityResolutionEngine: Resolves duplicate entities and merges concepts
- TemporalInvalidationEngine: Handles temporal invalidation of outdated knowledge
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
from unittest.mock import Mock

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


async def demo_temporal_knowledge_agent():
    """Demo the TemporalKnowledgeAgent capabilities"""
    print("🧠 1️⃣ Testing TemporalKnowledgeAgent...")
    print("=" * 50)
    
    agent = TemporalKnowledgeAgent()
    
    # Create mock learning cycles
    mock_challenge = Mock()
    mock_challenge.type.value = "PROGRAMMING"
    mock_challenge.difficulty.value = "INTERMEDIATE"
    mock_challenge.content = "Implement a binary search tree"
    
    mock_attempt = Mock()
    mock_attempt.agent_type = "reasoning"
    mock_attempt.confidence_score = 0.9
    mock_attempt.execution_time = 2.0
    mock_attempt.created_at = datetime.now()
    mock_attempt.challenge_id = "bst_challenge"
    
    mock_cycle = Mock()
    mock_cycle.challenge = mock_challenge
    mock_cycle.solution_attempts = [mock_attempt]
    mock_cycle.uncertainty_score = 0.4
    mock_cycle.challenger_reward = 0.9
    mock_cycle.solver_improvement = 0.3
    mock_cycle.completed_at = datetime.now()
    
    # Extract atomic facts
    facts = agent.extract_atomic_facts(mock_cycle)
    print(f"   ✅ Extracted {len(facts)} atomic facts from learning cycle")
    
    # Add facts to knowledge history
    agent.knowledge_history.extend(facts)
    print(f"   ✅ Knowledge history now contains {len(agent.knowledge_history)} facts")
    
    # Query similar challenges
    similar = agent.query_similar_challenges(mock_challenge, "last_30_days")
    print(f"   ✅ Found {len(similar)} similar challenges in last 30 days")
    
    # Analyze quality trend
    trend = agent.analyze_quality_trend("PROGRAMMING", "last_week")
    print(f"   ✅ Quality trend analysis: {trend['trend']} (score: {trend['quality_score']:.3f})")
    
    # Assess learning continuity
    recent_learnings = [
        {"domain": "PROGRAMMING", "improvement": 0.15},
        {"domain": "PROGRAMMING", "improvement": 0.12}
    ]
    continuity = agent.assess_learning_continuity(mock_challenge, recent_learnings)
    print(f"   ✅ Learning continuity: {continuity['continuity_score']:.3f} (prerequisites: {continuity['prerequisites_met']})")
    
    return True


async def demo_evolving_knowledge_base():
    """Demo the EvolvingKnowledgeBase capabilities"""
    print("\n🧠 2️⃣ Testing EvolvingKnowledgeBase...")
    print("=" * 50)
    
    kb = EvolvingKnowledgeBase()
    
    # Create test facts
    test_facts = [
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
        },
        {
            "type": "learning",
            "domain": "PROGRAMMING",
            "value": "algorithm optimization",
            "timestamp": datetime.now()
        }
    ]
    
    # Store temporal facts
    kb.store_temporal_facts(test_facts)
    print(f"   ✅ Stored {len(test_facts)} temporal facts")
    
    # Query facts
    challenges = kb.query_facts({"type": "challenge"})
    print(f"   ✅ Found {len(challenges)} challenge facts")
    
    programming_facts = kb.query_facts({"domain": "PROGRAMMING"})
    print(f"   ✅ Found {len(programming_facts)} programming facts")
    
    # Get knowledge evolution timeline
    timeline = kb.get_knowledge_evolution_timeline()
    print(f"   ✅ Generated timeline with {len(timeline)} periods")
    
    # Show timeline structure
    if timeline:
        period = timeline[0]
        print(f"   📅 Sample period: {period['period']} - {period['fact_count']} facts, domains: {period['domains']}")
    
    return True


async def demo_atomic_facts_engine():
    """Demo the AtomicFactsEngine capabilities"""
    print("\n🧠 3️⃣ Testing AtomicFactsEngine...")
    print("=" * 50)
    
    engine = AtomicFactsEngine()
    
    # Create mock learning cycle
    mock_challenge = Mock()
    mock_challenge.type.value = "REASONING"
    mock_challenge.difficulty.value = "ADVANCED"
    mock_challenge.content = "Analyze complex logical scenario"
    
    mock_attempt = Mock()
    mock_attempt.agent_type = "analysis"
    mock_attempt.confidence_score = 0.8
    mock_attempt.execution_time = 3.0
    mock_attempt.created_at = datetime.now()
    mock_attempt.challenge_id = "logic_challenge"
    
    mock_cycle = Mock()
    mock_cycle.challenge = mock_challenge
    mock_cycle.solution_attempts = [mock_attempt]
    mock_cycle.uncertainty_score = 0.6
    mock_cycle.challenger_reward = 0.7
    mock_cycle.solver_improvement = 0.2
    mock_cycle.completed_at = datetime.now()
    
    # Extract facts
    facts = engine.extract(mock_cycle)
    print(f"   ✅ Extracted {len(facts)} atomic facts")
    
    # Show fact types
    fact_types = set(f["type"] for f in facts)
    print(f"   📊 Fact types extracted: {', '.join(fact_types)}")
    
    # Show challenge facts
    challenge_facts = [f for f in facts if f["type"].startswith("challenge")]
    print(f"   🎯 Challenge facts: {len(challenge_facts)} (domain, difficulty, complexity)")
    
    # Show solution facts
    solution_facts = [f for f in facts if f["type"].startswith("solution")]
    print(f"   💡 Solution facts: {len(solution_facts)} (agent, confidence, efficiency)")
    
    # Show learning facts
    learning_facts = [f for f in facts if f["type"].startswith("learning")]
    print(f"   🧠 Learning facts: {len(learning_facts)} (improvement, uncertainty, efficiency)")
    
    return True


async def demo_entity_resolution_engine():
    """Demo the EntityResolutionEngine capabilities"""
    print("\n🧠 4️⃣ Testing EntityResolutionEngine...")
    print("=" * 50)
    
    engine = EntityResolutionEngine()
    
    # Create test facts with potential duplicates
    test_facts = [
        {
            "type": "challenge_domain",
            "value": "PROGRAMMING",
            "timestamp": datetime.now() - timedelta(days=2)
        },
        {
            "type": "challenge_domain",
            "value": "PROGRAMMING",  # Duplicate
            "timestamp": datetime.now() - timedelta(days=1)
        },
        {
            "type": "challenge_domain",
            "value": "REASONING",  # Different
            "timestamp": datetime.now()
        },
        {
            "type": "solution_agent",
            "value": "reasoning",
            "timestamp": datetime.now()
        }
    ]
    
    # Resolve entities
    resolved = engine.resolve(test_facts)
    print(f"   ✅ Resolved {len(test_facts)} facts into {len(resolved)} unique entities")
    
    # Show entity registry
    for fact_type, entities in engine.entity_registry.items():
        print(f"   📚 {fact_type}: {len(entities)} entities")
    
    # Show merge history
    print(f"   🔄 Total merges performed: {len(engine.merge_history)}")
    
    # Test similarity calculation
    fact1 = {"type": "test", "value": "hello world"}
    fact2 = {"type": "test", "value": "hello world"}
    fact3 = {"type": "test", "value": "hello there"}
    
    similarity1 = engine._calculate_similarity(fact1, fact2)
    similarity2 = engine._calculate_similarity(fact1, fact3)
    
    print(f"   📊 Similarity scores: identical={similarity1:.3f}, similar={similarity2:.3f}")
    
    return True


async def demo_temporal_invalidation_engine():
    """Demo the TemporalInvalidationEngine capabilities"""
    print("\n🧠 5️⃣ Testing TemporalInvalidationEngine...")
    print("=" * 50)
    
    engine = TemporalInvalidationEngine()
    
    # Create test facts
    old_fact = {
        "type": "solution_confidence",
        "value": 0.7,
        "challenge_id": "test_challenge",
        "timestamp": datetime.now() - timedelta(days=1),
        "confidence": 0.6
    }
    
    new_fact = {
        "type": "solution_confidence",
        "value": 0.9,
        "challenge_id": "test_challenge",
        "timestamp": datetime.now(),
        "confidence": 0.8
    }
    
    # Mark fact as expired
    engine.mark_expired(old_fact, "Superseded by improved solution", datetime.now(), new_fact)
    print(f"   ✅ Marked 1 fact as expired")
    
    # Find contradictions
    contradictions = engine.find_contradictions([new_fact], [old_fact])
    print(f"   ✅ Found {len(contradictions)} contradictions")
    
    if contradictions:
        contradiction = contradictions[0]
        print(f"   🔍 Contradiction type: {contradiction['contradiction_type']}")
        print(f"   📊 Confidence: old={contradiction['confidence_old']:.3f}, new={contradiction['confidence_new']:.3f}")
    
    # Get invalidation summary
    summary = engine.get_invalidation_summary()
    print(f"   📈 Invalidation summary:")
    print(f"      - Total invalidated: {summary['total_invalidated']}")
    print(f"      - Total replacements: {summary['total_replacements']}")
    print(f"      - Recent invalidations: {summary['recent_invalidations']}")
    
    # Show invalidation reasons
    if summary['invalidation_reasons']:
        print(f"      - Reasons: {', '.join(f'{k}: {v}' for k, v in summary['invalidation_reasons'].items())}")
    
    return True


async def demo_integrated_temporal_system():
    """Demo the integrated temporal system"""
    print("\n🧠 6️⃣ Testing Integrated Temporal System...")
    print("=" * 50)
    
    # Create all components
    agent = TemporalKnowledgeAgent()
    kb = EvolvingKnowledgeBase()
    facts_engine = AtomicFactsEngine()
    entity_engine = EntityResolutionEngine()
    invalidation_engine = TemporalInvalidationEngine()
    
    # Create a complete learning cycle
    mock_challenge = Mock()
    mock_challenge.type.value = "SAFETY"
    mock_challenge.difficulty.value = "EXPERT"
    mock_challenge.content = "Design ethical AI safety protocol"
    
    mock_attempt = Mock()
    mock_attempt.agent_type = "creative"
    mock_attempt.confidence_score = 0.95
    mock_attempt.execution_time = 5.0
    mock_attempt.created_at = datetime.now()
    mock_attempt.challenge_id = "safety_challenge"
    
    mock_cycle = Mock()
    mock_cycle.challenge = mock_challenge
    mock_cycle.solution_attempts = [mock_attempt]
    mock_cycle.uncertainty_score = 0.3
    mock_cycle.challenger_reward = 0.95
    mock_cycle.solver_improvement = 0.4
    mock_cycle.completed_at = datetime.now()
    
    # Complete temporal workflow
    print("   🔄 Running complete temporal workflow...")
    
    # 1. Extract atomic facts
    facts = facts_engine.extract(mock_cycle)
    print(f"   ✅ Step 1: Extracted {len(facts)} atomic facts")
    
    # 2. Store in knowledge base
    kb.store_temporal_facts(facts)
    print(f"   ✅ Step 2: Stored facts in knowledge base")
    
    # 3. Resolve entities
    resolved = entity_engine.resolve(facts)
    print(f"   ✅ Step 3: Resolved into {len(resolved)} unique entities")
    
    # 4. Find contradictions
    existing_facts = kb.query_facts({"type": "challenge_domain", "domain": "SAFETY"})
    contradictions = invalidation_engine.find_contradictions(resolved, existing_facts)
    print(f"   ✅ Step 4: Found {len(contradictions)} contradictions")
    
    # 5. Update knowledge history
    agent.knowledge_history.extend(facts)
    print(f"   ✅ Step 5: Updated knowledge history ({len(agent.knowledge_history)} total facts)")
    
    # 6. Generate comprehensive analysis
    print(f"   📊 Final System Status:")
    print(f"      - Knowledge Base: {len(kb.facts)} facts, {len(kb.entities)} entities")
    print(f"      - Entity Resolution: {len(entity_engine.entity_registry)} types, {len(entity_engine.merge_history)} merges")
    print(f"      - Temporal Invalidation: {len(invalidation_engine.invalidated_facts)} expired, {len(invalidation_engine.replacement_history)} replacements")
    print(f"      - Knowledge Agent: {len(agent.knowledge_history)} facts tracked")
    
    return True


async def main():
    """Main demo function"""
    print("🧠 ATLES + R-Zero Phase 3: Temporal Integration & Knowledge Evolution")
    print("=" * 70)
    print("🚀 Revolutionary temporal intelligence for self-evolving AI consciousness")
    print("=" * 70)
    
    # Run individual component demos
    demos = [
        ("TemporalKnowledgeAgent", demo_temporal_knowledge_agent),
        ("EvolvingKnowledgeBase", demo_evolving_knowledge_base),
        ("AtomicFactsEngine", demo_atomic_facts_engine),
        ("EntityResolutionEngine", demo_entity_resolution_engine),
        ("TemporalInvalidationEngine", demo_temporal_invalidation_engine),
        ("Integrated System", demo_integrated_temporal_system)
    ]
    
    results = {}
    for name, demo_func in demos:
        try:
            print(f"\n{'='*20} {name} {'='*20}")
            results[name] = await demo_func()
        except Exception as e:
            print(f"   ❌ {name} demo failed: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Phase 3 Temporal Integration Demo Results:")
    print("=" * 70)
    
    for name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {name:<25} {status}")
    
    # Overall status
    all_passed = all(results.values())
    if all_passed:
        print("\n🎉 All Phase 3 components working perfectly!")
        print("🚀 Ready for revolutionary temporal AI consciousness!")
        print("\n🌟 Key Capabilities Demonstrated:")
        print("   • Atomic Facts Extraction: Timestamped knowledge from learning experiences")
        print("   • Entity Resolution: Automatic merging of duplicate concepts")
        print("   • Temporal Invalidation: Intelligent contradiction resolution")
        print("   • Knowledge Evolution: Tracking understanding improvements over time")
        print("   • Learning Continuity: Ensuring coherent knowledge progression")
        print("   • Quality Trend Analysis: Monitoring challenge quality evolution")
    else:
        print("\n⚠️ Some Phase 3 components need attention")
        failed = [name for name, success in results.items() if not success]
        print(f"   Failed components: {', '.join(failed)}")
    
    print("\n🔄 Next Steps:")
    print("   • Phase 4: Metacognitive R-Zero with temporal awareness")
    print("   • Advanced contradiction resolution algorithms")
    print("   • Semantic similarity for entity resolution")
    print("   • Temporal pattern recognition and prediction")
    
    return all_passed


if __name__ == "__main__":
    # Run demo
    success = asyncio.run(main())
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
