#!/bin/bash

# Exit immediately if any command fails
set -e

echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install --no-cache-dir -r buildozer-requirements.txt || true  # allow safe fallback
pip install --no-cache-dir pysdl2
pip install --no-cache-dir python-for-android==2024.1.21
pip install --no-cache-dir buildozer

echo "🧹 Cleaning previous builds (if present)..."
if [ -d ".buildozer/android/platform/python-for-android" ]; then
  buildozer android clean
else
  echo "⚠️ No previous build to clean."
fi

echo "🚧 Building debug APK..."
buildozer --log-level=2 android debug | tee buildozer.log

echo "✅ APK build completed!"
ls -lh bin/*.apk || echo "❌ No APK found!"
