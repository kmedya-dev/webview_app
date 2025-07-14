import os
import json
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.clock import mainthread
from kivy.utils import platform

# --- Platform Detection ---
IS_ANDROID = platform == 'android'
IS_DESKTOP = not IS_ANDROID

# --- Desktop Specific Imports ---
if IS_DESKTOP:
    import webview

# --- Main Application Layout ---
class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # 1. Log Display Area
        self.log_scroll = ScrollView(size_hint=(1, 0.3))
        self.log_label = Label(
            text='--- WebView Log ---\n',
            size_hint_y=None,
            halign='left',
            valign='top',
            markup=True
        )
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        self.log_scroll.add_widget(self.log_label)
        self.add_widget(self.log_scroll)

        # 2. WebView Placeholder
        self.webview_placeholder = BoxLayout(size_hint=(1, 0.7))
        self.add_widget(self.webview_placeholder)

        # 3. Control Buttons
        controls_layout = BoxLayout(size_hint_y=None, height='48dp')
        self.py_to_js_btn = Button(text='Py -> JS (Message)')
        self.py_to_js_btn.bind(on_release=self.send_message_to_js)
        controls_layout.add_widget(self.py_to_js_btn)

        self.py_to_dom_btn = Button(text='Py -> JS (DOM)')
        self.py_to_dom_btn.bind(on_release=self.change_dom_from_python)
        controls_layout.add_widget(controls_layout)

        # --- Platform-Specific WebView Initialization ---
        self.webview = None
        if IS_ANDROID:
            self.setup_android_webview()
        else:
            self.setup_desktop_webview()

    @mainthread
    def log(self, message, source='App'):
        self.log_label.text += f'[b][{source}]:[/b] {message}\n'

    # --- WebView Setup ---
    def setup_android_webview(self):
        from webview_app.android_webview import AndroidWebView
        from jnius import autoclass, PythonJavaClass, java_method

        class JsApi(PythonJavaClass):
            __javainterfaces__ = ['com/kmllc/erudabrowser/JsApiCallback']
            __javacontext__ = 'app'

            def __init__(self, main_layout):
                super().__init__()
                self.main_layout = main_layout

            @java_method('(Ljava/lang/String;)Ljava/lang/String;')
            def jsCalledPython(self, data_string):
                data = json.loads(data_string)
                self.main_layout.log(f'Received from JS: {data}', 'JS -> Py')
                return f'Got it! Your value was: {data.get("value")}'

            @java_method('(Ljava/lang/String;)V')
            def logToPython(self, message):
                self.main_layout.log(message, 'JS Console')

            @java_method('(Ljava/lang/String;)V')
            def onPageLoaded(self, url):
                self.main_layout.log(f'Page loaded: {url}', 'WebView')

        self.webview = AndroidWebView()
        self.webview.add_js_interface("Android", JsApi(self))
        self.webview_placeholder.add_widget(self.webview.get_webview_widget())
        self.webview.load_url('file:///android_asset/index.html')
        self.log('Android WebView initialized.')

    def setup_desktop_webview(self):
        class Api:
            def __init__(self, main_layout):
                self.main_layout = main_layout

            def js_called_python(self, data):
                self.main_layout.log(f'Received from JS: {data}', 'JS -> Py')
                return f'Got it! Your value was: {data.get("value")}'

            def log_from_js(self, message):
                self.main_layout.log(message, 'JS Console')

        self.api = Api(self)
        html_path = os.path.join(os.path.dirname(__file__), 'assets', 'index.html')

        def _create_window():
            self.webview = webview.create_window(
                'Kivy WebView on Desktop',
                f'file://{os.path.abspath(html_path)}',
                js_api=self.api
            )
            webview.start(debug=True) # debug=True allows right-click inspect

        # Run pywebview in a separate thread
        thread = threading.Thread(target=_create_window)
        thread.daemon = True
        thread.start()
        self.log('Desktop WebView initialized in a separate window.')

    # --- Python to JS Communication ---
    def send_message_to_js(self, *args):
        self.log('Sending message to JS.')
        script = "updateFromPython('Hello from Kivy-Python!');"
        if self.webview:
            if IS_ANDROID:
                self.webview.evaluate_js(script)
            else: # Desktop
                self.webview.evaluate_js(script)

    def change_dom_from_python(self, *args):
        self.log('Requesting JS to change DOM.')
        script = "changeDom();"
        if self.webview:
            if IS_ANDROID:
                self.webview.evaluate_js(script)
            else: # Desktop
                self.webview.evaluate_js(script)

class WebViewApp(App):
    def build(self):
        return MainLayout()

    def on_stop(self):
        # Cleanly close the pywebview window on app exit
        if IS_DESKTOP and self.root and self.root.webview:
            self.root.webview.destroy()

if __name__ == '__main__':
    WebViewApp().run()