"""
Offline-First Response Processor - Replaces Enhanced Response Processor

This module provides offline-first response generation with confidence scoring,
replacing the complex enhanced_response_processor.py system.
"""

import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import re

logger = logging.getLogger(__name__)

@dataclass
class OfflineResponse:
    """Result of offline-first response generation."""
    content: str
    confidence_score: float
    confidence_level: str
    domain: str
    knowledge_freshness: str
    web_search_recommended: bool
    source: str
    timestamp: str

class OfflineFirstResponseProcessor:
    """
    Offline-first response processor that prioritizes internal knowledge
    with confidence scoring and intelligent fallback to web search.
    """
    
    def __init__(self):
        self.processing_history = []
        logger.info("Offline-first response processor initialized")
    
    def process_question(self, question: str, context: str = "") -> OfflineResponse:
        """
        Process a question using offline-first approach with confidence scoring.
        """
        try:
            # Analyze the question domain
            domain_analysis = self._analyze_question_domain(question)
            confidence_factors = self._assess_confidence_factors(question, domain_analysis)
            
            # Generate response using internal knowledge
            response_content = self._generate_internal_response(question, domain_analysis)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(confidence_factors)
            
            # Determine if web search is recommended
            needs_web_search = confidence_score < 0.7 or domain_analysis.get('requires_current_info', False)
            
            return OfflineResponse(
                content=response_content,
                confidence_score=confidence_score,
                confidence_level=self._get_confidence_level(confidence_score),
                domain=domain_analysis.get('domain', 'general'),
                knowledge_freshness=domain_analysis.get('freshness', 'stable'),
                web_search_recommended=needs_web_search,
                source="ATLES Internal Knowledge",
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error processing question: {e}")
            return OfflineResponse(
                content=f"Error processing question: {e}",
                confidence_score=0.0,
                confidence_level="error",
                domain="error",
                knowledge_freshness="unknown",
                web_search_recommended=True,
                source="ATLES Error Handler",
                timestamp=datetime.now().isoformat()
            )
    
    def _analyze_question_domain(self, question: str) -> Dict[str, Any]:
        """Analyze question to determine domain and knowledge requirements."""
        question_lower = question.lower()
        
        domains = {
            'healthcare': ['health', 'medical', 'disease', 'treatment', 'patient', 'diagnosis', 'therapy'],
            'technology': ['ai', 'artificial intelligence', 'machine learning', 'computer', 'software', 'programming'],
            'science': ['physics', 'chemistry', 'biology', 'research', 'experiment', 'theory'],
            'history': ['historical', 'past', 'ancient', 'century', 'war', 'civilization'],
            'current_events': ['recent', 'latest', 'news', 'today', 'current', '2024', '2025']
        }
        
        detected_domain = 'general'
        for domain, keywords in domains.items():
            if any(keyword in question_lower for keyword in keywords):
                detected_domain = domain
                break
        
        current_info_indicators = ['latest', 'recent', 'current', 'today', 'now', '2024', '2025', 'newest']
        requires_current_info = any(indicator in question_lower for indicator in current_info_indicators)
        
        return {
            'domain': detected_domain,
            'requires_current_info': requires_current_info,
            'freshness': 'current' if requires_current_info else 'stable'
        }
    
    def _assess_confidence_factors(self, question: str, domain_analysis: Dict[str, Any]) -> Dict[str, float]:
        """Assess factors that affect response confidence."""
        factors = {}
        
        # Question specificity
        question_length = len(question.split())
        factors['specificity'] = min(question_length / 20, 1.0)
        
        # Domain knowledge strength
        domain_strength = {
            'technology': 0.9,
            'science': 0.8,
            'healthcare': 0.7,
            'history': 0.8,
            'general': 0.6,
            'current_events': 0.3
        }
        factors['domain_strength'] = domain_strength.get(domain_analysis['domain'], 0.5)
        
        # Current information requirement penalty
        factors['current_info_penalty'] = 0.3 if domain_analysis['requires_current_info'] else 0.0
        
        # Question complexity penalty
        complexity_indicators = ['complex', 'detailed', 'comprehensive', 'thorough', 'in-depth']
        factors['complexity_penalty'] = 0.1 if any(indicator in question.lower() for indicator in complexity_indicators) else 0.0
        
        return factors
    
    def _generate_internal_response(self, question: str, domain_analysis: Dict[str, Any]) -> str:
        """Generate response using internal knowledge (no hardcoded replies)."""
        # This will be handled by the model's natural language generation
        # The function provides structure - actual content comes from the model
        return f"Based on my training knowledge about {domain_analysis['domain']}: {question}"
    
    def _calculate_confidence_score(self, factors: Dict[str, float]) -> float:
        """Calculate overall confidence score from individual factors."""
        weights = {
            'specificity': 0.2,
            'domain_strength': 0.4,
            'current_info_penalty': -0.3,
            'complexity_penalty': -0.1
        }
        
        confidence = 0.0
        for factor, weight in weights.items():
            confidence += factors.get(factor, 0.0) * weight
        
        return max(0.0, min(1.0, confidence))
    
    def _get_confidence_level(self, score: float) -> str:
        """Convert confidence score to human-readable level."""
        if score >= 0.9:
            return "very_high"
        elif score >= 0.8:
            return "high"
        elif score >= 0.7:
            return "moderate"
        elif score >= 0.5:
            return "low"
        else:
            return "very_low"

# Create a global instance for easy access
offline_processor = OfflineFirstResponseProcessor()

# Integration function for ATLES Brain
def integrate_enhanced_processor(atles_brain):
    """Integrate the enhanced response processor with ATLES Brain."""
    if not hasattr(atles_brain, 'enhanced_processor'):
        atles_brain.enhanced_processor = OfflineFirstResponseProcessor()
    return atles_brain.enhanced_processor