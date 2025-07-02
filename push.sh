#!/bin/bash
cd ~/webview_app
git add .
git commit -m "Auto push from Termux on $(date)"
git push origin main
