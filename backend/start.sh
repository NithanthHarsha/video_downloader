#!/usr/bin/env bash
# Production start script for Render backend service
set -e

echo "===> Preparing runtime environment..."

# Export Deno to PATH if installed in user directory
if [ -d "$HOME/.deno/bin" ]; then
    export PATH="$HOME/.deno/bin:$PATH"
fi

# Ensure bgutil-server is compiled and start in background
if [ -d "bgutil-server" ]; then
    if [ ! -f "bgutil-server/build/main.js" ]; then
        echo "Building bgutil-server TypeScript code..."
        (cd bgutil-server && npx tsc || true)
    fi

    if [ -f "bgutil-server/build/main.js" ]; then
        echo "Starting local bgutil PO Token HTTP server (v2.0.0) on 127.0.0.1:4416..."
        node bgutil-server/build/main.js --port 4416 --host 127.0.0.1 &
        sleep 2
    fi
fi

# Start Gunicorn server
PORT_VAL="${PORT:-8000}"
echo "===> Starting Gunicorn on 0.0.0.0:${PORT_VAL}..."
exec gunicorn config.wsgi:application --bind "0.0.0.0:${PORT_VAL}" --workers 2 --threads 4 --timeout 3600
