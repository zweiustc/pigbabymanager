#-*- coding: utf-8 -*-
import xlrd
import sys
import datetime
import MySQLdb

from pyexcel_xls import get_data 



def open_excel(file='file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print str(e)

def read_excel_file(filename):
    data = get_data(filename)
    return data

    print "Get data type:", type(data)
    import uniout
    for sheet_n in data.keys():
        print sheet_n, ":", data[sheet_n]

def insert_base(data):
    print "Get data type:", type(data)
    # 耳标  耳缺    胎龄    出生日期    性别    品种    状态    状态时间    "栋舍号（格式只能为：公猪xx栋、后备xx栋、配怀xx栋、分娩xx栋）"

    for record in data:
        # ignore the title
        if not isinstance(record[0], int):
            continue
        else:
            #print record
            insert_base_record(record)

def insert_base_record(record):
    # record display
    # 耳标  耳缺    胎龄    出生日期    性别    品种    状态    状态时间    "栋舍号（格式只能为：公猪xx栋、后备xx栋、配怀xx栋、分娩xx栋）"
    db = MySQLdb.connect(host='127.0.0.1', user='pig_manage',
            passwd='pig_manage',
            db='pig')
    cursor = db.cursor()

    # indata example: indata = [1, 2, 3, "2013/1/1", 5, 1, "2013/1/1", 1]

    # 1 for type "LY", 6 for unknown 
    if record[5] == u"LY":
        category_id = 1
    else:
        category_id = 6

    # 1 for normal; 2 for 怀孕; 3 for 哺乳 
    if record[6] == u"怀孕":
        state_id = 2
    elif record[6] == u"哺乳":
        state_id = 3
    else: 
        state_id = 1

    print record[8]
    for i in range(0, 10):
        if str(i) in record[8]:
            dormitory_id = i
            break

    indata = [record[0], record[1], record[2], record[3], category_id, state_id, record[7], dormitory_id]

    cmd = 'insert into sow (ear_tag, ear_lack, gestational_age, birthday, category_id, state_id, entryday, dormitory_id) values (%s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(cmd, indata)
    db.commit()

def init_base_type():
    db = MySQLdb.connect(host='127.0.0.1', user='pig_manage',
            passwd='pig_manage', db='pig', charset="utf8")
    cursor = db.cursor()
    cmd = "delete from state"
    cursor.execute(cmd)
    cmd = "delete from category"
    cursor.execute(cmd)
    cmd = "delete from dormitory"
    cursor.execute(cmd)
    db.commit()

    # init category type
    cmd = 'insert into category (id, name) values (1, "LY")'
    cursor.execute(cmd)
    cmd = 'insert into category (id, name) values (6, "others")'
    cursor.execute(cmd)
    db.commit()

    # init state type
    cmd = 'insert into state (id, name) values (1, "正常")'
    cursor.execute(cmd)
    cmd = 'insert into state (id, name) values (2, "怀孕")'
    cursor.execute(cmd)
    cmd = 'insert into state (id, name) values (3, "哺乳")'
    cursor.execute(cmd)
    db.commit()

    # init dormitory type
    for i in range(1, 100):
        reload(sys)
        sys.setdefaultencoding('utf8')
        addr = "分娩舍 %s 栋" % i
        cmd = 'insert into dormitory (id, name) values (%s, "%s")' % (i, addr)
        print cmd
        cursor.execute(cmd)
        db.commit()

if __name__ == "__main__":

    # only run by one time to init base type
    init_base_type()


    # Insert data based on excel files
    filename = './zjpigdata.xls'
    data = read_excel_file(filename)
    
    for sheet_n in data.keys():
        if sheet_n == u"基础信息":
            data_base = data[sheet_n]

    #insert_base(data_base)
