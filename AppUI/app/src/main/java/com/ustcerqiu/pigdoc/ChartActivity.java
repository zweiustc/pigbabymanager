package com.ustcerqiu.pigdoc;

import android.content.res.Resources;
import android.content.res.TypedArray;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;

public class ChartActivity extends BaseClass {
    //定义所需的属性
    private ItemData[] itemList; //保存所需要的列表功能数据

    //////////////////////////////////////////////////////////////////////
    //定义条列的数据模型
    public static class ItemData {
        //定义各行数据所需要的数据
        private int imageId; //图片id,
        private String name; //子项中功能名称
        private String[] funcParams; //子项中标记 功能类型的字符串数组，第一项是type标记，后面可选，可用以区分进一步功能页面的加载内容模板等信息

        //定义设置属性的构造方法; 给外部数据生成对象实例用
        public ItemData(int imageId, String name, String[] funcParams) {
            this.imageId = imageId;
            this.name = name;
            this.funcParams = funcParams;
        }
        //定义获取属性值方法
        public int getImageId(){return imageId;}
        public String getName(){return name;}
        public String[] getFuncParams(){return funcParams;}
    }//class itemData

    //定义adapter，继承通用adapter，实现数据处理
    private class mAdapter extends mCom.comAdapter<ItemData>{
        //定义需要保留的属性; 需要为每一个子项都保留此数据，adapter只有一个，但每个子项都有一个holder
        //无法得知是第几项，所以使用list
        private List<ImageView> funcImageList = new ArrayList<>(); //需要初始化，才能用方法
        private List<TextView> funcNameList = new ArrayList<>(); //
        //////////////////////////////////////

        //构造方法
        public mAdapter(ItemData[] itemAr, int itemLayoutId){
            super(itemAr, itemLayoutId);
        }

        @Override  //定义创建viewholder时候，保存 需要纪录的锚 到 adapter
        public void setOnCreateViewHolder(final mCom.ViewHolder holder, View v) {  //final成静态变量，方便内部虚拟函数调用
            ImageView funcImage = (ImageView) v.findViewById(R.id.item_image);
            TextView funcName = (TextView) v.findViewById(R.id.item_name);
            funcImageList.add(funcImage);
            funcNameList.add(funcName);
            //TODO 动作
            v.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    int position = holder.getAdapterPosition(); //取得数据所在的位置
                    ItemData item = getItems()[position]; // getItems是adapter的方法，返回自定义数据的数组（mCom.comAdapter)
                    mCom.doClickFuncSelect(v, item.getName(), item.getFuncParams()); //调用通用功能选择，自动分类走出去
                }//onClick
            });
        }

        @Override  //定义单个view展示前，需要的处理，替换锚点内容.positon是总数据数组中位置，item是对应数据，holder会传出对应的创建位置
        public void setOnBindViewHolder(mCom.ViewHolder holder, int position, ItemData item) {
            int viewPosition = holder.getInitPosition();
            funcImageList.get(viewPosition).setImageResource(item.getImageId());
            funcNameList.get(viewPosition).setText(item.getName()); //设置参数，显示第几个，用第几个的参数
            //Log.e("XXXX", viewPosition + " position: "+ position);
        }
    }// class mAdapter




 //##############################################################
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.chart_activity_layout);
        //设置底部导航条的动作
        new SetNavigatorClass().setClickOnNavigator(this, 4);  //this指代最近的类的实例

        //填充内部功能条
        //数据输入全部 点击后的功能列表所需的数据
        //先生成数据列表，并保存
        Resources res = getResources();
        String[] func_names = res.getStringArray(R.array.chart_func_names); //直接调用
        TypedArray imageAr = res.obtainTypedArray(R.array.chart_func_images); //只是获取图片的xml引用方式， 这个用过后需要释放
        String[] funcAr = res.getStringArray(R.array.com_detail_func_types); //功能列表
        int[] indexes = res.getIntArray(R.array.chart_func_indexes);  //功能列表选择
        int func_length = func_names.length;
        String[][] itemFuncParamAr = {  //数据列表中，功能参数的设定，type由xml中设定好了，直接引用
                {funcAr[indexes[0]]}, {funcAr[indexes[1]]}, {funcAr[indexes[2]]}, {funcAr[indexes[3]]}, {funcAr[indexes[4]]},
                {funcAr[indexes[5]]}, {funcAr[indexes[6]]}, {funcAr[indexes[7]]}, {funcAr[indexes[8]]}, {funcAr[indexes[9]]},
                {funcAr[indexes[10]]}, {funcAr[indexes[11]]}, {funcAr[indexes[12]]}, {funcAr[indexes[13]]}, {funcAr[indexes[14]]}
        };
        itemList = new ItemData[func_length]; //定义指针
        for(int i=0; i<func_length; i++){  //创建功能列表所需的数据列表
            itemList[i] = new ItemData( imageAr.getResourceId(i,0), func_names[i], itemFuncParamAr[i] );
        }//for
        imageAr.recycle(); //回收资源读取

        //调用适配器加入布局中
        RecyclerView recyclerView = (RecyclerView) findViewById(R.id.chart_list_RecyclerView);
        LinearLayoutManager layoutManager = new LinearLayoutManager(this);
        layoutManager.setOrientation(LinearLayoutManager.VERTICAL);
        recyclerView.setLayoutManager(layoutManager);
        mAdapter adapter = new mAdapter(itemList, R.layout.func_item_layout);
        recyclerView.setHasFixedSize(true);
        recyclerView.setAdapter(adapter);
        //recyclerView.setAdapter(adapter);  再次设置adapter时候，会将view中清空后，重新填写？？？




    }
}
