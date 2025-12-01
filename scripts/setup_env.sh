#!/bin/bash
# DualTwin Technologies 360° - Environment Setup Script (Linux/Mac)

set -e

echo "=============================================="
echo "  DualTwin Technologies 360° Setup"
echo "=============================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.10 or higher is required. Found: $python_version"
    exit 1
fi
echo "Python version: $python_version ✓"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "Virtual environment created ✓"
else
    echo "Virtual environment already exists ✓"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source .venv/bin/activate
echo "Virtual environment activated ✓"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "Pip upgraded ✓"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
echo "Dependencies installed ✓"

# Verify installation
echo ""
echo "Verifying installation..."
python3 -c "import numpy; import pandas; import matplotlib; import plotly; print('Core packages verified ✓')"
python3 -c "import jupyterlab; print('Jupyter Lab verified ✓')"

echo ""
echo "=============================================="
echo "  Setup Complete!"
echo "=============================================="
echo ""
echo "To activate the environment in the future, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To start Jupyter Lab, run:"
echo "  jupyter lab"
echo ""
echo "To run a concept demo, navigate to the concept folder and run:"
echo "  python code/main_<concept_slug>.py"
echo ""
echo "Happy learning!"
