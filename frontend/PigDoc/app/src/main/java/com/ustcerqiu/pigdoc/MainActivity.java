package com.ustcerqiu.pigdoc;

import android.graphics.drawable.ClipDrawable;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.ImageView;

public class MainActivity extends BaseClass {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main_activity_layout);
        //设置底部导航条的动作
        new SetNavigatorClass().setClickOnNavigator(this, 0);  //this指代最近的类的实例，此处就是MainActivity；

        ImageView image = (ImageView) findViewById(R.id.image_rate_1);
        ClipDrawable clipDrawable = (ClipDrawable) image.getBackground();
        clipDrawable.setLevel(8000);







    }
}


