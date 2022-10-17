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


def insert_into_es(book_massage_list: list,i: int):
    # helpers.bulk(es, book_massage_list, index='jobbole', doc_type="article", raise_on_error=True)
    es.index(index='jobbole',body=book_massage_list,doc_type="article",id=i)


if __name__ == '__main__':
    for i in range(20):
        print(es.get(index='jobbole', id=i))
