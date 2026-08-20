# Windows PowerShell Setup Script for Touchless Brightness Control
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host " Touchless Brightness Control - Setup Environment" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

$pythonExe = (Get-Command py).Source
if (-not $pythonExe) {
    $pythonExe = (Get-Command python).Source
}

Write-Host "[1/3] Creating Python Virtual Environment (venv)..." -ForegroundColor Yellow
py -3.11 -m venv venv

Write-Host "[2/3] Installing Backend Dependencies..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1
py -3.11 -m pip install --upgrade pip
py -3.11 -m pip install -r backend/requirements.txt

Write-Host "[3/3] Installing Frontend Dependencies..." -ForegroundColor Yellow
Set-Location frontend
npm install
Set-Location ..

Write-Host "`nEnvironment Setup Complete!" -ForegroundColor Green
Write-Host "Run '.\scripts\start_application.ps1' to launch application." -ForegroundColor Cyan
