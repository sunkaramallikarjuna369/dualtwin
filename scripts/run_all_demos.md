# Quick Start Commands - Run All Demos

This document provides fast commands to launch key demonstrations across all concept modules.

## Prerequisites

Ensure you have completed the setup:
```bash
# Linux/Mac
./scripts/setup_env.sh

# Windows
scripts\setup_env.bat
```

Or manually:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## Running Python Demos

### All Concepts - Quick Run

```bash
# From repository root, with virtual environment activated

# 01 - Digital Twin Fundamentals
python concepts/01_digital_twin_fundamentals/code/main_01_digital_twin_fundamentals.py

# 02 - Dual-Twin Architecture
python concepts/02_dual_twin_architecture/code/main_02_dual_twin_architecture.py

# 03 - IoT and Sensor Data Streams
python concepts/03_iot_and_sensor_data_streams/code/main_03_iot_and_sensor_data_streams.py

# 04 - Data Models and Semantics
python concepts/04_data_models_and_semantics/code/main_04_data_models_and_semantics.py

# 05 - Simulation and Physics Models
python concepts/05_simulation_and_physics_models/code/main_05_simulation_and_physics_models.py

# 06 - Twin Lifecycle Management
python concepts/06_twin_lifecycle_management/code/main_06_twin_lifecycle_management.py

# 07 - Cloud Edge Integration
python concepts/07_cloud_edge_integration_for_twins/code/main_07_cloud_edge_integration.py

# 08 - AI and Analytics on Twins
python concepts/08_ai_and_analytics_on_twins/code/main_08_ai_and_analytics.py

# 09 - GenAI with Digital Twins
python concepts/09_genai_with_digital_twins/code/main_09_genai_with_twins.py

# 10 - Twin Security and Access Control
python concepts/10_twin_security_and_access_control/code/main_10_twin_security.py

# 11 - Industry Use Cases
python concepts/11_industry_use_cases/code/main_11_industry_use_cases.py

# 12 - Governance, Compliance, and Standards
python concepts/12_governance_compliance_and_standards/code/main_12_governance.py

# 13 - Business Value and KPIs
python concepts/13_business_value_and_kpis_for_twins/code/main_13_business_value.py

# 14 - Future Trends
python concepts/14_future_trends/code/main_14_future_trends.py
```

## Running Jupyter Notebooks

### Start Jupyter Lab
```bash
jupyter lab
```

Then navigate to any concept folder and open the notebooks:
- `intro_*.ipynb` - Start here for concept introduction
- `examples_*.ipynb` - Practical examples
- `exercises_*.ipynb` - Hands-on practice

### Run Notebooks from Command Line
```bash
# Execute a notebook and save output
jupyter nbconvert --to notebook --execute concepts/01_digital_twin_fundamentals/intro_01_digital_twin_fundamentals.ipynb
```

## Viewing HTML Demos

### Option 1: Direct Browser Opening
Simply open the HTML file in your browser:
```bash
# Linux
xdg-open concepts/01_digital_twin_fundamentals/html_demo/index.html

# Mac
open concepts/01_digital_twin_fundamentals/html_demo/index.html

# Windows
start concepts\01_digital_twin_fundamentals\html_demo\index.html
```

### Option 2: Local HTTP Server
For a better experience with all demos:
```bash
# From repository root
python -m http.server 8080

# Then open http://localhost:8080 in your browser
# Navigate to concepts/<concept>/html_demo/
```

### Option 3: VS Code Live Server
If using VS Code with the Live Server extension:
1. Right-click on any `index.html` file
2. Select "Open with Live Server"

## Recommended Learning Sequence

### For Non-Technical Users
```bash
# Start with fundamentals
python concepts/01_digital_twin_fundamentals/code/main_01_digital_twin_fundamentals.py

# Then architecture
python concepts/02_dual_twin_architecture/code/main_02_dual_twin_architecture.py

# Understand data sources
python concepts/03_iot_and_sensor_data_streams/code/main_03_iot_and_sensor_data_streams.py

# Lifecycle concepts
python concepts/06_twin_lifecycle_management/code/main_06_twin_lifecycle_management.py

# Real-world applications
python concepts/11_industry_use_cases/code/main_11_industry_use_cases.py

# Business perspective
python concepts/13_business_value_and_kpis_for_twins/code/main_13_business_value.py

# What's next
python concepts/14_future_trends/code/main_14_future_trends.py
```

### For Technical Users
Follow the complete sequence from 01 through 14 for comprehensive coverage.

## Troubleshooting

### Import Errors
Ensure you're in the repository root and the virtual environment is activated:
```bash
cd /path/to/dualtwin
source .venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Jupyter Kernel Issues
```bash
# Install kernel for virtual environment
python -m ipykernel install --user --name=dualtwin360
```

### HTML Demos Not Loading
- Check that JavaScript is enabled in your browser
- Try a different browser (Chrome, Firefox, Edge recommended)
- Use the local HTTP server method instead of direct file opening
