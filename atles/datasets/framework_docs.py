"""
Framework Documentation Dataset

Handles API usage examples and documentation from various programming
frameworks, libraries, and tools.
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
class FrameworkExample:
    """Represents a framework API usage example."""
    id: str
    framework: str
    version: str
    category: str  # api, configuration, deployment, etc.
    language: str
    title: str
    description: str
    code: str
    api_endpoint: Optional[str]
    parameters: List[Dict[str, Any]]
    return_value: Optional[str]
    dependencies: List[str]
    tags: List[str]
    difficulty: str  # beginner, intermediate, advanced
    relevance_score: float = 0.0


class FrameworkDocsDataset:
    """
    Dataset handler for framework documentation and API examples.
    
    Provides access to usage examples, configuration patterns, and
    best practices from popular frameworks and libraries.
    """
    
    def __init__(self, data_dir: Path):
        """
        Initialize framework documentation dataset.
        
        Args:
            data_dir: Directory to store framework documentation data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize with sample data if empty
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample framework documentation examples."""
        sample_file = self.data_dir / 'sample_data.json'
        
        if not sample_file.exists():
            sample_data = self._create_sample_data()
            with open(sample_file, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info("Initialized framework documentation dataset with sample data")
    
    def _create_sample_data(self) -> List[Dict[str, Any]]:
        """Create sample framework documentation examples."""
        return [
            {
                "id": "fastapi_basic_crud",
                "framework": "FastAPI",
                "version": "0.104.0",
                "category": "api",
                "language": "python",
                "title": "Basic CRUD Operations with FastAPI",
                "description": "Create, read, update, and delete operations using FastAPI with Pydantic models",
                "code": """from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="User Management API")

# Pydantic model for User
class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    age: int

# In-memory storage (replace with database in production)
users_db = []
user_id_counter = 1

@app.post("/users/", response_model=User)
async def create_user(user: User):
    global user_id_counter
    user.id = user_id_counter
    user_id_counter += 1
    users_db.append(user)
    return user

@app.get("/users/", response_model=List[User])
async def get_users():
    return users_db

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: User):
    for i, user in enumerate(users_db):
        if user.id == user_id:
            user_update.id = user_id
            users_db[i] = user_update
            return user_update
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    for i, user in enumerate(users_db):
        if user.id == user_id:
            del users_db[i]
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)""",
                "api_endpoint": "/users/",
                "parameters": [
                    {"name": "user", "type": "User", "description": "User data to create"},
                    {"name": "user_id", "type": "int", "description": "User ID for operations"}
                ],
                "return_value": "User object or list of users",
                "dependencies": ["fastapi", "pydantic", "uvicorn"],
                "tags": ["python", "fastapi", "api", "crud", "pydantic"],
                "difficulty": "intermediate",
                "relevance_score": 0.95
            },
            {
                "id": "react_hooks_state_management",
                "framework": "React",
                "version": "18.2.0",
                "category": "state-management",
                "language": "javascript",
                "title": "State Management with React Hooks",
                "description": "Managing complex state using useState, useEffect, and custom hooks",
                "code": """import React, { useState, useEffect, useCallback } from 'react';

// Custom hook for managing form state
function useForm(initialState) {
    const [values, setValues] = useState(initialState);
    const [errors, setErrors] = useState({});
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleChange = useCallback((e) => {
        const { name, value } = e.target;
        setValues(prev => ({
            ...prev,
            [name]: value
        }));
        
        // Clear error when user starts typing
        if (errors[name]) {
            setErrors(prev => ({
                ...prev,
                [name]: ''
            }));
        }
    }, [errors]);

    const handleSubmit = useCallback(async (onSubmit) => {
        setIsSubmitting(true);
        try {
            await onSubmit(values);
            setValues(initialState);
        } catch (error) {
            console.error('Form submission error:', error);
        } finally {
            setIsSubmitting(false);
        }
    }, [values, initialState]);

    return {
        values,
        errors,
        isSubmitting,
        handleChange,
        handleSubmit,
        setErrors
    };
}

// Example form component
function UserForm() {
    const { values, errors, isSubmitting, handleChange, handleSubmit } = useForm({
        name: '',
        email: '',
        age: ''
    });

    const onSubmit = async (formData) => {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        console.log('Form submitted:', formData);
    };

    return (
        <form onSubmit={(e) => {
            e.preventDefault();
            handleSubmit(onSubmit);
        }}>
            <div>
                <label>Name:</label>
                <input
                    type="text"
                    name="name"
                    value={values.name}
                    onChange={handleChange}
                />
                {errors.name && <span className="error">{errors.name}</span>}
            </div>
            
            <div>
                <label>Email:</label>
                <input
                    type="email"
                    name="email"
                    value={values.email}
                    onChange={handleChange}
                />
                {errors.email && <span className="error">{errors.email}</span>}
            </div>
            
            <div>
                <label>Age:</label>
                <input
                    type="number"
                    name="age"
                    value={values.age}
                    onChange={handleChange}
                />
                {errors.age && <span className="error">{errors.age}</span>}
            </div>
            
            <button type="submit" disabled={isSubmitting}>
                {isSubmitting ? 'Submitting...' : 'Submit'}
            </button>
        </form>
    );
}

export default UserForm;""",
                "api_endpoint": None,
                "parameters": [
                    {"name": "initialState", "type": "object", "description": "Initial form state"},
                    {"name": "onSubmit", "type": "function", "description": "Form submission handler"}
                ],
                "return_value": "Form state and handlers object",
                "dependencies": ["react"],
                "tags": ["javascript", "react", "hooks", "state-management", "forms"],
                "difficulty": "intermediate",
                "relevance_score": 0.92
            },
            {
                "id": "django_orm_queries",
                "framework": "Django",
                "version": "4.2.0",
                "category": "database",
                "language": "python",
                "title": "Advanced Django ORM Queries",
                "description": "Complex database queries using Django ORM with annotations, aggregations, and select_related",
                "code": """from django.db import models
from django.db.models import Q, F, Count, Avg, Sum, Case, When, Value
from django.contrib.auth.models import User

# Example models
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

# Advanced ORM queries
def advanced_queries():
    # 1. Annotate with calculated fields
    products_with_stats = Product.objects.annotate(
        total_orders=Count('orderitem'),
        avg_quantity=Avg('orderitem__quantity'),
        revenue=Sum(F('orderitem__quantity') * F('orderitem__price'))
    ).filter(is_active=True)
    
    # 2. Complex filtering with Q objects
    popular_products = Product.objects.filter(
        Q(stock__gt=0) & 
        Q(price__lte=100) &
        (Q(category__name='Electronics') | Q(category__name='Books'))
    ).annotate(
        order_count=Count('orderitem')
    ).filter(order_count__gte=5)
    
    # 3. Conditional annotations
    products_with_status = Product.objects.annotate(
        stock_status=Case(
            When(stock__gt=10, then=Value('In Stock')),
            When(stock__gt=0, then=Value('Low Stock')),
            default=Value('Out of Stock')
        )
    )
    
    # 4. Select related to avoid N+1 queries
    orders_with_details = Order.objects.select_related('user').prefetch_related(
        'products', 'orderitem_set__product'
    ).filter(status__in=['pending', 'processing'])
    
    # 5. Aggregations by category
    category_stats = Category.objects.annotate(
        product_count=Count('product'),
        avg_price=Avg('product__price'),
        total_stock=Sum('product__stock')
    ).filter(product_count__gt=0)
    
    return {
        'products_with_stats': list(products_with_stats),
        'popular_products': list(popular_products),
        'products_with_status': list(products_with_status),
        'orders_with_details': list(orders_with_details),
        'category_stats': list(category_stats)
    }

# Usage example
if __name__ == "__main__":
    # This would be run in Django shell or view
    results = advanced_queries()
    for key, value in results.items():
        print(f"\\n{key}:")
        for item in value[:3]:  # Show first 3 items
            print(f"  - {item}")""",
                "api_endpoint": None,
                "parameters": [],
                "return_value": "Dictionary with query results",
                "dependencies": ["django"],
                "tags": ["python", "django", "orm", "database", "queries"],
                "difficulty": "advanced",
                "relevance_score": 0.88
            }
        ]
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about the framework documentation dataset."""
        return {
            "name": "Framework Documentation and API Examples",
            "description": "API usage examples and documentation from popular frameworks and libraries",
            "source": "Framework Documentation",
            "language": "multi",
            "tags": ["frameworks", "api", "documentation", "examples", "best-practices"],
            "size": len(self._load_data()),
            "last_updated": datetime.now(),
            "version": "1.0"
        }
    
    def _load_data(self) -> List[Dict[str, Any]]:
        """Load framework documentation data from storage."""
        try:
            sample_file = self.data_dir / 'sample_data.json'
            if sample_file.exists():
                with open(sample_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading framework documentation data: {e}")
        
        return []
    
    def search(self, query: str, framework: Optional[str] = None, 
               language: Optional[str] = None, tags: Optional[List[str]] = None,
               category: Optional[str] = None, difficulty: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search framework documentation examples.
        
        Args:
            query: Search query
            framework: Framework name filter
            language: Programming language filter
            tags: Tag filters
            category: Example category filter
            difficulty: Difficulty level filter
            
        Returns:
            List of matching examples
        """
        data = self._load_data()
        results = []
        
        query_lower = query.lower()
        
        for example in data:
            # Check if example matches query
            if (query_lower in example['title'].lower() or
                query_lower in example['description'].lower() or
                query_lower in example['code'].lower() or
                query_lower in example['framework'].lower() or
                query_lower in example['category'].lower() or
                query_lower in example['tags']):
                
                # Apply framework filter
                if framework and example['framework'].lower() != framework.lower():
                    continue
                
                # Apply language filter
                if language and example['language'].lower() != language.lower():
                    continue
                
                # Apply tag filter
                if tags and not any(tag.lower() in [t.lower() for t in example['tags']] for tag in tags):
                    continue
                
                # Apply category filter
                if category and example['category'].lower() != category.lower():
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
        """Calculate relevance score for a framework documentation example."""
        score = 0.0
        
        # Title relevance
        if query in example['title'].lower():
            score += 0.25
        
        # Description relevance
        if query in example['description'].lower():
            score += 0.2
        
        # Code content relevance
        if query in example['code'].lower():
            score += 0.2
        
        # Framework relevance
        if query in example['framework'].lower():
            score += 0.15
        
        # Category relevance
        if query in example['category'].lower():
            score += 0.1
        
        # Tag relevance
        for tag in example['tags']:
            if query in tag.lower():
                score += 0.1
        
        return min(score, 1.0)
    
    def get_example(self, example_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific framework documentation example by ID.
        
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
    
    def add_example(self, example: FrameworkExample) -> bool:
        """
        Add a new framework documentation example.
        
        Args:
            example: FrameworkExample instance
            
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
            
            logger.info(f"Added framework documentation example: {example.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding framework documentation example: {e}")
            return False
    
    def get_frameworks(self) -> List[str]:
        """Get list of available frameworks."""
        data = self._load_data()
        frameworks = set()
        
        for example in data:
            frameworks.add(example['framework'])
        
        return sorted(list(frameworks))
    
    def get_categories(self) -> List[str]:
        """Get list of available example categories."""
        data = self._load_data()
        categories = set()
        
        for example in data:
            categories.add(example['category'])
        
        return sorted(list(categories))
    
    def get_examples_by_framework(self, framework: str) -> List[Dict[str, Any]]:
        """
        Get examples by specific framework.
        
        Args:
            framework: Framework name
            
        Returns:
            List of examples for the framework
        """
        data = self._load_data()
        results = []
        
        framework_lower = framework.lower()
        
        for example in data:
            if example['framework'].lower() == framework_lower:
                results.append(example)
        
        return results
    
    def get_examples_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get examples by category.
        
        Args:
            category: Example category
            
        Returns:
            List of examples in the specified category
        """
        data = self._load_data()
        results = []
        
        category_lower = category.lower()
        
        for example in data:
            if example['category'].lower() == category_lower:
                results.append(example)
        
        return results
