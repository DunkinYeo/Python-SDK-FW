#!/usr/bin/env python3
"""
Build script to create standalone executable
독립 실행 파일 생성 스크립트
"""
import subprocess
import sys
import os
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed."""
    print("📦 Installing PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

def build_executable():
    """Build the standalone executable."""
    print("\n🔨 Building standalone executable...")

    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name=SDK검증테스트",
        "--windowed",  # No console window
        "--onefile",   # Single executable file
        "--icon=NONE",  # Add icon if you have one
        "--add-data=tests:tests",
        "--add-data=scripts:scripts",
        "--add-data=.env.template:.env.template",
        "--hidden-import=pytest",
        "--hidden-import=appium",
        "--hidden-import=selenium",
        "--hidden-import=dotenv",
        "--hidden-import=requests",
        "gui_test_runner.py"
    ]

    subprocess.run(cmd, check=True)

    print("\n✅ Build complete!")
    print(f"📁 Executable location: {Path('dist/SDK검증테스트')}")
    print("\n📝 Next steps:")
    print("1. Copy the executable to desired location")
    print("2. Create a .env file with SLACK_WEBHOOK_URL")
    print("3. Make sure Appium server is running")
    print("4. Connect Android device")
    print("5. Run the executable!")

def main():
    """Main build process."""
    print("="*60)
    print("🚀 SDK Validation Test - Standalone Builder")
    print("="*60)

    try:
        # Install PyInstaller
        install_pyinstaller()

        # Build executable
        build_executable()

    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
