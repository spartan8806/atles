# 🧠 ATLES Code Studio - Professional AI-Powered IDE

**The most advanced AI-integrated development environment built with Python and PyQt6**

![ATLES Code Studio](https://img.shields.io/badge/ATLES-Code%20Studio-blue?style=for-the-badge&logo=python)
![Version](https://img.shields.io/badge/version-1.0.0-green?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-orange?style=for-the-badge)

## 🚀 **Overview**

ATLES Code Studio is a revolutionary IDE that combines the power of traditional code editing with cutting-edge AI assistance. Built from the ground up with Python and PyQt6, it offers a VS Code-like experience enhanced with intelligent AI features powered by local language models.

## ✨ **Key Features**

### 🎨 **Professional Code Editor**
- **Advanced Syntax Highlighting**: 5 beautiful themes (VS Code Dark, Monokai, Solarized Dark, GitHub Dark, Dracula)
- **Multi-language Support**: Python, JavaScript, C++, with extensible architecture
- **Real-time Error Detection**: Instant syntax error highlighting with wavy underlines
- **Smart Code Folding**: Click-to-fold functions, classes, and control structures
- **Line Numbers**: Professional line numbering with fold indicators
- **Bracket Matching**: Intelligent bracket highlighting and auto-completion
- **Auto-indentation**: Context-aware indentation for Python and other languages

### 🔍 **Advanced Search & Navigation**
- **Find & Replace**: Powerful search with regex support, case sensitivity, and whole word matching
- **Go to Line**: Quick navigation with Ctrl+G
- **Replace All**: Batch replacements with occurrence counting
- **Smart Search**: Wraps around document automatically

### 🤖 **AI-Powered Intelligence**
- **Code Completion**: Context-aware suggestions as you type
- **Method Completion**: Smart object method suggestions (`.` triggers)
- **Import Assistance**: Automatic import suggestions for common modules
- **Comment-to-Code**: Generate code from natural language comments
- **Error Explanations**: AI-powered error message explanations
- **Refactoring Suggestions**: Intelligent code improvement recommendations

### 🖥️ **Enhanced Terminal**
- **Command History**: Navigate with Up/Down arrows
- **Tab Completion**: File and directory auto-completion
- **ATLES Commands**: Built-in commands for file management and analysis
- **Directory Tracking**: Smart prompt showing current directory
- **Built-in Commands**: `cd`, `clear`, `history`, and custom ATLES commands

### ⚙️ **Comprehensive Settings**
- **Theme Customization**: 5 pre-built themes plus custom color options
- **Font Configuration**: Family and size selection
- **Editor Behavior**: Toggle auto-indent, bracket matching, line numbers
- **AI Configuration**: Model selection, temperature control, feature toggles
- **Terminal Customization**: Appearance and behavior settings
- **Persistent Settings**: All preferences saved automatically

### 📁 **Project Management**
- **File Explorer**: VS Code-like sidebar with project tree
- **Multi-tab Editing**: Professional tabbed interface
- **File Icons**: Language-specific file type indicators
- **Project Navigation**: Quick file opening and management

## 🛠️ **Installation**

### Prerequisites
- Python 3.8 or higher
- PyQt6 (automatically installed)
- Optional: Ollama for AI features

### Quick Start
```bash
# Clone the repository
git clone https://github.com/your-repo/atles-code-studio.git
cd atles-code-studio

# Install dependencies
pip install PyQt6 psutil pywin32 pillow pygments

# Run ATLES Code Studio
python atles_code_studio.py
```

### Using the Launcher
```bash
# Windows
.\run_code_studio.bat

# The launcher will automatically check and install dependencies
```

## 🎯 **Usage Guide**

### **Getting Started**
1. **Launch**: Run `python atles_code_studio.py` or use the batch file
2. **Open Project**: Use `Ctrl+Shift+O` to open a folder
3. **Create File**: Use `Ctrl+N` for new file or `atles new filename.py` in terminal
4. **Start Coding**: Enjoy AI-powered assistance as you type!

### **Keyboard Shortcuts**
| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New File |
| `Ctrl+O` | Open File |
| `Ctrl+S` | Save File |
| `Ctrl+Shift+S` | Save As |
| `Ctrl+F` | Find |
| `Ctrl+H` | Replace |
| `Ctrl+G` | Go to Line |
| `Ctrl+,` | Settings |
| `Ctrl+`` | Toggle Terminal |
| `Ctrl+Shift+E` | Explain Code (AI) |
| `Ctrl+Shift+O` | Optimize Code (AI) |
| `Tab` | Indent / Auto-complete |
| `Shift+Tab` | Unindent |

### **AI Features**

#### **Code Completion**
- Type and get intelligent suggestions
- Use `.` after objects for method completion
- Start typing imports for module suggestions
- Write comments and get code generation

#### **Terminal Commands**
```bash
# ATLES-specific commands
atles help          # Show help
atles new <file>    # Create and open file
atles open <file>   # Open file in editor
atles run <file>    # Run Python file
atles analyze       # Analyze current directory

# Standard commands
cd <directory>      # Change directory
clear              # Clear terminal
history            # Show command history
```

### **Themes**
Switch between 5 beautiful themes in Settings (`Ctrl+,`):
- **VS Code Dark**: Classic dark theme with blue accents
- **Monokai**: Popular theme with vibrant colors
- **Solarized Dark**: Scientific color palette
- **GitHub Dark**: Modern GitHub-inspired theme
- **Dracula**: Purple and pink vampire theme

## 🏗️ **Architecture**

### **Core Components**
```
ATLES Code Studio
├── CodeEditor (QPlainTextEdit)
│   ├── SyntaxHighlighter
│   ├── LineNumberArea
│   └── AICompletionWidget
├── FileExplorer (QTreeWidget)
├── TerminalWidget (QWidget)
├── AIAssistantPanel (QWidget)
├── SettingsPanel (QDialog)
└── Main Window (QMainWindow)
```

### **AI Integration**
- **Local AI Models**: Uses Ollama for privacy and performance
- **Context-Aware**: Analyzes surrounding code for better suggestions
- **Extensible**: Easy to add new AI features and models
- **Offline-First**: Works without internet connection

### **Plugin Architecture**
The codebase is designed for extensibility:
- **Language Support**: Easy to add new programming languages
- **Theme System**: Simple theme creation and customization
- **AI Models**: Support for multiple AI backends
- **Tool Integration**: Extensible tool and command system

## 🔧 **Configuration**

### **Settings File**
Settings are automatically saved to `atles_settings.json`:
```json
{
  "font_family": "Consolas",
  "font_size": 11,
  "theme": "VS Code Dark",
  "auto_indent": true,
  "ai_model": "qwen2.5-coder:latest",
  "enable_completion": true
}
```

### **AI Configuration**
- **Models**: Support for various Ollama models
- **Temperature**: Control AI creativity (0-100%)
- **Features**: Toggle completion, suggestions, error explanations
- **Performance**: Configurable response timeouts and caching

## 🚀 **Advanced Features**

### **Code Folding**
- Click ▼/▶ indicators in line numbers
- Supports functions, classes, control structures
- Maintains fold state during editing
- Visual feedback with clear indicators

### **Real-time Error Detection**
- Instant Python syntax checking
- Wavy red underlines for errors
- Non-intrusive 1-second debounce
- AI-powered error explanations

### **Smart Editing**
- Auto-bracket completion: `(` → `()`
- Quote pairing: `"` → `""`
- Smart indentation after `:`, `{`, `[`
- Multi-line indent/unindent with Tab/Shift+Tab

### **AI Code Generation**
- Write comments starting with `#` and get code suggestions
- Context-aware completions based on surrounding code
- Method suggestions based on object types
- Import statement auto-completion

## 🎨 **Customization**

### **Creating Custom Themes**
Add new themes to the `SyntaxHighlighter` class:
```python
"My Theme": {
    "keyword": QColor(255, 100, 100),    # Red keywords
    "string": QColor(100, 255, 100),     # Green strings
    "comment": QColor(100, 100, 255),    # Blue comments
    # ... more colors
}
```

### **Adding Language Support**
Extend the syntax highlighter:
```python
def _setup_my_language_rules(self):
    """Setup syntax rules for new language"""
    # Define keywords, patterns, etc.
    pass
```

### **Custom AI Models**
Configure different AI models in settings:
- Ollama models: `qwen2.5-coder`, `codellama`, `deepseek-coder`
- Custom endpoints and API configurations
- Model-specific prompt templates

## 🐛 **Troubleshooting**

### **Common Issues**

#### **PyQt6 Installation**
```bash
# If PyQt6 fails to install
pip install PyQt6 --upgrade
# Or try PyQt5 as fallback
pip install PyQt5
```

#### **AI Features Not Working**
1. Install Ollama: https://ollama.ai/
2. Pull a coding model: `ollama pull qwen2.5-coder:latest`
3. Check AI settings in `Ctrl+,` → AI Assistant tab

#### **Syntax Highlighting Issues**
- Install Pygments: `pip install pygments`
- Check theme settings in preferences
- Verify file extension is recognized

#### **Terminal Not Working**
- Ensure proper shell access (cmd.exe on Windows)
- Check terminal settings in preferences
- Try restarting the application

### **Performance Tips**
- Use smaller AI models for faster completion
- Disable AI features if not needed
- Close unused tabs to save memory
- Use code folding for large files

## 🤝 **Contributing**

We welcome contributions! Here's how to get started:

### **Development Setup**
```bash
# Clone and setup development environment
git clone https://github.com/your-repo/atles-code-studio.git
cd atles-code-studio
pip install -r requirements.txt

# Run in development mode
python atles_code_studio.py
```

### **Code Style**
- Follow PEP 8 for Python code
- Use type hints where appropriate
- Add docstrings to all public methods
- Write tests for new features

### **Adding Features**
1. Fork the repository
2. Create a feature branch
3. Implement your feature with tests
4. Submit a pull request with detailed description

## 📊 **Comparison**

| Feature | ATLES Code Studio | VS Code | PyCharm | Sublime Text |
|---------|-------------------|---------|---------|--------------|
| **AI Integration** | ✅ Built-in | ❌ Extensions | ❌ Plugins | ❌ None |
| **Offline AI** | ✅ Local Models | ❌ Cloud Only | ❌ Cloud Only | ❌ None |
| **Python Focus** | ✅ Optimized | ⚠️ Generic | ✅ Specialized | ⚠️ Generic |
| **Lightweight** | ✅ Fast Startup | ❌ Heavy | ❌ Very Heavy | ✅ Fast |
| **Customizable** | ✅ Themes/Settings | ✅ Extensions | ⚠️ Limited | ✅ Packages |
| **Free & Open** | ✅ MIT License | ✅ Free | ❌ Paid | ❌ Paid |

## 🔮 **Roadmap**

### **Version 1.1** (Coming Soon)
- [ ] Git integration with status indicators
- [ ] Multiple cursor editing (Alt+Click)
- [ ] Project management with .atles files
- [ ] Plugin system for extensions
- [ ] Collaborative editing features

### **Version 1.2** (Future)
- [ ] Integrated debugger
- [ ] Code profiling tools
- [ ] Advanced refactoring tools
- [ ] Web development features
- [ ] Mobile app companion

### **Version 2.0** (Vision)
- [ ] Cloud synchronization
- [ ] Team collaboration features
- [ ] Advanced AI models
- [ ] Voice coding support
- [ ] AR/VR development tools

## 📄 **License**

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **PyQt6**: Excellent GUI framework
- **Ollama**: Local AI model serving
- **Pygments**: Syntax highlighting library
- **VS Code**: Inspiration for UI/UX design
- **Python Community**: Amazing ecosystem and support

## 📞 **Support**

- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Join our GitHub Discussions
- **Documentation**: Check our Wiki for detailed guides
- **Community**: Join our Discord server

---

**Built with ❤️ by the ATLES Team**

*Making AI-powered development accessible to everyone*
