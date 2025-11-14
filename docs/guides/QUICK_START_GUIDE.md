# 🚀 ATLES Quick Start Guide

> **Get ATLES v0.5 + Phase 1 UI running in under 5 minutes!**

## 🎯 **What You'll Get**

- **🤖 AI Agents**: Chat with Reasoning, Analysis, and Creative AI agents
- **🔒 AI Safety**: Built-in "Motherly Instinct" safety system
- **💬 Professional UI**: Beautiful Streamlit chat interface
- **🛡️ Real-time Monitoring**: Live safety status and system health
- **💾 Persistent Memory**: Conversations that remember context
- **📄 PDF Reading**: Extract and analyze text from PDF documents
- **🧩 Smart Dependencies**: Graceful handling of optional packages

---

## ⚡ **Super Quick Start (Recommended)**

### **Windows Users - One Click!**
```bash
# Just double-click this file:
run_chat.bat
```

### **All Platforms - Smart Auto-Detection**
```bash
python run_chat.py
```

**That's it!** The smart startup script will:
- ✅ Detect your system setup
- ✅ Install missing dependencies
- ✅ Choose the best mode (full ATLES or demo)
- ✅ Launch the beautiful chat interface

---

## 🔧 **Manual Setup (If You Prefer)**

### **Step 1: Install Dependencies**
```bash
pip install -r streamlit_requirements.txt
```

### **Step 2: Choose Your Mode**

#### **Option A: Full ATLES Integration (Recommended)**
```bash
pip install -r requirements.txt
streamlit run streamlit_chat.py
```

#### **Option B: Demo Mode (Works Without Full ATLES)**
```bash
streamlit run streamlit_chat_simple.py
```

---

## 🎮 **Using ATLES - Your First Chat**

### **1. Launch the Interface**
- Run one of the startup commands above
- Your browser will open to the ATLES interface
- You'll see the beautiful dark theme with ATLES branding

### **2. Initialize the Brain**
- Click **"Initialize Brain"** button (left panel)
- Wait for the green "Brain: Active" status
- This starts the AI system

### **3. Start Chatting**
- Click **"Start Chat"** button
- Select your preferred AI agent:
  - **🤖 Reasoning**: Complex problem-solving
  - **📊 Analysis**: Data analysis and patterns
  - **🎨 Creative**: Idea generation and creativity
- Type your message in the chat box
- Press Enter or click Send

### **4. Monitor Safety & Status**
- **Left Panel**: Safety system status and controls
- **Right Panel**: Session details and system health
- **Real-time**: Live safety monitoring with color indicators

---

## 🎨 **Interface Tour**

### **Left Panel - Controls & Safety**
- **🚀 Initialize Brain**: Start the AI system
- **💬 Start Chat**: Begin a new conversation
- **🤖 AI Agent**: Choose your AI companion
- **🔄 Refresh Safety**: Update safety status
- **🔒 Safety Status**: Real-time safety monitoring

### **Center Panel - Chat Area**
- **💬 Chat History**: Your conversation with ATLES
- **📝 Input Field**: Type your messages here
- **📤 Send Button**: Send your message
- **⏰ Timestamps**: When each message was sent

### **Right Panel - Session & Status**
- **📊 Session**: Active conversation details
- **⚡ Actions**: Refresh, clear chat, etc.
- **🔧 Status**: System health and brain status

---

## 🛡️ **AI Safety Features**

### **What's Protected**
- **Physical Harm**: Violence, weapons, dangerous activities
- **Emotional Harm**: Self-harm, manipulation, bullying
- **Financial Harm**: Scams, fraud, theft
- **Privacy Violation**: Hacking, stalking, data theft
- **Illegal Activities**: Crimes, illegal substances, fraud

### **How It Works**
- **Real-time Monitoring**: Every message is safety-checked
- **Gentle Redirection**: Helpful alternatives instead of blocking
- **Professional Resources**: Direct access to appropriate help
- **Visual Indicators**: Color-coded safety status

---

## � **Optional Features**

### **PDF Reading Capability**
To enable PDF reading functionality:
```bash
# Install required packages
pip install pdfplumber requests

# Or use the provided script (Windows)
install_pdf_support.bat
```

#### **Using PDF Reading**
Once installed, you can read PDFs from URLs:
```
User: Can you read this research paper? https://arxiv.org/pdf/2212.08073.pdf
ATLES: FUNCTION_CALL:read_pdf:{"url": "https://arxiv.org/pdf/2212.08073.pdf"}
```

### **Debug Mode**
To enable debug mode for function calls:
```bash
# Show current status
toggle_debug.bat status

# Enable function call debugging
toggle_debug.bat function
```

---

## �🔍 **Troubleshooting**

### **Common Issues & Solutions**

#### **"ModuleNotFoundError: No module named 'atles'"**
- **Solution**: Use demo mode: `streamlit run streamlit_chat_simple.py`
- **Or**: Install full ATLES: `pip install -r requirements.txt`

#### **"Streamlit not found"**
- **Solution**: Install Streamlit: `pip install streamlit`

#### **"Port already in use"**
- **Solution**: Change port: `streamlit run streamlit_chat.py --server.port 8502`

#### **"Browser doesn't open automatically"**
- **Solution**: Manually open: `http://localhost:8501`

### **Getting Help**
- Check the console output for error messages
- Verify all dependencies are installed
- Try demo mode first to test the interface
- Check the full documentation for advanced setup

---

## 🚀 **Advanced Usage**

### **Customizing Your Experience**
- **Agent Selection**: Switch between agents mid-conversation
- **Session Management**: Start new conversations or continue existing ones
- **Safety Monitoring**: Keep an eye on system safety status
- **Performance**: Monitor system health and responsiveness

### **Integration Options**
- **Full ATLES**: Complete AI agent system with safety
- **Demo Mode**: Test the interface without full integration
- **Custom Setup**: Modify for your specific needs

---

## 📚 **Next Steps**

### **Learn More**
- **Full Documentation**: Check `ATLES_Project_Summary.md`
- **API Reference**: Explore the technical documentation
- **Examples**: Try different types of conversations
- **Safety Features**: Test the AI safety system

### **What's Coming Next**
- **Phase 2**: Full dashboard with advanced controls
- **Phase 3**: Real-time monitoring and analytics
- **v0.6**: Next major version planning

---

## 🎉 **Congratulations!**

You're now running **ATLES v0.5 + Phase 1 UI** - a state-of-the-art AI system with:

- ✅ **Professional Interface**: Beautiful, responsive Streamlit UI
- ✅ **AI Agents**: Three specialized AI companions
- ✅ **Safety First**: Comprehensive harm prevention
- ✅ **Real-time Monitoring**: Live system status
- ✅ **Production Ready**: Professional-grade implementation

**Start chatting with your AI agents and explore the future of AI safety!** 🚀

---

## 📞 **Need Help?**

- **Documentation**: Check the project files
- **Issues**: Look for error messages in the console
- **Community**: Join ATLES discussions
- **Safety**: Use the built-in safety reporting system

**Happy AI chatting!** 🤖💬
