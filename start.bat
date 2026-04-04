@echo off
REM Start the LLM Knowledge Base system (Windows)

echo Starting LLM Knowledge Base...

if not exist ".env" (
    echo.
    echo [ERROR] .env file not found!
    echo Please create .env from .env.example and add your ANTHROPIC_API_KEY
    pause
    exit /b 1
)

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -q -r requirements.txt

echo Initializing directories...
if not exist "data\raw" mkdir data\raw
if not exist "data\wiki" mkdir data\wiki
if not exist "data\output" mkdir data\output

echo Starting backend API on port 8000...
cd backend
start python main.py
cd ..

timeout /t 2

echo.
echo Backend started successfully!
echo.
echo Frontend available at: frontend\index.html
echo.
echo API available at: http://localhost:8000
echo API docs at: http://localhost:8000/docs
echo.
echo CLI available at: cd cli ^&^& python main.py
echo.
pause
