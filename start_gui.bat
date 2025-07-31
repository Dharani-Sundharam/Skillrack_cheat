@echo off
title SkillRack Automation Suite
color 0A
echo.
echo  ==========================================
echo   🚀 SkillRack Automation Suite
echo  ==========================================
echo.
echo  Starting GUI application...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo  ❌ Python is not installed or not in PATH
    echo  Please install Python 3.8+ from https://python.org
    echo.
    pause
    exit /b 1
)

REM Try to run the GUI launcher
if exist "run_gui.py" (
    echo  ✅ Launching GUI...
    python run_gui.py
) else if exist "skillrack_gui.py" (
    echo  ✅ Launching GUI directly...
    python skillrack_gui.py
) else (
    echo  ❌ GUI files not found!
    echo  Please ensure you're in the correct directory.
    echo.
    pause
    exit /b 1
)

echo.
echo  👋 GUI closed. Thanks for using SkillRack Automation!
pause