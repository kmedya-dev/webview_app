import os
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import platform

# --- Platform-specific WebView Implementation ---

IS_ANDROID = platform == 'android'
WEBVIEW_AVAILABLE = False

# Android: Use webview-android
if IS_ANDROID:
    try:
        from android_webview import AndroidWebView
        WEBVIEW_AVAILABLE = True
    except ImportError:
        print("Android WebView not available. Please ensure 'webview-android' is in your requirements.")

# Desktop: Use pywebview
else:
    try:
        import webview
        WEBVIEW_AVAILABLE = True
    except ImportError:
        print("pywebview not available. Please run 'pip install pywebview'.")


class WebViewApp(App):
    def build(self):
        self.title = 'ErudaBrowser'
        layout = BoxLayout(orientation='vertical')

        if not WEBVIEW_AVAILABLE:
            return Label(text="WebView component is not available on this platform. Check logs.")

        # --- Android Implementation ---
        if IS_ANDROID:
            self.webview = AndroidWebView()
            
            # Create Android-specific button bar
            button_bar = BoxLayout(size_hint_y=None, height='48dp')
            devtools_btn = Button(text="DevTools")
            devtools_btn.bind(on_release=self.open_devtools)
            button_bar.add_widget(devtools_btn)
            
            layout.add_widget(button_bar)
            layout.add_widget(self.webview)

        # --- Desktop (pywebview) Implementation ---
        else:
            info_label = Label(
                text="The browser will open in a separate window.\nClose this window to exit the application.",
                halign="center"
            )
            launch_btn = Button(text="Launch Browser Window", size_hint_y=None, height='48dp')
            launch_btn.bind(on_release=self.launch_desktop_webview)
            layout.add_widget(info_label)
            layout.add_widget(launch_btn)

        return layout

    def on_start(self):
        """Load the URL after the app starts, especially for Android."""
        if IS_ANDROID and hasattr(self, 'webview'):
            # For Android, assets are bundled. The path is relative to the app's assets directory.
            local_html_path = 'file:///android_asset/index.html'
            self.webview.load_url(local_html_path)

    def launch_desktop_webview(self, instance):
        """Launch pywebview in a separate thread."""
        if not IS_ANDROID:
            instance.disabled = True
            instance.text = "Browser is running..."
            # For desktop, use a relative path to the HTML file
            html_url = 'file://' + os.path.join(os.getcwd(), 'assets', 'index.html')
            
            # Run pywebview in a separate thread so it doesn't block the Kivy event loop
            webview_thread = threading.Thread(
                target=webview.create_window,
                args=('ErudaBrowser - Desktop', html_url),
                kwargs={'width': 1200, 'height': 800}
            )
            webview_thread.start()

    def open_devtools(self, instance):
        """Toggle Eruda DevTools (Android only)."""
        if IS_ANDROID and hasattr(self, 'webview'):
            self.webview.evaluate_javascript('eruda.toggle();')

    def on_stop(self):
        """Clean up resources."""
        if not IS_ANDROID and webview.active:
             # pywebview manages its own lifecycle when the window is closed.
             pass

if __name__ == '__main__':
    WebViewApp().run()
