#!/bin/bash
cd ffllaapp # Your app working directory!!!
export PORT=5000
unset PIP_USER

# Create venv if not exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment with system site packages..."
    python3 -m venv venv --system-site-packages
fi

# Activate
source venv/bin/activate

# Try install (might fail if pip is broken, but packages should be there from packager_tool)
if [ -f "requirements.txt" ]; then
    echo "Checking dependencies..."
    # We skip pip install if it fails, assuming packager_tool handled it
    pip install -r requirements.txt || echo "Pip install failed, but continuing as packages might be pre-installed via system."
fi

echo "Starting application..."
cd ffllaapp/crm
export PYTHONPATH=..
python -m crm.main