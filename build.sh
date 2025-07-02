
#!/bin/bash

# This script is for building the APK in Termux

# Install dependencies
pip install -r requirements.txt
pip install buildozer

# Build the APK
buildozer android debug
