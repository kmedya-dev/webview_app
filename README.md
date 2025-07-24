# ErudaBrowser

![CI](https://github.com/kmedya-dev/erudabrowser/actions/workflows/erudabrowser.yml/badge.svg)

ErudaBrowser is a lightweight, 100% Java-free Android WebView browser application. It's designed for developers and users who want a simple browsing experience with access to a JavaScript console for debugging, thanks to the integrated Eruda.js library. The app is built using a Python-centric stack, making it a great choice for Python developers looking to get into mobile app development.

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
git clone <repository-url>
cd ErudaBrowser
./setup_dev.sh
```

### Option 2: Manual Setup
```bash
git clone <repository-url>
cd ErudaBrowser
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📋 Prerequisites

- **Python 3.11+** (recommended for best compatibility)
- **Git** for version control
- **Virtual environment** support

## Project Details

*   **Application Name:** ErudaBrowser
*   **Platform:** Android (with desktop testing support)
*   **Programming Languages:** Python, JavaScript
*   **Core Technologies:** Kivy, Buildozer, Eruda.js
*   **Key Features:**
    *   Dynamic URL loading with intelligent search/URL detection
    *   Eruda.js console for JavaScript debugging
    *   Offline and online browsing capabilities  
    *   Light, dark, and system theme support
    *   Automated APK builds and releases via GitHub Actions
    *   Cross-platform development (Android production, desktop testing)

## 📁 Project Structure

```
ErudaBrowser/
├── main.py                          # Main application entry point with improved cross-platform WebView handling
├── assets/
│   ├── index.html                   # HTML frontend with Eruda.js integration and theme support
│   ├── icon.svg                     # Main application icon (SVG format)
│   └── icon_demo.svg                # Demo profile icon
├── requirements.txt                 # Comprehensive Python dependencies for local development
├── kivy-requirements.txt            # Kivy-specific requirements for the build process
├── buildozer-requirements.txt       # Buildozer and build tool dependencies
├── buildozer.spec                   # Optimized Buildozer configuration for Android packaging
├── setup_dev.sh                     # Automated development environment setup script
├── build.sh                         # Build script for local APK generation
├── manifest.json                    # Application metadata and configuration
├── .github/workflows/
│   └── erudabrowser.yml             # Professional CI/CD pipeline for automated builds
└── PROJECT_OVERVIEW.md              # Detailed technical documentation
```

## 🏗️ Building the Application

### Local Development & Testing
```bash
# Set up development environment
./setup_dev.sh

# Activate virtual environment
source venv/bin/activate

# Run for desktop testing (limited functionality)
python3 main.py

# Build APK locally (requires Android SDK setup)
./build.sh
```

### Production Builds via GitHub Actions

The project uses a professional CI/CD pipeline for automated builds:

#### Automatic Builds
- **Push to main:** Triggers debug APK build
- **Version tags:** Creates signed release APK and GitHub release

#### Manual Builds
1. Go to the "Actions" tab in your GitHub repository
2. Select "Build ErudaBrowser APK" workflow  
3. Click "Run workflow"
4. Choose build profile: `default` or `demo`

#### Build Profiles
- **Default:** Full production build with all features
- **Demo:** Limited feature set for testing and demonstrations

## 🔧 Development Features

- **Cross-platform compatibility:** Develop on desktop, deploy to Android
- **Intelligent fallbacks:** Graceful handling of missing dependencies
- **Professional error handling:** Clear error messages and recovery options
- **Hot-reloading workflow:** Fast iteration during development
- **Comprehensive logging:** Detailed build logs for troubleshooting

## 📱 Platform Support

- **Primary Target:** Android devices (ARM64, ARMv7)
- **Development Platform:** Linux, macOS, Windows (via WSL)
- **Testing:** Desktop browsers for rapid prototyping

## 🔐 Release Management

Configure these GitHub secrets for automated release builds:
- `KEYSTORE_BASE64` - Base64 encoded Android keystore
- `KEYSTORE_PASSWORD` - Keystore password
- `KEY_ALIAS` - Key alias name  
- `KEY_PASSWORD` - Key password

## 🎯 Key Improvements

This version includes significant improvements:
- ✅ **Python 3.13 compatibility** with proper dependency management
- ✅ **Enhanced error handling** and user feedback
- ✅ **Professional build pipeline** with comprehensive CI/CD
- ✅ **Cross-platform development** support
- ✅ **Optimized dependencies** for faster, more reliable builds
- ✅ **Automated setup** for quick development environment creation

## Requirements

- Python 3.8+
- Kivy >=2.3.0
- Buildozer (for Android builds)
- Cython
- setuptools >=60.0.0
- python-for-android==2024.1.21
- pywebview (for desktop support only, do NOT add to buildozer.spec)

Install all requirements for desktop development:

```sh
pip install -r requirements.txt
```

For Android builds, ensure your `buildozer.spec` requirements line is:

```
requirements = python,kivy,pysdl2,openssl,zlib
```

**Do NOT add pywebview to buildozer.spec.**

## Cross-Platform WebView Support

- **Android:** Uses the native Android WebView via pyjnius (no kivy-garden.webview, no pywebview)
- **Desktop (Windows, Linux, macOS):** Uses pywebview (opens in a separate window)

## Running on Desktop

```sh
python main.py
```
This will launch the Kivy app and open the webview in a separate window (requires pywebview).

## Building for Android

```sh
buildozer android debug
```
This will build the APK using the native Android WebView. Do not include pywebview in your buildozer.spec.