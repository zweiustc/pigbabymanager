package com.ustcerqiu.pigdoc;

import android.graphics.Color;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;

public class NotesActivity extends BaseClass {
    //定义所需的属性
    //由于此处 只需要5个参数：类型，名称，日报数，提醒数，报警数；可以直接列表做。但为清晰，加一个tag标签，方便调用后台用
    private List<ItemData> itemDataList; //保存所需要的列表功能数据


//////////////////////////////////////////////////////////////////////
    //定义所需的条目数据模型
    public static class ItemData {
        //定义各行数据所需要的数据
        private String tag; //用于进一步向后台申请数据时候的标记；
        private String[] datas; //每项所需的5个参数：类型，名称，日报数，提醒数，报警数

        //定义设置属性的构造方法; 给外部数据生成对象实例用
        public ItemData( String tag, String[] datas) {
            this.tag = tag;
            this.datas = datas;
        }
        //定义获取属性值方法
        public String getTag(){return tag;}
        public String[] getDatas(){return datas;}
    }//class ItemData


    //定义adapter，继承通用adapter，实现数据处理
    private class mAdapter extends mCom.comListAdapter<ItemData>{
        //父类中有的参数为 private List<T> mItemList 和 private int itemLayoutId; 也可以用
        //定义需要保留的属性; 需要为每一个子项都保留此数据，adapter只有一个，holder有不少 且和数据条目数不同
        //无法得知是几项，所以使用list
        private List<TextView> itemMarkList = new ArrayList<>(); //必须初始化，在一个adapter实例化时
        private List<TextView> itemNameList = new ArrayList<>(); //
        private List<TextView> itemReportNumList = new ArrayList<>(); //
        private List<TextView> itemReminderNumList = new ArrayList<>(); //
        private List<TextView> itemWarningNumList = new ArrayList<>(); //
        //////////////////////////////////////

        //构造方法
        public mAdapter( List<ItemData> itemList, int itemLayoutId){
            super(itemList, itemLayoutId);
        }

        @Override  //定义创建每个viewholder时候，保存 需要纪录的锚 到 adapter; 与所需调用模板相关
        public void setOnCreateViewHolder(final mCom.ViewHolder holder, View v) {
            TextView itemMark = (TextView) v.findViewById(R.id.note_mark);
            TextView itemName = (TextView) v.findViewById(R.id.note_item_name);
            TextView itemReportNum = (TextView) v.findViewById(R.id.note_report_num);
            TextView itemReminderNum = (TextView) v.findViewById(R.id.note_reminder_num);
            TextView itemWarningNum = (TextView) v.findViewById(R.id.note_warning_num);
            itemMarkList.add(itemMark);
            itemNameList.add(itemName);
            itemReportNumList.add(itemReportNum);
            itemReminderNumList.add(itemReminderNum);
            itemWarningNumList.add(itemWarningNum);
            //TODO 动作
        }// setOnCreatViewHolser

        @Override  //定义单个view展示前，需要的处理，替换锚点内容.positon是总数据数组中位置，item是对应数据，holder会传出对应的创建位置
        public void setOnBindViewHolder(mCom.ViewHolder holder, int position, ItemData item) {
            int viewPosition = holder.getInitPosition();
            String[] dataAr = item.getDatas();
            itemMarkList.get(viewPosition).setText(dataAr[0]);
            itemNameList.get(viewPosition).setText(dataAr[1]);
            //设置完数据，还需要根据数据设置显示style
            TextView itemReportNum = itemReportNumList.get(viewPosition);
            TextView itemReminderNum = itemReminderNumList.get(viewPosition);
            TextView itemWarningNum = itemWarningNumList.get(viewPosition);
            itemReportNum.setText(dataAr[2]);
            itemReminderNum.setText(dataAr[3]);
            itemWarningNum.setText(dataAr[4]);
            //设置格式
            if(Integer.parseInt(dataAr[2]) >0 ){
                itemReportNum.setTextAppearance(itemReportNum.getContext(), R.style.note_report); //api太低
            }else{
                itemReportNum.setTextAppearance(itemReportNum.getContext(), R.style.note_report_zero); //api太低
            }

            if(Integer.parseInt(dataAr[3]) >0 ){
                itemReminderNum.setTextAppearance(itemReminderNum.getContext(), R.style.note_reminder); //api太低
                itemReminderNum.setBackgroundColor(Color.parseColor("#e7f9f215"));
            }else{
                itemReminderNum.setTextAppearance(itemReminderNum.getContext(), R.style.note_reminder_zero); //api太低
                itemReminderNum.setBackgroundColor(Color.parseColor("#00000000"));
            }

            if(Integer.parseInt(dataAr[4]) >0 ){
                itemWarningNum.setTextAppearance(itemWarningNum.getContext(), R.style.note_warning); //api太低
                itemWarningNum.setBackgroundColor(Color.parseColor("#d2ff0000"));
            }else{
                itemWarningNum.setTextAppearance(itemWarningNum.getContext(), R.style.note_warning_zero); //api太低
                itemWarningNum.setBackgroundColor(Color.parseColor("#00000000"));
            }
        }// setOnBindViewHolder
    }// class mAdapter


    //定义获取数据的方法，此处随便搞，后面需改成从网络申请数据
    public List<ItemData> getTheDataList(){
        //TODO 完成获取数据的方法,此方法应该需要成类，然后包含申请的参数，和已经读取到的位置，及此次申请的数目
        //下面为前台测试用代码
        String[] nameAr = {"免疫提醒", "怀孕100到120天产仔", "断奶提醒", "非怀孕状态", "断奶7日配种", "怀孕18到22天查反情"}; //一共6个，最大编号5,取除以5的余数
        String[] typeAr = {"A", "B", "C", "D", "E", "F"}; //6
        List<ItemData> dataList = new ArrayList<>();
        String tag = "tag";
        String[] dataAr ;
        int ty, na, rn, ren, rwn;
        for(int i=0; i<20; i++){
            ty = (int) (Math.random()*5); //随机成成 0~5之间整数
            na = (int) (Math.random()*5); //随机成成 0~5之间整数
            rn = (int) (Math.random()*100); //随机成成 0~20之间整数
            ren = (int) (Math.random()*100); //随机成成 0~1000之间整数
            rwn = (int) (Math.random()*100); //随机成成 0~100之间整数
            dataAr = new String[]{typeAr[ty], nameAr[na], ""+ rn%10 , ""+ren%10, "" +rwn%10 };
            dataList.add( new ItemData(tag, dataAr) );
        }
        return  dataList;
    }// getTheDataList




///##############################################################
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.notes_activity);
        //设置底部导航条的动作
        new SetNavigatorClass().setClickOnNavigator(this, 2);  //this指代最近的类的实例, 2用以标记导航条功能


        //填充内部功能条
        //数据输入全部 点击后的功能列表所需的数据
        //先生成数据列表，并保存
        itemDataList = getTheDataList();



        //调用适配器加入布局中
        RecyclerView recyclerView = (RecyclerView) findViewById(R.id.note_list_RecyclerView);
        LinearLayoutManager layoutManager = new LinearLayoutManager(this);
        layoutManager.setOrientation(LinearLayoutManager.VERTICAL);
        recyclerView.setLayoutManager(layoutManager);
        mAdapter adapter = new mAdapter(itemDataList, R.layout.note_reminder_item);
        recyclerView.setHasFixedSize(true);
        recyclerView.setAdapter(adapter);
        //recyclerView.setAdapter(adapter);  再次设置adapter时候，会将view中清空后，重新填写？？？



    }//onCreate
}//end class
