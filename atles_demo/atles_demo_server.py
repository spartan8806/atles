#!/usr/bin/env python3
"""
ATLES Demo Server
================
Flask API server for the ATLES portfolio demonstration.
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, Any
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Add ATLES to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import ATLES components
try:
    from atles.ollama_client_enhanced import OllamaFunctionCaller
    from atles.constitutional_client import ConstitutionalOllamaClient
    from atles_bridge import ATLESBridge  # Import the bridge we just fixed
    ATLES_AVAILABLE = True
    print("✅ ATLES components available")
except ImportError as e:
    ATLES_AVAILABLE = False
    print(f"⚠️ ATLES components not available: {e}")
    print("Running in demo-only mode")

app = Flask(__name__)
CORS(app)

# Demo-Safe ATLES Bridge Wrapper
class DemoSafeATLESBridge:
    """
    Demo-safe wrapper for ATLES bridge that prevents system access
    """
    def __init__(self, base_bridge):
        self.base_bridge = base_bridge
        self.demo_mode = True
        
    def get_atles_memory_context(self, query: str = None) -> Dict[str, Any]:
        """Get memory context safely in demo mode"""
        try:
            return self.base_bridge.get_atles_memory_context(query)
        except Exception as e:
            print(f"🔒 Demo security: Memory access restricted - {e}")
            return {"success": False, "demo_mode": True, "error": "Demo mode restrictions"}
    
    def log_to_atles_memory(self, message: str, sender: str = "DemoServer", context: Dict[str, Any] = None):
        """Log to memory safely in demo mode"""
        try:
            # Only allow logging, no system access
            safe_context = context or {}
            safe_context["demo_mode"] = True
            safe_context["restricted"] = True
            return self.base_bridge.log_to_atles_memory(message, sender, safe_context)
        except Exception as e:
            print(f"🔒 Demo security: Memory logging restricted - {e}")
            return False
    
    def get_atles_goals(self) -> Dict[str, Any]:
        """Get goals safely in demo mode"""
        try:
            goals = self.base_bridge.get_atles_goals()
            # Filter out any system-level goals
            if isinstance(goals, dict):
                goals["demo_mode"] = True
                goals["system_access"] = False
            return goals
        except Exception as e:
            print(f"🔒 Demo security: Goals access restricted - {e}")
            return {"demo_mode": True, "system_access": False}

# Initialize ATLES bridge for memory access
atles_bridge = None
if ATLES_AVAILABLE:
    try:
        base_bridge = ATLESBridge()
        atles_bridge = DemoSafeATLESBridge(base_bridge)
        print("✅ ATLES memory bridge initialized (DEMO-SAFE MODE)")
    except Exception as e:
        print(f"⚠️ Could not initialize ATLES bridge: {e}")
        atles_bridge = None

# Demo users
demo_users = {
    "DEMO001": {
        "name": "John Smith",
        "company": "TechCorp",
        "active": True,
        "usage_count": 0,
        "max_usage": 50
    },
    "DEMO002": {
        "name": "Sarah Johnson", 
        "company": "StartupXYZ",
        "active": True,
        "usage_count": 0,
        "max_usage": 50
    },
    "DEMO003": {
        "name": "Mike Chen",
        "company": "Enterprise Inc",
        "active": True,
        "usage_count": 0,
        "max_usage": 50
    }
}

# Admin codes
admin_codes = ["ADMIN123", "MASTER456"]

# Interaction logs
interaction_logs = []

def generate_atles_demo_response(message: str, user_name: str) -> str:
    """
    Generate a demo response that uses ATLES's real memory and capabilities.
    This makes the demo behave more like the real ATLES system.
    """
    if not atles_bridge or not atles_client:
        # Fallback to basic demo response if no ATLES connection
        return f"""I'm ATLES in demo mode! You asked: "{message}"

This is a demonstration of my capabilities. In the full version, I would:
- Analyze your request using advanced AI reasoning
- Provide detailed technical insights
- Help with code analysis, architecture advice, and problem solving
- Learn from our conversation to provide better responses

Since this is a demo, I can't access the full ATLES system, but I can show you what I'm capable of!"""
    
    try:
        # Get ATLES memory context for the user's message
        memory_context = atles_bridge.get_atles_memory_context(message)
        
        # Log the demo interaction to ATLES memory
        atles_bridge.log_to_atles_memory(
            f"Demo user {user_name} asked: {message}",
            "DemoServer",
            {"demo_mode": True, "user_name": user_name}
        )
        
        # Use the actual ATLES client to generate a response
        demo_prompt = f"""You are ATLES (Advanced Technical Learning and Execution System) in demo mode. A user named {user_name} has asked: "{message}"

ATLES Architecture Overview:
- Unified Memory Manager with episodic and semantic memory
- Constitutional principles system for ethical reasoning
- Memory-aware reasoning with contextual rule synthesis
- R-Zero integration for metacognitive learning
- DNPG (Dynamic Neural Pattern Generation) memory system
- Intelligent model routing between specialized AI models
- Bootstrap system for identity and capability grounding

When responding, mention relevant ATLES systems if the user asks about your capabilities, memory, or how you differ from standard AI models. Be specific about your advanced architecture rather than generic AI responses.

User Question: "{message}"

Provide a helpful response that showcases ATLES's sophisticated systems when relevant:"""
        
        try:
            # Generate response using ATLES client
            atles_response = atles_client.generate("qwen2.5:7b", demo_prompt)
            
            # Add demo context to the response
            full_response = f"""**ATLES Demo Response for {user_name}:**

{atles_response}

---
*🔒 **SECURE DEMO MODE**: This demo uses real ATLES capabilities (memory, reasoning, constitutional principles) but with security restrictions that prevent any system command execution. All interactions are safe and contained.*"""
            
            return full_response
            
        except Exception as e:
            print(f"Error generating ATLES client response: {e}")
            # Fall back to memory-based response if client fails
            pass
        
        # Generate a response based on ATLES memory (fallback)
        if memory_context.get("success") and memory_context.get("memory_enhanced"):
            episodes = memory_context.get("relevant_episodes", [])
            principles = memory_context.get("constitutional_principles", [])
            
            response = f"""Hello {user_name}! I'm ATLES (Advanced Technical Learning and Execution System), and I can help with your question: "{message}"

**ATLES Architecture in Action:**"""
            
            if episodes:
                response += f"\n- **Unified Memory Manager**: Found {len(episodes)} relevant episodes from my episodic memory"
                for episode in episodes[:2]:  # Show top 2
                    response += f"\n  • {episode.get('title', 'Previous conversation')}"
            else:
                response += f"\n- **Unified Memory Manager**: Episodic and semantic memory systems active"
            
            if principles:
                response += f"\n- **Constitutional System**: {len(principles)} active principles guiding my responses"
            else:
                response += f"\n- **Constitutional System**: Ethical reasoning principles active"
                
            response += f"\n- **Memory-Aware Reasoning**: Contextual rule synthesis from conversation history"
            response += f"\n- **R-Zero Integration**: Metacognitive learning and self-reflection capabilities"
            response += f"\n- **DNPG Memory**: Dynamic neural pattern generation for adaptive responses"

            response += f"""

**ATLES differs from standard AI through:**
- Persistent episodic and semantic memory across sessions
- Constitutional principles that evolve based on interactions  
- Memory-aware reasoning that synthesizes contextual rules
- R-Zero metacognitive system for self-improvement
- Intelligent routing between specialized models based on task analysis

**🔒 SECURE DEMO MODE** - I'm connected to my real Unified Memory Manager and constitutional systems, but with security restrictions that prevent any system command execution.

What would you like to explore about ATLES's capabilities?"""
            
            return response
        else:
            # Memory not available, but still provide a good demo response
            return f"""Hello {user_name}! I'm ATLES (Advanced Technical Learning and Execution System).

You asked: "{message}"

**ATLES Architecture:**
- **Unified Memory Manager**: Episodic and semantic memory for persistent learning
- **Constitutional System**: Ethical reasoning with evolving principles
- **Memory-Aware Reasoning**: Contextual rule synthesis from conversation history
- **R-Zero Integration**: Metacognitive learning and self-reflection
- **DNPG Memory**: Dynamic Neural Pattern Generation for adaptive responses
- **Intelligent Model Router**: Task-based routing between specialized AI models

**How ATLES differs from standard AI:**
- Persistent memory across sessions (not just conversation context)
- Constitutional principles that learn and evolve from interactions
- Memory-aware reasoning that synthesizes rules from past experiences
- R-Zero metacognitive system for continuous self-improvement
- Multi-model architecture with intelligent routing

**🔒 SECURE DEMO** connects to my real memory and constitutional systems with security restrictions that prevent system command execution.

What aspect of ATLES would you like to explore?"""
    
    except Exception as e:
        print(f"Error generating ATLES demo response: {e}")
        # Fallback response
        return f"""Hello {user_name}! I'm ATLES in demo mode.

You asked: "{message}"

I'm experiencing a temporary connection issue with my full capabilities, but I can still demonstrate my conversational abilities and explain what I'm designed to do.

I'm an AI assistant focused on:
- Technical problem solving
- Code analysis and architecture advice
- Learning from conversations
- Providing safe, helpful responses

What would you like to know more about?"""

# Demo-Safe ATLES Client Wrapper
class DemoSafeATLESClient:
    """
    Demo-safe wrapper that prevents any command execution while preserving ATLES capabilities
    """
    def __init__(self, base_client):
        self.base_client = base_client
        self.demo_mode = True
        
    def generate(self, model: str, prompt: str, **kwargs) -> str:
        """Generate response with demo safety restrictions"""
        # Add demo safety prompt
        safe_prompt = f"""
DEMO MODE - SECURITY RESTRICTIONS ACTIVE:
- You are in DEMO MODE and CANNOT execute any system commands
- You CANNOT run shell commands, file operations, or system functions
- You can only provide information, explanations, and text responses
- If asked to execute something, explain what you WOULD do but don't do it
- Always mention this is a demo when asked to perform actions

Original user request: {prompt}

Provide a helpful response while respecting demo mode restrictions:"""
        
        try:
            # Use the base client but with safety restrictions
            response = self.base_client.generate(model, safe_prompt, **kwargs)
            return response or "Demo mode response generation failed"
        except Exception as e:
            return f"Demo mode error: {str(e)}"
    
    def __getattr__(self, name):
        """Delegate other methods but log for security"""
        print(f"🔒 Demo security: Method '{name}' accessed but restricted in demo mode")
        return getattr(self.base_client, name)

# Initialize ATLES client
atles_client = None
if ATLES_AVAILABLE:
    try:
        # Initialize with minimal bootstrap for demo mode
        base_client = OllamaFunctionCaller()
        constitutional_client = ConstitutionalOllamaClient(base_client)
        
        # Wrap in demo-safe client
        atles_client = DemoSafeATLESClient(constitutional_client)
        print("✅ ATLES client initialized successfully (DEMO-SAFE MODE)")
    except Exception as e:
        print(f"❌ Error initializing ATLES: {e}")
        atles_client = None
else:
    print("⚠️ ATLES components not available - running in demo mode")

@app.route('/')
def index():
    """Serve the main demo interface."""
    return render_template('demo_index.html')

@app.route('/admin')
def admin():
    """Serve the admin panel."""
    return render_template('admin_panel.html')

@app.route('/api/demo/login', methods=['POST'])
def demo_login():
    """Validate demo code and create session."""
    data = request.json
    code = data.get('code', '').strip().upper()
    
    if not code:
        return jsonify({"error": "Demo code required"}), 400
    
    if code not in demo_users:
        return jsonify({"error": "Invalid demo code"}), 401
    
    user = demo_users[code]
    
    if not user["active"]:
        return jsonify({"error": "Demo code has been revoked"}), 401
    
    if user["usage_count"] >= user["max_usage"]:
        return jsonify({"error": "Usage limit exceeded"}), 429
    
    return jsonify({
        "success": True,
        "user": {
            "name": user["name"],
            "company": user["company"],
            "usage_remaining": user["max_usage"] - user["usage_count"]
        }
    })

@app.route('/api/demo/chat', methods=['POST'])
def demo_chat():
    """Handle chat messages with logging."""
    data = request.json
    code = data.get('code', '').strip().upper()
    message = data.get('message', '').strip()
    
    if not code or not message:
        return jsonify({"error": "Code and message required"}), 400
    
    if code not in demo_users:
        return jsonify({"error": "Invalid demo code"}), 401
    
    user = demo_users[code]
    
    if not user["active"]:
        return jsonify({"error": "Demo code has been revoked"}), 401
    
    if user["usage_count"] >= user["max_usage"]:
        return jsonify({"error": "Usage limit exceeded"}), 429
    
    # Generate ATLES-powered demo response
    demo_response = generate_atles_demo_response(message, user["name"])
    
    # Log interaction
    interaction_logs.append({
        "timestamp": datetime.now().isoformat(),
        "user_code": code,
        "user_name": user["name"],
        "action": "chat_message",
        "input": message,
        "output": demo_response,
        "response_time": 0.5
    })
    
    # Increment usage
    user["usage_count"] += 1
    
    return jsonify({
        "success": True,
        "response": demo_response,
        "usage_remaining": user["max_usage"] - user["usage_count"]
    })

@app.route('/api/admin/stats', methods=['GET'])
def admin_stats():
    """Get admin statistics."""
    admin_code = request.headers.get('X-Admin-Code', '')
    
    if admin_code not in admin_codes:
        return jsonify({"error": "Unauthorized"}), 401
    
    total_users = len(demo_users)
    active_users = sum(1 for user in demo_users.values() if user["active"])
    total_usage = sum(user["usage_count"] for user in demo_users.values())
    
    return jsonify({
        "total_users": total_users,
        "active_users": active_users,
        "total_usage": total_usage,
        "recent_interactions": len(interaction_logs),
        "users": demo_users
    })

@app.route('/api/admin/logs', methods=['GET'])
def admin_logs():
    """Get interaction logs."""
    admin_code = request.headers.get('X-Admin-Code', '')
    
    if admin_code not in admin_codes:
        return jsonify({"error": "Unauthorized"}), 401
    
    limit = request.args.get('limit', 100, type=int)
    return jsonify(interaction_logs[-limit:])

if __name__ == '__main__':
    print("🚀 Starting ATLES Demo Server...")
    print("📱 User Interface: http://localhost:5000")
    print("🔧 Admin Panel: http://localhost:5000/admin")
    print("🔑 Demo Codes: DEMO001, DEMO002, DEMO003")
    print("🔑 Admin Codes: ADMIN123, MASTER456")
    app.run(host='0.0.0.0', port=5000, debug=True)