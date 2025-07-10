#!/bin/bash
set -e

echo "🚀 Setting up ErudaBrowser Development Environment"

# 1️⃣ Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
major_minor=$(echo "$python_version" | cut -d. -f1,2)
echo "📍 Detected Python version: $major_minor"

if python3 -c "import sys; exit(0 if float('$major_minor') >= 3.11 else 1)"; then
    echo "✅ Python version is compatible"
else
    echo "⚠️  Warning: Python 3.11+ recommended for best compatibility"
fi

# 2️⃣ Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 3️⃣ Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# 4️⃣ Install project dependencies
echo "📥 Installing project dependencies..."
pip install -r requirements.txt

# 5️⃣ Install dev tools
echo "🛠️  Installing dev tools (black, isort, flake8)..."
pip install black isort flake8

# 6️⃣ Setup pre-commit hook
echo "🔧 Setting up pre-commit hook for auto formatting..."
HOOK_PATH=".git/hooks/pre-commit"
mkdir -p "$(dirname "$HOOK_PATH")"
cat > "$HOOK_PATH" <<'EOF'
#!/bin/bash
echo "🔍 Running pre-commit formatting checks..."

if ! command -v black >/dev/null 2>&1; then
  echo "⚠️  'black' not found. Install it with: pip install black"
  exit 1
fi

if ! command -v isort >/dev/null 2>&1; then
  echo "⚠️  'isort' not found. Install it with: pip install isort"
  exit 1
fi

black . || exit 1
isort . || exit 1

echo "✅ Code formatted successfully!"
EOF

chmod +x "$HOOK_PATH"
echo "✅ Pre-commit hook installed!"

# 🎉 Done!
echo ""
echo "✅ Dev environment setup complete!"
echo ""
echo "📌 Activate your environment anytime with:"
echo "   source venv/bin/activate"
echo ""
echo "📦 To build the APK for Android:"
echo "   ./build.sh"
echo ""
echo "🧪 To test the app on a desktop system (Linux, macOS, Windows):"
echo "   python3 main.py"
echo ""
