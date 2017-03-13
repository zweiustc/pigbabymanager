package com.ustcerqiu.pigdoc;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

public class LogActivity extends BaseClass {
    private String[] nameAndPassword = {"181234567890", "123456"}; //测试用账号和密码

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.log_activity_layout);

        Button button = (Button) findViewById(R.id.login_button1_signin);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String account = ((TextView) findViewById(R.id.phone_number)).getText().toString();
                String password = ((TextView) findViewById(R.id.password)).getText().toString();
                if(account.equals(nameAndPassword[0]) && password.equals(nameAndPassword[1])){
                    startActivity(new Intent(LogActivity.this, MainActivity.class));
                }else{
                    Toast.makeText(LogActivity.this, "账户名或者密码错误", Toast.LENGTH_SHORT).show();
                    startActivity(new Intent(LogActivity.this, MainActivity.class)); //test 阶段用
                }
            }
        });
    }
}
