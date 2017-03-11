package com.example.activitytest;

/**
 * Created by kkwang on 3/11/2017.
 */

public interface HttpCallbackListener {
    void onFinish(String response);
    void onError(Exception e);
}
