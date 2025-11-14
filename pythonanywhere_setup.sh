#!/bin/bash
# Quick setup script for PythonAnywhere
# Run this in the Bash console after uploading your code

echo "==================================="
echo "SEO Analyzer - PythonAnywhere Setup"
echo "==================================="
echo ""

# Get the current directory
CURRENT_DIR=$(pwd)
echo "Current directory: $CURRENT_DIR"
echo ""

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found!"
    echo "Please run this script from the SEO-Analyser directory"
    exit 1
fi

echo "✓ Found app.py"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3.10 -m venv venv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Verify installation
echo "✅ Verifying installation..."
pip list | grep -E "Flask|requests|beautifulsoup4|lxml"
echo ""

echo "==================================="
echo "✨ Setup Complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Go to the Web tab in PythonAnywhere"
echo "2. Create a new web app (Manual configuration, Python 3.10)"
echo "3. Configure the WSGI file (see DEPLOYMENT.md)"
echo "4. Set virtualenv path to: $CURRENT_DIR/venv"
echo "5. Configure static files: /static/ → $CURRENT_DIR/static"
echo "6. Reload your web app"
echo ""
echo "For detailed instructions, see DEPLOYMENT.md"
echo ""

