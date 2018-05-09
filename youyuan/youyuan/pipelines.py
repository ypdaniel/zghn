# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json, pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

class YouyuanPipeline(object):
    def __init__(self):
        self.filename = open("youyuan.json", "w")

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.filename.write(content)
        return item

    def close_spider(self, spider):
        self.filename.close()

class MongoDBPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        self.db = self.client[settings['MONGODB_DB']]
        self.collection = self.db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        data = [{
            'username': item['username'],
            'age': item['age'],
            'images_url': item['images_url'],
            'content': item['content'],
            'birthplace': item['birthplace'],
            'education': item['education'],
            'income': item['income'],
            'hobby': item['hobby'],
            'source_url': item['source_url'],
            'source': item['source'],
        }]

        self.collection.insert(data)
        log.msg('Item wrote to MongoDB database %s/%s' % (settings['MONGODB_DB'], settings['MONGODB_COLLECTION']), spider=spider)

        return item

    def close_spider(self, spider):
        self.client.close()