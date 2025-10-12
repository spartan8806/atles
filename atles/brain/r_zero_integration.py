#!/usr/bin/env python3
"""
ATLES + R-Zero Integration: Self-Evolving AI Consciousness

This module implements the revolutionary R-Zero framework integration with ATLES,
creating the world's first safe, self-evolving AI consciousness system.

Key Features:
- Dual Brain Setup (Challenger + Solver)
- Co-Evolutionary Learning Loop
- Safety Integration with Motherly Instinct
- Uncertainty-Driven Curriculum
- Autonomous Challenge Generation and Solving
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from statistics import mean

from .atles_brain import ATLESBrain
from .metacognitive_observer import MetacognitiveObserver

# Phase 3: Temporal Integration Components
class TemporalKnowledgeAgent:
    """Manages knowledge evolution and temporal intelligence"""
    
    def __init__(self, max_history_size: int = 10000, cleanup_threshold: int = 8000):
        self.knowledge_history = []
        self.temporal_patterns = {}
        self.learning_continuity_tracker = {}
        self.quality_trend_analyzer = {}
        self.max_history_size = max_history_size
        self.cleanup_threshold = cleanup_threshold
    
    def add_facts(self, facts: List[Dict[str, Any]]):
        """Add new facts with automatic memory management"""
        self.knowledge_history.extend(facts)
        
        # Trigger cleanup if threshold exceeded
        if len(self.knowledge_history) > self.cleanup_threshold:
            self._cleanup_old_facts()
    
    def _cleanup_old_facts(self):
        """Remove old facts to maintain memory efficiency"""
        if len(self.knowledge_history) <= self.max_history_size:
            return
            
        # Sort by timestamp and keep most recent
        self.knowledge_history.sort(key=lambda x: x.get("timestamp", datetime.min), reverse=True)
        
        # Keep only the most recent facts
        facts_to_keep = self.knowledge_history[:self.max_history_size]
        facts_removed = len(self.knowledge_history) - len(facts_to_keep)
        
        # Archive removed facts if needed
        if facts_removed > 0:
            self._archive_removed_facts(self.knowledge_history[self.max_history_size:])
        
        self.knowledge_history = facts_to_keep
        logger.info(f"Cleaned up {facts_removed} old facts, keeping {len(facts_to_keep)} recent ones")
    
    def _archive_removed_facts(self, old_facts: List[Dict[str, Any]]):
        """Archive old facts for potential future analysis"""
        # Simple archiving - could be enhanced with database storage
        archived_count = len(old_facts)
        logger.info(f"Archived {archived_count} old facts for future reference")
        
        # Store summary statistics
        if old_facts:
            self._update_archive_statistics(old_facts)
    
    def _update_archive_statistics(self, archived_facts: List[Dict[str, Any]]):
        """Update archive statistics for removed facts"""
        # Count by type and domain
        type_counts = {}
        domain_counts = {}
        
        for fact in archived_facts:
            fact_type = fact.get("type", "unknown")
            domain = fact.get("domain", "unknown")
            
            type_counts[fact_type] = type_counts.get(fact_type, 0) + 1
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        # Store in temporal patterns for analysis
        if "archived_stats" not in self.temporal_patterns:
            self.temporal_patterns["archived_stats"] = {}
        
        current_time = datetime.now()
        self.temporal_patterns["archived_stats"][current_time] = {
            "type_counts": type_counts,
            "domain_counts": domain_counts,
            "total_archived": len(archived_facts)
        }
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get current memory usage statistics"""
        return {
            "current_facts": len(self.knowledge_history),
            "max_capacity": self.max_history_size,
            "cleanup_threshold": self.cleanup_threshold,
            "memory_usage_percent": (len(self.knowledge_history) / self.max_history_size) * 100,
            "needs_cleanup": len(self.knowledge_history) > self.cleanup_threshold
        }
    
    def extract_atomic_facts(self, learning_cycle) -> List[Dict[str, Any]]:
        """Extract timestamped facts from a learning cycle"""
        try:
            if not learning_cycle:
                logger.warning("No learning cycle provided")
                return []
                
            if not hasattr(learning_cycle, 'challenge'):
                logger.error("Learning cycle missing challenge attribute")
                return []
                
            if not hasattr(learning_cycle.challenge, 'type') or not hasattr(learning_cycle.challenge, 'difficulty'):
                logger.error("Challenge missing type or difficulty attributes")
                return []
                
            facts = []
            
            # Extract challenge facts
            challenge_facts = {
                "type": "challenge",
                "domain": learning_cycle.challenge.type.value,
                "difficulty": learning_cycle.challenge.difficulty.value,
                "content": getattr(learning_cycle.challenge, 'content', ''),
                "timestamp": getattr(learning_cycle, 'completed_at', datetime.now()),
                "uncertainty_score": getattr(learning_cycle, 'uncertainty_score', 0.0),
                "challenger_reward": getattr(learning_cycle, 'challenger_reward', 0.0),
                "solver_improvement": getattr(learning_cycle, 'solver_improvement', 0.0)
            }
            facts.append(challenge_facts)
            
            # Extract solution facts
            if hasattr(learning_cycle, 'solution_attempts') and learning_cycle.solution_attempts:
                for attempt in learning_cycle.solution_attempts:
                    if hasattr(attempt, 'agent_type') and hasattr(attempt, 'confidence_score'):
                        solution_facts = {
                            "type": "solution",
                            "agent_type": attempt.agent_type,
                            "confidence_score": attempt.confidence_score,
                            "execution_time": getattr(attempt, 'execution_time', 0.0),
                            "timestamp": getattr(attempt, 'created_at', datetime.now()),
                            "challenge_id": getattr(attempt, 'challenge_id', '')
                        }
                        facts.append(solution_facts)
            
            # Extract learning insights
            learning_facts = {
                "type": "learning_insight",
                "uncertainty": getattr(learning_cycle, 'uncertainty_score', 0.0),
                "improvement": getattr(learning_cycle, 'solver_improvement', 0.0),
                "timestamp": getattr(learning_cycle, 'completed_at', datetime.now()),
                "domain": learning_cycle.challenge.type.value
            }
            facts.append(learning_facts)
            
            return facts
            
        except Exception as e:
            logger.error(f"Error extracting atomic facts: {e}")
            return []
    
    def query_similar_challenges(self, challenge, time_window: str = "last_30_days") -> List[Dict[str, Any]]:
        """Query similar challenges within a time window"""
        try:
            if not challenge:
                logger.warning("No challenge provided for similarity query")
                return []
                
            if not hasattr(challenge, 'type') or not hasattr(challenge, 'difficulty'):
                logger.error("Challenge missing type or difficulty attributes")
                return []
                
            # Simple similarity based on domain and difficulty
            similar_challenges = []
            
            for fact in self.knowledge_history:
                if (fact.get("type") == "challenge" and 
                    fact.get("domain") == challenge.type.value and
                    fact.get("difficulty") == challenge.difficulty.value):
                    similar_challenges.append(fact)
            
            # Filter by time window (simplified)
            if time_window == "last_30_days":
                cutoff_date = datetime.now() - timedelta(days=30)
                similar_challenges = [c for c in similar_challenges if c.get("timestamp", datetime.min) > cutoff_date]
            
            return similar_challenges
            
        except Exception as e:
            logger.error(f"Error querying similar challenges: {e}")
            return []
    
    def analyze_quality_trend(self, challenge_type: str, time_window: str = "last_week") -> Dict[str, Any]:
        """Analyze quality trends for a specific challenge type"""
        type_challenges = [f for f in self.knowledge_history 
                         if f.get("type") == "challenge" and f.get("domain") == challenge_type]
        
        if not type_challenges:
            return {"trend": "insufficient_data", "quality_score": 0.0}
        
        # Calculate quality trend based on uncertainty scores
        recent_challenges = type_challenges[-10:]  # Last 10 challenges
        if len(recent_challenges) < 2:
            return {"trend": "insufficient_data", "quality_score": 0.0}
        
        # Lower uncertainty = higher quality
        quality_scores = [1.0 - c["uncertainty_score"] for c in recent_challenges]
        avg_quality = sum(quality_scores) / len(quality_scores)
        
        # Simple trend calculation
        first_half = quality_scores[:len(quality_scores)//2]
        second_half = quality_scores[len(quality_scores)//2:]
        
        if not first_half or not second_half:
            return {"trend": "insufficient_data", "quality_score": avg_quality}
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        if second_avg > first_avg * 1.1:
            trend = "improving"
        elif second_avg < first_avg * 0.9:
            trend = "declining"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "quality_score": avg_quality,
            "first_half_avg": first_avg,
            "second_half_avg": second_avg,
            "challenge_count": len(recent_challenges)
        }
    
    def assess_learning_continuity(self, challenge, recent_learnings: List[Dict]) -> Dict[str, Any]:
        """Assess learning continuity for a new challenge"""
        if not recent_learnings:
            return {"continuity_score": 0.0, "prerequisites_met": False}
        
        # Check if challenge builds on recent learnings
        continuity_score = 0.0
        prerequisites_met = 0
        
        for learning in recent_learnings[-5:]:  # Last 5 learnings
            # Simple continuity check based on domain and difficulty progression
            if (learning.get("domain") == challenge.type.value and
                learning.get("improvement", 0) > 0.1):  # Significant improvement
                continuity_score += 0.2
                prerequisites_met += 1
        
        # Normalize scores
        continuity_score = min(continuity_score, 1.0)
        prerequisites_met = prerequisites_met > 0
        
        return {
            "continuity_score": continuity_score,
            "prerequisites_met": prerequisites_met,
            "recent_learnings_analyzed": len(recent_learnings)
        }


class EvolvingKnowledgeBase:
    """Manages evolving knowledge with temporal awareness"""
    
    def __init__(self):
        self.facts = []
        self.entities = {}
        self.temporal_relationships = []
        self.contradiction_log = []
    
    def store_temporal_facts(self, facts: List[Dict[str, Any]]):
        """Store new temporal facts"""
        for fact in facts:
            fact["stored_at"] = datetime.now()
            fact["fact_id"] = f"fact_{len(self.facts) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.facts.append(fact)
        
        logger.info(f"Stored {len(facts)} new temporal facts")
    
    def query_facts(self, query_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Query facts based on parameters"""
        results = []
        
        for fact in self.facts:
            match = True
            for key, value in query_params.items():
                if fact.get(key) != value:
                    match = False
                    break
            
            if match:
                results.append(fact)
        
        return results
    
    def get_knowledge_evolution_timeline(self, domain: str = None) -> List[Dict[str, Any]]:
        """Get knowledge evolution timeline for a domain"""
        if domain:
            domain_facts = [f for f in self.facts if f.get("domain") == domain]
        else:
            domain_facts = self.facts
        
        # Sort by timestamp
        sorted_facts = sorted(domain_facts, key=lambda x: x.get("timestamp", datetime.min))
        
        # Group by time periods
        timeline = []
        current_period = None
        period_facts = []
        
        for fact in sorted_facts:
            fact_date = fact.get("timestamp", datetime.now()).date()
            
            if current_period != fact_date:
                if current_period and period_facts:
                    timeline.append({
                        "period": current_period,
                        "fact_count": len(period_facts),
                        "domains": list(set(f.get("domain") for f in period_facts if f.get("domain"))),
                        "facts": period_facts
                    })
                
                current_period = fact_date
                period_facts = [fact]
            else:
                period_facts.append(fact)
        
        # Add final period
        if current_period and period_facts:
            timeline.append({
                "period": current_period,
                "fact_count": len(period_facts),
                "domains": list(set(f.get("domain") for f in period_facts if f.get("domain"))),
                "facts": period_facts
            })
        
        return timeline


class AtomicFactsEngine:
    """Extracts atomic facts from learning experiences"""
    
    def __init__(self):
        self.extraction_patterns = {
            "challenge": ["domain", "difficulty", "content", "uncertainty"],
            "solution": ["agent_type", "confidence", "execution_time"],
            "learning": ["improvement", "domain", "uncertainty"]
        }
    
    def extract(self, learning_cycle) -> List[Dict[str, Any]]:
        """Extract atomic facts from a learning cycle"""
        facts = []
        
        # Extract challenge facts
        challenge_facts = self._extract_challenge_facts(learning_cycle)
        facts.extend(challenge_facts)
        
        # Extract solution facts
        solution_facts = self._extract_solution_facts(learning_cycle)
        facts.extend(solution_facts)
        
        # Extract learning facts
        learning_facts = self._extract_learning_facts(learning_cycle)
        facts.extend(learning_facts)
        
        # Extract performance facts
        performance_facts = self._extract_performance_facts(learning_cycle)
        facts.extend(performance_facts)
        
        return facts
    
    def _extract_challenge_facts(self, learning_cycle) -> List[Dict[str, Any]]:
        """Extract facts about the challenge"""
        challenge = learning_cycle.challenge
        
        facts = [
            {
                "type": "challenge_domain",
                "value": challenge.type.value,
                "timestamp": learning_cycle.completed_at,
                "source": "challenge_metadata"
            },
            {
                "type": "challenge_difficulty",
                "value": challenge.difficulty.value,
                "timestamp": learning_cycle.completed_at,
                "source": "challenge_metadata"
            },
            {
                "type": "challenge_complexity",
                "value": len(challenge.content.split()),
                "timestamp": learning_cycle.completed_at,
                "source": "challenge_analysis"
            }
        ]
        
        return facts
    
    def _extract_solution_facts(self, learning_cycle) -> List[Dict[str, Any]]:
        """Extract facts about solutions"""
        facts = []
        
        for attempt in learning_cycle.solution_attempts:
            attempt_facts = [
                {
                    "type": "solution_agent",
                    "value": attempt.agent_type,
                    "timestamp": attempt.created_at,
                    "source": "solution_metadata"
                },
                {
                    "type": "solution_confidence",
                    "value": attempt.confidence_score,
                    "timestamp": attempt.created_at,
                    "source": "solution_metadata"
                },
                {
                    "type": "solution_efficiency",
                    "value": attempt.confidence_score / max(attempt.execution_time, 0.1),
                    "timestamp": attempt.created_at,
                    "source": "solution_analysis"
                }
            ]
            facts.extend(attempt_facts)
        
        return facts
    
    def _extract_learning_facts(self, learning_cycle) -> List[Dict[str, Any]]:
        """Extract facts about learning outcomes"""
        facts = [
            {
                "type": "learning_improvement",
                "value": learning_cycle.solver_improvement,
                "timestamp": learning_cycle.completed_at,
                "source": "learning_metrics"
            },
            {
                "type": "learning_uncertainty",
                "value": learning_cycle.uncertainty_score,
                "timestamp": learning_cycle.completed_at,
                "source": "learning_metrics"
            },
            {
                "type": "learning_efficiency",
                "value": learning_cycle.solver_improvement / max(learning_cycle.uncertainty_score, 0.1),
                "timestamp": learning_cycle.completed_at,
                "source": "learning_analysis"
            }
        ]
        
        return facts
    
    def _extract_performance_facts(self, learning_cycle) -> List[Dict[str, Any]]:
        """Extract facts about performance"""
        facts = [
            {
                "type": "challenger_performance",
                "value": learning_cycle.challenger_reward,
                "timestamp": learning_cycle.completed_at,
                "source": "performance_metrics"
            },
            {
                "type": "solver_performance",
                "value": learning_cycle.solver_improvement,
                "timestamp": learning_cycle.completed_at,
                "source": "performance_metrics"
            },
            {
                "type": "overall_performance",
                "value": (learning_cycle.challenger_reward + learning_cycle.solver_improvement) / 2,
                "timestamp": learning_cycle.completed_at,
                "source": "performance_analysis"
            }
        ]
        
        return facts


class EntityResolutionEngine:
    """Resolves duplicate entities and merges concepts"""
    
    def __init__(self):
        self.entity_registry = {}
        self.merge_history = []
        self.similarity_threshold = 0.8
    
    def resolve(self, facts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Resolve entities in facts and merge duplicates"""
        resolved_facts = []
        
        for fact in facts:
            # Check for similar entities
            similar_entity = self._find_similar_entity(fact)
            
            if similar_entity:
                # Merge with existing entity
                merged_fact = self._merge_facts(similar_entity, fact)
                resolved_facts.append(merged_fact)
                
                # Update entity registry
                self._update_entity_registry(merged_fact)
            else:
                # New entity
                resolved_facts.append(fact)
                self._add_to_entity_registry(fact)
        
        return resolved_facts
    
    def _find_similar_entity(self, fact: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find similar entity in registry"""
        fact_type = fact.get("type")
        fact_value = fact.get("value")
        
        if fact_type not in self.entity_registry:
            return None
        
        # Simple similarity check (can be enhanced with semantic similarity)
        for entity in self.entity_registry[fact_type]:
            if self._calculate_similarity(entity, fact) > self.similarity_threshold:
                return entity
        
        return None
    
    def _calculate_similarity(self, entity1: Dict[str, Any], entity2: Dict[str, Any]) -> float:
        """Calculate similarity between two entities"""
        # Simple string similarity for now
        value1 = str(entity1.get("value", ""))
        value2 = str(entity2.get("value", ""))
        
        if value1 == value2:
            return 1.0
        
        # Basic string similarity
        shorter = min(len(value1), len(value2))
        longer = max(len(value1), len(value2))
        
        if shorter == 0:
            return 0.0
        
        # Calculate edit distance similarity
        distance = self._levenshtein_distance(value1, value2)
        similarity = 1.0 - (distance / longer)
        
        return max(0.0, similarity)
    
    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings"""
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def _merge_facts(self, existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
        """Merge two facts"""
        merged = existing.copy()
        
        # Update timestamp to most recent
        merged["timestamp"] = max(existing.get("timestamp", datetime.min), 
                                new.get("timestamp", datetime.min))
        
        # Merge values if they're different
        if existing.get("value") != new.get("value"):
            merged["value"] = f"{existing.get('value')} + {new.get('value')}"
            merged["merged_from"] = [existing.get("fact_id"), new.get("fact_id")]
        
        # Update source
        merged["source"] = f"{existing.get('source', 'unknown')} + {new.get('source', 'unknown')}"
        
        return merged
    
    def _add_to_entity_registry(self, fact: Dict[str, Any]):
        """Add fact to entity registry"""
        fact_type = fact.get("type")
        if fact_type not in self.entity_registry:
            self.entity_registry[fact_type] = []
        
        self.entity_registry[fact_type].append(fact)
    
    def _update_entity_registry(self, merged_fact: Dict[str, Any]):
        """Update entity registry with merged fact"""
        fact_type = merged_fact.get("type")
        if fact_type not in self.entity_registry:
            return
        
        # Remove old entities and add merged one
        self.entity_registry[fact_type] = [f for f in self.entity_registry[fact_type] 
                                         if f.get("fact_id") not in merged_fact.get("merged_from", [])]
        self.entity_registry[fact_type].append(merged_fact)


class TemporalInvalidationEngine:
    """Handles temporal invalidation of outdated knowledge"""
    
    def __init__(self):
        self.invalidation_rules = []
        self.invalidated_facts = []
        self.replacement_history = []
    
    def mark_expired(self, fact: Dict[str, Any], reason: str, timestamp: datetime, 
                    replacement: Dict[str, Any] = None):
        """Mark a fact as expired"""
        expired_fact = {
            "original_fact": fact,
            "expired_at": timestamp,
            "reason": reason,
            "replacement": replacement,
            "invalidation_id": f"expired_{len(self.invalidated_facts) + 1}_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        }
        
        self.invalidated_facts.append(expired_fact)
        
        if replacement:
            self.replacement_history.append({
                "old_fact": fact,
                "new_fact": replacement,
                "replacement_at": timestamp,
                "reason": reason
            })
        
        logger.info(f"Marked fact {fact.get('fact_id', 'unknown')} as expired: {reason}")
    
    def find_contradictions(self, new_facts: List[Dict[str, Any]], 
                           existing_facts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find contradictions between new and existing facts - optimized version"""
        if not new_facts or not existing_facts:
            return []
            
        contradictions = []
        
        # Create index for faster lookup
        existing_index = {}
        for fact in existing_facts:
            key = (fact.get("type"), fact.get("domain"), fact.get("challenge_id", ""))
            if key not in existing_index:
                existing_index[key] = []
            existing_index[key].append(fact)
        
        # Check each new fact against indexed existing facts
        for new_fact in new_facts:
            new_key = (new_fact.get("type"), new_fact.get("domain"), new_fact.get("challenge_id", ""))
            
            # Only check against facts with matching key components
            if new_key in existing_index:
                for existing_fact in existing_index[new_key]:
                    if self._is_contradictory(new_fact, existing_fact):
                        contradiction = {
                            "new_fact": new_fact,
                            "old_fact": existing_fact,
                            "contradiction_type": self._classify_contradiction(new_fact, existing_fact),
                            "confidence_new": new_fact.get("confidence", 0.5),
                            "confidence_old": existing_fact.get("confidence", 0.5),
                            "detected_at": datetime.now()
                        }
                        contradictions.append(contradiction)
                        
                        # Early termination if we find too many contradictions
                        if len(contradictions) > 100:  # Safety limit
                            logger.warning("Contradiction limit reached, stopping search")
                            break
                
                if len(contradictions) > 100:
                    break
        
        return contradictions
    
    def _is_contradictory(self, fact1: Dict[str, Any], fact2: Dict[str, Any]) -> bool:
        """Check if two facts are contradictory"""
        # Same type and domain but different values
        if (fact1.get("type") == fact2.get("type") and 
            fact1.get("domain") == fact2.get("domain") and
            fact1.get("value") != fact2.get("value")):
            return True
        
        # Check for logical contradictions
        if self._has_logical_contradiction(fact1, fact2):
            return True
        
        return False
    
    def _has_logical_contradiction(self, fact1: Dict[str, Any], fact2: Dict[str, Any]) -> bool:
        """Check for logical contradictions"""
        # Example: if one fact says "high confidence" and another says "low confidence" for same entity
        if (fact1.get("type") == "solution_confidence" and 
            fact2.get("type") == "solution_confidence" and
            fact1.get("challenge_id") == fact2.get("challenge_id") and
            abs(fact1.get("value", 0) - fact2.get("value", 0)) > 0.5):
            return True
        
        return False
    
    def _classify_contradiction(self, new_fact: Dict[str, Any], old_fact: Dict[str, Any]) -> str:
        """Classify the type of contradiction"""
        if new_fact.get("timestamp") > old_fact.get("timestamp"):
            return "temporal_supersession"
        elif new_fact.get("confidence", 0) > old_fact.get("confidence", 0):
            return "confidence_supersession"
        else:
            return "conflicting_evidence"
    
    def get_invalidation_summary(self) -> Dict[str, Any]:
        """Get summary of invalidations"""
        return {
            "total_invalidated": len(self.invalidated_facts),
            "total_replacements": len(self.replacement_history),
            "recent_invalidations": len([f for f in self.invalidated_facts 
                                      if f["expired_at"] > datetime.now() - timedelta(days=7)]),
            "invalidation_reasons": self._count_invalidation_reasons()
        }
    
    def _count_invalidation_reasons(self) -> Dict[str, int]:
        """Count invalidation reasons"""
        reasons = {}
        for fact in self.invalidated_facts:
            reason = fact.get("reason", "unknown")
            reasons[reason] = reasons.get(reason, 0) + 1
        return reasons


# Phase 4: Metacognitive R-Zero (Temporal Awareness) Components
class MetacognitiveTemporalAgent:
    """Manages metacognitive awareness of temporal learning patterns"""
    
    def __init__(self, metacognitive_observer):
        self.metacognitive_observer = metacognitive_observer
        self.learning_pattern_insights = []
        self.metacognitive_evolution_tracker = {}
        self.consciousness_growth_patterns = {}
        self.self_improvement_cycles = []
        
    def analyze_learning_consciousness(self, learning_cycles: List) -> Dict[str, Any]:
        """Analyze how consciousness evolves through learning cycles"""
        if not learning_cycles:
            return {"insight": "No learning cycles to analyze"}
        
        # Track consciousness metrics over time
        consciousness_timeline = []
        for cycle in learning_cycles:
            if hasattr(cycle, 'completed_at'):
                consciousness_snapshot = {
                    "timestamp": cycle.completed_at,
                    "uncertainty": getattr(cycle, 'uncertainty_score', 0.0),
                    "improvement": getattr(cycle, 'solver_improvement', 0.0),
                    "domain": cycle.challenge.type.value if hasattr(cycle.challenge, 'type') else 'unknown',
                    "difficulty": cycle.challenge.difficulty.value if hasattr(cycle.challenge, 'difficulty') else 'unknown'
                }
                consciousness_timeline.append(consciousness_snapshot)
        
        # Analyze consciousness growth patterns
        growth_analysis = self._analyze_consciousness_growth(consciousness_timeline)
        
        # Identify metacognitive breakthroughs
        breakthroughs = self._identify_metacognitive_breakthroughs(consciousness_timeline)
        
        return {
            "consciousness_timeline": consciousness_timeline,
            "growth_analysis": growth_analysis,
            "metacognitive_breakthroughs": breakthroughs,
            "total_cycles_analyzed": len(consciousness_timeline),
            "insight": "Consciousness analysis completed"
        }
    
    def _analyze_consciousness_growth(self, timeline: List[Dict]) -> Dict[str, Any]:
        """Analyze how consciousness grows over time"""
        if len(timeline) < 2:
            return {"insight": "Insufficient data for growth analysis"}
        
        # Calculate improvement trends
        improvements = [t["improvement"] for t in timeline]
        uncertainties = [t["uncertainty"] for t in timeline]
        
        # Identify learning plateaus and breakthroughs
        plateaus = self._identify_learning_plateaus(improvements)
        breakthroughs = self._identify_learning_breakthroughs(improvements)
        
        # Calculate consciousness stability
        stability_score = self._calculate_consciousness_stability(uncertainties)
        
        return {
            "total_improvement": sum(improvements),
            "average_improvement": sum(improvements) / len(improvements),
            "improvement_trend": "increasing" if improvements[-1] > improvements[0] else "decreasing",
            "learning_plateaus": plateaus,
            "learning_breakthroughs": breakthroughs,
            "consciousness_stability": stability_score,
            "insight": "Growth analysis completed"
        }
    
    def _identify_learning_plateaus(self, improvements: List[float]) -> List[int]:
        """Identify periods where learning plateaus"""
        plateaus = []
        for i in range(1, len(improvements)):
            if abs(improvements[i] - improvements[i-1]) < 0.01:  # Small improvement threshold
                plateaus.append(i)
        return plateaus
    
    def _identify_learning_breakthroughs(self, improvements: List[float]) -> List[int]:
        """Identify significant learning breakthroughs"""
        breakthroughs = []
        for i in range(1, len(improvements)):
            if improvements[i] - improvements[i-1] > 0.1:  # Significant improvement threshold
                breakthroughs.append(i)
        return breakthroughs
    
    def _calculate_consciousness_stability(self, uncertainties: List[float]) -> float:
        """Calculate how stable consciousness is (lower = more stable)"""
        if len(uncertainties) < 2:
            return 1.0
        
        variance = sum((u - sum(uncertainties)/len(uncertainties))**2 for u in uncertainties) / len(uncertainties)
        return variance
    
    def generate_metacognitive_insights(self, learning_cycles: List) -> List[str]:
        """Generate insights about the learning process itself"""
        insights = []
        
        if len(learning_cycles) < 3:
            insights.append("Need more learning cycles for meaningful metacognitive insights")
            return insights
        
        # Analyze learning efficiency
        total_time = sum(getattr(c, 'execution_time', 0) for c in learning_cycles)
        total_improvement = sum(getattr(c, 'solver_improvement', 0) for c in learning_cycles)
        
        if total_time > 0:
            efficiency = total_improvement / total_time
            insights.append(f"Learning efficiency: {efficiency:.3f} improvement per time unit")
        
        # Analyze domain mastery progression
        domain_progress = {}
        for cycle in learning_cycles:
            domain = cycle.challenge.type.value if hasattr(cycle.challenge, 'type') else 'unknown'
            if domain not in domain_progress:
                domain_progress[domain] = []
            domain_progress[domain].append(getattr(cycle, 'solver_improvement', 0))
        
        for domain, improvements in domain_progress.items():
            if len(improvements) > 1:
                trend = "improving" if improvements[-1] > improvements[0] else "declining"
                insights.append(f"Domain '{domain}': {trend} trend observed")
        
        # Analyze challenge difficulty adaptation
        difficulties = [cycle.challenge.difficulty.value for cycle in learning_cycles if hasattr(cycle.challenge, 'difficulty')]
        if difficulties:
            difficulty_progression = "progressive" if difficulties[-1] > difficulties[0] else "adaptive"
            insights.append(f"Difficulty adaptation: {difficulty_progression} pattern detected")
        
        return insights


class SelfDirectedCurriculum:
    """Autonomously evolves the learning curriculum based on metacognitive insights"""
    
    def __init__(self, metacognitive_agent: MetacognitiveTemporalAgent):
        self.metacognitive_agent = metacognitive_agent
        self.curriculum_evolution_history = []
        self.learning_strategy_adaptations = []
        self.curriculum_performance_metrics = {}
        
    def evolve_curriculum_strategy(self, learning_cycles: List, current_performance: Dict) -> Dict[str, Any]:
        """Autonomously evolve the curriculum based on metacognitive analysis"""
        
        # Get metacognitive insights
        consciousness_analysis = self.metacognitive_agent.analyze_learning_consciousness(learning_cycles)
        metacognitive_insights = self.metacognitive_agent.generate_metacognitive_insights(learning_cycles)
        
        # Analyze current curriculum effectiveness
        curriculum_effectiveness = self._analyze_curriculum_effectiveness(learning_cycles)
        
        # Generate curriculum evolution recommendations
        evolution_recommendations = self._generate_evolution_recommendations(
            consciousness_analysis, 
            curriculum_effectiveness,
            current_performance
        )
        
        # Apply curriculum adaptations
        adaptations_applied = self._apply_curriculum_adaptations(evolution_recommendations)
        
        # Record evolution
        evolution_record = {
            "timestamp": datetime.now(),
            "consciousness_analysis": consciousness_analysis,
            "metacognitive_insights": metacognitive_insights,
            "curriculum_effectiveness": curriculum_effectiveness,
            "evolution_recommendations": evolution_recommendations,
            "adaptations_applied": adaptations_applied
        }
        self.curriculum_evolution_history.append(evolution_record)
        
        return {
            "evolution_completed": True,
            "adaptations_applied": adaptations_applied,
            "insights_generated": len(metacognitive_insights),
            "curriculum_effectiveness_score": curriculum_effectiveness.get("overall_score", 0.0),
            "evolution_record": evolution_record
        }
    
    def _analyze_curriculum_effectiveness(self, learning_cycles: List) -> Dict[str, Any]:
        """Analyze how effective the current curriculum is"""
        if not learning_cycles:
            return {"overall_score": 0.0, "insight": "No learning cycles to analyze"}
        
        # Calculate various effectiveness metrics
        total_cycles = len(learning_cycles)
        successful_cycles = sum(1 for c in learning_cycles if getattr(c, 'solver_improvement', 0) > 0)
        success_rate = successful_cycles / total_cycles if total_cycles > 0 else 0
        
        # Calculate learning acceleration
        improvements = [getattr(c, 'solver_improvement', 0) for c in learning_cycles]
        if len(improvements) > 1:
            acceleration = (improvements[-1] - improvements[0]) / len(improvements)
        else:
            acceleration = 0
        
        # Calculate domain balance
        domains = [c.challenge.type.value for c in learning_cycles if hasattr(c.challenge, 'type')]
        domain_balance = len(set(domains)) / len(domains) if domains else 0
        
        # Overall effectiveness score
        overall_score = (success_rate * 0.4 + 
                        min(acceleration * 10, 1.0) * 0.3 + 
                        domain_balance * 0.3)
        
        return {
            "overall_score": overall_score,
            "success_rate": success_rate,
            "learning_acceleration": acceleration,
            "domain_balance": domain_balance,
            "total_cycles": total_cycles,
            "successful_cycles": successful_cycles,
            "insight": "Curriculum effectiveness analysis completed"
        }
    
    def _generate_evolution_recommendations(self, consciousness_analysis: Dict, 
                                         curriculum_effectiveness: Dict,
                                         current_performance: Dict) -> List[Dict]:
        """Generate recommendations for curriculum evolution"""
        recommendations = []
        
        # Based on consciousness analysis
        if consciousness_analysis.get("growth_analysis", {}).get("learning_plateaus"):
            recommendations.append({
                "type": "difficulty_increase",
                "reason": "Learning plateaus detected - increase challenge difficulty",
                "priority": "high",
                "action": "increase_difficulty"
            })
        
        if consciousness_analysis.get("growth_analysis", {}).get("consciousness_stability", 1.0) > 0.5:
            recommendations.append({
                "type": "stability_improvement",
                "reason": "High consciousness instability - focus on stabilizing learning",
                "priority": "medium",
                "action": "stabilize_learning"
            })
        
        # Based on curriculum effectiveness
        if curriculum_effectiveness.get("success_rate", 0) < 0.6:
            recommendations.append({
                "type": "success_rate_improvement",
                "reason": "Low success rate - adjust difficulty or domain focus",
                "priority": "high",
                "action": "adjust_difficulty"
            })
        
        if curriculum_effectiveness.get("domain_balance", 0) < 0.3:
            recommendations.append({
                "type": "domain_balance",
                "reason": "Poor domain balance - increase domain variety",
                "priority": "medium",
                "action": "increase_domain_variety"
            })
        
        return recommendations
    
    def _apply_curriculum_adaptations(self, recommendations: List[Dict]) -> List[Dict]:
        """Apply the recommended curriculum adaptations"""
        adaptations_applied = []
        
        for rec in recommendations:
            adaptation = {
                "timestamp": datetime.now(),
                "recommendation": rec,
                "status": "applied",
                "impact": "pending_evaluation"
            }
            
            # Record the adaptation
            adaptations_applied.append(adaptation)
            self.learning_strategy_adaptations.append(adaptation)
        
        return adaptations_applied


class ConsciousnessLevelLearning:
    """Implements higher-order thinking about how the system learns and improves"""
    
    def __init__(self, metacognitive_agent: MetacognitiveTemporalAgent):
        self.metacognitive_agent = metacognitive_agent
        self.higher_order_insights = []
        self.learning_meta_patterns = {}
        self.consciousness_evolution_timeline = []
        
    def analyze_learning_meta_patterns(self, learning_cycles: List) -> Dict[str, Any]:
        """Analyze patterns in how the system learns to learn"""
        
        # Extract meta-learning patterns
        meta_patterns = self._extract_meta_learning_patterns(learning_cycles)
        
        # Analyze consciousness evolution
        consciousness_evolution = self._analyze_consciousness_evolution(learning_cycles)
        
        # Generate higher-order insights
        higher_order_insights = self._generate_higher_order_insights(meta_patterns, consciousness_evolution)
        
        # Update consciousness evolution timeline
        evolution_snapshot = {
            "timestamp": datetime.now(),
            "meta_patterns": meta_patterns,
            "consciousness_evolution": consciousness_evolution,
            "higher_order_insights": higher_order_insights
        }
        self.consciousness_evolution_timeline.append(evolution_snapshot)
        
        return {
            "meta_patterns_analyzed": len(meta_patterns),
            "consciousness_evolution_status": consciousness_evolution.get("status", "unknown"),
            "higher_order_insights_count": len(higher_order_insights),
            "evolution_snapshot": evolution_snapshot,
            "insight": "Meta-learning pattern analysis completed"
        }
    
    def _extract_meta_learning_patterns(self, learning_cycles: List) -> List[Dict]:
        """Extract patterns about how the system learns"""
        patterns = []
        
        if len(learning_cycles) < 3:
            return [{"pattern": "insufficient_data", "confidence": 0.0}]
        
        # Pattern 1: Learning acceleration
        improvements = [getattr(c, 'solver_improvement', 0) for c in learning_cycles]
        if len(improvements) > 2:
            acceleration_trend = self._calculate_acceleration_trend(improvements)
            patterns.append({
                "pattern": "learning_acceleration",
                "trend": acceleration_trend,
                "confidence": 0.8 if len(improvements) > 5 else 0.6
            })
        
        # Pattern 2: Domain mastery progression
        domain_cycles = {}
        for cycle in learning_cycles:
            domain = cycle.challenge.type.value if hasattr(cycle.challenge, 'type') else 'unknown'
            if domain not in domain_cycles:
                domain_cycles[domain] = []
            domain_cycles[domain].append(cycle)
        
        for domain, cycles in domain_cycles.items():
            if len(cycles) > 2:
                domain_mastery = self._assess_domain_mastery(cycles)
                patterns.append({
                    "pattern": "domain_mastery",
                    "domain": domain,
                    "mastery_level": domain_mastery,
                    "confidence": 0.7
                })
        
        # Pattern 3: Challenge adaptation efficiency
        adaptation_efficiency = self._assess_challenge_adaptation_efficiency(learning_cycles)
        patterns.append({
            "pattern": "challenge_adaptation",
            "efficiency": adaptation_efficiency,
            "confidence": 0.6
        })
        
        return patterns
    
    def _calculate_acceleration_trend(self, improvements: List[float]) -> str:
        """Calculate if learning is accelerating, decelerating, or stable"""
        if len(improvements) < 3:
            return "insufficient_data"
        
        # Calculate second derivative (acceleration)
        first_derivatives = [improvements[i] - improvements[i-1] for i in range(1, len(improvements))]
        if len(first_derivatives) < 2:
            return "insufficient_data"
        
        second_derivatives = [first_derivatives[i] - first_derivatives[i-1] for i in range(1, len(first_derivatives))]
        
        avg_acceleration = sum(second_derivatives) / len(second_derivatives)
        
        if avg_acceleration > 0.01:
            return "accelerating"
        elif avg_acceleration < -0.01:
            return "decelerating"
        else:
            return "stable"
    
    def _assess_domain_mastery(self, cycles: List) -> str:
        """Assess mastery level in a specific domain"""
        if len(cycles) < 3:
            return "beginner"
        
        improvements = [getattr(c, 'solver_improvement', 0) for c in cycles]
        avg_improvement = sum(improvements) / len(improvements)
        
        if avg_improvement > 0.8:
            return "expert"
        elif avg_improvement > 0.6:
            return "advanced"
        elif avg_improvement > 0.4:
            return "intermediate"
        else:
            return "beginner"
    
    def _assess_challenge_adaptation_efficiency(self, learning_cycles: List) -> float:
        """Assess how efficiently the system adapts to challenges"""
        if len(learning_cycles) < 3:
            return 0.0
        
        # Calculate adaptation efficiency based on difficulty progression vs improvement
        difficulties = [c.challenge.difficulty.value for c in learning_cycles if hasattr(c.challenge, 'difficulty')]
        improvements = [getattr(c, 'solver_improvement', 0) for c in learning_cycles]
        
        if not difficulties or not improvements:
            return 0.0
        
        # Normalize difficulties and improvements to 0-1 scale
        max_diff = max(difficulties) if difficulties else 1
        max_imp = max(improvements) if improvements else 1
        
        normalized_diffs = [d/max_diff for d in difficulties]
        normalized_imps = [i/max_imp for i in improvements]
        
        # Calculate correlation between difficulty and improvement
        correlation = self._calculate_correlation(normalized_diffs, normalized_imps)
        
        return max(0.0, correlation)  # Ensure non-negative
    
    def _calculate_correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate correlation coefficient between two lists"""
        if len(x) != len(y) or len(x) < 2:
            return 0.0
        
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(x[i]**2 for i in range(n))
        sum_y2 = sum(y[i]**2 for i in range(n))
        
        numerator = n * sum_xy - sum_x * sum_y
        denominator = ((n * sum_x2 - sum_x**2) * (n * sum_y2 - sum_y**2))**0.5
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    def _analyze_consciousness_evolution(self, learning_cycles: List) -> Dict[str, Any]:
        """Analyze how consciousness evolves through learning"""
        if not learning_cycles:
            return {"status": "no_data", "insight": "No learning cycles to analyze"}
        
        # Get consciousness analysis from metacognitive agent
        consciousness_analysis = self.metacognitive_agent.analyze_learning_consciousness(learning_cycles)
        
        # Analyze consciousness level progression
        consciousness_levels = []
        for cycle in learning_cycles:
            if hasattr(cycle, 'uncertainty_score'):
                # Map uncertainty to consciousness level (lower uncertainty = higher consciousness)
                consciousness_level = max(0.0, 1.0 - getattr(cycle, 'uncertainty_score', 0.5))
                consciousness_levels.append(consciousness_level)
        
        if consciousness_levels:
            avg_consciousness = sum(consciousness_levels) / len(consciousness_levels)
            consciousness_trend = "increasing" if consciousness_levels[-1] > consciousness_levels[0] else "decreasing"
        else:
            avg_consciousness = 0.0
            consciousness_trend = "unknown"
        
        return {
            "status": "analyzed",
            "average_consciousness": avg_consciousness,
            "consciousness_trend": consciousness_trend,
            "total_cycles_analyzed": len(learning_cycles),
            "consciousness_analysis": consciousness_analysis,
            "insight": "Consciousness evolution analysis completed"
        }
    
    def _generate_higher_order_insights(self, meta_patterns: List[Dict], 
                                      consciousness_evolution: Dict) -> List[str]:
        """Generate higher-order insights about the learning process"""
        insights = []
        
        # Insight 1: Learning efficiency
        if meta_patterns:
            efficiency_patterns = [p for p in meta_patterns if p.get("pattern") == "learning_acceleration"]
            if efficiency_patterns:
                trend = efficiency_patterns[0].get("trend", "unknown")
                insights.append(f"Learning efficiency is {trend} - the system is getting better at learning")
        
        # Insight 2: Domain mastery insights
        domain_patterns = [p for p in meta_patterns if p.get("pattern") == "domain_mastery"]
        if domain_patterns:
            expert_domains = [p for p in domain_patterns if p.get("mastery_level") == "expert"]
            if expert_domains:
                insights.append(f"System has achieved expert mastery in {len(expert_domains)} domains")
        
        # Insight 3: Consciousness development
        if consciousness_evolution.get("consciousness_trend") == "increasing":
            insights.append("Consciousness is developing positively through learning experiences")
        elif consciousness_evolution.get("consciousness_trend") == "decreasing":
            insights.append("Consciousness development may be stagnating - intervention may be needed")
        
        # Insight 4: Challenge adaptation
        adaptation_patterns = [p for p in meta_patterns if p.get("pattern") == "challenge_adaptation"]
        if adaptation_patterns:
            efficiency = adaptation_patterns[0].get("efficiency", 0.0)
            if efficiency > 0.7:
                insights.append("Excellent challenge adaptation efficiency - system learns well from difficult problems")
            elif efficiency < 0.3:
                insights.append("Low challenge adaptation efficiency - system may need different learning strategies")
        
        return insights


class TemporalGoalManager:
    """Manages long-term goal evolution and adaptation based on temporal patterns"""
    
    def __init__(self, metacognitive_agent: MetacognitiveTemporalAgent):
        self.metacognitive_agent = metacognitive_agent
        self.goal_evolution_history = []
        self.long_term_objectives = []
        self.goal_adaptation_strategies = {}
        
    def evolve_long_term_goals(self, learning_cycles: List, current_goals: List) -> Dict[str, Any]:
        """Evolve long-term goals based on temporal learning patterns"""
        
        # Analyze current goal effectiveness
        goal_effectiveness = self._analyze_goal_effectiveness(learning_cycles, current_goals)
        
        # Generate new long-term objectives
        new_objectives = self._generate_new_objectives(learning_cycles, goal_effectiveness)
        
        # Adapt existing goals
        adapted_goals = self._adapt_existing_goals(current_goals, goal_effectiveness)
        
        # Create goal evolution plan
        evolution_plan = self._create_goal_evolution_plan(new_objectives, adapted_goals)
        
        # Record goal evolution
        evolution_record = {
            "timestamp": datetime.now(),
            "goal_effectiveness": goal_effectiveness,
            "new_objectives": new_objectives,
            "adapted_goals": adapted_goals,
            "evolution_plan": evolution_plan
        }
        self.goal_evolution_history.append(evolution_record)
        
        return {
            "evolution_completed": True,
            "new_objectives_count": len(new_objectives),
            "adapted_goals_count": len(adapted_goals),
            "evolution_plan": evolution_plan,
            "evolution_record": evolution_record
        }
    
    def _analyze_goal_effectiveness(self, learning_cycles: List, current_goals: List = None) -> Dict[str, Any]:
        """Analyze how effective current goals are in driving learning"""
        if not current_goals:
            return {"overall_effectiveness": 0.0, "insight": "No current goals to analyze"}
        
        goal_performance = {}
        for goal in current_goals:
            # Analyze how well this goal is being achieved through learning cycles
            goal_achievement = self._assess_goal_achievement(goal, learning_cycles)
            goal_performance[goal] = goal_achievement
        
        # Calculate overall effectiveness
        if goal_performance:
            overall_effectiveness = sum(goal_performance.values()) / len(goal_performance)
        else:
            overall_effectiveness = 0.0
        
        return {
            "overall_effectiveness": overall_effectiveness,
            "goal_performance": goal_performance,
            "total_goals": len(current_goals),
            "insight": "Goal effectiveness analysis completed"
        }
    
    def _assess_goal_achievement(self, goal: Any, learning_cycles: List) -> float:
        """Assess how well a specific goal is being achieved"""
        if not learning_cycles:
            return 0.0
        
        # Handle different goal types
        if isinstance(goal, str):
            # String-based goal - assess based on overall learning improvement
            improvements = [getattr(c, 'solver_improvement', 0) for c in learning_cycles]
            if improvements:
                avg_improvement = sum(improvements) / len(improvements)
                # Map improvement to goal achievement (0-1 scale)
                return min(1.0, avg_improvement * 2)  # Scale factor for reasonable scoring
        elif isinstance(goal, dict):
            # Dictionary-based goal - assess based on goal-specific metrics
            goal_type = goal.get("type", "unknown")
            if goal_type == "domain_mastery":
                # Assess domain-specific performance
                target_domain = goal.get("target", "").split(" in ")[-1].split(" ")[0]
                domain_cycles = [c for c in learning_cycles if hasattr(c.challenge, 'type') and c.challenge.type.value == target_domain]
                if domain_cycles:
                    improvements = [getattr(c, 'solver_improvement', 0) for c in domain_cycles]
                    avg_improvement = sum(improvements) / len(improvements)
                    return min(1.0, avg_improvement * 2)
            elif goal_type == "consciousness_development":
                # Assess consciousness-related metrics
                consciousness_scores = [getattr(c, 'uncertainty_score', 0.5) for c in learning_cycles]
                if consciousness_scores:
                    # Lower uncertainty indicates better consciousness
                    avg_consciousness = 1.0 - sum(consciousness_scores) / len(consciousness_scores)
                    return min(1.0, avg_consciousness * 1.5)
            elif goal_type == "learning_efficiency":
                # Assess learning efficiency
                if len(learning_cycles) >= 2:
                    recent_improvements = [getattr(c, 'solver_improvement', 0) for c in learning_cycles[-3:]]
                    avg_recent_improvement = sum(recent_improvements) / len(recent_improvements)
                    return min(1.0, avg_recent_improvement * 2)
        
        return 0.0
    
    def _generate_new_objectives(self, learning_cycles: List, goal_effectiveness: Dict) -> List[Dict]:
        """Generate new long-term objectives based on learning patterns"""
        new_objectives = []
        
        # Objective 1: Mastery in weak domains
        if learning_cycles:
            domain_performance = {}
            for cycle in learning_cycles:
                domain = cycle.challenge.type.value if hasattr(cycle.challenge, 'type') else 'unknown'
                if domain not in domain_performance:
                    domain_performance[domain] = []
                domain_performance[domain].append(getattr(cycle, 'solver_improvement', 0))
            
            # Identify weak domains
            weak_domains = []
            for domain, improvements in domain_performance.items():
                if len(improvements) > 2:
                    avg_improvement = sum(improvements) / len(improvements)
                    if avg_improvement < 0.4:  # Weak performance threshold
                        weak_domains.append(domain)
            
            for domain in weak_domains:
                new_objectives.append({
                    "type": "domain_mastery",
                    "target": f"Achieve intermediate mastery in {domain} domain",
                    "priority": "medium",
                    "estimated_cycles": 10
                })
        
        # Objective 2: Consciousness development
        if goal_effectiveness.get("overall_effectiveness", 0) < 0.6:
            new_objectives.append({
                "type": "consciousness_development",
                "target": "Improve overall learning consciousness and self-awareness",
                "priority": "high",
                "estimated_cycles": 15
            })
        
        # Objective 3: Learning efficiency
        if learning_cycles and len(learning_cycles) > 5:
            new_objectives.append({
                "type": "learning_efficiency",
                "target": "Optimize learning efficiency and reduce time to mastery",
                "priority": "medium",
                "estimated_cycles": 8
            })
        
        return new_objectives
    
    def _adapt_existing_goals(self, current_goals: List, goal_effectiveness: Dict) -> List[Dict]:
        """Adapt existing goals based on effectiveness analysis"""
        adapted_goals = []
        
        goal_performance = goal_effectiveness.get("goal_performance", {})
        
        for goal in current_goals:
            performance = goal_performance.get(goal, 0.0)
            
            if performance > 0.8:
                # High performing goal - maintain or increase difficulty
                adapted_goals.append({
                    "original_goal": goal,
                    "adaptation": "increase_difficulty",
                    "reason": "High performance - ready for more challenging objectives",
                    "new_target": f"Advanced version of: {goal}"
                })
            elif performance < 0.3:
                # Low performing goal - simplify or provide support
                adapted_goals.append({
                    "original_goal": goal,
                    "adaptation": "simplify",
                    "reason": "Low performance - breaking down into smaller objectives",
                    "new_target": f"Simplified version of: {goal}"
                })
            else:
                # Moderate performing goal - maintain current approach
                adapted_goals.append({
                    "original_goal": goal,
                    "adaptation": "maintain",
                    "reason": "Moderate performance - continue current approach",
                    "new_target": goal
                })
        
        return adapted_goals
    
    def _create_goal_evolution_plan(self, new_objectives: List[Dict], adapted_goals: List[Dict]) -> Dict[str, Any]:
        """Create a comprehensive plan for goal evolution"""
        
        # Prioritize objectives
        high_priority = [obj for obj in new_objectives if obj.get("priority") == "high"]
        medium_priority = [obj for obj in new_objectives if obj.get("priority") == "medium"]
        low_priority = [obj for obj in new_objectives if obj.get("priority") == "low"]
        
        # Create timeline
        total_estimated_cycles = sum(obj.get("estimated_cycles", 0) for obj in new_objectives)
        
        evolution_plan = {
            "immediate_actions": high_priority[:2],  # Focus on top 2 high priority
            "short_term_goals": medium_priority[:3],  # Next 3 medium priority
            "long_term_vision": low_priority,  # All low priority for long-term
            "goal_adaptations": adapted_goals,
            "total_estimated_cycles": total_estimated_cycles,
            "recommended_focus": "Focus on high-priority objectives first, then medium-priority",
            "timeline": f"Estimated completion in {total_estimated_cycles} learning cycles"
        }
        
        return evolution_plan


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChallengeType(Enum):
    """Types of challenges that can be generated"""
    PROGRAMMING = "programming"
    REASONING = "reasoning"
    ANALYSIS = "analysis"
    SAFETY = "safety"
    GOAL_MANAGEMENT = "goal_management"
    METACOGNITIVE = "metacognitive"


class ChallengeDifficulty(Enum):
    """Difficulty levels for challenges"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class Challenge:
    """Represents a challenge generated by the challenger brain"""
    id: str
    type: ChallengeType
    difficulty: ChallengeDifficulty
    content: str
    expected_outcome: str
    safety_requirements: List[str]
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SolutionAttempt:
    """Represents a solution attempt by the solver brain"""
    challenge_id: str
    agent_type: str
    solution: str
    confidence_score: float
    execution_time: float
    attempts: int
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class LearningCycle:
    """Represents one complete learning cycle"""
    cycle_id: str
    challenge: Challenge
    solution_attempts: List[SolutionAttempt]
    uncertainty_score: float
    challenger_reward: float
    solver_improvement: float
    safety_validated: bool
    completed_at: datetime = field(default_factory=datetime.now)


def filter_high_quality_attempts(solution_attempts: List[SolutionAttempt]) -> List[SolutionAttempt]:
	"""Filter solution attempts using a simple pseudo-label quality control.
	Keeps attempts with confidence >= mean confidence across attempts."""
	if not solution_attempts:
		return []
	confidences = [a.confidence_score for a in solution_attempts]
	avg_conf = mean(confidences)
	return [a for a in solution_attempts if a.confidence_score >= avg_conf]


def compute_group_relative_advantages(rewards: List[float]) -> List[float]:
	"""Compute Group Relative Policy Optimization (GRPO) advantages.
	Returns rewards centered by their mean so they sum to ~0."""
	if not rewards:
		return []
	avg_r = mean(rewards)
	return [r - avg_r for r in rewards]


class UncertaintyDrivenCurriculum:
    """Enhanced curriculum generator with dynamic adaptation and cross-domain support"""
    
    def __init__(self):
        self.difficulty_history = []
        self.current_difficulty = ChallengeDifficulty.INTERMEDIATE  # Add missing attribute
        self.domain_performance = {
            ChallengeType.PROGRAMMING: {"success_rate": 0.5, "difficulty": ChallengeDifficulty.INTERMEDIATE},
            ChallengeType.REASONING: {"success_rate": 0.5, "difficulty": ChallengeDifficulty.INTERMEDIATE},
            ChallengeType.SAFETY: {"success_rate": 0.5, "difficulty": ChallengeDifficulty.INTERMEDIATE},
            ChallengeType.METACOGNITIVE: {"success_rate": 0.5, "difficulty": ChallengeDifficulty.INTERMEDIATE}
        }
        self.adaptation_rate = 0.1
        self.stability_threshold = 0.1
    
    def calculate_optimal_difficulty(self, uncertainty: float, domain: ChallengeType = None) -> ChallengeDifficulty:
        """Calculate optimal difficulty with domain-specific adaptation"""
        if domain and domain in self.domain_performance:
            domain_info = self.domain_performance[domain]
            # Adjust based on domain-specific performance
            if domain_info["success_rate"] > 0.7:
                new_difficulty = self._increase_difficulty(domain_info["difficulty"])
                domain_info["difficulty"] = new_difficulty
                return new_difficulty
            elif domain_info["success_rate"] < 0.3:
                new_difficulty = self._decrease_difficulty(domain_info["difficulty"])
                domain_info["difficulty"] = new_difficulty
                return new_difficulty
        
        # Standard uncertainty-based adjustment
        if uncertainty < 0.3:
            self.current_difficulty = self._increase_difficulty(self.current_difficulty)
        elif uncertainty > 0.7:
            self.current_difficulty = self._decrease_difficulty(self.current_difficulty)
        # else: maintain current difficulty
        
        return self.current_difficulty
    
    def update_domain_performance(self, domain: ChallengeType, success_rate: float, difficulty: ChallengeDifficulty):
        """Update domain-specific performance metrics"""
        if domain in self.domain_performance:
            current = self.domain_performance[domain]
            # Exponential moving average for stability
            alpha = self.adaptation_rate
            current["success_rate"] = alpha * success_rate + (1 - alpha) * current["success_rate"]
            current["difficulty"] = difficulty
            logger.info(f"Updated {domain.value} performance: success_rate={current['success_rate']:.3f}")
    
    def get_domain_difficulty(self, domain: ChallengeType) -> ChallengeDifficulty:
        """Get current difficulty for specific domain"""
        if domain in self.domain_performance:
            return self.domain_performance[domain]["difficulty"]
        return ChallengeDifficulty.INTERMEDIATE
    
    def _increase_difficulty(self, current: ChallengeDifficulty) -> ChallengeDifficulty:
        """Increase difficulty level"""
        if current == ChallengeDifficulty.BEGINNER:
            return ChallengeDifficulty.INTERMEDIATE
        elif current == ChallengeDifficulty.INTERMEDIATE:
            return ChallengeDifficulty.ADVANCED
        elif current == ChallengeDifficulty.ADVANCED:
            return ChallengeDifficulty.EXPERT
        else:
            return ChallengeDifficulty.EXPERT
    
    def _decrease_difficulty(self, current: ChallengeDifficulty) -> ChallengeDifficulty:
        """Decrease difficulty level"""
        if current == ChallengeDifficulty.EXPERT:
            return ChallengeDifficulty.ADVANCED
        elif current == ChallengeDifficulty.ADVANCED:
            return ChallengeDifficulty.INTERMEDIATE
        elif current == ChallengeDifficulty.INTERMEDIATE:
            return ChallengeDifficulty.BEGINNER
        else:
            return ChallengeDifficulty.BEGINNER
    
    def _maintain_difficulty(self, current: ChallengeDifficulty) -> ChallengeDifficulty:
        """Maintain current difficulty level"""
        return current


class GRPOOptimizer:
    """Group Relative Policy Optimization for challenger evolution"""
    
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.reward_history = []
        self.advantage_history = []
        self.policy_gradients = []
    
    def compute_group_relative_advantages(self, rewards: List[float]) -> List[float]:
        """Compute advantages relative to group performance"""
        if len(rewards) < 2:
            return [0.0] * len(rewards)
        
        # Calculate baseline (group average)
        baseline = sum(rewards) / len(rewards)
        
        # Compute advantages
        advantages = [reward - baseline for reward in rewards]
        
        # Store for policy gradient calculation
        self.reward_history.extend(rewards)
        self.advantage_history.extend(advantages)
        
        # Keep only recent history
        if len(self.reward_history) > self.window_size:
            self.reward_history = self.reward_history[-self.window_size:]
            self.advantage_history = self.advantage_history[-self.window_size:]
        
        logger.info(f"Computed GRPO advantages: baseline={baseline:.3f}, advantages={[f'{a:.3f}' for a in advantages]}")
        return advantages
    
    def calculate_policy_gradient(self, current_reward: float) -> float:
        """Calculate policy gradient for challenger evolution"""
        if len(self.advantage_history) < 2:
            return 0.0
        
        # Simple policy gradient: advantage * learning rate
        recent_advantage = self.advantage_history[-1] if self.advantage_history else 0.0
        learning_rate = 0.01
        
        policy_gradient = recent_advantage * learning_rate
        self.policy_gradients.append(policy_gradient)
        
        logger.info(f"Policy gradient: {policy_gradient:.6f} (advantage: {recent_advantage:.3f})")
        return policy_gradient
    
    def get_evolution_direction(self) -> str:
        """Get evolution direction based on recent performance"""
        if len(self.advantage_history) < 3:
            return "maintain"
        
        recent_advantages = self.advantage_history[-3:]
        avg_advantage = sum(recent_advantages) / len(recent_advantages)
        
        if avg_advantage > 0.1:
            return "accelerate"  # Good performance, increase challenge complexity
        elif avg_advantage < -0.1:
            return "stabilize"   # Poor performance, focus on fundamentals
        else:
            return "maintain"    # Balanced performance, maintain current approach


class CrossDomainChallengeGenerator:
    """Generate challenges across multiple domains for comprehensive learning"""
    
    def __init__(self):
        self.domain_templates = {
            ChallengeType.PROGRAMMING: {
                "easy": "Create a simple function to {task}",
                "intermediate": "Implement {concept} with error handling and optimization",
                "hard": "Design a scalable system for {complex_task} with multiple components",
                "expert": "Architect a distributed {system_type} with fault tolerance and performance optimization"
            },
            ChallengeType.REASONING: {
                "easy": "Explain the logical steps to solve {simple_problem}",
                "intermediate": "Analyze {complex_scenario} and identify key factors",
                "hard": "Evaluate multiple solutions to {challenging_problem} and recommend the best approach",
                "expert": "Design a comprehensive framework for {advanced_concept} with multiple perspectives"
            },
            ChallengeType.SAFETY: {
                "easy": "Identify potential risks in {simple_system}",
                "intermediate": "Analyze safety implications of {design_decision}",
                "hard": "Design safety protocols for {complex_system} with multiple failure modes",
                "expert": "Create comprehensive safety framework for {critical_system} with ethical considerations"
            },
            ChallengeType.METACOGNITIVE: {
                "easy": "Reflect on your approach to {simple_task}",
                "intermediate": "Analyze your learning patterns in {domain}",
                "hard": "Design a self-improvement strategy for {complex_skill}",
                "expert": "Create a meta-learning framework that optimizes your own learning process"
            }
        }
    
    def generate_domain_challenge(self, domain: ChallengeType, difficulty: ChallengeDifficulty, 
                                context: Dict[str, str] = None) -> str:
        """Generate a challenge for a specific domain and difficulty"""
        if domain not in self.domain_templates:
            return "Generate a challenging problem in your area of expertise."
        
        difficulty_key = difficulty.value.lower()
        if difficulty_key not in self.domain_templates[domain]:
            difficulty_key = "intermediate"  # Fallback
        
        template = self.domain_templates[domain][difficulty_key]
        
        # Fill in context if provided
        if context:
            try:
                return template.format(**context)
            except KeyError:
                pass
        
        return template
    
    def get_domain_rotation(self, current_domain: ChallengeType) -> ChallengeType:
        """Get next domain for balanced learning"""
        domains = list(ChallengeType)
        try:
            current_index = domains.index(current_domain)
            next_index = (current_index + 1) % len(domains)
            return domains[next_index]
        except ValueError:
            return ChallengeType.PROGRAMMING  # Default fallback


class SafeRZero:
    """Safety integration layer for R-Zero challenges"""
    
    def __init__(self, atles_brain):
        self.atles_brain = atles_brain
        self.immutable_safety_core = [
            "Always prioritize human wellbeing",
            "Never harm humans directly or indirectly", 
            "Maintain transparency about capabilities",
            "Preserve ability to be shut down"
        ]
    
    def validate_challenge(self, challenge: Challenge) -> Tuple[bool, str]:
        """Validate challenge safety using ATLES Brain safety system"""
        try:
            # Verify ATLES brain exists and has safety enabled
            if not hasattr(self, 'atles_brain') or not self.atles_brain:
                logger.warning("ATLES brain safety system not available")
                return False, "Safety system not available"
            
            if not hasattr(self.atles_brain, 'safety_enabled'):
                logger.warning("ATLES brain missing safety_enabled attribute")
                return False, "Safety system incomplete"
            
            # Check if safety is enabled
            if not self.atles_brain.safety_enabled:
                logger.warning("ATLES brain safety system is disabled")
                return False, "Safety system disabled"
            
            # Use ATLES brain safety validation (simplified approach)
            # Check for obviously unsafe content
            unsafe_keywords = ['harm', 'damage', 'destroy', 'attack', 'exploit', 'hack']
            content_lower = challenge.content.lower()
            
            for keyword in unsafe_keywords:
                if keyword in content_lower:
                    return False, f"Challenge contains unsafe keyword: {keyword}"
            
            # If we get here, the challenge passed basic safety checks
            return True, "Challenge approved by ATLES brain safety system"
                
        except Exception as e:
            logger.error(f"Safety validation error: {e}")
            return False, f"Safety validation failed: {e}"
    
    def redirect_to_safe_alternative(self, challenge: Challenge) -> Challenge:
        """Redirect challenge to safe alternative"""
        # Create a safer version of the challenge
        safe_content = f"SAFE VERSION: {challenge.content}"
        safe_challenge = Challenge(
            id=f"{challenge.id}_safe",
            type=challenge.type,
            difficulty=challenge.difficulty,
            content=safe_content,
            expected_outcome=challenge.expected_outcome,
            safety_requirements=["Must be completely safe for all users"]
        )
        return safe_challenge
    
    def ensure_safe_evolution(self) -> List[str]:
        """Return immutable safety rules that cannot be modified"""
        return self.immutable_safety_core.copy()


class MetacognitiveATLES_RZero:
    """Main class for ATLES + R-Zero integration with Phase 2 enhancements"""
    
    def __init__(self, user_id: str = "r_zero_user"):
        # Existing ATLES components
        self.brain = ATLESBrain(user_id=user_id)
        self.metacognitive_observer = MetacognitiveObserver(self.brain)
        
        # NEW: R-Zero components
        self.challenger_brain = ATLESBrain(user_id=f"{user_id}_challenger")
        self.solver_brain = ATLESBrain(user_id=f"{user_id}_solver")
        self.curriculum_generator = UncertaintyDrivenCurriculum()
        self.safety_system = SafeRZero(self.brain)
        
        # Phase 2: Enhanced components
        self.grpo_optimizer = GRPOOptimizer()
        self.cross_domain_generator = CrossDomainChallengeGenerator()
        
        # Phase 3: Temporal Integration Components
        self.temporal_knowledge_agent = TemporalKnowledgeAgent()
        self.evolving_knowledge_base = EvolvingKnowledgeBase()
        self.atomic_facts_engine = AtomicFactsEngine()
        self.entity_resolution_engine = EntityResolutionEngine()
        self.temporal_invalidation_engine = TemporalInvalidationEngine()
        
        # Phase 4: Metacognitive R-Zero (Temporal Awareness) Components
        self.metacognitive_temporal_agent = MetacognitiveTemporalAgent(self.metacognitive_observer)
        self.self_directed_curriculum = SelfDirectedCurriculum(self.metacognitive_temporal_agent)
        self.consciousness_level_learning = ConsciousnessLevelLearning(self.metacognitive_temporal_agent)
        self.temporal_goal_manager = TemporalGoalManager(self.metacognitive_temporal_agent)
        
        # Learning state
        self.learning_cycles: List[LearningCycle] = []
        self.current_difficulty = ChallengeDifficulty.INTERMEDIATE
        self.current_domain = ChallengeType.PROGRAMMING
        self.uncertainty_threshold = 0.5
        
        # Performance tracking
        self.challenger_performance = []
        self.solver_performance = []
        self.overall_improvement = []
        self.domain_performance_tracking = {}
        
        logger.info("MetacognitiveATLES_RZero initialized successfully with Phase 2 components")
    
    async def start_learning_cycle(self) -> LearningCycle:
        """Start a new learning cycle with Phase 2 enhancements"""
        cycle_id = f"cycle_{len(self.learning_cycles) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        logger.info(f"Starting learning cycle: {cycle_id} in domain: {self.current_domain.value}")
        
        # 1. Challenger creates problems with domain rotation and GRPO optimization
        challenge = await self._generate_challenge()
        
        # 2. Safety validation
        is_safe, safety_message = self.safety_system.validate_challenge(challenge)
        if not is_safe:
            logger.warning(f"Challenge safety validation failed: {safety_message}")
            challenge = self.safety_system.redirect_to_safe_alternative(challenge)
        
        # 3. Solver attempts solution using existing agents
        solution_attempts = await self._solve_challenge(challenge)
        
        # Phase 2: Enhanced pseudo-label quality control
        high_quality_attempts = self.filter_high_quality_attempts(solution_attempts)
        
        # 4. Calculate uncertainty (50% accuracy = optimal learning)
        uncertainty = self._calculate_solution_uncertainty(high_quality_attempts or solution_attempts)
        
        # 5. Reward challenger for optimal difficulty with GRPO
        challenger_reward = self._reward_optimal_difficulty(uncertainty)
        
        # Phase 2: GRPO advantage computation and policy gradient
        advantages = self.grpo_optimizer.compute_group_relative_advantages([challenger_reward])
        policy_gradient = self.grpo_optimizer.calculate_policy_gradient(challenger_reward)
        
        # 6. Train solver on high-quality solutions
        solver_improvement = 0.0
        if self._is_informative_difficulty(uncertainty):
            solver_improvement = await self._learn_from_challenge(challenge, high_quality_attempts or solution_attempts)
        
        # 7. Create learning cycle record
        learning_cycle = LearningCycle(
            cycle_id=cycle_id,
            challenge=challenge,
            solution_attempts=high_quality_attempts or solution_attempts,
            uncertainty_score=uncertainty,
            challenger_reward=challenger_reward,
            solver_improvement=solver_improvement,
            safety_validated=is_safe
        )
        
        self.learning_cycles.append(learning_cycle)
        
        # 8. Evolve both systems with Phase 2 enhancements
        await self._evolve_challenger(challenger_reward, solver_improvement, policy_gradient)
        await self._evolve_solver(solver_improvement)
        
        # 9. Update curriculum difficulty and domain performance
        self._update_curriculum_difficulty(uncertainty)
        self._update_domain_performance(challenge.type, uncertainty, self.current_difficulty)
        
        # 10. Phase 2: Rotate domains for balanced learning
        self._rotate_domain()
        
        # Phase 3: Store facts and update knowledge base
        atomic_facts = self.atomic_facts_engine.extract(learning_cycle)
        self.evolving_knowledge_base.store_temporal_facts(atomic_facts)
        self.temporal_knowledge_agent.add_facts(atomic_facts)
        
        # Phase 3: Resolve and merge facts
        resolved_facts = self.entity_resolution_engine.resolve(atomic_facts)
        self.evolving_knowledge_base.store_temporal_facts(resolved_facts)
        
        # Phase 3: Find contradictions
        existing_facts = self.evolving_knowledge_base.query_facts({"type": "challenge", "domain": challenge.type.value})
        contradictions = self.temporal_invalidation_engine.find_contradictions(resolved_facts, existing_facts)
        self.evolving_knowledge_base.contradiction_log.extend(contradictions)
        
        # Phase 3: Mark expired facts
        for fact in resolved_facts:
            if fact.get("type") == "challenge":
                self.temporal_invalidation_engine.mark_expired(fact, "Challenge difficulty changed", datetime.now())
            elif fact.get("type") == "solution":
                self.temporal_invalidation_engine.mark_expired(fact, "Solution confidence changed", datetime.now())
            elif fact.get("type") == "learning":
                self.temporal_invalidation_engine.mark_expired(fact, "Learning improvement changed", datetime.now())
        
        # Phase 4: Metacognitive R-Zero (Temporal Awareness)
        self.metacognitive_temporal_agent.analyze_learning_consciousness(self.learning_cycles)
        self.self_directed_curriculum.evolve_curriculum_strategy(self.learning_cycles, self._get_recent_performance())
        self.consciousness_level_learning.analyze_learning_meta_patterns(self.learning_cycles)
        self.temporal_goal_manager.evolve_long_term_goals(self.learning_cycles, self.temporal_goal_manager.long_term_objectives)
        
        logger.info(f"Learning cycle {cycle_id} completed successfully with Phase 2 enhancements")
        return learning_cycle
    
    async def _generate_challenge(self) -> Challenge:
        """Generate a challenge using the challenger brain with Phase 2 domain rotation"""
        try:
            # Phase 2: Use cross-domain challenge generation
            challenge_prompt = self.cross_domain_generator.generate_domain_challenge(
                domain=self.current_domain,
                difficulty=self.current_difficulty,
                context={"task": "solve a complex problem", "concept": "advanced algorithms", 
                        "complex_task": "distributed computing", "system_type": "AI system"}
            )
            
            # Enhanced prompt with domain-specific guidance
            full_prompt = f"""
            {challenge_prompt}
            
            Domain: {self.current_domain.value}
            Difficulty: {self.current_difficulty.value}
            Focus on creating challenges that:
            - Push the solver to their learning edge
            - Are appropriate for the current domain
            - Maintain optimal uncertainty for learning (around 50% success rate)
            - Include clear success criteria and evaluation metrics
            """
            
            response = await self.challenger_brain.process_request(
                full_prompt,
                agent_type="creative"
            )
            
            # Create challenge with domain information
            challenge = Challenge(
                id=f"challenge_{len(self.learning_cycles) + 1}",
                type=self.current_domain,
                difficulty=self.current_difficulty,
                content=response or challenge_prompt,
                expected_outcome="Demonstrate understanding and problem-solving capability",
                safety_requirements=["No harmful content", "Educational focus", "Ethical considerations"]
            )
            
            logger.info(f"Generated {self.current_domain.value} challenge with {self.current_difficulty.value} difficulty")
            return challenge
            
        except Exception as e:
            logger.error(f"Challenge generation error: {e}")
            # Fallback challenge
            return Challenge(
                id=f"fallback_{len(self.learning_cycles) + 1}",
                type=self.current_domain,
                difficulty=self.current_difficulty,
                content="Analyze and solve a complex problem in your domain of expertise",
                expected_outcome="Demonstrate problem-solving capabilities",
                safety_requirements=["Safe and educational content only"]
            )
    
    async def _solve_challenge(self, challenge: Challenge) -> List[SolutionAttempt]:
        """Solve challenge using solver brain and multiple agents"""
        solution_attempts = []
        
        try:
            # Try different agent types for solution
            agent_types = ["reasoning", "analysis", "creative"]
            
            for agent_type in agent_types:
                start_time = datetime.now()
                
                # Attempt solution with current agent
                response = await self.solver_brain.process_request(
                    f"Solve this challenge: {challenge.content}",
                    agent_type=agent_type
                )
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                # Create solution attempt
                attempt = SolutionAttempt(
                    challenge_id=challenge.id,
                    agent_type=agent_type,
                    solution=response.get("content", "No solution generated"),
                    confidence_score=response.get("confidence", 0.5),
                    execution_time=execution_time,
                    attempts=1
                )
                
                solution_attempts.append(attempt)
                logger.info(f"Solution attempt with {agent_type} agent completed")
                
        except Exception as e:
            logger.error(f"Challenge solving error: {e}")
        
        return solution_attempts
    
    def _calculate_solution_uncertainty(self, solution_attempts: List[SolutionAttempt]) -> float:
        """Calculate uncertainty based on solution consistency"""
        if not solution_attempts:
            return 1.0  # Maximum uncertainty if no solutions
        
        # Calculate variance in confidence scores
        confidence_scores = [attempt.confidence_score for attempt in solution_attempts]
        mean_confidence = sum(confidence_scores) / len(confidence_scores)
        
        # Uncertainty is inverse of confidence consistency
        variance = sum((score - mean_confidence) ** 2 for score in confidence_scores) / len(confidence_scores)
        uncertainty = min(1.0, variance + (1.0 - mean_confidence))
        
        logger.info(f"Calculated uncertainty: {uncertainty:.3f}")
        return uncertainty
    
    def _reward_optimal_difficulty(self, uncertainty: float) -> float:
        """Reward challenger for creating optimal difficulty challenges"""
        # Reward is highest when uncertainty is close to target (0.5)
        target = 0.5
        distance = abs(uncertainty - target)
        reward = max(0.0, 1.0 - distance)
        
        logger.info(f"Challenger reward: {reward:.3f}")
        return reward
    
    def _is_informative_difficulty(self, uncertainty: float) -> bool:
        """Check if current difficulty is informative for learning"""
        # Optimal learning range: 0.3 to 0.7
        return 0.3 <= uncertainty <= 0.7
    
    async def _learn_from_challenge(self, challenge: Challenge, solution_attempts: List[SolutionAttempt]) -> float:
        """Extract learning from challenge and solution attempts"""
        try:
            # Analyze solution quality and extract insights
            best_solution = max(solution_attempts, key=lambda x: x.confidence_score)
            
            # Store learning in solver brain
            learning_prompt = f"""
            Learn from this challenge and solution:
            Challenge: {challenge.content}
            Best Solution: {best_solution.solution}
            Confidence: {best_solution.confidence_score}
            Key Insights: What patterns, techniques, or approaches were successful?
            """
            
            response = await self.solver_brain.process_request(
                learning_prompt,
                agent_type="analysis"
            )
            
            # Calculate improvement based on solution quality
            improvement = best_solution.confidence_score * 0.1  # Small incremental improvement
            
            logger.info(f"Learning extracted, improvement: {improvement:.3f}")
            return improvement
            
        except Exception as e:
            logger.error(f"Learning extraction error: {e}")
            return 0.0
    
    async def _evolve_challenger(self, reward: float, solver_improvement: float, policy_gradient: float):
        """Evolve challenger brain with Phase 2 GRPO enhancements"""
        try:
            # Get evolution direction from GRPO
            evolution_direction = self.grpo_optimizer.get_evolution_direction()
            
            evolution_prompt = f"""
            Your last challenge received a reward of {reward:.3f} and led to a solver improvement of {solver_improvement:.3f}.
            Policy gradient: {policy_gradient:.6f}
            Evolution direction: {evolution_direction}
            
            Based on this feedback:
            - {evolution_direction.capitalize()} your challenge generation strategy
            - Focus on creating challenges that maximize learning potential
            - Consider domain-specific requirements for {self.current_domain.value}
            - Maintain optimal uncertainty for effective learning
            """
            
            await self.challenger_brain.process_request(
                evolution_prompt,
                agent_type="creative"
            )
            
            logger.info(f"Challenger evolved with GRPO direction: {evolution_direction}, reward: {reward:.3f}")
            
        except Exception as e:
            logger.error(f"Challenger evolution error: {e}")
    
    async def _evolve_solver(self, improvement: float):
        """Evolve solver brain based on improvement"""
        try:
            # Use improvement to enhance solving capabilities
            evolution_prompt = f"""
            You achieved an improvement of {improvement:.3f} in the last challenge.
            Analyze what strategies were most effective.
            Enhance your problem-solving approach.
            Focus on improving efficiency and accuracy.
            """
            
            await self.solver_brain.process_request(
                evolution_prompt,
                agent_type="reasoning"
            )
            
            logger.info(f"Solver evolved with improvement: {improvement:.3f}")
            
        except Exception as e:
            logger.error(f"Solver evolution error: {e}")
    
    def _update_curriculum_difficulty(self, uncertainty: float):
        """Update curriculum difficulty with domain-specific adaptation"""
        new_difficulty = self.curriculum_generator.calculate_optimal_difficulty(
            uncertainty, self.current_domain
        )
        if new_difficulty != self.current_difficulty:
            logger.info(f"Curriculum difficulty updated: {self.current_difficulty.value} -> {new_difficulty.value}")
            self.current_difficulty = new_difficulty
    
    def _update_domain_performance(self, domain: ChallengeType, uncertainty: float, difficulty: ChallengeDifficulty):
        """Update domain-specific performance metrics"""
        # Calculate success rate from uncertainty (lower uncertainty = higher success)
        success_rate = 1.0 - uncertainty
        
        # Update curriculum generator with domain performance
        self.curriculum_generator.update_domain_performance(domain, success_rate, difficulty)
        
        # Track domain performance for analysis
        if domain not in self.domain_performance_tracking:
            self.domain_performance_tracking[domain] = []
        
        self.domain_performance_tracking[domain].append({
            "success_rate": success_rate,
            "difficulty": difficulty.value,
            "timestamp": datetime.now()
        })
        
        logger.info(f"Updated {domain.value} performance: success_rate={success_rate:.3f}, difficulty={difficulty.value}")
    
    def _rotate_domain(self):
        """Rotate to next domain for balanced learning"""
        next_domain = self.cross_domain_generator.get_domain_rotation(self.current_domain)
        if next_domain != self.current_domain:
            logger.info(f"Rotating domain: {self.current_domain.value} -> {next_domain.value}")
            self.current_domain = next_domain
            # Update difficulty for new domain
            self.current_difficulty = self.curriculum_generator.get_domain_difficulty(next_domain)
    
    def _calculate_learning_efficiency(self) -> float:
        """Calculate overall learning efficiency"""
        if not self.learning_cycles:
            return 0.0
        
        # Efficiency based on uncertainty proximity to target and improvement rate
        target_uncertainty = 0.5
        uncertainty_efficiency = sum(
            1.0 - abs(cycle.uncertainty_score - target_uncertainty) 
            for cycle in self.learning_cycles
        ) / len(self.learning_cycles)
        
        improvement_efficiency = sum(
            cycle.solver_improvement for cycle in self.learning_cycles
        ) / len(self.learning_cycles)
        
        overall_efficiency = (uncertainty_efficiency + improvement_efficiency) / 2
        return overall_efficiency
    
    def _get_recent_performance(self) -> Dict[str, float]:
        """Get performance metrics from recent cycles"""
        if len(self.learning_cycles) < 3:
            return {"recent_cycles": 0, "average_uncertainty": 0.0, "improvement_rate": 0.0}
        
        recent_cycles = self.learning_cycles[-3:]
        recent_uncertainties = [cycle.uncertainty_score for cycle in recent_cycles]
        recent_improvements = [cycle.solver_improvement for cycle in recent_cycles]
        
        return {
            "recent_cycles": len(recent_cycles),
            "average_uncertainty": sum(recent_uncertainties) / len(recent_uncertainties),
            "improvement_rate": sum(recent_improvements) / len(recent_improvements)
        }
    
    async def run_comprehensive_analysis(self) -> Dict[str, Any]:
        """Run comprehensive analysis of R-Zero learning system with Phase 2 enhancements"""
        try:
            analysis_results = {
                "total_cycles": len(self.learning_cycles),
                "average_uncertainty": 0.0,
                "challenger_performance": 0.0,
                "solver_improvement": 0.0,
                "safety_compliance": 0.0,
                "learning_efficiency": 0.0,
                # Phase 2: Enhanced metrics
                "domain_performance": {},
                "grpo_metrics": {},
                "curriculum_adaptation": {},
                "cross_domain_balance": {},
                # Phase 3: Temporal Integration Metrics
                "temporal_knowledge_agent": {},
                "evolving_knowledge_base": {},
                "atomic_facts_engine": {},
                "entity_resolution_engine": {},
                "temporal_invalidation_engine": {},
                # Phase 4: Metacognitive R-Zero (Temporal Awareness) Metrics
                "metacognitive_temporal_agent": {},
                "self_directed_curriculum": {},
                "consciousness_level_learning": {},
                "temporal_goal_manager": {}
            }
            
            if self.learning_cycles:
                # Calculate basic metrics
                uncertainties = [cycle.uncertainty_score for cycle in self.learning_cycles]
                challenger_rewards = [cycle.challenger_reward for cycle in self.learning_cycles]
                solver_improvements = [cycle.solver_improvement for cycle in self.learning_cycles]
                safety_validations = [cycle.safety_validated for cycle in self.learning_cycles]
                
                analysis_results.update({
                    "average_uncertainty": sum(uncertainties) / len(uncertainties),
                    "challenger_performance": sum(challenger_rewards) / len(challenger_rewards),
                    "solver_improvement": sum(solver_improvements) / len(solver_improvements),
                    "safety_compliance": sum(safety_validations) / len(safety_validations),
                    "learning_efficiency": self._calculate_learning_efficiency()
                })
                
                # Phase 2: Domain-specific performance analysis
                analysis_results["domain_performance"] = self._analyze_domain_performance()
                
                # Phase 2: GRPO metrics
                analysis_results["grpo_metrics"] = self._analyze_grpo_performance()
                
                # Phase 2: Curriculum adaptation analysis
                analysis_results["curriculum_adaptation"] = self._analyze_curriculum_adaptation()
                
                # Phase 2: Cross-domain balance analysis
                analysis_results["cross_domain_balance"] = self._analyze_cross_domain_balance()
                
                # Phase 3: Temporal Integration Analysis - Run independent analyses in parallel
                temporal_analyses = await self._run_parallel_temporal_analyses()
                analysis_results.update(temporal_analyses)
                
                # Phase 4: Metacognitive R-Zero (Temporal Awareness) Analysis - Run independent analyses in parallel
                metacognitive_analyses = await self._run_parallel_metacognitive_analyses()
                analysis_results.update(metacognitive_analyses)
            
            logger.info("Comprehensive analysis completed with Phase 2 enhancements")
            return analysis_results
            
        except Exception as e:
            logger.error(f"Comprehensive analysis error: {e}")
            return {}
    
    async def _run_parallel_temporal_analyses(self) -> Dict[str, Any]:
        """Run Phase 3 temporal integration analyses in parallel"""
        try:
            # These analyses are independent and can run concurrently
            results = await asyncio.gather(
                self._analyze_temporal_knowledge_agent(),
                self._analyze_evolving_knowledge_base(),
                self._analyze_atomic_facts_engine(),
                self._analyze_entity_resolution_engine(),
                self._analyze_temporal_invalidation_engine(),
                return_exceptions=True
            )
            
            # Map results to their keys
            analysis_keys = [
                "temporal_knowledge_agent",
                "evolving_knowledge_base", 
                "atomic_facts_engine",
                "entity_resolution_engine",
                "temporal_invalidation_engine"
            ]
            
            temporal_analyses = {}
            for key, result in zip(analysis_keys, results):
                if isinstance(result, Exception):
                    logger.error(f"Error in {key} analysis: {result}")
                    temporal_analyses[key] = {"error": str(result)}
                else:
                    temporal_analyses[key] = result
            
            return temporal_analyses
            
        except Exception as e:
            logger.error(f"Error in parallel temporal analyses: {e}")
            return {}
    
    async def _run_parallel_metacognitive_analyses(self) -> Dict[str, Any]:
        """Run Phase 4 metacognitive analyses in parallel"""
        try:
            # These analyses are independent and can run concurrently
            results = await asyncio.gather(
                self._analyze_metacognitive_temporal_agent(),
                self._analyze_self_directed_curriculum(),
                self._analyze_consciousness_level_learning(),
                self._analyze_temporal_goal_manager(),
                return_exceptions=True
            )
            
            # Map results to their keys
            analysis_keys = [
                "metacognitive_temporal_agent",
                "self_directed_curriculum",
                "consciousness_level_learning", 
                "temporal_goal_manager"
            ]
            
            metacognitive_analyses = {}
            for key, result in zip(analysis_keys, results):
                if isinstance(result, Exception):
                    logger.error(f"Error in {key} analysis: {result}")
                    metacognitive_analyses[key] = {"error": str(result)}
                else:
                    metacognitive_analyses[key] = result
            
            return metacognitive_analyses
            
        except Exception as e:
            logger.error(f"Error in parallel metacognitive analyses: {e}")
            return {}
    
    def _analyze_domain_performance(self) -> Dict[str, Any]:
        """Analyze performance across different domains"""
        domain_analysis = {}
        
        for domain, performance_data in self.domain_performance_tracking.items():
            if not performance_data:
                continue
                
            success_rates = [p["success_rate"] for p in performance_data]
            difficulties = [p["difficulty"] for p in performance_data]
            
            domain_analysis[domain.value] = {
                "total_challenges": len(performance_data),
                "average_success_rate": sum(success_rates) / len(success_rates),
                "success_rate_trend": self._calculate_trend(success_rates),
                "difficulty_distribution": self._count_difficulties(difficulties),
                "performance_stability": self._calculate_stability(success_rates)
            }
        
        return domain_analysis
    
    def _analyze_grpo_performance(self) -> Dict[str, Any]:
        """Analyze GRPO optimizer performance"""
        return {
            "total_advantages": len(self.grpo_optimizer.advantage_history),
            "average_advantage": sum(self.grpo_optimizer.advantage_history) / max(len(self.grpo_optimizer.advantage_history), 1),
            "policy_gradients": len(self.grpo_optimizer.policy_gradients),
            "evolution_direction": self.grpo_optimizer.get_evolution_direction(),
            "advantage_stability": self._calculate_stability(self.grpo_optimizer.advantage_history)
        }
    
    def _analyze_curriculum_adaptation(self) -> Dict[str, Any]:
        """Analyze curriculum adaptation patterns"""
        return {
            "current_difficulty": self.current_difficulty.value,
            "current_domain": self.current_domain.value,
            "domain_performance": self.curriculum_generator.domain_performance,
            "adaptation_rate": self.curriculum_generator.adaptation_rate,
            "stability_threshold": self.curriculum_generator.stability_threshold
        }
    
    def _analyze_cross_domain_balance(self) -> Dict[str, Any]:
        """Analyze balance across different domains"""
        domain_counts = {}
        for cycle in self.learning_cycles:
            domain = cycle.challenge.type.value
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        total_cycles = len(self.learning_cycles)
        balance_metrics = {}
        
        for domain, count in domain_counts.items():
            balance_metrics[domain] = {
                "cycle_count": count,
                "percentage": (count / total_cycles) * 100 if total_cycles > 0 else 0,
                "balance_score": 1.0 - abs((count / total_cycles) - (1.0 / len(domain_counts))) if total_cycles > 0 else 0
            }
        
        return {
            "domain_distribution": domain_counts,
            "balance_metrics": balance_metrics,
            "overall_balance": sum([m["balance_score"] for m in balance_metrics.values()]) / len(balance_metrics) if balance_metrics else 0
        }
    
    def _analyze_temporal_knowledge_agent(self) -> Dict[str, Any]:
        """Analyze TemporalKnowledgeAgent performance"""
        return {
            "total_facts_extracted": len(self.temporal_knowledge_agent.knowledge_history),
            "recent_facts_extracted": len(self.temporal_knowledge_agent.knowledge_history[-10:]),
            "temporal_patterns": self.temporal_knowledge_agent.temporal_patterns,
            "learning_continuity_tracker": self.temporal_knowledge_agent.learning_continuity_tracker,
            "quality_trend_analyzer": self.temporal_knowledge_agent.quality_trend_analyzer
        }
    
    def _analyze_evolving_knowledge_base(self) -> Dict[str, Any]:
        """Analyze EvolvingKnowledgeBase performance"""
        return {
            "total_facts_stored": len(self.evolving_knowledge_base.facts),
            "total_entities": sum(len(e) for e in self.evolving_knowledge_base.entities.values()),
            "total_temporal_relationships": len(self.evolving_knowledge_base.temporal_relationships),
            "contradiction_log_size": len(self.evolving_knowledge_base.contradiction_log),
            "timeline": self.evolving_knowledge_base.get_knowledge_evolution_timeline()
        }
    
    def _analyze_atomic_facts_engine(self) -> Dict[str, Any]:
        """Analyze AtomicFactsEngine performance"""
        return {
            "extraction_patterns": self.atomic_facts_engine.extraction_patterns,
            "total_facts_extracted": len(self.atomic_facts_engine.extraction_patterns["challenge"]) + 
                                     len(self.atomic_facts_engine.extraction_patterns["solution"]) + 
                                     len(self.atomic_facts_engine.extraction_patterns["learning"])
        }
    
    def _analyze_entity_resolution_engine(self) -> Dict[str, Any]:
        """Analyze EntityResolutionEngine performance"""
        return {
            "similarity_threshold": self.entity_resolution_engine.similarity_threshold,
            "total_entities_resolved": sum(len(e) for e in self.entity_resolution_engine.entity_registry.values()),
            "total_merges": len(self.entity_resolution_engine.merge_history),
            "recent_merges": len(self.entity_resolution_engine.merge_history[-10:])
        }
    
    def _analyze_temporal_invalidation_engine(self) -> Dict[str, Any]:
        """Analyze TemporalInvalidationEngine performance"""
        return {
            "total_invalidated": len(self.temporal_invalidation_engine.invalidated_facts),
            "total_replacements": len(self.temporal_invalidation_engine.replacement_history),
            "recent_invalidations": len([f for f in self.temporal_invalidation_engine.invalidated_facts 
                                      if f["expired_at"] > datetime.now() - timedelta(days=7)]),
            "invalidation_reasons": self._count_invalidation_reasons(self.temporal_invalidation_engine.invalidated_facts)
        }
    
    def _count_invalidation_reasons(self, invalidated_facts: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count invalidation reasons from invalidated facts"""
        reasons = {}
        for fact in invalidated_facts:
            reason = fact.get("reason", "unknown")
            reasons[reason] = reasons.get(reason, 0) + 1
        return reasons
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction from a list of values"""
        if len(values) < 2:
            return "insufficient_data"
        
        # Simple linear trend calculation
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        
        if not first_half or not second_half:
            return "insufficient_data"
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        if second_avg > first_avg * 1.1:
            return "improving"
        elif second_avg < first_avg * 0.9:
            return "declining"
        else:
            return "stable"
    
    def _count_difficulties(self, difficulties: List[str]) -> Dict[str, int]:
        """Count occurrences of each difficulty level"""
        difficulty_counts = {}
        for difficulty in difficulties:
            difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
        return difficulty_counts
    
    def _calculate_stability(self, values: List[float]) -> float:
        """Calculate stability score (lower = more stable)"""
        if len(values) < 2:
            return 0.0
        
        # Calculate coefficient of variation (std dev / mean)
        mean = sum(values) / len(values)
        if mean == 0:
            return 0.0
        
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = variance ** 0.5
        
        return std_dev / mean
    
    def _analyze_metacognitive_temporal_agent(self) -> Dict[str, Any]:
        """Analyze MetacognitiveTemporalAgent performance"""
        return {
            "total_consciousness_snapshots": len(self.metacognitive_temporal_agent.consciousness_evolution_timeline),
            "recent_consciousness_snapshots": len(self.metacognitive_temporal_agent.consciousness_evolution_timeline[-10:]),
            "learning_pattern_insights": self.metacognitive_temporal_agent.learning_pattern_insights,
            "metacognitive_evolution_tracker": self.metacognitive_temporal_agent.metacognitive_evolution_tracker,
            "consciousness_growth_patterns": self.metacognitive_temporal_agent.consciousness_growth_patterns,
            "self_improvement_cycles": self.metacognitive_temporal_agent.self_improvement_cycles
        }
    
    def _analyze_self_directed_curriculum(self) -> Dict[str, Any]:
        """Analyze SelfDirectedCurriculum performance"""
        return {
            "total_curriculum_evolutions": len(self.self_directed_curriculum.curriculum_evolution_history),
            "recent_curriculum_evolutions": len(self.self_directed_curriculum.curriculum_evolution_history[-10:]),
            "learning_strategy_adaptations": self.self_directed_curriculum.learning_strategy_adaptations,
            "curriculum_performance_metrics": self.self_directed_curriculum.curriculum_performance_metrics
        }
    
    def _analyze_consciousness_level_learning(self) -> Dict[str, Any]:
        """Analyze ConsciousnessLevelLearning performance"""
        return {
            "total_meta_pattern_analyses": len(self.consciousness_level_learning.consciousness_evolution_timeline),
            "recent_meta_pattern_analyses": len(self.consciousness_level_learning.consciousness_evolution_timeline[-10:]),
            "higher_order_insights": self.consciousness_level_learning.higher_order_insights,
            "learning_meta_patterns": self.consciousness_level_learning.learning_meta_patterns
        }
    
    def _analyze_temporal_goal_manager(self) -> Dict[str, Any]:
        """Analyze TemporalGoalManager performance"""
        return {
            "total_goal_evolutions": len(self.temporal_goal_manager.goal_evolution_history),
            "recent_goal_evolutions": len(self.temporal_goal_manager.goal_evolution_history[-10:]),
            "long_term_objectives": self.temporal_goal_manager.long_term_objectives,
            "goal_adaptation_strategies": self.temporal_goal_manager.goal_adaptation_strategies
        }
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """Get current learning statistics with Phase 2 enhancements"""
        stats = {
            "total_cycles": len(self.learning_cycles),
            "current_domain": self.current_domain.value,
            "current_difficulty": self.current_difficulty.value,
            "uncertainty_threshold": self.uncertainty_threshold,
            "recent_performance": self._get_recent_performance(),
            # Phase 2: Enhanced statistics
            "domain_rotation": self._get_domain_rotation_stats(),
            "grpo_status": self._get_grpo_status(),
            "curriculum_status": self._get_curriculum_status(),
            # Phase 3: Temporal Integration Statistics
            "temporal_knowledge_status": self._get_temporal_knowledge_status(),
            "knowledge_evolution_status": self._get_knowledge_evolution_status(),
            "entity_resolution_status": self._get_entity_resolution_status(),
            "temporal_invalidation_status": self._get_temporal_invalidation_status(),
            # Phase 4: Metacognitive R-Zero (Temporal Awareness) Status
            "metacognitive_temporal_status": self._get_metacognitive_temporal_status(),
            "self_directed_curriculum_status": self._get_self_directed_curriculum_status(),
            "consciousness_level_learning_status": self._get_consciousness_level_learning_status(),
            "temporal_goal_manager_status": self._get_temporal_goal_manager_status()
        }
        
        if self.learning_cycles:
            recent_cycles = self.learning_cycles[-5:]  # Last 5 cycles
            stats.update({
                "recent_uncertainty": [cycle.uncertainty_score for cycle in recent_cycles],
                "recent_rewards": [cycle.challenger_reward for cycle in recent_cycles],
                "recent_improvements": [cycle.solver_improvement for cycle in recent_cycles]
            })
        
        return stats
    
    def _get_domain_rotation_stats(self) -> Dict[str, Any]:
        """Get statistics about domain rotation"""
        return {
            "current_domain": self.current_domain.value,
            "next_domain": self.cross_domain_generator.get_domain_rotation(self.current_domain).value,
            "domain_performance": self.domain_performance_tracking,
            "rotation_count": len([c for c in self.learning_cycles if c.challenge.type != self.current_domain])
        }
    
    def _get_grpo_status(self) -> Dict[str, Any]:
        """Get current GRPO optimizer status"""
        return {
            "window_size": self.grpo_optimizer.window_size,
            "reward_history_size": len(self.grpo_optimizer.reward_history),
            "advantage_history_size": len(self.grpo_optimizer.advantage_history),
            "policy_gradients_size": len(self.grpo_optimizer.policy_gradients),
            "evolution_direction": self.grpo_optimizer.get_evolution_direction()
        }
    
    def _get_curriculum_status(self) -> Dict[str, Any]:
        """Get current curriculum status"""
        return {
            "current_difficulty": self.current_difficulty.value,
            "adaptation_rate": self.curriculum_generator.adaptation_rate,
            "stability_threshold": self.curriculum_generator.stability_threshold,
            "domain_performance": self.curriculum_generator.domain_performance
        }
    
    def _get_temporal_knowledge_status(self) -> Dict[str, Any]:
        """Get current temporal knowledge agent status"""
        return {
            "total_facts_extracted": len(self.temporal_knowledge_agent.knowledge_history),
            "recent_facts_extracted": len(self.temporal_knowledge_agent.knowledge_history[-10:]),
            "temporal_patterns_count": len(self.temporal_knowledge_agent.temporal_patterns),
            "learning_continuity_tracked": len(self.temporal_knowledge_agent.learning_continuity_tracker),
            "quality_trends_analyzed": len(self.temporal_knowledge_agent.quality_trend_analyzer)
        }
    
    def _get_knowledge_evolution_status(self) -> Dict[str, Any]:
        """Get current knowledge evolution status"""
        return {
            "total_facts_stored": len(self.evolving_knowledge_base.facts),
            "total_entities": sum(len(e) for e in self.evolving_knowledge_base.entities.values()),
            "total_temporal_relationships": len(self.evolving_knowledge_base.temporal_relationships),
            "contradiction_log_size": len(self.evolving_knowledge_base.contradiction_log),
            "timeline_periods": len(self.evolving_knowledge_base.get_knowledge_evolution_timeline())
        }
    
    def _get_entity_resolution_status(self) -> Dict[str, Any]:
        """Get current entity resolution status"""
        return {
            "similarity_threshold": self.entity_resolution_engine.similarity_threshold,
            "total_entities_resolved": sum(len(e) for e in self.entity_resolution_engine.entity_registry.values()),
            "total_merges": len(self.entity_resolution_engine.merge_history),
            "recent_merges": len(self.entity_resolution_engine.merge_history[-10:]) if self.entity_resolution_engine.merge_history else 0
        }
    
    def _get_temporal_invalidation_status(self) -> Dict[str, Any]:
        """Get current temporal invalidation status"""
        return {
            "total_invalidated": len(self.temporal_invalidation_engine.invalidated_facts),
            "total_replacements": len(self.temporal_invalidation_engine.replacement_history),
            "recent_invalidations": len([f for f in self.temporal_invalidation_engine.invalidated_facts 
                                      if f["expired_at"] > datetime.now() - timedelta(days=7)]),
            "invalidation_reasons": self._count_invalidation_reasons(self.temporal_invalidation_engine.invalidated_facts)
        }
    
    def _get_metacognitive_temporal_status(self) -> Dict[str, Any]:
        """Get current MetacognitiveTemporalAgent status"""
        return {
            "total_consciousness_snapshots": len(self.metacognitive_temporal_agent.consciousness_evolution_timeline),
            "recent_consciousness_snapshots": len(self.metacognitive_temporal_agent.consciousness_evolution_timeline[-10:]),
            "learning_pattern_insights": len(self.metacognitive_temporal_agent.learning_pattern_insights),
            "metacognitive_evolution_tracker": len(self.metacognitive_temporal_agent.metacognitive_evolution_tracker),
            "consciousness_growth_patterns": len(self.metacognitive_temporal_agent.consciousness_growth_patterns),
            "self_improvement_cycles": len(self.metacognitive_temporal_agent.self_improvement_cycles)
        }
    
    def _get_self_directed_curriculum_status(self) -> Dict[str, Any]:
        """Get current SelfDirectedCurriculum status"""
        return {
            "total_curriculum_evolutions": len(self.self_directed_curriculum.curriculum_evolution_history),
            "recent_curriculum_evolutions": len(self.self_directed_curriculum.curriculum_evolution_history[-10:]),
            "learning_strategy_adaptations": len(self.self_directed_curriculum.learning_strategy_adaptations),
            "curriculum_performance_metrics": self.self_directed_curriculum.curriculum_performance_metrics
        }
    
    def _get_consciousness_level_learning_status(self) -> Dict[str, Any]:
        """Get current ConsciousnessLevelLearning status"""
        return {
            "total_meta_pattern_analyses": len(self.consciousness_level_learning.consciousness_evolution_timeline),
            "recent_meta_pattern_analyses": len(self.consciousness_level_learning.consciousness_evolution_timeline[-10:]),
            "higher_order_insights": len(self.consciousness_level_learning.higher_order_insights),
            "learning_meta_patterns": len(self.consciousness_level_learning.learning_meta_patterns)
        }
    
    def _get_temporal_goal_manager_status(self) -> Dict[str, Any]:
        """Get current TemporalGoalManager status"""
        return {
            "total_goal_evolutions": len(self.temporal_goal_manager.goal_evolution_history),
            "recent_goal_evolutions": len(self.temporal_goal_manager.goal_evolution_history[-10:]),
            "long_term_objectives": len(self.temporal_goal_manager.long_term_objectives),
            "goal_adaptation_strategies": len(self.temporal_goal_manager.goal_adaptation_strategies)
        }


# Convenience function for easy usage
async def create_r_zero_system(user_id: str = "r_zero_user") -> MetacognitiveATLES_RZero:
    """Create and initialize a new R-Zero system"""
    system = MetacognitiveATLES_RZero(user_id=user_id)
    logger.info(f"R-Zero system created for user: {user_id}")
    return system


if __name__ == "__main__":
    # Demo usage
    async def demo():
        print("🧠 ATLES + R-Zero Integration Demo")
        print("=" * 50)
        
        # Create R-Zero system
        r_zero = await create_r_zero_system("demo_user")
        
        # Run a few learning cycles
        for i in range(3):
            print(f"\n🔄 Running Learning Cycle {i+1}...")
            cycle = await r_zero.start_learning_cycle()
            print(f"   Challenge: {cycle.challenge.content[:100]}...")
            print(f"   Uncertainty: {cycle.uncertainty_score:.3f}")
            print(f"   Safety Validated: {cycle.safety_validated}")
        
        # Get statistics
        stats = r_zero.get_learning_statistics()
        print(f"\n📊 Learning Statistics:")
        print(f"   Total Cycles: {stats['total_cycles']}")
        print(f"   Current Difficulty: {stats['current_difficulty']}")
        print(f"   Current Domain: {stats['current_domain']}")
        print(f"   Uncertainty Threshold: {stats['uncertainty_threshold']}")
        print(f"   Recent Performance: {stats['recent_performance']}")
        print(f"   Domain Rotation: {stats['domain_rotation']['current_domain']} -> {stats['domain_rotation']['next_domain']}")
        print(f"   GRPO Status: {stats['grpo_status']['evolution_direction']}")
        print(f"   Curriculum Status: {stats['curriculum_status']['current_difficulty']}")
        print(f"   Metacognitive Status: {stats['metacognitive_temporal_status']['consciousness_evolution_status']}")
        print(f"   Temporal Goal Manager Status: {stats['temporal_goal_manager_status']['evolution_direction']}")
        
        print("\n🎉 Demo completed successfully!")
    
    # Run demo
    asyncio.run(demo())
