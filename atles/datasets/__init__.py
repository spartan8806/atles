"""
ATLES Code Datasets Module

This module provides access to various code datasets including:
- GitHub Code examples
- Programming Books and best practices
- Code Challenges and algorithms
- Framework Documentation
"""

from .github_code import GitHubCodeDataset
from .programming_books import ProgrammingBooksDataset
from .code_challenges import CodeChallengesDataset
from .framework_docs import FrameworkDocsDataset
from .dataset_manager import CodeDatasetManager

__all__ = [
    'GitHubCodeDataset',
    'ProgrammingBooksDataset', 
    'CodeChallengesDataset',
    'FrameworkDocsDataset',
    'CodeDatasetManager'
]
