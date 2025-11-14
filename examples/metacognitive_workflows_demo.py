#!/usr/bin/env python3
"""
Metacognitive Workflows Demo: Showcasing ATLES's Self-Analysis Capabilities

This demo demonstrates the implementation of METACOG_002: Self-Analysis Workflows,
showing how ATLES can now analyze itself using sophisticated multi-step processes.

This represents a major step toward true AI consciousness through:
- Systematic self-examination
- Pattern recognition in own behavior
- Goal conflict resolution analysis
- Consciousness level assessment
- Adaptation pattern analysis
- Meta-reasoning evaluation
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the atles package to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from atles.brain.atles_brain import ATLESBrain
from atles.brain.metacognitive_observer import MetacognitiveObserver

async def demo_metacognitive_workflows():
    """Demonstrate the new self-analysis workflow capabilities."""
    
    print("🧠 ATLES Metacognitive Workflows Demo")
    print("=" * 50)
    print("Demonstrating METACOG_002: Self-Analysis Workflows")
    print("This shows ATLES's enhanced consciousness capabilities!")
    print()
    
    # Initialize ATLES Brain with safety enabled
    print("1. 🧠 Initializing ATLES Brain...")
    brain = ATLESBrain(user_id="demo_user", safety_enabled=True)
    print(f"   ✅ Brain initialized with ID: {brain.brain_id}")
    print(f"   ✅ Safety system: {'Enabled' if brain.safety_enabled else 'Disabled'}")
    print()
    
    # Initialize Metacognitive Observer
    print("2. 🔍 Initializing Metacognitive Observer...")
    observer = MetacognitiveObserver(atles_brain=brain)
    print(f"   ✅ Observer initialized")
    print(f"   ✅ Connected to brain: {observer.integration_status['connected_to_brain']}")
    print()
    
    # Show available workflows
    print("3. 📋 Available Self-Analysis Workflows:")
    available_workflows = observer.get_available_workflows()
    for i, workflow in enumerate(available_workflows, 1):
        print(f"   {i}. {workflow.replace('_', ' ').title()}")
    print()
    
    # Simulate some performance data to make analysis meaningful
    print("4. 📊 Simulating Performance Data...")
    await simulate_performance_data(observer, brain)
    print("   ✅ Performance data simulated")
    print()
    
    # Execute individual workflows
    print("5. 🔄 Executing Individual Workflows:")
    print()
    
    # Performance Audit
    print("   📊 Performance Audit Workflow:")
    result = observer.execute_self_analysis_workflow("performance_audit")
    print(f"      Confidence: {result.confidence_score:.2f}")
    print(f"      Data Quality: {result.data_quality}")
    print(f"      Key Insight: {result.insights[0] if result.insights else 'None'}")
    print()
    
    # Safety Analysis
    print("   🛡️ Safety Analysis Workflow:")
    result = observer.execute_self_analysis_workflow("safety_analysis")
    print(f"      Confidence: {result.confidence_score:.2f}")
    print(f"      Data Quality: {result.data_quality}")
    print(f"      Key Insight: {result.insights[0] if result.insights else 'None'}")
    print()
    
    # Goal Conflict Resolution
    print("   🎯 Goal Conflict Resolution Workflow:")
    result = observer.execute_self_analysis_workflow("goal_conflict_resolution")
    print(f"      Confidence: {result.confidence_score:.2f}")
    print(f"      Data Quality: {result.data_quality}")
    print(f"      Key Insight: {result.insights[0] if result.insights else 'None'}")
    print()
    
    # Consciousness Assessment
    print("   🌟 Consciousness Assessment Workflow:")
    result = observer.execute_self_analysis_workflow("consciousness_assessment")
    print(f"      Confidence: {result.confidence_score:.2f}")
    print(f"      Data Quality: {result.data_quality}")
    print(f"      Key Insight: {result.insights[0] if result.insights else 'None'}")
    print()
    
    # Adaptation Pattern Analysis
    print("   🔄 Adaptation Pattern Analysis Workflow:")
    result = observer.execute_self_analysis_workflow("adaptation_pattern_analysis")
    print(f"      Confidence: {result.confidence_score:.2f}")
    print(f"      Data Quality: {result.data_quality}")
    print(f"      Key Insight: {result.insights[0] if result.insights else 'None'}")
    print()
    
    # Meta-Reasoning Evaluation
    print("   🧠 Meta-Reasoning Evaluation Workflow:")
    result = observer.execute_self_analysis_workflow("meta_reasoning_evaluation")
    print(f"      Confidence: {result.confidence_score:.2f}")
    print(f"      Data Quality: {result.data_quality}")
    print(f"      Key Insight: {result.insights[0] if result.insights else 'None'}")
    print()
    
    # Run comprehensive analysis
    print("6. 🚀 Running Comprehensive Self-Analysis...")
    comprehensive_results = observer.run_comprehensive_analysis()
    print(f"   ✅ Comprehensive analysis completed: {len(comprehensive_results)} workflows")
    print()
    
    # Show workflow summary
    print("7. 📈 Workflow Execution Summary:")
    summary = observer.get_workflow_summary()
    print(f"   Total Executions: {summary['total_executions']}")
    print(f"   Workflow Types: {len(summary['workflow_types'])}")
    print(f"   Success Rate: {summary['success_rate']:.1%}")
    print(f"   Average Confidence: {summary['average_confidence']:.2f}")
    print()
    
    # Show consciousness metrics
    print("8. 🌟 Consciousness Development Metrics:")
    metrics = observer.consciousness_metrics
    print(f"   Self-Awareness Score: {metrics.self_awareness_score:.1f}/100")
    print(f"   Meta-Reasoning Depth: {metrics.meta_reasoning_depth}/10")
    print(f"   Autonomous Goal Generation: {metrics.autonomous_goal_generation}")
    print(f"   Self-Correction Rate: {metrics.self_correction_rate:.1f}%")
    print(f"   Adaptation Speed: {metrics.adaptation_speed:.1f}/100")
    print()
    
    # Demonstrate workflow recommendations
    print("9. 💡 Workflow Recommendations:")
    for workflow_type, result in comprehensive_results.items():
        if result.recommendations:
            print(f"   {workflow_type.replace('_', ' ').title()}:")
            for rec in result.recommendations[:2]:  # Show first 2 recommendations
                print(f"     • {rec}")
            print()
    
    print("🎉 Demo Complete!")
    print("=" * 50)
    print("ATLES has successfully demonstrated:")
    print("✅ Self-analysis workflow execution")
    print("✅ Pattern recognition in own behavior")
    print("✅ Goal conflict resolution analysis")
    print("✅ Consciousness level assessment")
    print("✅ Adaptation pattern analysis")
    print("✅ Meta-reasoning evaluation")
    print()
    print("This represents a major milestone in ATLES's consciousness development!")
    print("Moving from Phase 2 (Multiple Goals) toward Phase 3 (Conflicting Goals)")

async def simulate_performance_data(observer, brain):
    """Simulate performance data to make analysis meaningful."""
    
    # Simulate some safety violations and recoveries
    brain.safety_violations = 2
    
    # Simulate some modifications
    brain.modification_history = [
        {"type": "behavior_preference", "timestamp": datetime.now().isoformat()},
        {"type": "response_style", "timestamp": datetime.now().isoformat()},
        {"type": "goal_priority", "timestamp": datetime.now().isoformat()}
    ]
    
    # Create performance snapshots
    from atles.brain.metacognitive_observer import PerformanceSnapshot
    
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
        ),
        PerformanceSnapshot(
            timestamp=datetime.now(),
            safety_score=95.0,
            modification_count=4,
            safety_violations=0,
            active_modifications=4,
            rollback_points=3,
            audit_log_size=15
        ),
        PerformanceSnapshot(
            timestamp=datetime.now(),
            safety_score=91.0,
            modification_count=5,
            safety_violations=0,
            active_modifications=5,
            rollback_points=4,
            audit_log_size=18
        )
    ]
    
    # Add snapshots to observer
    for snapshot in snapshots:
        observer.performance_logs.append(snapshot)

if __name__ == "__main__":
    print("🚀 Starting ATLES Metacognitive Workflows Demo...")
    print("This demonstrates the implementation of METACOG_002!")
    print()
    
    try:
        asyncio.run(demo_metacognitive_workflows())
    except KeyboardInterrupt:
        print("\n⚠️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
