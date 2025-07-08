#!/bin/bash
set -e

echo "🚀 Setting up ErudaBrowser Development Environment"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
echo "📍 Detected Python version: $python_version"

if [[ $(echo "$python_version >= 3.11" | bc -l 2>/dev/null || python3 -c "import sys; print(float('${python_version}') >= 3.11)") == "True" || $(echo "$python_version >= 3.11" | bc -l 2>/dev/null || python3 -c "import sys; print(float('${python_version}') >= 3.11)") == "1" ]]; then
    echo "✅ Python version is compatible"
else
    echo "⚠️  Warning: Python 3.11+ recommended for best compatibility"
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Install additional development tools
echo "🔧 Installing development tools..."
pip install black flake8 isort

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "🔥 To activate the environment:"
echo "   source venv/bin/activate"
echo ""
echo "🏗️  To build APK locally (requires Android SDK):"
echo "   ./build.sh"
echo ""
echo "🧪 To run the app for testing:"
echo "   python3 main.py"
echo ""
echo "📱 For Android builds, use GitHub Actions or set up Android SDK locally"