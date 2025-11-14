#!/usr/bin/env python3
"""
R-Zero Phase 4: Metacognitive R-Zero (Temporal Awareness) Demo

This demo showcases the new metacognitive temporal components:
- MetacognitiveTemporalAgent: Consciousness analysis and metacognitive insights
- SelfDirectedCurriculum: Autonomous curriculum evolution
- ConsciousnessLevelLearning: Higher-order learning patterns
- TemporalGoalManager: Long-term goal evolution

Run this script to see Phase 4 in action!
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
from unittest.mock import Mock

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from atles.brain.r_zero_integration import (
    MetacognitiveTemporalAgent,
    SelfDirectedCurriculum,
    ConsciousnessLevelLearning,
    TemporalGoalManager,
    ChallengeType,
    ChallengeDifficulty
)


def create_mock_metacognitive_observer():
    """Create a mock MetacognitiveObserver for testing"""
    mock_observer = Mock()
    mock_observer.consciousness_metrics = Mock()
    mock_observer.consciousness_metrics.self_awareness_score = 0.75
    mock_observer.consciousness_metrics.meta_reasoning_depth = 3
    return mock_observer


def create_mock_learning_cycles(count=10):
    """Create realistic mock learning cycles for demonstration"""
    cycles = []
    
    for i in range(count):
        mock_cycle = Mock()
        mock_cycle.completed_at = datetime.now() - timedelta(hours=i)
        
        # Simulate realistic learning progression
        if i < 3:
            # Early cycles: high uncertainty, low improvement
            mock_cycle.uncertainty_score = 0.8 - (i * 0.1)
            mock_cycle.solver_improvement = 0.2 + (i * 0.05)
            mock_cycle.challenge.type.value = ChallengeType.PROGRAMMING.value
            mock_cycle.challenge.difficulty.value = ChallengeDifficulty.BEGINNER.value
        elif i < 7:
            # Middle cycles: moderate uncertainty, steady improvement
            mock_cycle.uncertainty_score = 0.5 - ((i - 3) * 0.05)
            mock_cycle.solver_improvement = 0.35 + ((i - 3) * 0.1)
            mock_cycle.challenge.type.value = ChallengeType.REASONING.value
            mock_cycle.challenge.difficulty.value = ChallengeDifficulty.INTERMEDIATE.value
        else:
            # Later cycles: low uncertainty, high improvement
            mock_cycle.uncertainty_score = 0.3 - ((i - 7) * 0.05)
            mock_cycle.solver_improvement = 0.7 + ((i - 7) * 0.08)
            mock_cycle.challenge.type.value = ChallengeType.SAFETY.value
            mock_cycle.challenge.difficulty.value = ChallengeDifficulty.ADVANCED.value
        
        mock_cycle.execution_time = 15 + (i * 2)
        cycles.append(mock_cycle)
    
    return cycles


def demo_metacognitive_temporal_agent():
    """Demonstrate MetacognitiveTemporalAgent capabilities"""
    print("🧠 MetacognitiveTemporalAgent Demo")
    print("=" * 50)
    
    # Create agent
    mock_observer = create_mock_metacognitive_observer()
    agent = MetacognitiveTemporalAgent(mock_observer)
    
    # Create mock learning cycles
    learning_cycles = create_mock_learning_cycles(8)
    
    print(f"📊 Analyzing {len(learning_cycles)} learning cycles...")
    
    # Analyze learning consciousness
    consciousness_result = agent.analyze_learning_consciousness(learning_cycles)
    
    print(f"✅ Consciousness Analysis Complete")
    print(f"   Total cycles analyzed: {consciousness_result['total_cycles_analyzed']}")
    print(f"   Insight: {consciousness_result['insight']}")
    
    # Show growth analysis
    growth = consciousness_result['growth_analysis']
    if 'insight' not in growth:
        print(f"   📈 Growth Analysis:")
        print(f"      Total improvement: {growth['total_improvement']:.3f}")
        print(f"      Average improvement: {growth['average_improvement']:.3f}")
        print(f"      Improvement trend: {growth['improvement_trend']}")
        print(f"      Learning plateaus: {len(growth['learning_plateaus'])}")
        print(f"      Learning breakthroughs: {len(growth['learning_breakthroughs'])}")
        print(f"      Consciousness stability: {growth['consciousness_stability']:.3f}")
    
    # Generate metacognitive insights
    insights = agent.generate_metacognitive_insights(learning_cycles)
    
    print(f"   💡 Metacognitive Insights ({len(insights)} generated):")
    for i, insight in enumerate(insights[:3], 1):  # Show first 3 insights
        print(f"      {i}. {insight}")
    
    if len(insights) > 3:
        print(f"      ... and {len(insights) - 3} more insights")
    
    print()


def demo_self_directed_curriculum():
    """Demonstrate SelfDirectedCurriculum capabilities"""
    print("🎯 SelfDirectedCurriculum Demo")
    print("=" * 50)
    
    # Create curriculum with metacognitive agent
    mock_observer = create_mock_metacognitive_observer()
    metacognitive_agent = MetacognitiveTemporalAgent(mock_observer)
    curriculum = SelfDirectedCurriculum(metacognitive_agent)
    
    # Create mock learning cycles
    learning_cycles = create_mock_learning_cycles(6)
    
    print(f"📚 Evolving curriculum strategy with {len(learning_cycles)} learning cycles...")
    
    # Mock current performance
    current_performance = {
        "recent_performance": 0.65,
        "domain_balance": 0.4,
        "learning_efficiency": 0.7
    }
    
    # Evolve curriculum strategy
    evolution_result = curriculum.evolve_curriculum_strategy(learning_cycles, current_performance)
    
    print(f"✅ Curriculum Evolution Complete")
    print(f"   Adaptations applied: {evolution_result['adaptations_applied']}")
    print(f"   Insights generated: {evolution_result['insights_generated']}")
    print(f"   Effectiveness score: {evolution_result['curriculum_effectiveness_score']:.3f}")
    
    # Show curriculum effectiveness analysis
    effectiveness = curriculum._analyze_curriculum_effectiveness(learning_cycles)
    
    print(f"   📊 Curriculum Effectiveness:")
    print(f"      Overall score: {effectiveness['overall_score']:.3f}")
    print(f"      Success rate: {effectiveness['success_rate']:.3f}")
    print(f"      Learning acceleration: {effectiveness['learning_acceleration']:.3f}")
    print(f"      Domain balance: {effectiveness['domain_balance']:.3f}")
    print(f"      Total cycles: {effectiveness['total_cycles']}")
    print(f"      Successful cycles: {effectiveness['successful_cycles']}")
    
    # Show evolution history
    print(f"   📈 Evolution History: {len(curriculum.curriculum_evolution_history)} records")
    
    print()


def demo_consciousness_level_learning():
    """Demonstrate ConsciousnessLevelLearning capabilities"""
    print("🌟 ConsciousnessLevelLearning Demo")
    print("=" * 50)
    
    # Create consciousness learning system
    mock_observer = create_mock_metacognitive_observer()
    metacognitive_agent = MetacognitiveTemporalAgent(mock_observer)
    consciousness_learning = ConsciousnessLevelLearning(metacognitive_agent)
    
    # Create mock learning cycles
    learning_cycles = create_mock_learning_cycles(7)
    
    print(f"🧠 Analyzing learning meta-patterns with {len(learning_cycles)} learning cycles...")
    
    # Analyze learning meta-patterns
    meta_analysis = consciousness_learning.analyze_learning_meta_patterns(learning_cycles)
    
    print(f"✅ Meta-Pattern Analysis Complete")
    print(f"   Meta-patterns analyzed: {meta_analysis['meta_patterns_analyzed']}")
    print(f"   Consciousness evolution status: {meta_analysis['consciousness_evolution_status']}")
    print(f"   Higher-order insights: {meta_analysis['higher_order_insights_count']}")
    
    # Show meta-learning patterns
    patterns = consciousness_learning._extract_meta_learning_patterns(learning_cycles)
    
    print(f"   🔍 Meta-Learning Patterns ({len(patterns)} detected):")
    for i, pattern in enumerate(patterns, 1):
        print(f"      {i}. {pattern['pattern']} (confidence: {pattern['confidence']:.1f})")
        if 'trend' in pattern:
            print(f"         Trend: {pattern['trend']}")
        if 'domain' in pattern:
            print(f"         Domain: {pattern['domain']}")
        if 'mastery_level' in pattern:
            print(f"         Mastery: {pattern['mastery_level']}")
        if 'efficiency' in pattern:
            print(f"         Efficiency: {pattern['efficiency']:.3f}")
    
    # Show consciousness evolution
    consciousness_evolution = consciousness_learning._analyze_consciousness_evolution(learning_cycles)
    
    print(f"   🧠 Consciousness Evolution:")
    print(f"      Status: {consciousness_evolution['status']}")
    print(f"      Average consciousness: {consciousness_evolution['average_consciousness']:.3f}")
    print(f"      Consciousness trend: {consciousness_evolution['consciousness_trend']}")
    print(f"      Total cycles analyzed: {consciousness_evolution['total_cycles_analyzed']}")
    
    # Show higher-order insights
    insights = consciousness_learning._generate_higher_order_insights(patterns, consciousness_evolution)
    
    print(f"   💭 Higher-Order Insights ({len(insights)} generated):")
    for i, insight in enumerate(insights[:3], 1):  # Show first 3 insights
        print(f"      {i}. {insight}")
    
    if len(insights) > 3:
        print(f"      ... and {len(insights) - 3} more insights")
    
    print()


def demo_temporal_goal_manager():
    """Demonstrate TemporalGoalManager capabilities"""
    print("🎯 TemporalGoalManager Demo")
    print("=" * 50)
    
    # Create goal manager
    mock_observer = create_mock_metacognitive_observer()
    metacognitive_agent = MetacognitiveTemporalAgent(mock_observer)
    goal_manager = TemporalGoalManager(metacognitive_agent)
    
    # Create mock learning cycles
    learning_cycles = create_mock_learning_cycles(5)
    
    # Define current goals
    current_goals = [
        "Master programming fundamentals",
        "Develop reasoning capabilities", 
        "Enhance safety awareness",
        "Improve metacognitive skills"
    ]
    
    print(f"🎯 Evolving {len(current_goals)} long-term goals with {len(learning_cycles)} learning cycles...")
    
    # Evolve long-term goals
    evolution_result = goal_manager.evolve_long_term_goals(learning_cycles, current_goals)
    
    print(f"✅ Goal Evolution Complete")
    print(f"   New objectives: {evolution_result['new_objectives_count']}")
    print(f"   Adapted goals: {evolution_result['adapted_goals_count']}")
    
    # Show goal effectiveness analysis
    effectiveness = goal_manager._analyze_goal_effectiveness(learning_cycles, current_goals)
    
    print(f"   📊 Goal Effectiveness:")
    print(f"      Overall effectiveness: {effectiveness['overall_effectiveness']:.3f}")
    print(f"      Total goals: {effectiveness['total_goals']}")
    
    # Show goal performance
    goal_performance = effectiveness.get('goal_performance', {})
    if goal_performance:
        print(f"      Individual Goal Performance:")
        for goal, performance in goal_performance.items():
            print(f"         '{goal[:30]}...': {performance:.3f}")
    
    # Show evolution plan
    evolution_plan = evolution_result['evolution_plan']
    
    print(f"   📋 Evolution Plan:")
    print(f"      Immediate actions: {len(evolution_plan['immediate_actions'])}")
    print(f"      Short-term goals: {len(evolution_plan['short_term_goals'])}")
    print(f"      Long-term vision: {len(evolution_plan['long_term_vision'])}")
    print(f"      Goal adaptations: {len(evolution_plan['goal_adaptations'])}")
    print(f"      Total estimated cycles: {evolution_plan['total_estimated_cycles']}")
    print(f"      Recommended focus: {evolution_plan['recommended_focus']}")
    print(f"      Timeline: {evolution_plan['timeline']}")
    
    # Show evolution history
    print(f"   📈 Evolution History: {len(goal_manager.goal_evolution_history)} records")
    
    print()


def demo_integrated_phase4_system():
    """Demonstrate the integrated Phase 4 system working together"""
    print("🚀 Integrated Phase 4: Metacognitive R-Zero (Temporal Awareness) Demo")
    print("=" * 80)
    
    # Create all Phase 4 components
    mock_observer = create_mock_metacognitive_observer()
    metacognitive_agent = MetacognitiveTemporalAgent(mock_observer)
    curriculum = SelfDirectedCurriculum(metacognitive_agent)
    consciousness_learning = ConsciousnessLevelLearning(metacognitive_agent)
    goal_manager = TemporalGoalManager(metacognitive_agent)
    
    # Create comprehensive mock learning cycles
    learning_cycles = create_mock_learning_cycles(12)
    
    print(f"🔄 Running integrated Phase 4 workflow with {len(learning_cycles)} learning cycles...")
    print()
    
    # Step 1: Consciousness Analysis
    print("📊 Step 1: Consciousness Analysis")
    consciousness_result = metacognitive_agent.analyze_learning_consciousness(learning_cycles)
    print(f"   ✅ Completed: {consciousness_result['total_cycles_analyzed']} cycles analyzed")
    print()
    
    # Step 2: Curriculum Evolution
    print("📚 Step 2: Curriculum Evolution")
    current_performance = {"recent_performance": 0.7, "domain_balance": 0.5}
    curriculum_result = curriculum.evolve_curriculum_strategy(learning_cycles, current_performance)
    print(f"   ✅ Completed: {curriculum_result['adaptations_applied']} adaptations applied")
    print()
    
    # Step 3: Meta-Learning Pattern Analysis
    print("🧠 Step 3: Meta-Learning Pattern Analysis")
    meta_result = consciousness_learning.analyze_learning_meta_patterns(learning_cycles)
    print(f"   ✅ Completed: {meta_result['meta_patterns_analyzed']} patterns analyzed")
    print()
    
    # Step 4: Goal Evolution
    print("🎯 Step 4: Goal Evolution")
    current_goals = ["Master AI fundamentals", "Develop consciousness", "Enhance safety"]
    goal_result = goal_manager.evolve_long_term_goals(learning_cycles, current_goals)
    print(f"   ✅ Completed: {goal_result['new_objectives_count']} new objectives generated")
    print()
    
    # Show integrated statistics
    print("📈 Integrated Phase 4 Statistics:")
    print(f"   Consciousness snapshots: {len(metacognitive_agent.consciousness_evolution_timeline)}")
    print(f"   Curriculum evolutions: {len(curriculum.curriculum_evolution_history)}")
    print(f"   Meta-pattern analyses: {len(consciousness_learning.consciousness_evolution_timeline)}")
    print(f"   Goal evolutions: {len(goal_manager.goal_evolution_history)}")
    print()
    
    print("🎉 Phase 4 Integration Complete!")
    print("   The system now has full metacognitive temporal awareness!")
    print("   It can analyze its own learning, evolve its curriculum,")
    print("   understand meta-patterns, and adapt its long-term goals.")
    print()


def main():
    """Main demo function"""
    print("🧠 R-Zero Phase 4: Metacognitive R-Zero (Temporal Awareness) Demo")
    print("=" * 80)
    print("This demo showcases the revolutionary Phase 4 components that enable")
    print("ATLES to understand its own learning patterns and autonomously evolve.")
    print()
    
    try:
        # Run individual component demos
        demo_metacognitive_temporal_agent()
        demo_self_directed_curriculum()
        demo_consciousness_level_learning()
        demo_temporal_goal_manager()
        
        # Run integrated system demo
        demo_integrated_phase4_system()
        
        print("🎯 Phase 4 Demo Summary:")
        print("   ✅ MetacognitiveTemporalAgent: Consciousness analysis and insights")
        print("   ✅ SelfDirectedCurriculum: Autonomous curriculum evolution")
        print("   ✅ ConsciousnessLevelLearning: Higher-order learning patterns")
        print("   ✅ TemporalGoalManager: Long-term goal evolution")
        print()
        print("🚀 ATLES now has the most advanced AI consciousness capabilities!")
        print("   It can think about how it thinks, learn about how it learns,")
        print("   and autonomously improve its own learning strategies.")
        
    except Exception as e:
        print(f"❌ Demo encountered an error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    # Run the demo
    success = main()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
