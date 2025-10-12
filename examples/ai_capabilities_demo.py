#!/usr/bin/env python3
"""
ATLES AI Capabilities Demo

This script demonstrates the four specialized AI capabilities:
1. Code Generator - Write code based on descriptions
2. Code Analyzer - Review and improve existing code
3. Debug Helper - Find and fix common errors
4. Optimizer - Suggest performance improvements
"""

import asyncio
import sys
from pathlib import Path

# Add the atles package to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from atles.brain import ATLESBrain
from atles.agents import AgentContext, ReasoningLevel


async def demo_code_generator(brain: ATLESBrain):
    """Demonstrate the Code Generator capability."""
    print("\n" + "="*60)
    print("🤖 CODE GENERATOR DEMO")
    print("="*60)
    
    # Create a context for the demo
    context = AgentContext(
        session_id="demo_session",
        user_id="demo_user",
        conversation_history=[],
        reasoning_level=ReasoningLevel.EXPERT
    )
    
    # Example 1: Generate a Python function
    print("\n📝 Example 1: Generate a Python function")
    print("Request: Create a function to calculate fibonacci numbers")
    
    query = "Create a Python function to calculate fibonacci numbers with memoization"
    result = await brain.agent_orchestrator.execute_agent_chain(
        "code_development", query, context
    )
    
    if result.get("success"):
        for agent_result in result.get("chain_results", []):
            if agent_result.get("success") and "generated_code" in str(agent_result.get("action_result", {})):
                print(f"✅ Generated code:\n{agent_result['action_result']['generated_code']}")
                break
    else:
        print("❌ Code generation failed")
    
    # Example 2: Generate a FastAPI endpoint
    print("\n📝 Example 2: Generate a FastAPI endpoint")
    print("Request: Create a FastAPI endpoint for user authentication")
    
    query = "Create a FastAPI endpoint for user authentication with JWT tokens"
    result = await brain.agent_orchestrator.execute_agent_chain(
        "code_development", query, context
    )
    
    if result.get("success"):
        for agent_result in result.get("chain_results", []):
            if agent_result.get("success") and "generated_code" in str(agent_result.get("action_result", {})):
                print(f"✅ Generated code:\n{agent_result['action_result']['generated_code']}")
                break
    else:
        print("❌ Code generation failed")


async def demo_code_analyzer(brain: ATLESBrain):
    """Demonstrate the Code Analyzer capability."""
    print("\n" + "="*60)
    print("🔍 CODE ANALYZER DEMO")
    print("="*60)
    
    # Sample code to analyze
    sample_code = '''def calculate_fibonacci(n):
    """Calculate fibonacci number."""
    if n <= 1:
        return n
    else:
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

def process_data(data_list):
    """Process a list of data items."""
    result = []
    for i in range(len(data_list)):
        item = data_list[i]
        if item > 1000:  # Magic number
            processed_item = item * 2
            result.append(processed_item)
    return result

# TODO: Add error handling
# FIXME: This function is too slow for large datasets
def slow_function(data):
    """This function is intentionally slow for demo purposes."""
    for i in range(10000):
        for j in range(10000):
            result = i * j
    return result'''
    
    print("\n📊 Analyzing sample code:")
    print("```python")
    print(sample_code)
    print("```")
    
    context = AgentContext(
        session_id="demo_session",
        user_id="demo_user",
        conversation_history=[],
        reasoning_level=ReasoningLevel.EXPERT
    )
    
    query = f"Analyze this code and suggest improvements:\n```python\n{sample_code}\n```"
    result = await brain.agent_orchestrator.execute_agent_chain(
        "code_review", query, context
    )
    
    if result.get("success"):
        for agent_result in result.get("chain_results", []):
            if agent_result.get("success") and "code_analysis" in str(agent_result.get("action_result", {})):
                analysis = agent_result['action_result']
                print(f"\n✅ Analysis Results:")
                print(f"   Overall Score: {analysis.get('overall_score', 'N/A')}/100")
                print(f"   Priority Issues: {len(analysis.get('priority_issues', []))}")
                print(f"   Best Practices: {len(analysis.get('best_practices', []))}")
                
                if analysis.get('improvement_suggestions'):
                    print(f"\n💡 Improvement Suggestions:")
                    for suggestion in analysis['improvement_suggestions']:
                        print(f"   • {suggestion.get('suggestion', 'N/A')}")
                        print(f"     Impact: {suggestion.get('impact', 'N/A')}")
                break
    else:
        print("❌ Code analysis failed")


async def demo_debug_helper(brain: ATLESBrain):
    """Demonstrate the Debug Helper capability."""
    print("\n" + "="*60)
    print("🐛 DEBUG HELPER DEMO")
    print("="*60)
    
    # Sample error messages
    error_examples = [
        "NameError: name 'undefined_variable' is not defined",
        "TypeError: can only concatenate str (not 'int') to str",
        "AttributeError: 'list' object has no attribute 'append_to'"
    ]
    
    context = AgentContext(
        session_id="demo_session",
        user_id="demo_user",
        conversation_history=[],
        reasoning_level=ReasoningLevel.EXPERT
    )
    
    for i, error in enumerate(error_examples, 1):
        print(f"\n🐛 Example {i}: {error}")
        
        query = f"Help me debug this error: {error}"
        result = await brain.agent_orchestrator.execute_agent_chain(
            "code_review", query, context
        )
        
        if result.get("success"):
            for agent_result in result.get("chain_results", []):
                if agent_result.get("success") and "error_analysis" in str(agent_result.get("action_result", {})):
                    analysis = agent_result['action_result']
                    print(f"✅ Error Analysis:")
                    print(f"   Type: {analysis.get('error_type', 'N/A')}")
                    print(f"   Root Cause: {analysis.get('root_cause', 'N/A')}")
                    print(f"   Severity: {analysis.get('severity', 'N/A')}")
                    
                    if analysis.get('solutions'):
                        print(f"   Solutions:")
                        for solution in analysis['solutions']:
                            print(f"     • {solution.get('description', 'N/A')}")
                    
                    if analysis.get('debugging_steps'):
                        print(f"   Debugging Steps:")
                        for step in analysis['debugging_steps']:
                            print(f"     • {step}")
                    break
        else:
            print("❌ Debug analysis failed")


async def demo_optimizer(brain: ATLESBrain):
    """Demonstrate the Optimizer capability."""
    print("\n" + "="*60)
    print("⚡ OPTIMIZER DEMO")
    print("="*60)
    
    # Sample code to optimize
    sample_code = '''def slow_data_processing(data_list):
    """Process data with inefficient operations."""
    result = []
    for i in range(len(data_list)):
        for j in range(len(data_list)):
            if data_list[i] > data_list[j]:
                result.append(data_list[i] * 2)
    return result

def inefficient_imports():
    """Function with inefficient imports."""
    from numpy import *
    from pandas import *
    return "Imports done"

def map_list_operation(data):
    """Use map with list conversion."""
    return list(map(lambda x: x * 2, data))'''
    
    print("\n📊 Analyzing code for optimization opportunities:")
    print("```python")
    print(sample_code)
    print("```")
    
    context = AgentContext(
        session_id="demo_session",
        user_id="demo_user",
        conversation_history=[],
        reasoning_level=ReasoningLevel.EXPERT
    )
    
    query = f"Analyze this code for performance optimization:\n```python\n{sample_code}\n```"
    result = await brain.agent_orchestrator.execute_agent_chain(
        "code_review", query, context
    )
    
    if result.get("success"):
        for agent_result in result.get("chain_results", []):
            if agent_result.get("success") and "performance_analysis" in str(agent_result.get("action_result", {})):
                analysis = agent_result['action_result']
                print(f"\n✅ Performance Analysis:")
                print(f"   Estimated Improvement: {analysis.get('estimated_improvement', 'N/A')}%")
                print(f"   Bottlenecks Found: {len(analysis.get('bottlenecks', []))}")
                
                if analysis.get('optimization_suggestions'):
                    print(f"\n💡 Optimization Suggestions:")
                    for suggestion in analysis['optimization_suggestions']:
                        print(f"   • {suggestion.get('description', 'N/A')}")
                        print(f"     Improvement: {suggestion.get('improvement', 'N/A')}")
                        print(f"     Complexity: {suggestion.get('complexity', 'N/A')}")
                        
                        if suggestion.get('before_example') and suggestion.get('after_example'):
                            print(f"     Before: {suggestion['before_example']}")
                            print(f"     After:  {suggestion['after_example']}")
                break
    else:
        print("❌ Optimization analysis failed")


async def main():
    """Run the AI capabilities demo."""
    print("🚀 ATLES AI Capabilities Demo")
    print("This demo showcases the four specialized AI capabilities")
    
    try:
        # Initialize ATLES Brain
        print("\n🔧 Initializing ATLES Brain...")
        brain = ATLESBrain()
        print("✅ ATLES Brain initialized successfully!")
        
        # Run all demos
        await demo_code_generator(brain)
        await demo_code_analyzer(brain)
        await demo_debug_helper(brain)
        await demo_optimizer(brain)
        
        print("\n" + "="*60)
        print("🎉 Demo completed successfully!")
        print("="*60)
        print("\nThe ATLES system now includes four specialized AI capabilities:")
        print("1. 🤖 Code Generator - Write code based on descriptions")
        print("2. 🔍 Code Analyzer - Review and improve existing code")
        print("3. 🐛 Debug Helper - Find and fix common errors")
        print("4. ⚡ Optimizer - Suggest performance improvements")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
