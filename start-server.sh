#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-8000}"
DIR="$(cd "$(dirname "$0")" && pwd)"

echo "서버 시작: http://localhost:${PORT}"

python3 -c "
import http.server, os, urllib.parse

os.chdir('$DIR')

class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        parsed = urllib.parse.urlparse(path)
        clean = parsed.path

        # /content/ 요청은 프로젝트 루트에서 그대로 서빙
        if clean.startswith('/content/'):
            return super().translate_path(path)

        # 그 외 요청은 web/ 디렉터리에서 서빙
        new_path = '/web' + clean
        if parsed.query:
            new_path += '?' + parsed.query
        return super().translate_path(new_path)

http.server.HTTPServer(('', $PORT), Handler).serve_forever()
"
