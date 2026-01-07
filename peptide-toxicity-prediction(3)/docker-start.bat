@echo off
REM Quick start script for Docker (Windows)

echo ==========================================
echo Peptide Toxicity Prediction - Docker Setup
echo ==========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not installed!
    echo.
    echo Please install Docker Desktop:
    echo   https://www.docker.com/products/docker-desktop/
    echo.
    pause
    exit /b 1
)

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not running!
    echo.
    echo Please start Docker Desktop and try again.
    echo.
    pause
    exit /b 1
)

echo Docker is installed and running
echo.

REM Check if trained models exist
if not exist "results\trained_models.pkl" (
    echo Warning: No trained models found.
    echo.
    echo Do you want to train models now? (This will take 10-30 minutes)
    echo Options:
    echo   1) Yes, train models now
    echo   2) No, start app with mock predictions (for testing)
    echo.
    set /p choice="Enter choice (1 or 2): "
    
    if "!choice!"=="1" (
        echo.
        echo Training models...
        docker-compose build
        docker-compose run --rm peptide-app python3 scripts/train_pipeline.py
        echo.
        echo Training complete!
        echo.
    ) else (
        echo.
        echo Skipping training. App will use mock predictions.
        echo.
    )
)

REM Build and start the application
echo Building Docker image (this may take 5-10 minutes first time)...
docker-compose build

echo.
echo Starting application...
docker-compose up -d

echo.
echo ==========================================
echo Application started!
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:3001
echo.
echo To view logs:
echo   docker-compose logs -f
echo.
echo To stop:
echo   docker-compose down
echo ==========================================
echo.
pause

