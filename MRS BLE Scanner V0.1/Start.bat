@echo off
title MRS BLE Tools Installer & Launcher
cls

echo ====================================================
echo      MRS BLE Tools - Auto Launcher
echo ====================================================
echo.


:: Try python first
python --version >nul 2>&1
if %errorlevel% equ 0 goto found_python

:: Try py launcher
py --version >nul 2>&1
if %errorlevel% equ 0 goto found_py

:: Python not found
goto not_found

:found_python
echo [i] Found Python (command: python)
echo [i] Checking dependencies...
python -m pip show bleak >nul 2>&1
if %errorlevel% neq 0 goto install_bleak_python
echo [i] Dependencies all good.
goto run_python

:install_bleak_python
echo [i] Installing BLE library (bleak)...
python -m pip install bleak
echo [i] Dependencies installed.
goto run_python

:run_python
echo.
echo [i] Starting Scanner...
echo ====================================================
python Scanner.py
goto end

:found_py
echo [i] Found Python Launcher (command: py)
echo [i] Checking dependencies...
py -m pip show bleak >nul 2>&1
if %errorlevel% neq 0 goto install_bleak_py
echo [i] Dependencies all good.
goto run_py

:install_bleak_py
echo [i] Installing BLE library (bleak)...
py -m pip install bleak
echo [i] Dependencies installed.
goto run_py

:run_py
echo.
echo [i] Starting Scanner...
echo ====================================================
py Scanner.py
goto end

:not_found
echo [!] Python command was not found in your standard PATH.
echo.
echo     If you KNOW you have Python installed, you might just need to restart your PC
echo     or reinstall it with "Add to PATH" checked.
echo.
set /p INSTALL_CHOICE="Do you want this script to download and install Python 3.11 now? (Y/N): "
if /i "%INSTALL_CHOICE%"=="Y" goto do_install
echo.
echo [i] Aborting. Please install Python manually.
goto end

:do_install
echo [i] Downloading and Installing Python...
winget install -e --id Python.Python.3.11 --scope machine
echo.
echo [i] Python installation complete. Please RESTART this script.
goto end

:end
pause
