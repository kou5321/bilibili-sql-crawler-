import pymssql #引入pymssql模块


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

def insert_sqlserver(data):
    data = tuple(data)
    cursor.executemany(
        "insert into years(title,descs,href,postDesc) VALUES(%s,%s,%s,%s)",data
    )
    conn.commit()

# 爬取数据的函数
# def get_all():
    # try:
    #     res = requests.get(url,headers=headers)
    #     response = etree.HTML(res.text)
    #     titles = response.xpath('//a[@class="postTitle2"]/text()')
    #     descs = response.xpath('//div[@class="c_b_p_desc"]/text()')
    #     hrefs = response.xpath('//a[@class="c_b_p_desc_readmore"]/@href')
    #     postdescs = response.xpath('//div[@class="postDesc"]/text()')
        # data = []
        # for title,desc,href,postdesc in zip(titles,descs,hrefs,postdescs):
        #     # 追加要使用小括号，不能使用中括号，sql server提示只接受元组类型
        #     data.append((title.strip(),desc.strip(),href.strip(),postdesc.strip()))
        # if not data:
        #     return None
        # print(data)
    # data = [['1', '余景天粉丝：“他们只是失去了生命，我哥哥失去的可是出道机会”？？', '540.8万', '7.8万', '6559767', '郭云神奇',
    #    '//www.bilibili.com/video/BV1MU4y1t7mD', '524', '42463', '131031', '476923', '55942', '692308'],
    #    ['2','好兄弟是什么，能吃吗？','356.8万','3.2万','3695675','老番茄','//www.bilibili.com/video/BV1Bi4y1o7uj','836','8170','60561','148889','7862','372444',]]
    # data = [['python增删查改','摘要：pip install redis','www.baidu.com','ok'], ['lalal','hhh','link','6666']]
    # insert_sqlserver(data)
    #     return True
    # except Exception as e:
    #     print(e)



if __name__ == '__main__':
    conn = conn()
    cursor = conn.cursor()
    # 创建数据表id设为主键自增
    cursor.execute("""
    if object_id('years','U') is not null
        drop table years
    create table years(
        id int not null primary key IDENTITY(1,1),
        title varchar(500),
        descs varchar(500),
        href varchar(500),
        postDesc varchar(500)
    )
    """)
    data_list = [['python增删查改','摘要：pip install redis','www.baidu.com','ok'], ['lalal','hhh','link','6666']]
    data_tuple=[]
    for i in data_list:
        i = tuple(i)
        data_tuple.append(i)
    insert_sqlserver(data_tuple)
    conn.commit()
    cursor.close()
    conn.close() 
