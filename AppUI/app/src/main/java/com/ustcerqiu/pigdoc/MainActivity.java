package com.ustcerqiu.pigdoc;

import android.content.Intent;
import android.content.res.Resources;
import android.content.res.TypedArray;
import android.graphics.drawable.ClipDrawable;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends BaseClass {
 //内部属性定义区
    //定义进度条内部的图像id，百分比id, 文字id，进度值，文字值;(一一对应关系
    private final int[] levelImgIds = {R.id.main_rate_1, R.id.main_rate_2, R.id.main_rate_3, R.id.main_rate_4, R.id.main_rate_5, R.id.main_rate_6};
    private final int[] levelPercentIds = {R.id.main_rate_percent_1, R.id.main_rate_percent_2, R.id.main_rate_percent_3, R.id.main_rate_percent_4, R.id.main_rate_percent_5, R.id.main_rate_percent_6};
    private final int[] levelTextIds = {R.id.main_rate_text_1, R.id.main_rate_text_2, R.id.main_rate_text_3, R.id.main_rate_text_4, R.id.main_rate_text_5, R.id.main_rate_text_6};
    private int[] levelValues = {4560, 5000, 6000, 7000, 8000, 9000};
    private String[] levelTexts = {"456/1000", "50/100", "6000/10000", "14/20", "80/100", "12只/15max"};

    //布局中各种按钮的 id ，并设置点击后动作（进度条，常用功能，输入功能)
    private final int[] statusButtonIds = {R.id.main_status_1, R.id.main_status_2, R.id.main_status_3, R.id.main_status_4, R.id.main_status_5, R.id.main_status_6};
    private final int[] commonButtonIds = {R.id.main_icon_daily_report, R.id.main_icon_pig_statistics, R.id.main_icon_data_view,  R.id.main_icon_settings };
    private final int[] inputButtonIds = {R.id.main_data_input0, R.id.main_data_input1, R.id.main_data_input2, R.id.main_data_input3, R.id.main_data_input4,
            R.id.main_data_input5, R.id.main_data_input6, R.id.main_data_input7, R.id.main_data_input8, R.id.main_data_input10};

    //i输入功能中，全部功能，点击后用以显示所有功能列表，所需要传入的数据（图标，名称，点击后的动作类型及其它数据）
    //  需要 InputListActivity 中的 ParcelableItem 类数组
    private mCom.ParcelableItem[] parcelableItemList;


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main_activity_layout);
        //设置底部导航条的动作
        new SetNavigatorClass().setClickOnNavigator(this, 0);  //this指代最近的类的实例，此处就是MainActivity；
        //定义用户信息和显示

        //设置主状态条信息和显示
        ImageView image;
        ClipDrawable clipDrawable;
        for(int i=0; i<levelImgIds.length;i++){
            image = (ImageView) findViewById(levelImgIds[i]);
            clipDrawable = (ClipDrawable) image.getBackground();
            clipDrawable.setLevel(levelValues[i]);
            ( (TextView)findViewById(levelPercentIds[i]) ).setText( String.format(" %.1f%%",levelValues[i]/100.0) );
            ( (TextView)findViewById(levelTextIds[i]) ).setText(levelTexts[i]);
        }//for

        //设置主状态条的点击后的效果
        LinearLayout layout;
        for(int id : statusButtonIds){
            layout = (LinearLayout) findViewById(id);
            layout.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    ViewGroup vp = (ViewGroup) v;
                    String toastMassage = ((TextView)vp.getChildAt(0)).getText() + " =: " + ((TextView)vp.getChildAt(2)).getText();
                    Toast.makeText(MainActivity.this, toastMassage, Toast.LENGTH_SHORT).show();
                }
            });
        } //for

        //设置常用功能键的点击后的效果
        for(int Id : commonButtonIds){
            layout = (LinearLayout) findViewById(Id);
            layout.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    ViewGroup vp = (ViewGroup) v;
                    String toastMassage = "你点击了： " + ((TextView)vp.getChildAt(1)).getText();
                    Toast.makeText(MainActivity.this, toastMassage, Toast.LENGTH_SHORT).show();
                }
            });
        } //for

        //数据输入全部 点击后的功能列表所需的数据
        Resources res = getResources();
        String[] input_func_names = res.getStringArray(R.array.input_func_names); //直接调用
        TypedArray imageAr = res.obtainTypedArray(R.array.input_func_images); //只是获取图片的xml引用方式， 这个用过后需要释放
        String[] funcAr = res.getStringArray(R.array.detai_func_type_array);
        int[] indexes = res.getIntArray(R.array.input_func_indexes);
        int input_func_length = input_func_names.length;
        String[][] itemFuncParamAr = {  //数据列表中，功能参数的设定，type由xml中设定好了，直接引用
                {funcAr[indexes[0]]}, {funcAr[indexes[1]]}, {funcAr[indexes[2]]}, {funcAr[indexes[3]]}, {funcAr[indexes[4]]},
                {funcAr[indexes[5]]}, {funcAr[indexes[6]]}, {funcAr[indexes[7]]}, {funcAr[indexes[8]]}, {funcAr[indexes[9]]},
                {funcAr[indexes[10]]}, {funcAr[indexes[11]]}, {funcAr[indexes[12]]}, {funcAr[indexes[13]]}
        };
        parcelableItemList = new mCom.ParcelableItem[input_func_length]; //定义指针
        for(int i=0; i<input_func_length; i++){  //创建功能列表所需的数据列表
            parcelableItemList[i] = new mCom.ParcelableItem( imageAr.getResourceId(i,0), input_func_names[i], itemFuncParamAr[i] );
        }//for
        imageAr.recycle(); //回收资源读取

        //设置数据输入按钮的点击后的效果
        for(int i=0; i<inputButtonIds.length; i++){
            layout = (LinearLayout) findViewById(inputButtonIds[i]);
            if(i == inputButtonIds.length-1){  //最后一个功能是  全部
                layout.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        InputListActivity.actionStart(MainActivity.this, "猪博士 -- 操作与数据录入", parcelableItemList);  //后面动作，暂时的 TODO
                    }
                });
            }else{
                layout.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        ViewGroup vp = (ViewGroup) v;
                        String toastMassage = "您权限不够： " + ((TextView)vp.getChildAt(1)).getText();
                        Toast.makeText(MainActivity.this, toastMassage, Toast.LENGTH_SHORT).show();
                    }
                });
            }//if else

        } //for








    }//onCreate
}


