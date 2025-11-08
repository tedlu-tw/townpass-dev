#!/bin/bash
# Start TownPass Backend Server

echo "============================================================"
echo "🚴 TownPass Backend API Server"
echo "============================================================"
echo ""

# Check if Python is available
if ! command -v python &> /dev/null; then
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python is not installed"
        exit 1
    fi
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

echo "✓ Using: $($PYTHON_CMD --version)"
echo ""

# Check if we're in the backend directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found"
    echo "Please run this script from the backend directory"
    exit 1
fi

echo "✓ Found app.py"
echo ""

# Check if requirements are installed
echo "Checking dependencies..."
$PYTHON_CMD -c "import flask; import flask_cors; import requests; import dotenv" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Some dependencies are missing"
    echo "Installing requirements..."
    pip install -r requirements.txt
    echo ""
fi

echo "✓ All dependencies installed"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "API keys may not be available"
else
    echo "✓ Found .env file"
fi
echo ""

echo "Starting Flask server..."
echo "============================================================"
echo ""

# Start the server
$PYTHON_CMD app.py
