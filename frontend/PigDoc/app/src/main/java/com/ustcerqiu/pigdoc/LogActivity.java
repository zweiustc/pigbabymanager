package com.ustcerqiu.pigdoc;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class LogActivity extends BaseClass {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.log_activity_layout);

        Button button = (Button) findViewById(R.id.login_button1_signin);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(LogActivity.this, MainActivity.class));
            }
        });
    }
}
