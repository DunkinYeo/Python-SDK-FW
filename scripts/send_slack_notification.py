"""Send test results to Slack."""
import os
import json
import requests
import sys
from datetime import datetime
from pathlib import Path


def load_test_results():
    """Load test results from pytest JSON report."""
    report_file = Path(".report.json")

    if not report_file.exists():
        print("❌ Test report file not found: .report.json")
        return None

    with open(report_file, 'r') as f:
        return json.load(f)


def extract_device_info(report):
    """Extract device information from test output."""
    device_info = {
        "serial": "Unknown",
        "firmware": "Unknown",
        "hardware": "Unknown",
        "software": "Unknown",
        "model": "Unknown",
        "battery": "Unknown",
        "rssi": "Unknown"
    }

    # Parse stdout from tests to extract device info
    for test in report.get('tests', []):
        if 'call' in test and 'stdout' in test['call']:
            stdout = test['call']['stdout']

            # Extract serial number
            if 'Serial Number:' in stdout:
                for line in stdout.split('\n'):
                    if 'Serial Number:' in line:
                        device_info['serial'] = line.split(':')[-1].strip()

            # Extract firmware version
            if 'Firmware Version:' in stdout:
                for line in stdout.split('\n'):
                    if 'Firmware Version:' in line:
                        device_info['firmware'] = line.split(':')[-1].strip()

            # Extract hardware version
            if 'Hardware Version:' in stdout:
                for line in stdout.split('\n'):
                    if 'Hardware Version:' in line:
                        device_info['hardware'] = line.split(':')[-1].strip()

            # Extract software version
            if 'Software Version:' in stdout:
                for line in stdout.split('\n'):
                    if 'Software Version:' in line:
                        device_info['software'] = line.split(':')[-1].strip()

            # Extract model
            if 'Model Number:' in stdout:
                for line in stdout.split('\n'):
                    if 'Model Number:' in line:
                        device_info['model'] = line.split(':')[-1].strip()

            # Extract battery
            if 'Battery Level:' in stdout:
                for line in stdout.split('\n'):
                    if 'Battery Level:' in line:
                        device_info['battery'] = line.split(':')[-1].strip()

            # Extract RSSI
            if 'RSSI:' in stdout:
                for line in stdout.split('\n'):
                    if line.strip().startswith('Current RSSI:') or line.strip().startswith('✅ CONNECTED! RSSI:'):
                        device_info['rssi'] = line.split(':')[-1].strip()
                        break

    return device_info


def build_slack_payload(report, device_info):
    """Build Slack message payload."""
    summary = report.get('summary', {})

    total = summary.get('total', 0)
    passed = summary.get('passed', 0)
    failed = summary.get('failed', 0)
    duration = report.get('duration', 0)

    # Calculate pass rate
    pass_rate = (passed / total * 100) if total > 0 else 0

    # Determine status emoji and color
    if failed == 0:
        status_emoji = "✅"
        color = "#36a64f"  # Green
        status_text = "SUCCESS"
    else:
        status_emoji = "⚠️"
        color = "#ff9800"  # Orange
        status_text = "PARTIAL SUCCESS"

    # Build failed tests list
    failed_tests = []
    for test in report.get('tests', []):
        if test.get('outcome') == 'failed':
            test_name = test.get('nodeid', '').split('::')[-1]
            failed_tests.append(f"• {test_name}")

    failed_tests_text = "\n".join(failed_tests) if failed_tests else "None"

    # Build Slack blocks
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"{status_emoji} SDK 검증 테스트 결과"
            }
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*상태:*\n{status_text}"},
                {"type": "mrkdwn", "text": f"*성공률:*\n{pass_rate:.1f}% ({passed}/{total})"},
                {"type": "mrkdwn", "text": f"*실행 시간:*\n{duration:.1f}초"},
                {"type": "mrkdwn", "text": f"*실행 시각:*\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}
            ]
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*📱 디바이스 정보*"
            }
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Model:*\n`{device_info['model']}`"},
                {"type": "mrkdwn", "text": f"*Serial:*\n`{device_info['serial']}`"},
                {"type": "mrkdwn", "text": f"*FW Version:*\n`{device_info['firmware']}`"},
                {"type": "mrkdwn", "text": f"*HW Version:*\n`{device_info['hardware']}`"},
                {"type": "mrkdwn", "text": f"*SW Version:*\n`{device_info['software']}`"},
                {"type": "mrkdwn", "text": f"*Battery:*\n`{device_info['battery']}%`"},
                {"type": "mrkdwn", "text": f"*RSSI:*\n`{device_info['rssi']} dBm`"},
                {"type": "mrkdwn", "text": f"*App Version:*\n`2.1.5`"}
            ]
        }
    ]

    # Add failed tests section if any
    if failed_tests:
        blocks.extend([
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*❌ 실패한 테스트 ({failed}개):*\n{failed_tests_text}"
                }
            }
        ])

    # Add test results section
    blocks.extend([
        {
            "type": "divider"
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*✅ 성공:*\n{passed}개"},
                {"type": "mrkdwn", "text": f"*❌ 실패:*\n{failed}개"},
                {"type": "mrkdwn", "text": f"*📊 전체:*\n{total}개"},
                {"type": "mrkdwn", "text": f"*⏱️ 소요 시간:*\n{duration:.0f}초"}
            ]
        }
    ])

    # Add GitHub Actions link if available
    github_run_url = os.getenv('GITHUB_SERVER_URL')
    if github_run_url:
        repo = os.getenv('GITHUB_REPOSITORY')
        run_id = os.getenv('GITHUB_RUN_ID')
        if repo and run_id:
            url = f"{github_run_url}/{repo}/actions/runs/{run_id}"
            blocks.append({
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "📄 상세 리포트 보기"
                        },
                        "url": url,
                        "style": "primary"
                    }
                ]
            })

    return {
        "attachments": [
            {
                "color": color,
                "blocks": blocks
            }
        ]
    }


def send_to_slack(webhook_url, payload):
    """Send payload to Slack webhook."""
    try:
        response = requests.post(
            webhook_url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        if response.status_code == 200:
            print("✅ Slack notification sent successfully!")
            return True
        else:
            print(f"❌ Failed to send Slack notification: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error sending Slack notification: {e}")
        return False


def main():
    """Main function."""
    print("\n" + "="*60)
    print("📤 Sending test results to Slack...")
    print("="*60)

    # Get Slack webhook URL from environment
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')

    if not webhook_url:
        print("❌ SLACK_WEBHOOK_URL environment variable not set")
        print("Please set it in .env file or as environment variable")
        sys.exit(1)

    # Load test results
    print("\n📊 Loading test results...")
    report = load_test_results()

    if not report:
        sys.exit(1)

    # Extract device info
    print("📱 Extracting device information...")
    device_info = extract_device_info(report)

    # Build Slack payload
    print("🔨 Building Slack message...")
    payload = build_slack_payload(report, device_info)

    # Send to Slack
    print(f"📤 Sending to Slack webhook...")
    success = send_to_slack(webhook_url, payload)

    if success:
        print("\n✅ Notification sent successfully!")
        sys.exit(0)
    else:
        print("\n❌ Failed to send notification")
        sys.exit(1)


if __name__ == "__main__":
    main()
