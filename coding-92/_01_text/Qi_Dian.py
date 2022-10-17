"""
PROJECT_NAME: Project_scrapy -> Qi_Dian ;
FILE_NAME: Qi_Dian ;
AUTHOR: hoce ;
WORK_NUMBER: 8088
E_MAIL: 879620357@qq.com
DATE: 2022/9/15 ;
PRODUCT_NAME: PyCharm ;
"""
import requests
from lxml import etree, html
from html.parser import HTMLParser
import os
import time
import pymysql



headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

cookie = {
    'cookie': '__yjs_duid=1_d23f1ec6333334627624630398ce50531656116399443; Hm_lvt_0f461eb489c245a31c209d36e41fcc0f=1656116400; Hm_lpvt_0f461eb489c245a31c209d36e41fcc0f=1656116470; Hm_lvt_c59f2e992a863c2744e1ba985abaea6c=1656116579; zkhanecookieclassrecord=%2C66%2C; Hm_lpvt_c59f2e992a863c2744e1ba985abaea6c=1656116588'
}

address = 'https://www.qidian.com/finish/'

res = requests.get(address, headers=headers, cookies=cookie)
data = etree.HTML(res.text)


def get_book_onepage_massage():
    # 来源网址名称
    website = data.xpath('//a[@class="act"][@data-eid="qd_A01"]/text()')
    # print(website)

    # 来源网址书名
    book_name = data.xpath('//ul[@class="all-img-list cf"]//h2//a/text()')
    # print(book_name)
    # print(len(book_name))

    # 来源网址书作者
    writer = data.xpath(
        '//div[@class="book-mid-info"]//p[@class="author"]//a[@class="name" and @data-eid and @target="_blank"]/text()')
    # print(writer)
    # print(len(writer))

    # 书本链接并拼接https
    book_name_url = data.xpath('//h2//a/@href')
    book_name_url_http = []
    for i in book_name_url:
        book_name_url_http.append('https:' + i)
    # print(book_name_url_http)
    # print(len(book_name_url_http))

    # 来源网址书种类
    book_kind = data.xpath('//p[@class="author"]/a[@data-eid="qd_B60"]/text()')
    # print(book_kind)
    # print(len(book_kind))

    # 来源网址书状态
    book_status = data.xpath('//p[@class="author"]//span/text()')
    # print(book_status)
    # print(len(book_status))

    # 来源网址书简介
    book_introduce = data.xpath('//div[@class="book-mid-info"]//p[@class="intro"]/text()')
    # print(book_introduce)
    # print(len(book_introduce))

    # 钉装一本书
    book_massage = []
    for i in range(0, len(book_name)):
        one_book = {'website': website[0], 'book_name': book_name[i], 'writer': writer[i], 'book_name_url_http': book_name_url_http[i], 'book_kind': book_kind[i], 'book_status': book_status[i], 'book_introduce': book_introduce[i]}
        book_massage.append(one_book)
    # print(book_massage)
    # print(len(book_massage))
    return book_massage


def create_database_and_table():
    # 数据和数据表不存在的时候创建
    conn = pymysql.connect(host='192.168.88.161', user='root', password='123456', port=3306)
    cur = conn.cursor()
    cur.execute("""create database if not exists books default charset=utf8;""");
    cur.execute("""
        create table if not exists books.book_name_massage (
            id int primary key auto_increment,
            website varchar(255),
            book_name  varchar(255),
            writer  varchar(255),
            book_name_url_http  varchar(255),
            book_kind  varchar(255),
            book_status  varchar(255),
            book_introduce  varchar(255),
            in_time time
        )engine=innodb charset =utf8;
    """)
    conn.commit()
    conn.close()



def get_into_time():
    # 得到当前时间 格式为 yyyy-MM-dd HH:mm:ss
    the_time = str(time.asctime())
    year = the_time[20:24]
    month = the_time[4:7]
    if month == 'Jan':
        month = "01"
    elif month == 'Feb':
        month = "02"
    elif month == 'Mar':
        month = "03"
    elif month == 'Apr':
        month = "04"
    elif month == 'May':
        month = "05"
    elif month == 'Jun':
        month = "06"
    elif month == 'Jul':
        month = "07"
    elif month == 'Aug':
        month = "08"
    elif month == 'Sep':
        month = "09"
    elif month == 'Oct':
        month = "10"
    elif month == 'Nov':
        month = "11"
    elif month == 'Dec':
        month = "12"
    day = the_time[8:10]
    into_time = the_time[11:19]
    # 处理后的当前时间
    into_time1 = f'{year}-{month}-{day} {into_time}'
    return into_time1


def to_mysql(book_one_page_massage):
    # 爬取书名以及相关信息
    conn = pymysql.connect(host='192.168.88.161', user='root', password='123456', port=3306, database='books',
                           charset='utf8')
    cur = conn.cursor()
    in_time1 = get_into_time()
    for i in book_one_page_massage:
        website1 = i['website']
        book_name1 = i['book_name']
        writer1 = i['writer']
        book_name_url_http1 = i['book_name_url_http']
        book_kind1 = i['book_kind']
        book_status1 = i['book_status']
        book_introduce1 = i['book_introduce']


        # 测试 写入文件 、查看数据大小
        # print([website1, book_name1, writer1, book_name_url_http1, book_kind1, book_status1, book_introduce1, in_time1])
        data = str([website1, book_name1, writer1, book_name_url_http1, book_kind1, book_status1, book_introduce1, in_time1])+'\n'
        with open('./book.json', 'w', encoding='utf-8') as a:
            print(data)
            a.write(data)
            a.close()

        # 插入数据
        # sql = f"""insert into books.book_name_massage
        #             (website, book_name, writer, book_name_url_http, book_kind, book_status, book_introduce, in_time)
        #             values
        #             ('{website1}','{book_name1}','{writer1}','{book_name_url_http1}','{book_kind1}','{book_status1}','{book_introduce1}','{in_time1}');"""
        # # 测试
        # # print(sql)
        # cur.execute(sql)


    conn.commit()
    conn.close()


if __name__ == '__main__':
    # 爬取数据
    book_one_page_massage = get_book_onepage_massage()
    create_database_and_table()
    to_mysql(book_one_page_massage )
