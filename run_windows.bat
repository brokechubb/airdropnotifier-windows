@echo off
echo Starting Discord Airdrop Notifier (Windows Version)
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv_windows\" (
    echo Creating virtual environment...
    python -m venv venv_windows
)

REM Activate virtual environment
echo Activating virtual environment...
call venv_windows\Scripts\activate.bat

REM Install requirements
echo Installing/updating requirements...
pip install -r requirements.txt

REM Run the script
echo.
echo Starting airdrop notifier...
echo Press Ctrl+C to stop
echo.
python airdropnotif.py

pause
