"""
Logical Reasoning Validator
Validates logical consistency in responses before they're sent to users.

This module helps ATLES catch logical errors, contradictions, and inconsistencies
in its own reasoning, improving the quality and reliability of responses.
"""

import logging
import re
from typing import Dict, List, Optional, Tuple, Set

logger = logging.getLogger(__name__)


class LogicalReasoningValidator:
    """
    Validates logical consistency in reasoning and responses.
    Helps catch common logical errors before they reach the user.
    """
    
    def __init__(self):
        """Initialize logical patterns and validation rules."""
        
        # Quantifier patterns
        self.quantifier_patterns = {
            "at_least_one": [r"at least one", r"at least \d+"],
            "at_most_one": [r"at most one", r"at most \d+"],
            "exactly_one": [r"exactly one", r"exactly \d+"],
            "all": [r"\ball\b", r"\bevery\b", r"\beach\b"],
            "none": [r"\bnone\b", r"\bno\b", r"\bzero\b"],
            "some": [r"\bsome\b", r"\bseveral\b"],
            "most": [r"\bmost\b", r"\bmajority\b"]
        }
        
        # Contradiction indicators
        self.contradiction_pairs = [
            ("all", "none"),
            ("always", "never"),
            ("must", "cannot"),
            ("required", "impossible"),
            ("at least one", "none"),
            ("exactly one", "at least two"),
            ("cannot all", "all must"),
            ("possible", "impossible")
        ]
        
        # Common logical fallacies to detect
        self.fallacy_patterns = {
            "false_dichotomy": [
                r"either.*or.*(?:no other|only|must be)",
                r"only two (?:options|choices|possibilities)"
            ],
            "hasty_generalization": [
                r"all.*(?:must|always|never).*because.*one",
                r"this.*proves.*all"
            ],
            "circular_reasoning": [
                r"because.*(?:it is|they are).*(?:it is|they are)",
                r"true because.*true"
            ]
        }
        
        logger.info("LogicalReasoningValidator initialized")
    
    def validate_logical_constraint(self, constraint: str, conclusion: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that conclusion doesn't contradict the constraint.
        
        Args:
            constraint: The logical constraint or premise
            conclusion: The conclusion or inference drawn
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        constraint_lower = constraint.lower()
        conclusion_lower = conclusion.lower()
        
        # Check for direct contradictions
        for term1, term2 in self.contradiction_pairs:
            if term1 in constraint_lower and term2 in conclusion_lower:
                if self._is_contradictory_context(constraint, conclusion, term1, term2):
                    error = (
                        f"Logical contradiction: Constraint contains '{term1}' but "
                        f"conclusion contains '{term2}'"
                    )
                    logger.warning(error)
                    return False, error
        
        # Validate "at least" reasoning
        if any(pattern in constraint_lower for pattern in ["at least one", "at least"]):
            if self._concludes_none_possible(conclusion_lower):
                error = "'At least one' constraint violated by conclusion suggesting none possible"
                logger.warning(error)
                return False, error
                
            if self._confuses_at_least_with_exactly(constraint, conclusion):
                error = (
                    "Logical error: Confused 'at least one' (minimum threshold) with "
                    "'exactly one' (specific count) or 'at most one' (maximum threshold)"
                )
                logger.warning(error)
                return False, error
        
        # Validate "all" reasoning  
        if any(pattern in constraint_lower for pattern in [r"\ball\b", "every"]):
            if self._allows_none(conclusion_lower):
                error = "'All' constraint violated by conclusion allowing none"
                logger.warning(error)
                return False, error
        
        return True, None
    
    def _is_contradictory_context(self, constraint: str, conclusion: str, 
                                   term1: str, term2: str) -> bool:
        """
        Check if terms are contradictory in the given context.
        
        Args:
            constraint: Constraint text
            conclusion: Conclusion text
            term1: First term
            term2: Second term
            
        Returns:
            True if contradiction exists
        """
        # Look for negations or qualifiers that might resolve apparent contradictions
        negation_patterns = [
            r"not.*" + term1,
            r"if.*not.*" + term1,
            r"unless.*" + term1,
            r"except.*" + term1
        ]
        
        for pattern in negation_patterns:
            if re.search(pattern, constraint.lower()) or re.search(pattern, conclusion.lower()):
                return False  # Negation may resolve contradiction
        
        # Direct contradiction if both terms appear unnegated
        return True
    
    def _concludes_none_possible(self, conclusion: str) -> bool:
        """
        Check if conclusion suggests none are possible.
        
        Args:
            conclusion: Conclusion text
            
        Returns:
            True if conclusion suggests none possible
        """
        none_patterns = [
            r"cannot.*all.*be",
            r"none.*can.*be",
            r"impossible.*for.*all",
            r"all.*cannot",
            r"no.*(?:way|possibility).*for",
            r"would contradict.*if.*all"
        ]
        return any(re.search(pattern, conclusion, re.IGNORECASE) for pattern in none_patterns)
    
    def _allows_none(self, conclusion: str) -> bool:
        """
        Check if conclusion allows for none.
        
        Args:
            conclusion: Conclusion text
            
        Returns:
            True if conclusion allows none
        """
        none_allowance_patterns = [
            r"could.*be.*none",
            r"might.*be.*none",
            r"possibly.*none",
            r"zero.*(?:is|are).*possible"
        ]
        return any(re.search(pattern, conclusion, re.IGNORECASE) for pattern in none_allowance_patterns)
    
    def _confuses_at_least_with_exactly(self, constraint: str, conclusion: str) -> bool:
        """
        Detect confusion between 'at least' (minimum) and 'exactly' (specific) or 'at most' (maximum).
        
        This is a common logical error where someone treats "at least one X" as if it means
        "exactly one X" or "at most one X", when it actually means "one or more X".
        
        Args:
            constraint: Constraint text
            conclusion: Conclusion text
            
        Returns:
            True if confusion detected
        """
        constraint_lower = constraint.lower()
        conclusion_lower = conclusion.lower()
        
        # If constraint says "at least one"
        if "at least one" in constraint_lower or "at least 1" in constraint_lower:
            # Check if conclusion treats it as "exactly one" or "at most one"
            confusion_patterns = [
                r"only one",
                r"just one",
                r"exactly one",
                r"at most one",
                r"cannot.*(?:all|both|multiple|more than one)",
                r"must.*(?:only|just).*one",
                r"(?:all|both).*cannot.*be",  # Treating "at least one red" as "not all can be red"
                r"not.*(?:all|every|each).*can"
            ]
            
            if any(re.search(pattern, conclusion_lower) for pattern in confusion_patterns):
                # Additional check: Make sure it's actually confusion and not valid reasoning
                # Valid: "At least one red means not all can be blue"
                # Invalid: "At least one red means not all can be red"
                if not self._is_valid_negation_inference(constraint_lower, conclusion_lower):
                    return True
        
        return False
    
    def _is_valid_negation_inference(self, constraint: str, conclusion: str) -> bool:
        """
        Check if conclusion is a valid negative inference from constraint.
        
        For example:
        - "At least one red" → "Not all can be blue" (VALID)
        - "At least one red" → "Cannot all be red" (INVALID)
        
        Args:
            constraint: Constraint text
            conclusion: Conclusion text
            
        Returns:
            True if the negation inference is valid
        """
        # Extract what the constraint requires
        constraint_match = re.search(r"at least one (\w+)", constraint)
        if not constraint_match:
            return True  # Can't determine, assume valid
        
        required_item = constraint_match.group(1)
        
        # Check if conclusion is about the same item or different
        if required_item in conclusion:
            # Conclusion is about the same item that's required
            if any(pattern in conclusion for pattern in ["cannot all", "not all", "must not all"]):
                return False  # Invalid: "at least one X" doesn't mean "not all X"
        
        return True
    
    def validate_self_assessment(self, response: str, claimed_score: int) -> Tuple[bool, Optional[str]]:
        """
        Validate that self-assessment score is reasonable given the response content.
        
        Args:
            response: The generated response
            claimed_score: The consistency/confidence score claimed (0-100)
            
        Returns:
            Tuple of (is_reasonable, adjustment_note)
        """
        # Check for obvious error indicators
        error_indicators = [
            r"\berror\b",
            r"\bmistake\b",
            r"\bincorrect\b",
            r"\bwrong\b",
            r"\bcontradiction\b",
            r"\brevised.*thinking\b",
            r"\bactually\b.*\bno\b",
            r"\bon second thought\b",
            r"\bupon reflection\b"
        ]
        
        response_lower = response.lower()
        error_count = sum(1 for pattern in error_indicators 
                         if re.search(pattern, response_lower))
        
        # High error count with high claimed score is suspicious
        if error_count >= 2 and claimed_score >= 80:
            adjustment = (
                f"Response contains {error_count} error indicators but claims "
                f"{claimed_score}% consistency. Consider lower score (60-75%)."
            )
            logger.warning(adjustment)
            return False, adjustment
        
        # Perfect score for complex responses is suspicious
        if claimed_score == 100:
            # Count question marks (indicators of uncertainty)
            uncertainty_count = response.count('?')
            hedging_terms = ["might", "may", "possibly", "perhaps", "could be"]
            hedging_count = sum(1 for term in hedging_terms if term in response_lower)
            
            if uncertainty_count + hedging_count >= 3:
                adjustment = (
                    f"Response shows uncertainty ({uncertainty_count} questions, "
                    f"{hedging_count} hedging terms) but claims 100% consistency. "
                    "Consider 85-95% instead."
                )
                logger.warning(adjustment)
                return False, adjustment
            
            # Long responses with perfect scores are rare
            if len(response) > 1000:
                adjustment = (
                    "Long, complex response with 100% consistency is unlikely. "
                    "Consider more modest assessment (90-95%)."
                )
                logger.info(adjustment)
                return False, adjustment
        
        # Score of 0 suggests complete failure, check if justified
        if claimed_score == 0:
            if error_count == 0 and len(response) > 100:
                adjustment = (
                    "Response appears substantive but claims 0% consistency. "
                    "This seems overly pessimistic unless response is completely wrong."
                )
                logger.info(adjustment)
                return False, adjustment
        
        return True, None
    
    def detect_common_fallacies(self, text: str) -> List[Tuple[str, str]]:
        """
        Detect common logical fallacies in text.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of (fallacy_type, explanation) tuples
        """
        detected_fallacies = []
        text_lower = text.lower()
        
        for fallacy_type, patterns in self.fallacy_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    explanation = self._get_fallacy_explanation(fallacy_type)
                    detected_fallacies.append((fallacy_type, explanation))
                    logger.info(f"Detected potential {fallacy_type}: {pattern}")
        
        return detected_fallacies
    
    def _get_fallacy_explanation(self, fallacy_type: str) -> str:
        """Get explanation for a fallacy type."""
        explanations = {
            "false_dichotomy": (
                "False dichotomy: Presenting only two options when more exist"
            ),
            "hasty_generalization": (
                "Hasty generalization: Drawing broad conclusion from limited evidence"
            ),
            "circular_reasoning": (
                "Circular reasoning: Using conclusion as part of the premise"
            )
        }
        return explanations.get(fallacy_type, f"Logical fallacy: {fallacy_type}")
    
    def validate_multi_step_reasoning(self, steps: List[str]) -> Tuple[bool, List[str]]:
        """
        Validate consistency across multiple reasoning steps.
        
        Args:
            steps: List of reasoning steps
            
        Returns:
            Tuple of (all_consistent, error_messages)
        """
        errors = []
        
        # Check each step against previous steps for contradictions
        for i, current_step in enumerate(steps):
            for j, previous_step in enumerate(steps[:i]):
                # Check for contradictions
                for term1, term2 in self.contradiction_pairs:
                    if term1 in previous_step.lower() and term2 in current_step.lower():
                        if self._is_contradictory_context(previous_step, current_step, term1, term2):
                            error = (
                                f"Contradiction between step {j+1} and step {i+1}: "
                                f"Step {j+1} says '{term1}' but step {i+1} says '{term2}'"
                            )
                            errors.append(error)
                            logger.warning(error)
        
        return len(errors) == 0, errors


def create_logical_reasoning_validator() -> LogicalReasoningValidator:
    """
    Factory function to create logical reasoning validator.
    
    Returns:
        LogicalReasoningValidator instance
    """
    return LogicalReasoningValidator()


# Example usage and tests
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    validator = create_logical_reasoning_validator()
    
    print("\n=== Logical Reasoning Validator Tests ===\n")
    
    # Test 1: "At least one" confusion
    print("Test 1: At least one confusion")
    constraint = "At least one box contains a red ball"
    conclusion = "Therefore, all three boxes cannot contain red balls"
    is_valid, error = validator.validate_logical_constraint(constraint, conclusion)
    print(f"Constraint: {constraint}")
    print(f"Conclusion: {conclusion}")
    print(f"Valid: {is_valid}")
    if error:
        print(f"Error: {error}")
    print()
    
    # Test 2: Self-assessment validation
    print("Test 2: Self-assessment validation")
    response = "I made several errors in my reasoning. Upon reflection, I was incorrect."
    claimed_score = 100
    is_reasonable, note = validator.validate_self_assessment(response, claimed_score)
    print(f"Response: {response}")
    print(f"Claimed score: {claimed_score}")
    print(f"Reasonable: {is_reasonable}")
    if note:
        print(f"Note: {note}")
    print()
    
    # Test 3: Fallacy detection
    print("Test 3: Fallacy detection")
    text = "You must either agree with me completely or you're wrong. There are only two options."
    fallacies = validator.detect_common_fallacies(text)
    print(f"Text: {text}")
    print(f"Detected fallacies: {fallacies}")

