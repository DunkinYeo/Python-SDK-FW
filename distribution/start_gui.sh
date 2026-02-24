#!/bin/bash

# SDK Validation Test GUI Launcher

echo "============================================================"
echo "  SDK Validation Test GUI"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Check Python
if ! command -v python &> /dev/null; then
    echo "[ERROR] Python is not installed."
    echo "   Install Python 3.11+: https://www.python.org/"
    exit 1
fi

echo "[OK] Python version: $(python --version)"

# Check dependencies
echo ""
echo "Checking dependencies..."
python -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[ERROR] tkinter is not installed."
    echo "   macOS: brew install python-tk"
    echo "   Ubuntu: sudo apt-get install python3-tk"
    exit 1
fi

# Start GUI
echo ""
echo "Starting GUI app..."
python gui_test_runner.py

echo ""
echo "GUI app closed."
