@echo off
echo Starting Humanoid Robotics Textbook services...

REM Start the auth service in the background
echo Starting auth service on port 3002...
cd auth-service
start npm run dev

REM Wait a moment for the auth service to start
timeout /t 3 /nobreak >nul

REM Start the main backend in the background
echo Starting backend on port 8000...
cd ../backend
start uvicorn main:app --host 0.0.0.0 --port 8000 --reload

REM Wait a moment for the backend to start
timeout /t 3 /nobreak >nul

REM Start the Docusaurus website in the background
echo Starting website on port 3000...
cd ../website
start npm run start

echo All services started!
echo.
echo - Auth Service: http://localhost:3002
echo - Backend: http://localhost:8000
echo - Website: http://localhost:3000
echo.
echo Press any key to exit...
pause >nul