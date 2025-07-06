#!/bin/bash
set -e

# Get profile from argument (default if not provided)
PROFILE=${1:-default}

echo "🔰 Buildozer Build Script Started"
echo "📦 Using profile: $PROFILE"

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
if [[ "$PROFILE" == "default" ]]; then
  buildozer --log-level=2 android debug | tee buildozer.log
else
  buildozer --log-level=2 --profile "$PROFILE" android debug | tee buildozer.log
fi

echo "✅ APK build completed!"
ls -lh bin/*.apk || echo "❌ No APK found!"
