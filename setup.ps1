# AI Diet & Fitness Planner - Setup Script
# This script automates the setup process for Windows

Write-Host "================================" -ForegroundColor Cyan
Write-Host "AI Diet & Fitness Planner Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Get the directory where this script is located
$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check Python installation
Write-Host "[1/6] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "✗ Python not found. Please install Python 3.8+ from https://www.python.org/" -ForegroundColor Red
    exit 1
}

# Check Node.js installation
Write-Host "[2/6] Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Found: Node.js $nodeVersion" -ForegroundColor Green
}
catch {
    Write-Host "✗ Node.js not found. Please install Node.js from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Setup Backend
Write-Host "[3/6] Setting up Backend..." -ForegroundColor Yellow
Set-Location "$RootDir\backend"

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Cyan
    python -m venv venv
}

# Activate virtual environment and install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Cyan
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt --quiet
Write-Host "✓ Backend setup complete" -ForegroundColor Green

# Setup Frontend
Write-Host "[4/6] Setting up Frontend..." -ForegroundColor Yellow
Set-Location "$RootDir\frontend"

if (-not (Test-Path "node_modules")) {
    Write-Host "Installing Node.js dependencies (this may take a few minutes)..." -ForegroundColor Cyan
    npm install --silent
    Write-Host "✓ Frontend setup complete" -ForegroundColor Green
}
else {
    Write-Host "✓ Dependencies already installed" -ForegroundColor Green
}

# Verify .env file
Write-Host "[5/6] Checking configuration..." -ForegroundColor Yellow
Set-Location "$RootDir\backend"
if (Test-Path ".env") {
    Write-Host "✓ .env file found" -ForegroundColor Green
}
else {
    Write-Host "⚠ .env file not found, creating from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✓ .env file created" -ForegroundColor Green
}

# Summary
Write-Host ""
Write-Host "[6/6] Setup Complete! 🎉" -ForegroundColor Green
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Start the Backend:" -ForegroundColor White
Write-Host "   cd '$RootDir\backend'" -ForegroundColor Gray
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "   uvicorn main:app --reload" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Start the Frontend (in a NEW terminal):" -ForegroundColor White
Write-Host "   cd '$RootDir\frontend'" -ForegroundColor Gray
Write-Host "   npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Open your browser to: http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "For more details, see README.md or QUICKSTART.md" -ForegroundColor Cyan
Write-Host ""

Set-Location $RootDir
