@echo off
echo ========================================
echo   Rock Paper Scissors Game Setup
echo ========================================
echo.

echo [1/5] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment. Make sure Python is installed.
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/5] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies.
    pause
    exit /b 1
)

echo [4/5] Setting up database...
python manage.py migrate
if %errorlevel% neq 0 (
    echo Error: Failed to set up database.
    pause
    exit /b 1
)

echo [5/5] Starting the game server...
echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo   Open your browser and go to:
echo   http://127.0.0.1:8000/
echo.
echo   Press Ctrl+C to stop the server
echo ========================================
echo.

python manage.py runserver