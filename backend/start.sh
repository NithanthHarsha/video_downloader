#!/usr/bin/env bash
# Production start script for Render backend service
set -e

echo "===> Preparing runtime environment..."

# Export Deno to PATH if installed in user directory
export DENO_INSTALL="$HOME/.deno"
if [ -d "$DENO_INSTALL/bin" ]; then
    export PATH="$DENO_INSTALL/bin:$PATH"
fi

# Start bgutil PO Token Provider HTTP server
if [ -d "bgutil-server" ]; then
    cd bgutil-server

    # Ensure node_modules exists
    if [ ! -d "node_modules" ]; then
        echo "Installing bgutil-server dependencies at startup..."
        npm install --omit=dev --no-audit --no-fund || npm install
    fi

    # Ensure build/main.js exists
    if [ ! -f "build/main.js" ]; then
        echo "Compiling bgutil-server TypeScript..."
        npx tsc || true
    fi

    echo "Starting local bgutil PO Token HTTP server (v2.0.0) on 127.0.0.1:4416..."
    node build/main.js --port 4416 --host 127.0.0.1 >> ../bgutil_server.log 2>&1 &
    cd ..

    # Health check verification loop
    echo "Waiting for bgutil PO Token server to respond on 127.0.0.1:4416/ping..."
    SERVER_READY=false
    for i in {1..30}; do
        if curl -s -f http://127.0.0.1:4416/ping > /dev/null 2>&1; then
            echo "bgutil PO Token server is UP and responding on 127.0.0.1:4416!"
            SERVER_READY=true
            break
        fi
        sleep 0.5
    done

    if [ "$SERVER_READY" = false ]; then
        echo "WARNING: bgutil-server did not respond to /ping in 15 seconds. Log output:"
        cat bgutil_server.log || true
    fi
fi

# Start Gunicorn server
PORT_VAL="${PORT:-8000}"
echo "===> Starting Gunicorn on 0.0.0.0:${PORT_VAL}..."
exec gunicorn config.wsgi:application --bind "0.0.0.0:${PORT_VAL}" --workers 2 --threads 4 --timeout 3600
