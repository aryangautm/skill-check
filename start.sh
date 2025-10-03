#!/bin/bash

# Startup script for Skill Check API

echo "Starting Skill Check API..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please copy .env.example to .env and fill in your configuration:"
    echo "  cp .env.example .env"
    echo ""
    echo "Required environment variables:"
    echo "  - DATABASE_URL: PostgreSQL connection string"
    echo "  - GEMINI_API_KEY: Google Gemini API key"
    echo "  - SECRET_KEY: Application secret key"
    exit 1
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Warning: No virtual environment detected."
    echo "Consider activating a virtual environment first:"
    echo "  python -m venv venv"
    echo "  source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
    echo ""
fi

# Check if dependencies are installed
if ! python -c "import fastapi" &> /dev/null; then
    echo "Error: Dependencies not installed!"
    echo "Please install dependencies first:"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Start the server
echo "Starting uvicorn server..."
echo "API will be available at: http://localhost:8000"
echo "API documentation at: http://localhost:8000/docs"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
