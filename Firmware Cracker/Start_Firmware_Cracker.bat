@echo off
title Firmware Cracker - Extract Sensor Intelligence
color 0A

echo.
echo ========================================
echo    FIRMWARE CRACKER v1.0
echo    Extract ALL Sensor Intelligence
echo ========================================
echo.

python CrackFirmware.py

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to run. Make sure Python is installed.
    pause
)
