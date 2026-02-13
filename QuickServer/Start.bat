@echo off
title MRS BLE Scanner - Quick Server
color 0A

echo.
echo ========================================
echo    MRS BLE SCANNER - QUICK SERVER
echo ========================================
echo.
echo Starting local server...
echo.
echo Server Details:
echo   - Web Dashboard: http://localhost:5000
echo   - UDP Server: Port 8081
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Run the Python server from current directory
python TestServer.py

pause
