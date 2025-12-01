@echo off
REM DualTwin Technologies 360° - Environment Setup Script (Windows)

echo ==============================================
echo   DualTwin Technologies 360° Setup
echo ==============================================
echo.

REM Check Python version
echo Checking Python version...
python --version 2>nul
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo.
    echo Creating virtual environment...
    python -m venv .venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
pip install --upgrade pip --quiet

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt --quiet
echo Dependencies installed

REM Verify installation
echo.
echo Verifying installation...
python -c "import numpy; import pandas; import matplotlib; import plotly; print('Core packages verified')"
python -c "import jupyterlab; print('Jupyter Lab verified')"

echo.
echo ==============================================
echo   Setup Complete!
echo ==============================================
echo.
echo To activate the environment in the future, run:
echo   .venv\Scripts\activate.bat
echo.
echo To start Jupyter Lab, run:
echo   jupyter lab
echo.
echo To run a concept demo, navigate to the concept folder and run:
echo   python code\main_^<concept_slug^>.py
echo.
echo Happy learning!
