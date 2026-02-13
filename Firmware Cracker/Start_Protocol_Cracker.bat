@echo off
title Protocol Cracker - Custom Command Discovery
color 0E

echo.
echo ========================================
echo    CUSTOM PROTOCOL CRACKER v1.0
echo    Brute Force Command Discovery
echo ========================================
echo.
echo  This will test 200+ command variations
echo  Analysis time: 5-10 minutes
echo  Keep device within BLE range
echo.
echo ========================================
echo.

python ProtocolCracker.py

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to run. Make sure Python is installed.
    pause
)
