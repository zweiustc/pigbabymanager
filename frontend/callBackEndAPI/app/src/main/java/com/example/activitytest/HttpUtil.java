package com.example.activitytest;

import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * Created by kkwang on 3/11/2017.
 */

public class HttpUtil {
    public static void sendHttpRequest(final String address, final HttpCallbackListener listener){
        new Thread(new Runnable() {
            @Override
            public void run() {
                HttpURLConnection connection = null;
                BufferedReader reader = null;
                try{
                    URL url = new URL(address);
                    connection = (HttpURLConnection) url.openConnection();
                    connection.setRequestMethod("GET");
                    connection.setConnectTimeout(8000);
                    connection.setReadTimeout(8000);
                    InputStream in = connection.getInputStream();
                    reader = new BufferedReader(new InputStreamReader(in));
                    StringBuilder response = new StringBuilder();
                    String line;
                    while((line=reader.readLine())!=null){
                        response.append(line);
                    }
                    if(listener!=null)
                    {
                        listener.onFinish(response.toString());
                    }
                }catch (Exception e){
                    if(listener!=null)
                    {
                        listener.onError(e);
                    }
                }finally {
                    if(reader != null){
                        try{
                            reader.close();
                        }catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                    if(connection !=null)
                    {
                        connection.disconnect();
                    }
                }
            }
        }).start();
    }
}
