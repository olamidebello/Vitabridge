package com.olamide.vitabridge;
import android.app.Activity;
import android.os.Bundle;
import android.webkit.*;
import android.net.Uri;
import android.content.Intent;
import android.widget.*;
public class MainActivity extends Activity {
 private WebView web;
 private static final String HOME="https://vitabridge.olamidemedical.health/";
 private boolean trusted(Uri u){return "https".equals(u.getScheme())&&"vitabridge.olamidemedical.health".equals(u.getHost())&&(u.getPort()==-1||u.getPort()==443);}
 @Override public void onCreate(Bundle state){super.onCreate(state);web=new WebView(this);setContentView(web);WebSettings s=web.getSettings();s.setJavaScriptEnabled(true);s.setDomStorageEnabled(true);s.setAllowFileAccess(false);s.setAllowContentAccess(false);s.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);CookieManager.getInstance().setAcceptThirdPartyCookies(web,false);
 web.setWebViewClient(new WebViewClient(){@Override public boolean shouldOverrideUrlLoading(WebView v,WebResourceRequest request){Uri u=request.getUrl();if(trusted(u))return false;if("https".equals(u.getScheme())||"mailto".equals(u.getScheme())){try{startActivity(new Intent(Intent.ACTION_VIEW,u));}catch(Exception e){Toast.makeText(MainActivity.this,"No app available for this link",Toast.LENGTH_LONG).show();}}return true;}
 @Override public void onReceivedError(WebView v,WebResourceRequest req,WebResourceError err){if(req.isForMainFrame())Toast.makeText(MainActivity.this,"Connection unavailable. This preview cannot dispatch an ambulance. Use local emergency services if needed.",Toast.LENGTH_LONG).show();}});
 web.loadUrl(HOME);}
 @Override public void onBackPressed(){if(web.canGoBack())web.goBack();else super.onBackPressed();}
 @Override protected void onDestroy(){if(web!=null)web.destroy();super.onDestroy();}
}
