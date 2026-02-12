#!/bin/bash

# Run regression tests and send results to Slack

set -e  # Exit on error

echo "============================================================"
echo "🧪 SDK 검증 자동화 테스트"
echo "============================================================"

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Stop app first
echo ""
echo "🛑 Stopping app..."
adb shell am force-stop com.wellysis.spatch.sdk.sample || true
sleep 2

# Run tests with HTML and JSON reports
echo ""
echo "🧪 Running regression tests..."
python -m pytest tests/regression/test_regression.py \
    -v \
    --html=test-report.html \
    --self-contained-html \
    --json-report \
    --json-report-file=.report.json \
    --tb=short \
    || TEST_FAILED=true

echo ""
echo "============================================================"

# Send results to Slack
if [ -z "$SLACK_WEBHOOK_URL" ] || [ "$SLACK_WEBHOOK_URL" = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL" ]; then
    echo "⚠️  SLACK_WEBHOOK_URL not configured"
    echo "ℹ️  To enable Slack notifications, set SLACK_WEBHOOK_URL in .env"
else
    echo "📤 Sending results to Slack..."
    python scripts/send_slack_notification.py || echo "⚠️  Failed to send Slack notification"
fi

echo ""
echo "============================================================"
echo "📄 Test Report: test-report.html"
echo "============================================================"

# Open HTML report if on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo ""
    echo "Opening test report in browser..."
    open test-report.html
fi

# Exit with test result
if [ "$TEST_FAILED" = "true" ]; then
    echo ""
    echo "❌ Some tests failed"
    exit 1
else
    echo ""
    echo "✅ All tests passed"
    exit 0
fi
