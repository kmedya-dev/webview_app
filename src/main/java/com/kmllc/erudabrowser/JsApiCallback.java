package com.kmllc.erudabrowser;

import android.webkit.JavascriptInterface;

public interface JsApiCallback {
    @JavascriptInterface
    String jsCalledPython(String data);

    @JavascriptInterface
    void logToPython(String message);

    @JavascriptInterface
    void onPageLoaded(String url);
}