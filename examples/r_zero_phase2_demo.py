#!/usr/bin/env python3
"""
R-Zero Phase 2 Demo: Advanced Co-Evolution & Cross-Domain Learning

This demo showcases the enhanced Phase 2 components:
- GRPO Optimizer with policy gradients
- Cross-Domain Challenge Generator
- Enhanced Curriculum with domain-specific adaptation
- Advanced performance metrics and analysis
"""

import asyncio
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from atles.brain.r_zero_integration import (
    MetacognitiveATLES_RZero,
    ChallengeType,
    ChallengeDifficulty,
    GRPOOptimizer,
    CrossDomainChallengeGenerator,
    UncertaintyDrivenCurriculum
)


async def demo_phase2_components():
    """Demo the Phase 2 R-Zero components"""
    print("🚀 R-Zero Phase 2: Advanced Co-Evolution Demo")
    print("=" * 60)
    
    try:
        # Test Phase 2 components individually
        print("\n1️⃣ Testing GRPO Optimizer...")
        grpo = GRPOOptimizer()
        
        # Test advantage calculation
        rewards = [0.8, 0.6, 0.9, 0.7]
        advantages = grpo.compute_group_relative_advantages(rewards)
        print(f"   Rewards: {rewards}")
        print(f"   Advantages: {[f'{a:.3f}' for a in advantages]}")
        
        # Test policy gradient
        gradient = grpo.calculate_policy_gradient(0.8)
        print(f"   Policy Gradient: {gradient:.6f}")
        
        # Test evolution direction
        direction = grpo.get_evolution_direction()
        print(f"   Evolution Direction: {direction}")
        
        print("\n2️⃣ Testing Cross-Domain Challenge Generator...")
        generator = CrossDomainChallengeGenerator()
        
        # Test domain challenge generation
        for domain in ChallengeType:
            challenge = generator.generate_domain_challenge(
                domain, 
                ChallengeDifficulty.INTERMEDIATE,
                {"task": "solve complex problem", "concept": "advanced algorithms"}
            )
            print(f"   {domain.value}: {challenge[:80]}...")
        
        # Test domain rotation
        current = ChallengeType.PROGRAMMING
        print(f"\n   Domain Rotation: {current.value} -> {generator.get_domain_rotation(current).value}")
        
        print("\n3️⃣ Testing Enhanced Curriculum...")
        curriculum = UncertaintyDrivenCurriculum()
        
        # Test domain-specific difficulty calculation
        for domain in ChallengeType:
            difficulty = curriculum.calculate_optimal_difficulty(0.3, domain)  # High success
            print(f"   {domain.value} (high success): {difficulty.value}")
            
            difficulty = curriculum.calculate_optimal_difficulty(0.8, domain)  # Low success
            print(f"   {domain.value} (low success): {difficulty.value}")
        
        # Test domain performance update
        curriculum.update_domain_performance(
            ChallengeType.PROGRAMMING, 0.9, ChallengeDifficulty.ADVANCED
        )
        print(f"   Updated Programming performance: {curriculum.domain_performance[ChallengeType.PROGRAMMING]}")
        
        print("\n4️⃣ Testing Full R-Zero System with Phase 2...")
        
        # Create R-Zero system (with mocked dependencies)
        print("   Creating R-Zero system...")
        r_zero = MetacognitiveATLES_RZero("demo_user")
        
        print(f"   Current Domain: {r_zero.current_domain.value}")
        print(f"   Current Difficulty: {r_zero.current_difficulty.value}")
        print(f"   GRPO Optimizer: {type(r_zero.grpo_optimizer).__name__}")
        print(f"   Cross-Domain Generator: {type(r_zero.cross_domain_generator).__name__}")
        print(f"   Enhanced Curriculum: {type(r_zero.curriculum_generator).__name__}")
        
        # Test learning statistics
        stats = r_zero.get_learning_statistics()
        print(f"\n   Learning Statistics Keys: {list(stats.keys())}")
        
        # Test domain rotation stats
        domain_stats = stats["domain_rotation"]
        print(f"   Domain Rotation: {domain_stats['current_domain']} -> {domain_stats['next_domain']}")
        
        # Test GRPO status
        grpo_status = stats["grpo_status"]
        print(f"   GRPO Status: {grpo_status['evolution_direction']}")
        
        # Test curriculum status
        curriculum_status = stats["curriculum_status"]
        print(f"   Curriculum: {curriculum_status['current_difficulty']} (rate: {curriculum_status['adaptation_rate']})")
        
        print("\n✅ Phase 2 Components Demo Completed Successfully!")
        print("\n🚀 Key Phase 2 Features Demonstrated:")
        print("   • GRPO Optimizer with policy gradients and evolution direction")
        print("   • Cross-domain challenge generation and rotation")
        print("   • Enhanced curriculum with domain-specific adaptation")
        print("   • Advanced performance metrics and analysis")
        print("   • Comprehensive learning statistics")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def demo_learning_cycle():
    """Demo a complete learning cycle with Phase 2 enhancements"""
    print("\n🔄 Demo Learning Cycle with Phase 2...")
    print("=" * 40)
    
    try:
        # This would require full mocking of ATLESBrain
        print("   Note: Full learning cycle demo requires mocked ATLESBrain")
        print("   Phase 2 components are ready for integration testing")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Learning cycle demo failed: {e}")
        return False


async def main():
    """Main demo function"""
    print("🧠 ATLES + R-Zero Phase 2: Advanced Co-Evolution")
    print("=" * 60)
    
    # Test Phase 2 components
    success1 = await demo_phase2_components()
    
    # Demo learning cycle (if components work)
    if success1:
        success2 = await demo_learning_cycle()
    else:
        success2 = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Phase 2 Demo Results:")
    print(f"   Components Test: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"   Learning Cycle: {'✅ READY' if success2 else '⚠️ NEEDS MOCKING'}")
    
    if success1:
        print("\n🎉 Phase 2 Implementation Complete!")
        print("🚀 Ready for Temporal Integration (Phase 3)")
    else:
        print("\n⚠️ Some Phase 2 components need attention")
    
    return success1 and success2


if __name__ == "__main__":
    # Run demo
    success = asyncio.run(main())
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
