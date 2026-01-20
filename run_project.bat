@echo off
echo ========================================
echo    Government Intelligence Platform
echo    Installing Dependencies...
echo ========================================
echo.

REM Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo ========================================
echo    Starting Server...
echo    Open: http://localhost:8000
echo ========================================
echo.

REM Start the FastAPI server
python main.py

pause
