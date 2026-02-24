#!/bin/bash
# SDK Validation Test Launcher for Mac (double-click to run)

# Navigate to script directory
cd "$(dirname "$0")"

clear
echo "============================================================"
echo "  SDK Validation Test - Starting GUI"
echo "============================================================"
echo ""
echo "Launching GUI app..."
echo ""

# Launch GUI app (standalone version - no Appium required)
if [ -f "standalone_gui.py" ]; then
    python3 standalone_gui.py
else
    echo "[ERROR] GUI app not found."
    echo ""
    read -p "Press any key to exit..."
fi
