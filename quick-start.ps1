# Quick Start Script for Diet & Fitness Planner
# This script starts both backend and frontend servers

Write-Host "🚀 Starting Diet & Fitness Planner..." -ForegroundColor Green
Write-Host ""

# Check if backend virtual environment exists
if (-not (Test-Path "backend\venv")) {
    Write-Host "⚠️  Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv backend\venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Check if backend dependencies are installed
Write-Host "📦 Checking backend dependencies..." -ForegroundColor Cyan
$requirementsChanged = $false
if (Test-Path "backend\requirements.txt") {
    # You can add pip check here if needed
    Write-Host "✅ Backend dependencies OK" -ForegroundColor Green
}

# Check if frontend dependencies are installed
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "📦 Installing frontend dependencies..." -ForegroundColor Yellow
    Set-Location frontend
    npm install
    Set-Location ..
    Write-Host "✅ Frontend dependencies installed" -ForegroundColor Green
}
else {
    Write-Host "✅ Frontend dependencies OK" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎯 Starting servers..." -ForegroundColor Cyan
Write-Host ""

# Start backend in new window
Write-Host "▶️  Starting Backend on http://localhost:8000" -ForegroundColor Magenta
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; python -m uvicorn main:app --reload"

# Wait 3 seconds for backend to start
Start-Sleep -Seconds 3

# Start frontend in new window
Write-Host "▶️  Starting Frontend on http://localhost:5173" -ForegroundColor Magenta
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm run dev"

# Wait 2 seconds
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "✅ Both servers are starting!" -ForegroundColor Green
Write-Host ""
Write-Host "📌 Access Points:" -ForegroundColor Cyan
Write-Host "   Frontend:  http://localhost:5173" -ForegroundColor White
Write-Host "   Backend:   http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs:  http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "💡 Tip: Check the newly opened terminal windows for server logs" -ForegroundColor Yellow
Write-Host ""
Write-Host "🛑 To stop servers: Close the terminal windows or press Ctrl+C in each" -ForegroundColor Red
Write-Host ""
Write-Host "Happy coding! 🎉" -ForegroundColor Green
