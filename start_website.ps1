param(
    [switch]$InstallDeps = $false
)

Write-Host "Starting Aurovia Website on localhost..." -ForegroundColor Green

# Navigate to backend directory
cd backend

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# Activate virtual environment
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    . .\venv\Scripts\Activate.ps1
}

# Install requirements if requested or if FastAPI is missing
if ($InstallDeps -or -not (Get-Command uvicorn -ErrorAction SilentlyContinue)) {
    Write-Host "Installing dependencies..."
    pip install -r requirements.txt
}

Write-Host "Starting uvicorn server..." -ForegroundColor Cyan
Write-Host "You can access the website at: http://localhost:8000" -ForegroundColor Yellow

# Start the FastAPI server
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
