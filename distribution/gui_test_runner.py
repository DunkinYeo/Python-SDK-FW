#!/usr/bin/env python3
"""
SDK Validation Test Runner - Standalone GUI Application
비개발자를 위한 간단한 테스트 실행 도구
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
import requests

# Load environment variables
load_dotenv()


class TestRunnerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SDK 검증 테스트 자동화")
        self.root.geometry("700x800")
        self.root.resizable(False, False)

        # Variables
        self.device_serial = tk.StringVar(value=os.getenv('BLE_DEVICE_SERIAL', '610031'))
        self.target_packets = tk.StringVar(value="60")
        self.run_packet_test = tk.BooleanVar(value=False)
        self.is_running = False
        self.process = None

        self.setup_ui()
        self.check_environment()

    def setup_ui(self):
        """Setup the user interface."""
        # Header
        header_frame = tk.Frame(self.root, bg="#2196F3", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        header_label = tk.Label(
            header_frame,
            text="🚀 SDK 검증 테스트 자동화",
            font=("Arial", 20, "bold"),
            bg="#2196F3",
            fg="white"
        )
        header_label.pack(pady=20)

        # Main content
        content_frame = tk.Frame(self.root, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Device Serial Input
        serial_frame = tk.LabelFrame(content_frame, text="디바이스 설정", font=("Arial", 12, "bold"), padx=10, pady=10)
        serial_frame.pack(fill=tk.X, pady=10)

        tk.Label(serial_frame, text="디바이스 시리얼 넘버:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        serial_entry = tk.Entry(serial_frame, textvariable=self.device_serial, font=("Arial", 10), width=30)
        serial_entry.grid(row=0, column=1, pady=5, padx=10)
        tk.Label(serial_frame, text="예: 610031", font=("Arial", 8), fg="gray").grid(row=0, column=2, sticky=tk.W)

        # Test Options
        test_frame = tk.LabelFrame(content_frame, text="테스트 옵션", font=("Arial", 12, "bold"), padx=10, pady=10)
        test_frame.pack(fill=tk.X, pady=10)

        packet_check = tk.Checkbutton(
            test_frame,
            text="패킷 모니터링 테스트 포함",
            variable=self.run_packet_test,
            font=("Arial", 10),
            command=self.toggle_packet_options
        )
        packet_check.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=5)

        self.packet_label = tk.Label(test_frame, text="타겟 패킷 수:", font=("Arial", 10), state=tk.DISABLED)
        self.packet_label.grid(row=1, column=0, sticky=tk.W, pady=5)

        self.packet_entry = tk.Entry(test_frame, textvariable=self.target_packets, font=("Arial", 10), width=15, state=tk.DISABLED)
        self.packet_entry.grid(row=1, column=1, pady=5, padx=10)

        packet_info = tk.Label(
            test_frame,
            text="60=1분, 600=10분, 3600=1시간",
            font=("Arial", 8),
            fg="gray",
            state=tk.DISABLED
        )
        packet_info.grid(row=1, column=2, sticky=tk.W)
        self.packet_info_label = packet_info

        # Status Section
        status_frame = tk.LabelFrame(content_frame, text="실행 상태", font=("Arial", 12, "bold"), padx=10, pady=10)
        status_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.status_label = tk.Label(
            status_frame,
            text="준비됨",
            font=("Arial", 10),
            fg="green"
        )
        self.status_label.pack(pady=5)

        self.progress = ttk.Progressbar(status_frame, mode='indeterminate', length=600)
        self.progress.pack(pady=10)

        # Log output
        self.log_text = scrolledtext.ScrolledText(
            status_frame,
            height=15,
            font=("Courier", 9),
            bg="#f5f5f5"
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # Buttons
        button_frame = tk.Frame(content_frame)
        button_frame.pack(fill=tk.X, pady=10)

        self.start_button = tk.Button(
            button_frame,
            text="🚀 테스트 시작",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            height=2,
            command=self.start_test
        )
        self.start_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self.stop_button = tk.Button(
            button_frame,
            text="⏹ 중지",
            font=("Arial", 14, "bold"),
            bg="#f44336",
            fg="white",
            height=2,
            state=tk.DISABLED,
            command=self.stop_test
        )
        self.stop_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        # Footer
        footer_frame = tk.Frame(self.root, bg="#f5f5f5", height=40)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)

        footer_label = tk.Label(
            footer_frame,
            text="Made with Claude Code",
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
        self.log("환경 확인 중...\n")

        # Check ADB
        try:
            result = subprocess.run(
                ["adb", "devices"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if "device" in result.stdout:
                self.log("✅ Android 디바이스 연결됨\n", "green")
            else:
                self.log("⚠️ Android 디바이스가 연결되지 않음\n", "orange")
        except Exception as e:
            self.log(f"❌ ADB 확인 실패: {e}\n", "red")

        # Check Appium server
        try:
            response = requests.get("http://localhost:4723/status", timeout=2)
            if response.status_code == 200:
                self.log("✅ Appium 서버 실행 중\n", "green")
            else:
                self.log("⚠️ Appium 서버 응답 없음\n", "orange")
        except:
            self.log("❌ Appium 서버가 실행되지 않음\n", "red")
            self.log("   터미널에서 'appium' 명령으로 서버를 시작하세요\n", "gray")

        # Check Slack webhook
        if os.getenv('SLACK_WEBHOOK_URL'):
            self.log("✅ Slack 알림 설정됨\n", "green")
        else:
            self.log("⚠️ Slack 알림 미설정 (.env 파일 확인)\n", "orange")

        self.log("\n준비 완료! 테스트를 시작하세요.\n", "green")

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
        """Start the test in a separate thread."""
        if self.is_running:
            return

        # Validate inputs
        if not self.device_serial.get():
            messagebox.showerror("오류", "디바이스 시리얼 넘버를 입력하세요")
            return

        if self.run_packet_test.get():
            try:
                packets = int(self.target_packets.get())
                if packets <= 0:
                    raise ValueError()
            except:
                messagebox.showerror("오류", "올바른 타겟 패킷 수를 입력하세요")
                return

        # Update UI
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress.start()
        self.log_text.delete(1.0, tk.END)
        self.update_status("테스트 실행 중...", "blue")

        # Save device serial to .env
        self.save_device_serial()

        # Start test in thread
        test_thread = threading.Thread(target=self.run_test, daemon=True)
        test_thread.start()

    def save_device_serial(self):
        """Save device serial to .env file."""
        env_file = Path(".env")
        if env_file.exists():
            content = env_file.read_text()
            if "BLE_DEVICE_SERIAL=" in content:
                # Update existing
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith("BLE_DEVICE_SERIAL="):
                        lines[i] = f"BLE_DEVICE_SERIAL={self.device_serial.get()}"
                env_file.write_text('\n'.join(lines))
            else:
                # Append new
                with open(env_file, 'a') as f:
                    f.write(f"\nBLE_DEVICE_SERIAL={self.device_serial.get()}\n")

    def run_test(self):
        """Run the actual test."""
        try:
            # Force stop app
            self.log("🛑 앱 강제 종료 중...\n")
            subprocess.run(
                ["adb", "shell", "am", "force-stop", "com.wellysis.spatch.sdk.sample"],
                capture_output=True
            )
            time.sleep(2)

            # Check if packet monitoring test is requested
            if self.run_packet_test.get():
                # Show manual reset instructions
                self.root.after(0, self.show_reset_instructions)
                return

            # Build pytest command
            self.log("\n🧪 테스트 실행 중...\n", "blue")
            cmd = [
                sys.executable, "-m", "pytest",
                "tests/regression/test_regression.py",
                "-v",
                "--html=test-report.html",
                "--self-contained-html",
                "--json-report",
                "--json-report-file=.report.json",
                "--tb=short"
            ]

            if self.run_packet_test.get():
                cmd.append(f"--target-packets={self.target_packets.get()}")

            # Run pytest
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            # Stream output
            for line in self.process.stdout:
                if not self.is_running:
                    break
                self.root.after(0, self.log, line)

            self.process.wait()

            # Check result
            if self.process.returncode == 0:
                self.root.after(0, self.test_completed, True)
            else:
                self.root.after(0, self.test_completed, False)

        except Exception as e:
            self.root.after(0, self.test_failed, str(e))

    def show_reset_instructions(self):
        """Show device reset instructions for packet monitoring test."""
        self.progress.stop()
        result = messagebox.askyesno(
            "디바이스 초기화 필요",
            "패킷 모니터링 테스트를 시작하기 전에:\n\n"
            "1. 앱에서 WriteSet → STOP 클릭\n"
            "2. WriteSet → RESET DEVICE 클릭\n"
            "3. Packet Number가 0으로 초기화되었는지 확인\n\n"
            "초기화를 완료하셨습니까?"
        )

        if result:
            self.progress.start()
            # Continue with test
            test_thread = threading.Thread(target=self.run_test_after_reset, daemon=True)
            test_thread.start()
        else:
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.update_status("테스트 취소됨", "orange")
            self.log("\n❌ 테스트가 취소되었습니다.\n", "red")

    def run_test_after_reset(self):
        """Run test after manual reset is confirmed."""
        try:
            self.log("\n🧪 테스트 실행 중...\n", "blue")
            cmd = [
                sys.executable, "-m", "pytest",
                "tests/regression/test_regression.py",
                "-v",
                "--html=test-report.html",
                "--self-contained-html",
                "--json-report",
                "--json-report-file=.report.json",
                "--tb=short",
                f"--target-packets={self.target_packets.get()}"
            ]

            # Run pytest
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            # Stream output
            for line in self.process.stdout:
                if not self.is_running:
                    break
                self.root.after(0, self.log, line)

            self.process.wait()

            # Check result
            if self.process.returncode == 0:
                self.root.after(0, self.test_completed, True)
            else:
                self.root.after(0, self.test_completed, False)

        except Exception as e:
            self.root.after(0, self.test_failed, str(e))

    def test_completed(self, success):
        """Handle test completion."""
        self.is_running = False
        self.progress.stop()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        if success:
            self.update_status("✅ 테스트 완료!", "green")
            self.log("\n✅ 모든 테스트가 성공적으로 완료되었습니다!\n", "green")

            # Send Slack notification
            self.send_slack_notification()

            # Open HTML report
            self.log("\n📊 HTML 리포트를 여는 중...\n")
            report_path = Path("test-report.html").absolute()
            if report_path.exists():
                webbrowser.open(f"file://{report_path}")

            messagebox.showinfo(
                "테스트 완료",
                "✅ 모든 테스트가 성공적으로 완료되었습니다!\n\n"
                "- HTML 리포트가 브라우저에서 열립니다\n"
                "- Slack 알림이 전송되었습니다"
            )
        else:
            self.update_status("❌ 테스트 실패", "red")
            self.log("\n❌ 일부 테스트가 실패했습니다.\n", "red")
            self.send_slack_notification()
            messagebox.showwarning(
                "테스트 실패",
                "❌ 일부 테스트가 실패했습니다.\n\n"
                "상세 내용은 로그와 HTML 리포트를 확인하세요."
            )

    def test_failed(self, error):
        """Handle test failure."""
        self.is_running = False
        self.progress.stop()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.update_status("❌ 오류 발생", "red")
        self.log(f"\n❌ 오류: {error}\n", "red")
        messagebox.showerror("오류", f"테스트 실행 중 오류가 발생했습니다:\n\n{error}")

    def send_slack_notification(self):
        """Send Slack notification."""
        try:
            self.log("\n📤 Slack 알림 전송 중...\n")
            result = subprocess.run(
                [sys.executable, "scripts/send_slack_notification.py"],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                self.log("✅ Slack 알림이 전송되었습니다.\n", "green")
            else:
                self.log("⚠️ Slack 알림 전송 실패\n", "orange")
        except Exception as e:
            self.log(f"⚠️ Slack 알림 전송 중 오류: {e}\n", "orange")

    def stop_test(self):
        """Stop the running test."""
        if self.is_running and self.process:
            result = messagebox.askyesno(
                "테스트 중지",
                "실행 중인 테스트를 중지하시겠습니까?"
            )
            if result:
                self.is_running = False
                self.process.terminate()
                self.progress.stop()
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)
                self.update_status("테스트 중지됨", "orange")
                self.log("\n⚠️ 테스트가 사용자에 의해 중지되었습니다.\n", "orange")


def main():
    """Main entry point."""
    root = tk.Tk()
    app = TestRunnerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
