@echo off
TITLE AI Guitar Pedal - Core Initiation Sequence
COLOR 0A
echo =======================================================
echo          🎸 AI GUITAR PEDAL - SYSTEM LAUNCHER
echo =======================================================
echo.

echo [1/3] Checking Docker daemon status...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running or not installed.
    echo Please start Docker Desktop and try again.
    pause
    exit /b
)
echo [OK] Docker is running.
echo.

echo [2/3] Spinning up PostgreSQL & AI Backend via Docker-Compose...
docker-compose up -d --build
echo.

echo [3/3] Waiting for AI Matrix to stabilize (10 seconds)...
timeout /t 10 /nobreak >nul
echo.

echo 🌐 Launching the UI Control Panel...
start http://localhost:8000/

echo.
echo =======================================================
echo ✅ SYSTEM ONLINE. You can now close this terminal.
echo To stop the pedal stack later, run: docker-compose down
echo =======================================================
pause
