"""
Integration Example: Using Code Datasets with ATLES

This example shows how to integrate the code datasets
with the ATLES brain and other components.
"""

import asyncio
from pathlib import Path
from typing import List, Dict, Any

# Import ATLES components
try:
    from ..brain import ATLESBrain
    from .dataset_manager import CodeDatasetManager
except ImportError:
    # Fallback for standalone testing
    class MockATLESBrain:
        def __init__(self):
            self.name = "Mock ATLES Brain"
    
    ATLESBrain = MockATLESBrain
    from .dataset_manager import CodeDatasetManager


class CodeDatasetIntegration:
    """
    Integration class that connects code datasets with ATLES functionality.
    
    This class provides methods to:
    - Search code examples based on user queries
    - Suggest code patterns and best practices
    - Provide learning resources for programming concepts
    - Integrate with ATLES conversation flow
    """
    
    def __init__(self, brain: ATLESBrain = None):
        """
        Initialize the code dataset integration.
        
        Args:
            brain: ATLES brain instance (optional)
        """
        self.brain = brain
        self.dataset_manager = CodeDatasetManager()
        
        print(f"🔗 Code Dataset Integration initialized")
        print(f"   Available datasets: {len(self.dataset_manager.get_dataset_info())}")
    
    async def search_and_suggest(self, user_query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Search code datasets and provide suggestions based on user query.
        
        Args:
            user_query: User's programming question or request
            context: Additional context (language, difficulty, etc.)
            
        Returns:
            Dictionary with search results and suggestions
        """
        print(f"🔍 Searching for: {user_query}")
        
        # Extract context information
        language = context.get('language') if context else None
        difficulty = context.get('difficulty') if context else None
        tags = context.get('tags') if context else None
        
        # Search across all datasets
        results = self.dataset_manager.search_code(
            query=user_query,
            language=language,
            tags=tags
        )
        
        # Group results by dataset type
        grouped_results = {
            'github_code': [],
            'programming_books': [],
            'code_challenges': [],
            'framework_docs': []
        }
        
        for result in results:
            # Determine dataset type from result structure
            if 'repository' in result:
                grouped_results['github_code'].append(result)
            elif 'book_title' in result:
                grouped_results['programming_books'].append(result)
            elif 'problem_statement' in result:
                grouped_results['code_challenges'].append(result)
            elif 'framework' in result:
                grouped_results['framework_docs'].append(result)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(user_query, grouped_results, context)
        
        return {
            'query': user_query,
            'total_results': len(results),
            'grouped_results': grouped_results,
            'suggestions': suggestions,
            'context': context
        }
    
    def _generate_suggestions(self, query: str, results: Dict[str, List], context: Dict[str, Any] = None) -> List[str]:
        """Generate helpful suggestions based on search results."""
        suggestions = []
        
        # Count results by type
        github_count = len(results['github_code'])
        books_count = len(results['programming_books'])
        challenges_count = len(results['code_challenges'])
        framework_count = len(results['framework_docs'])
        
        # Suggest based on result distribution
        if github_count > 0:
            suggestions.append(f"Found {github_count} real-world code examples from GitHub repositories")
        
        if books_count > 0:
            suggestions.append(f"Found {books_count} best practices and design patterns from programming books")
        
        if challenges_count > 0:
            suggestions.append(f"Found {challenges_count} coding challenges and algorithm problems")
        
        if framework_count > 0:
            suggestions.append(f"Found {framework_count} framework documentation and API examples")
        
        # Suggest specific learning paths
        if 'python' in query.lower():
            suggestions.append("Consider starting with Python-specific examples and gradually moving to advanced concepts")
        
        if 'api' in query.lower():
            suggestions.append("Look at framework documentation examples for practical API implementation patterns")
        
        if 'algorithm' in query.lower() or 'data structure' in query.lower():
            suggestions.append("Start with easy coding challenges and work your way up to more complex problems")
        
        # Add general suggestions
        if not suggestions:
            suggestions.append("Try refining your search with more specific terms or programming language")
        
        return suggestions
    
    async def get_learning_path(self, topic: str, difficulty: str = "beginner") -> Dict[str, Any]:
        """
        Generate a learning path for a specific programming topic.
        
        Args:
            topic: Programming topic to learn
            difficulty: Starting difficulty level
            
        Returns:
            Structured learning path with resources
        """
        print(f"📚 Generating learning path for: {topic} ({difficulty})")
        
        # Search for relevant examples
        results = self.dataset_manager.search_code(topic)
        
        # Organize by difficulty and type
        learning_path = {
            'topic': topic,
            'difficulty': difficulty,
            'steps': [],
            'resources': {
                'beginner': [],
                'intermediate': [],
                'advanced': []
            }
        }
        
        # Categorize results by difficulty
        for result in results:
            result_difficulty = result.get('difficulty', 'intermediate')
            if result_difficulty in learning_path['resources']:
                learning_path['resources'][result_difficulty].append(result)
        
        # Generate step-by-step learning path
        if learning_path['resources']['beginner']:
            learning_path['steps'].append({
                'step': 1,
                'title': 'Start with Basic Examples',
                'description': 'Begin with simple, well-documented examples',
                'examples': learning_path['resources']['beginner'][:3]
            })
        
        if learning_path['resources']['intermediate']:
            learning_path['steps'].append({
                'step': 2,
                'title': 'Practice with Real Code',
                'description': 'Study production code from GitHub repositories',
                'examples': learning_path['resources']['intermediate'][:3]
            })
        
        if learning_path['resources']['advanced']:
            learning_path['steps'].append({
                'step': 3,
                'title': 'Master Advanced Concepts',
                'description': 'Tackle complex problems and advanced patterns',
                'examples': learning_path['resources']['advanced'][:3]
            })
        
        return learning_path
    
    async def suggest_next_steps(self, current_topic: str, user_level: str) -> List[str]:
        """
        Suggest next learning steps based on current topic and user level.
        
        Args:
            current_topic: What the user is currently learning
            user_level: User's current skill level
            
        Returns:
            List of suggested next topics
        """
        print(f"🎯 Suggesting next steps for: {current_topic} (Level: {user_level})")
        
        # This would typically use more sophisticated logic
        # For now, provide general suggestions
        suggestions = []
        
        if 'python' in current_topic.lower():
            if user_level == 'beginner':
                suggestions.extend(['Object-Oriented Programming', 'Error Handling', 'File I/O'])
            elif user_level == 'intermediate':
                suggestions.extend(['Decorators', 'Generators', 'Context Managers'])
            elif user_level == 'advanced':
                suggestions.extend(['Metaclasses', 'Async Programming', 'Performance Optimization'])
        
        elif 'api' in current_topic.lower():
            suggestions.extend(['Authentication', 'Rate Limiting', 'Error Handling', 'Testing'])
        
        elif 'algorithm' in current_topic.lower():
            suggestions.extend(['Data Structures', 'Sorting Algorithms', 'Dynamic Programming'])
        
        return suggestions[:5]  # Limit to 5 suggestions


# Example usage function
async def main():
    """Example of how to use the code dataset integration."""
    print("🚀 ATLES Code Dataset Integration Example")
    print("=" * 50)
    
    # Initialize integration
    integration = CodeDatasetIntegration()
    
    # Example 1: Search for Python examples
    print("\n📝 Example 1: Searching for Python examples")
    results = await integration.search_and_suggest("python flask api")
    print(f"Found {results['total_results']} results")
    for suggestion in results['suggestions']:
        print(f"  💡 {suggestion}")
    
    # Example 2: Generate learning path
    print("\n📚 Example 2: Generating learning path for algorithms")
    learning_path = await integration.get_learning_path("algorithm", "beginner")
    print(f"Learning path has {len(learning_path['steps'])} steps")
    for step in learning_path['steps']:
        print(f"  Step {step['step']}: {step['title']}")
    
    # Example 3: Suggest next steps
    print("\n🎯 Example 3: Suggesting next steps")
    next_steps = await integration.suggest_next_steps("python basics", "beginner")
    print("Suggested next topics:")
    for step in next_steps:
        print(f"  • {step}")
    
    print("\n✅ Integration example completed successfully!")


if __name__ == "__main__":
    # Run the example
    asyncio.run(main())
