# come on — Universal Video & Media Downloader

A full-stack, production-ready video downloader web application built with a **Next.js (React 19)** frontend and a **Django + Django REST Framework** backend.

GitHub Repository: [https://github.com/NithanthHarsha/video_downloader.git](https://github.com/NithanthHarsha/video_downloader.git)

---

## 📁 Repository Structure

```
video_downloader/
├── backend/                  # Django REST Framework API (Deploy as Backend)
│   ├── config/               # Project settings, wsgi, urls
│   ├── downloader/           # Downloader app (models, views, services, validators)
│   ├── manage.py
│   ├── requirements.txt      # Python dependencies (Django, DRF, yt-dlp, gunicorn, etc.)
│   ├── Procfile              # Production process entrypoint
│   └── .env.example
├── frontend/                 # Next.js 16 App (Deploy as Frontend)
│   ├── app/                  # App router (/, /features, /privacy)
│   ├── components/           # UI components
│   ├── lib/                  # API client & types
│   ├── package.json          # Node dependencies
│   └── .env.example
├── .gitignore                # Root gitignore protecting secrets & temp files
└── start.bat                 # Windows local 1-click launcher
```

---

## 🚀 Deployment Guide

### 1. Push to GitHub

Initialize and push the repository to GitHub:

```bash
# Initialize git if not already initialized
git init

# Add all project files (safe .gitignore prevents uploading .env, .venv, node_modules, etc.)
git add .

# Commit
git commit -m "feat: complete full-stack video downloader ready for deployment"

# Set remote repository
git remote add origin https://github.com/NithanthHarsha/video_downloader.git
git branch -M main

# Push to GitHub
git push -u origin main
```

---

### 2. Deploy Backend (Django)

Deploy the `backend/` folder on **Render**, **Railway**, **Heroku**, or any Linux VPS / container service.

- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt && python manage.py migrate`
- **Start Command**: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 3600`
- **Environment Variables**:
  ```env
  SECRET_KEY=your-secure-random-secret-key-here
  DEBUG=False
  ALLOWED_HOSTS=localhost,127.0.0.1,.onrender.com,.railway.app,your-custom-domain.com
  CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
  MAX_DOWNLOAD_SIZE_MB=10240
  DOWNLOAD_TIMEOUT=3600
  RATE_LIMIT=40/minute
  ```

---

### 3. Deploy Frontend (Next.js)

Deploy the `frontend/` folder on **Vercel**, **Netlify**, or **Cloudflare Pages**.

- **Root Directory**: `frontend`
- **Framework Preset**: `Next.js`
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Environment Variables**:
  ```env
  NEXT_PUBLIC_API_URL=https://your-backend-api.onrender.com
  ```
  *(Set this to your deployed Django backend URL without a trailing slash)*

---

## 💻 Local Development

### Option 1: 1-Click Launcher (Windows)
Double-click `start.bat` in the root folder.

### Option 2: Run in Two Terminals

#### Terminal 1 — Backend (Django):
```bash
cd backend
python -m venv .venv
# Windows: .\.venv\Scripts\activate | Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

#### Terminal 2 — Frontend (Next.js):
```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🧪 Testing & Validation

```bash
# Run backend tests
cd backend
python manage.py test

# Validate frontend production build
cd frontend
npm run build
```

---

## 🔒 Legal & Compliance Notice

This application is strictly designed for downloading public media that you own, have explicit legal rights to, or is in the public domain. It strictly refuses and contains no mechanisms to bypass DRM, copy protections, or private access controls.
