# AI Tutor Orchestrator - Setup Script
# Run this script to set up the complete project

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AI Tutor Orchestrator Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found! Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✓ Found Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found! Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Backend Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Backend setup
Set-Location backend

Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Backend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install backend dependencies" -ForegroundColor Red
    exit 1
}

# Check for .env file
if (-not (Test-Path .env)) {
    Write-Host ""
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "✓ Created .env file" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: Edit backend/.env and add your Gemini API key!" -ForegroundColor Red
    Write-Host "   Get your free key at: https://makersuite.google.com/app/apikey" -ForegroundColor Yellow
} else {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
}

Set-Location ..

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Frontend Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Frontend setup
Set-Location frontend

Write-Host "Installing Node dependencies (this may take a few minutes)..." -ForegroundColor Yellow
npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Frontend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install frontend dependencies" -ForegroundColor Red
    Write-Host "   Try: npm install --legacy-peer-deps" -ForegroundColor Yellow
}

Set-Location ..

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Add your Gemini API key to backend/.env" -ForegroundColor White
Write-Host "2. Open 3 terminal windows and run:" -ForegroundColor White
Write-Host ""
Write-Host "   Terminal 1 (Tools Service):" -ForegroundColor Yellow
Write-Host "   cd backend" -ForegroundColor White
Write-Host "   python tools_main.py" -ForegroundColor White
Write-Host ""
Write-Host "   Terminal 2 (Orchestrator):" -ForegroundColor Yellow
Write-Host "   cd backend" -ForegroundColor White
Write-Host "   python main.py" -ForegroundColor White
Write-Host ""
Write-Host "   Terminal 3 (Frontend):" -ForegroundColor Yellow
Write-Host "   cd frontend" -ForegroundColor White
Write-Host "   npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "3. Open browser: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions, see README.md" -ForegroundColor Gray
Write-Host ""
