# Start Both Frontend and Backend
# This script starts both servers in separate windows

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Starting AI Diet & Fitness App" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if setup has been run
if (-not (Test-Path "$RootDir\backend\venv")) {
    Write-Host "⚠ Virtual environment not found. Running setup first..." -ForegroundColor Yellow
    & "$RootDir\setup.ps1"
    Write-Host ""
    Write-Host "Setup complete. Press any key to start the application..." -ForegroundColor Green
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

# Start Backend in new window
Write-Host "Starting Backend Server..." -ForegroundColor Yellow
$backendScript = @"
Set-Location '$RootDir\backend'
.\venv\Scripts\Activate.ps1
Write-Host 'Backend Starting...' -ForegroundColor Green
uvicorn main:app --reload
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript

# Wait a bit for backend to start
Write-Host "Waiting for backend to initialize..." -ForegroundColor Cyan
Start-Sleep -Seconds 3

# Start Frontend in new window
Write-Host "Starting Frontend Server..." -ForegroundColor Yellow
$frontendScript = @"
Set-Location '$RootDir\frontend'
Write-Host 'Frontend Starting...' -ForegroundColor Green
npm run dev
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript

# Wait a bit for frontend to start
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "✓ Application Started!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host "Opening browser in 3 seconds..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Open browser
Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "Two new windows have been opened:" -ForegroundColor White
Write-Host "  1. Backend Server (FastAPI)" -ForegroundColor Gray
Write-Host "  2. Frontend Server (Vite)" -ForegroundColor Gray
Write-Host ""
Write-Host "To stop the servers, press CTRL+C in each window." -ForegroundColor Yellow
Write-Host ""
Write-Host "You can close this window now." -ForegroundColor Gray
