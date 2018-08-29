# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings

class Scrapyqidian2Pipeline(object):
    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        db_name = settings["MONGODB_DBNAME"]
        client = pymongo.MongoClient(host = host, port = port)
        tdb = client[db_name]#连接数据库
        self.post = tdb[settings["MONGODB_DOCNAME"]]#创建集合

    def process_item(self, item, spider):
        bookinfo = dict(item)
        self.post.insert(bookinfo)
        return item
