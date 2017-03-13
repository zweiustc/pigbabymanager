package com.ustcerqiu.pigdoc;

import android.app.Activity;
import android.content.Intent;
import android.support.v4.content.ContextCompat;
import android.view.View;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

/**
 * Created by ustcerQ on 2017/2/27.
 */

public class SetNavigatorClass {
    //给底部导航条加动作的方法
    //静态函数的方式，将导致活动context的滞留，容易导致内存泄漏，所以必须保证同时只有一个在使用中
    private   Activity actThis;  //定义此，成为类属性，才能在匿名函数或子函数中使用,并且记得用后一定要释放掉。
    //纪录导航条的子项目的layout 和里面的图片以及文字的 id，为后面加载动作做准备。
    private static final int[] ids = {R.id.navigator_b0_home, R.id.navigator_b1_message, R.id.navigator_b2_notes, R.id.navigator_b3_status, R.id.navigator_b4_chart};
    private static final int[] imageIds  ={R.id.nav_b0_image, R.id.nav_b1_image, R.id.nav_b2_image, R.id.nav_b3_image, R.id.nav_b4_image};
    private static final int[] imageIds_s  ={R.drawable.ic_home_s, R.drawable.ic_messag_s, R.drawable.ic_notes_s, R.drawable.ic_status_s, R.drawable.ic_chart_s};
    private static final int[] textIds ={R.id.nav_b0_text, R.id.nav_b1_text, R.id.nav_b2_text, R.id.nav_b3_text, R.id.nav_b4_text};
    //对应的 activity为{ MainActivity, MessageActivity, NotesActivity,  StatusActivity, ChartActivity }


    public void setClickOnNavigator(Activity context, int mark){
        //给导航条内部layout设置点击事件，并给对应当前活动取消点击事件，并给图片和背景标识；
        this.actThis = context; //传入的活动的 context，此环境将作为后面寻找对象和设置活动的环境
        LinearLayout[] layouts = new LinearLayout[5];
        //if中设置点击事件，在else中进行属性设置；
        for(int i=0; i<5; i++){
            layouts[i] = (LinearLayout) context.findViewById(ids[i]);  //将传入的活动环境作为当前寻找view的环境。
            if(i != mark ) {
                layouts[i].setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        switch (v.getId()){
                            case R.id.navigator_b0_home:
                                //必须使用actThis因为，这表明intent的执行环境是传入的活动context
                                actThis.startActivity(new Intent("com.ustcerqiu.pigdoc.MAIN_ACTIVITY")); //隐式活动跳转
                                break;
                            case R.id.navigator_b1_message:
                                actThis.startActivity(new Intent(actThis, MessageActivity.class));
                                break;
                            case R.id.navigator_b2_notes:
                                actThis.startActivity(new Intent(actThis, NotesActivity.class));
                                break;
                            case R.id.navigator_b3_status:
                                actThis.startActivity(new Intent(actThis, StatusActivity.class));
                                break;
                            case R.id.navigator_b4_chart:
                                actThis.startActivity(new Intent(actThis, ChartActivity.class));
                                break;
                            default:
                                break;
                        }
                    }
                });
            }else{
                //设置当前页面的图标没有点击效果，并且更换部分显示标记，以突出显示
                layouts[mark].setClickable(false);  //并未设置click事件，因为style中设置允许接听click，则无事件会点击死机，所以需要取消可点击属性；
                ((ImageView)context.findViewById(imageIds[mark])).setImageResource(imageIds_s[mark]);
                ((TextView) context.findViewById(textIds[mark])).setTextColor(ContextCompat.getColor(actThis, R.color.navigator_selected ));
            }
            if(i>=5){
                this.actThis = null; //释放传入的活动环境，以便节约内存等。
            }
        }
    }
}
