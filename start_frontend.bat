@echo off
echo Stopping any processes using port 3000...

REM Find and kill processes using port 3000
for /f "tokens=5" %%t in ('netstat -aon ^| findstr :3000') do (
    echo Killing process with PID %%t
    taskkill /f /pid %%t
)

timeout /t 2 /nobreak >nul

echo Starting frontend on port 3000...
cd /d "D:\hackthon\hackathon1\humanoid-robotics-textbook\website"
npm run start

pause