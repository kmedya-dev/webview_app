from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.webview import WebView
from kivy.utils import platform
import os

from jnius import autoclass

# Android specific imports for native WebView control
WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
WebSettings = autoclass('android.webkit.WebSettings')
PythonActivity = autoclass('org.kivy.android.PythonActivity')

class WebViewApp(App):
    def build(self):
        self.title = 'ErudaBrowser'
        layout = BoxLayout(orientation='vertical')

        # Load local HTML (your custom index.html with JS-based navigation)
        # For Android, assets are typically accessed via 'file:///android_asset/'
        # For local testing on desktop, you might need a simple HTTP server
        local_html_path = 'file:///android_asset/index.html'

        # Create native Android WebView instance
        self.android_webview = WebView(PythonActivity.mActivity)
        settings = self.android_webview.getSettings()
        settings.setJavaScriptEnabled(True) # Ensure JS is enabled by default

        # Store default user agent and define a custom one
        self.default_user_agent = settings.getUserAgentString()
        self.custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36" # Example desktop UA

        settings.setWebViewClient(WebViewClient())
        self.android_webview.loadUrl(local_html_path)

        # Add custom buttons for DevTools
        button_bar = BoxLayout(size_hint_y=None, height='48dp')

        devtools_btn = Button(text="DevTools")
        devtools_btn.bind(on_release=self.open_devtools)

        toggle_js_btn = Button(text="Toggle JS")
        toggle_js_btn.bind(on_release=self.toggle_js)

        toggle_ua_btn = Button(text="Toggle UA")
        toggle_ua_btn.bind(on_release=self.toggle_user_agent)

        button_bar.add_widget(devtools_btn)
        button_bar.add_widget(toggle_js_btn)
        button_bar.add_widget(toggle_ua_btn)

        layout.add_widget(button_bar)
        layout.add_widget(self.android_webview) # Add the native Android WebView to the layout

        return layout

    def open_devtools(self, instance):
        # Execute JavaScript to toggle Eruda DevTools
        self.android_webview.evaluateJavascript('eruda.toggle();', None)

    def toggle_js(self, instance):
        current = self.android_webview.getSettings().getJavaScriptEnabled()
        self.android_webview.getSettings().setJavaScriptEnabled(not current)
        print(f"JavaScript is now: {self.android_webview.getSettings().getJavaScriptEnabled()}")
        # Reload the current URL to apply changes
        self.android_webview.reload()

    def toggle_user_agent(self, instance):
        settings = self.android_webview.getSettings()
        current_ua = settings.getUserAgentString()
        if current_ua == self.default_user_agent:
            settings.setUserAgentString(self.custom_user_agent)
            print(f"User Agent set to custom: {self.custom_user_agent}")
        else:
            settings.setUserAgentString(self.default_user_agent)
            print(f"User Agent set to default: {self.default_user_agent}")
        self.android_webview.reload() # Reload to apply UA change