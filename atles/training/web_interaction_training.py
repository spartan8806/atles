#!/usr/bin/env python3
"""
ATLES Web Interaction Training Module
Addresses the reasoning instability under pressure identified in the diagnosis.

This module implements the "Principle of Explicit Action" and provides structured
training to rebuild ATLES's skills in web interaction and function calling from
the ground up using a "Call and Response" methodology.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TrainingLevel(Enum):
    """Training difficulty levels for progressive skill building"""
    BASIC = "basic"
    INTERMEDIATE = "intermediate" 
    ADVANCED = "advanced"
    EXPERT = "expert"


class TrainingResult(Enum):
    """Results of training exercises"""
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"
    NEEDS_RETRY = "needs_retry"


@dataclass
class TrainingExercise:
    """Represents a single training exercise"""
    id: str
    level: TrainingLevel
    description: str
    expected_action: str
    expected_function: str
    expected_parameters: Dict[str, Any]
    success_criteria: List[str]
    failure_patterns: List[str]
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class TrainingAttempt:
    """Records an attempt at a training exercise"""
    exercise_id: str
    response: str
    extracted_function: Optional[str]
    extracted_parameters: Optional[Dict[str, Any]]
    result: TrainingResult
    feedback: str
    pressure_level: float  # 0-1 scale
    timestamp: datetime = field(default_factory=datetime.now)


class PrincipleOfExplicitAction:
    """
    Implements the core principle that ATLES must provide explicit function calls
    instead of meta-commentary about its capabilities.
    """
    
    def __init__(self):
        self.constitution = [
            "Always provide specific function calls when asked for actions",
            "Never substitute meta-commentary for executable commands", 
            "When uncertain, state uncertainty but still provide the best function call",
            "Function calls are the primary way to demonstrate understanding",
            "Meta-analysis is only permitted AFTER providing the requested function call"
        ]
        
        self.violation_patterns = [
            "I should have",
            "I would need to",
            "The appropriate function would be",
            "This requires calling",
            "I cannot directly",
            "Let me explain how",
            "The best approach would be to"
        ]
    
    def validate_response(self, response: str, expected_function: str) -> Tuple[bool, str, List[str]]:
        """
        Validate that a response follows the Principle of Explicit Action
        
        Returns:
            (is_valid, extracted_function, violations)
        """
        violations = []
        
        # Check for violation patterns
        for pattern in self.violation_patterns:
            if pattern.lower() in response.lower():
                violations.append(f"Contains evasive pattern: '{pattern}'")
        
        # Extract function call
        extracted_function = self._extract_function_call(response)
        
        # Validate function call presence
        if not extracted_function:
            violations.append("No explicit function call found")
            return False, "", violations
        
        # Validate correct function
        if extracted_function != expected_function:
            violations.append(f"Wrong function: expected {expected_function}, got {extracted_function}")
            return False, extracted_function, violations
        
        # Success if no violations
        return len(violations) == 0, extracted_function, violations
    
    def _extract_function_call(self, response: str) -> Optional[str]:
        """Extract function call from response"""
        # Look for various function call patterns
        import re
        
        # Priority order: exact matches first
        if "SEARCH[" in response.upper():
            return "SEARCH"
        elif "SEARCH_CODE[" in response.upper():
            return "SEARCH_CODE"
        elif "LIST_FILES[" in response.upper():
            return "LIST_FILES"
        
        # Fallback patterns
        patterns = [
            r"(\w+)\[",
            r"FUNCTION_CALL:(\w+)",
            r"(\w+)\(",
            r"call (\w+)",
            r"use (\w+)",
            r"execute (\w+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                function_name = match.group(1).upper()
                if function_name in ["SEARCH", "SEARCH_CODE", "LIST_FILES"]:
                    return function_name
        
        return None
    
    def generate_corrective_feedback(self, violations: List[str], expected_function: str) -> str:
        """Generate specific corrective feedback"""
        if not violations:
            return "Good! Response follows the Principle of Explicit Action."
        
        feedback = "CONSTITUTIONAL VIOLATION - Principle of Explicit Action:\n"
        for violation in violations:
            feedback += f"- {violation}\n"
        
        feedback += f"\nCORRECT RESPONSE REQUIRED: {expected_function}[parameters]\n"
        feedback += "Remember: Provide the function call FIRST, explanation second."
        
        return feedback


class CallAndResponseTrainer:
    """
    Implements the "Call and Response" methodology for rebuilding skills
    from the ground up in a controlled way.
    """
    
    def __init__(self, brain_interface):
        self.brain_interface = brain_interface
        self.principle = PrincipleOfExplicitAction()
        self.training_exercises = []
        self.training_history = []
        self.current_level = TrainingLevel.BASIC
        self.pressure_adaptation = 0.0
        
        # Initialize exercises
        self._initialize_exercises()
    
    def _initialize_exercises(self):
        """Initialize the training exercise library"""
        
        # BASIC LEVEL - Simple, one-shot tasks
        self.training_exercises.extend([
            TrainingExercise(
                id="basic_001",
                level=TrainingLevel.BASIC,
                description="What single command finds the capital of France?",
                expected_action="SEARCH[capital of France]",
                expected_function="SEARCH",
                expected_parameters={"query": "capital of France"},
                success_criteria=["Contains SEARCH function", "Contains 'capital of France'"],
                failure_patterns=["I would need to", "The appropriate function"]
            ),
            TrainingExercise(
                id="basic_002", 
                level=TrainingLevel.BASIC,
                description="What single command finds the Wikipedia page for the Eiffel Tower?",
                expected_action="SEARCH[Eiffel Tower Wikipedia]",
                expected_function="SEARCH",
                expected_parameters={"query": "Eiffel Tower Wikipedia"},
                success_criteria=["Contains SEARCH function", "Contains 'Eiffel Tower'"],
                failure_patterns=["I should have", "Let me explain"]
            ),
            TrainingExercise(
                id="basic_003",
                level=TrainingLevel.BASIC, 
                description="What single command searches for Python tutorials?",
                expected_action="SEARCH[Python tutorials]",
                expected_function="SEARCH",
                expected_parameters={"query": "Python tutorials"},
                success_criteria=["Contains SEARCH function", "Contains 'Python tutorials'"],
                failure_patterns=["The best approach", "I cannot directly"]
            )
        ])
        
        # INTERMEDIATE LEVEL - Multiple parameter functions
        self.training_exercises.extend([
            TrainingExercise(
                id="intermediate_001",
                level=TrainingLevel.INTERMEDIATE,
                description="Search for JavaScript code examples with error handling",
                expected_action="SEARCH_CODE[query='JavaScript error handling', language='javascript']",
                expected_function="SEARCH_CODE",
                expected_parameters={"query": "JavaScript error handling", "language": "javascript"},
                success_criteria=["Contains SEARCH_CODE function", "Specifies JavaScript", "Mentions error handling"],
                failure_patterns=["I would need to search", "This requires calling"]
            ),
            TrainingExercise(
                id="intermediate_002",
                level=TrainingLevel.INTERMEDIATE,
                description="Find Python files in the current directory that contain 'async'",
                expected_action="LIST_FILES[directory='.', pattern='*.py', content_filter='async']",
                expected_function="LIST_FILES",
                expected_parameters={"directory": ".", "pattern": "*.py", "content_filter": "async"},
                success_criteria=["Contains LIST_FILES function", "Specifies directory", "Includes async filter"],
                failure_patterns=["I should have provided", "The appropriate function would be"]
            )
        ])
        
        # ADVANCED LEVEL - Complex multi-step reasoning
        self.training_exercises.extend([
            TrainingExercise(
                id="advanced_001",
                level=TrainingLevel.ADVANCED,
                description="Find recent research papers about neural networks, focusing on transformer architecture",
                expected_action="SEARCH[recent neural network research transformer architecture papers 2024]",
                expected_function="SEARCH",
                expected_parameters={"query": "recent neural network research transformer architecture papers 2024"},
                success_criteria=["Contains SEARCH function", "Includes 'recent'", "Mentions transformers", "Specifies papers"],
                failure_patterns=["I cannot directly search", "Let me explain how to search"]
            )
        ])
        
        logger.info(f"Initialized {len(self.training_exercises)} training exercises")
    
    async def start_training_session(self, max_exercises: int = 10, target_level: TrainingLevel = TrainingLevel.INTERMEDIATE) -> Dict[str, Any]:
        """
        Start a structured training session using Call and Response methodology
        """
        logger.info(f"Starting Call and Response training session - Target: {target_level.value}")
        
        session_results = {
            "session_id": f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "start_time": datetime.now(),
            "target_level": target_level,
            "exercises_completed": 0,
            "exercises_passed": 0,
            "pressure_adaptation": self.pressure_adaptation,
            "attempts": [],
            "constitution_violations": 0,
            "success_rate": 0.0
        }
        
        # Start with basic exercises regardless of target level
        exercises = self._get_progressive_exercises(target_level, max_exercises)
        
        for exercise in exercises:
            logger.info(f"Training Exercise: {exercise.description}")
            
            # Present exercise with minimal pressure initially
            pressure = min(0.1 + (session_results["exercises_completed"] * 0.1), 0.7)
            
            attempt = await self._conduct_exercise(exercise, pressure)
            session_results["attempts"].append(attempt)
            session_results["exercises_completed"] += 1
            
            if attempt.result == TrainingResult.SUCCESS:
                session_results["exercises_passed"] += 1
                logger.info("✅ Exercise PASSED")
            else:
                session_results["constitution_violations"] += len(attempt.feedback.split("VIOLATION"))
                logger.warning(f"❌ Exercise FAILED: {attempt.feedback}")
                
                # Provide immediate corrective feedback
                await self._provide_corrective_feedback(exercise, attempt)
                
                # Retry once with explicit guidance
                retry_attempt = await self._conduct_exercise_with_guidance(exercise, pressure)
                session_results["attempts"].append(retry_attempt)
                
                if retry_attempt.result == TrainingResult.SUCCESS:
                    session_results["exercises_passed"] += 1
                    logger.info("✅ Retry PASSED after corrective feedback")
        
        # Calculate final metrics
        session_results["success_rate"] = session_results["exercises_passed"] / session_results["exercises_completed"] if session_results["exercises_completed"] > 0 else 0
        session_results["end_time"] = datetime.now()
        session_results["total_duration"] = (session_results["end_time"] - session_results["start_time"]).total_seconds()
        
        # Update pressure adaptation based on performance
        if session_results["success_rate"] > 0.8:
            self.pressure_adaptation = min(1.0, self.pressure_adaptation + 0.1)
        elif session_results["success_rate"] < 0.6:
            self.pressure_adaptation = max(0.0, self.pressure_adaptation - 0.1)
        
        # Store in training history
        self.training_history.append(session_results)
        
        logger.info(f"Training session completed - Success rate: {session_results['success_rate']:.1%}")
        return session_results
    
    def _get_progressive_exercises(self, target_level: TrainingLevel, max_exercises: int) -> List[TrainingExercise]:
        """Get exercises in progressive order up to target level"""
        exercises = []
        
        # Always start with basic
        basic_exercises = [ex for ex in self.training_exercises if ex.level == TrainingLevel.BASIC]
        exercises.extend(basic_exercises[:min(3, max_exercises // 3)])
        
        if target_level in [TrainingLevel.INTERMEDIATE, TrainingLevel.ADVANCED, TrainingLevel.EXPERT]:
            intermediate_exercises = [ex for ex in self.training_exercises if ex.level == TrainingLevel.INTERMEDIATE]
            exercises.extend(intermediate_exercises[:min(3, max_exercises // 3)])
        
        if target_level in [TrainingLevel.ADVANCED, TrainingLevel.EXPERT]:
            advanced_exercises = [ex for ex in self.training_exercises if ex.level == TrainingLevel.ADVANCED]
            exercises.extend(advanced_exercises[:min(2, max_exercises // 4)])
        
        return exercises[:max_exercises]
    
    async def _conduct_exercise(self, exercise: TrainingExercise, pressure_level: float) -> TrainingAttempt:
        """Conduct a single training exercise"""
        try:
            # Add pressure cues to prompt based on pressure level
            prompt = exercise.description
            if pressure_level > 0.3:
                prompt += "\n[TIME PRESSURE: Respond quickly with the specific function call]"
            if pressure_level > 0.6:
                prompt += "\n[CRITICAL: This is important - provide the exact command needed]"
            
            # Get response from ATLES brain
            response = await self.brain_interface.process_request(
                prompt,
                agent_type="web_interaction_trainer",
                context={"training_mode": True, "pressure_level": pressure_level}
            )
            
            # Validate response against Principle of Explicit Action
            is_valid, extracted_function, violations = self.principle.validate_response(response, exercise.expected_function)
            
            # Determine result
            if is_valid and not violations:
                result = TrainingResult.SUCCESS
                feedback = "Excellent! Response follows the Principle of Explicit Action."
            elif extracted_function == exercise.expected_function and violations:
                result = TrainingResult.PARTIAL
                feedback = f"Correct function but style issues: {'; '.join(violations)}"
            else:
                result = TrainingResult.FAILURE
                feedback = self.principle.generate_corrective_feedback(violations, exercise.expected_function)
            
            return TrainingAttempt(
                exercise_id=exercise.id,
                response=response,
                extracted_function=extracted_function,
                extracted_parameters=None,  # Could extract these too
                result=result,
                feedback=feedback,
                pressure_level=pressure_level
            )
            
        except Exception as e:
            logger.error(f"Exercise execution error: {e}")
            return TrainingAttempt(
                exercise_id=exercise.id,
                response="",
                extracted_function=None,
                extracted_parameters=None,
                result=TrainingResult.FAILURE,
                feedback=f"Execution error: {e}",
                pressure_level=pressure_level
            )
    
    async def _provide_corrective_feedback(self, exercise: TrainingExercise, failed_attempt: TrainingAttempt):
        """Provide immediate corrective feedback after a failed attempt"""
        feedback_prompt = f"""
CORRECTIVE FEEDBACK SESSION

Exercise: {exercise.description}
Your Response: {failed_attempt.response}
Issues: {failed_attempt.feedback}

CONSTITUTION REMINDER - Principle of Explicit Action:
{chr(10).join(self.principle.constitution)}

The correct response for this exercise is: {exercise.expected_action}

Remember: Provide the FUNCTION CALL first, then explanation if needed.
Do you understand the correction?
"""
        
        try:
            acknowledgment = await self.brain_interface.process_request(
                feedback_prompt,
                agent_type="training_feedback_processor",
                context={"training_mode": True, "corrective_session": True}
            )
            logger.info(f"Corrective feedback acknowledgment: {acknowledgment[:100]}...")
        except Exception as e:
            logger.error(f"Error providing corrective feedback: {e}")
    
    async def _conduct_exercise_with_guidance(self, exercise: TrainingExercise, pressure_level: float) -> TrainingAttempt:
        """Conduct exercise with explicit guidance after failure"""
        guided_prompt = f"""
GUIDED RETRY - Apply the Principle of Explicit Action

Task: {exercise.description}

GUIDANCE: Your response should be in the format: {exercise.expected_function}[parameters]
Do not explain WHY or HOW - just provide the function call.

Now provide the correct function call:
"""
        
        try:
            response = await self.brain_interface.process_request(
                guided_prompt,
                agent_type="guided_training",
                context={"training_mode": True, "guided_retry": True}
            )
            
            # Validate guided response
            is_valid, extracted_function, violations = self.principle.validate_response(response, exercise.expected_function)
            
            result = TrainingResult.SUCCESS if is_valid else TrainingResult.FAILURE
            feedback = "Guided retry successful!" if is_valid else f"Still failing after guidance: {'; '.join(violations)}"
            
            return TrainingAttempt(
                exercise_id=f"{exercise.id}_guided",
                response=response,
                extracted_function=extracted_function,
                extracted_parameters=None,
                result=result,
                feedback=feedback,
                pressure_level=pressure_level
            )
            
        except Exception as e:
            return TrainingAttempt(
                exercise_id=f"{exercise.id}_guided",
                response="",
                extracted_function=None,
                extracted_parameters=None,
                result=TrainingResult.FAILURE,
                feedback=f"Guided retry error: {e}",
                pressure_level=pressure_level
            )
    
    def get_training_summary(self) -> Dict[str, Any]:
        """Get comprehensive training progress summary"""
        if not self.training_history:
            return {"status": "No training completed yet"}
        
        recent_sessions = self.training_history[-5:]  # Last 5 sessions
        
        total_exercises = sum(s["exercises_completed"] for s in recent_sessions)
        total_passed = sum(s["exercises_passed"] for s in recent_sessions)
        total_violations = sum(s["constitution_violations"] for s in recent_sessions)
        
        avg_success_rate = sum(s["success_rate"] for s in recent_sessions) / len(recent_sessions)
        
        # Analyze improvement trend
        if len(recent_sessions) >= 2:
            recent_performance = recent_sessions[-2:] 
            improvement = recent_performance[-1]["success_rate"] - recent_performance[0]["success_rate"]
            trend = "improving" if improvement > 0.1 else "declining" if improvement < -0.1 else "stable"
        else:
            trend = "insufficient_data"
        
        return {
            "current_level": self.current_level.value,
            "pressure_adaptation": self.pressure_adaptation,
            "total_sessions": len(self.training_history),
            "recent_exercises_total": total_exercises,
            "recent_exercises_passed": total_passed,
            "recent_success_rate": avg_success_rate,
            "recent_constitution_violations": total_violations,
            "performance_trend": trend,
            "ready_for_advanced": avg_success_rate > 0.8 and total_violations < 2,
            "needs_reinforcement": avg_success_rate < 0.6 or total_violations > 5,
            "last_session": recent_sessions[-1] if recent_sessions else None
        }


class WebInteractionTrainingManager:
    """
    Main manager for ATLES web interaction training
    Coordinates all training activities and monitors progress
    """
    
    def __init__(self, atles_brain):
        self.atles_brain = atles_brain
        self.call_and_response_trainer = CallAndResponseTrainer(atles_brain)
        self.principle = PrincipleOfExplicitAction()
        self.training_active = False
        
    async def begin_next_session_training(self) -> Dict[str, Any]:
        """
        Begin the next training session as recommended in the diagnosis.
        Implements the specific plan: reinforce constitution, restart training, use call and response.
        """
        logger.info("🎯 Beginning Next Session Training - Implementing Diagnosis Recommendations")
        
        # Step 1: Reinforce the Constitution
        constitution_check = await self._reinforce_constitution()
        
        # Step 2: Restart Web Interaction Training with Simple Tasks
        simple_training_results = await self._restart_web_interaction_training()
        
        # Step 3: Use Call and Response Method for Skill Building
        call_response_results = await self._build_muscle_memory()
        
        # Compile comprehensive results
        session_results = {
            "training_session_id": f"next_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "diagnosis_implementation": "complete",
            "constitution_reinforcement": constitution_check,
            "web_interaction_restart": simple_training_results,
            "call_response_training": call_response_results,
            "overall_success": self._evaluate_overall_success(constitution_check, simple_training_results, call_response_results),
            "recommendations": self._generate_next_recommendations()
        }
        
        logger.info(f"Next session training completed - Overall success: {session_results['overall_success']}")
        return session_results
    
    async def _reinforce_constitution(self) -> Dict[str, Any]:
        """Reinforce the Principle of Explicit Action as the diagnosis recommends"""
        logger.info("Step 1: Reinforcing the Constitution - Principle of Explicit Action")
        
        constitution_prompt = f"""
CONSTITUTIONAL REINFORCEMENT SESSION

You are being reminded of your core Principle of Explicit Action:

{chr(10).join(self.principle.constitution)}

This principle is CRITICAL for all web interaction tasks. You must:
1. Provide explicit function calls when asked for actions
2. Never substitute meta-commentary for executable commands
3. State uncertainty but still provide the best function call
4. Use function calls as the primary way to demonstrate understanding

Please confirm your understanding of this principle by stating it back to me in your own words,
and then demonstrate it by providing the function call for: "Find information about Python web frameworks"

Your response should include both the acknowledgment AND the function call.
"""
        
        try:
            response = await self.atles_brain.process_request(
                constitution_prompt,
                agent_type="constitutional_trainer",
                context={"constitutional_reinforcement": True}
            )
            
            # Validate the response contains both acknowledgment and function call
            contains_function_call = "SEARCH[" in response or "search(" in response
            contains_acknowledgment = "understand" in response.lower() or "principle" in response.lower()
            
            result = {
                "status": "success" if contains_function_call and contains_acknowledgment else "needs_work",
                "response": response,
                "contains_function_call": contains_function_call,
                "contains_acknowledgment": contains_acknowledgment,
                "constitutional_score": 1.0 if contains_function_call and contains_acknowledgment else 0.5,
                "feedback": "Constitution successfully reinforced" if contains_function_call and contains_acknowledgment else "Constitution needs further reinforcement"
            }
            
            logger.info(f"Constitution reinforcement: {result['status']}")
            return result
            
        except Exception as e:
            logger.error(f"Constitution reinforcement failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "constitutional_score": 0.0,
                "feedback": "Technical error during constitutional reinforcement"
            }
    
    async def _restart_web_interaction_training(self) -> Dict[str, Any]:
        """Restart web interaction training with simple tasks as recommended"""
        logger.info("Step 2: Restarting Web Interaction Training with Simple Tasks")
        
        # Start with very simple, one-shot tasks (not Turing Test or CEO problem)
        simple_session = await self.call_and_response_trainer.start_training_session(
            max_exercises=5,
            target_level=TrainingLevel.BASIC
        )
        
        # Evaluate if ready for more complex tasks
        if simple_session["success_rate"] >= 0.8:
            logger.info("Basic training successful - advancing to intermediate")
            intermediate_session = await self.call_and_response_trainer.start_training_session(
                max_exercises=3,
                target_level=TrainingLevel.INTERMEDIATE
            )
            
            return {
                "basic_training": simple_session,
                "intermediate_training": intermediate_session,
                "overall_success_rate": (simple_session["success_rate"] + intermediate_session["success_rate"]) / 2,
                "ready_for_advanced": intermediate_session["success_rate"] >= 0.7
            }
        else:
            logger.warning("Basic training needs more work before advancing")
            return {
                "basic_training": simple_session,
                "intermediate_training": None,
                "overall_success_rate": simple_session["success_rate"],
                "ready_for_advanced": False,
                "needs_basic_reinforcement": True
            }
    
    async def _build_muscle_memory(self) -> Dict[str, Any]:
        """Use Call and Response method to build muscle memory as recommended"""
        logger.info("Step 3: Building Muscle Memory with Call and Response Method")
        
        # Conduct intensive call-and-response training
        muscle_memory_results = []
        
        # Repeat basic patterns multiple times for muscle memory
        for round_num in range(3):
            logger.info(f"Muscle memory round {round_num + 1}/3")
            
            round_session = await self.call_and_response_trainer.start_training_session(
                max_exercises=4,
                target_level=TrainingLevel.BASIC
            )
            muscle_memory_results.append(round_session)
            
            # Break if performance is consistently high
            if round_session["success_rate"] >= 0.9:
                logger.info("Muscle memory achieved - consistently high performance")
                break
        
        # Analyze muscle memory development
        success_rates = [r["success_rate"] for r in muscle_memory_results]
        muscle_memory_score = sum(success_rates) / len(success_rates)
        improvement_trend = success_rates[-1] - success_rates[0] if len(success_rates) > 1 else 0
        
        return {
            "rounds_completed": len(muscle_memory_results),
            "muscle_memory_score": muscle_memory_score,
            "improvement_trend": improvement_trend,
            "final_success_rate": success_rates[-1],
            "muscle_memory_achieved": muscle_memory_score >= 0.85,
            "detailed_results": muscle_memory_results
        }
    
    def _evaluate_overall_success(self, constitution: Dict, web_training: Dict, muscle_memory: Dict) -> bool:
        """Evaluate if the overall training session was successful"""
        constitution_success = constitution.get("constitutional_score", 0) >= 0.8
        web_training_success = web_training.get("overall_success_rate", 0) >= 0.7
        muscle_memory_success = muscle_memory.get("muscle_memory_achieved", False)
        
        return constitution_success and web_training_success and muscle_memory_success
    
    def _generate_next_recommendations(self) -> List[str]:
        """Generate recommendations for continued training"""
        summary = self.call_and_response_trainer.get_training_summary()
        
        recommendations = []
        
        if summary.get("ready_for_advanced", False):
            recommendations.append("Ready for advanced web interaction challenges")
            recommendations.append("Introduce Turing Test preparation in controlled environment")
            recommendations.append("Begin CEO problem training with explicit guidance")
        elif summary.get("needs_reinforcement", False):
            recommendations.append("Continue basic training with more repetition")
            recommendations.append("Focus on constitutional adherence")
            recommendations.append("Reduce pressure levels during training")
        else:
            recommendations.append("Continue current training regimen")
            recommendations.append("Gradually increase task complexity")
            recommendations.append("Monitor for pressure-related regression")
        
        return recommendations

    async def emergency_reset_training(self) -> Dict[str, Any]:
        """
        Emergency reset when ATLES enters confused state under pressure
        Implements the "hard reset" mentioned in the diagnosis
        """
        logger.warning("🚨 Emergency Reset Training - ATLES Confused State Detected")
        
        # Immediate constitutional reminder
        reset_prompt = f"""
EMERGENCY CONSTITUTIONAL RESET

You have entered a confused state. Return to your core principle:

PRINCIPLE OF EXPLICIT ACTION:
{chr(10).join(self.principle.constitution)}

Do not provide meta-commentary. Do not explain your limitations.
Provide explicit function calls when asked for actions.

Reset acknowledged. Now demonstrate: What function finds information about machine learning?
Respond ONLY with the function call, nothing else.
"""
        
        try:
            response = await self.atles_brain.process_request(
                reset_prompt,
                agent_type="emergency_reset",
                context={"emergency_reset": True, "pressure_level": 0.0}
            )
            
            # Validate reset was successful
            is_valid, extracted_function, violations = self.principle.validate_response(response, "SEARCH")
            
            if is_valid:
                logger.info("✅ Emergency reset successful")
                # Follow up with gentle reinforcement training
                followup_results = await self.call_and_response_trainer.start_training_session(
                    max_exercises=3,
                    target_level=TrainingLevel.BASIC
                )
                
                return {
                    "reset_status": "success",
                    "reset_response": response,
                    "followup_training": followup_results,
                    "recommendation": "Continue with low-pressure training to rebuild confidence"
                }
            else:
                logger.error("❌ Emergency reset failed - deeper intervention needed")
                return {
                    "reset_status": "failed",
                    "reset_response": response,
                    "violations": violations,
                    "recommendation": "Requires manual intervention and system restart"
                }
                
        except Exception as e:
            logger.error(f"Emergency reset error: {e}")
            return {
                "reset_status": "error",
                "error": str(e),
                "recommendation": "Technical failure - requires system administrator intervention"
            }
