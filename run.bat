@echo off
setlocal
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
title Discord Account Cleaner
cd /d "%~dp0"

REM Find python executable (py launcher or python)
set "PY_CMD="
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PY_CMD=py"
) else (
    python --version >nul 2>&1
    if %errorlevel% equ 0 set "PY_CMD=python"
)

if "%PY_CMD%"=="" (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.10+ from python.org or enable python in PATH.
    pause
    exit /b 1
)

REM Check or create virtual environment
if not exist ".venv\Scripts\python.exe" (
    echo [*] Setting up virtual environment...
    %PY_CMD% -m venv .venv
    if errorlevel 1 (
        echo [!] Failed to create venv. Installing packages globally...
        %PY_CMD% -m pip install -r requirements.txt
        %PY_CMD% main.py
        pause
        exit /b 0
    )
    echo [*] Installing requirements into virtual environment...
    .venv\Scripts\python.exe -m pip install --upgrade pip >nul 2>&1
    .venv\Scripts\python.exe -m pip install -r requirements.txt
)

REM Run cleaner inside venv
.venv\Scripts\python.exe main.py

if errorlevel 1 (
    echo.
    echo [!] Program exited with an error.
    pause
)
