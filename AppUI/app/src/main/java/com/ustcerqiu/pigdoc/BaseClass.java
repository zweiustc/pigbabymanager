package com.ustcerqiu.pigdoc;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;

/**
 * Created by ustcerQ on 2017/2/28.
 */

public class BaseClass extends AppCompatActivity {

    @Override
    protected void onPause() {
        super.onPause();
        overridePendingTransition(R.anim.translate_in, R.anim.translate_out);
    }//onPause


}
