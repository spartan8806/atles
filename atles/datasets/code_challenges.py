"""
Code Challenges Dataset

Handles algorithm problems, coding challenges, and their solutions
from various programming competition platforms and educational resources.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class CodeChallenge:
    """Represents a coding challenge or algorithm problem."""
    id: str
    title: str
    description: str
    difficulty: str  # easy, medium, hard
    category: str  # algorithms, data-structures, dynamic-programming, etc.
    language: str
    problem_statement: str
    constraints: List[str]
    examples: List[Dict[str, Any]]
    solution: str
    explanation: str
    time_complexity: str
    space_complexity: str
    tags: List[str]
    source: str  # leetcode, hackerrank, etc.
    relevance_score: float = 0.0


class CodeChallengesDataset:
    """
    Dataset handler for coding challenges and algorithm problems.
    
    Provides access to problems from platforms like LeetCode, HackerRank,
    and other programming competition sites with detailed solutions.
    """
    
    def __init__(self, data_dir: Path):
        """
        Initialize code challenges dataset.
        
        Args:
            data_dir: Directory to store code challenges data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize with sample data if empty
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample code challenges."""
        sample_file = self.data_dir / 'sample_data.json'
        
        if not sample_file.exists():
            sample_data = self._create_sample_data()
            with open(sample_file, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info("Initialized code challenges dataset with sample data")
    
    def _create_sample_data(self) -> List[Dict[str, Any]]:
        """Create sample code challenges."""
        return [
            {
                "id": "two_sum",
                "title": "Two Sum",
                "description": "Find two numbers in an array that add up to a target value",
                "difficulty": "easy",
                "category": "arrays",
                "language": "python",
                "problem_statement": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice.",
                "constraints": [
                    "2 <= nums.length <= 10^4",
                    "-10^9 <= nums[i] <= 10^9",
                    "-10^9 <= target <= 10^9",
                    "Only one valid answer exists"
                ],
                "examples": [
                    {
                        "input": {"nums": [2, 7, 11, 15], "target": 9},
                        "output": [0, 1],
                        "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."
                    },
                    {
                        "input": {"nums": [3, 2, 4], "target": 6},
                        "output": [1, 2],
                        "explanation": "Because nums[1] + nums[2] == 6, we return [1, 2]."
                    }
                ],
                "solution": """def two_sum(nums, target):
    # Use a hash map to store complements
    seen = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        
        # If complement exists, we found our pair
        if complement in seen:
            return [seen[complement], i]
        
        # Store current number and its index
        seen[num] = i
    
    return []  # No solution found

# Test cases
nums1 = [2, 7, 11, 15]
target1 = 9
print(two_sum(nums1, target1))  # [0, 1]

nums2 = [3, 2, 4]
target2 = 6
print(two_sum(nums2, target2))  # [1, 2]""",
                "explanation": "The optimal solution uses a hash map to achieve O(n) time complexity. For each number, we check if its complement (target - current_number) exists in our hash map. If it does, we've found our pair. If not, we store the current number and its index for future lookups.",
                "time_complexity": "O(n)",
                "space_complexity": "O(n)",
                "tags": ["arrays", "hash-table", "two-pointers", "easy"],
                "source": "leetcode",
                "relevance_score": 0.95
            },
            {
                "id": "valid_parentheses",
                "title": "Valid Parentheses",
                "description": "Check if a string of parentheses is valid",
                "difficulty": "easy",
                "category": "stacks",
                "language": "python",
                "problem_statement": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid. An input string is valid if: 1) Open brackets must be closed by the same type of brackets. 2) Open brackets must be closed in the correct order.",
                "constraints": [
                    "1 <= s.length <= 10^4",
                    "s consists of parentheses only '()[]{}'"
                ],
                "examples": [
                    {
                        "input": {"s": "()"},
                        "output": True,
                        "explanation": "Simple valid parentheses."
                    },
                    {
                        "input": {"s": "([)]"},
                        "output": False,
                        "explanation": "Brackets are not closed in the correct order."
                    }
                ],
                "solution": """def is_valid_parentheses(s):
    # Use stack to keep track of opening brackets
    stack = []
    
    # Map closing brackets to their corresponding opening brackets
    bracket_map = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        # If it's an opening bracket, push to stack
        if char in '({[':
            stack.append(char)
        # If it's a closing bracket, check if it matches the top of stack
        elif char in ')}]':
            if not stack or stack.pop() != bracket_map[char]:
                return False
    
    # Stack should be empty if all brackets are properly closed
    return len(stack) == 0

# Test cases
test_cases = ["()", "()[]{}", "(]", "([)]", "{[]}"]
for test in test_cases:
    result = is_valid_parentheses(test)
    print(f"'{test}' -> {result}")""",
                "explanation": "This problem is a classic stack application. We use a stack to keep track of opening brackets. When we encounter a closing bracket, we check if it matches the most recent opening bracket (top of stack). If they don't match or if the stack is empty, the string is invalid.",
                "time_complexity": "O(n)",
                "space_complexity": "O(n)",
                "tags": ["stack", "string", "easy"],
                "source": "leetcode",
                "relevance_score": 0.90
            },
            {
                "id": "binary_tree_inorder_traversal",
                "title": "Binary Tree Inorder Traversal",
                "description": "Traverse a binary tree in inorder fashion",
                "difficulty": "medium",
                "category": "trees",
                "language": "python",
                "problem_statement": "Given the root of a binary tree, return the inorder traversal of its nodes' values. Inorder traversal visits nodes in the order: left subtree, root, right subtree.",
                "constraints": [
                    "The number of nodes in the tree is in the range [0, 100]",
                    "-100 <= Node.val <= 100"
                ],
                "examples": [
                    {
                        "input": {"root": "[1,null,2,3]"},
                        "output": [1, 3, 2],
                        "explanation": "Inorder traversal: left subtree (empty), root (1), right subtree (3, 2)."
                    }
                ],
                "solution": """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorder_traversal_recursive(root):
    # Recursive solution
    result = []
    
    def inorder(node):
        if node:
            inorder(node.left)      # Visit left subtree
            result.append(node.val) # Visit root
            inorder(node.right)     # Visit right subtree
    
    inorder(root)
    return result

def inorder_traversal_iterative(root):
    # Iterative solution using stack
    result = []
    stack = []
    current = root
    
    while current or stack:
        # Go to the leftmost node
        while current:
            stack.append(current)
            current = current.left
        
        # Process current node
        current = stack.pop()
        result.append(current.val)
        
        # Move to right subtree
        current = current.right
    
    return result

# Create sample tree: [1,null,2,3]
root = TreeNode(1)
root.right = TreeNode(2)
root.right.left = TreeNode(3)

print("Recursive:", inorder_traversal_recursive(root))
print("Iterative:", inorder_traversal_iterative(root))""",
                "explanation": "Inorder traversal visits nodes in the order: left subtree, root, right subtree. The recursive solution is straightforward and mirrors the definition. The iterative solution uses a stack to simulate the recursive call stack, going as far left as possible before processing nodes.",
                "time_complexity": "O(n)",
                "space_complexity": "O(n)",
                "tags": ["tree", "depth-first-search", "stack", "medium"],
                "source": "leetcode",
                "relevance_score": 0.85
            }
        ]
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about the code challenges dataset."""
        return {
            "name": "Code Challenges and Algorithms",
            "description": "Algorithm problems and solutions from programming competition platforms",
            "source": "Multiple Platforms",
            "language": "multi",
            "tags": ["algorithms", "data-structures", "coding-challenges", "problem-solving"],
            "size": len(self._load_data()),
            "last_updated": datetime.now(),
            "version": "1.0"
        }
    
    def _load_data(self) -> List[Dict[str, Any]]:
        """Load code challenges data from storage."""
        try:
            sample_file = self.data_dir / 'sample_data.json'
            if sample_file.exists():
                with open(sample_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading code challenges data: {e}")
        
        return []
    
    def search(self, query: str, language: Optional[str] = None, 
               tags: Optional[List[str]] = None, difficulty: Optional[str] = None,
               category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search code challenges.
        
        Args:
            query: Search query
            language: Programming language filter
            tags: Tag filters
            difficulty: Difficulty level filter (easy, medium, hard)
            category: Problem category filter
            
        Returns:
            List of matching challenges
        """
        data = self._load_data()
        results = []
        
        query_lower = query.lower()
        
        for challenge in data:
            # Check if challenge matches query
            if (query_lower in challenge['title'].lower() or
                query_lower in challenge['description'].lower() or
                query_lower in challenge['problem_statement'].lower() or
                query_lower in challenge['category'].lower() or
                query_lower in challenge['tags']):
                
                # Apply language filter
                if language and challenge['language'].lower() != language.lower():
                    continue
                
                # Apply tag filter
                if tags and not any(tag.lower() in [t.lower() for t in challenge['tags']] for tag in tags):
                    continue
                
                # Apply difficulty filter
                if difficulty and challenge['difficulty'].lower() != difficulty.lower():
                    continue
                
                # Apply category filter
                if category and challenge['category'].lower() != category.lower():
                    continue
                
                # Calculate relevance score based on query match
                relevance = self._calculate_relevance(query_lower, challenge)
                challenge['relevance_score'] = relevance
                
                results.append(challenge)
        
        # Sort by relevance score
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return results
    
    def _calculate_relevance(self, query: str, challenge: Dict[str, Any]) -> float:
        """Calculate relevance score for a code challenge."""
        score = 0.0
        
        # Title relevance
        if query in challenge['title'].lower():
            score += 0.3
        
        # Description relevance
        if query in challenge['description'].lower():
            score += 0.25
        
        # Problem statement relevance
        if query in challenge['problem_statement'].lower():
            score += 0.2
        
        # Category relevance
        if query in challenge['category'].lower():
            score += 0.15
        
        # Tag relevance
        for tag in challenge['tags']:
            if query in tag.lower():
                score += 0.1
        
        return min(score, 1.0)
    
    def get_challenge(self, challenge_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific code challenge by ID.
        
        Args:
            challenge_id: Unique identifier for the challenge
            
        Returns:
            Challenge data or None if not found
        """
        data = self._load_data()
        
        for challenge in data:
            if challenge['id'] == challenge_id:
                return challenge
        
        return None
    
    def add_challenge(self, challenge: CodeChallenge) -> bool:
        """
        Add a new code challenge.
        
        Args:
            challenge: CodeChallenge instance
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = self._load_data()
            
            # Check if ID already exists
            if any(ch['id'] == challenge.id for ch in data):
                logger.warning(f"Challenge with ID {challenge.id} already exists")
                return False
            
            # Add new challenge
            data.append(asdict(challenge))
            
            # Save updated data
            sample_file = self.data_dir / 'sample_data.json'
            with open(sample_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"Added code challenge: {challenge.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding code challenge: {e}")
            return False
    
    def get_categories(self) -> List[str]:
        """Get list of available problem categories."""
        data = self._load_data()
        categories = set()
        
        for challenge in data:
            categories.add(challenge['category'])
        
        return sorted(list(categories))
    
    def get_difficulty_levels(self) -> List[str]:
        """Get list of available difficulty levels."""
        return ["easy", "medium", "hard"]
    
    def get_challenges_by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        """
        Get challenges by difficulty level.
        
        Args:
            difficulty: Difficulty level (easy, medium, hard)
            
        Returns:
            List of challenges with the specified difficulty
        """
        data = self._load_data()
        results = []
        
        difficulty_lower = difficulty.lower()
        
        for challenge in data:
            if challenge['difficulty'].lower() == difficulty_lower:
                results.append(challenge)
        
        return results
    
    def get_challenges_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get challenges by category.
        
        Args:
            category: Problem category
            
        Returns:
            List of challenges in the specified category
        """
        data = self._load_data()
        results = []
        
        category_lower = category.lower()
        
        for challenge in data:
            if challenge['category'].lower() == category_lower:
                results.append(challenge)
        
        return results
