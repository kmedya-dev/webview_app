from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.webview import WebView
from kivy.utils import platform
import os

class ErudaBrowserApp(App):
    def build(self):
        self.title = 'ErudaBrowser'
        layout = BoxLayout(orientation='vertical')

        # Path to your local HTML file in assets folder
        # For Android, assets are typically accessed via 'file:///android_asset/'
        if platform == 'android':
            local_html_path = 'file:///android_asset/index.html'
        else:
            # For desktop/other platforms, use a relative path
            local_html_path = os.path.join(self.directory, 'assets', 'index.html')

        self.url_input = TextInput(
            text=local_html_path, # Default to loading local HTML
            size_hint_y=None,
            height='48dp',
            multiline=False
        )
        self.url_input.bind(on_text_validate=self.load_url)

        self.webview = WebView()

        browse_button = Button(
            text='Go',
            size_hint_y=None,
            height='48dp'
        )
        browse_button.bind(on_press=self.load_url)

        nav_bar = BoxLayout(size_hint_y=None, height='48dp')
        nav_bar.add_widget(self.url_input)
        nav_bar.add_widget(browse_button)

        layout.add_widget(nav_bar)
        layout.add_widget(self.webview)

        self.load_url() # Load initial URL

        return layout

    def load_url(self, instance=None):
        url = self.url_input.text
        # Basic URL validation/prefixing for external URLs
        if not url.startswith(('http://', 'https://', 'file://')):
            url = 'http://' + url
        self.webview.url = url

if __name__ == '__main__':
    ErudaBrowserApp().run()