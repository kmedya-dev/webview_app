#!/bin/bash
set -e

# 🔰 Profile support
PROFILE=${1:-default}
echo "🔰 Buildozer Build Script Started"
echo "📦 Using profile: $PROFILE"

# 📂 Check buildozer.spec exists
if [[ ! -f buildozer.spec ]]; then
  echo "❌ buildozer.spec not found!"
  exit 1
fi

# 🧠 Load extra requirements from libytool-requirements.txt
REQ_FILE="./libytool-requirements.txt"
if [[ -f "$REQ_FILE" ]]; then
  extra_reqs=$(paste -sd, "$REQ_FILE")
else
  echo "⚠️  $REQ_FILE not found. Using base requirements only."
  extra_reqs=""
fi

# 🛠️ Update buildozer.spec with new requirements
base_reqs="python,kivy,kivy-garden.webview,pysdl2"


# 🕒 Log file with timestamp
LOGFILE="buildozer_$(date +%F_%H-%M).log"

# 🚀 Start building
echo "🚀 Building debug APK..."
if [[ "$PROFILE" == "default" ]]; then
  buildozer --log-level=2 android debug | tee "$LOGFILE"
else
  buildozer --log-level=2 --profile "$PROFILE" android debug | tee "$LOGFILE"
fi

# 📦 Output build result
APK_PATH=$(find bin/ -type f -name "*.apk" | head -n 1)

if [[ -f "$APK_PATH" ]]; then
  echo "✅ Build successful!"
  echo "📱 APK: $APK_PATH"
  ls -lh "$APK_PATH"
else
  echo "❌ No APK found. Check $LOGFILE for errors."
fi
