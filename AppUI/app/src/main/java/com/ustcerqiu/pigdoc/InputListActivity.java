package com.ustcerqiu.pigdoc;

import android.content.Context;
import android.content.Intent;
import android.os.Parcel;
import android.os.Parcelable;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import java.io.Serializable;
import java.util.List;

public class InputListActivity extends AppCompatActivity {
    //属性区域
    //定义 数组用以保存 传递过来的 子项数据
    private mCom.ParcelableItem[] itemList; //parcelable属性在本页面内并没作用; 此处是为了保存intent中数据方便

///////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    //定义启动办法,和所需要的数据，方便其它程序转调;
    public static void actionStart(Context context, String titleName, mCom.ParcelableItem[] parcelableItemList){
        Intent intent = new Intent(context, InputListActivity.class);
        intent.putExtra("titleName", titleName); //传入标题，必须
        intent.putExtra("parcelableItemList", parcelableItemList); //传入对应项的item相关数据
        context.startActivity(intent);
    }

    //定义 item各项所需的数据的类型,采用parcelable接口，以便对象和数组通过intent传递；
 /*   public static class ParcelableItem implements Parcelable{
        //定义各行数据所需要的数据
        private int imageId; //图片id, 默认是一头存钱猪
        private String name; //子项中功能名称
        private String[] funcParams; //子项中标记 功能类型的字符串数组，第一项是type标记，后面可选，可用以区分进一步功能页面的加载内容模板等信息
        //定义设置属性的构造方法; 给外部数据生成对象实例用
        public ParcelableItem(int imageId, String name, String[] funcParams){
            this.imageId = imageId;
            this.name = name;
            this.funcParams = funcParams;
        }
        //定义获取属性值方法
        public int getImageId(){return imageId;}
        public String getName(){return name;}
        public String[] getFuncParams(){return funcParams;}

        //实现parcelable的接口, 定义content描述，定义writeToParcel的流序列（网络数据不建议，无法保证连续性，此时可用serializable接口）,
        // 定义create的静态接口变量   必须
        @Override
        public int describeContents() {
            return 0;
        }

        //定义如何将数据写入 数据流 ；主要是顺序
        @Override
        public void writeToParcel(Parcel dest, int flags) {
            //写入流的顺序, 此后需要按此顺序读出
            dest.writeInt(imageId);
            dest.writeString(name);
            //数组需要纪录数组长度，读取时候需要先根据长度定义数组指针实例；
            dest.writeInt(funcParams.length);
            dest.writeStringArray(funcParams);
        }

        //构造函数，用以将parcelable中数据读出到 实例中; 对应上面的writeToParcel顺序
        public ParcelableItem(Parcel in){
            imageId = in.readInt();
            name = in.readString();
            int length = in.readInt();  //读取数组长度
            funcParams = new String[length]; //给数组指针 赋内部项目指针
            in.readStringArray(funcParams); //读取数组， 数组需要大小。list不需要设置大小
        }

        //必须定义的 CREATOR 域，表明了创建方法
        public static final Parcelable.Creator<ParcelableItem> CREATOR = new Creator<ParcelableItem>() {
            @Override
            public ParcelableItem createFromParcel(Parcel source) {
                return new ParcelableItem(source);  //定义对象的读取建立方式，即，将数据流中数据构造实例
            }

            @Override  //此序列化的读法，适用于array list 等，内部实现就是这样的。此处我们前后文都用array是为了提高性能
            public ParcelableItem[] newArray(int size) {
                return new ParcelableItem[size];  //定义数据流数组的读取建立方式，将数据流生成 数据数组； 每个元素使用上面对象的实例创建方式；
            }
        };
    }//ParcelableItem
*/


    //定义次活动所调用recyclerView的adapter 和 viewholder
    //定义ViewHolder, mViewHolder，保存必要锚，继承的类必须实现的构造方法，其中view会作为参数传入
    private class mViewHolder extends RecyclerView.ViewHolder{
        ImageView funcImage;
        TextView funcName;
        //////////////////////////////////////////////
        public mViewHolder(View v){
            super(v);
            funcImage = (ImageView) v.findViewById(R.id.item_image);
            funcName = (TextView) v.findViewById(R.id.item_name);
        }
    }//class mViewHolder

    //定义 Adapter，mAdapter ; 基于自定义的viewholder实现继承类
    private class mAdapter extends RecyclerView.Adapter<mViewHolder>{
        //是否必须？？？此属性直接引用了所需用的数据实例
        private mCom.ParcelableItem[] mItemList;  //明确使用的数据
        private int itemLayoutId;  //明确使用的子项布局id

        //构造函数，明确了所引用的数据和布局，相对于直接调用活动中的属性，相当于便于人阅读了;
        public mAdapter(mCom.ParcelableItem[] itemList, int itemLayoutId){
            mItemList = itemList;
            this.itemLayoutId = itemLayoutId;
        }

        //定义创建适配器中的viewholder实例的方法; 返回实例，供adapter内部调用
        //parent即为调用方，也就是setAdapter的实例，此处应为对应的RecyclerView的布局组件
        @Override
        public mViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
            View view = LayoutInflater.from(parent.getContext()).inflate(itemLayoutId, parent, false);  //读取布局文件，生成view组件，不加入；
            final mViewHolder holder = new mViewHolder(view); //申明全局，使得虚拟函数可以调用
            //定义点击动作，此处可避免反复定义
            view.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    int positon = holder.getAdapterPosition(); //取出当前被点击view的位置
                    mCom.ParcelableItem item = itemList[positon]; //取出功能数据
                    mCom.doClickFunc(v,item); //执行操作；操作所处的环境是 v的contex()
                }//on click
            });
            return holder;
        }//onCreateViewHolder

        //重构 单个item进入视野时的执行方法，也就是view在加入视图之前所做的事情
        @Override
        public void onBindViewHolder(mViewHolder holder, int position) {
            mCom.ParcelableItem item = mItemList[position]; //取出对应的数据
            holder.funcImage.setImageResource(item.getImageId());
            holder.funcName.setText(item.getName());
        }//onBindViewHolder

        @Override
        public int getItemCount() {
            return mItemList.length;
        }
    }//class mAdapter



////--##############################################################################-----/////
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.input_list_activity);

        String titleName = getString(R.string.app_name);  //设置默认的title名
        //Intent中信息处理
        Intent intent = getIntent(); //getIntent 用以取得启动此活动的intent
        if(intent != null){ //intent中有数据; 如不符合一下数据类型，就直接bug了；
            titleName = intent.getStringExtra("titleName");
            Parcelable[] parcelableAr = intent.getParcelableArrayExtra("parcelableItemList");  //将类型强制转化
            itemList = new mCom.ParcelableItem[parcelableAr.length];  //此处有深坑，数组整体强制类型转化，必须先给其定义大小（其实就是内部子指针要实例话
            for(int i=0; i<parcelableAr.length; i++){
                itemList[i] = (mCom.ParcelableItem) parcelableAr[i]; //这句，直接用数组名强制转化，总是出错，？？？？？才写了此循环；以后还是用list吧
            }
        }//if  intent

        //设置标题行的显示标题，替换掉layout中的默认标题
        ((TextView) this.findViewById(R.id.title_name_textView)).setText(titleName);  //this仅仅是强调本活动的调用环境
        //设置返回键的操作
        (findViewById(R.id.button_back)).setOnClickListener(new View.OnClickListener() {  //无需限制view的具体形式，所以没有强制类型转化
            @Override
            public void onClick(View v) {
                //定义返回前的操作，返回数据到前一活动用 setResult方法
                finish(); //
                overridePendingTransition(R.anim.translate_in_back, R.anim.translate_out_back);  //添加返回切换动画
            }
        });


        //设置内部功能的recyclerview内容填充
        RecyclerView recyclerView = (RecyclerView) findViewById(R.id.input_list_RecyclerView);
        LinearLayoutManager layoutManager = new LinearLayoutManager(this);
        layoutManager.setOrientation(LinearLayoutManager.VERTICAL);
        recyclerView.setLayoutManager(layoutManager);
        mAdapter adapter = new mAdapter(itemList, R.layout.func_item_layout);
        recyclerView.setAdapter(adapter);



    }//onCreate

    @Override
    public void onBackPressed() {
        //重写点击安卓返回键后的动作
        // super.onBackPressed();
        finish(); //
        overridePendingTransition(R.anim.translate_in_back, R.anim.translate_out_back);  //添加返回切换动画
    }




}//the activity class
