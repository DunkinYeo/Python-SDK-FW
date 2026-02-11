#!/usr/bin/env python3
"""Check if any tests failed and exit with error code if so."""

import json
import sys

def main():
    try:
        with open('.report.json') as f:
            report = json.load(f)

        failed = report.get('summary', {}).get('failed', 0)

        if failed > 0:
            print(f'❌ {failed} test(s) failed')
            sys.exit(1)
        else:
            print('✅ All tests passed')
            sys.exit(0)

    except Exception as e:
        print(f'Error checking test results: {e}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
