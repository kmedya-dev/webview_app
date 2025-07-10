from abc import ABC, abstractmethod

class WebViewInterface(ABC):
    @abstractmethod
    def load_url(self, url: str):
        pass

    @abstractmethod
    def evaluate_js(self, script: str, callback=None):
        pass

    @abstractmethod
    def add_js_interface(self, name: str, obj):
        pass

    @abstractmethod
    def get_webview_widget(self):
        pass
