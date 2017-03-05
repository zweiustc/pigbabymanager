package com.ustcerqiu.pigdoc;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

public class StatusActivity extends BaseClass {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.status_activity_layout);
        //设置底部导航条的动作
        new SetNavigatorClass().setClickOnNavigator(this, 3);  //this指代最近的类的实例


    }
}
