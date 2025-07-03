
#!/bin/bash

# This script is for building the APK in Termux

# Install dependencies
pip install -r kivy-requirements.txt
pip install buildozer

# Build the APK
buildozer android debug
