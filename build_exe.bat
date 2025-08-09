@echo off
echo ================================================================
echo    Discord Airdrop Notifier - Executable Builder
echo ================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists, create if not
if not exist "venv_build\" (
    echo Creating build virtual environment...
    python -m venv venv_build
)

REM Activate virtual environment
echo Activating virtual environment...
call venv_build\Scripts\activate.bat

REM Install/upgrade requirements
echo Installing build requirements...
pip install --upgrade pip
pip install -r requirements.txt

REM Clean previous build artifacts
echo Cleaning previous build artifacts...
if exist "build\" rmdir /s /q "build"
if exist "dist\" rmdir /s /q "dist"
if exist "__pycache__\" rmdir /s /q "__pycache__"
if exist "*.pyc" del /q "*.pyc"

REM Build the executable
echo.
echo Building executable...
echo This may take several minutes...
echo.
pyinstaller --clean airdropnotif.spec

REM Check if build was successful
if exist "dist\DiscordAirdropNotifier.exe" (
    echo.
    echo ================================================================
    echo    BUILD SUCCESSFUL!
    echo ================================================================
    echo.
    echo Executable created: dist\DiscordAirdropNotifier.exe
    echo File size: 
    dir "dist\DiscordAirdropNotifier.exe" | findstr "DiscordAirdropNotifier.exe"
    echo.
    echo You can now distribute this single .exe file!
    echo.
    echo IMPORTANT: Remember to edit your Discord token before distributing!
    echo The token is embedded in the executable.
    echo.
) else (
    echo.
    echo ================================================================
    echo    BUILD FAILED!
    echo ================================================================
    echo.
    echo Check the output above for error messages.
    echo Common issues:
    echo - Missing dependencies
    echo - Antivirus blocking PyInstaller
    echo - Insufficient disk space
    echo.
)

echo Press any key to exit...
pause
