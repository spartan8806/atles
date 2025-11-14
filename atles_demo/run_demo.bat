@echo off
echo ========================================
echo 🧠 ATLES Demo Server - Portfolio Demo
echo ========================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

:: Install requirements
echo 📦 Installing requirements...
pip install flask flask-cors
if errorlevel 1 (
    echo ❌ Failed to install requirements
    echo Please run: pip install flask flask-cors
    pause
    exit /b 1
)

echo ✅ Requirements installed
echo.

:: Start the demo server
echo 🚀 Starting ATLES Demo Server...
echo.
echo 📱 User Interface: http://localhost:5000
echo 🔧 Admin Panel: http://localhost:5000/admin
echo 🔑 Demo Codes: DEMO001, DEMO002, DEMO003
echo 🔑 Admin Codes: ADMIN123, MASTER456
echo.
echo Press Ctrl+C to stop the server
echo.

python atles_demo_server.py

pause