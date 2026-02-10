#!/bin/bash

# Setup script for Rajasthan Green Cover Monitoring System

echo "🌳 Setting up Rajasthan Green Cover Monitoring System"
echo "======================================================="

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check if earthengine is installed
if pip list | grep -q "earthengine-api"; then
    echo "✓ Earth Engine API installed"
else
    echo "❌ Earth Engine API installation failed"
    exit 1
fi

# Create data directory
mkdir -p data

# Setup Earth Engine
echo ""
echo "🌍 Setting up Google Earth Engine..."
echo "======================================================="
echo "You need to authenticate with Google Earth Engine."
echo "This will open a browser window for authentication."
echo ""
read -p "Press Enter to continue with authentication..."

earthengine authenticate

if [ $? -eq 0 ]; then
    echo "✓ Earth Engine authentication successful"
else
    echo "❌ Earth Engine authentication failed"
    exit 1
fi

# Create .env file
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created. You can customize settings there."
fi

echo ""
echo "======================================================="
echo "✅ Setup complete!"
echo "======================================================="
echo ""
echo "To get started:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the backend analysis:"
echo "     python backend/vegetation_monitor.py"
echo ""
echo "  3. Or start the web dashboard:"
echo "     streamlit run frontend/app.py"
echo ""
echo "  4. Or use the Jupyter notebook:"
echo "     jupyter notebook notebooks/quick_analysis.ipynb"
echo ""
echo "🌳 Happy monitoring!"
