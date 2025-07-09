#!/bin/bash
set -e

# Get profile from argument (default if not provided)
PROFILE=${1:-default}

echo "🔰 Buildozer Build Script Started"
echo "📦 Using profile: $PROFILE"

extra_reqs=$(paste -sd, /data/data/com.termux/files/home/webview_app/libytool-requirements.txt)
sed -i "s/^requirements = .*/requirements = python,kivy,kivy-garden.webview,pysdl2,pyjnius,$extra_reqs/" buildozer.spec

# The GitHub Actions workflow handles dependency installation and cleaning.
# This script now focuses solely on executing the buildozer command.

echo "🚀 Building debug APK..."
if [[ "$PROFILE" == "default" ]]; then
  buildozer --log-level=2 android debug | tee buildozer.log
else
  buildozer --log-level=2 --profile "$PROFILE" android debug | tee buildozer.log
fi

echo "✅ APK build command executed! Check buildozer.log for details."
ls -lh bin/*.apk || echo "❌ No APK found yet. Check buildozer.log for errors."