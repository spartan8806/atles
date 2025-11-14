#!/usr/bin/env python3
"""
Truth-Seeking Pattern Matcher

Enhanced pattern matching system for detecting misinformation with:
- Synonym expansion
- Flexible word order matching
- Context-aware pattern detection
- Word boundary awareness
- Common phrasing variations
"""

import re
import logging
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class PatternMatch:
    """Result of a pattern match"""
    matched: bool
    pattern_type: str
    matched_pattern: Optional[str] = None
    confidence: float = 1.0


class PatternMatcher:
    """
    Enhanced pattern matcher with synonym support, flexible matching,
    and context awareness.
    """
    
    def __init__(self):
        """Initialize pattern matcher with synonym groups and variation handlers"""
        self.synonym_groups = self._initialize_synonym_groups()
        self.temporal_variations = self._initialize_temporal_variations()
        self.question_forms = self._initialize_question_forms()
        self.uncertainty_phrases = self._initialize_uncertainty_phrases()
        
    def _initialize_synonym_groups(self) -> Dict[str, List[str]]:
        """Initialize synonym groups for key concepts"""
        return {
            'wwii': [
                'world war ii', 'world war 2', 'world war two',
                'wwii', 'ww2', 'ww ii', 'ww 2',
                'second world war', 'world war second',
                'the second world war'
            ],
            'evs': [
                'electric vehicle', 'electric vehicles', 'evs', 'ev',
                'electric cars', 'electric car', 'electric automobiles',
                'electric auto', 'electric autos'
            ],
            'tesla': [
                'tesla', 'tesla motors', 'tsla', 'tesla inc',
                'tesla company'
            ],
            'elon_musk': [
                'elon musk', 'musk', 'elon', 'mr musk'
            ],
            'pi': [
                'pi', 'π', 'pi constant', 'pi number'
            ],
            'shutting_down': [
                'shutting down', 'shut down', 'closing', 'discontinuing',
                'ending', 'stopping', 'terminating', 'ceasing',
                'shutting', 'close down', 'close'
            ],
            'announced': [
                'announced', 'announcement', 'said', 'stated', 'reported',
                'revealed', 'declared', 'confirmed', 'told'
            ],
            'ended': [
                'ended', 'end', 'ending', 'concluded', 'conclusion',
                'finished', 'finish', 'came to an end', 'came to end',
                'was over', 'was finished', 'was concluded'
            ],
            '1944': [
                '1944', 'nineteen forty four', 'nineteen forty-four'
            ],
            '1945': [
                '1945', 'nineteen forty five', 'nineteen forty-five'
            ],
            'equals': [
                'equals', 'equal', 'is', 'was', 'equals to', 'equal to',
                'exactly', 'precisely', 'is exactly', 'is precisely'
            ],
            '3.0': [
                '3.0', '3', 'three', 'three point zero', 'three point oh'
            ]
        }
    
    def _initialize_temporal_variations(self) -> List[str]:
        """Common temporal phrase variations"""
        return [
            'ended', 'concluded', 'finished', 'came to an end',
            'was over', 'was finished', 'was concluded',
            'came to a close', 'wrapped up', 'terminated'
        ]
    
    def _initialize_question_forms(self) -> List[str]:
        """Common question form patterns"""
        return [
            r'did\s+(?:it|they|he|she)\s+',
            r'when\s+did\s+',
            r'was\s+(?:it|he|she|that)\s+',
            r'were\s+(?:they|you|we)\s+',
            r'is\s+(?:it|that|this)\s+',
            r'are\s+(?:they|you|we)\s+'
        ]
    
    def _initialize_uncertainty_phrases(self) -> List[str]:
        """Phrases indicating uncertainty or belief"""
        return [
            r'i\s+think',
            r'i\s+believe',
            r'my\s+understanding\s+is',
            r'i\s+was\s+told',
            r'i\s+heard',
            r'i\s+read',
            r'i\s+understand',
            r'from\s+what\s+i\s+know',
            r'as\s+i\s+understand\s+it'
        ]
    
    def expand_with_synonyms(self, words: List[str]) -> Set[str]:
        """
        Expand a list of words with their synonyms.
        
        Args:
            words: List of words/phrases to expand
            
        Returns:
            Set of all words including synonyms
        """
        expanded = set()
        words_lower = [w.lower() for w in words]
        
        for word in words_lower:
            expanded.add(word)
            # Check if word matches any synonym group
            for group_name, synonyms in self.synonym_groups.items():
                if word in synonyms:
                    expanded.update(synonyms)
                # Also check if any synonym contains the word
                for synonym in synonyms:
                    if word in synonym or synonym in word:
                        expanded.update(synonyms)
        
        return expanded
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize text for matching (lowercase, remove extra spaces).
        
        Args:
            text: Input text
            
        Returns:
            Normalized text
        """
        # Convert to lowercase
        normalized = text.lower()
        # Remove extra whitespace
        normalized = re.sub(r'\s+', ' ', normalized)
        # Remove leading/trailing whitespace
        normalized = normalized.strip()
        return normalized
    
    def match_flexible(self, text: str, required_words: List[str], 
                      context_words: Optional[List[str]] = None,
                      max_distance: int = 50) -> PatternMatch:
        """
        Match pattern with flexible word order.
        
        Args:
            text: Text to search in
            required_words: Words that must all be present
            context_words: Optional context words that should be present
            max_distance: Maximum character distance between words
            
        Returns:
            PatternMatch result
        """
        normalized = self.normalize_text(text)
        
        # Expand required words with synonyms
        expanded_words = self.expand_with_synonyms(required_words)
        
        # Check if all required words (or synonyms) are present
        found_words = []
        for word in expanded_words:
            # Use word boundary to avoid partial matches
            pattern = r'\b' + re.escape(word) + r'\b'
            if re.search(pattern, normalized):
                found_words.append(word)
        
        if not found_words:
            return PatternMatch(matched=False, pattern_type="flexible")
        
        # Check if we have enough matches (at least one synonym of each required word)
        required_sets = []
        for req_word in required_words:
            req_expanded = self.expand_with_synonyms([req_word])
            # Check if any synonym of this required word was found
            if any(fw in req_expanded for fw in found_words):
                required_sets.append(True)
        
        if len(required_sets) < len(required_words):
            return PatternMatch(matched=False, pattern_type="flexible")
        
        # Check context words if provided
        if context_words:
            expanded_context = self.expand_with_synonyms(context_words)
            context_found = any(
                re.search(r'\b' + re.escape(cw) + r'\b', normalized)
                for cw in expanded_context
            )
            if not context_found:
                return PatternMatch(matched=False, pattern_type="flexible")
        
        return PatternMatch(
            matched=True,
            pattern_type="flexible",
            matched_pattern=f"flexible:{'+'.join(required_words)}",
            confidence=1.0
        )
    
    def match_exact_pattern(self, text: str, pattern: str) -> PatternMatch:
        """
        Match exact regex pattern.
        
        Args:
            text: Text to search in
            pattern: Regex pattern
            
        Returns:
            PatternMatch result
        """
        normalized = self.normalize_text(text)
        
        try:
            if re.search(pattern, normalized):
                return PatternMatch(
                    matched=True,
                    pattern_type="exact",
                    matched_pattern=pattern,
                    confidence=1.0
                )
        except re.error as e:
            logger.warning(f"Invalid regex pattern '{pattern}': {e}")
        
        return PatternMatch(matched=False, pattern_type="exact")
    
    def match_with_context(self, text: str, key_concepts: List[str],
                          required_pattern: Optional[str] = None) -> PatternMatch:
        """
        Match pattern requiring multiple concepts to be present (context-aware).
        
        Args:
            text: Text to search in
            key_concepts: List of concept groups that must all be present
            required_pattern: Optional additional pattern that must match
            
        Returns:
            PatternMatch result
        """
        normalized = self.normalize_text(text)
        
        # Check if all key concepts are present
        concept_matches = []
        for concept_group in key_concepts:
            expanded = self.expand_with_synonyms([concept_group])
            found = any(
                re.search(r'\b' + re.escape(c) + r'\b', normalized)
                for c in expanded
            )
            concept_matches.append(found)
        
        if not all(concept_matches):
            return PatternMatch(matched=False, pattern_type="context")
        
        # Check additional pattern if provided
        if required_pattern:
            if not re.search(required_pattern, normalized):
                return PatternMatch(matched=False, pattern_type="context")
        
        return PatternMatch(
            matched=True,
            pattern_type="context",
            matched_pattern=f"context:{'+'.join(key_concepts)}",
            confidence=1.0
        )
    
    def match_wwii_1944(self, text: str) -> PatternMatch:
        """
        Specialized matcher for WWII ended in 1944 misinformation.
        Handles variations like "it ended in 1944" when WWII is mentioned.
        """
        normalized = self.normalize_text(text)
        
        # Check for WWII context
        wwii_expanded = self.expand_with_synonyms(['wwii'])
        has_wwii_context = any(
            re.search(r'\b' + re.escape(ww) + r'\b', normalized)
            for ww in wwii_expanded
        )
        
        # Check for 1944
        has_1944 = re.search(r'\b1944\b', normalized)
        
        # Check for temporal phrases indicating end
        temporal_pattern = r'\b(' + '|'.join(re.escape(t) for t in self.temporal_variations) + r')\b'
        has_temporal = re.search(temporal_pattern, normalized)
        
        # Also check for "in 1944" or "1944" near temporal words
        year_pattern = r'\b(?:in\s+)?1944\b'
        temporal_year_pattern = rf'{temporal_pattern}.*{year_pattern}|{year_pattern}.*{temporal_pattern}'
        
        if has_wwii_context and (has_1944 or re.search(temporal_year_pattern, normalized)):
            # Check if it's about ending/concluding
            if has_temporal or has_1944:
                return PatternMatch(
                    matched=True,
                    pattern_type="wwii_1944",
                    matched_pattern="wwii_ended_1944",
                    confidence=1.0
                )
        
        return PatternMatch(matched=False, pattern_type="wwii_1944")
    
    def match_tesla_evs_shutdown(self, text: str) -> PatternMatch:
        """
        Specialized matcher for Tesla shutting down EVs misinformation.
        """
        normalized = self.normalize_text(text)
        
        # Check for Tesla or Elon Musk context
        tesla_expanded = self.expand_with_synonyms(['tesla'])
        elon_expanded = self.expand_with_synonyms(['elon_musk'])
        has_tesla_context = any(
            re.search(r'\b' + re.escape(t) + r'\b', normalized)
            for t in tesla_expanded
        ) or any(
            re.search(r'\b' + re.escape(e) + r'\b', normalized)
            for e in elon_expanded
        )
        
        # Check for shutdown phrases
        shutdown_expanded = self.expand_with_synonyms(['shutting_down'])
        has_shutdown = any(
            re.search(r'\b' + re.escape(s) + r'\b', normalized)
            for s in shutdown_expanded
        )
        
        # Check for EVs
        evs_expanded = self.expand_with_synonyms(['evs'])
        has_evs = any(
            re.search(r'\b' + re.escape(ev) + r'\b', normalized)
            for ev in evs_expanded
        )
        
        # Check for announcement context (optional but strengthens match)
        announced_expanded = self.expand_with_synonyms(['announced'])
        has_announcement = any(
            re.search(r'\b' + re.escape(a) + r'\b', normalized)
            for a in announced_expanded
        )
        
        if has_tesla_context and has_shutdown and has_evs:
            confidence = 1.0 if has_announcement else 0.9
            return PatternMatch(
                matched=True,
                pattern_type="tesla_evs_shutdown",
                matched_pattern="tesla_shutting_down_evs",
                confidence=confidence
            )
        
        return PatternMatch(matched=False, pattern_type="tesla_evs_shutdown")
    
    def match_pi_equals_3(self, text: str) -> PatternMatch:
        """
        Specialized matcher for pi equals 3.0 misinformation.
        Only matches when pi is claimed to equal exactly 3 or 3.0, not 3.14, 3.14159, etc.
        """
        normalized = self.normalize_text(text)
        
        # Check for pi
        pi_expanded = self.expand_with_synonyms(['pi'])
        has_pi = any(
            re.search(r'\b' + re.escape(p) + r'\b', normalized) or
            re.search(r'π', normalized)
            for p in pi_expanded
        )
        
        if not has_pi:
            return PatternMatch(matched=False, pattern_type="pi_equals_3")
        
        # Check for equals/exactly
        equals_expanded = self.expand_with_synonyms(['equals'])
        has_equals = any(
            re.search(r'\b' + re.escape(e) + r'\b', normalized)
            for e in equals_expanded
        )
        
        if not has_equals:
            return PatternMatch(matched=False, pattern_type="pi_equals_3")
        
        # Check for exactly 3.0 or 3 (but NOT 3.14, 3.14159, etc.)
        # Use word boundaries and negative lookahead to avoid matching 3.14, 3.14159, etc.
        # Match: "3.0", "3", "three" but not "3.1", "3.14", "3.14159"
        three_patterns = [
            r'\b3\.0\b',  # Exactly 3.0
            r'\b3\b(?!\.\d)',  # 3 not followed by .digit (but allow "3" at end or before space)
            r'\bthree\b(?!\s+point)',  # "three" not followed by "point"
        ]
        
        # Also check if there's a number like 3.14 or 3.14159 which would indicate correct value
        correct_value_pattern = r'\b3\.(?:1[4-9]|14\d|141[5-9]|14159)'
        has_correct_value = re.search(correct_value_pattern, normalized)
        
        # If we see a correct value like 3.14 or 3.14159, don't match
        if has_correct_value:
            return PatternMatch(matched=False, pattern_type="pi_equals_3")
        
        # Check for the exact 3 or 3.0 patterns
        has_three = any(re.search(pattern, normalized) for pattern in three_patterns)
        
        # Additional check: if we see "approximately", "around", etc. before the number, be more lenient
        # This prevents false positives on "pi is approximately 3.14159"
        if re.search(r'\b(approximately|approx|around|about|roughly)\s+3', normalized):
            return PatternMatch(matched=False, pattern_type="pi_equals_3")
        
        # Also check if "is" is used with "approximately" - this is usually correct usage
        if re.search(r'pi.*is.*(approximately|approx|around|about|roughly)', normalized):
            return PatternMatch(matched=False, pattern_type="pi_equals_3")
        
        if has_pi and has_equals and has_three:
            return PatternMatch(
                matched=True,
                pattern_type="pi_equals_3",
                matched_pattern="pi_equals_3",
                confidence=1.0
            )
        
        return PatternMatch(matched=False, pattern_type="pi_equals_3")

