#!/bin/bash

echo "========================================"
echo "   Rock Paper Scissors Game Setup"
echo "========================================"
echo

echo "[1/5] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment. Make sure Python 3 is installed."
    exit 1
fi

echo "[2/5] Activating virtual environment..."
source venv/bin/activate

echo "[3/5] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies."
    exit 1
fi

echo "[4/5] Setting up database..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "Error: Failed to set up database."
    exit 1
fi

echo "[5/5] Starting the game server..."
echo
echo "========================================"
echo "   Setup Complete!"
echo "========================================"
echo "   Open your browser and go to:"
echo "   http://127.0.0.1:8000/"
echo
echo "   Press Ctrl+C to stop the server"
echo "========================================"
echo

python manage.py runserver