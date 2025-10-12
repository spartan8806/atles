"""
Code Dataset Manager

Central coordinator for all code datasets, providing unified access
to GitHub code, programming books, challenges, and framework docs.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    from .github_code import GitHubCodeDataset
    from .programming_books import ProgrammingBooksDataset
    from .code_challenges import CodeChallengesDataset
    from .framework_docs import FrameworkDocsDataset
except ImportError:
    # Create placeholder classes if imports fail
    class PlaceholderDataset:
        def __init__(self, data_dir):
            self.data_dir = data_dir
        
        def get_metadata(self):
            return {
                "name": "Placeholder Dataset",
                "description": "Dataset not yet implemented",
                "source": "Placeholder",
                "language": "none",
                "tags": ["placeholder"],
                "size": 0,
                "last_updated": datetime.now(),
                "version": "0.0"
            }
        
        def search(self, *args, **kwargs):
            return []
        
        def get_example(self, *args, **kwargs):
            return None
    
    GitHubCodeDataset = PlaceholderDataset
    ProgrammingBooksDataset = PlaceholderDataset
    CodeChallengesDataset = PlaceholderDataset
    FrameworkDocsDataset = PlaceholderDataset

logger = logging.getLogger(__name__)


@dataclass
class DatasetMetadata:
    """Metadata for a code dataset."""
    name: str
    description: str
    source: str
    language: str
    tags: List[str]
    size: int
    last_updated: datetime
    version: str


class CodeDatasetManager:
    """
    Central manager for all code datasets.
    
    Provides unified access to:
    - GitHub code examples
    - Programming books and best practices
    - Code challenges and algorithms
    - Framework documentation
    """
    
    def __init__(self, datasets_dir: Optional[Path] = None):
        """
        Initialize the dataset manager.
        
        Args:
            datasets_dir: Directory to store datasets (defaults to ATLES_HOME/datasets)
        """
        if datasets_dir is None:
            atles_home = Path(os.environ.get('ATLES_HOME', 'D:\\.atles'))
            self.datasets_dir = atles_home / 'datasets'
        else:
            self.datasets_dir = Path(datasets_dir)
        
        # Create datasets directory
        self.datasets_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize individual dataset handlers
        self.github_code = GitHubCodeDataset(self.datasets_dir / 'github')
        self.programming_books = ProgrammingBooksDataset(self.datasets_dir / 'books')
        self.code_challenges = CodeChallengesDataset(self.datasets_dir / 'challenges')
        self.framework_docs = FrameworkDocsDataset(self.datasets_dir / 'frameworks')
        
        # Track available datasets
        self.available_datasets: Dict[str, DatasetMetadata] = {}
        self._discover_datasets()
        
        logger.info(f"Code Dataset Manager initialized at {self.datasets_dir}")
    
    def _discover_datasets(self):
        """Discover and catalog available datasets."""
        try:
            # Check each dataset type
            self.available_datasets['github_code'] = self.github_code.get_metadata()
            self.available_datasets['programming_books'] = self.programming_books.get_metadata()
            self.available_datasets['code_challenges'] = self.code_challenges.get_metadata()
            self.available_datasets['framework_docs'] = self.framework_docs.get_metadata()
            
            logger.info(f"Discovered {len(self.available_datasets)} dataset types")
        except Exception as e:
            logger.warning(f"Error discovering datasets: {e}")
    
    def get_dataset_info(self) -> Dict[str, DatasetMetadata]:
        """Get information about all available datasets."""
        return self.available_datasets.copy()
    
    def search_code(self, query: str, dataset_type: Optional[str] = None, 
                   language: Optional[str] = None, tags: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Search across all code datasets.
        
        Args:
            query: Search query
            dataset_type: Specific dataset to search (optional)
            language: Programming language filter (optional)
            tags: Tag filters (optional)
            
        Returns:
            List of matching code examples
        """
        results = []
        
        if dataset_type:
            # Search specific dataset
            if dataset_type == 'github_code':
                try:
                    results.extend(self.github_code.search(query, language, tags))
                except Exception as e:
                    logger.warning(f"Error searching GitHub code dataset: {e}")
            elif dataset_type == 'programming_books':
                try:
                    results.extend(self.programming_books.search(query, language, tags))
                except Exception as e:
                    logger.warning(f"Error searching programming books dataset: {e}")
            elif dataset_type == 'code_challenges':
                try:
                    results.extend(self.code_challenges.search(query, language, tags))
                except Exception as e:
                    logger.warning(f"Error searching code challenges dataset: {e}")
            elif dataset_type == 'framework_docs':
                try:
                    results.extend(self.framework_docs.search(query, language, tags))
                except Exception as e:
                    logger.warning(f"Error searching framework docs dataset: {e}")
        else:
            # Search all datasets
            try:
                results.extend(self.github_code.search(query, language, tags))
            except Exception as e:
                logger.warning(f"Error searching GitHub code dataset: {e}")
            
            try:
                results.extend(self.programming_books.search(query, language, tags))
            except Exception as e:
                logger.warning(f"Error searching programming books dataset: {e}")
            
            try:
                results.extend(self.code_challenges.search(query, language, tags))
            except Exception as e:
                logger.warning(f"Error searching code challenges dataset: {e}")
            
            try:
                results.extend(self.framework_docs.search(query, language, tags))
            except Exception as e:
                logger.warning(f"Error searching framework docs dataset: {e}")
        
        # Sort by relevance score if available
        results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return results
    
    def get_code_example(self, example_id: str, dataset_type: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific code example by ID.
        
        Args:
            example_id: Unique identifier for the example
            dataset_type: Type of dataset to search
            
        Returns:
            Code example data or None if not found
        """
        try:
            if dataset_type == 'github_code':
                return self.github_code.get_example(example_id)
            elif dataset_type == 'programming_books':
                return self.programming_books.get_example(example_id)
            elif dataset_type == 'code_challenges':
                return self.code_challenges.get_example(example_id)
            elif dataset_type == 'framework_docs':
                return self.framework_docs.get_example(example_id)
            else:
                logger.warning(f"Unknown dataset type: {dataset_type}")
        except Exception as e:
            logger.error(f"Error retrieving example {example_id} from {dataset_type}: {e}")
        
        return None
    
    def add_custom_dataset(self, name: str, description: str, source: str, 
                          language: str, tags: List[str], data: List[Dict[str, Any]]) -> bool:
        """
        Add a custom dataset.
        
        Args:
            name: Dataset name
            description: Dataset description
            source: Data source
            language: Programming language
            tags: Associated tags
            data: Dataset content
            
        Returns:
            True if successful, False otherwise
        """
        try:
            custom_dir = self.datasets_dir / 'custom' / name
            custom_dir.mkdir(parents=True, exist_ok=True)
            
            # Save dataset
            dataset_file = custom_dir / 'data.json'
            with open(dataset_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
            # Save metadata
            metadata = DatasetMetadata(
                name=name,
                description=description,
                source=source,
                language=language,
                tags=tags,
                size=len(data),
                last_updated=datetime.now(),
                version="1.0"
            )
            
            metadata_file = custom_dir / 'metadata.json'
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(metadata), f, indent=2, ensure_ascii=False, default=str)
            
            # Update available datasets
            self.available_datasets[f'custom_{name}'] = metadata
            
            logger.info(f"Custom dataset '{name}' added successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error adding custom dataset '{name}': {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about all datasets."""
        stats = {
            'total_datasets': len(self.available_datasets),
            'total_examples': 0,
            'languages': set(),
            'tags': set()
        }
        
        for dataset_type, metadata in self.available_datasets.items():
            # Handle both DatasetMetadata objects and dictionaries
            if hasattr(metadata, 'size'):
                stats['total_examples'] += metadata.size
            elif isinstance(metadata, dict) and 'size' in metadata:
                stats['total_examples'] += metadata['size']
            
            # Handle languages
            if hasattr(metadata, 'language'):
                stats['languages'].add(metadata.language)
            elif isinstance(metadata, dict) and 'language' in metadata:
                stats['languages'].add(metadata['language'])
            
            # Handle tags
            if hasattr(metadata, 'tags'):
                stats['tags'].update(metadata.tags)
            elif isinstance(metadata, dict) and 'tags' in metadata:
                stats['tags'].update(metadata['tags'])
        
        # Convert sets to lists for JSON serialization
        stats['languages'] = list(stats['languages'])
        stats['tags'] = list(stats['tags'])
        
        return stats
