# 👨‍💻 ATLES Code Studio - Developer Guide

**Quick start guide for developers who want to contribute or extend ATLES Code Studio**

## 🚀 **Quick Setup**

### **1. Clone and Install**
```bash
git clone https://github.com/your-repo/atles-code-studio.git
cd atles-code-studio

# Install dependencies
pip install PyQt6 psutil pywin32 pillow pygments

# Optional: Install AI dependencies
pip install ollama-python requests
```

### **2. Run Development Version**
```bash
python atles_code_studio.py
```

### **3. Test Your Changes**
```bash
# Run with debug output
python atles_code_studio.py --debug

# Run tests (if available)
python -m pytest tests/
```

## 🏗️ **Architecture Overview**

```
ATLES Code Studio
├── 🎨 UI Layer (PyQt6)
│   ├── ATLESCodeStudio (Main Window)
│   ├── CodeEditor (Text Editor)
│   ├── FileExplorer (Project Tree)
│   ├── TerminalWidget (Integrated Terminal)
│   └── SettingsPanel (Configuration)
├── 🧠 AI Layer
│   ├── AICodeAssistant (Intelligence)
│   ├── AICompletionWidget (UI)
│   └── SyntaxHighlighter (Themes)
├── ⚙️ Core Systems
│   ├── Settings Management
│   ├── File Operations
│   └── Event Handling
└── 🔌 Extension Points
    ├── Plugin System
    ├── Theme Engine
    └── Language Support
```

## 🎯 **Common Development Tasks**

### **Adding a New Language**

1. **Extend SyntaxHighlighter:**
```python
def _setup_go_rules(self):
    """Setup Go syntax highlighting rules"""
    colors = self.themes.get(self.theme, self.themes["VS Code Dark"])
    
    # Go keywords
    keywords = ['package', 'import', 'func', 'var', 'const', 'type', 
                'struct', 'interface', 'if', 'else', 'for', 'range', 
                'switch', 'case', 'default', 'go', 'defer', 'return']
    
    keyword_format = QTextCharFormat()
    keyword_format.setForeground(colors["keyword"])
    keyword_format.setFontWeight(QFont.Weight.Bold)
    
    for keyword in keywords:
        pattern = QRegularExpression(f'\\b{keyword}\\b')
        self.highlighting_rules.append((pattern, keyword_format))
```

2. **Update language detection:**
```python
def _detect_language(self):
    """Detect programming language from file extension"""
    ext = os.path.splitext(self.file_path)[1].lower()
    language_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.go': 'go',        # Add your language
        # ... existing mappings
    }
```

3. **Add to AI completion:**
```python
def get_code_completions(self, code_context, cursor_position, language="python"):
    """Get AI-powered code completions"""
    if language == "go":
        return self._get_go_completions(code_context, cursor_position)
    # ... existing logic
```

### **Creating a New Theme**

1. **Add theme to SyntaxHighlighter:**
```python
self.themes["My Theme"] = {
    "keyword": QColor(255, 123, 114),     # Coral
    "string": QColor(164, 252, 205),      # Mint
    "comment": QColor(139, 148, 158),     # Gray
    "number": QColor(121, 192, 255),      # Sky blue
    "function": QColor(255, 184, 108),    # Orange
    "class": QColor(255, 123, 114),       # Coral
    "operator": QColor(255, 255, 255),    # White
    "error": QColor(248, 81, 73),         # Red
    "builtin": QColor(180, 142, 173),     # Purple
}
```

2. **Add to settings:**
```python
# In SettingsPanel._create_theme_tab()
themes = ["VS Code Dark", "Monokai", "Solarized Dark", 
          "GitHub Dark", "Dracula", "My Theme"]  # Add here
```

### **Adding AI Features**

1. **Extend AICodeAssistant:**
```python
def get_code_documentation(self, function_name: str, context: str) -> str:
    """Generate documentation for a function"""
    if not self.ollama_client:
        return ""
        
    prompt = f"""
    Generate documentation for this function:
    
    Function: {function_name}
    Context: {context}
    
    Provide a docstring with description, parameters, and return value.
    """
    
    return self.ollama_client.generate("qwen2.5-coder:latest", prompt)
```

2. **Add UI integration:**
```python
# In CodeEditor
def generate_docstring(self):
    """Generate docstring for current function"""
    cursor = self.textCursor()
    # Find function definition
    # Get AI documentation
    # Insert docstring
```

### **Creating Plugins**

1. **Basic plugin structure:**
```python
class MyPlugin(ATLESPlugin):
    def __init__(self, editor: CodeEditor):
        super().__init__(editor)
        self.name = "My Plugin"
        
    def activate(self):
        """Setup plugin"""
        # Add menu items, connect signals, etc.
        pass
        
    def deactivate(self):
        """Cleanup plugin"""
        # Remove UI elements, disconnect signals
        pass
```

2. **Register plugin:**
```python
# In main application
plugin_manager = PluginManager(editor)
plugin_manager.register_plugin(MyPlugin)
plugin_manager.activate_plugin("My Plugin")
```

## 🧪 **Testing Guidelines**

### **Unit Tests**
```python
import unittest
from PyQt6.QtWidgets import QApplication
from atles_code_studio import CodeEditor

class TestCodeEditor(unittest.TestCase):
    def setUp(self):
        self.app = QApplication.instance() or QApplication([])
        self.editor = CodeEditor()
        
    def test_load_file(self):
        """Test file loading functionality"""
        # Create test file
        with open("test.py", "w") as f:
            f.write("print('test')")
            
        # Test loading
        result = self.editor.load_file("test.py")
        self.assertTrue(result)
        self.assertEqual(self.editor.toPlainText(), "print('test')")
        
        # Cleanup
        os.remove("test.py")
```

### **Integration Tests**
```python
def test_ai_completion_integration(self):
    """Test AI completion with mock client"""
    mock_client = MockOllamaClient()
    ai_assistant = AICodeAssistant(mock_client)
    
    completions = ai_assistant.get_code_completions(
        "my_list.", 9, "python"
    )
    
    self.assertGreater(len(completions), 0)
    self.assertIn('append', [c['text'] for c in completions])
```

## 🐛 **Debugging Tips**

### **Enable Debug Mode**
```python
# Add to main()
import logging
logging.basicConfig(level=logging.DEBUG)

# Or run with debug flag
python atles_code_studio.py --debug
```

### **Common Issues**

1. **PyQt6 Import Errors:**
```bash
# Try PyQt5 as fallback
pip uninstall PyQt6
pip install PyQt5
```

2. **AI Features Not Working:**
```python
# Check Ollama installation
ollama --version

# Pull required model
ollama pull qwen2.5-coder:latest

# Test connection
curl http://localhost:11434/api/generate -d '{"model":"qwen2.5-coder:latest","prompt":"test"}'
```

3. **Syntax Highlighting Issues:**
```python
# Check if Pygments is installed
pip install pygments

# Verify theme loading
print(syntax_highlighter.themes.keys())
```

### **Performance Profiling**
```python
import cProfile
import pstats

# Profile the application
cProfile.run('main()', 'profile_stats')
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative').print_stats(20)
```

## 📝 **Code Style Guidelines**

### **Python Style**
- Follow PEP 8
- Use type hints where possible
- Add docstrings to all public methods
- Keep lines under 100 characters

```python
def process_file(file_path: str, encoding: str = 'utf-8') -> bool:
    """
    Process a file with the given encoding.
    
    Args:
        file_path: Path to the file to process
        encoding: File encoding (default: utf-8)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
        return True
    except Exception as e:
        logger.error(f"Failed to process {file_path}: {e}")
        return False
```

### **PyQt6 Style**
- Use signals and slots for communication
- Properly manage widget lifecycle
- Use stylesheets for consistent theming

```python
class MyWidget(QWidget):
    # Define signals at class level
    data_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        """Setup UI elements"""
        layout = QVBoxLayout(self)
        # ... setup widgets
        
    def connect_signals(self):
        """Connect signals and slots"""
        self.button.clicked.connect(self.on_button_clicked)
        
    def on_button_clicked(self):
        """Handle button click"""
        self.data_changed.emit("button clicked")
```

## 🚀 **Performance Optimization**

### **Editor Performance**
- Use `QPlainTextEdit` for large files
- Implement lazy loading for syntax highlighting
- Cache AI completions when possible

```python
class OptimizedEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Enable optimizations
        self.setMaximumBlockCount(10000)  # Limit for very large files
        self.setCenterOnScroll(True)      # Smooth scrolling
```

### **AI Performance**
- Cache frequent completions
- Use background threads for AI requests
- Implement request debouncing

```python
class CachedAIAssistant(AICodeAssistant):
    def __init__(self, ollama_client=None):
        super().__init__(ollama_client)
        self.completion_cache = {}
        self.cache_size = 100
        
    def get_code_completions(self, code_context, cursor_position, language="python"):
        """Get completions with caching"""
        cache_key = hash((code_context, cursor_position, language))
        
        if cache_key in self.completion_cache:
            return self.completion_cache[cache_key]
            
        completions = super().get_code_completions(code_context, cursor_position, language)
        
        # Cache result
        if len(self.completion_cache) >= self.cache_size:
            # Remove oldest entry
            oldest_key = next(iter(self.completion_cache))
            del self.completion_cache[oldest_key]
            
        self.completion_cache[cache_key] = completions
        return completions
```

## 📦 **Building and Distribution**

### **Create Executable**
```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed atles_code_studio.py

# With icon and additional files
pyinstaller --onefile --windowed --icon=icon.ico \
    --add-data "themes;themes" \
    --add-data "plugins;plugins" \
    atles_code_studio.py
```

### **Package for Distribution**
```bash
# Create wheel
python setup.py bdist_wheel

# Create source distribution
python setup.py sdist

# Upload to PyPI (if public)
twine upload dist/*
```

## 🤝 **Contributing Workflow**

### **1. Fork and Clone**
```bash
git clone https://github.com/your-username/atles-code-studio.git
cd atles-code-studio
git remote add upstream https://github.com/original-repo/atles-code-studio.git
```

### **2. Create Feature Branch**
```bash
git checkout -b feature/my-awesome-feature
```

### **3. Make Changes**
- Follow code style guidelines
- Add tests for new features
- Update documentation

### **4. Test Changes**
```bash
# Run tests
python -m pytest tests/

# Test manually
python atles_code_studio.py

# Check code style
flake8 atles_code_studio.py
black atles_code_studio.py
```

### **5. Submit Pull Request**
```bash
git add .
git commit -m "Add awesome feature"
git push origin feature/my-awesome-feature
```

Then create a pull request on GitHub with:
- Clear description of changes
- Screenshots if UI changes
- Test results
- Breaking change notes (if any)

## 📚 **Resources**

- **PyQt6 Documentation**: https://doc.qt.io/qtforpython/
- **Python Style Guide**: https://pep8.org/
- **Ollama Documentation**: https://ollama.ai/docs
- **Qt Designer**: For visual UI design
- **GitHub Issues**: For bug reports and feature requests

---

**Happy coding! 🚀 Let's make ATLES Code Studio even more awesome together!**
