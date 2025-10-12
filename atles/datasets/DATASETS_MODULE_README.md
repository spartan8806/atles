# ATLES Code Datasets - Module Documentation

This module provides comprehensive access to various code datasets including GitHub code examples, programming books, code challenges, and framework documentation.

## 🚀 Quick Start

```python
from atles.datasets import CodeDatasetManager

# Initialize the dataset manager
manager = CodeDatasetManager()

# Search across all datasets
results = manager.search_code("python flask api")

# Search specific dataset type
github_results = manager.search_code("react hooks", dataset_type="github_code")

# Get dataset information
info = manager.get_dataset_info()
stats = manager.get_statistics()
```

## 📚 Available Datasets

### 1. GitHub Code Examples
- **Purpose**: Real programming examples from popular GitHub repositories
- **Content**: Production-quality code patterns and best practices
- **Languages**: Python, JavaScript, TypeScript, Java, C++, Rust
- **Features**: Star ratings, fork counts, repository metadata

### 2. Programming Books
- **Purpose**: Best practices and design patterns from authoritative books
- **Content**: Clean code principles, design patterns, refactoring techniques
- **Difficulty Levels**: Beginner, Intermediate, Advanced
- **Books**: Clean Code, Design Patterns, Effective Python, Refactoring

### 3. Code Challenges
- **Purpose**: Algorithm problems and coding challenges
- **Content**: Problem statements, solutions, explanations, complexity analysis
- **Difficulty Levels**: Easy, Medium, Hard
- **Categories**: Arrays, Trees, Dynamic Programming, etc.
- **Sources**: LeetCode, HackerRank style problems

### 4. Framework Documentation
- **Purpose**: API usage examples and framework documentation
- **Content**: CRUD operations, state management, ORM queries
- **Frameworks**: FastAPI, React, Django, etc.
- **Categories**: API, Database, State Management, Configuration

## 🔍 Search and Filtering

### Basic Search
```python
# Search all datasets
results = manager.search_code("authentication")

# Search with language filter
python_results = manager.search_code("api", language="python")

# Search with tag filters
web_results = manager.search_code("web", tags=["frontend", "backend"])
```

### Advanced Search
```python
# Search specific dataset with multiple filters
book_results = manager.search_code(
    "design pattern",
    dataset_type="programming_books",
    difficulty="intermediate"
)

# Search challenges by category
array_challenges = manager.search_code(
    "array",
    dataset_type="code_challenges",
    category="arrays"
)
```

## 📊 Dataset Management

### Adding Custom Datasets
```python
# Add a custom dataset
success = manager.add_custom_dataset(
    name="my_custom_data",
    description="Custom programming examples",
    source="Internal",
    language="python",
    tags=["custom", "internal"],
    data=[...]  # List of example dictionaries
)
```

### Getting Statistics
```python
# Get comprehensive statistics
stats = manager.get_statistics()
print(f"Total datasets: {stats['total_datasets']}")
print(f"Total examples: {stats['total_examples']}")
print(f"Languages: {stats['languages']}")
print(f"Tags: {stats['tags']}")
```

## 🔗 Integration with ATLES

### Basic Integration
```python
from atles.datasets.integration_example import CodeDatasetIntegration

# Initialize integration
integration = CodeDatasetIntegration()

# Search and get suggestions
results = await integration.search_and_suggest("python async programming")
print(f"Found {results['total_results']} results")
for suggestion in results['suggestions']:
    print(f"💡 {suggestion}")
```

### Learning Paths
```python
# Generate learning path for a topic
learning_path = await integration.get_learning_path("machine learning", "beginner")
for step in learning_path['steps']:
    print(f"Step {step['step']}: {step['title']}")
    print(f"  {step['description']}")
```

### Next Steps Suggestions
```python
# Get learning suggestions
next_steps = await integration.suggest_next_steps("python basics", "beginner")
for step in next_steps:
    print(f"• {step}")
```

## 🧪 Testing

Run the test suite to verify everything works:

```bash
# Test the main functionality
python test_datasets.py

# Test individual datasets
python -m atles.datasets.integration_example
```

## 📁 File Structure

```
atles/datasets/
├── __init__.py              # Module initialization
├── dataset_manager.py       # Central dataset coordinator
├── github_code.py          # GitHub code examples handler
├── programming_books.py    # Programming books handler
├── code_challenges.py      # Code challenges handler
├── framework_docs.py       # Framework documentation handler
├── integration_example.py  # ATLES integration example
└── README.md              # This documentation
```

## 🔧 Configuration

The datasets are automatically configured to use the ATLES home directory:

- **Default Location**: `D:\.atles\datasets\`
- **GitHub Data**: `D:\.atles\datasets\github\`
- **Books Data**: `D:\.atles\datasets\books\`
- **Challenges Data**: `D:\.atles\datasets\challenges\`
- **Framework Data**: `D:\.atles\datasets\frameworks\`
- **Custom Data**: `D:\.atles\datasets\custom\`

## 💡 Usage Examples

### Example 1: Learning Python Flask
```python
# Search for Flask examples
flask_results = manager.search_code("flask", language="python")

# Get specific example
example = manager.get_code_example("python_flask_rest_api", "github_code")
if example:
    print(f"Title: {example['title']}")
    print(f"Code:\n{example['code']}")
```

### Example 2: Studying Design Patterns
```python
# Search for design pattern examples
pattern_results = manager.search_code(
    "singleton",
    dataset_type="programming_books",
    difficulty="intermediate"
)

# Get learning path
learning_path = await integration.get_learning_path("design patterns", "beginner")
```

### Example 3: Practicing Algorithms
```python
# Get easy array problems
easy_arrays = manager.search_code(
    "array",
    dataset_type="code_challenges",
    difficulty="easy"
)

# Get specific challenge
challenge = manager.get_code_example("two_sum", "code_challenges")
if challenge:
    print(f"Problem: {challenge['problem_statement']}")
    print(f"Solution:\n{challenge['solution']}")
```

## 🚨 Error Handling

The system includes comprehensive error handling:

- **Import Failures**: Graceful fallback to placeholder implementations
- **Search Errors**: Individual dataset failures don't crash the system
- **Data Loading**: Handles missing or corrupted data files
- **Network Issues**: Offline-first design with local sample data

## 🔮 Future Enhancements

- **Real-time GitHub Integration**: Fetch live data from GitHub API
- **Machine Learning**: Intelligent code suggestion and ranking
- **Collaborative Learning**: User-contributed examples and ratings
- **Multi-language Support**: Examples in multiple programming languages
- **Interactive Tutorials**: Step-by-step guided learning experiences

## 🤝 Contributing

To add new examples or improve existing ones:

1. **Add to Sample Data**: Modify the `_create_sample_data()` methods
2. **Extend Search**: Add new search parameters and filters
3. **Improve Relevance**: Enhance the relevance scoring algorithms
4. **Add New Datasets**: Create new dataset handler classes

## 📝 License

This module is part of the ATLES project and follows the same licensing terms.

---

**Happy Coding! 🎉**

The ATLES Code Datasets provide a comprehensive foundation for learning programming concepts, studying best practices, and exploring real-world code examples. Whether you're a beginner looking for simple examples or an advanced developer seeking complex patterns, there's something here for everyone.
