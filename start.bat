@echo off
title Velora Video Downloader Launcher (Django + Next.js)
cls
echo ===================================================
echo Starting Velora (Django + Next.js)...
echo ===================================================

echo [1/3] Freeing up ports 3000 and 8000 if occupied...
powershell -Command "Get-Process -Name node, python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue" >nul 2>&1

echo [2/3] Starting Django REST Framework Backend on Port 8000...
start "Velora Backend (Django)" cmd /k "cd backend && .venv\Scripts\activate && python manage.py migrate && python manage.py runserver 127.0.0.1:8000"

echo [3/3] Starting Next.js Frontend on Port 3000...
start "Velora Frontend (Next.js)" cmd /k "cd frontend && npm run dev"

echo.
echo Waiting for servers to initialize...
timeout /t 5 /nobreak >nul

echo.
echo Opening Velora in your default browser...
start http://localhost:3000

echo ===================================================
echo Velora is ready and running!
echo - Web App:      http://localhost:3000
echo - Django API:   http://127.0.0.1:8000/api/
echo - Django Admin: http://127.0.0.1:8000/admin/
echo ===================================================
echo Keep the opened terminal windows open while using.
echo Press any key to close this launcher window.
pause >nul
