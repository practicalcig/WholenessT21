package com.team21.wholeness;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.View;
import android.view.WindowManager;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebResourceRequest;
import android.webkit.PermissionRequest;

public class MainActivity extends Activity {

    private WebView webView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Edge-to-edge friendly: deep dark background to match the app
        getWindow().setStatusBarColor(0xFF080A0E);
        getWindow().setNavigationBarColor(0xFF080A0E);

        setContentView(R.layout.activity_main);
        webView = findViewById(R.id.webview);

        configureWebView();

        // Load the local HTML asset
        webView.loadUrl("file:///android_asset/web/index.html");
    }

    private void configureWebView() {
        WebSettings s = webView.getSettings();

        // Core web features
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);          // localStorage
        s.setDatabaseEnabled(true);
        s.setLoadsImagesAutomatically(true);
        s.setMediaPlaybackRequiresUserGesture(false);

        // Layout
        s.setUseWideViewPort(true);
        s.setLoadWithOverviewMode(true);
        s.setSupportZoom(false);
        s.setBuiltInZoomControls(false);
        s.setDisplayZoomControls(false);
        s.setTextZoom(100);

        // Allow file:// asset to fetch local resources only (Google Fonts still loads via network)
        s.setAllowFileAccess(true);
        s.setAllowContentAccess(true);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN) {
            s.setAllowFileAccessFromFileURLs(false);
            s.setAllowUniversalAccessFromFileURLs(false);
        }

        // Mixed content (allow https fonts; everything else is local)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            s.setMixedContentMode(WebSettings.MIXED_CONTENT_COMPATIBILITY_MODE);
        }

        // User agent suffix so site code can detect the app if needed
        s.setUserAgentString(s.getUserAgentString() + " WholenessApp/1.0");

        // Cache
        s.setCacheMode(WebSettings.LOAD_DEFAULT);

        // Background - matches splash to avoid white flash
        webView.setBackgroundColor(0xFF080A0E);

        // Force dark color scheme on the WebView host (CSS already handles theme)
        webView.setOverScrollMode(View.OVER_SCROLL_NEVER);

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest req) {
                Uri url = req.getUrl();
                String scheme = url.getScheme();
                String host = url.getHost();

                // Stay inside the WebView for our own asset URLs
                if ("file".equals(scheme)) return false;

                // External http(s) links open in the user's browser
                if ("http".equals(scheme) || "https".equals(scheme)) {
                    // Allow Google Fonts inline (these come through as resource loads, not nav)
                    if (host != null && (host.endsWith("fonts.googleapis.com") || host.endsWith("fonts.gstatic.com"))) {
                        return false;
                    }
                    try {
                        startActivity(new Intent(Intent.ACTION_VIEW, url));
                    } catch (Exception ignored) {}
                    return true;
                }

                // mailto:, tel:, etc.
                try {
                    startActivity(new Intent(Intent.ACTION_VIEW, url));
                } catch (Exception ignored) {}
                return true;
            }
        });

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onPermissionRequest(PermissionRequest request) {
                request.deny();
            }
        });
    }

    // Hardware back button: navigate WebView history before exiting
    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK && webView != null && webView.canGoBack()) {
            webView.goBack();
            return true;
        }
        return super.onKeyDown(keyCode, event);
    }

    @Override
    protected void onPause() {
        super.onPause();
        if (webView != null) webView.onPause();
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (webView != null) webView.onResume();
    }

    @Override
    protected void onDestroy() {
        if (webView != null) {
            webView.loadUrl("about:blank");
            webView.destroy();
            webView = null;
        }
        super.onDestroy();
    }
}
