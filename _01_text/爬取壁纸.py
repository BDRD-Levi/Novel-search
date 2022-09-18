import requests
from lxml import etree
import os
import time

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

cookie = {
    'cookie': '__yjs_duid=1_d23f1ec6333334627624630398ce50531656116399443; Hm_lvt_0f461eb489c245a31c209d36e41fcc0f=1656116400; Hm_lpvt_0f461eb489c245a31c209d36e41fcc0f=1656116470; Hm_lvt_c59f2e992a863c2744e1ba985abaea6c=1656116579; zkhanecookieclassrecord=%2C66%2C; Hm_lpvt_c59f2e992a863c2744e1ba985abaea6c=1656116588'
}

num_page = 2  # 每次爬取页数量
page = 'xxx'  # 从第几页开始爬 'xxx'默认使用文本里面的数据
page_address = f'https://pic.netbian.com/4kdongman'  # 分类页面
pic_dir = '../../Project_HeiMa/1.就业班第1阶段/day09/爬虫/source/4kdongman'  # 创建的目录名称


# 得到页的url
def get_page_url(n, m):
    page_url_list = []
    while n <= m:
        if n == 1:
            page_url_list.append(f'{page_address}/index.html')
        else:
            page_url_list.append(f'{page_address}/index_{n}.html')
        # print(n)
        n += 1
    return page_url_list


# 得到全页图片的url
def get_page_allurl(address_list):
    pass
    pic_url_list = []
    for i in address_list:
        res = requests.get(i, headers=headers, cookies=cookie)
        data = etree.HTML(res.text)
        pic_url = data.xpath('//div[@class="slist"]//li/a/@href')
        if pic_url:
            pic_url_list.extend(pic_url)

    pic_url_list2 = []
    for i in pic_url_list:
        i = f'https://pic.netbian.com{i}'
        pic_url_list2.append(i)
    return pic_url_list2


def get_every_picurl(pic_url_list):
    pic_url_list2 = []
    len1 = len(pic_url_list)
    len2 = 0
    for i in pic_url_list:
        res = requests.get(i, headers=headers, cookies=cookie)
        data = etree.HTML(res.text)
        massage = data.xpath('//div[@class="photo-pic"]/a/img/@src')
        # ['/uploads/allimg/220624/001113-16560006736042.jpg']
        if massage:
            pic_url_list2.extend(massage)
            len2 += len(massage)
        print(f'已经获取------>{len2 / len1 * 100 :.2f}%')
    # print(pic_url_list2)
    pic_url_list3 = []
    for i in pic_url_list2:
        pic_url_list3.append(f'https://pic.netbian.com{i}')

    return pic_url_list3


def get_every_pic(every_picurl_list, num):
    num = num
    for i in every_picurl_list:
        res = requests.get(i, headers=headers, cookies=cookie)
        data = res.content
        with open(f'./{pic_dir}/{num}.jpg', 'wb') as f:
            f.write(data)
            print(f'爬取成功----->{num}.jpg>------->{i}')
            num += 1


def get_pic_num():
    try:
        os.mkdir(f'{pic_dir}')
    except:
        print(f'{pic_dir}目录已存在！')
    list1 = os.listdir(f'./{pic_dir}/')
    if not list1:
        list1.append('0.jpg')
    list1.sort(reverse=True)
    list2 = []
    for i in list1:
        i2 = int(i[:-4])
        list2.append(i2)
    list2.sort(reverse=True)
    return list2[0] + 1


def get_page():
    global page
    if page == 'xxx':
        try:
            with open(f'{pic_dir}_page.txt', 'r+', encoding='utf-8') as f:
                n = f.read(1024)
                print(n)
                n = int(n)
                n += 1
                n2 = n + num_page - 1


        except:
            with open(f'{pic_dir}_page.txt', 'w', encoding='utf-8') as f:
                f.write('0')
        else:
            with open(f'{pic_dir}_page.txt', 'w', encoding='utf-8') as f:
                f.write(str(n2))
                print(f'保存界面----->{n2}')
            return n, n2
    else:
        page = int(page)
        with open(f'{pic_dir}_page.txt', 'w', encoding='utf-8') as f:
            f.write(str(page + num_page))
            print(f'已爬取的目录----->{page + num_page}')
        return page, page + num_page


def run():
    # tuple1[0]  num第几章图,
    # tuple1[1]  m - num_page 起始页
    tuple1 = get_errorfile()
    num = get_pic_num()
    n, m = get_page()
    if tuple1:
        if num >= tuple1[0]:
            num = tuple1[0]
            print(f"上次错误文件图片数量-------->{num}")
            n = tuple1[1]
            m = n + num_page
            with open(f'{pic_dir}_page.txt', 'w', encoding='utf-8') as f:
                f.write(str(m))
        else:
            print(f"目录中图片数量-------->{num}")
    address_list = get_page_url(n, m)
    print('页面已获得')
    pic_url_list = get_page_allurl(address_list)
    print('每页url已获得')
    # print(pic_url_list)
    every_picurl_list = get_every_picurl(pic_url_list)
    print('pic_url已获得')
    try:
        get_every_pic(every_picurl_list, num)
    except:
        print('爬虫被发现了---------->保存数据')
        save_error(num, m)
    else:
        print('正常爬取---------->保存数据')
        save_perfect()


def start():
    start_time = time.time()
    while 1:
        try:
            run()
        except:
            pass
        time.sleep(20)
        endtime = time.time()
        Time = start_time - endtime
        if Time > 3600:
            break


# 开始前的num 还是有结束的m - num_page
def save_error(num, m):
    with open(f'{pic_dir}_save_error.txt', 'w', encoding='utf-8') as f:
        tuple1 = (num, m - num_page)
        str1 = str(tuple1)
        f.write(str1)


def save_perfect():
    with open(f'{pic_dir}_save_error.txt', 'w', encoding='utf-8') as f:
        a = tuple()
        a = str(a)
        f.write(a)


def get_errorfile():
    with open(f'{pic_dir}_save_error.txt', 'r', encoding='utf-8') as f:
        tuple1 = eval(f.read())
    return tuple1


if __name__ == '__main__':
    start()
    # run()
