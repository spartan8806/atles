#!/usr/bin/env python3
"""
ATLES v0.5: Advanced AI Agents and Automation Demo

This demo showcases the new v0.5 capabilities:
- Autonomous AI agents with reasoning capabilities
- Tool usage and function calling for task execution
- Memory and state management for context-aware interactions
- Self-modification capabilities for behavior adaptation
"""

import asyncio
import logging
import json
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def demo_autonomous_agents(brain):
    """Demo autonomous agents with reasoning capabilities."""
    print("\n" + "="*60)
    print("🚀 DEMO: Autonomous AI Agents with Reasoning")
    print("="*60)
    
    # Start a conversation session
    session_id = await brain.start_conversation("demo_user", "demo_model")
    print(f"✅ Started conversation session: {session_id}")
    
    # Demo 1: Process query with reasoning agent
    print("\n🔍 Demo 1: Processing with Reasoning Agent")
    query = "How can I optimize a machine learning algorithm for better performance?"
    
    result = await brain.process_with_agents(
        query=query,
        session_id=session_id,
        agent_ids=["reasoning_agent"]
    )
    
    if result.get("success"):
        print(f"✅ Reasoning agent processed query successfully")
        print(f"📊 Agent: {result.get('agent_name', 'Unknown')}")
        print(f"🧠 Reasoning steps: {len(result.get('reasoning_steps', []))}")
        
        # Show reasoning steps
        for i, step in enumerate(result.get('reasoning_steps', [])):
            print(f"  Step {i+1} ({step.reasoning_type}): {step.content[:100]}...")
            print(f"    Confidence: {step.confidence:.2f}")
    else:
        print(f"❌ Agent processing failed: {result.get('error')}")
    
    # Demo 2: Process with agent chain
    print("\n🔗 Demo 2: Processing with Agent Chain")
    chain_result = await brain.process_with_agents(
        query="Analyze the current state of AI technology and predict future trends",
        session_id=session_id,
        use_chain=True,
        chain_id="problem_solving"
    )
    
    if chain_result.get("success"):
        print(f"✅ Agent chain executed successfully")
        print(f"🔗 Chain ID: {chain_result.get('chain_id')}")
        print(f"📋 Steps executed: {len(chain_result.get('chain_results', []))}")
        
        for step_result in chain_result.get('chain_results', []):
            agent_name = step_result.get('agent_name', 'Unknown')
            success = step_result.get('success', False)
            status = "✅" if success else "❌"
            print(f"  {status} {agent_name}: {'Success' if success else 'Failed'}")
    else:
        print(f"❌ Agent chain failed: {chain_result.get('error')}")
    
    return session_id


async def demo_advanced_tools(brain):
    """Demo advanced tool system and function calling."""
    print("\n" + "="*60)
    print("🛠️ DEMO: Advanced Tool System and Function Calling")
    print("="*60)
    
    # Demo 1: Execute built-in tools
    print("\n🔧 Demo 1: Executing Built-in Tools")
    
    # Text analysis tool
    text_analysis_result = await brain.execute_tool(
        tool_name="text_analyzer",
        parameters={"text": "I absolutely love this amazing product! It's incredible.", "analysis_type": "sentiment"},
        session_id="demo_session",
        user_id="demo_user"
    )
    
    if text_analysis_result.get("success"):
        tool_result = text_analysis_result.get("tool_result")
        print(f"✅ Text analysis completed")
        print(f"📊 Sentiment: {tool_result.result.get('sentiment', 'Unknown')}")
        print(f"📈 Sentiment score: {tool_result.result.get('sentiment_score', 'N/A')}")
        print(f"⏱️ Execution time: {tool_result.execution_time:.3f}s")
    else:
        print(f"❌ Text analysis failed: {text_analysis_result.get('error')}")
    
    # Text summarization tool
    long_text = """
    Artificial Intelligence (AI) has emerged as one of the most transformative technologies 
    of the 21st century. It encompasses machine learning, deep learning, natural language 
    processing, computer vision, and robotics. AI systems can now perform tasks that were 
    once thought to be exclusively human, such as recognizing speech, translating languages, 
    making decisions, and solving complex problems. The field continues to advance rapidly, 
    with new breakthroughs in areas like generative AI, autonomous systems, and quantum 
    machine learning. These developments are reshaping industries, from healthcare and 
    finance to transportation and entertainment.
    """
    
    summary_result = await brain.execute_tool(
        tool_name="text_summarizer",
        parameters={"text": long_text, "max_length": 50, "style": "concise"},
        session_id="demo_session",
        user_id="demo_user"
    )
    
    if summary_result.get("success"):
        tool_result = summary_result.get("tool_result")
        print(f"\n✅ Text summarization completed")
        print(f"📝 Summary: {tool_result.result.get('summary', 'N/A')}")
        print(f"📊 Compression ratio: {tool_result.result.get('compression_ratio', 0):.2f}")
    else:
        print(f"❌ Text summarization failed: {summary_result.get('error')}")
    
    # Demo 2: Create and execute custom tool chain
    print("\n🔗 Demo 2: Creating Custom Tool Chain")
    
    # Define tool chain steps
    chain_steps = [
        {
            "tool_name": "text_analyzer",
            "parameters": {"text": "Sample text for analysis", "analysis_type": "general"},
            "step_name": "Initial Analysis"
        },
        {
            "tool_name": "text_summarizer",
            "parameters": {"text": "Sample text for analysis", "max_length": 30},
            "step_name": "Generate Summary"
        }
    ]
    
    chain_creation = await brain.create_tool_chain(
        chain_name="Text Processing Pipeline",
        chain_description="Analyzes text and generates summaries",
        steps=chain_steps
    )
    
    if chain_creation.get("success"):
        print(f"✅ Tool chain created: {chain_creation.get('chain_name')}")
        print(f"🆔 Chain ID: {chain_creation.get('chain_id')}")
        
        # Execute the chain
        chain_execution = await brain.tool_registry.get_tool_chain(
            chain_creation.get('chain_id')
        ).execute(
            brain.tool_registry,
            {"input_text": "This is a sample text for processing through our custom tool chain."},
            "demo_user",
            "demo_session"
        )
        
        if chain_execution.get("success"):
            print(f"✅ Tool chain executed successfully")
            print(f"⏱️ Total execution time: {chain_execution.get('execution_time', 0):.3f}s")
            print(f"📋 Steps completed: {len(chain_execution.get('steps_executed', []))}")
        else:
            print(f"❌ Tool chain execution failed: {chain_execution.get('errors', [])}")
    else:
        print(f"❌ Tool chain creation failed: {chain_creation.get('error')}")


async def demo_state_management(brain):
    """Demo advanced state management and context awareness."""
    print("\n" + "="*60)
    print("🧠 DEMO: Advanced State Management and Context Awareness")
    print("="*60)
    
    # Demo 1: State persistence and retrieval
    print("\n💾 Demo 1: State Persistence and Retrieval")
    
    # Set various types of state
    session_state = brain.state_manager.set_state(
        "user_preferences",
        {"theme": "dark", "language": "en", "notifications": True},
        brain.state_management.StateType.USER,
        user_id="demo_user"
    )
    
    if session_state.get("success"):
        print(f"✅ User preferences state set successfully")
        print(f"🆔 Change ID: {session_state.get('change_id')}")
    
    # Set session-specific state
    brain.state_manager.set_state(
        "conversation_context",
        {"topic": "AI technology", "complexity": "advanced", "user_expertise": "intermediate"},
        brain.state_management.StateType.SESSION,
        session_id="demo_session",
        user_id="demo_user"
    )
    
    # Set system state
    brain.state_manager.set_state(
        "system_config",
        {"auto_save": True, "max_memory": "8GB", "performance_mode": "balanced"},
        brain.state_management.StateType.SYSTEM
    )
    
    # Demo 2: State retrieval with metadata
    print("\n📊 Demo 2: State Retrieval with Metadata")
    
    user_prefs = brain.state_manager.get_state_with_metadata("user_preferences", brain.state_management.StateType.USER)
    if user_prefs.get("exists"):
        print(f"✅ User preferences retrieved")
        print(f"📅 Last modified: {user_prefs.get('last_modified')}")
        print(f"🆔 Change ID: {user_prefs.get('change_id')}")
        print(f"📋 Metadata: {json.dumps(user_prefs.get('metadata', {}), indent=2)}")
    
    # Demo 3: State change history
    print("\n📜 Demo 3: State Change History")
    
    changes = brain.state_manager.get_change_history(
        user_id="demo_user",
        limit=5
    )
    
    print(f"📊 Retrieved {len(changes)} recent changes for demo_user")
    for change in changes:
        print(f"  🔄 {change.change_type}: {change.state_key} at {change.timestamp}")
    
    # Demo 4: State snapshots
    print("\n📸 Demo 4: State Snapshots")
    
    snapshot = brain.state_manager.create_snapshot({
        "description": "Demo snapshot before major changes",
        "demo_type": "state_management"
    })
    
    print(f"✅ State snapshot created: {snapshot.snapshot_id}")
    print(f"📅 Timestamp: {snapshot.timestamp}")
    print(f"🔒 Checksum: {snapshot.checksum[:8]}...")


async def demo_self_modification(brain):
    """Demo self-modification capabilities."""
    print("\n" + "="*60)
    print("🔧 DEMO: Self-Modification Capabilities")
    print("="*60)
    
    # Demo 1: Request behavior modification
    print("\n🎯 Demo 1: Request Behavior Modification")
    
    behavior_mod = await brain.request_self_modification(
        modification_type="behavior_change",
        target="response_style",
        description="Update response style to be more concise and technical",
        parameters={
            "style": "concise_technical",
            "max_length": 200,
            "include_examples": True
        },
        session_id="demo_session",
        user_id="demo_user"
    )
    
    if behavior_mod.get("success"):
        print(f"✅ Behavior modification completed")
        print(f"🆔 Request ID: {behavior_mod.get('request_id')}")
        print(f"📋 Execution result: {behavior_mod.get('execution_result', {}).get('message', 'N/A')}")
    else:
        print(f"❌ Behavior modification failed: {behavior_mod.get('error')}")
    
    # Demo 2: Request capability addition
    print("\n🚀 Demo 2: Request Capability Addition")
    
    capability_mod = await brain.request_self_modification(
        modification_type="capability_addition",
        target="new_analysis_tool",
        description="Add capability to analyze code complexity and suggest optimizations",
        parameters={
            "tool_name": "code_complexity_analyzer",
            "capabilities": ["complexity_analysis", "optimization_suggestions", "performance_metrics"],
            "integration_level": "advanced"
        },
        session_id="demo_session",
        user_id="demo_user"
    )
    
    if capability_mod.get("success"):
        print(f"✅ Capability addition completed")
        print(f"🆔 Request ID: {capability_mod.get('request_id')}")
        print(f"📋 New capability: {capability_mod.get('execution_result', {}).get('message', 'N/A')}")
    else:
        print(f"❌ Capability addition failed: {capability_mod.get('error')}")
    
    # Demo 3: View modification history
    print("\n📜 Demo 3: Modification History")
    
    mod_history = brain.self_modification_tracker.get_modification_history(
        user_id="demo_user",
        limit=10
    )
    
    print(f"📊 Retrieved {len(mod_history)} modification requests")
    for mod in mod_history:
        status_emoji = "✅" if mod.get("status") == "completed" else "❌"
        print(f"  {status_emoji} {mod.get('modification_type')}: {mod.get('description')[:50]}...")
        print(f"    Status: {mod.get('status')}, Time: {mod.get('timestamp')}")
    
    # Demo 4: Modification statistics
    print("\n📈 Demo 4: Modification Statistics")
    
    mod_stats = brain.self_modification_tracker.get_modification_statistics()
    print(f"📊 Total modifications: {mod_stats.get('total_modifications', 0)}")
    print(f"✅ Success rate: {mod_stats.get('success_rate', 0):.2%}")
    print(f"📋 Status distribution: {json.dumps(mod_stats.get('status_distribution', {}), indent=2)}")
    print(f"🔧 Type distribution: {json.dumps(mod_stats.get('type_distribution', {}), indent=2)}")


async def demo_agent_adaptation(brain):
    """Demo agent adaptation and learning capabilities."""
    print("\n" + "="*60)
    print("🎓 DEMO: Agent Adaptation and Learning")
    print("="*60)
    
    # Demo 1: Agent behavior adaptation
    print("\n🔄 Demo 1: Agent Behavior Adaptation")
    
    # Get reasoning agent
    reasoning_agent = brain.agent_orchestrator.agents.get("reasoning_agent")
    if reasoning_agent:
        print(f"🧠 Agent: {reasoning_agent.name}")
        print(f"📊 Current reasoning level: {reasoning_agent.reasoning_engine.reasoning_level.value}")
        
        # Adapt agent behavior
        adaptation_result = await reasoning_agent.adapt_behavior({
            "type": "reasoning_level_upgrade",
            "reasoning_level": "expert",
            "tool_preferences": ["text_analyzer", "text_summarizer"],
            "response_style": "detailed_with_examples"
        })
        
        if adaptation_result.get("success"):
            print(f"✅ Agent adaptation completed")
            print(f"🆕 New reasoning level: {adaptation_result.get('new_state', {}).get('reasoning_level')}")
            print(f"📈 Total adaptations: {adaptation_result.get('new_state', {}).get('total_adaptations')}")
        else:
            print(f"❌ Agent adaptation failed: {adaptation_result.get('error')}")
    
    # Demo 2: Agent self-modification
    print("\n🔧 Demo 2: Agent Self-Modification")
    
    if reasoning_agent:
        self_mod_result = await reasoning_agent.self_modify({
            "description": "Advanced reasoning agent specialized in complex problem-solving with multi-step analysis",
            "reasoning_level": "expert",
            "new_capabilities": {
                "multi_step_reasoning": True,
                "pattern_recognition": True,
                "meta_cognition": True
            }
        })
        
        if self_mod_result.get("success"):
            print(f"✅ Agent self-modification completed")
            print(f"🆕 New description: {self_mod_result.get('new_state', {}).get('description')}")
            print(f"🧠 New reasoning level: {self_mod_result.get('new_state', {}).get('reasoning_level')}")
            print(f"📈 Total modifications: {self_mod_result.get('new_state', {}).get('total_modifications')}")
        else:
            print(f"❌ Agent self-modification failed: {self_mod_result.get('error')}")
    
    # Demo 3: Agent performance metrics
    print("\n📊 Demo 3: Agent Performance Metrics")
    
    if reasoning_agent:
        status = reasoning_agent.get_status()
        print(f"🧠 Agent: {status.get('name')}")
        print(f"📊 State: {status.get('state')}")
        print(f"🧠 Reasoning level: {status.get('reasoning_level')}")
        print(f"💾 Memory stats: {json.dumps(status.get('memory_stats', {}), indent=2)}")
        print(f"📈 Performance metrics: {json.dumps(status.get('performance_metrics', {}), indent=2)}")


async def demo_system_status(brain):
    """Demo comprehensive system status and monitoring."""
    print("\n" + "="*60)
    print("📊 DEMO: Comprehensive System Status and Monitoring")
    print("="*60)
    
    # Get v0.5 status
    v0_5_status = brain.get_v0_5_status()
    
    print("\n🚀 ATLES v0.5 System Status:")
    print(f"🤖 Total Agents: {v0_5_status['agents']['total_agents']}")
    print(f"🛠️ Total Tools: {v0_5_status['tools']['total_tools']}")
    print(f"🔗 Total Tool Chains: {v0_5_status['tools']['total_chains']}")
    print(f"💾 Total States: {v0_5_status['state_management']['system_status']['total_states']}")
    print(f"🔧 Total Modifications: {v0_5_status['self_modification']['total_modifications']}")
    
    # Agent status details
    print("\n🤖 Agent Status Details:")
    agent_status = v0_5_status['agents']['agent_status']
    for agent_id, agent_info in agent_status['agents'].items():
        print(f"  🧠 {agent_info['name']}: {agent_info['state']} ({agent_info['reasoning_level']})")
        print(f"    💾 Memory: {agent_info['memory_stats']['short_term_count']} ST, {agent_info['memory_stats']['long_term_keys']} LT")
        print(f"    📈 Performance: {agent_info['performance_metrics'].get('performance_metrics', {}).get('success_rate', 0):.2%} success rate")
    
    # Tool categories
    print("\n🛠️ Tool Categories:")
    tool_categories = v0_5_status['tools']['tool_categories']
    for category, tools in tool_categories.items():
        print(f"  📁 {category}: {len(tools)} tools")
        for tool in tools[:3]:  # Show first 3 tools
            print(f"    🔧 {tool['name']} ({tool['safety_level']})")
    
    # State management status
    print("\n💾 State Management Status:")
    state_status = v0_5_status['state_management']['system_status']
    print(f"  📊 Total States: {state_status['total_states']}")
    print(f"  👀 Total Observers: {state_status['total_observers']}")
    print(f"  🔄 Auto-save: {state_status['auto_save']}")
    print(f"  🎯 Consistency Level: {state_status['consistency_level']}")
    
    # Self-modification statistics
    print("\n🔧 Self-Modification Statistics:")
    mod_stats = v0_5_status['self_modification']['modification_stats']
    print(f"  📈 Success Rate: {mod_stats['success_rate']:.2%}")
    print(f"  📊 Status Distribution: {json.dumps(mod_stats['status_distribution'], indent=4)}")
    print(f"  🔧 Type Distribution: {json.dumps(mod_stats['type_distribution'], indent=4)}")


async def main():
    """Main demo function."""
    print("🚀 ATLES v0.5: Advanced AI Agents and Automation Demo")
    print("=" * 80)
    print("This demo showcases the new v0.5 capabilities:")
    print("• Autonomous AI agents with reasoning capabilities")
    print("• Tool usage and function calling for task execution")
    print("• Memory and state management for context-aware interactions")
    print("• Self-modification capabilities for behavior adaptation")
    print("=" * 80)
    
    try:
        # Import brain (this would normally be from the installed package)
        from atles.brain import ATLESBrain
        
        # Initialize brain
        print("\n🔧 Initializing ATLES Brain v0.5...")
        brain = ATLESBrain()
        print("✅ ATLES Brain initialized successfully!")
        
        # Run all demos
        session_id = await demo_autonomous_agents(brain)
        await demo_advanced_tools(brain)
        await demo_state_management(brain)
        await demo_self_modification(brain)
        await demo_agent_adaptation(brain)
        await demo_system_status(brain)
        
        print("\n" + "="*80)
        print("🎉 ATLES v0.5 Demo Completed Successfully!")
        print("="*80)
        print("The system has demonstrated:")
        print("✅ Autonomous AI agents with advanced reasoning")
        print("✅ Comprehensive tool system with function calling")
        print("✅ Advanced state management and persistence")
        print("✅ Self-modification capabilities with safety checks")
        print("✅ Agent adaptation and learning")
        print("✅ Full system monitoring and status")
        print("\n🚀 Your ATLES system is now ready for advanced AI automation!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure ATLES is properly installed and accessible")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        logger.error(f"Demo error: {e}", exc_info=True)


if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())
