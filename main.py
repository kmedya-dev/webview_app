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

        # --- URL Input ---
        url_input_layout = BoxLayout(size_hint_y=None, height='48dp')
        from kivy.uix.textinput import TextInput
        self.url_input = TextInput(
            text='file:///android_asset/index.html', # Default URL
            multiline=False,
            size_hint_x=0.8
        )
        self.url_input.bind(on_text_validate=self.load_url)
        url_input_layout.add_widget(self.url_input)

        go_button = Button(text='Go', size_hint_x=0.2)
        go_button.bind(on_release=self.load_url)
        url_input_layout.add_widget(go_button)
        self.add_widget(url_input_layout)

        # --- Platform-specific WebView Setup ---
        if IS_ANDROID:
            from kivy.uix.relativelayout import RelativeLayout
            from webview_app.android_webview import AndroidWebView

            # Python side of the JavaScript interface
            class PythonWebViewInterface: # No longer needs to be PythonJavaClass directly
                def __init__(self, main_layout_instance):
                    self.main_layout = main_layout_instance

                def onPageLoaded(self, url):
                    self.main_layout.on_webview_page_loaded(url)

                def logToPython(self, message):
                    self.main_layout.update_log(message)

            self.webview_container = RelativeLayout(size_hint=(1, 0.8))
            self.add_widget(self.webview_container)

            self.android_webview_instance = AndroidWebView()
            self.android_webview_instance.on_page_finished_callback = self.on_webview_page_loaded
            self.android_webview_instance.add_js_interface("Android", PythonWebViewInterface(self))
            self.webview_container.add_widget(self.android_webview_instance.get_webview_widget())
            self.android_webview_instance.load_url(self.url_input.text)
            self.log_label.text += "\nAndroid WebView initialized and embedded."
            self.log_label.text += "\nCheck Android logcat for WebView console messages."

        else:
            self.setup_desktop_webview()

    @mainthread
    def update_log(self, message):
        """Updates the Kivy Label with console messages."""
        self.log_label.text += f"\nJS: {message}"

    @mainthread
    def on_webview_page_loaded(self, url):
        self.update_log(f"WebView page loaded: {url}")
        # Inject Eruda after page loads
        eruda_script = """
        (function() {
            if (!window.eruda) {
                var script = document.createElement('script');
                script.src = 'file:///android_asset/eruda.min.js';
                document.body.appendChild(script);
                script.onload = function() {
                    eruda.init();
                    eruda.show();
                };
            } else {
                eruda.show();
            }
        })();
        """
        if IS_ANDROID:
            self.webview_java.evaluateJavascriptFromPython(eruda_script)
        else:
            # For desktop, Eruda is already in index.html, but if we load external URLs,
            # we might need to inject it. For now, assume it's handled by index.html.
            pass

    def load_url(self, instance):
        url = self.url_input.text
        if not url.startswith(('http://', 'https://', 'file://')):
            url = 'http://' + url # Prepend http:// if no scheme is provided

        if IS_ANDROID:
            if hasattr(self, 'webview_java'):
                self.webview_java.loadUrlFromPython(url)
                self.update_log(f"Loading Android URL: {url}")
            else:
                self.update_log("Android WebView not yet initialized to load URL.")
        else:
            if hasattr(self, 'webview_window') and self.webview_window:
                self.webview_window.load_url(url)
                self.update_log(f"Loading Desktop URL: {url}")
            else:
                # For desktop, if not yet launched, set the URL for when it does launch
                self.desktop_initial_url = url
                self.update_log(f"Desktop WebView will load: {url} on launch.")

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

        # Load the local HTML file or initial URL from input
        initial_url = getattr(self, 'desktop_initial_url', 'file://' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'index.html'))

        # Launch button for desktop
        launch_btn = Button(text="Launch Desktop WebView", size_hint_y=None, height='48dp')
        launch_btn.bind(on_release=lambda x: threading.Thread(target=lambda: (
            setattr(self, 'webview_window', webview.create_window(
                'Kivy WebView Desktop',
                initial_url,
                js_api=self.api,
                width=1000,
                height=700
            )),
            self.webview_window.events.loaded += lambda: self.update_log(f"Desktop WebView loaded: {self.webview_window.url}")
        )).start())
        self.add_widget(launch_btn)

    # --- Python to JavaScript Communication ---
    def send_message_to_js(self, instance):
        message = "Hello from Python!"
        if IS_ANDROID:
            if hasattr(self, 'webview_java'):
                self.webview_java.evaluateJavascriptFromPython(f"updateFromPython('{message}');")
                self.update_log(f"Python sent to JS: {message}")
            else:
                self.update_log("Android WebView not yet initialized.")
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
            if hasattr(self, 'webview_java'):
                self.webview_java.evaluateJavascriptFromPython("changeDom();")
                self.update_log("Python requested JS to change DOM.")
            else:
                self.update_log("Android WebView not yet initialized.")
        else:
            if hasattr(self, 'webview_window') and self.webview_window and self.webview_window.loaded:
                self.webview_window.evaluate_js("changeDom();")
                self.update_log("Python requested JS to change DOM.")

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