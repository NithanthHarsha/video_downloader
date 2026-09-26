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

echo "===> Upgrading pip and installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "===> Running Django database migrations..."
python manage.py migrate

echo "===> Collecting static files..."
python manage.py collectstatic --no-input

echo "===> Build completed successfully!"
