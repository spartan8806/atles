# ATLES Phase 1: Basic Chat Interface

## 🚀 Overview

This is Phase 1 of the ATLES UI - a Basic Chat Interface built with Streamlit that allows users to chat with ATLES AI agents through a clean, modern web interface.

## ✨ Features

### Core Requirements ✅
- **Simple Chat Interface**: Users can chat with the ATLES brain
- **Agent Selection & Control**: Choose between Reasoning, Analysis, and Creative agents
- **Basic Safety Monitoring**: Show safety status and any blocked requests

### Technical Specs ✅
- **Framework**: Streamlit (Python)
- **Integration**: Connects to existing `atles.brain.ATLESBrain`
- **Features**: Chat input/output, agent dropdown, safety status display
- **Design**: Clean, modern interface that matches ATLES branding

### Key Functions ✅
- `start_conversation()` - Initialize chat session
- `chat()` - Send/receive messages with safety checks
- `process_with_agents()` - Route to selected agent
- `get_safety_status()` - Display safety system status

## 🏗️ Architecture

### UI Layout
- **Header**: ATLES logo and safety status
- **Sidebar**: Agent selection dropdown and controls
- **Main Area**: Chat area with message history and input field
- **Right Panel**: Session info and system status

### Safety System Integration
- Real-time safety monitoring
- Input and response validation
- Safety status display with color coding
- "Motherly Instinct" AI safety features

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### 1. Install Dependencies

```bash
# Install Streamlit and core dependencies
pip install -r streamlit_requirements.txt

# Or install manually
pip install streamlit streamlit-option-menu
```

### 2. ATLES Integration

#### Option A: Full ATLES Installation (Recommended)
```bash
# Install ATLES package
pip install -e .

# Run the full version
streamlit run streamlit_chat.py
```

#### Option B: Demo Mode (No ATLES Required)
```bash
# Run the simplified version (works without ATLES)
streamlit run streamlit_chat_simple.py
```

### 3. Launch the Application

```bash
# Navigate to the project directory
cd /path/to/atles

# Launch Streamlit
streamlit run streamlit_chat_simple.py
```

The application will open in your default web browser at `http://localhost:8501`

## 🎯 Usage Guide

### Getting Started

1. **Initialize ATLES Brain**
   - Click the "🚀 Initialize ATLES Brain" button in the sidebar
   - Wait for initialization to complete

2. **Start a Conversation**
   - Click "💬 Start New Conversation" to create a new chat session
   - A unique session ID will be generated

3. **Select an Agent**
   - Choose from the dropdown in the sidebar:
     - 🧠 **Reasoning Agent**: Logical analysis and problem-solving
     - 📊 **Analysis Agent**: Data analysis and pattern recognition
     - 🎨 **Creative Agent**: Idea generation and creative tasks

4. **Start Chatting**
   - Type your message in the input field
   - Click "Send" or press Enter
   - View responses and safety status

### Safety Monitoring

- **Safety Status**: Always visible in the sidebar
- **Real-time Checks**: Input and response validation
- **Safety Indicators**: Color-coded status (Safe/Moderate/Dangerous/Blocked)
- **Statistics**: View safety metrics and blocked requests

### Session Management

- **Session Info**: View current session details
- **Quick Actions**: Refresh session, clear history
- **System Status**: Monitor ATLES brain and safety system

## 🔧 Configuration

### Environment Variables

```bash
# Optional: Set custom models directory
export ATLES_MODELS_DIR="/path/to/models"

# Optional: Set logging level
export ATLES_LOG_LEVEL="INFO"
```

### Customization

The interface can be customized by modifying:

- **Colors**: Update CSS variables in the custom styles section
- **Agents**: Add new agent types in the `agent_options` dictionary
- **Safety Features**: Modify safety display functions
- **UI Layout**: Adjust column widths and component placement

## 🧪 Testing

### Demo Mode Testing

The simplified version (`streamlit_chat_simple.py`) includes a demo mode that:

- Simulates ATLES responses without requiring the full package
- Demonstrates all UI features and functionality
- Provides realistic chat interactions for testing

### Full Mode Testing

To test with the complete ATLES system:

1. Ensure all ATLES dependencies are installed
2. Run `streamlit run streamlit_chat.py`
3. Test agent selection and safety features
4. Verify integration with ATLES brain

## 🐛 Troubleshooting

### Common Issues

#### Import Errors
```
ModuleNotFoundError: No module named 'atles'
```
**Solution**: Install ATLES package or use demo mode

#### Streamlit Not Found
```
streamlit: command not found
```
**Solution**: Install Streamlit with `pip install streamlit`

#### Port Already in Use
```
Port 8501 is already in use
```
**Solution**: Use different port: `streamlit run app.py --server.port 8502`

#### ATLES Brain Initialization Failed
```
Failed to initialize ATLES Brain
```
**Solution**: Check ATLES installation or use demo mode

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📁 File Structure

```
atles/
├── streamlit_chat.py              # Full ATLES integration
├── streamlit_chat_simple.py       # Simplified demo version
├── streamlit_requirements.txt     # Dependencies
├── README_Streamlit_Chat.md       # This file
└── atles/                         # ATLES package
    ├── brain.py                   # ATLES brain implementation
    ├── agents.py                  # Agent system
    └── safety_system.py          # Safety features
```

## 🚀 Next Steps

### Phase 1 Enhancements
- [ ] Add message timestamps
- [ ] Implement conversation export
- [ ] Add user authentication
- [ ] Enhanced error handling

### Future Phases
- **Phase 2**: Advanced UI features and customization
- **Phase 3**: Multi-user support and collaboration
- **Phase 4**: Advanced agent orchestration
- **Phase 5**: Real-time streaming and notifications

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of ATLES and follows the same licensing terms.

## 🆘 Support

For issues and questions:

1. Check the troubleshooting section above
2. Review ATLES documentation
3. Open an issue in the repository
4. Contact the development team

---

**ATLES Phase 1 Chat Interface** - Built with ❤️ and Streamlit
