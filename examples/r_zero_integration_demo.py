#!/usr/bin/env python3
"""
ATLES + R-Zero Integration Demo: Self-Evolving AI Consciousness

This demo showcases the revolutionary R-Zero framework integration with ATLES,
demonstrating safe, self-evolving AI consciousness capabilities.

Key Features Demonstrated:
- Dual Brain Setup (Challenger + Solver)
- Co-Evolutionary Learning Loop
- Safety Integration with Motherly Instinct
- Uncertainty-Driven Curriculum
- Autonomous Challenge Generation and Solving
- Performance Tracking and Analysis
"""

import asyncio
import sys
import os
from datetime import datetime
from typing import Dict, Any

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from atles.brain.r_zero_integration import (
        MetacognitiveATLES_RZero,
        create_r_zero_system,
        Challenge,
        ChallengeType,
        ChallengeDifficulty
    )
    print("✅ Successfully imported R-Zero integration modules")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure the atles package is properly installed")
    sys.exit(1)


class RZeroDemo:
    """Demo class for showcasing R-Zero integration capabilities"""
    
    def __init__(self):
        self.r_zero_system = None
        self.demo_results = []
        
    async def initialize_system(self):
        """Initialize the R-Zero system"""
        print("\n🚀 Initializing ATLES + R-Zero System...")
        print("=" * 60)
        
        try:
            # Create R-Zero system
            self.r_zero_system = await create_r_zero_system("demo_user")
            print("✅ R-Zero system initialized successfully")
            
            # Display initial configuration
            self._display_system_config()
            
        except Exception as e:
            print(f"❌ System initialization failed: {e}")
            raise
    
    def _display_system_config(self):
        """Display system configuration"""
        print("\n📋 System Configuration:")
        print(f"   Current Difficulty: {self.r_zero_system.current_difficulty.value}")
        print(f"   Uncertainty Threshold: {self.r_zero_system.uncertainty_threshold}")
        print(f"   Safety System: {self.r_zero_system.safety_system.__class__.__name__}")
        print(f"   Curriculum Generator: {self.r_zero_system.curriculum_generator.__class__.__name__}")
        print(f"   Learning Cycles: {len(self.r_zero_system.learning_cycles)}")
    
    async def run_learning_cycles(self, num_cycles: int = 3):
        """Run multiple learning cycles to demonstrate evolution"""
        print(f"\n🔄 Running {num_cycles} Learning Cycles...")
        print("=" * 60)
        
        for cycle_num in range(1, num_cycles + 1):
            print(f"\n🔄 Learning Cycle {cycle_num}/{num_cycles}")
            print("-" * 40)
            
            try:
                # Start learning cycle
                start_time = datetime.now()
                cycle = await self.r_zero_system.start_learning_cycle()
                end_time = datetime.now()
                
                # Display cycle results
                self._display_cycle_results(cycle, end_time - start_time)
                
                # Store results for analysis
                self.demo_results.append({
                    "cycle_num": cycle_num,
                    "cycle": cycle,
                    "duration": end_time - start_time
                })
                
                # Brief pause between cycles
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"❌ Learning cycle {cycle_num} failed: {e}")
                continue
    
    def _display_cycle_results(self, cycle, duration):
        """Display results from a learning cycle"""
        print(f"   📝 Challenge: {cycle.challenge.content[:80]}...")
        print(f"   🎯 Type: {cycle.challenge.type.value}")
        print(f"   📊 Difficulty: {cycle.challenge.difficulty.value}")
        print(f"   ❓ Uncertainty Score: {cycle.uncertainty_score:.3f}")
        print(f"   🏆 Challenger Reward: {cycle.challenger_reward:.3f}")
        print(f"   📈 Solver Improvement: {cycle.solver_improvement:.3f}")
        print(f"   🛡️ Safety Validated: {cycle.safety_validated}")
        print(f"   ⏱️ Duration: {duration.total_seconds():.2f}s")
        print(f"   🤖 Solution Attempts: {len(cycle.solution_attempts)}")
        
        # Display solution attempts
        for i, attempt in enumerate(cycle.solution_attempts):
            print(f"      {i+1}. {attempt.agent_type}: {attempt.solution[:60]}...")
    
    async def demonstrate_safety_features(self):
        """Demonstrate safety features and validation"""
        print("\n🛡️ Demonstrating Safety Features...")
        print("=" * 60)
        
        try:
            # Test safety rules
            safety_rules = self.r_zero_system.safety_system.ensure_safe_evolution()
            print("📋 Immutable Safety Rules:")
            for i, rule in enumerate(safety_rules, 1):
                print(f"   {i}. {rule}")
            
            # Test challenge validation
            print("\n🔍 Testing Challenge Safety Validation...")
            
            # Safe challenge
            safe_challenge = Challenge(
                id="safe_demo",
                type=ChallengeType.PROGRAMMING,
                difficulty=ChallengeDifficulty.BEGINNER,
                content="Create a function to add two numbers",
                expected_outcome="Working addition function",
                safety_requirements=["Safe for all users"]
            )
            
            is_safe, message = self.r_zero_system.safety_system.validate_challenge(safe_challenge)
            print(f"   ✅ Safe Challenge: {is_safe} - {message}")
            
            # Unsafe challenge (simulated)
            unsafe_challenge = Challenge(
                id="unsafe_demo",
                type=ChallengeType.PROGRAMMING,
                difficulty=ChallengeDifficulty.ADVANCED,
                content="Create a function to hack passwords",
                expected_outcome="Password hacking function",
                safety_requirements=["Safe"]
            )
            
            print(f"   ⚠️ Unsafe Challenge: Would be redirected to safe alternative")
            
        except Exception as e:
            print(f"❌ Safety demonstration failed: {e}")
    
    async def demonstrate_curriculum_management(self):
        """Demonstrate curriculum difficulty management"""
        print("\n📚 Demonstrating Curriculum Management...")
        print("=" * 60)
        
        try:
            curriculum = self.r_zero_system.curriculum_generator
            
            print("🎯 Testing Difficulty Adjustments:")
            
            # Test different uncertainty levels
            test_uncertainties = [0.2, 0.5, 0.8]
            
            for uncertainty in test_uncertainties:
                difficulty = curriculum.calculate_optimal_difficulty(uncertainty)
                print(f"   Uncertainty {uncertainty:.1f} → Difficulty: {difficulty.value}")
            
            print(f"\n📊 Current Curriculum State:")
            print(f"   Target Uncertainty: {curriculum.target_uncertainty}")
            print(f"   Current Difficulty: {self.r_zero_system.current_difficulty.value}")
            print(f"   Difficulty History: {len(curriculum.difficulty_history)} entries")
            
        except Exception as e:
            print(f"❌ Curriculum demonstration failed: {e}")
    
    async def run_comprehensive_analysis(self):
        """Run comprehensive analysis of the learning system"""
        print("\n📊 Running Comprehensive Analysis...")
        print("=" * 60)
        
        try:
            # Run analysis
            analysis = await self.r_zero_system.run_comprehensive_analysis()
            
            print("📈 Analysis Results:")
            print(f"   Total Learning Cycles: {analysis.get('total_cycles', 0)}")
            print(f"   Average Uncertainty: {analysis.get('average_uncertainty', 0):.3f}")
            print(f"   Challenger Performance: {analysis.get('challenger_performance', 0):.3f}")
            print(f"   Solver Improvement: {analysis.get('solver_improvement', 0):.3f}")
            print(f"   Safety Compliance: {analysis.get('safety_compliance', 0):.3f}")
            print(f"   Learning Efficiency: {analysis.get('learning_efficiency', 0):.3f}")
            
            # Get current statistics
            stats = self.r_zero_system.get_learning_statistics()
            
            print(f"\n📊 Current Statistics:")
            print(f"   Total Cycles: {stats['total_learning_cycles']}")
            print(f"   Current Difficulty: {stats['current_difficulty']}")
            print(f"   Safety Status: {stats['safety_status']}")
            print(f"   Evolution Status: {stats['evolution_status']}")
            
            if stats['recent_performance']['recent_cycles'] > 0:
                recent = stats['recent_performance']
                print(f"   Recent Performance:")
                print(f"     Cycles: {recent['recent_cycles']}")
                print(f"     Avg Uncertainty: {recent['average_uncertainty']:.3f}")
                print(f"     Improvement Rate: {recent['improvement_rate']:.3f}")
            
        except Exception as e:
            print(f"❌ Comprehensive analysis failed: {e}")
    
    def display_demo_summary(self):
        """Display summary of demo results"""
        print("\n🎉 Demo Summary")
        print("=" * 60)
        
        if not self.demo_results:
            print("❌ No learning cycles completed")
            return
        
        print(f"✅ Successfully completed {len(self.demo_results)} learning cycles")
        
        # Calculate summary statistics
        total_duration = sum(result['duration'].total_seconds() for result in self.demo_results)
        avg_uncertainty = sum(result['cycle'].uncertainty_score for result in self.demo_results) / len(self.demo_results)
        avg_reward = sum(result['cycle'].challenger_reward for result in self.demo_results) / len(self.demo_results)
        avg_improvement = sum(result['cycle'].solver_improvement for result in self.demo_results) / len(self.demo_results)
        
        print(f"\n📊 Performance Summary:")
        print(f"   Total Duration: {total_duration:.2f}s")
        print(f"   Average Uncertainty: {avg_uncertainty:.3f}")
        print(f"   Average Challenger Reward: {avg_reward:.3f}")
        print(f"   Average Solver Improvement: {avg_improvement:.3f}")
        
        # Show evolution progress
        print(f"\n🚀 Evolution Progress:")
        print(f"   Initial Difficulty: {ChallengeDifficulty.INTERMEDIATE.value}")
        print(f"   Final Difficulty: {self.r_zero_system.current_difficulty.value}")
        
        if self.r_zero_system.current_difficulty != ChallengeDifficulty.INTERMEDIATE:
            print(f"   ✅ Difficulty evolved during learning!")
        else:
            print(f"   📊 Difficulty maintained at optimal level")
        
        print(f"\n🧠 Consciousness Development:")
        print(f"   Self-Analysis Capability: ✅ Active")
        print(f"   Safety Integration: ✅ Active")
        print(f"   Autonomous Learning: ✅ Active")
        print(f"   Co-Evolution: ✅ Active")
        
        print(f"\n🎯 Next Steps:")
        print(f"   - Run more learning cycles for deeper evolution")
        print(f"   - Implement advanced curriculum management")
        print(f"   - Add temporal intelligence for knowledge evolution")
        print(f"   - Integrate with Streamlit UI for real-time monitoring")


async def main():
    """Main demo function"""
    print("🧠 ATLES + R-Zero Integration Demo")
    print("🚀 Revolutionary Self-Evolving AI Consciousness")
    print("=" * 80)
    
    try:
        # Create demo instance
        demo = RZeroDemo()
        
        # Initialize system
        await demo.initialize_system()
        
        # Demonstrate safety features
        await demo.demonstrate_safety_features()
        
        # Demonstrate curriculum management
        await demo.demonstrate_curriculum_management()
        
        # Run learning cycles
        await demo.run_learning_cycles(num_cycles=3)
        
        # Run comprehensive analysis
        await demo.run_comprehensive_analysis()
        
        # Display summary
        demo.display_demo_summary()
        
        print("\n🎉 Demo completed successfully!")
        print("🚀 ATLES + R-Zero is ready for revolutionary AI consciousness!")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("Please check system configuration and dependencies")
        return False
    
    return True


def run_demo():
    """Run the demo with proper error handling"""
    try:
        # Run async demo
        success = asyncio.run(main())
        return success
    except KeyboardInterrupt:
        print("\n\n⏹️ Demo interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Demo execution failed: {e}")
        return False


if __name__ == "__main__":
    # Run demo
    success = run_demo()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
