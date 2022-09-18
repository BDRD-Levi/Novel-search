"""
PROJECT_NAME: Project_scrapy -> test2 ;
FILE_NAME: test2 ;
AUTHOR: hoce ;
WORK_NUMBER: 8088
E_MAIL: 879620357@qq.com
DATE: 2022/9/17 ;
PRODUCT_NAME: PyCharm ;
"""

from elasticsearch import Elasticsearch,  helpers

es = Elasticsearch(
    hosts={'192.168.88.161:9200'},  # 地址
    timeout=3600  # 超时时间
)

# 创建数据库
# es.indices.create("index_name")


def insert_into_es(book_massage_list: list):
    # helpers.bulk(es, book_massage_list, index='jobbole', doc_type="article", raise_on_error=True)
    es.index(index='jobbole',body=book_massage_list,doc_type="article",id=2)
    # 只能用一次
    # res = es.get(index='jobbole', id=2)
    # print(res)

if __name__ == '__main__':
    # insert_into_es()
    filter_path = 'website'
    es.search(index='jobbole',filter_path=filter_path)

    res = es.get(index='jobbole',id=2)
    print(res)
