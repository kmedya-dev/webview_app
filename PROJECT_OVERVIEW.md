# 🚀 Project Overview: Android WebView App

This document provides a comprehensive overview of the Android WebView application, detailing its purpose, technical stack, architecture, and development philosophy.

## 🎯 1. Project Purpose

This application aims to be a **lightweight, developer-focused Android WebView browser** with integrated debugging capabilities.

*   **Goal:** To provide a flexible browsing environment that can render both standard online websites and local server (localhost) pages, making it ideal for web developers testing local projects on an Android device.
*   **Functionality:** It behaves much like a standard browser (e.g., Chrome, Firefox), allowing users to input custom URLs and navigate the web.
*   **Key Feature:** The integration of Eruda DevTools provides an in-app console for debugging web content directly on the device, mirroring the developer experience found in desktop browsers.

## 🛠️ 2. Tools & Stack

The project leverages a modern and efficient stack, carefully chosen to minimize local dependencies while maximizing remote automation.

*   **Python:** Serves as the primary language for the application's core logic and Android embedding.
*   **HTML/CSS/JS:** Forms the complete frontend user interface, providing a familiar web development experience.
*   **Eruda.js:** An essential client-side script injected into the WebView, offering a powerful developer console for debugging web content.
*   **Kivy + Kivy Garden WebView:** The chosen framework for building the cross-platform GUI and embedding the WebView component within the Android application.
*   **GitHub Actions:** Utilized for Continuous Integration/Continuous Deployment (CI/CD), handling all the heavy lifting of APK building, signing, and release management remotely.
*   **Termux:** The local development environment on Android, enabling a pure Python/web-based workflow without traditional Android development tools.

## 💻 3. Code/Project Description

The application's architecture is designed for clear separation of concerns and efficient development.

*   **HTML/JS Frontend Loading:** The `main.py` Kivy application initializes an `WebView` component. The entire user interface, including navigation and content display, is built using standard web technologies (HTML, CSS, JavaScript) and loaded from `assets/index.html` into this WebView.
*   **Python-WebView Integration:** Kivy's `WebView` widget acts as the bridge. Python handles the overarching application logic, such as processing user input for URLs and instructing the WebView to load new pages.
*   **Eruda.js Injection:** Eruda.js is seamlessly integrated by being directly included within the `assets/index.html` file via a `<script>` tag. This ensures that the developer console is available as soon as the web content loads.
*   **CI for Heavy Lifting:** A core principle of this project is to keep the local development environment lean. All complex, resource-intensive tasks, including Java compilation, Android SDK setup, Gradle execution, APK creation, and cryptographic signing, are exclusively performed by the automated workflows on GitHub Actions.
*   **UI/UX Handled by JS:** User interface elements and interactive features, such as the theme switcher (light/dark mode) and any potential language selection (e.g., English/Bengali), are implemented directly within the HTML/JavaScript frontend. This allows for rapid iteration and a familiar web development workflow for UI changes.

## 📂 4. Project Structure

The project follows a clean and organized directory structure:

```
.
├── main.py                     # Main Python application logic (Kivy app)
├── assets/                     # Contains all web-based frontend assets
│   └── index.html              # The primary HTML file loaded into the WebView
├── .github/                    # GitHub-related configurations
│   └── workflows/              # GitHub Actions workflow definitions
│       └── erudabrowser.yml    # Workflow for automated APK builds and signing
├── buildozer.spec              # Buildozer configuration file for Android packaging
├── requirements.txt            # Python dependencies for the Kivy application
└── PROJECT_OVERVIEW.md         # This project overview document
```

## ✨ 5. Clean Setup Reminder

A key advantage of this project setup is its minimal local footprint:

*   **100% Java-Free Locally:** There is **no Java, Gradle, C++, or Android SDK** installed or required on the local Termux development environment.
*   **CI-Only Java/Native Steps:** All Java-related processes (Android SDK tools, Gradle) and C/C++ compilation (for Python-for-Android's native components) occur **exclusively within the GitHub Actions CI environment**. This ensures a lightweight, hassle-free local development experience on your mobile device.
