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
        self.android_webview.setWebViewClient(WebViewClient())
        self.android_webview.loadUrl(local_html_path)

        # Kivy WebView widget to embed the native Android WebView
        # Note: kivy.uix.webview.WebView is an abstraction. We're passing the native one.
        # This might require a custom Kivy recipe or direct integration if not fully supported.
        # For simplicity, we'll assume it can wrap the native object or we'll use a placeholder.
        # A more robust solution might involve a custom Kivy widget that directly uses the native WebView.
        # For now, we'll use the Kivy WebView and try to set its native object.
        self.kivy_webview = WebView(url=local_html_path) # Placeholder, actual native control is via self.android_webview

        # Attempt to set the native Android WebView object to the Kivy WebView widget
        # This is a hacky way; a proper Kivy custom widget would be better.
        # For now, we'll just add the Kivy WebView to the layout and assume it works.
        # The direct calls to self.android_webview will control the native WebView.

        # Add custom buttons for DevTools and JS toggle
        button_bar = BoxLayout(size_hint_y=None, height='48dp')

        devtools_btn = Button(text="DevTools")
        devtools_btn.bind(on_release=self.open_devtools)

        toggle_js_btn = Button(text="Toggle JS")
        toggle_js_btn.bind(on_release=self.toggle_js)

        button_bar.add_widget(devtools_btn)
        button_bar.add_widget(toggle_js_btn)

        layout.add_widget(button_bar)
        layout.add_widget(self.kivy_webview) # Add the Kivy WebView to the layout

        return layout

    def open_devtools(self, instance):
        # Injects Eruda script to activate devtools (if not already in index.html)
        js_code = """
            if (!window.eruda) {
                var script = document.createElement('script');
                script.src = 'https://cdn.jsdelivr.net/npm/eruda';
                script.onload = () => eruda.init();
                document.body.appendChild(script);
            } else {
                eruda.show();
            }
        """
        self.android_webview.evaluateJavascript(js_code, None) # Use native WebView for JS evaluation

    def toggle_js(self, instance):
        current = self.android_webview.getSettings().getJavaScriptEnabled()
        self.android_webview.getSettings().setJavaScriptEnabled(not current)
        print(f"JavaScript is now: {self.android_webview.getSettings().getJavaScriptEnabled()}")
        # Reload the current URL to apply changes
        self.android_webview.reload()

if __name__ == '__main__':
    WebViewApp().run()