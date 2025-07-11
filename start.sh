#!/data/data/com.termux/files/usr/bin/bash
# Author: Koustava Medya
# Description: Run Kivy WebView App (from source, no APK)

set -e

echo "📁 Switching to project folder..."
cd "$(dirname "$0")"

if [ -f venv/bin/activate ]; then
    echo "🐍 Activating venv..."
    source venv/bin/activate
else
    echo "⚙️ Creating Python venv..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 Installing requirements..."
    pip install --upgrade pip
    pip install -r requirements.txt || pip install kivy webview-android pywebview openssl
fi

echo "🚀 Running Kivy WebView app..."
python main.py
