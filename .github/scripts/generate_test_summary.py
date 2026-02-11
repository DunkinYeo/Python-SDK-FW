#!/usr/bin/env python3
"""Generate GitHub Actions test summary from pytest JSON report."""

import json
import sys

def main():
    try:
        with open('.report.json') as f:
            report = json.load(f)

        summary = report.get('summary', {})
        total = summary.get('total', 0)
        passed = summary.get('passed', 0)
        failed = summary.get('failed', 0)
        duration = report.get('duration', 0)

        print(f'**Total Tests:** {total}')
        print(f'**✅ Passed:** {passed}')
        print(f'**❌ Failed:** {failed}')
        print(f'**⏱️  Duration:** {duration:.1f}s')

        if total > 0:
            pass_rate = (passed / total) * 100
            print(f'**📊 Pass Rate:** {pass_rate:.1f}%')
        else:
            print('**📊 Pass Rate:** N/A')

    except Exception as e:
        print(f'Error generating summary: {e}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
