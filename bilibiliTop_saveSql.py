import requests
from bs4 import BeautifulSoup
import xlwt
import time
import urllib3
import requests
import json
from openpyxl import Workbook
import csv
import pymssql  # 引入pymssql模块

# 爬取B站热榜排行
# 格式解析，[0-当前排名，1-视频标题，2-播放数目，3-弹幕数量，4-综合得分，5-作者，6-视频地址，7-时长，8-评论数，9-收藏数，10-投币数，11-分享数，12-点赞数]

# 格式化


def whitespace(st):
    st = st.replace('\n', '')
    st = st.strip()
    st = st.replace(' ', '')
    return st


# 详情页
def info_Page(bv):
    url = 'http://api.bilibili.com/x/web-interface/view?bvid=' + bv
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    }  # 请求头，模拟浏览器的运行
    urllib3.disable_warnings()  # 从urllib3中消除警告
    response = requests.get(url, headers=headers)
    content = json.loads(response.text)
    # 很迷，获取到的是str字符串 需要解析成json数据
    statue_code = content.get('code')  # print(statue_code)
    if statue_code == 0:
        duration = content['data']['duration']  # 时长
        reply = content['data']['stat']['reply']  # 评论
        favorite = content['data']['stat']['favorite']  # 收藏
        coin = content['data']['stat']['coin']  # 投币
        share = content['data']['stat']['share']  # 分享
        like = content['data']['stat']['like']  # 点赞

    return duration, reply, favorite, coin, share, like


def conn():
    connect = pymssql.connect(host='localhost', server=r'DESKTOP-UCESP3S',
                              user=userName, password=passWord, database='b_sql', charset='utf8')
    if connect:
        print("连接成功!")
    return connect


def insert_sqlserver(data):
    data = tuple(data)
    cursor.executemany(
        "insert into years(rank_num,title,play_num,view_num,scores,author,href,duration,reply,favorite,coin,share,great) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data
    )
    conn.commit()


# sql服务器名，这里(127.0.0.1)是本地数据库IP
myhost = 'DESKTOP-UCESP3S'
serverName = '127.0.0.1'
# 登陆用户名和密码
userName = 'sa'
passWord = 'ouc123456'

if __name__ == '__main__':
    conn = conn()
    cursor = conn.cursor()
    # 创建数据表id设为主键自增
    cursor.execute("""
    if object_id('years','U') is not null
        drop table years
    create table years(
        rank_num varchar(500),
        title varchar(500),
        play_num float,
        view_num float,
        scores int,
        author varchar(500),
        href varchar(500),
        duration int,
        reply int,
        favorite int,
        coin int,
        share int,
        great int
    )
    """)

    url = 'https://www.bilibili.com/v/popular/rank/all'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

    rank = requests.get(url, headers=headers)  # 请求页面
    soup = BeautifulSoup(rank.text, 'lxml')
    all_rank = soup.find_all('li', class_='rank-item')

    num = 0
    lst = []
    for i in all_rank:
        record = []
        rank_num = i.find('div', class_='num').text  # 获取排名

        info = i.find('div', class_='info')  # 筛选出视频详细信息的标签
        href = info.find('a', class_='title').attrs['href']  # 获取链接
        title = info.find('a', class_='title').text  # 获取标题

        play_num = info.find(
                'i', class_='b-icon play').parent.text  # 获取播放量
        view_num = info.find(
                'i', class_='b-icon view').parent.text  # 获取弹幕数
        author = info.find(
                'i', class_='b-icon author').parent.text  # 获取作者名
        scores = int(info.find('div', class_='pts').find('div').text)  # 获取综合得分
            # 播放，弹幕，作者
        play_num = whitespace(play_num)
        play_num = float(play_num.strip("万"))*10000
        view_num = whitespace(view_num)
        view_num = float(view_num.strip("万"))*10000
        author = whitespace(author)

        bv = href.split('/')[-1]
        duration, reply, favorite, coin, share, like = info_Page(bv)
        duration, reply, favorite, coin, share, like = int(duration), int(reply), int(favorite), int(coin), int(share), int(like)

        record.append(rank_num)
        record.append(title)
        record.append(play_num)
        record.append(view_num)
        record.append(scores)
        record.append(author)
        record.append(href)

        record.append(duration)
        record.append(reply)
        record.append(favorite)
        record.append(coin)
        record.append(share)
        record.append(like)
        num += 1
        lst.append(record)
    print("记录完毕！")

# 写入数据库
    data_tuple = []
    for i in lst:
        i = tuple(i)
        data_tuple.append(i)
    insert_sqlserver(data_tuple)
    conn.commit()
    cursor.close()
    conn.close()
    print("写入完毕！")
