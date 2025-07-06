#!/bin/bash
set -e

echo "📦 Installing host tools from buildozer-requirements.txt"
pip install --no-cache-dir -r buildozer-requirements.txt

echo "🔌 Installing app dependencies from kivy-requirements.txt (optional local dev)"
pip install --no-cache-dir -r kivy-requirements.txt || true

echo "🧹 Cleaning previous builds (if needed)"
if [ -d ".buildozer/android/platform/python-for-android" ]; then
  buildozer android clean
else
  echo "⚠️ No previous build to clean."
fi

echo "🚀 Building debug APK..."
buildozer --log-level=2 android debug | tee buildozer.log

echo "✅ APK build completed!"
ls -lh bin/*.apk || echo "❌ No APK found!"
