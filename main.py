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

from jnius import autoclass
from android.runnable import run_on_ui_thread

class WebViewApp(App):
    def build(self):
        self.title = 'ErudaBrowser'
        layout = BoxLayout(orientation='vertical')

        # Android Implementation using pyjnius
        if IS_ANDROID:
            self.webview_java = autoclass('android.webkit.WebView')(activity)
            self.webview_java.getSettings().setJavaScriptEnabled(True)
            self.webview_java.setWebViewClient(autoclass('android.webkit.WebViewClient')())
            activity.setContentView(self.webview_java)
            self.webview_java.loadUrl('file:///android_asset/index.html')

            button_bar = BoxLayout(size_hint_y=None, height='48dp')
            devtools_btn = Button(text="DevTools")
            devtools_btn.bind(on_release=self.open_devtools)
            button_bar.add_widget(devtools_btn)
            
            layout.add_widget(button_bar)

        # Desktop (pywebview) Implementation
        else:
            import webview
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
        # No specific on_start logic needed for Android with pyjnius as WebView is set up in build
        pass

    @run_on_ui_thread
    def open_devtools(self, instance):
        if IS_ANDROID and hasattr(self, 'webview_java'):
            self.webview_java.evaluateJavascript('eruda.toggle();', None)

    def launch_desktop_webview(self, instance):
        if not IS_ANDROID:
            instance.disabled = True
            instance.text = "Browser is running..."
            html_url = 'file://' + os.path.join(os.getcwd(), 'assets', 'index.html')
            
            webview_thread = threading.Thread(
                target=webview.create_window,
                args=('ErudaBrowser - Desktop', html_url),
                kwargs={'width': 1200, 'height': 800}
            )
            webview_thread.start()

    def on_stop(self):
        if not IS_ANDROID and webview.active:
             pass

if __name__ == '__main__':
    from kivy.utils import platform
    IS_ANDROID = platform == 'android'
    if IS_ANDROID:
        activity = autoclass('org.kivy.android.PythonActivity').mActivity
    WebViewApp().run()
