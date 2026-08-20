# One-Command Startup Script for Touchless Brightness Control
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "  Starting Touchless Brightness Control Application " -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

$backendProcess = Start-Process -FilePath "py" -ArgumentList "-3.11", "-m", "uvicorn", "backend.app.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload" -PassThru -NoNewWindow
Write-Host "[OK] FastAPI Backend Server launched on http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "[OK] API Documentation available on http://127.0.0.1:8000/docs" -ForegroundColor Green

Start-Sleep -Seconds 2

Set-Location frontend
$frontendProcess = Start-Process -FilePath "npm.cmd" -ArgumentList "run", "dev" -PassThru -NoNewWindow
Set-Location ..

Write-Host "[OK] React Dashboard launched on http://127.0.0.1:3000" -ForegroundColor Green
Write-Host "Touchless Brightness Control is running!" -ForegroundColor Cyan
Write-Host "Pinch your Thumb and Index finger in front of the webcam to adjust screen brightness." -ForegroundColor Yellow
Write-Host "Press Ctrl+C to terminate application." -ForegroundColor Gray

try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
} finally {
    Write-Host "Stopping backend and frontend processes..." -ForegroundColor Red
    if ($backendProcess) { Stop-Process -Id $backendProcess.Id -Force -ErrorAction SilentlyContinue }
    if ($frontendProcess) { Stop-Process -Id $frontendProcess.Id -Force -ErrorAction SilentlyContinue }
}
