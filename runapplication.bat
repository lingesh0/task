@echo off
echo Starting Deep Work Session Tracker...
echo.

echo Starting backend server...
start "Backend Server" cmd /k "call env\Scripts\activate && python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo Waiting for backend to start...
timeout /t 3 /nobreak > nul

echo.
echo Starting frontend development server...
start "Frontend Server" cmd /k "cd frontend && npm start"

echo.
echo Both servers are starting up...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window (servers will continue running)
pause > nul
