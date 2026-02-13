@echo off
title MRS BLE Scanner V0.2 - Professional Network Diagnostics
color 0A

echo.
echo ========================================================================
echo   MRS BLE SCANNER V0.2 - PROFESSIONAL NETWORK DIAGNOSTICS
echo ========================================================================
echo.
echo   Features:
echo   - BLE Device Scanning and Connection
echo   - HTTP Data Forwarding
echo   - Automatic Network Diagnostics
echo   - PDF Report Generation
echo.
echo ========================================================================
echo.


REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [OK] Python detected
echo.

REM Create reports directory if it doesn't exist
if not exist "reports" (
    mkdir reports
    echo [SETUP] Created reports directory
)

echo [STARTING] Launching MRS BLE Scanner V0.2...
echo.
echo ========================================================================
echo.

REM Run the scanner
python Scanner.py

echo.
echo ========================================================================
echo   Session ended
echo ========================================================================
echo.
pause
