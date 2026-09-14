"""Read-only checks suitable for a deployed instance as well as disposable CI."""

import argparse
import json
from urllib.request import urlopen


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-url', required=True)
    parser.add_argument('--expected-revision', required=True)
    args = parser.parse_args()
    base_url = args.base_url.rstrip('/')
    checks = []
    for path in ['/health/live/', '/health/ready/']:
        with urlopen(base_url + path, timeout=10) as response:
            payload = json.load(response)
            if payload != {'status': 'ok', 'revision': args.expected_revision}:
                raise SystemExit(f'Unexpected health/revision response from {path}')
            checks.append({'path': path, 'status': response.status, 'revision': payload['revision']})
    for path, content_type in [('/', 'text/html'), ('/static/css/style.css', 'text/css'), ('/static/js/main.js', 'javascript')]:
        with urlopen(base_url + path, timeout=10) as response:
            if response.status != 200 or content_type not in response.headers.get('Content-Type', '') or not response.read():
                raise SystemExit(f'Failed page/static-file check: {path}')
            checks.append({'path': path, 'status': response.status})
    print(json.dumps({'checks': checks}, indent=2))


if __name__ == '__main__':
    main()
