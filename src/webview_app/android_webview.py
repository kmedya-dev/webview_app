from jnius import autoclass, PythonJavaClass, java_method
from kivy.clock import mainthread
from kivy.uix.widget import Widget

# Get the Java classes
PythonActivity = autoclass('org.kivy.android.PythonActivity')
KivyWebView = autoclass('com.kmllc.erudabrowser.KivyWebView')

class AndroidWebView:
    def __init__(self):
        self.activity = PythonActivity.mActivity
        self.webview_instance = KivyWebView(self.activity)
        self.webview_widget = AndroidWebViewWidget(self.webview_instance)

    def get_webview_widget(self):
        return self.webview_widget

    def load_url(self, url):
        self.webview_instance.loadUrlFromPython(url)

    def evaluate_js(self, script):
        self.webview_instance.evaluateJavascriptFromPython(script)

    def add_js_interface(self, name, py_object):
        # This method is for adding Python objects as JavaScript interfaces.
        # The KivyWebView.java already handles a generic interface.
        # We need to ensure the Python object's methods are exposed correctly.
        # For now, the KivyWebView.java expects a specific interface (JsApiCallback).
        # The `py_object` here should be an instance of the JsApi class defined in main.py
        # which implements the Java interface.
        self.webview_instance.addJavascriptInterface(py_object, name)

class AndroidWebViewWidget(Widget):
    def __init__(self, webview_instance, **kwargs):
        super().__init__(**kwargs)
        self.webview_instance = webview_instance
        self.bind(size=self._on_size, pos=self._on_pos)

    def _on_size(self, instance, size):
        # Update the WebView's layout parameters when Kivy widget size changes
        # This requires direct manipulation of Android View properties
        # which is complex and often not directly exposed via pyjnius for layout.
        # Kivy's GLSurfaceView is usually full screen, so direct sizing of the
        # WebView within Kivy's layout is tricky. For simplicity, we'll assume
        # the WebView will take up the full Kivy window area for now, or rely
        # on the Java side to handle its own layout within the PythonActivity.
        # A more robust solution would involve custom Java layout management.
        pass

    def _on_pos(self, instance, pos):
        pass

    def on_parent(self, widget, parent):
        if parent:
            # Add the Android WebView to the PythonActivity's content view
            # This is a simplified approach. A proper integration might involve
            # adding it to a specific ViewGroup in the PythonActivity's layout.
            self.webview_instance.setLayoutParams(
                autoclass('android.widget.LinearLayout$LayoutParams').
                new(autoclass('android.widget.LinearLayout$LayoutParams').MATCH_PARENT,
                    autoclass('android.widget.LinearLayout$LayoutParams').MATCH_PARENT)
            )
            self.activity.addContentView(self.webview_instance, self.webview_instance.getLayoutParams())
        else:
            # Remove the WebView when the Kivy widget is removed from its parent
            # This is also simplified. Removing from parent might require
            # finding the correct ViewGroup and calling removeView.
            pass

    @mainthread
    def on_console_message(self, message):
        # This method will be called from Java via PythonActivity.callPython
        # It's a placeholder for now, the actual logging is handled in main.py
        print(f"Python received console message: {message}")

    @mainthread
    def on_js_call(self, function_name, message):
        # This method will be called from Java via PythonActivity.callPython
        # It's a placeholder for now, the actual handling is in main.py
        print(f"Python received JS call: {function_name} with message: {message}")