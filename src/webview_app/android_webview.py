from jnius import autoclass, PythonActivity
from kivy.uix.widget import Widget
from kivy.clock import mainthread
from kivy.properties import ObjectProperty

from webview_app.webview_interface import WebViewInterface

# Android classes
WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
WebChromeClient = autoclass('android.webkit.WebChromeClient')
ValueCallback = autoclass('android.webkit.ValueCallback')
Log = autoclass('android.util.Log')
LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')

class AndroidWebView(Widget, WebViewInterface):
    # Kivy property to hold the native Android WebView instance
    _android_webview_instance = ObjectProperty(None)
    on_page_finished_callback = ObjectProperty(None)
    on_console_message_callback = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.activity = PythonActivity.mActivity
        self.root_view = self.activity.findViewById(autoclass('android.R$id').content) # Get the root content view
        self._create_webview()
        self.bind(pos=self._update_webview_layout, size=self._update_webview_layout)

    @mainthread
    def _create_webview(self):
        if self._android_webview_instance is None:
            self._android_webview_instance = WebView(self.activity)
            settings = self._android_webview_instance.getSettings()
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setAllowFileAccess(True)
            settings.setAllowContentAccess(True)
            settings.setBuiltInZoomControls(True) # Enable zoom controls
            settings.setDisplayZoomControls(False) # Hide zoom controls on screen

            # Set WebViewClient to handle page loading
            self._android_webview_instance.setWebViewClient(self._get_webview_client())
            # Set WebChromeClient to handle console messages, etc.
            self._android_webview_instance.setWebChromeClient(self._get_webchrome_client())

            # Add the WebView to the root view of the activity
            # We use WRAP_CONTENT for width and height initially, and then update via layout params
            self.root_view.addView(self._android_webview_instance, LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT))
            self._update_webview_layout() # Initial layout update

    @mainthread
    def _update_webview_layout(self, *args):
        if self._android_webview_instance:
            # Convert Kivy coordinates (bottom-left origin) to Android coordinates (top-left origin)
            # Kivy pos is relative to its parent, need to get absolute screen position
            abs_x, abs_y = self.to_window(self.x, self.y)

            # Android views are positioned from top-left.
            # Kivy y is from bottom, Android y is from top.
            # So, Android y = screen_height - Kivy_y - Kivy_height
            screen_height = self.activity.getWindowManager().getDefaultDisplay().getHeight()
            android_y = int(screen_height - abs_y - self.height)

            # Set layout parameters
            lp = self._android_webview_instance.getLayoutParams()
            lp.width = int(self.width)
            lp.height = int(self.height)
            self._android_webview_instance.setX(int(abs_x))
            self._android_webview_instance.setY(int(android_y))
            self._android_webview_instance.setLayoutParams(lp)
            self._android_webview_instance.requestLayout() # Request layout update

    def _get_webview_client(self):
        class MyWebViewClient(WebViewClient):
            def onPageFinished(self, view, url):
                Log.i("KivyWebView", f"Page finished loading: {url}")
                if self.this_object.on_page_finished_callback:
                    self.this_object.on_page_finished_callback(url)

            def onReceivedError(self, view, request, error):
                Log.e("KivyWebView", f"WebView error: {error.getDescription()}")
                pass

        return MyWebViewClient()

    def _get_webchrome_client(self):
        class MyWebChromeClient(WebChromeClient):
            def onConsoleMessage(self, consoleMessage):
                Log.d("KivyWebView", f"JS Console: {consoleMessage.message()} (Source: {consoleMessage.sourceId()}:{consoleMessage.lineNumber()})")
                return True # Indicate that we handled the message

        return MyWebChromeClient()

    def load_url(self, url: str):
        if self._android_webview_instance:
            self._android_webview_instance.loadUrl(url)

    def evaluate_js(self, script: str, callback=None):
        if self._android_webview_instance:
            if callback:
                # Need to wrap Python callback in a Java ValueCallback
                # This is more complex and will be added later.
                Log.w("KivyWebView", "evaluate_js with callback not yet fully implemented.")
                self._android_webview_instance.evaluateJavascript(script, None) # For now, no callback
            else:
                self._android_webview_instance.evaluateJavascript(script, None)

    def add_js_interface(self, name: str, obj):
        if self._android_webview_instance:
            self._android_webview_instance.addJavascriptInterface(obj, name)

    def get_webview_widget(self):
        return self

    def on_kv_post(self, base_widget):
        # This method is called after the Kivy widget is added to the widget tree
        # and its size/pos are determined by KV language.
        # Ensure the WebView is created and positioned correctly.
        self._create_webview()
        self._update_webview_layout()

    def on_parent(self, widget, parent):
        # When the widget is removed from its parent, remove the native WebView
        if not parent and self._android_webview_instance:
            self.root_view.removeView(self._android_webview_instance)
            self._android_webview_instance = None
