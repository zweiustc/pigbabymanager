package com.ustcerqiu.pigdoc;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

public class NotesActivity extends BaseClass {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.notes_activity);
        //设置底部导航条的动作
        new SetNavigatorClass().setClickOnNavigator(this, 2);  //this指代最近的类的实例


    }
}
