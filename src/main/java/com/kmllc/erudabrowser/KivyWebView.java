package com.kmllc.erudabrowser;

import android.content.Context;
import android.util.Log;
import android.view.ViewGroup;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebChromeClient;
import org.kivy.android.PythonActivity; // Assuming PythonActivity is the base

public class KivyWebView extends WebView {

    private static final String TAG = "KivyWebView";
    private PythonActivity mActivity;

    public KivyWebView(Context context) {
        super(context);
        if (context instanceof PythonActivity) {
            mActivity = (PythonActivity) context;
        } else {
            Log.e(TAG, "Context is not PythonActivity. Some features might not work.");
        }

        // Basic WebView settings
        WebSettings webSettings = this.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setDomStorageEnabled(true);
        webSettings.setAllowFileAccess(true); // For file:///android_asset/
        webSettings.setAllowContentAccess(true);

        // Set a WebViewClient to handle page loading
        this.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                Log.d(TAG, "Loading URL: " + url);
                // You can add logic here to intercept URLs if needed
                return false; // Return false to let WebView load the URL
            }
        });

        // Set a WebChromeClient to handle console messages, alerts, etc.
        this.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onConsoleMessage(android.webkit.ConsoleMessage consoleMessage) {
                Log.d(TAG, "JS Console: " + consoleMessage.message() + " -- From line "
                        + consoleMessage.lineNumber() + " of "
                        + consoleMessage.sourceId());
                // Pass console message to Python
                if (mActivity != null) {
                    mActivity.callPython("on_console_message", consoleMessage.message());
                }
                return true; // Indicate that we've handled the message
            }
        });

        // Add a JavaScript interface for JS to Python communication
        this.addJavascriptInterface(new KivyWebViewInterface(mActivity), "Android");
    }

    // Interface for JavaScript to call Python methods
    private class KivyWebViewInterface {
        PythonActivity activity;

        KivyWebViewInterface(PythonActivity activity) {
            this.activity = activity;
        }

        @android.webkit.JavascriptInterface
        public void callPython(final String functionName, final String message) {
            Log.d(TAG, "JS called Python function: " + functionName + " with message: " + message);
            if (activity != null) {
                activity.callPython(functionName, message);
            }
        }
    }

    // Public method to load a URL
    public void loadUrlFromPython(final String url) {
        mActivity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                KivyWebView.this.loadUrl(url);
            }
        });
    }

    // Public method to evaluate JavaScript
    public void evaluateJavascriptFromPython(final String script) {
        mActivity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                KivyWebView.this.evaluateJavascript(script, null);
            }
        });
    }
}