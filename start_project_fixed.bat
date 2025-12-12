@echo off
echo Starting Humanoid Robotics Textbook Project...

REM Kill any existing processes on the required ports
echo Killing existing processes (if any)...
taskkill /f /im uvicorn.exe >nul 2>&1
taskkill /f /im node.exe >nul 2>&1

REM Start the auth service in the background
echo Starting auth service on port 3002...
cd /d "D:\hackthon\hackathon1\humanoid-robotics-textbook\auth-service"
start /min cmd /c "npm run dev"

REM Wait a moment for the auth service to start
timeout /t 3 /nobreak >nul

REM Start the main backend in the background
echo Starting backend on port 3001...
cd /d "D:\hackthon\hackathon1\humanoid-robotics-textbook\backend"
start /min cmd /c "uvicorn main:app --reload --port 3001"

REM Wait a moment for the backend to start
timeout /t 5 /nobreak >nul

REM Start the Docusaurus website in the background
echo Starting website on port 3003 (auto-selected if 3000 is busy)...
cd /d "D:\hackthon\hackathon1\humanoid-robotics-textbook\website"
start /min cmd /c "npx docusaurus start --port 3003"

echo.
echo All services started!
echo.
echo - Website: http://localhost:3003 (or the port shown after "npx docusaurus start")
echo - Backend: http://localhost:3001 (with API docs at http://localhost:3001/docs)
echo - Auth Service: http://localhost:3002
echo.
echo Please check the individual console windows for any errors.
echo.
echo Press any key to exit...
pause >nul