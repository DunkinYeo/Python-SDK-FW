#!/bin/bash
# SDK Validation Test - Full Auto Installer for Mac (double-click to run)

# Navigate to script directory
cd "$(dirname "$0")"

echo "============================================================"
echo "  SDK Validation Test - Auto Install"
echo "============================================================"
echo ""
echo "Terminal opened. Setting everything up automatically..."
echo ""

# 1. Check Python
echo "[Step 1] Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python is not installed."
    echo ""
    echo "Opening Python download page..."
    sleep 2
    open "https://www.python.org/downloads/"
    echo ""
    echo "Please install Python, then run this program again."
    echo ""
    read -p "Press any key to exit..."
    exit 1
else
    PYTHON_VERSION=$(python3 --version)
    echo "[OK] $PYTHON_VERSION installed"
fi

echo ""

# 2. Check ADB and auto-install
echo "[Step 2] Checking ADB (Android Debug Bridge)..."
if ! command -v adb &> /dev/null; then
    echo "[WARN] ADB is not installed."
    echo ""
    echo "Attempting auto-install via Homebrew..."

    # Check for Homebrew
    if ! command -v brew &> /dev/null; then
        echo "Homebrew not found. Installing Homebrew first..."
        echo ""
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi

    # Install ADB
    echo "Installing ADB..."
    brew install android-platform-tools

    if command -v adb &> /dev/null; then
        echo "[OK] ADB installed!"
    else
        echo "[ERROR] Auto-install failed. Manual installation required."
        echo ""
        echo "Download Platform Tools from:"
        open "https://developer.android.com/studio/releases/platform-tools"
        echo ""
        read -p "Press any key after installation..."
    fi
else
    ADB_VERSION=$(adb version | head -n 1)
    echo "[OK] $ADB_VERSION installed"
fi

echo ""

# 3. Install Python packages
echo "[Step 3] Installing required packages..."
echo "   (This may take a moment...)"
echo ""

python3 -m pip install --upgrade pip --quiet
python3 -m pip install -r requirements.txt --quiet
python3 -m pip install uiautomator2 adbutils --quiet

echo "[OK] All packages installed!"

echo ""

# 4. Check Android device
echo "[Step 4] Checking Android device..."
adb devices

DEVICE_COUNT=$(adb devices | grep -w "device" | wc -l | tr -d ' ')

if [ "$DEVICE_COUNT" -gt 0 ]; then
    echo "[OK] Android device connected!"
else
    echo "[WARN] No Android device connected."
    echo ""
    echo "Connect your Android device via USB and enable USB debugging:"
    echo "1. Settings > About Phone > tap Build Number 7 times"
    echo "2. Settings > Developer options > enable USB Debugging"
fi

echo ""
echo "============================================================"
echo "[OK] Installation complete!"
echo "============================================================"
echo ""
echo "Double-click 'run_tests.command' to run the tests!"
echo ""
echo "This window will close in 10 seconds..."
sleep 10
