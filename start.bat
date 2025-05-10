@echo off
cd /d "%~dp0"

echo Activating virtual environment...

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo Virtual environment activated.
) else (
    echo No virtual environment found. Creating one...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Virtual environment created and activated.
)

if exist "backend\requirements.txt" (
    echo Installing backend dependencies...
    pip install -r backend\requirements.txt
)

echo Starting Flask server...
start cmd /k "cd backend && set FLASK_APP=app.py && set FLASK_ENV=development && flask run"

echo Starting React frontend...
start cmd /k "cd frontend && npm install && npm start"

pause