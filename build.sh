#!/usr/bin/env bash
set -e

# --- Profile support ---
PROFILE=${1:-default}
echo "[🔧 $(date '+%F %T')] Buildozer Build Script Started"
echo "[📁 $(date '+%F %T')] Using profile: @$PROFILE"

# --- Setup Logs ---
log() {
  echo "[$(date '+%F %T')] $1"
}

# --- Install Python packages ---
log "📦 Installing buildozer requirements..."
pip install -r buildozer-requirements.txt

log "📦 Installing application requirements..."
pip install -r requirements.txt









# --- Run Buildozer Build ---
echo "[+] Installing webview-android and pywebview..."
pip install webview-android pywebview

echo "[✓] Verifying webview-android and pywebview modules..."
python -c "from webview import WebView; import pywebview"

log "🚀 Launching Buildozer with profile @$PROFILE..."
buildozer -v -p android $PROFILE debug

log "✅ Build finished at $(date '+%F %T')"
