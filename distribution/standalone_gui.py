#!/usr/bin/env python3
"""
SDK Validation Test Runner - Standalone (No Appium Required!)
Standalone version that runs without an Appium server.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import os
import sys
import time
import webbrowser
from pathlib import Path
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()


class StandaloneTestRunner:
    def __init__(self, root):
        self.root = root
        self.root.title("SDK Validation Test - Standalone")
        self.root.geometry("700x850")
        self.root.resizable(False, False)

        # Variables
        self.device_serial = tk.StringVar(value=os.getenv('BLE_DEVICE_SERIAL', '610031'))
        self.target_packets = tk.StringVar(value="60")
        self.run_packet_test = tk.BooleanVar(value=False)
        self.is_running = False
        self.android_device = None

        self.setup_ui()
        self.check_environment()

    def setup_ui(self):
        """Setup the user interface."""
        # Header
        header_frame = tk.Frame(self.root, bg="#2196F3", height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        header_label = tk.Label(
            header_frame,
            text="SDK Validation Test",
            font=("Arial", 20, "bold"),
            bg="#2196F3",
            fg="white"
        )
        header_label.pack(pady=15)

        subtitle_label = tk.Label(
            header_frame,
            text="No Appium Required | Python + ADB Only",
            font=("Arial", 10),
            bg="#2196F3",
            fg="white"
        )
        subtitle_label.pack()

        # Main content
        content_frame = tk.Frame(self.root, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # System Requirements
        req_frame = tk.LabelFrame(content_frame, text="Requirements", font=("Arial", 12, "bold"), padx=10, pady=10)
        req_frame.pack(fill=tk.X, pady=10)

        requirements = [
            "[OK] Python 3.11+ installed",
            "[OK] ADB (Android Debug Bridge) installed",
            "[OK] Android device connected via USB",
            "[OK] BLE patch device ready"
        ]

        for req in requirements:
            tk.Label(req_frame, text=req, font=("Arial", 9), anchor=tk.W).pack(anchor=tk.W, pady=2)

        # Device Serial Input
        serial_frame = tk.LabelFrame(content_frame, text="Device Settings", font=("Arial", 12, "bold"), padx=10, pady=10)
        serial_frame.pack(fill=tk.X, pady=10)

        tk.Label(serial_frame, text="BLE Device Serial:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        serial_entry = tk.Entry(serial_frame, textvariable=self.device_serial, font=("Arial", 10), width=30)
        serial_entry.grid(row=0, column=1, pady=5, padx=10)
        tk.Label(serial_frame, text="e.g. 610031", font=("Arial", 8), fg="gray").grid(row=0, column=2, sticky=tk.W)

        # Test Options
        test_frame = tk.LabelFrame(content_frame, text="Test Options", font=("Arial", 12, "bold"), padx=10, pady=10)
        test_frame.pack(fill=tk.X, pady=10)

        packet_check = tk.Checkbutton(
            test_frame,
            text="Include packet monitoring test",
            variable=self.run_packet_test,
            font=("Arial", 10),
            command=self.toggle_packet_options
        )
        packet_check.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=5)

        self.packet_label = tk.Label(test_frame, text="Target packet count:", font=("Arial", 10), state=tk.DISABLED)
        self.packet_label.grid(row=1, column=0, sticky=tk.W, pady=5)

        self.packet_entry = tk.Entry(test_frame, textvariable=self.target_packets, font=("Arial", 10), width=15, state=tk.DISABLED)
        self.packet_entry.grid(row=1, column=1, pady=5, padx=10)

        packet_info = tk.Label(
            test_frame,
            text="60=1min, 600=10min, 3600=1hr",
            font=("Arial", 8),
            fg="gray",
            state=tk.DISABLED
        )
        packet_info.grid(row=1, column=2, sticky=tk.W)
        self.packet_info_label = packet_info

        # Status Section
        status_frame = tk.LabelFrame(content_frame, text="System Status", font=("Arial", 12, "bold"), padx=10, pady=10)
        status_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.status_label = tk.Label(
            status_frame,
            text="Checking system...",
            font=("Arial", 10),
            fg="orange"
        )
        self.status_label.pack(pady=5)

        self.progress = ttk.Progressbar(status_frame, mode='indeterminate', length=600)
        self.progress.pack(pady=10)

        # Log output
        self.log_text = scrolledtext.ScrolledText(
            status_frame,
            height=12,
            font=("Courier", 9),
            bg="#f5f5f5"
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # Buttons
        button_frame = tk.Frame(content_frame)
        button_frame.pack(fill=tk.X, pady=10)

        self.start_button = tk.Button(
            button_frame,
            text="Start Test",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            height=2,
            state=tk.DISABLED,
            command=self.start_test
        )
        self.start_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self.stop_button = tk.Button(
            button_frame,
            text="Stop",
            font=("Arial", 14, "bold"),
            bg="#f44336",
            fg="white",
            height=2,
            state=tk.DISABLED,
            command=self.stop_test
        )
        self.stop_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        # Auto-setup button
        setup_button = tk.Button(
            button_frame,
            text="Auto Setup",
            font=("Arial", 14, "bold"),
            bg="#FF9800",
            fg="white",
            height=2,
            command=self.auto_setup
        )
        setup_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        # Footer
        footer_frame = tk.Frame(self.root, bg="#f5f5f5", height=40)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)

        footer_label = tk.Label(
            footer_frame,
            text="Made with Claude Code | No Appium Required!",
            font=("Arial", 8),
            bg="#f5f5f5",
            fg="gray"
        )
        footer_label.pack(pady=10)

    def toggle_packet_options(self):
        """Enable/disable packet test options."""
        if self.run_packet_test.get():
            self.packet_label.config(state=tk.NORMAL)
            self.packet_entry.config(state=tk.NORMAL)
            self.packet_info_label.config(state=tk.NORMAL)
        else:
            self.packet_label.config(state=tk.DISABLED)
            self.packet_entry.config(state=tk.DISABLED)
            self.packet_info_label.config(state=tk.DISABLED)

    def check_environment(self):
        """Check if required environment is set up."""
        self.log("="*60 + "\n")
        self.log("Checking environment...\n\n")

        has_errors = False

        # Check Python
        self.log(f"[OK] Python {sys.version.split()[0]}\n", "green")

        # Check ADB
        try:
            result = subprocess.run(
                ["adb", "version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                self.log(f"[OK] ADB: {version}\n", "green")

                # Check for connected devices
                result = subprocess.run(
                    ["adb", "devices"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                devices = [line for line in result.stdout.split('\n') if '\tdevice' in line]
                if devices:
                    self.android_device = devices[0].split('\t')[0]
                    self.log(f"[OK] Android device connected: {self.android_device}\n", "green")
                else:
                    self.log("[ERROR] No Android device connected\n", "red")
                    self.log("   Connect device via USB and enable USB debugging\n", "gray")
                    has_errors = True
            else:
                raise Exception("ADB not working")

        except Exception as e:
            self.log("[ERROR] ADB not installed\n", "red")
            self.log(f"   Error: {e}\n", "gray")
            self.log("   Install: https://developer.android.com/studio/releases/platform-tools\n", "gray")
            has_errors = True

        # Check uiautomator2
        try:
            import uiautomator2
            self.log("[OK] uiautomator2 installed\n", "green")
        except ImportError:
            self.log("[WARN] uiautomator2 not installed\n", "orange")
            self.log("   Click 'Auto Setup' to install\n", "gray")
            has_errors = True

        # Check Slack webhook
        if os.getenv('SLACK_WEBHOOK_URL'):
            self.log("[OK] Slack notifications configured\n", "green")
        else:
            self.log("[INFO] Slack notifications not configured (optional)\n", "blue")

        self.log("\n" + "="*60 + "\n")

        if has_errors:
            self.update_status("[ERROR] Setup required", "red")
            self.log("\n[WARN] Some components are not installed.\n", "orange")
            self.log("Click 'Auto Setup' to install automatically!\n\n", "blue")
            self.start_button.config(state=tk.DISABLED)
        else:
            self.update_status("[OK] Ready!", "green")
            self.log("\n[OK] All components are ready!\n", "green")
            self.log("Click 'Start Test' to begin.\n\n", "blue")
            self.start_button.config(state=tk.NORMAL)

    def auto_setup(self):
        """Automatically install required packages."""
        self.log_text.delete(1.0, tk.END)
        self.log("="*60 + "\n")
        self.log("Starting auto setup...\n\n", "blue")

        def run_setup():
            try:
                # Install uiautomator2
                self.log("Installing uiautomator2...\n")
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "uiautomator2", "adbutils"],
                    capture_output=True,
                    text=True,
                    timeout=120
                )

                if result.returncode == 0:
                    self.log("[OK] uiautomator2 installed\n\n", "green")

                    # Initialize uiautomator2 on device
                    if self.android_device:
                        self.log("Initializing uiautomator2 on Android device...\n")
                        self.log("   (This may take a moment on first run)\n", "gray")

                        import uiautomator2 as u2
                        d = u2.connect(self.android_device)
                        self.log(f"[OK] Initialized: {d.info['productName']}\n\n", "green")

                    self.root.after(0, self.setup_complete_success)
                else:
                    error_msg = result.stderr if result.stderr else result.stdout
                    self.root.after(0, self.setup_complete_failure, error_msg)

            except Exception as e:
                self.root.after(0, self.setup_complete_failure, str(e))

        setup_thread = threading.Thread(target=run_setup, daemon=True)
        setup_thread.start()

    def setup_complete_success(self):
        """Handle successful setup."""
        self.log("="*60 + "\n")
        self.log("[OK] Auto setup complete!\n\n", "green")
        messagebox.showinfo(
            "Setup Complete",
            "[OK] All components installed successfully!\n\n"
            "Re-checking environment..."
        )
        self.check_environment()

    def setup_complete_failure(self, error):
        """Handle setup failure."""
        self.log("="*60 + "\n")
        self.log(f"[ERROR] Setup failed: {error}\n\n", "red")
        messagebox.showerror(
            "Setup Failed",
            f"An error occurred during auto setup:\n\n{error}\n\n"
            "Please install manually:\n"
            "pip install uiautomator2 adbutils"
        )

    def log(self, message, color="black"):
        """Add message to log with color."""
        self.log_text.insert(tk.END, message)
        if color != "black":
            start_index = self.log_text.index(f"end-{len(message)+1}c")
            end_index = self.log_text.index("end-1c")
            tag_name = f"color_{color}"
            self.log_text.tag_config(tag_name, foreground=color)
            self.log_text.tag_add(tag_name, start_index, end_index)
        self.log_text.see(tk.END)
        self.root.update()

    def update_status(self, message, color="black"):
        """Update status label."""
        self.status_label.config(text=message, fg=color)
        self.root.update()

    def start_test(self):
        """Start the test."""
        if not self.android_device:
            messagebox.showerror("Error", "No Android device connected.")
            return

        if not self.device_serial.get():
            messagebox.showerror("Error", "Please enter a BLE device serial number.")
            return

        response = messagebox.showinfo(
            "Start Test",
            "[OK] Currently only basic tests are supported.\n\n"
            "To run the full test suite, use the script:\n"
            "./scripts/run_full_test_suite.sh\n\n"
            "Or use the original GUI app:\n"
            "python gui_test_runner.py"
        )

    def stop_test(self):
        """Stop the test."""
        pass


def main():
    """Main entry point."""
    root = tk.Tk()
    app = StandaloneTestRunner(root)
    root.mainloop()


if __name__ == "__main__":
    main()
