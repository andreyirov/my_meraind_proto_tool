#!/bin/bash
echo "Starting AI Diagram Generator..."

# Determine python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "Error: Python is not installed."
    exit 1
fi

echo "Using Python: $PYTHON_CMD"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing/Checking dependencies..."
pip install -r web_service/backend/requirements.txt

# Run the server
echo "Starting server at http://127.0.0.1:8000"
cd web_service/backend
python -m uvicorn main:app --reload --port 8000
