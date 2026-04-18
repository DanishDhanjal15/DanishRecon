@echo off
title Scout - Security Assistant
echo ==========================================
echo   Scout - Security Assistant
echo   Open browser at http://localhost:8765
echo ==========================================
echo.
cd /d "%~dp0"
pip install -r requirements.txt -q 2>nul
start http://localhost:8765
python scout.py
pause
