from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.utils import platform
import os

# Android specific imports - only load on Android
ANDROID_AVAILABLE = False
if platform == 'android':
    try:
        from jnius import autoclass
        AndroidWebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        WebSettings = autoclass('android.webkit.WebSettings')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        ANDROID_AVAILABLE = True
    except ImportError:
        print("Android WebView APIs not available")

# Desktop pywebview import
PYWEBVIEW_AVAILABLE = False
if platform in ('win', 'linux', 'macosx'):
    try:
        import webview
        PYWEBVIEW_AVAILABLE = True
    except ImportError:
        print("pywebview not available - install pywebview")

class WebViewApp(App):
    def build(self):
        self.title = 'ErudaBrowser'
        layout = BoxLayout(orientation='vertical')

        # Create button bar first
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

        # Platform-specific WebView
        if platform == 'android' and ANDROID_AVAILABLE:
            self.setup_android_webview(layout)
        elif PYWEBVIEW_AVAILABLE:
            self.setup_pywebview(layout)
        else:
            from kivy.uix.label import Label
            layout.add_widget(Label(text="No WebView available. Please run on Android or install pywebview for desktop."))
        return layout

    def setup_android_webview(self, layout):
        """Setup native Android WebView"""
        local_html_path = 'file:///android_asset/index.html'
        self.webview = AndroidWebView(PythonActivity.mActivity)
        settings = self.webview.getSettings()
        settings.setJavaScriptEnabled(True)
        self.default_user_agent = settings.getUserAgentString()
        self.custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
        settings.setWebViewClient(WebViewClient())
        self.webview.loadUrl(local_html_path)
        layout.add_widget(self.webview)

    def setup_pywebview(self, layout):
        # Launch a pywebview window (runs outside Kivy's widget tree)
        html_path = os.path.abspath(os.path.join('assets', 'index.html'))
        webview.create_window('ErudaBrowser', html_path)
        from kivy.uix.label import Label
        layout.add_widget(Label(text="pywebview window launched in a separate window."))

    def open_devtools(self, instance):
        # DevTools toggling is only supported in Android WebView
        if hasattr(self, 'webview'):
            if platform == 'android' and ANDROID_AVAILABLE:
                self.webview.evaluateJavascript('eruda.toggle();', None)
            else:
                print("DevTools toggle is only available in Android WebView.")

    def toggle_js(self, instance):
        if platform == 'android' and ANDROID_AVAILABLE and hasattr(self, 'webview'):
            current = self.webview.getSettings().getJavaScriptEnabled()
            self.webview.getSettings().setJavaScriptEnabled(not current)
            print(f"JavaScript is now: {self.webview.getSettings().getJavaScriptEnabled()}")
            self.webview.reload()
        else:
            print("JavaScript toggle only available on Android")

    def toggle_user_agent(self, instance):
        if platform == 'android' and ANDROID_AVAILABLE and hasattr(self, 'webview'):
            settings = self.webview.getSettings()
            current_ua = settings.getUserAgentString()
            if current_ua == self.default_user_agent:
                settings.setUserAgentString(self.custom_user_agent)
                print(f"User Agent set to custom: {self.custom_user_agent}")
            else:
                settings.setUserAgentString(self.default_user_agent)
                print(f"User Agent set to default: {self.default_user_agent}")
            self.webview.reload()
        else:
            print("User Agent toggle only available on Android")

if __name__ == '__main__':
    WebViewApp().run()