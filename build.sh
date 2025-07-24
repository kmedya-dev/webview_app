#!/usr/bin/env bash
set -e

# --- Profile support ---
PROFILE=${1:-default}
echo "[ $(date '+%F %T')] Buildozer Build Script Started"
echo "[ $(date '+%F %T')] Using profile: @$PROFILE"

# --- Setup Logs ---
log() {
  echo "[ $(date '+%F %T')] $1"
}

# --- Install Python packages ---
log " Installing buildozer requirements..."
if [ -f buildozer-requirements.txt ]; then
  pip install -r buildozer-requirements.txt
else
  log "⚠️ Skipped: buildozer-requirements.txt not found."
fi

log " Installing application requirements..."
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
else
  log "⚠️ Skipped: requirements.txt not found."
fi

# --- Verify webview modules ---
# --- Launch Buildozer ---
log " Launching Buildozer with profile @$PROFILE..."
buildozer -v -p android "$PROFILE" debug --android-api=33

log "✅ Build finished at $(date '+%F %T')"