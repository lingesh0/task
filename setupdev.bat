@echo off
echo Setting up Deep Work Session Tracker development environment...
echo.

echo Setting up backend...
python -m venv env
call env\Scripts\activate
pip install -r requirements.txt

echo.
echo Running database migrations...
alembic upgrade head

echo.
echo Setting up frontend...
cd frontend
npm install
cd ..

echo.
echo Development environment setup complete!
echo.
echo To start the application, run: runapplication.bat
echo.
pause
