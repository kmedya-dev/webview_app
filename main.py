import os
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import mainthread
from kivy.utils import platform

# --- Platform Detection ---
IS_ANDROID = platform == 'android'
IS_DESKTOP = not IS_ANDROID

# --- Android Specific Imports (if on Android) ---
if IS_ANDROID:
    from jnius import autoclass, PythonJavaClass, java_method
    # Get the current Android Activity
    activity = autoclass('org.kivy.android.PythonActivity').mActivity
    # Define the Java classes we'll use
    AndroidWebView = autoclass('android.webkit.WebView')
    AndroidWebViewClient = autoclass('android.webkit.WebViewClient')
    AndroidWebChromeClient = autoclass('android.webkit.WebChromeClient')
    # Custom JavascriptInterface class (defined in PythonActivity.java by p4a)
    AndroidJavascriptInterface = autoclass('org.kivy.android.PythonActivity$PythonJavascriptInterface')

# --- Desktop Specific Imports (if on Desktop) ---
if IS_DESKTOP:
    import webview # pywebview library

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.log_label = Label(
            text='Console Log:',
            size_hint_y=0.2,
            halign='left',
            valign='top',
            text_size=(self.width, None) # Enable text wrapping
        )
        self.add_widget(self.log_label)

        # --- Python to JavaScript Communication Buttons ---
        js_comm_layout = BoxLayout(size_hint_y=None, height='48dp')
        self.send_to_js_btn = Button(text="Send 'Hello' to JS")
        self.send_to_js_btn.bind(on_release=self.send_message_to_js)
        js_comm_layout.add_widget(self.send_to_js_btn)

        self.change_dom_btn = Button(text="Change DOM from Python")
        self.change_dom_btn.bind(on_release=self.change_dom_from_python)
        js_comm_layout.add_widget(self.change_dom_btn)
        self.add_widget(js_comm_layout)

        # --- Platform-specific WebView Setup ---
        if IS_ANDROID:
            self.setup_android_webview()
        else:
            self.setup_desktop_webview()

    @mainthread
    def update_log(self, message):
        """Updates the Kivy Label with console messages."""
        self.log_label.text += f"\nJS: {message}"

    # --- Android WebView Setup (using pyjnius) ---
    def setup_android_webview(self):
        self.webview_java = AndroidWebView(activity)
        settings = self.webview_java.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True) # Important for some web apps

        # Custom WebViewClient to handle page loading (optional, but good practice)
        class MyWebViewClient(AndroidWebViewClient):
            @java_method('(Landroid/webkit/WebView;Ljava/lang/String;)Z')
            def shouldOverrideUrlLoading(self, webview, url):
                self.log_label.text += f"\nLoading URL: {url}"
                return False # Return False to let WebView load the URL

        self.webview_java.setWebViewClient(MyWebViewClient())

        # Custom WebChromeClient to capture console.log messages
        class MyWebChromeClient(AndroidWebChromeClient):
            @java_method('(Ljava/lang/String;Ljava/lang/String;I)Z')
            def onConsoleMessage(self, message, lineNumber, sourceID):
                # Call back to Python thread to update Kivy UI
                self.update_log(f"{message} (line {lineNumber} of {sourceID})")
                return True # Indicate that we've handled the message

        self.webview_java.setWebChromeClient(MyWebChromeClient())

        # Add JavaScript interface for JS to Python communication
        # The 'PythonBridge' class is defined in PythonActivity.java
        # It exposes a method 'callPythonFunction' to JavaScript
        self.python_bridge = AndroidJavascriptInterface(self) # Pass self to access update_log
        self.webview_java.addJavascriptInterface(self.python_bridge, "Android")

        # Load the local HTML file
        self.webview_java.loadUrl('file:///android_asset/index.html')

        # IMPORTANT: Setting setContentView replaces the Kivy UI.
        # For a truly embedded WebView within Kivy layout, a custom Kivy widget
        # wrapping an Android View would be needed, which is significantly more complex.
        # For this example, the WebView will overlay the Kivy UI.
        activity.setContentView(self.webview_java)
        self.log_label.text += "\nAndroid WebView initialized (overlaying Kivy UI)."
        self.log_label.text += "\nCheck Android logcat for WebView console messages."

    # --- Desktop WebView Setup (using pywebview) ---
    def setup_desktop_webview(self):
        self.log_label.text += "\nDesktop WebView will open in a separate window."
        self.log_label.text += "\nClose the browser window to exit the application."

        # Define a Python API for JavaScript to call
        class Api:
            def __init__(self, main_layout_instance):
                self.main_layout = main_layout_instance

            def js_called_python_function(self, message):
                @mainthread
                def _update():
                    self.main_layout.update_log(f"From JS: {message}")
                _update()
                return "Python received your message!"

        self.api = Api(self)

        # Load the local HTML file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, 'assets', 'index.html')
        html_url = 'file://' + html_path

        # Launch button for desktop
        launch_btn = Button(text="Launch Desktop WebView", size_hint_y=None, height='48dp')
        launch_btn.bind(on_release=lambda x: threading.Thread(target=lambda: webview.create_window(
            'Kivy WebView Desktop',
            html_url,
            js_api=self.api,
            width=1000,
            height=700
        )).start())
        self.add_widget(launch_btn)

    # --- Python to JavaScript Communication ---
    def send_message_to_js(self, instance):
        message = "Hello from Python!"
        if IS_ANDROID:
            # Android: Call JS function directly on the WebView object
            # Note: evaluateJavascript is asynchronous
            self.webview_java.evaluateJavascript(f"updateFromPython('{message}');", None)
            self.update_log(f"Python sent to JS: {message}")
        else:
            # Desktop: Call JS function via pywebview API
            # Check if the window exists and is loaded before evaluating JS
            if hasattr(self, 'webview_window') and self.webview_window and self.webview_window.loaded:
                self.webview_window.evaluate_js(f"updateFromPython('{message}');")
                self.update_log(f"Python sent to JS: {message}")
            else:
                self.update_log("Desktop WebView not ready to receive messages.")

    def change_dom_from_python(self, instance):
        if IS_ANDROID:
            self.webview_java.evaluateJavascript("changeDom();", None)
            self.update_log("Python requested JS to change DOM.")
        else:
            if hasattr(self, 'webview_window') and self.webview_window and self.webview_window.loaded:
                self.webview_window.evaluate_js("changeDom();")
                self.update_log("Python requested JS to change DOM.")
            else:
                self.update_log("Desktop WebView not ready to change DOM.")

class WebViewApp(App):
    def build(self):
        return MainLayout()

    def on_stop(self):
        # Ensure pywebview window is closed on desktop if app stops
        if IS_DESKTOP and hasattr(self.root, 'webview_window') and self.root.webview_window:
            self.root.webview_window.destroy()

if __name__ == '__main__':
    # For Android, the PythonActivity needs to be available for jnius.autoclass
    # This part is typically handled by p4a's bootstrap, but explicitly setting it here
    # for clarity in a standalone script context.
    if IS_ANDROID:
        try:
            activity = autoclass('org.kivy.android.PythonActivity').mActivity
        except Exception as e:
            print(f"Could not get Android activity: {e}. Running as desktop app.")
            IS_ANDROID = False # Fallback to desktop mode if activity not found

    WebViewApp().run()