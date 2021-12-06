import pymssql #引入pymssql模块
import pandas as pd
import numpy as np


#sql服务器名，这里(127.0.0.1)是本地数据库IP
myhost = 'DESKTOP-UCESP3S'
serverName = '127.0.0.1'
#登陆用户名和密码
userName = 'sa'
passWord = 'ouc123456'


def conn():
    connect = pymssql.connect(host='localhost',server=r'DESKTOP-UCESP3S', user=userName, password=passWord, database='b_sql',charset='utf8')
    if connect:
        print("连接成功!")
    return connect

if __name__ == "__main__":
    conn = conn()
    cursor = conn.cursor()
    sqlcom = 'select play_num, view_num from years'
    df = pd.read_sql(sqlcom, con=conn) 
    print(df) 
    print(type(df)) #<class'pandas.core.frame.DataFrame'> 
    df1 = np.array(df) #先使用array()將DataFrame轉換一下
    df2 = df1.tolist()#再將轉換後的資料用tolist()轉成列表
    # 轉成列表的資料是這樣的[[123],['213'],['sa']],使用的時候稍注意一下
    print(df2)
    # for i in range(0, len(df2)): 
    #     exist_url = df2[i][0] 
    # ​​​​​​​    print(exist_url)