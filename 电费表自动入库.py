# coding:utf-8
# import pymysql
from datetime import datetime
import time
import os
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus as urlquote

def shujuku( file):
    print('1、正在读取数据源')
    df = pd.read_excel(file)  # 读取excel
    print('2、完成数据源读取')

    # 读取数据库，判断若不存在该账期月度的表，则创建表结构
    print('3、正在入数据库')
    # db = pymysql.connect(host='10.17.94.17', port=3333, user='zzdb', passwd='A,zzdb123!@#', db='reward', charset='utf8')  # 打开数据库连接
    # cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    table_1 = 'temp_db_zg'   # PPT结论_202209  市级业务账单审核列账查询_201212
    #判断若不存在该表，则创建表结构
    # sql_1 = 'CREATE TABLE IF NOT EXISTS ' +  table_1 + '(data_month	int	,item_id	int	,fp_id	numeric(12)	,fp_nbr	numeric(12)	,fee_cb	numeric(16)	,fee_fax	numeric(16)	,create_date	date	,sup_name	varchar(100)	,sup_name2	varchar(100)	,cust_nbr	varchar(100)	,jld_nbr	varchar(100)	,yd_code	varchar(100)	,yd_name	varchar(100)	,is_gw	varchar(100)	,db_nbr	varchar(100)	,uprice	numeric(12,4)	,uprice2	numeric(12,4)	,note	varchar(100)	,db_nbr2	varchar(100)	,subst_name_bz	varchar(100)	,fee	numeric(12,4)	,fee_fax2	numeric(12,4)	,addr_db	varchar(300)	,db_code	varchar(100)	,cust_type	varchar(100)	,elec_type	varchar(100)	,month_id	int	,last_day	date	,this_day	date	,this_num	numeric(12,4)	,last_num	numeric(12,4)	,db_mult	numeric(10)	,dl_yg	numeric(16)	,dl_share1	numeric(12)	,dl_share2	numeric(12)	,dl_share3	numeric(12)	,dl_son	numeric(12)	,dl_ps	numeric(12)	,dl_loss	numeric(12,4)	,dl_sum	numeric(16,2)	,price	numeric(12,4)	,fee_wy	numeric(10)	,cust_name	varchar(300)	,vat_nbr	varchar(100)	,vat_code	varchar(100)	,vat_bank	varchar(300)	,acc_nbr	varchar(100)	,addr_cust	varchar(300)	,acct_jf	varchar(100)	,fp_type	varchar(100)	,fp_sc	varchar(100)	,cd_mode	varchar(100)	,jf_type	varchar(100)	,acct_code	varchar(100)	,cust_name2	varchar(300)	,js_code	varchar(100)	,note1	varchar(100));'
    # cursor.execute(sql_1)
    # db.commit()  # 若对数据库进行了修改，需进行提交之后再关闭
    # cursor.close()  # 使用完成之后需关闭游标和数据库连接，减少资源占用,cursor.close(),db.close()
    # db.close()
    df.columns = ['data_month', 'item_id', 'fp_id', 'fp_nbr', 'fee_cb', 'fee_fax', 'create_date', 'sup_name', 'sup_name2', 'cust_nbr', 'jld_nbr', 'yd_code', 'yd_name', 'is_gw', 'db_nbr', 'uprice', 'uprice2', 'note', 'db_nbr2', 'subst_name_bz', 'fee', 'fee_fax2', 'addr_db', 'db_code', 'cust_type', 'elec_type', 'month_id', 'last_day', 'this_day', 'this_num', 'last_num', 'db_mult', 'dl_yg', 'dl_share1', 'dl_share2', 'dl_share3', 'dl_son', 'dl_ps', 'dl_loss', 'dl_sum', 'price', 'fee_wy', 'cust_name', 'vat_nbr', 'vat_code', 'vat_bank', 'acc_nbr', 'addr_cust', 'acct_jf', 'fp_type', 'fp_sc', 'cd_mode', 'jf_type', 'acct_code', 'cust_name2', 'js_code', 'note1']

    host, port, user, password, db, tb  = '10.17.94.17', '3333', "zzdb", "A,zzdb123!@#", "reward",  table_1
    engine =create_engine( f'mysql+pymysql://{user}:{urlquote(password)}@{host}:{port}/{db}?charset=utf8')  # 密码中包含特殊字符，如@等，所以密码中有特殊字符需要转码，否则在拼接时会认为是密码和IP地址拼接的@字符，为了避免特殊字符的影响，采用urlquote(特殊字符)解决问题
    conn = engine.connect()

    try:
        time.sleep(0.1)
        df.to_sql(tb, con=conn, if_exists='append' , index = False)   # index = False： 忽略读取dataframe的index
    except Exception as e:
        try:
            print('数据库连接超时0.1秒')
            conn = engine.connect()
            time.sleep(5)
            df.to_sql(tb, con=conn, if_exists='append' , index = False)
        except Exception as e:
            print('数据库连接超时15秒')
            conn = engine.connect()
            time.sleep(10)
            df.to_sql(tb, con=conn, if_exists='append' , index = False)
            print('数据库连接用时65秒')
    conn.close()
    print('4、成功入库')

def log(logg):
    # 在同目录下，需要提前创建一个D.txt文件
    D_file = open('运行日志.txt', mode='a')  # 打开日志文档
    log_value = logg
    now = datetime.now()
    # 将当前时间（字符串）赋值
    now_time = now.strftime("%Y-%m-%d %H:%M:%S")
    # 将当前时间和出入来的logg的数据合并成一条并赋值
    time_values = now_time + '\t' + '\t' + log_value + '\n'
    # 将合并后的数据填写到txt
    D_file.write(time_values)
    D_file.close()  # 关闭日志文档

if __name__ == '__main__':
    # 报错：1、"Incorrect date value: '44866' for column 'last_day' at row 49"
    path = r'D:/work/日常/培训/大数据/项目/电费表自动入库/'  #D:\work\日常\培训\大数据\项目\电费表自动入库
    os.chdir(path)  # 切换到目录  path
    file = '2023年1月电费托收清单.xlsx'

    shujuku(file)  #数据入库

    log('运行成功')  # 运行日志
