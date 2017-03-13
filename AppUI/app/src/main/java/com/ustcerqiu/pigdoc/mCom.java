package com.ustcerqiu.pigdoc;

import android.content.Context;
import android.os.Parcel;
import android.os.Parcelable;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.widget.Toast;

import java.util.List;

/**
 * Created by ustcerQ on 2017/3/12.
 * 此方法用以纪录全局通用的方法和类
 */

public class mCom {
    //属性定义区

//////////////////////////////////////////////////////

//################# 功能块1-0 ####################
    //定义view的点击事件选择，基于内部的 ParcelableItem 类
    //基于item内部的 imageId funcName funcParams来设置执行不同的方法或活动；活动区分基于 inputList的种类
    //view通过点击事件确认被点击的view，对应的数据为item
    static public void doClickFunc(View v, ParcelableItem item){
        String[] funcP = item.getFuncParams(); //第一项为functype，用以识别不同的功能；
        String type = funcP[0];
        Context context = v.getContext(); //执行上下文
        String[] funcList = context.getResources().getStringArray(R.array.detai_func_type_array); //这行如此写，是为了让引用 和 标记的string不会出现拼写错误
        //不好引用常量，所以用if做
        if( type.equals( funcList[ 0 ] )){ //第一行功能类型标记
            //自定义的活动等操作内容，用以替换下面的信息显示
            Toast.makeText(context, "暂无权限0：" + item.getName(), Toast.LENGTH_SHORT).show();
        }else if( type.equals( funcList[ 1 ] )){
            //TODO
            Toast.makeText(context, "暂无权限1：" + item.getName(), Toast.LENGTH_SHORT).show();
        }else if( type.equals( funcList[ 2 ] )) {
            //TODO
            Toast.makeText(context, "暂无权限2：" + item.getName(), Toast.LENGTH_SHORT).show();
        }
        else if( type.equals( funcList[ 3 ] )) {
            //TODO
            Toast.makeText(context, "暂无权限3：" + item.getName(), Toast.LENGTH_SHORT).show();
        }
        else if( type.equals( funcList[ 4 ] )) {
            //TODO
            Toast.makeText(context, "暂无权限4：" + item.getName(), Toast.LENGTH_SHORT).show();
        }else if( type.equals( funcList[ 5 ] )) {
            //TODO
            Toast.makeText(context, "暂无权限5：" + item.getName(), Toast.LENGTH_SHORT).show();
        }else{
            Toast.makeText(context, "超出功能设置，超出功能定义范围" + item.getName(), Toast.LENGTH_SHORT).show();
        } //if
    }//doClickFunc


//################# 功能块1-1 ####################
    //定义view的点击事件选择，基于funcName 和 funcParams; 其中funcParams第一项为活动类型, funcName为备选参数(名称或标记名称)
    //功能选择列表基于 通用功能列表，便于全局统一。同时取消对自定义类的依赖
    //view通过点击事件自动传入被点击的view
    static public void doClickFuncSelect(View v, String funcName, String[] funcParams){
        //funcParams//第一项为functype，用以识别不同的功能；
        String type = funcParams[0];
        Context context = v.getContext(); //执行上下文
        String[] funcList = context.getResources().getStringArray(R.array.com_detail_func_types); //这行如此写，是为了让引用 和 标记的string不会出现拼写错误
        //不好引用常量，所以用if做
        if( type.equals( funcList[ 0 ] )){
            //第一行功能类型标记, 一般认为没有动作 定义。取消点击属性
            v.setClickable(false);
            //Toast.makeText(context, "暂无权限0：" + funcName, Toast.LENGTH_SHORT).show();
        }else if( type.equals( funcList[ 1 ] )){
            //TODO
            Toast.makeText(context, "暂无权限1：" + funcName, Toast.LENGTH_SHORT).show();
        }else if( type.equals( funcList[ 2 ] )) {
            //TODO
            Toast.makeText(context, "暂无权限2：" + funcName, Toast.LENGTH_SHORT).show();
        }
        else if( type.equals( funcList[ 3 ] )) {
            //TODO
            Toast.makeText(context, "暂无权限3：" + funcName, Toast.LENGTH_SHORT).show();
        }
        else if( type.equals( funcList[ 4 ] )) {
            //TODO
            Toast.makeText(context, "暂无权限4：" + funcName, Toast.LENGTH_SHORT).show();
        }else if( type.equals( funcList[ 5 ] )) {
            //TODO
            Toast.makeText(context, "暂无权限5：" + funcName, Toast.LENGTH_SHORT).show();
        }else{
            Toast.makeText(context, "超出功能设置，超出功能定义范围" + funcName, Toast.LENGTH_SHORT).show();
        } //if
    }//doClickFuncSelect

//################# 功能块2 ####################
    //定义活动之间数据的传递类，主要针对功能列表，运用背景为 点击按钮出现功能列表页，以及 点击列表项，进入不同的详细功能页
    //定义 item 各项所需的数据的类型,采用 parcelable 接口，以便对象和数组通过intent传递；
    static class ParcelableItem implements Parcelable {
        //定义各行数据所需要的数据
        private int imageId; //图片id
        private String name; //子项中功能名称
        private String[] funcParams; //子项中标记 功能类型的字符串数组，第一项是type标记，后面可选，可用以区分进一步功能页面的加载内容模板等信息
    /////////////////////////////

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
        public static final Parcelable.Creator<mCom.ParcelableItem> CREATOR = new Creator<mCom.ParcelableItem>() {
            @Override
            public mCom.ParcelableItem createFromParcel(Parcel source) {
                return new mCom.ParcelableItem(source);  //定义对象的读取建立方式，即，将数据流中数据构造实例
            }

            @Override  //此序列化的读法，适用于array list 等，内部实现就是这样的。此处我们前后文都用array是为了提高性能
            public mCom.ParcelableItem[] newArray(int size) {
                return new mCom.ParcelableItem[size];  //定义数据流数组的读取建立方式，将数据流生成 数据数组； 每个元素使用上面对象的实例创建方式；
            }
        };
    }// class ItemData


//################# 功能块3 ####################
//定义次活动所调用recyclerView的通用基础 adapter ; 主要适用于各种  数组array 或 [] 数据，
//由于所需要的数据 以及 布局 以及 替换方法和动作需要改变，布局可以作为id传入，数据需要自定义类型，
// 替换方法和动作通过写入 继承于  使用自定义类型的泛类adapter的 子类的方法实现上，来实现
    //定义 通用comAdapter ; 基于ViewHolder，内有抽象方法需要实现，且使用泛类
    static abstract public class comAdapter< T > extends RecyclerView.Adapter<ViewHolder>{
        //属性
        private T[] mItemList;  //明确使用的数据, 根据实际类型来
        private int itemLayoutId;  //明确使用的子项布局id
        private int holderInitCount = 0; //纪录创建顺序 序号
        /////////////////////////////////////////////////

        //构造函数，明确了所引用的数据和布局，相对于直接调用活动中的属性，相当于便于人阅读了;
        public comAdapter( T[] itemList, int itemLayoutId){
            mItemList = itemList;
            this.itemLayoutId = itemLayoutId;
        }

        //属性读取
        public T[] getItems(){return mItemList;}

    //定义生成view时，需要的方法，包括纪录view中的锚点;
    // view是对应的组件，holder是用此组件生成的holder
        abstract public void setOnCreateViewHolder(ViewHolder holder, View v);

    //定义view展示时，所需做的处理方法
    //holder为对应的holder，position为当前序号，item是当前所需的数据；此处信息有多余，可不全用
        abstract public void setOnBindViewHolder( ViewHolder holder, int position, T item);

        //定义创建适配器中的viewholder实例的方法; 返回实例，供adapter内部调用
        //parent即为调用方，也就是setAdapter的实例，此处应为对应的RecyclerView的布局组件
        @Override   //适配器会根据调用者尺寸，计算出需要的holder的个数，每个holder都保存有一个独立id的视图，滚动就是将不同视图内容更改，锚点基于视图
        public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
            View view = LayoutInflater.from(parent.getContext()).inflate(itemLayoutId, parent, false);  //读取布局文件，生成view组件，不加入；
            ViewHolder holder = new ViewHolder(view, holderInitCount); //申明全局，使得虚拟函数可以调用 //会在每个view第一次出现时候运行。为每一个创键一次
            holderInitCount++; //count从0开始数
            //定义点击动作，此处可避免反复定义； 因为view仔滚动中动态的进入或消失，会不停调用onbindViewholder
            //int posittion = holder.getAdapterPosition(); 无法获取位置;
            setOnCreateViewHolder(holder, view);
            return holder;
        }//onCreateViewHolder

        //重构 单个item进入视野时的执行方法，也就是view在加入视图之前所做的事情
        @Override
        public void onBindViewHolder(ViewHolder holder, int position) {
            T item = mItemList[position]; //取出对应的数据
            setOnBindViewHolder(holder, position, item);
        }//onBindViewHolder

        @Override
        public int getItemCount() {
            return mItemList.length; //此条会反复执行？？？？
        }
    }//class mAdapter
    //定义ViewHolder，用于此处通用的adapter
    static public class ViewHolder extends RecyclerView.ViewHolder{
        private int init_count;
        public ViewHolder(View v, int init_count){
            super(v);
            this.init_count = init_count;
        }
        public int getInitPosition(){return init_count;}
    }

//################# 功能块4 ####################
//定义次活动所调用recyclerView的通用基础 adapter ; 主要适用于各种 List 列表数据，
//由于所需要的数据 以及 布局 以及 替换方法和动作需要改变，布局可以作为id传入，数据需要自定义类型，
// 替换方法和动作通过写入 继承于  使用自定义类型的泛类adapter的 子类的方法实现上，来实现
    //定义 通用comListAdapter ; 基于基于ViewHolder，内有抽象方法需要实现，且使用泛类
    static abstract public class comListAdapter< T > extends RecyclerView.Adapter<ViewHolder>{
        //属性
        private List<T> mItemList;  //明确使用的数据, 根据实际类型来
        private int itemLayoutId;  //明确使用的子项布局id
        private int holderInitCount = 0; //纪录创建顺序 序号
        /////////////////////////////////////////////////

        //构造函数，明确了所引用的数据和布局，相对于直接调用活动中的属性，相当于便于人阅读了;
        public comListAdapter( List<T> itemList, int itemLayoutId){
            mItemList = itemList;
            this.itemLayoutId = itemLayoutId;
        }

        //属性读取
        public List<T> getItems(){return mItemList;}

        //定义生成view时，需要的方法，包括纪录view中的锚点;
        // view是对应的组件，holder是用此组件生成的holder
        abstract public void setOnCreateViewHolder(ViewHolder holder, View v);

        //定义view展示时，所需做的处理方法
        //holder为对应的holder，position为当前序号，item是当前所需的数据；此处信息有多余，可不全用
        abstract public void setOnBindViewHolder( ViewHolder holder, int position, T item);

        //定义创建适配器中的viewholder实例的方法; 返回实例，供adapter内部调用
        //parent即为调用方，也就是setAdapter的实例，此处应为对应的RecyclerView的布局组件
        @Override   //适配器会根据调用者尺寸，计算出需要的holder的个数，每个holder都保存有一个独立id的视图，滚动就是将不同视图内容更改，锚点基于视图
        public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
            View view = LayoutInflater.from(parent.getContext()).inflate(itemLayoutId, parent, false);  //读取布局文件，生成view组件，不加入；
            ViewHolder holder = new ViewHolder(view, holderInitCount); //申明全局，使得虚拟函数可以调用 //会在每个view第一次出现时候运行。为每一个创键一次
            holderInitCount++; //count从0开始数
            //定义点击动作，此处可避免反复定义； 因为view仔滚动中动态的进入或消失，会不停调用onbindViewholder
            //int posittion = holder.getAdapterPosition(); 无法获取位置;
            setOnCreateViewHolder(holder, view);
            return holder;
        }//onCreateViewHolder

        //重构 单个item进入视野时的执行方法，也就是view在加入视图之前所做的事情
        @Override
        public void onBindViewHolder(ViewHolder holder, int position) {
            T item = mItemList.get(position); //取出对应的数据
            setOnBindViewHolder(holder, position, item);
        }//onBindViewHolder

        @Override
        public int getItemCount() {
            return mItemList.size(); //此条会反复执行,每次有数据进出都会执行很多遍，当mItemList一直在增加时候，就有用了。
        }
    }//class mListAdapter

}//end mCom
