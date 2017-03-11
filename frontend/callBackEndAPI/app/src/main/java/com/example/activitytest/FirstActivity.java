package com.example.activitytest;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.view.menu.ExpandedMenuView;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.google.gson.Gson;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.StringReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class FirstActivity extends AppCompatActivity implements View.OnClickListener{

    TextView responseText;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.first_layout);
        Button sendRequest = (Button) findViewById(R.id.send_boar_request);
        responseText = (TextView) findViewById(R.id.response_text);
        sendRequest.setOnClickListener(this);
        sendRequest = (Button) findViewById(R.id.send_sow_request);
        responseText = (TextView) findViewById(R.id.response_text);
        sendRequest.setOnClickListener(this);
    }
    @Override
    public void onClick(View v){
        if(v.getId()==R.id.send_boar_request){
            String address = "http://180.76.148.62:8888/v1/boars/3";
            HttpUtil.sendHttpRequest(address, new HttpCallbackListener() {
                @Override
                public void onFinish(String response) {
                    parseBoar(response);
                    showResponse(response);
                }

                @Override
                public void onError(Exception e) {

                }
            });
        }
        if(v.getId()==R.id.send_sow_request){
            String address = "http://180.76.148.62:8888/v1/sows/2";
            HttpUtil.sendHttpRequest(address, new HttpCallbackListener() {
                @Override
                public void onFinish(String response) {
                    parseSow(response);
                    showResponse(response);
                }

                @Override
                public void onError(Exception e) {

                }
            });
        }
    }

    private void showResponse(final String response){
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                responseText.setText(response);
            }
        });
    }

    private void parseBoar(String jsonData){
        try{
            JSONObject jsonObject = new JSONObject(jsonData);
            String boar_info = jsonObject.getString("boar");
            Gson gson = new Gson();
            Boar boar = gson.fromJson(boar_info,Boar.class);
            Log.d("boar", boar.getBreedAccept());
        }catch (Exception e){
            e.printStackTrace();
        }
    }

    private void parseSow(String jsonData){
        try{
            JSONObject jsonObject = new JSONObject(jsonData);
            String sow_info = jsonObject.getString("sow");
            Gson gson = new Gson();
            Sow sow = gson.fromJson(sow_info,Sow.class);
            Log.d("sow", sow.getEarLack());
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
