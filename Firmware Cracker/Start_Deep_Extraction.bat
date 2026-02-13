@echo off
title DEEP Firmware Cracker - Maximum Extraction
color 0C

echo.
echo ========================================
echo    DEEP FIRMWARE CRACKER v2.0
echo    MAXIMUM DEPTH EXTRACTION
echo ========================================
echo.
echo  This will probe 100+ AT commands
echo  Extraction time: 5-10 minutes
echo  Keep device within BLE range
echo.
echo ========================================
echo.

python CrackFirmware_Deep.py

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to run. Make sure Python is installed.
    pause
)
