@echo off
echo Stopping any processes using port 8000...

REM Find and kill processes using port 8000
for /f "tokens=5" %%t in ('netstat -aon ^| findstr :8000') do (
    echo Killing process with PID %%t
    taskkill /f /pid %%t
)

timeout /t 2 /nobreak >nul

echo Starting backend on port 8000...
cd /d "D:\hackthon\hackathon1\humanoid-robotics-textbook\backend"
python -m uvicorn main:app --host 127.0.0.1 --port 8000

pause