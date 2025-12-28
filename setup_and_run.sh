#!/bin/bash

# Setup and run script for FastAPI Leaflet Map application

echo "Setting up FastAPI Leaflet Map application..."

# Create and activate virtual environment
echo "Creating virtual environment..."
cd backend
python -m venv venv

# Activate virtual environment (different syntax for different shells)
echo "Activating virtual environment..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "Virtual environment activated (bash/zsh)"
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
    echo "Virtual environment activated (Windows)"
else
    echo "Could not find virtual environment activation script"
    exit 1
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Seed the database with sample data
echo "Seeding database with sample cities..."
python seed_db.py

# Check if port 8000 is in use and kill the process if needed
echo "Checking for existing processes on port 8000..."
PORT=8000
PID=$(lsof -t -i :$PORT)

if [ ! -z "$PID" ]; then
    echo "Found process $PID using port $PORT. Killing it..."
    kill -9 $PID
    sleep 1  # Give the process time to terminate
    echo "Port $PORT is now free."
else
    echo "Port $PORT is available."
fi

# Start the FastAPI server
echo "Starting FastAPI server on http://localhost:8000..."
echo "Press Ctrl+C to stop the server"
python -m uvicorn app.main:app --reload

cd ..
