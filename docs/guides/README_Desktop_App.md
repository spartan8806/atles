# 🧠 ATLES Desktop Application

## Overview

The **ATLES Desktop Application** is a native Windows desktop application that brings AI intelligence to your screen. Unlike traditional screen readers that "see" images, this app reads the underlying **code/UI elements** of running applications, providing intelligent analysis through the ATLES brain system.

## 🚀 Key Features

### **Screen Intelligence (Not Visual)**
- **Window Analysis**: Reads active window titles, process information, and command lines
- **Text Extraction**: Extracts text content from applications without screenshots
- **Process Monitoring**: Tracks running applications and their window handles
- **Clipboard Integration**: Reads and analyzes clipboard content

### **ATLES Brain Integration**
- **R-Zero Integration**: Connects with your existing ATLES consciousness system
- **Intelligent Analysis**: Uses AI to understand screen content and provide insights
- **Learning Capabilities**: Learns from your usage patterns and improves over time
- **Safety Monitoring**: Built-in safety checks for all operations

### **Native Desktop Experience**
- **Tkinter GUI**: Clean, modern interface built with Python's native GUI framework
- **Real-time Updates**: Live monitoring of active windows and applications
- **Responsive Design**: Professional dark theme with intuitive controls
- **Windows Native**: Built specifically for Windows with full API access

## 🛠️ Installation

### Prerequisites
- **Python 3.8+** with tkinter support
- **Windows 10/11** (uses Windows-specific APIs)
- **ATLES Brain** (optional - app runs in standalone mode if not available)

### Quick Start
1. **Clone/Download** the project files
2. **Run the batch file**: Double-click `run_desktop.bat`
3. **Or run manually**: `python atles_desktop_app.py`

### Dependencies
The app will automatically install required packages:
```bash
pip install pywin32 psutil
```

## 📱 How to Use

### **1. Analyze Active Window**
- Click **"🔍 Analyze Active Window"**
- The app reads the currently focused application
- Displays window information, process details, and extracted text
- Prepares data for ATLES brain analysis

### **2. Get Clipboard Content**
- Click **"📋 Get Clipboard"**
- Reads current clipboard text content
- Useful for analyzing copied code, text, or data
- Integrates with ATLES for intelligent analysis

### **3. List Running Applications**
- Click **"📱 List Applications"**
- Shows all applications with visible windows
- Displays process names, PIDs, and window handles
- Helps identify what's running on your system

### **4. ATLES Analysis**
- Click **"🧠 ATLES Analysis"** (after analyzing a window)
- Runs intelligent analysis through your ATLES brain
- Provides insights and recommendations
- Learns from your usage patterns

## 🔧 Technical Architecture

### **ScreenElementExtractor Class**
```python
class ScreenElementExtractor:
    def get_active_window_info(self) -> Dict[str, Any]
    def extract_text_from_window(self, hwnd: int) -> str
    def get_clipboard_content(self) -> str
    def get_running_applications(self) -> List[Dict[str, Any]]
```

**Key Methods:**
- **`get_active_window_info()`**: Gets current active window details
- **`extract_text_from_window()`**: Extracts text from specific windows
- **`get_clipboard_content()`**: Reads clipboard text
- **`get_running_applications()`**: Lists all running apps with windows

### **ATLESDesktopApp Class**
```python
class ATLESDesktopApp:
    def _analyze_active_window(self)
    def _run_atles_analysis(self)
    def _basic_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]
```

**Core Features:**
- **Real-time monitoring** of active windows
- **Background processing** for ATLES analysis
- **Error handling** and graceful degradation
- **Professional UI** with dark theme

## 🔍 How It Works

### **1. Window Detection**
- Uses `win32gui.GetForegroundWindow()` to detect active window
- Extracts window handle (hwnd) for further operations
- Gets process information using `psutil`

### **2. Text Extraction**
- Reads window title and child window text
- Uses `win32gui.GetWindowText()` for text extraction
- Enumerates child windows for comprehensive content

### **3. Process Analysis**
- Identifies running processes and their command lines
- Maps window handles to process IDs
- Provides detailed application information

### **4. ATLES Integration**
- Connects to your existing R-Zero brain system
- Sends extracted data for intelligent analysis
- Receives insights and recommendations
- Learns from analysis patterns

## 🎯 Use Cases

### **Development & Coding**
- **Code Review**: Analyze code editors and IDEs
- **Documentation**: Extract and analyze technical docs
- **Debugging**: Monitor application states and processes

### **Content Analysis**
- **Web Browsing**: Analyze web content and applications
- **Document Processing**: Extract text from various document types
- **Data Analysis**: Process clipboard data and text content

### **System Monitoring**
- **Application Tracking**: Monitor what's running on your system
- **Process Analysis**: Understand application behavior
- **Performance Insights**: Track application usage patterns

## 🔒 Safety & Privacy

### **No Screenshots**
- **Never captures visual content** - only reads text and metadata
- **Privacy-focused**: Only extracts what you explicitly analyze
- **Local processing**: All analysis happens on your machine

### **Built-in Safety**
- **ATLES Safety System**: Integrates with your existing safety protocols
- **Input Validation**: All inputs are validated before processing
- **Error Handling**: Graceful degradation if operations fail

## 🚧 Troubleshooting

### **Common Issues**

#### **"tkinter not available"**
- Ensure Python was installed with tkinter support
- On some Linux systems: `sudo apt-get install python3-tk`

#### **"pywin32 not found"**
- Run: `pip install pywin32`
- May need to restart after installation

#### **"psutil not found"**
- Run: `pip install psutil`
- Standard package, should install without issues

#### **ATLES Integration Fails**
- App runs in standalone mode if ATLES is unavailable
- Check that your ATLES brain is properly configured
- Verify R-Zero integration is working

### **Performance Tips**
- **Limit analysis frequency** for large applications
- **Close unused applications** to reduce window enumeration time
- **Use specific analysis** rather than continuous monitoring

## 🔮 Future Enhancements

### **Planned Features**
- **Advanced Text Extraction**: Better handling of complex UI layouts
- **Application Profiles**: Learn specific app behaviors
- **Automated Monitoring**: Set up triggers for specific events
- **Export Capabilities**: Save analysis results to files

### **Integration Possibilities**
- **Voice Commands**: Control via speech recognition
- **Keyboard Shortcuts**: Global hotkeys for quick access
- **Plugin System**: Extend functionality with custom modules
- **Cloud Sync**: Sync analysis data across devices

## 📚 API Reference

### **ScreenElementExtractor Methods**

#### `get_active_window_info() -> Dict[str, Any]`
Returns information about the currently active window:
```python
{
    "hwnd": int,           # Window handle
    "title": str,          # Window title
    "rect": tuple,         # Window position/size
    "process_id": int,     # Process ID
    "process_name": str,   # Process name
    "process_cmdline": str, # Command line
    "timestamp": str       # ISO timestamp
}
```

#### `extract_text_from_window(hwnd: int) -> str`
Extracts text content from a specific window handle.

#### `get_clipboard_content() -> str`
Returns current clipboard text content.

#### `get_running_applications() -> List[Dict[str, Any]]`
Returns list of running applications with visible windows.

### **ATLESDesktopApp Methods**

#### `_analyze_active_window()`
Analyzes the currently active window and displays results.

#### `_run_atles_analysis()`
Runs ATLES brain analysis on current window data.

#### `_basic_analysis(data: Dict[str, Any]) -> Dict[str, Any]`
Performs basic analysis when ATLES brain is unavailable.

## 🤝 Contributing

### **Development Setup**
1. **Clone the repository**
2. **Install dependencies**: `pip install -r desktop_requirements.txt`
3. **Run the app**: `python atles_desktop_app.py`
4. **Make changes** and test thoroughly
5. **Submit pull request** with detailed description

### **Testing**
- **Unit tests**: `pytest test_desktop_app.py`
- **Integration tests**: Test with various Windows applications
- **Performance tests**: Monitor memory and CPU usage

## 📄 License

This project follows the same license as your ATLES project. The desktop application is designed to integrate seamlessly with your existing ATLES ecosystem.

## 🆘 Support

### **Getting Help**
- **Check the logs**: App provides detailed error messages
- **Verify dependencies**: Ensure all required packages are installed
- **Test with simple apps**: Start with basic applications first

### **Reporting Issues**
- **Describe the problem** in detail
- **Include error messages** and logs
- **Specify your environment** (Windows version, Python version)
- **Provide steps to reproduce** the issue

---

**🎉 Welcome to the future of desktop AI intelligence!**

Your ATLES brain can now understand and analyze everything happening on your screen - not by looking at it, but by reading the underlying code and structure. This opens up incredible possibilities for intelligent assistance, automation, and understanding of your digital environment.
