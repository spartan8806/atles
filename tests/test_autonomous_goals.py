#!/usr/bin/env python3
"""
Test the new autonomous goal system vs old repetitive behavior
"""

import asyncio
from autonomous_goal_system import AutonomousGoalSystem

async def demonstrate_real_autonomous_behavior():
    """Show what real autonomous behavior looks like"""
    
    print("🎯 ATLES Autonomous Goal System Demo")
    print("=" * 50)
    
    goal_system = AutonomousGoalSystem()
    
    # Generate and pursue 3 different goals
    for i in range(3):
        print(f"\n🔄 Cycle {i+1}: Generating new autonomous goal...")
        
        # Generate a new goal
        goal = await goal_system.generate_new_goal()
        goal_system.active_goals.append(goal)
        
        print(f"📋 Goal Generated:")
        print(f"   Title: {goal['title']}")
        print(f"   Type: {goal['type']}")
        print(f"   Priority: {goal['priority']}")
        print(f"   Description: {goal['description']}")
        print(f"   Estimated Duration: {goal['estimated_duration']/60:.1f} minutes")
        
        print(f"\n🚀 Pursuing goal: {goal['title']}")
        
        # Pursue the goal
        result = await goal_system.pursue_goal(goal)
        
        if result["success"]:
            print(f"✅ Goal completed successfully!")
            print(f"   Result: {result['result']}")
            
            # Move to completed goals
            goal["status"] = "completed"
            goal_system.completed_goals.append(goal)
            goal_system.active_goals.remove(goal)
        else:
            print(f"⚠️  Goal encountered challenges:")
            print(f"   Result: {result['result']}")
            goal["status"] = "needs_revision"
        
        print(f"\n📊 System Status:")
        status = goal_system.get_status_summary()
        print(f"   Active Goals: {status['active_goals']}")
        print(f"   Completed Goals: {status['completed_goals']}")
        print(f"   System Capabilities: {status['capabilities']}")
        
        await asyncio.sleep(1)  # Brief pause between cycles
    
    print(f"\n🎉 Autonomous Goal System Demonstration Complete!")
    print(f"This is what REAL autonomous behavior looks like - not endless repetition!")

if __name__ == "__main__":
    asyncio.run(demonstrate_real_autonomous_behavior())
