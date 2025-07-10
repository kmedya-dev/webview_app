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

log "📦 Installing Kivy core dependencies..."
pip install -r kivy-requirements.txt

log "📦 Installing extra Python libs..."
pip install -r libytools-requirements.txt

log "🔧 Installing libytools dependencies from libytools-requirements.txt"
pip install -r libytools-requirements.txt

# --- Install kivy-garden.webview safely ---
log "🌱 Installing kivy-garden.webview..."
pip install kivy-garden
python -m kivy_garden install webview

# --- Update buildozer.spec requirements if needed ---
if [ -f update_requirements.py ]; then
  log "⚙️ Running update_requirements.py..."
  python update_requirements.py "$PROFILE"
fi

# --- Run Buildozer Build ---
log "🚀 Launching Buildozer with profile @$PROFILE..."
buildozer -v -p android $PROFILE debug

log "✅ Build finished at $(date '+%F %T')"
