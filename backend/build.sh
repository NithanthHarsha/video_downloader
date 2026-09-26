#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "===> Checking and installing JavaScript runtime (Deno) for yt-dlp EJS solver..."
if ! command -v deno &> /dev/null; then
    echo "Deno not found in PATH. Installing Deno..."
    curl -fsSL https://deno.land/install.sh | sh
    export DENO_INSTALL="$HOME/.deno"
    export PATH="$DENO_INSTALL/bin:$PATH"
    echo "Deno installed at: $(which deno || echo $DENO_INSTALL/bin/deno)"
else
    echo "Deno is already installed at: $(which deno)"
fi

echo "===> Setting up YouTube PO Token Provider (bgutil-pot)..."
mkdir -p "$HOME/.deno/bin"
if [ ! -f "$HOME/.deno/bin/bgutil-pot" ]; then
    echo "Downloading bgutil-pot binary for Linux x86_64..."
    curl -fsSL https://github.com/jim60105/bgutil-ytdlp-pot-provider-rs/releases/latest/download/bgutil-pot-linux-x86_64 -o "$HOME/.deno/bin/bgutil-pot" || true
    chmod +x "$HOME/.deno/bin/bgutil-pot" || true
fi

echo "===> Upgrading pip and installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "===> Running Django database migrations..."
python manage.py migrate

echo "===> Collecting static files..."
python manage.py collectstatic --no-input

echo "===> Build completed successfully!"
