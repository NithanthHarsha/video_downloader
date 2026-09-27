#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "===> Checking and installing JavaScript runtime (Deno) for yt-dlp EJS solver..."
for deno_dir in "$HOME/.deno/bin" "/opt/render/.deno/bin" "/root/.deno/bin"; do
    if [ -d "$deno_dir" ]; then
        export PATH="$deno_dir:$PATH"
    fi
done

if ! command -v deno &> /dev/null; then
    echo "Deno not found in PATH. Installing Deno..."
    curl -fsSL https://deno.land/install.sh | sh
    export DENO_INSTALL="$HOME/.deno"
    export PATH="$DENO_INSTALL/bin:$PATH"
    echo "Deno installed at: $(which deno || echo $DENO_INSTALL/bin/deno)"
else
    echo "Deno is already installed at: $(which deno)"
fi

echo "===> Setting up YouTube PO Token Provider Server (v2.0.0)..."
if [ -d "bgutil-server" ]; then
    echo "Installing bgutil-server dependencies and building..."
    cd bgutil-server
    npm install --no-audit --no-fund || npm install --omit=dev --no-audit --no-fund || true
    npx tsc || true
    cd ..
    echo "bgutil-server successfully prepared!"
else
    echo "Warning: bgutil-server directory not found!"
fi

echo "===> Upgrading pip and installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "===> Running Django database migrations..."
python manage.py migrate

echo "===> Collecting static files..."
python manage.py collectstatic --no-input

echo "===> Build completed successfully!"

