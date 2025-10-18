#!/bin/bash

# Deep Work Session Tracker - Development Setup Script
# This script sets up the development environment for both backend and frontend

echo "🚀 Setting up Deep Work Session Tracker Development Environment"
echo "=============================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ from https://python.org"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ from https://nodejs.org"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm (comes with Node.js)"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Backend setup
echo ""
echo "🔧 Setting up Backend..."
echo "------------------------"

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv env

# Activate virtual environment
echo "Activating virtual environment..."
source env/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations
echo "Setting up database..."
alembic upgrade head

echo "✅ Backend setup complete"

# Frontend setup
echo ""
echo "🎨 Setting up Frontend..."
echo "-------------------------"

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "✅ Frontend setup complete"

echo ""
echo "🎉 Setup complete! You can now run the application with:"
echo "   ./runapplication.sh"
echo ""
echo "Or manually start:"
echo "   Backend:  python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000"
echo "   Frontend: cd frontend && npm start"
echo ""
echo "Access the application at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
