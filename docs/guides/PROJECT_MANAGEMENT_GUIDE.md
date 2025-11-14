# 🚀 ATLES Code Studio - Project Management Guide

**Complete guide to using ATLES project management features**

## 📋 **Table of Contents**

1. [Overview](#overview)
2. [ATLES Project Files](#atles-project-files)
3. [Creating Projects](#creating-projects)
4. [Project Settings](#project-settings)
5. [Build Configurations](#build-configurations)
6. [Git Integration](#git-integration)
7. [Package Management](#package-management)
8. [Project Templates](#project-templates)
9. [Best Practices](#best-practices)

## 🎯 **Overview**

ATLES Code Studio provides comprehensive project management capabilities that rival professional IDEs like Visual Studio Code and IntelliJ IDEA. The system is built around `.atles` project files that store project metadata, build configurations, and settings.

### **Key Features**
- **Project Templates**: Pre-configured setups for Python, JavaScript, C++, and web projects
- **Build Configurations**: Multiple environment setups (development, production, testing)
- **Git Integration**: Built-in version control with visual status indicators
- **Package Management**: Automatic dependency handling for Python (pip) and Node.js (npm)
- **Project Settings**: Customizable per-project configurations
- **Recent Projects**: Quick access to recently opened projects

## 📁 **ATLES Project Files**

### **Project Structure**
```
MyProject/
├── .atles/
│   ├── project.json          # Main project configuration
│   ├── build_configs.json    # Build configurations
│   └── cache/                # Build cache and temporary files
├── src/                      # Source code directory
├── tests/                    # Test files
├── docs/                     # Documentation
├── main.py                   # Main entry point
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── .gitignore               # Git ignore rules
```

### **Project Configuration (project.json)**
```json
{
  "config": {
    "name": "My ATLES Project",
    "type": "python",
    "version": "1.0.0",
    "created": "2024-01-15T10:30:00",
    "description": "A sample Python project",
    "author": "Developer",
    "main_file": "main.py",
    "source_dirs": ["."],
    "build_dir": "build",
    "dependencies": {},
    "scripts": {
      "start": "python main.py",
      "test": "python -m pytest tests/",
      "lint": "flake8 .",
      "format": "black ."
    },
    "settings": {
      "python_version": "3.8+",
      "encoding": "utf-8",
      "line_endings": "auto"
    }
  },
  "build_configs": {
    "development": { ... },
    "production": { ... },
    "test": { ... }
  },
  "last_modified": "2024-01-15T15:45:00"
}
```

## 🆕 **Creating Projects**

### **Using the Project Manager**

1. **Open Project Manager**: `File` → `Project` → `New Project...` or `Ctrl+Shift+N`

2. **Choose Project Type**:
   - **Python Application**: Full Python project with virtual environment
   - **JavaScript/Node.js**: Node.js project with package.json
   - **Web Project**: HTML/CSS/JS with development server
   - **C++ Application**: C++ project with build system
   - **General Project**: Basic project structure

3. **Configure Project**:
   - **Name**: Project name (will be the folder name)
   - **Location**: Where to create the project
   - **Description**: Optional project description
   - **Git Repository**: Initialize Git repository
   - **Virtual Environment**: Create Python venv (Python projects only)

### **Project Templates**

#### **Python Project Template**
```
MyPythonApp/
├── .atles/
├── src/
├── tests/
├── docs/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── venv/              # If virtual environment created
```

**Default Scripts**:
- `start`: `python main.py`
- `test`: `python -m pytest tests/`
- `lint`: `flake8 .`
- `format`: `black .`
- `install`: `pip install -r requirements.txt`

#### **JavaScript Project Template**
```
MyJSApp/
├── .atles/
├── src/
├── tests/
├── docs/
├── index.js
├── package.json
├── README.md
├── .gitignore
└── node_modules/      # After npm install
```

**Default Scripts**:
- `start`: `node index.js`
- `dev`: `npm run dev`
- `build`: `npm run build`
- `test`: `npm test`
- `install`: `npm install`

#### **Web Project Template**
```
MyWebApp/
├── .atles/
├── src/
│   ├── css/
│   ├── js/
│   └── images/
├── index.html
├── style.css
├── script.js
├── README.md
└── .gitignore
```

**Default Scripts**:
- `serve`: `python -m http.server 8000`
- `build`: `npm run build`
- `dev`: `npm run dev`

## ⚙️ **Project Settings**

### **Accessing Settings**
- **Project-specific**: Stored in `.atles/project.json`
- **Global settings**: Stored in `atles_settings.json`
- **Priority**: Project settings override global settings

### **Configuration Options**

#### **General Settings**
```json
{
  "name": "Project Name",
  "type": "python|javascript|cpp|web|general",
  "version": "1.0.0",
  "description": "Project description",
  "author": "Developer Name",
  "main_file": "main.py",
  "source_dirs": ["src", "lib"],
  "build_dir": "build"
}
```

#### **Development Settings**
```json
{
  "settings": {
    "python_version": "3.8+",
    "encoding": "utf-8",
    "line_endings": "auto|lf|crlf",
    "tab_size": 4,
    "use_spaces": true,
    "auto_save": true,
    "format_on_save": true
  }
}
```

#### **Custom Scripts**
```json
{
  "scripts": {
    "start": "python main.py",
    "dev": "python main.py --debug",
    "test": "python -m pytest tests/ -v",
    "coverage": "python -m pytest --cov=src tests/",
    "docs": "sphinx-build docs/ docs/_build/",
    "deploy": "python setup.py sdist bdist_wheel"
  }
}
```

## 🔧 **Build Configurations**

### **Managing Build Configurations**
Access via: `Build` → `Build Configurations...`

### **Configuration Structure**
```json
{
  "development": {
    "name": "Development",
    "command": "python main.py",
    "args": ["--debug", "--verbose"],
    "working_dir": ".",
    "env": {
      "PYTHONPATH": ".",
      "DEBUG": "1",
      "LOG_LEVEL": "DEBUG"
    }
  },
  "production": {
    "name": "Production",
    "command": "python main.py",
    "args": ["--optimize"],
    "working_dir": ".",
    "env": {
      "PYTHONPATH": ".",
      "DEBUG": "0",
      "LOG_LEVEL": "INFO"
    }
  },
  "test": {
    "name": "Run Tests",
    "command": "python -m pytest",
    "args": ["tests/", "-v", "--cov=src"],
    "working_dir": ".",
    "env": {
      "PYTHONPATH": ".",
      "TESTING": "1"
    }
  }
}
```

### **Running Configurations**
- **Run (F5)**: Execute development configuration
- **Build (Ctrl+F5)**: Execute production configuration
- **Custom**: Select specific configuration from Build menu

### **Configuration Examples**

#### **Python Web Server**
```json
{
  "web_server": {
    "name": "Development Server",
    "command": "python -m flask run",
    "args": ["--debug", "--port=5000"],
    "working_dir": ".",
    "env": {
      "FLASK_APP": "app.py",
      "FLASK_ENV": "development"
    }
  }
}
```

#### **Node.js Application**
```json
{
  "dev_server": {
    "name": "Development Server",
    "command": "npm run dev",
    "args": [],
    "working_dir": ".",
    "env": {
      "NODE_ENV": "development",
      "PORT": "3000"
    }
  }
}
```

#### **C++ Compilation**
```json
{
  "debug_build": {
    "name": "Debug Build",
    "command": "g++",
    "args": ["-g", "-Wall", "-std=c++17", "main.cpp", "-o", "main_debug"],
    "working_dir": ".",
    "env": {
      "CXX": "g++",
      "CXXFLAGS": "-g -Wall"
    }
  }
}
```

## 🔄 **Git Integration**

### **Git Features**
- **Status Indicators**: Visual file status in explorer
- **Basic Operations**: Commit, push, pull, status
- **Repository Detection**: Automatic Git repository detection
- **Branch Information**: Current branch display in status bar

### **Git Operations**

#### **Viewing Status**
- **Menu**: `Tools` → `Git` → `Status`
- **Terminal Output**: Shows modified, added, deleted files
- **File Explorer**: Visual indicators (M, A, D, ??)

#### **Committing Changes**
1. **Menu**: `Tools` → `Git` → `Commit...`
2. **Enter commit message** in dialog
3. **Automatic staging**: All changes are staged automatically
4. **Commit**: Creates commit with message

#### **Push/Pull Operations**
- **Push**: `Tools` → `Git` → `Push`
- **Pull**: `Tools` → `Git` → `Pull`
- **Status feedback**: Success/failure messages in status bar

### **Git Status Indicators**
| Indicator | Meaning |
|-----------|---------|
| `M` | Modified file |
| `A` | Added file |
| `D` | Deleted file |
| `??` | Untracked file |
| `R` | Renamed file |
| `C` | Copied file |

### **Git Workflow Example**
```bash
# 1. Make changes to files
# 2. View status
Tools → Git → Status

# 3. Commit changes
Tools → Git → Commit...
# Enter: "Add new feature X"

# 4. Push to remote
Tools → Git → Push
```

## 📦 **Package Management**

### **Supported Package Managers**
- **Python**: pip (with virtual environment support)
- **Node.js**: npm
- **Future**: yarn, poetry, conda

### **Python Package Management**

#### **Installing Dependencies**
1. **Menu**: `Tools` → `Package Manager` → `Install Dependencies`
2. **Requirements file**: Reads from `requirements.txt`
3. **Virtual environment**: Uses project venv if available
4. **Terminal output**: Shows installation progress

#### **Virtual Environment Support**
```bash
# ATLES automatically detects and uses:
MyProject/venv/Scripts/pip.exe    # Windows
MyProject/venv/bin/pip            # Linux/Mac

# Falls back to system pip if no venv
```

#### **Updating Dependencies**
- **Menu**: `Tools` → `Package Manager` → `Update Dependencies`
- **Shows outdated packages**: Lists packages that can be updated
- **Manual updates**: User can choose which packages to update

### **Node.js Package Management**

#### **Installing Dependencies**
1. **Menu**: `Tools` → `Package Manager` → `Install Dependencies`
2. **Package file**: Reads from `package.json`
3. **Command**: Executes `npm install`
4. **Dependencies**: Installs both dependencies and devDependencies

#### **Updating Dependencies**
- **Menu**: `Tools` → `Package Manager` → `Update Dependencies`
- **Command**: Executes `npm update`
- **Version checking**: Shows outdated packages

### **Package Management Examples**

#### **Python Requirements.txt**
```txt
# Core dependencies
requests>=2.25.0
flask>=2.0.0
sqlalchemy>=1.4.0

# Development dependencies
pytest>=6.0.0
black>=21.0.0
flake8>=3.9.0

# Optional dependencies
redis>=3.5.0  # For caching
celery>=5.0.0  # For background tasks
```

#### **Node.js Package.json**
```json
{
  "name": "my-project",
  "version": "1.0.0",
  "dependencies": {
    "express": "^4.18.0",
    "mongoose": "^6.0.0",
    "lodash": "^4.17.0"
  },
  "devDependencies": {
    "jest": "^28.0.0",
    "nodemon": "^2.0.0",
    "eslint": "^8.0.0"
  },
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "test": "jest"
  }
}
```

## 📋 **Project Templates**

### **Creating Custom Templates**
You can create custom project templates by:

1. **Create template project** with desired structure
2. **Add to templates directory**: `~/.atles/templates/`
3. **Template configuration**: Create `template.json`

#### **Template Configuration**
```json
{
  "name": "FastAPI Project",
  "description": "FastAPI web application with database",
  "type": "python",
  "files": [
    {
      "path": "main.py",
      "content": "# FastAPI application\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef read_root():\n    return {'Hello': 'World'}"
    },
    {
      "path": "requirements.txt",
      "content": "fastapi>=0.68.0\nuvicorn>=0.15.0\nsqlalchemy>=1.4.0"
    }
  ],
  "directories": ["app", "tests", "docs"],
  "scripts": {
    "start": "uvicorn main:app --reload",
    "test": "pytest tests/",
    "docs": "mkdocs serve"
  }
}
```

### **Available Templates**

#### **Python Templates**
- **Basic Python**: Simple Python application
- **Flask Web App**: Web application with Flask
- **FastAPI**: Modern API with FastAPI
- **Data Science**: Jupyter notebooks and data analysis
- **CLI Tool**: Command-line application with Click

#### **JavaScript Templates**
- **Node.js API**: Express.js REST API
- **React App**: React frontend application
- **Vue.js App**: Vue.js frontend application
- **Electron App**: Desktop application with Electron

#### **Web Templates**
- **Static Website**: HTML/CSS/JS website
- **Bootstrap Site**: Responsive website with Bootstrap
- **Progressive Web App**: PWA with service workers

## 🎯 **Best Practices**

### **Project Organization**
1. **Use meaningful names**: Clear project and file names
2. **Follow conventions**: Language-specific directory structures
3. **Document everything**: README, code comments, API docs
4. **Version control**: Always use Git for projects
5. **Virtual environments**: Isolate dependencies

### **Build Configurations**
1. **Environment separation**: Different configs for dev/prod/test
2. **Environment variables**: Use env vars for configuration
3. **Consistent naming**: Use standard names (development, production, test)
4. **Documentation**: Document what each configuration does

### **Git Workflow**
1. **Frequent commits**: Small, focused commits
2. **Descriptive messages**: Clear commit messages
3. **Branch strategy**: Use branches for features
4. **Regular pushes**: Don't lose work

### **Dependency Management**
1. **Pin versions**: Specify exact versions in production
2. **Regular updates**: Keep dependencies current
3. **Security scanning**: Check for vulnerabilities
4. **Minimal dependencies**: Only include what you need

### **Project Structure Examples**

#### **Python Project**
```
MyPythonProject/
├── .atles/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   ├── views/
│   └── utils/
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── fixtures/
├── docs/
│   ├── README.md
│   └── api.md
├── scripts/
│   ├── setup.py
│   └── deploy.py
├── requirements.txt
├── requirements-dev.txt
├── .gitignore
└── README.md
```

#### **Node.js Project**
```
MyNodeProject/
├── .atles/
├── src/
│   ├── index.js
│   ├── routes/
│   ├── models/
│   ├── middleware/
│   └── utils/
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
├── public/
│   ├── css/
│   ├── js/
│   └── images/
├── package.json
├── package-lock.json
├── .gitignore
└── README.md
```

## 🚀 **Advanced Features**

### **Project Workspace**
- **Multi-project support**: Open multiple projects simultaneously
- **Project switching**: Quick switching between projects
- **Shared settings**: Common settings across projects

### **Build Automation**
- **Pre/post build scripts**: Custom scripts before/after builds
- **Build notifications**: Success/failure notifications
- **Build history**: Track build results and timing

### **Integration Points**
- **External tools**: Integration with external build tools
- **CI/CD**: Export configurations for CI/CD systems
- **Docker**: Container-based development environments

---

**This comprehensive project management system makes ATLES Code Studio a powerful development environment that can handle projects of any size and complexity!** 🎉
