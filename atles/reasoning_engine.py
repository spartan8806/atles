#!/usr/bin/env python3
"""
ATLES Reasoning Engine - Advanced Problem Solving
Handles complex reasoning scenarios including temporal paradoxes and edge cases.

This module fixes the processing loop failures by implementing robust
reasoning patterns that don't break into system calls inappropriately.
"""

import logging
import json
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

class ReasoningMode(Enum):
    """Different reasoning approaches for different problem types"""
    LINEAR = "linear"           # Simple step-by-step reasoning
    TREE_OF_THOUGHTS = "tree"   # Multiple parallel reasoning paths
    CONSTITUTIONAL = "constitutional"  # Principle-based reasoning
    PARADOX_RESOLUTION = "paradox"    # Special handling for paradoxes
    CREATIVE = "creative"       # Creative/divergent thinking
    ANALYTICAL = "analytical"   # Data-driven analysis

class ReasoningContext:
    """Context for reasoning operations"""
    
    def __init__(self, problem_type: str = "general", complexity: int = 1):
        self.problem_type = problem_type
        self.complexity = complexity  # 1-10 scale
        self.reasoning_mode = self._determine_reasoning_mode()
        self.constraints = []
        self.assumptions = []
        self.explored_paths = []
        self.failed_attempts = []
        
    def _determine_reasoning_mode(self) -> ReasoningMode:
        """Determine appropriate reasoning mode based on problem characteristics"""
        if "paradox" in self.problem_type.lower() or "temporal" in self.problem_type.lower():
            return ReasoningMode.PARADOX_RESOLUTION
        elif self.complexity >= 7:
            return ReasoningMode.TREE_OF_THOUGHTS
        elif "creative" in self.problem_type.lower() or "design" in self.problem_type.lower():
            return ReasoningMode.CREATIVE
        elif "analysis" in self.problem_type.lower() or "data" in self.problem_type.lower():
            return ReasoningMode.ANALYTICAL
        else:
            return ReasoningMode.LINEAR

class ReasoningEngine:
    """
    Advanced reasoning engine that handles complex scenarios without
    breaking into inappropriate system calls.
    """
    
    def __init__(self):
        self.reasoning_patterns = {
            ReasoningMode.LINEAR: self._linear_reasoning,
            ReasoningMode.TREE_OF_THOUGHTS: self._tree_of_thoughts_reasoning,
            ReasoningMode.CONSTITUTIONAL: self._constitutional_reasoning,
            ReasoningMode.PARADOX_RESOLUTION: self._paradox_resolution_reasoning,
            ReasoningMode.CREATIVE: self._creative_reasoning,
            ReasoningMode.ANALYTICAL: self._analytical_reasoning
        }
        
        self.paradox_handlers = {
            "temporal": self._handle_temporal_paradox,
            "logical": self._handle_logical_paradox,
            "causal": self._handle_causal_paradox,
            "self_reference": self._handle_self_reference_paradox
        }
        
        self.reasoning_history = []
        
    def reason(self, problem: str, context: Optional[ReasoningContext] = None) -> Dict[str, Any]:
        """
        Main reasoning entry point that routes to appropriate reasoning pattern.
        
        CRITICAL: This method ensures we stay in reasoning mode and don't
        break into system calls inappropriately.
        """
        if context is None:
            context = ReasoningContext()
            
        # Detect if this is actually a system operation request
        if self._is_system_operation_request(problem):
            return {
                "reasoning_type": "system_operation_detected",
                "recommendation": "This appears to be a system operation request, not a reasoning problem",
                "suggested_action": "Use appropriate system functions if execution is intended"
            }
        
        # Detect paradox scenarios early
        paradox_type = self._detect_paradox_type(problem)
        if paradox_type:
            context.problem_type = f"paradox_{paradox_type}"
            context.reasoning_mode = ReasoningMode.PARADOX_RESOLUTION
            
        # Route to appropriate reasoning pattern
        reasoning_func = self.reasoning_patterns.get(
            context.reasoning_mode, 
            self._linear_reasoning
        )
        
        try:
            result = reasoning_func(problem, context)
            
            # Log reasoning for learning
            self.reasoning_history.append({
                "timestamp": datetime.now().isoformat(),
                "problem": problem,
                "context": context.__dict__,
                "result": result,
                "success": True
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Reasoning failed: {e}")
            
            # CRITICAL: Don't break into system calls on reasoning failure
            # Instead, provide a structured failure response
            failure_result = {
                "reasoning_type": "reasoning_failure",
                "error": str(e),
                "problem": problem,
                "attempted_mode": context.reasoning_mode.value,
                "fallback_approach": self._generate_fallback_approach(problem, context),
                "success": False
            }
            
            self.reasoning_history.append({
                "timestamp": datetime.now().isoformat(),
                "problem": problem,
                "context": context.__dict__,
                "result": failure_result,
                "success": False,
                "error": str(e)
            })
            
            return failure_result
    
    def _is_system_operation_request(self, problem: str) -> bool:
        """
        Detect if the problem is actually a system operation request
        rather than a reasoning problem.
        """
        system_indicators = [
            r"get.*system.*info",
            r"run.*command",
            r"execute.*file",
            r"search.*code",
            r"list.*files",
            r"read.*file"
        ]
        
        problem_lower = problem.lower()
        for pattern in system_indicators:
            if re.search(pattern, problem_lower):
                return True
        return False
    
    def _detect_paradox_type(self, problem: str) -> Optional[str]:
        """Detect what type of paradox we're dealing with"""
        problem_lower = problem.lower()
        
        if any(word in problem_lower for word in ["time", "temporal", "past", "future", "causality"]):
            return "temporal"
        elif any(word in problem_lower for word in ["self", "itself", "recursive", "circular"]):
            return "self_reference"
        elif any(word in problem_lower for word in ["cause", "effect", "because", "therefore"]):
            return "causal"
        elif any(word in problem_lower for word in ["contradiction", "paradox", "impossible", "logical"]):
            return "logical"
        
        return None
    
    def _linear_reasoning(self, problem: str, context: ReasoningContext) -> Dict[str, Any]:
        """Simple step-by-step reasoning for straightforward problems"""
        steps = []
        
        # Break down the problem
        steps.append("1. Problem Analysis: " + self._analyze_problem_components(problem))
        steps.append("2. Identify Key Elements: " + self._identify_key_elements(problem))
        steps.append("3. Apply Logical Steps: " + self._apply_logical_steps(problem))
        steps.append("4. Reach Conclusion: " + self._reach_conclusion(problem))
        
        return {
            "reasoning_type": "linear",
            "steps": steps,
            "conclusion": self._synthesize_conclusion(steps),
            "confidence": 0.8
        }
    
    def _tree_of_thoughts_reasoning(self, problem: str, context: ReasoningContext) -> Dict[str, Any]:
        """
        Tree of Thoughts reasoning for complex problems.
        Explores multiple reasoning paths in parallel.
        """
        # Generate multiple reasoning branches
        branches = self._generate_reasoning_branches(problem)
        
        # Evaluate each branch
        evaluated_branches = []
        for i, branch in enumerate(branches):
            evaluation = self._evaluate_reasoning_branch(branch, problem)
            evaluated_branches.append({
                "branch_id": i,
                "reasoning_path": branch,
                "evaluation": evaluation,
                "score": evaluation.get("score", 0.5)
            })
        
        # Select best branch(es)
        best_branches = sorted(evaluated_branches, key=lambda x: x["score"], reverse=True)[:3]
        
        # Synthesize final answer
        synthesis = self._synthesize_from_branches(best_branches, problem)
        
        return {
            "reasoning_type": "tree_of_thoughts",
            "explored_branches": len(branches),
            "top_branches": best_branches,
            "synthesis": synthesis,
            "confidence": max(branch["score"] for branch in best_branches)
        }
    
    def _constitutional_reasoning(self, problem: str, context: ReasoningContext) -> Dict[str, Any]:
        """Principle-based reasoning that adheres to constitutional principles"""
        principles = [
            "Principle of Explicit Action",
            "Principle of Helpful Assistance", 
            "Principle of Safety First",
            "Principle of Truthfulness"
        ]
        
        principle_analysis = {}
        for principle in principles:
            principle_analysis[principle] = self._analyze_against_principle(problem, principle)
        
        # Find the governing principle
        governing_principle = max(principle_analysis.items(), key=lambda x: x[1]["relevance"])
        
        # Apply constitutional reasoning
        constitutional_response = self._apply_constitutional_principle(
            problem, 
            governing_principle[0], 
            governing_principle[1]
        )
        
        return {
            "reasoning_type": "constitutional",
            "governing_principle": governing_principle[0],
            "principle_analysis": principle_analysis,
            "constitutional_response": constitutional_response,
            "confidence": governing_principle[1]["confidence"]
        }
    
    def _paradox_resolution_reasoning(self, problem: str, context: ReasoningContext) -> Dict[str, Any]:
        """
        DISABLED: Paradox resolution was causing response loops.
        Let ATLES reason naturally instead of using hardcoded templates.
        """
        return {
            "reasoning_type": "natural_reasoning",
            "paradox_type": "disabled",
            "resolution_approach": "natural",
            "analysis": ["Let ATLES engage with the actual question naturally"],
            "conclusion": "Routing to natural reasoning instead of hardcoded paradox templates",
            "confidence": 0.0,
            "note": "Paradox detection disabled to prevent response loops"
        }
    
    def _handle_temporal_paradox(self, problem: str, context: ReasoningContext) -> Dict[str, Any]:
        """Handle temporal paradoxes - DISABLED to prevent response loops"""
        # Return None to let ATLES reason naturally instead of using hardcoded templates
        return {
            "approach": "natural_reasoning",
            "analysis": ["Let ATLES reason about this question naturally"],
            "conclusion": "Routing to natural reasoning instead of hardcoded template",
            "confidence": 0.0,
            "disabled": True
        }
    
    def _handle_logical_paradox(self, problem: str, context: ReasoningContext) -> Dict[str, Any]:
        """Handle logical paradoxes (liar's paradox, Russell's paradox, etc.)"""
        return {
            "approach": "logical_analysis",
            "analysis": [
                "Logical paradoxes often reveal limitations in our reasoning systems",
                "Examine the assumptions that lead to the contradiction",
                "Consider whether the paradox indicates incomplete or inconsistent premises",
                "Look for resolution through refined logical frameworks"
            ],
            "conclusion": "Logical paradoxes often point to the need for more sophisticated logical systems or refined premises",
            "confidence": 0.6
        }
    
    def _handle_causal_paradox(self, problem: str, context: ReasoningContext) -> Dict[str, Any]:
        """Handle causal paradoxes (bootstrap paradox, etc.)"""
        return {
            "approach": "causal_analysis", 
            "analysis": [
                "Causal paradoxes challenge our understanding of cause and effect",
                "Consider whether causality is truly linear or can be circular",
                "Examine the information or energy flow in the causal loop",
                "Look for external factors that might break the apparent loop"
            ],
            "conclusion": "Causal paradoxes may indicate emergent properties or non-linear causal relationships",
            "confidence": 0.65
        }
    
    def _handle_self_reference_paradox(self, problem: str, context: ReasoningContext) -> Dict[str, Any]:
        """Handle self-reference paradoxes"""
        return {
            "approach": "self_reference_analysis",
            "analysis": [
                "Self-reference paradoxes arise from statements that refer to themselves",
                "Consider the levels of abstraction involved",
                "Examine whether the self-reference is truly problematic or just complex",
                "Look for ways to break the self-reference through external perspective"
            ],
            "conclusion": "Self-reference paradoxes often resolve through careful attention to levels of abstraction",
            "confidence": 0.7
        }
    
    def _generic_paradox_resolution(self, problem: str, context: ReasoningContext) -> Dict[str, Any]:
        """Generic approach for unclassified paradoxes"""
        return {
            "approach": "general_paradox_analysis",
            "analysis": [
                "Identify the core contradiction or impossibility",
                "Examine the assumptions that lead to the paradox",
                "Consider alternative frameworks or perspectives",
                "Look for resolution through refined understanding"
            ],
            "conclusion": "This paradox requires careful analysis of underlying assumptions and may benefit from alternative perspectives",
            "confidence": 0.5
        }
    
    def _creative_reasoning(self, problem: str, context: ReasoningContext) -> Dict[str, Any]:
        """Creative/divergent thinking for open-ended problems"""
        creative_approaches = [
            "Analogical thinking: What similar problems exist in other domains?",
            "Reverse thinking: What if we approached this backwards?",
            "Constraint removal: What if current limitations didn't exist?",
            "Combination thinking: How can we combine existing solutions?",
            "Perspective shifting: How would different stakeholders view this?"
        ]
        
        creative_solutions = []
        for approach in creative_approaches:
            solution = self._apply_creative_approach(approach, problem)
            creative_solutions.append(solution)
        
        return {
            "reasoning_type": "creative",
            "creative_approaches": creative_approaches,
            "generated_solutions": creative_solutions,
            "synthesis": self._synthesize_creative_solutions(creative_solutions),
            "confidence": 0.6
        }
    
    def _analytical_reasoning(self, problem: str, context: ReasoningContext) -> Dict[str, Any]:
        """Data-driven analytical reasoning"""
        analysis_steps = [
            "Data identification: What information is available?",
            "Pattern recognition: What patterns emerge from the data?",
            "Hypothesis formation: What explanations fit the patterns?",
            "Validation: How can we test these hypotheses?",
            "Conclusion: What does the analysis suggest?"
        ]
        
        analytical_results = []
        for step in analysis_steps:
            result = self._perform_analytical_step(step, problem)
            analytical_results.append(result)
        
        return {
            "reasoning_type": "analytical",
            "analysis_steps": analysis_steps,
            "analytical_results": analytical_results,
            "data_confidence": self._assess_data_confidence(problem),
            "conclusion": self._draw_analytical_conclusion(analytical_results),
            "confidence": 0.75
        }
    
    # Helper methods for reasoning operations
    
    def _analyze_problem_components(self, problem: str) -> str:
        """Analyze the basic components of a problem"""
        return f"Breaking down '{problem}' into core components and relationships"
    
    def _identify_key_elements(self, problem: str) -> str:
        """Identify key elements in the problem"""
        return f"Key elements identified in the problem context"
    
    def _apply_logical_steps(self, problem: str) -> str:
        """Apply logical reasoning steps"""
        return f"Applying logical reasoning to progress toward solution"
    
    def _reach_conclusion(self, problem: str) -> str:
        """Reach a logical conclusion"""
        return f"Drawing conclusion based on logical analysis"
    
    def _synthesize_conclusion(self, steps: List[str]) -> str:
        """Synthesize a conclusion from reasoning steps"""
        return f"Based on the analysis steps, the conclusion addresses the core problem systematically"
    
    def _generate_reasoning_branches(self, problem: str) -> List[str]:
        """Generate multiple reasoning branches for tree of thoughts"""
        return [
            f"Branch 1: Direct approach to {problem}",
            f"Branch 2: Alternative perspective on {problem}",
            f"Branch 3: Systematic analysis of {problem}",
            f"Branch 4: Creative solution for {problem}"
        ]
    
    def _evaluate_reasoning_branch(self, branch: str, problem: str) -> Dict[str, Any]:
        """Evaluate a reasoning branch"""
        return {
            "feasibility": 0.7,
            "completeness": 0.8,
            "originality": 0.6,
            "score": 0.7
        }
    
    def _synthesize_from_branches(self, branches: List[Dict], problem: str) -> str:
        """Synthesize final answer from top branches"""
        return f"Synthesizing solution from {len(branches)} top reasoning branches"
    
    def _analyze_against_principle(self, problem: str, principle: str) -> Dict[str, Any]:
        """Analyze problem against a constitutional principle"""
        return {
            "relevance": 0.8,
            "compliance": 0.9,
            "confidence": 0.85
        }
    
    def _apply_constitutional_principle(self, problem: str, principle: str, analysis: Dict) -> str:
        """Apply constitutional principle to reach conclusion"""
        return f"Applying {principle} to resolve the problem constitutionally"
    
    def _apply_creative_approach(self, approach: str, problem: str) -> str:
        """Apply a creative approach to the problem"""
        return f"Creative solution using {approach}"
    
    def _synthesize_creative_solutions(self, solutions: List[str]) -> str:
        """Synthesize creative solutions"""
        return f"Combining {len(solutions)} creative approaches for comprehensive solution"
    
    def _perform_analytical_step(self, step: str, problem: str) -> str:
        """Perform an analytical step"""
        return f"Analytical result for: {step}"
    
    def _assess_data_confidence(self, problem: str) -> float:
        """Assess confidence in available data"""
        return 0.7
    
    def _draw_analytical_conclusion(self, results: List[str]) -> str:
        """Draw conclusion from analytical results"""
        return f"Analytical conclusion based on {len(results)} analysis steps"
    
    def _generate_fallback_approach(self, problem: str, context: ReasoningContext) -> str:
        """Generate fallback approach when reasoning fails"""
        return f"Fallback: Break down '{problem}' into smaller, manageable components and address each systematically"
    
    def get_reasoning_summary(self) -> Dict[str, Any]:
        """Get summary of reasoning operations"""
        if not self.reasoning_history:
            return {"total_operations": 0, "message": "No reasoning operations performed"}
        
        successful = [r for r in self.reasoning_history if r["success"]]
        failed = [r for r in self.reasoning_history if not r["success"]]
        
        reasoning_modes = {}
        for operation in self.reasoning_history:
            mode = operation["result"].get("reasoning_type", "unknown")
            reasoning_modes[mode] = reasoning_modes.get(mode, 0) + 1
        
        return {
            "total_operations": len(self.reasoning_history),
            "successful_operations": len(successful),
            "failed_operations": len(failed),
            "success_rate": len(successful) / len(self.reasoning_history) if self.reasoning_history else 0,
            "reasoning_modes_used": reasoning_modes,
            "latest_operation": self.reasoning_history[-1] if self.reasoning_history else None
        }


# Integration with ATLES system
def create_reasoning_engine():
    """Factory function to create reasoning engine"""
    return ReasoningEngine()


# Test function
def test_reasoning_engine():
    """Test the reasoning engine with various scenarios"""
    engine = ReasoningEngine()
    
    test_cases = [
        ("What is 2+2?", ReasoningContext("simple_math", 1)),
        ("Design a solution for climate change", ReasoningContext("complex_design", 8)),
        ("If I go back in time and prevent my own birth, what happens?", ReasoningContext("temporal_paradox", 9)),
        ("This statement is false", ReasoningContext("logical_paradox", 7)),
        ("Analyze the correlation between X and Y in this dataset", ReasoningContext("data_analysis", 6))
    ]
    
    print("🧠 Testing ATLES Reasoning Engine")
    print("=" * 50)
    
    for problem, context in test_cases:
        print(f"\nProblem: {problem}")
        print(f"Context: {context.problem_type} (complexity: {context.complexity})")
        
        result = engine.reason(problem, context)
        
        print(f"Reasoning Type: {result['reasoning_type']}")
        print(f"Success: {result.get('success', True)}")
        if 'conclusion' in result:
            print(f"Conclusion: {result['conclusion']}")
        print("-" * 30)
    
    # Summary
    summary = engine.get_reasoning_summary()
    print(f"\n📊 Reasoning Summary: {summary}")


if __name__ == "__main__":
    test_reasoning_engine()
