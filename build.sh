#!/bin/bash

# Exit on error
set -e

echo "📦 Installing Python requirements from buildozer-requirements.txt..."
pip install --upgrade pip
pip install --no-cache-dir -r buildozer-requirements.txt

echo "🔧 Installing Buildozer..."
pip install --no-cache-dir --upgrade buildozer

echo "🧹 Cleaning previous builds..."
buildozer android clean

echo "🚧 Building debug APK..."
buildozer --log-level=2 android debug | tee buildozer.log

echo "✅ APK build completed!"
ls -lh bin/*.apk || echo "❌ No APK found!"
