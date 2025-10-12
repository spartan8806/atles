"""
Programming Books Dataset

Handles programming best practices, design patterns, and examples
from authoritative programming books and resources.
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
class ProgrammingBookExample:
    """Represents a programming example from a book."""
    id: str
    book_title: str
    author: str
    chapter: str
    section: str
    language: str
    code: str
    description: str
    concepts: List[str]
    difficulty: str  # beginner, intermediate, advanced
    tags: List[str]
    relevance_score: float = 0.0


class ProgrammingBooksDataset:
    """
    Dataset handler for programming books and best practices.
    
    Provides access to design patterns, best practices, and examples
    from authoritative programming books and resources.
    """
    
    def __init__(self, data_dir: Path):
        """
        Initialize programming books dataset.
        
        Args:
            data_dir: Directory to store programming books data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize with sample data if empty
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample programming book examples."""
        sample_file = self.data_dir / 'sample_data.json'
        
        if not sample_file.exists():
            sample_data = self._create_sample_data()
            with open(sample_file, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info("Initialized programming books dataset with sample data")
    
    def _create_sample_data(self) -> List[Dict[str, Any]]:
        """Create sample programming book examples."""
        return [
            {
                "id": "design_patterns_singleton",
                "book_title": "Design Patterns: Elements of Reusable Object-Oriented Software",
                "author": "Gang of Four",
                "chapter": "Creational Patterns",
                "section": "Singleton Pattern",
                "language": "python",
                "code": """class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialized = True
            # Initialize your singleton here
            self.data = []
    
    def add_data(self, item):
        self.data.append(item)
    
    def get_data(self):
        return self.data.copy()

# Usage
singleton1 = Singleton()
singleton1.add_data("First item")

singleton2 = Singleton()
singleton2.add_data("Second item")

print(singleton1 is singleton2)  # True
print(singleton1.get_data())     # ['First item', 'Second item']""",
                "description": "Singleton design pattern implementation in Python",
                "concepts": ["design-patterns", "singleton", "creational-patterns", "object-oriented"],
                "difficulty": "intermediate",
                "tags": ["python", "design-patterns", "singleton", "oop", "best-practices"],
                "relevance_score": 0.95
            },
            {
                "id": "clean_code_functions",
                "book_title": "Clean Code: A Handbook of Agile Software Craftsmanship",
                "author": "Robert C. Martin",
                "chapter": "Functions",
                "section": "Function Naming",
                "language": "python",
                "code": """# Bad: Unclear function name and purpose
def process(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result

# Good: Clear, descriptive function name
def filter_and_double_positive_numbers(numbers):
    # Filter positive numbers and double them
    # Args: numbers - List of numbers to process
    # Returns: List of doubled positive numbers
    positive_numbers = [num for num in numbers if num > 0]
    doubled_numbers = [num * 2 for num in positive_numbers]
    return doubled_numbers

# Usage example
numbers = [-1, 2, -3, 4, 5]
result = filter_and_double_positive_numbers(numbers)
print(result)  # [4, 8, 10]""",
                "description": "Clean code principles for function naming and structure",
                "concepts": ["clean-code", "function-design", "naming-conventions", "readability"],
                "difficulty": "beginner",
                "tags": ["python", "clean-code", "functions", "naming", "best-practices"],
                "relevance_score": 0.92
            },
            {
                "id": "effective_python_comprehensions",
                "book_title": "Effective Python: 90 Specific Ways to Write Better Python",
                "author": "Brett Slatkin",
                "chapter": "Comprehensions and Generators",
                "section": "List Comprehensions",
                "language": "python",
                "code": """# Bad: Traditional for loop approach
def get_squares_of_evens(numbers):
    squares = []
    for num in numbers:
        if num % 2 == 0:
            squares.append(num ** 2)
    return squares

# Good: List comprehension approach
def get_squares_of_evens(numbers):
    return [num ** 2 for num in numbers if num % 2 == 0]

# Even better: Generator expression for memory efficiency
def get_squares_of_evens_generator(numbers):
    return (num ** 2 for num in numbers if num % 2 == 0)

# Usage examples
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# List comprehension
squares_list = get_squares_of_evens(numbers)
print(list(squares_list))  # [4, 16, 36, 64, 100]

# Generator expression
squares_gen = get_squares_of_evens_generator(numbers)
for square in squares_gen:
    print(square, end=' ')  # 4 16 36 64 100""",
                "description": "Effective use of list comprehensions and generator expressions",
                "concepts": ["list-comprehensions", "generators", "pythonic-code", "memory-efficiency"],
                "difficulty": "intermediate",
                "tags": ["python", "comprehensions", "generators", "efficiency", "best-practices"],
                "relevance_score": 0.88
            },
            {
                "id": "refactoring_extract_method",
                "book_title": "Refactoring: Improving the Design of Existing Code",
                "author": "Martin Fowler",
                "chapter": "Composing Methods",
                "section": "Extract Method",
                "language": "python",
                "code": """# Before: Long method with multiple responsibilities
def print_owing(amount):
    print("*************************")
    print("**** Customer Owes ******")
    print("*************************")
    
    # Calculate outstanding amount
    outstanding = amount * 1.2
    
    # Print details
    print(f"name: {self.name}")
    print(f"amount: {amount}")
    print(f"outstanding: {outstanding}")

# After: Extracted methods with single responsibilities
def print_owing(self, amount):
    self._print_banner()
    outstanding = self._calculate_outstanding(amount)
    self._print_details(amount, outstanding)

def _print_banner(self):
    print("*************************")
    print("**** Customer Owes ******")
    print("*************************")

def _calculate_outstanding(self, amount):
    return amount * 1.2

def _print_details(self, amount, outstanding):
    print(f"name: {self.name}")
    print(f"amount: {amount}")
    print(f"outstanding: {outstanding}")

# Benefits:
# 1. Each method has a single responsibility
# 2. Methods are easier to test individually
# 3. Code is more readable and maintainable
# 4. Methods can be reused elsewhere""",
                "description": "Refactoring technique: Extract Method for better code organization",
                "concepts": ["refactoring", "extract-method", "single-responsibility", "code-organization"],
                "difficulty": "intermediate",
                "tags": ["python", "refactoring", "methods", "clean-code", "best-practices"],
                "relevance_score": 0.90
            }
        ]
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about the programming books dataset."""
        return {
            "name": "Programming Books and Best Practices",
            "description": "Design patterns, best practices, and examples from authoritative programming books",
            "source": "Programming Books",
            "language": "multi",
            "tags": ["programming-books", "best-practices", "design-patterns", "clean-code"],
            "size": len(self._load_data()),
            "last_updated": datetime.now(),
            "version": "1.0"
        }
    
    def _load_data(self) -> List[Dict[str, Any]]:
        """Load programming books data from storage."""
        try:
            sample_file = self.data_dir / 'sample_data.json'
            if sample_file.exists():
                with open(sample_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading programming books data: {e}")
        
        return []
    
    def search(self, query: str, language: Optional[str] = None, 
               tags: Optional[List[str]] = None, difficulty: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search programming book examples.
        
        Args:
            query: Search query
            language: Programming language filter
            tags: Tag filters
            difficulty: Difficulty level filter (beginner, intermediate, advanced)
            
        Returns:
            List of matching examples
        """
        data = self._load_data()
        results = []
        
        query_lower = query.lower()
        
        for example in data:
            # Check if example matches query
            if (query_lower in example['code'].lower() or
                query_lower in example['description'].lower() or
                query_lower in example['book_title'].lower() or
                query_lower in example['concepts'] or
                query_lower in example['tags']):
                
                # Apply language filter
                if language and example['language'].lower() != language.lower():
                    continue
                
                # Apply tag filter
                if tags and not any(tag.lower() in [t.lower() for t in example['tags']] for tag in tags):
                    continue
                
                # Apply difficulty filter
                if difficulty and example['difficulty'].lower() != difficulty.lower():
                    continue
                
                # Calculate relevance score based on query match
                relevance = self._calculate_relevance(query_lower, example)
                example['relevance_score'] = relevance
                
                results.append(example)
        
        # Sort by relevance score
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return results
    
    def _calculate_relevance(self, query: str, example: Dict[str, Any]) -> float:
        """Calculate relevance score for a programming book example."""
        score = 0.0
        
        # Code content relevance
        if query in example['code'].lower():
            score += 0.3
        
        # Description relevance
        if query in example['description'].lower():
            score += 0.25
        
        # Book title relevance
        if query in example['book_title'].lower():
            score += 0.2
        
        # Concepts relevance
        for concept in example['concepts']:
            if query in concept.lower():
                score += 0.15
        
        # Tag relevance
        for tag in example['tags']:
            if query in tag.lower():
                score += 0.1
        
        return min(score, 1.0)
    
    def get_example(self, example_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific programming book example by ID.
        
        Args:
            example_id: Unique identifier for the example
            
        Returns:
            Example data or None if not found
        """
        data = self._load_data()
        
        for example in data:
            if example['id'] == example_id:
                return example
        
        return None
    
    def add_example(self, example: ProgrammingBookExample) -> bool:
        """
        Add a new programming book example.
        
        Args:
            example: ProgrammingBookExample instance
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = self._load_data()
            
            # Check if ID already exists
            if any(ex['id'] == example.id for ex in data):
                logger.warning(f"Example with ID {example.id} already exists")
                return False
            
            # Add new example
            data.append(asdict(example))
            
            # Save updated data
            sample_file = self.data_dir / 'sample_data.json'
            with open(sample_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"Added programming book example: {example.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding programming book example: {e}")
            return False
    
    def get_books(self) -> List[str]:
        """Get list of available programming books."""
        data = self._load_data()
        books = set()
        
        for example in data:
            books.add(example['book_title'])
        
        return sorted(list(books))
    
    def get_concepts(self) -> List[str]:
        """Get list of available programming concepts."""
        data = self._load_data()
        concepts = set()
        
        for example in data:
            concepts.update(example['concepts'])
        
        return sorted(list(concepts))
    
    def get_difficulty_levels(self) -> List[str]:
        """Get list of available difficulty levels."""
        return ["beginner", "intermediate", "advanced"]
    
    def get_examples_by_concept(self, concept: str) -> List[Dict[str, Any]]:
        """
        Get examples by specific programming concept.
        
        Args:
            concept: Programming concept to search for
            
        Returns:
            List of examples for the concept
        """
        data = self._load_data()
        results = []
        
        concept_lower = concept.lower()
        
        for example in data:
            if any(concept_lower in c.lower() for c in example['concepts']):
                results.append(example)
        
        return results
