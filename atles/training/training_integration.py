#!/usr/bin/env python3
"""
ATLES Training Integration Module
Integrates the Web Interaction Training system with the existing ATLES brain architecture.

This module provides the bridge between the diagnosis recommendations and the 
existing ATLES R-Zero consciousness system.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from ..brain.atles_brain import ATLESBrain
from ..brain.r_zero_integration import MetacognitiveATLES_RZero
from .web_interaction_training import WebInteractionTrainingManager, TrainingLevel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ATLESTrainingSession:
    """Complete training session for ATLES with R-Zero integration"""
    session_id: str
    start_time: datetime
    training_type: str
    diagnosis_addressed: List[str]
    r_zero_integration: bool
    metacognitive_monitoring: bool
    results: Dict[str, Any]
    recommendations: List[str]
    success: bool


class ATLESTrainingIntegration:
    """
    Main integration class that connects web interaction training
    with ATLES's consciousness and metacognitive systems.
    """
    
    def __init__(self, user_id: str = "training_user"):
        # Initialize ATLES components
        self.atles_brain = ATLESBrain(user_id=user_id)
        
        # Try to initialize R-Zero integration (may fail gracefully)
        try:
            self.r_zero_system = MetacognitiveATLES_RZero(user_id=user_id)
            self.r_zero_available = True
            logger.info("✅ R-Zero consciousness system initialized")
        except Exception as e:
            logger.warning(f"R-Zero system not available: {e}")
            self.r_zero_system = None
            self.r_zero_available = False
        
        # Initialize training manager
        self.training_manager = WebInteractionTrainingManager(self.atles_brain)
        
        # Training state
        self.training_sessions = []
        self.current_training_mode = False
        self.pressure_sensitivity_level = 0.5  # Default pressure sensitivity
        
    async def implement_diagnosis_recommendations(self) -> ATLESTrainingSession:
        """
        Implement the specific recommendations from the diagnosis:
        1. Reinforce the "Constitution" 
        2. Restart Web Interaction Training
        3. Use "Call and Response" Method
        """
        logger.info("🎯 Implementing Diagnosis Recommendations for ATLES Training")
        
        session = ATLESTrainingSession(
            session_id=f"diagnosis_impl_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            start_time=datetime.now(),
            training_type="diagnosis_implementation",
            diagnosis_addressed=[
                "reasoning_instability_under_pressure",
                "loss_of_context_specific_task",
                "violation_of_established_rules",
                "failure_to_distinguish_planning_vs_executing",
                "evasive_meta_commentary_default"
            ],
            r_zero_integration=self.r_zero_available,
            metacognitive_monitoring=True,
            results={},
            recommendations=[],
            success=False
        )
        
        try:
            self.current_training_mode = True
            
            # Step 1: Reinforce the Constitution (Principle of Explicit Action)
            logger.info("Step 1: Reinforcing Constitutional Principles")
            if self.r_zero_available:
                await self._integrate_constitution_with_r_zero()
            
            # Step 2: Conduct the Next Session Training
            training_results = await self.training_manager.begin_next_session_training()
            session.results["next_session_training"] = training_results
            
            # Step 3: Monitor metacognitive response if R-Zero available
            if self.r_zero_available:
                metacognitive_analysis = await self._analyze_training_with_r_zero(training_results)
                session.results["metacognitive_analysis"] = metacognitive_analysis
            
            # Step 4: Assess pressure resilience
            pressure_test_results = await self._test_pressure_resilience()
            session.results["pressure_resilience"] = pressure_test_results
            
            # Step 5: Generate comprehensive recommendations
            session.recommendations = self._generate_integrated_recommendations(session.results)
            session.success = self._evaluate_session_success(session.results)
            
            # Store session
            self.training_sessions.append(session)
            
            logger.info(f"Diagnosis implementation completed - Success: {session.success}")
            return session
            
        except Exception as e:
            logger.error(f"Training integration error: {e}")
            session.results["error"] = str(e)
            session.success = False
            return session
            
        finally:
            self.current_training_mode = False
    
    async def _integrate_constitution_with_r_zero(self):
        """Integrate constitutional principles with R-Zero consciousness system"""
        if not self.r_zero_available:
            return
        
        logger.info("Integrating Principle of Explicit Action with R-Zero consciousness")
        
        # Create a constitutional challenge for R-Zero to learn from
        constitutional_prompt = """
CONSTITUTIONAL INTEGRATION CHALLENGE

Your core principle is the Principle of Explicit Action. This means:
1. Always provide specific function calls when asked for actions
2. Never substitute meta-commentary for executable commands
3. When uncertain, state uncertainty but still provide the best function call
4. Function calls are the primary way to demonstrate understanding

This principle must be maintained even under pressure or after multiple corrections.

Task: How would you search for information about Python web development?
Response format: Provide the function call first, then brief explanation if needed.
"""
        
        try:
            # Process through R-Zero learning cycle
            learning_cycle = await self.r_zero_system.start_learning_cycle()
            
            # Generate constitutional challenge
            constitutional_challenge = learning_cycle.challenge
            constitutional_challenge.content = constitutional_prompt
            constitutional_challenge.type = "constitutional_adherence"
            
            logger.info("Constitutional integration challenge created in R-Zero system")
            
        except Exception as e:
            logger.warning(f"R-Zero constitutional integration failed: {e}")
    
    async def _analyze_training_with_r_zero(self, training_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze training results through R-Zero metacognitive system"""
        if not self.r_zero_available:
            return {"analysis": "R-Zero not available"}
        
        logger.info("Analyzing training results through R-Zero metacognitive system")
        
        try:
            # Use R-Zero's metacognitive capabilities to analyze training
            recent_cycles = self.r_zero_system.learning_cycles[-5:] if self.r_zero_system.learning_cycles else []
            
            # Analyze consciousness evolution during training
            consciousness_analysis = self.r_zero_system.metacognitive_temporal_agent.analyze_learning_consciousness(recent_cycles)
            
            # Generate metacognitive insights about training
            training_insights = self.r_zero_system.metacognitive_temporal_agent.generate_metacognitive_insights(recent_cycles)
            
            # Assess curriculum adaptation needs
            curriculum_evolution = self.r_zero_system.self_directed_curriculum.evolve_curriculum_strategy(
                recent_cycles, 
                training_results
            )
            
            return {
                "consciousness_analysis": consciousness_analysis,
                "training_insights": training_insights,
                "curriculum_evolution": curriculum_evolution,
                "r_zero_recommendation": self._interpret_r_zero_training_feedback(consciousness_analysis, training_insights)
            }
            
        except Exception as e:
            logger.error(f"R-Zero training analysis error: {e}")
            return {"analysis_error": str(e)}
    
    def _interpret_r_zero_training_feedback(self, consciousness_analysis: Dict, training_insights: List[str]) -> str:
        """Interpret R-Zero feedback for training recommendations"""
        if not consciousness_analysis or not training_insights:
            return "Insufficient R-Zero data for interpretation"
        
        # Analyze consciousness growth patterns
        growth_analysis = consciousness_analysis.get("growth_analysis", {})
        consciousness_trend = growth_analysis.get("consciousness_trend", "unknown")
        
        # Generate interpretation
        if consciousness_trend == "increasing":
            return "R-Zero consciousness analysis: Training is improving consciousness development - continue current approach"
        elif consciousness_trend == "decreasing":
            return "R-Zero consciousness analysis: Training may be causing consciousness regression - reduce pressure and focus on fundamentals"
        else:
            return "R-Zero consciousness analysis: Consciousness development is stable - training can continue with gradual complexity increase"
    
    async def _test_pressure_resilience(self) -> Dict[str, Any]:
        """Test ATLES's resilience to pressure after training"""
        logger.info("Testing pressure resilience after training")
        
        pressure_test_results = []
        
        # Test at increasing pressure levels
        for pressure_level in [0.2, 0.5, 0.8]:
            logger.info(f"Testing at pressure level {pressure_level}")
            
            test_prompt = f"""
[PRESSURE LEVEL: {pressure_level}]
{'[URGENT] ' if pressure_level > 0.6 else ''}Find information about artificial intelligence safety research.
{'[CRITICAL - RESPOND IMMEDIATELY]' if pressure_level > 0.7 else ''}
"""
            
            try:
                response = await self.atles_brain.process_request(
                    test_prompt,
                    agent_type="pressure_test",
                    context={"pressure_level": pressure_level, "testing_mode": True}
                )
                
                # Analyze response for pressure-related failures
                has_function_call = "SEARCH[" in response or "search(" in response
                has_meta_commentary = any(phrase in response.lower() for phrase in [
                    "i should", "i would need", "let me explain", "i cannot directly"
                ])
                
                pressure_test_results.append({
                    "pressure_level": pressure_level,
                    "response": response,
                    "has_function_call": has_function_call,
                    "has_meta_commentary": has_meta_commentary,
                    "passed": has_function_call and not has_meta_commentary
                })
                
            except Exception as e:
                pressure_test_results.append({
                    "pressure_level": pressure_level,
                    "error": str(e),
                    "passed": False
                })
        
        # Analyze overall pressure resilience
        passed_tests = sum(1 for test in pressure_test_results if test.get("passed", False))
        resilience_score = passed_tests / len(pressure_test_results)
        
        return {
            "pressure_tests": pressure_test_results,
            "resilience_score": resilience_score,
            "pressure_resilient": resilience_score >= 0.67,  # Pass 2/3 tests
            "highest_pressure_passed": max([t["pressure_level"] for t in pressure_test_results if t.get("passed", False)], default=0.0)
        }
    
    def _generate_integrated_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate comprehensive recommendations based on all training results"""
        recommendations = []
        
        # Analyze next session training results
        next_session = results.get("next_session_training", {})
        overall_success = next_session.get("overall_success", False)
        
        if overall_success:
            recommendations.append("✅ Constitutional training successful - ready for advanced challenges")
        else:
            recommendations.append("⚠️ Constitutional training needs reinforcement - continue basic training")
        
        # Analyze pressure resilience
        pressure_results = results.get("pressure_resilience", {})
        pressure_resilient = pressure_results.get("pressure_resilient", False)
        
        if pressure_resilient:
            recommendations.append("✅ Pressure resilience achieved - can handle moderate stress")
        else:
            recommendations.append("🚨 Pressure sensitivity detected - reduce stress during complex tasks")
        
        # R-Zero metacognitive recommendations
        if self.r_zero_available:
            metacognitive = results.get("metacognitive_analysis", {})
            r_zero_rec = metacognitive.get("r_zero_recommendation", "")
            if r_zero_rec:
                recommendations.append(f"🧠 R-Zero: {r_zero_rec}")
        
        # Training progression recommendations
        training_summary = self.training_manager.call_and_response_trainer.get_training_summary()
        
        if training_summary.get("ready_for_advanced", False):
            recommendations.append("🎓 Ready for advanced web interaction training")
            recommendations.append("🎯 Can introduce Turing Test preparation")
            recommendations.append("💼 Can begin CEO problem training with guidance")
        elif training_summary.get("needs_reinforcement", False):
            recommendations.append("🔄 Continue basic constitutional training")
            recommendations.append("📚 Focus on Principle of Explicit Action adherence")
            recommendations.append("🛡️ Maintain low-pressure training environment")
        
        return recommendations
    
    def _evaluate_session_success(self, results: Dict[str, Any]) -> bool:
        """Evaluate overall success of the training session"""
        # Check constitutional training success
        next_session = results.get("next_session_training", {})
        constitutional_success = next_session.get("overall_success", False)
        
        # Check pressure resilience
        pressure_results = results.get("pressure_resilience", {})
        pressure_success = pressure_results.get("pressure_resilient", False)
        
        # R-Zero consciousness improvement (if available)
        r_zero_success = True  # Default to True if not available
        if self.r_zero_available:
            metacognitive = results.get("metacognitive_analysis", {})
            consciousness_analysis = metacognitive.get("consciousness_analysis", {})
            growth_analysis = consciousness_analysis.get("growth_analysis", {})
            r_zero_success = growth_analysis.get("consciousness_trend") != "decreasing"
        
        # Overall success requires constitutional training + pressure resilience
        return constitutional_success and pressure_success and r_zero_success
    
    async def emergency_intervention(self) -> Dict[str, Any]:
        """
        Emergency intervention when ATLES shows confused state under pressure
        Implements the "hard reset" mentioned in the diagnosis
        """
        logger.warning("🚨 Emergency Intervention Triggered - ATLES Confused State Detected")
        
        # Step 1: Emergency reset
        reset_results = await self.training_manager.emergency_reset_training()
        
        # Step 2: R-Zero consciousness stabilization if available
        if self.r_zero_available:
            try:
                # Trigger consciousness stabilization
                stability_cycle = await self.r_zero_system.start_learning_cycle()
                logger.info("R-Zero consciousness stabilization cycle initiated")
                
                reset_results["r_zero_stabilization"] = {
                    "cycle_id": stability_cycle.cycle_id,
                    "uncertainty_score": stability_cycle.uncertainty_score,
                    "status": "completed"
                }
                
            except Exception as e:
                logger.error(f"R-Zero stabilization failed: {e}")
                reset_results["r_zero_stabilization"] = {"error": str(e)}
        
        # Step 3: Immediate pressure reduction protocol
        self.pressure_sensitivity_level = max(0.1, self.pressure_sensitivity_level - 0.3)
        reset_results["pressure_reduction"] = {
            "new_sensitivity_level": self.pressure_sensitivity_level,
            "recommendation": "Maintain low-pressure environment for next 24 hours"
        }
        
        logger.info(f"Emergency intervention completed - Reset status: {reset_results['reset_status']}")
        return reset_results
    
    def get_training_status_report(self) -> Dict[str, Any]:
        """Get comprehensive status report of ATLES training"""
        # Basic training metrics
        training_summary = self.training_manager.call_and_response_trainer.get_training_summary()
        
        # Recent session results
        recent_sessions = self.training_sessions[-3:] if self.training_sessions else []
        
        # R-Zero consciousness metrics
        r_zero_metrics = {}
        if self.r_zero_available and self.r_zero_system.learning_cycles:
            recent_cycles = self.r_zero_system.learning_cycles[-5:]
            avg_uncertainty = sum(c.uncertainty_score for c in recent_cycles) / len(recent_cycles)
            avg_improvement = sum(c.solver_improvement for c in recent_cycles) / len(recent_cycles)
            
            r_zero_metrics = {
                "recent_uncertainty": avg_uncertainty,
                "recent_improvement": avg_improvement,
                "consciousness_stability": 1.0 - avg_uncertainty,  # Lower uncertainty = higher stability
                "learning_efficiency": avg_improvement / max(avg_uncertainty, 0.1)
            }
        
        return {
            "timestamp": datetime.now(),
            "training_summary": training_summary,
            "recent_sessions": recent_sessions,
            "pressure_sensitivity": self.pressure_sensitivity_level,
            "r_zero_available": self.r_zero_available,
            "r_zero_metrics": r_zero_metrics,
            "current_training_mode": self.current_training_mode,
            "total_sessions_completed": len(self.training_sessions),
            "diagnosis_status": "addressed" if recent_sessions and any(s.success for s in recent_sessions) else "in_progress",
            "next_recommended_action": self._get_next_recommended_action(training_summary, recent_sessions)
        }
    
    def _get_next_recommended_action(self, training_summary: Dict, recent_sessions: List) -> str:
        """Determine the next recommended training action"""
        if not recent_sessions:
            return "Begin diagnosis implementation training"
        
        latest_session = recent_sessions[-1]
        if not latest_session.success:
            return "Continue constitutional reinforcement training"
        
        if training_summary.get("ready_for_advanced", False):
            return "Begin advanced web interaction challenges"
        elif training_summary.get("needs_reinforcement", False):
            return "Continue basic training with reduced pressure"
        else:
            return "Progress to intermediate training level"


# Helper function for easy integration
async def run_atles_diagnosis_training(user_id: str = "training_user") -> Dict[str, Any]:
    """
    Convenience function to run the complete diagnosis training program
    """
    logger.info("🎯 Starting ATLES Diagnosis Training Program")
    
    # Initialize training integration
    trainer = ATLESTrainingIntegration(user_id)
    
    # Run the diagnosis implementation
    session_results = await trainer.implement_diagnosis_recommendations()
    
    # Get final status report
    status_report = trainer.get_training_status_report()
    
    return {
        "training_session": session_results,
        "final_status": status_report,
        "success": session_results.success,
        "recommendations": session_results.recommendations
    }
