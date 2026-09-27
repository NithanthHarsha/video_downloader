#!/usr/bin/env bash
# Production start script for Render backend service
set -e

echo "===> Preparing runtime environment..."

# Export Deno to PATH if installed in standard user or system directories
export DENO_INSTALL="$HOME/.deno"
for deno_dir in "$HOME/.deno/bin" "/opt/render/.deno/bin" "/root/.deno/bin"; do
    if [ -d "$deno_dir" ]; then
        export PATH="$deno_dir:$PATH"
    fi
done

# Start bgutil PO Token Provider HTTP server
if [ -d "bgutil-server" ]; then
    cd bgutil-server

    # Ensure build/main.js or dependencies exist
    if [ ! -f "build/main.js" ] && [ ! -d "node_modules" ]; then
        echo "Installing bgutil-server dependencies at startup..."
        npm install --no-audit --no-fund || true
        npx tsc || true
    fi

    echo "Starting local bgutil PO Token HTTP server (v2.0.0) on 127.0.0.1:4416..."
    if [ -f "build/main.js" ]; then
        node build/main.js --port 4416 --host 127.0.0.1 >> ../bgutil_server.log 2>&1 &
    elif command -v deno &> /dev/null; then
        deno run --allow-net --allow-read --allow-env src/main.ts --port 4416 --host 127.0.0.1 >> ../bgutil_server.log 2>&1 &
    fi
    cd ..

    # Health check verification loop
    echo "Waiting for bgutil PO Token server to respond on 127.0.0.1:4416/ping..."
    SERVER_READY=false
    for i in {1..20}; do
        if curl -s -f http://127.0.0.1:4416/ping > /dev/null 2>&1; then
            echo "bgutil PO Token server is UP and responding on 127.0.0.1:4416!"
            SERVER_READY=true
            break
        fi
        sleep 0.3
    done

    if [ "$SERVER_READY" = false ]; then
        echo "Note: bgutil HTTP daemon will fall back to dynamic script provider."
    fi
fi

# Start Gunicorn server
PORT_VAL="${PORT:-8000}"
echo "===> Starting Gunicorn on 0.0.0.0:${PORT_VAL}..."
exec gunicorn config.wsgi:application --bind "0.0.0.0:${PORT_VAL}" --workers 2 --threads 4 --timeout 3600
