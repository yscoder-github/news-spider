# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import time 
class QutoutiaoPipeline(object):

    def __init__(self):
        
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.qutoutiao_db = self.client.qutoutiao_db
        self.qutoutiao_db.news_brief_collect.create_index([("news_id", pymongo.DESCENDING)],
                                                    unique=True, background=True, name='idx_id_col_news_id')
        self.qutoutiao_db.news_brief_collect.create_index([("ctime", pymongo.DESCENDING)], name='idx_ctime')
        self.qutoutiao_db.news_detail.create_index([("news_id", pymongo.DESCENDING)], name='idx_col_news_id')

    def process_item(self, item, spider):
        news_detail = {"news_id": item["news_id"],
                            "detail": item['detail'],
                            "ctime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                            "mtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
                        }
        self.qutoutiao_db.news_detail.insert(news_detail)
        del(item['detail'])
        self.qutoutiao_db.news_brief_collect.insert(dict(item))
        return item
