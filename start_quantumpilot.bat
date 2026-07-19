@echo off
setlocal

title QuantumPilot AI Launcher
cd /d "%~dp0"

echo.
echo ==========================================
echo   QuantumPilot AI - Docker Launcher
echo ==========================================
echo.

where docker >nul 2>nul
if errorlevel 1 (
  echo Docker CLI was not found. Please install Docker Desktop first.
  pause
  exit /b 1
)

echo Checking Docker Engine...
docker info >nul 2>nul
if errorlevel 1 (
  echo Docker Engine is not ready. Starting Docker Desktop...
  if exist "C:\Program Files\Docker\Docker\Docker Desktop.exe" (
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
  ) else (
    echo Docker Desktop executable was not found in the default location.
    echo Open Docker Desktop manually, then run this file again.
    pause
    exit /b 1
  )

  echo Waiting for Docker Engine to become ready...
  set /a tries=0
  :wait_docker
  set /a tries+=1
  docker info >nul 2>nul
  if not errorlevel 1 goto docker_ready
  if %tries% geq 60 (
    echo Docker did not become ready after 5 minutes.
    echo Open Docker Desktop manually and try again.
    pause
    exit /b 1
  )
  timeout /t 5 /nobreak >nul
  goto wait_docker
)

:docker_ready
echo Docker is ready.
echo.

echo Starting QuantumPilot AI containers...
docker compose up -d
if errorlevel 1 (
  echo.
  echo Failed to start Docker containers.
  pause
  exit /b 1
)

echo.
echo Waiting for backend health endpoint...
set /a health_tries=0
:wait_health
set /a health_tries+=1
powershell -NoProfile -ExecutionPolicy Bypass -Command "try { $r = Invoke-WebRequest -UseBasicParsing 'http://localhost:8000/api/v1/health' -TimeoutSec 3; if ($r.StatusCode -eq 200) { exit 0 } } catch { exit 1 }" >nul 2>nul
if not errorlevel 1 goto app_ready
if %health_tries% geq 40 (
  echo Backend did not report healthy yet. Opening pages anyway.
  goto open_pages
)
timeout /t 3 /nobreak >nul
goto wait_health

:app_ready
echo Backend is healthy.

:open_pages
echo.
echo Opening QuantumPilot AI...
start "" "http://localhost:3000"
start "" "http://localhost:8000/docs"

echo.
echo Running services:
echo   Frontend:   http://localhost:3000
echo   API Docs:   http://localhost:8000/docs
echo   API Health: http://localhost:8000/api/v1/health
echo   RabbitMQ:   http://localhost:15672
echo.
echo To stop everything later, run:
echo   docker compose down
echo.
pause
