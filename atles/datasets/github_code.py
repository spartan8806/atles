"""
GitHub Code Dataset

Handles real programming examples from GitHub repositories,
providing access to production-quality code patterns.
"""

import os
import json
import logging
import requests
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import re

logger = logging.getLogger(__name__)


@dataclass
class GitHubCodeExample:
    """Represents a GitHub code example."""
    id: str
    repository: str
    file_path: str
    language: str
    code: str
    description: str
    tags: List[str]
    stars: int
    forks: int
    last_updated: datetime
    url: str
    relevance_score: float = 0.0


class GitHubCodeDataset:
    """
    Dataset handler for GitHub code examples.
    
    Provides access to real programming examples from popular repositories,
    focusing on production-quality code patterns and best practices.
    """
    
    def __init__(self, data_dir: Path):
        """
        Initialize GitHub code dataset.
        
        Args:
            data_dir: Directory to store GitHub code data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Sample curated repositories for different languages
        self.curated_repos = {
            'python': [
                'django/django',
                'pallets/flask',
                'psf/requests',
                'pandas-dev/pandas',
                'numpy/numpy',
                'scikit-learn/scikit-learn',
                'fastapi/fastapi',
                'pydantic/pydantic'
            ],
            'javascript': [
                'facebook/react',
                'vuejs/vue',
                'nodejs/node',
                'expressjs/express',
                'lodash/lodash',
                'moment/moment',
                'axios/axios',
                'webpack/webpack'
            ],
            'typescript': [
                'microsoft/TypeScript',
                'angular/angular',
                'nestjs/nest',
                'prisma/prisma',
                'typeorm/typeorm',
                'mikro-orm/mikro-orm'
            ],
            'java': [
                'spring-projects/spring-boot',
                'spring-projects/spring-framework',
                'google/guava',
                'apache/commons-lang',
                'hibernate/hibernate-orm'
            ],
            'cpp': [
                'microsoft/vcpkg',
                'nlohmann/json',
                'catchorg/Catch2',
                'fmtlib/fmt',
                'google/googletest'
            ],
            'rust': [
                'rust-lang/rust',
                'tokio-rs/tokio',
                'serde-rs/serde',
                'clap-rs/clap',
                'actix/actix-web'
            ]
        }
        
        # Initialize with sample data if empty
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample GitHub code examples."""
        sample_file = self.data_dir / 'sample_data.json'
        
        if not sample_file.exists():
            sample_data = self._create_sample_data()
            with open(sample_file, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info("Initialized GitHub code dataset with sample data")
    
    def _create_sample_data(self) -> List[Dict[str, Any]]:
        """Create sample GitHub code examples."""
        return [
            {
                "id": "python_flask_rest_api",
                "repository": "pallets/flask",
                "file_path": "examples/rest_api.py",
                "language": "python",
                "code": """from flask import Flask, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class UserAPI(Resource):
    def get(self, user_id):
        # Get user by ID
        user = get_user_by_id(user_id)
        if user:
            return jsonify(user)
        return {'message': 'User not found'}, 404
    
    def post(self):
        # Create new user
        data = request.get_json()
        user = create_user(data)
        return jsonify(user), 201

api.add_resource(UserAPI, '/users', '/users/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)""",
                "description": "Flask REST API example with user management",
                "tags": ["python", "flask", "rest-api", "web-development"],
                "stars": 65000,
                "forks": 15000,
                "last_updated": "2024-01-15T10:30:00Z",
                "url": "https://github.com/pallets/flask",
                "relevance_score": 0.95
            },
            {
                "id": "javascript_react_hooks",
                "repository": "facebook/react",
                "file_path": "examples/hooks/custom_hook.js",
                "language": "javascript",
                "code": """import { useState, useEffect } from 'react';

// Custom hook for API calls
function useApi(url) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const response = await fetch(url);
                const result = await response.json();
                setData(result);
            } catch (err) {
                setError(err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [url]);

    return { data, loading, error };
}

export default useApi;""",
                "description": "React custom hook for API calls with loading states",
                "tags": ["javascript", "react", "hooks", "api", "frontend"],
                "stars": 200000,
                "forks": 40000,
                "last_updated": "2024-01-20T14:15:00Z",
                "url": "https://github.com/facebook/react",
                "relevance_score": 0.92
            },
            {
                "id": "python_pandas_data_analysis",
                "repository": "pandas-dev/pandas",
                "file_path": "examples/data_analysis.py",
                "language": "python",
                "code": """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('sales_data.csv')

# Data cleaning
df['date'] = pd.to_datetime(df['date'])
df = df.dropna()

# Group by month and calculate metrics
monthly_sales = df.groupby(df['date'].dt.to_period('M')).agg({
    'sales': ['sum', 'mean', 'count'],
    'profit': 'sum'
}).round(2)

# Create visualization
plt.figure(figsize=(12, 6))
monthly_sales['sales']['sum'].plot(kind='bar')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("Monthly Sales Summary:")
print(monthly_sales)""",
                "description": "Pandas data analysis example with sales data",
                "tags": ["python", "pandas", "data-analysis", "visualization", "data-science"],
                "stars": 35000,
                "forks": 15000,
                "last_updated": "2024-01-18T09:45:00Z",
                "url": "https://github.com/pandas-dev/pandas",
                "relevance_score": 0.88
            }
        ]
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about the GitHub code dataset."""
        return {
            "name": "GitHub Code Examples",
            "description": "Real programming examples from popular GitHub repositories",
            "source": "GitHub",
            "language": "multi",
            "tags": ["github", "real-code", "production", "best-practices"],
            "size": len(self._load_data()),
            "last_updated": datetime.now(),
            "version": "1.0"
        }
    
    def _load_data(self) -> List[Dict[str, Any]]:
        """Load GitHub code data from storage."""
        try:
            sample_file = self.data_dir / 'sample_data.json'
            if sample_file.exists():
                with open(sample_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading GitHub code data: {e}")
        
        return []
    
    def search(self, query: str, language: Optional[str] = None, 
               tags: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Search GitHub code examples.
        
        Args:
            query: Search query
            language: Programming language filter
            tags: Tag filters
            
        Returns:
            List of matching code examples
        """
        data = self._load_data()
        results = []
        
        query_lower = query.lower()
        
        for example in data:
            # Check if example matches query
            if (query_lower in example['code'].lower() or
                query_lower in example['description'].lower() or
                query_lower in example['repository'].lower()):
                
                # Apply language filter
                if language and example['language'].lower() != language.lower():
                    continue
                
                # Apply tag filter
                if tags and not any(tag.lower() in [t.lower() for t in example['tags']] for tag in tags):
                    continue
                
                # Calculate relevance score based on query match
                relevance = self._calculate_relevance(query_lower, example)
                example['relevance_score'] = relevance
                
                results.append(example)
        
        # Sort by relevance score
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return results
    
    def _calculate_relevance(self, query: str, example: Dict[str, Any]) -> float:
        """Calculate relevance score for a code example."""
        score = 0.0
        
        # Code content relevance
        if query in example['code'].lower():
            score += 0.4
        
        # Description relevance
        if query in example['description'].lower():
            score += 0.3
        
        # Repository relevance
        if query in example['repository'].lower():
            score += 0.2
        
        # Tag relevance
        for tag in example['tags']:
            if query in tag.lower():
                score += 0.1
        
        # Popularity bonus
        score += min(example['stars'] / 10000, 0.1)
        
        return min(score, 1.0)
    
    def get_example(self, example_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific code example by ID.
        
        Args:
            example_id: Unique identifier for the example
            
        Returns:
            Code example data or None if not found
        """
        data = self._load_data()
        
        for example in data:
            if example['id'] == example_id:
                return example
        
        return None
    
    def add_example(self, example: GitHubCodeExample) -> bool:
        """
        Add a new GitHub code example.
        
        Args:
            example: GitHubCodeExample instance
            
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
            
            logger.info(f"Added GitHub code example: {example.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding GitHub code example: {e}")
            return False
    
    def get_languages(self) -> List[str]:
        """Get list of available programming languages."""
        data = self._load_data()
        languages = set()
        
        for example in data:
            languages.add(example['language'])
        
        return sorted(list(languages))
    
    def get_tags(self) -> List[str]:
        """Get list of available tags."""
        data = self._load_data()
        tags = set()
        
        for example in data:
            tags.update(example['tags'])
        
        return sorted(list(tags))
