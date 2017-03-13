package com.ustcerqiu.pigdoc;

import android.content.Intent;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class LaunchActivity extends AppCompatActivity {
    private int time_count = 4;
    private TextView textTime;
    Handler handler;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.launch_layout);

        //倒计时显示后，自动跳转到主活动，或者，登陆页面
        textTime = (TextView) findViewById(R.id.launch_text3_time);
        textTime.setText("" + time_count);
        handler = new Handler();
        handler.postDelayed(runTimeCounter, 1000);
    }

    Runnable runTimeCounter = new Runnable() {
        @Override
        public void run() {
            time_count --;
            if (time_count>0){
                textTime.setText("" + time_count);
                handler.postDelayed(this, 1000);
            }else{
                startActivity(new Intent(LaunchActivity.this, LogActivity.class));
                LaunchActivity.this.finish();
            }
        }
    };

    @Override
    protected void onPause() {
        super.onPause();
        overridePendingTransition(R.anim.translate_in, R.anim.translate_out);
    }
}
