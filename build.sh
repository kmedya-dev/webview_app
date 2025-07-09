#!/usr/bin/env bash
set -e

# --------------🔧 Buildozer Build Script --------------
PROFILE="${1:-default}"
LOGFILE="build_log_${PROFILE}.txt"

echo "📝 Logging to: $LOGFILE (with timestamps)"
exec > >(awk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0; fflush(); }' | tee -a "$LOGFILE") 2>&1

echo "🔄 Build Started"
echo "⚙️  Using profile: $PROFILE"
echo "----------------------------------------------------"

# ✅ Step 1: Install Python & pip dependencies
echo "📦 Installing Python/Buildozer dependencies..."
pip install --upgrade pip setuptools wheel

if [ -f buildozer-requirements.txt ]; then
  echo "📥 Installing buildozer-requirements.txt..."
  pip install -r buildozer-requirements.txt
else
  echo "⚠️ buildozer-requirements.txt not found, skipping..."
fi

if [ -f kivy-requirements.txt ]; then
  echo "📥 Installing kivy-requirements.txt..."
  pip install -r kivy-requirements.txt
else
  echo "⚠️ kivy-requirements.txt not found, skipping..."
fi

# ✅ Step 2: Update buildozer.spec with libytool dependencies
if [ -f libytool-requirements.txt ]; then
  echo "🛠️ Updating buildozer.spec from libytool-requirements.txt..."
  python update_requirements.py
else
  echo "⚠️ libytool-requirements.txt not found, skipping update_requirements.py"
fi

# ✅ Step 3: Build APK
echo "🚧 Building APK for profile: $PROFILE"
if [ "$PROFILE" = "default" ]; then
  buildozer android debug
else
  buildozer -p "$PROFILE" android debug
fi

# ✅ Step 4: Check APK output
echo "📁 Build Complete. APK files:"
ls -lh bin/*.apk || {
  echo "❌ APK build failed or file missing!"
  exit 1
}

echo "✅ Done! Log saved to $LOGFILE"
